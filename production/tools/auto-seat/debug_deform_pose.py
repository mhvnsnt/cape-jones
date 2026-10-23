"""Minimal: pose deform bones, verify mesh follows. No proxy, no FBX, no render."""
import bpy
from mathutils import Vector, Quaternion
scn = bpy.context.scene
rig = bpy.data.objects.get("CapeJones_Rig")
body = bpy.data.objects.get("CapeJones_Body")
for b in rig.pose.bones: b.rotation_mode='QUATERNION'
# rotate deform thigh_L 45 deg (should lift leg)
rig.pose.bones['thigh_L'].rotation_quaternion=Quaternion((1,0,0), 0.785)
bpy.context.view_layer.update()
deps=bpy.context.evaluated_depsgraph_get()
pm=body.evaluated_get(deps); mesh=pm.to_mesh(); mw=pm.matrix_world
# find lowest vert
minz=min((mw@v.co).z for v in mesh.vertices)
pm.to_mesh_clear()
print(f"thigh_L rotated: min_z={minz:.4f}", flush=True)
# reset
rig.pose.bones['thigh_L'].rotation_quaternion=Quaternion((1,0,0,0))
bpy.context.view_layer.update()
print("DONE", flush=True)
