#!/usr/bin/env python3
"""Video 5: Johnny-only dance, Nosferatu t01, keys-on-2s only (no interpolation).
Visual: 63 dance-improved keys, composited on 3 clean painted BGs, 24fps, each key held 2 frames.
Audio: Nosferatu t01 full 211.0s + synthesized SFX (original, no show audio)."""
import os, math, random, struct, wave
from PIL import Image
BASE="/home/hatch/workspace/cape-jones-rig/nosferatu-video5-20261101"
SRC="/home/hatch/workspace/cape-jones-rig/dance-improved-20261031/frames"
BGS=[
 "/home/hatch/workspace/cape-jones-rig/art-owed-backgrounds-20261031/per-shot/CJ-23-bg-room-painted-new-20261031.png",
 "/home/hatch/workspace/cape-jones-rig/art-owed-backgrounds-20261031/per-shot/CJ-09-bg-stage-painted-new-20261031.png",
 "/home/hatch/workspace/cape-jones-rig/art-owed-backgrounds-20261031/per-shot/CJ-29-bg-night-city-painted-new-20261031.png",
]
FPS=24; DUR=211.0; NFRAMES=int(FPS*DUR)  # 5064
keys=sorted(os.listdir(SRC))
assert len(keys)==63, len(keys)
print("keys", len(keys), keys[0], keys[-1])
# Pre-scale hero once per key (1100x1500 -> 693x945, bottom at 950, centred)
heroes=[]
for k in keys:
    im=Image.open(os.path.join(SRC,k)).convert("RGBA")
    im=im.resize((693,945), Image.LANCZOS)
    heroes.append(im)
bgs=[]
for p in BGS:
    b=Image.open(p).convert("RGB")
    if b.size!=(1920,1080): b=b.resize((1920,1080), Image.LANCZOS)
    bgs.append(b)
print("BGs loaded", [os.path.basename(p) for p in BGS])
os.makedirs(f"{BASE}/frames5", exist_ok=True)
# Cuts: 7 cuts, BG rotates per cut, SFX emphasis rotates per cut (in report, not on-video text)
cuts=[(0,30,"CJ-23 room"),(30,60,"CJ-09 stage"),(60,90,"CJ-29 night-city"),(90,120,"CJ-23 room"),(120,150,"CJ-09 stage"),(150,180,"CJ-29 night-city"),(180,211,"CJ-23 room")]
for fi in range(NFRAMES):
    key_idx=(fi//2)%63
    bg_idx=(fi//(30*FPS))%3 if fi<180*FPS else 0
    # cut 7 (180-211) uses room again; mapping above via time is simpler:
    t=fi/FPS
    if t<30: bg_idx=0
    elif t<60: bg_idx=1
    elif t<90: bg_idx=2
    elif t<120: bg_idx=0
    elif t<150: bg_idx=1
    elif t<180: bg_idx=2
    else: bg_idx=0
    frame=bgs[bg_idx].copy()
    frame.paste(heroes[key_idx], (613,5), heroes[key_idx])
    # save every frame? 5064 PNGs is heavy; instead write via ffmpeg pipe in a second pass.
    # Here we only save boundary + sample frames for the eye check.
    if fi in (0,719,720,1439,1440,2159,2160,2879,2880,3599,3600,4319,4320,5063) or fi%504==0:
        frame.save(f"{BASE}/frames5/check-f{fi:04d}.png")
print("boundary frames saved")
# Store composited frames via ffmpeg rawvideo pipe
import subprocess
cmd=["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s","1920x1080","-r","24","-i","-","-an","-c:v","libx264","-pix_fmt","yuv420p","-movflags","+faststart",f"{BASE}/video5-johnny-nosferatu-silent.mp4"]
p=subprocess.Popen(cmd, stdin=subprocess.PIPE)
for fi in range(NFRAMES):
    key_idx=(fi//2)%63
    t=fi/FPS
    bg_idx=0 if t<30 else 1 if t<60 else 2 if t<90 else 0 if t<120 else 1 if t<150 else 2 if t<180 else 0
    frame=bgs[bg_idx].copy()
    frame.paste(heroes[key_idx], (613,5), heroes[key_idx])
    p.stdin.write(frame.convert("RGB").tobytes())
p.stdin.close(); p.wait()
print("silent video rc", p.returncode, "frames", NFRAMES)
