"""Cape Jones dance v4 - STAGE B: retarget CMU 15_04 (front-facing window
@12625, chosen by bvh_facing_scan.py: front_frac 1.00, seam 0.57) onto the
Rigify rig. (First pick, CMU 61_03 salsa @1010, was rejected: the dancer
faces ~-90 deg profile for the whole window - partner work.)

World-space delta retargeting (repo method, mocap_retarget.py):
  R_ctrl(t) = R_ctrl_rest @ (R_src_rest^-1 @ R_src(t))     (orientation delta)
  P_ctrl(t) = P_joint_mapped(t) + (P_ctrl_rest - P_joint_rest_mapped)
IK controls (hands, feet, toes) take the mocap joints' world positions;
poles take elbow/knee positions pushed along the limb's own bend direction.
Fingers: CMU LeftHandIndex1/LThumb deltas drive index/thumb chains;
LeftFingerBase delta drives middle/ring/pinky (master coupling).
Cape: verlet spring chain trailing the solved chest, driving the Rigify
spline-tentacle hook controls cape.mid01 / cape.end01 (Cascadeur
secondary-motion method: stiffness falloff + damping + gravity).
Seam: last 12 frames crossfade toward the pre-window frames so frame 96
wraps exactly onto frame 0's neighbourhood (standard loop repair).

Opens rig_v4.blend, writes scene_v4.blend + measurements.json.
"""
import bpy, math, os, json, time
import numpy as np
from mathutils import Vector, Quaternion, Matrix

WORK = "/home/hatch/workspace/_cj_v4_build"
BVH_PATH = "/home/hatch/workspace/_cj_v4_assets/bvh/15_04.bvh"
SRC_START, LOOP, STEP, XFADE = 12625, 96, 5, 12
ROOT_DAMP, TARGET_H = 0.6, 0.925
t00 = time.time()
def log(*a):
    print("[v4solve]", *a, round(time.time() - t00, 1), "s", flush=True)

bpy.ops.wm.open_mainfile(filepath=os.path.join(WORK, "rig_v4.blend"))
sc = bpy.context.scene
sc.render.fps = 120  # source-native rate during solve
rig = bpy.data.objects["CapeJones_Rigify"]
body = bpy.data.objects["BodyR"]
sheet_ob = bpy.data.objects["CapeSheet"]
body.hide_viewport = True   # skip 107k-vert eval during the solve
sheet_ob.hide_viewport = True

# ---------------------------------------------------------------- BVH import
before = set(bpy.data.objects)
bpy.ops.import_anim.bvh(filepath=BVH_PATH, target="ARMATURE", global_scale=1.0,
                        frame_start=0, use_fps_scale=False, update_scene_fps=False,
                        update_scene_duration=False)
src = next(o for o in bpy.data.objects if o not in before and o.type == "ARMATURE")
log("source armature:", src.name, "bones:", len(src.data.bones))
SPB = src.pose.bones

_CACHE = {}
_SOLVING = [False]
def sworld(name, frame):
    if frame not in _CACHE:
        if _SOLVING[0]:
            raise RuntimeError(f"source cache miss during solve at frame {frame}")
        sc.frame_set(frame)
        bpy.context.view_layer.update()
        _CACHE[frame] = {n: ((src.matrix_world @ pb.matrix).to_translation().copy(),
                             (src.matrix_world @ pb.matrix).to_quaternion())
                         for n, pb in SPB.items()}
    return _CACHE[frame][name]

def sworld_mat(name, frame):
    sc.frame_set(frame)
    bpy.context.view_layer.update()
    return (src.matrix_world @ SPB[name].matrix).copy()

# rest (frame 0 = T-pose in the cgspeed conversion)
SRC_REST = {}
for n in SPB.keys():
    p, q = sworld(n, 0)
    SRC_REST[n] = (p, q)
head_top = SRC_REST["Head"][0] + (src.matrix_world.to_quaternion() @ Vector((0, 1, 0))) * 0.0  # placeholder
# height: head joint + head bone length vs lowest foot at rest
sc.frame_set(0); bpy.context.view_layer.update()
head_pb = SPB["Head"]
head_world_tail = src.matrix_world @ head_pb.tail
foot_min = min((src.matrix_world @ SPB[n].head).z for n in ("LeftFoot", "RightFoot", "LeftToeBase", "RightToeBase"))
SRC_H = head_world_tail.z - foot_min
SCALE = TARGET_H / SRC_H
log("source height", round(SRC_H, 3), "scale", round(SCALE, 5))

