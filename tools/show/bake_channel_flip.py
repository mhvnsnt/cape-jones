"""Ep1 Scene 2 — channel-flip clip (Cape, seated).
Base: CMU 13_05 (sit, hands against chin, fidget), source frames 600-1200 @120fps
  -> 151 frames @30fps, retargeted with the idle-pipeline math (see
  retarget_cmu_cape.py; pelvis location uses the corrected root-parent-space
  conversion). Seated plateau verified from BVH Hips Y (10.0-10.2 throughout
  the window; the f1350+ stand-up is excluded).
Overlay (procedural, documented — no mocap source exists for remote-pointing):
  - f10-25: right arm extends to point the remote at the TV (extrinsic Rz
    sweep computed from the rig's rest matrices, eased in; held through the
    flips; released f135-150).
  - Channel-change beats at f45, f85, f120: head yaw +-10deg (local-Y) +
    right-hand wag 6deg (local-X pitch) as thumb presses.
Output: anims/show/cape-jones/ep1_cape_channel_flip.glb (armature-only, idle convention).
"""
import bpy, sys, math, os
from mathutils import Quaternion, Vector
sys.path.insert(0, "/home/hatch/workspace/ep1-fight-anim")
OUT = "/home/hatch/workspace/ep1-fight-anim/clips/cape/ep1_cape_channel_flip.glb"
BVH = "/home/hatch/workspace/ep1-fight-anim/13_05.bvh"
SRC_F0, SRC_F1, STEP = 600, 1200, 4
BVH_SCALE = 0.056444; TARGET_H = 0.925
M = [
    ("Hips",        [("pelvis", 1.0)]),
    ("LowerBack",   [("spine_1", 0.5), ("spine_2", 0.5)]),
    ("Spine",       [("spine_3", 0.5), ("spine_4", 0.5)]),
    ("Spine1",      [("chest", 1.0)]),
    ("Neck",        [("neck_1", 1.0)]),
    ("Neck1",       [("neck_2", 1.0)]),
    ("Head",        [("head", 1.0)]),
    ("LeftShoulder",[("upperarm_L", 1.0)]),
    ("LeftArm",     [("forearm_L", 1.0)]),
    ("LeftForeArm", [("hand_L", 1.0)]),
    ("RightShoulder",[("upperarm_R", 1.0)]),
    ("RightArm",    [("forearm_R", 1.0)]),
    ("RightForeArm",[("hand_R", 1.0)]),
    ("LeftUpLeg",   [("thigh_L", 1.0)]),
    ("LeftLeg",     [("shin_L", 1.0)]),
    ("LeftFoot",    [("foot_L", 1.0)]),
    ("LeftToeBase", [("toe_L", 1.0)]),
    ("RightUpLeg",  [("thigh_R", 1.0)]),
    ("RightLeg",    [("shin_R", 1.0)]),
    ("RightFoot",   [("foot_R", 1.0)]),
    ("RightToeBase",[("toe_R", 1.0)]),
    ("LThumb",      [("finger_thumb_1_L", 1.0)]),
    ("LeftHandIndex1", [("finger_index_1_L", 0.6), ("finger_index_2_L", 0.4)]),
    ("RThumb",      [("finger_thumb_1_R", 1.0)]),
    ("RightHandIndex1",[("finger_index_1_R", 0.6), ("finger_index_2_R", 0.4)]),
]
bpy.context.scene.render.fps = 30
bpy.ops.import_scene.gltf(filepath="/home/hatch/workspace/scratch/cj-3d/cape-jones-show.glb")
rig = next(o for o in bpy.data.objects if o.type == 'ARMATURE' and o.name == 'CapeJones_Rig')
for b in rig.pose.bones: b.rotation_mode = 'QUATERNION'
for n in ("CapeJones_Body", "CapeJones_Cape"):
    o = bpy.data.objects.get(n)
    if o: o.hide_viewport = True; o.hide_render = True
bpy.ops.import_anim.bvh(filepath=BVH, global_scale=BVH_SCALE, frame_start=1)
src = next(o for o in bpy.data.objects if o.type == 'ARMATURE' and o != rig)
scn = bpy.context.scene
SRC_RESTW = {b.name: (src.matrix_world @ b.matrix_local).to_3x3().to_quaternion() for b in src.data.bones}
TGT_RESTW = {b.name: (rig.matrix_world @ b.matrix_local).to_3x3().to_quaternion() for b in rig.data.bones}
M_REL = {}
for b in rig.data.bones:
    M_REL[b.name] = b.matrix_local.to_3x3().to_quaternion() if b.parent is None else (b.parent.matrix_local.inverted() @ b.matrix_local).to_3x3().to_quaternion()
def fwd(arm, footL, footR, toeL, toeR):
    mw = arm.matrix_world
    fl = (mw @ arm.data.bones[footL].head_local); fr = (mw @ arm.data.bones[footR].head_local)
    tl = (mw @ arm.data.bones[toeL].head_local); tr = (mw @ arm.data.bones[toeR].head_local)
    v = ((tl + tr) / 2 - (fl + fr) / 2); v.z = 0; return v.normalized()
scn.frame_set(SRC_F0); bpy.context.view_layer.update()
sf = fwd(src, "LeftFoot", "RightFoot", "LeftToeBase", "RightToeBase")
tf = fwd(rig, "foot_L", "foot_R", "toe_L", "toe_R")
yaw = math.atan2(sf.cross(tf).z, sf.dot(tf)); YAW = Quaternion((0, 0, 1), yaw)
ankle = min((src.matrix_world @ b.head_local).z for b in src.data.bones if 'Foot' in b.name)
headb = src.data.bones['Head']
SRC_H = (src.matrix_world @ headb.head_local).z + headb.length - ankle
MOTION_SCALE = TARGET_H / SRC_H
PELVIS_HEAD_LOCAL = rig.data.bones['pelvis'].head_local.copy()
def scaled(q, w):
    return q if w == 1.0 else Quaternion(q.axis, q.angle * w)
