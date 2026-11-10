"""Kaggle PROBE: download Blender 4.0.2, bake cloth frames 1-6 with REAL settings,
report timing + peak RSS + cape bbox sanity. Decides full-bake settings."""
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

cands = []
for root, dirs, files in os.walk("/kaggle/input"):
    for f in files:
        if f.endswith(".blend"):
            cands.append(os.path.join(root, f))
print("input blends:", cands, flush=True)
assert cands, "no .blend in /kaggle/input"
src = cands[0]

PROBE = r'''
import bpy, time, resource
import numpy as np
bpy.ops.wm.open_mainfile(filepath="SRC_PATH")
sc = bpy.context.scene
cape = bpy.data.objects["CapeJones_Cape"]
cloth = [m for m in cape.modifiers if m.type == 'CLOTH'][0]
# --- settings overrides for a survivable bake (482k... 282k verts, 160 stacked shells) ---
cloth.settings.quality = 8
cloth.settings.bending_stiffness = 1.2
cloth.collision_settings.use_self_collision = False
cloth.collision_settings.collision_quality = 2
pc = cloth.point_cache
sc.frame_start, sc.frame_end = 1, 6
pc.frame_start, pc.frame_end = 1, 6
print(f"PROBE cloth: verts={len(cape.data.vertices)} quality={cloth.settings.quality} selfcol={cloth.collision_settings.use_self_collision} colq={cloth.collision_settings.collision_quality}", flush=True)
t0 = time.time()
bpy.ops.ptcache.bake_all(bake=True)
dt = time.time() - t0
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
print(f"PROBE bake 6 frames: {dt:.1f}s ({dt/6:.1f}s/frame) peakRSS={peak:.2f}GB is_baked={pc.is_baked}", flush=True)
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
for f in (1, 3, 6):
    mn, mx, mean, nan = cape_stats(f)
    print(f"PROBE frame{f}: min={mn.round(3).tolist()} max={mx.round(3).tolist()} mean={mean.round(3).tolist()} NaN={nan}", flush=True)
print("PROBE DONE", flush=True)
'''
probe_py = os.path.join(WORK, "probe.py")
with open(probe_py, "w") as fh:
    fh.write(PROBE.replace("SRC_PATH", src))
r = subprocess.run([blender, "-b", "--python", probe_py])
print("blender exit:", r.returncode, flush=True)
print("KERNEL PROBE FINISHED", flush=True)
