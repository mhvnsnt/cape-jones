import bpy, math, os
from mathutils import Vector

BASE = "/home/hatch/workspace/cape-jones-rig/canonical-main-room-10-angles-20261101"
OUT = os.path.join(BASE, "angles")
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=os.path.join(BASE, "work/room/3d-assets/living_room.blend"))

# Hide character rig/body/cape for EMPTY plates, and any CapeJones objects
hidden = []
for o in bpy.data.objects:
    if "CapeJones" in o.name or o.name.startswith("Cape"):
        o.hide_render = True
        hidden.append(o.name)
print("HIDDEN_CHARACTER:", hidden)

# List cameras / main objects for log
print("OBJECTS:", [o.name for o in bpy.data.objects][:200])

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 12
scene.cycles.device = 'CPU'
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'

# Room centre approx: use MainCam info if present
# Cameras: (name, location, look_target)
# Blender axes in this scene: MainCam (0,-4.6,1.7) looks into room (+Y direction).
# TV is around (-0.9, 2.6), chair around (2.65, 2.31), window at x~3.5 wall, sofa at (-2.9,-0.6)
# So room spans roughly x -3.5..3.5, y -3..3, z 0..3.
angles = [
    ("angle-01-tv-facing-front", (0.0, -4.6, 1.7), (0.0, 2.0, 1.0)),   # MainCam: leveled, facing TV
    ("angle-02-chair-facing", (-1.0, 0.5, 1.4), (2.65, 2.31, 0.9)),      # looking towards chair
    ("angle-03-from-tv-side", (-0.9, 2.2, 1.6), (0.5, -2.0, 1.0)),       # from TV side back into room
    ("angle-04-from-window-side", (3.2, 1.5, 1.6), (-2.0, 0.0, 1.0)),   # from window side across
    ("angle-05-from-doorway", (-3.2, -1.5, 1.6), (1.5, 2.0, 1.0)),      # doorway/hallway side in
    ("angle-06-low-angle", (0.0, -3.5, 0.45), (0.5, 2.5, 1.2)),          # low, near floor
    ("angle-07-high-angle", (0.0, -3.0, 2.8), (0.5, 1.5, 0.4)),          # high, looking down
    ("angle-08-rug-chair-closeup", (0.8, 0.8, 1.2), (2.65, 2.31, 0.7)),  # rug + chair closeup
    ("angle-09-coffee-table-foreground", (-0.5, -2.0, 1.1), (1.5, 2.5, 0.9)),  # coffee table foreground
    ("angle-10-tv-stand-closeup", (0.8, 0.2, 1.3), (-0.9, 2.6, 1.0)),    # TV stand closeup
]

def look_at(cam_obj, target):
    direction = Vector(target) - cam_obj.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cam_obj.rotation_euler = rot_quat.to_euler()

# Remove any previous angle cameras
for o in list(bpy.data.objects):
    if o.name.startswith("AngleCam"):
        bpy.data.objects.remove(o, do_unlink=True)
for c in list(bpy.data.cameras):
    if c.name.startswith("AngleCam"):
        bpy.data.cameras.remove(c)

for name, loc, tgt in angles:
    cam_data = bpy.data.cameras.new(name="AngleCam_" + name)
    cam_data.lens = 50
    cam_obj = bpy.data.objects.new("AngleCam_" + name, cam_data)
    bpy.context.collection.objects.link(cam_obj)
    cam_obj.location = Vector(loc)
    look_at(cam_obj, tgt)
    scene.camera = cam_obj
    scene.render.filepath = os.path.join(OUT, name + "-20261101.png")
    bpy.ops.render.render(write_still=True)
    print("RENDERED", name, loc, "->", tgt)
print("DONE_10")
