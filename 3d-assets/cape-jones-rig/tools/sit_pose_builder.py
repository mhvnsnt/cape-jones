"""Sitting pose library builder — Cape Jones.
Builds 5 FK sitting poses as Pose Asset actions in sitting_pose_library.blend,
with per-pose PNG proofs. Run: DISPLAY=:77 TMPDIR=<dir> blender -b --python this.py
"""
import bpy, math
from mathutils import Vector, Matrix, Quaternion

RIG_BLEND = "/home/hatch/workspace/cj-sitting-poses/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend"
CHAIR_BLEND = "/home/hatch/workspace/cj-sitting-poses/3d-assets/living_room.blend"
OUT_BLEND = "/home/hatch/workspace/cj-sitting-poses/3d-assets/cape-jones-rig/sitting_pose_library.blend"
OUT_PNG_DIR = "/home/hatch/workspace/cj-sitting-poses/3d-assets/cape-jones-rig/sitting-poses"

SEAT_TOP = 0.37
CHAIR_Y = 2.067
ANKLE_H = 0.064   # ankle height for a flat foot on the floor

bpy.ops.wm.open_mainfile(filepath=RIG_BLEND)
rig = bpy.data.objects['CapeJones_Rig']
body = bpy.data.objects['CapeJones_Body']
cape = bpy.data.objects.get('CapeJones_Cape')
cage = bpy.data.objects.get('BlenRigMdefCage')
idle = bpy.data.actions.get('idle_heroic_breathe')
if idle:
    idle.use_fake_user = True
if rig.animation_data is None:
    rig.animation_data_create()
rig.animation_data.action = None
if cape: cape.hide_render = True
if cage: cage.hide_render = True
for mod in body.modifiers:
    mod.show_viewport = False

bpy.context.view_layer.objects.active = rig
rig.select_set(True)

# chair (canon transform)
with bpy.data.libraries.load(CHAIR_BLEND) as (df, dt):
    dt.objects = ['loungeChairRelax(Clone)']
chair = dt.objects[0]
bpy.context.collection.objects.link(chair)
chair.location = (2.653, 2.312, 0.0)
chair.rotation_mode = 'XYZ'
chair.rotation_euler = (0, 0, math.radians(270.0))

# ---------------- posing core ----------------
def set_bone(name, M_desired):
    pb = rig.pose.bones[name]
    bone_rest = pb.bone.matrix_local
    if pb.parent:
        B = pb.parent.bone.matrix_local.inverted() @ bone_rest
        P = pb.parent.matrix
    else:
        B = bone_rest
        P = Matrix.Identity(4)
    S = B.inverted() @ P.inverted() @ M_desired
    pb.rotation_mode = 'QUATERNION'
    pb.rotation_quaternion = S.to_quaternion()
    pb.location = S.translation

def aim_bone(name, d1):
    pb = rig.pose.bones[name]
    bone_rest = pb.bone.matrix_local
    if pb.parent:
        B = pb.parent.bone.matrix_local.inverted() @ bone_rest
        P = pb.parent.matrix
    else:
        B = bone_rest
        P = Matrix.Identity(4)
    PB = P @ B
    Rp = PB.to_3x3()
    cur = (Rp @ Vector((0, 1, 0))).normalized()
    q = cur.rotation_difference(Vector(d1).normalized())
    j = PB.translation.copy()
    Rfinal = q.to_matrix() @ Rp
    set_bone(name, Matrix.Translation(j) @ Rfinal.to_4x4())

def keep_orientation(name):
    """Hold bone's current armature-space orientation (for feet/hands)."""
    pb = rig.pose.bones[name]
    B = pb.parent.bone.matrix_local.inverted() @ pb.bone.matrix_local
    cur = (((pb.parent.matrix @ B).to_3x3()) @ Vector((0, 1, 0))).normalized()
    aim_bone(name, cur)

def place_root(L, yaw_deg=-90.0):
    pb = rig.pose.bones['root']
    q = Quaternion((0, 0, 1), math.radians(yaw_deg))
    set_bone('root', Matrix.Translation(Vector(L)) @ q.to_matrix().to_4x4() @ pb.bone.matrix_local)

def reset_pose():
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    for pb in rig.pose.bones:
        pb.rotation_mode = 'QUATERNION'
        pb.rotation_quaternion = (1, 0, 0, 0)
        pb.location = (0, 0, 0)
        pb.scale = (1, 1, 1)
    bpy.context.view_layer.update()

