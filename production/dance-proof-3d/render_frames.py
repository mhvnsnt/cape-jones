"""Cape Jones dance proof 3D v3 - STAGE B: render from scene_v3.blend.

Modes:
  check            low-res verification stills (front loop phases + one frame
                   per lighting section) + per-frame eval timing
  stills           full-res 960x540 PNG stills: front extremes, back views,
                   back hem zoom - the source frames for zoomed cape crops
  loop             frames 1..48 at 480x270 into loop/ (movement-spec check)
  frames FS FE     JPEG sequence frames FS..FE into frames/ (skips existing)
Run: blender -b scene_v3.blend --python render_frames_v3.py -- <mode> [FS FE]
"""
import bpy, math, os, sys, time

D = math.radians
WORK = "/home/hatch/workspace/_cj-dance3d-v3"
argv = sys.argv[sys.argv.index("--") + 1:]
MODE = argv[0] if argv else "check"
sc = bpy.context.scene
t00 = time.time()
def log(*a):
    print("[stageB]", *a, round(time.time() - t00, 1), "s", flush=True)

def landed(path):
    """True only if the file is on disk, non-trivial, and well-formed.
    The box's storage layer intermittently drops writes (EPERM / 0-byte /
    truncated) under load, so a 'successful' render call is not proof."""
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
    # Retry ladder sized to ride out multi-minute storage-denial windows.
    for i, wait in enumerate((0, 3, 8, 20, 45, 90, 150)):
        if wait:
            time.sleep(wait)
        try:
            sc.frame_set(frame)
            sc.render.filepath = path
            bpy.ops.render.render(write_still=True)
        except Exception as e:
            log("render failed", path, e, "attempt", i)
            continue
        time.sleep(2)  # settle, then verify the bytes actually landed
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
    OUT = os.path.join(WORK, "check")
    os.makedirs(OUT, exist_ok=True)
    body = bpy.data.objects["BodyR"]
    sc.frame_set(1)
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(body.evaluated_get(dg))
    bpy.data.meshes.remove(me)
    for f in (2, 3):
        t0 = time.time()
        sc.frame_set(f)
        dg = bpy.context.evaluated_depsgraph_get()
        me = bpy.data.meshes.new_from_object(body.evaluated_get(dg))
        log("eval frame", f, round(time.time() - t0, 2), "s, verts", len(me.vertices))
        bpy.data.meshes.remove(me)
    sc.render.image_settings.file_format = "PNG"
    sc.render.resolution_x = 640; sc.render.resolution_y = 360
    for f in (5, 9, 21, 33, 39):
        t0 = time.time()
        ok = render_to(os.path.join(OUT, f"v3_f{f}.png"), f)
        log("check front", f, ok, round(time.time() - t0, 1), "s")
    # one frame per lighting section: magenta dip, cyan plant, night dip, day shrug
    for f, tag in ((417, "magenta33"), (777, "cyan9"), (1185, "night33"), (1575, "day39")):
        t0 = time.time()
        ok = render_to(os.path.join(OUT, f"v3_{tag}.png"), f)
        log("check section", tag, ok, round(time.time() - t0, 1), "s")
    main_cam = sc.camera
    bpy.ops.object.camera_add()
    bcam = bpy.context.active_object; bcam.data.lens = 40; sc.camera = bcam
    look_at(bcam, (0, 2.6, 1.35), (0, 0, 0.40))
    for f in (9, 33):
        t0 = time.time()
        ok = render_to(os.path.join(OUT, f"v3_back{f}.png"), f)
        log("check back", f, ok, round(time.time() - t0, 1), "s")
    bcam.data.lens = 55
    look_at(bcam, (0, 0.9, 0.35), (0, 0.08, 0.18))
    ok = render_to(os.path.join(OUT, "v3_hem33.png"), 33)
    log("check hem", ok)
    sc.camera = main_cam
    print("CHECK_DONE")
elif MODE == "stills":
    OUT = os.path.join(WORK, "stills")
    os.makedirs(OUT, exist_ok=True)
    sc.render.image_settings.file_format = "PNG"
    sc.render.resolution_x = 960; sc.render.resolution_y = 540
    for f in (5, 9, 21, 33, 39):
        t0 = time.time()
        ok = render_to(os.path.join(OUT, f"s_f{f}.png"), f)
        log("still front", f, ok, round(time.time() - t0, 1), "s")
    main_cam = sc.camera
    bpy.ops.object.camera_add()
    bcam = bpy.context.active_object; bcam.data.lens = 40; sc.camera = bcam
    look_at(bcam, (0, 2.6, 1.35), (0, 0, 0.40))
    for f in (9, 21, 33):
        t0 = time.time()
        ok = render_to(os.path.join(OUT, f"s_back{f}.png"), f)
        log("still back", f, ok, round(time.time() - t0, 1), "s")
    bcam.data.lens = 55
    look_at(bcam, (0, 0.9, 0.35), (0, 0.08, 0.18))
    ok = render_to(os.path.join(OUT, "s_hem33.png"), 33)
    log("still hem", ok)
    sc.camera = main_cam
    print("STILLS_DONE")
elif MODE == "loop":
    OUT = os.path.join(WORK, "loop")
    os.makedirs(OUT, exist_ok=True)
    sc.render.image_settings.file_format = "JPEG"
    sc.render.image_settings.quality = 90
    sc.render.resolution_x = 480; sc.render.resolution_y = 270
    done = 0
    for f in range(1, 49):
        path = os.path.join(OUT, f"f{f:04d}.jpg")
        if os.path.exists(path) and os.path.getsize(path) > 5000:
            done += 1
            continue
        t0 = time.time()
        ok = render_to(path, f)
        log("loop frame", f, ok, round(time.time() - t0, 1), "s")
        if ok:
            done += 1
    log("LOOP_DONE ok", done)
    print("LOOP_DONE")
else:
    FS = int(argv[1]); FE = int(argv[2])
    OUT = os.path.join(WORK, "frames")
    os.makedirs(OUT, exist_ok=True)
    sc.render.image_settings.file_format = "JPEG"
    sc.render.image_settings.quality = 90
    sc.render.resolution_x = 960; sc.render.resolution_y = 540
    done = 0
    for f in range(FS, FE + 1):
        path = os.path.join(OUT, f"f{f:04d}.jpg")
        if landed(path):
            done += 1
            continue
        t0 = time.time()
        ok = render_to(path, f)
        log("frame", f, ok, round(time.time() - t0, 1), "s")
        if ok:
            done += 1
    log("FRAMES_DONE", FS, FE, "ok", done)
    print("RENDER_SEQ_DONE")
