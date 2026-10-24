import bpy
import mathutils

scene = bpy.context.scene
scene.frame_set(40)
if "FINALCAM" in bpy.data.objects:
    cam = bpy.data.objects["FINALCAM"]
else:
    cam_data = bpy.data.cameras.new("FINALCAM")
    cam = bpy.data.objects.new("FINALCAM", cam_data)
    scene.collection.objects.link(cam)
cam.location = (1.1, 0.1, 1.25)
target = mathutils.Vector((2.95, 2.05, 0.5))
cam.rotation_euler = (target - cam.location).to_track_quat('-Z', 'Y').to_euler()
scene.camera = cam

scene.render.engine = 'CYCLES'
scene.cycles.samples = 4
scene.cycles.device = 'CPU'
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 50
scene.render.use_border = False
scene.render.filepath = "/home/hatch/workspace/your_files/final-repaired/MERGE_check_f40_v1.png"
bpy.ops.render.render(write_still=True)
print("RENDERED", scene.render.filepath)