def upd(): bpy.context.view_layer.update()
def phead(name): return rig.pose.bones[name].matrix.translation.copy()
def ptail(name):
    pb = rig.pose.bones[name]
    return (pb.matrix @ Vector((0, pb.bone.length, 0)))
def ankle(side): return (rig.matrix_world @ rig.pose.bones[f'foot_fk_{side}'].matrix).translation

def seat_and_ground(tx, tz_hip):
    """Place hips at (tx, CHAIR_Y, tz_hip), yaw -90; nudge so lowest ankle == ANKLE_H."""
    H = (phead('thigh_fk_L') + phead('thigh_fk_R')) * 0.5
    L = Vector((tx - H.y, CHAIR_Y + H.x, tz_hip - H.z))
    place_root(L); upd()
    az = min(ankle('L').z, ankle('R').z)
    L2 = L + Vector((0, 0, ANKLE_H - az))
    place_root(L2); upd()
    return L2

def report(tag):
    az = {s: round(ankle(s).z, 4) for s in ['L', 'R']}
    kl = tuple(round(v, 3) for v in (rig.matrix_world @ ptail('thigh_fk_L')))
    kr = tuple(round(v, 3) for v in (rig.matrix_world @ ptail('thigh_fk_R')))
    print(f"[{tag}] ankles {az} kneeL {kl} kneeR {kr}", flush=True)

def spine_base():
    aim_bone('pelvis', (0, -0.03, 1)); upd()

def legs_normal(spread=0.10, fwd=0.50, down=0.86):
    aim_bone('thigh_fk_L', ( spread, -fwd, -down)); upd()
    aim_bone('thigh_fk_R', (-spread, -fwd, -down)); upd()
    aim_bone('shin_fk_L', (0, 0, -1)); upd()
    aim_bone('shin_fk_R', (0, 0, -1)); upd()
    keep_orientation('foot_fk_L'); keep_orientation('foot_fk_R'); upd()

def arms_hang():
    for side, sgn in [('L', 1), ('R', -1)]:
        aim_bone(f'upperarm_fk_{side}', (sgn*0.12, -0.08, -0.99)); upd()
        aim_bone(f'forearm_fk_{side}', (sgn*0.05, -0.18, -0.98)); upd()
        keep_orientation(f'hand_fk_{side}')
    upd()

# ---------------- pose builders ----------------
def build_sit_normal():
    spine_base()
    aim_bone('spine_1', (0, -0.06, 1)); upd()
    aim_bone('spine_2', (0, -0.03, 1)); upd()
    aim_bone('chest', (0, 0.03, 1)); upd()
    aim_bone('neck_1', (0, -0.05, 1)); upd()
    aim_bone('neck_2', (0, -0.05, 1)); upd()
    aim_bone('head', (0, -0.14, 1)); upd()
    legs_normal()
    arms_hang()
    seat_and_ground(3.02, 0.42)

def build_sit_leg_folded():
    """Figure-4: right ankle rests on left knee. His casual reference pose."""
    spine_base()
    aim_bone('spine_1', (0, -0.06, 1)); upd()
    aim_bone('spine_2', (0, -0.03, 1)); upd()
    aim_bone('chest', (0, 0.05, 1)); upd()
    aim_bone('neck_1', (0, -0.08, 1)); upd()
    aim_bone('neck_2', (0, -0.08, 1)); upd()
    aim_bone('head', (0, -0.10, 1)); upd()
    # left leg normal (it becomes the footstool)
    aim_bone('thigh_fk_L', (0.10, -0.50, -0.86)); upd()
    aim_bone('shin_fk_L', (0, 0, -1)); upd()
    keep_orientation('foot_fk_L'); upd()
    # right thigh out-down-forward (opens the figure-4)
    aim_bone('thigh_fk_R', (-0.52, -0.38, -0.76)); upd()
    aim_bone('shin_fk_R', (-0.3, -0.3, -0.9)); upd()
    keep_orientation('foot_fk_R'); upd()
    # left arm hangs
    aim_bone('upperarm_fk_L', (0.12, -0.08, -0.99)); upd()
    aim_bone('forearm_fk_L', (0.05, -0.18, -0.98)); upd()
    keep_orientation('hand_fk_L'); upd()
    L = seat_and_ground(3.02, 0.42)
    # right ankle onto left knee: exact shin length from right knee
    knee_L = ptail('thigh_fk_L')
    ankle_target = knee_L + Vector((0, 0, 0.055))
    knee_R = ptail('thigh_fk_R')
    v = ankle_target - knee_R
    print(f"[fig4] kneeL {tuple(round(x,3) for x in knee_L)} kneeR {tuple(round(x,3) for x in knee_R)} tgt {tuple(round(x,3) for x in ankle_target)} d={round(v.length,3)}", flush=True)
    assert v.length <= 0.217 + 1e-6, f"fig4 shin unreachable: {v.length}"
    # place ankle exactly at shin length along v (no overshoot)
    ankle_a = knee_R + v.normalized() * 0.217
    aim_bone('shin_fk_R', (ankle_a - knee_R).normalized()); upd()
    keep_orientation('foot_fk_R'); upd()
    # right arm hangs naturally (knee too far for hand-on-knee)
    aim_bone('upperarm_fk_R', (-0.12, -0.08, -0.99)); upd()
    aim_bone('forearm_fk_R', (-0.05, -0.18, -0.98)); upd()
    keep_orientation('hand_fk_R'); upd()

