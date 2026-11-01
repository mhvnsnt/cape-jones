#!/usr/bin/env python3
"""Crystal Cape Jones V2 transformation upgrades, 2026-10-31.
V1 = earlier Crystal Cape Jones (already made, per Mars 2026-10-31 20:30 CDT).
V2 = Preset 8 set (crystallization-preset8-power-20261031/), P8-06 glint = default power-on.
Transformation #1 = existing feet-up sweep, 6 frames, 0-100%, a horizontal band
  (that is why Mars said it reads like an edit / crop edit).
Transformation #2 = facet-by-facet creep from the feet, BFS over facet adjacency.
Transformation #3 = vein-first branching growth + shard spikes + Gaussian-dot dust.
Base art is never recoloured: all outputs are new files on copies.
All renders are PIL/numpy/scipy CPU proxies, labelled as such. No vendor tool
is claimed to have run when it did not. Gaussian Splatting material is pulled
as reference (existing splat front, 5,846 Gaussians) and as a Gaussian-dot dust
proxy in T3; that dust is NOT a true gsplat/splatfacto render (no torch, no GPU).
"""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
from scipy.spatial import cKDTree
from collections import deque

ROOT = "/home/hatch/workspace/cape-jones-rig"
SRC = os.path.join(ROOT, "crystallization-preset8-power-20261031")
OUT = os.path.join(ROOT, "crystal-cape-jones-v2-transformation-upgrade-20261031")
os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(OUT, "frames_t2"), exist_ok=True)
os.makedirs(os.path.join(OUT, "frames_t3"), exist_ok=True)

BASE_P = os.path.join(ROOT, "rig-apose-v7c-clean-transparent.png")
CRYSTAL_P = os.path.join(SRC, "P8-06-facet-glint-apose.png")
SPLAT_P = os.path.join(ROOT, "gaussian-splatting-20261031", "splat-front-20261031.png")

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

def adjacency(mask, fid):
    adj = {}
    # right neighbours
    a = fid[:, :-1]; b = fid[:, 1:]; m = mask[:, :-1] & mask[:, 1:] & (a != b) & (a >= 0) & (b >= 0)
    for u, v in zip(a[m].tolist(), b[m].tolist()):
        adj.setdefault(u, set()).add(v); adj.setdefault(v, set()).add(u)
    a = fid[:-1, :]; b = fid[1:, :]; m = mask[:-1, :] & mask[1:, :] & (a != b) & (a >= 0) & (b >= 0)
    for u, v in zip(a[m].tolist(), b[m].tolist()):
        adj.setdefault(u, set()).add(v); adj.setdefault(v, set()).add(u)
    return adj

def on_grey(im):
    bg = Image.new("RGBA", im.size, (128, 128, 128, 255)); bg.alpha_composite(im); return bg.convert("RGB")

def save_grey(im, path):
    on_grey(im).save(path)

