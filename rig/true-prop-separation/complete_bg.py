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

def fill_rows(img, mask, diag=None, use_donor=True):
    """Fill every masked pixel.
    Two-axis fill (boards 02-07): for each masked pixel, compute BOTH
    the horizontal interpolation (nearest unmasked pixel left/right in
    the row) and the vertical interpolation (nearest unmasked above/
    below in the column), and blend them with a span weight
    w_v = h_span / (h_span + v_span) — the axis whose anchors are
    CLOSER dominates, because that axis carries the scene's real
    structure at that point. Where only one axis has anchors, use it.
    Why not horizontal-only (the board-01 way)? The Jones hole on these
    boards is 40-55% of the frame and spans sky, buildings, fence,
    car rows and asphalt at once. Horizontal-only smears the bright
    lamp glow across the torso (orange band), the suit across the legs
    (white slab) and leaves the head a black blob. The two-axis fill
    keeps the scene's vertical banding (sky -> buildings -> fence ->
    cars -> asphalt) while the horizontal axis keeps the light pools.
    It is a plausible lot, not the true background (unknowable — Jones
    occludes it); the rest composite is unaffected because the props
    cover the holes, and the moved-proof vacated spot reads as empty
    lot. Returns (blend, interp_only): `blend` is the two-axis fill
    (with the clean same-rows donor for wide runs when use_donor is
    set, board-01/plate only); `interp_only` is pure horizontal
    interpolation, used to feather the silhouette edge to the true
    edge colour. The final image feathers blend -> interp_only towards
    the mask edge, so the seam is continuous."""
    h, w = mask.shape
    blend = img.astype(np.float32).copy()
    interp_only = img.astype(np.float32).copy()
    m = mask > 0
    # --- nearest-unmasked anchor maps (vectorised scans) ---
    above = np.full((h, w), -1, np.int32)   # y of nearest unmasked above
    last = np.full(w, -1, np.int32)
    for y in range(h):
        above[y] = last
        last = np.where(~m[y], y, last)
    below = np.full((h, w), -1, np.int32)
    last = np.full(w, -1, np.int32)
    for y in range(h - 1, -1, -1):
        below[y] = last
        last = np.where(~m[y], y, last)
    img_f = img.astype(np.float32)
    xs = np.arange(w)
    for y in range(h):
        for (a, b) in row_intervals(m[y]):
            n = b - a + 1
            lx = max(a - 1, 0)
            rx = min(b + 1, w - 1)
            t = np.linspace(0, 1, n)[:, None]
            # Anchors: the MEDIAN of the 25px run just outside the
            # interval, not the single pixel beside it. The mask can
            # sit a few px short of a prop's true edge (the hand's
            # white ran 7px past the 03 mask, the arm's white 25px
            # past the 02 mask) — a single-pixel anchor then lands ON
            # the figure and poisons the whole row's gradient white.
            # A 25px run is wide enough that the background dominates
            # the median even when the mask is 10px short.
            l_run = img_f[y, max(a - 25, 0):a]
            r_run = img_f[y, b + 1:min(b + 26, w)]
            # Contamination check (board 07): the 25px run beside the
            # mask can be ENTIRELY figure colour when the mask sits
            # short of a wide bright feature (the cape rim-light is
            # 25-35px wide, so the run left of Jones at y550-650 is
            # all rim). Compare with a run 30px further out; if the
            # two medians differ by >40 in luminance, the near run is
            # figure colour and the far run is the real background.
            # Clean runs agree, so accepted boards are unchanged.
            def _anchor(run, far):
                if not len(run):
                    return None
                med = np.median(run, axis=0)
                if len(far):
                    far_med = np.median(far, axis=0)
                    # ONE-DIRECTIONAL: switch only when the near run is
                    # BRIGHTER than the far run. A bright near run is
                    # figure colour leaking past the mask (the 07 rim,
                    # a white suit edge). A near run DARKER than the far
                    # run is real background (the 06 light pool's edge:
                    # dark asphalt beside the arm, brighter pool 30px
                    # further out) — keep it.
                    if float(med.mean()) - float(far_med.mean()) > 40:
                        return far_med
                return med
            l_far = img_f[y, max(a - 55, 0):max(a - 30, 0)] if a > 30 else l_run
            r_far = img_f[y, min(b + 31, w):min(b + 56, w)] if b < w - 31 else r_run
            l_col = _anchor(l_run, l_far)
            if l_col is None:
                l_col = img_f[y, lx]
            r_col = _anchor(r_run, r_far)
            if r_col is None:
                r_col = img_f[y, rx]
            # Frame-touching interval (board 04: Jones touches the top,
            # left AND bottom edges, so a whole column has no vertical
            # anchors and the left "anchor" is the figure itself — the
            # cowl purple on top rows, the white sleeve below). There is
            # no background on that side: fall back to the opposite
            # anchor (a constant from the real background) instead of
            # smearing the figure's own colours across the hole.
            if a == 0:
                l_col = r_col.copy()
            if b >= w - 1:
                r_col = l_col.copy()
            interp = l_col[None, :] * (1 - t) + r_col[None, :] * t
            interp_only[y, a:b+1] = interp
            # --- vertical interpolation for this interval ---
            seg = slice(a, b + 1)
            yt = above[y, seg]
            yb = below[y, seg]
            v_ok = (yt >= 0) & (yb >= 0)
            v_span = np.where(v_ok, yb - yt, 0)
            h_span = max(rx - lx, 1)
            w_v = np.where(v_ok, h_span / (h_span + v_span), 0.0)
            vert = np.zeros((n, 3), np.float32)
            # Vertical anchors are MEDIANS of the 10px run just outside
            # the mask edge, not the single pixel beside it — the mask
            # can sit a few px short of a prop's true edge (the 06
            # shoulder's white ran 1px past the mask, so the single
            # above-anchor pixel WAS the suit and the whole column
            # filled white). The median over 10px rejects the sliver.
            def _med_anchor(rows, cols, direction):
                stack = [img_f[np.clip(rows + direction * k, 0, h - 1), cols]
                         for k in range(10)]
                return np.median(np.stack(stack), axis=0)
            # One-sided columns (the Jones hole runs to the frame bottom,
            # so most of his columns have NO below anchor): extend the
            # single available anchor, but as a VERTICAL GRADIENT, not a
            # constant — a constant paints the sky's colour all the way
            # down the legs and reads as a flat stripe. The gradient
            # runs from the above anchor (sky/buildings, w_v 0.75) at
            # the hole's top to the row's own horizontal interp
            # (asphalt, w_v 0.25) at the frame bottom, so the fill goes
            # sky -> buildings -> asphalt like the real lot.
            one_above = (~v_ok) & (yt >= 0)
            one_below = (~v_ok) & (yt < 0) & (yb >= 0)
            # Disagreement guard (board 07): when the vertical anchor
            # is BRIGHTER than the row's horizontal interp by >50 in
            # luminance, trust the HORIZONTAL interp (w_v=0). A bright
            # vertical anchor is almost always figure colour leaking
            # past the mask (the 07 cape rim-light, which smeared into
            # a purple streak). A dark anchor is kept — the background
            # there is dark anyway (the 06 cape's black anchor is
            # closer to the dark lot than the mid-grey interp).
            if one_above.any():
                anc = _med_anchor(yt[one_above], xs[seg][one_above], -1)
                vert[one_above] = anc
                t_ab = (y - yt[one_above]) / np.maximum(h - 1 - yt[one_above], 1)
                w_ab = 0.75 - 0.5 * t_ab
                disagree = (anc.mean(axis=1) - interp[one_above].mean(axis=1)) > 50
                w_ab[disagree] = 0.0
                w_v[one_above] = w_ab
            if one_below.any():
                anc = _med_anchor(yb[one_below], xs[seg][one_below], +1)
                vert[one_below] = anc
                t_be = (yb[one_below] - y) / np.maximum(yb[one_below], 1)
                w_be = 0.75 - 0.5 * t_be
                disagree = (anc.mean(axis=1) - interp[one_below].mean(axis=1)) > 50
                w_be[disagree] = 0.0
                w_v[one_below] = w_be
            if v_ok.any():
                tv = ((y - yt) / np.maximum(v_span, 1))[:, None]
                top_col = _med_anchor(yt, xs[seg], -1)
                bot_col = _med_anchor(yb, xs[seg], +1)
                vert = np.where(v_ok[:, None],
                                top_col * (1 - tv) + bot_col * tv, vert)
                # 5px horizontal smoothing on the two-sided part only:
                # the per-column top/bottom anchors can step where a
                # narrow prop (arm, pole) ends.
                # 5px horizontal smoothing: the per-column top/bottom
                # anchors can step where a narrow prop (arm, pole) ends.
                if n >= 5:
                    ker = np.ones(5, np.float32) / 5.0
                    for c in range(3):
                        padded = np.pad(vert[:, c], 2, mode="edge")
                        sm = np.convolve(padded, ker, mode="valid")
                        vert[:, c] = np.where(v_ok, sm, vert[:, c])
            two_axis = interp * (1 - w_v[:, None]) + vert * w_v[:, None]
            if n <= 60 or not use_donor:
                blend[y, a:b+1] = two_axis
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
    # line: y = slope * x + c; colour: the Hough segment follows the
    # stripe's EDGE (Canny), so the pixels on the line itself are the
    # asphalt/line boundary (nearly black — the old code redrew a dark
    # line). Sample a +-5px band around the line and keep only warm
    # stripe-like pixels (BGR: R high, B low); fall back to the plain
    # median if there are none.
    c = y1 - slope * x1
    # Colour: the stripe is a BRIGHT painted line on dark asphalt, so
    # sample the median of the pixels along the full line (with a +-5px
    # band) that are clearly brighter than the band's own median
    # luminance — that is the stripe itself, whether it is yellow
    # (board 02), lavender (board 05) or white. The plain median along
    # the line is mostly dark asphalt (the Hough segment follows the
    # stripe's edge) and redrew a dark line.
    xs = np.arange(0, 2048)
    ys = np.round(slope * xs + c).astype(int)
    ok = (ys >= 0) & (ys < 1152)
    band = []
    for dy in range(-5, 6):
        yy = np.clip(ys[ok] + dy, 0, 1151)
        band.append(img_bgr[yy, xs[ok]].astype(np.float32))
    cols = np.concatenate(band, axis=0)
    lum = cols.mean(axis=1)
    # Bright AND saturated: the stripe is a coloured line (yellow on
    # 02, lavender on 05). Brightness alone also catches the white
    # suit where the fitted line passes under Jones, and the median
    # then comes out white. Saturation rejects the suit (neutral
    # white/grey) and the asphalt (dark).
    sat = cols.max(axis=1) - cols.min(axis=1)
    stripe = cols[(lum > np.median(lum) + 30) & (sat > 40)]
    col = np.median(stripe, axis=0) if len(stripe) >= 20 else np.median(cols, axis=0)
    return slope, c, col

