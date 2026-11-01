"""Batch B — side rig next steps + belt/palm trials, Cape Jones, 2026-11-01.
New dated folder only. No repo PR. No overwrite of any Mars-seen version.
Method (same as side-rig-wrist-fix-20261101): bone-parent cut-out rig in
Blender 4.5.3 LTS. A piece is an image plane PARENTED TO A BONE
(parent_type BONE, parent_bone); the plane transform is stored relative to
the bone-TAIL origin (rotation-only bone matrix, NOT the full matrix —
using the full matrix double-translated planes in the wrist-fix first run).
Rotating a parent bone moves its children automatically. No PIL placement
in any .blend output; PIL is used ONLY for measurement/contact sheets.
Usage: blender -b --python build_batch_b.py -- <stage>
Stages: side, back, knee, beltpalm, quarter
"""
import bpy, math, os, sys
from mathutils import Matrix, Euler, Vector

OUT = os.path.expanduser('~/workspace/cape-jones-rig/batch-b-side-rig-next-20261101')
CJ = os.path.expanduser('~/workspace/cape-jones-rig')
BLENDER = os.path.join(OUT, 'work', 'blender-4.5.3-linux-x64', 'blender')

def clear():
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
    # Purge orphan data between builds in one process: without this,
    # images/materials/armatures accumulate across rebuilds and the
    # process grows until the VM OOM-killer strikes (Batch B lesson).
    for _ in range(2):
        for coll in [bpy.data.meshes, bpy.data.materials, bpy.data.images,
                     bpy.data.armatures, bpy.data.cameras, bpy.data.worlds]:
            for x in list(coll):
                if x.users == 0:
                    coll.remove(x)

def make_armature(name, bones):
    """bones: list of (name, head_world, tail_world, parent). Returns arm."""
    bpy.ops.object.armature_add(enter_editmode=True)
    arm = bpy.context.object; arm.name = name
    eb = arm.data.edit_bones
    eb[0].name = bones[0][0]; eb[0].head = bones[0][1]; eb[0].tail = bones[0][2]
    for bn, hp, tp, parent in bones[1:]:
        b = eb.new(bn); b.head = hp; b.tail = tp
        if parent: b.parent = eb[parent]
    bpy.ops.object.mode_set(mode='OBJECT')
    return arm

def bone_rest_frames(arm, bones):
    bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode='POSE')
    rest = {}
    for bn, hp, tp, parent in bones:
        pb = arm.pose.bones[bn]
        rest[bn] = (pb.tail.copy(), pb.matrix.to_3x3().to_4x4())
    bpy.ops.object.mode_set(mode='OBJECT')
    return rest

def add_plane(arm, rest, name, path, w_px, h_px, scale, centre_world, rotdeg, z):
    w, h = w_px * scale / 100.0, h_px * scale / 100.0
    # NOTE: w/h here are in canvas-px units only if the W() mapping below
    # uses /100; we instead pass world sizes directly via centre_world and
    # a scale factor: caller gives w_world,h_world through scale trick.
    raise RuntimeError('use add_plane_world')

def add_plane_world(arm, rest, bone, name, path, w_world, h_world, centre_world, rotdeg, z):
    """centre_world: Vector world; rotdeg about Z; z added to centre z."""
    bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0))
    ob = bpy.context.object; ob.name = 'Plane_' + name
    mat = bpy.data.materials.new(name='Mat_' + name); mat.use_nodes = True; mat.blend_method = 'BLEND'
    bsdf = mat.node_tree.nodes['Principled BSDF']
    tex = mat.node_tree.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(path)
    mat.node_tree.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
    mat.node_tree.links.new(tex.outputs['Alpha'], bsdf.inputs['Alpha'])
    ob.data.materials.append(mat)
    cx = Vector((centre_world[0], centre_world[1], z))
    D = Matrix.Translation(cx) @ Euler((0, 0, math.radians(rotdeg))).to_matrix().to_4x4() @ Matrix.Diagonal((w_world / 2.0, h_world / 2.0, 1.0, 1.0))
    tail, Rmat = rest[bone]
    tail_origin = Matrix.Translation(tail) @ Rmat
    ob.parent = arm; ob.parent_type = 'BONE'; ob.parent_bone = bone
    ob.matrix_parent_inverse = Matrix.Identity(4)
    ob.matrix_basis = tail_origin.inverted() @ D
    return ob

def setup_scene(cam_y, res=(1400, 1600), pct=100):
    # pct: hero stills render at 100%; multi-frame trials at 50%
    # (700x800) for speed on software EEVEE — stated in REPORT.
    scene = bpy.context.scene; scene.render.engine = 'BLENDER_EEVEE_NEXT'
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.render.resolution_percentage = pct
    if pct < 100:
        scene.eevee.taa_render_samples = 32
    scene.render.image_settings.file_format = 'PNG'
    scene.world = bpy.data.worlds.new('GreyWorld'); scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.5, 0.5, 0.5, 1)
    bpy.ops.object.camera_add(location=(0, cam_y, 12), rotation=(0, 0, 0))
    cam = bpy.context.object; cam.data.type = 'ORTHO'; cam.data.ortho_scale = 14.0
    scene.camera = cam
    return scene

