#!/usr/bin/env python3
"""
anime_fx.py — Anime-style 2D effect overlays for Cape Jones.

Generates:
  --speed-lines   Radial speed lines (manga/anime surprise/speed effect)
  --impact        White impact flash frame(s) with optional starburst
  --shake         Screen shake (for hits/explosions)
  --speed-overlay Apply speed lines as overlay on a video segment

All CPU, PIL/numpy only. No GPU needed.

Examples:
  # Generate 24 speed-line frames (1 sec @ 24fps), 1080x1920
  python3 anime_fx.py --speed-lines --frames 24 --size 1080x1920 -o speedlines/

  # Generate 3 impact flash frames
  python3 anime_fx.py --impact --frames 3 --size 1080x1920 -o impact/

  # Overlay speed lines onto a video for 2 seconds starting at 5s
  python3 anime_fx.py --speed-overlay input.mp4 --start 5 --duration 2 -o output.mp4
"""
import argparse, os, math, subprocess, sys
import numpy as np

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("pip install pillow numpy")


def parse_size(s):
    w, h = s.lower().split("x")
    return int(w), int(h)


def gen_speed_lines(w, h, n_frames, seed=7, line_count=90, cx=None, cy=None):
    """Radial speed lines emanating from center (or given point)."""
    rng = np.random.default_rng(seed)
    cx = cx or w // 2
    cy = cy or h // 2
    max_r = math.hypot(w, h)
    frames = []
    for f in range(n_frames):
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        # rotate slightly each frame for shimmer
        rot = (f / n_frames) * 0.12
        for _ in range(line_count):
            ang = rng.uniform(0, 2 * math.pi) + rot
            r0 = rng.uniform(max_r * 0.25, max_r * 0.55)
            r1 = r0 + rng.uniform(max_r * 0.15, max_r * 0.45)
            x0, y0 = cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)
            x1, y1 = cx + r1 * math.cos(ang), cy + r1 * math.sin(ang)
            width = int(rng.integers(2, 7))
            alpha = int(rng.integers(140, 255))
            d.line([x0, y0, x1, y1], fill=(255, 255, 255, alpha), width=width)
        frames.append(img)
    return frames


def gen_impact_frames(w, h, n_frames, seed=3):
    """White flash frames with starburst lines. Frame 0 = full white."""
    rng = np.random.default_rng(seed)
    cx, cy = w // 2, h // 2
    max_r = math.hypot(w, h)
    frames = []
    for f in range(n_frames):
        if f == 0:
            frames.append(Image.new("RGBA", (w, h), (255, 255, 255, 255)))
            continue
        fade = 1.0 - (f / n_frames)
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        # jagged starburst
        pts = []
        spikes = 12
        for i in range(spikes * 2):
            ang = (i / (spikes * 2)) * 2 * math.pi
            r = max_r * (0.55 if i % 2 == 0 else 0.30) * fade
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        d.polygon(pts, fill=(255, 255, 255, int(230 * fade)))
        # radiating lines
        for _ in range(40):
            ang = rng.uniform(0, 2 * math.pi)
            r0 = max_r * 0.35 * fade
            r1 = r0 + rng.uniform(max_r * 0.1, max_r * 0.3)
            d.line([cx + r0 * math.cos(ang), cy + r0 * math.sin(ang),
                    cx + r1 * math.cos(ang), cy + r1 * math.sin(ang)],
                   fill=(255, 255, 255, int(200 * fade)), width=4)
        frames.append(img)
    return frames


