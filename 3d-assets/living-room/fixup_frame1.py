#!/usr/bin/env python3
"""
One-time fixup for the integrated living_room.blend (2026-10-18).

Corrects two issues found after the first assembly save:
1. The linked recliner carries the ReclinerOpen action (frames 1-24,
   recline 0->1). The blend was saved at frame 48 -> recline=1.0 (open).
   The task requires closed default, so the blend must sit at frame 1.
2. To keep the "CAPE JONES / TONIGHT" title card as the hero TV frame, the
   image sequence is offset (image_user.frame_offset = 47) so scene frame 1
   shows loop frame 48.

Also re-applies the repo-relative paths and the yawed TV_Glow position that
tv_setup.py resets to its hardcoded defaults on re-run.

Does NOT re-run place_sitter / lighting rig (already applied). Saves the blend.
"""

import bpy
import os
import runpy
import sys
from mathutils import Vector

BLEND = "3d-assets/living_room.blend"
bpy.ops.wm.open_mainfile(filepath=BLEND)
sc = bpy.context.scene
vl = bpy.context.view_layer
ASSETS = os.path.dirname(os.path.abspath(BLEND))
LR = os.path.join(ASSETS, "living-room")

# re-run tv_setup (idempotent; re-installs the session handler)
old_argv = sys.argv
sys.argv = ["blender", "--"]
runpy.run_path(os.path.join(LR, "tv", "tv_setup.py"), run_name="__main__")
sys.argv = old_argv

tv = bpy.data.objects["crt_tv"]
tv["tv_power"] = 1.0

# repo-relative sequence path (tv_setup resets it to absolute)
img = bpy.data.images.get("tv_show_seq")
img.filepath = "//living-room/tv/frames/tv_show_0001.png"
img.reload()

# title card (loop frame 48) on scene frame 1
mat = bpy.data.materials["tvScreenMat"]
tex = next(n for n in mat.node_tree.nodes if n.type == "TEX_IMAGE")
tex.image_user.frame_offset = 47

# TV_Glow back along the yawed screen normal (tv_setup hardcodes pre-yaw pos)
screen = bpy.data.objects["crt_screen"]
nrm = (screen.matrix_world.to_3x3() @ Vector((0, 0, 1))).normalized()
ctr = screen.matrix_world.translation
glow = bpy.data.objects["TV_Glow"]
glow.location = ctr + nrm * 0.612 + Vector((0, 0, 0.04))

tv.update_tag()
sc.frame_set(1)      # recline=0 (closed) via ReclinerOpen; handler applies TV power
vl.update()

# ---- verify
arm = bpy.data.objects["recliner_rig"]
assert float(arm.get("recline")) == 0.0, f"recline={arm.get('recline')} (want 0)"
mix = next(n for n in mat.node_tree.nodes if n.type == "MIX_SHADER")
assert abs(mix.inputs[0].default_value - 1.0) < 1e-6, "TV mix not ON"
assert abs(glow.data.energy - 14.0) < 1e-6, f"glow={glow.data.energy}"
assert sc.frame_current == 1
print(f"FIXUP OK: frame 1, recline={arm.get('recline')}, TV ON, "
      f"glow={tuple(round(v,3) for v in glow.location)}, seq start={tex.image_user.frame_start}")
bpy.ops.wm.save_mainfile()
print("saved", bpy.data.filepath)
