#!/usr/bin/env python3
"""10 industry-standard methods for Grok sweep honest defects + gaps.
RUN with numpy/scipy/PIL only (no cv2 on this VM, so GrabCut/MediaPipe are
MAPPING, not counted). No original touched; all outputs in this folder.
Fringe definition (measured, not eyeballed): a kept pixel (alpha>10) within
3px of a transparent pixel, whose colour is saturated: max-min channel >60
AND (blue dominant B>R+40 OR red dominant R>B+40, R>80).
"""
import json, hashlib, os
from collections import Counter
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

BASE = os.path.expanduser("~/workspace/cape-jones-rig")
SWEEP = os.path.join(BASE, "transparent-plates-grok-full-sweep-20261031")
OUT = os.path.join(BASE, "honest-defects-10-methods-20261031")
os.makedirs(os.path.join(OUT, "variants"), exist_ok=True)
os.makedirs(os.path.join(OUT, "contacts"), exist_ok=True)

def load_rgba(p):
    return np.array(Image.open(p).convert("RGBA")).astype(np.float64)

def fringe(arr):
    a = arr[:, :, 3]
    kept = a > 10
    # edge band: kept pixels within 3px of transparent
    transp = ~kept
    dist = ndimage.distance_transform_edt(~transp)  # distance to transparent? EDT of kept gives dist to background
    # Actually distance_transform_edt(kept) = distance to nearest 0 (transparent)
    edge = kept & (dist <= 3.5)
    rgb = arr[:, :, :3]
    mx = rgb.max(axis=2); mn = rgb.min(axis=2)
    sat = (mx - mn) > 60
    blue = (rgb[:, :, 2] - rgb[:, :, 0]) > 40
    red = (rgb[:, :, 0] - rgb[:, :, 2]) > 40
    fringe_edge = int((edge & sat & (blue | red)).sum())
    fringe_all = int((kept & sat & (blue | red)).sum())
    return fringe_edge, fringe_all, int(kept.sum())

def save(arr, name):
    out = np.clip(arr, 0, 255).astype(np.uint8)
    Image.fromarray(out, "RGBA").save(os.path.join(OUT, "variants", name))
    return fringe(arr)

hero_plate = os.path.join(SWEEP, "plates/root/09-hero-shot-black.png")
hero = load_rgba(hero_plate)
results = {}
results["hero_baseline"] = dict(zip(["fringe_edge", "fringe_all", "alpha_gt10"], fringe(hero)))
print("baseline", results["hero_baseline"])

# M1 colour decontamination / spill suppression (Premiere/Photoshop decontaminate):
# premultiplied blur: RGB*alpha blurred / alpha blurred, applied only in edge band
def decontaminate(arr, sigma=2.0):
    a = arr[:, :, 3:4] / 255.0
    prem = arr[:, :, :3] * a
    im_prem = Image.fromarray(np.clip(prem, 0, 255).astype(np.uint8))
    im_a = Image.fromarray(np.clip(a[:, :, 0] * 255, 0, 255).astype(np.uint8))
    blur_prem = np.array(im_prem.filter(ImageFilter.GaussianBlur(sigma))).astype(np.float64)
    blur_a = np.array(im_a.filter(ImageFilter.GaussianBlur(sigma))).astype(np.float64) / 255.0
    blur_a = np.maximum(blur_a, 1e-6)
    decon = blur_prem / blur_a[:, :, None]
    kept = arr[:, :, 3] > 10
    dist = ndimage.distance_transform_edt(kept)
    edge = kept & (dist <= 3.5)
    out = arr.copy()
    out[edge, :3] = decon[edge, :3]
    return out

m1 = decontaminate(hero)
results["M1_decontaminate"] = dict(zip(["fringe_edge", "fringe_all", "alpha_gt10"], save(m1, "hero-M1-decontaminate.png")))
print("M1", results["M1_decontaminate"])

# M2 alpha erosion 1px (matte choke / edge trim)
def erode(arr):
    mask = arr[:, :, 3] > 10
    er = ndimage.binary_erosion(mask, iterations=1)
    out = arr.copy(); out[~er, 3] = 0
    return out
m2 = erode(hero)
results["M2_erode1"] = dict(zip(["fringe_edge", "fringe_all", "alpha_gt10"], save(m2, "hero-M2-erode1.png")))
print("M2", results["M2_erode1"])

# M3 alpha feather / Gaussian alpha smoothing + re-threshold
def feather(arr, sigma=1.5):
    a = Image.fromarray(arr[:, :, 3].astype(np.uint8)).filter(ImageFilter.GaussianBlur(sigma))
    an = np.array(a)
    out = arr.copy(); out[:, :, 3] = np.where(an >= 128, 255, 0).astype(np.float64)
    # keep partial? use thresholded alpha as new alpha for softness: use an where >=10 else 0
    out[:, :, 3] = np.where(an >= 10, an, 0)
    return out
