#!/usr/bin/env python3
"""STRICT ISOLATED 90-DEGREE ELBOW PASS (PIL cross-check, 2026-11-01).
Single arm only. NO torso, NO head, NO other limb, NO source motion,
NO crossing: the canvas contains exactly one upper piece, one lower
piece (forearm+gauntlet+fist whole; wrist never cut) and one cap disc.
Geometry follows rig-chains build_chains.py exactly (same anchors,
same ball centres), at native piece scale 1.0 so gaps read in piece px:
  ARM (build_chains.ARM): L ball (60,222) shoulder-anchor (76,30);
                          R ball (99,222) shoulder-anchor (76,30).
  Lower ball centres (cutlimbs builder, measured): L (60,15), R (99,15).
Rotation method (per task rule): the lower piece is pasted onto a
FULL-CANVAS layer twice canvas size, rotated about the elbow pivot,
then the centre canvas is cropped back out. The piece itself is NEVER
rotated in place, never with expand on the piece, never cropped at
piece level. Alpha-count preservation after rotation is checked.
Gap metric (stated, not hidden): inside a disc of radius 30px around
the elbow pivot, gap_px = longest consecutive transparent run along
any row, column, or diagonal through the disc (0 iff disc fully
covered). Coverage % at r=22 and r=30 is reported alongside, with and
without the cap disc, so the cap cannot silently hide a gap: the
without-cap row is the strict row.
Shoulder S=(450,200) on a 900x900 canvas, gray #808080 background
for stills; measurements use the alpha channel of the same composite.
"""
import os, json, math
import numpy as np
from PIL import Image

ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
CUT = os.path.join(ROOT, "cut-limbs-v7c")
OUT = "/var/tmp/elbow-sole-20261101/elbow"
os.makedirs(OUT, exist_ok=True)
W = H = 900
SHOULDER = (450, 200)
BG = (128, 128, 128, 255)

ARMS = {
    "Front": {"upper": "Arm_Front_Upper.png", "lower": "Arm_Front_Lower.png",
              "cap": "Arm_Front_Cap.png", "ball": (60, 222), "anchor": (76, 30),
              "lower_ball": (60, 15)},
    "Back": {"upper": "Arm_Back_Upper.png", "lower": "Arm_Back_Lower.png",
             "cap": "Arm_Back_Cap.png", "ball": (99, 222), "anchor": (76, 30),
             "lower_ball": (99, 15)},
}

def load(name):
    return Image.open(os.path.join(CUT, name)).convert("RGBA")

