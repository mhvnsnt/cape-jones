"""Quick Workbench render to see character."""
import bpy
from mathutils import Vector
scn = bpy.context.scene
scn.render.engine = 'BLENDER_WORKBENCH'
scn.render.resolution_x = 640; scn.render.resolution_y = 360
scn.frame_set(41); bpy.context.view_layer.update()
# check body visibility
body = bpy.data.objects.get("CapeJones_Body")
print(f"body hide_render={body.hide_render}, location=({body.location.x:.2f},{body.location.y:.2f},{body.location.z:.2f})", flush=True)
rig = bpy.data.objects.get("CapeJones_Rig")
pb = rig.pose.bones['pelvis']
print(f"pelvis.location=({pb.location.x:.3f},{pb.location.y:.3f},{pb.location.z:.3f})", flush=True)
# bbox
ws = [body.matrix_world @ Vector(c) for c in body.bound_box]
print(f"body bbox center: ({sum(v.x for v in ws)/8:.2f},{sum(v.y for v in ws)/8:.2f},{sum(v.z for v in ws)/8:.2f})", flush=True)
cam = scn.camera
cam.location = (1.35, 2.067, 0.85)
d = Vector((3.05,2.067,0.45)) - cam.location
cam.rotation_euler = d.to_track_quat('-Z','Y').to_euler()
bpy.context.view_layer.update()
scn.render.filepath = "/tmp/wb_check.png"
bpy.ops.render.render(write_still=True)
print("WB DONE", flush=True)
