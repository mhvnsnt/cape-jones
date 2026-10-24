"""Kaggle kernel: download Blender 4.0.2, run cloth bake on the attached dataset blend."""
import subprocess, os, sys, glob, tarfile, urllib.request, shutil

WORK = "/kaggle/working"
BLENDER_URL = "https://mirrors.kernel.org/blender/release/Blender4.0/blender-4.0.2-linux-x64.tar.xz"
BLENDER_TAR = os.path.join(WORK, "blender.tar.xz")
BLENDER_DIR = os.path.join(WORK, "blender-4.0.2-linux-x64")

def run(cmd, **kw):
    print("+", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, **kw)
    print("  exit:", r.returncode, flush=True)
    return r

if not os.path.exists(os.path.join(BLENDER_DIR, "blender")):
    print("downloading blender...", flush=True)
    urllib.request.urlretrieve(BLENDER_URL, BLENDER_TAR)
    print("size:", os.path.getsize(BLENDER_TAR), flush=True)
    with tarfile.open(BLENDER_TAR) as t:
        t.extractall(WORK)
blender = os.path.join(BLENDER_DIR, "blender")
run([blender, "--version"])

# find input blend from attached dataset(s)
cands = []
for root, dirs, files in os.walk("/kaggle/input"):
    for f in files:
        if f.endswith(".blend"):
            cands.append(os.path.join(root, f))
print("input blends:", cands, flush=True)
assert cands, "no .blend in /kaggle/input"
src = cands[0]

bake_py = os.path.join(WORK, "blender_bake.py")
BAKE_SRC = r'''
import bpy, os, sys, time
SRC = sys.argv[sys.argv.index("--") + 1]
OUT = sys.argv[sys.argv.index("--") + 2]
print(f"BAKE: opening {SRC}", flush=True)
bpy.ops.wm.open_mainfile(filepath=SRC)
sc = bpy.context.scene
sc.frame_start, sc.frame_end = 1, 81
cape = bpy.data.objects.get("CapeJones_Cape")
assert cape, "CapeJones_Cape missing!"
cloth = None
for m in cape.modifiers:
    if m.type == 'CLOTH':
        cloth = m
assert cloth, "no CLOTH modifier on cape"
pc = cloth.point_cache
pc.frame_start, pc.frame_end = 1, 81
print(f"cloth verts={len(cape.data.vertices)} cache baked={pc.is_baked}", flush=True)
bpy.ops.ptcache.free_bake_all()
t0 = time.time()
bpy.ops.ptcache.bake_all(bake=True)
print(f"bake_all took {time.time()-t0:.1f}s; is_baked={pc.is_baked}", flush=True)
assert pc.is_baked, "bake did not complete"
import numpy as np
def cape_bbox(f):
    sc.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = cape.evaluated_get(dg)
    me = ev.to_mesh()
    arr = np.empty(len(me.vertices) * 3, dtype=np.float64)
    me.vertices.foreach_get("co", arr)
    ev.to_mesh_clear()
    arr = arr.reshape(-1, 3)
    return arr.min(axis=0), arr.max(axis=0), arr.mean(axis=0)
b1 = cape_bbox(1)
b40 = cape_bbox(40)
print("frame1 cape bbox min/max/mean:", [x.round(3).tolist() for x in b1], flush=True)
print("frame40 cape bbox min/max/mean:", [x.round(3).tolist() for x in b40], flush=True)
sc.frame_set(40)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print(f"SAVED {OUT} size={os.path.getsize(OUT)}", flush=True)
print("BAKE DONE", flush=True)
'''
with open(bake_py, "w") as fh:
    fh.write(BAKE_SRC)

out = os.path.join(WORK, "scene_capebaked.blend")
r = run([blender, "-b", "--python", bake_py, "--", src, out])
assert r.returncode == 0, "blender bake failed"
assert os.path.exists(out), "output blend missing"
print("KERNEL DONE, output size:", os.path.getsize(out), flush=True)
