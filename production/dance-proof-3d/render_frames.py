"""Cape Jones dance proof 3D v2 - STAGE B: render from scene_v2.blend.

Modes:
  check            low-res verification stills (front loop phases, back views,
                   back hem zoom) + per-frame eval timing
  frames FS FE     JPEG sequence frames FS..FE into frames/ (skips existing)
Run: blender -b scene_v2.blend --python render_seq.py -- <mode> [FS FE]
"""
import bpy, math, os, sys, time

D = math.radians
WORK = "/home/hatch/workspace/_cj-dance3d-v2"
argv = sys.argv[sys.argv.index("--") + 1:]
MODE = argv[0] if argv else "check"
sc = bpy.context.scene
t00 = time.time()
def log(*a):
    print("[stageB]", *a, round(time.time() - t00, 1), "s", flush=True)

def render_to(path, frame, tries=4):
    for i in range(tries):
        try:
            sc.frame_set(frame)
            sc.render.filepath = path
            bpy.ops.render.render(write_still=True)
            return True
        except Exception as e:
            log("render failed", path, e, "retry", i)
            time.sleep(10)
    return False

if MODE == "check":
    OUT = os.path.join(WORK, "check")
    os.makedirs(OUT, exist_ok=True)
    # eval timing on the rig (posed frames, after warm-up)
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
    main_cam = sc.camera
    for f in (5, 9, 21, 33, 39):
        t0 = time.time()
        ok = render_to(os.path.join(OUT, f"v2_f{f}.png"), f)
        log("check front", f, ok, round(time.time() - t0, 1), "s")
    from mathutils import Vector
    def look_at(cam, loc, target):
        cam.location = loc
        d = Vector(target) - Vector(loc)
        cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    bpy.ops.object.camera_add()
    bcam = bpy.context.active_object; bcam.data.lens = 40; sc.camera = bcam
    look_at(bcam, (0, 2.6, 1.35), (0, 0, 0.40))
    for f in (9, 33):
        t0 = time.time()
        ok = render_to(os.path.join(OUT, f"v2_back{f}.png"), f)
        log("check back", f, ok, round(time.time() - t0, 1), "s")
    bcam.data.lens = 55
    look_at(bcam, (0, 0.9, 0.35), (0, 0.08, 0.18))
    ok = render_to(os.path.join(OUT, "v2_hem33.png"), 33)
    log("check hem", ok)
    sc.camera = main_cam
    print("CHECK_DONE")
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
        if os.path.exists(path) and os.path.getsize(path) > 10000:
            done += 1
            continue
        t0 = time.time()
        ok = render_to(path, f)
        log("frame", f, ok, round(time.time() - t0, 1), "s")
        if ok:
            done += 1
    log("FRAMES_DONE", FS, FE, "ok", done)
    print("RENDER_SEQ_DONE")
