#!/usr/bin/env python3
"""REPLACE FISTS WITH SEPARATE HANDS, MIRRORED FOR ARM 2, Mars 2026-11-01 01:51 CDT.
Base: rig-34-attachment-fix-20261101 sit-chair-attachment-fix (exact figure, untouched).
Final version: hands centred on measured fist centres, scale 1.45.
- Fist centres from front-lower piece geometry, NOT the old computed wrist
  (which was ~60px left of the actual fist): Arm1 (479,791), Arm2 (909,827).
- Arm1 (LEFT): hand_spare_L as-is, PIL rotate +6 (native axis -10.7deg left
  -> forearm axis -4.6deg left).
- Arm2 (RIGHT): hand_spare_L MIRRORED left-right, thumb opposite Arm 1,
  PIL rotate 0 (mirrored axis +10.7deg right -> forearm axis +10.9deg right).
- No crop, no erase, no square crop, no split. Hand layer covers the fist
  layer underneath; a gauntlet-only front forearm file does not exist, so
  the fist is NOT erased. At full-figure scale no fist is visible; at zoom
  a ~10px fist sliver still peeks at one edge per hand (see REPORT) — that
  is the remaining defect, not hidden, and it is NOT fixed by scaling the
  hand further (that would distort hand size) or by cropping/erasing.
"""
from PIL import Image, ImageDraw
import os, json, hashlib
import numpy as np
ROOT = os.path.expanduser("~/workspace/cape-jones-rig/rig-34-hands-replace-20261101")
BASE = os.path.expanduser("~/workspace/cape-jones-rig/rig-34-attachment-fix-20261101")
SRC = os.path.expanduser("~/workspace/cape-jones-rig/sitting-rig-34-20261101/pieces")
W, H, S = 1400, 1600, 1.45
base = Image.open(f"{BASE}/poses/sit-chair-attachment-fix-20261101.png").convert("RGBA")
canvas = base.copy()
fists = {"L": (479, 791), "R": (909, 827)}
spare = Image.open(os.path.join(SRC, "hand_spare_L.png")).convert("RGBA")
spare = spare.resize((int(spare.width * S), int(spare.height * S)), Image.LANCZOS)
mirrored = spare.transpose(Image.FLIP_LEFT_RIGHT)
spare.save(f"{ROOT}/pieces/hand_arm1.png"); mirrored.save(f"{ROOT}/pieces/hand_arm2_mirrored.png")
def place(hand, centre, angle):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(hand, (int(centre[0] - hand.width / 2), int(centre[1] - hand.height / 2)))
    layer = layer.rotate(angle, center=centre, expand=False, resample=Image.BICUBIC)
    canvas.alpha_composite(layer)
    a = np.array(layer)[:, :, 3]; ys, xs = np.where(a > 10)
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
b1 = place(spare, fists["L"], 6); b2 = place(mirrored, fists["R"], 0)
canvas.save(f"{ROOT}/poses/sit-chair-hands-replace-20261101.png")
grey = Image.new("RGBA", canvas.size, (126, 126, 126, 255)); grey.alpha_composite(canvas)
grey.convert("RGB").save(f"{ROOT}/poses/sit-chair-hands-replace-20261101-on-grey.png")
full = grey.convert("RGB")
def zoom(box, out, label):
    c = full.crop(box); c = c.resize((c.width * 2, c.height * 2), Image.NEAREST)
    sheet = Image.new("RGB", (c.width, c.height + 30), (30, 30, 30))
    ImageDraw.Draw(sheet).text((10, 8), label, fill="white"); sheet.paste(c, (0, 30)); sheet.save(out)
