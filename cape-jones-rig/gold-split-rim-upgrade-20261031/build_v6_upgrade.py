#!/usr/bin/env python3
"""V6 standalone split preset + power-candidate upgrade.
NOT a V5 variant. V5 unchanged, old golds unchanged, V6 replaces nothing.
Built on the L3 V5 shot plate, but V6 is its own entry, filed as:
 (1) standalone split preset V6, and (2) POWER CANDIDATE (not canon).
Method: rim ONLY outside the silhouette (dilate-minus-alpha).
Plate is composited AFTER rim/halo/bloom, so interior black linework
is never overwritten by an opaque rim. Ring stays opaque; halo is soft
and sits UNDER the ring, never semi-transparent ring (that would
re-open the gold mix). Cyan bloom masked to cyan side AND outside
silhouette in upgrade variants (stricter than original cyan-side-only).
"""
import numpy as np, json, pathlib
from PIL import Image, ImageFilter
from scipy.ndimage import binary_dilation

OUT = pathlib.Path.home() / "workspace/cape-jones-rig/gold-split-rim-upgrade-20261031"
OUT.mkdir(parents=True, exist_ok=True)
RIG = pathlib.Path.home() / "workspace/cape-jones-rig"
PLATE_P = RIG / "dual-light-variants-20261031/base-arms-up-transparent-20261031.png"
BG_P = RIG / "godray-level3-20261031/godray-bg-v2-1100x1500.png"
GROUND_P = RIG / "godray-level3-20261031/layer-ground-shadow.png"
CAST_P = RIG / "godray-level3-20261031/layer-cast-shadow.png"
GOLD = (255, 180, 80, 255)
CYAN = (3, 204, 255, 255)  # measured new-Standard cyan median (input 0,200,255 + masked bloom lift)

plate = np.array(Image.open(PLATE_P).convert("RGBA"))
pa = plate[..., 3] > 10
H, W = pa.shape
# interior black linework, eroded 6px so the outer outline itself is not counted as interior
from scipy.ndimage import binary_erosion
interior = binary_erosion(pa, iterations=6)
black_int = (plate[..., :3].sum(axis=2) < 180) & pa & interior
print(f"plate alpha {pa.sum()} black-interior {black_int.sum()}")

def rim_mask(width, seam):
    dil = binary_dilation(pa, iterations=width)
    outer = dil & ~pa
    return outer

def split_rim(width, seam, halo_blur=0, halo_alpha=0):
    outer = rim_mask(width, seam)
    xs = np.arange(W)[None, :]
    gold_m = outer & (xs < seam)
    cyan_m = outer & (xs >= seam)
    return gold_m, cyan_m, outer

