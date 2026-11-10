"""Volumetric god-ray base render, Blender 5.2.3, Cycles CPU.
Dual-light COMBINED case only: cyan back light + warm gold front key.
Scene: camera looking down -Z? Camera at (0,0,6) looking at origin.
Volume cube encloses scene. Cyan spot BEHIND (z=-3) pointing to camera,
dark pillars between spot and camera break light into shafts.
Warm point light in FRONT (z=4) gives warm front glow.
No character in 3D scene: plate is composited in the second pass.
"""
import bpy, math
print("VOLUM BASE START")
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 32
scene.cycles.use_denoising = True
try:
    scene.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception as e:
    print('denoiser set failed', e)
scene.render.resolution_x = 640
scene.render.resolution_y = 360
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = '/home/hatch/workspace/cape-jones-rig/blender-composite-fix-20261031/scratch/volumetric-base-20261031.png'
scene.render.use_compositing = False
# World dark
world = bpy.data.worlds.new("DarkWorld")
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs[0].default_value = (0.01, 0.01, 0.03, 1.0)
    bg.inputs[1].default_value = 1.0
scene.world = world
# Camera
bpy.ops.object.camera_add(location=(0, 0, 6), rotation=(0, 0, 0))
cam = bpy.context.active_object
cam.data.lens = 50
scene.camera = cam
# Volume cube
bpy.ops.mesh.primitive_cube_add(size=12, location=(0, 0, 0))
vol = bpy.context.active_object
vol.name = "VolumeCube"
mat = bpy.data.materials.new("VolumeScatter")
mat.use_nodes = True
nt = mat.node_tree
nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputMaterial")
scatter = nt.nodes.new("ShaderNodeVolumeScatter")
scatter.inputs['Color'].default_value = (0.10, 0.35, 0.45, 1.0)
scatter.inputs['Density'].default_value = 0.18
scatter.inputs['Anisotropy'].default_value = 0.0
nt.links.new(scatter.outputs['Volume'], out.inputs['Volume'])
vol.data.materials.append(mat)
# Pillars (occluders) between spot and camera
for x, w in [(-2.2, 0.9), (-0.6, 0.7), (1.0, 1.1), (2.4, 0.8)]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, -1))
    p = bpy.context.active_object
    p.dimensions = (w, 10, 0.5)
    pm = bpy.data.materials.new(f"Pillar{x}")
    pm.use_nodes = True
    bsdf = pm.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.0, 0.0, 0.0, 1.0)
        bsdf.inputs['Roughness'].default_value = 1.0
    p.data.materials.append(pm)
# Cyan spot behind, pointing toward camera (+Z)
bpy.ops.object.light_add(type='SPOT', location=(0, 0.5, -3))
spot = bpy.context.active_object
spot.name = "CyanBackSpot"
spot.data.color = (0.2, 0.9, 1.0)
spot.data.energy = 12000
spot.data.spot_size = 1.2
spot.data.spot_blend = 0.3
# Point spot at origin: spot default points down -Z; rotate 180 deg about X to point +Z
spot.rotation_euler = (math.radians(180), 0, 0)
# Warm point front (camera side)
bpy.ops.object.light_add(type='POINT', location=(0, 1, 4))
pt = bpy.context.active_object
pt.name = "WarmFrontPoint"
pt.data.color = (1.0, 0.75, 0.35)
pt.data.energy = 150
print("objects:", [o.name for o in bpy.data.objects])
print("rendering volumetric base...")
bpy.ops.render.render(write_still=True)
print("VOLUM BASE DONE")
