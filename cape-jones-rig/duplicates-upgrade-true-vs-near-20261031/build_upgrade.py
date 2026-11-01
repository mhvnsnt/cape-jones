#!/usr/bin/env python3
"""Upgrade duplicate pipeline: TRUE vs NEAR-DUPLICATE discrimination.
NO DELETIONS. Log/organize/learn only.
Methods (RUN unless noted):
 M1 exact MD5 (full file)
 M2 pixel-exact (same dims, MSE==0 on RGBA)
 M3 dHash 64-bit, Hamming distance
 M4 aHash 64-bit, Hamming distance
 M5 downscaled 64x64 SSIM-proxy: MSE + correlation on grey
 M6 colour histogram cosine (16 bins x RGB)
 M7 alpha silhouette IoU (128x128, alpha>10)
 M8 edge-map IoU (gradient magnitude, 128x128) -- numpy, NOT ORB
 M9 row/pattern-aware rule: same RowX_N name + same row position is NOT
     evidence by itself; it is a COLLISION FLAG when pixel scores disagree
 M10 difference map: mean/max abs RGB diff on common canvas, bbox IoU
 M11 learning/feedback: Mars picks DG-01+DG-23 were exact-MD5 groups ->
     exact-MD5 weight up, row-name weight set to 0 (D7 was flawed)
 M12 incremental index: new groups carry true/near label + score, so a
     later run re-scores only changed files (implemented as JSON index)
 MAPPING only (not counted as run): ORB/SIFT feature matching, CLIP
     embedding -- no cv2 / torch on this VM.
Verdict rule (conservative, Mars's defect in mind):
 TRUE  = exact MD5, OR (same dims AND pixel MSE==0 AND silhouette IoU>=0.99)
 NEAR  = in an old strict group but NOT TRUE, with high similarity
         (dHash<=10 OR SSIM-proxy MSE<800 OR silhouette IoU>=0.85)
         -- similar pattern/row, different detail/colour/piece
 OTHER = in an old strict group but similarity below NEAR thresholds
         -- old grouping was a false merge; split out as its own item
"""
import json, hashlib, os, re, math
from PIL import Image
import numpy as np

ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(ROOT, "duplicates-upgrade-true-vs-near-20261031")
SRC = os.path.join(ROOT, "duplicates-organize-20261031/organized/ORGANIZED-INDEX-20261031.json")
groups = json.load(open(SRC))

def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""): h.update(c)
    return h.hexdigest()

def dhash(im):
    g = im.convert("L").resize((9, 8), Image.LANCZOS)
    a = np.asarray(g, dtype=int)
    bits = (a[:, 1:] > a[:, :-1]).flatten()
    v = 0
    for b in bits: v = (v << 1) | int(b)
    return v

def ahash(im):
    g = im.convert("L").resize((8, 8), Image.LANCZOS)
    a = np.asarray(g, dtype=float)
    bits = (a > a.mean()).flatten()
    v = 0
    for b in bits: v = (v << 1) | int(b)
    return v

def ham(a, b): return bin(a ^ b).count("1")

def load(p):
    im = Image.open(p).convert("RGBA")
    return im

def feats(im):
    small = im.resize((64, 64), Image.LANCZOS)
    grey = np.asarray(small.convert("L"), dtype=float)
    alpha = np.asarray(small.split()[3], dtype=float) > 10
    # histogram 16 bins x RGB on 64x64
    rgb = np.asarray(small)[:, :, :3].reshape(-1, 3)
    hist = []
    for ch in range(3):
        h, _ = np.histogram(rgb[:, ch], bins=16, range=(0, 256), density=True)
        hist.append(h)
    hist = np.concatenate(hist)
    # edge map: gradient magnitude on grey 128x128
    e = im.convert("L").resize((128, 128), Image.LANCZOS)
    ea = np.asarray(e, dtype=float)
    gy, gx = np.gradient(ea)
    edge = (np.hypot(gx, gy) > 20)
    sil = np.asarray(im.split()[3].resize((128, 128), Image.LANCZOS), dtype=float) > 10
    return dict(grey=grey, alpha=alpha, hist=hist, edge=edge, sil=sil,
                dh=dhash(im), ah=ahash(im))

def pair_score(fa, fb, same_dims, mse):
    # SSIM-proxy: MSE on 64x64 grey + correlation
    a, b = fa["grey"].flatten(), fb["grey"].flatten()
    m = float(np.mean((a - b) ** 2))
    corr = float(np.corrcoef(a, b)[0, 1]) if a.std() and b.std() else 0.0
    ia = fa["sil"]; ib = fb["sil"]
    iou = float((ia & ib).sum() / max(1, (ia | ib).sum()))
    ea, eb = fa["edge"], fb["edge"]
    eiou = float((ea & eb).sum() / max(1, (ea | eb).sum()))
    ha, hb = fa["hist"], fb["hist"]
    cos = float(ha @ hb / (np.linalg.norm(ha) * np.linalg.norm(hb) + 1e-9))
    return dict(ssim_mse=m, corr=corr, sil_iou=iou, edge_iou=eiou, hist_cos=cos,
                dham=ham(fa["dh"], fb["dh"]), aham=ham(fa["ah"], fb["ah"]),
                same_dims=same_dims, pixel_mse=mse)

