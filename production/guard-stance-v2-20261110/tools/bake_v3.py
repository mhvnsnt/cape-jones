"""v3 cloth: same proxy/pins/surface-deform as rig_v2_cloth_b, but collision = clean per-bone ellipsoids
(capsules.py) instead of the decimated fragment shell; self-collision ON; friction 0 on cloth side; time_scale 1."""
import bpy,sys,numpy as np; sys.path.insert(0,__import__("os").environ.get("CJ_TOOLS","/workspace/cj3d/v2")); import capsules
OUT=sys.argv[-1]; sc=bpy.context.scene; p=bpy.data.objects["CapeClothProxy"]; cl=p.modifiers["Cloth"]; rg=bpy.data.objects["CapeJones_Rig"]
col=bpy.data.objects["CapeCollisionBody"]; col.modifiers["Collision"].show_viewport=False; col.modifiers["Collision"].show_render=False
rg.data.pose_position='REST'; bpy.context.view_layer.update(); print("CAPS",capsules.build(rg,bpy.data.objects["CapeJones_Body"])); rg.data.pose_position='POSE'
c=cl.collision_settings; c.use_self_collision=True; c.self_distance_min=0.0015; c.self_friction=0; c.friction=0; c.distance_min=0.002
cl.settings.time_scale=1.0
bpy.data.objects["BlenRigMdefCage"].hide_viewport=True
bpy.ops.wm.save_as_mainfile(filepath=OUT,compress=True)
# --- ground: per frame, shift pelvis vertically so the lowest sole touches z=0 (feet floated all shot in v1/v2)
from mathutils import Matrix
body=bpy.data.objects["CapeJones_Body"]; me=body.data; n=len(me.vertices)
co=np.zeros(n*3); me.vertices.foreach_get("co",co); co=co.reshape(-1,3)
fg={body.vertex_groups[b].index:b for b in ("foot_L","toe_L","foot_R","toe_R") if b in body.vertex_groups}
FV={b:[] for b in fg.values()}
for v in me.vertices:
    for g in v.groups:
        if g.group in fg and g.weight>0.6: FV[fg[g.group]].append(v.index)
FV={b:co[np.array(ix)] for b,ix in FV.items() if ix}
pb=rg.pose.bones["pelvis"]; DZ=[]
for f in range(1,289):
    sc.frame_set(f); bpy.context.view_layer.update(); lo=9
    for b,V in FV.items():
        bb=rg.pose.bones[b]; M=np.array(rg.matrix_world@bb.matrix@bb.bone.matrix_local.inverted())
        lo=min(lo,((M[:3,:3]@V.T).T+M[:3,3])[:,2].min())
    DZ.append(lo); pb.matrix=Matrix.Translation((0,0,-lo))@pb.matrix; bpy.context.view_layer.update(); pb.keyframe_insert("location",frame=f)
sc["cj_floor_z"]=0.0; print("GROUND dz range",min(DZ),max(DZ))
pc=cl.point_cache; pc.use_disk_cache=False
with bpy.context.temp_override(scene=sc,point_cache=pc): bpy.ops.ptcache.free_bake()
pc.use_disk_cache=True
heavy=[bpy.data.objects[k] for k in ("CapeJones_Body","CapeJones_CapeHi","CapeJones_Cape")]
for o in heavy: o.hide_viewport=True
with bpy.context.temp_override(scene=sc,point_cache=pc): bpy.ops.ptcache.bake(bake=True)
for o in heavy: o.hide_viewport=False
# floor: lowest evaluated sole over the shot (feet were floating in v1/v2)
body=bpy.data.objects["CapeJones_Body"]; zs=[]
for f in range(51,289,17):
    sc.frame_set(f); m=body.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
    a=np.zeros(len(m.vertices)*3); m.vertices.foreach_get("co",a); zs.append(a.reshape(-1,3)[:,2].min())
print("SOLE_MIN_AFTER_GROUND",[round(float(z),4) for z in zs])
bpy.ops.wm.save_mainfile(compress=True); print("BAKED",pc.is_baked)
