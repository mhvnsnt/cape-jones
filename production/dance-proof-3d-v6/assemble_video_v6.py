#!/usr/bin/env python3
"""Assemble cj-dance-proof-3d-v6.mp4 from rendered frames + JP v2 mix,
build the delivery sheet (arms-down start, deepest-squat feet zoom,
shoulder zoom, cape zoom, world cycle), and measure the PR #269
section-5 yardstick (torso/foot band travel on frame masks).
Usage: assemble_video_v6.py <frames_dir> <out_dir>"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

FRAMES, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
SONG = "/home/hatch/workspace/your_files/cape-jones-dance-proof/song/song-full-v2-jp.mp3"
MP4 = os.path.join(OUT, "cj-dance-proof-3d-v6.mp4")

files = sorted(f for f in os.listdir(FRAMES) if f.endswith(".png"))
print("frames:", len(files))
assert len(files) >= 1800, f"only {len(files)} frames"

cmd = ["ffmpeg", "-y", "-framerate", "24", "-start_number", "1",
       "-i", os.path.join(FRAMES, "f%04d.png"),
       "-i", SONG, "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-crf", "18", "-c:a", "aac", "-shortest", MP4]
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stderr[-1200:])
assert os.path.getsize(MP4) > 1_000_000
print("MP4:", MP4, os.path.getsize(MP4))

# ---- section-5 yardstick (same method as v5)
def mask_of(img):
    a = np.asarray(img.convert("RGB"), dtype=np.int16)
    bg = np.median(np.concatenate([a[:20, :20].reshape(-1, 3), a[:20, -20:].reshape(-1, 3),
                                   a[-20:, :20].reshape(-1, 3), a[-20:, -20:].reshape(-1, 3)]), axis=0)
    d = np.abs(a - bg).sum(axis=2)
    return d > 90

sample_idx = list(range(0, len(files), 19))
torso_c, foot_c, masks = [], [], []
for i in sample_idx:
    img = Image.open(os.path.join(FRAMES, files[i])).resize((480, 270))
    m = mask_of(img)
    masks.append(m)
    ys, xs = np.nonzero(m)
    if len(ys) == 0:
        continue
    H = ys.max() - ys.min()
    torso_band = m[int(ys.min() + 0.25 * H):int(ys.min() + 0.45 * H)]
    foot_band = m[int(ys.min() + 0.85 * H):]
    if torso_band.any():
        torso_c.append(np.nonzero(torso_band)[1].mean())
    if foot_band.any():
        foot_c.append(np.nonzero(foot_band)[1].mean())
def travel(c):
    return (max(c) - min(c)) / 480 * 100 if len(c) > 2 else 0.0
tt, ft = travel(torso_c), travel(foot_c)
print(f"MEASURE torso travel {tt:.1f}%  foot travel {ft:.1f}%  ratio {ft/max(tt,0.1):.2f} (spec: torso>=10, ratio>=0.5)")
diffs = [np.abs(masks[i].astype(int) - masks[i - 1].astype(int)).mean() for i in range(1, len(masks))]
print(f"distinct sample steps: min {min(diffs):.3f} mean {np.mean(diffs):.3f} of {len(masks)} samples")

# ---- sheet: 3 cols x 4 rows. Global frame map: 1-24 idle-in,
# loop tiles start at 25 (tile frame t = global 24+t); deepest squat
# is tile frame 71 -> global 95.
def frame_img(fno):
    return Image.open(os.path.join(FRAMES, f"f{fno:04d}.png")).convert("RGB")
def crop(img, box):
    w, h = img.size
    return img.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))

W, Hh = 480, 270
f1, f95, f300 = frame_img(1), frame_img(95), frame_img(300)
cells = [
    ("START f1 - arms-down idle", f1),
    ("f1 ARMS ZOOM - hands at thighs", crop(f1, (0.22, 0.02, 0.78, 0.60))),
    ("f95 deepest squat", f95),
    ("f95 FEET ZOOM - soles flat, grounded", crop(f95, (0.30, 0.68, 0.70, 1.0))),
    ("f95 CAPE ZOOM - one solid piece", crop(f95, (0.28, 0.38, 0.72, 0.99))),
    ("f300 groove - day", f300),
    ("f300 SHOULDER ZOOM - arms alive", crop(f300, (0.24, 0.0, 0.74, 0.46))),
    ("f700 world - LED colors", frame_img(700)),
    ("f1200 world - night", frame_img(1200)),
    ("f1500 late groove", frame_img(1500)),
    ("f1700 world - day returns", frame_img(1700)),
    ("f1820 return to idle - arms down", frame_img(1820)),
]
sheet = Image.new("RGB", (W * 3, (Hh + 22) * 4), (12, 12, 14))
dr = ImageDraw.Draw(sheet)
for i, (label, img) in enumerate(cells):
    x, y = (i % 3) * W, (i // 3) * (Hh + 22)
    sheet.paste(img.resize((W, Hh)), (x, y + 22))
    dr.text((x + 8, y + 5), label, fill=(255, 235, 150))
sheet_path = os.path.join(OUT, "cj-dance-proof-3d-v6-sheet.png")
sheet.save(sheet_path)
print("SHEET:", sheet_path)
print("ASSEMBLE_V6_DONE")
