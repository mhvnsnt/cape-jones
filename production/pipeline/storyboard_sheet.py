#!/usr/bin/env python3
"""storyboard_sheet.py -- printable storyboard worksheet (panels + shot fields).

Generates a landscape worksheet PNG (and optional PDF) with N 16:9 panels,
each with Scene/Shot, Action, Dialogue, and Duration fields -- for hand
boarding or printing shot lists. Complements Storyboarder (which has its own
printed worksheets) with a zero-dependency printable.

Usage:
  python3 storyboard_sheet.py -o sheet.png --panels 6 --title "CAPE JONES EP01"
  python3 storyboard_sheet.py -o sheet.pdf --panels 8 --cols 4
"""
import argparse

from PIL import Image, ImageDraw, ImageFont

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser(description="printable storyboard worksheet")
    ap.add_argument("-o", "--out", required=True, help=".png or .pdf")
    ap.add_argument("--panels", type=int, default=6)
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--title", default="STORYBOARD")
    ap.add_argument("--project", default="")
    ap.add_argument("--page", default="1")
    ap.add_argument("--w", type=int, default=2200, help="sheet width px")
    args = ap.parse_args()

    W = args.w
    H = int(W / 1.294)  # ~ landscape letter ratio
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    fb, fr, fs = font(FONT_BOLD, 44), font(FONT_REG, 30), font(FONT_REG, 24)
    INK = (30, 30, 34)
    GRID = (150, 150, 158)

    # header
    d.rectangle([0, 0, W, 150], outline=INK, width=4)
    d.text((30, 28), args.title, font=fb, fill=INK)
    if args.project:
        d.text((30, 88), args.project, font=fr, fill=(90, 90, 96))
    d.text((W - 260, 40), f"Page {args.page}", font=fr, fill=INK)
    d.text((W - 260, 88), "Date ______", font=fr, fill=INK)

    cols, rows = args.cols, -(-args.panels // args.cols)
    gx0, gy0 = 30, 180
    gw, gh = W - 60, H - 210
    cw, ch = gw / cols, gh / rows

    fields = [("SCENE / SHOT", 0.62), ("ACTION", 0.74), ("DIALOGUE", 0.86), ("DUR", 0.97)]
    for p in range(args.panels):
        r, c = divmod(p, cols)
        x0, y0 = gx0 + c * cw, gy0 + r * ch
        px, py, pw, ph = x0 + 14, y0 + 14, cw - 28, ch - 28
        # 16:9 panel
        panel_h = pw * 9 / 16
        d.rectangle([px, py, px + pw, py + panel_h], outline=INK, width=3)
        # thirds guides
        for f_ in (1 / 3, 2 / 3):
            d.line([px + pw * f_, py, px + pw * f_, py + panel_h], fill=(210, 210, 216), width=1)
            d.line([px, py + panel_h * f_, px + pw, py + panel_h * f_], fill=(210, 210, 216), width=1)
        fy = py + panel_h + 12
        for label, frac in fields:
            yy = py + ph * frac
            d.text((px, yy - 26), label, font=fs, fill=(110, 110, 118))
            d.line([px, yy, px + pw, yy], fill=GRID, width=2)
        d.text((px, py - 4), f"PANEL {p + 1}", font=fs, fill=(110, 110, 118))

    if args.out.lower().endswith(".pdf"):
        img.save(args.out, "PDF", resolution=150)
    else:
        img.save(args.out)
    print(f"Wrote {args.out} ({args.panels} panels)")


if __name__ == "__main__":
    main()
