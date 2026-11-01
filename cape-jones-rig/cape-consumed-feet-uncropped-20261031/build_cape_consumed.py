#!/usr/bin/env python3
"""Cape Consumed — feet uncropped + Feet Front Facing Engulfed variant, 2026-10-31.

Mars ordered 2026-10-31 21:26 CDT, replying to future-symbiote-contact-20261031.png:
the feet in that contact read as cropped off by a square crop; make one where
the feet are NOT cropped off, and save the cropped one as Feet Front Facing
Engulfed. The all-black variant is CAPE CONSUMED.

Measured cause, stated plainly (not a canvas-edge crop):
- The version Mars saw (crystal-builder NO-cape plate) has bottom margin
  207 px — nothing touches the canvas edge. Its feet READ as cut off
  because the old crude cape erase (alpha y>=600 outside x380-720, removed
  85,752 px) left a black slab behind the legs: its feet bands are confined
  to x380-720 (y1200-1250: 4,132 px; y1250-1293: 2,471 px), no toes spreading
  outward. The feet are engulfed in black, not canvas-cropped.
- The uncropped version here uses the later true piece-removal capeless
  plate (cape pieces Cape_Back_Main + Cape_Collar omitted, no rectangle
  erase): feet bands y1200-1250: 6,983 px, x329-822; y1250-1295: 8,455 px,
  x304-831 — full feet, toes forward, front-facing reading preserved.
- No-crop rule applied to the NEW presentation: the uncropped plates are
  padded 100 px on every side (1100x1500 -> 1300x1700) so the figure plus
  any glow has margin on all four sides, and the contact tiles are full-
  aspect (never square-cropped). The engulfed variant is NOT re-padded or
  fixed: it is a byte-identical copy of the original plate, kept as-is.

FUTURE ONLY, NOT V2, NOT canon. Body (18,18,22), symbol WHITE diamond only.
White outline rule: where body crosses itself, the front part gets a white
outline (shown in the crossed pose, ring from the earlier builder).
No repo push. No existing file overwritten, no original deleted.
"""
import hashlib, json, shutil, os
from PIL import Image, ImageDraw

ROOT = "/home/hatch/workspace/cape-jones-rig"
OUT = os.path.join(ROOT, "cape-consumed-feet-uncropped-20261031")
CAPELESS = os.path.join(ROOT, "future-symbiote-capeless-white-outline-20261031",
                        "symbiote-apose-CAPELESS-20261031.png")
CROSSED = os.path.join(ROOT, "future-symbiote-capeless-white-outline-20261031",
                       "symbiote-crossed-WHITE-OUTLINE-20261031.png")
ENGULFED = os.path.join(ROOT, "crystal-cape-jones-v2-transformation-upgrade-20261031",
                        "future-symbiote-black-white-symbol-NO-cape-20261031.png")
ENGULFED_GREY = os.path.join(ROOT, "crystal-cape-jones-v2-transformation-upgrade-20261031",
                             "future-symbiote-black-white-symbol-NO-cape-20261031-on-grey.png")
PAD = 100

def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()

