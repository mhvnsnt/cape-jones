#!/usr/bin/env python3
"""Draw BROTHERMAN Rig Jones 1 cutout parts with PIL — LOCKED LIKENESS v2.

Owner lock 2026-11-23 07:17 EST (PR #436): bald top, long blond hair
sides/back, blond horseshoe mustache, strong jaw, tanned skin, BLUE tank
with BROTHERMAN in pink, white wristbands, black belt + gold buckle,
pink+blue+purple tie-dye long tights, blue boots with pink laces,
PINK bandana first appearance (blue sometimes, none most of the time).

Gumball rig method (repo-documented; no .fla on this VM — see report):
layered puppet, swappable libraries, REAL elbow + knee joints with
overlap caps so joints never gap, articulating fingers + thumbs.
Every part is a transparent-alpha PNG. No photo traced.

Layout (Y up, ground 0): head top 16.85, shoulder 13.3, elbow 10.8,
wrist 8.3, hip 7.6, knee 4.3, ankle 1.5, boot bottom 0.
1 rig unit = 200 px (drawn at 400 = 2x supersample, then halved).
"""
import math
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__)) + "/parts"
os.makedirs(OUT, exist_ok=True)

SKIN = (216, 155, 98, 255)      # tanned #D89B62
BLOND = (232, 194, 94, 255)     # #E8C25E
BLUE = (43, 143, 212, 255)      # tank/boot blue #2B8FD4
PINK = (236, 77, 140, 255)      # #EC4D8C
PURPLE = (123, 75, 214, 255)    # tie-dye purple #7B4BD6
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
GOLD = (232, 184, 58, 255)
DARK = (26, 26, 26, 255)
INK = (12, 12, 12, 255)
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
    """Outline-only polygon (no fill — a transparent fill would erase)."""
    pp = pts + [pts[0]]
    for a, b in zip(pp, pp[1:]):
        d.line(u([a[0], a[1], b[0], b[1]]), fill=INK, width=width)


def orrect(d, box, rad, width=7):
    d.rounded_rectangle(u(box), radius=rad * S, fill=None, outline=INK, width=width)


def oell(d, box, width=7):
    d.ellipse(u(box), fill=None, outline=INK, width=width)


def tiedye_texture(wu, hu, seeds):
    """Pink/blue/purple tie-dye: mottled wash + small spiral centres.
    Big perfect rings read as targets; small chaotic blobs + tight
    spirals read as tie-dye at rig scale."""
    import random
    W, H = int(wu * S), int(hu * S)
    tex = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    td = ImageDraw.Draw(tex)
    rnd = random.Random(7)
    for _ in range(70):
        x = rnd.uniform(-0.2, wu + 0.2)
        y = rnd.uniform(-0.2, hu + 0.2)
        r = rnd.uniform(0.22, 0.65)
        c = rnd.choice([PINK, BLUE, PURPLE, PINK, BLUE])
        td.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=c)
    tex = tex.filter(ImageFilter.GaussianBlur(16))
    td = ImageDraw.Draw(tex)
    cols = [PINK, BLUE, PURPLE, (255, 255, 255, 255)]
    for (cx, cy, rmax) in seeds:
        r = min(rmax, 0.55)
        k = 0
        while r > 0.08:
            ox = cx + 0.03 * k
            oy = cy + 0.02 * k
            td.ellipse([(ox - r) * S, (oy - r) * S, (ox + r) * S, (oy + r) * S],
                       fill=cols[k % len(cols)])
            r -= 0.16
            k += 1
    tex = tex.filter(ImageFilter.GaussianBlur(5))
    return tex


def tie_part(wu, hu, silhouette, outline, seeds):
    """Part filled with tie-dye: silhouette(mask) + outline strokes."""
    tex = tiedye_texture(wu, hu, seeds)
    mask = Image.new("L", (int(wu * S), int(hu * S)), 0)
    md = ImageDraw.Draw(mask)
    silhouette(md)
    im = Image.new("RGBA", (int(wu * S), int(hu * S)), (0, 0, 0, 0))
    im.paste(tex, (0, 0), mask)
    d = ImageDraw.Draw(im)
    outline(d)
    return im


