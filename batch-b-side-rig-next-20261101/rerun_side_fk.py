"""Rerun ONLY the side FK chain + .blend save + side belt trial, after the
first side run was OOM-killed during FK frame 1 (rest + bent renders had
already saved and are NOT re-rendered). FK frames at 50% (700x800) and
EEVEE samples 32 to fit the 8 GB VM alongside other agents' jobs.
Run alone (no concurrent Blender) to avoid a second OOM kill.
"""
import bpy, math, os, sys
sys.path.insert(0, os.path.expanduser('~/workspace/cape-jones-rig/batch-b-side-rig-next-20261101'))
import build_batch_b as B

OUT = B.OUT
arm, rest, planes = B.build_side()
scene = B.setup_scene(6.65, pct=50)
scene.eevee.taa_render_samples = 32
# bent pose for the gate print (then keys take over)
B.pose_bone(arm, 'forearm_near', rotz=math.pi / 2)
B.pose_bone(arm, 'forearm_far', rotz=math.pi / 2)
B.pose_bones_report(arm, ['forearm_near', 'hand_near', 'forearm_far', 'hand_far'])
def wrist_world(ob):
    return ob.matrix_world @ B.Vector((-0.587, -0.818, 0))
for f, op in [('forearm_near', 'open_near'), ('forearm_far', 'open_far')]:
    fb = arm.pose.bones[f]; wp = wrist_world(planes[op])
    print(' WRISTOPEN', f, 'tail', tuple(round(v, 3) for v in fb.tail),
          'hand wrist pt', tuple(round(v, 3) for v in wp),
          'dist', round((fb.tail - wp).length, 4))
# FK keys rest -> bent -> rest
bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode='POSE')
for bn in ['forearm_near', 'forearm_far']:
    arm.pose.bones[bn].rotation_mode = 'XYZ'
for fr, ang in [(1, 0.0), (13, math.pi / 4), (25, math.pi / 2), (37, math.pi / 4), (49, 0.0)]:
    bpy.context.scene.frame_set(fr)
    for bn in ['forearm_near', 'forearm_far']:
        arm.pose.bones[bn].rotation_euler.z = ang
        arm.pose.bones[bn].keyframe_insert(data_path='rotation_euler', frame=fr)
bpy.ops.object.mode_set(mode='OBJECT')
os.makedirs(os.path.join(OUT, 'frames-fk'), exist_ok=True)
for fr in [1, 7, 13, 19, 25, 31, 37, 43, 49]:
    bpy.context.scene.frame_set(fr)
    B.render_to(scene, os.path.join(OUT, 'frames-fk', 'fk-%02d-20261101.png' % fr))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'side-rig-batch-b-open-hand-20261101.blend'))
print('SAVED side .blend')
# side belt trial (Row7_10 overlay), 50% like the other trials
arm2, rest2, planes2 = B.build_side(extra_belt=True)
scene2 = B.setup_scene(6.65, pct=50)
scene2.eevee.taa_render_samples = 32
B.render_to(scene2, os.path.join(OUT, 'side-belt-row7-trial-20261101.png'))
print('SAVED side belt trial render')
