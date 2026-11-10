"""Cape Jones 3D dance v6 - retarget CMU 15_04 onto the v5 STANDING rig,
with the three owner-ordered v6 fixes at the solve layer:
 1. IDLE: a 24-frame lead-in solved from the SAME mocap take (source
    frames immediately before the loop window, inside the verified
    arms-down standing stretch src 12395-12680) -> the shot opens on a
    true arms-down stance from real data, no hand-keying. (MODE=lead)
 2. FEET GROUNDED: leg solve is contact-aware - when the source toe is
    on the floor (true for 100% of this window: max source toe liftoff
    ~1.5cm, zero liftoff frames), the ankle target is pinned to its
    flat-foot height and the sole is flattened; after each frame's
    solve, a root ground-snap drops the whole body so the lowest toe
    sits exactly at its rest contact height (pelvis drops into the
    squat instead of the feet hovering in world space).
 3. Arms/torso/cape solve is v5's verbatim (probe-verified: at k=0 it
    produces a 10.2-degree upper arm from the 11.9-degree source pose);
    arm swing is NOT damped anywhere.
Modes: -- <out.blend> loop   (96-frame DanceV6Loop + full scene build)
       -- <out.blend> lead   (24-frame IdleIn action, rig only)
Original v5 header follows:
--- Cape Jones 3D dance v5 - STAGE B+C: retarget CMU 15_04 onto the new
STANDING rig (repo CapeJones_Rig, FK layer) and build the dance scene.

Method (repo world-space delta retarget, as in mocap_retarget.py and the
v4 solver - salvaged method, new rig):
 * BVH world joint positions/orientations cached BEFORE the rig gets its
   action (v4 bug lesson 1).
 * Torso: orientation deltas (delta = q_src(t) @ q_src_rest^-1) applied
   about each bone's own head, distributed over the spine FK chain.
 * Limbs: two-bone analytic FK - desired elbow/wrist (knee/ankle) world
   positions rebuilt from the source's own joint directions with the
   TARGET's segment lengths (normalized reach), then each FK bone is
   aimed at its child joint position (rotation about its head point).
   The bend plane comes from the captured elbow/knee itself.
 * Root: mapped hips translation (XZ damp 0.6, Z 0.7 - v4 staging values).
 * Fingers: CMU index/thumb deltas; middle/ring/pinky follow the
   finger-base delta with per-finger falloff (Cascadeur AutoPosing
   method, same as v4).
 * Cape: cape bones take the chest orientation delta lagged 3 frames
   with down-chain falloff (secondary motion), plus a slight constant
   backward droop.
 * Seam: last 12 frames crossfade to the pre-window (v4 loop repair).
Output: scene_v5.blend (96-frame DanceV5 action tiled x19 via NLA =
1824 frames) with the v3 world-cycle set appended (day/LED/night actions
ride along with their objects). Body/cape hidden during the solve.

Run: blender -b <standing_v5.blend> --python solve_v5.py -- <out.blend>
"""
import bpy, math, os, sys, json, time
import numpy as np
from mathutils import Vector, Quaternion, Matrix

OUT = sys.argv[sys.argv.index("--") + 1]
MODE = sys.argv[sys.argv.index("--") + 2] if len(sys.argv) > sys.argv.index("--") + 2 else "loop"
BVH_PATH = "/home/hatch/workspace/_cj_v4_assets/bvh/15_04.bvh"
V3_SCENE = "/home/hatch/workspace/_cj-dance3d-v3/scene_v3.blend"
SRC_START, LOOP, STEP, XFADE = 12625, 96, 5, 12
LEAD = 24
K0, NFRAMES = (0, LOOP) if MODE == "loop" else (-LEAD, LEAD)
ACT_NAME = "DanceV6Loop" if MODE == "loop" else "IdleIn"
ROOT_DAMP, TARGET_H = 0.6, 0.925
SNAP_LOG = []
t00 = time.time()
def log(*a):
    print("[v6solve]", *a, round(time.time() - t00, 1), "s", flush=True)

sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
body = None
for ob in bpy.data.objects:
    if ob.type == "MESH" and len(ob.data.vertices) > 100000:
        body = ob
        break
if body:
    body.hide_viewport = True
    body.hide_render = True
for ob in bpy.data.objects:
    if ob.type == "MESH" and ob != body:
        ob.hide_viewport = True

# FK mode: deform follows FK layer (root custom props)
RPB = rig.pose.bones
for pb in RPB:
    pb.rotation_mode = "QUATERNION"
root_pb = RPB["root"]
for k in ("ik_arm_L", "ik_arm_R", "ik_leg_L", "ik_leg_R", "ik_spine"):
    if k in root_pb.keys():
        root_pb[k] = 0.0

# ---- V6 rest ground references (identity pose, feet flat on floor z=0)
bpy.context.view_layer.update()
def _eval_head(name):
    return (rig.matrix_world @ RPB[name].matrix).to_translation().copy()
REST_TOE_Z = min(_eval_head("toe_L").z, _eval_head("toe_R").z)
REST_ANKLE_Z = min(_eval_head("foot_fk_L").z, _eval_head("foot_fk_R").z)
BODY_MIN_Z = None
if body:
    import numpy as _np
    _vs = _np.empty(len(body.data.vertices) * 3)
    body.data.vertices.foreach_get("co", _vs)
    BODY_MIN_Z = float(_vs[2::3].min() + body.matrix_world.translation.z)
log("rest refs: toe_z", round(REST_TOE_Z, 4), "ankle_z", round(REST_ANKLE_Z, 4),
    "body_min_z", None if BODY_MIN_Z is None else round(BODY_MIN_Z, 4))

# ---------------------------------------------------------------- BVH
sc.render.fps = 120
before = set(bpy.data.objects)
bpy.ops.import_anim.bvh(filepath=BVH_PATH, target="ARMATURE", global_scale=1.0,
                        frame_start=0, use_fps_scale=False, update_scene_fps=False,
                        update_scene_duration=False)
src = next(o for o in bpy.data.objects if o not in before and o.type == "ARMATURE")
SPB = src.pose.bones
log("source:", src.name, len(src.data.bones), "bones")
_CACHE = {}
def sworld(name, frame):
    if frame not in _CACHE:
        sc.frame_set(frame)
        bpy.context.view_layer.update()
        _CACHE[frame] = {n: ((src.matrix_world @ pb.matrix).to_translation().copy(),
                             (src.matrix_world @ pb.matrix).to_quaternion().copy())
                         for n, pb in SPB.items()}
    return _CACHE[frame][name]
SRC_REST = {n: sworld(n, 0) for n in SPB.keys()}
sc.frame_set(0)
bpy.context.view_layer.update()
head_tail = src.matrix_world @ SPB["Head"].tail
foot_min = min((src.matrix_world @ SPB[n].head).z for n in ("LeftFoot", "RightFoot", "LeftToeBase", "RightToeBase"))
SCALE = TARGET_H / (head_tail.z - foot_min)
log("scale", round(SCALE, 5))
for _k in range(K0 - XFADE, LOOP):
    sworld("Hips", SRC_START + int(round(_k * STEP)))
log("cached", len(_CACHE), "frames")
ank = sworld("LeftFoot", 1200)[0]; toe = sworld("LeftToeBase", 1200)[0]
FACING_ROT = Quaternion((0, 0, 1), math.pi) if (toe - ank).y > 0 else Quaternion()
hips_pts, floor_min = [], 1e9
for k in range(-XFADE, LOOP):
    sf = SRC_START + STEP * k
    hips_pts.append(sworld("Hips", sf)[0])
    for nm in ("LeftFoot", "RightFoot", "LeftToeBase", "RightToeBase"):
        floor_min = min(floor_min, sworld(nm, sf)[0].z)
hips_mean = sum(hips_pts, Vector()) / len(hips_pts)
ROOT_Z = 0.7
def map_pos(p):
    v = Vector((p.x - hips_mean.x, p.y - hips_mean.y, p.z - floor_min))
    if FACING_ROT.angle > 0.01:
        v = FACING_ROT @ v
    return Vector((v.x * SCALE * ROOT_DAMP, v.y * SCALE * ROOT_DAMP, v.z * SCALE * ROOT_Z))
