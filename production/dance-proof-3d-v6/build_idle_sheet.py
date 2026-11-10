#!/usr/bin/env python3
"""Build cj-idle-proofs-v6.png: corrected standing idle (dance frame 1
crop) + the breathe idle + each corrected sitting pose, labeled with
measured upper-arm angles.
Usage: build_idle_sheet.py <pose_proofs_dir> <dance_frames_dir> <out_png>"""
import os, sys
from PIL import Image, ImageDraw

PP, FRAMES, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
cells = []
f1 = Image.open(os.path.join(FRAMES, "f0001.png")).convert("RGB")
w, h = f1.size
cells.append(("STANDING IDLE (dance f1) - arms 1.0/0.0 deg on screen, FK 4.9/0.9",
              f1.crop((int(0.18 * w), 0, int(0.82 * w), int(0.72 * h)))))
labels = [
    ("proof_pose_sit_normal.png", "sit_normal - 8.3 deg (already arms-down)"),
    ("proof_pose_sit_leg_folded.png", "sit_leg_folded - 8.3 deg (already arms-down)"),
    ("proof_pose_sit_lean_forward.png", "sit_lean_forward - 22.8 deg (elbows on knees)"),
    ("proof_pose_sit_recline.png", "sit_recline - 9.2 deg (already arms-down)"),
    ("proof_pose_sit_shrug.png", "sit_shrug - 23.0 deg, forearms 158.8 = the shrug itself"),
    ("proof_idle_heroic_breathe.png", "idle_heroic_breathe FIXED - arms 9.5-17.6 deg, was INERT (H at 80)"),
]
for fn, label in labels:
    p = os.path.join(PP, fn)
    if os.path.exists(p):
        cells.append((label, Image.open(p).convert("RGB")))
W, Hh = 470, 352
cols, rows = 3, 3
sheet = Image.new("RGB", (W * cols, (Hh + 20) * rows), (12, 12, 14))
dr = ImageDraw.Draw(sheet)
for i, (label, img) in enumerate(cells[:9]):
    x, y = (i % cols) * W, (i // cols) * (Hh + 20)
    img = img.copy()
    img.thumbnail((W, Hh))
    sheet.paste(img, (x, y + 20))
    dr.text((x + 6, y + 4), label, fill=(255, 235, 150))
sheet.save(OUT)
print("IDLE SHEET:", OUT, "cells:", len(cells))
