#!/usr/bin/env python3
"""Full Grok sheet transparent-plate sweep.
Method = standing clean-cut rule (slice_clean.py), applied to the WHOLE sheet
as one plate, NOT re-sliced into pieces:
 1. bg = median of four corners
 2. mask = distance from bg > 30
 3. closing 3x3 x2 + hole fill
 4. components area >= 800, unioned into one alpha mask
 5. 1px feather (gaussian 0.8) + fringe decontamination, interior = original colour
 6. Output keeps ORIGINAL canvas size (no-crop), RGBA.
Backgrounds group is EXCLUDED by the caller (they are backgrounds, not figures).
"""
import os, sys, json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = Path.home()/"workspace/cape-jones-flying/characters/sheets"
OUT = Path.home()/"workspace/cape-jones-rig/transparent-plates-grok-full-sweep-20261031/plates"

def convert(src, dst):
    im = Image.open(src).convert("RGB")
    arr = np.array(im).astype(float)
    corners = np.concatenate([arr[:5,:5].reshape(-1,3), arr[:5,-5:].reshape(-1,3),
                              arr[-5:,:5].reshape(-1,3), arr[-5:,-5:].reshape(-1,3)])
    bg = np.median(corners, axis=0)
    dist = np.sqrt(((arr-bg)**2).sum(axis=2))
    mask = dist > 30
    mask = ndimage.binary_closing(mask, structure=np.ones((3,3)), iterations=2)
    mask = ndimage.binary_fill_holes(mask)
    lab, n = ndimage.label(mask, structure=np.ones((3,3)))
    objs = ndimage.find_objects(lab)
    keep = np.zeros(mask.shape, dtype=bool)
    comps = 0; comp_px = 0
    for i, sl in enumerate(objs, start=1):
        if sl is None: continue
        area = int((lab[sl]==i).sum())
        if area < 800: continue
        keep[lab==i] = True; comps += 1; comp_px += area
    alpha = (keep*255).astype(float)
    alpha = ndimage.gaussian_filter(alpha, 0.8)
    alpha_u8 = np.clip(alpha, 0, 255).astype(np.uint8)
    a = np.clip(alpha/255.0, 0.01, 1.0)[..., None]
    rgb = np.clip((arr - bg*(1-a))/a, 0, 255)
    rgb[keep] = arr[keep]
    rgba = np.zeros((*arr.shape[:2], 4), dtype=np.uint8)
    rgba[:,:,:3] = rgb.astype(np.uint8); rgba[:,:,3] = alpha_u8
    dst.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(dst)
    ys, xs = np.where(alpha_u8>10)
    bbox = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None
    return {"bg": bg.tolist(), "size": [int(im.width), int(im.height)],
            "components_kept": comps, "alpha_px_gt10": int((alpha_u8>10).sum()),
            "alpha_frac": float((alpha_u8>10).mean()), "bbox": bbox}

def main():
    manifest = []
    import json as _json
    _mp = Path(__file__).parent/"conversion-manifest.json"
    if _mp.exists():
        try: manifest = _json.load(open(_mp))
        except: manifest = []
    _done = {m["source"] for m in manifest if m.get("status")=="converted"}
    files = sorted([p for p in SRC.rglob("*") if p.is_file() and p.suffix.lower() in (".jpg",".jpeg",".png")])
    for src in files:
        rel = src.relative_to(SRC)
        group = rel.parts[0] if len(rel.parts)>1 else "root"
        if str(rel) in _done:
            continue
        if group == "backgrounds":
            manifest.append({"source": str(rel), "group": group, "status": "excluded-background",
                             "reason": "Image IS a background/room, not a figure sheet; cutting its background would destroy it."})
            continue
        dst = OUT/group/(src.stem + ".png")
        if dst.exists():
            print("skip", src.name); continue
        try:
            m = convert(src, dst)
            # quality flag: very low or near-full coverage is suspicious for a figure sheet
            frac = m["alpha_frac"]
            m["quality"] = "PASS" if 0.05 <= frac <= 0.98 else ("CHECK-low" if frac < 0.05 else "CHECK-high")
            m.update({"source": str(rel), "group": group, "status": "converted", "output": str(dst.relative_to(OUT))})
            manifest.append(m)
        except Exception as e:
            manifest.append({"source": str(rel), "group": group, "status": "FAILED", "error": str(e)})
        print(src.name, manifest[-1].get("status"), manifest[-1].get("alpha_frac",""))
    json.dump(manifest, open(Path(__file__).parent/"conversion-manifest.json","w"), indent=1)
    print(f"total {len(manifest)} converted {sum(1 for m in manifest if m['status']=='converted')} excluded {sum(1 for m in manifest if m['status']=='excluded-background')} failed {sum(1 for m in manifest if m['status']=='FAILED')}")

if __name__ == "__main__":
    main()
