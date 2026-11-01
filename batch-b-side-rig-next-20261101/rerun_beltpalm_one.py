"""Render ONE belt or palm trial variant (single-render process).
Usage: blender -b --python rerun_beltpalm_one.py -- <tag>
tag: belt0 | belt1 | belt2 | palm0 | palm1 | palm2 | palm3
belt0=fused control, belt1=split layer, belt2=Row7 overlay;
palm0=fused, palm1=Row5_15 ArmFront, palm2=Hand_10 ArmFront,
palm3=Row5_15 ArmFront + Hand_10 ArmBack. 50% / 32 samples.
"""
import bpy, os, sys
sys.path.insert(0, os.path.expanduser('~/workspace/cape-jones-rig/batch-b-side-rig-next-20261101'))
import build_batch_b as B

tag = sys.argv[sys.argv.index('--') + 1]
if tag.startswith('belt'):
    belt = {'belt0': None, 'belt1': 'split', 'belt2': 'row7'}[tag]
    arm, rest, planes = B.build_back(belt=belt)
    out = os.path.join(B.OUT, 'belt-trial-%s-20261101.png' % tag[-1])
elif tag.startswith('palm'):
    palm = {'palm0': None, 'palm1': ('row5', 'ArmFront'),
            'palm2': ('hand10', 'ArmFront'), 'palm3': 'both'}[tag]
    arm, rest, planes = B.build_back(palm=palm)
    out = os.path.join(B.OUT, 'palm-trial-%s-20261101.png' % tag[-1])
scene = B.setup_scene(6.88, pct=50)
scene.eevee.taa_render_samples = 32
B.render_to(scene, out)
print('DONE', tag, out)
