"""Cape Jones custom deform rig + BlenRig MDEF cage + procedural weights.
Loads .rig_tmp/cj_blenrig_raw.blend. Builds a clean FK/IK deform armature at the
measured joints, fits BlenRig's MDEF cage, paints procedural zone weights on the
cage, binds cage->armature, character->cage (mesh deform). Saves final blend.
"""
import bpy, json, os
import numpy as np
from mathutils import Matrix, Vector

TMP = os.path.expanduser('~/workspace/cj-rig-wt/.rig_tmp')
OUT = os.path.expanduser('~/workspace/cj-rig-wt/3d-assets/cape-jones-rig/cape_jones_rigged.blend')
bpy.ops.wm.open_mainfile(filepath=os.path.join(TMP, 'cj_blenrig_raw.blend'))
J = json.load(open('/tmp/cj_joints.json'))

scn = bpy.context.scene
char = bpy.data.objects['CapeJones_Body']
cage = bpy.data.objects['BlenRigMdefCage']
rig_obj = bpy.data.objects['biped_blenrig']
print('CHAR', len(char.data.vertices), 'CAGE', len(cage.data.vertices))

def V(p):
    return Vector(p)

# ============ 1. DEFORM ARMATURE ============
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')
arm_data = bpy.data.armatures.new('CapeJones_Rig')
arm = bpy.data.objects.new('CapeJones_Rig', arm_data)
scn.collection.objects.link(arm)
bpy.context.view_layer.update()
arm.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.context.view_layer.update()
bpy.ops.object.mode_set(mode='EDIT')
eb = arm_data.edit_bones
print('EDIT MODE OK, edit_bones accessible:', len(eb) >= 0)

def bone(name, h, t, parent=None, deform=True, roll=0):
    b = eb.new(name)
    b.head = V(h); b.tail = V(t)
    b.use_deform = deform
    if parent:
        b.parent = eb[parent]
    return b

hip_z, waist_z, chest_z, neck_z = J['hip_z'], J['waist_z'], J['chest_z'], J['neck_z']
chin_z = J['chin_z']

# root + spine
bone('root', (0, 0, 0), (0, 0, 0.05), deform=False)
bone('pelvis', (0, 0, hip_z - 0.03), (0, 0, hip_z + 0.03), 'root')
bone('spine_1', (0, 0, waist_z - 0.07), (0, 0, waist_z + 0.01), 'pelvis')
bone('spine_2', (0, 0, waist_z + 0.01), (0, 0, chest_z - 0.05), 'spine_1')
bone('chest', (0, 0, chest_z - 0.05), (0, 0, chest_z + 0.04), 'spine_2')
bone('neck_1', (0, -0.01, neck_z - 0.02), (0, -0.015, neck_z + 0.03), 'chest')
bone('neck_2', (0, -0.015, neck_z + 0.03), (0, -0.02, chin_z), 'neck_1')
bone('head', (0, -0.02, chin_z), V(J['head_top']), 'neck_2')
# jaw (for dialogue)
bone('jaw', (0, J['face_y'] + 0.04, 0.845), (0, J['face_y'] + 0.01, 0.825), 'head', deform=True)

