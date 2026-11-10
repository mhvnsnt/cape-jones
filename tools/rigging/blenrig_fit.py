"""BlenRig 6 headless reproportion fitting for Cape Jones.
Loads .rig_tmp/cj_blenrig_raw.blend, positions guide bones from /tmp/cj_joints.json,
verifies deform bones, saves .rig_tmp/cj_blenrig_fit.blend.
"""
import bpy, json, os
from mathutils import Matrix, Vector

TMP = os.path.expanduser('~/workspace/cj-rig-wt/.rig_tmp')
bpy.ops.wm.open_mainfile(filepath=os.path.join(TMP, 'cj_blenrig_raw.blend'))
J = json.load(open('/tmp/cj_joints.json'))

arm = bpy.data.objects['biped_blenrig']
scn = bpy.context.scene
scn.view_layers[0].objects.active = arm
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')

# ---------------- STEP 0: scale rest pose to character height ----------------
# Default BlenRig biped ~1.70 m; Cape Jones is 0.9248 m. Scaling the rest pose
# first makes reproportion a fine-tune (what the guide was designed for) instead
# of a full retarget, keeping the constraint network coherent.
bpy.ops.object.mode_set(mode='EDIT')
for eb in arm.data.edit_bones:
    eb.head *= 0.544
    eb.tail *= 0.544
bpy.ops.object.mode_set(mode='POSE')
bpy.context.view_layer.update()
print('REST SCALED x0.544')

# reproportion on (BlenRig guide mechanism) -- set the property AND replicate
# reproportion_toggle's constraint muting (the update callback needs a screen)
def set_reproportion(arm_obj, on):
    arm_obj.data['reproportion'] = 1 if on else 0
    for pb in arm_obj.pose.bones:
        for C in pb.constraints:
            if 'REPROP' in C.name:
                C.mute = not on
            elif 'NOREP' in C.name:
                C.mute = on
    bpy.context.view_layer.update()

set_reproportion(arm, True)

def V(p):
    return Vector(p)

# ---------------- guide targets: name -> (head, tail) ----------------
T = {}
hip_z, waist_z, chest_z, neck_z = J['hip_z'], J['waist_z'], J['chest_z'], J['neck_z']
chin_z = J['chin_z']
T['master_torso_str'] = (V((0, 0, hip_z - 0.02)), V((0, 0, chest_z)))
T['pelvis_str'] = (V((0, 0, hip_z - 0.04)), V((0, 0, hip_z + 0.03)))
T['spine_ctrl_1_str'] = (V((0, 0, waist_z - 0.07)), V((0, 0, waist_z + 0.01)))
T['spine_ctrl_2_str'] = (V((0, 0, waist_z + 0.01)), V((0, 0, (waist_z + chest_z) / 2)))
T['spine_ctrl_3_str'] = (V((0, 0, (waist_z + chest_z) / 2)), V((0, 0, chest_z)))
T['spine_ctrl_4_str'] = (V((0, 0, chest_z - 0.02)), V((0, 0, chest_z + 0.05)))
T['neck_ctrl_2_str'] = (V((0, -0.01, neck_z - 0.03)), V((0, -0.015, neck_z + 0.005)))
T['neck_ctrl_3_str'] = (V((0, -0.015, neck_z + 0.005)), V((0, -0.02, neck_z + 0.035)))
T['neck_ctrl_4_str'] = (V((0, -0.02, neck_z + 0.035)), V((0, -0.02, chin_z)))
T['head_str'] = (V((0, -0.02, chin_z)), V(J['head_top']))
T['face_mstr_str'] = (V((0, J['face_y'] + 0.055, 0.862)), V((0, J['face_y'] + 0.005, 0.862)))

for side, s in (('L', 1), ('R', -1)):
    sh, el, wr = V(J[f'shoulder_{side}']), V(J[f'elbow_{side}']), V(J[f'wrist_{side}'])
    tip = V(J[f'fingertip_{side}'])
    hip, knee, ank, toe = V(J[f'hip_{side}']), V(J[f'knee_{side}']), V(J[f'ankle_{side}']), V(J[f'toe_{side}'])
    heel = V(J[f'heel_{side}'])
    T[f'clavi_str_{side}'] = (V((0, -0.01, neck_z)), sh)
    T[f'shoulder_str_{side}'] = (sh, el)
    T[f'elbow_str_{side}'] = (el, wr)
    T[f'wrist_str_{side}'] = (wr, tip)
    T[f'hand_str_{side}'] = (wr, tip)
    T[f'elbow_pole_str_{side}'] = (el + V((0, 0.24, -0.02)), el + V((0, 0.30, -0.02)))
    T[f'pelvis_str_{side}'] = (hip, knee)
    T[f'knee_str_{side}'] = (knee, ank)
    T[f'ankle_str_{side}'] = (ank, toe)
    T[f'foot_str_{side}'] = (ank, toe)
    T[f'toe_str_1_{side}'] = (toe, toe + V((0, -0.028, -0.004)))
    T[f'toe_str_2_{side}'] = (toe + V((0, -0.028, -0.004)), toe + V((0, -0.052, -0.006)))
    T[f'sole_str_{side}'] = (heel, toe)
    T[f'knee_pole_str_{side}'] = (knee + V((0, -0.24, 0.02)), knee + V((0, -0.30, 0.02)))
    # fingers: 4 x 5 segments + thumb x 4, along measured finger dir
    fdir = V(J[f'finger_dir_{side}'])
    palm = V(J[f'palm_{side}'])
    flen = max(0.035, J[f'finger_len_{side}'] * 2.2)
    perp = fdir.cross(V((0, 0, 1)))
    if perp.length < 1e-6:
        perp = V((1, 0, 0))
    perp.normalize()
    for fi, fn in enumerate(['ind', 'mid', 'ring', 'lit']):
        base = palm + fdir * 0.008 + perp * (-0.018 + fi * 0.012)
        seg = flen / 5
        for sg in range(1, 6):
            h = base + fdir * (sg - 1) * seg
            T[f'fing_{fn}_str_{sg}_{side}'] = (h, h + fdir * seg)
    th = V(J[f'thumb_{side}']) if J[f'thumb_{side}'] else palm + V((0, -0.02, -0.01))
    tdir = (fdir * 0.6 + V((0, -0.55, -0.45))).normalized()
    tlen = flen * 0.8
    seg = tlen / 4
    for sg in range(1, 5):
        h = th + tdir * (sg - 1) * seg
        T[f'fing_thumb_str_{sg}_{side}'] = (h, h + tdir * seg)

