#!/usr/bin/env python3
"""Assemble a Rig Jones 2 (V3) SHORT TEST — same proven pipeline as
assemble_v3.py, parameterized: frames dir, keys file, output mp4.
The test is 120f, all inside the sodium half (f1-120), so it composites
over the sodium plate only and grades with the repo verbatim sodium
chain. No gag beat, no crossfade, no black tail (those are full-cut
beats, beyond the test's range).
Usage: python3 v3-swap-system/assemble_test_v3.py <frames_dir> <keys.json> <out.mp4>
"""
import hashlib
import json
import os
import subprocess
import sys

from PIL import Image

sys.path.insert(0, "/home/hatch/workspace/_cape-jones-parking-lot-2d/rig")
from composite import plate_window, camera_at

WD = "/home/hatch/workspace/_cape-jones-parking-lot-2d"
FRAMES, KEYS_PATH, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
TMP = os.path.join(os.path.dirname(OUT), "test-assembly")
os.makedirs(TMP, exist_ok=True)

BULB_ORANGE_DIM = (
    "colorchannelmixer=rr=1.35:rg=0.15:rb=0.0:gr=0.10:gg=0.90:gb=0.0:br=0.0:bg=0.0:bb=0.70,"
    "eq=saturation=1.30:contrast=1.10:brightness=-0.08,"
    "curves=b='0/0.0 0.5/0.30 1/0.65',"
    "unsharp=5:5:0.4"
)

keys = json.load(open(KEYS_PATH))["keys"]
nframes = json.load(open(KEYS_PATH))["frames"]
sodium = Image.open(f"{WD}/rig/plate-sodium.png").convert("RGB")

have = sorted(f for f in os.listdir(FRAMES) if f.startswith("f") and f.endswith(".png"))
assert len(have) == nframes, f"expected {nframes} rig frames, got {len(have)}"
for f in range(1, nframes + 1):
    pup = Image.open(f"{FRAMES}/f{f:04d}.png").convert("RGBA")
    cam = camera_at(keys, f)
    win = plate_window(cam)
    bg = sodium.crop(win).resize((1280, 720), Image.LANCZOS)
    bg.paste(pup, (0, 0), pup)
    bg.save(f"{TMP}/f{f:04d}.png")
print("composited", nframes, "frames")

subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "24",
                "-i", f"{TMP}/f%04d.png",
                "-vf", BULB_ORANGE_DIM, "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-crf", "18", OUT], check=True)
print("TEST CUT:", OUT)
print("sha256:", hashlib.sha256(open(OUT, "rb").read()).hexdigest())
print("bytes:", os.path.getsize(OUT))