def render_to(scene, path):
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print('RENDERED', path)

def pose_bone(arm, bn, rotz=None, rotx=None):
    bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode='POSE')
    pb = arm.pose.bones[bn]; pb.rotation_mode = 'XYZ'
    if rotz is not None: pb.rotation_euler.z = rotz
    if rotx is not None: pb.rotation_euler.x = rotx
    bpy.ops.object.mode_set(mode='OBJECT'); bpy.context.view_layer.update()

def pose_bones_report(arm, names):
    bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode='POSE')
    for bn in names:
        pb = arm.pose.bones[bn]
        print(' BONE', bn, 'parent', pb.parent.name if pb.parent else None,
              'rotXYZ', tuple(round(v, 4) for v in pb.rotation_euler),
              'head', tuple(round(v, 3) for v in pb.head),
              'tail', tuple(round(v, 3) for v in pb.tail))
    bpy.ops.object.mode_set(mode='OBJECT')

# ---------------------------------------------------------------- SIDE
def W(px, py, z=0.0):
    return Vector(((px - 700) / 100.0, (1450 - py) / 100.0, z))

SIDE_BONES = [
    ('hip',       (680, 900),  (675, 770),  None),
    ('chest',     (675, 770),  (665, 540),  'hip'),
    ('neck',      (665, 540),  (662, 280),  'chest'),
    ('head',      (662, 280),  (662, 120),  'neck'),
    ('upper_near', (650, 500),  (650, 690),  'chest'),
    ('forearm_near', (650, 690), (650, 900), 'upper_near'),
    ('hand_near', (650, 900),  (650, 1000), 'forearm_near'),
    ('upper_far', (625, 600),  (625, 790),  'chest'),
    ('forearm_far', (625, 790), (625, 1000), 'upper_far'),
    ('hand_far',  (625, 1000), (625, 1100), 'forearm_far'),
    ('thigh_near', (670, 900),  (690, 1120), 'hip'),
    ('shin_near', (690, 1120), (700, 1450), 'thigh_near'),
    ('thigh_far', (645, 900),  (660, 1120), 'hip'),
    ('shin_far',  (660, 1120), (670, 1450), 'thigh_far'),
]
S = 0.9557
SIDE_BASE = os.path.join(CJ, 'side-pack-new-20261101')
SIDE_SIZES = {'side_cape_long.png': (235, 683), 'side_thigh_right.png': (157, 325),
    'side_shin_right.png': (111, 316), 'side_boot_right.png': (193, 202),
    'side_upper_arm_left.png': (134, 267), 'side_forearm_gauntlet_right.png': (234, 107),
    'side_fist_right.png': (130, 103), 'side_pelvis_hip.png': (194, 167),
    'side_torso_belt.png': (256, 365), 'side_cowl_neck.png': (145, 186),
    'side_head_profile.png': (173, 193), 'side_thigh_left.png': (166, 335),
    'side_shin_boot_left.png': (193, 358), 'side_upper_arm_right.png': (144, 266),
    'side_cape_drape.png': (277, 208)}

