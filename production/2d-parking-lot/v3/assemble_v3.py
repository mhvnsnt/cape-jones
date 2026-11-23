#!/usr/bin/env python3
"""Assemble PURPLE LOT V3 (2D) — Rig Jones 2 / Clean-Up Jones 1, built to
Gumball level, 100% their method: slot swap, frame-addressed comps,
anatomical pivots, one-piece deforming cape.
480f @ 24fps, 1280x720, silent. Rig-only cut — NO V1 anchor dissolves
(the mixed cut's phasing is gone), hard cuts only.
- One hand per arm, ever: forearm ends at the cuff, hand plane is the
  only hand, swapped in place on the same plane (cj_swap_addon slots).
- Arm pivots AT the shoulder, attached to the body, through the raise.
- Cape: ONE skin-weighted mesh, hangs from the torso, trails the arm's
  motion (velocity lag, +/-1.5 deg), never lifts with the arm.
- Gag beat f169-205 is V1 plates (board 04 + ib-04b), as in V2 — hard
  cut, not a dissolve. Sodium->purple crossfade f206-253. Black f469-480.
Pipeline (same proven base as assemble_fixed2.py):
1. Composite PIL rig frames over clean plates per camera
   (rig/composite.py): sodium f1-253, purple f206-480.
2. Grade each stream with ffmpeg, repo verbatim chains.
3. Sodium->purple crossfade f206-253 as per-frame PIL blend.
4. Hard cut to black f469-480. Encode libx264 CRF 18.
Input: v3-swap-system/v3-frames/f%04d.png (from pil_render_v3.py).
Output: v2/purple-lot-v3.mp4
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
REPO = f"{WD}/repo"
FRAMES = f"{WD}/v3-swap-system/v3-frames"
MIX = f"{WD}/v3-swap-system/v3-assembly"
OUT = f"{WD}/v2"
for d in (f"{MIX}/comp", f"{MIX}/na_frames", f"{MIX}/pu_frames", f"{MIX}/final"):
    os.makedirs(d, exist_ok=True)

BULB_ORANGE_DIM = (
    "colorchannelmixer=rr=1.35:rg=0.15:rb=0.0:gr=0.10:gg=0.90:gb=0.0:br=0.0:bg=0.0:bb=0.70,"
    "eq=saturation=1.30:contrast=1.10:brightness=-0.08,"
    "curves=b='0/0.0 0.5/0.30 1/0.65',"
    "unsharp=5:5:0.4"
)
PURPLE_STREETLIGHT = (
    "colorchannelmixer=rr=0.70:rg=0.0:rb=0.30:gr=0.0:gg=0.75:gb=0.25:br=0.25:bg=0.05:bb=1.35,"
    "eq=saturation=1.30:contrast=1.18:brightness=0.0,"
    "curves=r='0/0.0 0.5/0.35 1/0.85':g='0/0.0 0.5/0.42 1/0.90':b='0/0.02 0.5/0.58 1/1.0',"
    "unsharp=5:5:0.4"
)

keys = json.load(open(f"{WD}/v3-swap-system/v3_keys.json"))["keys"]
sodium = Image.open(f"{WD}/rig/plate-sodium.png").convert("RGB")
purple = Image.open(f"{WD}/rig/plate-purple.png").convert("RGB")
B = f"{REPO}/production/2d-parking-lot/boards"
I = f"{REPO}/production/2d-parking-lot/inbetweens"
board04 = Image.open(f"{B}/cj-pl-04.png").convert("RGB").resize((1280, 720), Image.LANCZOS)
ib04b = Image.open(f"{I}/ib-04b-click.png").convert("RGB").resize((1280, 720), Image.LANCZOS)

have = sorted(f for f in os.listdir(FRAMES) if f.startswith("f") and f.endswith(".png"))
assert len(have) == 480, f"expected 480 rig frames, got {len(have)}"
for f in range(1, 481):
    if 169 <= f <= 205:
        frame = board04 if f <= 192 else ib04b
        frame.save(f"{MIX}/comp/na{f:04d}.png")
        frame.save(f"{MIX}/comp/pu{f:04d}.png")
        continue
    pup = Image.open(f"{FRAMES}/f{f:04d}.png").convert("RGBA")
    cam = camera_at(keys, f)
    win = plate_window(cam)
    for tag, plate in (("na", sodium), ("pu", purple)):
        bg = plate.crop(win).resize((1280, 720), Image.LANCZOS)
        bg.paste(pup, (0, 0), pup)
        bg.save(f"{MIX}/comp/{tag}{f:04d}.png")
print("composited")

for tag, grade in (("na", BULB_ORANGE_DIM), ("pu", PURPLE_STREETLIGHT)):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "24",
                    "-i", f"{MIX}/comp/{tag}%04d.png",
                    "-vf", grade, "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-crf", "18", f"{MIX}/{tag}.mp4"], check=True)
    print("graded stream:", tag)

for tag in ("na", "pu"):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{MIX}/{tag}.mp4",
                    f"{MIX}/{tag}_frames/f%04d.png"], check=True)

for f in range(1, 481):
    if f <= 205:
        im = Image.open(f"{MIX}/na_frames/f{f:04d}.png")
    elif f >= 254:
        im = Image.open(f"{MIX}/pu_frames/f{f:04d}.png")
    else:
        t = (f - 205) / 48.0
        im = Image.blend(Image.open(f"{MIX}/na_frames/f{f:04d}.png"),
                         Image.open(f"{MIX}/pu_frames/f{f:04d}.png"), t)
    if f >= 469:
        im = Image.new("RGB", (1280, 720), (0, 0, 0))
    im.save(f"{MIX}/final/f{f:04d}.png")
print("final frames built")

out = f"{OUT}/purple-lot-v3.mp4"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "24",
                "-i", f"{MIX}/final/f%04d.png",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", out], check=True)
print("V3 cut:", out)
print("sha256:", hashlib.sha256(open(out, "rb").read()).hexdigest())
print("bytes:", os.path.getsize(out))
