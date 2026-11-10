"""Runs INSIDE Blender on Kaggle: bake cloth point cache frames 1-81, save."""
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

# free any existing bake then bake fresh
bpy.ops.ptcache.free_bake_all()
t0 = time.time()
bpy.ops.ptcache.bake_all(bake=True)
print(f"bake_all took {time.time()-t0:.1f}s; is_baked={pc.is_baked}", flush=True)
assert pc.is_baked, "bake did not complete"

# sanity: cape shape must differ between frame 1 and frame 40 (sim actually ran)
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