def build_side(extra_belt=False):
    """Side rig, wrist-fix bones, with neck fix (neck centre 663,357, neck
    z 0.04 behind head z 0.06) and Row5_15 standalone open hands on both
    hand bones (wrist-anchored, rest rot -148 deg). Fists are NOT in this
    .blend (they stay in the wrist-fix .blend untouched) — no double hand.
    Returns (arm, rest, planes)."""
    clear()
    bones = [(n, W(*hp), W(*tp), p) for n, hp, tp, p in SIDE_BONES]
    arm = make_armature('SideRigArmature_BatchB', bones)
    rest = bone_rest_frames(arm, bones)
    PLANES = [
        ('cape_long',  'side_cape_long.png',  'chest', (640, 866), 0, -0.20),
        ('thigh_far',  'side_thigh_right.png', 'thigh_far', (652, 1010), 0, -0.10),
        ('shin_far',   'side_shin_right.png', 'shin_far', (665, 1285), 0, -0.10),
        ('boot_far',   'side_boot_right.png', 'shin_far', (670, 1354), 0, -0.10),
        ('upper_far',  'side_upper_arm_left.png', 'upper_far', (625, 695), 0, -0.10),
        ('forearm_far', 'side_forearm_gauntlet_right.png', 'forearm_far', (625, 895), -90, -0.10),
        ('pelvis',     'side_pelvis_hip.png', 'hip',     (677, 835), 0, -0.05),
        ('torso',      'side_torso_belt.png', 'chest',   (670, 655), 0,  0.00),
        ('neck',       'side_cowl_neck.png',  'neck',    (663, 357), 0,  0.04),  # FIX: up 10, behind head
        ('head',       'side_head_profile.png', 'head',   (662, 200), 0,  0.06),
        ('thigh_near', 'side_thigh_left.png', 'thigh_near', (680, 1010), 0,  0.10),
        ('shin_near',  'side_shin_boot_left.png', 'shin_near', (695, 1279), 0,  0.10),
        ('upper_near', 'side_upper_arm_right.png', 'upper_near', (650, 595), 0,  0.15),
        ('forearm_near', 'side_forearm_gauntlet_right.png', 'forearm_near', (650, 795), -90, 0.15),
        ('cape_collar', 'side_cape_drape.png', 'chest',   (634, 475), 0,  0.20),
    ]
    planes = {}
    for name, fn, bone, (cx, cy), rotdeg, z in PLANES:
        w_px, h_px = SIDE_SIZES[fn]
        planes[name] = add_plane_world(arm, rest, bone, name,
            os.path.join(SIDE_BASE, fn), w_px * S / 100.0, h_px * S / 100.0,
            W(cx, cy), rotdeg, z)
    # Standalone open hands: Row5_15, wrist-anchored.
    # Native finger angle ~+58.3 deg (world); rest rot -148 deg gives
    # fingers down at rest and +X after the +90 deg forearm bend.
    # Wrist native (25,110), piece centre (60.5,60.5); local wrist
    # (-0.587,-0.818). Centres below are wrist-anchored at rest (see
    # REPORT for the math); bone parenting preserves the anchor in pose.
    r5 = os.path.join(CJ, 'sliced-clean-20261031', 'A-root', '08-body-parts-limbs-capes', 'Row5_15.png')
    for name, bone, (cx, cy), z in [
            ('open_near', 'hand_near', (645, 958), 0.15),
            ('open_far', 'hand_far', (620, 1058), -0.10)]:
        planes[name] = add_plane_world(arm, rest, bone, name, r5,
            121 * S / 100.0, 121 * S / 100.0, W(cx, cy), -148, z)
    if extra_belt:
        r7 = os.path.join(CJ, 'sliced-clean-20261031', 'A-root', '08-body-parts-limbs-capes', 'Row7_10.png')
        planes['belt_row7'] = add_plane_world(arm, rest, 'chest', 'belt_row7', r7,
            206 * S / 100.0, 82 * S / 100.0, W(670, 790), 0, 0.25)
    bpy.context.view_layer.update()
    return arm, rest, planes

def stage_side():
    arm, rest, planes = build_side()
    scene = setup_scene(6.65)
    # rest render
    render_to(scene, os.path.join(OUT, 'side-open-hand-rest-20261101.png'))
    # bent pose (same as wrist-fix: forearms +90 deg)
    pose_bone(arm, 'forearm_near', rotz=math.pi / 2)
    pose_bone(arm, 'forearm_far', rotz=math.pi / 2)
    render_to(scene, os.path.join(OUT, 'side-open-hand-bent-20261101.png'))
    pose_bones_report(arm, ['forearm_near', 'hand_near', 'forearm_far', 'hand_far'])
    # wrist gate: hand-plane wrist point vs forearm tail (posed)
    def wrist_world(ob):
        return ob.matrix_world @ Vector((-0.587, -0.818, 0))
    for f, h, op in [('forearm_near', 'hand_near', 'open_near'), ('forearm_far', 'hand_far', 'open_far')]:
        fb = arm.pose.bones[f]
        wp = wrist_world(planes[op])
        print(' WRISTOPEN', f, 'tail', tuple(round(v, 3) for v in fb.tail),
              'hand wrist pt', tuple(round(v, 3) for v in wp),
              'dist', round((fb.tail - wp).length, 4))
    # FK chain: keys rest -> bent -> rest, forearm bones only (hands are
    # children: 6/6 arm bones FK-driven, 0 IK, 0 PIL placement).
    bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode='POSE')
    for bn in ['forearm_near', 'forearm_far']:
        pb = arm.pose.bones[bn]; pb.rotation_mode = 'XYZ'
    keys = [(1, 0.0), (13, math.pi / 4), (25, math.pi / 2), (37, math.pi / 4), (49, 0.0)]
    for fr, ang in keys:
        bpy.context.scene.frame_set(fr)
        for bn in ['forearm_near', 'forearm_far']:
            arm.pose.bones[bn].rotation_euler.z = ang
            arm.pose.bones[bn].keyframe_insert(data_path='rotation_euler', frame=fr)
    bpy.ops.object.mode_set(mode='OBJECT')
    frames = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49]
    os.makedirs(os.path.join(OUT, 'frames-fk'), exist_ok=True)
    for fr in frames:
        bpy.context.scene.frame_set(fr)
        render_to(scene, os.path.join(OUT, 'frames-fk', 'fk-%02d-20261101.png' % fr))
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'side-rig-batch-b-open-hand-20261101.blend'))
    print('SAVED side .blend')
    # side belt trial render (Row7_10 overlay, fresh build)
    arm2, rest2, planes2 = build_side(extra_belt=True)
    scene2 = setup_scene(6.65)
    render_to(scene2, os.path.join(OUT, 'side-belt-row7-trial-20261101.png'))
    print('SAVED side belt trial render')