for side, s in (('L', 1), ('R', -1)):
    sh, el, wr = J[f'shoulder_{side}'], J[f'elbow_{side}'], J[f'wrist_{side}']
    tip = J[f'fingertip_{side}']
    hip, knee, ank, toe = J[f'hip_{side}'], J[f'knee_{side}'], J[f'ankle_{side}'], J[f'toe_{side}']
    # arm FK chain
    bone(f'clavicle_{side}', (0, -0.01, neck_z), sh, 'chest')
    bone(f'upperarm_fk_{side}', sh, el, f'clavicle_{side}')
    bone(f'forearm_fk_{side}', el, wr, f'upperarm_fk_{side}')
    bone(f'hand_fk_{side}', wr, tip, f'forearm_fk_{side}')
    # arm IK chain
    bone(f'upperarm_ik_{side}', sh, el, f'clavicle_{side}')
    bone(f'forearm_ik_{side}', el, wr, f'upperarm_ik_{side}')
    bone(f'hand_ik_{side}', wr, tip, f'forearm_ik_{side}', deform=False)
    bone(f'elbow_pole_{side}', (el[0], el[1] + 0.25 * s * 0 + 0.25, el[2]),
         (el[0], el[1] + 0.30, el[2]), 'root', deform=False)
    # deform arm (driven by FK/IK via switch; default FK)
    bone(f'upperarm_{side}', sh, el, f'clavicle_{side}')
    bone(f'forearm_{side}', el, wr, f'upperarm_{side}')
    bone(f'hand_{side}', wr, tip, f'forearm_{side}')
    # fingers (3 segments x4 + thumb x2)
    fdir = V(J[f'finger_dir_{side}'])
    palm = V(J[f'palm_{side}'])
    flen = max(0.030, J[f'finger_len_{side}'] * 2.0)
    perp = fdir.cross(V((0, 0, 1)))
    perp = V((1, 0, 0)) if perp.length < 1e-6 else perp.normalized()
    for fi, fn in enumerate(['index', 'middle', 'ring', 'pinky']):
        base = palm + fdir * 0.006 + perp * (-0.015 + fi * 0.010)
        seg = flen / 3
        prev = f'hand_{side}'
        for sg in range(1, 4):
            h = base + fdir * (sg - 1) * seg
            nm = f'finger_{fn}_{sg}_{side}'
            bone(nm, h, h + fdir * seg, prev)
            prev = nm
    th = V(J[f'thumb_{side}']) if J[f'thumb_{side}'] else palm + V((0, -0.02, -0.01))
    tdir = (fdir * 0.6 + V((0, -0.55, -0.45))).normalized()
    tseg = flen * 0.35
    prev = f'hand_{side}'
    for sg in range(1, 3):
        h = th + tdir * (sg - 1) * tseg
        nm = f'finger_thumb_{sg}_{side}'
        bone(nm, h, h + tdir * tseg, prev)
        prev = nm
    # leg FK + IK
    bone(f'thigh_fk_{side}', hip, knee, 'pelvis')
    bone(f'shin_fk_{side}', knee, ank, f'thigh_fk_{side}')
    bone(f'foot_fk_{side}', ank, toe, f'shin_fk_{side}')
    bone(f'thigh_ik_{side}', hip, knee, 'pelvis')
    bone(f'shin_ik_{side}', knee, ank, f'thigh_ik_{side}')
    bone(f'foot_ik_{side}', ank, toe, 'root', deform=False)
    bone(f'toe_ik_{side}', toe, (toe[0], toe[1] - 0.05, toe[2] - 0.005), f'foot_ik_{side}', deform=False)
    bone(f'knee_pole_{side}', (knee[0], knee[1] - 0.25, knee[2]),
         (knee[0], knee[1] - 0.30, knee[2]), 'root', deform=False)
    # deform leg
    bone(f'thigh_{side}', hip, knee, 'pelvis')
    bone(f'shin_{side}', knee, ank, f'thigh_{side}')
    bone(f'foot_{side}', ank, toe, f'shin_{side}')
    bone(f'toe_{side}', toe, (toe[0], toe[1] - 0.05, toe[2] - 0.005), f'foot_{side}')
    # wrist blaster attachment (Mega Man / Android 16 style power-band blasters)
    bone(f'blaster_{side}', (wr[0], wr[1] - 0.01, wr[2] + 0.035),
         (wr[0], wr[1] - 0.01, wr[2] - 0.035), f'hand_{side}', deform=False)

print('EDIT bones:', len(arm_data.edit_bones))
bpy.ops.object.mode_set(mode='OBJECT')
print('ARMATURE BONES:', len(arm_data.bones))

# ============ 2. FK/IK SWITCHES (pose mode, constraints + drivers) ============
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')
# properties on root
root_pb = arm.pose.bones['root']
root_pb['ik_arm_L'] = 0.0; root_pb['ik_arm_R'] = 0.0
root_pb['ik_leg_L'] = 0.0; root_pb['ik_leg_R'] = 0.0
for prop in ['ik_arm_L', 'ik_arm_R', 'ik_leg_L', 'ik_leg_R']:
    ui = root_pb.id_properties_ui(prop)
    ui.update(min=0.0, max=1.0, description='IK/FK switch (0=FK, 1=IK)')

