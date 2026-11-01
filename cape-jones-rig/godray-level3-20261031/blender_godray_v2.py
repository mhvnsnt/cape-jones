# Blender 5.2.3 EEVEE volumetric god-ray v2: BRIGHT cyan shafts (v1 was density 0.12 / spot 800, too weak).
# Methods: higher density, anisotropy forward-scatter, high-energy spots aimed at camera (Track To),
# thin occluder bars (shaft separation), dust motes in the volume, dark world for contrast.
import bpy, math, random
random.seed(31)
OUT = '/home/hatch/workspace/cape-jones-rig/godray-level3-20261031/godray-bg-v2-20261031.png'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'BLENDER_EEVEE'
sc.render.resolution_x = 550; sc.render.resolution_y = 750
sc.render.resolution_percentage = 100
sc.render.film_transparent = False
sc.render.filepath = OUT
try:
    sc.eevee.taa_render_samples = 32
except Exception as e:
    print("eevee samples note", e)
w = bpy.data.worlds.new("W"); w.use_nodes = True
bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.005, 0.01, 0.03, 1)
sc.world = w
bpy.ops.object.camera_add(location=(0, -9, 2.5), rotation=(math.radians(90), 0, 0))
sc.camera = bpy.context.object
cam = sc.camera
# volume cube
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 2.5))
vol = bpy.context.object; vol.scale = (6, 6, 5)
mat = bpy.data.materials.new("Vol"); mat.use_nodes = True
nt = mat.node_tree; nt.nodes.clear()
pv = nt.nodes.new("ShaderNodeVolumePrincipled")
pv.inputs["Density"].default_value = 0.35
pv.inputs["Anisotropy"].default_value = 0.6
pv.inputs["Color"].default_value = (0.2, 0.9, 1.0, 1)
outn = nt.nodes.new("ShaderNodeOutputMaterial")
nt.links.new(pv.outputs[0], outn.inputs["Volume"])
vol.data.materials.append(mat)
# target empty at camera for spot tracking
bpy.ops.object.empty_add(location=(0, -9, 2.5))
target = bpy.context.object
def spot(name, loc, energy, size_deg, color):
    bpy.ops.object.light_add(type='SPOT', location=loc)
    s = bpy.context.object; s.name = name
    s.data.energy = energy; s.data.color = color
    s.data.spot_size = math.radians(size_deg); s.data.spot_blend = 0.4
    c = s.constraints.new('TRACK_TO'); c.target = target; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
    return s
spot("SpotCyanMain", (0, 5, 6), 8000, 60, (0.2, 0.9, 1.0))
spot("SpotCyanLeft", (-3.5, 5, 7), 4000, 45, (0.1, 0.8, 1.0))
spot("SpotCyanRight", (3.5, 5, 7), 4000, 45, (0.3, 0.95, 1.0))
# thin occluder bars
for x in (-3.2, -1.6, 0.4, 2.0, 3.4):
    bpy.ops.mesh.primitive_cube_add(size=2, location=(x, 2.5, 2.5))
    p = bpy.context.object; p.scale = (0.35, 0.5, 4)
    pm = bpy.data.materials.new("Dark"); pm.use_nodes = True
    bsdf = pm.node_tree.nodes["Principled BSDF"]; bsdf.inputs["Base Color"].default_value = (0, 0, 0, 1)
    p.data.materials.append(pm)
# dust motes: tiny emission spheres inside the volume
dm = bpy.data.materials.new("Dust"); dm.use_nodes = True
em = dm.node_tree.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (0.6, 0.95, 1.0, 1); em.inputs["Strength"].default_value = 2.0
dm.node_tree.links.new(em.outputs[0], dm.node_tree.nodes["Material Output"].inputs[0])
for i in range(60):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.03, location=(random.uniform(-5,5), random.uniform(-2,4), random.uniform(-1,6)))
    bpy.context.object.data.materials.append(dm)
bpy.ops.render.render(write_still=True)
print("GODRAY_V2_DONE", OUT)
