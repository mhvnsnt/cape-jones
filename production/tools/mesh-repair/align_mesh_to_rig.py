"""align_mesh_to_rig.py — fix mesh/armature object transform mismatch.

Root cause: the sitting placement moved ONLY the rig object, leaving the body
mesh object at identity. The Armature modifier then deforms the mesh in the
wrong space (it assumes mesh space == armature rest space), displacing ~182k
verts by up to 14 units. The skeleton itself is correct (pelvis lands on the
chair); only the mesh object transform is stale.

Fix: copy the rig's world transform onto the body object. This does NOT move
the character's intended placement — it restores it: with mesh space ==
armature space, the deform puts the posed character exactly where the
placement put the skeleton (pelvis on the chair).

Headless:
    xvfb-run -a env -u PYTHONPATH <blender> -b <in.blend> --python align_mesh_to_rig.py \
        -- <body_object> <rig_object>

Idempotent: re-running sets the same transform. Saves the blend in place
(run_pipeline.py operates on a disposable copy).
"""
import bpy
import sys


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    body_name, rig_name = argv[0], argv[1]

    body = bpy.data.objects.get(body_name)
    rig = bpy.data.objects.get(rig_name)
    if body is None:
        raise SystemExit(f"object '{body_name}' not found")
    if rig is None:
        raise SystemExit(f"object '{rig_name}' not found")

    before = [round(x, 4) for x in body.matrix_world.translation]
    # copy world transform (location + rotation + scale)
    body.matrix_world = rig.matrix_world.copy()
    bpy.context.view_layer.update()
    after = [round(x, 4) for x in body.matrix_world.translation]
    print(f"ALIGN: {body_name} world loc {before} -> {after} "
          f"(rig {rig_name} at {[round(x,4) for x in rig.matrix_world.translation]})",
          flush=True)
    bpy.ops.wm.save_mainfile()
    print("ALIGN: saved", flush=True)


if __name__ == "__main__":
    main()
