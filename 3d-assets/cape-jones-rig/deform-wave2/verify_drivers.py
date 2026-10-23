"""Sample ROTATION_DIFF driver variable at 0/25/50/75/100% of each wave-2 pose
to verify monotonicity before writing driver expressions."""
import bpy, math
from mathutils import Quaternion, Vector

rig = bpy.data.objects['CapeJones_Rig']

def reset_pose():
    for pb in rig.pose.bones:
        pb.rotation_mode = 'XYZ'
        pb.rotation_euler = (0, 0, 0)
        pb.location = (0, 0, 0)
        pb.scale = (1, 1, 1)
    root = rig.pose.bones['root']
    for prop in ['ik_arm_L', 'ik_arm_R', 'ik_leg_L', 'ik_leg_R']:
        if prop in root:
            root[prop] = 0.0

def set_world_rot(pb_name, axis, deg):
    pb = rig.pose.bones[pb_name]
    q_rest = pb.bone.matrix_local.to_quaternion()
    q_delta = Quaternion(Vector(axis), math.radians(deg))
    pb.rotation_mode = 'QUATERNION'
    pb.rotation_quaternion = q_rest.inverted() @ q_delta @ q_rest

def angle_between(b1, b2):
    q1 = rig.pose.bones[b1].matrix.to_quaternion()
    q2 = rig.pose.bones[b2].matrix.to_quaternion()
    return q1.rotation_difference(q2).angle

KEYS = [
    ("corr_shoulderL", "clavicle_L", "upperarm_L", ("upperarm_fk_L", (0, 1, 0), -80)),
    ("corr_shoulderR", "clavicle_R", "upperarm_R", ("upperarm_fk_R", (0, 1, 0), 80)),
    ("corr_hipL", "pelvis", "thigh_L", ("thigh_fk_L", (1, 0, 0), 90)),
    ("corr_hipR", "pelvis", "thigh_R", ("thigh_fk_R", (1, 0, 0), 90)),
    ("corr_kneeL", "thigh_L", "shin_L", ("shin_fk_L", (1, 0, 0), -120)),
    ("corr_kneeR", "thigh_R", "shin_R", ("shin_fk_R", (1, 0, 0), -120)),
    ("corr_ankleL", "shin_L", "foot_L", ("foot_fk_L", (1, 0, 0), 30)),
    ("corr_ankleR", "shin_R", "foot_R", ("foot_fk_R", (1, 0, 0), 30)),
    ("corr_spine_spine_fwd", "pelvis", "spine_1", ("spine_1", (1, 0, 0), 35)),
    ("corr_spine_spine_twist", "pelvis", "spine_1", ("spine_1", (0, 0, 1), 35)),
]
for name, b1, b2, (pb_name, axis, deg) in KEYS:
    vals = []
    for t in (0, 0.25, 0.5, 0.75, 1.0):
        reset_pose()
        set_world_rot(pb_name, axis, deg * t)
        bpy.context.view_layer.update()
        vals.append(angle_between(b1, b2))
    mono = all(vals[i] <= vals[i+1] + 1e-6 for i in range(4)) or \
           all(vals[i] >= vals[i+1] - 1e-6 for i in range(4))
    print(f"{name}: " + " ".join(f"{v:.4f}" for v in vals) + f" mono={mono}", flush=True)
