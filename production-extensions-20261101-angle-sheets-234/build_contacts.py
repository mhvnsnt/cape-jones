#!/usr/bin/env python3
"""Labelled contact sheets. Every cell carries its status so a derived
piece can never be mistaken for native art."""
import os, json
from PIL import Image, ImageDraw, ImageFont

OUT = "/tmp/angle-sheets-234"
try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
    FONT_S = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
except Exception:
    FONT, FONT_S = ImageFont.load_default(), ImageFont.load_default()

def cell(im_or_none, label, sub, cw, ch):
    c = Image.new("RGBA", (cw, ch), (255, 255, 255, 255))
    d = ImageDraw.Draw(c)
    if im_or_none is None:
        d.rectangle([20, 20, cw - 20, ch - 110], outline=(180, 0, 0), width=4)
        d.text((cw // 2, (ch - 90) // 2), "SPEC ONLY\nNO ART", font=FONT, fill=(180, 0, 0), anchor="mm", align="center")
    else:
        im = im_or_none.copy()
        im.thumbnail((cw - 20, ch - 110), Image.LANCZOS)
        c.alpha_composite(im, ((cw - im.width) // 2, (ch - 100 - im.height) // 2 + 5))
    d.text((cw // 2, ch - 72), label, font=FONT_S, fill=(0, 0, 0), anchor="mm")
    d.text((cw // 2, ch - 38), sub, font=FONT_S, fill=(90, 90, 90), anchor="mm")
    return c

def sheet(cells, cols, cw, ch, title, path):
    rows = (len(cells) + cols - 1) // cols
    W, H = cols * cw, 70 + rows * ch
    base = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(base)
    d.text((20, 18), title, font=FONT, fill=(0, 0, 0))
    for i, c in enumerate(cells):
        base.alpha_composite(c, ((i % cols) * cw, 70 + (i // cols) * ch))
    base.convert("RGB").save(path)
    print(path, base.size)

idx = json.load(open(os.path.join(OUT, "piece-index-20261101.json")))
by = {r["item"]: r for r in idx}
def piece(name):
    r = by[name]
    if not r["output"]:
        return None
    return Image.open(os.path.join(OUT, r["output"]))

# Z contact: 3 cols x 4 rows
order = [
    ("Hand_Fist_Z_Close", "Hand_Fist_Z_Close", "DERIVED 1.5x scale"),
    ("Hand_Palm_Z_Close", "Hand_Palm_Z_Close", "DERIVED 1.5x scale"),
    ("UpperArm_Z_Short", "UpperArm_Z_Short", "DERIVED warp x1.30/y0.55"),
    ("Forearm_Gauntlet_AimingAtLens", "Gauntlet_AimingAtLens", "DERIVED composite"),
    ("Thigh_KneeForward_Z", "Thigh_KneeForward_Z", "DERIVED trapezoid warp"),
    ("Shin_Boot_Z_Compressed", "Shin_Boot_Z_Compressed", "DERIVED warp x1.12/y0.62"),
    ("Foot_Kick_Z", "Foot_Kick_Z", "DERIVED 1.5x sole swap"),
    ("Pelvis_Whole_TiltBack", "Pelvis_Whole_TiltBack", "REISSUE of Pelvis_UnderView"),
    ("Torso_LeanBack", "Torso_LeanBack", "EXISTS-PRIOR slice"),
    ("Head_TiltDown_Z", "Head_TiltDown_Z", "SPEC-ONLY - needs new art"),
    ("Head_TiltUp_Z", "Head_TiltUp_Z", "SPEC-ONLY - needs new art"),
]
cells = [cell(piece(k), lbl, sub, 500, 460) for k, lbl, sub in order]
cells.append(cell(None, "NOT A SHEET", "See assemblies contact", 500, 460))
sheet(cells, 3, 500, 460, "Sheet-1 Z pieces - status per cell (derived != native art) - 20261101",
      os.path.join(OUT, "contact-sheet-z-pieces-20261101.png"))

# Assemblies contact: 3 cols
acells = []
for item, lbl, sub in [
    ("Angle_Sheet_2_BirdsEye", "Sheet 2 Bird's-Eye +45d", "DERIVED ASSEMBLY, not native"),
    ("Angle_Sheet_3_WormsEye", "Sheet 3 Worm's-Eye -45d", "DERIVED ASSEMBLY, not native"),
    ("Angle_Sheet_4_DiagonalLunge", "Sheet 4 Diagonal Lunge", "DERIVED ASSEMBLY, not native"),
]:
    im = Image.open(os.path.join(OUT, by[item]["output"]))
    acells.append(cell(im, lbl, sub, 620, 760))
sheet(acells, 3, 620, 760, "Angle Sheets 2-4 - DERIVED ASSEMBLIES ONLY (specs are the deliverable; native sheets still owed)",
      os.path.join(OUT, "contact-sheet-angle-sheets-234-20261101.png"))
