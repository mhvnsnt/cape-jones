"""LANE 1 — make a LIGHT sim file: keep rig + cape + shell + floor,
DELETE the 910k body, MDEF cage, old fragments. The sim doesn't need them.
Saves cape_sim_light.blend (small, fast to bake)."""
import bpy, os

# PERMANENT ARM FIX (owner pt98u 2026-11-10): route through the shared guarded loader before any arm work.
# The raw w5r arm chain (joints one segment out -> "H" arms) is repaired in memory; unknown chains are refused.
# Runs BEFORE the body is deleted below (the loader needs CapeJones_Body present to redistribute arm weights).
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../..", "guard-stance-v2-20261110", "tools"))
import cj_arm_guard
cj_arm_guard.ensure_arm_fix()

LIGHT = os.path.join(os.getcwd(), 'cape_sim_light.blend')

# objects to keep
keep = {'CapeJones_Rig', 'CapeJones_Cape', 'BackShell_Collider', 'Floor_Collision'}
for ob in list(bpy.data.objects):
    if ob.name not in keep and ob.type != 'CAMERA':
        # remove object and its data
        bpy.data.objects.remove(ob, do_unlink=True)

# purge orphan data
for _ in range(3):
    bpy.ops.outliner.orphans_purge(do_recursive=True)

print(f"objects kept: {[o.name for o in bpy.data.objects]}", flush=True)
bpy.ops.wm.save_as_mainfile(filepath=LIGHT)
print(f"SAVED {LIGHT}", flush=True)
import os as _os
print(f"size: {_os.path.getsize(LIGHT)}", flush=True)