def map_quat(q):
    return FACING_ROT @ q if FACING_ROT.angle > 0.01 else q
def desired(name, k):
    sf = SRC_START + STEP * k
    p, q = sworld(name, sf)
    p, q = map_pos(p), map_quat(q)
    if k >= LOOP - XFADE:
        a = (k - (LOOP - XFADE) + 1) / XFADE
        p2, q2 = sworld(name, sf - STEP * LOOP)
        p2, q2 = map_pos(p2), map_quat(q2)
        p = p.lerp(p2, a)
        q = q.slerp(q2, a)
    return p, q
def src_delta(name, k):
    _, q = desired(name, k)
    _, rq = SRC_REST[name]
    return q @ rq.inverted()

# ------------------------------------------------------------ rig helpers
def upd():
    bpy.context.view_layer.update()
def head_of(name):
    return Vector(RPB[name].head)
def rot_about_head(name, q_world):
    """Apply world-space rotation q about the bone's own head point."""
    pb = RPB[name]
    M = pb.matrix.copy()
    h = M.to_translation()
    R = q_world.to_matrix().to_4x4()
    pb.matrix = Matrix.Translation(h) @ R @ Matrix.Translation(-h) @ M
    upd()
def aim(name, target_pos):
    pb = RPB[name]
    h = Vector(pb.head)
    cur = (Vector(pb.tail) - h)
    tgt = Vector(target_pos) - h
    if cur.length < 1e-6 or tgt.length < 1e-6:
        return
    q = cur.normalized().rotation_difference(tgt.normalized())
    rot_about_head(name, q)
def bone_len(name):
    pb = RPB[name]
    return (Vector(pb.tail) - Vector(pb.head)).length

def solve_two_bone(up_name, lo_name, src_up, src_mid, src_lo, k):
    """Aim upper bone at rebuilt elbow pos, lower bone at rebuilt wrist pos.
    Positions rebuilt from source directions with target segment lengths,
    anchored at the target upper bone's evaluated head."""
    S = head_of(up_name)
    _, _ = None, None
    ps, _q = desired(src_up, k)
    pm, _q = desired(src_mid, k)
    pl, _q = desired(src_lo, k)
    d1 = (pm - ps); d2 = (pl - pm)
    if d1.length < 1e-6 or d2.length < 1e-6:
        return
    E = S + d1.normalized() * bone_len(up_name)
    W = E + d2.normalized() * bone_len(lo_name)
    aim(up_name, E)
    aim(lo_name, W)

# FK name resolution (94-bone rig has spine_fk_1..4 + chest_fk; 85-bone
# falls back to deform spine names for the extra joints)
def first(names):
    for n in names:
        if n in RPB:
            return n
    return None
SPINE_LOW = [n for n in ("spine_fk_1", "spine_fk_2", "spine_1", "spine_2") if n in RPB][:2]
SPINE_HI = [n for n in ("spine_fk_3", "spine_fk_4", "chest_fk", "spine_3", "spine_4", "chest") if n in RPB][:3]
log("spine low:", SPINE_LOW, "hi:", SPINE_HI)

act = bpy.data.actions.new(ACT_NAME)
act.use_fake_user = True
rig.animation_data_create()
# DO NOT attach the action while solving (bug found by probe13: with the
# action attached, each frame's rot_about_head premultiplied its delta
# onto a matrix that already contained earlier frames' keyed deltas -
# the deltas COMPOUNDED and the pelvis wound through a full 360 deg
# revolution over the loop). v4's solver set absolute matrices; here we
# solve with the action detached, reset every bone each frame, RECORD
# the resulting bases, and write the keys afterwards.
rig.animation_data.action = None
REC = {}
# V6: recording happens ONCE at the end of each frame, AFTER the ground
# snap - so key_rot/key_loc only mark the bone as posed this frame.
def key_rot(name, f):
    POSED.add(name)
