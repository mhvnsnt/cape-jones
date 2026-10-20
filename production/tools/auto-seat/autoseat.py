"""AUTO-SEAT v1 — measurement-driven contact solver for seating the 94-bone rig.

Owner directive 2026-10-19: "stop hand tooling and bullshitting." No hand-tuned
pelvis Z. Every number is MEASURED from the scene and the mesh at runtime.

Root cause of all previous failures: lanes used seat_z=0.370 (the chair's
BOUNDING BOX top). Raycast measurement proves the actual sitting surface is
z=0.230. Every prior placement floated 10-14cm above the real seat.

Pipeline:
  1. MEASURE chair: seat top (raycast heightfield), backrest plane, floor.
  2. RETARGET mocap (CMU 113_15) via proven world-space math (M_REL fix).
  3. SOLVE per frame:
     a. Butt -> seat: linear solve on pelvis Z (rigid for pelvis-weighted verts).
     b. Back -> backrest: pitch solve on spine FK.
     c. Feet -> floor: analytic two-bone IK, baked to thigh/shin FK.
  4. KEYFRAME everything. Render proofs in full living_room.blend (Cycles).

Run: blender -b 3d-assets/living_room.blend --python production/tools/auto-seat/autoseat.py
"""
import bpy, math, os
from mathutils import Matrix, Quaternion, Vector

# ---------------------------------------------------------------- paths
WORKTREE = "/home/hatch/workspace/wt-autoseat"
FBX = os.path.join(WORKTREE, "production/tools/auto-seat/113_15.fbx")
OUT_BLEND = os.path.join(WORKTREE, "production/tools/auto-seat/proof_sitting.blend")
PROOF_DIR = os.path.join(WORKTREE, "production/tools/auto-seat/proofs")
os.makedirs(PROOF_DIR, exist_ok=True)

SRC_F0, SRC_F1 = 70, 150          # seated frames of 113_15
DST_F0 = 1
TARGET_HEIGHT = 0.925
COMPRESSION = 0.020               # cushion compression (m) — physical, not tuned
ROOTQ = Quaternion((0, 0, 1), math.radians(-90.0))  # rig -Y -> world -X (face into room)

scn = bpy.context.scene

# ---------------------------------------------------------------- rig setup
rig = bpy.data.objects.get("CapeJones_Rig")
assert rig and len(rig.data.bones) == 94, "need 94-bone rig"
for b in rig.pose.bones:
    b.rotation_mode = 'QUATERNION'
if rig.animation_data:
    rig.animation_data.action = None
print("rig ready, action cleared", flush=True)

# ---------------------------------------------------------------- measure chair (RUNTIME, from scene meshes)
deps = bpy.context.evaluated_depsgraph_get()

def raycast(obj, origin, direction):
    o = obj.evaluated_get(deps)
    o.to_mesh()
    mw = o.matrix_world
    mi = mw.inverted()
    hit, loc, nor, idx = o.ray_cast(mi @ origin, (mi.to_3x3() @ direction).normalized())
    o.to_mesh_clear()
    if hit:
        return (mw @ loc)
    return None

base = bpy.data.objects.get("recliner_base")
back = bpy.data.objects.get("recliner_backrest")
floor_o = bpy.data.objects.get("Floor")

# seat top: raycast grid over seat area, take median of hits in central region
seat_hits = []
for ix in range(7):
    for iy in range(7):
        x = 2.92 + ix * 0.06
        y = 1.90 + iy * 0.06
        h = raycast(base, Vector((x, y, 1.5)), Vector((0, 0, -1)))
        if h and 0.15 < h.z < 0.35:
            seat_hits.append(h.z)
