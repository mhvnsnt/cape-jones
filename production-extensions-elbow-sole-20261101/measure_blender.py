#!/usr/bin/env python3
"""Score Blender isolated-elbow renders: gray-distance coverage + gap.
World background (237,237,230); art = colour distance >25 from it
(same rule as cutlimbs measure_gap.py). Gap = longest background run
inside the r30 disc (rows/cols/diagonals), same definition as PIL pass.
"""
import os, json
import numpy as np
from PIL import Image

OUT = "/var/tmp/elbow-sole-20261101/elbow_blender"
BG = np.array([237, 237, 230])

def longest_run_1d(art, mask):
    vals = np.where(mask, art, True)
    d = np.diff(np.concatenate(([0], (~vals).astype(np.int8), [0])))
    starts = np.where(d == 1)[0]
    ends = np.where(d == -1)[0]
    return int((ends - starts).max()) if len(starts) else 0

def metrics(png, cx, cy, r):
    im = np.asarray(Image.open(png).convert("RGB")).astype(int)
    h, w, _ = im.shape
    x0, x1 = max(0, int(cx) - r), min(w, int(cx) + r + 1)
    y0, y1 = max(0, int(cy) - r), min(h, int(cy) + r + 1)
    yy, xx = np.mgrid[y0:y1, x0:x1]
    disc = (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r
    art = np.abs(im[y0:y1, x0:x1] - BG).sum(axis=2) > 25
    cov = float(art[disc].mean() * 100)
    bg_n = int((~art[disc]).sum())
    gap = 0
    for row in range(art.shape[0]):
        gap = max(gap, longest_run_1d(art[row], disc[row]))
    for col in range(art.shape[1]):
        gap = max(gap, longest_run_1d(art[:, col], disc[:, col]))
    for off in range(-art.shape[0] + 1, art.shape[1]):
        gap = max(gap, longest_run_1d(np.diagonal(art, offset=off),
                                      np.diagonal(disc, offset=off)))
        gap = max(gap, longest_run_1d(np.diagonal(np.fliplr(art), offset=off),
                                      np.diagonal(np.fliplr(disc), offset=off)))
    return round(cov, 2), bg_n, int(gap)

joints = json.load(open(os.path.join(OUT, "elbow_blender_joints.json")))
out = {}
for tag, j in joints.items():
    png = os.path.join(OUT, tag + ".png")
    cx, cy = j["elbow_px"]
    c22, b22, g22 = metrics(png, cx, cy, 22)
    c30, b30, g30 = metrics(png, cx, cy, 30)
    out[tag] = dict(j, cover_r22_pct=c22, bg_r22_px=b22, gap_r22_px=g22,
                    cover_r30_pct=c30, bg_r30_px=b30, gap_r30_px=g30)
    print(tag, "elbow_px", j["elbow_px"], "r22", c22, "gap", g22,
          "| r30", c30, "gap", g30, "bg", b30)
json.dump(out, open(os.path.join(OUT, "elbow_blender_measurements.json"), "w"), indent=1)
print("BLENDER MEASURE DONE")
