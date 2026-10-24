"""Kaggle FULL BAKE: Blender 4.0.2, cloth bake frames 1-81 with probe-proven settings.
Settings: quality 8, self-collision OFF (cape is 160 stacked shells - self-collision
pair explosion OOM-killed both the local VM and a Kaggle probe at quality 12),
collision quality 2, bending_stiffness 1.2. Saves scene_capebaked.blend."""
import subprocess, os, urllib.request, tarfile

WORK = "/kaggle/working"
BTMP = "/tmp/blender_dl"
os.makedirs(BTMP, exist_ok=True)
BLENDER_URLS = [
    "https://download.blender.org/release/Blender4.0/blender-4.0.2-linux-x64.tar.xz",
    "https://ftp.nluug.nl/pub/graphics/blender/release/Blender4.0/blender-4.0.2-linux-x64.tar.xz",
    "https://mirrors.ocf.berkeley.edu/blender/release/Blender4.0/blender-4.0.2-linux-x64.tar.xz",
    "https://mirrors.kernel.org/blender/release/Blender4.0/blender-4.0.2-linux-x64.tar.xz",
]
BLENDER_TAR = os.path.join(BTMP, "blender.tar.xz")
BLENDER_DIR = os.path.join(BTMP, "blender-4.0.2-linux-x64")

if not os.path.exists(os.path.join(BLENDER_DIR, "blender")):
    last_err = None
    for url in BLENDER_URLS:
        try:
            print("downloading blender from", url, flush=True)
            urllib.request.urlretrieve(url, BLENDER_TAR)
            sz = os.path.getsize(BLENDER_TAR)
            print("tar size:", sz, flush=True)
            assert sz > 200_000_000, "tar too small"
            break
        except Exception as e:
            last_err = e
            print("failed:", e, flush=True)
    else:
        raise RuntimeError(f"all blender mirrors failed: {last_err}")
    with tarfile.open(BLENDER_TAR) as t:
        t.extractall(BTMP)
blender = os.path.join(BLENDER_DIR, "blender")
print(subprocess.run([blender, "--version"], capture_output=True, text=True).stdout, flush=True)

cands = []
for root, dirs, files in os.walk("/kaggle/input"):
    for f in files:
        if f.endswith(".blend"):
            cands.append(os.path.join(root, f))
print("input blends:", cands, flush=True)
assert cands, "no .blend in /kaggle/input"
src = cands[0]

BAKE = r'''
import bpy, time, resource, os
import numpy as np
SRC = "SRC_PATH"
OUT = "/kaggle/working/scene_capebaked.blend"
print("BAKE opening", SRC, flush=True)
bpy.ops.wm.open_mainfile(filepath=SRC)
sc = bpy.context.scene
cape = bpy.data.objects["CapeJones_Cape"]
cloth = [m for m in cape.modifiers if m.type == 'CLOTH'][0]
cloth.settings.quality = 8
cloth.settings.bending_stiffness = 1.2
cloth.collision_settings.use_self_collision = False
cloth.collision_settings.collision_quality = 3
pc = cloth.point_cache
sc.frame_start, sc.frame_end = 1, 81
pc.frame_start, pc.frame_end = 1, 81
pc.use_disk_cache = False
print(f"BAKE cloth verts={len(cape.data.vertices)} quality={cloth.settings.quality} selfcol={cloth.collision_settings.use_self_collision}", flush=True)
bpy.ops.ptcache.free_bake_all()
t0 = time.time()
bpy.ops.ptcache.bake_all(bake=True)
dt = time.time() - t0
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
print(f"BAKE 81 frames: {dt:.1f}s ({dt/81:.1f}s/frame) peakRSS={peak:.2f}GB is_baked={pc.is_baked}", flush=True)
assert pc.is_baked, "bake incomplete"
def cape_stats(f):
    sc.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = cape.evaluated_get(dg)
    me = ev.to_mesh()
    arr = np.empty(len(me.vertices) * 3, dtype=np.float64)
    me.vertices.foreach_get("co", arr)
    ev.to_mesh_clear()
    arr = arr.reshape(-1, 3)
    return arr.min(axis=0), arr.max(axis=0), arr.mean(axis=0), bool(np.isnan(arr).any())
for f in (1, 40, 81):
    mn, mx, mean, nan = cape_stats(f)
    print(f"BAKE frame{f}: min={mn.round(3).tolist()} max={mx.round(3).tolist()} mean={mean.round(3).tolist()} NaN={nan}", flush=True)
    assert not nan, f"NaN in cape at frame {f}"
sc.frame_set(40)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print(f"SAVED {OUT} size={os.path.getsize(OUT)}", flush=True)
print("BAKE DONE", flush=True)
'''
bake_py = os.path.join(WORK, "blender_bake_full.py")
with open(bake_py, "w") as fh:
    fh.write(BAKE.replace("SRC_PATH", src))
r = subprocess.run([blender, "-b", "--python", bake_py])
print("blender exit:", r.returncode, flush=True)
assert r.returncode == 0
out = os.path.join(WORK, "scene_capebaked.blend")
assert os.path.exists(out), "output blend missing"
print("KERNEL DONE, output size:", os.path.getsize(out), flush=True)
