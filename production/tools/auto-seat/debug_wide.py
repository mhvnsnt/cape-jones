"""Wide Workbench shot to see the whole room layout."""
import bpy
from mathutils import Vector
scn = bpy.context.scene
scn.render.engine = 'BLENDER_WORKBENCH'
scn.render.resolution_x = 960; scn.render.resolution_y = 540
scn.frame_set(41); bpy.context.view_layer.update()
cam = scn.camera
# wide shot from above-front
cam.location = (0.5, -1.5, 3.0)
d = Vector((3.0, 2.0, 0.3)) - cam.location
cam.rotation_euler = d.to_track_quat('-Z','Y').to_euler()
bpy.context.view_layer.update()
scn.render.filepath = "/home/hatch/workspace/wt-autoseat/production/tools/auto-seat/proofs/debug_wide.png"
bpy.ops.render.render(write_still=True)
print("WIDE DONE")
