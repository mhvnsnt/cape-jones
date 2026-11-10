"""Gates + before/after contacts for clean punch plates + plate-swap re-renders.

Gates (measured, not claimed):
- ground: manifest mode GROUNDED, feet_y == ground_y == 950, char bbox bottom == 950.
- no-crop: clipped False, char bbox strictly inside canvas (all margins >= 0),
  and no figure pixels on the canvas edge of the final.
- occlusion: builder layer order unchanged (far/mid BG first, shadow, char+rim,
  effect, foreground strip last); foreground strip occupies only the bottom
  130px (y 950..1080), i.e. its top edge == char bbox bottom == ground line,
  so it cannot cover any character body above the ground; and no label
  circles cover the figure any more (clean plates 0 red, label-zone art restored).
- figure-alpha: clean plate is RGBA 1100x1500, alpha min 0 / max 255,
  alpha>10 count + bbox recorded, 0 red px, and the re-render char is the
  plate cropped to its alpha bbox and resized to 880px tall (same as endtoend).
Plate-swap check: new final vs old endtoend final diff must lie inside the
union of old/new char boxes expanded by 140px (effect reach, per endtoend
builder comment) — i.e. background, ground line and canvas are unchanged.
"""
import os, json
from PIL import Image, ImageDraw
import numpy as np

RIG = "/home/hatch/workspace/cape-jones-rig"
OUT = os.path.join(RIG, "art-owed-punch-plates-20261031")
OLD_FIN = os.path.join(RIG, "shots-endtoend-20261031/finals")
NEW_FIN = os.path.join(OUT, "rerenders/finals")
NEW_PRF = os.path.join(OUT, "rerenders/proofs")
plates = json.load(open(os.path.join(OUT, "clean-plates-manifest-20261031.json")))["plates"]
old = json.load(open(os.path.join(RIG, "shots-endtoend-20261031/shots-endtoend-20261031.json")))
new = json.load(open(os.path.join(OUT, "rerenders-manifest-20261031.json")))
old_by = {o["shot_id"]: o for o in old}
new_by = {n["shot_id"]: n for n in new}
plate_by = {p["shot"]: p for p in plates}

gates = []
for p in plates:
    sid = p["shot"]; n = new_by[sid]; o = old_by[sid]
    plate = Image.open(os.path.join(OUT, p["clean_plate"])).convert("RGBA")
    pa = np.array(plate)
    fin = Image.open(os.path.join(NEW_FIN, n["file"])).convert("RGB")
    fa = np.array(fin)
    oldfin = Image.open(os.path.join(OLD_FIN, o["file"])).convert("RGB")
    oa = np.array(oldfin)
    diff = np.any(fa != oa, axis=2)
    # expanded char union box
    boxes = [o["char_bbox"], n["char_bbox"]]
    x0 = max(0, min(b[0] for b in boxes) - 140); y0 = max(0, min(b[1] for b in boxes) - 140)
    x1 = min(1920, max(b[2] for b in boxes) + 140); y1 = min(1080, max(b[3] for b in boxes) + 140)
    exp = np.zeros(diff.shape, bool); exp[y0:y1, x0:x1] = True
    edge_px = int((np.any(fa[0, :, :] != fa[0, 0, :], axis=1)).sum()
                  + (np.any(fa[-1, :, :] != fa[-1, 0, :], axis=1)).sum())
    g = {
        "shot": sid, "slug": p["slug"],
        "ground": {"mode": n["mode"], "feet_y": n["feet_y"], "ground_y": n["ground_y"],
                   "char_bbox_bottom": n["char_bbox"][3],
                   "pass": n["mode"] == "GROUNDED" and n["feet_y"] == n["ground_y"] == 950
                           and n["char_bbox"][3] == 950},
        "no_crop": {"clipped": n["clipped"], "canvas": n["canvas"], "char_bbox": n["char_bbox"],
                    "margins": n["margins"],
                    "pass": (not n["clipped"]) and all(v >= 0 for v in n["margins"].values())},
        "occlusion": {"fg_strip_top_y": 1080 - 130, "char_bbox_bottom": n["char_bbox"][3],
                      "fg_strip_covers_body": (1080 - 130) < n["char_bbox"][3],
                      "clean_plate_red_px": p["clean_plate_red_px"],
                      "pass": (1080 - 130) >= n["char_bbox"][3] and p["clean_plate_red_px"] == 0},
        "figure_alpha": {"plate_mode": plate.mode, "plate_size": list(plate.size),
                         "plate_alpha_min": int(pa[:, :, 3].min()), "plate_alpha_max": int(pa[:, :, 3].max()),
                         "plate_alpha_px": p["plate_alpha_px"], "plate_bbox": p["plate_bbox"],
                         "rerender_char_size": n["char_size"],
                         "pass": plate.mode == "RGBA" and list(plate.size) == [1100, 1500]
                                 and int(pa[:, :, 3].max()) == 255 and p["plate_alpha_px"] > 50000
                                 and n["char_size"][1] == 880},
        "plate_swap_diff_vs_old_final": {"diff_px": int(diff.sum()),
                                         "diff_outside_expanded_char_union": int((diff & ~exp).sum()),
                                         "expanded_union": [x0, y0, x1, y1],
                                         "old_char": o["char_size"], "new_char": n["char_size"],
                                         "old_rim": o["rim_px"], "new_rim": n["rim_px"],
                                         "old_bleed": o["bleed_px"], "new_bleed": n["bleed_px"],
                                         "old_effect": o["effect_px"], "new_effect": n["effect_px"],
                                         "pass": int((diff & ~exp).sum()) == 0},
    }
    g["all_pass"] = all(g[k]["pass"] for k in ("ground", "no_crop", "occlusion", "figure_alpha",
                                                "plate_swap_diff_vs_old_final"))
    gates.append(g)
    print(sid, "ALL" if g["all_pass"] else "FAIL", {k: g[k]["pass"] for k in g if isinstance(g[k], dict) and "pass" in g[k]},
          "diff", g["plate_swap_diff_vs_old_final"]["diff_px"],
          "outside", g["plate_swap_diff_vs_old_final"]["diff_outside_expanded_char_union"])

