"""BlenRig 6 headless fitting via EDIT-MODE rest-pose warp.
Loads .rig_tmp/cj_blenrig_raw.blend (default rest), repositions guide bones to
measured joints, and warps every other bone by its nearest guide's transform.
Result: the rig's REST POSE matches the character -- no pose baking, no
REPROP/NOREP issues. Saves .rig_tmp/cj_blenrig_fit.blend.
"""
import bpy, json, os
from mathutils import Matrix, Vector

TMP = os.path.expanduser('~/workspace/cj-rig-wt/.rig_tmp')
bpy.ops.wm.open_mainfile(filepath=os.path.join(TMP, 'cj_blenrig_raw.blend'))
J = json.load(open('/tmp/cj_joints.json'))

arm = bpy.data.objects['biped_blenrig']
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='EDIT')

def V(p):
    return Vector(p)

# ---------------- guide targets (same as pose-fit) ----------------
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

ebones = arm.data.edit_bones
# record guide rest positions + build warp transforms
guide_rest = {}
guide_xform = {}
for name, (H, Tl) in T.items():
    eb = ebones.get(name)
    if not eb:
        print('GUIDE MISSING:', name)
        continue
    h0, t0 = Vector(eb.head), Vector(eb.tail)
    guide_rest[name] = h0
    d0 = t0 - h0
    L0 = d0.length
    d = Tl - H
    L = d.length
    q = (d0 / L0).rotation_difference(d / L)
    # similarity transform: rest -> fitted
    M = Matrix.Translation(H) @ q.to_matrix().to_4x4()
    if abs(L / L0 - 1.0) > 1e-9:
        M = M @ Matrix.Scale(L / L0, 4)
    M = M @ Matrix.Translation(-h0)
    guide_xform[name] = M
    # set guide directly
    eb.head = H
    eb.tail = Tl

print('GUIDES SET:', len(guide_xform))

# warp every other bone by nearest guide (per-endpoint)
names = list(guide_rest.keys())
rests = [guide_rest[n] for n in names]
n_warped = 0
for eb in ebones:
    if eb.name in guide_xform:
        continue
    # nearest guide to head / tail
    h, t = Vector(eb.head), Vector(eb.tail)
    nh = min(names, key=lambda n: (guide_rest[n] - h).length)
    nt = min(names, key=lambda n: (guide_rest[n] - t).length)
    eb.head = guide_xform[nh] @ h
    eb.tail = guide_xform[nt] @ t
    n_warped += 1

print('WARPED:', n_warped)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(TMP, 'cj_blenrig_fit.blend'))
print('WARP DONE')
