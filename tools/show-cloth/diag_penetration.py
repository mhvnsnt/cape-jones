#!/usr/bin/env python3
"""Diagnose WHERE the v3 cape penetrates the body at frame 48:
split penetrating verts by pin weight (pinned band vs free cloth)."""
import bpy, json
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

BAKED = "/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_v3_baked.blend"
BASE = "/home/hatch/workspace/scratch/cj-cloth-20261024/cloth_idle_base.blend"
bpy.ops.wm.open_mainfile(filepath=BAKED)
with bpy.data.libraries.load(BASE, link=False) as (df, dt):
    dt.objects = ["CapeJones_Body"] if "CapeJones_Body" in set(df.objects) else []
body = bpy.data.objects.get("CapeJones_Body")
bpy.context.scene.collection.objects.link(body)
cape = bpy.data.objects["CapeJones_Cape"]
sc = bpy.context.scene
sc.frame_set(48)
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()

# pin weights on the BASE mesh (decimate preserves groups approximately;
# use base-mesh vertex indices mapped through evaluated order is unreliable,
# so instead use local z: pin band = local z >= 0.40, ramp 0.36-0.40)
ev = cape.evaluated_get(deps)
me = ev.to_mesh()
arr = np.empty(len(me.vertices) * 3, dtype=np.float64)
me.vertices.foreach_get("co", arr)
mw = np.array(ev.matrix_world, dtype=np.float64)
world = (np.concatenate([arr.reshape(-1, 3), np.ones((len(me.vertices), 1))], axis=1) @ mw.T)[:, :3]
# local coords (before matrix_world) for pin-band classification
local = arr.reshape(-1, 3)
ev.to_mesh_clear()

bt = BVHTree.FromObject(body.evaluated_get(deps), deps)
ds = []
for v in world:
    loc, _, _, d = bt.find_nearest(Vector(v))
    ds.append(d if loc is not None else 999.0)
ds = np.array(ds)
# penetration proxy: verts within 1mm of body surface (nearest distance ~0
# + inside). BVH nearest gives unsigned distance; use overlap faces instead:
ct = BVHTree.FromObject(cape.evaluated_get(deps), deps)
pairs = bt.overlap(ct)
print(f"overlap pairs at frame 48: {len(pairs)}", flush=True)
# which cape faces overlap? collect cape face indices from pairs
from collections import Counter
face_ids = Counter(p[1] for p in pairs)
print(f"cape faces involved: {len(face_ids)}", flush=True)
# map faces -> verts (evaluated mesh polygon vertex indices)
ev2 = cape.evaluated_get(deps)
me2 = ev2.to_mesh()
poly_verts = {}
for pi, p in enumerate(me2.polygons):
    poly_verts[pi] = list(p.vertices)
ev2.to_mesh_clear()
involved = set()
for fi in face_ids:
    involved.update(poly_verts.get(fi, []))
involved = np.array(sorted(involved))
print(f"cape verts in overlapping faces: {len(involved)} / {len(world)}", flush=True)
if len(involved):
    lz = local[involved, 2]
    print(f"their local z: min {lz.min():.3f} max {lz.max():.3f} mean {lz.mean():.3f}", flush=True)
    print(f"pinned band (local z>=0.40): {(lz >= 0.40).sum()}, ramp (0.36-0.40): {((lz >= 0.36) & (lz < 0.40)).sum()}, free (<0.36): {(lz < 0.36).sum()}", flush=True)
    wz = world[involved, 2]
    print(f"their world z: min {wz.min():.3f} max {wz.max():.3f}", flush=True)
print("DIAG_DONE", flush=True)
