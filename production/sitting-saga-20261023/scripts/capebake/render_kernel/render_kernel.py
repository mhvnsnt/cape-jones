"""Kaggle proof renders from the baked scene (kernel-source input = cape-bake-full output).
Renders the two tasked frame-40 shots at Cycles 4 samples, 960x540 @50%."""
import subprocess, os, urllib.request, tarfile

WORK = "/kaggle/working"
BTMP = "/tmp/blender_dl"
os.makedirs(BTMP, exist_ok=True)
BLENDER_URLS = [
    "https://download.blender.org/release/Blender4.0/blender-4.0.2-linux-x64.tar.xz",
    "https://ftp.nluug.nl/pub/graphics/blender/release/Blender4.0/blender-4.0.2-linux-x64.tar.xz",
    "https://mirrors.ocf.berkeley.edu/blender/release/Blender4.0/blender-4.0.2-linux-x64.tar.xz",
]
BLENDER_TAR = os.path.join(BTMP, "blender.tar.xz")
BLENDER_DIR = os.path.join(BTMP, "blender-4.0.2-linux-x64")

if not os.path.exists(os.path.join(BLENDER_DIR, "blender")):
    last_err = None
    for url in BLENDER_URLS:
        try:
            print("downloading blender from", url, flush=True)
            urllib.request.urlretrieve(url, BLENDER_TAR)
            assert os.path.getsize(BLENDER_TAR) > 200_000_000
            break
        except Exception as e:
            last_err = e
            print("failed:", e, flush=True)
    else:
        raise RuntimeError(f"all blender mirrors failed: {last_err}")
    with tarfile.open(BLENDER_TAR) as t:
        t.extractall(BTMP)
blender = os.path.join(BLENDER_DIR, "blender")

cands = []
for root, dirs, files in os.walk("/kaggle/input"):
    for f in files:
        if f == "scene_capebaked.blend":
            cands.append(os.path.join(root, f))
print("baked blends:", cands, flush=True)
assert cands, "scene_capebaked.blend not found in input"
src = cands[0]

RENDER = r'''
import bpy
import mathutils
SRC = "SRC_PATH"
bpy.ops.wm.open_mainfile(filepath=SRC)
scene = bpy.context.scene
cape = bpy.data.objects["CapeJones_Cape"]
cloth = [m for m in cape.modifiers if m.type == 'CLOTH'][0]
print(f"VERIFY: is_baked={cloth.point_cache.is_baked} verts={len(cape.data.vertices)}", flush=True)
scene.frame_set(40)
scene.render.engine = 'CYCLES'
scene.cycles.samples = 4
scene.cycles.device = 'CPU'
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 50

def shot(name, loc, tgt):
    cam_data = bpy.data.cameras.new(name)
    cam = bpy.data.objects.new(name, cam_data)
    scene.collection.objects.link(cam)
    cam.location = loc
    tv = mathutils.Vector(tgt)
    cam.rotation_euler = (tv - cam.location).to_track_quat('-Z', 'Y').to_euler()
    scene.camera = cam
    scene.render.filepath = f"/kaggle/working/{name}.png"
    bpy.ops.render.render(write_still=True)
    print("RENDERED", scene.render.filepath, flush=True)
    bpy.data.objects.remove(cam, do_unlink=True)

shot("capebake_front_f40_v1", (1.1, 0.1, 1.25), (2.95, 2.05, 0.5))
shot("capebake_closeup_f40_v1", (2.15, 1.15, 0.85), (2.92, 2.08, 0.55))
print("RENDERS DONE", flush=True)
'''
render_py = os.path.join(WORK, "render_proofs_k.py")
with open(render_py, "w") as fh:
    fh.write(RENDER.replace("SRC_PATH", src))
r = subprocess.run([blender, "-b", "--python", render_py])
print("blender exit:", r.returncode, flush=True)
assert r.returncode == 0
print("KERNEL DONE", flush=True)
