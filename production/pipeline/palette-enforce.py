#!/usr/bin/env python3
"""
palette-enforce.py — extract a show palette from key art, then ENFORCE it.

  1. extract: k-means (seeded, numpy-only) dominant colors from reference art
  2. export:  .gpl (Krita/GIMP), .json, .css, .aco-ish text dump
  3. enforce:  quantize target frames/images to the palette (nearest color)

Usage:
  palette-enforce.py extract refs/*.png --colors 24 --out show-palette
  palette-enforce.py enforce show-palette.gpl frames/*.png --outdir frames_pal/
"""
import argparse
import glob
import json
import os
import numpy as np
from PIL import Image

def _kmeans(px, k, seed=7, iters=25):
    rng = np.random.default_rng(seed)
    centers = px[rng.choice(len(px), k, replace=False)].astype(np.float64)
    for _ in range(iters):
        d = ((px[:, None, :] - centers[None, :, :])**2).sum(-1)
        labels = d.argmin(1)
        new = np.array([px[labels == i].mean(0) if (labels == i).any()
                        else centers[i] for i in range(k)])
        if np.allclose(new, centers):
            break
        centers = new
    counts = np.bincount(labels, minlength=k)
    order = np.argsort(-counts)
    return np.clip(centers[order], 0, 255).astype(np.uint8), counts[order]

def _sample_pixels(paths, max_px=60000, seed=7):
    rng = np.random.default_rng(seed)
    allpx = []
    for p in paths:
        im = Image.open(p).convert("RGB")
        im.thumbnail((512, 512))
        a = np.asarray(im).reshape(-1, 3)
        if len(a) > max_px // max(1, len(paths)):
            a = a[rng.choice(len(a), max_px // max(1, len(paths)), replace=False)]
        allpx.append(a)
    return np.concatenate(allpx).astype(np.float64)

def write_gpl(colors, path, name="show-palette"):
    with open(path, "w") as f:
        f.write("GIMP Palette\nName: %s\nColumns: 8\n#\n" % name)
        for c in colors:
            f.write("%3d %3d %3d  #%02x%02x%02x\n" % (c[0], c[1], c[2], c[0], c[1], c[2]))

def read_gpl(path):
    colors = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(("GIMP", "Name:", "Columns:", "#")):
                continue
            parts = line.split()
            colors.append(tuple(int(parts[i]) for i in range(3)))
    return np.array(colors, dtype=np.uint8)

def cmd_extract(args):
    paths = [p for pat in args.refs for p in glob.glob(pat)]
    assert paths, "no reference images matched"
    px = _sample_pixels(paths)
    colors, counts = _kmeans(px, args.colors)
    base = args.out
    write_gpl(colors, base + ".gpl")
    with open(base + ".json", "w") as f:
        json.dump([{"hex": "#%02x%02x%02x" % tuple(c), "px": int(n)}
                   for c, n in zip(colors.tolist(), counts.tolist())], f, indent=1)
    with open(base + ".css", "w") as f:
        f.write(":root {\n" + "".join(
            "  --c%02d: #%02x%02x%02x;\n" % (i, *c) for i, c in enumerate(colors)) + "}\n")
    print(f"extracted {len(colors)} colors -> {base}.gpl/.json/.css")

def cmd_enforce(args):
    pal = read_gpl(args.palette).astype(np.float64)
    os.makedirs(args.outdir, exist_ok=True)
    paths = [p for pat in args.targets for p in glob.glob(pat)]
    for p in paths:
        im = Image.open(p).convert("RGB")
        a = np.asarray(im).astype(np.float64).reshape(-1, 3)
        # chunked nearest-color to bound memory
        out = np.empty_like(a, dtype=np.uint8)
        for i in range(0, len(a), 200000):
            d = ((a[i:i+200000, None, :] - pal[None, :, :])**2).sum(-1)
            out[i:i+200000] = pal[d.argmin(1)].astype(np.uint8)
        Image.fromarray(out.reshape(im.size[1], im.size[0], 3)).save(
            os.path.join(args.outdir, os.path.basename(p)))
    print(f"enforced {args.palette} on {len(paths)} images -> {args.outdir}/")

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extract")
    e.add_argument("refs", nargs="+")
    e.add_argument("--colors", type=int, default=24)
    e.add_argument("--out", default="show-palette")
    n = sub.add_parser("enforce")
    n.add_argument("palette")
    n.add_argument("targets", nargs="+")
    n.add_argument("--outdir", default="frames_pal")
    args = ap.parse_args()
    {"extract": cmd_extract, "enforce": cmd_enforce}[args.cmd](args)

if __name__ == "__main__":
    main()
