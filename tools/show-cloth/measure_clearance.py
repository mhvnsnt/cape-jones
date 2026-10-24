#!/usr/bin/env python3
"""Measure cape clearances in a baked scene.

Usage: blender -b --python measure_clearance.py -- <blend> <cape> <targets_csv>
       <frames_csv_or_all> <sample_step>
- distances: sampled cape verts -> BVH nearest on each target (mm)
- overlap pairs: BVH overlap, only for targets with <50k polys (cheap ones)
Prints JSON. Read-only (does not save).
"""
import bpy, sys, json
from mathutils.bvhtree import BVHTree

a = sys.argv[sys.argv.index("--") + 1:]
BLEND, CAPE_NAME, TARGETS_CSV, FRAMES_ARG, STEP = a[0], a[1], a[2], a[3], int(a[4])
bpy.ops.wm.open_mainfile(filepath=BLEND)
sc = bpy.context.scene
cape = bpy.data.objects[CAPE_NAME]
targets = [bpy.data.objects[n] for n in TARGETS_CSV.split(",") if bpy.data.objects.get(n)]
if FRAMES_ARG == "all":
    frames = list(range(sc.frame_start, sc.frame_end + 1))
else:
    frames = [int(f) for f in FRAMES_ARG.split(",")]

out = {"blend": BLEND, "frames": []}
for f in frames:
    sc.frame_set(f)
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    ev = cape.evaluated_get(deps)
    me = ev.to_mesh()
    import numpy as np
    arr = np.empty(len(me.vertices) * 3, dtype=np.float64)
    me.vertices.foreach_get("co", arr)
    mw = np.array(ev.matrix_world, dtype=np.float64)
    world = (np.concatenate([arr.reshape(-1, 3), np.ones((len(me.vertices), 1))], axis=1) @ mw.T)[:, :3]
    ev.to_mesh_clear()
    sample = world[::STEP]
    frec = {"frame": f, "sampled_verts": int(len(sample)), "targets": {}}
    for t in targets:
        tev = t.evaluated_get(deps)
        bt = BVHTree.FromObject(tev, deps)
        ds = []
        for v in sample:
            loc, _, _, d = bt.find_nearest(v)
            if loc is not None:
                ds.append(d)
        ds.sort()
        trec = {"min_mm": round(ds[0] * 1000, 2) if ds else None,
                "p5_mm": round(ds[len(ds) // 20] * 1000, 2) if ds else None,
                "median_mm": round(ds[len(ds) // 2] * 1000, 2) if ds else None}
        if len(tev.data.polygons) < 50000:
            ct = BVHTree.FromObject(ev, deps)
            trec["overlap_pairs"] = len(bt.overlap(ct))
        frec["targets"][t.name] = trec
        print(f"frame {f} vs {t.name}: {trec}", flush=True)
    out["frames"].append(frec)

print("MEASURE_JSON_BEGIN")
print(json.dumps(out, indent=1))
print("MEASURE_JSON_END")
