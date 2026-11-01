#!/usr/bin/env python3
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mouth_pipeline import *
from PIL import Image, ImageDraw
import numpy as np

ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(ROOT, "mouth-packs-clean-pipeline-20261031")
BASE = Image.open(os.path.join(ROOT, "visemes-v2-20261031/clean-head-base-20261031.png")).convert("RGBA")
CX, CY = 231.5, 504.5
stats = {}

# --- 1. Clean-line MBP: fitted ONLY to original tight fragments ---
tight = Image.open(os.path.join(ROOT, "pahgo-mouth-fix-20261031/mouths-tight/mbp-front-09_tight_patch.png")).convert("RGBA")
mask = dark_mask(np.array(tight))
mbp_vec, mbp_svg, mbp_stats = vector_line_patch(mask, (178, 23), 5, "MBP-clean-line", smoothing=5)
mbp_vec.save(os.path.join(OUT, "packs/mbp-clean-line-patch.png"))
open(os.path.join(OUT, "packs/mbp-clean-line.svg"), "w").write(mbp_svg)
stats["MBP_clean_line"] = mbp_stats
stats["MBP_clean_line"]["gate"] = gate_thin_line(mbp_vec, "MBP-clean-line")
# Approved version for comparison (do NOT edit source folder; copy for contact only)
approved = Image.open(os.path.join(ROOT, "mouth-jaw-cleanup-5-methods-20261031/clean-mbp-patch.png")).convert("RGBA")
approved.save(os.path.join(OUT, "packs/mbp-approved-copy-for-contact-only.png"))
stats["MBP_approved"] = {"gate": gate_thin_line(approved, "MBP-approved"), "note": "Straight 6px bridge, gap 88-137, flat y14.0, step vs wavy fragments at 3x."}

# --- 2. Pipeline proof 2: EE smile vector-fit ---
ee_src = Image.open(os.path.join(ROOT, "pahgo-mouth-cleanup-v2-20261031/mouths-v2/ee-v2_clean_patch.png")).convert("RGBA")
ee_mask = dark_mask(np.array(ee_src))
ee_vec, ee_svg, ee_stats = vector_line_patch(ee_mask, (200, 113), 3, "EE-clean-line", smoothing=3)
ee_vec.save(os.path.join(OUT, "packs/ee-clean-line-patch.png"))
open(os.path.join(OUT, "packs/ee-clean-line.svg"), "w").write(ee_svg)
stats["EE_clean_line"] = ee_stats
stats["EE_clean_line"]["gate"] = gate_thin_line(ee_vec, "EE-clean-line")

# --- 3. Packs through pipeline (thick mouths: alpha>=128, no new shapes) ---
# Reuse v2 clean patches as pipeline inputs, verify gates, place at target.
# FRONT-4 pack: mbp-v2 (thin, vector version is the MBP-clean-line at PAH GO size;
# for pack consistency also provide v2-size vector? Keep pack patches at their
# v2 fitted sizes, with MBP represented by the clean-line method at 211x25.)
# Simpler honest pack structure:
#  Pack LINECLEAN-PAHGO: MBP vector 178x23 + approved AH 196x67 + approved GK 188x30
#  Pack FRONT-4: AH-v2, GK-v2, EE vector 200x113, MBP-v2 clean (pixel, thin-line rule)
#  Pack THREEQUARTER-3: AH34, MBP34, SMILE34 — all labelled 3/4-source, never front
packs = {}
def load_patch(p):
    im = Image.open(p).convert("RGBA")
    a = np.array(im); a[:, :, 3] = np.where(a[:, :, 3] >= 128, 255, 0)
    return Image.fromarray(a)
