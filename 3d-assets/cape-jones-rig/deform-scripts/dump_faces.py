"""Dump polygon faces as tris/quads index arrays for adjacency building."""
import bpy, sys
import numpy as np

out = sys.argv[sys.argv.index("--") + 1]
body = bpy.data.objects['CapeJones_Body']
mesh = body.data
npoly = len(mesh.polygons)
loop_start = np.empty(npoly, dtype=np.int64)
loop_total = np.empty(npoly, dtype=np.int64)
mesh.polygons.foreach_get("loop_start", loop_start)
mesh.polygons.foreach_get("loop_total", loop_total)
nloop = len(mesh.loops)
loop_vert = np.empty(nloop, dtype=np.int32)
mesh.loops.foreach_get("vertex_index", loop_vert)

tris = []
quads = []
ngon = 0
for s, t in zip(loop_start, loop_total):
    vs = loop_vert[s:s + t]
    if t == 3:
        tris.append(vs)
    elif t == 4:
        quads.append(vs)
    else:
        ngon += 1
tris = np.array(tris, dtype=np.int32).reshape(-1, 3)
quads = np.array(quads, dtype=np.int32).reshape(-1, 4)
print(f"polys={npoly} tris={len(tris)} quads={len(quads)} ngons={ngon}", flush=True)
np.savez_compressed(out, tris=tris, quads=quads)
print("SAVED", out, flush=True)
