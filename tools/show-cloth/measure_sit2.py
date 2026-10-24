#!/usr/bin/env python3
"""Sitting settle measurements, take 2.
- Shell/thighs/floor via BVHTree.FromObject (worked) for all frames 1-60.
- Chair via BVHTree.FromPolygons (FromObject returns NULL on the linked
  chair in this blend) for sampled frames 1/12/24/36/48/60: nearest + overlap.
"""
import bpy, json
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/scratch/cj-cloth-20261024/sit_cloth_proxy_baked.blend")
sc = bpy.context.scene
cape = bpy.data.objects["CapeJones_Cape"]
chair = bpy.data.objects["loungeChairRelax(Clone)"]
# chair polygons in world space (static object)
cmw = np.array(chair.matrix_world, dtype=np.float64)
cverts = np.array([v.co[:] for v in chair.data.vertices], dtype=np.float64)
cworld = (np.concatenate([cverts, np.ones((len(cverts), 1))], axis=1) @ cmw.T)[:, :3]
cpolys = [list(p.vertices) for p in chair.data.polygons]
chair_bt = BVHTree.FromPolygons([Vector(v) for v in cworld], cpolys)
print(f"chair BVH built: {len(cverts)} verts, {len(cpolys)} polys", flush=True)

def cape_world(frame):
    sc.frame_set(frame)
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    ev = cape.evaluated_get(deps)
    me = ev.to_mesh()
    arr = np.empty(len(me.vertices) * 3, dtype=np.float64)
    me.vertices.foreach_get("co", arr)
    mw = np.array(ev.matrix_world, dtype=np.float64)
    w = (np.concatenate([arr.reshape(-1, 3), np.ones((len(me.vertices), 1))], axis=1) @ mw.T)[:, :3]
    polys = [list(p.vertices) for p in me.polygons]
    ev.to_mesh_clear()
    return w, polys, deps, ev

out = {"frames": [], "chair": []}
for f in range(1, 61):
    w, polys, deps, ev = cape_world(f)
    rec = {"frame": f, "targets": {}}
    for tname in ("BackShell_Collider", "thigh_L_Collider", "thigh_R_Collider", "Floor"):
        t = bpy.data.objects.get(tname)
        if not t:
            continue
        bt = BVHTree.FromObject(t.evaluated_get(deps), deps)
        ds = []
        for v in w[::5]:
            loc, _, _, d = bt.find_nearest(Vector(v))
            if loc is not None:
                ds.append(d)
        ds.sort()
        ct = BVHTree.FromObject(ev, deps)
        rec["targets"][tname] = {"min_mm": round(ds[0] * 1000, 2),
                                 "p5_mm": round(ds[len(ds) // 20] * 1000, 2),
                                 "median_mm": round(ds[len(ds) // 2] * 1000, 2),
                                 "overlap_pairs": len(bt.overlap(ct)) if len(t.data.polygons) < 50000 else None}
    out["frames"].append(rec)
    if f in (1, 12, 24, 36, 48, 60):
        ds = []
        for v in w[::5]:
            loc, _, _, d = chair_bt.find_nearest(Vector(v))
            if loc is not None:
                ds.append(d)
        ds.sort()
        cape_bt = BVHTree.FromPolygons([Vector(v) for v in w], polys)
        out["chair"].append({"frame": f, "min_mm": round(ds[0] * 1000, 2),
                             "p5_mm": round(ds[len(ds) // 20] * 1000, 2),
                             "median_mm": round(ds[len(ds) // 2] * 1000, 2),
                             "overlap_pairs": len(chair_bt.overlap(cape_bt))})
        print(f"frame {f}: chair min {ds[0]*1000:.2f}mm overlap {out['chair'][-1]['overlap_pairs']}", flush=True)
    if f % 12 == 0:
        print(f"frame {f} done", flush=True)

print("SIT2_JSON_BEGIN")
print(json.dumps(out, indent=1))
print("SIT2_JSON_END")
