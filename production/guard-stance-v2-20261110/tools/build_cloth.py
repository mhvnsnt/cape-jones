"""Cape cloth rig for Cape Jones (on rig_v2_arms.blend). The visible cape is ~100 Tripo fragment islands fused
into CapeJones_Body (plus the static CapeJones_Cape panel) -> not simulatable directly. Standard pro setup:
 1 low-res cloth PROXY sheet fitted to the cape surface (sim mesh), top band pinned to collar/shoulders via
   armature weights transferred from the body;
 2 decimated, armature-driven COLLISION body (torso, arms, legs) ;
 3 hi-res cape fragments separated (body copy) and driven by the proxy with SURFACE DEFORM; body hides them with a MASK.
Usage: blender -b rig_v2_arms.blend --python build_cloth.py -- STANCE.glb OUT.blend [NLOOPMOTIONFRAMES]"""
import bpy, bmesh, numpy as np, sys, math
sys.path.insert(0,"/workspace/cj3d/v2"); import cj_retarget as R
glb,OUT=sys.argv[-2],sys.argv[-1]
sc=bpy.context.scene; rig=bpy.data.objects["CapeJones_Rig"]; body=bpy.data.objects["CapeJones_Body"]; me=body.data
n=len(me.vertices); co=np.zeros(n*3); me.vertices.foreach_get("co",co); co=co.reshape(-1,3)
lab=np.load("/workspace/cj3d/v2/body_islands.npy"); lum=np.load("/workspace/cj3d/v2/body_texcol.npy").mean(1)
cnt=np.bincount(lab); ml=np.bincount(lab,lum)/cnt; my=np.bincount(lab,co[:,1])/cnt
capeisl=np.where((ml<0.15)&(my>0.02)&(cnt>=50))[0]; capev=np.isin(lab,capeisl)
print("CAPE islands",len(capeisl),"verts",int(capev.sum()))
# vertex group marking separated cape verts, body masks them out (non-destructive)
g=body.vertex_groups.new(name="cape_hi_sel"); g.add(np.where(capev)[0].tolist(),1.0,'REPLACE')
mk=body.modifiers.new("HideCapeHi",'MASK'); mk.vertex_group="cape_hi_sel"; mk.invert_vertex_group=True
bpy.ops.object.select_all(action='DESELECT')
# Mask stays LAST (after CorrectiveSmooth) so vertex counts match
# --- hi-res cape copy
def sub_copy(name,keep):
    d=me.copy(); o=bpy.data.objects.new(name,d); sc.collection.objects.link(o)
    bm=bmesh.new(); bm.from_mesh(d); bm.verts.ensure_lookup_table()
    bmesh.ops.delete(bm,geom=[bm.verts[i] for i in np.where(~keep)[0]],context='VERTS'); bm.to_mesh(d); bm.free()
    return o
capehi=sub_copy("CapeJones_CapeHi",capev)
for gg in list(capehi.vertex_groups): capehi.vertex_groups.remove(gg)
# --- proxy sheet
cc=co[capev]; X=np.linspace(-0.25,0.25,35); Z=np.linspace(0.06,0.80,50)
grid=np.full((len(Z),len(X)),np.nan)
for j,z in enumerate(Z):
    band=cc[np.abs(cc[:,2]-z)<0.012]
    for i,x in enumerate(X):
        s=band[np.abs(band[:,0]-x)<0.012]
        if len(s)>=8: grid[j,i]=np.percentile(s[:,1],92)+0.004
keep=~np.isnan(grid)
# fill holes inside rows (between leftmost/rightmost valid) by interpolation
for j in range(len(Z)):
    v=np.where(keep[j])[0]
    if len(v)>=2:
        a,b=v[0],v[-1]; grid[j,a:b+1]=np.interp(np.arange(a,b+1),v,grid[j,v]); keep[j,a:b+1]=True
pv=[];idx=-np.ones(keep.shape,int)
for j in range(len(Z)):
    for i in range(len(X)):
        if keep[j,i]: idx[j,i]=len(pv); pv.append((X[i],grid[j,i],Z[j]))
faces=[]
for j in range(len(Z)-1):
    for i in range(len(X)-1):
        q=[idx[j,i],idx[j,i+1],idx[j+1,i+1],idx[j+1,i]]
        if min(q)>=0: faces.append(q)
pm=bpy.data.meshes.new("CapeProxy"); pm.from_pydata(pv,[],faces); pm.update()
# drop verts not used by faces
bm=bmesh.new(); bm.from_mesh(pm); bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS'); bm.to_mesh(pm); bm.free()
proxy=bpy.data.objects.new("CapeClothProxy",pm); sc.collection.objects.link(proxy)
P=np.array([v.co[:] for v in pm.vertices]); print("PROXY verts",len(P),"faces",len(pm.polygons))
ztop=P[:,2].max()
pin=proxy.vertex_groups.new(name="pin")
for k,p in enumerate(P):
    w=float(np.clip((p[2]-(ztop-0.07))/0.04,0,1))
    if w>0: pin.add([k],w,'REPLACE')
