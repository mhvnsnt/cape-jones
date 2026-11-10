"""Clean collision proxies for cloth: one ellipsoid per body bone, sized from the Cape body mesh itself
(verts whose dominant weight is that bone, 85th percentile extent in bone-local X/Z, full length along Y),
parented to the bone. Replaces the decimated fragment-shell collision body (bad normals -> cloth pushed up/through)."""
import bpy, numpy as np
BONES=["pelvis","spine_1","spine_2","chest","thigh_L","shin_L","thigh_R","shin_R","upperarm_L","forearm_L","upperarm_R","forearm_R","neck_1","head"]
def build(rig,body,thick=0.002):
    me=body.data; n=len(me.vertices); co=np.zeros(n*3); me.vertices.foreach_get("co",co); co=co.reshape(-1,3)
    gi={g.name:g.index for g in body.vertex_groups}; want={gi[b]:b for b in BONES if b in gi}
    dom=np.full(n,-1)
    best=np.zeros(n)
    for v in me.vertices:
        for g in v.groups:
            if g.group in want and g.weight>best[v.index]: best[v.index]=g.weight; dom[v.index]=g.group
    excl=set(np.where(np.array([g.name=="cape_hi_sel" for g in body.vertex_groups]))[0])
    capesel=np.zeros(n,bool)
    if "cape_hi_sel" in gi:
        ci=gi["cape_hi_sel"]
        for v in me.vertices:
            for g in v.groups:
                if g.group==ci and g.weight>0.5: capesel[v.index]=True
    out=[]
    for g,b in want.items():
        sel=(dom==g)&(best>0.5)&~capesel
        if sel.sum()<50: continue
        bb=rig.data.bones[b]; M=np.array(bb.matrix_local); inv=np.linalg.inv(M)
        L=(inv[:3,:3]@co[sel].T).T+inv[:3,3]
        y0,y1=np.percentile(L[:,1],[2,98]); rx=np.percentile(np.abs(L[:,0]),85); rz=np.percentile(np.abs(L[:,2]),85)
        cx=np.median(L[:,0]); cz=np.median(L[:,2])
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=10,radius=1)
        o=bpy.context.object; o.name="ColCap_"+b
        o.scale=(rx,(y1-y0)/2,rz); o.location=(cx,(y0+y1)/2,cz)
        o.parent=rig; o.parent_type='BONE'; o.parent_bone=b
        # parent_type BONE places child at bone TAIL with bone-space axes; compensate by matrix_world
        o.matrix_world=rig.matrix_world@bb.matrix_local@__import__('mathutils').Matrix.LocRotScale(((cx,(y0+y1)/2,cz)),None,(rx,(y1-y0)/2,rz))
        o.modifiers.new("Collision",'COLLISION'); o.collision.thickness_outer=thick; o.collision.cloth_friction=1.0; o.collision.damping=0.2
        o.hide_render=True; out.append((b,round(rx,3),round(rz,3),round(y1-y0,3)))
    return out