def build(board_name, src, board_dir, rebuild_rects=(), extra_inpaint_ellipses=(),
          use_donor=True, use_diag=True, diag_y_range=(560, 700),
          shadow_zones=None, shadow_ellipses=()):
    """shadow_zones: list of (x0,y0,x1,y1) ground strips under the props
    where contact shadows are extracted (board-01 default: the y615-665
    strip + the Jones-feet ellipse). Boards 02-07 pass their own strips
    (Jones is cropped at the frame bottom on 02/03/06/07, so he casts no
    ground shadow there; 05 is the only board where his feet touch the
    ground)."""
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
    diag = detect_diagonal(img) if use_diag else None
    if diag is not None:
        print(f"  {board_name}: diagonal line y = {diag[0]:.3f}x + {diag[1]:.1f}")
    blend, interp_only = fill_rows(img_rgb, union_d > 0, diag, use_donor)
    # Soften the fill inside the mask (sigma 15): the per-column /
    # per-row anchors leave sharp vertical/horizontal band edges
    # exactly where the figure's silhouette was, and the eye reads
    # those edges as the figure's ghost. A 15px blur removes the
    # edges while keeping the broad light/dark structure (dark
    # buildings left, lamp glow right, sunlit pool right). The blur
    # is restricted to the mask — the original outside is untouched.
    blend = np.where((union_d > 0)[..., None],
                     cv2.GaussianBlur(blend, (0, 0), 15), blend)
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
        for y in range(diag_y_range[0], diag_y_range[1]):
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
    if shadow_zones is None:
        # board-01 / plate default
        zone[615:665, 0:2048] = 255
        cv2.ellipse(zone, (1020, 782), (165, 32), 0, 0, 360, 255, -1)
        zone[600:670, 1710:1760] = 0
    else:
        for (x0, y0, x1, y1) in shadow_zones:
            zone[y0:y1, x0:x1] = 255
    for (cx, cy, rx, ry) in shadow_ellipses:
        cv2.ellipse(zone, (cx, cy), (rx, ry), 0, 0, 360, 255, -1)
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
    import sys
    targets = sys.argv[1:] or ["plate", "cj-pl-01"]
    B = f"{WD}/repo/production/2d-parking-lot/boards"
    # Per-board background config for 02-07 (see build() docstring):
    # interp-only fill (no donor — Jones spans sky/buildings/asphalt at
    # once), no diagonal unless noted, shadow strips under each prop row.
    BG = {
      "cj-pl-02": dict(use_donor=False, use_diag=True, diag_y_range=(830, 1030),
                       shadow_zones=[(0, 675, 420, 730), (1460, 680, 2048, 735)]),
      "cj-pl-03": dict(use_donor=False, use_diag=False,
                       shadow_zones=[(0, 820, 520, 880), (1147, 650, 2048, 700)]),
      "cj-pl-04": dict(use_donor=False, use_diag=False,
                       shadow_zones=[(1455, 810, 2048, 870)]),
      "cj-pl-05": dict(use_donor=False, use_diag=True, diag_y_range=(560, 700),
                       shadow_zones=[(850, 940, 1200, 990)],
                       shadow_ellipses=[(1025, 955, 150, 22)]),
      "cj-pl-06": dict(use_donor=False, use_diag=False,
                       shadow_zones=[(0, 840, 820, 900), (1640, 840, 2048, 900)]),
      "cj-pl-07": dict(use_donor=False, use_diag=False,
                       shadow_zones=[(0, 320, 400, 370), (1230, 390, 1425, 440),
                                     (1737, 510, 2048, 560), (0, 410, 670, 450)]),
    }
    if "plate" in targets:
        print("== plate")
        build("plate", f"{WD}/rig/plate-sodium.png", f"{OUT}/plate",
              rebuild_rects=[(895, 453, 1145, 860),
                             # lamp arm's lower outline survives as a dark
                             # S-curve wire in the glow (x1700-1770, y182-236):
                             # erase it (vertical interp, bright glow fill)
                             (1700, 182, 1770, 236)])
    if "cj-pl-01" in targets:
        print("== cj-pl-01")
        build("cj-pl-01", f"{B}/cj-pl-01.png",
              f"{OUT}/boards/cj-pl-01",
              extra_inpaint_ellipses=[(1020, 782, 165, 32)])
    for t in targets:
        if t in BG:
            print("==", t)
            kw = dict(BG[t])
            if t == "cj-pl-05":
                # Jones's contact shadow under his boots: inpaint it so
                # the shadow layer (not the bg) carries it.
                build(t, f"{B}/{t}.png", f"{OUT}/boards/{t}",
                      extra_inpaint_ellipses=[(1025, 955, 150, 22)], **kw)
            else:
                build(t, f"{B}/{t}.png", f"{OUT}/boards/{t}", **kw)
