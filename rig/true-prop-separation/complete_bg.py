#!/usr/bin/env python3
"""Rebuild the COMPLETE background under the separated props (v2).

The background-complete plate is the Gumball "beauty" layer: the whole
setting with every prop and Jones removed, so any prop can move over it
without revealing a hole, a box, or a ghost.

Why not cv2.inpaint (Telea): on 250-500px holes it marches a diagonal
front and leaves a huge triangle (seen in the v1 attempt). Instead:
  * Narrow runs (<=60px: poles, sign, fence band y<565): horizontal
    interpolation between the nearest real pixels on the row.
  * Wide asphalt runs (car rows, Jones box): same-rows donor — the clean
    asphalt strip x700-895 (no cars, no Jones, same rows, so every
    horizontal parking line continues at the right height) resampled to
    the run width, blended 65% donor / 35% horizontal interp. The donor
    carries real asphalt texture, the interp anchors the local light.
  * The plate's v3 Jones box (x895-1145, y453-860) is rebuilt whole: the
    mirrored-asphalt fill dragged a GHOST of the blue car's rear into the
    box (sliced by the box edge at x1120). The donor here is x700-895 —
    the blue car ends at x667 and the white car behind it ends at y555 —
    so no car can leak in. The ghost is gone.
  * The fill is feathered along the MASK edge (distance-transform ramp
    over 8px), so the seam follows the prop's silhouette, never a box.
  * Parking lines: the diagonal bay line is re-drawn across the filled
    bands from its fitted equation (detected in the original).
  * Shadows are extracted, not left baked in: shadow_alpha =
    (bg_complete_lum - original_lum) / bg_complete_lum where the original
    is darker, clipped to the ground strips under the props, excluding
    the prop footprints — saved as a MULTIPLY layer.
"""
import os, json
import numpy as np
import cv2
from PIL import Image

WD = "/home/hatch/workspace/_cape-jones-parking-lot-2d"
OUT = f"{WD}/true-sep"

def load_layers(board_dir):
    """Prop masks only: the layer names listed in masks.json.
    (The layers/ dir also holds light/grade PNGs for the PSD — those are
    full-frame and must NEVER be treated as prop masks. An earlier run
    globbed the whole dir and 'inpainted' the entire frame.)"""
    layers = {}
    ldir = os.path.join(board_dir, "layers")
    with open(os.path.join(board_dir, "masks.json")) as f:
        names = list(json.load(f)["props"].keys())
    for name in names:
        im = np.asarray(Image.open(os.path.join(ldir, name + ".png")).convert("RGBA"))
        layers[name] = im[..., 3] > 10
    return layers

def row_intervals(mask_row):
    xs = np.where(mask_row)[0]
    if len(xs) == 0:
        return []
    starts, ends = [xs[0]], []
    for i in range(1, len(xs)):
        if xs[i] > xs[i-1] + 1:
            ends.append(xs[i-1]); starts.append(xs[i])
    ends.append(xs[-1])
    return list(zip(starts, ends))