# Pre-sample EVERY source frame the solve will touch, BEFORE the target rig
# gets its action: sworld() frame_sets the shared scene, and once the rig
# carries an action those frame_sets would corrupt the evaluated parents
# that set_ctrl_world reads. After this, desired() is cache-only.
for _k in range(-12, LOOP):
    sworld("Hips", SRC_START + int(round(_k * STEP)))
log("source cache frames:", len(_CACHE))
# facing: toe-ankle direction at a mid frame
ank = sworld("LeftFoot", 1200)[0]; toe = sworld("LeftToeBase", 1200)[0]
FACING_ROT = Quaternion((0, 0, 1), math.pi) if (toe - ank).y > 0 else Quaternion()
log("source faces +Y -> pre-rotating" if (toe - ank).y > 0 else "source faces -Y already")

# window statistics: hips centroid + floor
hips_pts, floor_min = [], 1e9
for k in range(-XFADE, LOOP):
    sf = SRC_START + STEP * k
    hp, _ = sworld("Hips", sf)
    hips_pts.append(hp)
    for n in ("LeftFoot", "RightFoot", "LeftToeBase", "RightToeBase"):
        floor_min = min(floor_min, sworld(n, sf)[0].z)
hips_mean = sum(hips_pts, Vector()) / len(hips_pts)

ROOT_Z = 0.7   # vertical damping: the source's exercise-depth squats would
               # over-stretch the spine chain; 0.7 keeps the shape, shallower
def map_pos(p):
    """BVH world position -> stage position (recenter, damp XZ, floor at 0)."""
    v = Vector((p.x - hips_mean.x, p.y - hips_mean.y, p.z - floor_min))
    if FACING_ROT.angle > 0.01:
        v = FACING_ROT @ v
    return Vector((v.x * SCALE * ROOT_DAMP, v.y * SCALE * ROOT_DAMP, v.z * SCALE * ROOT_Z))

def map_quat(q):
    return FACING_ROT @ q if FACING_ROT.angle > 0.01 else q

# desired world transform for a source joint at output frame k (with crossfade)
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

# ---------------------------------------------------------------- rig setup
RPB = rig.pose.bones
for pb in RPB:
    pb.rotation_mode = "QUATERNION"
CTRL_REST = {}
for pb in RPB:
    CTRL_REST[pb.name] = (pb.head.copy(), (rig.matrix_world @ pb.matrix).to_quaternion(), pb.matrix.copy())
act = bpy.data.actions.new("DanceV4Loop")
rig.animation_data_create()
rig.animation_data.action = act

def key(pb, frame, loc=True, rot=True, scale=False):
    if loc: pb.keyframe_insert("location", frame=frame)
    if rot: pb.keyframe_insert("rotation_quaternion", frame=frame)
    if scale: pb.keyframe_insert("scale", frame=frame)

# IK/FK: full IK on arms + legs for the whole loop
for parent_name in ("upper_arm_parent.L", "upper_arm_parent.R", "thigh_parent.L", "thigh_parent.R"):
    pb = RPB[parent_name]
    pb["IK_FK"] = 0.0
    pb.keyframe_insert('["IK_FK"]', frame=1)

def depth(name):
    d, b = 0, rig.data.bones[name]
    while b.parent:
        d += 1; b = b.parent
    return d

def set_ctrl_world(ctrl, des_p, des_q, frame, joint_rest_p):
    """Drive a control bone to a desired world transform via the delta method."""
    pb = RPB[ctrl]
    rest_p, rest_q, _ = CTRL_REST[ctrl]
    # orientation: control rest * source delta is applied by caller via des_q
    m = Matrix.Translation(des_p) @ des_q.to_matrix().to_4x4()
    pb.matrix = m
    return pb

# Torso group: rotation deltas (+ anchored hips position). Limb IK targets
# are computed AFTER the torso is posed, relative to the evaluated shoulder /
# hip anchors, scaled by the limb-length ratio and reach-clamped - the
# HumanIK/Rokoko-style normalized-reach retarget. (Position-delta from the
# T-pose rest hand overshoots when the two skeletons' proportions differ.)
TORSO_MAP = [
    ("hips",  "Hips", "P"),
    ("torso", "Spine", "R"),
    ("chest", "Spine1", "PR"),
    ("neck",  "Neck1", "RW"),
    ("head",  "Head", "RW"),
    ("shoulder.L", "LeftShoulder", "RW"),
    ("shoulder.R", "RightShoulder", "RW"),
]
ordered = sorted(TORSO_MAP, key=lambda m: depth(m[0]))

