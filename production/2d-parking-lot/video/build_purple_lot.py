#!/usr/bin/env python3
"""PURPLE LOT V1 — build the Tahoma2D scene + render inputs.

17 unique drawings (7 keys + 10 in-betweens) -> one 17-frame raster level,
480-frame xsheet @ 24fps, 1280x720, black bg (empty cells = hard-cut black tail).

Edit (1-based frames):
  f1-72    cold open wide:   01,01a,01,01b,01a,01  (12f each, breathing loop)
  f73-120  medium cut:       02 (24f), 02a (24f)
  f121-168 raise:            03a (16f), 03b (16f), 03 (16f)
  f169-205 close-up gag:     04 (24f), 04b click (13f)
  f206-312 hero shift:       05 throughout (grade xfade done in ffmpeg)
  f313-379 lower:            06a (24f), 06 (24f), 06b (19f)
  f380-480 nod + pupil:      07a (24f), 06 (24f), 07b (24f), 07 (17f), BLACK (12f)
"""
import os, sys, hashlib
sys.path.insert(0, "/home/hatch/workspace/_tahoma2d-wirein-20261112")
from build_scene import build
from PIL import Image

WD = "/home/hatch/workspace/_cape-jones-parking-lot-2d"
LEVEL_DIR = os.path.join(WD, "tahoma-levels")
os.makedirs(LEVEL_DIR, exist_ok=True)

# level frame -> source file (all resized to 2048x1152 then 1280x720)
SOURCES = {
    1: "boards/cj-pl-01.png",
    2: "inbetweens/ib-01a-breath-in.png",
    3: "inbetweens/ib-01b-breath-out.png",
    4: "boards/cj-pl-02.png",
    5: "inbetweens/ib-02a-hand-drift.png",
    6: "inbetweens/ib-03a-raise-mid.png",
    7: "inbetweens/ib-03b-raise-high.png",
    8: "boards/cj-pl-03.png",
    9: "boards/cj-pl-04.png",
    10: "inbetweens/ib-04b-click.png",
    11: "boards/cj-pl-05.png",
    12: "inbetweens/ib-06a-lower-mid.png",
    13: "boards/cj-pl-06.png",
    14: "inbetweens/ib-06b-arm-down-turn.png",
    15: "inbetweens/ib-07a-nod-mid.png",
    16: "inbetweens/ib-07b-pupil-half.png",
    17: "boards/cj-pl-07.png",
}
# level 18 is a solid-black frame written directly (no source drawing)

for idx, rel in SOURCES.items():
    src = os.path.join(WD, rel)
    im = Image.open(src).convert("RGB")
    if im.size != (2048, 1152):
        im = im.resize((2048, 1152), Image.LANCZOS)
    im = im.resize((1280, 720), Image.LANCZOS)
    out = os.path.join(LEVEL_DIR, f"purple-lot.{idx:04d}.png")
    im.save(out, "PNG")
    h = hashlib.sha256(open(out, "rb").read()).hexdigest()[:12]
    print(f"level {idx:02d} {rel} -> {out} sha {h}")

def run(level, start, end):
    """Append `level` for frames start..end (1-based, inclusive)."""
    return [level] * (end - start + 1)

cells = []
cells += run(1, 1, 12) + run(2, 13, 24) + run(1, 25, 36) + run(3, 37, 48) + run(2, 49, 60) + run(1, 61, 72)
cells += run(4, 73, 96) + run(5, 97, 120)
cells += run(6, 121, 136) + run(7, 137, 152) + run(8, 153, 168)
cells += run(9, 169, 192) + run(10, 193, 205)
cells += run(11, 206, 312)
cells += run(12, 313, 336) + run(13, 337, 360) + run(14, 361, 379)
cells += run(15, 380, 403) + run(13, 404, 427) + run(16, 428, 451) + run(17, 452, 468)
cells += run(18, 469, 480)  # f469-480: black level frame = hard cut to black
assert len(cells) == 480, len(cells)
print("cells:", len(cells), "black tail:", sum(1 for c in cells if c == 18))

RENDER_DIR = os.path.join(WD, "render")
os.makedirs(RENDER_DIR, exist_ok=True)
OUT_PATTERN = os.path.join(RENDER_DIR, "purple-lot..png")

scene = build(
    width=1280, height=720, fps=24, frames=480,
    bg=(0, 0, 0, 255),
    dpi=120.0,
    levels=[("purple-lot", os.path.join(LEVEL_DIR, "purple-lot..png"), 120.0)],
    columns=[{"level_idx": 0, "cells": cells, "name": "purple-lot", "visible": True, "params": {}}],
    camera_params={},
    output_path=OUT_PATTERN,
)
tnz_work = os.path.join(WD, "purple-lot.tnz")
with open(tnz_work, "w") as f:
    f.write(scene)
print(f"wrote {tnz_work} ({len(scene)} bytes)")
print(f"output pattern: {OUT_PATTERN}")