def donor_segments(y, a, b, diag=None):
    """Clean same-row asphalt/fence to resample from, for the run [a,b].
    The old donor x700-895 was contaminated: it holds the stop-sign pole
    (dark vertical -> resampled into a long dark streak with a red edge)
    and the diagonal bay line (resampled to the wrong x -> ghost line).
    This donor excludes the pole and excises the diagonal, and stays
    local to the run so the light matches (left row: centre donor;
    right row: centre + far-right fence donor)."""
    cx = (a + b) // 2
    if cx < 700:
        segs = [(700, 890), (1150, 1220)]
    elif cx < 1200:
        segs = [(700, 890), (1150, 1220)]
    elif y < 565:
        # fence band behind the right row: the far-right fence alone
        # (one segment, no concat seam mid-fill)
        segs = [(1790, 2048)]
    else:
        # below the fence: the concrete barrier + planter wall.
        # NOT the bushes at x1900+ (their dark brown resampled into
        # a long red shelf across the whole row).
        segs = [(1150, 1220), (1790, 1900)]
    out = []
    for (x0, x1) in segs:
        parts = [(x0, x1)]
        # stop-sign pole occupies x768-785, y500-580: never a donor
        if 500 <= y <= 580:
            cut = []
            for (p0, p1) in parts:
                if p1 <= 765 or p0 >= 790:
                    cut.append((p0, p1))
                else:
                    if p0 < 765:
                        cut.append((p0, 765))
                    if p1 > 790:
                        cut.append((790, p1))
            parts = cut
        # diagonal bay line: excise +-5px around its x at this row
        if diag is not None:
            slope, c = diag[0], diag[1]
            xd = int(round((y - c) / slope)) if slope != 0 else -1
            cut = []
            for (p0, p1) in parts:
                if p1 <= xd - 5 or p0 >= xd + 5:
                    cut.append((p0, p1))
                else:
                    if p0 < xd - 5:
                        cut.append((p0, xd - 5))
                    if p1 > xd + 5:
                        cut.append((xd + 5, p1))
            parts = cut
        out.extend(parts)
    # Keep the donor LOCAL and balanced: truncate every segment to at
    # most 90px from the end nearest the interval. Without this the
    # left donor (190px of shaded asphalt) swamped the right donor
    # (70px of sunlit pool) and the Jones fill came out as a dark
    # vertical band in the middle of the lit lot.
    balanced = []
    for (x0, x1) in out:
        if x1 - x0 > 90:
            if (x0 + x1) // 2 < cx:
                x0 = x1 - 90
            else:
                x1 = x0 + 90
        if x1 - x0 > 8:
            balanced.append((x0, x1))
    return balanced

def fill_rows(img, mask, diag=None):
    """Fill every masked pixel, per row.
    Returns (blend, interp_only): `blend` uses the clean same-rows donor
    for wide runs; `interp_only` is pure horizontal interpolation.
    The final image feathers blend -> interp_only towards the mask edge,
    so the seam is continuous (never the original prop pixels)."""
    h, w = mask.shape
    blend = img.astype(np.float32).copy()
    interp_only = img.astype(np.float32).copy()
    for y in range(h):
        for (a, b) in row_intervals(mask[y]):
            n = b - a + 1
            if n > 60 and y < 400:
                # Lamp head / arm hole inside the glow: the glow is
                # bright ABOVE and BELOW the head, dark sky to the sides,
                # so horizontal interp makes a dark slab. Fill vertically
                # (nearest unmasked pixel above and below, per column).
                # A 5px horizontal smoothing across the interval keeps the
                # per-column anchors from stepping at the arm/head join.
                vals = np.zeros((n, 3), np.float32)
                for i, x in enumerate(range(a, b + 1)):
                    y_top = y - 1
                    while y_top >= 0 and mask[y_top, x]:
                        y_top -= 1
                    y_bot = y + 1
                    while y_bot < h and mask[y_bot, x]:
                        y_bot += 1
                    if y_top < 0 or y_bot >= h:
                        continue
                    t = (y - y_top) / max(y_bot - y_top, 1)
                    vals[i] = img[y_top, x].astype(np.float32) * (1 - t) \
                        + img[y_bot, x].astype(np.float32) * t
                if n >= 5:
                    ker = np.ones(5, np.float32) / 5.0
                    for c in range(3):
                        padded = np.pad(vals[:, c], 2, mode="edge")
                        vals[:, c] = np.convolve(padded, ker, mode="valid")
                blend[y, a:b+1] = vals
                interp_only[y, a:b+1] = vals
                continue
            lx = max(a - 1, 0)
            rx = min(b + 1, w - 1)
            t = np.linspace(0, 1, n)[:, None]
            interp = img[y, lx][None, :].astype(np.float32) * (1 - t) \
                + img[y, rx][None, :].astype(np.float32) * t
            interp_only[y, a:b+1] = interp
            if n <= 60:
                blend[y, a:b+1] = interp
            else:
                segs = donor_segments(y, a, b, diag)
                if segs:
                    donor = np.concatenate(
                        [img[y, x0:x1].astype(np.float32) for (x0, x1) in segs], axis=0)
                    donor_rs = cv2.resize(donor[None, :, :], (n, 1),
                                          interpolation=cv2.INTER_LINEAR)[0]
                    # The donor segments have very different brightness
                    # (shaded asphalt vs sunlit pool): a hard concat
                    # leaves a vertical step inside the fill. Blur the
                    # resampled donor along x so it is a smooth gradient.
                    donor_rs = cv2.GaussianBlur(donor_rs[None, :, :], (0, 0), 8)[0]
                    # Match the donor's brightness to the local interp:
                    # the donor may come from a much brighter part of the
                    # lot (the pool) than the hole (shade) — without this
                    # the blue car's old spot filled in as a pale ghost
                    # of the car. Gain is a single scalar per row, so the
                    # donor's texture and gradient are kept.
                    lum_d = float(donor_rs.mean())
                    lum_i = float(interp.mean())
                    if lum_d > 1 and lum_i > 1:
                        gain = float(np.clip(lum_i / lum_d, 0.5, 1.5))
                        donor_rs = donor_rs * gain
                    blend[y, a:b+1] = 0.5 * donor_rs + 0.5 * interp
                else:
                    blend[y, a:b+1] = interp
    return blend, interp_only