# ---------------------------------------------------------------- BACK
def WB(px, py, z=0.0):
    return Vector(((px - 700) / 100.0, (1540 - py) / 100.0, z))

SB = 1.20
BACK_BASE = os.path.join(CJ, 'back-pack-base-20261101')
BACK_SIZES = {'back_cape_full_SECONDARY.png': (468, 766), 'back_cape_drape_top.png': (283, 188),
    'back_torso.png': (362, 296), 'back_cowl_neck.png': (165, 142), 'back_cowl_head.png': (167, 207),
    'back_belt_pelvis.png': (192, 160), 'back_upper_arm_left.png': (126, 213),
    'back_upper_arm_right.png': (126, 213), 'back_forearm_gauntlet_hand_left.png': (103, 273),
    'back_forearm_gauntlet_hand_right.png': (103, 273), 'back_thigh_left.png': (116, 242),
    'back_thigh_right.png': (115, 242), 'back_shin_boot_left.png': (114, 301),
    'back_shin_boot_right.png': (113, 301)}
# Character-side mapping (back view mirrors): sheet-LEFT = viewer's left =
# character's RIGHT = Arm_Back; sheet-RIGHT = character's LEFT = Arm_Front.
BACK_BONES = [
    ('hip',       (700, 885),  (700, 800),  None),
    ('chest',     (700, 800),  (700, 490),  'hip'),
    ('neck',      (700, 490),  (700, 360),  'chest'),
    ('head',      (700, 360),  (700, 170),  'neck'),
    ('upper_ArmBack', (606, 500), (575, 756), 'chest'),
    ('forearm_ArmBack', (575, 756), (542, 1084), 'upper_ArmBack'),
    ('hand_ArmBack', (542, 1084), (542, 1184), 'forearm_ArmBack'),
    ('upper_ArmFront', (793, 500), (824, 756), 'chest'),
    ('forearm_ArmFront', (824, 756), (857, 1084), 'upper_ArmFront'),
    ('hand_ArmFront', (857, 1084), (857, 1184), 'forearm_ArmFront'),
    ('thigh_ArmBack', (645, 940), (648, 1230), 'hip'),
    ('shin_ArmBack', (648, 1230), (627, 1540), 'thigh_ArmBack'),
    ('thigh_ArmFront', (753, 940), (750, 1230), 'hip'),
    ('shin_ArmFront', (750, 1230), (771, 1540), 'thigh_ArmFront'),
]

