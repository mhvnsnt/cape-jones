"""Fix the broken idle/breathe action in a Cape Jones rig file (COPY).
Two historical failure modes, both audit-verified:
- sitting_pose_library.blend: ALL pose bones are rotation_mode=
  QUATERNION but idle_heroic_breathe keys rotation_euler -> the action
  is 100% INERT; layered anywhere it shows the rig's H-pose rest
  (upper arms ~80 deg).
- cape_jones_rigged_w5r_idle.blend: bones are rotation_mode='XYZ' so
  the euler keys ARE live, but the author's mirrored arm signs
  (upperarm_fk X: L -1.25 / R +1.25) land the RIGHT arm flipped up
  (152 deg) on the current rig - the keys predate a rig revision.
Fix, mode-aware per bone:
- Arms (both files): rebuild the hang procedurally on THIS rig with
  the dance solver's aim machinery - upper arm to a 4-degree hang,
  forearm with the author's 0.12 rad elbow bend toward facing - and
  key it in each bone's NATIVE channel (quat or euler), frame 1 only,
  exactly as authored.
- Spine/head breathing keys: if the bone is QUATERNION mode, convert
  its euler keys to quaternion (exact for these small non-mirrored
  pitch tilts) and drop the dead euler curves; if XYZ mode, the keys
  are already live - leave them untouched.
NOTHING else is touched: every other action must verify identical.
Args: <in.blend> <out.blend>
"""
import bpy, math, sys
from mathutils import Vector, Euler, Matrix, Quaternion

argv = sys.argv[sys.argv.index("--") + 1:]
INP, OUTP = argv[0], argv[1]
sc = bpy.context.scene
# PERMANENT ARM FIX (owner pt98u 2026-11-10): route through the shared guarded loader before any arm work.
# Raw w5r arm chain (joints one segment out -> "H" arms) is repaired in memory; unknown chains are refused.
import os as _os
sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "guard-stance-v2-20261110", "tools"))
import cj_arm_guard
cj_arm_guard.ensure_arm_fix()
rig = bpy.data.objects["CapeJones_Rig"]
RPB = rig.pose.bones
DOWN = Vector((0, 0, -1))

def get_all_fcurves(action):
    fcs, seen = [], set()
    def add_from_channelbag(cb):
        if cb is None: return
        try:
            for fc in cb.fcurves:
                try: key = fc.as_pointer()
                except Exception: key = (fc.data_path, fc.array_index)
                if key not in seen:
                    seen.add(key); fcs.append(fc)
        except Exception:
            pass
    try:
        legacy = list(action.fcurves)
        if legacy: return legacy
    except Exception:
        pass
    try: slots = list(action.slots) if hasattr(action, "slots") else []
    except Exception: slots = []
    try:
        for layer in action.layers:
            for strip in layer.strips:
                try:
                    for cb in strip.channelbags: add_from_channelbag(cb)
                except Exception: pass
                cb_attr = getattr(strip, "channelbag", None)
                if cb_attr is None: continue
                if callable(cb_attr):
                    for s in (slots if slots else [None]):
                        try: cb = cb_attr(s) if s is not None else cb_attr()
                        except Exception: continue
                        add_from_channelbag(cb)
                else:
                    add_from_channelbag(cb_attr)
    except Exception:
        pass
    return fcs

def channelbag_of(action):
    try: slots = list(action.slots) if hasattr(action, "slots") else []
    except Exception: slots = []
    for layer in action.layers:
        for strip in layer.strips:
            cb_attr = getattr(strip, "channelbag", None)
            if cb_attr is None: continue
            if callable(cb_attr):
                for s in (slots if slots else [None]):
                    try:
                        cb = cb_attr(s) if s is not None else cb_attr()
                    except Exception: continue
                    if cb is not None: return cb
            else:
                return cb_attr
    return None