def apply_shake(input_mp4, output_mp4, start, duration, magnitude=18, fps=24):
    """Screen shake via ffmpeg crop w/ sinusoidal offsets on a segment."""
    # Use ffmpeg's crop with animated x/y via sendcmd is complex;
    # simpler: use the 'shake' via crop filter with time-based expressions.
    vf = (
        f"crop=w=iw-40:h=ih-40:"
        f"x='20+{magnitude}*sin(2*PI*13*t)':"
        f"y='20+{magnitude}*cos(2*PI*17*t)',"
        f"scale=iw+40:ih+40"
    )
    # Apply only to the segment: split, filter, concat
    cmd = [
        "ffmpeg", "-y", "-i", input_mp4,
        "-filter_complex",
        f"[0:v]trim=0:{start},setpts=PTS-STARTPTS[a];"
        f"[0:v]trim={start}:{start+duration},setpts=PTS-STARTPTS,"
        f"{vf}[b];"
        f"[0:v]trim={start+duration},setpts=PTS-STARTPTS[c];"
        f"[a][b][c]concat=n=3:v=1:a=0[v]",
        "-map", "[v]", "-map", "0:a?", "-c:v", "libx264",
        "-preset", "medium", "-crf", "18", "-c:a", "aac", output_mp4,
    ]
    subprocess.run(cmd, check=True)
    print(f"shake -> {output_mp4}")


def overlay_png_sequence(input_mp4, png_dir, output_mp4, start, duration, fps=24):
    """Overlay a PNG sequence (with alpha) onto video at given time."""
    cmd = [
        "ffmpeg", "-y", "-i", input_mp4,
        "-framerate", str(fps), "-i", os.path.join(png_dir, "frame_%03d.png"),
        "-filter_complex",
        f"[1:v]trim=duration={duration},setpts=PTS-STARTPTS,"
        f"format=rgba[fx];"
        f"[0:v][fx]overlay=0:0:enable='between(t,{start},{start+duration})'[v]",
        "-map", "[v]", "-map", "0:a?", "-c:v", "libx264",
        "-preset", "medium", "-crf", "18", "-c:a", "aac",
        "-shortest", output_mp4,
    ]
    subprocess.run(cmd, check=True)
    print(f"overlay -> {output_mp4}")


def main():
    ap = argparse.ArgumentParser(description="Anime-style 2D FX generator")
    ap.add_argument("--speed-lines", action="store_true")
    ap.add_argument("--impact", action="store_true")
    ap.add_argument("--frames", type=int, default=24)
    ap.add_argument("--size", default="1080x1920")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("-o", "--output", required=True,
                    help="Output dir (for frame gen) or mp4 (for overlay/shake)")
    ap.add_argument("--speed-overlay", metavar="INPUT_MP4")
    ap.add_argument("--shake-input", metavar="INPUT_MP4")
    ap.add_argument("--start", type=float, default=0)
    ap.add_argument("--duration", type=float, default=2)
    ap.add_argument("--magnitude", type=int, default=18)
    ap.add_argument("--fps", type=int, default=24)
    args = ap.parse_args()

    w, h = parse_size(args.size)

    if args.speed_lines or args.impact:
        frames = (gen_speed_lines(w, h, args.frames, args.seed)
                  if args.speed_lines
                  else gen_impact_frames(w, h, args.frames, args.seed))
        os.makedirs(args.output, exist_ok=True)
        for i, fr in enumerate(frames):
            fr.save(os.path.join(args.output, f"frame_{i:03d}.png"))
        print(f"Wrote {len(frames)} frames to {args.output}/")
        return

    if args.speed_overlay:
        tmp = "/tmp/anime_fx_speedlines"
        frames = gen_speed_lines(w, h, int(args.duration * args.fps), args.seed)
        os.makedirs(tmp, exist_ok=True)
        for i, fr in enumerate(frames):
            fr.save(os.path.join(tmp, f"frame_{i:03d}.png"))
        overlay_png_sequence(args.speed_overlay, tmp, args.output,
                             args.start, args.duration, args.fps)
        return

    if args.shake_input:
        apply_shake(args.shake_input, args.output, args.start,
                    args.duration, args.magnitude, args.fps)
        return

    ap.print_help()


if __name__ == "__main__":
    main()
