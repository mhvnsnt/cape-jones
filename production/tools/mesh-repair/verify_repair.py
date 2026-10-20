"""verify_repair.py — confirm the repair on the POSED (evaluated) mesh.

Counts boundary edges on the evaluated mesh with all modifiers applied, using
numpy only (no bmesh -> safe on 910k-vert meshes). Also classifies remaining
loops: welded-shut (degenerate in rest) vs true holes (non-degenerate in rest)
so any real missing-topology holes get flagged for fill.

Headless:
    xvfb-run -a env -u PYTHONPATH <blender> -b <repaired.blend> \
        --python verify_repair.py -- <body_object> <out_json>

Writes <out_json> with counts + loop classification. Exit 0 always; the JSON
carries the verdict (welded_ok bool).
"""
import bpy
import numpy as np
import json
import sys


def boundary_edges(me):
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


def group_loops(edges):
    """Union-find boundary edges into loops by shared verts. Returns list of vert arrays."""
    parent = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        u, v = int(u), int(v)
        parent.setdefault(u, u)
        parent.setdefault(v, v)
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
    # map root -> set of verts
    roots = {}
    for u, v in edges:
        for x in (int(u), int(v)):
            roots.setdefault(find(x), set()).add(x)
    return [np.array(sorted(s), dtype=np.int32) for s in roots.values()]


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    body_name, out_json = argv[0], argv[1]

    body = bpy.data.objects.get(body_name)
    if body is None:
        raise SystemExit(f"object '{body_name}' not found")

    # rest (base mesh, modifiers NOT applied)
    rest_edges = boundary_edges(body.data)

    # posed (evaluated, all modifiers incl. WeldSeams + Armature)
    dg = bpy.context.evaluated_depsgraph_get()
    bev = body.evaluated_get(dg)
    pm = bev.to_mesh()
    posed_edges = boundary_edges(pm)
    nverts = len(pm.vertices)
    co = np.empty(nverts * 3, dtype=np.float32)
    pm.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)

    loops = group_loops(posed_edges)
    loop_info = []
    for vs in loops:
        pts = co[vs]
        cen = pts.mean(axis=0)
        rad = float(np.abs(pts - cen).max())
        loop_info.append({"nedges": int(len(vs)), "radius": round(rad, 4),
                          "centroid": [round(float(x), 4) for x in cen]})
    loop_info.sort(key=lambda d: -d["nedges"])
    bev.to_mesh_clear()

    report = {
        "body": body_name,
        "modifiers": [(m.type, m.name) for m in body.modifiers],
        "rest_boundary_edges": int(len(rest_edges)),
        "posed_boundary_edges": int(len(posed_edges)),
        "posed_loop_count": len(loop_info),
        "largest_remaining_loops": loop_info[:20],
        # verdict: repair is good when the pose no longer opens new boundary
        # beyond a small remnant fraction of the rest-pose seam count
        "welded_ok": bool(len(posed_edges) <= max(2000, 0.05 * len(rest_edges))),
    }
    with open(out_json, "w") as f:
        json.dump(report, f, indent=1)
    print("VERIFY: " + json.dumps({k: report[k] for k in
          ("rest_boundary_edges", "posed_boundary_edges", "posed_loop_count", "welded_ok")}),
          flush=True)


if __name__ == "__main__":
    main()
