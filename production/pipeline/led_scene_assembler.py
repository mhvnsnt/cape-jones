#!/usr/bin/env python3
"""
led_scene_assembler.py — Cape Jones LED remote scene builder.

The owner's vision: Cape Jones sitting in his chair holding the LED remote.
He presses the button, the room color changes. Each press = new color.
Ends on party mode (slow spectrum rotation). 15-second vibe segment.

The trick: the room color changes are NOT animation. They're ffmpeg grades
applied on top via led_controller.py presets. The character barely moves.

INPUT: 3 PNG frames the owner draws in FlipaClip:
  sit.png     — sitting in chair, holding remote, thumb resting
  press.png   — thumb pressing the remote button
  release.png — thumb lifting off the button

OUTPUT: MP4 — character sits, presses button (thumb animates), room color
changes ON the press frame, synced. Ends with party mode hold.

Usage:
  # Basic: 5 colors, 3 seconds each, ends on 10s party mode
  led_scene_assembler.py sit.png press.png release.png output.mp4 \
      --sequence purple-pulse chill-blue ember-glow ocean-calm rainbow-smooth

  # Random colors: 6 random presets, 2.5s each
  led_scene_assembler.py sit.png press.png release.png output.mp4 \
      --random 6 --duration 2.5

  # Custom timing + party mode length
  led_scene_assembler.py sit.png press.png release.png output.mp4 \
      --sequence purple-pulse chill-blue rainbow-smooth \
      --duration 4 --party-duration 15 --fps 24

  # With audio underneath
  led_scene_assembler.py sit.png press.png release.png output.mp4 \
      --random 5 --audio music.mp3

How the sync works:
  Each color segment = [sit hold in CURRENT color] -> [press+release in NEW color]
  The grade switches exactly on the press frame. That's the button doing it.

Pipeline position:
  FlipaClip (3 frames) -> led_scene_assembler.py -> finish.py -> delivery
  No GPU needed. All CPU ffmpeg. 3 drawings -> minutes of scene.
"""

import argparse
import os
import random
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from led_controller import PRESETS, get_preset_filter

FPS_DEFAULT = 24
# Thumb animation timing (seconds)
PRESS_HOLD = 0.20    # press.png on screen — thumb down
RELEASE_HOLD = 0.30  # release.png on screen — thumb lifting
# Party mode default: slow spectrum rotation hold at the end
PARTY_PRESET = "rainbow-smooth"
PARTY_DURATION_DEFAULT = 10.0

# Presets too harsh for the random picker (owner can still name them explicitly)
RANDOM_EXCLUDE = {"party-strobe", "strobe-white"}


def check_deps():
    for tool in ("ffmpeg", "ffprobe"):
        r = subprocess.run(["which", tool], capture_output=True)
        if r.returncode != 0:
            print(f"Missing dependency: {tool}", file=sys.stderr)
            sys.exit(1)


def probe_size(png_path):
    """Get WxH of a PNG via ffprobe."""
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height",
         "-of", "csv=p=0", png_path],
        capture_output=True, text=True)
    if r.returncode != 0:
        print(f"ffprobe failed on {png_path}", file=sys.stderr)
        sys.exit(1)
    w, h = r.stdout.strip().split(",")
    return int(w), int(h)


def make_still_clip(png_path, duration, grade_filter, out_path, fps, crf,
                    width, height, speed=1.0):
    """
    Loop a single PNG for `duration` seconds, apply the LED grade.
    Normalizes to width x height so all segments concat cleanly.
    """
    frames = max(1, int(round(duration * fps)))
    vf = (
        f"scale={width}:{height}:flags=lanczos,"
        f"format=yuv420p,{grade_filter}"
    )
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-loop", "1", "-framerate", str(fps), "-i", png_path,
        "-frames:v", str(frames),
        "-vf", vf,
        "-r", str(fps),
        "-c:v", "libx264", "-crf", str(crf),
        "-preset", "medium", "-pix_fmt", "yuv420p",
        out_path,
    ]
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print(f"ffmpeg failed building clip from {png_path}", file=sys.stderr)
        sys.exit(1)


