import bpy
import mathutils
import sys

# usage: --python render-strip.py -- <ymin> <ymax> <blend> <outname>
argv = sys.argv[sys.argv.index("--") + 1:]
ymin = float(argv[0])
ymax = float(argv[1])
blend = argv[2]
outname = argv[3]

bpy.ops.wm.open_mainfile(filepath=blend)
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
scene.cycles.samples = 24
scene.cycles.device = 'CPU'
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.use_border = True
scene.render.use_crop_to_border = False
scene.render.border_min_y = ymin
scene.render.border_max_y = ymax
scene.render.border_min_x = 0.0
scene.render.border_max_x = 1.0
scene.render.filepath = outname
bpy.ops.render.render(write_still=True)
print("STRIP DONE", ymin, ymax, scene.render.filepath)