m3 = feather(hero)
results["M3_feather"] = dict(zip(["fringe_edge", "fringe_all", "alpha_gt10"], save(m3, "hero-M3-feather.png")))
print("M3", results["M3_feather"])

# M4 morphological closing + hole fill (matte repair)
def closing_fill(arr):
    mask = arr[:, :, 3] > 10
    cl = ndimage.binary_closing(mask, iterations=2)
    fl = ndimage.binary_fill_holes(cl)
    out = arr.copy(); out[:, :, 3] = np.where(fl, arr[:, :, 3], 0)
    return out
m4 = closing_fill(hero)
results["M4_closing_fill"] = dict(zip(["fringe_edge", "fringe_all", "alpha_gt10"], save(m4, "hero-M4-closing-fill.png")))
print("M4", results["M4_closing_fill"])

# M5 combined: decontaminate + erode 1px (strongest trial, still no hand paint)
m5 = erode(decontaminate(hero))
results["M5_decon_erode"] = dict(zip(["fringe_edge", "fringe_all", "alpha_gt10"], save(m5, "hero-M5-decon-erode.png")))
print("M5", results["M5_decon_erode"])

# M6 full-frame classifier, all 208 converted plates
manifest = json.load(open(os.path.join(SWEEP, "conversion-manifest.json")))
converted = [e for e in manifest if e["status"] == "converted"]
cls = []
for e in converted:
    p = os.path.join(SWEEP, "plates", e["output"])
    if not os.path.exists(p): continue
    im = Image.open(p).convert("RGBA"); a = np.array(im)[:, :, 3]
    kept = a > 10; frac = float(kept.mean())
    bbox = e["bbox"]; w, h = e["size"]
    touches = sum([bbox[0] <= 2, bbox[1] <= 2, bbox[2] >= w - 3, bbox[3] >= h - 3])
    if frac >= 0.98 and touches >= 3:
        label = "FULL-FRAME-TEXTURE (not a cut object)"
    elif frac >= 0.90:
        label = "NEAR-FULL-FRAME (check)"
    else:
        label = "FIGURE-CUT"
    cls.append({"source": e["source"], "output": e["output"], "alpha_frac": round(frac, 4),
                "bbox_touch_edges": touches, "label": label, "quality_old": e.get("quality")})
results["M6_classifier"] = {"n": len(cls), "FULL-FRAME-TEXTURE": sum(1 for c in cls if c["label"].startswith("FULL")),
                            "NEAR-FULL": sum(1 for c in cls if c["label"].startswith("NEAR")),
                            "FIGURE-CUT": sum(1 for c in cls if c["label"] == "FIGURE-CUT"),
                            "props_4": [c for c in cls if any(k in c["source"] for k in ["8LjQY", "oCpSw", "rY6iH", "xyug7"])]}
print("M6", results["M6_classifier"])

# M7 duplicate hash audit
hashes = {}
for e in converted:
    p = os.path.join(SWEEP, "plates", e["output"])
    if not os.path.exists(p): continue
    h = hashlib.md5(open(p, "rb").read()).hexdigest()
    hashes.setdefault(h, []).append(e["source"])
dups = {h: v for h, v in hashes.items() if len(v) > 1}
results["M7_duplicates"] = {"unique_hashes": len(hashes), "plates_checked": len(converted),
                            "duplicate_groups": len(dups), "duplicate_sources": sum(len(v) for v in dups.values()),
                            "groups": list(dups.values())}
print("M7", len(hashes), len(dups))

# M8 component inventory for whole-sheet plates (provisional, NOT semantic)
comp_inv = []
for e in converted:
    p = os.path.join(SWEEP, "plates", e["output"])
    if not os.path.exists(p): continue
    a = np.array(Image.open(p).convert("RGBA"))[:, :, 3] > 10
    lab, n = ndimage.label(a)
    sizes = ndimage.sum(np.ones_like(a), lab, range(1, n + 1)) if n else []
    big = [int(s) for s in sizes if s >= 800]
    comp_inv.append({"source": e["source"], "components_ge800": len(big), "largest_px": max(big) if big else 0,
                     "total_components": int(n)})
results["M8_components"] = {"plates": len(comp_inv), "total_big_components": sum(c["components_ge800"] for c in comp_inv),
                            "plates_with_0_big": sum(1 for c in comp_inv if c["components_ge800"] == 0)}
print("M8", results["M8_components"])

