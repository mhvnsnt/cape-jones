"""Rerun ONLY the back v2 sitting trials (the back v2 run was OOM-killed
during S-A; standing + .blend already saved and are NOT re-rendered).
Trials only, no decision. Run alone (no concurrent Blender).
"""
import bpy, math, os, sys
sys.path.insert(0, os.path.expanduser('~/workspace/cape-jones-rig/batch-b-side-rig-next-20261101'))
import build_batch_b as B

OUT = B.OUT
# S-A v2 already saved (back-sitting-trial-v2-A-splay-20261101.png);
# skipped here so this rerun only renders S-B and S-C.
# S-B rotX foreshorten sit
arm, rest, planes = B.build_back()
scene = B.setup_scene(6.88, pct=50)
scene.eevee.taa_render_samples = 32
B.pose_bone(arm, 'thigh_ArmBack', rotx=math.radians(70))
B.pose_bone(arm, 'shin_ArmBack', rotx=math.radians(-70))
B.pose_bone(arm, 'thigh_ArmFront', rotx=math.radians(70))
B.pose_bone(arm, 'shin_ArmFront', rotx=math.radians(-70))
B.render_to(scene, os.path.join(OUT, 'back-sitting-trial-v2-B-foreshorten-20261101.png'))
# S-C S-B + hip drop (feet at ground)
arm, rest, planes = B.build_back()
scene = B.setup_scene(6.88, pct=50)
scene.eevee.taa_render_samples = 32
B.pose_bone(arm, 'thigh_ArmBack', rotx=math.radians(70))
B.pose_bone(arm, 'shin_ArmBack', rotx=math.radians(-70))
B.pose_bone(arm, 'thigh_ArmFront', rotx=math.radians(70))
B.pose_bone(arm, 'shin_ArmFront', rotx=math.radians(-70))
arm.location.y -= 1.91
bpy.context.view_layer.update()
B.render_to(scene, os.path.join(OUT, 'back-sitting-trial-v2-C-drop-20261101.png'))
print('SAVED sitting v2 trials')