def seg3(a, b, c):
    return (b - a).length + (c - b).length
RATIOS = {}
for S, T in (("Left", "L"), ("Right", "R")):
    src_arm = seg3(SRC_REST[f"{S}Arm"][0], SRC_REST[f"{S}ForeArm"][0], SRC_REST[f"{S}Hand"][0]) * SCALE
    tgt_arm = (RPB[f"DEF-hand.{T}"].head - RPB[f"DEF-upper_arm.{T}"].head).length
    src_leg = seg3(SRC_REST[f"{S}UpLeg"][0], SRC_REST[f"{S}Leg"][0], SRC_REST[f"{S}Foot"][0]) * SCALE
    tgt_leg = (RPB[f"DEF-foot.{T}"].head - RPB[f"DEF-thigh.{T}"].head).length
    src_ft = (SRC_REST[f"{S}ToeBase"][0] - SRC_REST[f"{S}Foot"][0]).length * SCALE
    tgt_ft = (RPB[f"DEF-toe.{T}"].tail - RPB[f"DEF-foot.{T}"].head).length
    RATIOS[T] = {"arm": tgt_arm / src_arm, "leg": tgt_leg / src_leg, "foot": tgt_ft / max(src_ft, 1e-6),
                 "arm_len": tgt_arm, "leg_len": tgt_leg, "foot_len": tgt_ft}
    log("ratios", T, {kk: round(vv, 3) for kk, vv in RATIOS[T].items()})

def des_quat(ctrl, joint, k):
    _, q = desired(joint, k)
    _, rq = SRC_REST[joint]
    delta = q @ map_quat(rq).inverted()
    des_q = delta @ CTRL_REST[ctrl][1]
    if ctrl in PREV_Q and des_q.dot(PREV_Q[ctrl]) < 0:
        des_q = -des_q
    PREV_Q[ctrl] = des_q
    return des_q

def anchor_world(defname):
    return rig.matrix_world @ RPB[defname].head

def reach(anchor, vec, ratio, maxlen):
    v = vec * ratio
    if v.length > maxlen:
        v = v.normalized() * maxlen
    return anchor + v

