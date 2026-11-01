#!/usr/bin/env python3
"""Whole-figure transparent-plate converter.
Method = slice_clean.py clean-cut rule, applied to the WHOLE figure as one
silhouette instead of slicing it into pieces (pieces already exist in
sliced/ and sliced-clean-20261031/ and are NOT re-sliced here):
 1. bg = median of four corners (flat sheet bg, grey 128 on v7c plates)
 2. mask = distance from bg > 30 (keeps white art AND black outlines)
 3. closing 3x3 x2 + hole fill, keep components area >= 800, union
 4. 1px alpha feather + fringe decontamination; interior = original colour
    (never recoloured; light/shadow/bleed stay on their own layers, none here)
 5. NO-CROP: output keeps the ORIGINAL canvas size, never clipped.
rembg is per-piece check only in the standing rule and is NOT the default
for flat sheets (slice_clean doc: on grey it eats white suit edges, on
black it eats the black cape) — a rembg check on one flying plate is run
separately and reported, not used as the conversion.
"""
import os, sys, json
from PIL import Image
import numpy as np
from scipy import ndimage

RIG = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(RIG, "transparent-plates-sweep-20261031", "plates")

SOURCES = []
for rel in ["clips-v7c", "clips", "clips-v7", "clips-v7c-clean-20261031"]:
    base = os.path.join(RIG, rel)
    for dp, _, fs in os.walk(base):
        for f in sorted(fs):
            if f.lower().endswith(".png"):
                SOURCES.append(os.path.join(dp, f))
# reposes-v7c-clean: single figures only, no before-after/crops
base = os.path.join(RIG, "reposes-v7c-clean")
for f in sorted(os.listdir(base)):
    if f.lower().endswith(".png") and not any(k in f for k in ["before-after", "crops"]):
        SOURCES.append(os.path.join(base, f))
SOURCES = sorted(set(SOURCES))

def convert(src, dst):
    im = Image.open(src).convert("RGB")
    arr = np.array(im).astype(float)
    corners = np.concatenate([arr[:5,:5].reshape(-1,3), arr[:5,-5:].reshape(-1,3),
                              arr[-5:,:5].reshape(-1,3), arr[-5:,-5:].reshape(-1,3)])
    bg = np.median(corners, axis=0)
    dist = np.sqrt(((arr - bg)**2).sum(axis=2))
    mask = dist > 30
    mask = ndimage.binary_closing(mask, structure=np.ones((3,3)), iterations=2)
    mask = ndimage.binary_fill_holes(mask)
    lab, n = ndimage.label(mask, structure=np.ones((3,3)))
    keep = np.zeros_like(mask)
    for i in range(1, n+1):
        if (lab == i).sum() >= 800:
            keep |= (lab == i)
    alpha = (keep * 255).astype(float)
    alpha = ndimage.gaussian_filter(alpha, 0.8)
    alpha_u8 = np.clip(alpha, 0, 255).astype(np.uint8)
    rgb = arr.copy()
    a = np.clip(alpha / 255.0, 0.01, 1.0)[..., None]
    rgb = np.clip((arr - bg * (1 - a)) / a, 0, 255)
    rgb[keep] = arr[keep]
    rgba = np.zeros((*arr.shape[:2], 4), dtype=np.uint8)
    rgba[:, :, :3] = rgb.astype(np.uint8)
    rgba[:, :, 3] = alpha_u8
    out = Image.fromarray(rgba, "RGBA")
    out.save(dst)
    ys, xs = np.where(alpha_u8 > 10)
    return {"bg": bg.tolist(), "size": list(im.size),
            "alpha_px": int((alpha_u8 > 10).sum()),
            "alpha_min": int(alpha_u8.min()), "alpha_max": int(alpha_u8.max()),
            "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None}

os.makedirs(OUT, exist_ok=True)
results = []
for src in SOURCES:
    rel = os.path.relpath(src, RIG)
    # flat name: folder path with __, keeps provenance, no collisions
    flat = rel.replace("/", "__")
    dst = os.path.join(OUT, flat)
    r = convert(src, dst)
    r["source"] = rel; r["output"] = "plates/" + flat
    results.append(r)
    print(rel, "->", flat, r["bbox"], r["alpha_px"])
json.dump(results, open(os.path.join(RIG, "transparent-plates-sweep-20261031", "conversion-manifest.json"), "w"), indent=1)
print(f"converted {len(results)}")
