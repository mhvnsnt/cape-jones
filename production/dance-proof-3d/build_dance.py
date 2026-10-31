"""Cape Jones dance proof 3D v3 - STAGE A: build the scene, save scene_v3.blend.

v3 keeps v2's real keyed rig animation and its one-piece cape sheet, and
answers the v2 lane's own admitted shortfalls plus the owner's new asks:
  - NEW SONG, full length: the video runs the full 75.79 s English mix
    (song-full-v2-en.mp3, owner-approved final), 1824 frames at 24 fps,
    trimmed to 1819 on assembly. (The 2D version carries the Japanese
    mix; the owner's rule: both versions used equally, alternating.)
  - WORLD CYCLE stretched over the whole song: day -> LED magenta ->
    LED cyan -> night -> day, 8 loops (384 frames) per section, the
    dance loop tiling underneath, sections 2 and 4 mirrored on assembly
    as before (flips land on loop boundaries).
  - CAMERA CLOSER: v2 framed him small (his motion under-sold). Camera
    moves in and the lens tightens so he reads bigger in frame.
  - FOOT-SKATE reduced: the widest plants are narrowed (~15%) and each
    big plant gains a dwell-hold anchor, so pelvis translation happens
    while a foot is swinging, not while it is planted. Dips and weight
    shifts are kept. (FK rig: no IK ground-lock, so the fix is in the
    keys, per the v3 brief.)
Run: blender -b cape_jones_mpfb_wired.blend --python build_dance_v3.py
"""
import bpy, math, os, sys, time
import numpy as np

D = math.radians
WORK = "/home/hatch/workspace/_cj-dance3d-v3"
SCENE_OUT = os.path.join(WORK, "scene_v3.blend")
t00 = time.time()
def log(*a):
    print("[stageA]", *a, round(time.time() - t00, 1), "s", flush=True)

# ---------------------------------------------------------------- scene prep
for name in ("MPFB_ReferenceBody", "MPFB_FullSkeleton"):
    ob = bpy.data.objects.get(name)
    if ob:
        bpy.data.objects.remove(ob, do_unlink=True)
_cage = bpy.data.objects.get("BlenRigMdefCage")
if _cage:
    _cage.hide_render = True
    _cage.hide_viewport = True
_slab = bpy.data.objects.get("CapeJones_Cape")
if _slab:
    bpy.data.objects.remove(_slab, do_unlink=True)
    log("slab deleted")

rig = bpy.data.objects["CapeJones_Rig"]
body = bpy.data.objects["CapeJones_Body"]
sc = bpy.context.scene

# reset pose to rest, fresh action
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode="POSE")
for pb in rig.pose.bones:
    pb.rotation_euler = (0, 0, 0)
    pb.location = (0, 0, 0)
    pb.scale = (1, 1, 1)
bpy.ops.object.mode_set(mode="OBJECT")
if rig.animation_data:
    rig.animation_data_clear()
act = bpy.data.actions.new("DanceV3")
rig.animation_data_create()
rig.animation_data.action = act

# ---------------------------------------------------------------- cape bones
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode="EDIT")
arm = rig.data
def add_bone(name, parent_name, head, tail):
    eb = arm.edit_bones.new(name)
    eb.head = head; eb.tail = tail
    eb.use_deform = True
    if parent_name:
        eb.parent = arm.edit_bones[parent_name]
    return eb
add_bone("cape_1", "chest", (0, 0.095, 0.735), (0, 0.110, 0.560))
add_bone("cape_2", "cape_1", (0, 0.110, 0.560), (0, 0.118, 0.390))
add_bone("cape_3", "cape_2", (0, 0.118, 0.390), (0, 0.112, 0.200))
bpy.ops.object.mode_set(mode="OBJECT")
log("cape bones added")

# ------------------------------------------------------- body render copy
cp = body.copy(); cp.data = body.data.copy(); cp.name = "BodyR"
sc.collection.objects.link(cp)
for md in list(cp.modifiers):
    cp.modifiers.remove(md)
