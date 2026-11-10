#!/usr/bin/env python3
"""
Mouth / lip / jaw movement system for Cape Jones — 2026-10-31.
Pulled Robin mouths only for production proofs. NO PIL vector mouths.
NO duplicated EH for missing OH. OH = GAP (clean head, jaw still moves).
Input dependency, stated plainly: the separate tight-cut re-cut agent's
output was NOT ready when this was built (its folder was empty), so this
builder uses the existing pulled patches in superhero-mouths-20261031/mouths/
with a tight bbox crop, and states that dependency in the report. It does
NOT use the old loose fitted heads, and it does NOT use mixed-angle mouths
beyond the pulled set itself (all Robin, front-facing model-sheet heads
per the original library; angle audit for the re-cut is the other agent's job).

Jaw model, honest proxy: the jaw is NOT a true rotated mandible mesh.
It is a lower-face shift: the chin region below y=560 (4x head) is shifted
down by jaw_drop, the gap is filled with skin sampled from the chin, and
the mouth patch height is stretched from its top (upper lip fixed, lower
lip follows the jaw). That reads as jaw drop in 2D, and is labelled a proxy.
"""
import json, math, os
from PIL import Image, ImageDraw

ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(ROOT, "mouth-jaw-movement-20261031")
BASE = Image.open(os.path.join(ROOT, "visemes-v2-20261031/clean-head-base-20261031.png")).convert("RGBA")
W, H = BASE.size  # 476 x 688

# --- pulled mouth patches, tight bbox crop ---------------------------------
PATCHES = {
    # Front-only tight re-cut set from pahgo-mouth-fix-20261031/.
    # MBP-front = NEW 09 model-sheet closed (front). AH-front = 03 open
    # smile, FRONT, used as AH (shape cost: smile, not shout, no upper
    # teeth — 01 shout is 3/4 and was rejected for a front head).
    # GK-front = 05 grit, FRONT, tight (chin/jaw curve dropped).
    # Corner wrinkles kept by that re-cut: 0.
    "MBP": "mbp-front-09_tight_patch.png",
    "AH":  "ah-front-03_tight_patch.png",
    "GK":  "gk-front-05_tight_patch.png",
}
def tight(path):
    im = Image.open(path).convert("RGBA")
    a = im.getchannel("A")
    bbox = a.getbbox()
    assert bbox, path
    return im.crop(bbox)

mouths = {}
for k, fn in PATCHES.items():
    mouths[k] = tight(os.path.join(ROOT, "pahgo-mouth-fix-20261031/mouths-tight", fn))
    print(k, fn, "tight", mouths[k].size)

# --- placement, Mars correction: left, down, 0.75x ---------------------------
# Original fitted placement: zone [111,409,392,560], width 281, centre (251.5, 484.5).
# Mars ordered: a little more left, a little more down, scaled down 25%.
# "A little" is not a number from Mars, so this builder uses measured
# provisional amounts and states them: left 12px, down 10px (4x head scale).
# 0.75x IS Mars's number. These are provisional until Mars confirms the
# left/down amounts on the fixed version.
ZONE_CX, ZONE_CY = 251.5, 484.5
# Fixed agent's interpretation of Mars's "a little more" (direction + 0.75x
# are Mars's; -20/+20 px are the fixed agent's, stated plainly there):
SHIFT_L, SHIFT_D, SCALE = -20, +20, 0.75
TARGET_W = None  # per-viseme placed sizes below, from the fixed agent
CX, CY = ZONE_CX + SHIFT_L, ZONE_CY + SHIFT_D
print(f"placement centre ({CX}, {CY}) shift L{SHIFT_L} D{SHIFT_D} scale {SCALE} (per-viseme placed sizes in PARAMS)")