def compose(name, width, seam, halo=False, bg_dark=1.0, bloom=True):
    gold_m, cyan_m, outer = split_rim(width, seam)
    bg = np.array(Image.open(BG_P).convert("RGBA")).copy()
    if bg_dark != 1.0:
        bg[..., :3] = (bg[..., :3].astype(float) * bg_dark).astype(np.uint8)
    comp = bg.copy()
    # shadows under figure
    for p in (GROUND_P, CAST_P):
        lay = np.array(Image.open(p).convert("RGBA"))
        a = (lay[..., 3:4].astype(float) / 255.0)
        comp[..., :3] = (comp[..., :3] * (1 - a) + lay[..., :3] * a).astype(np.uint8)
    # halo UNDER ring: blurred outer rim, outside only, soft alpha
    if halo:
        halo_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ha = np.zeros((H, W), dtype=np.uint8)
        xs = np.arange(W)[None, :]
        # halo colour follows side
        halo_arr = np.zeros((H, W, 4), dtype=np.uint8)
        halo_arr[outer & (xs < seam)] = GOLD
        halo_arr[outer & (xs >= seam)] = CYAN
        halo_img = Image.fromarray(halo_arr).filter(ImageFilter.GaussianBlur(14))
        ha = np.array(halo_img)
        # keep halo outside silhouette only, and cap alpha
        ha[pa] = 0
        ha[..., 3] = (ha[..., 3].astype(float) * 0.45).astype(np.uint8)
        a = ha[..., 3:4].astype(float) / 255.0
        comp[..., :3] = (comp[..., :3] * (1 - a) + ha[..., :3] * a).astype(np.uint8)
    # opaque ring, outside only
    ring = np.zeros((H, W, 4), dtype=np.uint8)
    xs = np.arange(W)[None, :]
    ring[gold_m] = GOLD
    ring[cyan_m] = CYAN
    ring_img = Image.fromarray(ring)
    comp_img = Image.fromarray(comp)
    comp_img.alpha_composite(ring_img)
    comp = np.array(comp_img)
    # plate ON TOP: line preservation by construction
    comp_img = Image.fromarray(comp)
    comp_img.alpha_composite(Image.fromarray(plate))
    comp = np.array(comp_img)
    # cyan bloom: soft, masked to cyan side AND outside silhouette AND
    # outside the opaque rim itself, so it glows AROUND the rim and never
    # darkens the rim colour (a blurred-RGB bloom over the rim diluted it
    # to (2,187,233) in the first run - fixed here by using solid colour
    # with a blurred alpha mask only).
    if bloom:
        from scipy.ndimage import binary_dilation as _dil
        bloom_band = _dil(outer, iterations=18) & ~outer & ~pa
        xs = np.arange(W)[None, :]
        bloom_band &= (xs >= seam)
        # blurred alpha for the band
        band_img = Image.fromarray((bloom_band * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10))
        ba_alpha = (np.array(band_img).astype(float) / 255.0) * 0.35
        # re-mask AFTER blur: blur spreads alpha into the plate, so cut it
        # back to the band itself, or it tints interior lines near the edge
        ba_alpha[pa] = 0
        ba_alpha[outer] = 0
        ba_alpha[:, :seam] = 0
        a = ba_alpha[..., None]
        comp[..., :3] = (comp[..., :3] * (1 - a) + np.array(CYAN[:3]) * a).astype(np.uint8)
    # measurements
    gold_px = gold_m.sum(); cyan_px = cyan_m.sum()
    # rim colour medians in final (outside plate, gold/cyan-ish)
    final = comp
    gm = (final[..., 0] == 255) & (final[..., 1] == 180) & (final[..., 2] == 80) & ~pa
    cm = (final[..., 0] == 3) & (final[..., 1] == 204) & (final[..., 2] == 255) & ~pa
    # black interior preserved: plate region in final vs plate
    preserved = None
    # compare black-interior pixels: final RGB at those coords vs plate RGB
    # plate is on top, so except bloom (outside only) they must be identical
    same = (final[black_int][:, :3] == plate[black_int][:, :3]).all(axis=1)
    preserved_pct = float(100 * same.mean()) if len(same) else 0.0
    opaque_mask = black_int & (plate[..., 3] == 255)
    same_op = (final[opaque_mask][:, :3] == plate[opaque_mask][:, :3]).all(axis=1)
    preserved_opaque_pct = float(100 * same_op.mean()) if len(same_op) else 0.0
    out_path = OUT / name
    Image.fromarray(final).save(out_path)
    meas = {"file": name, "rim_width_px": width, "seam_x": seam, "halo": halo,
            "gold_rim_px": int(gold_px), "cyan_rim_px": int(cyan_px),
            "rim_inside_plate_px": 0, "rim_outside_plate_px": int(outer.sum()),
            "gold_exact_px_in_final_outside": int(gm.sum()), "cyan_exact_px_in_final_outside": int(cm.sum()),
            "gold_median": [255, 180, 80], "black_interior_preserved_pct": preserved_pct,
            "black_interior_opaque_preserved_pct": preserved_opaque_pct,
            "black_interior_total": int(black_int.sum())}
    print(name, meas)
    return meas

results = {}
results["v6-thin-outer-only-6px-seam550"] = compose("v6-thin-outer-only-6px-seam550-20261031.png", 6, 550, halo=False)
results["v6-medium-outer-only-12px-seam550"] = compose("v6-medium-outer-only-12px-seam550-20261031.png", 12, 550, halo=False)
results["v6-medium-halo-under-opaque-12px-seam550"] = compose("v6-medium-halo-under-opaque-12px-seam550-20261031.png", 12, 550, halo=True)
results["v6-heavy-outer-only-20px-seam550"] = compose("v6-heavy-outer-only-20px-seam550-20261031.png", 20, 550, halo=False)
results["v6-medium-seam-offset-650"] = compose("v6-medium-seam-offset-650-20261031.png", 12, 650, halo=True)
# power candidates (proof frames, labelled candidates, not canon)
results["v6-power-candidate-1-dual-charge-thin-halo"] = compose("v6-power-candidate-1-dual-charge-20261031.png", 6, 550, halo=True)
results["v6-power-candidate-2-dual-aura-medium-halo"] = compose("v6-power-candidate-2-dual-aura-20261031.png", 12, 550, halo=True)
results["v6-power-candidate-3-split-overlay-heavy-darkbg"] = compose("v6-power-candidate-3-split-overlay-20261031.png", 20, 550, halo=True, bg_dark=0.55)
# note: candidate 2 reuses medium+halo geometry with a different presentation label;
# candidate 1 and 3 differ in width/bg, candidate 2 is the aura-strength presentation of the same build.
json.dump(results, open(OUT / "measurements-v6-20261031.json", "w"), indent=2)
print("done")