def key_loc(name, f):
    POSED.add(name)
def reset_all_bones():
    for b in RPB:
        b.rotation_quaternion = (1, 0, 0, 0)
        b.rotation_euler = (0, 0, 0)
        b.location = (0, 0, 0)
        b.scale = (1, 1, 1)
    upd()

POSED = set()
CONTACT = {}

def solve_leg_grounded(side, S, k):
    """V6 leg solve: v5's direction-rebuild two-bone aim, made
    contact-aware. When the SOURCE toe is on the floor at this frame
    (raw toe height within 2.5cm of the window floor - true for every
    frame of this window), the ankle target is pinned to the rig's
    flat-foot ankle height and the sole is flattened, so the leg chain
    reaches the floor instead of hovering. Returns the contact flag."""
    up, lo = f"thigh_fk_{side}", f"shin_fk_{side}"
    ps, _ = desired(f"{S}UpLeg", k)
    pm, _ = desired(f"{S}Leg", k)
    pl, _ = desired(f"{S}Foot", k)
    d1 = pm - ps; d2 = pl - pm
    if d1.length < 1e-6 or d2.length < 1e-6:
        return False
    Sh = head_of(up)
    E = Sh + d1.normalized() * bone_len(up)
    W = E + d2.normalized() * bone_len(lo)
    toe_raw = sworld(f"{S}ToeBase", SRC_START + STEP * k)[0].z
    contact = (toe_raw - floor_min) <= 2.5
    if contact:
        W = Vector((W.x, W.y, REST_ANKLE_Z))
    aim(up, E)
    aim(lo, W)
    # foot orientation: v5 ToeBase direction; sole flattened on contact
    tp, _ = desired(f"{S}ToeBase", k)
    fp, _ = desired(f"{S}Foot", k)
    ankle = head_of(f"foot_fk_{side}")
    tgt = ankle + (tp - fp)
    if contact:
        tgt = Vector((tgt.x, tgt.y, ankle.z - (REST_ANKLE_Z - REST_TOE_Z)))
    aim(f"foot_fk_{side}", tgt)
    return contact

