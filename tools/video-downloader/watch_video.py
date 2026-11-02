#!/usr/bin/env python3
"""AI-EYES, honest label: FRAME-STREAM ANALYSIS, not human eyes — 2026-11-02.

Reads a video with ffmpeg at its NATIVE fps (never upscaled past 60:
if the source is 60 fps we stream 60, if it is 24/30 we stream 24/30),
extracts one small frame per source frame, and measures, per second:
  - mean absolute pixel difference vs the previous frame (motion score)
  - scene changes (a second whose motion score jumps far above the median)
Key moments = the highest-motion seconds. A contact sheet of one frame
per second is also written, so a human can eye-check the machine's picks.

No OpenCV needed: ffmpeg + ffprobe + Pillow only, so it runs on this VM.

Usage:
    python3 watch_video.py <video.mp4> [--out-dir DIR] [--scale 320]

Output: <out-dir>/watch-report.json + <out-dir>/contact-sheet.png
Exit codes: 0 ok, 2 bad usage, 3 probe/ffmpeg failure.
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw

def probe(path):
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json",
           "-show_format", "-show_streams", path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        return None
    d = json.loads(r.stdout)
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    num, den = (v.get("r_frame_rate", "0/1").split("/") + ["1"])[:2]
    fps = float(num) / float(den) if float(den) else 0.0
    return {"fps": fps, "width": v.get("width"), "height": v.get("height"),
            "duration_s": float(d.get("format", {}).get("duration", 0)),
            "size_bytes": int(d.get("format", {}).get("size", 0)),
            "codec": v.get("codec_name")}

def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    path, out_dir, scale = argv[1], "watch-out", 320
    i = 2
    while i < len(argv):
        if argv[i] == "--out-dir" and i + 1 < len(argv):
            out_dir, i = argv[i + 1], i + 2
        elif argv[i] == "--scale" and i + 1 < len(argv):
            scale, i = int(argv[i + 1]), i + 2
        else:
            print(f"unknown arg: {argv[i]}", file=sys.stderr); return 2
    info = probe(path)
    if not info or not info["fps"]:
        print("ffprobe failed or no video stream", file=sys.stderr); return 3
    # Stream at native fps, capped at 60 (never invented frames).
    stream_fps = min(info["fps"], 60.0)
    os.makedirs(out_dir, exist_ok=True)
    frames_dir = os.path.join(out_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)
    r = subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", path, "-vf",
         f"fps={stream_fps},scale={scale}:-1",
         os.path.join(frames_dir, "f%06d.png")],
        capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1000:], file=sys.stderr); return 3
    files = sorted(os.listdir(frames_dir))
    per_second, prev, prev_sec, acc, n = {}, None, -1, 0.0, 0
    thumbs = []
    for idx, fn in enumerate(files):
        im = Image.open(os.path.join(frames_dir, fn)).convert("L")
        sec = int(idx / stream_fps)
        if prev is not None:
            import itertools
            diff = sum(abs(a - b) for a, b in zip(prev.tobytes(), im.tobytes()))
            diff /= max(1, len(prev.tobytes()))
            if sec != prev_sec:
                per_second[prev_sec] = acc / max(1, n); acc, n = 0.0, 0
            acc += diff; n += 1
        if sec != prev_sec and sec % 1 == 0:
            thumbs.append((sec, os.path.join(frames_dir, fn)))
        prev, prev_sec = im, sec
    if n:
        per_second[prev_sec] = acc / n
    scores = sorted(per_second.values())
    median = scores[len(scores) // 2] if scores else 0.0
    scene_changes = [s for s, v in per_second.items() if v > max(3 * median, 8.0)]
    key = sorted(per_second.items(), key=lambda kv: -kv[1])[:10]
    # Contact sheet: one thumb per second, 4 columns.
    cols = 4
    rows = (len(thumbs) + cols - 1) // cols
    tw = scale
    th = int(scale * info["height"] / max(1, info["width"])) if info["width"] else 180
    sheet = Image.new("RGB", (cols * tw, rows * (th + 18)), "white")
    draw = ImageDraw.Draw(sheet)
    for k, (sec, fp) in enumerate(thumbs):
        x, y = (k % cols) * tw, (k // cols) * (th + 18)
        sheet.paste(Image.open(fp).resize((tw, th)), (x, y + 18))
        draw.text((x + 4, y + 2), f"{sec}s", fill="black")
    sheet_path = os.path.join(out_dir, "contact-sheet.png")
    sheet.save(sheet_path)
    report = {
        "label": "FRAME-STREAM ANALYSIS — not human eyes",
        "source": path, "native_fps": info["fps"],
        "stream_fps": stream_fps, "duration_s": info["duration_s"],
        "size_bytes": info["size_bytes"], "width": info["width"],
        "height": info["height"], "frames_extracted": len(files),
        "motion_per_second": {str(k): round(v, 3) for k, v in per_second.items()},
        "median_motion": round(median, 3),
        "scene_change_seconds": scene_changes,
        "key_moments_top10_seconds": [{"second": s, "motion": round(v, 3)}
                                      for s, v in key],
        "contact_sheet": sheet_path,
    }
    with open(os.path.join(out_dir, "watch-report.json"), "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
