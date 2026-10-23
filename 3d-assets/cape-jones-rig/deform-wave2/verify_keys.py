"""Verify wave-2 corrective drivers evaluate correctly on the fixed blend.
For each key: pose joint at 0/50/100%, read evaluated shape-key value via depsgraph.
Expect ~0 at rest, monotonic rise, ~1 at full."""
import bpy, math, sys
from mathutils import Quaternion, Vector

fp = sys.argv[-1]
bpy.ops.wm.open_mainfile(filepath=fp)
rig = bpy.data.objects['CapeJones_Rig']
body = bpy.data.objects['CapeJones_Body']
sk = body.data.shape_keys

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

def key_value(name):
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    deps.update()
    eb = deps.objects.get('CapeJones_Body')
    return eb.data.shape_keys.key_blocks[name].value

KEYS = [
    ("corr_shoulderL", [("upperarm_fk_L", (0, 1, 0), -80)]),
    ("corr_shoulderR", [("upperarm_fk_R", (0, 1, 0), 80)]),
    ("corr_hipL", [("thigh_fk_L", (1, 0, 0), 90)]),
    ("corr_hipR", [("thigh_fk_R", (1, 0, 0), 90)]),
    ("corr_kneeL", [("shin_fk_L", (1, 0, 0), -120)]),
    ("corr_kneeR", [("shin_fk_R", (1, 0, 0), -120)]),
    ("corr_ankleL", [("foot_fk_L", (1, 0, 0), 30)]),
    ("corr_ankleR", [("foot_fk_R", (1, 0, 0), 30)]),
]
for name, spec in KEYS:
    vals = []
    for t in (0, 0.5, 1.0):
        reset_pose()
        for bname, axis, deg in spec:
            set_world_rot(bname, axis, deg * t)
        vals.append(key_value(name))
    ok = vals[0] < 0.05 and vals[2] > 0.9 and vals[0] <= vals[1] <= vals[2]
    print(f"{name}: 0%={vals[0]:.3f} 50%={vals[1]:.3f} 100%={vals[2]:.3f} {'OK' if ok else 'FAIL'}", flush=True)

# spine keys: pose via local euler on spine_1 (XYZ mode, matching driver space)
for name, axis_idx, deg in [("corr_spine_fwd", 0, 35), ("corr_spine_twist", 1, 35)]:
    vals = []
    for t in (0, 0.5, 1.0):
        reset_pose()
        pb = rig.pose.bones["spine_1"]
        pb.rotation_mode = 'XYZ'
        e = [0, 0, 0]
        e[axis_idx] = math.radians(deg * t)
        pb.rotation_euler = e
        vals.append(key_value(name))
    ok = vals[0] < 0.05 and vals[2] > 0.9 and vals[0] <= vals[1] <= vals[2]
    print(f"{name}: 0%={vals[0]:.3f} 50%={vals[1]:.3f} 100%={vals[2]:.3f} {'OK' if ok else 'FAIL'}", flush=True)
    # cross-check: other axis should NOT fire this key
    reset_pose()
    pb = rig.pose.bones["spine_1"]
    pb.rotation_mode = 'XYZ'
    e = [0, 0, 0]
    e[1 - axis_idx] = math.radians(deg)
    pb.rotation_euler = e
    cross = key_value(name)
    print(f"  cross-axis fire: {cross:.3f} (want <0.15)", flush=True)