def measure(im):
    import numpy as np
    a = np.asarray(im.convert("RGBA"))
    m = a[:, :, 3] > 10
    ys, xs = np.where(m)
    body = int(((a[:, :, 0] == 18) & (a[:, :, 1] == 18) & (a[:, :, 2] == 22) & m).sum())
    white = int(((a[:, :, 0] == 255) & (a[:, :, 1] == 255) & (a[:, :, 2] == 255) & m).sum())
    feet = {}
    yb = int(ys.max())
    for label, (y0, y1) in [("above_feet_90-45px", (yb - 90, yb - 45)),
                            ("feet_lowest_45px", (yb - 45, yb + 1))]:
        sub = m[y0:y1, :]
        f_ys, f_xs = np.where(sub)
        feet[label] = dict(alpha_px=int(sub.sum()),
                           x_min=int(f_xs.min()) if len(f_xs) else None,
                           x_max=int(f_xs.max()) if len(f_xs) else None,
                           y_range=[int(y0), int(y1 - 1)])
    return dict(canvas=list(im.size),
                alpha_px=int(m.sum()),
                bbox=[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                margins=dict(top=int(ys.min()), bottom=int(im.size[1] - 1 - ys.max()),
                             left=int(xs.min()), right=int(im.size[0] - 1 - xs.max())),
                edge_alpha=dict(top=int((a[0, :, 3] > 10).sum()),
                                bottom=int((a[-1, :, 3] > 10).sum()),
                                left=int((a[:, 0, 3] > 10).sum()),
                                right=int((a[:, -1, 3] > 10).sum())),
                body_18_18_22_px=body, white_px=white, feet_bands=feet)

def pad(im, pad=PAD):
    out = Image.new("RGBA", (im.size[0] + 2 * pad, im.size[1] + 2 * pad), (0, 0, 0, 0))
    out.alpha_composite(im, (pad, pad))
    return out

def on_grey(im):
    bg = Image.new("RGBA", im.size, (128, 128, 128, 255))
    bg.alpha_composite(im)
    return bg.convert("RGB")

meas = {}
# 1. UNCROPPED Cape Consumed apose (padded, piece-removal capeless plate)
unc = pad(Image.open(CAPELESS).convert("RGBA"))
unc.save(os.path.join(OUT, "cape-consumed-uncropped-20261031.png"))
on_grey(unc).save(os.path.join(OUT, "cape-consumed-uncropped-20261031-on-grey.png"))
meas["cape_consumed_uncropped_apose"] = measure(unc)
meas["cape_consumed_uncropped_apose"]["source"] = "future-symbiote-capeless-white-outline-20261031/symbiote-apose-CAPELESS-20261031.png (true piece omission, no rectangle erase), padded 100 px all sides"
meas["cape_consumed_uncropped_apose"]["feet_note"] = "Full feet visible: lowest band spreads x304-831 on the source canvas (x404-931 padded); toes forward, front-facing."
# 2. UNCROPPED crossed pose with white outline (padded)
cro = pad(Image.open(CROSSED).convert("RGBA"))
cro.save(os.path.join(OUT, "cape-consumed-crossed-white-outline-uncropped-20261031.png"))
on_grey(cro).save(os.path.join(OUT, "cape-consumed-crossed-white-outline-uncropped-20261031-on-grey.png"))
meas["cape_consumed_crossed_white_outline_uncropped"] = measure(cro)
meas["cape_consumed_crossed_white_outline_uncropped"]["source"] = "future-symbiote-capeless-white-outline-20261031/symbiote-crossed-WHITE-OUTLINE-20261031.png, padded 100 px all sides; white crossing ring 3,458 px, width 4, from that builder (white_px here includes symbol diamond 1,524 px + ring + outline detail)"
# 3. FEET FRONT FACING ENGULFED — byte-identical copy, NOT fixed, NOT re-padded
eng_path = os.path.join(OUT, "feet-front-facing-engulfed-20261031.png")
shutil.copyfile(ENGULFED, eng_path)
eng_grey = os.path.join(OUT, "feet-front-facing-engulfed-20261031-on-grey.png")
shutil.copyfile(ENGULFED_GREY, eng_grey)
meas["feet_front_facing_engulfed"] = measure(Image.open(eng_path).convert("RGBA"))
meas["feet_front_facing_engulfed"]["source"] = "crystal-cape-jones-v2-transformation-upgrade-20261031/future-symbiote-black-white-symbol-NO-cape-20261031.png, BYTE-IDENTICAL copy, md5 " + md5(eng_path) + " (original md5 " + md5(ENGULFED) + "), kept as-is, feet engulfed in the black slab, not fixed over"
meas["feet_front_facing_engulfed"]["feet_note"] = "Feet engulfed: lowest bands confined to x380-720 on the source canvas, no outward toes — this is the read Mars flagged as cropped off. Canvas bottom margin is 207 px, so it is engulfment, not a canvas-edge crop."

# 4. Contact: full-aspect tiles, NEVER square-cropped, plus a labelled feet detail row
def tile(im_rgba, tw):
    g = on_grey(im_rgba)
    h = int(g.size[1] * tw / g.size[0])
    return g.resize((tw, h))

TW = 360
tiles = [tile(unc, TW), tile(cro, TW), tile(Image.open(eng_path).convert("RGBA"), TW)]
labels = ["1  UNCROPPED", "2  CROSSED + WHITE OUTLINE", "3  ENGULFED (as-is)"]
th = max(t.size[1] for t in tiles)
# feet detail row: 2x crops of the feet zone, scaled to fit one tile width each
# (no overlap), labelled as detail magnifiers, not replacements
def feet_detail(im_rgba, box):
    crop = on_grey(im_rgba).crop(box)
    h = int(crop.size[1] * TW / crop.size[0])
    return crop.resize((TW, h))
# uncropped padded feet zone: source feet y1250-1295 -> padded y1350-1395, x304-831 -> x404-931
d_unc = feet_detail(unc, (350, 1300, 980, 1450))
d_eng = feet_detail(Image.open(eng_path).convert("RGBA"), (300, 1150, 800, 1350))
dh = max(d_unc.size[1], d_eng.size[1])
sheet = Image.new("RGB", (3 * TW, th + 30 + dh + 60), (200, 200, 200))
dd = ImageDraw.Draw(sheet)
for i, t in enumerate(tiles):
    sheet.paste(t, (i * TW, 30))
    dd.text((i * TW + 6, 8), labels[i], fill=(0, 0, 0))
sheet.paste(d_unc, (0, th + 60))
sheet.paste(d_eng, (TW, th + 60))
dd.text((6, th + 38), "FEET DETAIL (magnifier, not a crop of the figure): left = UNCROPPED full feet, right = ENGULFED narrow slab", fill=(0, 0, 0))
sheet.save(os.path.join(OUT, "cape-consumed-contact-20261031.png"))
meas["contact"] = dict(file="cape-consumed-contact-20261031.png",
                       tiles="full-aspect, width 360 px each, never square-cropped; tile heights follow each plate's own aspect",
                       note="Detail row is a labelled magnifier of the feet zone only; the full figures above it are uncropped.")

json.dump(meas, open(os.path.join(OUT, "measurements-20261031.json"), "w"), indent=2)
print(json.dumps(meas, indent=2))
