#!/usr/bin/env python3
"""
verify_all_poses.py — numeric sit verification for all 5 sitting poses in ONE
blender session (append rig once, swap actions). Prints a PASS/FAIL table.
Run: blender -b 3d-assets/living_room.blend --python verify_all_poses.py
Does not modify or save the scene.
"""
import bpy, json, os, sys
from mathutils import Vector
from mathutils.bvhtree import BVHTree

blend_path = bpy.data.filepath
repo_assets = os.path.dirname(os.path.abspath(blend_path))
ST = os.path.join(repo_assets, "living-room", "sit-targets")
with open(os.path.join(ST, "chair_measurements.json")) as f:
    M = json.load(f)
RIG_BLEND = os.path.join(repo_assets, "cape-jones-rig", "cape_jones_rigged_w5r.blend")
POSE_BLEND = os.path.join(repo_assets, "cape-jones-rig", "sitting_pose_library.blend")
POSES = ["pose_sit_normal", "pose_sit_leg_folded", "pose_sit_lean_forward",
         "pose_sit_recline", "pose_sit_shrug"]

BUTT = Vector(M["butt_target"]["position"])
SEAT_Z = M["seat_surface"]["top_z_center"]
FOOT_TOP = M["footrest"]["top_z"]

def append_from(lib, kind, names):
    with bpy.data.libraries.load(lib, link=False) as (df, dt):
        avail = {n for n in getattr(df, kind)}
        setattr(dt, kind, [n for n in names if n in avail])
    for n in names:
        o = bpy.data.objects.get(n)
        if o and o.name not in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.link(o)

append_from(RIG_BLEND, "objects", ["CapeJones_Rig", "CapeJones_Body"])
rig = bpy.data.objects["CapeJones_Rig"]
body = bpy.data.objects["CapeJones_Body"]
rig.location = (0, 0, 0); rig.rotation_euler = (0, 0, 0); rig.scale = (1, 1, 1)
with bpy.data.libraries.load(POSE_BLEND, link=False) as (df, dt):
    dt.actions = [p for p in POSES if p in set(df.actions)]
if rig.animation_data is None:
    rig.animation_data_create()
chair = bpy.data.objects.get(M["object_name"])
deps = bpy.context.evaluated_depsgraph_get()
chair_ev = chair.evaluated_get(deps)
ct = BVHTree.FromObject(chair_ev, deps)

print("POSE                 | butt_sink_mm | back_pen_mm | feet_z  | bvh_overlap | RESULT")
for pname in POSES:
    rig.animation_data.action = bpy.data.actions.get(pname)
    bpy.context.scene.frame_set(1)
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    bev = body.evaluated_get(deps)
    bme = bev.to_mesh()
    bverts = [body.matrix_world @ v.co for v in bme.vertices]
    bv = [v for v in bverts if abs(v.x-BUTT.x)<0.16 and abs(v.y-BUTT.y)<0.16 and v.z<BUTT.z+0.10]
    sink = (SEAT_Z - min(v.z for v in bv))*1000
    backv = [v for v in bverts if 0.42 < v.z < 0.75 and abs(v.y-BUTT.y)<0.15]
    pen = max([v.x - (3.268 + 0.142*(v.z-0.37)) for v in backv] or [0])*1000
    fv = [v for v in bverts if v.z < 0.20 and v.x < 2.95]
    fz = min(v.z for v in fv) if fv else float('nan')
    bt = BVHTree.FromObject(bev, deps)
    ov = len(ct.overlap(bt))
    ok = sink <= 5 and pen <= 10 and ov == 0 and (fz <= 0.13 if pname=="pose_sit_recline" else fz <= 0.01)
    print(f"{pname:20s} | {sink:11.1f} | {pen:10.1f} | {fz:7.3f} | {ov:11d} | {'PASS' if ok else 'FAIL'}")
    bev.to_mesh_clear()
