"""Blender multiplane scene for BARS PRESET — scene construction only.

Run in Blender 5.2.3 (blender --background --python build_multiplane_blender.py).
This builds a camera + three planes at relative distances matching the PIL
parallax table (distance = 1/parallax): far 3.33, hero 1.0, foreground 0.56.
It does NOT claim a rendered frame: rendering is a separate step, run it
and report its own output if you want a Blender frame.
"""
import bpy

for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

scene = bpy.context.scene
scene.render.resolution_x, scene.render.resolution_y = 1100, 750

cam_data = bpy.data.cameras.new("MultiplaneCam")
cam = bpy.data.objects.new("MultiplaneCam", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
cam.location = (0, 0, 10)
cam.data.type = 'ORTHO'
cam.data.ortho_scale = 12.0

# planes: (name, relative distance, colour) — distance = 1/parallax
for name, dist, colour in [("FarBG", 3.33, (0.2, 0.4, 0.45, 1)),
                           ("HeroCape", 1.0, (0.9, 0.9, 0.9, 1)),
                           ("ForegroundBars", 0.56, (0.08, 0.07, 0.1, 1))]:
    bpy.ops.mesh.primitive_plane_add(size=14, location=(0, 0, 10 - dist))
    p = bpy.context.active_object
    p.name = name
    mat = bpy.data.materials.new(name + "Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = colour
    p.data.materials.append(mat)
    print(name, "distance", dist, "parallax", round(1 / dist, 2))

# camera lateral move: keyframes at frame 1 and 24, 120 px equivalent in
# ortho units (12 units across 1100 px -> 1.31 units)
cam.location.x = 0
cam.keyframe_insert(data_path="location", frame=1)
cam.location.x = 1.31
cam.keyframe_insert(data_path="location", frame=24)
scene.frame_start, scene.frame_end = 1, 24
bpy.ops.wm.save_as_mainfile(filepath="/home/hatch/workspace/cape-jones-rig/multiplane-upgrade-20261031/bars-preset-blender-20261031.blend")
print("BARS PRESET Blender scene saved; no render claimed.")
