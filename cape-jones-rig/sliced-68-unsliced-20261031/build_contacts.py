#!/usr/bin/env python3
"""Proof contacts for the 68-sheet slicing job."""
import json, glob, os
from PIL import Image, ImageDraw
from pathlib import Path

OUT = Path.home() / "workspace/cape-jones-rig/sliced-68-unsliced-20261031"
CH = "grey"

def checker(w, h, s=16):
    im = Image.new("RGB", (w, h), (180, 180, 180))
    d = ImageDraw.Draw(im)
    for y in range(0, h, s):
        for x in range(0, w, s):
            if ((x // s) + (y // s)) % 2 == 0:
                d.rectangle([x, y, x + s - 1, y + s - 1], fill=(220, 220, 220))
    return im

def tile(piece_path, size=300):
    im = Image.open(piece_path).convert("RGBA")
    im.thumbnail((size - 8, size - 36))
    bg = checker(size, size)
    bg.paste(im, ((size - im.width) // 2, (size - im.height) // 2 + 14), im)
    d = ImageDraw.Draw(bg)
    d.text((6, 4), os.path.basename(piece_path), fill=(0, 0, 0))
    return bg

def grid(tiles, cols, tile=300):
    rows = (len(tiles) + cols - 1) // cols
    out = Image.new("RGB", (cols * tile, rows * tile), (90, 90, 90))
    for i, t in enumerate(tiles):
        out.paste(t, ((i % cols) * tile, (i // cols) * tile))
    return out

def main():
    manifests = sorted(glob.glob(str(OUT / "sheets/**/MANIFEST.json"), recursive=True))
    # 1) largest piece per sheet, 68 tiles
    tiles = []
    for mf in manifests:
        d = json.load(open(mf))
        if not d["pieces"]:
            continue
        big = max(d["pieces"], key=lambda p: p["area_px"])
        tiles.append(tile(os.path.join(os.path.dirname(mf), big["file"])))
    grid(tiles, 8).save(OUT / "contact-largest-piece-per-sheet-20261031.png")
    print("largest-piece contact:", len(tiles), "tiles")

    # 2) color-key-sheet-5 grid-split pieces
    for mf in manifests:
        d = json.load(open(mf))
        if d["source"].endswith("color-key-sheet-5.jpg"):
            pieces = [p for p in d["pieces"] if p.get("grid_split")]
            tiles = [tile(os.path.join(os.path.dirname(mf), p["file"])) for p in pieces]
            grid(tiles, 5).save(OUT / "contact-color-key-sheet-5-grid-split-20261031.png")
            print("sheet-5 grid-split pieces:", len(pieces))

    # 3) one sample sheet per group: first 6 pieces each
    for mf in manifests:
        d = json.load(open(mf))
        # pick the first sheet alphabetically per group only
        # (handled by caller loop below via group tracking)
        pass
    seen = set()
    for mf in manifests:
        d = json.load(open(mf))
        if d["group"] in seen:
            continue
        seen.add(d["group"])
        tiles = [tile(os.path.join(os.path.dirname(mf), p["file"])) for p in d["pieces"][:6]]
        grid(tiles, 3).save(OUT / f"contact-sample-{d['group']}-20261031.png")
        print("sample group:", d["group"], len(tiles))

if __name__ == "__main__":
    main()
