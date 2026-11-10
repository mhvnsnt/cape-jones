#!/usr/bin/env python3
"""
fix_pose_library_rotation_mode.py — PERMANENT FIX (2026-10-18).

The pose_sit_* actions keyframe rotation_quaternion, but the rig's pose bones
default to rotation_mode='XYZ' (euler), which SILENTLY IGNORES quaternion
keyframes. Result: the sitting poses never applied (character stayed in
T-pose). This script sets all pose bones to QUATERNION mode and saves.

Run: blender -b sitting_pose_library.blend --python fix_pose_library_rotation_mode.py
"""
import bpy

arm = next((o for o in bpy.data.objects if o.type == 'ARMATURE'), None)
assert arm, "no armature found"
n = 0
for pb in arm.pose.bones:
    if pb.rotation_mode != 'QUATERNION':
        pb.rotation_mode = 'QUATERNION'
        n += 1
print(f"set {n} bones to QUATERNION mode (of {len(arm.pose.bones)})")

# verify the actions now evaluate correctly
act = bpy.data.actions.get('pose_sit_normal')
if not arm.animation_data:
    arm.animation_data_create()
arm.animation_data.action = act
bpy.context.scene.frame_set(1)
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
arm_ev = arm.evaluated_get(deps)
thigh = arm_ev.pose.bones.get('thigh_L')
d = (thigh.tail - thigh.head).normalized()
print(f"thigh_L dir with pose_sit_normal: {tuple(round(v,2) for v in d)}")
assert abs(d.z) < 0.95, "thigh still pointing down - fix failed!"
print("FIX VERIFIED: thigh bends forward for sitting")

bpy.ops.wm.save_mainfile()
print("saved", bpy.data.filepath)