def ang(name, rig_=None, RPB_=None):
    RPB_ = RPB_ or RPB; rig_ = rig_ or rig
    pb = RPB_[name]
    m = rig_.matrix_world @ pb.matrix
    h = m.to_translation(); t = m @ Vector((0, pb.length, 0))
    return round(math.degrees((t - h).normalized().angle(DOWN)), 1)

def snapshot_actions():
    snap = {}
    for act in bpy.data.actions:
        curves = []
        for fc in get_all_fcurves(act):
            pts = tuple((round(kp.co[0], 3), round(kp.co[1], 6)) for kp in fc.keyframe_points)
            curves.append((fc.data_path, fc.array_index, pts))
        snap[act.name] = sorted(curves)
    return snap

before = snapshot_actions()
print("actions in file:", sorted(before.keys()))
idle_name = next((n for n in before if "breathe" in n or "idle" in n), None)
print("idle action:", idle_name)
act = bpy.data.actions[idle_name]
rig.animation_data_create()
rig.animation_data.action = act
for f in (1, 24, 48):
    sc.frame_set(f); bpy.context.view_layer.update()
    print(f"BEFORE f{f}: armL {ang('upperarm_L')} armR {ang('upperarm_R')}")

# collect euler keys of the idle action
euler_data = {}
for fc in get_all_fcurves(act):
    if ".rotation_euler" in fc.data_path:
        bone = fc.data_path.split('"')[1]
        euler_data.setdefault(bone, {})[fc.array_index] = \
            [(kp.co[0], kp.co[1]) for kp in fc.keyframe_points]
print("euler-keyed bones:", {b: sorted(v.keys()) for b, v in euler_data.items()})
modes = {pb.name: pb.rotation_mode for pb in RPB}
print("modes: spine_1", modes.get("spine_1"), "| upperarm_fk_L", modes.get("upperarm_fk_L"))

# ---- spine/head: convert ONLY where the bone is quaternion-mode
converted_bones = []
for bone in ("spine_1", "spine_2", "chest", "head"):
    if bone not in euler_data: continue
    if modes.get(bone) != "QUATERNION":
        print(f"{bone}: mode {modes.get(bone)} - euler keys already live, leaving")
        continue
    axes = euler_data[bone]
    frames = sorted({fr for pts in axes.values() for fr, _ in pts})
    def val(axis, fr, axes=axes):
        pts = axes.get(axis)
        if not pts: return 0.0
        for f0, v0 in pts:
            if abs(f0 - fr) < 0.01: return v0
        return pts[-1][1]
    pb = RPB[bone]
    for fr in frames:
        pb.rotation_quaternion = Euler((val(0, fr), val(1, fr), val(2, fr)), 'XYZ').to_quaternion()
        pb.keyframe_insert("rotation_quaternion", frame=int(round(fr)))
    converted_bones.append(bone)
    print(f"{bone}: converted {len(frames)} keys euler->quat")

# ---- arms: procedural hang on this rig, keyed in the native channel
def upd(): bpy.context.view_layer.update()
def rot_about_head(name, q_world):
    pb = RPB[name]
    M = pb.matrix.copy(); h = M.to_translation()
    R = q_world.to_matrix().to_4x4()
    pb.matrix = Matrix.Translation(h) @ R @ Matrix.Translation(-h) @ M
    upd()
def aim_bone(name, target_pos):
    pb = RPB[name]
    h = Vector(pb.head)
    cur = Vector(pb.tail) - h
    tgt = Vector(target_pos) - h
    if cur.length < 1e-6 or tgt.length < 1e-6: return
    rot_about_head(name, cur.normalized().rotation_difference(tgt.normalized()))
rig.animation_data.action = None
for pb in RPB:
    pb.rotation_quaternion = (1, 0, 0, 0); pb.rotation_euler = (0, 0, 0)
    pb.location = (0, 0, 0); pb.scale = (1, 1, 1)
