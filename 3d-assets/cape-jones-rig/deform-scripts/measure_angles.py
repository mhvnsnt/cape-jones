import bpy, math
from mathutils import Quaternion, Vector

rig = bpy.data.objects['CapeJones_Rig']

def reset_pose():
    for pb in rig.pose.bones:
        pb.rotation_mode = 'XYZ'
        pb.rotation_euler = (0, 0, 0)
        pb.location = (0, 0, 0)
        pb.scale = (1, 1, 1)

def set_world_rot(pb_name, axis, deg):
    pb = rig.pose.bones[pb_name]
    q_rest = pb.bone.matrix_local.to_quaternion()
    q_delta = Quaternion(Vector(axis), math.radians(deg))
    pb.rotation_mode = 'QUATERNION'
    pb.rotation_quaternion = q_rest.inverted() @ q_delta @ q_rest

def angle_between(b1, b2):
    # world orientation angle between two pose bones
    q1 = (rig.matrix_world @ rig.pose.bones[b1].matrix).to_quaternion()
    q2 = (rig.matrix_world @ rig.pose.bones[b2].matrix).to_quaternion()
    return q1.rotation_difference(q2).angle

tests = [
    ("jaw", "head", "jaw", [("jaw", (1,0,0), 32)]),
    ("jaw_half", "head", "jaw", [("jaw", (1,0,0), 15)]),
    ("neck_turn", "neck_2", "head", [("head", (0,0,1), 60)]),
    ("neck_tilt", "neck_2", "head", [("neck_2", (1,0,0), -18), ("head", (1,0,0), -12)]),
    ("elbow", "upperarm_L", "forearm_L", [("forearm_fk_L", (0,0,1), -130)]),
]
for name, b1, b2, spec in tests:
    reset_pose()
    bpy.context.view_layer.update()
    rest_a = angle_between(b1, b2)
    for pb_name, axis, deg in spec:
        set_world_rot(pb_name, axis, deg)
    bpy.context.view_layer.update()
    full_a = angle_between(b1, b2)
    print(f"{name}: rest={rest_a:.4f} full={full_a:.4f} delta={full_a-rest_a:+.4f}", flush=True)