act = bpy.data.actions.new("ep1_cape_channel_flip")
if not rig.animation_data: rig.animation_data_create()
rig.animation_data.action = act
n = (SRC_F1 - SRC_F0) // STEP + 1
print(f"baking {n} frames...")
for i in range(n):
    sf_ = SRC_F0 + i * STEP; df = i
    scn.frame_set(sf_); bpy.context.view_layer.update()
    Ws = {b.name: (src.matrix_world @ b.matrix).to_3x3().to_quaternion() for b in src.pose.bones}
    Wdes = {}
    for (sname, targets) in M:
        D = SRC_RESTW[sname].inverted() @ Ws[sname]
        for (tname, w) in targets: Wdes[tname] = YAW @ TGT_RESTW[tname] @ scaled(D, w)
    for (sname, targets) in M:
        for (tname, w) in targets:
            qpb = rig.pose.bones[tname]; par = qpb.parent
            Wpar = Quaternion() if par is None else (Wdes[par.name] if par.name in Wdes else TGT_RESTW[par.name])
            qpb.rotation_quaternion = (Wpar @ M_REL[tname]).inverted() @ Wdes[tname]
            qpb.keyframe_insert(data_path="rotation_quaternion", frame=df)
    hip_w = (src.matrix_world @ src.pose.bones['Hips'].head) * MOTION_SCALE
    hip_w = YAW @ hip_w
    O = hip_w - PELVIS_HEAD_LOCAL
    pb = rig.pose.bones['pelvis']
    pb.location = Vector((O.x, O.z, -O.y))
    pb.keyframe_insert(data_path="location", frame=df)
print("base bake done")
# ---- overlay: arm point + head turns + thumb wags (added on top of baked keys) ----
def ease(t):
    return t * t * (3 - 2 * t)
def set_pose_from_action(frame):
    scn.frame_set(frame); bpy.context.view_layer.update()
# Capture BAKED upperarm_R quats BEFORE inserting any overlay keys (overlay keys
# are dense in the ease window, so evaluating mid-loop would return overlay
# values, not baked ones -- that caused a pop at the reach start in v1).
baked_arm = {}
for f in list(range(10, 26)) + list(range(135, 151)):
    set_pose_from_action(f)
    baked_arm[f] = rig.pose.bones['upperarm_R'].rotation_quaternion.copy()
# arm point: extrinsic Rz sweep on upperarm_R. Right arm at rest points -X;
# Rz(+90) maps -X -> -Y (forward). point_loc = (parent_rest)^-1 @ (Rz90 @ rest).
rest_u = TGT_RESTW['upperarm_R']
par_w = TGT_RESTW['clavicle_R']
point_loc = (par_w @ M_REL['upperarm_R']).inverted() @ (Quaternion((0, 0, 1), math.radians(90)) @ rest_u)
for f in range(10, 26):
    t = ease((f - 10) / 15)
    loc = baked_arm[f].slerp(point_loc, t)
    rig.pose.bones['upperarm_R'].rotation_quaternion = loc
    rig.pose.bones['upperarm_R'].keyframe_insert(data_path="rotation_quaternion", frame=f)
rig.pose.bones['upperarm_R'].rotation_quaternion = point_loc
rig.pose.bones['upperarm_R'].keyframe_insert(data_path="rotation_quaternion", frame=135)
for f in range(136, 151):
    t = ease((f - 135) / 15)
    loc = baked_arm[f].slerp(point_loc, 1 - t)
    rig.pose.bones['upperarm_R'].rotation_quaternion = loc
    rig.pose.bones['upperarm_R'].keyframe_insert(data_path="rotation_quaternion", frame=f)
# head turns + thumb wags at beats 45, 85, 120 (dense baked keys isolate each beat)
for (beat, yawdeg) in ((45, -12), (85, 10), (120, -8)):
    for f in (beat - 4, beat, beat + 6):
        set_pose_from_action(f)
        for bn in ('neck_1', 'neck_2', 'head'):
            pb = rig.pose.bones[bn]
            w = 1.0 if f == beat else 0.0
            pb.rotation_quaternion = pb.rotation_quaternion @ Quaternion((0, 1, 0), math.radians(yawdeg * w))
            pb.keyframe_insert(data_path="rotation_quaternion", frame=f)
        pb = rig.pose.bones['hand_R']
        pb.rotation_quaternion = pb.rotation_quaternion @ Quaternion((1, 0, 0), math.radians(6 if f == beat else 0))
        pb.keyframe_insert(data_path="rotation_quaternion", frame=f)
print("overlay done")
# clean-scene rule (idle convention): exactly one action at export, or the
# exporter emits every action it finds (v1 leaked the BVH source action).
for o in list(bpy.data.objects):
    if o.type == 'ARMATURE' and o != rig:
        bpy.data.objects.remove(o, do_unlink=True)
for a in list(bpy.data.actions):
    if a != act:
        bpy.data.actions.remove(a)
scn.frame_start = 0; scn.frame_end = 150
bpy.ops.object.select_all(action='DESELECT')
rig.select_set(True); bpy.context.view_layer.objects.active = rig
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True,
    export_animations=True, export_frame_range=True, export_anim_single_armature=True,
    export_skins=True, export_morph=False, export_cameras=False, export_lights=False)
print("EXPORTED", OUT, os.path.getsize(OUT), "bytes")
