"""Test: does rotating pelvis move the mesh?"""
import bpy
from mathutils import Vector, Quaternion
scn = bpy.context.scene
rig = bpy.data.objects.get("CapeJones_Rig")
body = bpy.data.objects.get("CapeJones_Body")
for b in rig.pose.bones: b.rotation_mode='QUATERNION'
def butt_min():
    bpy.context.view_layer.update()
    deps=bpy.context.evaluated_depsgraph_get()
    pm=body.evaluated_get(deps); mesh=pm.to_mesh(); mw=pm.matrix_world
    gi=body.vertex_groups["pelvis"].index
    zs=[(mw@v.co).z for v in mesh.vertices for g in v.groups
        if g.group==gi and g.weight>0.6 and v.co.z<0.5]
    pm.to_mesh_clear()
    return min(zs) if zs else None
print(f"rest: {butt_min():.4f}", flush=True)
# rotate pelvis 45 deg
rig.pose.bones['pelvis'].rotation_quaternion=Quaternion((0,0,1), 0.785)
print(f"pelvis rot: {butt_min():.4f}", flush=True)
# move pelvis bone location
rig.pose.bones['pelvis'].rotation_quaternion=Quaternion((1,0,0,0))
rig.pose.bones['pelvis'].location=Vector((0,0,0.1))
print(f"pelvis loc: {butt_min():.4f}", flush=True)
print("DONE", flush=True)
