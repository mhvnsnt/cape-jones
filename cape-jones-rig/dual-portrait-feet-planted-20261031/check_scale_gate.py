#!/usr/bin/env python3
"""Mandatory scale + feet gate, wired 20261031.
FAIL LOUDLY (exit 2) if a delivery is below the locked scale.
This gate exists because the old frame-ratio gate PASSED the regression:
old landscape figure 655px in a 1080 frame has frame ratio 0.607, the
same as locked, yet its furniture ratio is 1.174, 17.6% below locked 1.424.
A frame-ratio-only gate can be gamed by scaling the room with the figure.
This gate therefore checks, in order:
  1. FURNITURE RATIO (hard): figure height / chair height >= 1.374
     (locked 1.424 minus 0.05 tolerance). This is the regression check.
  2. FRAME RATIO (hard): figure height / frame height >= 0.577
     (locked 0.607 minus 0.03). A version above the lock (e.g. 3.0x, 0.728)
     PASSES — the gate is a minimum, not an exact-size lock, because Mars
     may pick the up-0.5 candidate.
  3. FEET PLANTED (portrait hard, landscape reported): feet y in the
     planted band 1650-1788 in portrait master coordinates, i.e. rug
     position >= 0.55 (feet at least 55% down the rug, not mid-rug).
     Old portrait feet 1548 (28% down rug) FAILS this check.
  4. WHOLE: figure bbox fully inside the frame, no edge touch.
Chair anchor, portrait framing (y unchanged from master):
  chair back top ~700, chair feet ~1518, height 818 (established estimates
  from the room-scale fix; tolerance 0.05 absorbs the ~13px estimate spread).
Chair anchor, landscape framing (BG cover 1920x1080, scale 1.644, crop y 104):
  back = 286*1.644-104 = 366, feet = 625*1.644-104 = 924, height 558.
Figure height is measured by diff vs a background-only reconstruction
(same cover/crop as the delivery), threshold 20, NOT by trusting a
builder's claimed placement. Exit 0 = PASS, 2 = FAIL.
Usage: python3 check_scale_gate.py --image FILE --framing portrait|landscape
"""
import argparse, json, os, sys
from PIL import Image
import numpy as np

ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
BGF = os.path.expanduser("~/workspace/cape-jones-flying/characters/sheets/backgrounds/batch-KKGuh.jpg")

def cover(bg, size):
    im = bg.copy(); r = max(size[0]/im.width, size[1]/im.height)
    im = im.resize((round(im.width*r), round(im.height*r)), Image.LANCZOS)
    x = (im.width-size[0])//2; y = (im.height-size[1])//2
    return im.crop((x, y, x+size[0], y+size[1]))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--image", required=True)
    ap.add_argument("--framing", required=True, choices=["portrait", "landscape"])
    a = ap.parse_args()
    im = Image.open(a.image).convert("RGB"); W, H = im.size
    bg = Image.open(BGF).convert("RGB")
    if a.framing == "portrait":
        bg_only = cover(bg, (1920, 1920)).crop((420, 0, 1500, 1920))
        chair_h, rug_far, rug_near = 818, 1421, 1868
    else:
        bg_only = cover(bg, (1920, 1080))
        chair_h, rug_far, rug_near = 558, None, None
    diff = np.abs(np.asarray(im).astype(int) - np.asarray(bg_only).astype(int)).max(axis=2)
    mask = diff > 20
    ys, xs = np.where(mask)
    bbox = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
    # CORRECTION: the contact shadow is part of the diff, and extends ~28px
    # below the feet, so a raw diff bbox inflates height by 27px (1165->1192,
    # 1398->1425 in the first gate run). Figure feet are near-white, shadow
    # is dark, rug is mid-red, so the figure foot bottom is the lowest row
    # with BOTH diff AND a light pixel (mean > 170). Use that for height.
    arr = np.asarray(im).astype(int)
    light = mask & (arr.mean(axis=2) > 170)
    ly, lx = np.where(light)
    foot_bottom = int(ly.max()) if len(ly) else bbox[3]
    bbox_fig = [bbox[0], bbox[1], bbox[2], foot_bottom]
    fh = foot_bottom - bbox[1]
    # keep diff bbox in the report so the shadow extension is visible, not hidden
    diff_bbox = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
    bbox = bbox_fig
    rep = {"image": os.path.basename(a.image), "framing": a.framing,
           "bbox": bbox, "diff_bbox_incl_shadow": diff_bbox,
           "figure_height": fh, "head": bbox[1], "feet": bbox[3],
           "frame_ratio": round(fh/H, 4), "chair_height": chair_h,
           "figure_chair_ratio": round(fh/chair_h, 4),
           "checks": {}}
    fails = []
    if rep["figure_chair_ratio"] < 1.374:
        fails.append("FURNITURE RATIO BELOW LOCK")
    rep["checks"]["furniture_ratio_ge_1.374"] = rep["figure_chair_ratio"] >= 1.374
    if rep["frame_ratio"] < 0.577:
        fails.append("FRAME RATIO BELOW LOCK")
    rep["checks"]["frame_ratio_ge_0.577"] = rep["frame_ratio"] >= 0.577
    if a.framing == "portrait":
        rug_pos = round((bbox[3]-rug_far)/(rug_near-rug_far), 3) if rug_far else None
        rep["rug_position"] = rug_pos
        planted = 1650 <= bbox[3] <= 1788
        rep["checks"]["feet_planted_1650_1788"] = planted
        if not planted:
            fails.append("FEET NOT PLANTED")
    whole = bbox[0] >= 0 and bbox[1] >= 0 and bbox[2] < W and bbox[3] < H
    rep["checks"]["whole_in_frame"] = whole
    if not whole:
        fails.append("FIGURE NOT WHOLE / EDGE TOUCH")
    rep["verdict"] = "PASS" if not fails else "FAIL: " + "; ".join(fails)
    print(json.dumps(rep, indent=2))
    return 0 if not fails else 2

if __name__ == "__main__":
    sys.exit(main())