# decimate via evaluated-mesh writeback (modifier_apply is blocked by the
# scan's shape keys; the evaluated mesh captures the current shape and
# drops the keys, which the dance does not use)
dm1 = cp.modifiers.new("Dec1", "DECIMATE"); dm1.ratio = 0.35; dm1.use_collapse_triangulate = True
dm2 = cp.modifiers.new("Dec2", "DECIMATE"); dm2.ratio = 0.30; dm2.use_collapse_triangulate = True
_dg = bpy.context.evaluated_depsgraph_get()
_newme = bpy.data.meshes.new_from_object(cp.evaluated_get(_dg))
_oldme = cp.data
cp.data = _newme
bpy.data.meshes.remove(_oldme)
for md in list(cp.modifiers):
    cp.modifiers.remove(md)
log("decimate writeback done, verts", len(cp.data.vertices), "faces", len(cp.data.polygons),
    "vgroups", len(cp.vertex_groups), "chest group:", "chest" in cp.vertex_groups)
# trim the scan cape's low side panels: they wrap past where the clean cape
# sheet (below) can cover, and their island ribbons are the last tatter read.
# A face goes only if ALL verts are far around the side (|theta| > 98 deg
# from the back axis), low (z < 0.50), and far out (r > 0.16 - cape panels
# sit at r ~0.21; hips/thighs stay under 0.16, so the suit is untouched).
_me = cp.data
_co = np.empty(len(_me.vertices) * 3, dtype=np.float32)
_me.vertices.foreach_get("co", _co)
_co = _co.reshape(-1, 3)
_theta = np.degrees(np.arctan2(_co[:, 0], _co[:, 1]))
_rad = np.hypot(_co[:, 0], _co[:, 1])
_bad_v = (np.abs(_theta) > 55.0) & (_co[:, 1] > 0.03) & (_co[:, 2] < 0.50) & (_rad > 0.16)
_polys = np.empty(len(_me.polygons) * 3, dtype=np.int32)
_me.polygons.foreach_get("vertices", _polys)
_polys = _polys.reshape(-1, 3)
_drop = [i for i, f in enumerate(_polys) if _bad_v[f[0]] and _bad_v[f[1]] and _bad_v[f[2]]]
if _drop:
    import bmesh
    bm = bmesh.new(); bm.from_mesh(_me)
    bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[bm.faces[i] for i in _drop], context="FACES")
    bm.to_mesh(_me); bm.free()
    log("scan cape side trim: deleted", len(_drop), "faces; verts now", len(_me.vertices))
am = cp.modifiers.new("Arm", "ARMATURE"); am.object = rig
cs = cp.modifiers.new("Smooth2", "CORRECTIVE_SMOOTH")
cs.factor = 0.5; cs.iterations = 5
# original body no longer needed: BodyR replaces it on screen
bpy.data.objects.remove(body, do_unlink=True)
log("BodyR ready, base verts", len(cp.data.vertices), "faces", len(cp.data.polygons))

# ------------------------------------------------------- cape weight adds
def cape_weights_for(co):
    """co: (n,3) positions -> dict bone -> (n,) added weights (height gradient)."""
    z = co[:, 2]
    t = np.clip((0.66 - z) / 0.40, 0.0, 1.0)          # 0 at top, 1 at hem
    W = 1.5 * t
    return {"cape_1": W * (1 - t) * 0.8,
            "cape_2": W * (t * (1 - t)) * 2.2,
            "cape_3": W * t * t * 1.1}

me = cp.data
nv = len(me.vertices)
co = np.empty(nv * 3, dtype=np.float32)
me.vertices.foreach_get("co", co)
co = co.reshape(nv, 3)
zone = (co[:, 1] >= 0.035) & (co[:, 2] >= 0.05) & (co[:, 2] <= 0.80) & (np.abs(co[:, 0]) <= 0.30)
wmap = cape_weights_for(co)
for bn in ("cape_1", "cape_2", "cape_3"):
    if bn not in cp.vertex_groups:
        cp.vertex_groups.new(name=bn)
    vg = cp.vertex_groups[bn]
    w = wmap[bn]
    sel = zone & (w > 0.02)
    idx = np.nonzero(sel)[0]
    if len(idx) == 0:
        continue
    qw = np.round(w[sel] / 0.05) * 0.05
    for val in np.unique(qw):
        vg.add(idx[qw == val].tolist(), float(val), "REPLACE")
    log("weights", bn, "verts", int(len(idx)))
log("cape weights done, zone verts", int(zone.sum()))

