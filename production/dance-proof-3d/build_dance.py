"""Cape Jones dance proof (3D) — build + render.

One 48-frame Charlie Brown shuffle loop (FK keys, CONSTANT interpolation,
poses on 6-frame steps), tiled across 480 frames at 24 fps. Five 4-second
montage sections with hard-cut lighting + set-dressing changes:
  S1 day | S2 LED magenta | S3 LED cyan | S4 night | S5 day again.
Locked camera. Modes: check (5 stills) / render (full sequence, frame step 2).
Run: blender -b rig.blend --python build_dance.py -- <mode> <outdir>
"""
import bpy, math, sys, os

argv = sys.argv[sys.argv.index("--") + 1:]
MODE = argv[0] if len(argv) > 0 else "check"
OUTDIR = argv[1] if len(argv) > 1 else "/tmp/cjdance/check"
os.makedirs(OUTDIR, exist_ok=True)
D = math.radians

# ---------------------------------------------------------------- rig setup
for name in ("MPFB_ReferenceBody", "MPFB_FullSkeleton"):
    ob = bpy.data.objects.get(name)
    if ob:
        bpy.data.objects.remove(ob, do_unlink=True)
_cage = bpy.data.objects.get("BlenRigMdefCage")
if _cage:
    _cage.hide_render = True

rig = bpy.data.objects["CapeJones_Rig"]

# ---------------------------------------------------------------- materials
def prin(mat):
    mat.use_nodes = True
    for n in mat.node_tree.nodes:
        if n.type == "BSDF_PRINCIPLED":
            return n
    return None

def new_mat(name, color, emission=None, e_strength=0.0):
    m = bpy.data.materials.new(name)
    p = prin(m)
    p.inputs["Base Color"].default_value = (*color, 1.0)
    if emission is not None:
        p.inputs["Emission Color"].default_value = (*emission, 1.0)
        p.inputs["Emission Strength"].default_value = e_strength
    return m

def base_input(mat):
    return prin(mat).inputs["Base Color"]

def emis_input(mat):
    return prin(mat).inputs["Emission Strength"]

MAT_GROUND = new_mat("Ground", (0.09, 0.34, 0.09))
MAT_CANOPY = new_mat("Canopy", (0.05, 0.27, 0.08))
MAT_TRUNK = new_mat("Trunk", (0.30, 0.18, 0.10))
MAT_FENCE = new_mat("Fence", (0.90, 0.88, 0.82))
MAT_FLOWER = new_mat("FlowerHeads", (0.95, 0.25, 0.20))
MAT_TUFT = new_mat("Tufts", (0.08, 0.30, 0.10))
MAT_SUN = new_mat("SunDisc", (1.0, 0.85, 0.30), emission=(1.0, 0.80, 0.25), e_strength=2.0)
MAT_MOON = new_mat("MoonDisc", (0.85, 0.90, 1.0), emission=(0.70, 0.80, 1.0), e_strength=1.2)
MAT_STAR = new_mat("Stars", (1, 1, 1), emission=(1, 1, 1), e_strength=2.5)
MAT_FLY = new_mat("Fireflies", (0.8, 1.0, 0.4), emission=(0.8, 1.0, 0.4), e_strength=3.0)
MAT_POLE = new_mat("PoleTips", (0.9, 0.9, 0.9), emission=(1, 1, 1), e_strength=0.0)

def mesh_obj(name, prim, loc, scale, mat, **kw):
    fn = {"CUBE": bpy.ops.mesh.primitive_cube_add,
          "SPHERE": bpy.ops.mesh.primitive_uv_sphere_add,
          "CYL": bpy.ops.mesh.primitive_cylinder_add,
          "CONE": bpy.ops.mesh.primitive_cone_add,
          "PLANE": bpy.ops.mesh.primitive_plane_add,
          "CIRCLE": bpy.ops.mesh.primitive_circle_add}[prim]
    fn(location=loc, **kw)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = scale
    if mat:
        ob.data.materials.append(mat)
    return ob

