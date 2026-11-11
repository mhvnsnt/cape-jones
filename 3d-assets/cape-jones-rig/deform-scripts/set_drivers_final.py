"""Set CORRECT corrective driver expressions from measured angles. Set base values to 0."""
import bpy

# PERMANENT ARM FIX (owner pt98u 2026-11-10): route through the shared guarded loader before any arm work.
# The raw w5r arm chain (joints one segment out -> "H" arms) is repaired in memory; unknown chains are refused.
# NOTE: the FIXES expressions below were calibrated on the RAW (defective) chain's rest angles
# (see LANDING.md / PR body) — they need re-derivation from the fixed rig before this script is re-run.
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../..", "guard-stance-v2-20261110", "tools"))
import cj_arm_guard
cj_arm_guard.ensure_arm_fix()

body = bpy.data.objects['CapeJones_Body']
rig = bpy.data.objects['CapeJones_Rig']
sk = body.data.shape_keys

# (key, bone1, bone2, expression) -- expressions from measured ROTATION_DIFF angles
FIXES = [
    ("corr_elbow_L", "upperarm_L", "forearm_L",
     "max(0.0, min(1.0, (bend - 0.6685) / 1.5500))"),   # rest 0.219 -> 2.49 at 130deg
    ("corr_elbow_R", "upperarm_R", "forearm_R",
     "max(0.0, min(1.0, (bend - 0.6338) / 1.5500))"),   # rest 0.184 -> 2.45 at 130deg
    ("corr_jaw_open", "head", "jaw",
     "max(0.0, min(1.0, (4.3117 - bend) / 0.4500))"),    # rest 4.4117 DECREASES to 3.8532 at 32deg
    ("corr_neck_head", "neck_2", "head",
     "max(0.0, min(1.0, (bend - 3.2858) / 0.4500))"),    # rest 3.1358 INCREASES to 3.7442 at 60deg
]

ad = sk.animation_data
for key_name, b1, b2, expr in FIXES:
    kb = sk.key_blocks[key_name]
    # remove existing driver
    if ad:
        for fc in list(ad.drivers):
            if fc.data_path == f'key_blocks["{key_name}"].value':
                ad.drivers.remove(fc)
    drv = kb.driver_add("value").driver
    drv.type = 'SCRIPTED'
    var = drv.variables.new()
    var.name = "bend"
    var.type = 'ROTATION_DIFF'
    var.targets[0].id = rig
    var.targets[0].bone_target = b1
    var.targets[1].id = rig
    var.targets[1].bone_target = b2
    drv.expression = expr
    kb.value = 0.0
    print(f"{key_name}: expr={expr}", flush=True)

bpy.ops.wm.save_mainfile()
print("SAVED", flush=True)
