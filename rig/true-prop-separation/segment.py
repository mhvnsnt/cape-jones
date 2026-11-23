#!/usr/bin/env python3
"""True prop separation for Cape Jones PURPLE LOT boards (v2).

Method (NOT box cuts): every prop is cut along the art's own edges.
  * grabCut props (cars, Jones): a hand-measured polygon traces the prop
    ~5px outside its true edge; grabCut segments the true silhouette
    inside it; the result is CLAMPED to the polygon dilated 6-8px, so it
    can never leak into the background the way v1's first pass did.
    Sure-background seeds pin the asphalt below the tires and the fence
    above the rooflines.
  * traced props (lamps, stop sign): thin/geometric objects whose edges
    are straight lines and ellipses. The mask IS the traced outline
    (pole rect, head ellipse, sign octagon), feathered 1px. No grabCut,
    no glow: the lamp glow is a light layer, not part of the prop.
  * Masks are saved as full-frame RGBA — alpha follows the silhouette,
    never a box. Background underneath is rebuilt by complete_bg.py.

Source art: production/2d-parking-lot/boards/cj-pl-0N.png (the original
drawings) and rig/plate-sodium.png (the flat V2 plate, itself built from
board 01). There are no hidden layers in the boards — they are flat RGB
drawings — so "re-sliced from the board art" means edge-following
segmentation of the board art itself, not recovery of layers that never
existed. Overlapping car rows cannot be split car-by-car: the cars occlude
each other and their shared edges do not exist in the drawing, so each row
is ONE cluster layer whose outer silhouette follows the cars' real edges.
"""
import os, json, math
import numpy as np
import cv2
from PIL import Image

WD = "/home/hatch/workspace/_cape-jones-parking-lot-2d"
BOARDS = f"{WD}/repo/production/2d-parking-lot/boards"
OUT = f"{WD}/true-sep"

def ellipse_poly(cx, cy, rx, ry, n=24):
    return [(int(cx + rx * math.cos(2 * math.pi * i / n)),
             int(cy + ry * math.sin(2 * math.pi * i / n))) for i in range(n)]

# Shared plate/board-01 prop specs (plate == board 01 minus Jones).
PLATE_PROPS = {
  "cars_left_row": dict(method="grabcut", clamp=3,
    poly=[(0,568),(25,555),(90,544),(180,539),(260,536),(340,534),(400,539),(422,552),(422,636),(0,636)],
    seeds_fg=[(60,590,12),(180,590,12),(300,585,12),(390,590,10)],
    seeds_bg=[(100,522,8),(300,518,8),(100,648,10),(300,648,10)], erode=10),
  "blue_car_mid": dict(method="grabcut", clamp=3,
    # Hood top edge measured from the 3x zoom: leading edge y572@435,
    # windshield base y545@505, roof y537@600. The white car behind the
    # roof (y520-545, x590-690) is NOT the blue car: bg seeds pin it out.
    poly=[(435,572),(450,566),(475,556),(505,545),(545,538),(600,537),(640,544),(663,560),(668,595),(665,610),(655,614),(460,614),(442,606)],
    seeds_fg=[(500,590,14),(580,585,14),(640,600,10),(520,605,10)],
    seeds_bg=[(620,528,8),(665,525,6),(460,548,10),(480,540,6),(550,630,10),(420,600,8)], erode=10),
  "cars_right_row": dict(method="grabcut", clamp=3,
    poly=[(1225,562),(1290,542),(1380,533),(1480,529),(1580,526),(1680,529),(1755,542),(1775,562),(1775,636),(1225,636)],
    seeds_fg=[(1300,590,12),(1450,590,12),(1600,590,14),(1720,595,12)],
    seeds_bg=[(1400,514,8),(1650,510,8),(1400,648,10),(1650,648,10),(1758,580,4),(1734,635,8)], erode=10),
  "stop_sign": dict(method="traced", shapes=[
    {"poly": [(788,490),(784,502),(773,506),(762,502),(758,490),(762,478),(773,474),(784,478)]},
    {"poly": [(768,500),(785,500),(785,576),(768,576)]},
    {"poly": ellipse_poly(776, 576, 11, 4, 12)}]),
  "street_lamp_right": dict(method="traced", shapes=[
    # CORRECTED 2026-11-23 (pixel profiles, not the eyeballed zoom): the
    # pole is at x1752-1767, NOT x1727-1738 — the first trace caught sky
    # and left the real pole standing in the background. Brightest-pixel
    # trace: lit edge x1756, y280-560; base widens left below y613.
    {"poly": ellipse_poly(1666, 205, 46, 13)},
    {"poly": [(1688,196),(1720,186),(1756,180),(1758,196),(1725,202),(1692,208)]},
    {"poly": [(1752,182),(1767,182),(1767,615),(1752,615)]},
    {"poly": [(1719,612),(1748,612),(1748,662),(1719,662)]}]),
  "street_lamp_far": dict(method="traced", shapes=[
    {"poly": ellipse_poly(606, 386, 20, 8)},
    {"poly": [(588,384),(600,378),(614,380),(612,390),(596,392)]},
    {"poly": [(584,388),(594,388),(594,540),(584,540)]}]),
}

