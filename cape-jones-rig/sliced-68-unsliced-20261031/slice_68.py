#!/usr/bin/env python3
"""Slice the 68 unsliced figure sheets into labelled pieces.

Mars ordered 2026-10-31 23:26 CDT. Count correction (do not repeat the
confusion): 245 sheets = 208 figure sheets + 37 backgrounds.
Already sliced: 140 sheets. NOT sliced: 68 figure sheets + 37 backgrounds
(backgrounds are rooms, NOT sliced). This job = exactly those 68.

Method (standing clean-cut rule, slice_clean.py logic, adapted to the
already background-cut transparent plates from the Grok full sweep):
- Input = the transparent plate (alpha already cut, interior = original
  colour, never recoloured). No original sheet is touched.
- Components = connected components of alpha > 10, area >= 800 px,
  8-connectivity. No hand-drawn rectangles.
- Pieces = component cropped to its own bbox, pixels copied exactly
  from the plate (RGBA unchanged, no recolour, no decontamination
  re-run, no feather re-run — the plate already carries those).
- Naming = existing sliced-clean convention: rows clustered by
  component centre-y with a >150 px gap, left-to-right in each row,
  Row{r}_{n}.png, plus a MANIFEST.json per sheet.
- Provisional class: ONLY where the sheet type makes it clear, never
  guessed as a body part:
    storyboards      -> storyboard_panel (6 equal panels)
    layout-line-art  -> layout_panel (4 equal panels)
    color-keys       -> colour_variant_figure (large figure comps)
    viseme-charts    -> viseme_head_cell (grid heads, NOT a phoneme)
    props            -> prop_main_object (only the dominant object)
    variations tpose-front (single comp) -> full_figure_tpose
    variations tpose-front-alt largest    -> full_figure_tpose
    everything else  -> MIXED/UNCLASSIFIED (human eye needed)
  Fla-pack pieces are therefore MIXED/UNCLASSIFIED: a pack component
  may be a torso, a limb, a hand, a cape, or a full pose, and position
  alone does not tell which. Labelling a 390x734 torso as a "full
  figure" would be a guessed label, and is NOT done here.
- Exception, documented: color-key-sheet-5. Its 5 figures touch at
  the fingertips and form ONE alpha component (845,913 px). Component
  slicing alone would give 1 merged strip, not 5 individual figures.
  That strip is split at the 4 vertical midpoints between the 5
  figure centres (x = 360, 720, 1080, 1440 on the 1792-wide sheet),
  giving 5 colour_variant_figure pieces. This is a grid split of a
  merged row, NOT a hand-drawn body-part rectangle, and it is flagged
  here and in the manifest, not hidden.
- Duplicates: 22 of the 68 source entries are byte-identical repo
  duplicates (11 jojo-packs vs jojo-packs-2, 11 lounge-packs vs
  lounge-3quarter clean). Each duplicate source gets its OWN sheet
  folder (suffix __dup2) with its own pieces, so the count is 68/68
  sheets, not 46 unique contents. The manifest flags duplicate_of.
- NOT sliced here: the 37 backgrounds, the already-sliced 140 sheets,
  and 09-hero-shot-black is NOT hand-fixed here (separate question).
"""
import json, os, re, hashlib
from collections import Counter
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

HOME = Path.home()
RIG = HOME / "workspace/cape-jones-rig"
GROK = RIG / "transparent-plates-grok-full-sweep-20261031"
OUT = RIG / "sliced-68-unsliced-20261031"

def stem_of(src):
    return re.sub(r"\.[^.]+$", "", os.path.basename(src))

def plate_md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()

def provisional(sheet_group, sheet_stem, comp, sheet_alpha, n_comps, is_largest):
    area, w, h = comp["area"], comp["w"], comp["h"]
    if sheet_group == "storyboards":
        return "storyboard_panel"
    if sheet_group == "layout-line-art":
        return "layout_panel"
    if sheet_group == "color-keys":
        return "colour_variant_figure" if area >= 100000 else "MIXED/UNCLASSIFIED"
    if sheet_group == "viseme-charts":
        return "viseme_head_cell" if area >= 20000 else "MIXED/UNCLASSIFIED"
    if sheet_group == "props":
        if sheet_stem == "prop-xyug7":
            return "MIXED/UNCLASSIFIED"  # full-frame pattern, not an object
        if is_largest and area >= 0.5 * sheet_alpha:
            return "prop_main_object"
        return "MIXED/UNCLASSIFIED"
    if sheet_group == "variations":
        if sheet_stem == "cape-jones-tpose-front" and n_comps == 1:
            return "full_figure_tpose"
        if sheet_stem == "cape-jones-tpose-front-alt" and is_largest:
            return "full_figure_tpose"
        return "MIXED/UNCLASSIFIED"
    return "MIXED/UNCLASSIFIED"