def build_sit_lean_forward():
    spine_base()
    aim_bone('pelvis', (0, -0.10, 1)); upd()
    aim_bone('spine_1', (0, -0.25, 1)); upd()
    aim_bone('spine_2', (0, -0.25, 1)); upd()
    aim_bone('chest', (0, -0.15, 1)); upd()
    aim_bone('neck_1', (0, -0.55, 0.84)); upd()
    aim_bone('neck_2', (0, -0.65, 0.76)); upd()
    aim_bone('head', (0, -0.85, 0.53)); upd()
    legs_normal(spread=0.12, fwd=0.55, down=0.83)
    # arms: elbows on knees, hands clasped hanging between knees
    for side, sgn in [('L', 1), ('R', -1)]:
        shoulder = phead(f'upperarm_fk_{side}')
        knee = ptail(f'thigh_fk_{side}')
        elbow_t = knee + Vector((sgn*0.01, 0.03, 0.055))
        aim_bone(f'upperarm_fk_{side}', (elbow_t - shoulder).normalized()); upd()
        elbow = ptail(f'upperarm_fk_{side}')
        knee_mid = (ptail('thigh_fk_L') + ptail('thigh_fk_R')) * 0.5
        clasp = knee_mid + Vector((0, -0.02, -0.13))
        aim_bone(f'forearm_fk_{side}', (clasp - elbow).normalized()); upd()
        keep_orientation(f'hand_fk_{side}')
    upd()
    seat_and_ground(2.93, 0.42)

def build_sit_recline():
    spine_base()
    aim_bone('pelvis', (0, 0.05, 1)); upd()
    aim_bone('spine_1', (0, 0.12, 1)); upd()
    aim_bone('spine_2', (0, 0.12, 1)); upd()
    aim_bone('chest', (0, 0.10, 1)); upd()
    aim_bone('neck_1', (0, 0.10, 1)); upd()
    aim_bone('neck_2', (0, 0.08, 1)); upd()
    aim_bone('head', (0, 0.15, 1)); upd()
    # legs extended forward, feet flat
    aim_bone('thigh_fk_L', (0.08, -0.88, -0.47)); upd()
    aim_bone('thigh_fk_R', (-0.08, -0.88, -0.47)); upd()
    aim_bone('shin_fk_L', (0, -0.18, -0.98)); upd()
    aim_bone('shin_fk_R', (0, -0.18, -0.98)); upd()
    keep_orientation('foot_fk_L'); keep_orientation('foot_fk_R'); upd()
    # arms hang naturally (hands-behind-head impossible: arms 0.254m < head height above shoulders)
    for side, sgn in [('L', 1), ('R', -1)]:
        aim_bone(f'upperarm_fk_{side}', (sgn*0.15, -0.05, -0.98)); upd()
        aim_bone(f'forearm_fk_{side}', (sgn*0.08, -0.12, -0.99)); upd()
        keep_orientation(f'hand_fk_{side}')
    upd()
    seat_and_ground(2.98, 0.42)

