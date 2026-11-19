import bpy, os
from mathutils import Vector

sc = bpy.context.scene
pat = bpy.data.objects.get("CapePatches")
if pat is not None:
    bpy.data.objects.remove(pat, do_unlink=True)
    print("PATCHES_REMOVED")
sc.render.image_settings.file_format = "PNG"
sc.render.resolution_x = 640; sc.render.resolution_y = 360
bpy.ops.object.camera_add()
cam = bpy.context.active_object; cam.data.lens = 55; sc.camera = cam
loc = Vector((0, 0.9, 0.35)); tgt = Vector((0, 0.08, 0.18))
cam.location = loc
cam.rotation_euler = (tgt - loc).to_track_quat("-Z", "Y").to_euler()
sc.frame_set(33)
sc.render.filepath = "/home/hatch/workspace/_cj-dance3d-v2/check/v2_hem33_nopatch.png"
bpy.ops.render.render(write_still=True)
print("HEM_NOPATCH_DONE")