def rotate_layer_fullcanvas(piece, paste_xy, pivot, angle):
    """Paste piece on a 2x layer, rotate about pivot, crop centre canvas.
    Returns (canvas-size RGBA layer, alpha-preservation info)."""
    layer2 = Image.new("RGBA", (2 * W, 2 * H), (0, 0, 0, 0))
    layer2.alpha_composite(piece, (paste_xy[0] + W // 2, paste_xy[1] + H // 2))
    before = float(np.asarray(layer2)[:, :, 3].sum())
    piv2 = (pivot[0] + W // 2, pivot[1] + H // 2)
    rot = layer2.rotate(angle, center=piv2, expand=False, resample=Image.BICUBIC)
    after = float(np.asarray(rot)[:, :, 3].sum())
    out = rot.crop((W // 2, H // 2, W // 2 + W, H // 2 + H))
    return out, (after / before if before else 0.0)

def _longest_false_run(art_1d, mask_1d):
    """Longest consecutive False in art_1d restricted to mask_1d True cells.
    Cells outside the mask break runs. Vectorised run-length via diff."""
    if not mask_1d.any():
        return 0
    vals = np.where(mask_1d, art_1d, True)  # outside-mask cells act as art
    # Transparent runs in (~vals): pad with 0 (art) both ends so every
    # run yields a +1 start followed by a -1 end, correctly paired.
    d = np.diff(np.concatenate(([0], (~vals).astype(np.int8), [0])))
    starts = np.where(d == 1)[0]
    ends = np.where(d == -1)[0]
    if len(starts) == 0:
        return 0
    return int((ends - starts).max())

def disc_metrics(alpha, cx, cy, r):
    # Crop to the disc bounding box: all scans below are <= (2r+1)^2 cells.
    x0, x1 = max(0, cx - r), min(W, cx + r + 1)
    y0, y1 = max(0, cy - r), min(H, cy + r + 1)
    yy, xx = np.mgrid[y0:y1, x0:x1]
    disc = (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r
    art = (alpha[y0:y1, x0:x1] > 10)
    cov = float(art[disc].mean() * 100)
    bg = int((~art[disc]).sum())
    gap = 0
    for row in range(art.shape[0]):
        gap = max(gap, _longest_false_run(art[row], disc[row]))
    for col in range(art.shape[1]):
        gap = max(gap, _longest_false_run(art[:, col], disc[:, col]))
    for off in range(-art.shape[0] + 1, art.shape[1]):
        gap = max(gap, _longest_false_run(np.diagonal(art, offset=off),
                                          np.diagonal(disc, offset=off)))
        gap = max(gap, _longest_false_run(np.diagonal(np.fliplr(art), offset=off),
                                          np.diagonal(np.fliplr(disc), offset=off)))
    return round(cov, 2), bg, int(gap)

def build(arm, angle, direction, with_cap=True, pivot_override=None):
    cfg = ARMS[arm]
    up = load(cfg["upper"]); low = load(cfg["lower"]); cap = load(cfg["cap"])
    ball, anchor = cfg["ball"], cfg["anchor"]
    vec = (ball[0] - anchor[0], ball[1] - anchor[1])  # px, y down
    elbow = (SHOULDER[0] + vec[0], SHOULDER[1] + vec[1])
    lb = pivot_override or cfg["lower_ball"]
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.alpha_composite(up, (SHOULDER[0] - anchor[0], SHOULDER[1] - anchor[1]))
    up_alpha = np.asarray(canvas)[:, :, 3].copy()
    low_layer, preserve = rotate_layer_fullcanvas(
        low, (elbow[0] - lb[0], elbow[1] - lb[1]), elbow, direction * angle)
    low_alpha = np.asarray(low_layer)[:, :, 3]
    canvas.alpha_composite(low_layer)
    nocap_alpha = np.asarray(canvas)[:, :, 3].copy()
    if with_cap:
        canvas.alpha_composite(cap, (elbow[0] - cap.size[0] // 2,
                                     elbow[1] - cap.size[1] // 2))
    # upper/lower overlap inside r=40 disc around elbow (no-cap masks)
    yy, xx = np.mgrid[0:H, 0:W]
    disc40 = (xx - elbow[0]) ** 2 + (yy - elbow[1]) ** 2 <= 40 * 40
    overlap = int(((up_alpha > 10) & (low_alpha > 10) & disc40).sum())
    m = {"arm": arm, "angle": angle, "direction": direction,
         "elbow_px": list(elbow), "lower_pivot_px": list(lb),
         "alpha_preserve_pct": round(preserve * 100, 2),
         "upper_lower_overlap_r40_px": overlap}
    for label, alpha in (("with_cap", np.asarray(canvas)[:, :, 3]),
                         ("without_cap", nocap_alpha)):
        c22, b22, g22 = disc_metrics(alpha, elbow[0], elbow[1], 22)
        c30, b30, g30 = disc_metrics(alpha, elbow[0], elbow[1], 30)
        m[label] = {"cover_r22_pct": c22, "bg_r22_px": b22, "gap_r22_px": g22,
                    "cover_r30_pct": c30, "bg_r30_px": b30, "gap_r30_px": g30}
    # still (gray background, with cap)
    still = Image.new("RGBA", (W, H), BG)
    still.alpha_composite(canvas)
    return still, m

results = []
for arm in ("Front", "Back"):
    for angle in (0, 45, 90):
        for direction in (1, -1):
            still, m = build(arm, angle, direction, with_cap=True)
            d = "plus" if direction == 1 else "minus"
            still.save(os.path.join(OUT, f"elbow_{arm}_{angle:02d}_{d}.png"))
            results.append(m)
            print(arm, angle, d, "elbow", m["elbow_px"],
                  "with_cap r30", m["with_cap"]["cover_r30_pct"],
                  "gap", m["with_cap"]["gap_r30_px"],
                  "| without_cap r30", m["without_cap"]["cover_r30_pct"],
                  "gap", m["without_cap"]["gap_r30_px"],
                  "| overlap_r40", m["upper_lower_overlap_r40_px"],
                  "| preserve", m["alpha_preserve_pct"])
# pivot sensitivity at 90 deg, Front, both directions, pivots (62,15),(60,10),(60,20)
sens = []
for piv in ((62, 15), (60, 10), (60, 20)):
    for direction in (1, -1):
        _, m = build("Front", 90, direction, with_cap=True, pivot_override=piv)
        sens.append(m)
        print("SENS Front 90 pivot", piv, "dir", direction,
              "with_cap gap_r30", m["with_cap"]["gap_r30_px"],
              "without_cap gap_r30", m["without_cap"]["gap_r30_px"],
              "without_cap cover_r30", m["without_cap"]["cover_r30_pct"])
json.dump({"method": "PIL full-canvas-layer rotation, single arm, no torso, "
                      "no source motion; gap_px = longest transparent run "
                      "inside r30 disc; wrist never cut",
           "results": results, "pivot_sensitivity_90_Front": sens},
          open(os.path.join(OUT, "elbow_pil_measurements.json"), "w"), indent=1)
print("PIL DONE", len(results), "renders +", len(sens), "sensitivity")