def concat_clips(clip_paths, out_path, crf):
    """Concat MP4 segments (same codec/dims) without re-encoding."""
    with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False) as f:
        for p in clip_paths:
            # escape single quotes for concat demuxer
            f.write(f"file '{p.replace(chr(39), chr(39)+chr(92)+chr(39)+chr(39))}'\n")
        list_path = f.name
    try:
        cmd = [
            "ffmpeg", "-y", "-v", "error",
            "-f", "concat", "-safe", "0", "-i", list_path,
            "-c", "copy",
            out_path,
        ]
        r = subprocess.run(cmd)
        if r.returncode != 0:
            print("ffmpeg concat failed", file=sys.stderr)
            sys.exit(1)
    finally:
        os.unlink(list_path)


def pick_random(n, seed=None):
    """Pick n random presets (no immediate repeats)."""
    if seed is not None:
        random.seed(seed)
    pool = [k for k in PRESETS if k not in RANDOM_EXCLUDE]
    picks = []
    while len(picks) < n:
        c = random.choice(pool)
        if picks and picks[-1] == c:
            continue
        picks.append(c)
    return picks


def build_sequence(args):
    """Resolve the preset sequence from --sequence or --random."""
    if args.sequence:
        seq = args.sequence
        unknown = [s for s in seq if s not in PRESETS]
        if unknown:
            print(f"Unknown presets: {', '.join(unknown)}", file=sys.stderr)
            print("Run led_controller.py --list to see all.", file=sys.stderr)
            sys.exit(1)
        return seq
    n = args.random or 5
    seq = pick_random(n, seed=args.seed)
    print(f"Random sequence ({n}): {' -> '.join(seq)}")
    return seq


