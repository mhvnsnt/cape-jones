"""Cape Jones dance proof 3D v4 - STAGE C: render from scene_v4.blend.

Modes:
  check            low-res verification stills (loop phases + lighting sections)
  stills           full-res 960x540 PNG stills: front extremes, back views,
                   back hem zoom, shoulder zoom, hand zoom - zoom-check sources
  loop             frames 1..96 at 480x270 into loop/ (movement-spec check)
  frames FS FE     JPEG sequence frames FS..FE into frames/ (skips existing)
Run via blender_render.sh (EGL surfaceless):
  blender -b scene_v4.blend --python render_v4.py -- <mode> [FS FE]
"""
import bpy, math, os, sys, time

WORK = "/home/hatch/workspace/_cj_v4_build"
argv = sys.argv[sys.argv.index("--") + 1:]
MODE = argv[0] if argv else "check"
sc = bpy.context.scene
t00 = time.time()
def log(*a):
    print("[stageC]", *a, round(time.time() - t00, 1), "s", flush=True)

def landed(path):
    try:
        sz = os.path.getsize(path)
        if path.endswith(".jpg"):
            if sz <= 10000:
                return False
            with open(path, "rb") as fh:
                fh.seek(-2, 2)
                return fh.read(2) == b"\xff\xd9"
        if sz <= 5000:
            return False
        with open(path, "rb") as fh:
            return fh.read(4) == b"\x89PNG"
    except Exception:
        return False

def render_to(path, frame):
    for i, wait in enumerate((0, 3, 8, 20, 45, 90)):
        if wait:
            time.sleep(wait)
        try:
            sc.frame_set(frame)
            sc.render.filepath = path
            bpy.ops.render.render(write_still=True)
        except Exception as e:
            log("render failed", path, e, "attempt", i)
            continue
        time.sleep(1)
        if landed(path):
            return True
        log("save did not land", path, "attempt", i)
    return False

from mathutils import Vector
def look_at(cam, loc, target):
    cam.location = loc
    d = Vector(target) - Vector(loc)
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()

if MODE == "check":
    OUT = os.path.join(WORK, "check"); os.makedirs(OUT, exist_ok=True)
    sc.render.image_settings.file_format = "PNG"
    sc.render.resolution_x = 640; sc.render.resolution_y = 360
    for f in (5, 25, 49, 73, 93):
        ok = render_to(os.path.join(OUT, f"v4_f{f}.png"), f)
        log("check front", f, ok)
    for f, tag in ((417, "magenta"), (801, "cyan"), (1185, "night"), (1569, "day2")):
        ok = render_to(os.path.join(OUT, f"v4_{tag}{f}.png"), f)
        log("check section", tag, ok)
    print("CHECK_DONE")
elif MODE == "stills":
    OUT = os.path.join(WORK, "stills"); os.makedirs(OUT, exist_ok=True)
    sc.render.image_settings.file_format = "PNG"
    sc.render.resolution_x = 960; sc.render.resolution_y = 540
    for f in (9, 33, 57, 81):
        ok = render_to(os.path.join(OUT, f"s_f{f}.png"), f)
        log("still front", f, ok)
    main_cam = sc.camera
    bpy.ops.object.camera_add()
    bcam = bpy.context.active_object; sc.camera = bcam
    bcam.data.lens = 40
    look_at(bcam, (0, 2.6, 1.35), (0, 0, 0.40))
    for f in (33, 57):
        ok = render_to(os.path.join(OUT, f"s_back{f}.png"), f)
        log("still back", f, ok)
    bcam.data.lens = 55
    look_at(bcam, (0, 0.9, 0.35), (0, 0.08, 0.18))
    ok = render_to(os.path.join(OUT, "s_hem33.png"), 33); log("still hem", ok)
    # shoulder + hand zooms from the front at a high-arm-motion frame
    bcam.data.lens = 85
    look_at(bcam, (0.55, -1.05, 0.95), (0.30, -0.03, 0.74))
    ok = render_to(os.path.join(OUT, "s_shoulder33.png"), 33); log("still shoulder", ok)
    look_at(bcam, (0.75, -0.85, 0.85), (0.47, -0.04, 0.70))
    ok = render_to(os.path.join(OUT, "s_hand33.png"), 33); log("still hand", ok)
    sc.camera = main_cam
    print("STILLS_DONE")
elif MODE == "loop":
    OUT = os.path.join(WORK, "loop"); os.makedirs(OUT, exist_ok=True)
    sc.render.image_settings.file_format = "JPEG"
    sc.render.image_settings.quality = 90
    sc.render.resolution_x = 480; sc.render.resolution_y = 270
    done = 0
    for f in range(1, 97):
        path = os.path.join(OUT, f"f{f:04d}.jpg")
        if os.path.exists(path) and os.path.getsize(path) > 5000:
            done += 1; continue
        if render_to(path, f):
            done += 1
    log("LOOP_DONE ok", done)
    print("LOOP_DONE")
else:
    FS, FE = int(argv[1]), int(argv[2])
    OUT = os.path.join(WORK, "frames"); os.makedirs(OUT, exist_ok=True)
    sc.render.image_settings.file_format = "JPEG"
    sc.render.image_settings.quality = 90
    sc.render.resolution_x = 960; sc.render.resolution_y = 540
    done = 0
    for f in range(FS, FE + 1):
        path = os.path.join(OUT, f"f{f:04d}.jpg")
        if landed(path):
            done += 1; continue
        if render_to(path, f):
            done += 1
    log("FRAMES_DONE", FS, FE, "ok", done)
    print("RENDER_SEQ_DONE")