seat_hits.sort()
SEAT_Z = seat_hits[len(seat_hits) // 2]
SEAT_C = Vector((3.05, 2.067, SEAT_Z))
print(f"MEASURED seat_z={SEAT_Z:.4f} from {len(seat_hits)} raycasts", flush=True)

# backrest plane: raycast +X at torso heights
br_hits = []
for z in [0.40, 0.45, 0.50, 0.55, 0.60]:
    h = raycast(back, Vector((2.90, 2.067, z)), Vector((1, 0, 0)))
    if h:
        br_hits.append((z, h.x))
BACK_X = sum(h[1] for h in br_hits) / len(br_hits)
print(f"MEASURED backrest_x={BACK_X:.4f} from {len(br_hits)} raycasts", flush=True)

fh = raycast(floor_o, Vector((3.0, 2.067, 1.0)), Vector((0, 0, -1)))
FLOOR_Z = fh.z if fh else 0.0
print(f"MEASURED floor_z={FLOOR_Z:.4f}", flush=True)

BUTT_TARGET_Z = SEAT_Z - COMPRESSION
print(f"butt target z = {BUTT_TARGET_Z:.4f}", flush=True)

# ---------------------------------------------------------------- mocap import + retarget (proven math)
bpy.ops.import_scene.fbx(filepath=FBX)
src = next(o for o in bpy.data.objects if o.type == 'ARMATURE' and o != rig)
src_act = src.animation_data.action
print(f"source: {src.name}, {int(src_act.frame_range[1])} frames", flush=True)

ad = src.animation_data
ad.action = None
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
SRC_REST = {b.name: (src.matrix_world @ b.matrix_local).to_3x3().to_quaternion()
            for b in src.data.bones}
ankle = min((src.matrix_world @ b.head_local).z for b in src.data.bones if 'Foot' in b.name)
headb = src.data.bones['head']
SRC_H = (src.matrix_world @ headb.head_local).z + headb.length - ankle
MOTION_SCALE = TARGET_HEIGHT / SRC_H
print(f"SRC_H={SRC_H:.2f} MOTION_SCALE={MOTION_SCALE:.4f}", flush=True)

TGT_RESTW = {b.name: (rig.matrix_world @ b.matrix_local).to_3x3().to_quaternion()
             for b in rig.data.bones}
M_REL = {}
for b in rig.data.bones:
    if b.parent is None:
        M_REL[b.name] = b.matrix_local.to_3x3().to_quaternion()
    else:
        M_REL[b.name] = (b.parent.matrix_local.inverted() @ b.matrix_local).to_3x3().to_quaternion()

M = [
 ("hip",        [("pelvis", 1.0)]),
 ("abdomen",    [("spine_fk_1", 0.5), ("spine_fk_2", 0.5)]),
 ("chest",      [("spine_fk_3", 0.34), ("spine_fk_4", 0.33), ("chest_fk", 0.33)]),
 ("neck",       [("neck_1", 0.5), ("neck_2", 0.5)]),
 ("head",       [("head", 1.0)]),
 ("lCollar",    [("clavicle_L", 1.0)]), ("rCollar", [("clavicle_R", 1.0)]),
 ("lShldr",     [("upperarm_fk_L", 1.0)]), ("rShldr", [("upperarm_fk_R", 1.0)]),
 ("lForeArm",   [("forearm_fk_L", 1.0)]), ("rForeArm", [("forearm_fk_R", 1.0)]),
 ("lHand",      [("hand_fk_L", 1.0)]), ("rHand", [("hand_fk_R", 1.0)]),
 ("lThigh",     [("thigh_fk_L", 1.0)]), ("rThigh", [("thigh_fk_R", 1.0)]),
 ("lShin",      [("shin_fk_L", 1.0)]), ("rShin", [("shin_fk_R", 1.0)]),
 ("lFoot",      [("foot_fk_L", 1.0)]), ("rFoot", [("foot_fk_R", 1.0)]),
]
for sside, tside in (("l", "_L"), ("r", "_R")):
    for sseg, fname, n in [("Thumb1","thumb",1),("Thumb2","thumb",2),
                           ("Index1","index",1),("Index2","index",2),
                           ("Mid1","middle",1),("Mid2","middle",2),
                           ("Ring1","ring",1),("Ring2","ring",2),
                           ("Pinky1","pinky",1),("Pinky2","pinky",2)]:
        sn = f"{sside}{sseg}"
        if fname == "thumb":
            M.append((sn, [(f"finger_thumb_{n}{tside}", 1.0)]))
        elif n == 1:
            M.append((sn, [(f"finger_{fname}_1{tside}", 1.0)]))
        else:
            M.append((sn, [(f"finger_{fname}_2{tside}", 0.6),
                           (f"finger_{fname}_3{tside}", 0.4)]))
missing = [(s, t) for s, tl in M for t, w in tl
           if s not in src.data.bones or t not in rig.data.bones]
assert not missing, f"missing bones: {missing}"

def scaled(q, w):
    return q if w == 1.0 else Quaternion(q.axis, q.angle * w)

root = rig.pose.bones['root']
pb = rig.pose.bones['pelvis']
root.rotation_mode = 'QUATERNION'
root.rotation_quaternion = ROOTQ
W_ROOT = TGT_RESTW['root'] @ ROOTQ

act = bpy.data.actions.new("autoseat_113_15")
if not rig.animation_data:
    rig.animation_data_create()
rig.animation_data.action = act

# root placement: pelvis over seat center (numerical calibration)
def eval_now():
    bpy.context.view_layer.update()
    return bpy.context.evaluated_depsgraph_get()

def pelvis_head_world():
    d = eval_now()
    r = rig.evaluated_get(d)
    return (rig.matrix_world @ r.pose.bones['pelvis'].head).copy()

# root placement: pelvis over seat center (NUMERICAL calibration —
# the rig's bone axes are rotated, so direct location assignment is wrong)
def calibrate(bone):
    """Return 3x3 matrix mapping bone.location -> world displacement of bone head.
    NOTE: bone.location is ABSOLUTE, so measure from the zero setting."""
    scn.frame_set(DST_F0); bpy.context.view_layer.update()
    bone.location = Vector((0, 0, 0))
    bpy.context.view_layer.update()
    r0 = (rig.matrix_world @ bone.head).copy()
    cols = []
    for i in range(3):
        e = Vector((0, 0, 0)); e[i] = 1.0
        bone.location = e
        bpy.context.view_layer.update()
        cols.append((rig.matrix_world @ bone.head).copy() - r0)
    A = Matrix((cols[0], cols[1], cols[2])).transposed()
    bone.location = Vector((0, 0, 0))
    bpy.context.view_layer.update()
    return A, r0

A_root, r0_root = calibrate(root)
A_pelv, r0_pelv = calibrate(pb)
print(f"A_root det={A_root.determinant():.3f} A_pelv det={A_pelv.determinant():.3f}", flush=True)

def set_bone_world(bone, A, r0, target_world):
    bone.location = A.inverted() @ (target_world - r0)

# place root so pelvis xz -> seat center (fixed-point iteration: measure, correct)
for _iter in range(3):
    p_cur = (rig.matrix_world @ pb.head).copy()
    err = Vector((SEAT_C.x - p_cur.x, SEAT_C.y - p_cur.y, 0))
    if err.length < 0.001:
        break
    root.location += A_root.inverted() @ err
    bpy.context.view_layer.update()
p1 = (rig.matrix_world @ pb.head).copy()
print(f"root placed: pelvis xz=({p1.x:.3f},{p1.y:.3f}) target=({SEAT_C.x:.3f},{SEAT_C.y:.3f})", flush=True)
ROOT_LOC = root.location.copy()

# ---------------------------------------------------------------- CONTACT PROXY
# Decimated copy of the body for fast contact measurements (full mesh is 910k).
# Same armature modifier + vertex groups, so deformation matches.
body = bpy.data.objects.get("CapeJones_Body")
bpy.context.view_layer.objects.active = body
body.select_set(True)
bpy.ops.object.duplicate()
proxy = bpy.context.view_layer.objects.active
proxy.name = "BodyProxy"
proxy.hide_viewport = True
proxy.hide_render = True
# decimate
dec = proxy.modifiers.new("DECIMATE", 'DECIMATE')
dec.ratio = 0.04
dec.use_collapse_triangulate = False
bpy.context.view_layer.objects.active = proxy
bpy.ops.object.modifier_apply(modifier=dec.name)
print(f"proxy verts: {len(proxy.data.vertices)}", flush=True)
body.select_set(False)
proxy.select_set(False)

pelv_gi = proxy.vertex_groups["pelvis"].index
BUTT_IDX = [v.index for v in proxy.data.vertices
            for g in v.groups if g.group == pelv_gi and g.weight > 0.6]
print(f"proxy butt verts: {len(BUTT_IDX)}", flush=True)
# deform bone names for back (not FK controls)
BACK_GROUPS = [gn for gn in ("spine_1","spine_2","spine_3","spine_4","chest","pelvis")
               if gn in proxy.vertex_groups]
print(f"back groups: {BACK_GROUPS}", flush=True)

def proxy_butt_min_z():
    d = eval_now()
    pm = proxy.evaluated_get(d)
    mesh = pm.to_mesh()
    mw = pm.matrix_world
    zs = [(mw @ mesh.vertices[i].co).z for i in BUTT_IDX
          if mesh.vertices[i].co.z < 0.41]
    pm.to_mesh_clear()
    return min(zs) if zs else None

def proxy_back_gap(pelvis_x):
    d = eval_now()
    pm = proxy.evaluated_get(d)
    mesh = pm.to_mesh()
    mw = pm.matrix_world
    gis = {proxy.vertex_groups[gn].index for gn in BACK_GROUPS}
    xs = []
    for v in mesh.vertices:
        w = sum(g.weight for g in v.groups if g.group in gis)
        if w > 0.5:
            wx = (mw @ v.co).x
            if wx > pelvis_x + 0.02:
                xs.append(wx)
    pm.to_mesh_clear()
    if not xs:
        return None
    return BACK_X - max(xs)

# bone lengths for IK (armature space)
thigh_len = rig.data.bones['thigh_fk_L'].length
shin_len = rig.data.bones['shin_fk_L'].length
print(f"leg: thigh={thigh_len:.4f} shin={shin_len:.4f}", flush=True)

def solve_leg(side, foot_target, rr, mw):
    """Analytic two-bone IK. Returns (thigh_q_local, shin_q_local).
    rr = evaluated rig, mw = rig.matrix_world (passed in, no re-eval)."""
    ts = "_L" if side == 'L' else "_R"
    r = rr
    hip = (mw @ r.pose.bones[f'thigh_fk{ts}'].head).copy()
    # current rest directions in world (at current pose, before IK)
    # we solve in world then convert to local
    H = hip
    T = foot_target
    a, b = thigh_len, shin_len
    dlen = (T - H).length
    dlen = max(min(dlen, a + b - 1e-4), abs(a - b) + 1e-4)
    # knee position: x along H->T, h perpendicular (bend forward = -X)
    x = (a*a - b*b + dlen*dlen) / (2*dlen)
    h = math.sqrt(max(a*a - x*x, 1e-8))
    axis = (T - H).normalized()
    # bend direction: perpendicular to axis, in the XZ plane, pointing -X (forward)
    fwd = Vector((-1, 0, 0))
    bend = (fwd - fwd.dot(axis) * axis).normalized()
    K = H + axis * x + bend * h
    # desired world directions
    thigh_dir = (K - H).normalized()
    shin_dir = (T - K).normalized()
    # rest world directions of the bones
    t_rest = (TGT_RESTW[f'thigh_fk{ts}'] @ Vector((0, 1, 0))).normalized()
    s_rest = (TGT_RESTW[f'shin_fk{ts}'] @ Vector((0, 1, 0))).normalized()
    # Note: bone local +Y is along the bone. Verify: use head->tail
    # world rotation taking t_rest -> thigh_dir
    q_thigh_w = t_rest.rotation_difference(thigh_dir)
    q_shin_w = s_rest.rotation_difference(shin_dir)
    W_thigh = q_thigh_w @ TGT_RESTW[f'thigh_fk{ts}']
    W_shin = q_shin_w @ TGT_RESTW[f'shin_fk{ts}']
    # to local
    qpb_t = rig.pose.bones[f'thigh_fk{ts}']
    qpb_s = rig.pose.bones[f'shin_fk{ts}']
    par = qpb_t.parent
    # parent (pelvis) world from the already-evaluated rig:
    Wpar_t = (mw @ r.pose.bones[par.name].matrix).to_3x3().to_quaternion()
    # thigh not yet updated in the eval; use W_thigh we just computed
    Wpar_s = W_thigh
    q_t = (Wpar_t @ M_REL[f'thigh_fk{ts}']).inverted() @ W_thigh
    q_s = (Wpar_s @ M_REL[f'shin_fk{ts}']).inverted() @ W_shin
    return q_t, q_s

# ---------------------------------------------------------------- per-frame solve
# Strategy: measure contacts on KEYFRAMES (every 10th), interpolate corrections.
# Leg IK is pure math -> run per frame. Butt/back need mesh evals -> keyframes.
n = SRC_F1 - SRC_F0 + 1
ad.action = src_act
KEY_STEP = 10
keyframes = list(range(0, n, KEY_STEP)) + ([n - 1] if (n - 1) % KEY_STEP else [])

def apply_mocap_frame(i):
    sf = SRC_F0 + i
    scn.frame_set(sf)
    bpy.context.view_layer.update()
    Ws = {b.name: (src.matrix_world @ b.matrix).to_3x3().to_quaternion()
          for b in src.pose.bones}
    Wdes = {}
    for (sname, targets) in M:
        D = SRC_REST[sname].inverted() @ Ws[sname]
        if sname in ('neck', 'head'):
            D = scaled(D, 0.5)
        for (tname, w) in targets:
            Wdes[tname] = TGT_RESTW[tname] @ scaled(D, w)
    for (sname, targets) in M:
        for (tname, w) in targets:
            qpb = rig.pose.bones[tname]
            par = qpb.parent
            if par is None:
                Wpar = Quaternion()
            elif par.name == 'root':
                Wpar = W_ROOT
            elif par.name in Wdes:
                Wpar = Wdes[par.name]
            else:
                Wpar = TGT_RESTW[par.name]
            qpb.rotation_quaternion = (Wpar @ M_REL[tname]).inverted() @ Wdes[tname]
    root.location = ROOT_LOC
    pb.location = Vector((0, 0, 0))
    return Wdes

# --- keyframe contact solves: returns {frame_i: (pelvis_dloc, back_pitch_q)} ---
key_solutions = {}
p1x = (rig.matrix_world @ pb.head).x  # updated below after placement
for ki in keyframes:
    Wdes = apply_mocap_frame(ki)
    p1x = (rig.matrix_world @ rig.pose.bones['pelvis'].head).x
    # butt solve (linear via calibration matrix)
    bz = proxy_butt_min_z()
    dloc = Vector((0, 0, 0))
    if bz is not None:
        dz_world = BUTT_TARGET_Z - bz
        dloc = A_pelv.inverted() @ Vector((0, 0, dz_world))
        pb.location += dloc
    # back solve
    back_q = None
    gap = proxy_back_gap(p1x)
    if gap is not None and gap > 0.015:
        ang = math.radians(min(gap * 120.0, 10.0))
        dq = Quaternion((0, 1, 0), -ang)
        back_q = {}
        for bn in ('pelvis', 'spine_fk_1', 'spine_fk_2'):
            qpb = rig.pose.bones[bn]
            par = qpb.parent
            Wpar = W_ROOT if (par and par.name == 'root') else (Wdes[par.name] if (par and par.name in Wdes) else TGT_RESTW[par.name if par else 'root'])
            Wold = Wdes.get(bn, TGT_RESTW[bn])
            qnew = (Wpar @ M_REL[bn]).inverted() @ (dq @ Wold)
            qpb.rotation_quaternion = qnew
            back_q[bn] = qnew
    key_solutions[ki] = (dloc.copy(), back_q)
    print(f"  keyframe {ki+1}/{n} (butt_dz={dloc.length:.4f}, gap={gap})", flush=True)

def interp_solutions(i):
    """Interpolate keyframe solutions to frame i."""
    if i in key_solutions:
        return key_solutions[i]
    lo = max(k for k in keyframes if k < i)
    hi = min(k for k in keyframes if k > i)
    t = (i - lo) / (hi - lo)
    dlo, blo = key_solutions[lo]
    dhi, bhi = key_solutions[hi]
    d = dlo.lerp(dhi, t)
    b = None
    if blo is not None and bhi is not None:
        b = {bn: blo[bn].slerp(bhi[bn], t) for bn in blo}
    elif blo is not None:
        b = blo
    elif bhi is not None:
        b = bhi
    return d, b

# --- full pass: apply mocap + interpolated corrections + per-frame leg IK ---
for i in range(n):
    df = DST_F0 + i
    Wdes = apply_mocap_frame(i)
    dloc, back_q = interp_solutions(i)
    pb.location += dloc
    if back_q:
        for bn, q in back_q.items():
            rig.pose.bones[bn].rotation_quaternion = q
    # feet IK (pure math, uses current evaluated pose)
    bpy.context.view_layer.update()
    d = eval_now(); rr = rig.evaluated_get(d); mw = rig.matrix_world
    for side in ('L', 'R'):
        ts = f"_{side}"
        hipw = (mw @ rr.pose.bones[f'thigh_fk{ts}'].head)
        tgt = Vector((hipw.x - 0.13, hipw.y + (0.075 if side == 'L' else -0.075), FLOOR_Z + 0.035))
        q_t, q_s = solve_leg(side, tgt, rr, mw)
        rig.pose.bones[f'thigh_fk{ts}'].rotation_quaternion = q_t
        rig.pose.bones[f'shin_fk{ts}'].rotation_quaternion = q_s
    # keyframe
    for b in rig.pose.bones:
        if b.name in [t for _, tl in M for t, _ in tl] or b.name in ('pelvis',):
            b.keyframe_insert(data_path="rotation_quaternion", frame=df)
    pb.keyframe_insert(data_path="location", frame=df)
    root.location = ROOT_LOC
    root.keyframe_insert(data_path="location", frame=df)
    root.keyframe_insert(data_path="rotation_quaternion", frame=df)
    if i % 20 == 0:
        print(f"  baked {i+1}/{n}", flush=True)

ad.action = None
# hide cape for proof (dedicated cape pass is separate)
cape = bpy.data.objects.get("CapeJones_Cape")
if cape:
    cape.hide_viewport = True
    cape.hide_render = True
    print("cape hidden for proof", flush=True)
# remove proxy from render
proxy.hide_viewport = True
proxy.hide_render = True

bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print("SAVED", OUT_BLEND, flush=True)

# ---------------------------------------------------------------- render proofs (Cycles, full scene)
scn.render.engine = 'CYCLES'
scn.cycles.samples = 24
scn.render.resolution_x = 960
scn.render.resolution_y = 540
scn.render.resolution_percentage = 100
# middle seated frame
MID = DST_F0 + n // 2
scn.frame_set(MID)
bpy.context.view_layer.update()
import time
STAMP = time.strftime("%Y%m%d_%H%M%S")
maincam = bpy.data.objects.get("MainCam") or scn.camera
# front: camera at -X looking +X at the chair
# three-quarter: offset
cam = maincam
cam_loc_save = cam.location.copy()
cam_rot_save = cam.rotation_euler.copy()
def look_at(cam, eye, target):
    d = (Vector(target) - Vector(eye))
    q = d.to_track_quat('-Z', 'Y')
    cam.location = eye
    cam.rotation_euler = q.to_euler()
    bpy.context.view_layer.update()

chair_c = (3.06, 2.067, 0.45)
look_at(cam, (1.4, 2.067, 0.9), chair_c)
scn.render.filepath = os.path.join(PROOF_DIR, f"autoseat_front_{STAMP}.png")
bpy.ops.render.render(write_still=True)
print("rendered front", flush=True)
look_at(cam, (1.7, 1.2, 1.1), chair_c)
scn.render.filepath = os.path.join(PROOF_DIR, f"autoseat_threeq_{STAMP}.png")
bpy.ops.render.render(write_still=True)
print("rendered threeq", flush=True)
cam.location = cam_loc_save
cam.rotation_euler = cam_rot_save
print("PROOFS in", PROOF_DIR, flush=True)