JONES_01 = dict(method="grabcut", clamp=3,
  # Measured from the board (pixel profiles, not the downscaled preview):
  # head top y497, cowl x1000-1055; shoulders flare only BELOW y560;
  # cape left edge x965@600 -> 944@700, right edge x1080@600 -> 1075@700;
  # cape tips end y745; boots end y776. Above y560 the polygon stays
  # narrow (head+neck only) so grabCut cannot eat the fence behind the
  # shoulders; below the boots bg seeds pin the ground shadow out.
  poly=[(992,505),(1000,497),(1046,497),(1056,508),(1062,535),(1068,560),(1080,600),(1072,650),(1078,700),(1070,745),(1058,762),(1046,774),(1016,774),(1010,758),(1002,774),(972,774),(962,760),(948,745),(942,700),(950,650),(962,600),(968,570),(978,545),(986,520)],
  seeds_fg=[(1000,650,15),(1000,740,12),(1015,515,10),(1015,545,8),(955,680,8),(1065,680,8)],
  seeds_bg=[(920,700,8),(1100,700,8),(1015,482,8),(955,768,6),(1062,768,6),(1009,768,5),(960,792,8),(1010,795,8),(1060,792,8)], erode=6)

SPECS = {
  "plate": {
    "src": f"{WD}/rig/plate-sodium.png",
    "props": dict(PLATE_PROPS),
    # make_plates.py v3 painted Jones out with a BOX (x920-1120, y478-835):
    # horizontal interp + mirrored asphalt. The mirror dragged the blue
    # car's rear into the box (ghost car sliced by the box edge at x1120)
    # and left a visible rectangle. Rebuild the whole box, not just Jones.
    "rebuild_rects": [(895, 453, 1145, 860)],
  },
  "cj-pl-01": {
    "src": f"{BOARDS}/cj-pl-01.png",
    "props": dict(PLATE_PROPS, jones=JONES_01),
    "rebuild_rects": [],
  },
}

# ---------------------------------------------------------------- helpers
def grabcut_poly(img_bgr, spec):
    poly = np.array(spec["poly"], dtype=np.int32)
    x0, y0 = max(0, poly[:, 0].min() - 20), max(0, poly[:, 1].min() - 20)
    x1, y1 = min(img_bgr.shape[1], poly[:, 0].max() + 20), min(img_bgr.shape[0], poly[:, 1].max() + 20)
    crop = img_bgr[y0:y1, x0:x1]
    ch, cw = crop.shape[:2]
    lp = poly - np.array([x0, y0])
    mask = np.full((ch, cw), cv2.GC_PR_BGD, np.uint8)
    cv2.fillPoly(mask, [lp], cv2.GC_PR_FGD)
    pm = np.zeros((ch, cw), np.uint8)
    cv2.fillPoly(pm, [lp], 255)
    e = spec.get("erode", 8)
    er = cv2.erode(pm, np.ones((2 * e + 1, 2 * e + 1), np.uint8))
    mask[er > 0] = cv2.GC_FGD
    for (x, y, r) in spec.get("seeds_fg", []):
        cv2.circle(mask, (x - x0, y - y0), r, cv2.GC_FGD, -1)
    for (x, y, r) in spec.get("seeds_bg", []):
        cv2.circle(mask, (x - x0, y - y0), r, cv2.GC_BGD, -1)
    bgd = np.zeros((1, 65), np.float64)
    fgd = np.zeros((1, 65), np.float64)
    cv2.grabCut(crop, mask, None, bgd, fgd, 5, cv2.GC_INIT_WITH_MASK)
    fg_crop = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    fg = np.zeros(img_bgr.shape[:2], np.uint8)
    fg[y0:y1, x0:x1] = fg_crop
    # clamp: never more than `clamp` px outside the traced polygon
    cl = spec.get("clamp", 8)
    pm_full = np.zeros(img_bgr.shape[:2], np.uint8)
    cv2.fillPoly(pm_full, [poly], 255)
    allowed = cv2.dilate(pm_full, np.ones((2 * cl + 1, 2 * cl + 1), np.uint8))
    fg[allowed == 0] = 0
    return fg