# ---- HEAD (bald top, blond side hair, strong jaw, horseshoe; no eyes/mouth)
im, d = canvas(4.0, 3.1)
# side hair locks, tapered (behind the face)
poly(d, [(0.30, 0.70), (0.70, 0.70), (0.80, 2.05), (0.42, 2.28), (0.16, 1.45)], BLOND)
poly(d, [(3.30, 0.70), (2.90, 0.70), (2.80, 2.05), (3.18, 2.28), (3.44, 1.45)], BLOND)
# ears
ell(d, [0.02, 1.10, 0.48, 1.78], SKIN)
ell(d, [3.12, 1.10, 3.58, 1.78], SKIN)
# face: ONE clean outline — round cranium, tapered strong jaw, round chin
face_pts = []
for k in range(13):  # top arc, left -> right over the top
    a = math.pi * (1 - k / 12)
    face_pts.append((1.80 + 1.55 * math.cos(a), 1.20 - 1.10 * math.sin(a)))
face_pts += [(3.30, 1.90), (3.02, 2.55)]
for k in range(1, 12):  # chin arc, right -> left under the bottom
    a = math.pi * (k / 12)
    face_pts.append((1.80 + 1.22 * math.cos(a), 2.55 + 0.45 * math.sin(a)))
face_pts += [(0.30, 1.90), (0.25, 1.20)]
poly(d, face_pts, SKIN)
# (no separate sideburn blocks — the mustache top bar runs edge to edge
# and meets the side hair, so nothing floats on the cheek)
# thick blond brows
line(d, [(0.80, 0.95), (1.25, 0.82), (1.65, 0.95)], BLOND, 11)
line(d, [(1.95, 0.95), (2.35, 0.82), (2.80, 0.95)], BLOND, 11)
# strong nose
ell(d, [1.58, 1.30, 2.02, 1.75], SKIN)
# BLOND HORSESHOE mustache: top bar + two bars flaring down past the mouth
rrect(d, [0.95, 1.80, 2.65, 2.04], 0.12, BLOND)
poly(d, [(0.92, 1.80), (1.28, 1.80), (1.36, 2.68), (0.98, 2.68)], BLOND)
poly(d, [(2.32, 1.80), (2.68, 1.80), (2.62, 2.68), (2.24, 2.68)], BLOND)
# chin line
d.arc(u([1.45, 2.55, 2.15, 2.95]), 20, 160, fill=INK, width=6)
save("Head_Front.png", im)

# ---- HAIR BACK (long blond hair, separate plane for follow-through) -------
im, d = canvas(4.0, 4.2)
poly(d, [(0.55, 0.05), (3.45, 0.05), (3.75, 1.20), (3.55, 3.55), (3.10, 4.10),
         (2.45, 3.70), (1.80, 4.15), (1.15, 3.70), (0.50, 4.10), (0.25, 3.55),
         (0.45, 1.20)], BLOND)
line(d, [(1.30, 0.60), (1.20, 2.20), (1.35, 3.60)], (190, 150, 60, 255), 6)
line(d, [(2.00, 0.60), (2.00, 2.40), (1.90, 3.80)], (190, 150, 60, 255), 6)
line(d, [(2.70, 0.60), (2.80, 2.20), (2.65, 3.60)], (190, 150, 60, 255), 6)
save("Hair_Back.png", im)

# ---- BANDANA cap + tails (swaps: pink default, blue sometimes) ------------
def bandana(color, name):
    im, d = canvas(4.0, 1.6)
    poly(d, [(0.30, 0.95), (0.42, 0.28), (1.80, 0.02), (3.18, 0.28),
             (3.30, 0.95), (2.85, 0.60), (1.80, 0.46), (0.75, 0.60)], color)
    ell(d, [3.12, 0.42, 3.48, 0.80], color)  # knot bump
    save(name, im)
    # tails: separate plane, swings on its own bone
    im2, d2 = canvas(1.2, 2.2)
    poly(d2, [(0.30, 0.05), (0.85, 0.05), (1.05, 1.10), (0.75, 2.10), (0.45, 1.05)], color)
    poly(d2, [(0.10, 0.10), (0.55, 0.02), (0.90, 0.90), (0.55, 1.75), (0.20, 0.85)], color)
    save(name.replace("Bandana_", "BandanaTails_"), im2)