def build_back(palm=None, belt=None):
    """palm: None | ('row5', arm) | ('hand10', arm) | ('both', None)
    belt: None | 'split' | 'row7' — belt variant replaces the fused
    belt+pelvis plane as noted in REPORT; fused original is never edited.
    Returns (arm, rest, planes)."""
    clear()
    bones = [(n, WB(*hp), WB(*tp), p) for n, hp, tp, p in BACK_BONES]
    arm = make_armature('BackRigArmature_BatchB', bones)
    rest = bone_rest_frames(arm, bones)
    PLANES = [
        ('cape_full', 'back_cape_full_SECONDARY.png', 'chest', (700, 960), 0, -0.20),
        ('thigh_ArmBack', 'back_thigh_left.png', 'thigh_ArmBack', (655, 1085), 0, -0.10),
        ('shin_ArmBack', 'back_shin_boot_left.png', 'shin_ArmBack', (636, 1360), 0, -0.10),
        ('upper_ArmBack', 'back_upper_arm_left.png', 'upper_ArmBack', (605, 628), 0, -0.10),
        ('forearm_ArmBack', 'back_forearm_gauntlet_hand_left.png', 'forearm_ArmBack', (560, 920), 0, -0.10),
        ('torso', 'back_torso.png', 'chest', (700, 659), 0, 0.00),
        ('neck', 'back_cowl_neck.png', 'neck', (700, 437), 0, 0.05),
        ('head', 'back_cowl_head.png', 'head', (700, 288), 0, 0.05),
        ('drape', 'back_cape_drape_top.png', 'chest', (700, 560), 0, 0.12),
        ('thigh_ArmFront', 'back_thigh_right.png', 'thigh_ArmFront', (745, 1085), 0, 0.15),
        ('shin_ArmFront', 'back_shin_boot_right.png', 'shin_ArmFront', (763, 1360), 0, 0.15),
        ('upper_ArmFront', 'back_upper_arm_right.png', 'upper_ArmFront', (795, 628), 0, 0.15),
        ('forearm_ArmFront', 'back_forearm_gauntlet_hand_right.png', 'forearm_ArmFront', (841, 920), 0, 0.15),
    ]
    if belt is None:
        PLANES.append(('belt_pelvis', 'back_belt_pelvis.png', 'hip', (700, 883), 0, -0.05))
    planes = {}
    for name, fn, bone, (cx, cy), rotdeg, z in PLANES:
        w_px, h_px = BACK_SIZES[fn]
        planes[name] = add_plane_world(arm, rest, bone, name,
            os.path.join(BACK_BASE, fn), w_px * SB / 100.0, h_px * SB / 100.0,
            WB(cx, cy), rotdeg, z)
    if belt == 'split':
        # Outline-row split pieces made by PIL (see REPORT): belt keeps its
        # drawn bottom outline; pelvis starts below it. Layered belt
        # above pelvis reconstructs the fused piece.
        planes['belt_layer'] = add_plane_world(arm, rest, 'hip', 'belt_layer',
            os.path.join(OUT, 'belt-split-belt-20261101.png'), 192 * SB / 100.0, 160 * SB / 100.0,
            WB(700, 883), 0, -0.03)
        planes['pelvis_layer'] = add_plane_world(arm, rest, 'hip', 'pelvis_layer',
            os.path.join(OUT, 'belt-split-pelvis-20261101.png'), 192 * SB / 100.0, 160 * SB / 100.0,
            WB(700, 883), 0, -0.05)
    if belt == 'row7':
        planes['belt_pelvis'] = add_plane_world(arm, rest, 'hip', 'belt_pelvis',
            os.path.join(BACK_BASE, 'back_belt_pelvis.png'), 192 * SB / 100.0, 160 * SB / 100.0,
            WB(700, 883), 0, -0.05)
        r7 = os.path.join(CJ, 'sliced-clean-20261031', 'A-root', '08-body-parts-limbs-capes', 'Row7_10.png')
        # Waist = top of the belt+pelvis piece (fused belt rows 0-47 ->
        # canvas 787-857); band centre 822 covers that band.
        planes['belt_row7'] = add_plane_world(arm, rest, 'hip', 'belt_row7', r7,
            206 * SB / 100.0, 82 * SB / 100.0, WB(700, 822), 0, -0.01)
    # Palm trials: separate palm planes on hand bones, CENTRED OVER the
    # fused palm region (fused palm canvas centre ~(790,1015) ArmFront,
    # ~(610,1015) ArmBack; fused wrist ~y 940, inside the forearm piece).
    # This is a static coverage trial: same centre makes overhang vs the
    # fused palm exact. Fingers DOWN at rest (matching fused direction).
    # Row5_15: native finger angle +58.3 deg -> rest rot -148 deg.
    # Hand_10: native fingers +X (0 deg) -> rest rot -90 deg.
    # For a POSED use the palm plane must be re-anchored to the hand-bone
    # head (wrist point); that re-anchor is NOT done in this static fit
    # trial and is stated in REPORT.
    r5 = os.path.join(CJ, 'sliced-clean-20261031', 'A-root', '08-body-parts-limbs-capes', 'Row5_15.png')
    h10 = os.path.join(CJ, 'pack1', 'Hand_10.png')
    palm_spec = []
    if palm == ('row5', 'ArmFront'):
        palm_spec = [('palm_row5', 'hand_ArmFront', r5, 121, 121, -148, (851, 1015), 0.20)]
    elif palm == ('hand10', 'ArmFront'):
        palm_spec = [('palm_hand10', 'hand_ArmFront', h10, 161, 110, -90, (851, 1015), 0.20)]
    elif palm == 'both':
        palm_spec = [('palm_row5', 'hand_ArmFront', r5, 121, 121, -148, (795, 1010), 0.20),
                     ('palm_hand10', 'hand_ArmBack', h10, 161, 110, -90, (548, 1015), 0.20)]
    for name, bone, path, w_px, h_px, rotdeg, (cx, cy), z in palm_spec:
        planes[name] = add_plane_world(arm, rest, bone, name, path,
            w_px * SB / 100.0, h_px * SB / 100.0, WB(cx, cy), rotdeg, z)
    bpy.context.view_layer.update()
    return arm, rest, planes

