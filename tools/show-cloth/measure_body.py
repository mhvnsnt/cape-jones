#!/usr/bin/env python3
"""Measure baked proxy cape vs the REAL body mesh (appended from the base
blend). Nearest distances at frames 0/24/48/72/96 + BVH overlap at frame 48
(the worst shell-contact frame). Read-only."""
import bpy, json
from mathutils import Vector
from mathutils.bvhtree import BVHTree

BAKED = "/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_proxy_baked.blend"
BASE = "/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_base.blend"
bpy.ops.wm.open_mainfile(filepath=BAKED)
with bpy.data.libraries.load(BASE, link=False) as (df, dt):
    dt.objects = ["CapeJones_Body"] if "CapeJones_Body" in set(df.objects) else []
body = bpy.data.objects.get("CapeJones_Body")
assert body, "body append failed"
bpy.context.scene.collection.objects.link(body)
arm_mod = next((m for m in body.modifiers if m.type == "ARMATURE"), None)
print("body armature target:", arm_mod.object.name if arm_mod and arm_mod.object else None, flush=True)
cape = bpy.data.objects["CapeJones_Cape"]
sc = bpy.context.scene

out = {"frames": []}
for f in (0, 24, 48, 72, 96):
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
    bt = BVHTree.FromObject(body.evaluated_get(deps), deps)
    ds = []
    for v in world[::5]:
        loc, _, _, d = bt.find_nearest(Vector(v))
        if loc is not None:
            ds.append(d)
    ds.sort()
    rec = {"frame": f, "sampled": len(ds),
           "min_mm": round(ds[0] * 1000, 2),
           "p5_mm": round(ds[len(ds) // 20] * 1000, 2),
           "median_mm": round(ds[len(ds) // 2] * 1000, 2)}
    if f == 48:
        ct = BVHTree.FromObject(ev, deps)
        rec["overlap_pairs_vs_body"] = len(bt.overlap(ct))
    out["frames"].append(rec)
    print(f"frame {f}: {rec}", flush=True)

print("BODY_JSON_BEGIN")
print(json.dumps(out, indent=1))
print("BODY_JSON_END")