bandana(PINK, "Bandana_Pink.png")
bandana(BLUE, "Bandana_Blue.png")

# ---- EYES ------------------------------------------------------------------
im, d = canvas(0.72, 0.46)
ell(d, [0.02, 0.05, 0.70, 0.41], WHITE)
ell(d, [0.27, 0.09, 0.45, 0.37], DARK, outline=DARK, width=1)
save("Eye_Open.png", im)

im, d = canvas(0.72, 0.46)
d.arc(u([0.08, 0.05, 0.64, 0.42]), 200, 340, fill=INK, width=8)
save("Eye_Happy.png", im)

# ---- MOUTHS (6) ------------------------------------------------------------
def mouth_canvas(wu=1.3, hu=0.7):
    return canvas(wu, hu)

im, d = mouth_canvas()
d.arc(u([0.35, 0.10, 0.95, 0.55]), 15, 165, fill=INK, width=8)
save("Mouth_Closed.png", im)

im, d = mouth_canvas()
pts = [(0.18, 0.14), (1.12, 0.14)]
for k in range(21):
    a = math.pi * (1 - k / 20)
    pts.append((0.65 + 0.47 * math.cos(a), 0.14 + 0.38 * math.sin(a)))
poly(d, pts, WHITE)
save("Mouth_Smile.png", im)

im, d = mouth_canvas()
poly(d, [(0.15, 0.10), (1.15, 0.10), (1.05, 0.45), (0.55, 0.62), (0.25, 0.45)], WHITE)
d.arc(u([0.15, 0.05, 1.15, 0.55]), 0, 180, fill=INK, width=7)
save("Mouth_Grin.png", im)

im, d = mouth_canvas()
ell(d, [0.30, 0.06, 1.00, 0.64], DARK)
ell(d, [0.42, 0.38, 0.88, 0.60], TONGUE, outline=INK, width=5)
save("Mouth_Open.png", im)

im, d = canvas(1.4, 0.95)
ell(d, [0.12, 0.05, 1.28, 0.90], DARK)
poly(d, [(0.22, 0.10), (1.18, 0.10), (1.10, 0.32), (0.30, 0.32)], WHITE)
ell(d, [0.38, 0.55, 1.02, 0.85], TONGUE, outline=INK, width=5)
save("Mouth_Shout.png", im)

im, d = mouth_canvas()
d.arc(u([0.35, 0.15, 0.95, 0.60]), 195, 345, fill=INK, width=8)
save("Mouth_Frown.png", im)

# ---- NECK ------------------------------------------------------------------
im, d = canvas(1.1, 1.7)
rrect(d, [0.08, 0.0, 1.02, 1.65], 0.18, SKIN)
save("Neck.png", im)

# ---- TORSO: BLUE tank, BROTHERMAN in pink ----------------------------------
im, d = canvas(5.8, 4.4)
poly(d, [(0.45, 0.55), (1.25, 0.12), (2.10, 0.10), (2.90, 0.95), (3.70, 0.10),
         (4.55, 0.12), (5.35, 0.55), (5.50, 1.30), (5.15, 4.15), (0.65, 4.15),
         (0.30, 1.30)], BLUE)
d.arc(u([1.95, -0.55, 3.85, 1.05]), 0, 180, fill=(255, 255, 255, 255), width=14)
# BROTHERMAN in pink comic letters across the chest
txt = Image.new("RGBA", (int(5.8 * S), int(4.4 * S)), (0, 0, 0, 0))
td = ImageDraw.Draw(txt)
font = ImageFont.truetype(FONT, 175)
td.text((2.90 * S, 1.85 * S), "BROTHERMAN", font=font, fill=PINK,
        anchor="mm", stroke_width=7, stroke_fill=INK)
im = Image.alpha_composite(im, txt)
d = ImageDraw.Draw(im)
d.arc(u([0.90, 2.55, 2.60, 3.30]), 200, 340, fill=INK, width=6)
d.arc(u([3.20, 2.55, 4.90, 3.30]), 200, 340, fill=INK, width=6)
d.arc(u([0.80, 3.55, 5.00, 4.10]), 200, 340, fill=INK, width=6)
save("Torso.png", im)

