"""average_seams.py — close unwelded seams WITHOUT topology changes.

Why not a Weld modifier: merging verts changes the vert count (910374 ->
849146), which permanently disables the CorrectiveSmooth modifier (it needs
the original mesh for reference) and breaks PR #158's deform stack.

Instead, this makes coincident seam verts deform IDENTICALLY:
  * average deform weights across each coincident cluster, then normalize
  * average shape-key positions across each cluster (so correctives can't
    pry the seam open either)

Identical rest position + identical weights + identical shape offsets =
identical deformed position. The seam stays shut (degenerate, invisible)
through every pose, with zero topology change. CorrectiveSmooth, shape keys,
UVs and vertex groups are all preserved.

Only BOUNDARY-BOUNDARY coincident pairs are averaged (clothing-over-skin
contacts, where a seam vert meets an interior vert, are left alone).

Headless:
    xvfb-run -a env -u PYTHONPATH <blender> -b <in.blend> --python average_seams.py \
        -- <body_object> <seam_vert_indices.npy> [threshold]

Saves the blend in place (run_pipeline.py works on a disposable copy).
"""
import bpy
import numpy as np
import sys
from mathutils.kdtree import KDTree


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    body_name = argv[0]
    npy_path = argv[1]
    threshold = float(argv[2]) if len(argv) > 2 else 0.02

    body = bpy.data.objects.get(body_name)
    if body is None:
        raise SystemExit(f"object '{body_name}' not found")
    me = body.data
    nv = len(me.vertices)
    print(f"AVERAGE: {nv} verts, threshold={threshold}", flush=True)

    seam = np.load(npy_path).astype(np.int32)
    print(f"AVERAGE: {len(seam)} seam verts", flush=True)

    # positions of seam verts
    co = np.empty(nv * 3, dtype=np.float32)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)

    # KDTree over seam verts only; cluster coincident pairs
    kd = KDTree(len(seam))
    for i, vi in enumerate(seam):
        kd.insert(co[int(vi)], int(i))
    kd.balance()
    parent = list(range(len(seam)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, vi in enumerate(seam):
        for (_c, j, d) in kd.find_range(co[int(vi)], threshold):
            if j <= i:
                continue
            ri, rj = find(i), find(int(j))
            if ri != rj:
                parent[ri] = rj
    clusters = {}
    for i, vi in enumerate(seam):
        r = find(i)
        clusters.setdefault(r, []).append(int(vi))
    clusters = [v for v in clusters.values() if len(v) > 1]
    print(f"AVERAGE: {len(clusters)} coincident clusters", flush=True)

    # ---- 1. average shape-key positions per cluster ----
    if me.shape_keys:
        for kb in me.shape_keys.key_blocks:
            kco = np.empty(nv * 3, dtype=np.float32)
            kb.data.foreach_get("co", kco)
            kco = kco.reshape(-1, 3)
            for cl in clusters:
                kco[cl] = kco[cl].mean(axis=0)
            kb.data.foreach_set("co", kco.ravel())
            del kco
        print(f"AVERAGE: shape keys done ({len(me.shape_keys.key_blocks)} keys)", flush=True)

    # ---- 2. average deform weights per cluster ----
    # read all weights once (Python loop, seam verts only)
    wdata = {}
    for vi in seam:
        v = me.vertices[int(vi)]
        wdata[int(vi)] = [(g.group, g.weight) for g in v.groups]
    for cl in clusters:
        acc = {}
        for vi in cl:
            for gi, w in wdata[vi]:
                acc[gi] = acc.get(gi, 0.0) + w
        n = len(cl)
        avg = [(gi, tot / n) for gi, tot in acc.items()]
        for vi in cl:
            wdata[vi] = avg
    # write back: clear + add per vert (seam verts only)
    for vi in seam:
        vi = int(vi)
        v = me.vertices[vi]
        # remove existing
        for g in list(v.groups):
            body.vertex_groups[g.group].remove([vi])
        for gi, w in wdata[vi]:
            if w > 1e-6:
                body.vertex_groups[gi].add([vi], w, 'REPLACE')
    print("AVERAGE: weights done", flush=True)

    # ---- 3. normalize ----
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.vertex_group_normalize_all(group_select_mode='ALL', lock_active=False)
    print("AVERAGE: normalized", flush=True)

    bpy.ops.wm.save_mainfile()
    print("AVERAGE: saved", flush=True)


if __name__ == "__main__":
    main()
