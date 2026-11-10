import bpy,sys; sys.path.insert(0,__import__("os").environ.get("CJ_TOOLS","/workspace/cj3d/v2")); import cj_retarget as R, cj_scene as S
glb,sf,out=sys.argv[-3],int(sys.argv[-2]),sys.argv[-1]
tgt=bpy.data.objects["CapeJones_Rig"]; src=R.import_src(glb); R.prep_target(tgt); R.bake(tgt,src,[sf],[1])
for v in ("front","side"):
    for o in [o for o in bpy.data.objects if o.name.startswith(("SetFloor","cam","key","fill","rim"))]: bpy.data.objects.remove(o)
    S.setup(v,pct=50); bpy.context.scene.frame_set(1); bpy.context.scene.render.filepath=f"{out}_{v}.png"; bpy.ops.render.render(write_still=True)