approved_ah = load_patch(os.path.join(ROOT, "mouth-jaw-cleanup-5-methods-20261031/clean-ah-patch.png"))
approved_gk = load_patch(os.path.join(ROOT, "mouth-jaw-cleanup-5-methods-20261031/clean-gk-patch.png"))
v2 = {k: load_patch(os.path.join(ROOT, "pahgo-mouth-cleanup-v2-20261031/mouths-v2", f))
      for k, f in [("ah-v2", "ah-v2_clean_patch.png"), ("gk-v2", "gk-v2_clean_patch.png"),
                   ("mbp-v2", "mbp-v2_clean_patch.png"), ("ah34", "ah34-v2_clean_patch.png"),
                   ("mbp34", "mbp34-v2_clean_patch.png"), ("smile34", "smile34-v2_clean_patch.png")]}
for k, im in v2.items():
    im.save(os.path.join(OUT, f"packs/{k}-pipeline-patch.png"))
    a = np.array(im); stats[k] = {"size": list(im.size), "alpha_px": int((a[:, :, 3] > 0).sum())}
packs["LINECLEAN-PAHGO"] = {"MBP": mbp_vec, "AH": approved_ah, "GK": approved_gk}
packs["FRONT-4"] = {"MBP-v2": v2["mbp-v2"], "AH-v2": v2["ah-v2"], "GK-v2": v2["gk-v2"], "EE-vector": ee_vec}
packs["THREEQUARTER-3"] = {"AH34": v2["ah34"], "MBP34": v2["mbp34"], "SMILE34": v2["smile34"]}

# --- 4. Rebuild PAH GO movement with clean-line MBP (same timeline/jaw as approved) ---
# Copy approved frames logic: use BASE + jaw shift + mouth at target, timeline from approved builder.
PARAMS = {"MBP": (178, 23, 0), "AH": (196, 67, 16), "GK": (188, 30, 8), "GAP": (0, 0, 10), "REST": (178, 23, 0)}
mouths = {"MBP": mbp_vec, "AH": approved_ah, "GK": approved_gk}
JAW_SPLIT = 560; W, H = BASE.size
def smoothstep(t): return t*t*(3-2*t)
def render(viseme, w, h, jaw):
    fr = BASE.copy(); jaw = int(round(jaw))
    if jaw > 0:
        chin = fr.crop((0, JAW_SPLIT, W, H)); row = BASE.getchannel("A").crop((0, JAW_SPLIT-1, W, JAW_SPLIT))
        hinge = BASE.crop((0, JAW_SPLIT-1, W, JAW_SPLIT)); band = Image.new("RGBA", (W, jaw))
        for yy in range(jaw): band.paste(hinge, (0, yy))
        mask = Image.new("L", (W, jaw), 0)
        for yy in range(jaw): mask.paste(row, (0, yy))
        fr.paste(band, (0, JAW_SPLIT), mask); fr.paste(chin, (0, JAW_SPLIT + jaw))
    if viseme == "GAP": return fr
    if viseme == "REST": viseme = "MBP"
    patch = mouths[viseme].resize((int(round(w)), int(round(h))), Image.LANCZOS)
    # alpha threshold after resize to kill fringe
    a = np.array(patch); a[:, :, 3] = np.where(a[:, :, 3] >= 128, 255, 0); patch = Image.fromarray(a)
    fr.alpha_composite(patch, (int(round(CX - w/2)), int(round(CY - h/2 + jaw*0.25))))
    return fr
keys = ["MBP", "AH", "GK", "GAP", "REST"]; tl = []; prev = PARAMS[keys[0]]
for i, k in enumerate(keys):
    cur = PARAMS[k]
    for f in range(6):
        if i == 0 or f >= 3: tl.append((k, cur[0], cur[1], cur[2]))
        else:
            t = smoothstep((f+1)/3); tl.append((f"{keys[i-1]}->{k}", prev[0]+(cur[0]-prev[0])*t, prev[1]+(cur[1]-prev[1])*t, prev[2]+(cur[2]-prev[2])*t))
    prev = cur
