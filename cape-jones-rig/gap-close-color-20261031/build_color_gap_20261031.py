#!/usr/bin/env python3
"""Gap-close chunk C — COLOUR / BLENDER / LIGHTING (PIL parts only).
Blender parts are separate scripts (ACES Cycles renders, Cycles room proof).
Method for JoJo shifts: v3 palette REPLACEMENT (nearest-base classification,
new = shifted + (pixel - base), clamped). Black outline never reassigned.
No show art/name/dialogue/logo. Labels on sheets only, never in clean pieces.
"""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = os.path.expanduser("~/workspace/cape-jones-rig/gap-close-color-20261031")
RIG = os.path.expanduser("~/workspace/cape-jones-rig")
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else F, sz)

BASE = {"cowl": (90,39,114), "skin": (239,175,131), "suit": (255,255,255),
        "shadow": (178,186,199), "cape": (23,21,26)}
BG_GREY = (128,128,128)

PALETTES = {
 "TENSION": {"cowl": (255,40,140), "skin": (250,170,150), "suit": (255,110,180),
   "shadow": (200,90,150), "cape": (255,20,120), "eye": (255,220,235),
   "world": ((255,110,180),(130,40,170),(90,20,60)), "suit_note": "CHANGED to rose",
   "theory": "magenta-rose, split-complementary off violet"},
 "POWER": {"cowl": (200,20,40), "skin": (245,180,140), "suit": (255,80,50),
   "shadow": (190,60,50), "cape": (220,30,50), "eye": (255,230,200),
   "world": ((255,90,40),(140,30,30),(70,15,15)), "suit_note": "CHANGED to red-orange",
   "theory": "scarlet / red-orange, complementary heat"},
 "DREAM": {"cowl": (40,200,210), "skin": (255,200,180), "suit": (255,255,255),
   "shadow": (178,186,199), "cape": (255,60,180), "eye": (220,250,255),
   "world": ((80,220,230),(255,140,200),(30,90,110)), "suit_note": "WHITE (addendum Variant A)",
   "theory": "turquoise + magenta-pink bath, split-complementary"},
 "BRIGHT PINK": {"cowl": (255,40,140), "skin": (250,175,160), "suit": (255,255,255),
   "shadow": (178,186,199), "cape": (255,80,200), "eye": (255,225,240),
   "world": ((255,150,190),(130,40,170),(90,20,60)), "suit_note": "WHITE (pink-hour variant)",
   "theory": "TENSION-family pink-hour world, suit held white"},
 "UNCERTAINTY": {"cowl": (110,110,110), "skin": (190,190,190), "suit": (230,230,230),
   "shadow": (150,150,150), "cape": (30,30,30), "eye": (240,240,240),
   "world": ((170,170,170),(110,110,110),(60,60,60)), "suit_note": "CHANGED to near-white grey",
   "theory": "monochromatic — hue removal IS the shift"},
}
BASE_PAL = {"cowl": (90,39,114), "skin": (239,175,131), "suit": (255,255,255),
  "shadow": (178,186,199), "cape": (23,21,26), "eye": (255,255,255),
  "world": ((150,180,210),(90,140,90),(120,90,60)), "suit_note": "canon white",
  "theory": "canon base"}

_CACHE = {}
def _classify(pose_path):
    if pose_path in _CACHE:
        return _CACHE[pose_path]
    a = np.array(Image.open(pose_path).convert("RGB")).astype(np.int16)
    bg = np.all(np.abs(a - np.array(BG_GREY)) < 20, axis=2)
    outline = np.all(a <= 18, axis=2)
    keys = ["cowl", "skin", "suit", "shadow", "cape"]
    bases = np.array([BASE[k] for k in keys], dtype=np.int16)
    d = np.sqrt(((a[:, :, None, :].astype(float) - bases[None, None, :, :]) ** 2).sum(axis=3))
    nearest = d.argmin(axis=2)
    mind = d.min(axis=2)
    ok = (~bg) & (~outline) & (mind < 90)
    delta = a - bases[nearest]
    res = (a, bg, ok, nearest, delta)
    _CACHE[pose_path] = res
    return res

def classify_replace(im_rgb, pal):
    a = np.array(im_rgb).astype(int)
    bg = np.all(np.abs(a - np.array(BG_GREY)) < 20, axis=2)
    return a, bg, None

def plate_on_world(pose_path, pal, pw=420, ph=600):
    """Pose plate recoloured (cached classification), over flat world bands."""
    a, bg, ok, nearest, delta = _classify(pose_path)
    keys = ["cowl", "skin", "suit", "shadow", "cape"]
    shifted = np.array([pal[k] for k in keys], dtype=np.int16)
    new = shifted[nearest] + delta
    arr = np.where(ok[:, :, None], np.clip(new, 0, 255), a).astype(np.uint8)
    H, W = arr.shape[:2]
    world = np.empty_like(arr)
    world[:int(H * 0.45)] = pal["world"][0]
    world[int(H * 0.45):int(H * 0.68)] = pal["world"][1]
    world[int(H * 0.68):] = pal["world"][2]
    comp = np.where(bg[:, :, None], world, arr)
    return Image.fromarray(comp).resize((pw, ph), Image.LANCZOS)

