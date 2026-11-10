"""SPINE LANE — apply IK stiffness tuning to the FK spine control chain.
The Blender IK solver converges tip-first and leaves the waist (spine_fk_1)
straight; stiffening the upper FK joints biases the solve toward the waist
so ik_spine=1 bends "at the waist" like the FK mode does.
Run: blender -b cape_jones_rigged_w5r.blend --python spine_stiffness.py
"""
import bpy

rig = bpy.data.objects["CapeJones_Rig"]
for bn, s in (("spine_fk_2", 0.5), ("spine_fk_3", 0.8), ("spine_fk_4", 0.9)):
    rig.pose.bones[bn].ik_stiffness_x = s
    print(f"STIFFNESS {bn}.ik_stiffness_x = {s}")
bpy.ops.wm.save_mainfile()
print("SAVED", bpy.data.filepath)
