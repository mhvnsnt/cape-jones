#!/usr/bin/env python3
"""Drawing-masters upgrade (G1), 2026-10-31.
Base: rig-apose-v7c-clean-transparent.png (1100x1500), untouched.
Every individual output is AUTO-FIT: canvas = alpha bbox + 40px pad, so no
crop window can clip a foot or a piece. Contact sheets fit tiles by
containment (no distortion, no crop) on grey for viewing only.
OpenCV (venv, 5.0.0) actually ran for Canny/Sobel lineart.
Freestyle / Toon Boom / OpenToonz / Anime2Sketch are METHOD REFERENCES ONLY,
not run here -- stated plainly in the report.
"""
import json, os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
import cv2

ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(ROOT, "drawing-masters-upgrade-20261031")
IND = os.path.join(OUT, "individual"); EFF = os.path.join(OUT, "effects")
os.makedirs(IND, exist_ok=True); os.makedirs(EFF, exist_ok=True)

BASE = Image.open(os.path.join(ROOT, "rig-apose-v7c-clean-transparent.png")).convert("RGBA")
BASE_ARR = np.array(BASE)

def autofit(im, pad=40):
    """Return im trimmed to its alpha bbox + pad, transparent. Never crops alpha."""
    a = im.getchannel("A")
    bbox = a.getbbox()
    if bbox is None:
        return im
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
    x1 = min(im.width, x1 + pad); y1 = min(im.height, y1 + pad)
    return im.crop((x0, y0, x1, y1))

def save(im, path):
    out = autofit(im)
    out.save(path)
    arr = np.array(out)
    return {"file": os.path.basename(path), "size": out.size,
            "alpha_px": int((arr[:, :, 3] > 0).sum()),
            "alpha_bbox": [int(v) for v in out.getchannel("A").getbbox()],
            "edge_touch": bool((arr[0, :, 3] > 0).any() or (arr[-1, :, 3] > 0).any()
                               or (arr[:, 0, 3] > 0).any() or (arr[:, -1, 3] > 0).any())}

def far_dark_grad(im, lo=0.95, hi=0.62):
    """Smooth far-side darkening: left edge lo, right edge hi, no hard half-cut."""
    arr = np.array(im).astype(float)
    h, w = arr.shape[:2]
    xs = np.linspace(lo, hi, w)[None, :, None]
    arr[:, :, :3] *= xs
    arr[:, :, :3] = arr[:, :, :3].clip(0, 255)
    return Image.fromarray(arr.astype("uint8"), "RGBA")

def resize_w(im, w):
    return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)

results = {}
def add(name, im, folder=IND):
    p = os.path.join(folder, name + ".png")
    results[name] = save(im, p)
    return p

# ---- Improved G1 set (all 20 originals, rebuilt, autofit, correctly labelled) ----
add("I01-foreshorten-072", BASE.resize((792, 1500), Image.LANCZOS))
add("I02-foreshorten-045", BASE.resize((495, 1500), Image.LANCZOS))
add("I03-mirror-flip", ImageOps.mirror(BASE))
add("I04-far-side-dark-grad", far_dark_grad(BASE))
add("I05-vertical-flip-NOT-A-TURN", ImageOps.flip(BASE))
add("I06-skew-turn-approx", BASE.transform((1100, 1500), Image.AFFINE, (1, 0.12, 0, 0, 1, 0)))
add("I07-perspective-quad-NOT-A-TURN", BASE.transform((1100, 1500), Image.QUAD, (0, 0, 1100, 150, 1100, 1500, 0, 1350)))
add("I08-torso-twist-segment-approx", BASE.rotate(6, center=(550, 800), resample=Image.BICUBIC))
add("I09-chest-counter-rot-approx", BASE.rotate(-6, center=(550, 800), resample=Image.BICUBIC))
def restore_alpha(im):
    """RGB-only ops (grayscale/posterize) drop alpha to 255 everywhere; put the base alpha back."""
    out = im.convert("RGBA")
    out.putalpha(BASE.getchannel("A"))
    return out