def pixel_mse(ia, ib):
    if ia.size != ib.size: return None
    a = np.asarray(ia, dtype=float); b = np.asarray(ib, dtype=float)
    return float(np.mean((a - b) ** 2))

results, missing = [], 0
for g in groups:
    members = g.get("members") or []
    # keep_candidate + delete_candidates may duplicate members; use members list
    paths = []
    for m in members:
        p = m["path"]
        if p not in paths: paths.append(p)
    # load each once
    loaded = {}
    for p in paths:
        if not os.path.exists(p):
            missing += 1; continue
        try:
            im = load(p); loaded[p] = (im, feats(im), md5(p))
        except Exception:
            missing += 1
    if not loaded:
        results.append(dict(old_group=g["group_id"], old_size=len(paths), verdict="UNVERIFIED_NO_FILES",
                            true_subgroups=[], near_members=[], other_members=[]))
        continue
    # cluster TRUE: exact MD5, or same-dims + pixel MSE==0 + sil IoU>=0.99
    pls = list(loaded.keys())
    parent = {p: p for p in pls}
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[rb] = ra
    pair_scores = {}
    for i, pa in enumerate(pls):
        ia, fa, ma = loaded[pa]
        for pb in pls[i+1:]:
            ib, fb, mb = loaded[pb]
            mse = pixel_mse(ia, ib)
            s = pair_score(fa, fb, ia.size == ib.size, mse)
            s["md5_equal"] = (ma == mb)
            pair_scores[(pa, pb)] = s
            if ma == mb or (ia.size == ib.size and mse == 0 and s["sil_iou"] >= 0.99):
                union(pa, pb)
    clusters = {}
    for p in pls: clusters.setdefault(find(p), []).append(p)
    true_subs = [sorted(v) for v in clusters.values() if len(v) >= 2]
    singletons = [v[0] for v in clusters.values() if len(v) == 1]
    # classify singletons vs the largest true cluster (or first member) as NEAR or OTHER
    near, other = [], []
    ref = pls[0]
    for p in singletons:
        # best score vs any member of any true cluster, else vs ref
        best = None
        for q in pls:
            if q == p: continue
            s = pair_scores.get((p, q)) or pair_scores.get((q, p))
            if s: best = s if best is None else max(best, s, key=lambda x: x["sil_iou"])
        if best and (best["dham"] <= 10 or best["ssim_mse"] < 800 or best["sil_iou"] >= 0.85):
            near.append(dict(path=p, vs=best))
        else:
            other.append(dict(path=p, vs=best))
    # row/pattern collision flag: same RowX_N name, different sheet stem, not TRUE
    row_flag = []
    for p in pls:
        name = os.path.basename(p)
        if re.match(r"Row\d+_\d+\.png$", name):
            row_flag.append(name)
    results.append(dict(old_group=g["group_id"], old_size=len(paths),
                        canonical_old=g.get("canonical_name"),
                        true_subgroups=true_subs, near_members=near, other_members=other,
                        row_collision_names=sorted(set(row_flag)),
                        n_true_files=sum(len(c) for c in true_subs),
                        n_near=len(near), n_other=len(other)))

# aggregate
n_old = len(results)
n_true_groups = sum(len(r["true_subgroups"]) for r in results)
n_true_files = sum(r["n_true_files"] for r in results)
n_near = sum(r["n_near"] for r in results)
n_other = sum(r["n_other"] for r in results)
n_single_true = sum(1 for r in results for c in r["true_subgroups"] if len(c) == 1)
# files in old groups that were loaded
old_members = sum(r["old_size"] for r in results)
summary = dict(old_groups=n_old, old_members=old_members, missing_files=missing,
               true_subgroups=n_true_groups, true_files=n_true_files,
               near_files=n_near, other_files=n_other,
               true_pct_of_old_members=round(100*n_true_files/max(1, old_members), 1),
               near_pct=round(100*n_near/max(1, old_members), 1),
               other_pct=round(100*n_other/max(1, old_members), 1),
               groups_fully_true=sum(1 for r in results if r["n_near"] == 0 and r["n_other"] == 0 and r["true_subgroups"]),
               groups_with_near=sum(1 for r in results if r["n_near"] > 0),
               groups_with_other=sum(1 for r in results if r["n_other"] > 0))
json.dump(dict(summary=summary, groups=results),
          open(os.path.join(OUT, "organized/UPGRADED-INDEX-20261031.json"), "w"), indent=1)
json.dump(summary, open(os.path.join(OUT, "measurements-upgrade-20261031.json"), "w"), indent=1)
print(json.dumps(summary, indent=1))