# ---------------- apply in parent-first order ----------------
data_bones = arm.data.bones
def depth(name):
    d, b = 0, data_bones.get(name)
    while b and b.parent:
        b = b.parent
        d += 1
    return d

desired = {}
missing = []
for name in sorted(T, key=depth):
    if name not in arm.pose.bones or name not in data_bones:
        missing.append(name)
        continue
    H, Tl = T[name]
    pb = arm.pose.bones[name]
    rb = data_bones[name]
    h0, t0 = Vector(rb.head_local), Vector(rb.tail_local)
    d0 = t0 - h0
    L0 = d0.length
    if L0 < 1e-9:
        continue
    u0 = d0 / L0
    d = Tl - H
    L = d.length
    u = d / L
    q = u0.rotation_difference(u)
    M = Matrix.Translation(H) @ q.to_matrix().to_4x4()
    if abs(L / L0 - 1.0) > 1e-6:
        M = M @ Matrix.Scale(L / L0, 4)
    # matrix_basis is the delta from rest: final = parent_final @ parent_rest^-1
    #   @ bone_rest @ matrix_basis  =>  mb = bone_rest^-1 @ parent_rest @ parent_final^-1 @ M
    bone_rest = rb.matrix_local
    par = pb.parent
    if par:
        parent_rest = par.bone.matrix_local
        Mp = desired[par.name] if par.name in desired else par.matrix
        mb = bone_rest.inverted() @ parent_rest @ Mp.inverted() @ M
    else:
        mb = bone_rest.inverted() @ M
    pb.rotation_mode = 'QUATERNION'
    pb.matrix_basis = mb
    desired[name] = M

bpy.context.view_layer.update()
print('GUIDES FIT:', len(desired), 'MISSING:', missing)

# ---------------- verify deform bones ----------------
def verify(tag):
    checks = {
        'thigh_def_L': J['hip_L'], 'thigh_def_R': J['hip_R'],
        'shin_def_L': J['knee_L'], 'shin_def_R': J['knee_R'],
        'foot_def_L': J['ankle_L'], 'foot_def_R': J['ankle_R'],
        'spine_1_def': [0, 0, waist_z], 'head_def_mstr': J['head_center'],
        'hand_def_L': J['wrist_L'], 'hand_def_R': J['wrist_R'],
        'forearm_def_L': J['elbow_L'],
    }
    print(f'--- deform check [{tag}] ---')
    for bn, jp in checks.items():
        pb = arm.pose.bones.get(bn)
        if not pb:
            print(bn, 'MISSING')
            continue
        err = (pb.head - Vector(jp)).length
        print(f'{bn}: err={err:.4f}m')

verify('reproportion-ON')

# ---------------- REST-BAKE: write ON-mode finals into EDIT-mode rest ----------------
# BlenRig's REPROP constraints only drive the rig while reproportion is ON, and
# the OFF-mode network cannot be reproduced by pose baking (constraint feedback).
# The robust headless equivalent of the artist's fitting: record every bone's
# ON-mode (fitted) head/tail, then rewrite the EDIT-mode rest pose from it.
# With rest == fitted, the OFF-mode (animation) constraint network operates on
# the correct base, and no pose transforms are needed.
ON_ht = {}
for pb in arm.pose.bones:
    ON_ht[pb.name] = (Vector(pb.head), Vector(pb.tail))
print('RECORDED', len(ON_ht), 'bones ON-mode')

bpy.ops.object.mode_set(mode='EDIT')
n_set, n_skip = 0, 0
for eb in arm.data.edit_bones:
    if eb.name not in ON_ht:
        n_skip += 1
        continue
    h, t = ON_ht[eb.name]
    if (t - h).length < 1e-9:
        n_skip += 1
        continue
    eb.head = h
    eb.tail = t
    n_set += 1
bpy.ops.object.mode_set(mode='POSE')
print('REST-SET', n_set, 'bones, skipped', n_skip)

# clear all pose transforms (rest is now the fitted pose)
from mathutils import Matrix as M4
for pb in arm.pose.bones:
    pb.matrix_basis = M4.Identity(4)

set_reproportion(arm, False)
bpy.context.view_layer.update()
print('REST-BAKED, reproportion OFF')

verify('reproportion-OFF-final (pose-baked)')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(TMP, 'cj_blenrig_fit.blend'))
print('FIT DONE')