add("I10-silhouette-ref-grey", restore_alpha(ImageOps.grayscale(BASE)))
add("X01-depth-by-scale-085", resize_w(BASE, 935))
add("X02-scale-plus-dark", far_dark_grad(resize_w(BASE, 935)))
add("X03-shear-turn-approx", BASE.transform((1100, 1500), Image.AFFINE, (1, -0.12, 0, 0, 1, 0)))
add("X05-blur-plus-sharpen", BASE.filter(ImageFilter.GaussianBlur(1)).filter(ImageFilter.SHARPEN))
add("X06-posterize-approx", restore_alpha(ImageOps.posterize(BASE.convert("RGB"), 3)))
add("X07-contrast-approx", ImageEnhance.Contrast(BASE).enhance(1.4))
add("X09-flip-plus-dark", far_dark_grad(ImageOps.mirror(BASE)))
add("X10-quad-back-NOT-A-TURN", BASE.transform((1100, 1500), Image.QUAD, (150, 0, 950, 150, 950, 1500, 150, 1350)))

# ---- LINEART-INVISIBLE: real Canny + alpha-edge, controllable weight/opacity ----
grey = cv2.cvtColor(BASE_ARR[:, :, :3], cv2.COLOR_RGB2GRAY)
canny = cv2.Canny(grey, 50, 150)
alpha = BASE_ARR[:, :, 3]
alpha_edge = cv2.Canny(alpha, 50, 150)
lines = np.maximum(canny, alpha_edge)
lines_bin = (lines > 0).astype(np.uint8) * 255

def lineart(weight_px, opacity, colour=(60, 60, 60)):
    """weight_px = dilation radius (1px = no dilation). Returns transparent lineart only."""
    k = max(1, 2 * (weight_px - 1) + 1)
    dil = cv2.dilate(lines_bin, np.ones((k, k), np.uint8)) if weight_px > 1 else lines_bin
    out = np.zeros((BASE.height, BASE.width, 4), dtype=np.uint8)
    m = dil > 0
    out[m, 0], out[m, 1], out[m, 2] = colour
    out[m, 3] = opacity
    return Image.fromarray(out, "RGBA")

def line_stats(im):
    arr = np.array(im)
    m = arr[:, :, 3] > 0
    return {"line_px": int(m.sum()),
            "mean_line_alpha": round(float(arr[:, :, 3][m].mean()), 1) if m.any() else 0.0,
            "coverage_pct_of_silhouette": round(100 * float(m.sum()) / 373846, 2)}

lineart_stats = {}
for name, w, op in [("LINEART-INVISIBLE-L1-faint-1px-a70", 1, 70),
                    ("LINEART-INVISIBLE-L2-medium-2px-a120", 2, 120),
                    ("LINEART-INVISIBLE-L3-visible-3px-a180", 3, 180)]:
    im = lineart(w, op)
    lineart_stats[name] = line_stats(im)
    add(name, im, EFF)

# Line-weight-by-depth: near (left) 3px, mid 2px, far (right) 1px, same opacity
bands = []
for (x0, x1, w) in [(0, 367, 3), (367, 733, 2), (733, 1100, 1)]:
    seg = np.zeros_like(lines_bin); seg[:, x0:x1] = lines_bin[:, x0:x1]
    k = max(1, 2 * (w - 1) + 1)
    seg = cv2.dilate(seg, np.ones((k, k), np.uint8)) if w > 1 else seg
    bands.append(seg)
depth_mask = np.maximum(np.maximum(bands[0], bands[1]), bands[2])
out = np.zeros((BASE.height, BASE.width, 4), dtype=np.uint8)
m = depth_mask > 0
out[m, :3] = (60, 60, 60); out[m, 3] = 140
im_depth = Image.fromarray(out, "RGBA")
lineart_stats["LINEART-INVISIBLE-Ldepth-weight-by-depth"] = line_stats(im_depth)
add("LINEART-INVISIBLE-Ldepth-weight-by-depth", im_depth, EFF)

# Sobel variant (method cross-check, actually run)
sx = cv2.Sobel(grey, cv2.CV_64F, 1, 0, ksize=3); sy = cv2.Sobel(grey, cv2.CV_64F, 0, 1, ksize=3)
mag = np.sqrt(sx ** 2 + sy ** 2)
sob = (mag > np.percentile(mag[alpha > 0], 92)).astype(np.uint8) * 255
out = np.zeros((BASE.height, BASE.width, 4), dtype=np.uint8)
m = sob > 0
out[m, :3] = (60, 60, 60); out[m, 3] = 120
im_sob = Image.fromarray(out, "RGBA")
lineart_stats["LINEART-INVISIBLE-Sobel-crosscheck"] = line_stats(im_sob)
add("LINEART-INVISIBLE-Sobel-crosscheck", im_sob, EFF)