def add_driver(pb, cname, prop):
    c = pb.constraints[cname]
    d = c.driver_add('influence').driver
    d.type = 'SCRIPTED'
    d.expression = 'sw'
    var = d.variables.new()
    var.name = 'sw'
    var.type = 'SINGLE_PROP'
    tgt = var.targets[0]
    tgt.id = arm
    tgt.data_path = f'pose.bones["root"]["{prop}"]'
    return d

for side in ('L', 'R'):
    # arm deform: FK vs IK
    for seg, fk, ik in (('upperarm', f'upperarm_fk_{side}', f'upperarm_ik_{side}'),
                        ('forearm', f'forearm_fk_{side}', f'forearm_ik_{side}'),
                        ('hand', f'hand_fk_{side}', f'hand_ik_{side}')):
        db = arm.pose.bones[f'{seg}_{side}']
        c1 = db.constraints.new('COPY_TRANSFORMS'); c1.name = 'FK'; c1.target = arm; c1.subtarget = fk
        c2 = db.constraints.new('COPY_TRANSFORMS'); c2.name = 'IK'; c2.target = arm; c2.subtarget = ik
        c1.influence = 1.0; c2.influence = 0.0
        add_driver(db, 'IK', f'ik_arm_{side}')
        # FK influence = 1 - IK: use driver with expression
        d = db.constraints['FK'].driver_add('influence').driver
        d.type = 'SCRIPTED'; d.expression = '1 - sw'
        var = d.variables.new(); var.name = 'sw'; var.type = 'SINGLE_PROP'
        tgt = var.targets[0]; tgt.id = arm
        tgt.data_path = f'pose.bones["root"]["ik_arm_{side}"]'
    # arm IK: forearm tracks hand_ik, pole target
    fib = arm.pose.bones[f'forearm_ik_{side}']
    ikc = fib.constraints.new('IK'); ikc.target = arm; ikc.subtarget = f'hand_ik_{side}'
    ikc.pole_target = arm; ikc.pole_subtarget = f'elbow_pole_{side}'
    ikc.chain_count = 2; ikc.pole_angle = 0.0
    # leg deform: FK vs IK
    for seg, fk, ik in (('thigh', f'thigh_fk_{side}', f'thigh_ik_{side}'),
                        ('shin', f'shin_fk_{side}', f'shin_ik_{side}'),
                        ('foot', f'foot_fk_{side}', f'foot_ik_{side}')):
        db = arm.pose.bones[f'{seg}_{side}']
        c1 = db.constraints.new('COPY_TRANSFORMS'); c1.name = 'FK'; c1.target = arm; c1.subtarget = fk
        c2 = db.constraints.new('COPY_TRANSFORMS'); c2.name = 'IK'; c2.target = arm; c2.subtarget = ik
        c1.influence = 1.0; c2.influence = 0.0
        add_driver(db, 'IK', f'ik_leg_{side}')
        d = db.constraints['FK'].driver_add('influence').driver
        d.type = 'SCRIPTED'; d.expression = '1 - sw'
        var = d.variables.new(); var.name = 'sw'; var.type = 'SINGLE_PROP'
        tgt = var.targets[0]; tgt.id = arm
        tgt.data_path = f'pose.bones["root"]["ik_leg_{side}"]'
    shb = arm.pose.bones[f'shin_ik_{side}']
    ikc = shb.constraints.new('IK'); ikc.target = arm; ikc.subtarget = f'foot_ik_{side}'
    ikc.pole_target = arm; ikc.pole_subtarget = f'knee_pole_{side}'
    ikc.chain_count = 2; ikc.pole_angle = 0.0

bpy.context.view_layer.update()
print('FK/IK SWITCHES DONE')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(TMP, 'cj_custom_rig.blend'))
print('CUSTOM RIG DONE')
