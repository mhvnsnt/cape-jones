#!/usr/bin/env python3
"""Crystal Cape Jones V2 — Transformation #4, chest-emblem origin, 2026-10-31.
Mars, 2026-10-31 20:54 CDT, replying to transformation-3: #3 is SAVED as
Transformation Three (awesome/cool, NOT overwritten, NOT reworked into #4);
#4 starts from the centre of his chest, around his emblem / symbol.

Emblem centre VERIFIED from the actual base plate
(rig-apose-v7c-clean-transparent.png, 1100x1500), NOT guessed, NOT the old
approximate symbiote zone:
- purple connected component in the chest: bbox x539-562, y475-510, 474 px,
  centroid (550.8, 491.1). Origin used: (551, 491).
- Correction, stated plainly: the earlier future-symbiote diamond used
  centre (557, 502) / zone x540-575 y460-545. That was approximate and is
  ~6 px right / ~11 px low versus the measured purple emblem piece. #4 uses
  the measured piece. The old symbiote files are untouched.

Method: same Preset 8 facet system as #2/#3 (Voronoi, spacing 48, seed 7,
308 seed-grid facets, 208 occupied facets with actual pixels). Facets are
revealed by Euclidean distance from the emblem centre + small jitter, so
growth spreads OUTWARD radially from the chest, not feet-up (#1), not
feet-creep (#2), not vein-from-feet (#3). Frontier = last 20 revealed
facets, 60% crystal + 40% base + 25 brighten, plus a cyan (0,200,255) edge
on the frontier boundary, so the live front reads. No spikes, no dust in
#4 — those belong to #3; #4's read is the radial emblem burst.
Start 0% base, end 100% P8-06 glint (V2 default power-on). Base art is never
recoloured: outputs are new files on copies. Grey in GIF/contact is
display-only; frames in frames_t4/ are transparent RGBA.
"""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
from scipy.spatial import cKDTree

ROOT = "/home/hatch/workspace/cape-jones-rig"
SRC = os.path.join(ROOT, "crystallization-preset8-power-20261031")
OUT = os.path.join(ROOT, "crystal-cape-jones-v2-transformation-4-chest-emblem-20261031")
BASE_P = os.path.join(ROOT, "rig-apose-v7c-clean-transparent.png")
CRYSTAL_P = os.path.join(SRC, "P8-06-facet-glint-apose.png")
os.makedirs(os.path.join(OUT, "frames_t4"), exist_ok=True)

ORIGIN = (551, 491)  # measured emblem centroid, rounded (550.8, 491.1)

def facet_ids(mask, spacing=48, seed=7):
    rng = np.random.default_rng(seed)
    H, W = mask.shape
    ys, xs = np.where(mask)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    gx = np.arange(x0, x1+1, spacing); gy = np.arange(y0, y1+1, spacing)
    seeds = []
    for yy in gy:
        for xx in gx:
            seeds.append((xx + rng.uniform(-spacing*0.35, spacing*0.35),
                          yy + rng.uniform(-spacing*0.35, spacing*0.35)))
    seeds = np.array(seeds, float)
    tree = cKDTree(seeds)
    pts = np.column_stack([xs, ys])
    _, idx = tree.query(pts, workers=-1)
    fid = np.full(mask.shape, -1, dtype=np.int32)
    fid[ys, xs] = idx
    return fid, len(seeds)

def facet_stats(mask, fid, nfacets):
    ys, xs = np.where(mask)
    ids = fid[ys, xs]
    stats = []
    for f in range(nfacets):
        sel = ids == f
        if not sel.any():
            stats.append(None); continue
        stats.append(dict(cx=float(xs[sel].mean()), cy=float(ys[sel].mean()),
                          n=int(sel.sum()), ymin=int(ys[sel].min()), ymax=int(ys[sel].max())))
    return stats

def on_grey(im):
    bg = Image.new("RGBA", im.size, (128, 128, 128, 255)); bg.alpha_composite(im); return bg.convert("RGB")

