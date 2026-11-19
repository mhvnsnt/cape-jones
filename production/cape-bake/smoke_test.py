"""Smoke test: bake frames 1-10 on a copy, report timing + cape bbox sanity."""
import bpy, time
import numpy as np

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/capebake-work/test_bake.blend")
sc = bpy.context.scene
cape = bpy.data.objects["CapeJones_Cape"]
cloth = [m for m in cape.modifiers if m.type == 'CLOTH'][0]
pc = cloth.point_cache
sc.frame_start, sc.frame_end = 1, 10
pc.frame_start, pc.frame_end = 1, 10

def cape_stats(f):
    sc.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = cape.evaluated_get(dg)
    me = ev.to_mesh()
    arr = np.empty(len(me.vertices) * 3, dtype=np.float64)
    me.vertices.foreach_get("co", arr)
    ev.to_mesh_clear()
    arr = arr.reshape(-1, 3)
    return arr.min(axis=0), arr.max(axis=0), arr.mean(axis=0), np.isnan(arr).any()

mn, mx, mean, nan = cape_stats(1)
print(f"pre-bake frame1: min={mn.round(3).tolist()} max={mx.round(3).tolist()} mean={mean.round(3).tolist()} NaN={nan}", flush=True)
t0 = time.time()
bpy.ops.ptcache.bake_all(bake=True)
dt = time.time() - t0
print(f"bake 10 frames took {dt:.1f}s ({dt/10:.1f}s/frame) is_baked={pc.is_baked}", flush=True)
for f in (1, 5, 10):
    mn, mx, mean, nan = cape_stats(f)
    print(f"frame{f}: min={mn.round(3).tolist()} max={mx.round(3).tolist()} mean={mean.round(3).tolist()} NaN={nan}", flush=True)
print("SMOKE DONE", flush=True)