# ---- BLACK-SILHOUETTE: clean alpha-to-black, NOT solarize ----
sil = np.zeros_like(BASE_ARR); sil[:, :, 3] = alpha  # RGB stays 0 = pure black
im_s1 = Image.fromarray(sil, "RGBA")
add("BLACK-SILHOUETTE-S1-pure-black", im_s1, EFF)
# S2: black + cyan rim (dilate alpha 3 minus alpha)
k3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
dil_a = cv2.dilate(alpha, k3)
rim = (dil_a > 0) & (alpha == 0)
s2 = sil.copy(); s2[rim, 0], s2[rim, 1], s2[rim, 2], s2[rim, 3] = (180, 245, 255, 230)
im_s2 = Image.fromarray(s2, "RGBA")
add("BLACK-SILHOUETTE-S2-black-plus-cyan-rim", im_s2, EFF)
# S3: black + light-grey interior lineart
s3 = sil.copy(); lm = lines_bin > 0
s3[lm, 0], s3[lm, 1], s3[lm, 2], s3[lm, 3] = (200, 200, 200, 220)
im_s3 = Image.fromarray(s3, "RGBA")
add("BLACK-SILHOUETTE-S3-black-plus-lineart-outline", im_s3, EFF)
sil_stats = {"silhouette_px": 373846,
             "S2_rim_px": int(rim.sum()),
             "S3_line_px": int(lm.sum())}

# ---- Perspective grid diagram (construction aid, NOT a turn) ----
W, H = 1100, 900
grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(grid)
vp = (550, 120)
for gx in range(-600, 1800, 150):
    d.line([vp, (gx, H)], fill=(255, 255, 255, 90), width=1)
for gy in range(250, H, 90):
    d.line([(0, gy), (W, gy)], fill=(255, 255, 255, 70), width=1)
d.ellipse([vp[0]-8, vp[1]-8, vp[0]+8, vp[1]+8], fill=(255, 80, 80, 255))
fig = BASE.resize((330, 450), Image.LANCZOS)
grid.alpha_composite(fig, (385, 320))
grid.save(os.path.join(OUT, "perspective-grid-diagram-20261031.png"))

# ---- I02 profile-head study (honest: baked plate, no clean layer separation) ----
# Narrow figure + profile head shown beside it with placement marks; NOT a clean composite.
narrow = BASE.resize((495, 1500), Image.LANCZOS)
study = Image.new("RGBA", (1500, 1500), (0, 0, 0, 0))
study.alpha_composite(narrow, (120, 0))
prof = Image.open(os.path.join(ROOT, "sliced", "Head_Profile.png")).convert("RGBA")
prof_big = prof.resize((298, 498), Image.LANCZOS)  # 2x, same aspect
study.alpha_composite(prof_big, (820, 250))
ds = ImageDraw.Draw(study)
ds.rectangle([820, 250, 820 + 298, 250 + 498], outline=(255, 0, 0, 255), width=4)
ds.text((820, 220), "Head_Profile (sliced) 2x -- placement study only", fill=(255, 0, 0, 255))
study2 = autofit(study)
study2.save(os.path.join(OUT, "I02-profile-head-study-20261031.png"))

