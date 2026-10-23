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

Only verts listed in the seam .npy (detect_seams.py output: boundary verts)
are touched.

=== 2026-10-20 CORRUPTION POSTMORTEM (why this file was rewritten) ===
The original version clustered seam verts with a KDTree radius search
(threshold default 0.02 m) and merged clusters TRANSITIVELY (union-find).
On a 910k-vert mesh whose verts sit millimetres apart, radius chaining
walked across whole body regions: tens of thousands of verts collapsed
into single "clusters" and every member received the cluster's averaged
weights — 53,128 verts ended up sharing ONE identical 39-group weight set
(a fingertip could be 9.3% shin bone). Seams measured perfectly shut
(identical weights separate nowhere), so verify_repair.py passed it while
the skinning was destroyed body-wide. The owner caught it by eye in a
posed render (fingertips, face/neck and legs dragging to wrong joints).

Fix (this version):
  * Clustering is EXACT-COINCIDENCE ONLY: verts are grouped by a position
    hash on a 1e-5 m grid. No radius, no chaining, ever. The [threshold]
    CLI argument is retained for call compatibility and IGNORED for
    clustering (a loud warning prints if it exceeds 1e-4).
  * Hard guard: any cluster larger than MAX_CLUSTER verts aborts the run
    (a true coincident seam cluster on this asset is 2-4 verts).
  * No global vertex_group_normalize_all (it rewrote every vert in the
    mesh). Only touched verts are renormalized, per vert.
  * Post-write gates: a touched vert's group count may not grow by more
    than +2 or exceed 16 groups, or the run aborts WITHOUT saving.
Companion gate: verify_repair.py now also runs a weight-plausibility
audit (dominant bone vs nearest bone segment) and fails repaired_ok if
the repaired body is worse than the clean-body baseline (~0.7% flagged).

Measured on the sitting scene with this version: 30,080 coincident
clusters, max size 4, 60,754 seam verts; weight audit 6,369 flagged vs
6,405 on the untouched clean body (the corrupt run scored 57,533).

Headless:
    xvfb-run -a env -u PYTHONPATH <blender> -b <in.blend> --python average_seams.py \
        -- <body_object> <seam_vert_indices.npy> [threshold]

Saves the blend in place (run_pipeline.py works on a disposable copy).
"""
import bpy
import numpy as np
import sys
from collections import defaultdict

GRID = 1e-5          # exact-coincidence position grid (metres)
MAX_CLUSTER = 12     # true seam clusters are 2-4 verts; anything bigger is a bug
MAX_GROUPS = 16      # a touched vert may never exceed this many deform groups
MAX_GROUP_GROWTH = 2


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    body_name = argv[0]
    npy_path = argv[1]
    threshold = float(argv[2]) if len(argv) > 2 else None
    if threshold is not None and threshold > 1e-4:
        print(f"AVERAGE: WARNING threshold={threshold} IGNORED for clustering. "
              "Radius chaining at that scale caused the 2026-10-20 weight "
              "corruption; clustering is exact-coincidence (1e-5 grid) only.",
              flush=True)

    body = bpy.data.objects.get(body_name)
    if body is None:
        raise SystemExit(f"object '{body_name}' not found")
    me = body.data
    nv = len(me.vertices)
    print(f"AVERAGE: {nv} verts", flush=True)

    seam = np.load(npy_path).astype(np.int64)
    print(f"AVERAGE: {len(seam)} seam verts", flush=True)

    co = np.empty(nv * 3, dtype=np.float32)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)

    # ---- cluster: exact-coincidence hash grid over seam verts only ----
    keys = np.round(co[seam] / GRID).astype(np.int64)
    buckets = defaultdict(list)
    for row, vi in zip(keys, seam):
        buckets[(int(row[0]), int(row[1]), int(row[2]))].append(int(vi))
    clusters = [v for v in buckets.values() if len(v) > 1]
    sizes = [len(c) for c in clusters]
    print(f"AVERAGE: {len(clusters)} coincident clusters, "
          f"max size {max(sizes) if sizes else 0}", flush=True)
    if sizes and max(sizes) > MAX_CLUSTER:
        raise SystemExit(
            f"ABORT: cluster of {max(sizes)} verts exceeds MAX_CLUSTER="
            f"{MAX_CLUSTER}. This is the 2026-10-20 chaining failure mode; "
            "refusing to average. Nothing saved.")

    touched = sorted({vi for c in clusters for vi in c})
    print(f"AVERAGE: {len(touched)} seam verts in clusters", flush=True)

    # group counts BEFORE (post-gate baseline)
    before_counts = {vi: len(me.vertices[vi].groups) for vi in touched}

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
    wdata = {}
    for vi in touched:
        v = me.vertices[vi]
        wdata[vi] = [(g.group, g.weight) for g in v.groups if g.weight > 0.0]
    for cl in clusters:
        acc = {}
        for vi in cl:
            for gi, w in wdata[vi]:
                acc[gi] = acc.get(gi, 0.0) + w
        n = len(cl)
        avg = [(gi, tot / n) for gi, tot in acc.items()]
        # per-vert renormalization of the averaged set (sums to ~1 already;
        # this only corrects drift on members whose weights were unnormalized)
        s = sum(w for _gi, w in avg)
        if s > 1e-9:
            avg = [(gi, w / s) for gi, w in avg]
        for vi in cl:
            wdata[vi] = avg
    for vi in touched:
        v = me.vertices[vi]
        for g in list(v.groups):
            body.vertex_groups[g.group].remove([vi])
        for gi, w in wdata[vi]:
            if w > 1e-6:
                body.vertex_groups[gi].add([vi], w, 'REPLACE')
    print("AVERAGE: weights done", flush=True)

    # ---- 3. post-write gates (abort WITHOUT saving on any failure) ----
    worst_growth = 0
    worst_count = 0
    for vi in touched:
        c = len(me.vertices[vi].groups)
        worst_count = max(worst_count, c)
        worst_growth = max(worst_growth, c - before_counts[vi])
    print(f"AVERAGE: post-gate: max groups on a touched vert {worst_count}, "
          f"max growth +{worst_growth}", flush=True)
    if worst_count > MAX_GROUPS or worst_growth > MAX_GROUP_GROWTH:
        raise SystemExit(
            f"ABORT: post-write gate failed (max groups {worst_count} > "
            f"{MAX_GROUPS} or growth +{worst_growth} > +{MAX_GROUP_GROWTH}). "
            "Weights look smeared; refusing to save.")

    bpy.ops.wm.save_mainfile()
    print("AVERAGE: saved", flush=True)


if __name__ == "__main__":
    main()
