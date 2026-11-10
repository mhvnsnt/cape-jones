#!/usr/bin/env python3
# Blender 5.2 EEVEE volumetric god-ray background, portrait 1100x1500.
# Run: blender -b --python blender_godrays.py -- /tmp/godray-bg.png
import bpy, sys, math
out = sys.argv[-1]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'BLENDER_EEVEE'
sc.render.resolution_x = 550; sc.render.resolution_y = 750
sc.render.resolution_percentage = 100
sc.render.film_transparent = False
sc.render.filepath = out
# world: near-black blue
w = bpy.data.worlds.new("W"); w.use_nodes = True
bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.01, 0.02, 0.05, 1)
sc.world = w
# camera looking +Y from y=-9
bpy.ops.object.camera_add(location=(0, -9, 2.5), rotation=(math.radians(90), 0, 0))
sc.camera = bpy.context.object
# volume cube between back light and camera
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 2.5))
vol = bpy.context.object; vol.scale = (5, 5, 4)
mat = bpy.data.materials.new("Vol"); mat.use_nodes = True
nt = mat.node_tree; nt.nodes.clear()
pv = nt.nodes.new("ShaderNodeVolumePrincipled")
pv.inputs["Density"].default_value = 0.12
pv.inputs["Color"].default_value = (0.2, 0.9, 1.0, 1)
outn = nt.nodes.new("ShaderNodeOutputMaterial")
nt.links.new(pv.outputs[0], outn.inputs["Volume"])
vol.data.materials.append(mat)
# cyan spot behind subject, pointing toward camera (-Y)
bpy.ops.object.light_add(type='SPOT', location=(0, 5, 5))
spot = bpy.context.object
spot.data.energy = 800; spot.data.color = (0.2, 0.9, 1.0)
spot.data.spot_size = math.radians(70); spot.data.spot_blend = 0.5
spot.rotation_euler = (math.radians(115), 0, 0)
# dark pillars to break light into shafts
for x in (-2.2, 0.0, 2.2):
    bpy.ops.mesh.primitive_cube_add(size=2, location=(x, 2.5, 2.5))
    p = bpy.context.object; p.scale = (0.5, 0.5, 4)
    pm = bpy.data.materials.new("Dark"); pm.use_nodes = True
    bsdf = pm.node_tree.nodes["Principled BSDF"]; bsdf.inputs["Base Color"].default_value = (0, 0, 0, 1)
    p.data.materials.append(pm)
bpy.ops.render.render(write_still=True)
print("BLENDER_DONE", out)
