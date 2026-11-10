"""Render-only pass for the W7b bake-off entry.

The full bakeoff.py W7b run weighted + bound + saved blends/W7b.blend, but was
OOM-killed during the Cycles renders. This script reopens that blend, applies
the W7b pose subset (P2/P3/P5/P7), and renders the proof PNGs.

Run headless:
  xvfb-run -a env -u PYTHONPATH <blender> -b blends/W7b.blend --python tools/weights/cj_bakeoff/render_w7b.py
"""
import os
import sys

sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy  # noqa: E402
from bakeoff import POSES, apply_pose, setup_render, PNG_DIR  # noqa: E402

W7B_POSES = ['P2_arms_raised', 'P3_elbow_90', 'P5_shoulder_raise', 'P7_crouch']


def main():
    rig = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
    print('W7b render-only: rig =', rig.name, flush=True)
    setup_render()
    for p in W7B_POSES:
        apply_pose(rig, POSES[p])
        out = os.path.join(PNG_DIR, 'W7b_%s.png' % p)
        bpy.context.scene.render.filepath = out
        bpy.ops.render.render(write_still=True)
        print('rendered', out, flush=True)
    print('W7b RENDER DONE', flush=True)


main()
