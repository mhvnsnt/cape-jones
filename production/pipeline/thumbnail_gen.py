#!/usr/bin/env python3
"""
thumbnail_gen.py — episode thumbnail generator.

Picks the best frame(s) from a finished video and builds a
clickable episode thumbnail:
  - samples N frames across the video
  - scores each by brightness variance + edge density (picks punchy frames)
  - crops to 16:9, upscales, sharpens
  - optionally burns in episode title text

Usage:
  python3 thumbnail_gen.py episode.mp4 thumb.jpg
  python3 thumbnail_gen.py episode.mp4 thumb.jpg --title "CAPE JONES EP01"
  python3 thumbnail_gen.py episode.mp4 thumb.jpg --candidates 24 --title "NUDE JONES"
  python3 thumbnail_gen.py episode.mp4 thumb.jpg --list-frames   # just show scores

Requires: ffmpeg, ffprobe, Python PIL (Pillow).
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import shutil

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageStat
except ImportError:
    sys.exit("ERROR: Pillow required: pip install Pillow")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ERROR: {' '.join(cmd[:3])} failed:\n{r.stderr[:500]}")
    return r.stdout


def get_duration(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "json", path])
    return float(json.loads(out)["format"]["duration"])


def score_frame(path):
    """Higher = punchier thumbnail candidate."""
    im = Image.open(path).convert("RGB")
    small = im.resize((160, 90))
    stat = ImageStat.Stat(small)
    # brightness variance across channels = colorful/contrasty
    var = sum(stat.var) / 3.0
    # edge density via FIND_EDGES
    edges = small.filter(ImageFilter.FIND_EDGES).convert("L")
    estat = ImageStat.Stat(edges)
    edge = estat.mean[0]
    # penalize near-black frames (letterbox / fades)
    bright = stat.mean
    mean_bright = sum(bright) / 3.0
    if mean_bright < 25:
        return -1
    return var * 0.5 + edge * 2.0


def main():
    ap = argparse.ArgumentParser(description="episode thumbnail generator")
    ap.add_argument("input", help="finished episode video")
    ap.add_argument("output", help="output jpg (omit with --list-frames)")
    ap.add_argument("--candidates", type=int, default=16,
                    help="frames to sample (default 16)")
    ap.add_argument("--title", default=None, help="burn-in title text")
    ap.add_argument("--list-frames", action="store_true",
                    help="print candidate scores, don't render")
    ap.add_argument("--width", type=int, default=1280, help="output width")
    ns = ap.parse_args()

    if not shutil.which("ffmpeg"):
        sys.exit("ERROR: ffmpeg not found")

    dur = get_duration(ns.input)
    # sample across middle 80% (skip cold open fade-in / end card)
    times = [dur * (0.1 + 0.8 * i / max(ns.candidates - 1, 1))
             for i in range(ns.candidates)]

    tmpd = tempfile.mkdtemp(prefix="thumbgen_")
    scored = []
    for i, t in enumerate(times):
        fp = os.path.join(tmpd, f"c{i:02d}.png")
        # clamp seek inside duration; skip if extraction fails
        tc = min(t, max(dur - 0.1, 0.05))
        r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{tc:.2f}",
                            "-i", ns.input, "-frames:v", "1", fp])
        if r.returncode != 0 or not os.path.exists(fp):
            continue
        try:
            s = score_frame(fp)
        except Exception:
            continue
        scored.append((s, t, fp))

    if not scored:
        shutil.rmtree(tmpd, ignore_errors=True)
        sys.exit("ERROR: could not extract any frames")

    scored.sort(reverse=True)
    if ns.list_frames:
        for s, t, _ in scored:
            print(f"  t={t:7.2f}s  score={s:10.1f}")
        shutil.rmtree(tmpd, ignore_errors=True)
        return

    if not ns.output:
        sys.exit("ERROR: output path required (or use --list-frames)")

    best = scored[0][2]
    print(f"best frame: t={scored[0][1]:.2f}s score={scored[0][0]:.1f}",
          file=sys.stderr)
    im = Image.open(best).convert("RGB")

    # 16:9 center crop
    w, h = im.size
    target_ratio = 16 / 9
    if w / h > target_ratio:
        nw = int(h * target_ratio)
        x0 = (w - nw) // 2
        im = im.crop((x0, 0, x0 + nw, h))
    else:
        nh = int(w / target_ratio)
        y0 = (h - nh) // 2
        im = im.crop((0, y0, w, y0 + nh))

    im = im.resize((ns.width, int(ns.width * 9 / 16)), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=3))

    if ns.title:
        d = ImageDraw.Draw(im)
        # try a bold font, fall back to default
        font = None
        for fp in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                   "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"]:
            if os.path.exists(fp):
                try:
                    font = ImageFont.truetype(fp, size=ns.width // 14)
                    break
                except Exception:
                    pass
        if font is None:
            font = ImageFont.load_default()
        text = ns.title
        # bottom-left with black stroke for readability
        x, y = ns.width // 20, ns.width * 9 // 16 - ns.width // 8
        for dx in (-3, 3):
            for dy in (-3, 3):
                d.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0))
        d.text((x, y), text, font=font, fill=(255, 255, 255))

    im.save(ns.output, "JPEG", quality=92)
    print(f"wrote {ns.output}")
    shutil.rmtree(tmpd, ignore_errors=True)


if __name__ == "__main__":
    main()
