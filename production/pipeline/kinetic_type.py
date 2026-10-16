#!/usr/bin/env python3
"""kinetic_type.py -- kinetic typography -> mp4 (or ProRes mov with alpha).

Three motion grammars for animated titles / lyric lines / captions, rendered
with PIL frames piped to ffmpeg. No browser, no GPU needed.

Styles:
  typewriter  characters appear one by one with a block cursor
  word        words pop in one by one; the current word is accent-highlighted
              (TikTok caption style). --wps sets words per second.
  cascade     lines rise into place with a staggered ease-out (hero title style)

Usage:
  python3 kinetic_type.py --text "CAPE JONES" --style cascade -o title.mp4
  python3 kinetic_type.py --file lyrics.txt --style word --wps 3 -o captions.mp4
  python3 kinetic_type.py --text "WIZARD GANG" --style typewriter --transparent -o wg.mov

Multi-line input: lines separated by \\n (or actual newlines in --file).
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
    t = min(1.0, max(0.0, t))
    return 1 - (1 - t) ** 3


def ease_out_back(t):
    t = min(1.0, max(0.0, t))
    c = 1.70158
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2


def main():
    ap = argparse.ArgumentParser(description="kinetic typography -> mp4/mov")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--text", help="text (\\n for line breaks)")
    g.add_argument("--file", help="text file")
    ap.add_argument("--style", choices=["typewriter", "word", "cascade"], default="cascade")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--duration", type=float, default=4.0)
    ap.add_argument("--wps", type=float, default=2.5, help="words/sec for word style")
    ap.add_argument("--cps", type=float, default=18.0, help="chars/sec for typewriter")
    ap.add_argument("--size", default="1920x1080")
    ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--font-size", type=int, default=120)
    ap.add_argument("--fg", default="#F2F2F5")
    ap.add_argument("--accent", default="#FFB020")
    ap.add_argument("--bg", default="#101014", help="background color (mp4 only)")
    ap.add_argument("--transparent", action="store_true",
                    help="ProRes 4444 .mov with alpha instead of mp4")
    ap.add_argument("--font", default=FONT_BOLD)
    args = ap.parse_args()

    text = open(args.file, encoding="utf-8").read() if args.file else args.text
    text = text.replace("\\n", "\n")
    W, H = map(int, args.size.split("x"))
    fps = args.fps
    fg, accent = hexcolor(args.fg), hexcolor(args.accent)
    fnt = font(args.font, args.font_size)
    meas = ImageDraw.Draw(Image.new("RGB", (8, 8)))

    lines = [l for l in text.split("\n")]
    line_h = int(args.font_size * 1.35)
    total_h = line_h * len(lines)
    y_base = (H - total_h) // 2

    # ---- per-style timing plan ----
    if args.style == "typewriter":
        chars = list(" ".join(lines))
        total_units = len(chars) / args.cps
    elif args.style == "word":
        words = " ".join(lines).split()
        total_units = len(words) / args.wps
    else:
        total_units = 0.9 + 0.28 * len(lines)
    hold = 1.2
    duration = max(args.duration, total_units + hold)

    def frame(i):
        t = i / fps
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        if args.style == "typewriter":
            shown = int(t * args.cps)
            joint = "\n".join(lines)
            vlines = joint[:max(0, shown)].split("\n")
            for li, vl in enumerate(vlines):
                y = y_base + li * line_h
                d.text(((W - meas.textlength(lines[li], font=fnt)) / 2, y), vl, font=fnt, fill=fg + (255,))
            # cursor
            if int(t * 2) % 2 == 0 and shown < len(joint):
                last = vlines[-1] if vlines else ""
                li = len(vlines) - 1
                cx = (W - meas.textlength(lines[li], font=fnt)) / 2 + meas.textlength(last, font=fnt)
                d.rectangle([cx + 6, y_base + li * line_h + 8, cx + 26, y_base + li * line_h + args.font_size], fill=accent + (255,))
        elif args.style == "word":
            words = " ".join(lines).split()
            k = int(t * args.wps)
            # re-flow words centered as lines of ~6 words for readability
            per = 6
            wlines = [" ".join(words[j:j + per]) for j in range(0, len(words), per)] or [""]
            lh = int(args.font_size * 1.3)
            yb = (H - lh * len(wlines)) // 2
            wi = 0
            for li, wl in enumerate(wlines):
                ws = wl.split()
                x = W / 2 - sum(meas.textlength(w_ + " ", font=fnt) for w_ in ws) / 2
                for w_ in ws:
                    col = accent if wi == k - 1 and wi < len(words) else fg
                    pop = ease_out_back(min(1, t * args.wps - wi)) if wi < k else 0
                    a = int(255 * pop)
                    if wi < k:
                        d.text((x, yb + li * lh), w_, font=fnt, fill=col + (a,))
                    x += meas.textlength(w_ + " ", font=fnt)
                    wi += 1
        else:  # cascade
            for li, line in enumerate(lines):
                local = t - li * 0.28
                p = ease_out_cubic(local / 0.9)
                dy = int((1 - p) * 90)
                a = int(255 * min(1, local / 0.5)) if local > 0 else 0
                if a > 0:
                    w_ = meas.textlength(line, font=fnt)
                    d.text(((W - w_) / 2, y_base + li * line_h + dy), line, font=fnt, fill=fg + (a,))
        return img

    n = int(duration * fps)
    if args.transparent:
        cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba",
               "-s", f"{W}x{H}", "-framerate", str(fps), "-i", "-",
               "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le",
               "-r", str(fps), args.out]
        cvt = lambda im: im.tobytes()  # noqa: E731
    else:
        cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", f"{W}x{H}", "-framerate", str(fps), "-i", "-",
               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps), args.out]
        bg = Image.new("RGBA", (W, H), hexcolor(args.bg) + (255,))
        cvt = lambda im: Image.alpha_composite(bg, im).convert("RGB").tobytes()  # noqa: E731

    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(cvt(frame(i)))
        if i % 60 == 0:
            print(f"  frame {i}/{n}", end="\r")
    print()
    p.stdin.close()
    rc = p.wait()
    if rc != 0:
        print("ffmpeg failed", file=sys.stderr)
        sys.exit(1)
    print(f"Wrote {args.out} ({duration:.1f}s, {args.style})")


if __name__ == "__main__":
    main()
