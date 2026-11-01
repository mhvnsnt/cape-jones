#!/usr/bin/env python3
"""Visual Preset 8 + Crystallization Power, 2026-10-31.
Source look: apose normal map (shading-upgrade-20261031/normal-map-apose-20261031.png),
estimated from silhouette + linework, NOT a rendered crystal character.
Base art is never recoloured permanently: the preset is an OVERLAY layer
applied on a copy; the original plate files are untouched.
Method: per-plate estimated normals (raw EDT, sigma 2, z-scale 1.5, same as
shading upgrade) -> Voronoi facets (jittered grid, cKDTree nearest seed) ->
per-facet flat colour = mean normal colour of that facet (faithful map look),
with a vivid boost option. All outputs are new files in this folder.
"""
import json, os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
from scipy.spatial import cKDTree

ROOT = "/home/hatch/workspace/cape-jones-rig"
OUT = os.path.join(ROOT, "crystallization-preset8-power-20261031")
os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(OUT, "frames"), exist_ok=True)

APOSE = os.path.join(ROOT, "rig-apose-v7c-clean-transparent.png")
ARMS = os.path.join(ROOT, "dual-light-variants-20261031", "base-arms-up-transparent-20261031.png")
NORMAL_APOSE = os.path.join(ROOT, "shading-upgrade-20261031", "normal-map-apose-20261031.png")

PALETTE_MEASURED = {
    "cyan_left_mean": [42, 126, 207],
    "pink_right_mean": [213, 123, 206],
    "centre_mean": [128, 136, 219],
    "all_mean": [127, 127, 209],
}
PALETTE_VIVID = {"cyan": [0, 200, 255], "pink": [255, 110, 210], "purple": [140, 120, 255]}

def compute_normals(im):
    a = np.asarray(im).astype(np.float32) / 255.0
    alpha, mask = a[..., 3], a[..., 3] > 0.5
    dist = ndimage.distance_transform_edt(mask)
    ds = ndimage.gaussian_filter(dist, 2.0)
    dzdy, dzdx = np.gradient(ds)
    nx, ny, nz = -dzdx * 1.5, -dzdy * 1.5, np.ones_like(dist)
    nlen = np.sqrt(nx**2 + ny**2 + nz**2)
    return mask, alpha, nx/nlen, ny/nlen, nz/nlen, dist

def facet_ids(mask, spacing, seed=7):
    rng = np.random.default_rng(seed)
    H, W = mask.shape
    ys, xs = np.where(mask)
    # jittered grid seeds over bbox
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

def facet_colour_image(im, mask, nx, ny, nz, fid, nfacets, boost=1.0):
    """Per-facet flat normal colour. boost>1 saturates away from grey."""
    nvis = np.dstack([(nx*0.5+0.5), (ny*0.5+0.5), (nz*0.5+0.5)])  # 0..1
    out = np.zeros((*mask.shape, 3), float)
    ys, xs = np.where(mask)
    ids = fid[ys, xs]
    # mean per facet via bincount
    for ch in range(3):
        s = np.bincount(ids, weights=nvis[ys, xs, ch], minlength=nfacets)
        cnt = np.bincount(ids, minlength=nfacets)
        mean = np.divide(s, np.maximum(cnt, 1))
        out[ys, xs, ch] = mean[ids]
    if boost != 1.0:
        grey = out.mean(axis=2, keepdims=True)
        out = np.clip(grey + (out - grey) * boost, 0, 1)
    rgba = np.dstack([out, np.asarray(im).astype(float)[..., 3]/255.0])
    return Image.fromarray((np.clip(rgba, 0, 1)*255).astype(np.uint8), "RGBA")

def add_edges(img, fid, mask, width=1, colour=(20, 20, 40, 255)):
    a = np.asarray(img).copy()
    # facet boundary: pixel whose right or down neighbour has a different facet id
    b = np.zeros_like(mask)
    b[:, :-1] |= (fid[:, :-1] != fid[:, 1:]) & mask[:, :-1] & mask[:, 1:]
    b[:-1, :] |= (fid[:-1, :] != fid[1:, :]) & mask[:-1, :] & mask[1:, :]
    a[b] = colour
    return Image.fromarray(a, "RGBA")

