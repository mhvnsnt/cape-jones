"""LANE 1 CAPE REBUILD — pose/shoulder analysis.
Reports: key bone head/tail world positions (shoulders, neck, hips),
body back-surface y at several z heights (to place the cape sheet),
and the cape fragment union vs body overlap."""
import bpy
from mathutils import Vector

rig = bpy.data.objects['CapeJones_Rig']
bpy.context.view_layer.objects.active = rig

print("KEY BONE WORLD POSITIONS (posed):")
for bn in ['root', 'pelvis', 'spine_1', 'spine_2', 'chest', 'neck_1', 'neck_2', 'head',
           'clavicle_L', 'clavicle_R', 'upperarm_L', 'upperarm_R',
           'thigh_L', 'thigh_R', 'foot_L', 'foot_R']:
    b = rig.pose.bones.get(bn)
    if b:
        h = rig.matrix_world @ b.head
        t = rig.matrix_world @ b.tail
        print(f"  {bn:14s} head=({h.x:.3f},{h.y:.3f},{h.z:.3f}) tail=({t.x:.3f},{t.y:.3f},{t.z:.3f})")

body = bpy.data.objects['CapeJones_Body']
me = body.data
mw = body.matrix_world
print("\nBODY BACK SURFACE (max y) per z-band:")
for z0 in [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.60, 0.70, 0.75, 0.80]:
    ys = []
    for v in me.vertices:
        w = mw @ v.co
        if abs(w.z - z0) < 0.02:
            ys.append(w.y)
    if ys:
        print(f"  z~{z0:.2f}: max_y(back)={max(ys):.3f}  min_y(front)={min(ys):.3f}  n={len(ys)}")

cape = bpy.data.objects['CapeJones_Cape']
cme = cape.data
cmw = cape.matrix_world
print("\nCAPE vs BODY: fragment verts inside body bbox?")
bx = [ (mw @ v.co).x for v in me.vertices ]; by = [(mw @ v.co).y for v in me.vertices]; bz=[(mw @ v.co).z for v in me.vertices]
bx0,bx1,by0,by1,bz0,bz1 = min(bx),max(bx),min(by),max(by),min(bz),max(bz)
inside = 0; total = len(cme.vertices)
for v in cme.vertices:
    w = cmw @ v.co
    if bx0 <= w.x <= bx1 and by0 <= w.y <= by1 and bz0 <= w.z <= bz1:
        inside += 1
print(f"  body bbox x[{bx0:.3f},{bx1:.3f}] y[{by0:.3f},{by1:.3f}] z[{bz0:.3f},{bz1:.3f}]")
print(f"  cape verts inside body bbox: {inside}/{total} ({100*inside/total:.1f}%)")