# armature weights for proxy from body via DataTransfer (nearest face interpolated)
for vg in body.vertex_groups:
    if vg.name not in("cape_hi_sel","cape_mask"): proxy.vertex_groups.new(name=vg.name)
dt=proxy.modifiers.new("dt",'DATA_TRANSFER'); dt.object=body; dt.use_vert_data=True; dt.data_types_verts={'VGROUP_WEIGHTS'}
dt.vert_mapping='POLYINTERP_NEAREST'; dt.layers_vgroup_select_src='ALL'; dt.layers_vgroup_select_dst='NAME'
rig.data.pose_position='REST'; bpy.context.view_layer.update()
with bpy.context.temp_override(object=proxy,active_object=proxy): bpy.ops.object.modifier_apply(modifier="dt")
for nm in [v.name for v in proxy.vertex_groups if any(t in v.name for t in ("upperarm","forearm","hand","finger","blaster","head","neck","jaw"))]:
    proxy.vertex_groups.remove(proxy.vertex_groups[nm])
am=proxy.modifiers.new("Armature",'ARMATURE'); am.object=rig
cl=proxy.modifiers.new("Cloth",'CLOTH'); s=cl.settings; c=cl.collision_settings
s.quality=16; s.mass=0.06; s.air_damping=1.2; s.tension_stiffness=20; s.compression_stiffness=20; s.shear_stiffness=8
s.bending_stiffness=0.6; s.tension_damping=5; s.compression_damping=5; s.shear_damping=5; s.bending_damping=0.5
s.vertex_group_mass="pin"; s.pin_stiffness=1.0; s.time_scale=0.73
c.collision_quality=8; c.distance_min=0.005; c.use_self_collision=True; c.self_distance_min=0.002; c.self_friction=2; c.friction=2
# --- collision body: non-cape body, decimated at rest, armature driven
colm=sub_copy("CapeCollisionBody",~capev); 
for mm in list(colm.modifiers): colm.modifiers.remove(mm)
dc=colm.modifiers.new("dec",'DECIMATE'); dc.ratio=0.012
with bpy.context.temp_override(object=colm,active_object=colm): bpy.ops.object.modifier_apply(modifier="dec")
print("COLLISION verts",len(colm.data.vertices))
a2=colm.modifiers.new("Armature",'ARMATURE'); a2.object=rig; colm.modifiers.new("Collision",'COLLISION')
colm.collision.thickness_outer=0.007; colm.collision.cloth_friction=2; colm.collision.damping=0.3; colm.hide_render=True
proxy.hide_render=True
# --- motion: rest(1) -> guard first frame (40), hold to 50 (settle), guard loop x2 from 51
rig.data.pose_position='POSE'
src=R.import_src(glb); R.prep_target(rig); f0,f1=src.animation_data.action.frame_range; N=int(f1-f0)
for t in [b for _,b in R.M]:
    pb=rig.pose.bones[t]; pb.rotation_quaternion=(1,0,0,0); pb.location=(0,0,0)
    pb.keyframe_insert("rotation_quaternion",frame=1); pb.keyframe_insert("location",frame=1)
SF=[int(f0)]*2+[int(f0)+(k%N) for k in range(2*N)]; DF=[40,50]+list(range(51,51+2*N))
R.bake(rig,src,SF,DF)
sc.frame_start=1; sc.frame_end=DF[-1]
cache=cl.point_cache; cache.frame_start=1; cache.frame_end=DF[-1]
# --- surface deform hi-res cape + static panel onto proxy, bound at frame 1 (rest)
sc.frame_set(1); bpy.context.view_layer.update()
for o in (capehi,bpy.data.objects["CapeJones_Cape"]):
    sd=o.modifiers.new("SurfDef",'SURFACE_DEFORM'); sd.target=proxy; sd.falloff=4.0
    with bpy.context.temp_override(object=o,active_object=o): bpy.ops.object.surfacedeform_bind(modifier="SurfDef")
    print("BOUND",o.name,sd.is_bound)
bpy.ops.wm.save_as_mainfile(filepath=OUT,compress=True)
cache.use_disk_cache=True
heavy=[bpy.data.objects[k] for k in ("CapeJones_Body","CapeJones_CapeHi","CapeJones_Cape","BlenRigMdefCage")]
for o in heavy: o.hide_viewport=True   # cloth bake needs only rig+proxy+collision body
with bpy.context.temp_override(scene=sc,point_cache=cache): bpy.ops.ptcache.bake(bake=True)
for o in heavy: o.hide_viewport=False
bpy.data.objects["BlenRigMdefCage"].hide_viewport=True
bpy.ops.wm.save_mainfile(compress=True)
print("BAKED",cache.is_baked,"frames",DF[-1],"SAVED",OUT)