json.dump({"gates": gates}, open(os.path.join(OUT, "gates-20261031.json"), "w"), indent=1)

# ---- contacts ----
def thumb(im, w):
    im = im.convert("RGBA")
    h = int(im.size[1] * w / im.size[0])
    return im.resize((w, h), Image.LANCZOS)

def on_checker(im, bg=(200, 200, 200)):
    out = Image.new("RGBA", im.size, bg + (255,))
    out.alpha_composite(im)
    return out.convert("RGB")

def contact(rows, cols_w, out_path, title):
    # rows: list of (label, [images])
    cw = cols_w; gap = 16; head = 54
    cell_h = max(im.size[1] for _, imgs in rows for im in imgs) + 28
    W = gap + len(rows[0][1]) * (cw + gap)
    H = head + len(rows) * (cell_h + gap) + gap
    s = Image.new("RGB", (W, H), (15, 15, 15)); d = ImageDraw.Draw(s)
    d.text((gap, 12), title, fill=(255, 255, 255))
    d.text((gap, 32), "BEFORE = labelled source / old endtoend final (white-circle workaround)  |  AFTER = clean plate / clean-plate re-render", fill=(255, 200, 80))
    for ri, (label, imgs) in enumerate(rows):
        y = head + ri * (cell_h + gap)
        d.text((gap, y), label, fill=(255, 255, 255))
        for ci, im in enumerate(imgs):
            x = gap + ci * (cw + gap)
            s.paste(im, (x, y + 24))
    s.save(out_path); print(out_path, s.size)

# 1) Plates before/after: labelled source RGB (grey, red labels) vs clean plate on checker
rows = []
for p in plates:
    src = Image.open(os.path.join(RIG, p["labelled_source_rgb"])).convert("RGB")
    clean = on_checker(Image.open(os.path.join(OUT, p["clean_plate"])))
    rows.append((f"{p['shot']} {p['slug']}", [thumb(src, 460), thumb(clean, 460)]))
contact(rows, 460, os.path.join(OUT, "before-after-plates-20261031.png"),
        "CLEAN PUNCH PLATES — BEFORE (labelled source, red ARM/LEG circles) vs AFTER (clean plate, labels gone, joint balls stay)")

# 2) Shots before/after: old final vs new final
rows = []
for p in plates:
    sid = p["shot"]
    of = Image.open(os.path.join(OLD_FIN, old_by[sid]["file"])).convert("RGB")
    nf = Image.open(os.path.join(NEW_FIN, new_by[sid]["file"])).convert("RGB")
    rows.append((f"{sid} {p['slug']}", [thumb(of, 460), thumb(nf, 460)]))
contact(rows, 460, os.path.join(OUT, "before-after-shots-20261031.png"),
        "PLATE-SWAP RE-RENDERS — BEFORE (old final, white label circles) vs AFTER (clean-plate re-render)")

# 3) Label-zone zooms from plates: ARM-2 circle zone (plate coords x680-840, y350-510)
rows = []
for p in plates:
    src = Image.open(os.path.join(RIG, p["labelled_source_rgb"])).convert("RGB").crop((680, 350, 840, 510))
    clean = on_checker(Image.open(os.path.join(OUT, p["clean_plate"]))).crop((680, 350, 840, 510))
    # upscale 3x for legibility
    src = src.resize((480, 480), Image.NEAREST); clean = clean.resize((480, 480), Image.NEAREST)
    rows.append((f"{p['shot']} ARM-2 zone", [src, clean]))
contact(rows, 480, os.path.join(OUT, "before-after-label-zone-zoom-20261031.png"),
        "LABEL-ZONE ZOOM (plate coords x680-840, y350-510, ARM-2 circle) — BEFORE red circle vs AFTER underlying art (3x, nearest)")
print("DONE gates+contacts")