def add_glints(img, fid, mask, nx, ny, spacing):
    """White glint dot at facet centroids where normal faces the light (left-up)."""
    out = img.copy(); d = ImageDraw.Draw(out)
    ys, xs = np.where(mask)
    ids = fid[ys, xs]
    n = int(ids.max())+1 if len(ids) else 0
    for f in range(n):
        sel = ids == f
        if sel.sum() < 40: continue
        cx, cy = int(xs[sel].mean()), int(ys[sel].mean())
        if not (0 <= cx < img.size[0] and 0 <= cy < img.size[1]): continue
        if not mask[cy, cx]: continue
        # light from left-up: nx negative, ny negative (up in image = -y in our ny convention? use nx<0)
        if nx[cy, cx] < -0.2:
            r = max(2, spacing//12)
            d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(255, 255, 255, 230))
    return out

def rim_outside(img, mask, colour=(0, 200, 255, 255), width=6):
    """Cyan rim ONLY outside silhouette (dilate minus mask). No interior coverage."""
    dil = ndimage.binary_dilation(mask, iterations=width)
    ring = dil & ~mask
    a = np.asarray(img).copy()
    # paste rim on transparent background area: need canvas RGBA, alpha set
    a[ring] = colour
    return Image.fromarray(a, "RGBA")

def on_grey(im):
    bg = Image.new("RGBA", im.size, (128, 128, 128, 255)); bg.alpha_composite(im); return bg.convert("RGB")

def save(im, name):
    im.save(os.path.join(OUT, name))
    on_grey(im).save(os.path.join(OUT, name.replace(".png", "-on-grey.png")))
    return name

def build_plate(label, plate_path, spacing=48):
    plate = Image.open(plate_path).convert("RGBA")
    mask, alpha, nx, ny, nz, dist = compute_normals(plate)
    fid, nfacets = facet_ids(mask, spacing)
    results = {}
    # P8-01 faithful facet (mean normal per facet)
    f1 = facet_colour_image(plate, mask, nx, ny, nz, fid, nfacets, boost=1.0)
    save(f1, f"P8-01-facet-faithful-{label}.png"); results["P8-01"] = int(nfacets)
    # P8-02 vivid boost
    f2 = facet_colour_image(plate, mask, nx, ny, nz, fid, nfacets, boost=1.6)
    save(f2, f"P8-02-facet-vivid-{label}.png")
    # P8-03 coarse facets (spacing 80)
    fid_c, nf_c = facet_ids(mask, 80)
    f3 = facet_colour_image(plate, mask, nx, ny, nz, fid_c, nf_c, boost=1.3)
    save(f3, f"P8-03-facet-coarse-{label}.png"); results["P8-03_facets"] = int(nf_c)
    # P8-04 fine facets (spacing 28)
    fid_f, nf_f = facet_ids(mask, 28)
    f4 = facet_colour_image(plate, mask, nx, ny, nz, fid_f, nf_f, boost=1.3)
    save(f4, f"P8-04-facet-fine-{label}.png"); results["P8-04_facets"] = int(nf_f)
    # P8-05 facets + hard edges
    f5 = add_edges(f2, fid, mask)
    save(f5, f"P8-05-facet-edges-{label}.png")
    # P8-06 facets + glints
    f6 = add_glints(f5, fid, mask, nx, ny, spacing)
    save(f6, f"P8-06-facet-glint-{label}.png")
    # P8-07 facets mixed 50% with base plate (refraction / glass tint)
    a = np.asarray(f2).astype(float); b = np.asarray(plate).astype(float)
    mix = a.copy(); m = mask
    mix[m, :3] = a[m, :3]*0.5 + b[m, :3]*0.5
    save(Image.fromarray(mix.astype(np.uint8), "RGBA"), f"P8-07-facet-mix-base-{label}.png")
    # P8-08 facets + outside-only cyan rim
    f8 = rim_outside(f6, mask)
    save(f8, f"P8-08-facet-rim-outside-{label}.png")
    # coverage / alpha check
    results["mask_px"] = int(mask.sum())
    results["alpha_preserved"] = bool((np.asarray(f1)[..., 3] > 0).sum() == mask.sum())
    results["facets_spacing48"] = int(nfacets)
    return plate, mask, nx, ny, nz, fid, nfacets, results

