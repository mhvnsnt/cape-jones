#!/usr/bin/env python3
"""Portrait feet-planted fix, with BOTH scale candidates, 20261031.
Mars 2026-10-31 20:23 CDT: portrait room-scale APPROVED PERFECT, but feet
need to be more planted — reads slightly too far in the background, slightly
floating off the ground, just slightly.
Mars 2026-10-31 20:24 CDT correction: bottom-right tile (new portrait) is
closer but still NOT correct scale; he thinks the correct version was up
0.5, and told us NOT to revert / regress. The up-0.5 number is AMBIGUOUS
("I think") — do NOT assert 3.0x as fact. Report BOTH 2.5x and 3.0x.

Measured old portrait (diff vs background-only portrait crop):
- figure diff bbox (172,386)-(906,1548), height 1162 (claimed 1165, 3px fringe)
- feet bottom 1548, rug far edge ~1421, rug near edge ~1868
- feet are 127px below rug far edge, 320px ABOVE rug near edge:
  feet are 28% down the rug ( (1548-1421)/(1868-1421) = 0.284 ), i.e. mid-rug,
  deep in the room, with a lot of empty rug in front of them. That is why
  the master gate ("feet on rug", 1371-1700) PASSED while Mars's eye still
  reads floating: the gate was too loose. No contact shadow was in the
  original composite either — flat white feet on a busy rug pattern.
- chair anchor in portrait framing (y unchanged from master):
  chair back top ~700, chair feet ~1518, chair height 818.
  figure/chair = 1165/818 = 1.424 (locked furniture ratio).
- Old landscape regression, for the gate demo: figure 655 in a 1080 frame
  has frame ratio 0.607, so a frame-ratio gate PASSES it — that is the bug.
  Furniture ratio: chair height in landscape framing = (625-286)*1.644-104
  = 558, figure/chair = 655/558 = 1.174, 17.6% BELOW locked 1.424.
  The new gate checks furniture ratio, not frame ratio alone.

Fix, portrait only (landscape is a separate agent's task, not rebuilt here):
- Same planted feet line for both candidates, so scale is the ONLY
  difference Mars is judging: FEET = 1700 (62% down the rug, 168px of rug
  left in front, vs 320px before).
- A, locked 2.5x: height 1165, head 535, frame ratio 0.607, chair ratio 1.424.
- B, up-0.5 candidate 3.0x: height round(1165*3.0/2.5)=1398, head 302,
  frame ratio 0.728, chair ratio 1.709 (+20.0% vs locked).
  B is a CANDIDATE, not a confirmed lock, until Mars picks it.
- Both: figure centre x kept at old portrait centre 539, whole in frame,
  no silent shrink, no recolour of base art. Contact shadow is a SEPARATE
  labelled layer (soft black ellipse under each foot, blurred), drawn
  under the figure, never baked into the base art.
- Chair-back-at-waist: still a WARNING, not a pass, in this KKGuh crop
  (waist A ~1152, B ~1043, chair back ~700). Do not fake it.
Background: STAND-IN batch-KKGuh, NOT canonical.
"""
import json, os
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(ROOT, "dual-light-variants-20261031/base-arms-up-transparent-20261031.png")
BGF = os.path.expanduser("~/workspace/cape-jones-flying/characters/sheets/backgrounds/batch-KKGuh.jpg")
OLD_DIR = os.path.join(ROOT, "dual-orientation-room-scale-fix-20261031")
OLD = os.path.join(OLD_DIR, "portrait-room-scale-1080x1920-20261031.png")

def cover(bg, size):
    im = bg.copy(); r = max(size[0]/im.width, size[1]/im.height)
    im = im.resize((round(im.width*r), round(im.height*r)), Image.LANCZOS)
    x = (im.width-size[0])//2; y = (im.height-size[1])//2
    return im.crop((x, y, x+size[0], y+size[1]))

fig = Image.open(FIG).convert("RGBA")
fb = fig.split()[3].getbbox()  # (222,239,880,1283)
bg = Image.open(BGF).convert("RGB")
master_bg = cover(bg, (1920, 1920))
port_bg = master_bg.crop((420, 0, 1500, 1920)).convert("RGBA")

