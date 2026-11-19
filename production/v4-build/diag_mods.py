import bpy, os
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/_cj_v4_build/scene_v4.blend")
sc = bpy.context.scene
body = bpy.data.objects["BodyR"]
print("MODS", [(m.name, m.type) for m in body.modifiers])
for m in body.modifiers:
    if m.type == "CORRECTIVE_SMOOTH":
        m.show_viewport = False; m.show_render = False
sc.render.image_settings.file_format = "PNG"
sc.render.resolution_x = 960; sc.render.resolution_y = 540
sc.frame_set(49)
sc.render.filepath = "/home/hatch/workspace/_cj_v4_build/check/zoom_f49_nocs.png"
bpy.ops.render.render(write_still=True)
print("rendered", os.path.getsize(sc.render.filepath))