upd()
_fa = (rig.matrix_world @ RPB["toe_L"].matrix).to_translation()
_fb = (rig.matrix_world @ RPB["foot_L"].matrix).to_translation()
FACING = Vector((_fa.x - _fb.x, _fa.y - _fb.y, 0))
FACING.normalize() if FACING.length > 1e-6 else Vector((0, -1, 0))
print("facing (xy):", [round(x, 2) for x in FACING])
_arm_keys = {}
for side, sgn in (("L", 1.0), ("R", -1.0)):
    up = f"upperarm_fk_{side}"; fo = f"forearm_fk_{side}"
    h = Vector(RPB[up].head); L1 = RPB[up].length
    hang = Vector((sgn * math.tan(math.radians(4.0)), 0, -1)).normalized()
    aim_bone(up, h + hang * L1)
    e = Vector(RPB[fo].head); L2 = RPB[fo].length
    bend = Quaternion(FACING.cross(hang).normalized(), 0.12) if FACING.cross(hang).length > 1e-6 \
        else Quaternion((1, 0, 0, 0))
    wdir = bend @ hang
    aim_bone(fo, e + wdir * L2)
    for bn in (up, fo):
        # capture via matrix_basis: mode-independent. (On euler-mode
        # bones rotation_quaternion reads back IDENTITY even when the
        # bone is posed - the w5r file proved it.)
        _arm_keys[bn] = RPB[bn].matrix_basis.to_quaternion()
    print(f"arm {side} aimed: upper {ang(f'upperarm_{side}')} forearm {ang(f'forearm_{side}')}")
rig.animation_data.action = act
for bn, q in _arm_keys.items():
    if modes.get(bn) == "QUATERNION":
        RPB[bn].rotation_quaternion = q
        RPB[bn].keyframe_insert("rotation_quaternion", frame=1)
    else:
        RPB[bn].rotation_euler = q.to_euler('XYZ')
        RPB[bn].keyframe_insert("rotation_euler", frame=1)
    converted_bones.append(bn)
print("arm keys written (native channels):", sorted(_arm_keys.keys()))

# ---- remove euler fcurves ONLY for bones converted to quaternion
cb = channelbag_of(act)
removed = 0
if cb is not None:
    for fc in get_all_fcurves(act):
        if ".rotation_euler" in fc.data_path and fc.data_path.split('"')[1] in converted_bones \
                and modes.get(fc.data_path.split('"')[1]) == "QUATERNION":
            try:
                cb.fcurves.remove(fc); removed += 1
            except Exception as e:
                print("euler remove failed:", e); break
print("dead euler fcurves removed:", removed)

# ---- measure AFTER
res = {}
for f in (1, 12, 24, 36, 48):
    sc.frame_set(f); bpy.context.view_layer.update()
    res[f] = (ang('upperarm_L'), ang('upperarm_R'), ang('chest'))
    print(f"AFTER f{f}: armL {res[f][0]} armR {res[f][1]} chest {res[f][2]}")
max_arm = max(max(v[0], v[1]) for v in res.values())
chest_var = max(v[2] for v in res.values()) - min(v[2] for v in res.values())
print("max arm angle after:", max_arm, "chest variation (breathing):", round(chest_var, 2))
if max_arm > 25:
    print("ABORT: converted idle still raises the arms - not saving")
    sys.exit(1)

bpy.ops.wm.save_as_mainfile(filepath=OUTP)
print("saved", OUTP)

# ---- verify: reopen, compare all OTHER actions value-for-value
bpy.ops.wm.open_mainfile(filepath=OUTP)
sc = bpy.context.scene
after = snapshot_actions()
bad = [n for n, c in before.items() if n != idle_name and after.get(n) != c]
print("non-idle actions changed:", bad if bad else "NONE - all identical")
rig2 = bpy.data.objects["CapeJones_Rig"]
RPB2 = rig2.pose.bones
for name in sorted(after.keys()):
    if name.startswith("pose_"):
        rig2.animation_data.action = bpy.data.actions[name]
        sc.frame_set(1); bpy.context.view_layer.update()
        print(f"pose {name}: armL {ang('upperarm_L', rig2, RPB2)} armR {ang('upperarm_R', rig2, RPB2)}")
print("FIX_BREATHE_DONE")
