#!/usr/bin/env python3
"""
finish.py — Post-interpolation finishing stage for the Cape Jones pipeline.

This is what professional studios do AFTER inbetweening:
  1. QC — automated checks on the interpolated frames
  2. GRADE — apply the Cape Jones signature color grade
  3. AUDIO — mix in music/SFX
  4. ASSEMBLE — final delivery encode

Usage:
  finish.py input.mp4 output.mp4 [--grade cape-jones] [--audio music.mp3] [--no-grade]

The Cape Jones signature grade is tuned for the locked palette:
  - Suit #FFFFFF (pure white) — protected, stays blown out, never tinted
  - Cowl #3E1473 (deep violet) — saturation punched
  - Skin #E5B28C — kept warm and natural
  - Cape #000000 (absolute black) — deepened, not crushed
"""

import argparse
import subprocess
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grades import GRADES, GRADE_INFO, get_grade, list_grades


def qc_check(input_path):
    """Automated QC on the interpolated video. Returns list of issues."""
    issues = []
    # Check: valid video stream
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=nb_frames,r_frame_rate,width,height,duration",
         "-of", "default=noprint_wrappers=1", input_path],
        capture_output=True, text=True)
    if r.returncode != 0:
        issues.append("ffprobe failed — not a valid video")
        return issues
    info = dict(line.split("=") for line in r.stdout.strip().split("\n") if "=" in line)
    # Check: has frames
    frames = info.get("nb_frames", "N/A")
    if frames == "0":
        issues.append("zero frames — likely corrupt")
    elif frames == "N/A":
        # nb_frames can be N/A for images or some codecs; check duration/frames differently
        # For single images, width/height check below is sufficient
        pass
    # Check: reasonable resolution
    w, h = int(info.get("width", 0) or 0), int(info.get("height", 0) or 0)
    if w < 320 or h < 320:
        issues.append(f"suspiciously small resolution: {w}x{h}")
    return issues


def build_filter(grade_name):
    filt = get_grade(grade_name)
    if grade_name not in GRADES:
        print(f"Unknown grade '{grade_name}', using 'cj-day'", file=sys.stderr)
    return filt


def main():
    ap = argparse.ArgumentParser(description="Post-interpolation finishing stage")
    ap.add_argument("input", nargs="?", help="Interpolated video (post-ToonCrafter/RIFE)")
    ap.add_argument("output", nargs="?", help="Finished output video")
    ap.add_argument("--grade", default="cj-day",
                    help="Color grade to apply (default: cj-day). "
                         "Use --list-grades to see all.")
    ap.add_argument("--audio", default=None,
                    help="Audio file to mix under (music/SFX)")
    ap.add_argument("--audio-volume", type=float, default=1.0,
                    help="Audio mix volume (default: 1.0)")
    ap.add_argument("--crf", type=int, default=18,
                    help="Output quality CRF (default: 18)")
    ap.add_argument("--list-grades", action="store_true",
                    help="List all available grades and exit")
    args = ap.parse_args()

    if args.list_grades:
        print("Available color grades:\n")
        for key in sorted(GRADES.keys()):
            info = GRADE_INFO.get(key, ("", "", ""))
            print(f"  {key:20s} {info[0]}")
            if info[1]:
                print(f"  {'':20s} {info[1]}")
        return

    if not args.input or not args.output:
        print("Need input and output. Use --list-grades to see grades.",
              file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.input):
        print(f"Input not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Stage 1: QC
    print("Stage 1/4: QC check...")
    issues = qc_check(args.input)
    if issues:
        print("QC ISSUES:", file=sys.stderr)
        for i in issues:
            print(f"  - {i}", file=sys.stderr)
        sys.exit(1)
    print("  QC passed.")

    # Stage 2+4: Grade + encode (+ audio mix)
    grade_filter = build_filter(args.grade)
    print(f"Stage 2/4: Applying '{args.grade}' grade...")

    cmd = ["ffmpeg", "-y", "-v", "error", "-i", args.input]
    if args.audio:
        if not os.path.exists(args.audio):
            print(f"Audio not found: {args.audio}", file=sys.stderr)
            sys.exit(1)
        cmd += ["-i", args.audio]
        print("Stage 3/4: Mixing audio...")

    if grade_filter:
        cmd += ["-vf", grade_filter]
    else:
        print("  (grade skipped)")

    # Video encode
    cmd += ["-c:v", "libx264", "-crf", str(args.crf), "-preset", "medium",
            "-pix_fmt", "yuv420p"]

    if args.audio:
        # Mix audio: use the provided file, match video duration
        cmd += ["-c:a", "aac", "-b:a", "192k",
                "-filter:a", f"volume={args.audio_volume}",
                "-shortest"]
    # If no audio input, keep any existing audio stream
    elif True:
        cmd += ["-c:a", "aac", "-b:a", "192k"]

    cmd.append(args.output)

    print("Stage 4/4: Final encode...")
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print("ffmpeg failed", file=sys.stderr)
        sys.exit(1)

    # Verify output
    issues = qc_check(args.output)
    if issues:
        print(f"Output QC failed: {issues}", file=sys.stderr)
        sys.exit(1)

    size = os.path.getsize(args.output) / (1024 * 1024)
    print(f"Done: {args.output} ({size:.1f} MB)")


if __name__ == "__main__":
    main()
