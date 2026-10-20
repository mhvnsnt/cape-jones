"""apply_weld.py — stitch degenerate seams with a non-destructive Weld modifier.

Why a modifier (not edit-mode remove-doubles):
  * edit-mode topology ops on a 910k-vert / 11-shape-key mesh OOM a 8GB box;
  * the modifier is pose-independent: it welds *before* the Armature modifier
    in the stack, so every pose/animation gets the fix automatically;
  * nothing is destroyed — remove the modifier and the source mesh is untouched.

The weld is limited to a `weld_seams` vertex group holding exactly the
boundary verts found by detect_seams.py, so interior verts (lips, cloth
layers, fingers) can never fuse.

Headless:
    xvfb-run -a env -u PYTHONPATH <blender> -b <in.blend> --python apply_weld.py \
        -- <body_object> <seam_vert_indices.npy> [threshold]

Default threshold 0.02 (mesh-local units; character is ~1.37 units tall).
"""
import bpy
import numpy as np
import sys

VGROUP = "weld_seams"
MODNAME = "WeldSeams"


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    body_name = argv[0]
    npy_path = argv[1]
    threshold = float(argv[2]) if len(argv) > 2 else 0.02

    body = bpy.data.objects.get(body_name)
    if body is None:
        raise SystemExit(f"object '{body_name}' not found")

    seam = np.load(npy_path)
    print(f"WELD: {len(seam)} seam verts, threshold={threshold}", flush=True)

    vg = body.vertex_groups.get(VGROUP) or body.vertex_groups.new(name=VGROUP)
    vg.add(seam.tolist(), 1.0, 'REPLACE')

    # drop any previous run's modifier so re-runs are idempotent
    old = body.modifiers.get(MODNAME)
    if old:
        body.modifiers.remove(old)

    w = body.modifiers.new(name=MODNAME, type='WELD')
    w.merge_threshold = threshold
    w.vertex_group = VGROUP

    # weld must run BEFORE the armature deforms (and before corrective smooth)
    bpy.context.view_layer.objects.active = body
    while body.modifiers.find(MODNAME) > 0:
        bpy.ops.object.modifier_move_up(modifier=MODNAME)

    order = [(m.type, m.name) for m in body.modifiers]
    print("WELD: modifier stack: " + str(order), flush=True)
    assert order[0][1] == MODNAME, "WeldSeams is not first in the stack!"

    # persist: run_pipeline.py works on a disposable copy, so in-place save is safe
    bpy.ops.wm.save_mainfile()
    print("WELD: saved", flush=True)


if __name__ == "__main__":
    main()