def build(H, FEET, name):
    fh = round(H / ((fb[3]-fb[1]) / fig.height))
    fw = round(fig.width * fh / fig.height)
    fig_s = fig.resize((fw, fh), Image.LANCZOS)
    py = FEET - round(fb[3]*fh/fig.height)
    px = 539 - (round(fb[0]*fw/fig.width) + round((fb[2]-fb[0])*fw/fig.width)//2)
    # foot clusters from resized alpha, bottom 40 rows
    am = np.asarray(fig_s.split()[3])
    ay0, ay1 = py + round(fb[1]*fh/fig.height), py + round(fb[3]*fh/fig.height)
    # shadow layer, in portrait coords
    shadow = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    ab = round(fb[3]*fh/fig.height)
    bot = am[max(0, ab-40):ab, :]
    # map bottom-row alpha x clusters (in fig_s coords) to portrait coords
    cols = np.where((bot > 10).any(axis=0))[0]
    clusters = []
    if len(cols):
        cur = [cols[0]]
        for c in cols[1:]:
            if c - cur[-1] > 30:
                clusters.append(cur); cur = [c]
            else:
                cur.append(c)
        clusters.append(cur)
    for cl in clusters:
        if len(cl) < 20:
            continue
        cx = px + (cl[0] + cl[-1]) // 2
        w = (cl[-1] - cl[0]) // 2
        sd.ellipse([cx - int(w*0.75), FEET - 8, cx + int(w*0.75), FEET + 24],
                   fill=(0, 0, 0, 95))
    shadow = shadow.filter(ImageFilter.GaussianBlur(7))
    out = port_bg.copy()
    out.alpha_composite(shadow, (0, 0))
    out.alpha_composite(fig_s, (px, py))
    fx0 = px + round(fb[0]*fw/fig.width); fy0 = py + round(fb[1]*fh/fig.height)
    fx1 = px + round(fb[2]*fw/fig.width); fy1 = py + round(fb[3]*fh/fig.height)
    out.convert("RGB").save(os.path.join(OUT, name))
    # feet crop
    crop = out.convert("RGB").crop((100, 1380, 1000, 1850)).resize((1800, 940), Image.LANCZOS)
    crop.save(os.path.join(OUT, name.replace(".png", "-feet-crop.png")))
    return {"file": name, "bbox": [fx0, fy0, fx1, fy1], "height": fy1-fy0,
            "width": fx1-fx0, "head": fy0, "feet": fy1, "centre_x": (fx0+fx1)//2,
            "frame_ratio": round((fy1-fy0)/1920, 4),
            "chair_height_portrait": 818,
            "figure_chair_ratio": round((fy1-fy0)/818, 4),
            "rug_far_edge": 1421, "rug_near_edge": 1868,
            "rug_position": round((fy1-1421)/(1868-1421), 3),
            "rug_in_front_px": 1868-fy1,
            "shadow_clusters": len([c for c in clusters if len(c) >= 20])}

A = build(1165, 1700, "portrait-2p5-planted-20261031.png")
B = build(1398, 1700, "portrait-3p0-planted-20261031.png")
print("A", A); print("B", B)

# before/after contact: OLD | A | B, scaled to 360 wide each, header 44px
old = Image.open(OLD).convert("RGB")
a_im = Image.open(os.path.join(OUT, A["file"])).convert("RGB")
b_im = Image.open(os.path.join(OUT, B["file"])).convert("RGB")
def sc(im, w=360): return im.resize((w, round(im.height*w/im.width)), Image.LANCZOS)
sheet = Image.new("RGB", (1080, 44 + 640), (128, 128, 128))
d = ImageDraw.Draw(sheet)
d.text((10, 12), "OLD portrait (feet 1548, mid-rug) | A 2.5x planted (feet 1700) | B 3.0x candidate planted (feet 1700)", fill=(255, 255, 0))
sheet.paste(sc(old), (0, 44)); sheet.paste(sc(a_im), (360, 44)); sheet.paste(sc(b_im), (720, 44))
sheet.save(os.path.join(OUT, "before-after-contact-20261031.png"))

meta = {"old_portrait": {"file": "portrait-room-scale-1080x1920-20261031.png",
        "diff_bbox": [172, 386, 906, 1548], "height_diff": 1162, "height_claimed": 1165,
        "feet": 1548, "rug_far_edge": 1421, "rug_near_edge": 1868,
        "rug_position": 0.284, "rug_in_front_px": 320, "chair_ratio": 1.424,
        "verdict": "scale locked, feet NOT planted (mid-rug, no contact shadow)"},
        "A_locked_2p5_planted": A, "B_up0p5_candidate_3p0_planted": B,
        "chair_back_warning": "waist A ~1152, B ~1043, chair back ~700 — WARNING, not a pass",
        "background": "STAND-IN batch-KKGuh, NOT canonical"}
json.dump(meta, open(os.path.join(OUT, "measurements-20261031.json"), "w"), indent=2)
print(json.dumps(meta, indent=2))
