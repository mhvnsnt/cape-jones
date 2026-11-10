"""Verify warped rig deform bones (clean rest, OFF mode)."""
import bpy, json
from mathutils import Vector
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_fit.blend')
J = json.load(open('/tmp/cj_joints.json'))
arm = bpy.data.objects['biped_blenrig']
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
# ensure OFF + clean pose
arm.data['reproportion'] = 0
for pb in arm.pose.bones:
    for C in pb.constraints:
        if 'REPROP' in C.name:
            C.mute = True
        elif 'NOREP' in C.name:
            C.mute = False
bpy.context.view_layer.update()
checks = {
    'thigh_def_L': J['hip_L'], 'shin_def_L': J['knee_L'], 'foot_def_L': J['ankle_L'],
    'thigh_def_R': J['hip_R'], 'shin_def_R': J['knee_R'], 'foot_def_R': J['ankle_R'],
    'spine_1_def': [0, 0, J['waist_z']], 'head_def_mstr': J['head_center'],
    'hand_def_L': J['wrist_L'], 'hand_def_R': J['wrist_R'],
    'forearm_def_L': J['elbow_L'],
}
for bn, jp in checks.items():
    pb = arm.pose.bones.get(bn)
    err = (pb.head - Vector(jp)).length if pb else -1
    print(f'{bn}: err={err:.4f}m')
