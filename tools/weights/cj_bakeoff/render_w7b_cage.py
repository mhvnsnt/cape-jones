"""Cage-level pose verification for the W7b bake-off entry.

The full 991,082-vert mesh with the 731-vert mesh-deform cage OOMs this 8GB VM
during depsgraph sync (2 attempts, exit 137, 5.47GB Blender peak; A/B with the
deform modifier disabled renders fine). This script verifies the mechanism one
level down: it hides the heavy mesh, shows the cage, poses the rig, and renders
the DEFORMED CAGE. If the cage tracks the armature cleanly through the poses,
the technique is sound and only RAM blocks the full-mesh proof.

Also prints a numeric bend check: angle between the arm-cage sections at P3.

Run headless:
  xvfb-run -a env -u PYTHONPATH <blender> -b blends/W7b.blend --python tools/weights/cj_bakeoff/render_w7b_cage.py
"""
import math
import os
import sys

sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
from bakeoff import POSES, apply_pose, setup_render, PNG_DIR  # noqa: E402

W7B_POSES = ['P2_arms_raised', 'P3_elbow_90', 'P5_shoulder_raise', 'P7_crouch']


def main():
    rig = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
    cage = next(o for o in bpy.data.objects if 'Cage' in o.name)
    big = next(o for o in bpy.data.objects
               if o.type == 'MESH' and len(o.data.vertices) > 100000)
    big.hide_render = True
    big.hide_viewport = True
    cage.hide_render = False
    cage.hide_viewport = False
    print('cage verts: %d' % len(cage.data.vertices), flush=True)

    setup_render()
    dg = bpy.context.evaluated_depsgraph_get()
    for p in W7B_POSES:
        apply_pose(rig, POSES[p])
        bpy.context.view_layer.update()
        out = os.path.join(PNG_DIR, 'W7b_cage_%s.png' % p)
        bpy.context.scene.render.filepath = out
        bpy.ops.render.render(write_still=True)
        print('rendered', out, flush=True)

    # numeric bend check at P3: upper-arm cage section vs forearm cage section
    apply_pose(rig, POSES['P3_elbow_90'])
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    cage_eval = cage.evaluated_get(dg)
    verts = [cage_eval.matrix_world @ v.co for v in cage_eval.data.vertices]
    # split cage verts by side (x sign in armature space ~ world here)
    left = [v for v in verts if v.x < -0.05]
    upper = [v for v in left if -0.05 < v.y < 0.30]
    fore = [v for v in left if v.y >= 0.30]
    def centroid(vs):
        c = Vector((0, 0, 0))
        for v in vs:
            c += v
        return c / len(vs)
    cu, cf = centroid(upper), centroid(fore)
    elbow = Vector(rig.pose.bones['ForeArm.L'].head)
    a = (cu - elbow).normalized()
    b = (cf - elbow).normalized()
    ang = math.degrees(math.acos(max(-1.0, min(1.0, a.dot(b)))))
    print('P3 cage bend angle (upper->fore around elbow): %.1f deg '
          '(rest=180, perfect 90-bend=90)' % ang, flush=True)
    print('W7b CAGE CHECK DONE', flush=True)


main()