# --- jaw / lip parameters per viseme ----------------------------------------
# jaw_drop px at 4x head scale; lip_w / lip_h are multipliers on the
# placed mouth size (1.0 = placed size). FACS names are mappings, not runs.
# Absolute placed sizes (alpha, after 0.75x) from pahgo-mouth-fix:
# MBP 178x23, AH 196x67, GK 188x30. Jaw in px at 4x head scale.
PARAMS = {
    "MBP": dict(jaw=0,  w=178, h=23, label="MBP closed front (AU24, jaw shut)"),
    "AH":  dict(jaw=16, w=196, h=67, label="AH-front open smile (AU25+AU26 jaw drop)"),
    "GK":  dict(jaw=8,  w=188, h=30, label="GK grit front, spread (AU12, mapping)"),
    "GAP": dict(jaw=10, w=0,   h=0,  label="OH GAP — no mouth patch, jaw still drops"),
    "REST":dict(jaw=0,  w=178, h=23, label="REST = MBP closed"),
}
JAW_SPLIT = 560  # chin region below this line shifts with the jaw

def skin_fill():
    # mean skin colour sampled from the chin region of the clean head
    crop = BASE.crop((180, 580, 300, 660))
    px = [p for p in crop.getdata() if p[3] > 200]
    r = sum(p[0] for p in px)//len(px); g = sum(p[1] for p in px)//len(px); b = sum(p[2] for p in px)//len(px)
    return (r, g, b, 255)

SKIN = skin_fill()
print("skin fill", SKIN)

