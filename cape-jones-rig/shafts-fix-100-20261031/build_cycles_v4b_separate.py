"""Cycles separate-volume shafts v4 — DIFFERENT occluder/light design.
NOT another spot-energy tweak on a shared volume (tried twice, merged centre).

Design change:
- NO shared volume cube. 5 SEPARATE volume boxes, one per column, gaps
  between them are empty space (no density), so columns cannot merge.
- NO Sun (a sun fills gaps). 1 spot per column, aimed straight down its
  own column, narrow angle, so each column is lit independently.
- Ceiling: NO large black slat blocks. Only a thin top trim bar at the
  very top of the volume (z=7.6, thickness 0.08 world units) spanning the
  width — it reads as a ceiling edge, not dominating black blocks.
- Floor: a real Blender floor plane at z=-1.5 (bottom of the volumes),
  diffuse, receiving each spot — TRUE in-scene ground pools, not a
  composite ellipse. Floor material is light grey so pools read; spots
  create bright elliptical footprints where they hit it.
- Dust motes only inside column volumes.
Blender 5.2.3, Cycles CPU, 24 samples, denoising ON, 1100x1500.
"""
import bpy, math, random
random.seed(31)
OUT = '/home/hatch/workspace/cape-jones-rig/shafts-fix-100-20261031/shafts-only-cycles-v4b-separate-20261031.png'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = 24
sc.cycles.volume_step_rate = 1.0
try:
    sc.cycles.use_denoising = True
    print("DENOISE_ON")
except Exception as e:
    print("DENOISE_FAIL", e)
sc.render.resolution_x = 1100
sc.render.resolution_y = 1500
sc.render.resolution_percentage = 100
sc.render.film_transparent = False
sc.render.filepath = OUT
w = bpy.data.worlds.new("W")
w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.01, 0.012, 0.03, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
sc.world = w
bpy.ops.object.camera_add(location=(0, -15, 2.0), rotation=(math.radians(90), 0, 0))
sc.camera = bpy.context.object

COLS = [-3.0, -1.5, 0.0, 1.5, 3.0]
# 5 separate volumes: cube size 2, scale x 0.55 -> width 1.1 world units,
# gap between neighbouring volumes = 1.5 - 1.1 = 0.4 world units of empty air.
for i, gx in enumerate(COLS):
    bpy.ops.mesh.primitive_cube_add(size=2, location=(gx, 0, 3.0))
    vol = bpy.context.object
    vol.name = f"VolumeCol_{i}"
    vol.scale = (0.60, 3.0, 4.5)
    mat = bpy.data.materials.new(f"VolCol_{i}")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    pv = nt.nodes.new("ShaderNodeVolumePrincipled")
    pv.inputs["Density"].default_value = 0.28
    pv.inputs["Anisotropy"].default_value = 0.7
    pv.inputs["Color"].default_value = (1.0, 0.85, 0.55, 1)
    outn = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(pv.outputs[0], outn.inputs["Volume"])
    vol.data.materials.append(mat)

# Thin ceiling trim only — NOT large slat blocks.
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 7.6))
trim = bpy.context.object
trim.name = "CeilingTrim"
trim.scale = (6.0, 3.0, 0.04)  # thickness 0.08 world units
tm = bpy.data.materials.new("TrimDark")
tm.use_nodes = True
tm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0, 0, 0, 1)
trim.data.materials.append(tm)

# Floor plane receiving light — true in-scene pools.
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -1.5))
floor = bpy.context.object
floor.name = "FloorPools"
fm = bpy.data.materials.new("FloorMat")
fm.use_nodes = True
fm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.25, 0.22, 0.18, 1)
fm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9
floor.data.materials.append(fm)

# Sun restored: with SEPARATE volumes a sun cannot fill gaps (gaps have
# no density), so it lights all 5 columns uniformly — v4's spot-only
# lighting left outer columns dim. This is not a return to the shared
# volume that merged in v2/v3.
bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
sun = bpy.context.object; sun.name = "SunDown"; sun.data.energy = 3.0
sun.data.color = (1.0, 0.88, 0.60); sun.rotation_euler = (0, 0, 0)

# One spot per column, aimed at its own floor footprint.
for i, gx in enumerate(COLS):
    bpy.ops.object.empty_add(location=(gx, 0, -1.5))
    target = bpy.context.object
    target.name = f"TargetCol_{i}"
    bpy.ops.object.light_add(type='SPOT', location=(gx, 0, 9.0))
    s = bpy.context.object
    s.name = f"SpotCol_{i}"
    s.data.energy = 20000
    s.data.color = (1.0, 0.88, 0.62)
    s.data.spot_size = math.radians(28)
    s.data.spot_blend = 0.5
    c = s.constraints.new('TRACK_TO')
    c.target = target
    c.track_axis = 'TRACK_NEGATIVE_Z'
    c.up_axis = 'UP_Y'

# Dust only inside columns.
dm = bpy.data.materials.new("Dust")
dm.use_nodes = True
em = dm.node_tree.nodes.new("ShaderNodeEmission")
em.inputs["Color"].default_value = (1.0, 0.9, 0.65, 1)
em.inputs["Strength"].default_value = 3.0
dm.node_tree.links.new(em.outputs[0], dm.node_tree.nodes["Material Output"].inputs[0])
for i in range(50):
    gx = random.choice(COLS)
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.015, location=(gx + random.uniform(-0.4, 0.4), random.uniform(-2, 2), random.uniform(-1, 6)))
    bpy.context.object.data.materials.append(dm)

bpy.ops.render.render(write_still=True)
print("SHAFTS_V4_SEPARATE_DONE", OUT)