def main():
    base = Image.open(BASE_P).convert("RGBA")
    crystal = Image.open(CRYSTAL_P).convert("RGBA")
    ba = np.asarray(base).astype(float); ca = np.asarray(crystal).astype(float)
    mask = np.asarray(base)[..., 3] > 10
    fid, nfacets = facet_ids(mask, 48, 7)
    stats = facet_stats(mask, fid, nfacets)
    valid = [i for i, s in enumerate(stats) if s is not None]
    print(f"facets valid {len(valid)} of {nfacets}, mask px {int(mask.sum())}")

    # ---------- Transformation #2: BFS creep from feet ----------
    adj = adjacency(mask, fid)
    seeds = [i for i in valid if stats[i]['ymax'] >= 1250 or stats[i]['cy'] >= 1180]
    print(f"T2 seeds (feet facets): {len(seeds)}")
    order = []; seen = set(seeds); q = deque(seeds); rng = np.random.default_rng(11)
    # BFS layer by layer, shuffled within layer -> irregular tendril front, not a straight line
    while q:
        layer = []
        for _ in range(len(q)):
            u = q.popleft(); layer.append(u)
            nbrs = sorted(adj.get(u, []))
            rng.shuffle(nbrs)
            for v in nbrs:
                if v not in seen and stats[v] is not None:
                    seen.add(v); q.append(v)
        order.extend(layer)
    # any unreached facets (disconnected) appended at end, sorted by cy descending
    missing = [i for i in valid if i not in seen]
    missing.sort(key=lambda i: -stats[i]['cy'])
    order.extend(missing)
    print(f"T2 order {len(order)}, missing appended {len(missing)}")

    meas = {"t2": {}, "t3": {}}
    nframes2 = 16
    t2_frames = []
    for k in range(nframes2):
        nrev = int(round((k+1)/nframes2 * len(order))) if k < nframes2-1 else len(order)
        revealed = set(order[:nrev])
        frontier = set(order[max(0, nrev-15):nrev])
        out = ba.copy()
        # revealed facets -> crystal
        rev_mask = np.isin(fid, list(revealed)) & mask if revealed else np.zeros_like(mask)
        out[rev_mask] = ca[rev_mask]
        # frontier facets -> 50% mix + white brighten, so the front reads as live growth, not a cut
        if frontier:
            fr_mask = np.isin(fid, list(frontier)) & mask
            out[fr_mask, :3] = ca[fr_mask, :3]*0.5 + ba[fr_mask, :3]*0.5 + 30
            out[fr_mask, :3] = np.clip(out[fr_mask, :3], 0, 255)
            # cyan glow edge around frontier: dilate frontier mask 2px, outside silhouette only? inside edge: draw on frontier boundary
            fr_dil = ndimage.binary_dilation(fr_mask, iterations=2)
            edge = fr_dil & mask & ~fr_mask
            out[edge, :3] = np.array([0, 200, 255], float)
        im = Image.fromarray(out.astype(np.uint8), "RGBA")
        im.save(os.path.join(OUT, "frames_t2", f"t2-{k:02d}.png"))
        t2_frames.append(im)
        # metrics at 50% frame (k=7)
        if k == 7:
            rev_ys = [stats[i]['cy'] for i in revealed]
            meas["t2"]["frame08_50pct"] = dict(facets_revealed=nrev, pct_facets=round(100*nrev/len(order), 1),
                pixels_revealed=int(rev_mask.sum()), pct_pixels=round(100*rev_mask.sum()/mask.sum(), 1),
                revealed_centroid_y_min=round(min(rev_ys), 1), revealed_centroid_y_max=round(max(rev_ys), 1),
                note="BFS creep: at 50% the revealed set spans feet to mid-torso with branches, NOT a clean horizontal band like #1 at 50% (y threshold only).")
    # GIF
    grey2 = [on_grey(f) for f in t2_frames]
    grey2[0].save(os.path.join(OUT, "transformation-2-creep-20261031.gif"), save_all=True, append_images=grey2[1:], duration=200, loop=0)
    meas["t2"].update(dict(frames=nframes2, duration_ms=200, seeds=len(seeds), facets_total=len(order),
        growth="feet seeds, BFS over facet adjacency, shuffled within layer, frontier 15 facets at 50% mix + cyan edge",
        final="100% P8-06 glint, same as V2 power-on"))
    print("T2 done")

    # ---------- Transformation #3: vein-first + shards + Gaussian dust ----------
    # vein skeleton polylines (image coords)
    veins = [
        [(450, 1290), (500, 1000), (560, 750), (560, 500), (560, 350)],  # centre up
        [(560, 500), (350, 450)],  # left arm
        [(560, 500), (770, 450)],  # right arm
        [(560, 750), (660, 1290)],  # right leg
        [(560, 750), (450, 1290)],  # left leg (already centre, adds weight)
    ]
    def vein_dist(cx, cy):
        best = 1e9
        for poly in veins:
            for (x1, y1), (x2, y2) in zip(poly, poly[1:]):
                dx, dy = x2-x1, y2-y1
                L2 = dx*dx+dy*dy
                t = 0 if L2 == 0 else max(0, min(1, ((cx-x1)*dx + (cy-y1)*dy)/L2))
                px, py = x1+t*dx, y1+t*dy
                best = min(best, math.hypot(cx-px, cy-py))
        return best
    rng3 = np.random.default_rng(23)
    scored = []
    for i in valid:
        s = stats[i]
        vd = vein_dist(s['cx'], s['cy'])
        # vein facets first, then fill outward; jitter breaks ties so fill is organic, not rings
        key = vd*2.0 + (1300 - s['cy'])*0.15 + rng3.uniform(0, 60)
        scored.append((key, i))
    scored.sort()
    order3 = [i for _, i in scored]
    nframes3 = 20
    t3_frames = []
    # silhouette edge mask for shard spikes
    edge_mask = mask & ~ndimage.binary_erosion(mask, iterations=2)
    for k in range(nframes3):
        nrev = int(round((k+1)/nframes3 * len(order3))) if k < nframes3-1 else len(order3)
        revealed = set(order3[:nrev])
        frontier = set(order3[max(0, nrev-20):nrev])
        out = ba.copy()
        rev_mask = np.isin(fid, list(revealed)) & mask if revealed else np.zeros_like(mask)
        out[rev_mask] = ca[rev_mask]
        if frontier and k < nframes3-1:
            fr_mask = np.isin(fid, list(frontier)) & mask
            out[fr_mask, :3] = np.clip(ca[fr_mask, :3]*0.6 + ba[fr_mask, :3]*0.4 + 25, 0, 255)
        im = Image.fromarray(out.astype(np.uint8), "RGBA")
        # shard spikes + Gaussian dust, only on intermediate frames
        if 0 < k < nframes3-1:
            layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
            # spikes: frontier facets on silhouette edge -> outward triangle 8-14px
            # outward direction approx = centroid - figure centre (562, 775), normalised
            for f in frontier:
                s = stats[f]
                # only if facet touches edge
                # check: any pixel of this facet on edge_mask (approx via centroid neighbourhood)
                cx, cy = int(s['cx']), int(s['cy'])
                if not (0 <= cx < im.size[0] and 0 <= cy < im.size[1]): continue
                # neighbourhood edge check
                win = edge_mask[max(0, cy-24):cy+25, max(0, cx-24):cx+25]
                if not win.any(): continue
                dx, dy = cx-562, cy-775
                L = math.hypot(dx, dy) or 1; dx, dy = dx/L, dy/L
                ln = 10 + (f % 5)  # 10-14px, deterministic per facet
                tip = (cx + dx*ln*2.2, cy + dy*ln*2.2)
                perp = (-dy, dx)
                d.polygon([(cx + perp[0]*5, cy + perp[1]*5), (cx - perp[0]*5, cy - perp[1]*5), tip],
                          fill=(0, 200, 255, 230))
            # Gaussian-dot dust ahead of front: soft dots in not-yet-revealed facets near frontier
            # deterministic particles seeded per frame
            prng = np.random.default_rng(1000+k)
            cand = [i for i in order3[nrev:min(nrev+120, len(order3))]]
            for f in cand[:60]:
                s = stats[f]
                r = prng.uniform(2.5, 5.5)
                col = (0, 200, 255) if prng.random() < 0.5 else (255, 110, 210)
                d.ellipse([s['cx']-r, s['cy']-r, s['cx']+r, s['cy']+r], fill=col + (170,))
            layer = layer.filter(ImageFilter.GaussianBlur(1.2))
            im.alpha_composite(layer)
        im.save(os.path.join(OUT, "frames_t3", f"t3-{k:02d}.png"))
        t3_frames.append(im)
        if k == 9:
            rev_ys = [stats[i]['cy'] for i in revealed]
            meas["t3"]["frame10_50pct"] = dict(facets_revealed=nrev, pct_facets=round(100*nrev/len(order3), 1),
                pixels_revealed=int(rev_mask.sum()), pct_pixels=round(100*rev_mask.sum()/mask.sum(), 1),
                note="Vein-first: at 50% vein facets up the centre/arms are crystallised while large off-vein areas are still base, unlike #1's horizontal band.")
    grey3 = [on_grey(f) for f in t3_frames]
    grey3[0].save(os.path.join(OUT, "transformation-3-vein-shard-20261031.gif"), save_all=True, append_images=grey3[1:], duration=160, loop=0)
    meas["t3"].update(dict(frames=nframes3, duration_ms=160, facets_total=len(order3),
        growth="vein skeleton centre+arms+legs, facets sorted by vein distance + height term + jitter, frontier 20 facets, shard spikes 10-14px on silhouette-edge frontier facets, Gaussian-dot dust 60 particles/frame ahead of front (PIL proxy, NOT a true splat render)",
        final="100% P8-06 glint, spikes and dust fade to 0 at final frame"))
    print("T3 done")

    # ---------- Future all-black symbiote variant (NOT V2, NOT canon) ----------
    # All figure pixels -> near-black, preserving alpha. White symbol = centre chest diamond zone only.
    # Symbol zone (measured, approximate): x 540-575, y 460-545, where original plate has the small chest diamond.
    # Head cowl purple is NOT recoloured white — that would be a white cowl, not the symbol.
    black = np.asarray(base).copy().astype(float)
    black[mask, :3] = np.array([18, 18, 22], float)
    # subtle linework: keep original dark lines darker? already near-black, so no change; keep alpha verbatim
    sym = black.copy()
    zone = np.zeros_like(mask); zone[460:546, 540:576] = True
    # in zone, white where original had alpha and was purple/dark emblem area: use original alpha + (original pixel not skin?) — simplest honest: white where zone & mask & original blue>red (purple emblem) OR zone centre diamond shape
    orig = np.asarray(base).astype(int)
    # diamond shape in zone: |x-557|/18 + |y-502|/42 <= 1
    yy, xx = np.mgrid[0:1500, 0:1100]
    diamond = (np.abs(xx-557)/18.0 + np.abs(yy-502)/42.0) <= 1.0
    sym_zone = mask & zone & diamond
    sym[sym_zone, :3] = np.array([255, 255, 255], float)
    # cape consumed / loses cape: for y>=600, erase alpha outside legs zone x 380-720 (cape side flaps).
    # For y<600 cape is behind shoulders and black-on-black, so no visual difference is claimed there.
    cape_out = np.zeros_like(mask); cape_out[600:, :] = True
    outside_legs = np.zeros_like(mask); outside_legs[:, :380] = True; outside_legs[:, 721:] = True
    erase = cape_out & outside_legs
    sym_cape = sym.copy(); sym_cape[erase, 3] = 0
    # also a with-cape version for comparison (black, white symbol, cape still present)
    im_with = Image.fromarray(sym.astype(np.uint8), "RGBA")
    im_without = Image.fromarray(sym_cape.astype(np.uint8), "RGBA")
    im_with.save(os.path.join(OUT, "future-symbiote-black-white-symbol-WITH-cape-20261031.png"))
    im_without.save(os.path.join(OUT, "future-symbiote-black-white-symbol-NO-cape-20261031.png"))
    save_grey(im_with, os.path.join(OUT, "future-symbiote-black-white-symbol-WITH-cape-20261031-on-grey.png"))
    save_grey(im_without, os.path.join(OUT, "future-symbiote-black-white-symbol-NO-cape-20261031-on-grey.png"))
    meas["future_variant"] = dict(
        status="FUTURE VARIANT ONLY, NOT V2, NOT canon, approval 0/1",
        body="all figure pixels (18,18,22), alpha verbatim from base plate",
        symbol="white (255,255,255) diamond zone x540-575 y460-545, diamond |x-557|/18+|y-502|/42<=1, approximate chest emblem, NOT head cowl (cowl purple left black)",
        cape_consumed="y>=600 alpha erased outside x380-720 (cape side flaps), legs kept; y<600 cape behind shoulders is black-on-black so no difference claimed there — true cape-piece separation would need sliced cape pieces, not a zone erase",
        alpha_with_cape=int((np.asarray(im_with)[..., 3] > 10).sum()),
        alpha_no_cape=int((np.asarray(im_without)[..., 3] > 10).sum()),
        alpha_removed=int((np.asarray(im_with)[..., 3] > 10).sum() - (np.asarray(im_without)[..., 3] > 10).sum()),
    )
    print("Future variant done", meas["future_variant"])

    # ---------- Contacts ----------
    def contact(paths, outname, cols=4, tw=275):
        imgs = []
        for p in paths:
            im = on_grey(Image.open(p).convert("RGBA")) if p.endswith(".png") else Image.open(p).convert("RGB")
            h = int(im.size[1]*tw/im.size[0]); imgs.append(im.resize((tw, h)))
        rows = math.ceil(len(imgs)/cols); th = max(t.size[1] for t in imgs)
        sheet = Image.new("RGB", (cols*tw, rows*th), (200, 200, 200)); dd = ImageDraw.Draw(sheet)
        for i, t in enumerate(imgs):
            x, y = (i % cols)*tw, (i // cols)*th
            sheet.paste(t, (x, y)); dd.text((x+4, y+4), os.path.basename(paths[i])[:40], fill=(255, 255, 0))
        sheet.save(os.path.join(OUT, outname))
    contact([os.path.join(OUT, "frames_t2", f"t2-{k:02d}.png") for k in [0, 3, 7, 11, 15]],
            "transformation-2-contact-20261031.png", cols=5)
    contact([os.path.join(OUT, "frames_t3", f"t3-{k:02d}.png") for k in [0, 4, 9, 14, 19]],
            "transformation-3-contact-20261031.png", cols=5)
    contact([os.path.join(OUT, "future-symbiote-black-white-symbol-WITH-cape-20261031.png"),
             os.path.join(OUT, "future-symbiote-black-white-symbol-NO-cape-20261031.png")],
            "future-symbiote-contact-20261031.png", cols=2, tw=400)

    json.dump(meas, open(os.path.join(OUT, "measurements-20261031.json"), "w"), indent=2)
    print(json.dumps(meas, indent=2))

if __name__ == "__main__":
    main()