# ---- PELVIS: tie-dye tights + black belt, gold buckle ----------------------
def pelvis_sil(md):
    md.polygon([(0.35 * S, 0.55 * S), (4.25 * S, 0.55 * S), (4.42 * S, 1.45 * S),
                (3.55 * S, 1.55 * S), (2.85 * S, 1.92 * S), (2.30 * S, 1.92 * S),
                (1.75 * S, 1.92 * S), (1.05 * S, 1.55 * S), (0.18 * S, 1.45 * S)],
               fill=255)
def pelvis_out(d):
    opoly(d, [(0.35, 0.55), (4.25, 0.55), (4.42, 1.45), (3.55, 1.55), (2.85, 1.92),
              (2.30, 1.92), (1.75, 1.92), (1.05, 1.55), (0.18, 1.45)])
im = tie_part(4.6, 2.0, pelvis_sil, pelvis_out, [(1.2, 1.0, 1.3), (3.4, 1.1, 1.2)])
d = ImageDraw.Draw(im)
rrect(d, [0.30, 0.10, 4.30, 0.56], 0.12, BLACK)
rrect(d, [1.95, 0.12, 2.65, 0.54], 0.08, GOLD)
d.polygon([(2.30 * S, 0.18 * S), (2.38 * S, 0.34 * S), (2.55 * S, 0.34 * S),
           (2.42 * S, 0.44 * S), (2.47 * S, 0.50 * S), (2.30 * S, 0.40 * S),
           (2.13 * S, 0.50 * S), (2.18 * S, 0.44 * S), (2.05 * S, 0.34 * S),
           (2.22 * S, 0.34 * S)], fill=INK)
line(d, [(2.30, 0.56), (2.30, 1.92)], INK, 6)
save("Pelvis.png", im)

# ---- UPPER ARM (shoulder -> elbow) + FOREARM (elbow -> wrist) --------------
# Elbow overlap caps on BOTH pieces so the joint never gaps when bent.
im, d = canvas(1.7, 2.9)
ell(d, [0.12, 0.02, 1.58, 1.35], SKIN)                       # deltoid
rrect(d, [0.18, 0.85, 1.52, 2.35], 0.35, SKIN)               # upper arm
ell(d, [0.95, 1.45, 1.55, 2.45], SKIN)                       # bicep bulge R
ell(d, [0.15, 2.05, 1.55, 3.05], SKIN)                       # elbow cap (overlap)
save("UpperArm_R.png", im)
flip("UpperArm_R.png", "UpperArm_L.png")

im, d = canvas(1.5, 2.9)
ell(d, [0.05, -0.15, 1.45, 0.85], SKIN)                      # elbow cap (overlap)
rrect(d, [0.18, 0.30, 1.32, 2.15], 0.30, SKIN)               # forearm
rrect(d, [0.14, 2.02, 1.36, 2.52], 0.10, WHITE)              # WHITE wristband
rrect(d, [0.18, 2.52, 1.32, 2.88], 0.10, SKIN)               # wrist
save("Forearm_R.png", im)
flip("Forearm_R.png", "Forearm_L.png")

# ---- THIGH (hip -> knee) + SHIN (knee -> ankle) + BOOT ----------------------
def thigh_sil(md):
    md.rounded_rectangle(u([0.22, 0.0, 1.68, 3.30]), radius=0.40 * S, fill=255)
    md.ellipse(u([0.15, 2.85, 1.75, 3.70]), fill=255)        # knee cap
def thigh_out(d):
    orrect(d, [0.22, 0.0, 1.68, 3.30], 0.40)
    oell(d, [0.15, 2.85, 1.75, 3.70])
im = tie_part(1.9, 3.7, thigh_sil, thigh_out, [(0.95, 1.2, 1.1), (0.95, 2.8, 0.9)])
save("Thigh_R.png", im)
flip("Thigh_R.png", "Thigh_L.png")

def shin_sil(md):
    md.rounded_rectangle(u([0.22, 0.0, 1.48, 2.90]), radius=0.30 * S, fill=255)
    md.polygon([(0.12 * S, 2.80 * S), (1.42 * S, 2.80 * S), (1.78 * S, 4.28 * S),
                (1.78 * S, 4.65 * S), (0.08 * S, 4.65 * S), (0.08 * S, 4.35 * S)],
               fill=255)