def detect_diagonal(img_bgr):
    """Fit the prominent diagonal parking-bay line in the ground."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray[560:1152, 0:2048], 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=120,
                            minLineLength=150, maxLineGap=30)
    best = None
    if lines is not None:
        for l in lines.reshape(-1, 4):
            x1, y1, x2, y2 = (int(v) for v in l)
            y1 += 560; y2 += 560
            if x2 == x1:
                continue
            slope = (y2 - y1) / (x2 - x1)
            length = np.hypot(x2 - x1, y2 - y1)
            # diagonal bay line: shallow negative slope, long, mid-ground
            if -0.45 < slope < -0.08 and length > 250:
                if best is None or length > best[0]:
                    best = (length, slope, x1, y1, x2, y2)
    if best is None:
        return None
    _, slope, x1, y1, x2, y2 = best
    # line: y = slope * x + c; colour = median along the visible segment
    c = y1 - slope * x1
    n = max(abs(x2 - x1), abs(y2 - y1))
    xs = np.linspace(x1, x2, n).astype(int)
    ys = np.linspace(y1, y2, n).astype(int)
    cols = img_bgr[ys, xs]
    col = np.median(cols, axis=0)
    return slope, c, col

def build(board_name, src, board_dir, rebuild_rects=(), extra_inpaint_ellipses=()):
    img = cv2.imread(src)
    assert img is not None, src
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    layers = load_layers(board_dir)
    union = np.zeros(img.shape[:2], np.uint8)
    for m in layers.values():
        union[m] = 255
    for (x0, y0, x1, y1) in rebuild_rects:
        union[y0:y1, x0:x1] = 255
    for (cx, cy, rx, ry) in extra_inpaint_ellipses:
        cv2.ellipse(union, (cx, cy), (rx, ry), 0, 0, 360, 255, -1)
    union_d = cv2.dilate(union, np.ones((9, 9), np.uint8))
    diag = detect_diagonal(img)
    if diag is not None:
        print(f"  {board_name}: diagonal line y = {diag[0]:.3f}x + {diag[1]:.1f}")
    blend, interp_only = fill_rows(img_rgb, union_d > 0, diag)
    # feather blend -> interp_only towards the mask silhouette
    # (distance ramp, 8px): distanceTransform on the MASK gives 0 at the
    # edge, growing inward — so at the edge the fill IS the edge colour,
    # and the donor texture fades in 8px inside the silhouette.
    dist = cv2.distanceTransform((union_d > 0).astype(np.uint8),
                                 cv2.DIST_L2, 5)
    alpha = np.clip(dist / 8.0, 0, 1)[..., None]
    bg_f = blend * alpha + interp_only * (1 - alpha)
    bg_f[union_d == 0] = img_rgb[union_d == 0]
    # redraw the diagonal bay line across the filled bands
    if diag is not None:
        slope, c, col_bgr = diag
        col = np.array([col_bgr[2], col_bgr[1], col_bgr[0]], dtype=np.float32)
        print(f"  {board_name}: diagonal colour {col}")
        for y in range(560, 700):
            x = int(round((y - c) / slope))
            if 0 <= x < 2048 and union_d[y, x] > 0:
                for dy in (-1, 0, 1):
                    for dx in range(-2, 3):
                        xx, yy = x + dx, y + dy
                        if 0 <= xx < 2048 and 0 <= yy < 1152:
                            bg_f[yy, xx] = 0.75 * col + 0.25 * bg_f[yy, xx]
    bg = np.clip(bg_f, 0, 255).astype(np.uint8)
    Image.fromarray(bg).save(os.path.join(board_dir, "background-complete.png"))

    # Shadows (see module docstring).
    orig = img_rgb.astype(np.float32)
    lum_o = orig.mean(axis=2)
    lum_b = bg.astype(np.float32).mean(axis=2)
    shadow = np.clip((lum_b - lum_o) / np.maximum(lum_b, 1.0), 0, 1)
    shadow = cv2.GaussianBlur(shadow, (0, 0), 2.0)
    hard_union = np.zeros(img.shape[:2], np.uint8)
    for m in layers.values():
        hard_union[m] = 255
    for (x0, y0, x1, y1) in rebuild_rects:
        hard_union[y0:y1, x0:x1] = 255
    zone = np.zeros(img.shape[:2], np.uint8)
    zone[615:665, 0:2048] = 255
    cv2.ellipse(zone, (1020, 782), (165, 32), 0, 0, 360, 255, -1)
    zone[600:670, 1710:1760] = 0
    zone[hard_union > 0] = 0
    s = shadow * (zone > 0)
    s[s < 0.08] = 0
    a = (np.clip(s, 0, 1) * 255).astype(np.uint8)
    rgba = np.zeros((*shadow.shape, 4), np.uint8)
    rgba[..., 3] = a
    Image.fromarray(rgba, "RGBA").save(os.path.join(board_dir, "layers", "car_shadows.png"))
    shadow_px = int((a > 0).sum())
    # rest-composite check: bg + props (normal) then shadows (multiply)
    comp = bg.astype(np.float32)
    for name in sorted(layers):
        rgba_l = np.asarray(Image.open(os.path.join(board_dir, "layers", name + ".png")).convert("RGBA")).astype(np.float32)
        al = rgba_l[..., 3:4] / 255.0
        comp = rgba_l[..., :3] * al + comp * (1 - al)
    comp = comp * (1 - s[..., None])
    diff = np.abs(comp - orig).mean()
    print(f"  {board_name}: inpaint px {int((union_d>0).sum())}, "
          f"rest-composite mean abs diff vs original: {diff:.3f}, shadow px {shadow_px}")
    with open(os.path.join(board_dir, "background.json"), "w") as f:
        json.dump({"inpaint_px": int((union_d > 0).sum()),
                   "rest_mean_abs_diff": float(diff),
                   "shadow_px": shadow_px,
                   "diagonal": [float(diag[0]), float(diag[1])] if diag else None}, f, indent=2)
    return bg

if __name__ == "__main__":
    print("== plate")
    build("plate", f"{WD}/rig/plate-sodium.png", f"{OUT}/plate",
          rebuild_rects=[(895, 453, 1145, 860),
                         # lamp arm's lower outline survives as a dark
                         # S-curve wire in the glow (x1700-1770, y182-236):
                         # erase it (vertical interp, bright glow fill)
                         (1700, 182, 1770, 236)])
    print("== cj-pl-01")
    build("cj-pl-01", f"{WD}/repo/production/2d-parking-lot/boards/cj-pl-01.png",
          f"{OUT}/boards/cj-pl-01",
          extra_inpaint_ellipses=[(1020, 782, 165, 32)])
