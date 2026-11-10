#!/usr/bin/env python3
"""Mandatory no-crop gate for Invisible Power V1 (fixed).
Run before ANY delivery of this power. Exit 0 = PASS (ship), 1 = FAIL
(edge touch / margin < 40 / halo still flat-cut — DO NOT SHIP).
Checks, on the transparent fixed masters (never on grey view copies):
  1. No alpha on any canvas edge, all 17 frames.
  2. Min margin >= 40 px on all sides, all frames.
  3. Outline-hold frame (f08) alpha > old outline-hold alpha (104,787)
     AND its bbox top sits ABOVE the visible-body head top (f00 bbox top),
     proving the halo is no longer sliced flat at the head top.
  4. Visible frames f00/f16 alpha == 337,389 (motion/body unchanged).
  5. OpenCV boundingRect cross-check (venv cv2 5.0.0) matches Pillow bbox.
Appends a run line to gate-log.jsonl (append-only).
"""
import os, sys, json
from PIL import Image
sys.path.insert(0, "/home/hatch/workspace/cape-jones-rig/no-crop-window-20261031")
from no_crop import margins as nc_margins, edge_touch

OUT = "/home/hatch/workspace/cape-jones-rig/invisible-power-v1-nocrop-fix-20261031"
frames_dir = os.path.join(OUT, "frames")
fails = []
report = {"frames": []}
try:
    import cv2
    import numpy as np
    HAVE_CV2 = True
except ImportError:
    HAVE_CV2 = False
for i in range(17):
    p = os.path.join(frames_dir, f"f{i:02d}.png")
    im = Image.open(p).convert("RGBA")
    bb = im.getbbox()
    e = edge_touch(im)
    m = nc_margins(im)
    cv = None
    if HAVE_CV2:
        a = (np.array(im.split()[3]) > 0).astype("uint8") * 255
        x, y, w, h = cv2.boundingRect(a)
        cv = [x, y, x + w, y + h]
        if cv != list(bb):
            fails.append(f"f{i:02d} cv2 bbox {cv} != Pillow {list(bb)}")
    report["frames"].append({"frame": i, "bbox": list(bb), "edge": e, "margins": m, "cv2_bbox": cv})
    if any(v > 0 for v in e.values()):
        fails.append(f"f{i:02d} edge touch {e}")
    if min(m.values()) < 40:
        fails.append(f"f{i:02d} margin < 40: {m}")
f00 = Image.open(os.path.join(frames_dir, "f00.png")).getchannel("A")
f08 = Image.open(os.path.join(frames_dir, "f08.png")).getchannel("A")
f16 = Image.open(os.path.join(frames_dir, "f16.png")).getchannel("A")
a00 = sum(1 for p in f00.getdata() if p > 0)
a08 = sum(1 for p in f08.getdata() if p > 0)
a16 = sum(1 for p in f16.getdata() if p > 0)
report.update({"f00_alpha": a00, "f08_alpha": a08, "f16_alpha": a16,
               "f00_bbox_top": f00.getbbox()[1], "f08_bbox_top": f08.getbbox()[1]})
if a00 != 337389 or a16 != 337389:
    fails.append(f"visible body changed: f00 {a00}, f16 {a16}, expected 337389")
if not (a08 > 104787):
    fails.append(f"outline hold not uncropped: f08 {a08} <= old 104787")
if not (f08.getbbox()[1] < f00.getbbox()[1]):
    fails.append(f"halo still flat-cut: f08 top {f08.getbbox()[1]} >= body head top {f00.getbbox()[1]}")
report["verdict"] = "PASS" if not fails else "FAIL"
report["fails"] = fails
with open(os.path.join(OUT, "gate-log.jsonl"), "a") as fh:
    fh.write(json.dumps(report) + "\n")
print(json.dumps(report, indent=2))
sys.exit(0 if not fails else 1)