def traced_mask(img_shape, spec):
    m = np.zeros(img_shape[:2], np.uint8)
    for sh in spec["shapes"]:
        cv2.fillPoly(m, [np.array(sh["poly"], dtype=np.int32)], 255)
    return m

def refine(fg):
    h, w = fg.shape
    ff = fg.copy()
    flood = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(ff, flood, (0, 0), 128)
    fg[ff == 0] = 255
    n, lab, stats, _ = cv2.connectedComponentsWithStats((fg > 0).astype(np.uint8), 8)
    if n > 1:
        areas = stats[1:, cv2.CC_STAT_AREA]
        biggest = 1 + int(np.argmax(areas))
        keep = np.zeros_like(fg)
        for i in range(1, n):
            if i == biggest or stats[i, cv2.CC_STAT_AREA] >= 0.005 * stats[biggest, cv2.CC_STAT_AREA]:
                keep[lab == i] = 255
        fg = keep
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    return fg

def soft_alpha(fg):
    a = cv2.GaussianBlur(fg.astype(np.float32), (0, 0), 0.8)
    return np.clip(a, 0, 255).astype(np.uint8)

def run_board(name, spec):
    img = cv2.imread(spec["src"])
    assert img is not None, spec["src"]
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    outdir = os.path.join(OUT, "boards", name) if name.startswith("cj-") else os.path.join(OUT, name)
    layers_dir = os.path.join(outdir, "layers")
    os.makedirs(layers_dir, exist_ok=True)
    report = {"board": name, "src": spec["src"], "props": {}}
    qa = rgb.copy()
    for pname, pspec in spec["props"].items():
        if pspec["method"] == "grabcut":
            fg = grabcut_poly(img, pspec)
            fg = refine(fg)
        else:
            fg = traced_mask(img.shape, pspec)
        alpha = soft_alpha(fg)
        rgba = np.dstack([rgb, alpha])
        Image.fromarray(rgba, "RGBA").save(os.path.join(layers_dir, pname + ".png"))
        ys, xs = np.where(fg > 0)
        report["props"][pname] = {
            "method": pspec["method"],
            "pixels": int((fg > 0).sum()),
            "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
        }
        cnts, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        overlay = qa.copy()
        cv2.drawContours(overlay, cnts, -1, (255, 0, 255), 2)
        cv2.fillPoly(overlay, cnts, (255, 0, 255))
        qa = cv2.addWeighted(overlay, 0.30, qa, 0.70, 0)
        cv2.drawContours(qa, cnts, -1, (255, 0, 255), 2)
        print(f"  {name}/{pname}: {(fg>0).sum()} px bbox {report['props'][pname]['bbox']}", flush=True)
    Image.fromarray(qa).save(os.path.join(outdir, "mask-qa.png"))
    with open(os.path.join(outdir, "masks.json"), "w") as f:
        json.dump(report, f, indent=2)
    return report

if __name__ == "__main__":
    import sys
    targets = sys.argv[1:] or ["plate", "cj-pl-01"]
    for t in targets:
        print("==", t, flush=True)
        run_board(t, SPECS[t])
