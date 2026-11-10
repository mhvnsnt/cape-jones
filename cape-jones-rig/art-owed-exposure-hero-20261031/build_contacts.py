#!/usr/bin/env python3
import json, os
from PIL import Image, ImageDraw

BASE = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(BASE, "art-owed-exposure-hero-20261031")
SRC = os.path.join(BASE, "transparent-plates-grok-full-sweep-20261031/plates/exposure-sheets")
HERO_SRC = os.path.join(BASE, "transparent-plates-grok-full-sweep-20261031/plates/root/09-hero-shot-black.png")
CT = os.path.join(OUT, "contacts")
MAN = json.load(open(os.path.join(OUT, "MANIFEST-20261031.json")))

def label_bar(w, text):
    bar = Image.new("RGB", (w, 28), (20, 20, 20))
    d = ImageDraw.Draw(bar)
    d.text((6, 6), text, fill=(255, 255, 255))
    return bar

def checker(w, h, s=16):
    img = Image.new("RGB", (w, h), (190, 190, 190))
    d = ImageDraw.Draw(img)
    for y in range(0, h, s):
        for x in range(0, w, s):
            if (x // s + y // s) % 2 == 0:
                d.rectangle([x, y, x + s - 1, y + s - 1], fill=(230, 230, 230))
    return img

def composite_on(im_rgba, bg_rgb):
    bg = bg_rgb.copy()
    bg.paste(im_rgba, (0, 0), im_rgba)
    return bg

# 1. BEFORE contact: 10 original sheets, 5x2
files = ["exposure-sheet-1-walk.png", "exposure-sheet-2-jump.png", "exposure-sheet-3-punch.png",
         "exposure-sheet-4-flight.png", "exposure-sheet-5-reaction.png", "exposure-sheet-6-sit.png",
         "exposure-sheet-7-cape.png", "exposure-sheet-8-turnaround.png", "exposure-sheet-9-run.png",
         "exposure-sheet-10-flex.png"]
tw, th = 360, 470
sheet = Image.new("RGB", (tw * 5, th * 2), (255, 255, 255))
d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(os.path.join(SRC, f)).convert("RGBA")
    im.thumbnail((tw - 8, th - 32))
    bg = checker(im.size[0], im.size[1])
    tile = composite_on(im, bg)
    x = (i % 5) * tw + 4; y = (i // 5) * th + 28
    sheet.paste(tile, (x, y))
    tag = "NOT SPLIT" if "10-flex" in f else "split -> see after contacts"
    d.text(((i % 5) * tw + 6, (i // 5) * th + 6), f"{f}  {tag}", fill=(0, 0, 0))
sheet.save(os.path.join(CT, "contact-before-10-exposure-sheets-20261031.png"))
print("before", sheet.size)

# 2. AFTER contacts: one per split sheet, strips stacked vertically, scaled to width 900
for s in MAN["sheets"]:
    if s["strip_count"] == 0:
        continue
    strips = []
    for e in s["strips"]:
        im = Image.open(os.path.join(OUT, "exposure-strips", e["file"])).convert("RGBA")
        strips.append((e, im))
    W = 900
    # scale each strip to width 900 (keep aspect), plus label bar
    tiles = []
    total_h = 0
    for e, im in strips:
        h = int(im.size[1] * W / im.size[0])
        tiles.append((e, im.resize((W, h), Image.LANCZOS), h))
        total_h += h + 28
    out = Image.new("RGB", (W, total_h), (255, 255, 255))
    y = 0
    for e, tim, h in tiles:
        out.paste(label_bar(W, f"{e['file']}  y {e['y0']}-{e['y1']}"), (0, y)); y += 28
        bg = checker(W, h)
        out.paste(composite_on(tim, bg), (0, y)); y += h
    name = f"contact-after-{s['source'].replace('.png','')}-20261031.png"
    out.save(os.path.join(CT, name))
    print(name, out.size, len(strips))

# 3. AFTER overview: first strip of each split sheet, 3x3
tiles = []
for s in MAN["sheets"]:
    if s["strip_count"] == 0:
        continue
    e = s["strips"][0]
    im = Image.open(os.path.join(OUT, "exposure-strips", e["file"])).convert("RGBA")
    im.thumbnail((340, 280))
    tiles.append((s["source"], e["file"], im))
tw, th = 360, 330
sheet = Image.new("RGB", (tw * 3, th * 3), (255, 255, 255))
d = ImageDraw.Draw(sheet)
for i, (src, fn, im) in enumerate(tiles):
    bg = checker(im.size[0], im.size[1])
    x = (i % 3) * tw + 10; y = (i // 3) * th + 28
    sheet.paste(composite_on(im, bg), (x, y))
    d.text(((i % 3) * tw + 6, (i // 3) * th + 6), f"{src} / {fn}", fill=(0, 0, 0))
sheet.save(os.path.join(CT, "contact-after-overview-first-strip-each-20261031.png"))
print("after overview", sheet.size)

# 4. HERO contact scale: baseline | M1 | M2 on black, same height 900
paths = [("BASELINE (fringe_edge 1190)", HERO_SRC),
         ("M1 decontaminate (275, alpha unchanged)", os.path.join(OUT, "hero-variants/hero-09-M1-decontaminate.png")),
         ("M2 erode 1px (250, alpha -9711)", os.path.join(OUT, "hero-variants/hero-09-M2-erode1.png"))]
H = 900
cols = []
for lab, p in paths:
    im = Image.open(p).convert("RGBA")
    w = int(im.size[0] * H / im.size[1])
    cols.append((lab, im.resize((w, H), Image.LANCZOS), w))
W = sum(c[2] for c in cols) + 8 * 4
out = Image.new("RGB", (W, H + 28), (0, 0, 0))
d = ImageDraw.Draw(out)
x = 0
for lab, im, w in cols:
    d.text((x + 4, 6), lab, fill=(255, 255, 0))
    bg = Image.new("RGB", (w, H), (0, 0, 0))
    out.paste(composite_on(im, bg), (x, 28))
    x += w + 8
out.save(os.path.join(CT, "contact-hero-contact-scale-baseline-M1-M2-20261031.png"))
print("hero contact", out.size)

# 5. HERO zoom: two crops, each 400x400, 3x NEAREST, side by side, on black AND on white? 
# Deliver one contact per crop, with black background (as intended) - fringe colours pop on black.
# Crop A: densest fringe window (160,280). Crop B: right cape (520,1060).
for cname, (cx, cy) in [("cropA-densest-160-280", (160, 280)), ("cropB-right-cape-520-1060", (520, 1060))]:
    cols = []
    for lab, p in paths:
        im = Image.open(p).convert("RGBA").crop((cx, cy, cx + 400, cy + 400))
        cols.append((lab, im.resize((1200, 1200), Image.NEAREST)))
    W = 1200 * 3 + 16
    out = Image.new("RGB", (W, 1200 + 28), (0, 0, 0))
    d = ImageDraw.Draw(out)
    x = 0
    for lab, im in cols:
        d.text((x + 4, 6), lab, fill=(255, 255, 0))
        bg = Image.new("RGB", (1200, 1200), (0, 0, 0))
        out.paste(composite_on(im, bg), (x, 28))
        x += 1200 + 8
    out.save(os.path.join(CT, f"contact-hero-zoom-{cname}-baseline-M1-M2-20261031.png"))
    print(cname, out.size)
print("done")
