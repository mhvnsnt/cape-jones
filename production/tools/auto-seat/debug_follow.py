"""Minimal test: does moving root.location move the proxy butt verts?"""
import bpy
from mathutils import Vector, Quaternion
scn = bpy.context.scene
rig = bpy.data.objects.get("CapeJones_Rig")
body = bpy.data.objects.get("CapeJones_Body")
# make a tiny proxy (no decimate, just 1k verts via mask? no — use full body, 1 eval)
for b in rig.pose.bones: b.rotation_mode='QUATERNION'
root = rig.pose.bones['root']
# simple pose: clear all
for b in rig.pose.bones:
    b.location=Vector((0,0,0))
for b in rig.pose.bones:
    if b.rotation_mode=='QUATERNION':
        b.rotation_quaternion=Quaternion((1,0,0,0))
bpy.context.view_layer.update()
deps=bpy.context.evaluated_depsgraph_get()
def butt_min():
    pm=body.evaluated_get(deps); mesh=pm.to_mesh(); mw=pm.matrix_world
    gi=body.vertex_groups["pelvis"].index
    zs=[]
    for v in mesh.vertices:
        for g in v.groups:
            if g.group==gi and g.weight>0.6 and mesh.vertices[v.index].co.z<0.5:
                zs.append((mw@v.co).z); break
    pm.to_mesh_clear()
    return min(zs) if zs else None
print(f"before: butt_min={butt_min():.4f}", flush=True)
root.location=Vector((0,0,0.1))
bpy.context.view_layer.update()
deps=bpy.context.evaluated_depsgraph_get()
print(f"after +0.1z: butt_min={butt_min():.4f}", flush=True)
print("TEST DONE", flush=True)