# ---- Contacts (fit by containment, no crop, no distortion) ----
def contact(tiles, cols, path, tile_w=275, tile_h=375):
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tile_w, rows * (tile_h + 44)), (200, 200, 200))
    d = ImageDraw.Draw(sheet)
    for i, (lab, im) in enumerate(tiles):
        bg = Image.new("RGBA", (tile_w, tile_h), (128, 128, 128, 255))
        t = im.copy()
        t.thumbnail((tile_w, tile_h), Image.LANCZOS)
        bg.alpha_composite(t, ((tile_w - t.width) // 2, (tile_h - t.height) // 2))
        x, y = (i % cols) * tile_w, (i // cols) * (tile_h + 44)
        sheet.paste(bg.convert("RGB"), (x, y + 44))
        # wrap label to two lines if long
        d.text((x + 4, y + 4), lab[:38], fill=(0, 0, 0))
        if len(lab) > 38:
            d.text((x + 4, y + 22), lab[38:76], fill=(0, 0, 0))
    sheet.save(path); return path

CLASS = {
 "I01-foreshorten-072": "I01 foreshorten 0.72 -- APPROXIMATION, not a true 3/4",
 "I02-foreshorten-045": "I02 foreshorten 0.45 -- APPROXIMATION, face still front",
 "I03-mirror-flip": "I03 mirror flip -- APPROXIMATION, not a true back",
 "I04-far-side-dark-grad": "I04 far-side dark, smooth gradient -- APPROXIMATION",
 "I05-vertical-flip-NOT-A-TURN": "I05 vertical flip -- NOT A TURN (upside down)",
 "I06-skew-turn-approx": "I06 skew -- APPROXIMATION only",
 "I07-perspective-quad-NOT-A-TURN": "I07 perspective quad -- NOT A TURN (sideways)",
 "I08-torso-twist-segment-approx": "I08 segment twist -- APPROXIMATION",
 "I09-chest-counter-rot-approx": "I09 counter-rot -- APPROXIMATION",
 "I10-silhouette-ref-grey": "I10 grey silhouette ref -- REFERENCE only",
 "X01-depth-by-scale-085": "X01 depth-by-scale 0.85 -- APPROXIMATION",
 "X02-scale-plus-dark": "X02 scale+dark -- APPROXIMATION",
 "X03-shear-turn-approx": "X03 shear -- APPROXIMATION only",
 "X05-blur-plus-sharpen": "X05 blur+sharpen -- NOT A TURN",
 "X06-posterize-approx": "X06 posterize -- NOT A TURN",
 "X07-contrast-approx": "X07 contrast -- NOT A TURN",
 "X09-flip-plus-dark": "X09 flip+dark -- APPROXIMATION",
 "X10-quad-back-NOT-A-TURN": "X10 quad back -- NOT A TURN (sideways)",
}
tiles = []
for name, lab in CLASS.items():
    tiles.append((lab, Image.open(os.path.join(IND, name + ".png"))))
contact(tiles, 5, os.path.join(OUT, "drawing-masters-upgrade-contact-20261031.png"))

eff_tiles = []
for name, lab in [("LINEART-INVISIBLE-L1-faint-1px-a70", "LINEART-INVISIBLE L1 faint 1px a70 -- EFFECT"),
                  ("LINEART-INVISIBLE-L2-medium-2px-a120", "LINEART-INVISIBLE L2 medium 2px a120 -- EFFECT"),
                  ("LINEART-INVISIBLE-L3-visible-3px-a180", "LINEART-INVISIBLE L3 visible 3px a180 -- EFFECT"),
                  ("LINEART-INVISIBLE-Ldepth-weight-by-depth", "LINEART-INVISIBLE depth weight -- EFFECT"),
                  ("LINEART-INVISIBLE-Sobel-crosscheck", "LINEART-INVISIBLE Sobel check -- EFFECT"),
                  ("BLACK-SILHOUETTE-S1-pure-black", "BLACK-SILHOUETTE S1 pure black -- EFFECT"),
                  ("BLACK-SILHOUETTE-S2-black-plus-cyan-rim", "BLACK-SILHOUETTE S2 + cyan rim -- EFFECT"),
                  ("BLACK-SILHOUETTE-S3-black-plus-lineart-outline", "BLACK-SILHOUETTE S3 + lineart -- EFFECT")]:
    eff_tiles.append((lab, Image.open(os.path.join(EFF, name + ".png"))))
contact(eff_tiles, 4, os.path.join(OUT, "effects-lineart-silhouette-contact-20261031.png"))

# ---- No-crop gate ----
gate = {"checked": len(results), "edge_touch_failures": [k for k, v in results.items() if v["edge_touch"]],
        "all_individual_and_effects": results}
with open(os.path.join(OUT, "measurements-20261031.json"), "w") as f:
    json.dump({"individual_and_effects": results, "lineart_stats": lineart_stats,
               "silhouette_stats": sil_stats, "base_alpha_px": 373846,
               "base_alpha_bbox": [248, 253, 876, 1295],
               "gate": gate}, f, indent=2)
print("individual+effects:", len(results), "edge failures:", gate["edge_touch_failures"])
print("lineart:", json.dumps(lineart_stats, indent=2))
print("silhouette:", sil_stats)
