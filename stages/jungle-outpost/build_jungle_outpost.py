"""Build Jungle Outpost (show reconstruction) for Cape Jones Ep 1, Scene 6.

NOT extracted game geometry: original geometry built to the publicly
documented layout of the T7 stage stg02 (see README.md in the repo):
  upper fight floor 23 x 13 m, lower floor 26 x 11.5 m, wall-break
  expansion to 26 x 26 m. Daytime version (original T7 look).
Fighting surface: upper floor top at z=0 (Blender Z-up; glTF export
converts to Y-up, same convention as stages/cape-house/living-room.glb).
Lower floor top at z=-4.2 (balcony-break drop level).

Usage (headless):
  blender -b --python build_jungle_outpost.py -- <out.glb> <proof_dir>
Renders 3 proof frames into <proof_dir> and exports the GLB.
"""
import bpy, sys, math, os
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
OUT_GLB, PROOF_DIR = argv[0], argv[1]
os.makedirs(PROOF_DIR, exist_ok=True)

# --- clean scene ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
    for x in coll:
        coll.remove(x)

def mat(name, rgb, rough=0.85, metallic=0.0, emit=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    if emit is not None:
        bsdf.inputs["Emission Color"].default_value = (*emit, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.6
    return m

M = {
    "wood":      mat("Wood_Platform", (0.30, 0.19, 0.09)),
    "wood_dark": mat("Wood_Dark", (0.20, 0.12, 0.06)),
    "thatch":    mat("Thatch", (0.55, 0.46, 0.24)),
    "leaf":      mat("Leaf", (0.10, 0.32, 0.10)),
    "leaf2":     mat("Leaf_Light", (0.16, 0.42, 0.14)),
    "trunk":     mat("Trunk", (0.28, 0.19, 0.11)),
    "stone":     mat("Stone", (0.48, 0.47, 0.44)),
    "stone_dark":mat("Stone_Dark", (0.33, 0.32, 0.30)),
    "dirt":      mat("Dirt", (0.32, 0.24, 0.14)),
    "vine":      mat("Vine", (0.12, 0.35, 0.12)),
    "metal":     mat("Plane_Metal", (0.55, 0.55, 0.56), rough=0.5, metallic=0.6),
    "rust":      mat("Plane_Rust", (0.45, 0.25, 0.12), rough=0.9),
    "tiki":      mat("Tiki_Stone", (0.52, 0.48, 0.38)),
    "rope":      mat("Rope", (0.60, 0.52, 0.32)),
    "wallhut":   mat("Hut_Wall", (0.62, 0.52, 0.34)),
}

def box(name, loc, size, material, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.dimensions = size
    o.data.materials.append(material)
    return o

def cyl(name, loc, r, depth, material, rot=(0, 0, 0), verts=20):
    bpy.ops.mesh.primitive_cylinder_add(location=loc, rotation=rot, vertices=verts, radius=r, depth=depth)
    o = bpy.context.active_object
    o.name = name
    o.data.materials.append(material)
    return o

def sphere(name, loc, r, material, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(location=loc, segments=24, ring_count=16, radius=r)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    o.data.materials.append(material)
    for p in o.data.polygons:
        p.use_smooth = True
    return o

def empty(name, loc):
    o = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(o)
    o.location = loc
    o.empty_display_size = 0.8
    return o

# ================= UPPER FIGHT FLOOR (23 x 13, top z=0) =================
box("FightFloor_Upper", (0, 0, -0.35), (23, 13, 0.7), M["wood"])
# plank seams across the width
for i in range(11):
    x = -10 + i * 2.0
    box(f"PlankSeam_{i:02d}", (x, 0, 0.005), (0.12, 13, 0.02), M["wood_dark"])
# edge beams + support posts down to the lower level
box("UpperBeam_N", (0, 6.5, -0.35), (23, 0.5, 0.7), M["wood_dark"])
box("UpperBeam_S", (0, -6.5, -0.35), (23, 0.5, 0.7), M["wood_dark"])
for x in (-10.5, -3.5, 3.5, 10.5):
    for y in (-5.8, 5.8):
        cyl(f"SupportPost_{x}_{y}", (x, y, -2.4), 0.35, 4.2, M["trunk"])

# Balcony rail (BREAKABLE, pre-break state) along the south edge (-Y)
for i in range(12):
    x = -11 + i * 2.0
    box(f"BalconyRail_Post_{i:02d}", (x, -6.4, 0.55), (0.18, 0.18, 1.1), M["wood_dark"])
box("BalconyRail_Top", (0, -6.4, 1.12), (23, 0.18, 0.18), M["wood_dark"])
box("BalconyRail_Mid", (0, -6.4, 0.60), (23, 0.10, 0.10), M["rope"])
# rope rail on the north edge (open side, no break)
box("RopeRail_N_Top", (0, 6.4, 1.05), (23, 0.12, 0.12), M["rope"])
for i in range(8):
    x = -10.5 + i * 3.0
    box(f"RopeRail_N_Post_{i}", (x, 6.4, 0.5), (0.14, 0.14, 1.0), M["wood_dark"])

# Canopy: trunks + leaf masses overhead and around (kept high / to the sides
# so the fight stays readable from the hero camera)
canopy_spots = [(-16, -12, 7.5), (-16, 12, 8.0), (16, -12, 7.5), (16, 12, 8.0),
                (-6, -14, 6.5), (6, 14, 7.0), (0, -15, 7.0), (-19, 0, 7.5), (19, 0, 7.5)]
for i, (x, y, z) in enumerate(canopy_spots):
    cyl(f"CanopyTrunk_{i:02d}", (x, y, z / 2 - 0.5), 0.45, z, M["trunk"])
    sphere(f"CanopyLeaves_{i:02d}a", (x, y, z), 2.5, M["leaf"], scale=(1.2, 1.1, 0.7))
    sphere(f"CanopyLeaves_{i:02d}b", (x + 1.2, y + 0.8, z + 0.8), 1.8, M["leaf2"], scale=(1.2, 1.0, 0.7))
# hanging vines from the canopy over the platform edges
for i, x in enumerate((-8, -4, 0, 4, 8)):
    cyl(f"HangingVine_{i}", (x, -7.5, 3.2), 0.08, 3.5, M["vine"])

# ================= LOWER FLOOR (26 x 11.5, top z=-4.2) =================
box("FightFloor_Lower", (0, 0, -4.55), (26, 11.5, 0.7), M["stone"])
# carved stone disc at the centre of the lower court
cyl("CarvedStone_Disc", (0, 0, -4.15), 3.6, 0.15, M["stone_dark"])
cyl("CarvedStone_Ring", (0, 0, -4.06), 2.4, 0.10, M["stone"])
cyl("CarvedStone_Centre", (0, 0, -4.00), 0.9, 0.12, M["stone_dark"])
# vine wall (BREAKABLE, pre-break state) along the north long edge (+Y)
for i in range(14):
    x = -12.5 + i * 1.9
    cyl(f"VineWall_Strand_{i:02d}", (x, 5.7, -2.5), 0.10, 3.6, M["vine"])
box("VineWall_Top", (0, 5.7, -0.85), (26, 0.25, 0.25), M["vine"])
for i in range(7):
    sphere(f"VineWall_Leaf_{i}", (-11 + i * 3.6, 5.7, -1.6 - (i % 3) * 0.5), 0.9, M["leaf2"], scale=(1.2, 0.5, 1.0))
# tiki statues around the lower court
for i, (x, y, rot) in enumerate([(-11, -4.5, 0.4), (11, -4.5, -0.4), (-11, 4.2, 2.7), (11, 4.2, -2.7)]):
    box(f"Tiki_Base_{i}", (x, y, -3.85), (1.2, 1.2, 0.7), M["tiki"])
    cyl(f"Tiki_Body_{i}", (x, y, -3.0), 0.55, 1.6, M["tiki"], rot=(0, 0, rot))
    box(f"Tiki_Head_{i}", (x, y, -1.95), (0.9, 0.9, 0.9), M["tiki"], rot=(0, 0, rot))
    box(f"Tiki_Brow_{i}", (x, y + 0.5, -1.75), (0.95, 0.15, 0.25), M["stone_dark"], rot=(0, 0, rot))
# crashed plane wreckage at the east edge of the lower level
cyl("PlaneWreck_Fuselage", (14.5, -2.0, -3.3), 1.15, 8.0, M["metal"], rot=(0, 1.25, 0.5))
box("PlaneWreck_Wing", (13.0, -2.0, -3.1), (5.5, 0.25, 2.2), M["rust"], rot=(0.2, 0, 0.5))
box("PlaneWreck_Tail", (17.5, -3.5, -2.6), (0.3, 2.4, 2.0), M["rust"], rot=(0, 0, 0.5))
cyl("PlaneWreck_Engine", (12.0, -3.2, -3.4), 0.6, 1.6, M["metal"], rot=(1.57, 0, 0.5))

# ================= BACKGROUND DRESSING =================
box("JungleGround", (0, 0, -4.95), (140, 140, 0.5), M["dirt"])
# distant bahay kubo (stilt hut) + temple ruin, background only
for x, y, z in [(-1.2, 0, 0), (1.2, 0, 0)]:
    cyl("HutStilt", (10 + x, -30 + y, -3.4), 0.22, 2.4, M["trunk"])
box("Hut_Walls", (10, -30, -1.6), (6, 5, 2.4), M["wallhut"])
box("Hut_Roof", (10, -30, -0.1), (7.5, 6.5, 0.4), M["thatch"], rot=(0, 0, 0))
box("Hut_Roof2", (10, -30, 0.5), (5.5, 5.0, 0.4), M["thatch"], rot=(0, 0, 0))
box("Temple_Base", (-17, -27, -3.6), (8, 6, 2.0), M["stone_dark"])
box("Temple_Pillar1", (-19, -27, -1.8), (1.0, 1.0, 3.5), M["stone"])
box("Temple_Pillar2", (-15, -27, -1.8), (1.0, 1.0, 3.5), M["stone"])
box("Temple_Lintel", (-17, -27, 0.1), (6.5, 1.2, 0.8), M["stone"])
# background tree line
import random
random.seed(7)
for i in range(26):
    ang = random.uniform(0, 6.28)
    dist = random.uniform(32, 55)
    x, y = math.cos(ang) * dist, math.sin(ang) * dist
    if abs(y) < 14 and abs(x) < 20:
        continue
    h = random.uniform(8, 14)
    cyl(f"BgTree_{i:02d}", (x, y, -4.9 + h / 2), 0.5, h, M["trunk"])
    sphere(f"BgLeaves_{i:02d}", (x, y, -4.9 + h + 1.0), 3.0, M["leaf"], scale=(1.2, 1.2, 0.8))
# scattered bushes / ferns on the jungle floor
for i in range(22):
    x = random.uniform(-24, 24)
    y = random.uniform(-16, 16)
    if abs(x) < 14 and abs(y) < 7.5:
        continue
    sphere(f"Bush_{i:02d}", (x, y, -4.5), random.uniform(0.6, 1.3), M["leaf2"], scale=(1.3, 1.1, 0.6))

# ================= SPAWNS + LIGHTS =================
empty("Spawn_Cape", (-2.0, 0, 0))
empty("Spawn_Pantera", (2.0, 0, 0))
empty("FightCentre_Upper", (0, 0, 0))
empty("FightCentre_Lower", (0, 0, -4.2))

world = bpy.data.worlds.new("JungleSky")
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.62, 0.78, 0.88, 1.0)  # daytime sky
bg.inputs["Strength"].default_value = 0.6
bpy.context.scene.world = world

bpy.ops.object.light_add(type='SUN', location=(20, -15, 30))
sun = bpy.context.active_object
sun.name = "Sun_Day"
sun.data.energy = 1.5
sun.data.angle = 25
bpy.ops.object.light_add(type='POINT', location=(0, 0, 8))
fill = bpy.context.active_object
fill.name = "Fill_Canopy"
fill.data.energy = 150
fill.data.shadow_soft_size = 1.0

# ================= RENDER PROOFS (Eevee) =================
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.film_transparent = False
scene.cycles.device = 'CPU'
scene.cycles.samples = 32
scene.cycles.use_denoising = True

def render_view(name, cam_loc, tgt_loc):
    tgt = empty("CamTarget_" + name, tgt_loc)
    bpy.ops.object.camera_add(location=cam_loc)
    cam = bpy.context.active_object
    cam.name = "Cam_" + name
    con = cam.constraints.new('TRACK_TO')
    con.target = tgt
    con.track_axis = 'TRACK_NEGATIVE_Z'
    con.up_axis = 'UP_Y'
    scene.camera = cam
    scene.render.filepath = os.path.join(PROOF_DIR, name + ".png")
    bpy.ops.render.render(write_still=True)
    print("RENDERED:", scene.render.filepath)

render_view("hero_upper", (24, 10, 12), (0, 0, 0.0))
render_view("lower_court", (16, -16, 2.0), (0, 0, -3.5))
render_view("wide_tiers", (34, 6, 10), (0, 0, -2.0))

# remove cameras/targets before export (stage asset only)
bpy.ops.object.select_all(action='DESELECT')
for o in list(bpy.data.objects):
    if o.name.startswith("Cam_") or o.name.startswith("CamTarget_"):
        bpy.data.objects.remove(o, do_unlink=True)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=OUT_GLB, export_format='GLB',
                          use_selection=True, export_animations=False,
                          export_skins=False, export_morph=False,
                          export_cameras=False, export_lights=True)
print("STAGE_GLB:", OUT_GLB)