PREV_Q = {}
solved_chest = []   # chest world matrices per frame, for the cape pass
_SOLVING[0] = True
for k in range(LOOP):
    f = k + 1
    sc.frame_set(f)
    # ---- torso group (positions precomputed: the torso anchor must FOLLOW
    # the hips translation, or the Rigify spine mechanism stretches the
    # spine deform bones to bridge the gap - the squat "puffer torso")
    p_hips, _ = desired("Hips", k)
    rp_hips, _ = SRC_REST["Hips"]
    hips_des_p = p_hips + Vector((0, 0, CTRL_REST["hips"][0].z - map_pos(rp_hips).z))
    hips_delta = hips_des_p - CTRL_REST["hips"][0]
    torso_des = {}
    for ctrl, joint, mode in TORSO_MAP:
        p, _ = desired(joint, k)
        rp, _ = SRC_REST[joint]
        rest_p = CTRL_REST[ctrl][0]
        if ctrl == "hips":
            des_p = hips_des_p
        elif ctrl == "torso":
            des_p = rest_p + hips_delta
        elif mode == "PR":   # chest: hips follow + relative chest motion, damped
            des_p = rest_p + hips_delta + ((p - map_pos(rp)) - (p_hips - map_pos(rp_hips))) * 0.6
        else:
            des_p = rest_p
        torso_des[ctrl] = (des_p, des_quat(ctrl, joint, k))
    cur_depth = -1
    for ctrl, joint, mode in ordered:
        d = depth(ctrl)
        if d != cur_depth:
            bpy.context.view_layer.update()
            cur_depth = d
        if mode == "RW":
            # rotation-only in world space: keep the position the parents
            # produced (assigning a fixed world position here would pin the
            # bone and stretch the chain - the spine.003 puffer bug)
            pb = RPB[ctrl]
            cur_p = (rig.matrix_world @ pb.matrix).to_translation()
            pb.matrix = Matrix.Translation(cur_p) @ torso_des[ctrl][1].to_matrix().to_4x4()
            key(pb, f)
        else:
            pb = set_ctrl_world(ctrl, torso_des[ctrl][0], torso_des[ctrl][1], f, None)
            key(pb, f)
    bpy.context.view_layer.update()
    # ---- limb IK targets from evaluated anchors
    limb = {}
    for S, T in (("Left", "L"), ("Right", "R")):
        R = RATIOS[T]
        sh = anchor_world(f"DEF-upper_arm.{T}")
        hp = anchor_world(f"DEF-thigh.{T}")
        p_sh, _ = desired(f"{S}Arm", k); p_el, _ = desired(f"{S}ForeArm", k); p_ha, _ = desired(f"{S}Hand", k)
        hand_p = reach(sh, p_ha - p_sh, R["arm"], R["arm_len"] * 0.99)
        elbow_p = reach(sh, p_el - p_sh, R["arm"], R["arm_len"] * 0.99)
        p_up, _ = desired(f"{S}UpLeg", k); p_kn, _ = desired(f"{S}Leg", k); p_ft, _ = desired(f"{S}Foot", k)
        foot_p = reach(hp, p_ft - p_up, R["leg"], R["leg_len"] * 0.99)
        foot_p.z = max(foot_p.z, 0.045)
        knee_p = reach(hp, p_kn - p_up, R["leg"], R["leg_len"] * 0.99)
        limb[T] = (hand_p, elbow_p, foot_p, knee_p, sh, hp)
    for S, T in (("Left", "L"), ("Right", "R")):
        hand_p, elbow_p, foot_p, knee_p, sh, hp = limb[T]
        for ctrl, joint, pos in ((f"hand_ik.{T}", f"{S}Hand", hand_p), (f"foot_ik.{T}", f"{S}Foot", foot_p)):
            pb = set_ctrl_world(ctrl, pos, des_quat(ctrl, joint, k), f, None)
            key(pb, f)
        for ctrl, mid_p, a_p, b_p in ((f"upper_arm_ik_target.{T}", elbow_p, sh, hand_p),
                                      (f"thigh_ik_target.{T}", knee_p, hp, foot_p)):
            out = mid_p - (a_p + b_p) * 0.5
            if out.length < 1e-6:
                out = Vector((0, 1, 0))
            pb = RPB[ctrl]
            pb.matrix = Matrix.Translation(mid_p + out.normalized() * 0.22) @ CTRL_REST[ctrl][1].to_matrix().to_4x4()
            key(pb, f, rot=False)
    bpy.context.view_layer.update()
    # ---- toes from evaluated foot anchors
    for S, T in (("Left", "L"), ("Right", "R")):
        R = RATIOS[T]
        fa = anchor_world(f"DEF-foot.{T}")
        p_ft, _ = desired(f"{S}Foot", k); p_to, _ = desired(f"{S}ToeBase", k)
        toe_p = reach(fa, p_to - p_ft, R["foot"], R["foot_len"] * 0.99)
        pb = set_ctrl_world(f"toe_ik.{T}", toe_p, des_quat(f"toe_ik.{T}", f"{S}ToeBase", k), f, None)
        key(pb, f)
    bpy.context.view_layer.update()
    solved_chest.append((rig.matrix_world @ RPB["chest"].matrix).copy())
    if k % 24 == 0:
        log("solved frame", f)

# ---------------------------------------------------------------- fingers
def qpow(q, t):
    return Quaternion((1, 0, 0, 0)).slerp(q, t)
FING = []  # (ctrl, source joint, fraction)
for side_s, side_t in (("Left", "L"), ("Right", "R")):
    FING += [(f"f_index.01.{side_t}", f"{side_s}HandIndex1", 0.75),
             (f"f_index.02.{side_t}", f"{side_s}HandIndex1", 0.55),
             (f"f_index.03.{side_t}", f"{side_s}HandIndex1", 0.40),
             (f"thumb.01.{side_t}", f"{side_s}Thumb", 0.7),
             (f"thumb.02.{side_t}", f"{side_s}Thumb", 0.55),
             (f"thumb.03.{side_t}", f"{side_s}Thumb", 0.4)]
    for fname, frac in (("f_middle", 0.95), ("f_ring", 0.85), ("f_pinky", 0.75)):
        for seg, sf_ in ((1, 0.7), (2, 0.5), (3, 0.35)):
            FING.append((f"{fname}.{seg:02d}.{side_t}", f"{side_s}FingerBase", frac * sf_))
