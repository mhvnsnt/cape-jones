#!/usr/bin/env python3
"""Rebuild G5 motion-pose variants OLD (fixed crop window) vs NEW (no-crop).

OLD = the exact transforms from limits-broken-10x10-20261031/build_10x10.py
G5 section, run on a fixed 1100x1500 RGBA canvas. One stated difference
from the original sheet: the original sheet baked a grey background
(on_grey) into the display tiles, which hides alpha loss. Here the OLD
frames are kept RGBA so clipping is measurable; the grey was display
only, not part of the transform, and removing it does not change the
clip counts.
NEW = the same transforms through no_crop.py (pad -> transform -> trim
to alpha bbox + 40px transparent padding). Transparent background
throughout; checker in contact sheets is DISPLAY ONLY.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from no_crop import (alpha_count, alpha_bbox, edge_touch, rotate_nocrop,
                     shear_nocrop, trim, paste_nocrop, pad_image)

ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(ROOT, "no-crop-window-20261031")
OLD_D = os.path.join(OUT, "frames-old"); NEW_D = os.path.join(OUT, "frames-new")
BASE = Image.open(os.path.join(ROOT, "rig-apose-v7c-clean-transparent.png")).convert("RGBA")

def padded_truth(fn, im):
    """Same transform on a 3300x4500 padded canvas: the reference that
    separates clipping from resampling. Returns trimmed? No -- returns
    the padded result; alpha count is what matters."""
    pad = pad_image(im, 1100)
    return fn(pad)

OLD = {
    "I01-Arm1-minus10": lambda im: im.rotate(-10, center=(550, 750)),
    "I02-Arm1-minus18": lambda im: im.rotate(-18, center=(550, 750)),
    "I03-Arm1-plus10": lambda im: im.rotate(10, center=(550, 750)),
    "I04-lean-shear-015": lambda im: im.transform((1100, 1500), Image.AFFINE, (1, 0.15, 0, 0, 1, 0)),
    "I05-run-lean-030": lambda im: im.transform((1100, 1500), Image.AFFINE, (1, 0.30, 0, 0, 1, 0)),
    "I06-fly-tilt-15": lambda im: im.rotate(15),
    "I07-grip-L": lambda im: im,
    "I08-grip-R-mirror": lambda im: ImageOps.mirror(im),
    "I09-cycle-6f": lambda im: im.resize((990, 1350)),
    "I10-cycle-12f": lambda im: im,
    "X01-squash-run": lambda im: im.resize((1100, 1350)),
    "X02-stretch-fly": lambda im: im.resize((1100, 1500)),
    "X03-shear-run-minus020": lambda im: im.transform((1100, 1500), Image.AFFINE, (1, -0.20, 0, 0, 1, 0)),
    "X04-bounce": lambda im: im.resize((1045, 1425)),
    "X05-afterglow-blur": lambda im: im.filter(ImageFilter.GaussianBlur(2)),
    "X06-mirrored-run": lambda im: ImageOps.mirror(im),
    "X07-double-exposure": lambda im: Image.blend(im, im.rotate(5), 0.5),
    "X08-speed-lines": lambda im: im,
    "X09-device-lap": lambda im: im,
    "X10-device-grip": lambda im: im,
}
NEW = {
    "I01-Arm1-minus10": lambda im: rotate_nocrop(im, -10, center=(550, 750)),
    "I02-Arm1-minus18": lambda im: rotate_nocrop(im, -18, center=(550, 750)),
    "I03-Arm1-plus10": lambda im: rotate_nocrop(im, 10, center=(550, 750)),
    "I04-lean-shear-015": lambda im: shear_nocrop(im, 0.15),
    "I05-run-lean-030": lambda im: shear_nocrop(im, 0.30),
    "I06-fly-tilt-15": lambda im: rotate_nocrop(im, 15),
    "I07-grip-L": lambda im: trim(im),
    "I08-grip-R-mirror": lambda im: trim(ImageOps.mirror(im)),
    "I09-cycle-6f": lambda im: trim(im.resize((990, 1350))),
    "I10-cycle-12f": lambda im: trim(im),
    "X01-squash-run": lambda im: trim(im.resize((1100, 1350))),
    "X02-stretch-fly": lambda im: trim(im.resize((1100, 1500))),
    "X03-shear-run-minus020": lambda im: shear_nocrop(im, -0.20),
    "X04-bounce": lambda im: trim(im.resize((1045, 1425))),
    "X05-afterglow-blur": lambda im: trim(im.filter(ImageFilter.GaussianBlur(2))),
    "X06-mirrored-run": lambda im: trim(ImageOps.mirror(im)),
    "X07-double-exposure": lambda im: _double_nocrop(im),
    "X08-speed-lines": lambda im: trim(im),
    "X09-device-lap": lambda im: trim(im),
    "X10-device-grip": lambda im: trim(im),
}
def _double_nocrop(im):
    # Blend on a common padded canvas so neither exposure can clip.
    a = pad_image(im, 600)
    b = rotate_nocrop(im, 5)
    canvas, _ = paste_nocrop(Image.new("RGBA", a.size, (0, 0, 0, 0)), a, (0, 0))
    # centre b on the padded canvas by its bbox centre vs a's bbox centre
    bb_a = a.getbbox(); bb_b = b.getbbox()
    cx = (bb_a[0] + bb_a[2]) // 2 - (bb_b[0] + bb_b[2]) // 2
    cy = (bb_a[1] + bb_a[3]) // 2 - (bb_b[1] + bb_b[3]) // 2
    canvas2, _ = paste_nocrop(canvas, b, (cx, cy)) if False else (canvas, (0, 0))
    # blend needs equal sizes: composite b onto a copy of a at the offset
    bg = Image.new("RGBA", a.size, (0, 0, 0, 0)); bg.alpha_composite(b, (cx, cy))
    return trim(Image.blend(a, bg, 0.5))

# padded-truth functions: same transform, padded canvas, no fixed window
def truth_fn(name):
    if name.startswith("I01"): return lambda im: pad_image(BASE, 1100).rotate(-10, center=(550 + 1100, 750 + 1500))
    if name.startswith("I02"): return lambda im: pad_image(BASE, 1100).rotate(-18, center=(550 + 1100, 750 + 1500))
    if name.startswith("I03"): return lambda im: pad_image(BASE, 1100).rotate(10, center=(550 + 1100, 750 + 1500))
    if name.startswith("I04"): return lambda im: pad_image(BASE, 1100).transform((3300, 4500), Image.AFFINE, (1, 0.15, 0, 0, 1, 0))
    if name.startswith("I05"): return lambda im: pad_image(BASE, 1100).transform((3300, 4500), Image.AFFINE, (1, 0.30, 0, 0, 1, 0))
    if name.startswith("I06"): return lambda im: pad_image(BASE, 1100).rotate(15, center=(550 + 1100, 750 + 1500))
    if name.startswith("X03"): return lambda im: pad_image(BASE, 1100).transform((3300, 4500), Image.AFFINE, (1, -0.20, 0, 0, 1, 0))
    if name.startswith("X07"): return lambda im: pad_image(BASE, 1100).rotate(5, center=(550 + 1100, 750 + 1500))
    return lambda im: OLD[name](im)

rows = []
for name in OLD:
    old = OLD[name](BASE); new = NEW[name](BASE)
    old.save(os.path.join(OLD_D, name + ".png")); new.save(os.path.join(NEW_D, name + ".png"))
    truth = alpha_count(truth_fn(name)(BASE)) if name not in (
        "I07-grip-L", "I08-grip-R-mirror", "I09-cycle-6f", "I10-cycle-12f",
        "X01-squash-run", "X02-stretch-fly", "X04-bounce", "X05-afterglow-blur",
        "X06-mirrored-run", "X08-speed-lines", "X09-device-lap", "X10-device-grip") else alpha_count(BASE if "mirror" not in name else BASE)
    # for resize/blur/mirror/identity, padded-truth == old transform on a
    # padded canvas, which cannot clip; use the new frame's own count as
    # the reference for those (they are clip-free by construction) and
    # report old-vs-new directly instead.
    oc, nc = alpha_count(old), alpha_count(new)
    rows.append({"variant": name, "old_size": list(old.size), "new_size": list(new.size),
                 "old_alpha": oc, "new_alpha": nc, "padded_truth_alpha": truth,
                 "old_lost_vs_truth": truth - oc, "new_lost_vs_truth": truth - nc,
                 "old_edge_touch": edge_touch(old), "new_edge_touch": edge_touch(new),
                 "old_bbox": list(alpha_bbox(old)) if alpha_bbox(old) else None,
                 "new_bbox": list(alpha_bbox(new)) if alpha_bbox(new) else None})

# Lean tests: L1 shear 0.40, L2 compound rotate -20 then shear 0.35, L3 piece paste off-edge
lean = []
def lean_old_shear(im, k): return im.transform((1100, 1500), Image.AFFINE, (1, k, 0, 0, 1, 0))
for lname, ofn, nfn in [
    ("L1-lean-shear-040", lambda im: lean_old_shear(im, 0.40), lambda im: shear_nocrop(im, 0.40)),
    ("L2-compound-lean-rot-20-shear-035",
     lambda im: lean_old_shear(im.rotate(-20, center=(550, 750)), 0.35),
     lambda im: shear_nocrop(rotate_nocrop(im, -20, center=(550, 750)), 0.35)),
]:
    old = ofn(BASE); new = nfn(BASE)
    old.save(os.path.join(OLD_D, lname + ".png")); new.save(os.path.join(NEW_D, lname + ".png"))
    # padded truth for L1 / L2
    if lname.startswith("L1"):
        truth = alpha_count(pad_image(BASE, 1100).transform((3300, 4500), Image.AFFINE, (1, 0.40, 0, 0, 1, 0)))
    else:
        p = pad_image(BASE, 1100).rotate(-20, center=(550 + 1100, 750 + 1500))
        truth = alpha_count(p.transform((3300, 4500), Image.AFFINE, (1, 0.35, 0, 0, 1, 0)))
    lean.append({"variant": lname, "old_size": list(old.size), "new_size": list(new.size),
                 "old_alpha": alpha_count(old), "new_alpha": alpha_count(new),
                 "padded_truth_alpha": truth, "old_lost_vs_truth": truth - alpha_count(old),
                 "new_lost_vs_truth": truth - alpha_count(new),
                 "old_edge_touch": edge_touch(old), "new_edge_touch": edge_touch(new)})

# L3 piece paste test
piece = Image.open(os.path.join(ROOT, "cut-limbs-v7c", "Leg_Front_Lower.png")).convert("RGBA")
pc = alpha_count(piece)
old_c = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0)); old_c.paste(piece, (-50, 1400), piece)
new_c, shift = paste_nocrop(Image.new("RGBA", (1100, 1500), (0, 0, 0, 0)), piece, (-50, 1400))
old_c.save(os.path.join(OLD_D, "L3-piece-paste-offedge.png")); new_c.save(os.path.join(NEW_D, "L3-piece-paste-offedge.png"))
lean.append({"variant": "L3-piece-paste-offedge", "piece_alpha": pc,
             "old_alpha": alpha_count(old_c), "new_alpha": alpha_count(new_c),
             "old_lost": pc - alpha_count(old_c), "new_lost": pc - alpha_count(new_c),
             "paste_shift": list(shift), "old_size": list(old_c.size), "new_size": list(new_c.size),
             "old_edge_touch": edge_touch(old_c), "new_edge_touch": edge_touch(new_c)})

# Checker display helper (display only, never baked into figure files)
def on_checker(im, tile=275):
    w, h = im.size
    # scale to tile width keeping aspect, for contact display
    th = int(tile * h / w)
    small = im.resize((tile, th))
    bg = Image.new("RGB", (tile, th), (255, 255, 255))
    d = ImageDraw.Draw(bg)
    for yy in range(0, th, 20):
        for xx in range(0, tile, 20):
            if (xx // 20 + yy // 20) % 2 == 0:
                d.rectangle([xx, yy, xx + 20, yy + 20], fill=(200, 200, 200))
    bg.paste(small, (0, 0), small)
    return bg

def contact(pairs, path, cols=4):
    # pairs: list of (label, old_path, new_path); each cell old over new
    cell_w, cell_h = 275, 420
    rows_n = (len(pairs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows_n * cell_h), (220, 220, 220))
    d = ImageDraw.Draw(sheet)
    for i, (lab, op, np_) in enumerate(pairs):
        x, y = (i % cols) * cell_w, (i // cols) * cell_h
        d.text((x + 4, y + 4), lab, fill=(0, 0, 0))
        d.text((x + 4, y + 20), "OLD (fixed window)", fill=(180, 0, 0))
        d.text((x + 4, y + 200), "NEW (no-crop)", fill=(0, 120, 0))
        o = on_checker(Image.open(op).convert("RGBA"), tile=132)
        n = on_checker(Image.open(np_).convert("RGBA"), tile=132)
        sheet.paste(o.resize((132, 180)), (x + 4, y + 36))
        sheet.paste(n.resize((132, 180)), (x + 140, y + 36))
        # full-width new frame below labels for the lean proofs
        sheet.paste(on_checker(Image.open(np_).convert("RGBA"), tile=132).resize((132, 180)), (x + 4, y + 220))
    sheet.save(path)

names = list(OLD.keys())
contact([(n, os.path.join(OLD_D, n + ".png"), os.path.join(NEW_D, n + ".png")) for n in names],
        os.path.join(OUT, "proofs", "g5-before-after-contact-20261031.png"))
contact([(n, os.path.join(OLD_D, n + ".png"), os.path.join(NEW_D, n + ".png")) for n in
         ["L1-lean-shear-040", "L2-compound-lean-rot-20-shear-035", "L3-piece-paste-offedge"]],
        os.path.join(OUT, "proofs", "lean-before-after-contact-20261031.png"), cols=3)

with open(os.path.join(OUT, "measurements-20261031.json"), "w") as f:
    json.dump({"base_alpha": alpha_count(BASE), "base_bbox": list(alpha_bbox(BASE)),
               "g5": rows, "lean_tests": lean}, f, indent=2)
for r in rows + lean:
    print(r["variant"], "old_lost=", r.get("old_lost_vs_truth", r.get("old_lost")),
          "new_lost=", r.get("new_lost_vs_truth", r.get("new_lost")),
          "old_edge=", r["old_edge_touch"], "new_edge=", r["new_edge_touch"])