# M9 MIXED triage queue
idx = json.load(open(os.path.join(BASE, "fight-and-sheets-20261031/piece-label-index-20261031.json")))
mixed = [e for e in idx if e.get("provisional") == "MIXED/UNCLASSIFIED"]
mixed_sorted = sorted(mixed, key=lambda e: e["opaque_px"], reverse=True)
triage = []
for e in mixed_sorted[:40]:
    pcts = {"WHITE": e["white_pct"], "DARK": e["dark_pct"], "PURPLE": e["purple_pct"], "SKIN": e["skin_pct"], "GREEN": e["green_pct"]}
    sug = max(pcts, key=pcts.get)
    triage.append({"file": e["file"], "size": e["size"], "opaque_px": e["opaque_px"],
                   "colour_pcts": pcts, "suggestion_only": sug, "human_confirms": True})
results["M9_triage"] = {"mixed_total": len(mixed), "index_total": len(idx),
                        "named": len(idx) - len(mixed), "triage_top40": triage}
print("M9", len(mixed))

# M10 re-QC gate all 208
qc = []
for e in converted:
    p = os.path.join(SWEEP, "plates", e["output"])
    if not os.path.exists(p): continue
    arr = load_rgba(p); fe, fa, al = fringe(arr)
    frac = al / (arr.shape[0] * arr.shape[1])
    # holes: transparent pixels inside bbox that are enclosed? approximate: bbox area - alpha
    bbox = e["bbox"]; bbox_area = (bbox[2]-bbox[0]) * (bbox[3]-bbox[1])
    hole_frac = 1 - al / max(bbox_area, 1)
    verdict = "PASS" if fe < 5000 and frac < 0.98 else ("CHECK" if fe < 20000 else "FLAG")
    qc.append({"source": e["source"], "fringe_edge": fe, "alpha_frac": round(float(frac), 4),
               "hole_frac_in_bbox": round(float(hole_frac), 4), "verdict": verdict})
results["M10_qc"] = {"n": len(qc), "PASS": sum(1 for q in qc if q["verdict"] == "PASS"),
                     "CHECK": sum(1 for q in qc if q["verdict"] == "CHECK"),
                     "FLAG": sum(1 for q in qc if q["verdict"] == "FLAG"),
                     "hero_qc": [q for q in qc if "hero-shot-black" in q["source"]]}
print("M10", results["M10_qc"])

json.dump({"methods": results, "M6_all": cls, "M8_all": comp_inv, "M10_all": qc},
          open(os.path.join(OUT, "measurements-10-methods-20261031.json"), "w"), indent=1)

# Contacts
def checker_bg(w, h):
    bg = Image.new("RGB", (w, h), (200, 200, 200))
    d = ImageDraw.Draw(bg)
    s = 20
    for y in range(0, h, s):
        for x in range(0, w, s):
            if ((x // s) + (y // s)) % 2 == 0:
                d.rectangle([x, y, x + s - 1, y + s - 1], fill=(160, 160, 160))
    return bg

def tile(path, tw=460):
    im = Image.open(path).convert("RGBA")
    im.thumbnail((tw, 900))
    bg = checker_bg(tw, im.height)
    bg.paste(im, (0, 0), im)
    return bg

# Hero contact: baseline, M1, M2, M5 + zoom crop of baseline vs M5
files = [("BASELINE", hero_plate),
         ("M1 decontaminate", os.path.join(OUT, "variants/hero-M1-decontaminate.png")),
         ("M2 erode1", os.path.join(OUT, "variants/hero-M2-erode1.png")),
         ("M5 decon+erode", os.path.join(OUT, "variants/hero-M5-decon-erode.png"))]
tiles = []
for label, p in files:
    t = tile(p, 460)
    d = ImageDraw.Draw(t); d.rectangle([0, 0, 460, 28], fill=(0, 0, 0)); d.text((8, 6), label, fill=(255, 255, 0))
    tiles.append(t)
H = max(t.height for t in tiles) + 30
contact = Image.new("RGB", (460 * 4, H), (0, 0, 0))
for i, t in enumerate(tiles):
    contact.paste(t, (i * 460, 0))
contact.save(os.path.join(OUT, "contacts/hero-before-after-contact-20261031.png"))

# Props contact
props = ["props/prop-8LjQY.png", "props/prop-oCpSw.png", "props/prop-rY6iH.png", "props/prop-xyug7.png"]
ptiles = []
for pp in props:
    p = os.path.join(SWEEP, "plates", pp)
    t = tile(p, 460)
    d = ImageDraw.Draw(t); d.rectangle([0, 0, 460, 28], fill=(0, 0, 0)); d.text((8, 6), pp.split("/")[-1] + " FULL-FRAME", fill=(255, 255, 0))
    ptiles.append(t)
H = max(t.height for t in ptiles) + 30
contact2 = Image.new("RGB", (460 * 4, H), (0, 0, 0))
for i, t in enumerate(ptiles):
    contact2.paste(t, (i * 460, 0))
contact2.save(os.path.join(OUT, "contacts/props-fullframe-contact-20261031.png"))
print("contacts done")