def build_sit_arms_crossed():
    spine_base()
    aim_bone('spine_1', (0, 0.08, 1)); upd()
    aim_bone('spine_2', (0, 0.06, 1)); upd()
    aim_bone('chest', (0, 0.04, 1)); upd()
    aim_bone('neck_1', (0, -0.06, 1)); upd()
    aim_bone('neck_2', (0, -0.06, 1)); upd()
    aim_bone('head', (0, -0.18, 1)); upd()
    legs_normal()
    # elbows tucked in, hands meet in front of chest (arms-crossed read)
    aim_bone('upperarm_fk_L', (-0.30, -0.25, -0.92)); upd()
    aim_bone('forearm_fk_L', (-0.20, -0.30, 0.93)); upd()
    keep_orientation('hand_fk_L'); upd()
    aim_bone('upperarm_fk_R', (0.30, -0.25, -0.92)); upd()
    aim_bone('forearm_fk_R', (0.20, -0.30, 0.93)); upd()
    keep_orientation('hand_fk_R'); upd()
    seat_and_ground(3.02, 0.42)

POSES = [
    ("sit_normal", "Normal relaxed sit", build_sit_normal),
    ("sit_leg_folded", "Figure-4: right ankle on left knee (his reference)", build_sit_leg_folded),
    ("sit_lean_forward", "Lean-forward pensive/focused", build_sit_lean_forward),
    ("sit_recline", "Recline, legs extended (relaxed sprawl)", build_sit_recline),
    ("sit_arms_crossed", "Arms crossed, leaning back (comedic annoyed)", build_sit_arms_crossed),
]

# ---------------- lights / camera / render ----------------
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.mesh.primitive_plane_add(size=14, location=(2.0, 1.0, 0.0))
bpy.context.active_object.name = "ProofFloor"
bpy.ops.object.light_add(type='SUN', location=(0.5, 4.5, 3.0))
sun = bpy.context.active_object
sun.data.energy = 3.0
d = Vector((2.95, 2.05, 0.4)) - sun.location
sun.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
bpy.ops.object.light_add(type='AREA', location=(1.2, 3.6, 1.6))
area = bpy.context.active_object
area.data.energy = 60.0
area.data.size = 1.5
d = Vector((2.95, 2.05, 0.4)) - area.location
area.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
if bpy.context.scene.world is None:
    bpy.context.scene.world = bpy.data.worlds.new('ProofWorld')
bpy.context.scene.world.use_nodes = True
bg = bpy.context.scene.world.node_tree.nodes['Background']
bg.inputs['Color'].default_value = (0.35, 0.35, 0.38, 1.0)
bg.inputs['Strength'].default_value = 0.9

bpy.ops.object.camera_add(location=(0.85, 3.1, 0.95))
cam = bpy.context.active_object
cam.name = "ProofCam"
d = Vector((2.95, 2.05, 0.42)) - cam.location
cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = 24
sc.render.resolution_x, sc.render.resolution_y = 768, 432
sc.render.film_transparent = False
# memory: CorrectiveSmooth off + decimate proxy for proof renders
cs = body.modifiers.get('CorrectiveSmooth')
if cs: cs.show_viewport = False; cs.show_render = False
import os
os.makedirs(OUT_PNG_DIR, exist_ok=True)

bpy.context.view_layer.objects.active = rig
rig.select_set(True)
bpy.ops.object.mode_set(mode='POSE')

import os as _os
_pose_idx = int(_os.environ.get("POSE_IDX", "-1"))
_todo = [POSES[_pose_idx]] if 0 <= _pose_idx < len(POSES) else POSES
STAGE_DIR = "/home/hatch/workspace/cj-sitting-poses/3d-assets/cape-jones-rig/pose_stage"
_os.makedirs(STAGE_DIR, exist_ok=True)
for key, label, builder in _todo:
    print(f"===== POSE {key}: {label} =====", flush=True)
    reset_pose()
    builder()
    report(key)
    # bake into a pose-asset action
    act = bpy.data.actions.new(f"pose_{key}")
    act.use_fake_user = True
    rig.animation_data.action = act
    sc.frame_set(1)
    for pb in rig.pose.bones:
        pb.keyframe_insert(data_path="location")
        pb.keyframe_insert(data_path="rotation_quaternion")
        pb.keyframe_insert(data_path="scale")
    act.asset_mark()
    sc.render.filepath = os.path.join(OUT_PNG_DIR, f"{key}.png")
    bpy.ops.render.render(write_still=True)
    print(f"RENDERED {key}", flush=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(STAGE_DIR, f"pose_{key}.blend"))
    print(f"STAGE-SAVED {key}", flush=True)

rig.animation_data.action = None
print("POSE DONE", flush=True)