def main():
    ap = argparse.ArgumentParser(
        description="Cape Jones LED remote scene assembler — "
                    "3 drawings in, finished vibe segment out.")
    ap.add_argument("sit", help="sit.png — sitting, holding remote")
    ap.add_argument("press", help="press.png — thumb pressing button")
    ap.add_argument("release", help="release.png — thumb lifting off")
    ap.add_argument("output", help="Output MP4")
    ap.add_argument("--sequence", nargs="+", default=None,
                    help="Preset names in order (see led_controller.py --list)")
    ap.add_argument("--random", type=int, default=None, metavar="N",
                    help="Pick N random presets instead of --sequence")
    ap.add_argument("--seed", type=int, default=None,
                    help="Random seed for reproducible --random picks")
    ap.add_argument("--duration", type=float, default=3.0,
                    help="Seconds to sit in each color (default: 3.0)")
    ap.add_argument("--party-duration", type=float,
                    default=PARTY_DURATION_DEFAULT,
                    help="Seconds to hold the final party mode "
                         f"(default: {PARTY_DURATION_DEFAULT}). "
                         "0 = no party hold, end after last press.")
    ap.add_argument("--party-preset", default=PARTY_PRESET,
                    help=f"Preset for the final hold (default: {PARTY_PRESET})")
    ap.add_argument("--no-party", action="store_true",
                    help="Skip the party-mode ending entirely")
    ap.add_argument("--speed", type=float, default=1.0,
                    help="LED animation speed multiplier (default: 1.0)")
    ap.add_argument("--fps", type=int, default=FPS_DEFAULT,
                    help=f"Output framerate (default: {FPS_DEFAULT})")
    ap.add_argument("--audio", default=None,
                    help="Audio file to mix under the scene")
    ap.add_argument("--audio-volume", type=float, default=0.7,
                    help="Audio mix volume (default: 0.7)")
    ap.add_argument("--crf", type=int, default=18,
                    help="Output quality CRF (default: 18)")
    ap.add_argument("--list", action="store_true",
                    help="List presets and exit")
    args = ap.parse_args()

    if args.list:
        print("LED presets:\n")
        for key in sorted(PRESETS):
            print(f"  {key:16s} {PRESETS[key][0]}")
        return

    check_deps()

    for p, label in ((args.sit, "sit"), (args.press, "press"),
                     (args.release, "release")):
        if not os.path.exists(p):
            print(f"{label} frame not found: {p}", file=sys.stderr)
            sys.exit(1)

    if args.party_preset not in PRESETS:
        print(f"Unknown party preset: {args.party_preset}", file=sys.stderr)
        sys.exit(1)

    seq = build_sequence(args)
    if len(seq) < 1:
        print("Need at least one preset in the sequence.", file=sys.stderr)
        sys.exit(1)

    # Normalize all segments to the sit frame's dimensions
    width, height = probe_size(args.sit)
    for p, label in ((args.press, "press"), (args.release, "release")):
        w, h = probe_size(p)
        if (w, h) != (width, height):
            print(f"Note: {label} frame is {w}x{h}, scaling to "
                  f"{width}x{height} to match sit frame.")

    print(f"Canvas: {width}x{height} @ {args.fps}fps")
    print(f"Sequence: {' -> '.join(seq)}")
    print(f"Sit per color: {args.duration}s | "
          f"press: {PRESS_HOLD}s | release: {RELEASE_HOLD}s")

    tmpdir = tempfile.mkdtemp(prefix="ledscene_")
    clips = []
    try:
        # Build each color segment.
        # Segment i: sit in color[i], then press+release graded with
        # color[i+1] — the room changes ON the button press.
        for i, preset in enumerate(seq):
            filt = get_preset_filter(preset, speed=args.speed)

            # Sit hold in the current color
            sit_dur = args.duration
            sit_clip = os.path.join(tmpdir, f"seg{i:02d}_sit.mp4")
            make_still_clip(args.sit, sit_dur, filt, sit_clip,
                            args.fps, args.crf, width, height)
            clips.append(sit_clip)

            # Button press -> color changes here.
            # The press+release frames wear the NEXT color's grade,
            # unless this is the last segment.
            if i < len(seq) - 1:
                next_filt = get_preset_filter(seq[i + 1], speed=args.speed)
            else:
                # Last color: press into the party hold (or just end)
                if args.no_party or args.party_duration <= 0:
                    next_filt = filt
                else:
                    next_filt = get_preset_filter(args.party_preset,
                                                  speed=args.speed)

            press_clip = os.path.join(tmpdir, f"seg{i:02d}_press.mp4")
            make_still_clip(args.press, PRESS_HOLD, next_filt, press_clip,
                            args.fps, args.crf, width, height)
            clips.append(press_clip)

            rel_clip = os.path.join(tmpdir, f"seg{i:02d}_rel.mp4")
            make_still_clip(args.release, RELEASE_HOLD, next_filt, rel_clip,
                            args.fps, args.crf, width, height)
            clips.append(rel_clip)

        # Final party hold: just sitting, spectrum slowly rotating.
        # No more button presses — "he flicks to the one where it's just
        # doing the thing where it's slowly rotating through the whole
        # spectrum of colors like how the party lights do."
        if not args.no_party and args.party_duration > 0:
            party_filt = get_preset_filter(args.party_preset,
                                           speed=args.speed)
            party_clip = os.path.join(tmpdir, "party_hold.mp4")
            make_still_clip(args.sit, args.party_duration, party_filt,
                            party_clip, args.fps, args.crf, width, height)
            clips.append(party_clip)
            print(f"Party hold: {args.party_duration}s of "
                  f"{args.party_preset} ({PRESETS[args.party_preset][0]})")

        # Stitch everything together
        silent_out = os.path.join(tmpdir, "assembled_silent.mp4")
        concat_clips(clips, silent_out, args.crf)

        # Optional audio mix
        if args.audio:
            if not os.path.exists(args.audio):
                print(f"Audio not found: {args.audio}", file=sys.stderr)
                sys.exit(1)
            cmd = [
                "ffmpeg", "-y", "-v", "error",
                "-i", silent_out,
                "-i", args.audio,
                "-filter_complex",
                f"[1:a]volume={args.audio_volume},apad[a]",
                "-map", "0:v", "-map", "[a]",
                "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k",
                "-shortest",
                args.output,
            ]
            r = subprocess.run(cmd)
            if r.returncode != 0:
                print("ffmpeg audio mix failed", file=sys.stderr)
                sys.exit(1)
        else:
            os.rename(silent_out, args.output)

        # Report
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "format=duration", "-of", "csv=p=0", args.output],
            capture_output=True, text=True)
        dur = float(r.stdout.strip()) if r.returncode == 0 else 0.0
        size = os.path.getsize(args.output) / (1024 * 1024)
        total_presses = len(seq) - 1 + (0 if args.no_party else 1)
        print(f"\nDone: {args.output}")
        print(f"  {dur:.1f}s, {size:.1f} MB, {len(seq)} colors, "
              f"{total_presses} button presses")
        print(f"  3 drawings -> {dur:.0f} seconds of scene. "
              f"No GPU. All CPU ffmpeg.")
    finally:
        # Clean up segment clips
        for c in clips:
            if os.path.exists(c):
                os.unlink(c)
        try:
            os.rmdir(tmpdir)
        except OSError:
            pass


if __name__ == "__main__":
    main()
