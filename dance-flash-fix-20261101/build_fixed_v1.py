#!/usr/bin/env python3
"""
build_fixed.py — FLASH-FIXED dance test, hold-instead-of-blend.

Cause (measured, see REPORT): dance-recreation-20261031 built its
217 frames @48fps by 50% alpha cross-blends between consecutive
poses (build_recreation.py: Image.blend(a, b, 0.5)). Every odd frame
therefore shows TWO forearms at once — the white near forearm at
pose A and the dark far forearm at pose B, both semi-transparent —
alternating with clean key frames at 48 fps. That is the black/white
forearm flash Mars flagged 2026-11-01 11:03 CST.

Fix (industry-standard animation, not a filter):
- NO cross-blends at all. Timeline 1..109 @24fps (the original
  dance grid, ~107 BPM, 13-14f/beat) is rebuilt from KEYS ONLY:
  dance-arm-snap-20261031/frames (63 keys, f001..f109).
  A missing timeline step HOLDS the previous key (animation on
  2s, 12 drawings/sec, normal movement), exactly as the original
  dance was timed. Fast section f043-f056 has consecutive keys,
  so it stays on 1s there — intentional fast action, still no blend.
- One consistent shading per arm per key: the key frame's own
  front/back forearm, never an averaged ghost. Hand stays attached
  in the key frame; no wrist cut, no hand-draw, no new piece.
- Environments and framing are the SAME as dance-test-20261101
  build_test2.py: 1920x1080, hero 715x975, ground y=950, centred,
  3 clean painted BGs, segments 0-36 room CJ-23, 37-72 stage CJ-09,
  73-108 night-city CJ-29. The 109-frame loop repeats for the
  full song length (75.789s, 1819 frames @24fps = 16 full loops +
  75 frames). This is a LOOP, stated plainly — not a new 75s
  choreography. Vocals that tell EN vs JP apart enter around 20s,
  which is why the full length matters (Mars 2026-11-01 11:07 CST).

Outputs (new dated files, originals untouched):
- dance-test-FIXED-visual-silent-20261101.mp4 (1920x1080, 24fps, 75.789s)
- dance-test-FIXED-EN-full-20261101.mp4 (same visual + song-full-v2-en.mp3)
- dance-test-FIXED-JP-full-20261101.mp4 (same visual + song-full-v2-jp.mp3)
- dance-test-FIXED-loop-preview-20261101.gif (960x540, 109f @24fps, one loop)
"""
import os, re, subprocess, sys
from PIL import Image

BASE = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(BASE, "dance-flash-fix-20261101")
SRC = os.path.join(BASE, "dance-arm-snap-20261031/frames")
SONG = os.path.expanduser("~/workspace/cape-jones-flying/production/vocal-stack/song")
W, H, GROUND = 1920, 1080, 950
FPS = 24
TIMELINE = 109
TOTAL_FRAMES = 1819  # 75.789s * 24 = 1818.9

def load_keys():
    keys = {}
    for fn in sorted(os.listdir(SRC)):
        m = re.search(r'f(\d+)', fn)
        if m:
            keys[int(m.group(1))] = Image.open(os.path.join(SRC, fn)).convert("RGBA").resize((715, 975))
    return keys

def timeline_frames(keys):
    seq, last = [], None
    for n in range(1, TIMELINE + 1):
        if n in keys:
            last = keys[n]
        assert last is not None, f"no key at or before {n}"
        seq.append(last)
    return seq

def main():
    keys = load_keys()
    print(f"keys: {len(keys)} (f{min(keys)}..f{max(keys)})")
    seq = timeline_frames(keys)
    print(f"timeline: {len(seq)} frames @24fps = {len(seq)/FPS:.4f}s, holds used, blends used: 0")
    envs = [
        Image.open(os.path.join(BASE, "art-owed-backgrounds-20261031/per-shot/CJ-23-bg-room-painted-new-20261031.png")).convert("RGB").resize((W, H)),
        Image.open(os.path.join(BASE, "art-owed-backgrounds-20261031/per-shot/CJ-09-bg-stage-painted-new-20261031.png")).convert("RGB").resize((W, H)),
        Image.open(os.path.join(BASE, "art-owed-backgrounds-20261031/per-shot/CJ-29-bg-night-city-painted-new-20261031.png")).convert("RGB").resize((W, H)),
    ]
    # Pre-composite the 109 loop frames at full size in a temp dir is
    # heavy; instead pipe composited frames directly to ffmpeg.
    # For the GIF preview we also save the 109 loop frames small.
    gif_frames = []
    proc = subprocess.Popen([
        "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23",
        "-movflags", "+faststart",
        os.path.join(OUT, "dance-test-FIXED-visual-silent-20261101.mp4")],
        stdin=subprocess.PIPE)
    for i in range(TOTAL_FRAMES):
        t = i % TIMELINE
        seg = 0 if t < 37 else (1 if t < 73 else 2)
        hero = seq[t]
        bbox = hero.getchannel("A").getbbox()
        canvas = envs[seg].convert("RGBA")
        canvas.alpha_composite(hero, ((W - hero.width)//2, GROUND - bbox[3]))
        rgb = canvas.convert("RGB")
        if i < TIMELINE:
            gif_frames.append(rgb.resize((960, 540)))
        proc.stdin.write(rgb.tobytes())
    proc.stdin.close(); proc.wait()
    assert proc.returncode == 0
    print(f"silent full visual: {TOTAL_FRAMES} frames, {TOTAL_FRAMES/FPS:.3f}s")
    # GIF: one loop only, labelled preview
    gif_frames[0].save(os.path.join(OUT, "dance-test-FIXED-loop-preview-20261101.gif"),
                       save_all=True, append_images=gif_frames[1:], duration=1000//FPS, loop=0)
    print("gif preview: 109f @24fps, one loop")
    # Mux audio, same visual, EN and JP
    for lang, audio in [("EN", "song-full-v2-en.mp3"), ("JP", "song-full-v2-jp.mp3")]:
        out = os.path.join(OUT, f"dance-test-FIXED-{lang}-full-20261101.mp4")
        r = subprocess.run(["ffmpeg", "-v", "error", "-y",
                            "-i", os.path.join(OUT, "dance-test-FIXED-visual-silent-20261101.mp4"),
                            "-i", os.path.join(SONG, audio),
                            "-map", "0:v:0", "-map", "1:a:0",
                            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                            "-shortest", out], capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stderr); raise SystemExit(1)
        print(f"muxed {lang}: {out}")

if __name__ == "__main__":
    main()