def shin_out(d):
    orrect(d, [0.22, 0.0, 1.48, 2.90], 0.30)
    opoly(d, [(0.12, 2.80), (1.42, 2.80), (1.78, 4.28), (1.78, 4.65),
              (0.08, 4.65), (0.08, 4.35)])
im = tie_part(1.7, 4.7, shin_sil, shin_out, [(0.85, 1.2, 1.0), (0.85, 2.4, 0.8)])
d = ImageDraw.Draw(im)
# BLUE boot with PINK laces over the tie-dye below the ankle
poly(d, [(0.12, 2.80), (1.42, 2.80), (1.62, 4.35), (1.62, 4.65),
         (0.08, 4.65), (0.08, 4.35)], BLUE)
for k in range(4):
    y0 = 3.00 + k * 0.32
    line(d, [(0.55, y0), (1.00, y0 + 0.22)], PINK, 7)
    line(d, [(1.00, y0), (0.55, y0 + 0.22)], PINK, 7)
rrect(d, [0.08, 4.58, 1.78, 4.68], 0.05, DARK)
save("Shin_R.png", im)
flip("Shin_R.png", "Shin_L.png")

# ---- HANDS: wrist at TOP, fingers point DOWN (wrist-to-wrist) ---------------
im, d = canvas(1.5, 1.5)
rrect(d, [0.28, 0.0, 1.22, 0.45], 0.12, SKIN)
ell(d, [0.18, 0.30, 1.32, 1.05], SKIN)
ell(d, [0.22, 0.90, 0.55, 1.28], SKIN)
ell(d, [0.55, 0.95, 0.88, 1.33], SKIN)
ell(d, [0.88, 0.90, 1.20, 1.28], SKIN)
ell(d, [0.95, 0.55, 1.32, 0.95], SKIN)
line(d, [(0.30, 0.95), (0.55, 0.98)], INK, 5)
line(d, [(0.62, 1.00), (0.85, 1.02)], INK, 5)
save("Hand_Fist_R.png", im)
flip("Hand_Fist_R.png", "Hand_Fist_L.png")

im, d = canvas(1.6, 1.1)
rrect(d, [0.45, 0.0, 1.15, 0.35], 0.10, SKIN)
ell(d, [0.22, 0.18, 1.38, 1.02], SKIN)
d.arc(u([0.55, 0.45, 1.15, 0.95]), 200, 340, fill=INK, width=5)
save("Hand_Open_R.png", im)
flip("Hand_Open_R.png", "Hand_Open_L.png")

# Finger + thumb capsules (articulate on their own bones)
im, d = canvas(0.34, 1.0)
rrect(d, [0.02, 0.0, 0.32, 0.98], 0.16, SKIN)
save("Finger.png", im)

im, d = canvas(0.36, 0.85)
rrect(d, [0.02, 0.0, 0.34, 0.83], 0.17, SKIN)
save("Thumb.png", im)

# Point 1.4 x 1.9 (fist + index finger down)
im, d = canvas(1.4, 1.9)
rrect(d, [0.25, 0.0, 1.05, 0.42], 0.12, SKIN)
ell(d, [0.15, 0.28, 1.25, 1.00], SKIN)
ell(d, [0.20, 0.85, 0.50, 1.20], SKIN)
ell(d, [0.50, 0.90, 0.80, 1.25], SKIN)
ell(d, [0.80, 0.85, 1.10, 1.20], SKIN)
rrect(d, [0.52, 0.95, 0.86, 1.88], 0.16, SKIN)
save("Hand_Point_R.png", im)
flip("Hand_Point_R.png", "Hand_Point_L.png")

# ---- SHADOW ---------------------------------------------------------------
im = Image.new("RGBA", (int(5.2 * S), int(1.1 * S)), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
d.ellipse([0.1 * S, 0.1 * S, 5.1 * S, 1.0 * S], fill=(0, 0, 0, 110))
im = im.filter(ImageFilter.GaussianBlur(18))
w, h = im.size
im.resize((w // 2, h // 2), Image.LANCZOS).save(os.path.join(OUT, "Shadow.png"))
print("Shadow.png")

print("PARTS DONE", sorted(os.listdir(OUT)))
