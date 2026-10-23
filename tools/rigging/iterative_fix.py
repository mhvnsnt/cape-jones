"""Iterative EDIT-mode correction: measure pose error, adjust rest, repeat."""
import bpy, json
from mathutils import Vector
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_fit.blend')
J = json.load(open('/tmp/cj_joints.json'))
arm = bpy.data.objects['biped_blenrig']
bpy.context.view_layer.objects.active = arm

# key deform bones -> target joints (head, tail)
TARGETS = {
    'thigh_def_L': (J['hip_L'], J['knee_L']),
    'thigh_def_R': (J['hip_R'], J['knee_R']),
    'shin_def_L': (J['knee_L'], J['ankle_L']),
    'shin_def_R': (J['knee_R'], J['ankle_R']),
    'foot_def_L': (J['ankle_L'], J['toe_L']),
    'foot_def_R': (J['ankle_R'], J['toe_R']),
    'forearm_def_L': (J['elbow_L'], J['wrist_L']),
    'forearm_def_R': (J['elbow_R'], J['wrist_R']),
    'hand_def_L': (J['wrist_L'], J['fingertip_L']),
    'hand_def_R': (J['wrist_R'], J['fingertip_R']),
    'head_def_mstr': (J['neck_base'], J['head_top']),
    'spine_1_def': ([0, 0, J['waist_z'] - 0.07], [0, 0, J['waist_z'] + 0.01]),
}

for iteration in range(3):
    bpy.ops.object.mode_set(mode='POSE')
    # ensure OFF
    arm.data['reproportion'] = 0
    for pb in arm.pose.bones:
        for C in pb.constraints:
            if 'REPROP' in C.name:
                C.mute = True
            elif 'NOREP' in C.name:
                C.mute = False
    bpy.context.view_layer.update()
    # measure errors
    errors = {}
    max_err = 0
    for bn, (th, tt) in TARGETS.items():
        pb = arm.pose.bones.get(bn)
        if not pb:
            continue
        eh = Vector(th) - pb.head
        et = Vector(tt) - pb.tail
        errors[bn] = (eh, et)
        max_err = max(max_err, eh.length, et.length)
    print(f'ITER {iteration}: max_err={max_err:.4f}m')
    if max_err < 0.015:
        break
    # correct rest in EDIT mode (damped)
    bpy.ops.object.mode_set(mode='EDIT')
    for bn, (eh, et) in errors.items():
        eb = arm.data.edit_bones.get(bn)
        if not eb:
            continue
        eb.head = Vector(eb.head) + eh * 0.7
        eb.tail = Vector(eb.tail) + et * 0.7

bpy.ops.object.mode_set(mode='POSE')
bpy.context.view_layer.update()
print('--- final ---')
for bn, (th, tt) in TARGETS.items():
    pb = arm.pose.bones.get(bn)
    if pb:
        print(f'{bn}: head_err={(Vector(th)-pb.head).length:.4f} tail_err={(Vector(tt)-pb.tail).length:.4f}')

bpy.ops.wm.save_as_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_fit.blend')
print('ITERATIVE DONE')