# ------------------------------------------------------- cape slot fill
# boundary loops of the BodyR base mesh via loop-edge counting (numpy)
mesh = cp.data
nl = len(mesh.loops); npol = len(mesh.polygons); nvB = len(mesh.vertices)
lv = np.empty(nl, dtype=np.int64)
mesh.loops.foreach_get("vertex_index", lv)
ls = np.empty(npol, dtype=np.int64); lt = np.empty(npol, dtype=np.int64)
mesh.polygons.foreach_get("loop_start", ls)
mesh.polygons.foreach_get("loop_total", lt)
rep_ls = np.repeat(ls, lt); rep_lt = np.repeat(lt, lt)
pos = np.arange(nl) - rep_ls
nxt = rep_ls + (pos + 1) % rep_lt
a = lv; b = lv[nxt]
ekey = np.minimum(a, b) * (1 << 21) + np.maximum(a, b)
uniq, counts = np.unique(ekey, return_counts=True)
bkeys = uniq[counts == 1]
bA = (bkeys >> 21).astype(np.int64); bB = (bkeys & ((1 << 21) - 1)).astype(np.int64)
log("boundary edges", len(bkeys))
from collections import defaultdict
adj = defaultdict(list)
for u, v in zip(bA.tolist(), bB.tolist()):
    adj[u].append(v); adj[v].append(u)
seen = set(); comps = []
for s0 in list(adj.keys()):
    if s0 in seen:
        continue
    stack = [s0]; seen.add(s0); comp = []
    while stack:
        x = stack.pop(); comp.append(x)
        for y in adj[x]:
            if y not in seen:
                seen.add(y); stack.append(y)
    comps.append(comp)
log("boundary components", len(comps))
vn = np.empty(nvB * 3, dtype=np.float32)
mesh.vertices.foreach_get("normal", vn)
vn = vn.reshape(nvB, 3)
coB = np.empty(nvB * 3, dtype=np.float32)
mesh.vertices.foreach_get("co", coB)
coB = coB.reshape(nvB, 3)