REST_MAP = map_pos(SRC_REST["Hips"][0])
log("mapped rest hips:", [round(x, 3) for x in REST_MAP])
for i in range(NFRAMES):
    k = K0 + i
    f = i + 1
    POSED.clear()
    sc.frame_set(f)
    reset_all_bones()
    # root travel: mapped hips position relative to mapped rest hips, so
    # at a rest-equivalent frame the rig stands exactly at its rest spot.
    # V6 ROOT-AXIS FIX (probe I): the root bone's local axes are rotated
    # -90 deg about X vs the world (use_local_location=True; local Y =
    # world Z, local Z = world -Y). v5 assigned the WORLD hips vector
    # straight into the local location channel, so the hips' VERTICAL
    # bounce played back as forward/back sway and the body's height
    # never followed the data - a core half of the floating-feet defect.
    # Convert: local = (world.x, world.z, -world.y).
    hp, _ = desired("Hips", k)
    _w = hp - REST_MAP
    root_pb.location = Vector((_w.x, _w.z, -_w.y))
    key_loc("root", f); POSED.add("root")
    # pelvis orientation delta (hips) - rotation only, about its head
    rot_about_head("pelvis", src_delta("Hips", k))
    key_rot("pelvis", f); POSED.add("pelvis")
    # spine: PARENT-RELATIVE deltas, SPLIT across each chain group.
    # (Second compounding bug, found on the frame-48 crouch: applying a
    # joint's full WORLD delta at every bone of a parented chain adds
    # the delta once per bone - 2-3x over-bend, torso folds shut. The
    # world delta of a child joint already contains its parent's delta,
    # so each group takes only its relative delta, divided by the
    # number of bones sharing it.)
    _IDENT = Quaternion((1, 0, 0, 0))
    def rel_delta(joint, parent_joint):
        return src_delta(joint, k) @ src_delta(parent_joint, k).inverted()
    dq_low = rel_delta("Spine", "Hips")
    for nm in SPINE_LOW:
        rot_about_head(nm, _IDENT.slerp(dq_low, 1.0 / len(SPINE_LOW)))
        key_rot(nm, f); POSED.add(nm)
    dq_hi = rel_delta("Spine1", "Spine")
    for nm in SPINE_HI:
        rot_about_head(nm, _IDENT.slerp(dq_hi, 1.0 / len(SPINE_HI)))
        key_rot(nm, f); POSED.add(nm)
    # clavicles: shoulder delta relative to the chest (Spine1)
    for S, side in (("Left", "L"), ("Right", "R")):
        nm = f"clavicle_{side}"
        rot_about_head(nm, rel_delta(f"{S}Shoulder", "Spine1"))
        key_rot(nm, f); POSED.add(nm)
    # neck + head: parent-relative, neck delta split across neck bones
    neck_bones = [n for n in ("neck_1", "neck_2") if n in RPB]
    dq_neck = rel_delta("Neck1", "Spine1")
    for nm in neck_bones:
        rot_about_head(nm, _IDENT.slerp(dq_neck, 1.0 / len(neck_bones)))
        key_rot(nm, f); POSED.add(nm)
    rot_about_head("head", rel_delta("Head", "Neck1")); key_rot("head", f); POSED.add("head")
    # arms (FK layer) + legs (FK layer)
    for S, side in (("Left", "L"), ("Right", "R")):
        solve_two_bone(f"upperarm_fk_{side}", f"forearm_fk_{side}",
                       f"{S}Arm", f"{S}ForeArm", f"{S}Hand", k)
        key_rot(f"upperarm_fk_{side}", f); key_rot(f"forearm_fk_{side}", f)
        POSED.add(f"upperarm_fk_{side}"); POSED.add(f"forearm_fk_{side}")
        # hand orientation: PARENT-RELATIVE wrist delta only. hand_fk
        # inherits the solved forearm motion through parenting; applying
        # the source hand's full world delta on top double-rotates the
        # hand layer and shears the mitten's mixed wrist weights (the
        # gate bisect: 71-97 deg of imposed divergence tears the wrist;
        # the true wrist delta in this window is small). Relative delta
        # = hand world delta composed with inverse forearm world delta.
        dq_hand = src_delta(f"{S}Hand", k)
        dq_fore = src_delta(f"{S}ForeArm", k)
        rot_about_head(f"hand_fk_{side}", dq_hand @ dq_fore.inverted())
        key_rot(f"hand_fk_{side}", f); POSED.add(f"hand_fk_{side}")
        contact = solve_leg_grounded(side, S, k)
        key_rot(f"thigh_fk_{side}", f); key_rot(f"shin_fk_{side}", f)
        key_rot(f"foot_fk_{side}", f)
        CONTACT[f"{side}"] = contact
    # fingers: index + thumb deltas; middle/ring/pinky from finger base
    for S, side in (("Left", "L"), ("Right", "R")):
        chans = [(f"{S}HandIndex1", [f"finger_index_{i}_{side}" for i in (1, 2, 3)], 1.0),
                 (f"{S}HandThumb1", [f"finger_thumb_{i}_{side}" for i in (1, 2)], 1.0),
                 (f"{S}FingerBase", [f"finger_middle_{i}_{side}" for i in (1, 2, 3)], 0.85),
                 (f"{S}FingerBase", [f"finger_ring_{i}_{side}" for i in (1, 2, 3)], 0.7),
                 (f"{S}FingerBase", [f"finger_pinky_{i}_{side}" for i in (1, 2, 3)], 0.55)]
        dq_hand_abs = src_delta(f"{S}Hand", k)
        for src_joint, bones_, fall in chans:
            if src_joint not in SPB:
                continue
            # parent-relative: finger deform bones are children of the
            # hand; their world delta must not re-apply the hand's own
            # delta (same double-rotation shear as the wrist)
            dq = src_delta(src_joint, k) @ dq_hand_abs.inverted()
            if fall != 1.0:
                ident = Quaternion((1, 0, 0, 0))
                dq = ident.slerp(dq, fall)
            # split across the chain: each segment bone takes an equal
            # share of the finger's relative delta (full delta at every
            # segment tripled the curl)
            share = Quaternion((1, 0, 0, 0)).slerp(dq, 1.0 / len(bones_))
            for bn in bones_:
                if bn in RPB:
                    rot_about_head(bn, share)
                    key_rot(bn, f); POSED.add(bn)
    # cape: chest delta lagged (use k-3 source delta via Spine1 at k-3)
    kk = max(k - 3, -XFADE)
    dq_cape = src_delta("Spine1", kk) if kk >= 0 else src_delta("Spine1", 0)
    for i, cn in enumerate(("cape_1", "cape_2", "cape_3")):
        if cn in RPB:
            ident = Quaternion((1, 0, 0, 0))
            # chain fractions summing to ~1.0 at the tip (the old
            # 0.85/0.7/0.55 per-bone takes compounded to 2.1x at cape_3
            # and the sheet whipped over the head)
            dq = ident.slerp(dq_cape, (0.5, 0.3, 0.2)[i])
            rot_about_head(cn, dq)
            key_rot(cn, f); POSED.add(cn)
    # ---- V6 IDLE RELAXATION (lead mode only): the source dancer's hang
    # still splays the forearm ~25 deg (natural carrying angle on a
    # bulky sculpt reads as arms-out). For the IDLE stance only, settle
    # the arms the last stretch toward the body - upperarm 5 deg,
    # forearm 14 deg toward straight-down, ramped in/out across the
    # lead-in so the loop seam stays pure data. The dance itself is
    # never touched by this.
    if MODE == "lead":
        _r = min(1.0, (i + 1) / 5.0, (NFRAMES - i) / 5.0)
        _r = _r * _r * (3 - 2 * _r)
        if _r > 0:
            for _side in ("L", "R"):
                for _bn, _deg in ((f"upperarm_fk_{_side}", 5.0), (f"forearm_fk_{_side}", 14.0)):
                    _pb = RPB[_bn]
                    _m = _pb.matrix
                    _h = _m.to_translation()
                    _t = _m @ Vector((0, _pb.length, 0))
                    _d = (_t - _h).normalized()
                    _full = _d.rotation_difference(Vector((0, 0, -1)))
                    _ang = math.degrees(_full.angle)
                    if _ang > 0.5:
                        _q = Quaternion((1, 0, 0, 0)).slerp(_full, min(_deg * _r / _ang, 1.0))
                        rot_about_head(_bn, _q)
    # ---- V6 GROUND SNAP + record. The lowest toe must sit exactly at
    # its rest contact height; the whole body (root) drops/rises by the
    # residual, so the pelvis falls INTO the squat and the feet stop
    # hovering in world space. Applied every frame: the source window
    # is in contact 100% of the time (probe-verified).
    upd()
    toe_z = min((rig.matrix_world @ RPB[n].matrix).to_translation().z
                for n in ("toe_L", "toe_R"))
    shift = toe_z - REST_TOE_Z
    if abs(shift) > 0.0005:
        if abs(shift) < 0.09:
            # world -shift in Z == root-local -shift in Y (probe I axes)
            _l = root_pb.location
            root_pb.location = Vector((_l.x, _l.y - shift, _l.z))
            upd()
        else:
            log("WARN snap too large, skipped:", k, round(shift, 4))
            shift = 0.0
    SNAP_LOG.append((k, round(shift, 4), CONTACT.get("L"), CONTACT.get("R")))
    for name in POSED:
        REC.setdefault(f, {})[name] = (Vector(RPB[name].location),
                                       Quaternion(RPB[name].rotation_quaternion))
    if k % 24 == 0:
        log("frame", f, "posed bones:", len(POSED))

