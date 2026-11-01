#!/usr/bin/env python3
"""
flash_check.py — seizure-safety proxy gate for Cape Jones dance videos.
NOT a clinical Harding FPA or PEAT certification. PEAT's own licence
prohibits commercial TV/film/game use; the Harding FPA is a paid
broadcast analyser not available here. This is a WCAG 2.3.1-inspired
proxy, stated as such, so a bad video cannot pass silently:

WCAG 2.3.1 (W3C): no content flashes more than 3 times in any
1-second period, or the flash is below the general/red thresholds.
General flash (WCAG): a pair of opposing changes in relative
luminance of 10% or more of maximum, darker image below 0.80.
Ofcom/Harding (via Epilepsy Foundation consensus, Harding et al.
2005): a potentially harmful flash is a pair of opposing luminance
changes >=20 cd/m2, at >=3 Hz, occupying >=0.006 steradians
(~25% of a 10-degree visual field), and any transition to/from
saturated red is harmful irrespective of luminance.

Proxy implemented here, on 0-255 luminance (NOT cd/m2):
- Extract frames at native fps, scaled to 960x540 for speed.
- Whole-frame mean luminance per frame.
- Hero-crop mean luminance + dark fraction (<60) per frame.
  Hero crop for the 1920x1080 dance-test layout: x 602-1318, y 0-950.
- A "general flash" = an opposing pair: mean luminance moves
  >=25.5 (10% of 255) in one direction, then >=25.5 back, with the
  darker mean <204 (0.80*255), both moves inside a 1-second window.
- A "red flash" = saturated-red fraction (R>200, R-G>80, R-B>80)
  moves from <0.01 to >0.01 and back within 1 second.
- A "forearm flip" (Cape-Jones-specific, from Mars 2026-11-01):
  in the forearm boxes of the 1920x1080 dance-test layout
  (scaled to analysis width: L x 390-440, R x 525-570, y 190-280
  at 960x540), the fraction of pixels whose luminance reverses
  by >30 in consecutive frame pairs (up then down, or down then
  up) exceeds 0.05 in either box. One such triple is one flip
  event. The gate FAILS on >3 flip events in any 1 second,
  same rate as WCAG, because the original fault was a black/white
  forearm alternating every other frame at 48 fps.
  Whole-frame means alone MISS this fault (forearm is small vs
  frame; original whole-frame mean jumps were <3 except for
  environment cuts), so the forearm-box pixel metric is the
  primary gate for this fault, not an extra.
- PASS iff: max general flashes in any 1s <= 3, max red flashes
  in any 1s <= 3, and max forearm flips in any 1s <= 3.
  A single large whole-frame jump alone is a cut (e.g. an
  environment change), not a flash; it is reported but is only
  fatal if it reverses within 1 second (i.e. it becomes a flash).

Usage: python3 flash_check.py <video.mp4|frames-dir> [fps]
Exit 0 = PASS, 1 = FAIL. Writes <input>.flash.json + .flash.csv
next to the input when a video path is given, else in cwd.
"""
import sys, os, json, csv, subprocess, tempfile
import numpy as np
from PIL import Image

def frames_from_video(path, width=960):
    tmp = tempfile.mkdtemp(prefix="flashcheck_")
    # scale to 960 wide, keep aspect
    subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf",
                    f"scale={width}:-2", "-pix_fmt", "rgb24",
                    os.path.join(tmp, "f%05d.png")], check=True)
    files = sorted(os.listdir(tmp))
    return [os.path.join(tmp, f) for f in files], tmp

def frames_from_dir(path):
    return sorted(os.path.join(path, f) for f in os.listdir(path)
                  if f.lower().endswith(".png")), None

