#!/usr/bin/env python3
"""Assemble cj-dance-proof-3d-v5.mp4 from rendered frames + EN v2 mix,
build the delivery sheet, and measure the PR #269 section-5 yardstick
(torso/foot band travel on downscaled frame masks).
Usage: assemble_v5.py <frames_dir> <out_dir>"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

FRAMES, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
SONG = "/home/hatch/workspace/your_files/cape-jones-dance-proof/song/song-full-v2-en.mp3"
MP4 = os.path.join(OUT, "cj-dance-proof-3d-v5.mp4")

files = sorted(f for f in os.listdir(FRAMES) if f.endswith(".png"))
print("frames:", len(files))
assert len(files) >= 1800, f"only {len(files)} frames"

# concat via ffmpeg image sequence (frames are f%04d.png starting 1)
cmd = ["ffmpeg", "-y", "-framerate", "24", "-start_number", "1",
       "-i", os.path.join(FRAMES, "f%04d.png"),
       "-i", SONG, "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-crf", "18", "-c:a", "aac", "-shortest", MP4]
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stdout[-500:], r.stderr[-1500:])
assert os.path.getsize(MP4) > 1_000_000
print("MP4:", MP4, os.path.getsize(MP4))

# ---- section-5 yardstick: character mask = pixels far from the median
# background colour of the frame corners; measure band travel.
def mask_of(img):
    a = np.asarray(img.convert("RGB"), dtype=np.int16)
    bg = np.median(np.concatenate([a[:20, :20].reshape(-1, 3), a[:20, -20:].reshape(-1, 3),
                                   a[-20:, :20].reshape(-1, 3), a[-20:, -20:].reshape(-1, 3)]), axis=0)
    d = np.abs(a - bg).sum(axis=2)
    return d > 90

sample_idx = list(range(0, len(files), 19))  # ~96 samples across the loop tiles
torso_c, foot_c, masks = [], [], []
H = None
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

# distinct-frame check on samples
diffs = [np.abs(masks[i].astype(int) - masks[i - 1].astype(int)).mean() for i in range(1, len(masks))]
print(f"distinct sample steps: min {min(diffs):.3f} mean {np.mean(diffs):.3f} of {len(masks)} samples")

# ---- sheet: loop phases + world sections + zooms
picks = [("loop start", 10), ("bounce", 300), ("squat", 700), ("arms wide", 1100),
         ("late loop", 1500), ("final", 1800)]
thumbs = []
for label, fno in picks:
    p = os.path.join(FRAMES, f"f{fno:04d}.png")
    if os.path.exists(p):
        thumbs.append((label, Image.open(p).convert("RGB")))
W, Hh = 480, 270
sheet = Image.new("RGB", (W * 3, (Hh + 22) * 3), (12, 12, 14))
dr = ImageDraw.Draw(sheet)
for i, (label, img) in enumerate(thumbs[:6]):
    x, y = (i % 3) * W, (i // 3) * (Hh + 22)
    sheet.paste(img.resize((W, Hh)), (x, y + 22))
    dr.text((x + 8, y + 5), label, fill=(255, 235, 150))
# zoom row: crop centre-character regions from three frames
zooms = []
for label, fno, box in (("zoom shoulder", 300, (0.30, 0.05, 0.62, 0.45)),
                        ("zoom cape hem / between legs", 700, (0.30, 0.45, 0.65, 1.0)),
                        ("zoom hand", 1100, (0.45, 0.05, 0.80, 0.45))):
    p = os.path.join(FRAMES, f"f{fno:04d}.png")
    if os.path.exists(p):
        im = Image.open(p).convert("RGB")
        w, h = im.size
        crop = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
        zooms.append((label, crop.resize((W, Hh))))
for j, (label, img) in enumerate(zooms[:3]):
    x, y = j * W, 2 * (Hh + 22)
    sheet.paste(img, (x, y + 22))
    dr.text((x + 8, y + 5), label, fill=(255, 235, 150))
sheet_path = os.path.join(OUT, "cj-dance-proof-3d-v5-sheet.png")
sheet.save(sheet_path)
print("SHEET:", sheet_path)
print("ASSEMBLE_V5_DONE")