# ---- write the recorded bases into the action (absolute keys)
rig.animation_data.action = act
for f in sorted(REC):
    sc.frame_set(f)
    for name, (loc, quat) in REC[f].items():
        pb = RPB[name]
        pb.location = loc
        pb.rotation_quaternion = quat
        pb.keyframe_insert("location", frame=f)
        pb.keyframe_insert("rotation_quaternion", frame=f)
log("keys written:", len(REC), "frames")
log("snap log (k, shift, contactL, contactR):", SNAP_LOG[:6], "... total", len(SNAP_LOG),
    "max |shift|", max((abs(s[1]) for s in SNAP_LOG), default=0))
# ---- V6 SELF-CHECK: re-evaluate the STORED action (no solving) and
# measure what playback will actually show. Catches any write/playback
# divergence at the source instead of after a render.
import math as _math
def _sc_angle(name):
    pb = RPB[name]
    m = rig.matrix_world @ pb.matrix
    h = m.to_translation(); t = m @ Vector((0, pb.length, 0))
    return round(_math.degrees((t - h).normalized().angle(Vector((0, 0, -1)))), 1)
def _sc_toe():
    return round(min((rig.matrix_world @ RPB[n].matrix).to_translation().z
                     for n in ("toe_L", "toe_R")) - REST_TOE_Z, 4)