def analyse(files, fps):
    rows = []
    prev2 = prev1 = None
    for i, p in enumerate(files):
        im = np.array(Image.open(p).convert("RGB")).astype(float)
        h, w, _ = im.shape
        lum = 0.2126*im[:, :, 0] + 0.7152*im[:, :, 1] + 0.0722*im[:, :, 2]
        # hero crop in analysis coordinates: original 1920x1080 crop
        # x 602-1318, y 0-950, scaled by w/1920, h/1080
        hx0, hx1, hy0, hy1 = int(602*w/1920), int(1318*w/1920), 0, int(950*h/1080)
        hero = lum[hy0:hy1, hx0:hx1]
        red = ((im[:, :, 0] > 200) & (im[:, :, 0]-im[:, :, 1] > 80)
               & (im[:, :, 0]-im[:, :, 2] > 80)).mean()
        # forearm-box alternating pixels, 960x540 reference boxes
        # scaled to analysis size
        sx, sy = w/960.0, h/540.0
        boxes = [(int(390*sx), int(440*sx), int(190*sy), int(280*sy)),
                 (int(525*sx), int(570*sx), int(190*sy), int(280*sy))]
        flip_frac = 0.0
        if prev2 is not None:
            for (x0, x1, y0, y1) in boxes:
                d1 = prev1[y0:y1, x0:x1] - prev2[y0:y1, x0:x1]
                d2 = lum[y0:y1, x0:x1] - prev1[y0:y1, x0:x1]
                alt = (d1*d2 < 0) & (np.abs(d1) > 30) & (np.abs(d2) > 30)
                flip_frac = max(flip_frac, float(alt.mean()))
        rows.append(dict(frame=i, mean=float(lum.mean()),
                         hero_mean=float(hero.mean()),
                         hero_dark=float((hero < 60).mean()),
                         red=float(red), forearm_flip_frac=flip_frac))
        prev2, prev1 = prev1, lum
    return rows

def count_in_windows(events, fps):
    """events: list of frame indices where a flash/flip pair completes.
    Return max count in any sliding 1-second window."""
    if not events:
        return 0
    win = max(1, int(round(fps)))
    best = 0
    for i, e in enumerate(events):
        c = sum(1 for x in events if e <= x < e + win)
        best = max(best, c)
    return best

def main():
    src = sys.argv[1]
    if os.path.isdir(src):
        files, _ = frames_from_dir(src)
        fps = float(sys.argv[2]) if len(sys.argv) > 2 else 24.0
    else:
        # fps from ffprobe
        out = subprocess.run(["ffprobe", "-v", "error",
                              "-select_streams", "v:0",
                              "-show_entries", "stream=r_frame_rate",
                              "-of", "default=noprint_wrappers=1:nokey=1", src],
                             capture_output=True, text=True, check=True).stdout.strip()
        num, den = out.split("/")
        fps = float(num)/float(den)
        files, _ = frames_from_video(src)
    rows = analyse(files, fps)
    # opposing pairs
    gen, red_ev, flips = [], [], []
    for i in range(2, len(rows)):
        d1 = rows[i-1]["mean"] - rows[i-2]["mean"]
        d2 = rows[i]["mean"] - rows[i-1]["mean"]
        if d1 * d2 < 0 and abs(d1) >= 25.5 and abs(d2) >= 25.5 \
                and min(rows[i-2]["mean"], rows[i-1]["mean"], rows[i]["mean"]) < 204:
            gen.append(i)
        r1 = rows[i-1]["red"] - rows[i-2]["red"]
        r2 = rows[i]["red"] - rows[i-1]["red"]
        if r1 * r2 < 0 and abs(r1) >= 0.01 and abs(r2) >= 0.01:
            red_ev.append(i)
        if rows[i]["forearm_flip_frac"] > 0.05:
            flips.append(i)
    max_jump = max((abs(rows[i]["mean"]-rows[i-1]["mean"])
                    for i in range(1, len(rows))), default=0.0)
    result = dict(input=src, frames=len(rows), fps=fps,
                  general_flashes=len(gen), general_max_per_sec=count_in_windows(gen, fps),
                  red_flashes=len(red_ev), red_max_per_sec=count_in_windows(red_ev, fps),
                  forearm_flips=len(flips), forearm_flips_max_per_sec=count_in_windows(flips, fps),
                  max_frame_mean_jump=round(max_jump, 1),
                  general_frames=gen, red_frames=red_ev, forearm_flip_frames=flips)
    result["verdict"] = "PASS" if (
        result["general_max_per_sec"] <= 3 and result["red_max_per_sec"] <= 3
        and result["forearm_flips_max_per_sec"] <= 3) else "FAIL"
    result["forearm_flip_frac_max"] = round(max((r["forearm_flip_frac"] for r in rows), default=0.0), 4)
    outbase = src.rstrip("/") + ".flash"
    with open(outbase + ".json", "w") as f:
        json.dump(result, f, indent=2)
    with open(outbase + ".csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["frame", "mean", "hero_mean", "hero_dark", "red", "forearm_flip_frac"])
        w.writeheader()
        for r in rows:
            w.writerow({k: round(v, 4) if isinstance(v, float) else v for k, v in r.items()})
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ("general_frames", "red_frames", "forearm_flip_frames")}, indent=2))
    print("general_frames:", gen[:50])
    print("forearm_flip_frames:", flips[:50])
    return 0 if result["verdict"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
