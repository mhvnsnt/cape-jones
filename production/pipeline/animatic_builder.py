#!/usr/bin/env python3
"""
animatic_builder.py — Storyboard images + timing + temp audio → timed animatic.

The missing link between Storyboarder and the animation pipeline.

Input: a directory of storyboard panels (PNG/JPG) + a timing file.
  Timing file (CSV or simple text):
    panel001.png,3.0        # 3 seconds
    panel002.png,1.5
    panel003.png,4.0

  Or --beat-file with JSON: {"panels": [{"file": "...", "duration": 3.0}, ...]}

Optional: --audio track.mp3 (temp music/dialogue laid under the animatic)
Optional: --transition 0.3 (crossfade seconds between panels)

Output: MP4 animatic at 24fps, 1920x1080 (panels letterboxed).

Example:
  python3 animatic_builder.py boards/ timing.csv --audio temp_music.mp3 -o animatic.mp4
"""
import argparse, csv, json, os, subprocess, sys

FPS = 24
W, H = 1920, 1080


def load_timing(path):
    panels = []
    if path.endswith(".json"):
        data = json.load(open(path))
        items = data.get("panels", data)
        for it in items:
            panels.append((it["file"], float(it.get("duration", 2.0))))
    else:
        with open(path) as f:
            for row in csv.reader(f):
                if not row or row[0].strip().startswith("#"):
                    continue
                panels.append((row[0].strip(), float(row[1].strip())))
    return panels


def main():
    ap = argparse.ArgumentParser(description="Storyboard → timed animatic")
    ap.add_argument("boards_dir")
    ap.add_argument("timing", help="CSV or JSON timing file")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--audio", help="Temp audio track (mp3/wav)")
    ap.add_argument("--transition", type=float, default=0.0,
                    help="Crossfade seconds between panels")
    ap.add_argument("--fps", type=int, default=24)
    args = ap.parse_args()

    panels = load_timing(args.timing)
    if not panels:
        sys.exit("No panels in timing file.")

    # Build per-panel clips, then concat
    segs = []
    tmpdir = "/tmp/animatic_build"
    os.makedirs(tmpdir, exist_ok=True)
    for i, (fname, dur) in enumerate(panels):
        src = os.path.join(args.boards_dir, fname)
        if not os.path.exists(src):
            sys.exit(f"Missing panel: {src}")
        seg = os.path.join(tmpdir, f"seg_{i:03d}.mp4")
        # pad to 1080p, hold for duration
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
              f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=black,"
              f"format=yuv420p")
        subprocess.run(["ffmpeg", "-y", "-loop", "1", "-i", src,
                        "-t", str(dur), "-vf", vf,
                        "-r", str(args.fps), "-c:v", "libx264",
                        "-preset", "veryfast", "-crf", "20", seg],
                       check=True, capture_output=True)
        segs.append(seg)

    # Concat (with optional xfade — simple concat if transition=0)
    if args.transition > 0 and len(segs) > 1:
        # full xfade chain is verbose; do pairwise for now
        print("NOTE: --transition uses simple concat for >2 panels in v1; "
              "xfade chain coming. Using hard cuts.", file=sys.stderr)

    lst = os.path.join(tmpdir, "list.txt")
    with open(lst, "w") as f:
        for s in segs:
            f.write(f"file '{s}'\n")

    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst,
           "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p"]
    if args.audio:
        cmd += ["-i", args.audio, "-c:a", "aac", "-b:a", "160k", "-shortest"]
    cmd += [args.output]
    subprocess.run(cmd, check=True)
    total = sum(d for _, d in panels)
    print(f"animatic -> {args.output} ({len(panels)} panels, {total:.1f}s)")


if __name__ == "__main__":
    main()
