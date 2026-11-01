#!/usr/bin/env python3
"""G2 shading upgrade, 2026-10-31. PIL/numpy primary, Blender compositor V8 second.
Base art untouched. All outputs are new files in shading-upgrade-20261031/.
Method, stated plainly: normals are ESTIMATED from silhouette distance +
interior linework creases (normal-from-depth / shape-from-silhouette).
No true 3D character model exists, so no variant here is a true 3D mesh
normal pass. That unblocker is still owed and is stated, not hidden.
Key fix vs old G2: shading is computed PER PIXEL from the estimated
normal and a stated light vector, with a shadow-side range that actually
darkens (0.35-1.00, never brightening above 1.00, because the white suit
at 255 cannot get brighter - brightening only clips). Old G2 used a
whole-canvas linear gradient centred on the canvas, not on the figure,
so the figure (only 628 px wide in a 1100 px canvas) saw only a small
slice of the gradient, and the white suit clipped the bright side.
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

ROOT = "/home/hatch/workspace/cape-jones-rig"
OUT = os.path.join(ROOT, "shading-upgrade-20261031")
os.makedirs(OUT, exist_ok=True)
BASE_PATH = os.path.join(ROOT, "rig-apose-v7c-clean-transparent.png")
ARMS_PATH = os.path.join(ROOT, "dual-light-variants-20261031", "base-arms-up-transparent-20261031.png")

def norm(v):
    v = np.array(v, dtype=float); return v / np.linalg.norm(v)

def compute_fields(im):
    """Return mask, depth, normals (nx,ny,nz in v4 convention: nx left-negative,
    ny up-positive), interior-line mask, figure bbox centre."""
    a = np.asarray(im).astype(np.float32) / 255.0
    rgb, alpha = a[..., :3], a[..., 3]
    mask = alpha > 0.5
    ys, xs = np.where(mask)
    bbox = (int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()))
    cx_fig = (bbox[0] + bbox[1]) / 2.0
    dist = ndimage.distance_transform_edt(mask)
    depth = np.zeros_like(dist)
    if dist[mask].max() > 0:
        depth[mask] = dist[mask] / dist[mask].max()
    gray = rgb.mean(axis=2)
    eroded = ndimage.binary_erosion(mask, iterations=4)
    gmax = ndimage.maximum_filter(gray, size=7)
    lines = eroded & (gray < 0.43) & ((gmax - gray) > 0.12)
    depth = depth.copy(); depth[lines] -= 0.35
    depth = np.clip(ndimage.gaussian_filter(depth, 3.0), 0, 1)
    depth[~mask] = 0
    # NORMALS FROM RAW DISTANCE IN PIXELS, not from normalized depth.
    # Normalized depth changes ~0.02/px, so nx,ny were ~0.04 vs nz=1 and
    # the old "Lambert" was almost uniform darkening, not form shading.
    # Raw EDT changes ~1 px per px inward, so its gradient is a real
    # outward-pointing direction per limb edge. Smoothed (sigma 2) to
    # soften the medial-axis ridge flip, z-scale 1.5 for readable relief.
    dist_s = ndimage.gaussian_filter(dist, 2.0)
    dzdy, dzdx = np.gradient(dist_s)
    nx = -dzdx * 1.5; ny = -dzdy * 1.5; nz = np.ones_like(depth)
    nlen = np.sqrt(nx**2 + ny**2 + nz**2)
    return dict(mask=mask, depth=depth, nx=nx/nlen, ny=ny/nlen, nz=nz/nlen,
                lines=lines, dist=dist, bbox=bbox, cx_fig=cx_fig, rgb=rgb, alpha=alpha)

def apply_shade(im, shade, tint=None):
    """shade: per-pixel factor array (H,W). tint: (3,) or None. Alpha unchanged."""
    a = np.asarray(im).astype(float)
    out = a.copy()
    out[..., :3] *= shade[..., None]
    if tint is not None:
        # tint only the lit portion: blend toward tint where shade is high
        w = np.clip((shade - 0.35) / 0.65, 0, 1)[..., None]
        out[..., :3] = out[..., :3] * (1 - w * 0.15) + np.array(tint)[None, None, :] * (w * 0.15) * 255 * 0  # no-op safeguard
        out = a.copy(); out[..., :3] *= shade[..., None]
    out[..., 3] = a[..., 3]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA")

def stats_for(im, fields):
    arr = np.asarray(im).astype(float)
    mask = fields["mask"]; cx = fields["cx_fig"]; W = arr.shape[1]
    xs = np.arange(W)[None, :]
    left = mask & (xs < cx); right = mask & (xs >= cx)
    lum = arr[..., :3].mean(axis=2)
    def m(sel, ch):
        return float(arr[..., ch][sel].mean()) if sel.any() else 0.0
    # Edge-contrast metric: pixels whose estimated normal faces left (nx < -0.3)
    # vs faces right (nx > 0.3). This is the TRUE form-shading metric: a limb
    # lit from the left has its left edge bright and its right edge dark,
    # and every limb contributes both edges to BOTH figure halves, so the
    # half-mean delta cancels for pure form shading. L02's +31.9 was NOT
    # pure normal shading: its code multiplied by an explicit side weight
    # (1.15 left of canvas centre, 0.85 right), which is what moved the
    # half-mean. Both metrics are reported; neither is hidden.
    nx = fields["nx"]
    lf = mask & (nx < -0.3); rf = mask & (nx > 0.3)
    return {
        "left_R": round(m(left, 0), 1), "right_R": round(m(right, 0), 1),
        "delta_R": round(m(left, 0) - m(right, 0), 1),
        "left_lum": round(float(lum[left].mean()), 1), "right_lum": round(float(lum[right].mean()), 1),
        "delta_lum": round(float(lum[left].mean() - lum[right].mean()), 1),
        "left_facing_R": round(m(lf, 0), 1), "right_facing_R": round(m(rf, 0), 1),
        "edge_delta_R": round(m(lf, 0) - m(rf, 0), 1),
        "figure_centre_x": fields["cx_fig"], "mask_px": int(mask.sum()),
    }

def on_grey(im):
    bg = Image.new("RGBA", im.size, (128, 128, 128, 255)); bg.alpha_composite(im); return bg.convert("RGB")

def main():
    base = Image.open(BASE_PATH).convert("RGBA")
    F = compute_fields(base)
    mask, depth, lines, dist = F["mask"], F["depth"], F["lines"], F["dist"]
    nx, ny, nz = F["nx"], F["ny"], F["nz"]
    # normal map + depth map (proof, not scene layers)
    nvis = np.dstack([(nx*0.5+0.5), (ny*0.5+0.5), (nz*0.5+0.5), F["alpha"]])
    Image.fromarray((nvis*255).astype(np.uint8), "RGBA").save(f"{OUT}/normal-map-apose-20261031.png")
    Image.fromarray((np.dstack([depth, depth, depth, F["alpha"]])*255).astype(np.uint8), "RGBA").save(f"{OUT}/depth-map-apose-20261031.png")

    L_LEFT = norm([-0.80, -0.20, 0.56])   # light from viewer's left, slightly above
    L_RIGHT = norm([0.80, -0.20, 0.56])   # light from viewer's right, slightly above
    def diff(L):
        return np.clip(nx*L[0] + ny*L[1] + nz*L[2], 0, 1)
    dL, dR = diff(L_LEFT), diff(L_RIGHT)
    ao = np.clip(dist / 18.0, 0, 1)  # 0 at silhouette edge, 1 deep inside

    # Old G2 gradient, reproduced exactly in spirit: canvas-global, centred 550,750
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w]
    d = ((xx - w/2) * 1.0 + (yy - h/2) * 0.0) / max(w, h)
    d = (d - d.min()) / (d.max() - d.min() + 1e-9) - 0.5
    old_grad = 1 + d * 0.5

    variants = []
    def add(name, shade, light_desc, method, verdict_note=""):
        im = apply_shade(base, np.where(mask, shade, 1.0))
        im.save(f"{OUT}/{name}.png")
        st = stats_for(im, F)
        st.update({"light": light_desc, "method": method, "note": verdict_note})
        variants.append((name, im, st))
        print(name, st["left_R"], st["right_R"], "delta_R", st["delta_R"], "delta_lum", st["delta_lum"])
        return im

    add("V0-control-no-shade", np.ones_like(depth), "none (control)", "Original plate, no shading. Expected delta ~0.")
    add("V1-old-G2-gradient-reproduced", old_grad, "canvas gradient, left bright",
        "Old G2 shade(): whole-canvas linear gradient, strength 0.5. REPRODUCED to show the flaw.")
    add("V2-lambert-LEFT-strong", 0.35 + 0.65 * dL, "KEY LEFT, slightly above; shadow RIGHT",
        "Lambert N.L, light (-0.80,-0.20,0.56), ambient 0.35, diffuse 0.65. Per-pixel normals.")
    add("V3-lambert-RIGHT-strong", 0.35 + 0.65 * dR, "KEY RIGHT, slightly above; shadow LEFT",
        "Lambert N.L, light (0.80,-0.20,0.56), ambient 0.35, diffuse 0.65. Mirror of V2.")
    # Toon / cel: quantize diffuse into 3 bands
    bands = np.select([dL < 0.35, dL < 0.70], [0.40, 0.68], default=1.00)
    add("V4-toon-cel-LEFT-3band", bands, "KEY LEFT; shadow RIGHT, stepped bands",
        "Cel/toon shading: Lambert diffuse quantized to 3 bands (0.40 / 0.68 / 1.00).")
    # Three-point: key left warm, fill right cool, rim on lit edge
    base_shade = 0.40 + 0.55 * dL + 0.15 * dR
    im5 = apply_shade(base, np.where(mask, base_shade, 1.0))
    arr5 = np.asarray(im5).astype(float)
    # warm key tint on lit side, cool fill tint on shadow side (subtle, no hue invention beyond tints)
    lit = np.clip(dL, 0, 1)[..., None]; shad = np.clip(1 - dL, 0, 1)[..., None]
    arr5[..., 0] = arr5[..., 0] * (1 + 0.06 * lit[..., 0]) + 0 * shad[..., 0]
    arr5[..., 2] = arr5[..., 2] * (1 + 0.06 * shad[..., 0])
    edge = mask & (dist < 5)
    arr5[edge, :3] += np.array([30, 18, 0])  # warm rim on silhouette edge
    im5 = Image.fromarray(np.clip(arr5, 0, 255).astype(np.uint8), "RGBA")
    im5.save(f"{OUT}/V5-three-point-LEFT-warm-RIGHT-cool.png")
    st5 = stats_for(im5, F); st5.update({"light": "KEY LEFT warm, FILL RIGHT cool, warm rim", "method": "Three-point lighting, per-pixel normals + edge rim."})
    variants.append(("V5-three-point-LEFT-warm-RIGHT-cool", im5, st5)); print("V5", st5["left_R"], st5["right_R"], st5["delta_R"])
    # AO + Lambert left
    ao_shade = (0.35 + 0.65 * dL) * (0.55 + 0.45 * ao)
    ao_shade = np.where(lines, ao_shade * 0.70, ao_shade)
    add("V6-AO-plus-lambert-LEFT", ao_shade, "KEY LEFT; edges + creases darkened",
        "Ambient occlusion from distance-to-edge (0 at edge, 1 deep) + Lambert left + crease darkening x0.70.")
    # Figure-local side-weight + normal (corrected side-weight: inside figure bbox only)
    x0, x1 = F["bbox"][0], F["bbox"][1]
    s_left = np.clip((x1 - xx) / max(1, (x1 - x0)), 0, 1)  # 1 at figure left edge, 0 at right
    side_shade = 0.35 + 0.65 * (0.5 * dL + 0.5 * s_left)
    add("V7-form-depth-plus-sideweight-LEFT", side_shade, "KEY LEFT; form depth + figure-local side weight",
        "Depth/form shading: 50% normal diffuse + 50% figure-bbox-local side gradient (NOT canvas-global).")
    # Top light, for contrast: should show small left/right delta, large top/bottom
    L_TOP = norm([0.0, -1.0, 0.45])
    dT = diff(L_TOP)
    add("V8-top-light", 0.35 + 0.65 * dT, "KEY ABOVE; shadow BELOW (left/right delta expected small)",
        "Lambert, light from above. Included so left/right delta is NOT misread: top light must NOT move left/right much.")
    # Combined production variant: normal + strong figure-local side weight + AO.
    # This is the variant that is MEANT to move the half-mean delta, by
    # side-weighting, labelled as such, not as pure normal shading.
    comb = (0.35 + 0.65 * (0.4 * dL + 0.6 * s_left)) * (0.70 + 0.30 * ao)
    add("V10-combined-normal-sideweight-AO-LEFT", comb, "KEY LEFT, side-weighted + AO",
        "Combined: 40% normal diffuse + 60% figure-local side weight, times AO. Side-weight is what moves half-mean delta.")

    # Arms-up hero: best method (V2 Lambert left) applied to arms-up plate
    arms = Image.open(ARMS_PATH).convert("RGBA")
    FA = compute_fields(arms)
    dLA = np.clip(FA["nx"]*L_LEFT[0] + FA["ny"]*L_LEFT[1] + FA["nz"]*L_LEFT[2], 0, 1)
    hero = apply_shade(arms, np.where(FA["mask"], 0.35 + 0.65 * dLA, 1.0))
    hero.save(f"{OUT}/HERO-arms-up-lambert-LEFT-20261031.png")
    hero_st = stats_for(hero, FA); hero_st.update({"light": "KEY LEFT", "method": "V2 Lambert left applied to approved arms-up plate."})
    print("HERO arms-up", hero_st)

    # Contact sheet, labelled with delta, on grey, no crop (tiles are full frames scaled)
    tiles = []
    for name, im, st in variants:
        tiles.append((f"{name} dR {st['delta_R']:+.1f}", on_grey(im)))
    tiles.append(("HERO arms-up dR %.1f" % hero_st["delta_R"], on_grey(hero)))
    cols = 3; tw = 366; th = int(tw * 1500 / 1100)
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 28)), (200, 200, 200))
    dr = ImageDraw.Draw(sheet)
    for i, (lab, t) in enumerate(tiles):
        x, y = (i % cols) * tw, (i // cols) * (th + 28)
        sheet.paste(t.resize((tw, th)), (x, y + 28)); dr.text((x + 4, y + 6), lab, fill=(0, 0, 0))
    sheet.save(f"{OUT}/shading-upgrade-contact-20261031.png")
    # Diagram: silhouette + light arrow from left, shadow right, labelled
    diag = Image.new("RGB", (1100, 1500), (32, 32, 40))
    d = ImageDraw.Draw(diag)
    d.text((40, 40), "LIGHT DIAGRAM - KEY LIGHT FROM VIEWER'S LEFT, SLIGHTLY ABOVE", fill=(255, 255, 0))
    d.text((40, 80), "Lit side = LEFT (bright). Shadow side = RIGHT (dark).", fill=(255, 255, 255))
    d.text((40, 120), "Arrow: light travels left -> right, down slightly.", fill=(255, 255, 255))
    d.line([(40, 700), (240, 700)], fill=(255, 200, 80), width=12)
    d.polygon([(240, 700), (200, 680), (200, 720)], fill=(255, 200, 80))
    d.text((40, 1350), "Normals: estimated from silhouette distance + interior lines. NOT a true 3D mesh pass.", fill=(255, 255, 0))
    sil = base.copy(); sil_arr = np.array(sil); sil_arr[..., :3] = 255
    diag_rgba = diag.convert("RGBA"); diag_rgba.alpha_composite(Image.fromarray(sil_arr, "RGBA"), (0, 0))
    diag_rgba.convert("RGB").save(f"{OUT}/light-diagram-LEFT-20261031.png")

    # No-crop check: alpha mask identical for every variant, edge alpha 0, size unchanged
    base_mask = np.asarray(base)[..., 3] > 10
    nocrop = {}
    for name, im, st in variants:
        m = np.asarray(im)[..., 3] > 10
        nocrop[name] = {"size": list(im.size), "mask_identical_to_base": bool((m == base_mask).all()),
                        "pixels_lost": int((base_mask & ~m).sum()),
                        "edge_alpha_px": int((np.asarray(im)[0, :, 3] > 10).sum() + (np.asarray(im)[-1, :, 3] > 10).sum() + (np.asarray(im)[:, 0, 3] > 10).sum() + (np.asarray(im)[:, -1, 3] > 10).sum())}
    out_json = {"base": "rig-apose-v7c-clean-transparent.png (1100x1500)", "figure_bbox": F["bbox"],
                "figure_centre_x": F["cx_fig"], "L02_baseline_delta_R": 31.9, "old_G2_best_delta_R": -18.2,
                "variants": {n: s for n, _, s in variants}, "hero_arms_up": hero_st, "no_crop": nocrop}
    with open(f"{OUT}/shading-upgrade-stats-20261031.json", "w") as f:
        json.dump(out_json, f, indent=2)
    print("DONE", len(variants), "variants")

if __name__ == "__main__":
    main()
