#!/usr/bin/env python3
"""Clean contacts v2: aspect-preserving tiles, no stretch.
Checker = DISPLAY ONLY. Plus zoom insets for L3 so the corner leg
piece is actually readable (full-canvas tiles make it tiny)."""
import json, os
from PIL import Image, ImageDraw
ROOT = os.path.expanduser("~/workspace/cape-jones-rig/no-crop-window-20261031")

def on_checker(im, w=260):
    h = int(w * im.size[1] / im.size[0])
    small = im.resize((w, h))
    bg = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(bg)
    for yy in range(0, h, 20):
        for xx in range(0, w, 20):
            if (xx // 20 + yy // 20) % 2 == 0:
                d.rectangle([xx, yy, xx + 20, yy + 20], fill=(205, 205, 205))
    bg.paste(small, (0, 0), small)
    return bg

def contact(pairs, path, title, cols=2):
    tw = 260; cell_w = tw * 2 + 24
    tiles = []
    for lab, op, np_, no, nn, zoom in pairs:
        o = on_checker(Image.open(op).convert("RGBA"))
        n = on_checker(Image.open(np_).convert("RGBA"))
        if zoom:
            # zoom: crop around the figure/piece bbox in each frame
            def z(p):
                im = Image.open(p).convert("RGBA"); bb = im.getbbox()
                x0 = max(0, bb[0] - 30); y0 = max(0, bb[1] - 30)
                x1 = min(im.size[0], bb[2] + 30); y1 = min(im.size[1], bb[3] + 30)
                return on_checker(im.crop((x0, y0, x1, y1)), w=tw)
            o, n = z(op), z(np_)
        tiles.append((lab, o, n, no, nn))
    rows = (len(pairs) + cols - 1) // cols
    row_h = []
    for r in range(rows):
        row = tiles[r * cols:(r + 1) * cols]
        row_h.append(64 + max(max(o.size[1], n.size[1]) for _, o, n, _, _ in row) + 8)
    sheet = Image.new("RGB", (cols * cell_w, 30 + sum(row_h)), (230, 230, 230))
    d = ImageDraw.Draw(sheet)
    d.text((8, 8), title + " | checker = DISPLAY ONLY, figure files are transparent RGBA, tiles keep aspect (no stretch)", fill=(0, 0, 0))
    y = 30
    for r in range(rows):
        for i, (lab, o, n, no, nn) in enumerate(tiles[r * cols:(r + 1) * cols]):
            x = i * cell_w
            d.text((x + 8, y + 4), lab, fill=(0, 0, 0))
            d.text((x + 8, y + 20), "OLD fixed window", fill=(180, 0, 0))
            d.text((x + tw + 16, y + 20), "NEW no-crop", fill=(0, 120, 0))
            d.text((x + 8, y + 36), no, fill=(120, 0, 0))
            d.text((x + tw + 16, y + 36), nn, fill=(0, 100, 0))
            sheet.paste(o, (x + 8, y + 64)); sheet.paste(n, (x + tw + 16, y + 64))
        y += row_h[r]
    sheet.save(path); print(path, sheet.size)

data = json.load(open(os.path.join(ROOT, "measurements-20261031.json")))
def no_(r):
    lost = r.get("old_lost_vs_truth", r.get("old_lost")); et = r["old_edge_touch"]
    return f"lost {lost}px, edge L{et['left']} B{et['bottom']} R{et['right']} T{et['top']}"
def nn_(r):
    lost = r.get("new_lost_vs_truth", r.get("new_lost"))
    return f"lost {lost}px, edge 0"
g5 = [(r["variant"], os.path.join(ROOT, "frames-old", r["variant"] + ".png"),
       os.path.join(ROOT, "frames-new", r["variant"] + ".png"), no_(r), nn_(r), False)
      for r in data["g5"]]
contact(g5, os.path.join(ROOT, "proofs", "g5-before-after-contact-20261031.png"),
        "G5 motion-pose: OLD fixed window vs NEW no-crop (20 variants)")
lean = [(r["variant"], os.path.join(ROOT, "frames-old", r["variant"] + ".png"),
         os.path.join(ROOT, "frames-new", r["variant"] + ".png"), no_(r), nn_(r),
         r["variant"].startswith("L3"))
        for r in data["lean_tests"]]
contact(lean, os.path.join(ROOT, "proofs", "lean-before-after-contact-20261031.png"),
        "LEAN TESTS: foot/piece clipping before vs whole figure after (L3 shown zoomed to the piece)", cols=2)
