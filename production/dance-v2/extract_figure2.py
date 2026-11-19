#!/usr/bin/env python3
"""Extract the drawn full-body figure (sheet 04 'HOVERING') as the v2
character source. Sheet 04 is drawn 2D art (viewed and confirmed); the
01 T-pose turnaround is banned by owner ruling 2026-10-29."""
import cv2, numpy as np
from PIL import Image, ImageDraw
import os

SRC = os.path.expanduser('~/workspace/cape-jones/characters/sheets/04-action-flight-vfx-reference.jpg')
OUT = os.path.expanduser('~/workspace/_cj-dance-v2/build/parts2')
os.makedirs(OUT, exist_ok=True)
img = cv2.imread(SRC); img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
H, W = img.shape[:2]
print('sheet', W, H)
# hovering figure: top-right of the sheet
crop = img[int(0.085 * H):int(0.435 * H), int(0.585 * W):int(0.995 * W)]
ch, cw = crop.shape[:2]
hsv = cv2.cvtColor(crop, cv2.COLOR_RGB2HSV)
cand = ((hsv[:, :, 2] > 168) & (hsv[:, :, 1] < 60)).astype(np.uint8)
n, lab = cv2.connectedComponents(cand, 4)
border = set(np.unique(np.concatenate([lab[0, :], lab[-1, :], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, list(border))
alpha = np.where(bg, 0, 255).astype(np.uint8)
alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
n, lab, stats, _ = cv2.connectedComponentsWithStats((alpha > 0).astype(np.uint8), 8)
keep = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1
alpha = np.where(lab == keep, 255, 0).astype(np.uint8)
rgba = np.dstack([crop, alpha])
ys, xs = np.where(alpha > 0)
box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
fig = Image.fromarray(rgba).crop(box)
fig.save(f'{OUT}/figure2_rgba.png')
print('figure2', fig.size, 'box', box, 'in crop', (cw, ch))
# grid overlay for setting masks/pivots (10% lines, labelled in %)
g = fig.convert('RGB').copy(); d = ImageDraw.Draw(g)
w, h = fig.size
for i in range(1, 10):
    d.line([i * w / 10, 0, i * w / 10, h], fill=(255, 0, 0), width=2)
    d.line([0, i * h / 10, w, i * h / 10], fill=(255, 0, 0), width=2)
    d.text((i * w / 10 + 3, 3), str(i * 10), fill=(255, 0, 0))
    d.text((3, i * h / 10 + 3), str(i * 10), fill=(255, 0, 0))
g.save(f'{OUT}/figure2_grid.png')
print('grid saved')
