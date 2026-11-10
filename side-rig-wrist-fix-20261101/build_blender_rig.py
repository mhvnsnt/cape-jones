"""Bone-parent side bent rig, Blender 4.5.3. NO PIL placement, NO cutting.
Method (research, see REPORT): cut-out bone rig - Harmony/Blender/Tahoma/Spine:
a piece is an image plane PARENTED TO A BONE (parent_type BONE, parent_bone),
its transform stored relative to the bone's tail origin. Rotating the forearm
bone moves forearm plane AND its child hand bone AND the hand plane with it.
Hand is a CHILD bone of forearm, forearm a CHILD of upper arm - no separate
hand placement, no wrist cut, fused assemblies are NOT used for the near arm.
Rest pose: arms/legs vertical down. Pose: forearm bones rotate +90 deg Z,
which Blender bone tests proved moves a down-pointing bone's tail to +X
(facing right, flexion forward, not extension). Only bent pose is built -
no idle arms-down pose in this task.
Bones are defined once (head/tail in canvas px, centre 700, ground 1450);
plane centres are bone midpoints / bone-tail anchors, NOT per-piece x/y.
"""
import bpy, math, os
from mathutils import Matrix, Euler, Vector

OUT = os.path.expanduser('~/workspace/cape-jones-rig/side-rig-wrist-fix-20261101')
BASE = os.path.expanduser('~/workspace/cape-jones-rig/side-pack-new-20261101')
S = 0.9557  # single global scale from side-rig-auto manifest, not per-piece
def W(px, py, z=0.0):
    return Vector(((px-700)/100.0, (1450-py)/100.0, z))

# bone: name, head px, tail px, parent
BONES = [
    ('hip',       (680,900),  (675,770),  None),
    ('chest',     (675,770),  (665,540),  'hip'),
    ('neck',      (665,540),  (662,280),  'chest'),
    ('head',      (662,280),  (662,120),  'neck'),
    ('upper_near',(650,500),  (650,690),  'chest'),
    ('forearm_near',(650,690),(650,900),  'upper_near'),
    ('hand_near', (650,900),  (650,1000), 'forearm_near'),
    ('upper_far', (625,600),  (625,790),  'chest'),
    ('forearm_far',(625,790), (625,1000), 'upper_far'),
    ('hand_far',  (625,1000), (625,1100), 'forearm_far'),
    ('thigh_near',(670,900),  (690,1120), 'hip'),
    ('shin_near', (690,1120), (700,1450), 'thigh_near'),
    ('thigh_far', (645,900),  (660,1120), 'hip'),
    ('shin_far',  (660,1120), (670,1450), 'thigh_far'),
]
# plane: name, file, bone, centre px, rot_z deg, z layer
PLANES = [
    ('cape_long',  'side_cape_long.png',  'chest', (640,866), 0, -0.20),
    ('thigh_far',  'side_thigh_right.png','thigh_far',(652,1010),0, -0.10),
    ('shin_far',   'side_shin_right.png', 'shin_far',(665,1285),0, -0.10),
    ('boot_far',   'side_boot_right.png', 'shin_far',(670,1354),0, -0.10),
    ('upper_far',  'side_upper_arm_left.png','upper_far',(625,695),0, -0.10),
    ('forearm_far','side_forearm_gauntlet_right.png','forearm_far',(625,895),-90,-0.10),
    ('fist_far',   'side_fist_right.png', 'hand_far',(625,1050),-90,-0.10),
    ('pelvis',     'side_pelvis_hip.png', 'hip',     (677,835), 0, -0.05),
    ('torso',      'side_torso_belt.png', 'chest',   (670,655), 0,  0.00),
    ('neck',       'side_cowl_neck.png',  'neck',    (663,367), 0,  0.05),  # anchor: top 278 = head bottom 292 - 14 overlap
    ('head',       'side_head_profile.png','head',   (662,200), 0,  0.05),
    ('thigh_near', 'side_thigh_left.png', 'thigh_near',(680,1010),0,  0.10),
    ('shin_near',  'side_shin_boot_left.png','shin_near',(695,1279),0,  0.10),
    ('upper_near', 'side_upper_arm_right.png','upper_near',(650,595),0,  0.15),
    ('forearm_near','side_forearm_gauntlet_right.png','forearm_near',(650,795),-90,0.15),
    ('fist_near',  'side_fist_right.png', 'hand_near',(650,950),-90,0.15),
    ('cape_collar','side_cape_drape.png', 'chest',   (634,475), 0,  0.20),
]
POSE_ROT = {'forearm_near': math.pi/2, 'forearm_far': math.pi/2}  # +90 Z = down -> +X forward

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
# armature
bpy.ops.object.armature_add(enter_editmode=True)
arm = bpy.context.object; arm.name = 'SideRigArmature_WristFix'
eb = arm.data.edit_bones
eb[0].name = BONES[0][0]; eb[0].head = W(*BONES[0][1]); eb[0].tail = W(*BONES[0][2])
for name, hp, tp, parent in BONES[1:]:
    b = eb.new(name); b.head = W(*hp); b.tail = W(*tp)
    if parent: b.parent = eb[parent]
bpy.ops.object.mode_set(mode='OBJECT')
# rest bone tail-origin matrices (pose mode, rest pose)
bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode='POSE')
bone_rest = {}
for name, hp, tp, parent in BONES:
    pb = arm.pose.bones[name]
    bone_rest[name] = (pb.tail.copy(), pb.matrix.to_3x3().to_4x4())
