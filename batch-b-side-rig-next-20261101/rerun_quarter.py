"""3/4-back skeleton-overlay trial (single process, two renders).
Whole-figure plane only — NO piece cuts (Mars Q4 decision pending).
Rest at 100% / 64 samples, pose attempt at 50% / 32 samples.
"""
import bpy, math, os, sys
sys.path.insert(0, os.path.expanduser('~/workspace/cape-jones-rig/batch-b-side-rig-next-20261101'))
import build_batch_b as B
from mathutils import Matrix, Vector

B.clear()
def WQ(px, py):
    return Vector(((px - 700) / 100.0, (1540 - py) / 100.0, 0))
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
arm = B.make_armature('QuarterBackArmature_Trial', bb)
rest = B.bone_rest_frames(arm, bb)
sheet = os.path.join(B.CJ, 'sliced-clean-20261031', 'B-model', 'model-sheet-3quarter-back-set2', 'Row1_1.png')
plane = B.add_plane_world(arm, rest, 'chest', 'quarter_figure', sheet,
    619 * 1.40 / 100.0, 996 * 1.40 / 100.0, WQ(700, 780), 0, 0.0)
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
scene = B.setup_scene(6.88)
B.render_to(scene, os.path.join(B.OUT, 'quarter-back-trial-20261101.png'))
B.pose_bone(arm, 'thigh_R', rotz=math.radians(30))
B.pose_bone(arm, 'forearm_R', rotz=math.radians(30))
scene.render.resolution_percentage = 50
scene.eevee.taa_render_samples = 32
B.render_to(scene, os.path.join(B.OUT, 'quarter-back-pose-attempt-20261101.png'))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(B.OUT, 'quarter-back-trial-20261101.blend'))
print('SAVED quarter-back trial')