def main():
    meas = {"palette_measured": PALETTE_MEASURED, "palette_vivid": PALETTE_VIVID, "plates": {}}
    apose_plate, apose_mask, nx, ny, nz, fid, nf, r = build_plate("apose", APOSE)
    meas["plates"]["apose"] = r
    arms_plate, arms_mask, anx, any_, anz, afid, anf, r2 = build_plate("armsup", ARMS)
    meas["plates"]["armsup"] = r2
    # --- Power transition: crystallisation 0% -> 100% by height sweep + facet reveal ---
    # Transition mask: crystallised fraction = rows from feet upward (power rises).
    # Frame t: pixels below threshold y are facet image, above are base plate.
    facet_apose = Image.open(os.path.join(OUT, "P8-06-facet-glint-apose.png")).convert("RGBA")
    ys, xs = np.where(apose_mask)
    y0, y1 = int(ys.min()), int(ys.max())
    frames = []
    for i, frac in enumerate([0, 0.2, 0.4, 0.6, 0.8, 1.0]):
        thresh = y1 - frac * (y1 - y0)
        fa = np.asarray(facet_apose).copy(); ba = np.asarray(apose_plate).copy()
        out = ba.copy()
        sel = apose_mask & (np.arange(apose_mask.shape[0])[:, None] >= thresh)
        out[sel] = fa[sel]
        im = Image.fromarray(out, "RGBA")
        im.save(os.path.join(OUT, "frames", f"crystal-transition-{i:02d}-{int(frac*100)}pct.png"))
        frames.append(f"frames/crystal-transition-{i:02d}-{int(frac*100)}pct.png")
    # GIF on grey for chat viewing
    gif_frames = []
    for f in frames:
        gif_frames.append(on_grey(Image.open(os.path.join(OUT, f)).convert("RGBA")))
    gif_frames[0].save(os.path.join(OUT, "crystallization-power-transition-20261031.gif"),
                       save_all=True, append_images=gif_frames[1:], duration=400, loop=0)
    meas["transition_frames"] = frames
    meas["transition_note"] = "Power OFF = base plate (0%). Power ON = full facet glint image (100%). Sweep rises from feet upward; intermediate frames are a partial-crystallisation proof, not a story claim about hardness/reflectivity."
    # --- Contacts ---
    def contact(names, outname, cols=4):
        imgs = [on_grey(Image.open(os.path.join(OUT, n)).convert("RGBA")) for n in names]
        # tile at 275px wide each, keep aspect
        tw = 275
        tiles = []
        for im in imgs:
            h = int(im.size[1] * tw / im.size[0]); tiles.append(im.resize((tw, h)))
        rows = math.ceil(len(tiles)/cols)
        th = max(t.size[1] for t in tiles)
        sheet = Image.new("RGB", (cols*tw, rows*th), (200, 200, 200))
        from PIL import ImageDraw as ID
        dd = ID.Draw(sheet)
        for i, t in enumerate(tiles):
            x, y = (i % cols)*tw, (i // cols)*th
            sheet.paste(t, (x, y)); dd.text((x+4, y+4), names[i][:38], fill=(255, 255, 0))
        sheet.save(os.path.join(OUT, outname))
    apose_names = [f"P8-0{i}-facet-{s}-apose.png" if False else n for i, s in [(1, "faithful"), (2, "vivid")] for n in [f"P8-0{i}-facet-{s}-apose.png"]]
    # explicit list
    contact(["P8-01-facet-faithful-apose.png", "P8-02-facet-vivid-apose.png",
             "P8-03-facet-coarse-apose.png", "P8-04-facet-fine-apose.png",
             "P8-05-facet-edges-apose.png", "P8-06-facet-glint-apose.png",
             "P8-07-facet-mix-base-apose.png", "P8-08-facet-rim-outside-apose.png"],
            "preset8-apose-contact-20261031.png")
    contact(["P8-01-facet-faithful-armsup.png", "P8-02-facet-vivid-armsup.png",
             "P8-05-facet-edges-armsup.png", "P8-06-facet-glint-armsup.png",
             "P8-08-facet-rim-outside-armsup.png"],
            "preset8-armsup-contact-20261031.png", cols=3)
    json.dump(meas, open(os.path.join(OUT, "measurements-20261031.json"), "w"), indent=2)
    print(json.dumps(meas, indent=2))

if __name__ == "__main__":
    main()