def sheet_title(draw, title, sub, W):
    draw.rectangle([0, 0, W, 78], fill=(20, 20, 20))
    draw.text((16, 8), title, font=font(26, True), fill=(255, 255, 255))
    draw.text((16, 44), sub, font=font(16), fill=(220, 220, 220))

def footer(draw, y, W, text):
    draw.text((16, y), text, font=font(15), fill=(30, 30, 30))

# ---------------------------------------------------------------- task 3
def build_task3():
    fight = os.path.join(RIG, "reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png")
    panels = [("BASE (canon)", BASE_PAL)] + [(k, PALETTES[k]) for k in
              ["TENSION", "POWER", "DREAM", "BRIGHT PINK"]]
    pw, ph = 420, 600
    gap, mx = 12, 16
    W = mx * 2 + 5 * pw + 4 * gap
    rows = []
    for name, pal in panels:
        rows.append((name, pal))
    table_y = 78 + 16 + ph + 40
    table_h = 30 + len(panels) * 34 + 60
    H = table_y + table_h + 30
    sheet = Image.new("RGB", (W, H), (245, 245, 245))
    d = ImageDraw.Draw(sheet)
    sheet_title(d, "JOJO POSE SHIFTS — clean fighting pose, v3 palette replacement (NOT a gain)",
                "Cape = FULL colour per addendum (Mars 16:35). Suit white in two, changed in two. Black outline never reassigned.",
                W)
    x = mx
    for name, pal in panels:
        panel = plate_on_world(fight, pal, pw, ph)
        sheet.paste(panel, (x, 78 + 16))
        d.rectangle([x, 78 + 16, x + pw - 1, 78 + 16 + ph - 1], outline=(0, 0, 0), width=2)
        d.text((x + 8, 78 + 16 + ph + 4), name, font=font(17, True), fill=(0, 0, 0))
        x += pw + gap
    # palette table on sheet
    y = table_y + 34
    d.text((mx, table_y), "PALETTE TABLE — base (90,39,114) cowl / (239,175,131) skin / (255,255,255) suit / (178,186,199) shadow / (23,21,26) cape",
           font=font(15, True), fill=(0, 0, 0))
    hdr = ["Palette", "Cowl", "Skin", "Suit", "Suit shadow", "Cape (FULL)", "World sky/hills/ground"]
    colx = [mx, mx + 190, mx + 340, mx + 500, mx + 740, mx + 900, mx + 1060]
    for cx, htxt in zip(colx, hdr):
        d.text((cx, y), htxt, font=font(14, True), fill=(0, 0, 0))
    y += 26
    for name, pal in panels:
        stag = "WHITE" if "WHITE" in pal["suit_note"] else ("CHANGED" if "CHANGED" in pal["suit_note"] else "canon")
        vals = [name, str(pal["cowl"]), str(pal["skin"]),
                f'{pal["suit"]} {stag}', str(pal["shadow"]),
                str(pal["cape"]), f'{pal["world"][0]}/{pal["world"][1]}/{pal["world"][2]}']
        for cx, v in zip(colx, vals):
            d.text((cx, y), v, font=font(14), fill=(0, 0, 0))
        y += 30
    y += 8
    footer(d, y, W, "Method: nearest-base classification + delta remap, clamped; fringe pixels >90 from any base left untouched (v3 cape-fringe speckle note applies).")
    y += 26
    footer(d, y, W, "NOT Mars-approved (0/4 here). Production Blender renders of these shifts: still owed. Pose: clean fighting pose, gauntlet-out-fixed.")
    out = os.path.join(OUT, "jojo-pose-shifts-fighting-20261031.png")
    sheet.save(out)
    print("task3", out, sheet.size)
    return out

