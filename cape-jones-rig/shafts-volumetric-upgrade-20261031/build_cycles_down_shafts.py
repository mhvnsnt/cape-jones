# Blender 5.2.3 Cycles, CPU: REAL volumetric shafts shining DOWN from above.
# Light source ABOVE the scene, occluder slats at the top make separate columns.
# Camera looks from the front, so columns read as vertical shafts falling down.
# Figure is NOT in this Blender scene: this render is the SHAFT-ONLY layer.
# The 2D Cape plate is composited IN FRONT later, so shafts sit BEHIND him, never over him.
import bpy, math, random
random.seed(31)
OUT = '/home/hatch/workspace/cape-jones-rig/shafts-volumetric-upgrade-20261031/shafts-only-cycles-20261031.png'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = 32
sc.cycles.volume_step_rate = 1.0
sc.render.resolution_x = 1100
sc.render.resolution_y = 1500
sc.render.resolution_percentage = 100
sc.render.film_transparent = False
sc.render.filepath = OUT
# Dark world so shafts read
w = bpy.data.worlds.new("W"); w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.01, 0.012, 0.03, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
sc.world = w
# Camera, front view, centred on the volume
bpy.ops.object.camera_add(location=(0, -11, 3.2), rotation=(math.radians(90), 0, 0))
sc.camera = bpy.context.object
# Volume box: air the light travels through
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 3.0))
vol = bpy.context.object; vol.name = "VolumeAir"; vol.scale = (6.5, 3.0, 4.5)
mat = bpy.data.materials.new("Vol"); mat.use_nodes = True
nt = mat.node_tree; nt.nodes.clear()
pv = nt.nodes.new("ShaderNodeVolumePrincipled")
pv.inputs["Density"].default_value = 0.28
pv.inputs["Anisotropy"].default_value = 0.7
pv.inputs["Color"].default_value = (1.0, 0.85, 0.55, 1)  # warm sunlight colour
outn = nt.nodes.new("ShaderNodeOutputMaterial")
nt.links.new(pv.outputs[0], outn.inputs["Volume"])
vol.data.materials.append(mat)
# Floor, to catch light pools at the bottom: proves light travels DOWN
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -1.6))
fl = bpy.context.object; fl.name = "Floor"
fm = bpy.data.materials.new("FloorMat"); fm.use_nodes = True
fm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.08, 0.07, 0.10, 1)
fl.data.materials.append(fm)
# Sun straight DOWN (-Z)
bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
sun = bpy.context.object; sun.name = "SunDown"
sun.data.energy = 4.0
sun.data.color = (1.0, 0.88, 0.60)
sun.rotation_euler = (0, 0, 0)  # sun direction is -Z = straight down
# Occluder slats at the top: long in Y, bars in X, gaps between bars = shaft columns
# Gaps (shaft centres) at x = -3.9, -1.95, 0.0, 1.95, 3.9  -> 5 shafts
bar_x = [-5.4, -2.95, -0.98, 0.98, 2.95, 5.4]
for i, x in enumerate(bar_x):
    bpy.ops.mesh.primitive_cube_add(size=2, location=(x, 0, 6.8))
    p = bpy.context.object; p.name = f"CeilingSlat_{i}"
    p.scale = (0.55, 3.0, 0.25)
    pm = bpy.data.materials.new("DarkSlat"); pm.use_nodes = True
    pm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0, 0, 0, 1)
    p.data.materials.append(pm)
# Spot lights above each gap, pointing straight down, to strengthen each column
bpy.ops.object.empty_add(location=(0, 0, -1.5))
target = bpy.context.object
for i, gx in enumerate([-3.9, -1.95, 0.0, 1.95, 3.9]):
    bpy.ops.object.light_add(type='SPOT', location=(gx, 0, 9.0))
    s = bpy.context.object; s.name = f"SpotDown_{i}"
    s.data.energy = 6000; s.data.color = (1.0, 0.88, 0.62)
    s.data.spot_size = math.radians(28); s.data.spot_blend = 0.5
    c = s.constraints.new('TRACK_TO'); c.target = target
    c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
# Dust motes inside the shafts: tiny emission spheres, seeded only inside gap columns
dm = bpy.data.materials.new("Dust"); dm.use_nodes = True
em = dm.node_tree.nodes.new("ShaderNodeEmission")
em.inputs["Color"].default_value = (1.0, 0.9, 0.65, 1); em.inputs["Strength"].default_value = 3.0
dm.node_tree.links.new(em.outputs[0], dm.node_tree.nodes["Material Output"].inputs[0])
for i in range(80):
    gx = random.choice([-3.9, -1.95, 0.0, 1.95, 3.9])
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.035, location=(gx + random.uniform(-0.5, 0.5), random.uniform(-2, 2), random.uniform(-1, 6)))
    bpy.context.object.data.materials.append(dm)
bpy.ops.render.render(write_still=True)
print("SHAFTS_DOWN_DONE", OUT)