zoom((380, 690, 580, 990), f"{ROOT}/contacts/hand1-new-zoom-20261101.png", "Arm1 LEFT hand scale 1.45 centred on fist (479,791)")
zoom((810, 730, 1010, 1030), f"{ROOT}/contacts/hand2-new-zoom-20261101.png", "Arm2 RIGHT hand MIRRORED scale 1.45 centred on fist (909,827)")
c1 = full.crop((380, 690, 580, 990)); c2 = full.crop((810, 730, 1010, 1030))
sheet = Image.new("RGB", (c1.width + c2.width + 20, max(c1.height, c2.height) + 30), (30, 30, 30)); d = ImageDraw.Draw(sheet)
d.text((10, 8), "Arm1 LEFT open hand", fill="white"); d.text((c1.width + 20, 8), "Arm2 RIGHT open hand MIRRORED", fill="white")
sheet.paste(c1, (0, 30)); sheet.paste(c2, (c1.width + 20, 30)); sheet.save(f"{ROOT}/contacts/both-hands-new-20261101.png")
old = Image.open(f"{BASE}/poses/sit-chair-attachment-fix-20261101-on-grey.png").convert("RGB")
o = old.copy(); n = full.copy(); o.thumbnail((700, 800)); n.thumbnail((700, 800))
contact = Image.new("RGB", (2 * 710, 840), (30, 30, 30)); d = ImageDraw.Draw(contact)
d.text((10, 10), "OLD attachment fix (FISTS)", fill="white"); d.text((720, 10), "NEW hands replace (separate open hands, Arm2 mirrored)", fill="white")
contact.paste(o, (5, 40)); contact.paste(n, (715, 40)); contact.save(f"{ROOT}/contacts/old-vs-new-hands-replace-20261101.png")
a = np.array(canvas)[:, :, 3]; ys, xs = np.where(a > 10)
def col_runs(x, lo, hi):
    col = a[:, x]; runs = []; inr = False; s = 0
    for y, v in enumerate(col):
        if v > 10 and not inr: s = y; inr = True
        if v <= 10 and inr: runs.append((s, y - 1)); inr = False
    return [r for r in runs if r[1] >= lo and r[0] <= hi]
gates = {"base": "rig-34-attachment-fix-20261101/sit-chair-attachment-fix-20261101.png",
 "base_md5": hashlib.md5(open(f"{BASE}/poses/sit-chair-attachment-fix-20261101.png", 'rb').read()).hexdigest(),
 "fist_centres_measured_from_piece_geometry": {"L": list(fists["L"]), "R": list(fists["R"])},
 "old_computed_wrist_REJECTED": {"L": [412.3, 773.7], "R": [856.3, 829.7], "note": "computed wrist formula was ~60px left of actual fist centre; NOT used here"},
 "arm1_left": {"source": "hand_spare_L.png, as-is", "scale": S, "angle_pil_rotate": 6, "centred_on_fist": list(fists["L"]), "hand_bbox": b1},
 "arm2_right": {"source": "hand_spare_L.png MIRRORED left-right, thumb opposite Arm 1", "scale": S, "angle_pil_rotate": 0, "centred_on_fist": list(fists["R"]), "hand_bbox": b2},
 "hands_total": 2, "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
 "feet_alpha_bottom": {"L": 1475, "R": 1475},
 "knee_shin_gap_still_present": "NOT silently fixed; re-measured same columns as attachment fix",
 "knee_shin_centre_columns": {"x590_runs_1000_1250": col_runs(590, 1000, 1250), "x775_runs_1000_1250": col_runs(775, 1000, 1250)},
 "attachment_joins_kept": "Arm1 behind torso, raised shoulder (580,385); Arm2 perfect; pelvis-torso clean; hips-pelvis clean; kneecaps as rotation pivots; shins on knees; cape on shoulders back",
 "method_note": "No crop, no erase, no square crop, no split. Hand centred on fist centre, larger than fist, so fist is covered by hand layer. A gauntlet-only front forearm file does not exist.",
 "remaining_defect": "At zoom, a ~10px fist sliver still peeks at one edge per hand (Arm1 lower-right edge, Arm2 lower-left edge), where the open hand's finger shape is narrower than the round fist. At full-figure scale it reads as one open hand per arm. A truly clean version needs a gauntlet-only forearm piece; NOT faked by cropping/erasing or by scaling the hand further."}
json.dump(gates, open(f"{ROOT}/gates-20261101.json", "w"), indent=2)
print(json.dumps(gates, indent=2))