for _f in sorted(REC)[:1] + [sorted(REC)[len(REC) // 2]]:
    sc.frame_set(_f)
    upd()
    log("SELFCHECK frame", _f, "arm_fk_L", _sc_angle("upperarm_fk_L"),
        "arm_fk_R", _sc_angle("upperarm_fk_R"), "toe_above_rest_contact", _sc_toe())
log("solve done", round(time.time() - t00, 1), "s")
if MODE == "lead":
    bpy.data.objects.remove(src, do_unlink=True)
    rig.animation_data.action = None
    act.use_fake_user = True
    sc.frame_start, sc.frame_end = 1, NFRAMES
    bpy.ops.wm.save_as_mainfile(filepath=OUT)
    print("SOLVE_V6_DONE", OUT, MODE)
    sys.exit(0)

# ------------------------------------------------------------- scene build
# remove the BVH source armature from the output
bpy.data.objects.remove(src, do_unlink=True)
# append the v3 set (world cycle: sun/moon/stars/LEDs carry their actions)
skip = {"CapeJones_Rig", "BodyR", "CapeSheet", "BlenRigMdefCage"}
with bpy.data.libraries.load(V3_SCENE) as (data_from, data_to):
    data_to.objects = [n for n in data_from.objects if n not in skip]
for ob in data_to.objects:
    if ob is not None:
        sc.collection.objects.link(ob)
# cape: append the proven one-piece CapeSheet and bind to this rig
with bpy.data.libraries.load(V3_SCENE) as (data_from, data_to):
    data_to.objects = ["CapeSheet"]
sheet = data_to.objects[0]
sc.collection.objects.link(sheet)
for md in sheet.modifiers:
    if md.type == "ARMATURE":
        md.object = rig
        md.use_deform_preserve_volume = True
sheet.hide_viewport = False
sheet.hide_render = False
# the base file's cloth cape (sitting-line asset) is not the dance cape,
# and the BlenRig cage is a deform helper that must never render
for ob in list(bpy.data.objects):
    if ob.type == "MESH" and ob != body and ob != sheet and (
            len(ob.data.vertices) > 20000 or ob.name == "BlenRigMdefCage"):
        ob.hide_render = True
        ob.hide_viewport = True
if body:
    body.hide_viewport = False
    body.hide_render = False
# V6: NO NLA tiling here. DanceV6Loop is stored as a plain action; the
# assembly step bakes the full 1824-frame timeline (idle lead-in +
# loop tiles + idle return) into ONE action, so what is gated is
# exactly what is rendered - no strip mapping in between.
ad = rig.animation_data
ad.action = None
act.use_fake_user = True
sc.render.fps = 24
sc.frame_start, sc.frame_end = 1, 1824
cam = bpy.data.objects.get("MainCam")
if cam:
    sc.camera = cam
sc.render.engine = "BLENDER_WORKBENCH"
sc.display.shading.light = "STUDIO"
sc.display.shading.color_type = "MATERIAL"
sc.render.resolution_x, sc.render.resolution_y = 960, 540
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SOLVE_V6_DONE", OUT, MODE)