# ---------------------------------------------------------------- task 4
def build_task4():
    fight = os.path.join(RIG, "reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png")
    beats = [
        ("1  BASE", BASE_PAL, "Establishing, room. Canon palette.",
         "warm gold front key", "warm amber (255,180,80)", "both", "48f (2.0s)", "Already base"),
        ("2  TENSION", PALETTES["TENSION"], "Threat lands — the beat tightens.",
         "magenta-rose shifted key", "magenta-rose (255,40,140) — rim follows SHIFTED key",
         "both", "36f (1.5s)", "Cut to POWER, never fade through base"),
        ("3  POWER", PALETTES["POWER"], "Power lands — explosive beat.",
         "scarlet shifted key", "scarlet/orange (255,80,50) — rim follows SHIFTED key",
         "both", "48f (2.0s)", "Cut to UNCERTAINTY on the doubt beat"),
        ("4  UNCERTAINTY", PALETTES["UNCERTAINTY"], "Doubt — nothing is certain.",
         "neutral grey shifted key", "grey (230,230,230) — rim follows SHIFTED key",
         "both", "36f (1.5s)", "Hard cut to BASE on the decision beat"),
        ("5  RETURN TO BASE", BASE_PAL, "He decides — canon restored.",
         "warm gold front key", "warm amber (255,180,80)", "both", "48f (2.0s)",
         "RETURN RULE: hard palette cut on the decision beat, not a grade fade"),
    ]
    pw, ph = 400, 570
    gap, mx = 12, 16
    W = mx * 2 + 5 * pw + 4 * gap
    table_y = 78 + 16 + ph + 44
    H = table_y + 30 + len(beats) * 56 + 70
    sheet = Image.new("RGB", (W, H), (245, 245, 245))
    d = ImageDraw.Draw(sheet)
    sheet_title(d, "JOJO SEQUENCE COLOUR SCRIPT — 5 beats: base -> tension -> power -> uncertainty -> return to base",
                "Rim always follows the SHIFTED key, never the base key. Return is a hard cut, not a fade. No shift without a trigger.", W)
    x = mx
    for name, pal, trig, key, rim, scope, dur, ret in beats:
        panel = plate_on_world(fight, pal, pw, ph)
        sheet.paste(panel, (x, 78 + 16))
        d.rectangle([x, 78 + 16, x + pw - 1, 78 + 16 + ph - 1], outline=(0, 0, 0), width=2)
        d.text((x + 8, 78 + 16 + ph + 6), f"{name} — {dur}", font=font(16, True), fill=(0, 0, 0))
        x += pw + gap
    y = table_y
    d.text((mx, y), "BEAT TABLE — trigger / palette / scope / duration / rim under shifted key / return rule", font=font(15, True), fill=(0, 0, 0))
    y += 28
    palnames = {"1  BASE": "BASE", "2  TENSION": "TENSION", "3  POWER": "POWER",
                "4  UNCERTAINTY": "UNCERTAINTY", "5  RETURN TO BASE": "BASE"}
    for name, pal, trig, key, rim, scope, dur, ret in beats:
        d.text((mx, y), f"{name}: trigger: {trig} | palette: {palnames[name]} | scope: {scope} | {dur}",
               font=font(14), fill=(0, 0, 0))
        y += 24
        d.text((mx, y), f"      key: {key} | rim: {rim} | return: {ret}", font=font(14), fill=(0, 0, 0))
        y += 30
    y += 6
    footer(d, y, W, "JSON twin carries the same beats machine-readably. NOT Mars-approved. Durations at 24fps; total 216f (9.0s).")
    out = os.path.join(OUT, "jojo-sequence-colour-script-20261031.png")
    sheet.save(out)
    data = {"sequence": "base -> tension -> power -> uncertainty -> return to base",
            "fps": 24, "total_frames": 216, "mars_approved": False,
            "beats": [
        {"beat": 1, "name": "BASE", "trigger": "Establishing, room. Canon palette.",
         "palette": "BASE", "scope": "both", "duration_frames": 48, "duration_s": 2.0,
         "key": "warm gold front key", "rim_under_shifted_key": "warm amber (255,180,80)",
         "return_rule": "Already base"},
        {"beat": 2, "name": "TENSION", "trigger": "Threat lands — the beat tightens.",
         "palette": "TENSION", "cape": "FULL magenta (255,20,120)", "suit": "CHANGED to rose (255,110,180)",
         "scope": "both", "duration_frames": 36, "duration_s": 1.5,
         "key": "magenta-rose shifted key", "rim_under_shifted_key": "magenta-rose (255,40,140)",
         "return_rule": "Cut to POWER, never fade through base"},
        {"beat": 3, "name": "POWER", "trigger": "Power lands — explosive beat.",
         "palette": "POWER", "cape": "FULL scarlet (220,30,50)", "suit": "CHANGED to red-orange (255,80,50)",
         "scope": "both", "duration_frames": 48, "duration_s": 2.0,
         "key": "scarlet shifted key", "rim_under_shifted_key": "scarlet/orange (255,80,50)",
         "return_rule": "Cut to UNCERTAINTY on the doubt beat"},
        {"beat": 4, "name": "UNCERTAINTY", "trigger": "Doubt — nothing is certain.",
         "palette": "UNCERTAINTY", "cape": "neutral (30,30,30) — monochromatic choice",
         "suit": "CHANGED to near-white grey (230,230,230)",
         "scope": "both", "duration_frames": 36, "duration_s": 1.5,
         "key": "neutral grey shifted key", "rim_under_shifted_key": "grey (230,230,230)",
         "return_rule": "Hard cut to BASE on the decision beat"},
        {"beat": 5, "name": "RETURN TO BASE", "trigger": "He decides — canon restored.",
         "palette": "BASE", "scope": "both", "duration_frames": 48, "duration_s": 2.0,
         "key": "warm gold front key", "rim_under_shifted_key": "warm amber (255,180,80)",
         "return_rule": "RETURN RULE: hard palette cut on the decision beat, not a grade fade"},
    ]}
    jout = os.path.join(OUT, "jojo-sequence-colour-script-20261031.json")
    json.dump(data, open(jout, "w"), indent=2)
    print("task4", out, sheet.size, jout)
    return out, jout

if __name__ == "__main__":
    build_task3()
    build_task4()
