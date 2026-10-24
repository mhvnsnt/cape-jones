"""Render-only proof: import the exported jungle-outpost.glb and render
the lower court through the west slot under the upper platform.
Usage: blender -b --python render_lower.py -- <glb> <out.png>
"""
import bpy, sys, os

argv = sys.argv[sys.argv.index("--") + 1:]
GLB, OUT = argv[0], argv[1]

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=GLB)

world = bpy.data.worlds.new("JungleSky")
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.62, 0.78, 0.88, 1.0)
bg.inputs["Strength"].default_value = 0.6
bpy.context.scene.world = world

tgt = bpy.data.objects.new("CamTarget_LowerWest", None)
bpy.context.collection.objects.link(tgt)
tgt.location = (2, 0, -4.0)
bpy.ops.object.camera_add(location=(-24, -3, -1.8))
cam = bpy.context.active_object
con = cam.constraints.new('TRACK_TO')
con.target = tgt
con.track_axis = 'TRACK_NEGATIVE_Z'
con.up_axis = 'UP_Y'

scene = bpy.context.scene
scene.camera = cam
scene.render.engine = 'CYCLES'
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.film_transparent = False
scene.cycles.device = 'CPU'
scene.cycles.samples = 32
scene.cycles.use_denoising = True
scene.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("RENDERED:", OUT)