FING_PREV = {}
for k in range(LOOP):
    f = k + 1
    for ctrl, joint, frac in FING:
        if ctrl not in RPB or joint not in SPB:
            continue
        _, q = desired(joint, k)
        _, rq = SRC_REST[joint]
        delta = qpow(map_quat(rq).inverted() @ q, frac)
        if ctrl in FING_PREV and delta.dot(FING_PREV[ctrl]) < 0:
            delta = -delta
        FING_PREV[ctrl] = delta
        pb = RPB[ctrl]
        pb.rotation_quaternion = delta
        pb.keyframe_insert("rotation_quaternion", frame=f)
log("fingers keyed")

# ---------------------------------------------------------------- cape (verlet)
# cape rest points in chest-local space (from the metarig cape chain coords,
# expressed against the DEF-spine.003 rest matrix)
chest_rest_m = CTRL_REST["chest"][2]
cape_local = [chest_rest_m.inverted() @ Vector(p) for p in
              [(0.0, 0.098, 0.750), (0.0, 0.108, 0.620), (0.0, 0.114, 0.490),
               (0.0, 0.118, 0.360), (0.0, 0.118, 0.230), (0.0, 0.112, 0.100)]]
seg_len = [ (cape_local[i + 1] - cape_local[i]).length for i in range(5)]
STIFF = [0.0, 0.38, 0.26, 0.17, 0.11, 0.07]
pts = None; prev = None
cape_frames = []
for rep in range(3):
    for k in range(LOOP):
        cm = solved_chest[k]
        anchors = [cm @ p for p in cape_local]
        if pts is None:
            pts = [Vector(a) for a in anchors]; prev = [Vector(a) for a in anchors]
        new = []
        for i in range(6):
            if i == 0:
                new.append(Vector(anchors[0])); continue
            vel = (pts[i] - prev[i]) * 0.90
            q = pts[i] + vel + Vector((0, 0, -0.0035))
            q = q.lerp(anchors[i], STIFF[i])
            new.append(q)
        for _ in range(3):  # distance constraints down the chain
            new[0] = Vector(anchors[0])
            for i in range(1, 6):
                d = new[i] - new[i - 1]
                if d.length > 1e-9:
                    new[i] = new[i - 1] + d.normalized() * seg_len[i - 1]
        prev, pts = pts, new
        if rep == 2:
            cape_frames.append([Vector(p) for p in pts])
for k in range(LOOP):
    f = k + 1
    for ctrl, pi in (("cape.mid01", 3), ("cape.end01", 5), ("cape.end", 5)):
        if ctrl not in RPB:
            continue
        pb = RPB[ctrl]
        pb.matrix = Matrix.Translation(cape_frames[k][pi]) @ pb.matrix.to_quaternion().to_matrix().to_4x4()
        pb.keyframe_insert("location", frame=f)
log("cape keyed")

# ---------------------------------------------------------------- NLA tile
rig.animation_data.action = None
track = rig.animation_data.nla_tracks.new()
track.name = "DanceV4"
strip = track.strips.new("DanceV4Loop", 1, act)
strip.repeat = 19.0
strip.use_sync_length = False
sc.frame_start, sc.frame_end = 1, 1824
sc.render.fps = 24
body.hide_viewport = False
sheet_ob.hide_viewport = False
bpy.data.objects.remove(src, do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(WORK, "scene_v4.blend"))
log("saved scene_v4.blend")

# ---------------------------------------------------------------- measurements
rig.animation_data.action = act  # measure the loop directly
def bpos(name):
    pb = RPB[name]
    return rig.matrix_world @ pb.head, rig.matrix_world @ pb.tail
def bang(a, b, c):
    """angle at b between a and c, degrees"""
    v1, v2 = a - b, c - b
    if v1.length < 1e-9 or v2.length < 1e-9:
        return 0.0
    return math.degrees(v1.angle(v2))
