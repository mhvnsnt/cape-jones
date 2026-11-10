#!/usr/bin/env python3
"""Slim a cloth setup blend for baking: strip the heavy body mesh (not a
collider), purge orphans, save a small blend. The bake then runs from the
slim blend so the 1.6M-vert body never sits in memory during the solve.

Usage: blender -b --python slim_scene.py -- <src.blend> <out.blend>
"""
import bpy, sys

a = sys.argv[sys.argv.index("--") + 1:]
SRC, OUT = a[0], a[1]
bpy.ops.wm.open_mainfile(filepath=SRC)
for name in ("CapeJones_Body", "Cube", "Icosphere"):
    o = bpy.data.objects.get(name)
    if o:
        me = o.data if o.type == "MESH" else None
        bpy.data.objects.remove(o, do_unlink=True)
        if me and me.users == 0:
            bpy.data.meshes.remove(me)
# purge orphan data blocks (frees the body mesh from memory accounting)
for _ in range(3):
    try:
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
    except Exception as e:
        print("purge note:", e)
        break
print("slim objects:", sorted(o.name for o in bpy.data.objects), flush=True)
print("slim meshes:", [(m.name, len(m.vertices)) for m in bpy.data.meshes], flush=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED SLIM", OUT, flush=True)
