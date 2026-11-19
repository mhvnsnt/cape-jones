#!/usr/bin/env python3
"""Movement-spec acceptance measurement, research doc section 5 method.
Usage: measure.py <video.mp4> [loop_start_frame] [loop_len]
Extracts one loop at 480x270 grayscale, builds the motion mask against the
per-pixel median frame, takes the character box from the mask, and reports
foot-band vs torso-band centroid travel as % of box width, plus a distinct-
frame count (mean abs step > 0.5 grey levels = frame differs from previous).
"""
import subprocess, sys
import numpy as np

video = sys.argv[1]
start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
n = int(sys.argv[3]) if len(sys.argv) > 3 else 48
W, H = 480, 270
cmd = ["ffmpeg", "-v", "error", "-i", video,
       "-vf", f"select='between(n\\,{start}\\,{start + n - 1})',scale={W}:{H},format=gray",
       "-vsync", "0", "-f", "rawvideo", "-"]
raw = subprocess.run(cmd, capture_output=True).stdout
frames = np.frombuffer(raw, dtype=np.uint8)
got = len(frames) // (W * H)
frames = frames[:got * W * H].reshape(got, H, W).astype(np.float32)
print(f"frames decoded: {got}")
med = np.median(frames, axis=0)
mask = np.abs(frames - med) > 20
allmask = mask.any(axis=0)
ys, xs = np.nonzero(allmask)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
boxw = x1 - x0 + 1
print(f"character box: x {x0}..{x1} (w {boxw}), y {y0}..{y1}")
bh = y1 - y0 + 1
foot = (y0 + int(0.82 * bh), y1 + 1)
torso = (y0 + int(0.28 * bh), y0 + int(0.55 * bh))
def band_travel(band):
    ya, yb = band
    cents = []
    for f in range(got):
        m = mask[f, ya:yb, x0:x1 + 1]
        if m.sum() < 10:
            cents.append(np.nan)
            continue
        cols = m.sum(axis=0)
        cents.append(float((cols * np.arange(boxw)).sum() / cols.sum()))
    cents = np.array(cents)
    return (np.nanmax(cents) - np.nanmin(cents)) / boxw * 100.0
ft = band_travel(foot)
tt = band_travel(torso)
print(f"foot-band travel:  {ft:.1f}% of box width")
print(f"torso-band travel: {tt:.1f}% of box width")
print(f"ratio foot/torso:  {ft / tt:.2f}  (spec: >= 0.50; torso spec: >= 10%)")
steps = np.abs(np.diff(frames, axis=0)).mean(axis=(1, 2))
print(f"frame steps (mean abs diff): min {steps.min():.2f} med {np.median(steps):.2f} max {steps.max():.2f}")
print(f"distinct frames (step > 0.5): {(steps > 0.5).sum() + 1} of {got}")
