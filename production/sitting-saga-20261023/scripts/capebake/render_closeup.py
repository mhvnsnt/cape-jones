import bpy
import mathutils

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/capebake-work/scene_capebaked.blend")
scene = bpy.context.scene
scene.frame_set(40)
cam_data = bpy.data.cameras.new("closeup")
cam = bpy.data.objects.new("closeup", cam_data)
scene.collection.objects.link(cam)
cam.location = (2.15, 1.15, 0.85)
tgt = mathutils.Vector((2.92, 2.08, 0.55))
cam.rotation_euler = (tgt - cam.location).to_track_quat('-Z', 'Y').to_euler()
scene.camera = cam
scene.render.engine = 'CYCLES'
scene.cycles.samples = 4
scene.cycles.device = 'CPU'
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 50
scene.render.filepath = "/home/hatch/workspace/your_files/cape-bake/capebake_closeup_f40_v1.png"
bpy.ops.render.render(write_still=True)
print("CLOSEUP DONE", flush=True)
