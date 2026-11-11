"""Cape Jones 3D dance v5 - STAGE B+C: retarget CMU 15_04 onto the new
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
BVH_PATH = "/home/hatch/workspace/_cj_v4_assets/bvh/15_04.bvh"
V3_SCENE = "/home/hatch/workspace/_cj-dance3d-v3/scene_v3.blend"
SRC_START, LOOP, STEP, XFADE = 12625, 96, 5, 12
ROOT_DAMP, TARGET_H = 0.6, 0.925
t00 = time.time()
def log(*a):
    print("[v5solve]", *a, round(time.time() - t00, 1), "s", flush=True)

sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
body = None
for ob in bpy.data.objects:
    if ob.type == "MESH" and len(ob.data.vertices) > 100000:
        body = ob
        break

# PERMANENT ARM FIX (owner pt98u 2026-11-10): route through the shared guarded loader before any arm work.
# The raw w5r arm chain (joints one segment out -> "H" arms) is repaired in memory; unknown chains are refused.
# Runs FIRST: the two-bone FK solve below aims bones at mocap joint positions using the TARGET's segment
# lengths — those lengths must come from the FIXED chain, not the one-segment-out defect.
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "guard-stance-v2-20261110", "tools"))
import cj_arm_guard
_cj_body = bpy.data.objects.get("CapeJones_Body") or body
if bpy.data.objects.get("CapeJones_Rig") is not None and _cj_body is not None:
    cj_arm_guard.ensure_arm_fix(body_name=_cj_body.name)

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
for _k in range(-XFADE, LOOP):
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

act = bpy.data.actions.new("DanceV5")
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
def key_rot(name, f):
    REC.setdefault(f, {})[name] = (Vector(RPB[name].location),
                                   Quaternion(RPB[name].rotation_quaternion))
def key_loc(name, f):
    REC.setdefault(f, {})[name] = (Vector(RPB[name].location),
                                   Quaternion(RPB[name].rotation_quaternion))
def reset_all_bones():
    for b in RPB:
        b.rotation_quaternion = (1, 0, 0, 0)
        b.rotation_euler = (0, 0, 0)
        b.location = (0, 0, 0)
        b.scale = (1, 1, 1)
    upd()

POSED = set()
REST_MAP = map_pos(SRC_REST["Hips"][0])
log("mapped rest hips:", [round(x, 3) for x in REST_MAP])
for k in range(LOOP):
    f = k + 1
    sc.frame_set(f)
    reset_all_bones()
    # root travel: mapped hips position relative to mapped rest hips, so
    # at a rest-equivalent frame the rig stands exactly at its rest spot
    hp, _ = desired("Hips", k)
    root_pb.location = hp - REST_MAP
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
        solve_two_bone(f"thigh_fk_{side}", f"shin_fk_{side}",
                       f"{S}UpLeg", f"{S}Leg", f"{S}Foot", k)
        key_rot(f"thigh_fk_{side}", f); key_rot(f"shin_fk_{side}", f)
        POSED.add(f"thigh_fk_{side}"); POSED.add(f"shin_fk_{side}")
        # foot orientation from ToeBase direction: aim foot at toe target
        tp, _ = desired(f"{S}ToeBase", k)
        fp, _ = desired(f"{S}Foot", k)
        ankle = head_of(f"foot_fk_{side}")
        toe_dir_target = ankle + (tp - fp)
        aim(f"foot_fk_{side}", toe_dir_target)
        key_rot(f"foot_fk_{side}", f); POSED.add(f"foot_fk_{side}")
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
log("solve done", round(time.time() - t00, 1), "s")

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
# NLA tile x19 -> 1824 frames
ad = rig.animation_data
track = ad.nla_tracks.new()
track.name = "DanceV5x19"
strip = track.strips.new("DanceV5", 1, act)
strip.repeat = 19
strip.use_animated_influence = False
ad.action = None
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
print("SOLVE_V5_DONE", OUT)
