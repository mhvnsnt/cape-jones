#!/usr/bin/env python3
"""Flash gate for Video 5: per-frame mean luminance + forearm-box mean, 24fps.
PASS criteria (WCAG 2.3.1 / Harding style, simplified): no 3+ flashes/sec,
no frame-to-frame whole-frame mean jump > 50 that reverses next frame (black/white flip),
forearm-box mean never flips <100 -> >180 in one frame."""
import subprocess, json, numpy as np, sys
VID="/home/hatch/workspace/cape-jones-rig/nosferatu-video5-20261101/video5-johnny-nosferatu-silent.mp4"
# extract 480x270 gray frames via ffmpeg pipe
cmd=["ffmpeg","-v","error","-i",VID,"-vf","scale=480:270,format=gray","-f","rawvideo","-pix_fmt","gray","-"]
data=subprocess.check_output(cmd)
W,H=480,270; n=len(data)//(W*H)
frames=np.frombuffer(data, dtype=np.uint8).reshape(n,W*H//1) if False else np.frombuffer(data, dtype=np.uint8).reshape(n,H,W)
whole=frames.mean(axis=(1,2))
# forearm box in 480x270 coords: hero centre x~240, y~90-140 (scaled from 1920x1080: x 800-1200 -> 200-300, y 350-550 -> 88-138)
fore=frames[:,88:138,200:300].mean(axis=(1,2))
jumps=np.abs(np.diff(whole))
fjumps=np.abs(np.diff(fore))
flips=int(((fore[:-1]<100)&(fore[1:]>180)).sum() + ((fore[:-1]>180)&(fore[1:]<100)).sum())
# flashes/sec: count large whole-frame jumps in any 1s window
max_per_sec=0
for s in range(0, n-24):
    c=int((jumps[s:s+24]>50).sum())
    max_per_sec=max(max_per_sec,c)
out={"frames":int(n),"fps":24,"whole_mean_min":float(whole.min()),"whole_mean_max":float(whole.max()),
 "whole_max_jump":float(jumps.max()),"forearm_max_jump":float(fjumps.max()),
 "forearm_black_white_flips":flips,"max_large_jumps_per_sec":max_per_sec,
 "verdict":"PASS" if flips==0 and max_per_sec<3 else "FAIL"}
print(json.dumps(out, indent=2))
open("/home/hatch/workspace/cape-jones-rig/nosferatu-video5-20261101/flash_check.json","w").write(json.dumps(out, indent=2))
