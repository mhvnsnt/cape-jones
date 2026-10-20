"""Test pelvis translation measuring full 3D."""
import bpy
from mathutils import Vector, Quaternion
scn = bpy.context.scene
rig = bpy.data.objects.get("CapeJones_Rig")
body = bpy.data.objects.get("CapeJones_Body")
for b in rig.pose.bones: b.rotation_mode='QUATERNION'
def butt_mean():
    bpy.context.view_layer.update()
    deps=bpy.context.evaluated_depsgraph_get()
    pm=body.evaluated_get(deps); mesh=pm.to_mesh(); mw=pm.matrix_world
    gi=body.vertex_groups["pelvis"].index
    pts=[mw@v.co for v in mesh.vertices for g in v.groups
         if g.group==gi and g.weight>0.6 and v.co.z<0.5]
    pm.to_mesh_clear()
    s=Vector((0,0,0))
    for p in pts: s+=p
    return s/len(pts)
m0=butt_mean()
print(f"before: ({m0.x:.4f},{m0.y:.4f},{m0.z:.4f})", flush=True)
rig.pose.bones['pelvis'].location=Vector((0,0,0.1))
m1=butt_mean()
print(f"pelvis loc (0,0,0.1): ({m1.x:.4f},{m1.y:.4f},{m1.z:.4f}) delta=({m1.x-m0.x:.4f},{m1.y-m0.y:.4f},{m1.z-m0.z:.4f})", flush=True)
print("DONE", flush=True)
