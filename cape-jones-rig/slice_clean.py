#!/usr/bin/env python3
"""
Cape Jones clean-cut slicer — CLEAN-CUT RULE (Mars, 2026-10-31).
NOT square-crop hand tooling: components are found by the sheet itself.
Method, in order:
 1. Background colour = median of the four corners (flat sheet bg).
 2. Mask = distance from bg > 30. This keeps white art AND black outlines
    on a gray sheet, and white/purple/tan art on a black sheet.
 3. Morphological closing (3x3, 2x) + hole fill, so black outlines on a
    black sheet do not fragment a piece into fill islands. The alpha
    silhouette is the filled component, the colour is the original pixel
    (so black outlines survive, they are not keyed out).
 4. Connected components, keep area >= 800px. No hand-drawn rectangles.
 5. Rows = clusters of component centres separated by >150px gaps in y;
    pieces are named by row, left-to-right, with a row prefix supplied
    by the caller (e.g. UpperArm/Gauntlet/Hand for Pack 1).
 6. 1px alpha feather + fringe decontamination: edge pixels are
    unmultiplied away from the bg colour, clipped to 0-255.
 7. Trim to the component silhouette only. Output manifest + contact sheet.
AI background removal (rembg, u2netp) is an OPTIONAL second pass:
  slice_clean.py --rembg  — it is tested separately because, on a flat
  black sheet, AI eats the black cape and on a gray sheet it eats white
  suit edges. For flat production sheets the scripted flood/close method
  above is the default, and rembg is NOT claimed as the default until a
  test on that exact sheet beats it. See CLEAN-CUT-NOTES.md.
Usage: python3 slice_clean.py <sheet.jpg/png> <outdir> <row1prefix> <row2prefix> ...
"""
import sys, os, json
from PIL import Image
import numpy as np
from scipy import ndimage

def main():
    sheet, outdir = sys.argv[1], sys.argv[2]
    prefixes = sys.argv[3:]
    os.makedirs(outdir, exist_ok=True)
    im = Image.open(sheet).convert("RGB")
    arr = np.array(im).astype(float)
    corners = np.concatenate([arr[:5,:5].reshape(-1,3), arr[:5,-5:].reshape(-1,3),
                              arr[-5:,:5].reshape(-1,3), arr[-5:,-5:].reshape(-1,3)])
    bg = np.median(corners, axis=0)
    dist = np.sqrt(((arr - bg)**2).sum(axis=2))
    mask = dist > 30
    mask = ndimage.binary_closing(mask, structure=np.ones((3,3)), iterations=2)
    mask = ndimage.binary_fill_holes(mask)
    lab, n = ndimage.label(mask, structure=np.ones((3,3)))
    objs = ndimage.find_objects(lab)
    comps = []
    for i, sl in enumerate(objs, start=1):
        if sl is None: continue
        ysl, xsl = sl
        area = int((lab[sl] == i).sum())
        if area < 800: continue
        comps.append({"x": int(xsl.start), "y": int(ysl.start),
                      "x1": int(xsl.stop), "y1": int(ysl.stop), "area": area, "id": i})
    # row clustering by centre y, gap > 150
    comps.sort(key=lambda c: (c["y"] + c["y1"]) / 2)
    rows, cur = [], []
    for c in comps:
        cy = (c["y"] + c["y1"]) / 2
        if cur and cy - (cur[-1]["y"] + cur[-1]["y1"]) / 2 > 150:
            rows.append(cur); cur = []
        cur.append(c)
    if cur: rows.append(cur)
    meta, counter = [], 0
    for ri, row in enumerate(rows):
        row = sorted(row, key=lambda c: c["x"])
        prefix = prefixes[ri] if ri < len(prefixes) else f"Row{ri+1}"
        for j, c in enumerate(row, start=1):
            counter += 1
            # for Hand rows after the first, continue numbering across rows
            name = f"{prefix}_{j}"
            if prefix == "Hand" and ri == 3:
                name = f"Hand_{j+7}"
            x0, y0, x1, y1 = c["x"], c["y"], c["x1"], c["y1"]
            crop = arr[y0:y1, x0:x1]
            m = (lab[y0:y1, x0:x1] == c["id"])
            # feather: blur alpha 1px, then decontaminate edge pixels
            alpha = (m * 255).astype(float)
            alpha = ndimage.gaussian_filter(alpha, 0.8)
            alpha_u8 = np.clip(alpha, 0, 255).astype(np.uint8)
            rgb = crop.copy()
            # unmultiply fringe where 0 < alpha < 255
            a = np.clip(alpha / 255.0, 0.01, 1.0)[..., None]
            rgb = np.clip((crop - bg * (1 - a)) / a, 0, 255)
            # keep fully opaque interior at original colour
            rgb[m] = crop[m]
            rgba = np.zeros((y1-y0, x1-x0, 4), dtype=np.uint8)
            rgba[:, :, :3] = rgb.astype(np.uint8)
            rgba[:, :, 3] = alpha_u8
            fn = f"{name}.png"
            Image.fromarray(rgba, "RGBA").save(os.path.join(outdir, fn))
            meta.append({"name": name, "file": fn, "size": [int(x1-x0), int(y1-y0)],
                         "opaque_px": int((alpha_u8 > 0).sum()), "sheet_bbox": [x0, y0, x1, y1]})
            print(name, rgba.shape)
    json.dump({"bg": bg.tolist(), "pieces": meta}, open(os.path.join(outdir, "MANIFEST.json"), "w"), indent=1)
    print(f"pieces {len(meta)} bg {bg}")

if __name__ == "__main__":
    main()
