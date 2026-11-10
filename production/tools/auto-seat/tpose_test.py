"""Test: does the body render at origin in T-pose?"""
import bpy
from mathutils import Vector, Quaternion
scn = bpy.context.scene
rig = bpy.data.objects.get("CapeJones_Rig")
# clear pose to T-pose at origin
for b in rig.pose.bones:
    if b.rotation_mode == 'QUATERNION':
        b.rotation_quaternion = Quaternion((1,0,0,0))
    b.location = Vector((0,0,0))
bpy.context.view_layer.update()
scn.render.engine='CYCLES'; scn.cycles.samples=16
scn.render.resolution_x=640; scn.render.resolution_y=360
scn.frame_set(1); bpy.context.view_layer.update()
cam = scn.camera
cam.location = (-1.5, 0, 1.0)
d = Vector((0,0,0.5)) - cam.location
cam.rotation_euler = d.to_track_quat('-Z','Y').to_euler()
bpy.context.view_layer.update()
scn.render.filepath = "/tmp/tpose_test.png"
bpy.ops.render.render(write_still=True)
print("TPOSE RENDERED", flush=True)
