#!/usr/bin/env python3
"""SCALE HANDS DOWN 25%, Mars 2026-11-01 01:56 CDT.
Start point: rig-34-hands-replace-20261101 (hands at 1.45x).
Final hands: 1.45 * 0.75 = 1.0875x, same centres/rotations/mirror.
Rebuilt from the attachment-fix base (NOT layered on top of the 1.45 hands),
so there is exactly ONE hand per arm, no double hand layer.
No crop, no erase, no square crop, no split."""
from PIL import Image, ImageDraw
import os, json, hashlib
import numpy as np
ROOT = os.path.expanduser("~/workspace/cape-jones-rig/rig-34-hands-scale-down25-20261101")
BASE = os.path.expanduser("~/workspace/cape-jones-rig/rig-34-attachment-fix-20261101")
PREV = os.path.expanduser("~/workspace/cape-jones-rig/rig-34-hands-replace-20261101")
SRC = os.path.expanduser("~/workspace/cape-jones-rig/sitting-rig-34-20261101/pieces")
W, H, S = 1400, 1600, 1.45 * 0.75  # 1.0875
base = Image.open(f"{BASE}/poses/sit-chair-attachment-fix-20261101.png").convert("RGBA")
canvas = base.copy()
fists = {"L": (479, 791), "R": (909, 827)}
spare = Image.open(os.path.join(SRC, "hand_spare_L.png")).convert("RGBA")
spare = spare.resize((int(spare.width * S), int(spare.height * S)), Image.LANCZOS)
mirrored = spare.transpose(Image.FLIP_LEFT_RIGHT)
spare.save(f"{ROOT}/pieces/hand_arm1_scaled.png"); mirrored.save(f"{ROOT}/pieces/hand_arm2_mirrored_scaled.png")
def place(hand, centre, angle):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(hand, (int(centre[0] - hand.width / 2), int(centre[1] - hand.height / 2)))
    layer = layer.rotate(angle, center=centre, expand=False, resample=Image.BICUBIC)
    canvas.alpha_composite(layer)
    a = np.array(layer)[:, :, 3]; ys, xs = np.where(a > 10)
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
b1 = place(spare, fists["L"], 6); b2 = place(mirrored, fists["R"], 0)
canvas.save(f"{ROOT}/poses/sit-chair-hands-scaledown25-20261101.png")
grey = Image.new("RGBA", canvas.size, (126, 126, 126, 255)); grey.alpha_composite(canvas)
grey.convert("RGB").save(f"{ROOT}/poses/sit-chair-hands-scaledown25-20261101-on-grey.png")
full = grey.convert("RGB")
def zoom(box, out, label):
    c = full.crop(box); c = c.resize((c.width * 2, c.height * 2), Image.NEAREST)
    sheet = Image.new("RGB", (c.width, c.height + 30), (30, 30, 30))
    ImageDraw.Draw(sheet).text((10, 8), label, fill="white"); sheet.paste(c, (0, 30)); sheet.save(out)
zoom((380, 690, 580, 990), f"{ROOT}/contacts/hand1-new-zoom-20261101.png", "Arm1 LEFT hand scale 1.0875 centred on fist (479,791)")
zoom((810, 730, 1010, 1030), f"{ROOT}/contacts/hand2-new-zoom-20261101.png", "Arm2 RIGHT hand MIRRORED scale 1.0875 centred on fist (909,827)")
c1 = full.crop((380, 690, 580, 990)); c2 = full.crop((810, 730, 1010, 1030))
sheet = Image.new("RGB", (c1.width + c2.width + 20, max(c1.height, c2.height) + 30), (30, 30, 30)); d = ImageDraw.Draw(sheet)
d.text((10, 8), "Arm1 LEFT open hand 1.0875x", fill="white"); d.text((c1.width + 20, 8), "Arm2 RIGHT open hand MIRRORED 1.0875x", fill="white")
sheet.paste(c1, (0, 30)); sheet.paste(c2, (c1.width + 20, 30)); sheet.save(f"{ROOT}/contacts/both-hands-new-20261101.png")
old = Image.open(f"{PREV}/poses/sit-chair-hands-replace-20261101-on-grey.png").convert("RGB")
o = old.copy(); n = full.copy(); o.thumbnail((700, 800)); n.thumbnail((700, 800))
contact = Image.new("RGB", (2 * 710, 840), (30, 30, 30)); d = ImageDraw.Draw(contact)
d.text((10, 10), "OLD hands 1.45x", fill="white"); d.text((720, 10), "NEW hands 1.0875x (down 25%)", fill="white")
contact.paste(o, (5, 40)); contact.paste(n, (715, 40)); contact.save(f"{ROOT}/contacts/old-vs-new-hands-scaledown25-20261101.png")
a = np.array(canvas)[:, :, 3]; ys, xs = np.where(a > 10)
# Fist-sliver estimate: pixels in fist neighbourhood present in base but NOT covered by hand layer.
# Approximate fist neighbourhood: circle radius 55 around each fist centre, in base alpha.
# Count base-alpha pixels in that circle that remain alpha in new figure but lie OUTSIDE the hand bbox.
def sliver(centre, bbox):
    cx, cy = centre; cnt = 0; tot = 0
    ba = np.array(base)[:, :, 3]; na = a
    for y in range(cy-60, cy+61):
        for x in range(cx-60, cx+61):
            if (x-cx)**2 + (y-cy)**2 > 55**2: continue
            if ba[y, x] > 10:
                tot += 1
                if not (bbox[0] <= x <= bbox[2] and bbox[1] <= y <= bbox[3]):
                    cnt += 1
    return {"fist_neighbourhood_alpha_px": int(tot), "outside_hand_bbox_px": int(cnt)}
gates = {"base": "rig-34-attachment-fix-20261101 (rebuilt, not layered over 1.45x hands, to keep 1 hand per arm)",
 "prev": "rig-34-hands-replace-20261101", "prev_md5": hashlib.md5(open(f"{PREV}/poses/sit-chair-hands-replace-20261101.png",'rb').read()).hexdigest(),
 "old_scale": 1.45, "new_scale": S, "scale_factor": 0.75,
 "fist_centres": {"L": list(fists["L"]), "R": list(fists["R"])},
 "arm1_left": {"source": "hand_spare_L.png, as-is", "scale": S, "angle_pil_rotate": 6, "hand_bbox": b1},
 "arm2_right": {"source": "hand_spare_L.png MIRRORED left-right, thumb opposite Arm 1", "scale": S, "angle_pil_rotate": 0, "hand_bbox": b2},
 "hand_native_size": "81x117 -> 1.45x 117x170 -> 1.0875x 88x127",
 "hands_total": 2, "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
 "feet_alpha_bottom": {"L": 1475, "R": 1475},
 "fist_sliver_estimate": {"arm1": sliver(fists["L"], b1), "arm2": sliver(fists["R"], b2),
   "note": "Estimate only: base-alpha pixels within r=55 of fist centre lying outside the scaled hand bbox. At 1.45x this was ~10px peek at zoom; smaller hand covers less, so peek is larger — see zooms, not faked away."}}
json.dump(gates, open(f"{ROOT}/gates-20261101.json", "w"), indent=2)
print(json.dumps(gates, indent=2))