bpy.ops.object.mode_set(mode='OBJECT')
print('REST BONES:')
for n,(t,m) in bone_rest.items(): print(' ', n, 'tail', tuple(round(v,3) for v in t), 'rotZ', round(m.to_euler().z,3))

planes = {}
for name, fn, bone, (cx,cy), rotdeg, z in PLANES:
    path = os.path.join(BASE, fn)
    SIZES = {'side_cape_long.png':(235,683),'side_thigh_right.png':(157,325),'side_shin_right.png':(111,316),'side_boot_right.png':(193,202),'side_upper_arm_left.png':(134,267),'side_forearm_gauntlet_right.png':(234,107),'side_fist_right.png':(130,103),'side_pelvis_hip.png':(194,167),'side_torso_belt.png':(256,365),'side_cowl_neck.png':(145,186),'side_head_profile.png':(173,193),'side_thigh_left.png':(166,335),'side_shin_boot_left.png':(193,358),'side_upper_arm_right.png':(144,266),'side_cape_drape.png':(277,208)}
    w_px, h_px = SIZES[fn]
    w, h = w_px*S/100.0, h_px*S/100.0
    bpy.ops.mesh.primitive_plane_add(size=2, location=(0,0,0))
    ob = bpy.context.object; ob.name = 'Plane_' + name
    # material with image texture + alpha
    mat = bpy.data.materials.new(name='Mat_' + name); mat.use_nodes = True; mat.blend_method = 'BLEND'
    bsdf = mat.node_tree.nodes['Principled BSDF']
    tex = mat.node_tree.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(path)
    mat.node_tree.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
    mat.node_tree.links.new(tex.outputs['Alpha'], bsdf.inputs['Alpha'])
    ob.data.materials.append(mat)
    # desired world matrix: translation centre, rotation rotdeg, scale w/2,h/2 (plane is 2x2)
    D = Matrix.Translation(W(cx,cy,z)) @ Euler((0,0,math.radians(rotdeg))).to_matrix().to_4x4() @ Matrix.Diagonal((w/2.0, h/2.0, 1.0, 1.0))
    tail, Rmat = bone_rest[bone]
    tail_origin = Matrix.Translation(tail) @ Rmat  # Rmat is rotation-only, see bone_rest
    # Blender bone-parent origin is the bone TAIL (verified by test script):
    # basis = tail_origin^-1 * desired, parent_inverse = identity
    ob.parent = arm; ob.parent_type = 'BONE'; ob.parent_bone = bone
    ob.matrix_parent_inverse = Matrix.Identity(4)
    ob.matrix_basis = tail_origin.inverted() @ D
    planes[name] = ob
bpy.context.view_layer.update()
print('REST PLANE WORLDS (should equal desired centres):')
for name, fn, bone, (cx,cy), rotdeg, z in PLANES:
    print(' ', name, tuple(round(v,3) for v in planes[name].matrix_world.translation))
# pose: rotate forearm bones only; hand bones are children, they follow
bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode='POSE')
for bn, ang in POSE_ROT.items():
    pb = arm.pose.bones[bn]; pb.rotation_mode = 'XYZ'; pb.rotation_euler.z = ang
bpy.ops.object.mode_set(mode='OBJECT'); bpy.context.view_layer.update()
print('POSED BONES:')
for bn in ['forearm_near','hand_near','forearm_far','hand_far']:
    pb = arm.pose.bones[bn]
    print(' ', bn, 'head', tuple(round(v,3) for v in pb.head), 'tail', tuple(round(v,3) for v in pb.tail), 'rotZ', round(pb.rotation_euler.z,3))
# wrist gate: forearm tail == hand head (bone space, exact by parenting) and plane edges
def plane_x_range(ob):
    xs = []
    for v in ob.data.vertices:
        xs.append((ob.matrix_world @ v.co).x)
    return min(xs), max(xs)
for near, far in [('forearm_near','fist_near'), ('forearm_far','fist_far')]:
    a = planes[near]; b = planes[far]
    print(' WRIST', near, 'plane X range', [round(v,3) for v in plane_x_range(a)], '->', far, [round(v,3) for v in plane_x_range(b)],
          'overlap_world', round(plane_x_range(a)[1]-plane_x_range(b)[0],3), 'overlap_px', round((plane_x_range(a)[1]-plane_x_range(b)[0])*100,1))
    print('  centres', near, tuple(round(v,3) for v in a.matrix_world.translation), far, tuple(round(v,3) for v in b.matrix_world.translation))
# scene / camera / render
scene = bpy.context.scene; scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 1400; scene.render.resolution_y = 1600
scene.render.image_settings.file_format = 'PNG'
scene.world = bpy.data.worlds.new('GreyWorld'); scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.5,0.5,0.5,1)
bpy.ops.object.camera_add(location=(0,6.65,12), rotation=(0,0,0))
cam = bpy.context.object; cam.data.type = 'ORTHO'; cam.data.ortho_scale = 14.0
scene.camera = cam
out_blend = os.path.join(OUT, 'side-rig-wrist-fix-20261101.blend')
out_png = os.path.join(OUT, 'side-bent-wrist-fix-grey-20261101.png')
scene.render.filepath = out_png
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=out_blend)
print('SAVED', out_blend, out_png)
