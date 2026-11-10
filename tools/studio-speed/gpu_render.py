"""GPU render driver for the Cape Jones studio pipeline.

Speed without quality loss (owner directive 2026-10-24 22:10 CDT):
  1. Cycles on GPU (Kaggle main, Colab T4 second, local CPU fallback only).
  2. Adaptive sampling: noise threshold stops clean tiles early, hard tiles
     get the samples they need. Fewer wasted samples, same final quality.
  3. Denoise: OptiX on NVIDIA GPU, OpenImageDenoise otherwise. Denoise
     lets a lower sample count finish clean — it is a quality tool, not a
     blur pass, when paired with adaptive sampling.
  4. Persistent data + spatial splits off for animation (avoids re-upload
     per frame on GPU).
  5. Camera: auto_camera.fit_camera (bbox-measured, framing self-checked).
     NEVER a hand-set camera distance/target.

Usage (on a GPU machine with Blender 4.2):
  blender --background scene.blend --python gpu_render.py -- \
    --subject CapeJones_Body --frames 1-48 --fps 12 --out /tmp/frames \
    --lens 35 --orbit 30
  --orbit N: slow orbit of N degrees across the frame range (0 = static).
  Render at 12fps, then interpolate.py doubles to 24fps with RIFE — half
  the frames rendered, smoother motion than FFmpeg minterpolate alone.

Local CPU fallback: --device CPU. Expect ~4 min/frame at 480x270 32spp
on this VM's 2 vCPU — that is why video goes to GPU, not local.
"""
import bpy, math, mathutils as mu, sys, argparse, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from auto_camera import fit_camera, subject_bbox, make_camera, check_framing

ap = argparse.ArgumentParser()
ap.add_argument("--subject", default="CapeJones_Body")
ap.add_argument("--frames", default="1-48")
ap.add_argument("--fps", type=int, default=12)
ap.add_argument("--out", default="/tmp/frames")
ap.add_argument("--lens", type=float, default=35)
ap.add_argument("--margin", type=float, default=0.15)
ap.add_argument("--orbit", type=float, default=0.0)
ap.add_argument("--device", default="GPU")
ap.add_argument("--samples", type=int, default=128)
ap.add_argument("--resolution", default="1280x720")
a = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])

sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.samples = a.samples
sc.cycles.use_adaptive_sampling = True
sc.cycles.adaptive_threshold = 0.01
sc.cycles.use_persistent_data = True
prefs = bpy.context.preferences
cprefs = prefs.addons['cycles'].preferences
if a.device == "GPU":
    cprefs.compute_device_type = 'CUDA'
    for dev in cprefs.devices:
        dev.use = True
    sc.cycles.device = 'GPU'
    # OptiX denoise on NVIDIA GPU, OIDN otherwise (set at render time)
    sc.cycles.denoiser = 'OPTIX'
else:
    sc.cycles.device = 'CPU'
    sc.cycles.denoiser = 'OPENIMAGEDENOISE'
sc.cycles.use_denoising = True
w, h = a.resolution.split('x')
sc.render.resolution_x, sc.render.resolution_y = int(w), int(h)
sc.render.fps = a.fps
f0, f1 = a.frames.split('-')
sc.frame_start, sc.frame_end = int(f0), int(f1)
sc.render.image_settings.file_format = 'PNG'
os.makedirs(a.out, exist_ok=True)

bbox = subject_bbox([a.subject])
loc, target, dist = fit_camera(bbox, lens=a.lens, margin=a.margin)
cam = make_camera("GpuCam", loc, target, a.lens)
sc.camera = cam
bpy.context.view_layer.update()
ok, rng = check_framing(cam, bbox)
print("GPU_RENDER framing", "PASS" if ok else "FAIL", rng)
if not ok:
    raise SystemExit("GPU_RENDER refused: framing check failed, fix before spending GPU time")
# Orbit: rotate camera location around the target's Z axis across frames
if a.orbit:
    for f in range(sc.frame_start, sc.frame_end + 1):
        t = (f - sc.frame_start) / max(sc.frame_end - sc.frame_start, 1)
        ang = math.radians(a.orbit * t)
        rel = loc - mu.Vector(target)
        rot = mu.Matrix.Rotation(ang, 4, 'Z')
        cloc = mu.Vector(target) + rot @ rel
        cam.location = cloc
        cam.rotation_euler = (mu.Vector(target) - cloc).to_track_quat('-Z', 'Y').to_euler()
        cam.keyframe_insert(data_path="location", frame=f)
        cam.keyframe_insert(data_path="rotation_euler", frame=f)
    cam.location = loc
    cam.rotation_euler = (mu.Vector(target) - loc).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = os.path.join(a.out, "frame_####")
bpy.ops.render.render(animation=True)
print("GPU_RENDER done", a.out)
