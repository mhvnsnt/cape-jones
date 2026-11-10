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
if "heavy" in mode:
    cl.settings.bending_stiffness=5; cl.settings.air_damping=0.3; cl.settings.tension_stiffness=40; cl.settings.compression_stiffness=40
print("GRAV",sc.gravity[:],sc.use_gravity,"field",cl.settings.effector_weights.gravity)
for f in range(1,int(dict(a.split("=") for a in ["n=31"]+[x for x in mode.split("_") if "=" in x])["n"])):
    sc.frame_set(f)
    if f%5==0:
        m=p.evaluated_get(bpy.context.evaluated_depsgraph_get()).data; c=np.array([v.co[:] for v in m.vertices]); print("F",mode,f,"zmin %.3f zmax %.3f ymin %.3f"%(c[:,2].min(),c[:,2].max(),c[:,1].min()))
