"""Render from wider angle."""
import bpy, os, time
from mathutils import Vector
PROOF_DIR = "/home/hatch/workspace/wt-autoseat/production/tools/auto-seat/proofs"
STAMP = time.strftime("%Y%m%d_%H%M%S")
scn = bpy.context.scene
scn.render.engine='CYCLES'; scn.cycles.samples=16
scn.render.resolution_x=960; scn.render.resolution_y=540
scn.frame_set(41); bpy.context.view_layer.update()
cam=scn.camera
# wide: back and up
cam.location = (0.0, 2.067, 2.0)
d = Vector((3.05,2.067,0.3)) - cam.location
cam.rotation_euler = d.to_track_quat('-Z','Y').to_euler()
bpy.context.view_layer.update()
scn.render.filepath=os.path.join(PROOF_DIR,f"autoseat_wide_{STAMP}.png")
bpy.ops.render.render(write_still=True)
print("WIDE RENDERED",flush=True)
