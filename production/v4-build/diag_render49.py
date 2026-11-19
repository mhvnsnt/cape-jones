import bpy, os
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/_cj_v4_build/scene_v4.blend")
sc = bpy.context.scene
sc.render.image_settings.file_format = "PNG"
sc.render.resolution_x = 960; sc.render.resolution_y = 540
for f in (47, 49, 51):
    sc.frame_set(f)
    sc.render.filepath = f"/home/hatch/workspace/_cj_v4_build/check/zoom_f{f}.png"
    bpy.ops.render.render(write_still=True)
    print("rendered", f, os.path.getsize(sc.render.filepath))
