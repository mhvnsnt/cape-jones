"""Visual gate: two renders from stage1 file.
A) cape ONLY at frame 40 (armature pose) - silhouette coverage check
B) body ONLY (cape hidden) at frame 40 - suit integrity / no cape left behind
"""
import bpy
import mathutils

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/capebake-work/stage1_separated.blend")
scene = bpy.context.scene
scene.frame_set(40)
cape = bpy.data.objects["CapeJones_Cape"]
body = bpy.data.objects["CapeJones_Body"]

cam_data = bpy.data.cameras.new("GateCam")
cam = bpy.data.objects.new("GateCam", cam_data)
scene.collection.objects.link(cam)
cam.location = (1.1, 0.1, 1.25)
target = mathutils.Vector((2.95, 2.05, 0.5))
cam.rotation_euler = (target - cam.location).to_track_quat('-Z', 'Y').to_euler()
scene.camera = cam
scene.render.engine = 'CYCLES'
scene.cycles.samples = 2
scene.cycles.device = 'CPU'
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 50

# hide everything except body+cape first
keep = {cape.name, body.name, "RoomLight", "RimLight", "HallLight", "LampCone_Floor", "LampCone_Table"}
for o in bpy.data.objects:
    if o.type in ('MESH', 'LIGHT'):
        o.hide_render = o.name not in keep

body.hide_render = True
cape.hide_render = False
scene.render.filepath = "/home/hatch/workspace/capebake-work/gate_cape_only.png"
bpy.ops.render.render(write_still=True)
print("RENDERED gate_cape_only", flush=True)

body.hide_render = False
cape.hide_render = True
scene.render.filepath = "/home/hatch/workspace/capebake-work/gate_body_only.png"
bpy.ops.render.render(write_still=True)
print("RENDERED gate_body_only", flush=True)
print("GATE DONE", flush=True)