# ---------------------------------------------------------------- set build
mesh_obj("Ground", "PLANE", (0, 0, 0), (30, 30, 1), MAT_GROUND, size=2.0)
# trees: trunk + 2 canopy blobs
for i, (tx, ts) in enumerate([(-4.6, 1.15), (-2.4, 0.9), (0.2, 1.3), (2.8, 0.95), (5.0, 1.2)]):
    mesh_obj(f"Trunk{i}", "CYL", (tx, 4.6, 0.45 * ts), (0.09 * ts, 0.09 * ts, 0.45 * ts), MAT_TRUNK, radius=1.0)
    mesh_obj(f"Canopy{i}a", "SPHERE", (tx, 4.6, 1.05 * ts), (0.62 * ts, 0.5 * ts, 0.5 * ts), MAT_CANOPY)
    mesh_obj(f"Canopy{i}b", "SPHERE", (tx + 0.4 * ts, 4.7, 1.35 * ts), (0.42 * ts, 0.36 * ts, 0.36 * ts), MAT_CANOPY)
# bushes
for i, bx in enumerate([-2.6, 2.7]):
    mesh_obj(f"Bush{i}", "SPHERE", (bx, 2.3, 0.28), (0.55, 0.4, 0.30), MAT_CANOPY)
# fence pickets
for i in range(13):
    mesh_obj(f"Picket{i}", "CUBE", (-5.4 + i * 0.9, 3.3, 0.33), (0.09, 0.05, 0.33), MAT_FENCE)
mesh_obj("FenceRail", "CUBE", (0, 3.3, 0.38), (5.6, 0.05, 0.05), MAT_FENCE)
# sky discs
sun_disc = mesh_obj("SunDisc", "CIRCLE", (-3.5, 6.5, 1.9), (0.55, 0.55, 0.55), MAT_SUN, radius=1.0)
moon_disc = mesh_obj("MoonDisc", "CIRCLE", (3.6, 6.5, 2.0), (0.42, 0.42, 0.42), MAT_MOON, radius=1.0)
stars = []
import random
random.seed(7)
for i in range(36):
    sx = random.uniform(-7, 7); sz = random.uniform(1.6, 3.4)
    stars.append(mesh_obj(f"Star{i}", "SPHERE", (sx, 6.8, sz), (0.03, 0.03, 0.03), MAT_STAR))
# LED poles behind him
pole_tips = []
for i, px in enumerate([-2.3, 2.3]):
    mesh_obj(f"Pole{i}", "CYL", (px, 0.9, 0.55), (0.03, 0.03, 0.55), MAT_TRUNK, radius=1.0)
    pole_tips.append(mesh_obj(f"PoleTip{i}", "SPHERE", (px, 0.9, 1.18), (0.09, 0.09, 0.09), MAT_POLE))
# foreground flowers + tufts
for i, (fx, fy) in enumerate([(-1.7, -1.5), (-1.35, -1.8), (1.6, -1.6), (1.95, -1.35), (-2.2, -1.1), (2.3, -1.9)]):
    mesh_obj(f"Stem{i}", "CYL", (fx, fy, 0.17), (0.02, 0.02, 0.17), MAT_TUFT, radius=1.0)
    mesh_obj(f"Flower{i}", "SPHERE", (fx, fy, 0.38), (0.10, 0.10, 0.10), MAT_FLOWER)
for i in range(10):
    gx = random.uniform(-3.4, 3.4); gy = random.uniform(-2.2, -0.8)
    if abs(gx) < 0.5:
        gx += 0.9
    mesh_obj(f"Tuft{i}", "CONE", (gx, gy, 0.09), (0.07, 0.07, 0.12), MAT_TUFT, radius1=1.0)
# fireflies
flies = []
for i in range(12):
    fx = random.uniform(-3, 3); fy = random.uniform(0.6, 2.6); fz = random.uniform(0.2, 0.9)
    flies.append(mesh_obj(f"Fly{i}", "SPHERE", (fx, fy, fz), (0.025, 0.025, 0.025), MAT_FLY))

# ---------------------------------------------------------------- lights
sc = bpy.context.scene
sc.world = bpy.data.worlds.new("DanceWorld")
sc.world.use_nodes = True
bg = sc.world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.45, 0.65, 0.95, 1)
bg.inputs[1].default_value = 1.0

