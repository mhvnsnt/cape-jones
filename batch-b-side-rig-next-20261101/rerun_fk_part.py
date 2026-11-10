"""Render a subset of side FK frames + optionally save the side .blend
and the side belt trial. Usage:
  blender -b --python rerun_fk_part.py -- <part>
part: fk1 (frames 1,7,13) | fk2 (19,25,31) | fk3 (37,43,49 + save + belt)
Each part rebuilds the side rig + FK keys identically, so frames are
consistent across processes. Frames at 50% / 32 samples.
"""
import bpy, math, os, sys
sys.path.insert(0, os.path.expanduser('~/workspace/cape-jones-rig/batch-b-side-rig-next-20261101'))
import build_batch_b as B

part = sys.argv[sys.argv.index('--') + 1]
arm, rest, planes = B.build_side()
scene = B.setup_scene(6.65, pct=50)
scene.eevee.taa_render_samples = 32
bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode='POSE')
for bn in ['forearm_near', 'forearm_far']:
    arm.pose.bones[bn].rotation_mode = 'XYZ'
for fr, ang in [(1, 0.0), (13, math.pi / 4), (25, math.pi / 2), (37, math.pi / 4), (49, 0.0)]:
    bpy.context.scene.frame_set(fr)
    for bn in ['forearm_near', 'forearm_far']:
        arm.pose.bones[bn].rotation_euler.z = ang
        arm.pose.bones[bn].keyframe_insert(data_path='rotation_euler', frame=fr)
bpy.ops.object.mode_set(mode='OBJECT')
os.makedirs(os.path.join(B.OUT, 'frames-fk'), exist_ok=True)
frames = {'fk1': [1, 7, 13], 'fk2': [19, 25, 31], 'fk3': [37, 43, 49]}[part]
for fr in frames:
    bpy.context.scene.frame_set(fr)
    B.render_to(scene, os.path.join(B.OUT, 'frames-fk', 'fk-%02d-20261101.png' % fr))
if part == 'fk3':
    # bent-pose wrist gate (frame 25 equivalent: set 25, measure, restore)
    bpy.context.scene.frame_set(25)
    bpy.context.view_layer.update()
    def wrist_world(ob):
        return ob.matrix_world @ B.Vector((-0.587, -0.818, 0))
    for f, op in [('forearm_near', 'open_near'), ('forearm_far', 'open_far')]:
        fb = arm.pose.bones[f]; wp = wrist_world(planes[op])
        print(' WRISTOPEN', f, 'tail', tuple(round(v, 3) for v in fb.tail),
              'hand wrist pt', tuple(round(v, 3) for v in wp),
              'dist', round((fb.tail - wp).length, 4))
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(B.OUT, 'side-rig-batch-b-open-hand-20261101.blend'))
    print('SAVED side .blend')
    arm2, rest2, planes2 = B.build_side(extra_belt=True)
    scene2 = B.setup_scene(6.65, pct=50)
    scene2.eevee.taa_render_samples = 32
    B.render_to(scene2, os.path.join(B.OUT, 'side-belt-row7-trial-20261101.png'))
    print('SAVED side belt trial render')
print('DONE', part)