def main():
    base = Image.open(BASE_P).convert("RGBA")
    crystal = Image.open(CRYSTAL_P).convert("RGBA")
    ba = np.asarray(base).astype(float); ca = np.asarray(crystal).astype(float)
    mask = np.asarray(base)[..., 3] > 10
    fid, nfacets = facet_ids(mask, 48, 7)
    stats = facet_stats(mask, fid, nfacets)
    valid = [i for i, s in enumerate(stats) if s is not None]
    print(f"facets valid {len(valid)} of {nfacets}, mask px {int(mask.sum())}")
    assert len(valid) == 208, f"expected 208 occupied facets, got {len(valid)}"

    # Radial order from emblem centre + jitter (jitter breaks perfect rings)
    rng = np.random.default_rng(31)
    scored = []
    for i in valid:
        s = stats[i]
        d = math.hypot(s['cx'] - ORIGIN[0], s['cy'] - ORIGIN[1])
        scored.append((d + rng.uniform(0, 45), i, d))
    scored.sort()
    order = [i for _, i, _ in scored]
    maxd = max(d for _, _, d in scored)
    print(f"emblem origin {ORIGIN}, max facet-centroid distance {maxd:.1f} px")

    nframes = 20
    frames = []
    meas = {}
    for k in range(nframes):
        nrev = int(round((k+1)/nframes * len(order))) if k < nframes-1 else len(order)
        revealed = set(order[:nrev])
        frontier = set(order[max(0, nrev-20):nrev])
        out = ba.copy()
        rev_mask = np.isin(fid, list(revealed)) & mask if revealed else np.zeros_like(mask)
        out[rev_mask] = ca[rev_mask]
        if frontier and k < nframes-1:
            fr_mask = np.isin(fid, list(frontier)) & mask
            out[fr_mask, :3] = np.clip(ca[fr_mask, :3]*0.6 + ba[fr_mask, :3]*0.4 + 25, 0, 255)
            fr_dil = ndimage.binary_dilation(fr_mask, iterations=2)
            edge = fr_dil & mask & ~fr_mask
            out[edge, :3] = np.array([0, 200, 255], float)
        im = Image.fromarray(out.astype(np.uint8), "RGBA")
        im.save(os.path.join(OUT, "frames_t4", f"t4-{k:02d}.png"))
        frames.append(im)
        pct_f = round(100*nrev/len(order), 1)
        pct_p = round(100*rev_mask.sum()/mask.sum(), 1)
        meas[f"frame{k:02d}"] = dict(facets_revealed=nrev, pct_facets=pct_f,
            pixels_revealed=int(rev_mask.sum()), pct_pixels=pct_p)
        if k in (0, 9, 19):
            rev_d = [math.hypot(stats[i]['cx']-ORIGIN[0], stats[i]['cy']-ORIGIN[1]) for i in revealed]
            meas[f"frame{k:02d}"]["revealed_distance_max_px"] = round(max(rev_d), 1) if rev_d else 0.0
            print(f"frame {k}: {nrev}/{len(order)} facets ({pct_f}%), {int(rev_mask.sum())} px ({pct_p}%), max dist {max(rev_d):.1f}")

    grey = [on_grey(f) for f in frames]
    grey[0].save(os.path.join(OUT, "transformation-4-chest-emblem-20261031.gif"),
                 save_all=True, append_images=grey[1:], duration=160, loop=0)

    # Contact: frames 0, 4, 9, 14, 19 + origin diagram (DIAGRAM ONLY, not a frame)
    tiles, labels = [], []
    for k in [0, 4, 9, 14, 19]:
        tiles.append(on_grey(frames[k])); labels.append(f"t4-{k:02d} ({meas[f'frame{k:02d}']['pct_facets']}% facets)")
    # diagram: base on grey + emblem centre cross + distance rings
    diag = on_grey(base).copy(); dd = ImageDraw.Draw(diag)
    ox, oy = ORIGIN
    for r in (100, 250, 400, 550):
        dd.ellipse([ox-r, oy-r, ox+r, oy+r], outline=(0, 200, 255), width=3)
    dd.line([(ox-25, oy), (ox+25, oy)], fill=(255, 255, 0), width=4)
    dd.line([(ox, oy-25), (ox, oy+25)], fill=(255, 255, 0), width=4)
    dd.text((ox+30, oy-12), "EMBLEM (551,491)", fill=(255, 255, 0))
    tiles.append(diag); labels.append("DIAGRAM ONLY: origin + radial rings")
    tw = 275
    resized = []
    for t in tiles:
        h = int(t.size[1]*tw/t.size[0]); resized.append(t.resize((tw, h)))
    cols = 3; rows = math.ceil(len(resized)/cols); th = max(t.size[1] for t in resized)
    sheet = Image.new("RGB", (cols*tw, rows*(th+18)), (200, 200, 200)); d2 = ImageDraw.Draw(sheet)
    for i, t in enumerate(resized):
        x, y = (i % cols)*tw, (i // cols)*(th+18)
        sheet.paste(t, (x, y)); d2.text((x+4, y+th+2), labels[i], fill=(0, 0, 0))
    sheet.save(os.path.join(OUT, "transformation-4-contact-20261031.png"))

    out_meas = {
        "transformation_4": {
            "status": "Crystal Form V2 transformation, NOT V1, NOT canon story effects, approval 0/1",
            "transformation_3_status": "SAVED as Transformation Three, awesome/cool, NOT overwritten, NOT reworked into #4",
            "origin": "chest emblem centre, VERIFIED from base plate",
            "origin_xy": list(ORIGIN),
            "origin_measured": "purple connected component bbox x539-562 y475-510, 474 px, centroid (550.8, 491.1)",
            "origin_correction": "earlier future-symbiote diamond centre (557, 502) / zone x540-575 y460-545 was approximate, ~6 px right / ~11 px low vs measured piece; #4 uses measured (551, 491); old symbiote files untouched",
            "growth": "facets sorted by Euclidean distance from emblem centre + jitter (0-45 px), frontier 20 facets 60% crystal + 40% base + 25 brighten + cyan (0,200,255) edge; no spikes, no dust (those belong to #3)",
            "frames": nframes, "duration_ms": 160, "duration_s": 3.2,
            "facets_total": len(order), "seed_grid_facets": nfacets,
            "facet_system": "Preset 8 Voronoi, spacing 48, seed 7, same as #2/#3",
            "end_state": "100% P8-06 glint, V2 default power-on",
            "palette": "cyan (42,126,207) / pink (213,123,206) / centre (128,136,219); vivid boost (0,200,255)/(255,110,210)/(140,120,255) NOT used in #4 frames (P8-06 file as-is)",
            "frame00_0pct": meas["frame00"],
            "frame09_50pct": meas["frame09"],
            "frame19_100pct": meas["frame19"],
            "all_frames": meas,
            "base_plate": "rig-apose-v7c-clean-transparent.png, mask 373846 px, base never recoloured",
        }
    }
    json.dump(out_meas, open(os.path.join(OUT, "measurements-20261031.json"), "w"), indent=2)
    print(json.dumps(out_meas["transformation_4"], indent=2)[:2000])

if __name__ == "__main__":
    main()