bpy.ops.object.light_add(type="SUN", location=(2.5, -1.5, 4))
sun = bpy.context.active_object; sun.name = "SunKey"
sun.data.energy = 3.2; sun.data.color = (1.0, 0.95, 0.85)
sun.rotation_euler = (D(48), 0, D(28))

bpy.ops.object.light_add(type="AREA", location=(0, -2.6, 1.4))
fill = bpy.context.active_object; fill.name = "FrontFill"
fill.data.energy = 260; fill.data.shape = "DISK"; fill.data.size = 3.0
fill.data.color = (1, 1, 1)
fill.rotation_euler = (D(90), 0, 0)

bpy.ops.object.light_add(type="POINT", location=(-2.3, 0.9, 1.3))
led_l = bpy.context.active_object; led_l.name = "LedL"
led_l.data.energy = 0; led_l.data.color = (1.0, 0.15, 0.75)
bpy.ops.object.light_add(type="POINT", location=(2.3, 0.9, 1.3))
led_r = bpy.context.active_object; led_r.name = "LedR"
led_r.data.energy = 0; led_r.data.color = (0.1, 0.75, 1.0)

bpy.ops.object.camera_add(location=(0, -3.35, 0.62), rotation=(D(87), 0, 0))
cam = bpy.context.active_object; cam.data.lens = 35
sc.camera = cam

# ---------------------------------------------------------------- section keys
# frames: S1 1-96 day, S2 97-192 magenta, S3 193-288 cyan, S4 289-384 night, S5 385-480 day
SECTIONS = [
    # world, worldstr, sunE, sunC, fillE, ledL_E, ledR_E, ground, canopy, flower, poleEmis
    dict(f=1,   world=(0.45, 0.65, 0.95), ws=1.0, sunE=3.2, sunC=(1.0, 0.95, 0.85), fillE=260,
         ledL=0, ledR=0, ground=(0.09, 0.34, 0.09), canopy=(0.05, 0.27, 0.08),
         flower=(0.95, 0.25, 0.20), pole=0.0),
    dict(f=97,  world=(0.15, 0.04, 0.24), ws=0.7, sunE=0.5, sunC=(1.0, 0.30, 0.80), fillE=110,
         ledL=60, ledR=10, ground=(0.20, 0.10, 0.26), canopy=(0.16, 0.08, 0.28),
         flower=(1.0, 0.30, 0.85), pole=3.0),
    dict(f=193, world=(0.02, 0.11, 0.19), ws=0.7, sunE=0.5, sunC=(0.30, 0.80, 1.0), fillE=110,
         ledL=10, ledR=60, ground=(0.05, 0.17, 0.24), canopy=(0.04, 0.16, 0.26),
         flower=(0.30, 0.95, 1.0), pole=3.0),
    dict(f=289, world=(0.008, 0.015, 0.05), ws=0.5, sunE=0.35, sunC=(0.45, 0.60, 1.0), fillE=36,
         ledL=0, ledR=0, ground=(0.02, 0.05, 0.05), canopy=(0.015, 0.04, 0.04),
         flower=(0.10, 0.14, 0.35), pole=0.0),
    dict(f=385, world=(0.45, 0.65, 0.95), ws=1.0, sunE=3.2, sunC=(1.0, 0.95, 0.85), fillE=260,
         ledL=0, ledR=0, ground=(0.09, 0.34, 0.09), canopy=(0.05, 0.27, 0.08),
         flower=(1.0, 0.55, 0.15), pole=0.0),
]

def key_pair(setter, frame, prev, new):
    if frame > 1 and prev is not None:
        setter(prev, frame - 1)
    setter(new, frame)

def s_world(v, f):
    bg.inputs[0].default_value = (*v, 1.0); bg.inputs[0].keyframe_insert("default_value", frame=f)
def s_ws(v, f):
    bg.inputs[1].default_value = v; bg.inputs[1].keyframe_insert("default_value", frame=f)
def s_sunE(v, f):
    sun.data.energy = v; sun.data.keyframe_insert("energy", frame=f)
def s_sunC(v, f):
    sun.data.color = v; sun.data.keyframe_insert("color", frame=f)
