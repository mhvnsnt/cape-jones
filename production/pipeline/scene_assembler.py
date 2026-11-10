#!/usr/bin/env python3
"""
scene_assembler.py — Cape Jones general episode scene assembler.

Takes a sequence of pre-processed scene clips (or FlipaClip exports that have
already gone through flipaclip_post.sh) and assembles them into a finished
episode segment with transitions, titles, and optional audio.

This is the "you place the scenes, we auto-assemble the episode" layer.

Usage:
  # From a manifest JSON
  scene_assembler.py --manifest episode_01.json --out episode_01.mp4

  # Simple sequential concat of clips
  scene_assembler.py scene_a.mp4 scene_b.mp4 scene_c.mp4 --out episode.mp4

  # With crossfades and title card
  scene_assembler.py --manifest ep.json --crossfade 0.5 --title "Cape Jones" --out ep.mp4

Manifest format (JSON):
{
  "title": "Episode 1 — The Remote",
  "fps": 24,
  "scenes": [
    {"file": "scenes/intro.mp4", "duration": null, "transition": "cut"},
    {"file": "scenes/living_room_led.mp4", "transition": "crossfade", "duration": 15.0},
    {"file": "scenes/punchline.mp4", "transition": "wipe"}
  ],
  "audio": "audio/theme.mp3",
  "audio_volume": 0.6
}
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile


def check_deps():
    for tool in ("ffmpeg", "ffprobe"):
        r = subprocess.run(["which", tool], capture_output=True)
        if r.returncode != 0:
            print(f"Missing dependency: {tool}", file=sys.stderr)
            sys.exit(1)


def probe_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        capture_output=True, text=True)
    return float(r.stdout.strip()) if r.returncode == 0 else 0.0


def make_title_card(title, duration, fps, width, height, out_path):
    """Simple title card using ffmpeg drawtext."""
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-f", "lavfi", "-i", f"color=c=black:s={width}x{height}:d={duration}:r={fps}",
        "-vf", f"drawtext=text='{title}':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
        out_path,
    ]
    subprocess.run(cmd, check=True)


def apply_transition(prev_path, next_path, transition, duration, out_path, fps):
    """Apply a simple transition between two clips."""
    if transition == "cut" or transition is None:
        # Just return the next as-is for sequential concat later
        return next_path

    if transition == "crossfade":
        cmd = [
            "ffmpeg", "-y", "-v", "error",
            "-i", prev_path, "-i", next_path,
            "-filter_complex",
            f"[0:v][1:v]xfade=transition=fade:duration={duration}:offset=0[v]",
            "-map", "[v]",
            "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
            "-r", str(fps),
            out_path,
        ]
        subprocess.run(cmd, check=True)
        return out_path

    # Default: hard cut
    return next_path


def concat_simple(clips, out_path):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        for p in clips:
            f.write(f"file '{os.path.abspath(p)}'\n")
        list_path = f.name
    try:
        subprocess.run([
            "ffmpeg", "-y", "-v", "error",
            "-f", "concat", "-safe", "0", "-i", list_path,
            "-c", "copy", out_path,
        ], check=True)
    finally:
        os.unlink(list_path)


def main():
    ap = argparse.ArgumentParser(description="Cape Jones scene assembler")
    ap.add_argument("clips", nargs="*", help="Scene clips in order")
    ap.add_argument("--manifest", help="JSON manifest of scenes")
    ap.add_argument("--out", required=True, help="Output MP4")
    ap.add_argument("--crossfade", type=float, default=0.0,
                    help="Default crossfade duration between scenes")
    ap.add_argument("--title", help="Optional title card text")
    ap.add_argument("--title-duration", type=float, default=2.5)
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--audio", help="Background audio")
    ap.add_argument("--audio-volume", type=float, default=0.6)
    args = ap.parse_args()

    check_deps()

    scenes = []
    if args.manifest:
        with open(args.manifest) as f:
            man = json.load(f)
        scenes = man.get("scenes", [])
        if not args.audio and man.get("audio"):
            args.audio = man["audio"]
            args.audio_volume = man.get("audio_volume", args.audio_volume)
        if not args.title and man.get("title"):
            args.title = man["title"]
    else:
        for c in args.clips:
            scenes.append({"file": c, "transition": "crossfade" if args.crossfade else "cut"})

    if not scenes:
        print("No scenes provided", file=sys.stderr)
        sys.exit(1)

    tmp = tempfile.mkdtemp(prefix="sceneasm_")
    processed = []

    # Optional title
    if args.title:
        title_path = os.path.join(tmp, "title.mp4")
        # Probe first scene for size
        first = scenes[0]["file"]
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0", first],
            capture_output=True, text=True)
        w, h = map(int, r.stdout.strip().split(",")) if r.returncode == 0 else (1920, 1080)
        make_title_card(args.title, args.title_duration, args.fps, w, h, title_path)
        processed.append(title_path)

    # Process scenes
    for i, sc in enumerate(scenes):
        fpath = sc["file"]
        if not os.path.exists(fpath):
            print(f"Missing scene: {fpath}", file=sys.stderr)
            sys.exit(1)
        processed.append(fpath)

    # Simple concat for now (crossfade can be expanded)
    silent = os.path.join(tmp, "silent.mp4")
    concat_simple(processed, silent)

    if args.audio and os.path.exists(args.audio):
        subprocess.run([
            "ffmpeg", "-y", "-v", "error",
            "-i", silent, "-i", args.audio,
            "-filter_complex", f"[1:a]volume={args.audio_volume},apad[a]",
            "-map", "0:v", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest", args.out,
        ], check=True)
    else:
        os.rename(silent, args.out)

    dur = probe_duration(args.out)
    print(f"Assembled: {args.out} ({dur:.1f}s, {len(scenes)} scenes)")


if __name__ == "__main__":
    main()
