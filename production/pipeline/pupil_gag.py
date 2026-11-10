#!/usr/bin/env python3
"""
pupil_gag.py — Cape Jones pupil gag automation.

Classic cartoon gag: character looks at something, pupils snap to a direction,
then snap back. Or the "pupils shrink to dots" shock gag.

This script takes a sequence of face close-up frames (or a short clip) and
inserts the pupil reaction frames at the right moment.

Usage:
  # Simple: insert shock pupils at frame 12 for 4 frames
  pupil_gag.py faces/*.png --shock-at 12 --shock-frames 4 --out gag_sequence/

  # Directional look: pupils look left for 8 frames starting at frame 20
  pupil_gag.py faces/*.png --look left --at 20 --hold 8 --out gag_sequence/

  # From a short clip
  pupil_gag.py input.mp4 --shock-at 0.5 --out gag.mp4
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw


def make_shock_pupils(base: Image.Image, intensity: float = 1.0) -> Image.Image:
    """Draw tiny black dots as pupils on a face frame (simple overlay)."""
    img = base.copy().convert("RGBA")
    draw = ImageDraw.Draw(img)
    w, h = img.size
    # Approximate eye positions (center-ish, can be refined with landmarks later)
    left = (int(w * 0.38), int(h * 0.42))
    right = (int(w * 0.62), int(h * 0.42))
    r = max(2, int(min(w, h) * 0.015 * intensity))
    for cx, cy in (left, right):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 0, 0, 255))
    return img


def make_look(base: Image.Image, direction: str) -> Image.Image:
    """Shift pupils in a direction."""
    img = base.copy().convert("RGBA")
    draw = ImageDraw.Draw(img)
    w, h = img.size
    # Base eye centers
    eyes = [(int(w * 0.38), int(h * 0.42)), (int(w * 0.62), int(h * 0.42))]
    offsets = {
        "left": (-int(w * 0.04), 0),
        "right": (int(w * 0.04), 0),
        "up": (0, -int(h * 0.03)),
        "down": (0, int(h * 0.03)),
    }
    dx, dy = offsets.get(direction, (0, 0))
    r = max(3, int(min(w, h) * 0.02))
    for cx, cy in eyes:
        draw.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                     fill=(0, 0, 0, 255))
    return img


def process_frames(paths, out_dir, shock_at=None, shock_frames=4,
                   look=None, look_at=None, look_hold=6):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, p in enumerate(sorted(paths)):
        img = Image.open(p)
        if shock_at is not None and shock_at <= i < shock_at + shock_frames:
            img = make_shock_pupils(img)
        elif look and look_at is not None and look_at <= i < look_at + look_hold:
            img = make_look(img, look)
        img.convert("RGB").save(out_dir / Path(p).name)


def main():
    ap = argparse.ArgumentParser(description="Pupil gag automation")
    ap.add_argument("inputs", nargs="+", help="Frame PNGs or a video")
    ap.add_argument("--out", required=True, help="Output dir or video")
    ap.add_argument("--shock-at", type=int, help="Frame index to start shock pupils")
    ap.add_argument("--shock-frames", type=int, default=4)
    ap.add_argument("--look", choices=["left", "right", "up", "down"])
    ap.add_argument("--at", type=int, help="Frame index for look")
    ap.add_argument("--hold", type=int, default=6)
    ap.add_argument("--fps", type=int, default=24)
    args = ap.parse_args()

    # Expand globs if needed
    frames = []
    for pat in args.inputs:
        p = Path(pat)
        if p.is_file() and p.suffix.lower() in {".mp4", ".mov"}:
            # Extract frames first
            work = Path(args.out).parent / ".pupil_tmp"
            work.mkdir(exist_ok=True)
            subprocess.run([
                "ffmpeg", "-y", "-v", "error", "-i", str(p),
                str(work / "f%04d.png"),
            ], check=True)
            frames = sorted(work.glob("f*.png"))
            break
        else:
            frames.extend(Path().glob(pat) if "*" in pat else [p])

    if not frames:
        print("No frames found", file=sys.stderr)
        sys.exit(1)

    out = Path(args.out)
    if out.suffix.lower() in {".mp4", ".mov"}:
        tmp = out.parent / ".pupil_out"
        process_frames(frames, tmp, args.shock_at, args.shock_frames,
                       args.look, args.at, args.hold)
        subprocess.run([
            "ffmpeg", "-y", "-v", "error",
            "-framerate", str(args.fps), "-i", str(tmp / "f%04d.png"),
            "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
            str(out),
        ], check=True)
        print(f"Wrote {out}")
    else:
        process_frames(frames, out, args.shock_at, args.shock_frames,
                       args.look, args.at, args.hold)
        print(f"Wrote frames to {out}")


if __name__ == "__main__":
    main()