def stage_back():
    arm, rest, planes = build_back()
    scene = setup_scene(6.88)
    render_to(scene, os.path.join(OUT, 'back-rig-standing-v2-20261101.png'))
    pose_bones_report(arm, ['forearm_ArmBack', 'hand_ArmBack', 'forearm_ArmFront', 'hand_ArmFront'])
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'back-rig-batch-b-v2-20261101.blend'))
    print('SAVED back .blend')
    # Sitting trials (TRIALS ONLY — no decision; see REPORT for why none
    # of these replaces a true back-sitting drawing).
    # S-A: in-plane splay crouch.
    arm, rest, planes = build_back()
    scene = setup_scene(6.88, pct=50)
    pose_bone(arm, 'thigh_ArmBack', rotz=math.radians(25))
    pose_bone(arm, 'shin_ArmBack', rotz=math.radians(-25))
    pose_bone(arm, 'thigh_ArmFront', rotz=math.radians(-25))
    pose_bone(arm, 'shin_ArmFront', rotz=math.radians(25))
    render_to(scene, os.path.join(OUT, 'back-sitting-trial-v2-A-splay-20261101.png'))
    # S-B: rotX foreshorten sit (thighs forward, shins down).
    arm, rest, planes = build_back()
    scene = setup_scene(6.88, pct=50)
    pose_bone(arm, 'thigh_ArmBack', rotx=math.radians(70))
    pose_bone(arm, 'shin_ArmBack', rotx=math.radians(-70))
    pose_bone(arm, 'thigh_ArmFront', rotx=math.radians(70))
    pose_bone(arm, 'shin_ArmFront', rotx=math.radians(-70))
    render_to(scene, os.path.join(OUT, 'back-sitting-trial-v2-B-foreshorten-20261101.png'))
    # S-C: S-B + hip drop so feet reach the ground (armature lowered).
    arm, rest, planes = build_back()
    scene = setup_scene(6.88, pct=50)
    pose_bone(arm, 'thigh_ArmBack', rotx=math.radians(70))
    pose_bone(arm, 'shin_ArmBack', rotx=math.radians(-70))
    pose_bone(arm, 'thigh_ArmFront', rotx=math.radians(70))
    pose_bone(arm, 'shin_ArmFront', rotx=math.radians(-70))
    arm.location.y -= 1.91
    bpy.context.view_layer.update()
    render_to(scene, os.path.join(OUT, 'back-sitting-trial-v2-C-drop-20261101.png'))
    print('SAVED sitting trials')

