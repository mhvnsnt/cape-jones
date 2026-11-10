"""Write a NEW arm-fixed copy of a w5r rig blend (original untouched). Logic lives in cj_arm_guard.py (shared loader).
usage: blender -b cape_jones_rigged_w5r_clean.blend --python build_rig_v2.py -- OUT.blend"""
import bpy, sys, os
sys.path.insert(0, os.environ.get("CJ_TOOLS", os.path.dirname(os.path.abspath(__file__))))
import cj_arm_guard as G
OUT=sys.argv[-1]
print("V2STATS", G.ensure_arm_fix())
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True); print("SAVED", OUT)