def s_fillE(v, f):
    fill.data.energy = v; fill.data.keyframe_insert("energy", frame=f)
def s_ledL(v, f):
    led_l.data.energy = v; led_l.data.keyframe_insert("energy", frame=f)
def s_ledR(v, f):
    led_r.data.energy = v; led_r.data.keyframe_insert("energy", frame=f)
def mat_setter(mat):
    inp = base_input(mat)
    def s(v, f):
        inp.default_value = (*v, 1.0); inp.keyframe_insert("default_value", frame=f)
    return s
def s_pole(v, f):
    inp = emis_input(MAT_POLE)
    inp.default_value = v; inp.keyframe_insert("default_value", frame=f)

SETTERS = [("world", s_world), ("ws", s_ws), ("sunE", s_sunE), ("sunC", s_sunC),
           ("fillE", s_fillE), ("ledL", s_ledL), ("ledR", s_ledR),
           ("ground", mat_setter(MAT_GROUND)), ("canopy", mat_setter(MAT_CANOPY)),
           ("flower", mat_setter(MAT_FLOWER)), ("pole", s_pole)]

prev = None
for sec in SECTIONS:
    for key, setter in SETTERS:
        key_pair(setter, sec["f"], None if prev is None else prev[key], sec[key])
    prev = sec

# visibility: sun disc S1+S5, moon/stars/flies S4 only
def vis_keys(ob, spans):
    # spans: list of (start, end) visible ranges within 1..480
    f = 1
    state = any(a <= 1 <= b for a, b in spans)
    ob.hide_render = not state; ob.keyframe_insert("hide_render", frame=1)
    changes = sorted({x for a, b in spans for x in (a, b + 1) if 1 < x <= 480})
    for cf in changes:
        state = any(a <= cf <= b for a, b in spans)
        ob.hide_render = not state; ob.keyframe_insert("hide_render", frame=cf)

vis_keys(sun_disc, [(1, 96), (385, 480)])
vis_keys(moon_disc, [(289, 384)])
for s in stars:
    vis_keys(s, [(289, 384)])
for fl in flies:
    vis_keys(fl, [(289, 384)])

# ---------------------------------------------------------------- dance keys
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode="POSE")

def pose_key(frame, pelvis_x, dip, tap_left, shrug=False):
    def R(bone, x=0.0, y=0.0, z=0.0):
        pb = rig.pose.bones[bone]
        pb.rotation_mode = "XYZ"
        pb.rotation_euler = (D(x), D(y), D(z))
        pb.keyframe_insert("rotation_euler", frame=frame)
    side = 1 if pelvis_x > 0 else -1
    pb = rig.pose.bones["pelvis"]
    pb.location = (pelvis_x, 0, 0)
    pb.keyframe_insert("location", frame=frame)
    R("pelvis", 0, 0, -5 * side)
    R("chest", 0, 9 * side, 0)
    R("neck_2", 0, 0, 5 * side)
    R("head", (5 if dip else 0) - (4 if shrug else 0), 0, 7 * side)
    # legs: tap vs plant
    if tap_left:
        R("thigh_fk_L", -22, 0, 2); R("shin_fk_L", 28); R("foot_fk_L", 10)
        R("thigh_fk_R", 4, 0, -2); R("shin_fk_R", 5)
    else:
        R("thigh_fk_R", -22, 0, -2); R("shin_fk_R", 28); R("foot_fk_R", 10)
        R("thigh_fk_L", 4, 0, 2); R("shin_fk_L", 5)
    # arms swing opposite the tap; bent elbows; shrug accent raises both
    swing = 18
    zlift = 14 if shrug else 0
    if tap_left:
        R("upperarm_fk_L", swing, 0, 20 + zlift); R("upperarm_fk_R", -swing, 0, -20 - zlift)
    else:
        R("upperarm_fk_L", -swing, 0, 20 + zlift); R("upperarm_fk_R", swing, 0, -20 - zlift)
    R("forearm_fk_L", -55); R("forearm_fk_R", -55)
    R("hand_fk_L", 0, 0, 8); R("hand_fk_R", 0, 0, -8)
    # whole-body bounce on the armature object (world Z, safe axis)
    rig.location = (0, 0, -0.012 if dip else 0.0)
    rig.keyframe_insert("location", frame=frame)

