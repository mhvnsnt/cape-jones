import bpy,sys; sys.path.insert(0,"/workspace/cj3d/v2"); import cj_retarget as R, cj_scene as S
out=sys.argv[-1]; sc=bpy.context.scene; tgt=bpy.data.objects["CapeJones_Rig"]
src=R.import_src("/workspace/cj3d/stance.glb"); R.prep_target(tgt); f0,f1=src.animation_data.action.frame_range; N=int(f1-f0)
R.bake(tgt,src,[int(f0)+k for k in range(N)],list(range(1,N+1)))
S.setup("front3q"); sc.frame_start=1; sc.frame_end=N; sc.render.image_settings.file_format='PNG'; sc.render.filepath=out
bpy.ops.render.render(animation=True)
