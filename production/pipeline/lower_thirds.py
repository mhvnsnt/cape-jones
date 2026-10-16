#!/usr/bin/env python3
"""lower_thirds.py -- animated lower-third graphic -> ProRes 4444 .mov (alpha) + preview mp4.

Renders a broadcast-style lower third: accent bar + name + title slide in with
an ease-out, hold, then slide out. The .mov carries alpha so it can be laid
over footage directly in Kdenlive/Olive/Shotcut; the preview mp4 shows it on a
dark background for quick review.

Usage:
  python3 lower_thirds.py --name "MARS FMMG" --title "Director / Showrunner" -o lt_mars
  python3 lower_thirds.py --name "CAPE JONES" --title "Episode 01" --accent "#FFB020" --style box -o lt_cape

Styles: bar (accent bar + text, default), box (filled box behind text).
"""
import argparse
import math
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def hexcolor(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def ease_out_cubic(t):
    return 1 - (1 - t) ** 3


def main():
    ap = argparse.ArgumentParser(description="animated lower third -> mov(alpha)+mp4")
    ap.add_argument("--name", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("-o", "--out", required=True, help="output basename (no extension)")
    ap.add_argument("--duration", type=float, default=5.0)
    ap.add_argument("--size", default="1920x1080")
    ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--accent", default="#FFB020")
    ap.add_argument("--style", choices=["bar", "box"], default="bar")
    ap.add_argument("--font", default=FONT_BOLD)
    ap.add_argument("--font-reg", default=FONT_REG)
    args = ap.parse_args()

    W, H = map(int, args.size.split("x"))
    fps = args.fps
    n = max(1, int(args.duration * fps))
    accent = hexcolor(args.accent)
    accent_dark = tuple(max(0, c - 60) for c in accent)

    fb, fr = font(args.font, 64), font(args.font_reg, 40)
    tmp_d = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    name_w = tmp_d.textlength(args.name, font=fb)
    title_w = tmp_d.textlength(args.title, font=fr) if args.title else 0
    text_w = max(name_w, title_w)

    # geometry: lower-left, safe margins
    x0, y0 = 120, H - 300
    box_w = int(text_w + 120)
    box_h = 190 if args.title else 130
    intro, outro = 0.6, 0.6  # seconds

    def frame(i):
        t = i / fps
        # slide progress 0..1 in, hold, 1..0 out
        if t < intro:
            p = ease_out_cubic(t / intro)
        elif t > args.duration - outro:
            p = ease_out_cubic(max(0, (args.duration - t) / outro))
        else:
            p = 1.0
        off = int((1 - p) * (box_w + 200))  # slide from left, off-screen
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        bx = x0 - off
        if args.style == "box":
            d.rectangle([bx, y0, bx + box_w, y0 + box_h], fill=(10, 10, 14, 235))
            d.rectangle([bx, y0, bx + 14, y0 + box_h], fill=accent + (255,))
        else:  # bar
            d.rectangle([bx, y0 + 18, bx + 10, y0 + box_h - 18], fill=accent + (255,))
            d.rectangle([bx + 10, y0 + box_h - 6, bx + box_w, y0 + box_h], fill=accent_dark + (255,))
        # text with slight extra lag for style
        toff = int((1 - ease_out_cubic(min(1, t / max(intro * 1.4, 0.01)))) * 60) if t < intro * 1.4 else 0
        if t > args.duration - outro:
            toff = int((1 - p) * 60)
        tx = bx + 48 - toff
        alpha = int(255 * min(1, p * 1.5))
        d.text((tx, y0 + 28), args.name, font=fb, fill=(245, 245, 248, alpha))
        if args.title:
            d.text((tx, y0 + 108), args.title, font=fr, fill=(200, 200, 208, alpha))
        return img

    def run(cmd):
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"FAILED: {' '.join(cmd)}\n{r.stderr[-2000:]}", file=sys.stderr)
            sys.exit(1)

    # ProRes 4444 with alpha
    mov = args.out + ".mov"
    p1 = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba",
         "-s", f"{W}x{H}", "-framerate", str(fps), "-i", "-",
         "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le",
         "-r", str(fps), mov],
        stdin=subprocess.PIPE)
    # preview on dark bg
    mp4 = args.out + "_preview.mp4"
    p2 = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-framerate", str(fps), "-i", "-",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps), mp4],
        stdin=subprocess.PIPE)
    bg = Image.new("RGB", (W, H), (18, 18, 24))
    for i in range(n):
        fr_img = frame(i)
        p1.stdin.write(fr_img.tobytes())
        p2.stdin.write(Image.alpha_composite(bg.convert("RGBA"), fr_img).convert("RGB").tobytes())
        if i % 60 == 0:
            print(f"  frame {i}/{n}", end="\r")
    print()
    for p in (p1, p2):
        p.stdin.close()
        p.wait()
        if p.returncode != 0:
            print(f"ffmpeg exited {p.returncode}", file=sys.stderr)
            sys.exit(1)
    print(f"Wrote {mov} (alpha) and {mp4} (preview)")


if __name__ == "__main__":
    main()
