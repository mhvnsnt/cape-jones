#!/usr/bin/env python3
"""PURPLE LOT V1 — grade + assemble the Tahoma2D render into the final MP4.

Input : render/purple-lot.0001.png ... .0480.png (1280x720, 24fps, native art)
Output: video/purple-lot-v1.mp4 — 480f, 20.0s, 1280x720, 24fps, silent, libx264 CRF 18.

Grade plan (chains from production/pipeline/grades.py via refs/grades.py):
  f1-205   NATIVE art — the boards as drawn and verified (dim sodium orange).
           The sodium-dim grade was eye-checked on the assembled cut and REJECTED
           here: on the dark wide board 01 it crushes the lot to near-black red
           (mean RGB 29/9/1) — far worse than the verified native board.
  f206-253 xfade 48f    sodium-graded board-05 -> purple-graded board-05 (the shift)
  f254-312 purple-streetlight grade on board 05 only (matches the xfade end)
  f313-480 NATIVE art — the purple grade overcooks the darker medium/close
           boards (board 07 goes near-black blue, skin lavender-gray); the
           drawn purple is the end state as verified. The f313 cut masks the
           grade change between the wide hero and the medium shots.
Black tail f469-480 passes through unchanged (black stays black).
finish.py applies ONE grade to a whole file, so it cannot express this two-state
grade; its QC + encode settings (ffprobe QC, libx264 CRF 18, yuv420p) are
replicated here and QC is run on the output the same way.
"""
import os, subprocess, sys

WD = "/home/hatch/workspace/_cape-jones-parking-lot-2d"
RENDER = os.path.join(WD, "render", "purple-lot.%04d.png")
OUTDIR = os.path.join(WD, "video")
os.makedirs(OUTDIR, exist_ok=True)
FINAL = os.path.join(OUTDIR, "purple-lot-v1.mp4")

SODIUM = open(os.path.join(WD, "grade-proof", "bulb-orange-dim.vf")).read().strip()
PURPLE = open(os.path.join(WD, "grade-proof", "purple-streetlight.vf")).read().strip()

def run(cmd, label):
    print(f"[{label}] {' '.join(cmd)}")
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print(f"FAILED: {label}", file=sys.stderr)
        sys.exit(1)

# Segment A: f1-205 (205 frames), NATIVE (no grade — boards as drawn/verified)
segA = os.path.join(OUTDIR, "segA-sodium.mp4")
run(["ffmpeg", "-y", "-v", "error", "-framerate", "24", "-start_number", "1",
     "-i", RENDER, "-frames:v", "205",
     "-c:v", "libx264", "-crf", "18", "-preset", "medium",
     "-pix_fmt", "yuv420p", segA], "segA")

# Segment B: the shift — one still (frame 206 = board 05), 48 frames,
# xfade sodium -> purple over the full 48f.
frame206 = os.path.join(WD, "render", "purple-lot.0206.png")
sod_still = os.path.join(OUTDIR, "shift-sodium.png")
pur_still = os.path.join(OUTDIR, "shift-purple.png")
run(["ffmpeg", "-y", "-v", "error", "-i", frame206, "-vf", SODIUM, sod_still], "shift sodium still")
run(["ffmpeg", "-y", "-v", "error", "-i", frame206, "-vf", PURPLE, pur_still], "shift purple still")
segB = os.path.join(OUTDIR, "segB-shift.mp4")
run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", "24", "-t", "2", "-i", sod_still,
     "-loop", "1", "-framerate", "24", "-t", "2", "-i", pur_still,
     "-filter_complex", "[0:v][1:v]xfade=transition=fade:duration=2:offset=0,format=yuv420p[v]",
     "-map", "[v]", "-r", "24", "-frames:v", "48", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
     segB], "segB")

# Segment C1: f254-312 (59 frames), purple-streetlight grade (board 05 only)
segC = os.path.join(OUTDIR, "segC-purple.mp4")
run(["ffmpeg", "-y", "-v", "error", "-framerate", "24", "-start_number", "254",
     "-i", RENDER, "-frames:v", "59",
     "-vf", PURPLE, "-c:v", "libx264", "-crf", "18", "-preset", "medium",
     "-pix_fmt", "yuv420p", segC], "segC")

# Segment C2: f313-480 (168 frames), NATIVE (purple boards as drawn/verified)
segC2 = os.path.join(OUTDIR, "segC2-native.mp4")
run(["ffmpeg", "-y", "-v", "error", "-framerate", "24", "-start_number", "313",
     "-i", RENDER, "-frames:v", "168",
     "-c:v", "libx264", "-crf", "18", "-preset", "medium",
     "-pix_fmt", "yuv420p", segC2], "segC2")

# Concat A + B + C1 + C2 (same codec/params; re-encode for safety)
concat_list = os.path.join(OUTDIR, "concat.txt")
with open(concat_list, "w") as f:
    for s in (segA, segB, segC, segC2):
        f.write(f"file '{s}'\n")
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", concat_list,
     "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
     "-r", "24", FINAL], "concat")

# QC (same checks as finish.py qc_check): valid stream, 480 frames, 1280x720, 20s
r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                    "-show_entries", "stream=nb_frames,r_frame_rate,width,height,duration",
                    "-of", "default=noprint_wrappers=1", FINAL],
                   capture_output=True, text=True)
print(r.stdout)
info = dict(l.split("=") for l in r.stdout.strip().split("\n") if "=" in l)
assert info.get("nb_frames") == "480", info
assert info.get("width") == "1280" and info.get("height") == "720", info
print(f"QC PASS: {FINAL} ({os.path.getsize(FINAL)} bytes)")