# ---------------------------------------------------------------- KNEE
def stage_knee():
    """Leg-only trial rig. K = knee-cap centre = thigh bone tail.
    P = saved shin pivot, offset from K by the RIG-06 reported gaps:
    L (-70,+13) -> 71.2 px, R (-74,-12) -> 75.0 px (canvas px, y down).
    Options: A saved pivot; B pivot moved to K (TRIAL ONLY, not saved
    anywhere as a default); C saved pivot + shin plane re-anchored at
    rest so its top-centre sits under K. Renders at 0/30/60 deg."""
    clear()
    def W2(px, py):
        return Vector(((px - 700) / 100.0, (1540 - py) / 100.0, 0))
    bones = []
    # thigh bones vertical; shin bones start at P (option A/C) — for
    # option B the shin bone head is rebuilt at K in its own build.
    for side, tx, off in [('L', 560, (-70, 13)), ('R', 840, (-74, -12))]:
        kx, ky = tx, 1230
        px, py = kx + off[0], ky + off[1]
        bones.append(('thigh_' + side, W2(tx, 940), W2(tx, 1230), None))
        bones.append(('shin_' + side, W2(px, py), W2(px, py + 310), 'thigh_' + side))
    # NOTE: shin bones are children of thigh bones here so the rig is a
    # chain; rotation is applied to the shin bone in POSE mode (local
    # rotation about its own head). Parenting does not move the head:
    # a child bone head stays where the edit bone put it.
    arm = make_armature('KneeTrialArmature_BatchB', bones)
    rest = bone_rest_frames(arm, bones)
    scene = setup_scene(6.88, pct=50)
    planes = {}
    for side, tx, off in [('L', 560, (-70, 13)), ('R', 840, (-74, -12))]:
        fn_t = 'back_thigh_left.png' if side == 'L' else 'back_thigh_right.png'
        fn_s = 'back_shin_boot_left.png' if side == 'L' else 'back_shin_boot_right.png'
        planes['thigh_' + side] = add_plane_world(arm, rest, 'thigh_' + side,
            'thigh_' + side, os.path.join(BACK_BASE, fn_t),
            116 * SB / 100.0, 242 * SB / 100.0, W2(tx, 1085), 0, 0.0)
        # shin plane: top at 1180 (50 px overlap under thigh bottom 1230),
        # centre x = shin bone x (P_x) for option A.
        px = tx + off[0]
        planes['shin_' + side] = add_plane_world(arm, rest, 'shin_' + side,
            'shin_' + side, os.path.join(BACK_BASE, fn_s),
            114 * SB / 100.0, 301 * SB / 100.0, W2(px, 1360), 0, 0.10)
    bpy.context.view_layer.update()
    for opt, angles in [('A', [0, 30, 60]), ('B', [0, 30, 60]), ('C', [0, 30, 60])]:
        if opt == 'C':
            # Saved pivots KEPT; only the shin PLANE is re-anchored at
            # rest so its top-centre sits under the knee-cap centre K
            # (centre x = thigh x). Rotation still swings about P, so
            # the gap reappears when bent — that is what C measures.
            for side, tx in [('L', 560), ('R', 840)]:
                old = planes['shin_' + side]
                bpy.data.objects.remove(old, do_unlink=True)
                fn_s = 'back_shin_boot_left.png' if side == 'L' else 'back_shin_boot_right.png'
                planes['shin_' + side] = add_plane_world(arm, rest, 'shin_' + side,
                    'shin_' + side, os.path.join(BACK_BASE, fn_s),
                    114 * SB / 100.0, 301 * SB / 100.0, W2(tx, 1360), 0, 0.10)
            bpy.context.view_layer.update()
        for ang in angles:
            # reset
            bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode='POSE')
            for bn in ['shin_L', 'shin_R']:
                pb = arm.pose.bones[bn]; pb.rotation_mode = 'XYZ'; pb.rotation_euler.z = 0
            bpy.ops.object.mode_set(mode='OBJECT')
            if opt == 'B':
                # TRIAL ONLY: move shin bone heads to K by moving the
                # whole shin bone (edit mode) — this .blend is NOT saved
                # as a default; it exists only for the trial renders.
                bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode='EDIT')
                for side, tx in [('L', 560), ('R', 840)]:
                    eb = arm.data.edit_bones['shin_' + side]
                    dx = W2(tx, 1230) - eb.head
                    eb.head += dx; eb.tail += dx
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.context.view_layer.update()
                # re-parent planes to the moved bones is unnecessary:
                # planes follow their bone; the bone move shifts planes
                # with it, which is exactly the trial geometry.
            if ang:
                pose_bone(arm, 'shin_L', rotz=math.radians(ang))
                pose_bone(arm, 'shin_R', rotz=math.radians(ang))
            # shin top-centre vs K measurement (plane top edge midpoint)
            for side, tx in [('L', 560), ('R', 840)]:
                ob = planes['shin_' + side]
                xs = []; ys = []
                for v in ob.data.vertices:
                    wv = ob.matrix_world @ v.co
                    xs.append(wv.x); ys.append(wv.y)
                # top edge midpoint in world: average of the two top verts
                top = sorted([(ob.matrix_world @ v.co) for v in ob.data.vertices], key=lambda p: -p.y)[:2]
                tm = sum(top, Vector((0, 0, 0))) / 2
                K = W2(tx, 1230)
                print(' KNEE opt', opt, 'ang', ang, 'leg', side,
                      'shin-top-mid', tuple(round(v, 3) for v in tm),
                      'K', tuple(round(v, 3) for v in K),
                      'dist_px', round((tm - K).length * 100, 1))
            render_to(scene, os.path.join(OUT, 'knee-trial-%s-%02d-20261101.png' % (opt, ang)))
            if opt == 'B':
                # restore shin bones to saved pivots for the next option
                bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode='EDIT')
                for side, tx, off in [('L', 560, (-70, 13)), ('R', 840, (-74, -12))]:
                    eb = arm.data.edit_bones['shin_' + side]
                    dx = W2(tx + off[0], 1230 + off[1]) - eb.head
                    eb.head += dx; eb.tail += dx
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.context.view_layer.update()
    print('KNEE trials rendered (option B geometry is trial-only, not saved)')

# ---------------------------------------------------------------- BELT/PALM
def stage_beltpalm():
    # Belt split renders: fused control, split layer, Row7 overlay.
    arm, rest, planes = build_back(belt=None)
    scene = setup_scene(6.88, pct=50)
    render_to(scene, os.path.join(OUT, 'belt-trial-0-fused-20261101.png'))
    arm, rest, planes = build_back(belt='split')
    scene = setup_scene(6.88, pct=50)
    render_to(scene, os.path.join(OUT, 'belt-trial-1-split-20261101.png'))
    arm, rest, planes = build_back(belt='row7')
    scene = setup_scene(6.88, pct=50)
    render_to(scene, os.path.join(OUT, 'belt-trial-2-row7-20261101.png'))
    # Palm trials: fused control, Row5_15 on ArmFront, Hand_10 on
    # ArmFront, both (Row5_15 ArmFront + Hand_10 ArmBack).
    for tag, palm in [('0-fused', None), ('1-row5', ('row5', 'ArmFront')),
                      ('2-hand10', ('hand10', 'ArmFront')), ('3-both', 'both')]:
        arm, rest, planes = build_back(palm=palm)
        scene = setup_scene(6.88, pct=50)
        render_to(scene, os.path.join(OUT, 'palm-trial-%s-20261101.png' % tag))
    print('BELT/PALM trials rendered')

