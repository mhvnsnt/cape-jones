#!/usr/bin/env python3
"""Audit the 5 sitting poses (show-context): body-vs-chair overlap (the
place_sitter hard gate), mantle placement + mantle-vs-body/chair clearances
(pre-cloth, rigid placement). Read-only: never saves living_room.blend.

Usage: blender -b --python audit_sitting.py
"""
import bpy, math, json
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOM = "/home/hatch/workspace/scratch/cj-3d/repo/3d-assets/living_room.blend"
LIB = "/home/hatch/workspace/scratch/cj-3d/repo/3d-assets/cape-jones-rig/sitting_pose_library.blend"
POSES = ["pose_sit_normal", "pose_sit_leg_folded", "pose_sit_lean_forward",
         "pose_sit_recline", "pose_sit_shrug"]

bpy.ops.wm.open_mainfile(filepath=ROOM)
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
body = bpy.data.objects["CapeJones_Body"]
cape = bpy.data.objects["CapeJones_Cape"]
chair = bpy.data.objects["loungeChairRelax(Clone)"]

# load pose actions from the library
with bpy.data.libraries.load(LIB, link=False) as (df, dt):
    dt.actions = [p for p in POSES if p in set(df.actions)]
print("loaded actions:", [a.name for a in bpy.data.actions if a.name in POSES], flush=True)

def world_verts(obj, deps, step=1):
    ev = obj.evaluated_get(deps)
    me = ev.to_mesh()
    arr = np.empty(len(me.vertices) * 3, dtype=np.float64)
    me.vertices.foreach_get("co", arr)
    mw = np.array(ev.matrix_world, dtype=np.float64)
    w = (np.concatenate([arr.reshape(-1, 3), np.ones((len(me.vertices), 1))], axis=1) @ mw.T)[:, :3]
    ev.to_mesh_clear()
    return w[::step]

def nearest_stats(sample, target_obj, deps):
    bt = BVHTree.FromObject(target_obj.evaluated_get(deps), deps)
    ds = []
    for v in sample:
        loc, _, _, d = bt.find_nearest(Vector(v))
        if loc is not None:
            ds.append(d)
    ds.sort()
    return {"min_mm": round(ds[0] * 1000, 2), "p5_mm": round(ds[len(ds) // 20] * 1000, 2),
            "median_mm": round(ds[len(ds) // 2] * 1000, 2)} if ds else None

# Chair BVH from polygons: FromObject returns NULL on the linked chair
# (proven in measure_clearance.py); the chair is static, so build once.
_cmw = np.array(chair.matrix_world, dtype=np.float64)
_cverts = np.array([v.co[:] for v in chair.data.vertices], dtype=np.float64)
_cworld = (np.concatenate([_cverts, np.ones((len(_cverts), 1))], axis=1) @ _cmw.T)[:, :3]
_chair_bt = BVHTree.FromPolygons([Vector(v) for v in _cworld],
                                 [list(p.vertices) for p in chair.data.polygons])
print(f"chair BVH (polygons): {len(_cverts)} verts", flush=True)

def nearest_stats_chair(sample):
    ds = []
    for v in sample:
        loc, _, _, d = _chair_bt.find_nearest(Vector(v))
        if loc is not None:
            ds.append(d)
    ds.sort()
    return {"min_mm": round(ds[0] * 1000, 2), "p5_mm": round(ds[len(ds) // 20] * 1000, 2),
            "median_mm": round(ds[len(ds) // 2] * 1000, 2)} if ds else None

results = {}
for pose in POSES:
    act = bpy.data.actions.get(pose)
    if act is None:
        results[pose] = {"error": "action not found"}
        continue
    if rig.animation_data is None:
        rig.animation_data_create()
    rig.animation_data.action = act
    sc.frame_set(1)
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    rec = {}
    # body vs chair overlap (hard gate)
    bt = BVHTree.FromObject(body.evaluated_get(deps), deps)
    rec["body_vs_chair_overlap"] = len(bt.overlap(_chair_bt))
    pelvis = rig.matrix_world @ rig.pose.bones["pelvis"].head
    rec["pelvis_z"] = round(pelvis.z, 3)
    # place mantle on seated shoulders (same logic as build_cloth_sit.py)
    neck = rig.matrix_world @ rig.pose.bones["neck_1"].head
    bworld = world_verts(body, deps, step=5)
    band = bworld[np.abs(bworld[:, 2] - neck.z) < 0.06]
    back_x = float(np.percentile(band[:, 0], 95)) if len(band) else 3.35
    cape.rotation_mode = "XYZ"  # room cape is QUATERNION; euler alone is ignored
    cape.rotation_euler = (0, 0, -math.pi / 2)
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    cworld = world_verts(cape, deps, step=1)
    top = cworld[cworld[:, 2] > cworld[:, 2].max() - 0.05]
    top_center = top.mean(axis=0)
    slab_min_x = cworld[:, 0].min()
    cape.location = ((back_x + 0.012) - slab_min_x, 2.067 - top_center[1], neck.z - top_center[2])
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    cworld = world_verts(cape, deps, step=50)
    rec["mantle_vs_chair_dist"] = nearest_stats_chair(cworld)
    capet = BVHTree.FromObject(cape.evaluated_get(deps), deps)
    rec["mantle_vs_chair_overlap"] = len(_chair_bt.overlap(capet))
    rec["mantle_vs_body_dist"] = nearest_stats(cworld, body, deps)
    if pose == "pose_sit_normal":
        rec["mantle_vs_body_overlap"] = len(bt.overlap(capet))
    results[pose] = rec
    print(f"{pose}: {json.dumps(rec)}", flush=True)

print("AUDIT_JSON_BEGIN")
print(json.dumps(results, indent=1))
print("AUDIT_JSON_END")
