"""Render ONE knee-pivot trial option (A, B, or C) at 0/30/60 deg.
Usage: blender -b --python rerun_knee_opt.py -- <A|B|C>
Leg-only rig, back-pack thigh/shin pieces, saved-pivot gaps imposed:
L (-70,+13) = 71.2 px, R (-74,-12) = 75.0 px (RIG-06 reported).
Option B moves shin bone heads to K in EDIT mode (TRIAL ONLY geometry,
never saved as a .blend). Option C re-anchors shin planes at rest so
their top-centres sit under K, pivots kept. Renders at 50% / 32 samples.
"""
import bpy, math, os, sys
sys.path.insert(0, os.path.expanduser('~/workspace/cape-jones-rig/batch-b-side-rig-next-20261101'))
import build_batch_b as B
from mathutils import Vector

opt = sys.argv[sys.argv.index('--') + 1]
B.clear()
def W2(px, py):
    return Vector(((px - 700) / 100.0, (1540 - py) / 100.0, 0))
bones = []
for side, tx, off in [('L', 560, (-70, 13)), ('R', 840, (-74, -12))]:
    kx, ky = tx, 1230
    px, py = kx + off[0], ky + off[1]
    bones.append(('thigh_' + side, W2(tx, 940), W2(tx, 1230), None))
    bones.append(('shin_' + side, W2(px, py), W2(px, py + 310), 'thigh_' + side))
arm = B.make_armature('KneeTrialArmature_BatchB', bones)
rest = B.bone_rest_frames(arm, bones)
scene = B.setup_scene(6.88, pct=50)
scene.eevee.taa_render_samples = 32
planes = {}
for side, tx, off in [('L', 560, (-70, 13)), ('R', 840, (-74, -12))]:
    fn_t = 'back_thigh_left.png' if side == 'L' else 'back_thigh_right.png'
    fn_s = 'back_shin_boot_left.png' if side == 'L' else 'back_shin_boot_right.png'
    planes['thigh_' + side] = B.add_plane_world(arm, rest, 'thigh_' + side,
        'thigh_' + side, os.path.join(B.BACK_BASE, fn_t),
        116 * B.SB / 100.0, 242 * B.SB / 100.0, W2(tx, 1085), 0, 0.0)
    cx = tx if opt == 'C' else tx + off[0]
    planes['shin_' + side] = B.add_plane_world(arm, rest, 'shin_' + side,
        'shin_' + side, os.path.join(B.BACK_BASE, fn_s),
        114 * B.SB / 100.0, 301 * B.SB / 100.0, W2(cx, 1360), 0, 0.10)
bpy.context.view_layer.update()
if opt == 'B':
    bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode='EDIT')
    for side, tx in [('L', 560), ('R', 840)]:
        eb = arm.data.edit_bones['shin_' + side]
        dx = W2(tx, 1230) - eb.head
        eb.head += dx; eb.tail += dx
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.update()
for ang in [0, 30, 60]:
    bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode='POSE')
    for bn in ['shin_L', 'shin_R']:
        pb = arm.pose.bones[bn]; pb.rotation_mode = 'XYZ'; pb.rotation_euler.z = 0
    bpy.ops.object.mode_set(mode='OBJECT')
    if ang:
        B.pose_bone(arm, 'shin_L', rotz=math.radians(ang))
        B.pose_bone(arm, 'shin_R', rotz=math.radians(ang))
    for side, tx in [('L', 560), ('R', 840)]:
        ob = planes['shin_' + side]
        top = sorted([(ob.matrix_world @ v.co) for v in ob.data.vertices], key=lambda p: -p.y)[:2]
        tm = sum(top, Vector((0, 0, 0))) / 2
        K = W2(tx, 1230)
        print(' KNEE opt', opt, 'ang', ang, 'leg', side,
              'shin-top-mid', tuple(round(v, 3) for v in tm),
              'dist_px', round((tm - K).length * 100, 1))
    B.render_to(scene, os.path.join(B.OUT, 'knee-trial-%s-%02d-20261101.png' % (opt, ang)))
print('DONE knee', opt)
