"""Cape Jones v5 dance render: frames from scene_v5.blend, resumable.
Run: blender -b scene_v5.blend --python render_v5.py -- <frames_dir> <FS> <FE>
Frames already on disk with size > 20000 bytes are skipped (resume-safe).
Each rendered frame is size-verified; failures are retried once.
"""
import bpy, os, sys

argv = sys.argv[sys.argv.index("--") + 1:]
FRAMES_DIR, FS, FE = argv[0], int(argv[1]), int(argv[2])
os.makedirs(FRAMES_DIR, exist_ok=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE"
sc.eevee.taa_render_samples = 8
sc.render.resolution_x, sc.render.resolution_y = 960, 540
sc.render.image_settings.file_format = "PNG"
sc.render.fps = 24

def ok(path):
    return os.path.exists(path) and os.path.getsize(path) > 20000

done = skipped = 0
for f in range(FS, FE + 1):
    out = os.path.join(FRAMES_DIR, f"f{f:04d}.png")
    if ok(out):
        skipped += 1
        continue
    sc.frame_set(f)
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)
    if not ok(out):
        bpy.ops.render.render(write_still=True)
    if ok(out):
        done += 1
    else:
        print("FRAME_FAIL", f, flush=True)
    if f % 60 == 0:
        print(f"RENDER_PROGRESS {f} done={done} skipped={skipped}", flush=True)
print(f"RENDER_CHUNK_DONE {FS}-{FE} done={done} skipped={skipped}")
