"""SPINE LANE — apply IK stiffness tuning to the FK spine control chain.
The Blender IK solver converges tip-first and leaves the waist (spine_fk_1)
straight; stiffening the upper FK joints biases the solve toward the waist
so ik_spine=1 bends "at the waist" like the FK mode does.
Run: blender -b cape_jones_rigged_w5r.blend --python spine_stiffness.py
"""
import bpy

# PERMANENT ARM FIX (owner pt98u 2026-11-10): route through the shared guarded loader before any arm work.
# The raw w5r arm chain (joints one segment out -> "H" arms) is repaired in memory; unknown chains are refused.
# SPINE-LANE NOTE (PR #401 caveat): this script saves the file in place, so the saved file now carries the
# fixed arm chain + cj_arm_fix mark. Flagged in the landing PR body for lane review; spine behaviour unchanged.
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../..", "guard-stance-v2-20261110", "tools"))
import cj_arm_guard
cj_arm_guard.ensure_arm_fix()

rig = bpy.data.objects["CapeJones_Rig"]
for bn, s in (("spine_fk_2", 0.5), ("spine_fk_3", 0.8), ("spine_fk_4", 0.9)):
    rig.pose.bones[bn].ik_stiffness_x = s
    print(f"STIFFNESS {bn}.ik_stiffness_x = {s}")
bpy.ops.wm.save_mainfile()
print("SAVED", bpy.data.filepath)
