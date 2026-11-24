#!/usr/bin/env python3
"""Draw BROTHERMAN Rig Jones 2 cutout parts with PIL — from the APPROVED
concept art (owner 2026-11-23 19:42 EST: Rig Jones 1 is a cool FIRST rig,
saved as DRAFT; Rig Jones 2 must look like the approved concept).

Approved sources (read-only, NOT copied pixel-for-pixel — parts are
re-drawn in the same style, measured from the art):
- brotherman/media-generation-brotherman-v3-exact-bald-top-*.webp
  (sha256 8879ad70..., owner: "That's perfect, yeah"): bald top, long
  blond hair sides/back, blue tank #2B8FD4, BROTHERMAN in pink #EC4D8C
  comic letters, pink+blue+purple SPIRAL tie-dye tights, championship
  belt with big oval gold buckle + black centre, white wristbands,
  blue lace-up boots with pink laces, tanned skin #D89B62, blond #E8C25E.
- v3-pink-bandana (pink bandana, gold STAR buckle variant) and
  v4-cape-correct (Cape likeness correct in-scene).

What was WRONG with the draft (own-eyes, rest-f0001.png):
- tiny head, flat-rectangle mustache, eyes pinpricks, no jaw, no muscle
- rectangular torso, small flat letters, tie-dye = concentric target
  rings, belt a thin strip with a star, arms/legs thin sticks.
Rig Jones 2 fixes, measured from v3: head ~1.35x bigger, face wide with
a broad strong jaw, horseshoe with ridge detail, BIG blue eyes, thick
blond angled brows, long wavy side hair to the shoulders, torso 6.6
units wide with pecs + abs shading, letters 190px comic pink with dark
outline + starburst ticks, tie-dye = real SPIRAL arms (not rings),
championship belt = wide strap + big oval gold buckle, boots tall with
pink X laces, arms/legs thick and muscular.

CLEAN ALPHA LAW (permanent, owner 2026-11-23 11:22 EST): every part cut
along the art's own edges, transparent alpha, no rectangular edges, no
baked background. SOCKET-CUT JOINTS (V3 rule): elbow/knee = ball in the
lower piece + concave socket in the upper piece — NO caps/discs/circles
ever. Hands: one per arm, wrist at TOP, fingers DOWN, wrist-to-wrist.

Layout (Y up, ground 0 — same armature as draft): head top 16.85,
shoulder 13.3, elbow 10.8, wrist 8.3, hip 7.6, knee 4.3, ankle 1.5.
1 rig unit = 200 px (drawn at 400 = 2x supersample, then halved).
"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__)) + "/parts"
os.makedirs(OUT, exist_ok=True)

SKIN = (216, 155, 98, 255)       # tanned #D89B62
SKIN_D = (190, 128, 76, 255)     # skin shade
BLOND = (232, 194, 94, 255)      # #E8C25E
BLOND_D = (196, 152, 52, 255)    # blond shade
BLUE = (43, 143, 212, 255)       # tank/boot blue #2B8FD4
BLUE_L = (64, 178, 222, 255)     # tank highlight
PINK = (236, 77, 140, 255)       # #EC4D8C
PURPLE = (123, 75, 214, 255)     # tie-dye purple #7B4BD6
PURPLE_D = (74, 32, 130, 255)    # letter outline
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
GOLD = (232, 184, 58, 255)
GOLD_D = (176, 128, 32, 255)
DARK = (26, 26, 26, 255)
INK = (12, 12, 12, 255)
EYE_BLUE = (43, 108, 176, 255)
TONGUE = (224, 122, 122, 255)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

S = 400


def canvas(wu, hu):
    im = Image.new("RGBA", (int(wu * S), int(hu * S)), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def save(name, im):
    w, h = im.size
    im2 = im.resize((w // 2, h // 2), Image.LANCZOS)
    im2.save(os.path.join(OUT, name))
    print(name, im2.size)


def flip(src_name, dst_name):
    Image.open(os.path.join(OUT, src_name)).transpose(Image.FLIP_LEFT_RIGHT).save(os.path.join(OUT, dst_name))
    print(dst_name, "(flipped)")


def u(box):
    return [c * S for c in box]


def ell(d, box, fill, outline=INK, width=7):
    d.ellipse(u(box), fill=fill, outline=outline, width=width)


def poly(d, pts, fill, outline=INK, width=7):
    d.polygon([(x * S, y * S) for x, y in pts], fill=fill, outline=outline)
    pp = pts + [pts[0]]
    for a, b in zip(pp, pp[1:]):
        d.line(u([a[0], a[1], b[0], b[1]]), fill=outline, width=width)


def rrect(d, box, rad, fill, outline=INK, width=7):
    d.rounded_rectangle(u(box), radius=rad * S, fill=fill, outline=outline, width=width)


def line(d, pts, fill=INK, width=7):
    d.line([(x * S, y * S) for x, y in pts], fill=fill, width=width, joint="curve")


def opoly(d, pts, width=7):
    pp = pts + [pts[0]]
    for a, b in zip(pp, pp[1:]):
        d.line(u([a[0], a[1], b[0], b[1]]), fill=INK, width=width)


def orrect(d, box, rad, width=7):
    d.rounded_rectangle(u(box), radius=rad * S, fill=None, outline=INK, width=width)


def oell(d, box, width=7):
    d.ellipse(u(box), fill=None, outline=INK, width=width)


def spiral_texture(wu, hu, seeds):
    """Tie-dye as SPIRAL arms (v3 art: pink/blue/purple spirals), not
    concentric rings. Mottled wash underneath, then Archimedean spiral
    strokes in alternating colours, slight blur so it reads as fabric."""
    W, H = int(wu * S), int(hu * S)
    tex = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    td = ImageDraw.Draw(tex)
    rnd = random.Random(11)
    for _ in range(60):
        x = rnd.uniform(-0.2, wu + 0.2)
        y = rnd.uniform(-0.2, hu + 0.2)
        r = rnd.uniform(0.25, 0.7)
        c = rnd.choice([PINK, BLUE, PURPLE, (140, 220, 240, 255)])
        td.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=c)
    tex = tex.filter(ImageFilter.GaussianBlur(14))
    td = ImageDraw.Draw(tex)
    cols = [PINK, BLUE, PURPLE, WHITE]
    for (cx, cy, rmax) in seeds:
        for k, col in enumerate(cols):
            # one spiral arm per colour, offset in phase
            pts = []
            phase = k * 1.7
            th = 0.0
            while th < 4.6:
                r = 0.06 + 0.11 * th
                if r > rmax:
                    break
                a = th + phase
                pts.append(((cx + r * math.cos(a)) * S, (cy + r * math.sin(a)) * S))
                th += 0.12
            if len(pts) > 2:
                td.line(pts, fill=col, width=26, joint="curve")
    tex = tex.filter(ImageFilter.GaussianBlur(4))
    return tex


def tie_part(wu, hu, silhouette, outline, seeds):
    tex = spiral_texture(wu, hu, seeds)
    mask = Image.new("L", (int(wu * S), int(hu * S)), 0)
    md = ImageDraw.Draw(mask)
    silhouette(md)
    im = Image.new("RGBA", (int(wu * S), int(hu * S)), (0, 0, 0, 0))
    im.paste(tex, (0, 0), mask)
    d = ImageDraw.Draw(im)
    if outline is None:
        # outline = dilated mask minus mask, in INK — follows the true edge
        dil = mask.filter(ImageFilter.MaxFilter(7))
        edge = Image.new("RGBA", mask.size, (0, 0, 0, 0))
        ed = Image.new("L", mask.size, 0)
        ed.paste(255, (0, 0), dil)
        import numpy as _np
        m = _np.array(mask, dtype=int)
        dl = _np.array(dil, dtype=int)
        rim = ((dl > 0) & (m == 0)).astype('uint8') * 255
        edge.paste(INK, (0, 0), Image.fromarray(rim))
        im.paste(edge, (0, 0), edge)
    else:
        outline(d)
    return im


# ---- HEAD: big, wide jaw, big blue eyes, detailed horseshoe --------------
im, d = canvas(4.6, 3.6)
# long wavy side hair, to the shoulders (behind the face)
poly(d, [(0.10, 0.45), (1.05, 0.45), (1.25, 1.30), (1.08, 2.10), (0.95, 2.90),
         (0.70, 3.35), (0.35, 3.10), (0.12, 2.10), (0.10, 1.05)], BLOND)
poly(d, [(4.50, 0.45), (3.55, 0.45), (3.35, 1.30), (3.52, 2.10), (3.65, 2.90),
         (3.90, 3.35), (4.25, 3.10), (4.48, 2.10), (4.50, 1.05)], BLOND)
line(d, [(0.55, 0.90), (0.48, 1.80), (0.58, 2.80)], BLOND_D, 6)
line(d, [(4.05, 0.90), (4.12, 1.80), (4.02, 2.80)], BLOND_D, 6)
# ears
ell(d, [0.28, 1.30, 0.72, 2.05], SKIN)
ell(d, [3.88, 1.30, 4.32, 2.05], SKIN)
# face: ONE clean outline — wide cranium, broad strong jaw, flat chin
face_pts = []
for k in range(13):
    a = math.pi * (1 - k / 12)
    face_pts.append((2.30 + 1.72 * math.cos(a), 1.35 - 1.12 * math.sin(a)))
face_pts += [(4.00, 1.95), (3.82, 2.62), (3.42, 3.02)]
for k in range(1, 12):
    a = math.pi * (k / 12)
    face_pts.append((2.30 + 1.12 * math.cos(a), 2.98 + 0.28 * math.sin(a)))
face_pts += [(1.18, 3.02), (0.78, 2.62), (0.60, 1.95), (0.58, 1.35)]
poly(d, face_pts, SKIN)
# jaw shading + cheek lines
d.arc(u([1.05, 2.45, 1.75, 3.05]), 10, 120, fill=SKIN_D, width=6)
d.arc(u([2.85, 2.45, 3.55, 3.05]), 60, 170, fill=SKIN_D, width=6)
# thick blond brows, angled down toward the nose (determined, not angry)
poly(d, [(1.18, 1.28), (1.92, 1.08), (1.98, 1.32), (1.24, 1.50)], BLOND)
poly(d, [(2.68, 1.08), (3.42, 1.28), (3.36, 1.50), (2.62, 1.32)], BLOND)
# (eyes are separate swap planes — Eye_Open / Eye_Happy — so the rig can
# blink and wink; they sit at head-canvas y 1.42-1.92, x centres 1.55/3.05)
# broad nose
ell(d, [2.08, 1.85, 2.52, 2.30], SKIN)
d.arc(u([2.12, 2.10, 2.48, 2.42]), 20, 160, fill=INK, width=5)
# HORSESHOE mustache: thick top bar + two bars down past the mouth,
# with vertical ridge detail (v3 art) and sideburns meeting the hair
rrect(d, [1.28, 2.28, 3.32, 2.56], 0.13, BLOND)
poly(d, [(1.26, 2.28), (1.68, 2.28), (1.78, 3.12), (1.34, 3.12)], BLOND)
poly(d, [(2.92, 2.28), (3.34, 2.28), (3.26, 3.12), (2.82, 3.12)], BLOND)
for x in (1.48, 1.58, 3.02, 3.12):
    line(d, [(x, 2.34), (x + 0.02, 3.02)], BLOND_D, 5)
# (mouth is a separate swap plane — Mouth_* — so the rig can talk;
# it sits between the mustache bars at head-canvas y ~2.62-2.92)
# chin line
d.arc(u([1.95, 3.02, 2.65, 3.38]), 20, 160, fill=INK, width=6)
save("Head_Front.png", im)

# ---- HAIR BACK: long blond, wavy, to mid-back ----------------------------
im, d = canvas(4.6, 4.6)
poly(d, [(0.85, 0.05), (3.75, 0.05), (4.15, 1.30), (3.95, 3.60), (3.55, 4.45),
         (2.95, 3.95), (2.30, 4.50), (1.65, 3.95), (1.05, 4.45), (0.65, 3.60),
         (0.45, 1.30)], BLOND)
line(d, [(1.55, 0.70), (1.45, 2.30), (1.60, 3.90)], BLOND_D, 6)
line(d, [(2.30, 0.70), (2.30, 2.50), (2.20, 4.10)], BLOND_D, 6)
line(d, [(3.05, 0.70), (3.15, 2.30), (3.00, 3.90)], BLOND_D, 6)
save("Hair_Back.png", im)

# ---- BANDANA cap + tails ----------------------------------------------------
def bandana(color, name):
    im, d = canvas(4.6, 1.7)
    ell(d, [0.60, 0.02, 4.00, 0.95], color)
    poly(d, [(0.45, 1.05), (0.60, 0.30), (2.30, 0.02), (4.00, 0.30),
             (4.15, 1.05), (3.60, 0.78), (2.30, 0.62), (1.00, 0.78)], color)
    ell(d, [3.95, 0.45, 4.35, 0.85], color)  # knot bump
    save(name, im)
    im2, d2 = canvas(1.3, 2.4)
    poly(d2, [(0.35, 0.05), (0.95, 0.05), (1.15, 1.20), (0.82, 2.30), (0.50, 1.15)], color)
    poly(d2, [(0.12, 0.10), (0.60, 0.02), (0.98, 0.95), (0.60, 1.90), (0.22, 0.90)], color)
    save(name.replace("Bandana_", "BandanaTails_"), im2)

bandana(PINK, "Bandana_Pink.png")
bandana(BLUE, "Bandana_Blue.png")

# ---- EYES (bigger) ----------------------------------------------------------
im, d = canvas(0.72, 0.50)
ell(d, [0.02, 0.04, 0.70, 0.46], WHITE)
ell(d, [0.26, 0.08, 0.48, 0.42], EYE_BLUE, outline=INK, width=4)
ell(d, [0.31, 0.15, 0.43, 0.35], DARK, outline=DARK, width=1)
save("Eye_Open.png", im)

im, d = canvas(0.72, 0.50)
d.arc(u([0.08, 0.04, 0.64, 0.46]), 200, 340, fill=INK, width=9)
save("Eye_Happy.png", im)

# ---- MOUTHS (6, bigger) -----------------------------------------------------
def mouth_canvas(wu=1.5, hu=0.8):
    return canvas(wu, hu)

im, d = mouth_canvas()
d.arc(u([0.40, 0.12, 1.10, 0.62]), 15, 165, fill=INK, width=9)
save("Mouth_Closed.png", im)

im, d = mouth_canvas()
pts = [(0.20, 0.16), (1.30, 0.16)]
for k in range(21):
    a = math.pi * (1 - k / 20)
    pts.append((0.75 + 0.55 * math.cos(a), 0.16 + 0.44 * math.sin(a)))
poly(d, pts, WHITE)
save("Mouth_Smile.png", im)

im, d = mouth_canvas()
poly(d, [(0.16, 0.12), (1.34, 0.12), (1.22, 0.52), (0.75, 0.72), (0.28, 0.52)], WHITE)
d.arc(u([0.16, 0.06, 1.34, 0.62]), 0, 180, fill=INK, width=8)
save("Mouth_Grin.png", im)

im, d = mouth_canvas()
ell(d, [0.34, 0.06, 1.16, 0.74], DARK)
ell(d, [0.48, 0.44, 1.02, 0.70], TONGUE, outline=INK, width=5)
save("Mouth_Open.png", im)

im, d = canvas(1.6, 1.05)
ell(d, [0.14, 0.05, 1.46, 1.00], DARK)
poly(d, [(0.26, 0.12), (1.34, 0.12), (1.26, 0.36), (0.34, 0.36)], WHITE)
ell(d, [0.44, 0.62, 1.16, 0.95], TONGUE, outline=INK, width=5)
save("Mouth_Shout.png", im)

im, d = mouth_canvas()
d.arc(u([0.40, 0.16, 1.10, 0.68]), 195, 345, fill=INK, width=9)
save("Mouth_Frown.png", im)

# ---- NECK (thicker) ---------------------------------------------------------
im, d = canvas(1.5, 1.7)
rrect(d, [0.10, 0.0, 1.40, 1.65], 0.22, SKIN)
save("Neck.png", im)

# ---- TORSO: wide, muscular, big comic letters ------------------------------
im, d = canvas(6.6, 4.6)
poly(d, [(0.55, 0.55), (1.45, 0.10), (2.45, 0.08), (3.30, 0.95), (4.15, 0.08),
         (5.15, 0.10), (6.05, 0.55), (6.25, 1.35), (5.85, 4.30), (0.75, 4.30),
         (0.35, 1.35)], BLUE)
# scoop neckline
d.ellipse(u([2.30, -0.60, 4.30, 1.10]), fill=SKIN, outline=INK, width=14)
# pecs + abs shading
d.arc(u([1.05, 2.60, 3.05, 3.45]), 200, 340, fill=INK, width=6)
d.arc(u([3.55, 2.60, 5.55, 3.45]), 200, 340, fill=INK, width=6)
d.arc(u([1.00, 3.70, 5.60, 4.30]), 200, 340, fill=INK, width=6)
line(d, [(3.30, 1.10), (3.30, 2.45)], (20, 90, 140, 255), 6)
# BROTHERMAN — big comic pink letters, dark outline, starburst ticks
txt = Image.new("RGBA", (int(6.6 * S), int(4.6 * S)), (0, 0, 0, 0))
td = ImageDraw.Draw(txt)
font = ImageFont.truetype(FONT, 245)
td.text((3.30 * S, 1.95 * S), "BROTHERMAN", font=font, fill=PINK,
        anchor="mm", stroke_width=9, stroke_fill=PURPLE_D)
im = Image.alpha_composite(im, txt)
d = ImageDraw.Draw(im)
for sx in (0.55, 6.05):
    for dx, dy in [(-0.12, -0.10), (0.0, -0.16), (0.12, -0.10)]:
        line(d, [(sx, 1.95), (sx + dx, 1.95 + dy)], PURPLE_D, 5)
save("Torso.png", im)

# ---- TORSO BACK (no letters, shoulder-blade shading) ------------------------
im, d = canvas(6.6, 4.6)
poly(d, [(0.55, 0.55), (1.45, 0.10), (2.45, 0.08), (3.30, 0.95), (4.15, 0.08),
         (5.15, 0.10), (6.05, 0.55), (6.25, 1.35), (5.85, 4.30), (0.75, 4.30),
         (0.35, 1.35)], BLUE)
d.arc(u([2.30, -0.60, 4.30, 1.10]), 0, 180, fill=(255, 255, 255, 255), width=16)
d.arc(u([1.30, 1.60, 3.00, 2.60]), 200, 340, fill=(20, 90, 140, 255), width=6)
d.arc(u([3.60, 1.60, 5.30, 2.60]), 200, 340, fill=(20, 90, 140, 255), width=6)
line(d, [(3.30, 1.10), (3.30, 3.90)], (20, 90, 140, 255), 6)
save("Torso_Back.png", im)

# ---- PELVIS: spiral tie-dye + CHAMPIONSHIP belt, oval gold buckle ----------
def pelvis_sil(md):
    md.polygon([(0.40 * S, 0.60 * S), (4.60 * S, 0.60 * S), (4.78 * S, 1.50 * S),
                (3.85 * S, 1.62 * S), (3.10 * S, 2.02 * S), (2.50 * S, 2.02 * S),
                (1.90 * S, 2.02 * S), (1.15 * S, 1.62 * S), (0.22 * S, 1.50 * S)],
               fill=255)
def pelvis_out(d):
    opoly(d, [(0.40, 0.60), (4.60, 0.60), (4.78, 1.50), (3.85, 1.62), (3.10, 2.02),
              (2.50, 2.02), (1.90, 2.02), (1.15, 1.62), (0.22, 1.50)])
im = tie_part(5.0, 2.1, pelvis_sil, pelvis_out, [(1.3, 1.1, 1.4), (3.7, 1.2, 1.3)])
d = ImageDraw.Draw(im)
rrect(d, [0.34, 0.08, 4.66, 0.62], 0.14, BLACK)
ell(d, [2.02, 0.06, 2.98, 0.64], GOLD)
ell(d, [2.18, 0.16, 2.82, 0.54], BLACK, outline=GOLD, width=5)
rrect(d, [0.70, 0.18, 1.05, 0.52], 0.06, GOLD)
rrect(d, [3.95, 0.18, 4.30, 0.52], 0.06, GOLD)
line(d, [(2.50, 0.62), (2.50, 2.02)], INK, 6)
save("Pelvis.png", im)

# ---- UPPER ARM: thick, bicep bulge, SOCKET notch at the elbow --------------
# Socket = concave semicircle cut into the bottom edge (ball lives on the
# forearm). No cap, no disc — the V3 socket-cut rule.
im, d = canvas(2.0, 3.0)
ell(d, [0.15, 0.02, 1.85, 1.55], SKIN)                       # deltoid
poly(d, [(0.22, 0.90), (1.78, 0.90), (1.72, 2.35), (1.65, 2.55)], SKIN)
ell(d, [1.05, 1.45, 1.85, 2.55], SKIN)                       # bicep bulge
# socket notch: arc from (0.35,2.55) up through (1.0,2.15) to (1.65,2.55)
pts = [(0.22, 0.90), (0.22, 2.35), (0.35, 2.55)]
for k in range(11, 0, -1):
    a = math.pi * (k / 12)
    pts.append((1.00 + 0.65 * math.cos(a), 2.55 - 0.32 * math.sin(a)))
pts += [(1.65, 2.55), (1.72, 2.35), (1.78, 0.90)]
poly(d, pts, SKIN)
save("UpperArm_R.png", im)
flip("UpperArm_R.png", "UpperArm_L.png")

# ---- FOREARM: BALL at the elbow, thick, white wristband --------------------
im, d = canvas(1.7, 3.0)
ell(d, [0.15, -0.10, 1.55, 0.90], SKIN)                      # elbow BALL
rrect(d, [0.22, 0.35, 1.48, 2.20], 0.32, SKIN)               # forearm
rrect(d, [0.16, 2.08, 1.54, 2.62], 0.10, WHITE)              # WHITE wristband
rrect(d, [0.20, 2.62, 1.50, 2.95], 0.10, SKIN)               # wrist
save("Forearm_R.png", im)
flip("Forearm_R.png", "Forearm_L.png")

# ---- THIGH: thick, spiral tie-dye, SOCKET notch at the knee ----------------
def thigh_sil(md):
    md.rounded_rectangle(u([0.25, 0.0, 1.95, 3.10]), radius=0.45 * S, fill=255)
    pts = [(0.25 * S, 3.10 * S), (0.35 * S, 3.10 * S)]
    for k in range(11, 0, -1):
        a = math.pi * (k / 12)
        pts.append(((1.10 + 0.72 * math.cos(a)) * S, (3.10 - 0.32 * math.sin(a)) * S))
    pts += [(1.85 * S, 3.10 * S), (1.95 * S, 3.10 * S)]
    md.polygon(pts, fill=255)
im = tie_part(2.2, 3.4, thigh_sil, None, [(1.10, 1.3, 1.2), (1.10, 2.7, 1.0)])
save("Thigh_R.png", im)
flip("Thigh_R.png", "Thigh_L.png")

# ---- SHIN: BALL at the knee + tall BLUE lace-up boot -----------------------
def shin_sil(md):
    md.ellipse(u([0.15, -0.10, 1.75, 0.85]), fill=255)       # knee BALL
    md.rounded_rectangle(u([0.25, 0.30, 1.65, 2.95]), radius=0.32 * S, fill=255)
    md.polygon([(0.14 * S, 2.85 * S), (1.58 * S, 2.85 * S), (1.95 * S, 4.40 * S),
                (1.95 * S, 4.80 * S), (0.10 * S, 4.80 * S), (0.10 * S, 4.40 * S)],
               fill=255)
def shin_out(d):
    oell(d, [0.15, -0.10, 1.75, 0.85])
    orrect(d, [0.25, 0.30, 1.65, 2.95], 0.32)
    opoly(d, [(0.14, 2.85), (1.58, 2.85), (1.95, 4.40), (1.95, 4.80),
              (0.10, 4.80), (0.10, 4.40)])
im = tie_part(1.9, 4.9, shin_sil, shin_out, [(0.95, 1.3, 1.1), (0.95, 2.5, 0.9)])
d = ImageDraw.Draw(im)
poly(d, [(0.10, 2.85), (1.58, 2.85), (1.80, 4.42), (1.80, 4.80),
         (0.10, 4.80), (0.10, 4.42)], BLUE)
for k in range(4):
    y0 = 3.05 + k * 0.34
    line(d, [(0.62, y0), (1.10, y0 + 0.24)], PINK, 8)
    line(d, [(1.10, y0), (0.62, y0 + 0.24)], PINK, 8)
rrect(d, [0.10, 4.72, 1.95, 4.84], 0.05, DARK)
save("Shin_R.png", im)
flip("Shin_R.png", "Shin_L.png")

# ---- HANDS: BIG, wrist at TOP, fingers DOWN --------------------------------
im, d = canvas(1.9, 1.7)
rrect(d, [0.35, 0.0, 1.55, 0.50], 0.14, SKIN)
ell(d, [0.22, 0.32, 1.68, 1.18], SKIN)
ell(d, [0.26, 1.00, 0.66, 1.45], SKIN)
ell(d, [0.66, 1.06, 1.06, 1.52], SKIN)
ell(d, [1.06, 1.00, 1.46, 1.45], SKIN)
ell(d, [1.18, 0.60, 1.68, 1.08], SKIN)                       # thumb knuckle
line(d, [(0.36, 1.06), (0.66, 1.10)], INK, 5)
line(d, [(0.74, 1.10), (1.04, 1.12)], INK, 5)
save("Hand_Fist_R.png", im)
flip("Hand_Fist_R.png", "Hand_Fist_L.png")

im, d = canvas(1.9, 1.3)
rrect(d, [0.55, 0.0, 1.35, 0.40], 0.12, SKIN)
ell(d, [0.26, 0.20, 1.64, 1.18], SKIN)
line(d, [(0.62, 0.55), (0.62, 1.02)], INK, 5)
line(d, [(0.95, 0.55), (0.95, 1.08)], INK, 5)
line(d, [(1.28, 0.55), (1.28, 1.02)], INK, 5)
d.arc(u([0.65, 0.52, 1.35, 1.10]), 200, 340, fill=INK, width=6)
save("Hand_Open_R.png", im)
flip("Hand_Open_R.png", "Hand_Open_L.png")

im, d = canvas(0.38, 1.1)
rrect(d, [0.02, 0.0, 0.36, 1.08], 0.18, SKIN)
save("Finger.png", im)

im, d = canvas(0.40, 0.95)
rrect(d, [0.02, 0.0, 0.38, 0.93], 0.19, SKIN)
save("Thumb.png", im)

im, d = canvas(1.7, 2.1)
rrect(d, [0.30, 0.0, 1.30, 0.46], 0.13, SKIN)
ell(d, [0.18, 0.30, 1.52, 1.10], SKIN)
ell(d, [0.24, 0.94, 0.60, 1.32], SKIN)
ell(d, [0.60, 1.00, 0.96, 1.38], SKIN)
ell(d, [0.96, 0.94, 1.32, 1.32], SKIN)
rrect(d, [0.62, 1.05, 1.02, 2.06], 0.18, SKIN)
save("Hand_Point_R.png", im)
flip("Hand_Point_R.png", "Hand_Point_L.png")

# ---- SHADOW ------------------------------------------------------------------
im = Image.new("RGBA", (int(5.6 * S), int(1.1 * S)), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
d.ellipse([0.1 * S, 0.1 * S, 5.5 * S, 1.0 * S], fill=(0, 0, 0, 110))
im = im.filter(ImageFilter.GaussianBlur(18))
w, h = im.size
im.resize((w // 2, h // 2), Image.LANCZOS).save(os.path.join(OUT, "Shadow.png"))
print("Shadow.png")

print("PARTS V2 DONE", sorted(os.listdir(OUT)))
