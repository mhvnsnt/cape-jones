import bpy,sys; sys.path.insert(0,__import__("os").environ.get("CJ_TOOLS","/workspace/cj3d/v2")); import cj_scene as S
a,b,out,pct=int(sys.argv[-4]),int(sys.argv[-3]),sys.argv[-2],int(sys.argv[-1])
sc=bpy.context.scene
if 'cj_arm_fix' not in bpy.data.objects['CapeJones_Rig'].data.keys(): raise SystemExit('REFUSED: raw w5r rig (H arms). Use guard_shot_pipeline.sh')
 S.setup("front3q",pct=pct)
for o in bpy.data.objects:
    if o.name in("CapeClothProxy","CapeCollisionBody","BlenRigMdefCage"): o.hide_render=True
sc.frame_start=a; sc.frame_end=b; sc.render.image_settings.file_format='PNG'; sc.render.filepath=out
bpy.ops.render.render(animation=True)