frames = []
for i, (label, w, h, jaw) in enumerate(tl):
    dk = label.split("->")[-1] if "->" in label else label
    fr = render(dk, w, h, jaw); fr.save(os.path.join(OUT, "frames_lineclean", f"f{i:02d}_{dk}.png")); frames.append(fr.convert("RGB"))
frames[0].save(os.path.join(OUT, "pahgo-lineclean-20261031.gif"), save_all=True, append_images=frames[1:], duration=1000//24, loop=0)
print("lineclean gif", len(frames))

# --- 5. Contacts ---
def fitted(patch, size=None):
    fr = BASE.copy()
    p = patch if size is None else patch.resize(size, Image.LANCZOS)
    a = np.array(p); a[:, :, 3] = np.where(a[:, :, 3] >= 128, 255, 0); p = Image.fromarray(a)
    fr.alpha_composite(p, (int(round(CX - p.size[0]/2)), int(round(CY - p.size[1]/2))))
    return fr
# Line comparison: approved vs clean-line, normal + 3x zoom (mouth crop from fitted head)
def mouth_crop(fr): return fr.crop((140, 460, 330, 560))
old_fit = fitted(approved); new_fit = fitted(mbp_vec)
sheet = Image.new("RGB", (476*2 + 20, 688 + 300 + 44), (40, 40, 40)); d = ImageDraw.Draw(sheet)
sheet.paste(old_fit.convert("RGB"), (0, 22)); sheet.paste(new_fit.convert("RGB"), (476+20, 22))
d.text((6, 4), "APPROVED MBP (straight bridge) fitted", fill=(255, 255, 0)); d.text((476+26, 4), "NEW MBP clean vector line fitted", fill=(0, 255, 0))
sheet.paste(mouth_crop(old_fit).resize((570, 300), Image.NEAREST), (0, 710)); sheet.paste(mouth_crop(new_fit).resize((570, 300), Image.NEAREST), (590, 710))
d.text((6, 1014), "3x zoom below: approved left, clean vector right", fill=(255, 255, 0))
# Actually zoom rows are at y710-1010; label above them
sheet.save(os.path.join(OUT, "lineclean-before-after-20261031.png"))
# Pack contacts: mouth-only on magenta + fitted
for pack_name, items in packs.items():
    # mouth-only strip
    tiles = []
    for k, p in items.items():
        bg = Image.new("RGBA", (p.size[0], p.size[1]), (255, 0, 255, 255)); bg.alpha_composite(p); tiles.append(bg.convert("RGB"))
    Wc = sum(t.size[0] for t in tiles) + 20*len(tiles); Hc = max(t.size[1] for t in tiles) + 24
    s = Image.new("RGB", (Wc, Hc), (40, 40, 40)); dd = ImageDraw.Draw(s); x = 0
    for (k, p), t in zip(items.items(), tiles):
        s.paste(t, (x, 24)); dd.text((x+4, 4), k, fill=(255, 255, 0)); x += t.size[0] + 20
    s.save(os.path.join(OUT, f"pack-{pack_name}-mouthonly-20261031.png"))
    # fitted strip
    ftiles = [fitted(p).resize((238, 344), Image.LANCZOS).convert("RGB") for p in items.values()]
    fs = Image.new("RGB", (238*len(ftiles), 344+22), (40, 40, 40)); dd = ImageDraw.Draw(fs)
    for j, (k, t) in enumerate(zip(items.keys(), ftiles)):
        fs.paste(t, (238*j, 22)); dd.text((238*j+4, 4), k, fill=(255, 255, 0))
    fs.save(os.path.join(OUT, f"pack-{pack_name}-fitted-20261031.png"))
    print(pack_name, list(items.keys()))
with open(os.path.join(OUT, "measurements-clean-pipeline-20261031.json"), "w") as f:
    json.dump({"placement_target": [CX, CY], "stats": stats, "packs": {k: list(v.keys()) for k, v in packs.items()}}, f, indent=1)
print(json.dumps(stats, indent=1))
