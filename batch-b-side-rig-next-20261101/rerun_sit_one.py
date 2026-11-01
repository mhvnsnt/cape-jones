"""Render ONE sitting trial (S-B or S-C) on the back v2 rig.
Usage: blender -b --python rerun_sit_one.py -- <B|C>
Single-render invocations survive the VM's OOM pressure better than
multi-render processes while the episode lane is encoding.
"""
import bpy, math, os, sys
sys.path.insert(0, os.path.expanduser('~/workspace/cape-jones-rig/batch-b-side-rig-next-20261101'))
import build_batch_b as B
tag = sys.argv[sys.argv.index('--') + 1]
arm, rest, planes = B.build_back()
scene = B.setup_scene(6.88, pct=50)
scene.eevee.taa_render_samples = 32
B.pose_bone(arm, 'thigh_ArmBack', rotx=math.radians(70))
B.pose_bone(arm, 'shin_ArmBack', rotx=math.radians(-70))
B.pose_bone(arm, 'thigh_ArmFront', rotx=math.radians(70))
B.pose_bone(arm, 'shin_ArmFront', rotx=math.radians(-70))
if tag == 'C':
    arm.location.y -= 1.91
    bpy.context.view_layer.update()
B.render_to(scene, os.path.join(B.OUT, 'back-sitting-trial-v2-%s-%s-20261101.png' % (tag, 'foreshorten' if tag == 'B' else 'drop')))
print('SAVED sitting', tag)
