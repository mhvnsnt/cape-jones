import bpy,sys; sys.path.insert(0,__import__("os").environ.get("CJ_TOOLS","/workspace/cj3d/v2")); import cj_scene as S
out=sys.argv[-1]; frames=[int(x) for x in sys.argv[-2].split(",")]
sc=bpy.context.scene; print("BAKED",bpy.data.objects["CapeClothProxy"].modifiers["Cloth"].point_cache.is_baked)
for o in bpy.data.objects:
    if o.name.startswith(("ColCap_","CapeClothProxy","CapeCollisionBody")): o.hide_render=True
for v in ("front3q","side","back"):
    for o in [o for o in bpy.data.objects if o.name.startswith(("SetFloor","cam","key","fill","rim"))]: bpy.data.objects.remove(o)
    cam=S.setup("front3q" if v=="back" else v,pct=40)
    if v=="back": cam.location=(-0.6,2.8,0.55); from mathutils import Vector; cam.rotation_euler=(Vector((0,0,0.456))-cam.location).to_track_quat('-Z','Y').to_euler()
    for f in frames: sc.frame_set(f); sc.render.filepath=f"{out}_{v}_{f:03d}.png"; bpy.ops.render.render(write_still=True)