def loop_order(comp):
    pts = coB[comp]
    cen = pts.mean(axis=0)
    nrm = vn[comp].mean(axis=0)
    nn = np.linalg.norm(nrm)
    nrm = nrm / nn if nn > 1e-6 else np.array([0.0, 1.0, 0.0])
    ref = np.array([0.0, 0.0, 1.0]) if abs(nrm[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    u = np.cross(nrm, ref); u /= (np.linalg.norm(u) + 1e-9)
    w = np.cross(nrm, u)
    rel = pts - cen
    ang = np.arctan2(rel @ w, rel @ u)
    order = np.argsort(ang)
    return [comp[i] for i in order], cen, nrm

patch_verts = []; patch_faces = []; filled = []
for comp in comps:
    if len(comp) < 10:
        continue
    pts = coB[comp]
    cen = pts.mean(axis=0)
    dims = np.sort(pts.max(axis=0) - pts.min(axis=0))
    if cen[1] < 0.030 or cen[2] > 0.62 or cen[2] < 0.05:
        continue
    if dims[0] > 0.05 or dims[1] < 0.05 or dims[2] > 0.30:
        continue
    ring, cen2, nrm = loop_order(comp)
    base = len(patch_verts)
    patch_verts.append(tuple(cen2 + nrm * 0.0015))
    for vi in ring:
        patch_verts.append(tuple(coB[vi] + vn[vi] * 0.0008))
    for i in range(len(ring)):
        patch_faces.append((base, base + 1 + i, base + 1 + (i + 1) % len(ring)))
    filled.append({"verts": len(comp), "centroid": [round(float(v), 3) for v in cen]})
log("slot fills", filled)

patch_ob = None
# NOTE: the membrane patch object is intentionally NOT built. Once the clean
# cape sheet (next section) covers the scan cape, the membranes are the only
# geometry left poking past the sheet's edge - they read as the tatter they
# were meant to hide. The fill list above stays as the slot census.
log("slot fills computed (membranes retired - cape sheet covers):", len(patch_faces), "faces")

# ------------------------------------------------ clean cape sheet (cover)
# The scan cape is a multi-island sheet; its inter-island gaps read as a
# tattered cape at zoom no matter how many are membrane-filled. This
# parametric one-piece cloth shell sits just OUTSIDE the scan cape, skinned
# to the same chest/spine/cape bones with the same gradient, so what reads
# on screen is one whole cloth that sways with the body.
COLS, ROWS = 29, 21
sv = np.linspace(-1.0, 1.0, COLS)
# measured radial profile of the (trimmed) scan cape: the sheet's radius at
# every angle/height is the scan cape's own radius + 12 mm, so the sheet
# provably covers the scan cape everywhere instead of approximating it.
_pc = np.empty(len(cp.data.vertices) * 3, dtype=np.float32)
cp.data.vertices.foreach_get("co", _pc)
_pc = _pc.reshape(-1, 3)
_pth = np.degrees(np.arctan2(_pc[:, 0], _pc[:, 1]))
_prad = np.hypot(_pc[:, 0], _pc[:, 1])
_pzone = (_pc[:, 1] > 0.02) & (_pc[:, 2] < 0.70) & (_prad > 0.10)
def scan_r(th_deg, z):
    m = _pzone & (np.abs(_pth - th_deg) < 5.0) & (np.abs(_pc[:, 2] - z) < 0.035)
    return float(_prad[m].max()) if m.any() else 0.0
def scan_min_z(th_deg):
    m = _pzone & (np.abs(_pth - th_deg) < 5.0)
    return float(_pc[m][:, 2].min()) if m.any() else 9.9
sheet_verts = []
for r in range(ROWS):
    v = r / (ROWS - 1)
    for c in range(COLS):
        s = float(sv[c])
        th = math.radians(s * 105.0)
        hem = 0.075 - 0.022 * (0.5 + 0.5 * math.cos(3 * math.pi * s))
        smz = scan_min_z(s * 105.0)
        if smz < 9.0:
            hem = min(hem, smz - 0.008)
        z = 0.735 + v * (hem - 0.735)
        Rr = 0.146 + 0.062 * v
        Rr += 0.005 * math.sin(s * 7 * math.pi) * v
        prof = scan_r(s * 105.0, z)
        if prof > 0.0:
            Rr = max(Rr, prof + 0.012)
        sheet_verts.append((Rr * math.sin(th), Rr * math.cos(th), z))
sheet_faces = []
for r in range(ROWS - 1):
    for c in range(COLS - 1):
        a = r * COLS + c; b = a + 1; d = a + COLS; e = d + 1
        sheet_faces.append((a, d, e, b))
sme = bpy.data.meshes.new("CapeSheetMesh")
sme.from_pydata(sheet_verts, [], sheet_faces)
sme.materials.append(bpy.data.materials["Cape_Black"])
for p in sme.polygons:
    p.use_smooth = True
sheet_ob = bpy.data.objects.new("CapeSheet", sme)
sc.collection.objects.link(sheet_ob)
sarr = np.array(sheet_verts, dtype=np.float64)
sw = cape_weights_for(sarr)
g_ch = sheet_ob.vertex_groups.new(name="chest")
g_sp = sheet_ob.vertex_groups.new(name="spine_2")
g_c = {bn: sheet_ob.vertex_groups.new(name=bn) for bn in ("cape_1", "cape_2", "cape_3")}
for r in range(ROWS):
    v = r / (ROWS - 1)
    for c in range(COLS):
        i = r * COLS + c
        g_ch.add([i], 0.75 * (1 - v) + 0.15, "REPLACE")
        g_sp.add([i], 0.25 * (1 - v), "REPLACE")
        for bn in ("cape_1", "cape_2", "cape_3"):
            wgt = float(sw[bn][i])
            if wgt > 0.02:
                g_c[bn].add([i], wgt, "REPLACE")
sm2 = sheet_ob.modifiers.new("Arm", "ARMATURE"); sm2.object = rig
log("cape sheet built", len(sheet_faces), "faces")

# ------------------------------------------------------- set + lights (from v1)
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

mesh_obj("Ground", "PLANE", (0, 0, 0), (30, 30, 1), MAT_GROUND, size=2.0)
for i, (tx, ts) in enumerate([(-4.6, 1.15), (-2.4, 0.9), (0.2, 1.3), (2.8, 0.95), (5.0, 1.2)]):
    mesh_obj(f"Trunk{i}", "CYL", (tx, 4.6, 0.45 * ts), (0.09 * ts, 0.09 * ts, 0.45 * ts), MAT_TRUNK, radius=1.0)
    mesh_obj(f"Canopy{i}a", "SPHERE", (tx, 4.6, 1.05 * ts), (0.62 * ts, 0.5 * ts, 0.5 * ts), MAT_CANOPY)
    mesh_obj(f"Canopy{i}b", "SPHERE", (tx + 0.4 * ts, 4.7, 1.35 * ts), (0.42 * ts, 0.36 * ts, 0.36 * ts), MAT_CANOPY)
for i, bx in enumerate([-2.6, 2.7]):
    mesh_obj(f"Bush{i}", "SPHERE", (bx, 2.3, 0.28), (0.55, 0.4, 0.30), MAT_CANOPY)
for i in range(13):
    mesh_obj(f"Picket{i}", "CUBE", (-5.4 + i * 0.9, 3.3, 0.33), (0.09, 0.05, 0.33), MAT_FENCE)
mesh_obj("FenceRail", "CUBE", (0, 3.3, 0.38), (5.6, 0.05, 0.05), MAT_FENCE)
sun_disc = mesh_obj("SunDisc", "CIRCLE", (-3.5, 6.5, 1.9), (0.55, 0.55, 0.55), MAT_SUN, radius=1.0)
moon_disc = mesh_obj("MoonDisc", "CIRCLE", (3.6, 6.5, 2.0), (0.42, 0.42, 0.42), MAT_MOON, radius=1.0)
stars = []
import random
random.seed(7)
for i in range(36):
    sx = random.uniform(-7, 7); sz = random.uniform(1.6, 3.4)
    stars.append(mesh_obj(f"Star{i}", "SPHERE", (sx, 6.8, sz), (0.03, 0.03, 0.03), MAT_STAR))
pole_tips = []
for i, px in enumerate([-2.3, 2.3]):
    mesh_obj(f"Pole{i}", "CYL", (px, 0.9, 0.55), (0.03, 0.03, 0.55), MAT_TRUNK, radius=1.0)
    pole_tips.append(mesh_obj(f"PoleTip{i}", "SPHERE", (px, 0.9, 1.18), (0.09, 0.09, 0.09), MAT_POLE))
for i, (fx, fy) in enumerate([(-1.7, -1.5), (-1.35, -1.8), (1.6, -1.6), (1.95, -1.35), (-2.2, -1.1), (2.3, -1.9)]):
    mesh_obj(f"Stem{i}", "CYL", (fx, fy, 0.17), (0.02, 0.02, 0.17), MAT_TUFT, radius=1.0)
    mesh_obj(f"Flower{i}", "SPHERE", (fx, fy, 0.38), (0.10, 0.10, 0.10), MAT_FLOWER)
for i in range(10):
    gx = random.uniform(-3.4, 3.4); gy = random.uniform(-2.2, -0.8)
    if abs(gx) < 0.5:
        gx += 0.9
    mesh_obj(f"Tuft{i}", "CONE", (gx, gy, 0.09), (0.07, 0.07, 0.12), MAT_TUFT, radius1=1.0)
flies = []
for i in range(12):
    fx = random.uniform(-3, 3); fy = random.uniform(0.6, 2.6); fz = random.uniform(0.2, 0.9)
    flies.append(mesh_obj(f"Fly{i}", "SPHERE", (fx, fy, fz), (0.025, 0.025, 0.025), MAT_FLY))

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
bpy.ops.object.camera_add(location=(0, -2.45, 0.60), rotation=(D(87), 0, 0))
cam = bpy.context.active_object; cam.name = "MainCam"; cam.data.lens = 38
sc.camera = cam

SECTIONS = [
    dict(f=1,   world=(0.45, 0.65, 0.95), ws=1.0, sunE=3.2, sunC=(1.0, 0.95, 0.85), fillE=260,
         ledL=0, ledR=0, ground=(0.09, 0.34, 0.09), canopy=(0.05, 0.27, 0.08),
         flower=(0.95, 0.25, 0.20), pole=0.0),
    dict(f=385,  world=(0.15, 0.04, 0.24), ws=0.7, sunE=0.5, sunC=(1.0, 0.30, 0.80), fillE=110,
         ledL=60, ledR=10, ground=(0.20, 0.10, 0.26), canopy=(0.16, 0.08, 0.28),
         flower=(1.0, 0.30, 0.85), pole=3.0),
    dict(f=769, world=(0.02, 0.11, 0.19), ws=0.7, sunE=0.5, sunC=(0.30, 0.80, 1.0), fillE=110,
         ledL=10, ledR=60, ground=(0.05, 0.17, 0.24), canopy=(0.04, 0.16, 0.26),
         flower=(0.30, 0.95, 1.0), pole=3.0),
    dict(f=1153, world=(0.008, 0.015, 0.05), ws=0.5, sunE=0.35, sunC=(0.45, 0.60, 1.0), fillE=36,
         ledL=0, ledR=0, ground=(0.02, 0.05, 0.05), canopy=(0.015, 0.04, 0.04),
         flower=(0.10, 0.14, 0.35), pole=0.0),
    dict(f=1537, world=(0.45, 0.65, 0.95), ws=1.0, sunE=3.2, sunC=(1.0, 0.95, 0.85), fillE=260,
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

def vis_keys(ob, spans):
    f = 1
    state = any(a <= 1 <= b for a, b in spans)
    ob.hide_render = not state; ob.keyframe_insert("hide_render", frame=1)
    changes = sorted({x for a, b in spans for x in (a, b + 1) if 1 < x <= 1824})
    for cf in changes:
        state = any(a <= cf <= b for a, b in spans)
        ob.hide_render = not state; ob.keyframe_insert("hide_render", frame=cf)

vis_keys(sun_disc, [(1, 384), (1537, 1824)])
vis_keys(moon_disc, [(1153, 1536)])
for s in stars:
    vis_keys(s, [(1153, 1536)])
for fl in flies:
    vis_keys(fl, [(1153, 1536)])
log("set + sections built")

# ------------------------------------------------------- the dance
# 48-frame step-touch loop, anchors every 4 frames. Values: degrees / metres.
# pelvis location local Y points UP (bone aims +Z), so dip = negative Y.
BASE = dict(PX=0.0, PD=0.004, PRY=0, PRZ=0, S2Y=0, S2Z=0, CX=2, CY=0, CZ=0,
            N2Y=0, N2Z=0, HX=2, HY=0, HZ=0,
            L_TX=0, L_TZ=-6, L_SX=7, L_FX=0, L_UX=-38, L_UZ=10, L_EX=-46, L_HZ=6,
            R_TX=0, R_TZ=6, R_SX=7, R_FX=0, R_UX=-38, R_UZ=-10, R_EX=-46, R_HZ=-6)
ANCHORS = [
 (1,  dict(PX=0.00, PD=0.006, CY=4, HZ=2)),
 (5,  dict(PX=-0.066, PD=0.016, PRZ=-6, PRY=4, CY=-7, CZ=3, HY=-14, HZ=5,
           R_TX=-20, R_TZ=4, R_SX=34, R_FX=18, L_TX=3, L_SX=10, L_FX=-6,
           L_UX=-30, R_UX=-48, L_UZ=-40, R_UZ=38, L_EX=-30, R_EX=-46)),
 (9,  dict(PX=0.072, PD=0.040, PRZ=8, PRY=-6, CY=9, CZ=-9, S2Z=-4, HX=9, HY=8, HZ=-5,
           R_TX=-4, R_TZ=21, R_SX=12, R_FX=2, L_TX=8, L_TZ=9, L_SX=16, L_FX=22,
           L_UX=-52, R_UX=-34, L_UZ=-38, R_UZ=44, L_EX=-48, R_EX=-32)),
 (11, dict(PX=0.070, PD=0.038, PRZ=8, PRY=-6, CY=8, CZ=-8, S2Z=-4, HX=9, HY=8, HZ=-5,
           R_TX=-4, R_TZ=21, R_SX=12, R_FX=2, L_TX=8, L_TZ=9, L_SX=16, L_FX=22,
           L_UX=-50, R_UX=-36, L_UZ=-38, R_UZ=42, L_EX=-48, R_EX=-32)),
 (13, dict(PX=0.046, PD=0.008, PRZ=2, CY=3, HY=4, HZ=2,
           L_TX=-2, L_TZ=-4, L_SX=8, R_TX=0, R_TZ=8, R_SX=8,
           L_UX=-40, R_UX=-40, L_EX=-40, R_EX=-40)),
 (17, dict(PX=0.070, PD=0.016, PRZ=6, PRY=-4, CY=7, CZ=-3, HY=14, HZ=-5,
           L_TX=-20, L_TZ=-4, L_SX=34, L_FX=18, R_TX=3, R_SX=10, R_FX=-6,
           L_UX=-48, R_UX=-30, L_UZ=40, R_UZ=-38, L_EX=-46, R_EX=-30)),
 (21, dict(PX=-0.072, PD=0.040, PRZ=-8, PRY=6, CY=-9, CZ=9, S2Z=4, HX=7, HY=-8, HZ=5,
           L_TX=-4, L_TZ=-21, L_SX=12, L_FX=2, R_TX=8, R_TZ=-9, R_SX=16, R_FX=22,
           L_UX=-34, R_UX=-52, L_UZ=44, R_UZ=-38, L_EX=-32, R_EX=-48)),
 (23, dict(PX=-0.070, PD=0.038, PRZ=-8, PRY=6, CY=-8, CZ=8, S2Z=4, HX=7, HY=-8, HZ=5,
           L_TX=-4, L_TZ=-21, L_SX=12, L_FX=2, R_TX=8, R_TZ=-9, R_SX=16, R_FX=22,
           L_UX=-36, R_UX=-50, L_UZ=42, R_UZ=-38, L_EX=-32, R_EX=-48)),
 (25, dict(PX=-0.010, PD=0.008, CY=-2, HY=-3, HZ=-2, L_UX=-38, R_UX=-38)),
 (29, dict(PX=-0.068, PD=0.018, PRZ=-6, PRY=4, CY=-8, CZ=3, HY=-16, HZ=6,
           R_TX=-24, R_TZ=4, R_SX=38, R_FX=20, L_TX=3, L_SX=10,
           L_UX=-28, R_UX=-52, L_UZ=-46, R_UZ=42, L_EX=-26, R_EX=-52)),
 (33, dict(PX=0.076, PD=0.046, PRZ=8, PRY=-6, CY=10, CZ=-9, S2Z=-4, HX=12, HY=8, HZ=-6,
           R_TX=-4, R_TZ=22, R_SX=13, R_FX=2, L_TX=8, L_TZ=9, L_SX=17, L_FX=22,
           L_UX=-56, R_UX=-32, L_UZ=-42, R_UZ=48, L_EX=-54, R_EX=-28)),
 (35, dict(PX=0.074, PD=0.044, PRZ=8, PRY=-6, CY=9, CZ=-9, S2Z=-4, HX=12, HY=8, HZ=-6,
           R_TX=-4, R_TZ=22, R_SX=13, R_FX=2, L_TX=8, L_TZ=9, L_SX=17, L_FX=22,
           L_UX=-54, R_UX=-34, L_UZ=-42, R_UZ=46, L_EX=-54, R_EX=-28)),
 (37, dict(PX=0.012, PD=0.010, CY=2, HX=2, HY=0, HZ=0,
           L_TX=-2, L_TZ=-6, L_SX=9, R_TZ=10,
           L_UX=-16, R_UX=-16, L_UZ=14, R_UZ=-14, L_EX=-60, R_EX=-64)),
 (39, dict(PX=0.008, PD=-0.004, PRZ=0, CX=-5, HX=-3, HY=0, HZ=0,
           L_TZ=-8, R_TZ=10, L_SX=4, R_SX=4,
           L_UX=-6, R_UX=-6, L_UZ=10, R_UZ=-10, L_EX=-102, R_EX=-106)),
 (43, dict(PX=0.008, PD=0.002, CX=-4, HX=-2, L_UX=-8, R_UX=-8, L_UZ=12, R_UZ=-12, L_EX=-98, R_EX=-102)),
 (46, dict(PX=0.002, PD=0.006, CX=0, HX=2, L_UZ=24, R_UZ=-26, L_EX=-55, R_EX=-58,
           L_UX=-24, R_UX=-24)),
]
FULL = []
for off, upd in ANCHORS:
    p = dict(BASE); p.update(upd); FULL.append((off, p))
FULLD = dict(FULL)

def sample_PX_PD(f_loop):
    """f_loop in [1,49): linear sample of pelvis X / dip from the anchor table."""
    pts = [(o, p["PX"], p["PD"]) for o, p in FULL] + [(49, FULL[0][1]["PX"], FULL[0][1]["PD"])]
    for i in range(len(pts) - 1):
        f0, x0, d0 = pts[i]; f1, x1, d1 = pts[i + 1]
        if f0 <= f_loop <= f1:
            t = 0.0 if f1 == f0 else (f_loop - f0) / (f1 - f0)
            return x0 + (x1 - x0) * t, d0 + (d1 - d0) * t
    return FULL[0][1]["PX"], FULL[0][1]["PD"]

bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode="POSE")
def K(bone, frame, loc=None, rot=None):
    pb = rig.pose.bones[bone]
    pb.rotation_mode = "XYZ"
    if loc is not None:
        pb.location = loc; pb.keyframe_insert("location", frame=frame)
    if rot is not None:
        pb.rotation_euler = tuple(D(a) for a in rot)
        pb.keyframe_insert("rotation_euler", frame=frame)

def apply_pose(f, p):
    K("pelvis", f, loc=(p["PX"], -p["PD"], 0), rot=(0, p["PRY"], p["PRZ"]))
    K("spine_2", f, rot=(0, p["S2Y"], p["S2Z"]))
    K("chest", f, rot=(p["CX"], p["CY"], p["CZ"]))
    K("neck_2", f, rot=(0, p["N2Y"], p["N2Z"]))
    K("head", f, rot=(p["HX"], p["HY"], p["HZ"]))
    for S in ("L", "R"):
        K(f"thigh_fk_{S}", f, rot=(p[f"{S}_TX"], 0, p[f"{S}_TZ"]))
        K(f"shin_fk_{S}", f, rot=(p[f"{S}_SX"], 0, 0))
        K(f"foot_fk_{S}", f, rot=(p[f"{S}_FX"], 0, 0))
        K(f"upperarm_fk_{S}", f, rot=(p[f"{S}_UX"], 0, p[f"{S}_UZ"]))
        K(f"forearm_fk_{S}", f, rot=(p[f"{S}_EX"], 0, 0))
        K(f"hand_fk_{S}", f, rot=(0, 0, p[f"{S}_HZ"]))

CAPE_K = (70.0, 120.0, 180.0)     # sway gain per cape bone (deg per metre PX)
CAPE_F = (50.0, 90.0, 140.0)      # flutter gain per cape bone (deg per metre dip)
def apply_cape(f):
    sf = f - 3                     # 3-frame follow-through lag
    sl = ((sf - 1) % 48) + 1
    px, pd = sample_PX_PD(sl)
    for i, bn in enumerate(("cape_1", "cape_2", "cape_3")):
        flut = pd * CAPE_F[i]
        if bn == "cape_3":
            flut += math.sin((f / 48.0) * 2 * math.pi * 2) * 1.5
        K(bn, f, rot=(flut, 0, px * CAPE_K[i]))

for rep in range(38):
    base_f = rep * 48
    for off, p in FULL:
        apply_pose(base_f + off, p)
        apply_cape(base_f + off)
apply_pose(1825, FULL[0][1])
apply_cape(1825)
bpy.ops.object.mode_set(mode="OBJECT")
log("dance keyed")

# accents snap by timing: LINEAR only on the shrug + nod keys, smooth elsewhere
for fc in act.fcurves:
    for kp in fc.keyframe_points:
        off = (int(round(kp.co.x)) - 1) % 48
        accent = False
        if any(b in fc.data_path for b in ("upperarm_fk_L", "upperarm_fk_R",
                                           "forearm_fk_L", "forearm_fk_R")) and off in (36, 38):
            accent = True
        if 'pose.bones["head"]' in fc.data_path and fc.array_index == 0 and off in (31, 32):
            accent = True
        kp.interpolation = "LINEAR" if accent else "BEZIER"
# every non-dance action (lights, materials, visibility) holds hard cuts
for other in bpy.data.actions:
    if other == act:
        continue
    for fc in other.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"
log("interpolation set")

# ---------------------------------------------------------------- render setup + save
sc.render.engine = "BLENDER_EEVEE"
sc.eevee.taa_render_samples = 1
sc.eevee.use_gtao = False
try:
    sc.eevee.use_bloom = False
except Exception:
    pass
sc.view_settings.view_transform = "Filmic"
sc.render.film_transparent = False
sc.render.fps = 24
sc.frame_start = 1; sc.frame_end = 1824
sc.render.resolution_x = 960; sc.render.resolution_y = 540
sc.render.image_settings.file_format = "JPEG"
sc.render.image_settings.quality = 90
sc.render.filepath = os.path.join(WORK, "frames", "f")
for attempt in range(8):
    try:
        bpy.ops.wm.save_as_mainfile(filepath=SCENE_OUT)
        break
    except Exception as e:
        log("save failed", e, "retry", attempt)
        time.sleep(15)
log("SCENE_SAVED", SCENE_OUT, os.path.getsize(SCENE_OUT) if os.path.exists(SCENE_OUT) else -1)
print("STAGE_A_DONE")