# ---------------------------------------------------------------- 3/4 BACK
def stage_quarter():
    """Whole-figure plane + skeleton overlay ONLY. No piece cuts (that
    decision is Mars's, per the view-field report Q4). Joint coords are
    estimates from visible landmarks; occluded joints are labelled
    INVENTED-estimate in REPORT. A pose attempt proves the single plane
    cannot articulate: bones/markers move, the plane does not."""
    clear()
    def WQ(px, py):
        return Vector(((px - 700) / 100.0, (1540 - py) / 100.0, 0))
    # canvas joints (see REPORT for sheet->canvas mapping, S=1.40)
    bones = [
        ('hip',   (771, 810),  (771, 450),  None),
        ('chest', (771, 450),  (778, 400),  'hip'),
        ('neck',  (778, 400),  (782, 340),  'chest'),
        ('head',  (782, 340),  (785, 210),  'neck'),
        ('upper_R', (925, 377), (967, 642), 'chest'),
        ('forearm_R', (967, 642), (995, 838), 'upper_R'),
        ('hand_R', (995, 838), (995, 894), 'forearm_R'),
        ('upper_L', (561, 405), (477, 614), 'chest'),
        ('forearm_L', (477, 614), (477, 684), 'upper_L'),
        ('hand_L', (477, 684), (477, 740), 'forearm_L'),
        ('thigh_R', (800, 810), (883, 1090), 'hip'),
        ('shin_R', (883, 1090), (897, 1342), 'thigh_R'),
        ('thigh_L', (740, 810), (659, 1090), 'hip'),
        ('shin_L', (659, 1090), (673, 1342), 'thigh_L'),
    ]
    bb = [(n, WQ(*hp), WQ(*tp), p) for n, hp, tp, p in bones]
    arm = make_armature('QuarterBackArmature_Trial', bb)
    rest = bone_rest_frames(arm, bb)
    sheet = os.path.join(CJ, 'sliced-clean-20261031', 'B-model', 'model-sheet-3quarter-back-set2', 'Row1_1.png')
    plane = add_plane_world(arm, rest, 'chest', 'quarter_figure', sheet,
        619 * 1.40 / 100.0, 996 * 1.40 / 100.0, WQ(700, 780), 0, 0.0)
    # joint markers (red spheres, bone-parented to their bone's TAIL frame
    # so they follow the skeleton in the pose attempt)
    joints = {'hip': (771, 810), 'neck_base': (778, 400), 'head_top': (785, 210),
        'shoulder_R': (925, 377), 'elbow_R': (967, 642), 'wrist_R': (995, 838),
        'shoulder_L': (561, 405), 'elbow_L': (477, 614), 'wrist_L': (477, 684),
        'knee_R': (883, 1090), 'ankle_R': (897, 1342), 'knee_L': (659, 1090), 'ankle_L': (673, 1342)}
    joint_bone = {'hip': 'hip', 'neck_base': 'neck', 'head_top': 'head',
        'shoulder_R': 'upper_R', 'elbow_R': 'forearm_R', 'wrist_R': 'hand_R',
        'shoulder_L': 'upper_L', 'elbow_L': 'forearm_L', 'wrist_L': 'hand_L',
        'knee_R': 'shin_R', 'ankle_R': 'shin_R', 'knee_L': 'shin_L', 'ankle_L': 'shin_L'}
    mat = bpy.data.materials.new(name='Mat_marker'); mat.use_nodes = True
    mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (1, 0, 0, 1)
    for jn, (jx, jy) in joints.items():
        bone = joint_bone[jn]
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.09, location=(0, 0, 0))
        ob = bpy.context.object; ob.name = 'Marker_' + jn
        ob.data.materials.append(mat)
        tail, Rmat = rest[bone]
        tail_origin = Matrix.Translation(tail) @ Rmat
        D = Matrix.Translation(WQ(jx, jy) + Vector((0, 0, 0.30)))
        ob.parent = arm; ob.parent_type = 'BONE'; ob.parent_bone = bone
        ob.matrix_parent_inverse = Matrix.Identity(4)
        ob.matrix_basis = tail_origin.inverted() @ D
    bpy.context.view_layer.update()
    scene = setup_scene(6.88)
    render_to(scene, os.path.join(OUT, 'quarter-back-trial-20261101.png'))
    # pose attempt: rotate thigh_R + forearm_R; markers move, plane does not
    pose_bone(arm, 'thigh_R', rotz=math.radians(30))
    pose_bone(arm, 'forearm_R', rotz=math.radians(30))
    scene.render.resolution_percentage = 50
    render_to(scene, os.path.join(OUT, 'quarter-back-pose-attempt-20261101.png'))
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'quarter-back-trial-20261101.blend'))
    print('SAVED quarter-back trial .blend')

if __name__ == '__main__':
    argv = sys.argv
    stage = argv[argv.index('--') + 1] if '--' in argv else 'side'
    print('STAGE', stage)
    {'side': stage_side, 'back': stage_back, 'knee': stage_knee,
     'beltpalm': stage_beltpalm, 'quarter': stage_quarter}[stage]()