def render_frame(viseme, w_mul, h_mul, jaw):
    """One head frame. Mouth anchored at its top (upper lip fixed)."""
    frame = BASE.copy()
    # jaw: shift chin region down, fill the gap with skin
    jaw = int(round(jaw))
    if jaw > 0:
        chin = frame.crop((0, JAW_SPLIT, W, H))
        # Gap fill masked to the head silhouette: use the head alpha row
        # just above the split, replicated down the gap. The first version
        # filled the full width and leaked a skin stripe outside the head.
        head_alpha = BASE.getchannel("A")
        row = head_alpha.crop((0, JAW_SPLIT - 1, W, JAW_SPLIT))
        # Fill with the hinge row's own pixels stretched down, not a flat
        # mean skin colour — the flat fill left a visible hinge seam.
        hinge = BASE.crop((0, JAW_SPLIT - 1, W, JAW_SPLIT))
        band = Image.new("RGBA", (W, jaw))
        for yy in range(jaw):
            band.paste(hinge, (0, yy))
        mask = Image.new("L", (W, jaw), 0)
        for yy in range(jaw):
            mask.paste(row, (0, yy))
        frame.paste(band, (0, JAW_SPLIT), mask)
        frame.paste(chin, (0, JAW_SPLIT + jaw))
    meas = dict(viseme=viseme, jaw_drop=jaw, mouth_w=0, mouth_h=0,
                mouth_cx=CX, mouth_top=None, wrinkle_l=0, wrinkle_r=0)
    if viseme in ("GAP",):
        return frame, meas
    if viseme == "REST":
        viseme = "MBP"
    patch = mouths[viseme]
    tw = int(round(w_mul))
    th = int(round(h_mul))
    # height stretch is from the top: upper lip stays, lower lip follows jaw
    resized = patch.resize((tw, th), Image.LANCZOS)
    top = int(round(CY - th / 2 + jaw * 0.25))  # mouth centre follows jaw a quarter
    left = int(round(CX - tw / 2))
    frame.alpha_composite(resized, (left, top))
    # corner-wrinkle measurement: dark pixels in the patch's own corner zones.
    # Nothing is drawn: wrinkles are the pulled patch's own corner linework,
    # counted, not invented. Honest limit: this count includes the mouth
    # outline in the corner zone, so it is corner-linework presence, not
    # isolated wrinkle strokes separated from the outline.
    import numpy as np
    arr = np.array(resized)
    alpha = arr[:, :, 3] > 50
    dark = (arr[:, :, 0] < 90) & (arr[:, :, 1] < 90) & (arr[:, :, 2] < 90)
    cw = max(4, tw // 5)
    meas.update(mouth_w=tw, mouth_h=th, mouth_top=top,
                wrinkle_l=int((alpha[:, :cw] & dark[:, :cw]).sum()),
                wrinkle_r=int((alpha[:, tw - cw:] & dark[:, tw - cw:]).sum()))
    return frame, meas

def smoothstep(t):
    return t * t * (3 - 2 * t)

def timeline(keys, fps=24):
    """keys: list of visemes, one key every 6 frames, 3-frame smooth
    interpolation into each new key. Returns list of (viseme_label, w, h, jaw)."""
    frames = []
    prev = PARAMS[keys[0]]
    for i, k in enumerate(keys):
        cur = PARAMS[k]
        for f in range(6):
            if i == 0 or f >= 3:
                frames.append((k, cur["w"], cur["h"], cur["jaw"]))
            else:
                t = smoothstep((f + 1) / 3)
                frames.append((f"{keys[i-1]}->{k}",
                               prev["w"] + (cur["w"] - prev["w"]) * t,
                               prev["h"] + (cur["h"] - prev["h"]) * t,
                               prev["jaw"] + (cur["jaw"] - prev["jaw"]) * t))
        prev = cur
    return frames

def build(name, keys, subdir):
    tl = timeline(keys)
    import shutil
    if os.path.isdir(os.path.join(OUT, subdir)):
        shutil.rmtree(os.path.join(OUT, subdir))
    os.makedirs(os.path.join(OUT, subdir), exist_ok=True)
    meas = []
    gif_frames = []
    for i, (label, w, h, jaw) in enumerate(tl):
        # label may be a transition; the viseme to draw is the target key
        draw_key = label.split("->")[-1] if "->" in label else label
        fr, m = render_frame(draw_key, w, h, jaw)
        m["frame"] = i; m["timeline_label"] = label
        meas.append(m)
        fr.save(os.path.join(OUT, subdir, f"f{i:02d}_{draw_key}.png"))
        gif_frames.append(fr.convert("RGB"))
    gif_frames[0].save(os.path.join(OUT, f"{name}.gif"), save_all=True,
                       append_images=gif_frames[1:], duration=1000 // 24, loop=0)
    with open(os.path.join(OUT, f"{name}-measurements.json"), "w") as f:
        json.dump({"phrase_keys": keys, "placement": {"centre": [CX, CY],
                   "shift_left": SHIFT_L, "shift_down": SHIFT_D, "scale": SCALE,
                   "placed_sizes": {k: {"w": v["w"], "h": v["h"]} for k, v in PARAMS.items()}},
                   "frames": meas}, f, indent=1)
    print(name, len(tl), "frames, jaw range", min(m["jaw_drop"] for m in meas),
          "to", max(m["jaw_drop"] for m in meas))
    return meas, tl

def contact(name, keys, frames_dir, picks):
    import glob
    by = {}
    for f in glob.glob(os.path.join(OUT, frames_dir, "f*.png")):
        by[int(os.path.basename(f)[1:3])] = f
    tiles = []
    for i in picks:
        tiles.append(Image.open(by[i]).resize((238, 344), Image.LANCZOS))
    sheet = Image.new("RGB", (238 * len(tiles), 344 + 22), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    for j, t in enumerate(tiles):
        sheet.paste(t, (238 * j, 22))
        d.text((238 * j + 6, 4), f"f{picks[j]}", fill=(255, 255, 0))
    sheet.save(os.path.join(OUT, f"{name}-contact.png"))
    print(name, "contact", sheet.size)

# PAH GO first: P(MBP) - AH - G(GK mapping) - O(GAP), then rest
pahgo_meas, _ = build("pahgo-movement", ["MBP", "AH", "GK", "GAP", "REST"], "frames_pahgo")
contact("pahgo-movement", ["MBP", "AH", "GK", "GAP", "REST"], "frames_pahgo", [3, 9, 15, 21, 27])

# Longer phrase, only honestly covered front tight shapes: PAH GO AH
# keys: MBP, AH, GK, GAP, AH, REST — no invented OH/OO, no EH duplication,
# no EE (04 is front but was not re-cut tight in the fixed set, so it is
# NOT used as a movement key here).
phrase_meas, _ = build("phrase-movement", ["MBP", "AH", "GK", "GAP", "AH", "REST"], "frames_phrase")
contact("phrase-movement", ["MBP", "AH", "GK", "GAP", "AH", "REST"], "frames_phrase", [3, 9, 15, 21, 27, 33])
print("done")