def qrange(name, samples):
    qs = []
    for f in samples:
        sc.frame_set(f); bpy.context.view_layer.update()
        qs.append((rig.matrix_world @ RPB[name].matrix).to_quaternion())
    mx = 0.0
    for i in range(len(qs)):
        for j in range(i + 1, len(qs)):
            mx = max(mx, math.degrees(qs[i].rotation_difference(qs[j]).angle))
    return mx
M = {}
samples = list(range(1, LOOP + 1, 2))
series = {k: [] for k in ("elbowL", "elbowR", "kneeL", "kneeR", "ankleL", "ankleR",
                          "finger", "armdirL", "armdirR", "pelvis", "footL", "footR", "capetip")}
for f in samples:
    sc.frame_set(f); bpy.context.view_layer.update()
    S = lambda n: bpos(n)[0]
    series["elbowL"].append(bang(S("DEF-upper_arm.L"), S("DEF-forearm.L"), S("DEF-hand.L")))
    series["elbowR"].append(bang(S("DEF-upper_arm.R"), S("DEF-forearm.R"), S("DEF-hand.R")))
    series["kneeL"].append(bang(S("DEF-thigh.L"), S("DEF-shin.L"), S("DEF-foot.L")))
    series["kneeR"].append(bang(S("DEF-thigh.R"), S("DEF-shin.R"), S("DEF-foot.R")))
    series["ankleL"].append(bang(S("DEF-shin.L"), S("DEF-foot.L"), S("DEF-toe.L")))
    series["ankleR"].append(bang(S("DEF-shin.R"), S("DEF-foot.R"), S("DEF-toe.R")))
    series["finger"].append(bang(S("DEF-f_middle.01.L"), S("DEF-f_middle.02.L"), S("DEF-f_middle.03.L")))
    for nm, key_ in (("DEF-upper_arm.L", "armdirL"), ("DEF-upper_arm.R", "armdirR")):
        h, t = bpos(nm)
        d = t - h
        s = max(-1.0, min(1.0, d.z / max(d.length, 1e-9)))
        series[key_].append(math.degrees(math.asin(s)))
    series["pelvis"].append(S("DEF-spine"))
    series["footL"].append(S("DEF-foot.L")); series["footR"].append(S("DEF-foot.R"))
    series["capetip"].append(bpos("DEF-cape.005")[1])
for k in ("elbowL", "elbowR", "kneeL", "kneeR", "ankleL", "ankleR", "finger"):
    v = series[k]
    M[k] = {"min": round(min(v), 1), "max": round(max(v), 1), "range": round(max(v) - min(v), 1)}
for k in ("armdirL", "armdirR"):
    v = series[k]
    M[k] = {"min_deg_from_horizontal": round(min(v), 1), "max_deg_from_horizontal": round(max(v), 1),
            "pct_frames_below_horizontal_15deg": round(100.0 * sum(1 for x in v if x < -15) / len(v), 1)}
M["spine_bend_quat_range_deg"] = round(qrange("DEF-spine.002", samples), 1)
M["chest_quat_range_deg"] = round(qrange("DEF-spine.003", samples), 1)
M["neck_quat_range_deg"] = round(qrange("DEF-spine.005", samples), 1)
M["head_quat_range_deg"] = round(qrange("DEF-spine.006", samples), 1)
M["wrist_quat_range_deg_L"] = round(qrange("DEF-hand.L", samples), 1)
M["wrist_quat_range_deg_R"] = round(qrange("DEF-hand.R", samples), 1)
pv = np.array([list(v) for v in series["pelvis"]])
M["pelvis_travel_m"] = {"x": round(float(pv[:, 0].max() - pv[:, 0].min()), 3),
                        "z_bounce": round(float(pv[:, 2].max() - pv[:, 2].min()), 3)}
for k in ("footL", "footR"):
    a = np.array([list(v) for v in series[k]])
    M[k + "_travel_m"] = {"x": round(float(a[:, 0].max() - a[:, 0].min()), 3),
                          "z_lift": round(float(a[:, 2].max() - a[:, 2].min()), 3)}
ct = np.array([list(v) for v in series["capetip"]])
M["cape_tip_travel_m"] = {ax: round(float(ct[:, i].max() - ct[:, i].min()), 3) for i, ax in enumerate("xyz")}
with open(os.path.join(WORK, "measurements.json"), "w") as fh:
    json.dump(M, fh, indent=1)
log("measurements:", json.dumps(M))
print("STAGE_B_DONE")