KEYS = [  # pelvis_x, dip, tap_left, shrug
    ( 0.05, False, True,  False),
    ( 0.05, True,  True,  False),
    (-0.05, False, False, False),
    (-0.05, True,  False, True),
    ( 0.05, False, True,  False),
    ( 0.05, True,  True,  False),
    (-0.05, False, False, False),
    (-0.05, True,  False, True),
]
for rep in range(10):
    base = 1 + rep * 48
    for k, (px, dip, tl, sh) in enumerate(KEYS):
        pose_key(base + k * 6, px, dip, tl, sh)
pose_key(481, *KEYS[0])
bpy.ops.object.mode_set(mode="OBJECT")


# ---- bake the 8 loop poses to static meshes; drop the live rig (render speed)
_bake_srcs = [(bpy.data.objects["CapeJones_Body"], "Body"),
              (bpy.data.objects["CapeJones_Cape"], "Cape")]
_baked = []
for _i in range(8):
    sc.frame_set(1 + _i * 6)
    _dg = bpy.context.evaluated_depsgraph_get()
    for _src, _tag in _bake_srcs:
        _ev = _src.evaluated_get(_dg)
        _me = bpy.data.meshes.new_from_object(_ev)
        _ob = bpy.data.objects.new(f"Dance{_tag}{_i}", _me)
        _ob.matrix_world = _src.matrix_world.copy()
        sc.collection.objects.link(_ob)
        _baked.append((_ob, _i))
for _ob, _i in _baked:
    vis_keys(_ob, [(1 + 48 * r + 6 * _i, 6 + 48 * r + 6 * _i) for r in range(10)])
for _name in ("CapeJones_Body", "CapeJones_Cape", "CapeJones_Rig", "BlenRigMdefCage"):
    _ob = bpy.data.objects.get(_name)
    if _ob:
        bpy.data.objects.remove(_ob, do_unlink=True)
print("BAKE_DONE", len(_baked))

# stepped interpolation everywhere: poses + lighting cuts hold, never blend
for act in bpy.data.actions:
    for fc in act.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"

# ---------------------------------------------------------------- render setup
sc.render.engine = "BLENDER_EEVEE"
sc.eevee.use_gtao = False
sc.view_settings.view_transform = "Filmic"
sc.render.film_transparent = False
sc.render.fps = 24
sc.frame_start = 1; sc.frame_end = 480

if MODE == "check":
    sc.eevee.taa_render_samples = 16
    sc.render.resolution_x = 640; sc.render.resolution_y = 360
    for fr, tag in [(24, "s1_day"), (130, "s2_magenta"), (250, "s3_cyan"),
                    (340, "s4_night"), (440, "s5_day")]:
        sc.frame_set(fr)
        sc.render.filepath = os.path.join(OUTDIR, f"check_{tag}.png")
        bpy.ops.render.render(write_still=True)
        print("CHECK_DONE", tag)
else:
    FS = int(argv[2]) if len(argv) > 2 else 1
    FE = int(argv[3]) if len(argv) > 3 else 480
    sc.eevee.taa_render_samples = 1
    sc.render.resolution_x = 960; sc.render.resolution_y = 540
    sc.render.image_settings.file_format = "PNG"
    import time
    SEC_STARTS = [(1, "s1"), (97, "s2"), (193, "s3"), (289, "s4"), (385, "s5")]
    for sec_f, tag in SEC_STARTS:
        if not (FS <= sec_f <= FE):
            continue
        for i in range(8):
            f = sec_f + 6 * i
            path = os.path.join(OUTDIR, f"still_{tag}_{i}.png")
            if os.path.exists(path):
                print("SKIP", path, flush=True)
                continue
            t0 = time.time()
            sc.frame_set(f)
            sc.render.filepath = path
            bpy.ops.render.render(write_still=True)
            print(f"STILL {tag} pose{i} frame{f} {time.time() - t0:.1f}s", flush=True)
    print("RENDER_DONE", FS, FE)
print("SCRIPT_COMPLETE", MODE)
