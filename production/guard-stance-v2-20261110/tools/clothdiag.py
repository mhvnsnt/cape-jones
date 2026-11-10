import bpy,numpy as np,sys
mode=sys.argv[-1]; sc=bpy.context.scene; p=bpy.data.objects["CapeClothProxy"]; cl=p.modifiers["Cloth"]
for k in ("CapeJones_Body","CapeJones_CapeHi","CapeJones_Cape"): bpy.data.objects[k].hide_viewport=True
pc=cl.point_cache; pc.use_disk_cache=False
with bpy.context.temp_override(scene=sc,point_cache=pc): bpy.ops.ptcache.free_bake()
col=bpy.data.objects["CapeCollisionBody"]
if "nocol" in mode: col.modifiers["Collision"].show_viewport=False
if "noself" in mode: cl.collision_settings.use_self_collision=False
if "rest" in mode: bpy.data.objects["CapeJones_Rig"].data.pose_position='REST'
if "thin" in mode:
    col.collision.thickness_outer=0.0015; cl.collision_settings.distance_min=0.0015
if "fric0" in mode:
    col.collision.cloth_friction=0; cl.collision_settings.friction=0; cl.settings.time_scale=1.0
if "selfon" in mode:
    cl.collision_settings.use_self_collision=True; cl.collision_settings.self_distance_min=0.0015; cl.collision_settings.self_friction=0
if "caps" in mode:
    col.modifiers["Collision"].show_viewport=False
    sys.path.insert(0,__import__("os").environ.get("CJ_TOOLS","/workspace/cj3d/v2")); import capsules
    rg=bpy.data.objects["CapeJones_Rig"]; pp=rg.data.pose_position; rg.data.pose_position='REST'; bpy.context.view_layer.update()
    print("CAPS",capsules.build(rg,bpy.data.objects["CapeJones_Body"])); rg.data.pose_position=pp
    cl.collision_settings.distance_min=0.002
if "heavy" in mode:
    cl.settings.bending_stiffness=5; cl.settings.air_damping=0.3; cl.settings.tension_stiffness=40; cl.settings.compression_stiffness=40
print("GRAV",sc.gravity[:],sc.use_gravity,"field",cl.settings.effector_weights.gravity)
for f in range(1,int(dict(a.split("=") for a in ["n=31"]+[x for x in mode.split("_") if "=" in x])["n"])):
    sc.frame_set(f)
    if f%5==0:
        m=p.evaluated_get(bpy.context.evaluated_depsgraph_get()).data; c=np.array([v.co[:] for v in m.vertices])
        rg=bpy.data.objects["CapeJones_Rig"]; pel=rg.matrix_world@rg.pose.bones["pelvis"].matrix
        inv=np.array(pel.inverted()); L=(inv[:3,:3]@c.T).T+inv[:3,3]
        lo=np.sort(L[:,1])[:max(1,len(L)//10)].mean(); print("F",mode,f,"hang_below_pelvis %.3f zmin %.3f"%(-lo,c[:,2].min()))
