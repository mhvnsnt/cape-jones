#!/usr/bin/env python3
"""Rebuild the locked default T-pose (v7, 2026-10-31) from sliced pieces.
Run: python3 assemble_tpose_default.py [output.png]
Default output: assembly-preview-v7-20261031.png (rebuilt, not overwritten
in place — pass a new filename for a new version).
Canvas 1100x1500, grey 128. Scale 0.95 unless noted.
Layer order is bottom -> top. Arm flip is VERTICAL (top-to-bottom),
NOT horizontal (left-to-right).
"""
import sys, os
from PIL import Image
BASE = os.path.join(os.path.dirname(__file__), "pieces")
if not os.path.isdir(BASE):
    BASE = os.path.join(os.path.dirname(__file__), "sliced")
def load(n, scale=0.95):
    im = Image.open(os.path.join(BASE, n)).convert("RGBA")
    return im.resize((int(im.size[0]*scale), int(im.size[1]*scale)), Image.LANCZOS)
def main(out):
    canvas = Image.new("RGBA", (1100, 1500), (128, 128, 128, 255))
    def paste(im, cx, top):
        canvas.paste(im, (int(cx - im.size[0]/2), int(top)), im)
    paste(load("Cape_Back_Main.png"), 550, 410)          # top at shoulders
    paste(load("Leg_Front.png"), 450, 720)               # screen-left leg
    paste(load("Leg_Back_GRAFTED.png"), 650, 720)        # screen-right, full toe
    left = load("Arm_Front.png"); left = left.transpose(Image.FLIP_TOP_BOTTOM).rotate(90, expand=True); left = left.transpose(Image.FLIP_TOP_BOTTOM)
    right = load("Arm_Front.png"); right = right.rotate(90, expand=True); right = right.transpose(Image.FLIP_TOP_BOTTOM)
    paste(left, 300, 380); paste(right, 800, 380)        # pads top, fists bottom
    paste(load("Pelvis.png"), 550, 680)                  # v7: up 20, overlaps torso 23px
    paste(load("Cape_Collar.png"), 550, 370)
    paste(load("Torso_Chest.png"), 550, 400)
    paste(load("Belt_Overlay.png"), 550, 670)            # v7: up 10, covers junction
    paste(load("Neck.png", scale=1.05), 550, 360)         # v6: wider, 109x87
    paste(load("Head_Front.png"), 550, 250)              # v6: lowered, jaw on neck
    canvas.convert("RGB").save(out)
    print(f"saved {out}")
if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "assembly-preview-v7-20261031.png")