def main():
    man = json.load(open(GROK / "conversion-manifest.json"))
    sliced = set()
    for mf in (RIG / "sliced-clean-20261031").rglob("MANIFEST.json"):
        sliced.add(mf.parent.name)
    unsliced = [x for x in man if x["status"] == "converted" and stem_of(x["source"]) not in sliced]
    assert len(unsliced) == 68, f"expected 68 unsliced, got {len(unsliced)}"
    plates_dir = GROK / "plates"
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "sheets").mkdir(exist_ok=True)

    seen_folders = {}
    sheet_records = []
    total_pieces = 0
    named = 0
    mixed = 0
    for entry in unsliced:
        src, group = entry["source"], entry["group"]
        stem = stem_of(src)
        plate_path = plates_dir / entry["output"]
        plate_md5v = plate_md5(plate_path)
        # duplicate handling: same stem seen before -> __dup2 folder
        if stem in seen_folders:
            folder_name = stem + "__dup2"
            dup_of = seen_folders[stem]
        else:
            folder_name = stem
            dup_of = None
            seen_folders[stem] = src
        outdir = OUT / "sheets" / group / folder_name
        outdir.mkdir(parents=True, exist_ok=True)

        im = Image.open(plate_path).convert("RGBA")
        arr = np.array(im)
        alpha = arr[:, :, 3] > 10
        sheet_alpha = int(alpha.sum())
        lab, _ = ndimage.label(alpha, structure=np.ones((3, 3)))
        objs = ndimage.find_objects(lab)
        comps = []
        for i, sl in enumerate(objs, start=1):
            if sl is None:
                continue
            area = int((lab[sl] == i).sum())
            if area < 800:
                continue
            ysl, xsl = sl
            comps.append({"id": i, "x": int(xsl.start), "y": int(ysl.start),
                          "x1": int(xsl.stop), "y1": int(ysl.stop), "area": area,
                          "w": int(xsl.stop - xsl.start), "h": int(ysl.stop - ysl.start)})

        # Grid-split exception: color-key-sheet-5 merged strip
        grid_split = False
        if stem == "color-key-sheet-5" and len(comps) == 1 or (stem == "color-key-sheet-5" and any(c["area"] > 800000 for c in comps)):
            # split the single huge component at figure-centre midpoints
            big = max(comps, key=lambda c: c["area"])
            cuts = [360, 720, 1080, 1440]
            new_comps = []
            bounds = [big["x"]] + cuts + [big["x1"]]
            for k in range(5):
                x0, x1 = bounds[k], bounds[k + 1]
                submask = (lab[big["y"]:big["y1"], x0:x1] == big["id"])
                # Keep ONLY the largest connected component in this slab:
                # a neighbour figure's fingertip/cape tip crossing the cut
                # would otherwise survive as a stray sliver in this piece.
                slab_lab, _ = ndimage.label(submask, structure=np.ones((3, 3)))
                slab_objs = ndimage.find_objects(slab_lab)
                best, best_area = None, 0
                for si, ssl in enumerate(slab_objs, start=1):
                    if ssl is None:
                        continue
                    a = int((slab_lab[ssl] == si).sum())
                    if a > best_area:
                        best, best_area = si, a
                if best is None or best_area < 800:
                    continue
                ys, xs = np.where(slab_lab == best)
                new_comps.append({"id": big["id"], "slab_component": best,
                                  "x": int(x0 + xs.min()), "y": int(big["y"] + ys.min()),
                                  "x1": int(x0 + xs.max() + 1), "y1": int(big["y"] + ys.max() + 1),
                                  "area": int(best_area), "w": int(xs.max() - xs.min() + 1), "h": int(ys.max() - ys.min() + 1),
                                  "grid_split": True, "slab_x0": x0, "slab_x1": x1,
                                  "slab_y0": int(big["y"]), "slab_y1": int(big["y1"])})
            comps = [c for c in comps if c is not big] + new_comps
            grid_split = True

        # row clustering, as in slice_clean.py: centre-y gap > 150
        comps.sort(key=lambda c: (c["y"] + c["y1"]) / 2)
        rows, cur = [], []
        for c in comps:
            cy = (c["y"] + c["y1"]) / 2
            if cur and cy - (cur[-1]["y"] + cur[-1]["y1"]) / 2 > 150:
                rows.append(cur); cur = []
            cur.append(c)
        if cur:
            rows.append(cur)

        largest_area = max((c["area"] for c in comps), default=0)
        pieces = []
        for ri, row in enumerate(rows):
            row = sorted(row, key=lambda c: c["x"])
            for j, c in enumerate(row, start=1):
                name = f"Row{ri+1}_{j}"
                fn = f"{name}.png"
                x0, y0, x1, y1 = c["x"], c["y"], c["x1"], c["y1"]
                if c.get("grid_split"):
                    # mask is the big component restricted to this x-slab,
                    # largest component in that slab only (no neighbour slivers)
                    slab = (lab[c["slab_y0"]:c["slab_y1"], c["slab_x0"]:c["slab_x1"]] == c["id"])
                    slab_lab, _ = ndimage.label(slab, structure=np.ones((3, 3)))
                    keep = (slab_lab == c["slab_component"])
                    crop = np.zeros((y1 - y0, x1 - x0, 4), dtype=np.uint8)
                    # piece bbox is inside the slab; map it back
                    sy0, sx0 = y0 - c["slab_y0"], x0 - c["slab_x0"]
                    sub = keep[sy0:sy0 + (y1 - y0), sx0:sx0 + (x1 - x0)]
                    crop[sub] = arr[y0:y1, x0:x1][sub]
                    Image.fromarray(crop, "RGBA").save(outdir / fn)
                else:
                    m = (lab[y0:y1, x0:x1] == c["id"])
                    crop = arr[y0:y1, x0:x1].copy()
                    crop[~m] = [0, 0, 0, 0]
                    Image.fromarray(crop, "RGBA").save(outdir / fn)
                cls = provisional(group, stem, c, sheet_alpha, len(comps), c["area"] == largest_area)
                if grid_split and c.get("grid_split"):
                    cls = "colour_variant_figure"
                pieces.append({"name": name, "file": fn, "size": [c["w"], c["h"]],
                               "opaque_px": int((arr[y0:y1, x0:x1, 3][m] > 0).sum()) if not c.get("grid_split") else c["area"],
                               "sheet_bbox": [x0, y0, x1, y1], "area_px": c["area"],
                               "provisional_class": cls,
                               "grid_split": bool(c.get("grid_split", False))})
        json.dump({"source": src, "group": group, "plate": str(entry["output"]),
                   "plate_md5": plate_md5v, "duplicate_of": dup_of,
                   "grid_split": grid_split, "pieces": pieces},
                  open(outdir / "MANIFEST.json", "w"), indent=1)
        n_named = sum(1 for p in pieces if p["provisional_class"] != "MIXED/UNCLASSIFIED")
        sheet_records.append({"source": src, "group": group, "folder": str(outdir.relative_to(OUT)),
                              "plate_md5": plate_md5v, "duplicate_of": dup_of, "grid_split": grid_split,
                              "pieces": len(pieces), "named": n_named, "mixed": len(pieces) - n_named})
        total_pieces += len(pieces); named += n_named; mixed += len(pieces) - n_named
        print(f"{src}: {len(pieces)} pieces, named {n_named}, mixed {len(pieces)-n_named}")

    summary = {"sheets_sliced": len(sheet_records), "total_new_pieces": total_pieces,
               "named": named, "mixed": mixed,
               "by_group": Counter(r["group"] for r in sheet_records),
               "sheets": sheet_records}
    json.dump(summary, open(OUT / "SLICING-MANIFEST-20261031.json", "w"), indent=1, default=str)
    print(f"TOTAL sheets {len(sheet_records)} pieces {total_pieces} named {named} mixed {mixed}")

if __name__ == "__main__":
    main()
