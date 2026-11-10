"""detect_seams.py — find degenerate (unwelded) seam boundaries on a mesh.

Root cause it detects: Tripo-assembled character meshes ship as hundreds of
open shells whose part boundaries are *coincident but never merged*. In rest
pose the seams are invisible; under armature deformation the coincident verts
carry different bone weights and tear apart -> the "holes everywhere" look.

Runs headless inside Blender (needs bpy + numpy only, no bmesh -> low memory):

    xvfb-run -a env -u PYTHONPATH <blender> -b <in.blend> --python detect_seams.py \
        -- <body_object> <out_dir>

Writes <out_dir>/seam_vert_indices.npy and <out_dir>/seam_stats.json
"""
import bpy
import numpy as np
import json
import os
import sys


def boundary_edges(me):
    """Return (2, E) int32 array of boundary edge endpoint vert indices (numpy only)."""
    nv = len(me.vertices)
    nl = len(me.loops)
    nply = len(me.polygons)
    loop_vert = np.empty(nl, dtype=np.int32)
    me.loops.foreach_get("vertex_index", loop_vert)
    lstart = np.empty(nply, dtype=np.int32)
    ltot = np.empty(nply, dtype=np.int32)
    me.polygons.foreach_get("loop_start", lstart)
    me.polygons.foreach_get("loop_total", ltot)
    poly_of_loop = np.repeat(np.arange(nply, dtype=np.int32), ltot)
    s = lstart[poly_of_loop]
    t = ltot[poly_of_loop]
    rel = np.arange(nl, dtype=np.int32) - s
    nxt = s + (rel + 1) % t
    a = loop_vert
    b = loop_vert[nxt]
    lo = np.minimum(a, b).astype(np.int64)
    hi = np.maximum(a, b).astype(np.int64)
    key = lo * np.int64(nv) + hi
    uniq, counts = np.unique(key, return_counts=True)
    bnd = uniq[counts == 1]
    e0 = (bnd // nv).astype(np.int32)
    e1 = (bnd % nv).astype(np.int32)
    return np.stack([e0, e1], axis=1)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    body_name, out_dir = argv[0], argv[1]
    os.makedirs(out_dir, exist_ok=True)

    body = bpy.data.objects.get(body_name)
    if body is None:
        raise SystemExit(f"object '{body_name}' not found")

    me = body.data
    edges = boundary_edges(me)
    seam_verts = np.unique(edges.ravel()) if len(edges) else np.empty(0, dtype=np.int32)

    np.save(os.path.join(out_dir, "seam_vert_indices.npy"), seam_verts)
    stats = {
        "body": body_name,
        "total_verts": len(me.vertices),
        "boundary_edges": int(len(edges)),
        "seam_verts": int(len(seam_verts)),
        "seam_fraction": round(float(len(seam_verts)) / max(1, len(me.vertices)), 4),
    }
    with open(os.path.join(out_dir, "seam_stats.json"), "w") as f:
        json.dump(stats, f, indent=1)
    print("SEAM DETECT: " + json.dumps(stats), flush=True)


if __name__ == "__main__":
    main()
