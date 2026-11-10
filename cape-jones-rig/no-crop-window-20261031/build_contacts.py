#!/usr/bin/env python3
"""Clean before/after contacts: OLD (fixed window) left, NEW (no-crop) right.
Checker background is DISPLAY ONLY for viewing; figure files stay RGBA.
Each cell: label on top, OLD tile, NEW tile, with the tile's own size
and edge-touch note underneath. Tiles are scaled to a common height
for display; scaling here does not change the figure files."""
import os, sys
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

def contact(pairs, path, title):
    # pairs: (label, old_path, new_path, note_old, note_new)
    tw = 260; cell_w = tw * 2 + 24; head = 64
    # uniform tile height: use the tallest tile among all, capped
    tiles = []
    for lab, op, np_, no, nn in pairs:
        o = on_checker(Image.open(op).convert("RGBA"))
        n = on_checker(Image.open(np_).convert("RGBA"))
        tiles.append((lab, o, n, no, nn))
    th = max(max(o.size[1], n.size[1]) for _, o, n, _, _ in tiles)
    th = min(th, 340)
    cell_h = head + th + 36
    cols = 2; rows = (len(pairs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h + 30), (230, 230, 230))
    d = ImageDraw.Draw(sheet)
    d.text((8, 8), title + "  |  checker = DISPLAY ONLY, figure files are transparent RGBA", fill=(0, 0, 0))
    for i, (lab, o, n, no, nn) in enumerate(tiles):
        x, y = (i % cols) * cell_w, 30 + (i // cols) * cell_h
        d.text((x + 8, y + 4), lab, fill=(0, 0, 0))
        d.text((x + 8, y + 20), "OLD fixed window", fill=(180, 0, 0))
        d.text((x + tw + 16, y + 20), "NEW no-crop", fill=(0, 120, 0))
        d.text((x + 8, y + 36), no, fill=(120, 0, 0))
        d.text((x + tw + 16, y + 36), nn, fill=(0, 100, 0))
        sheet.paste(o.resize((tw, th)) if o.size[1] != th else o, (x + 8, y + head))
        sheet.paste(n.resize((tw, th)) if n.size[1] != th else n, (x + tw + 16, y + head))
    sheet.save(path); print(path, sheet.size)

import json
data = json.load(open(os.path.join(ROOT, "measurements-20261031.json")))
def note_old(r):
    lost = r.get("old_lost_vs_truth", r.get("old_lost"))
    et = r["old_edge_touch"]
    return f"lost {lost}px, edge L{et['left']} B{et['bottom']}"
def note_new(r):
    lost = r.get("new_lost_vs_truth", r.get("new_lost"))
    et = r["new_edge_touch"]
    return f"lost {lost}px, edge 0"
g5 = [(r["variant"], os.path.join(ROOT, "frames-old", r["variant"] + ".png"),
       os.path.join(ROOT, "frames-new", r["variant"] + ".png"), note_old(r), note_new(r))
      for r in data["g5"]]
contact(g5, os.path.join(ROOT, "proofs", "g5-before-after-contact-20261031.png"),
        "G5 motion-pose: OLD fixed window vs NEW no-crop (all 20 variants)")
lean = [(r["variant"], os.path.join(ROOT, "frames-old", r["variant"] + ".png"),
         os.path.join(ROOT, "frames-new", r["variant"] + ".png"), note_old(r), note_new(r))
        for r in data["lean_tests"]]
contact(lean, os.path.join(ROOT, "proofs", "lean-before-after-contact-20261031.png"),
        "LEAN TESTS: foot/piece clipping before vs whole figure after")
