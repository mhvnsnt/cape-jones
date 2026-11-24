#!/usr/bin/env python3
"""BROTHERMAN Rig Jones 2 — SHEET JONES v3 (from the APPROVED concept art).

Sheets first, rig from the sheets — Sheet Jones is the foundation.
- 01-turnaround: front (Blender rest render of Rig Jones 2) + back
  (assembled from the new parts) + bandana variants + the approved v3
  concept image as the reference panel it was measured from.
- 02-construction: T-pose with red construction lines, 7-head ruler,
  design notes (locked likeness, owner 2026-11-23 07:17 EST).
- 03-expressions-hands-colors: Neutral / Grin / Shout / Wink heads,
  Fist / Open / Point hands, locked palette with hex values.
The mislabeled generator turnaround in brotherman/ (a purple-cowl Cape
Jones figure, NOT Brotherman) is NOT used anywhere here.
"""
import os
from PIL import Image, ImageDraw, ImageFont

WD = os.path.dirname(os.path.abspath(__file__))
PARTS = os.path.join(WD, "parts")
OUT = os.path.join(WD, "sheets")
os.makedirs(OUT, exist_ok=True)

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
INK = (20, 20, 20, 255)
RED = (200, 30, 30, 255)
PAPER = (244, 238, 224, 255)
BLUE = (43, 143, 212, 255)
PINK = (236, 77, 140, 255)
PURPLE = (123, 75, 214, 255)
SKIN = (216, 155, 98, 255)
BLOND = (232, 194, 94, 255)
GOLD = (232, 184, 58, 255)


def fnt(size, bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def part(name):
    return Image.open(os.path.join(PARTS, name)).convert("RGBA")


def size_u(name):
    w, h = part(name).size
    return w / 200.0, h / 200.0


def assemble(scale, back=False):
    """Assemble the figure from parts in PIL. scale = px per rig unit.
    Origin: ground y=0, x=0 centre. Returns RGBA image, figure ~17 units."""
    W, H = int(9.0 * scale), int(17.6 * scale)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cx, gy = W // 2, H - int(0.3 * scale)

    def paste(name, ccx, ccy):
        p = part(name)
        w, h = p.size
        # scale part from 200px/unit to `scale` px/unit
        p2 = p.resize((int(w * scale / 200), int(h * scale / 200)), Image.LANCZOS)
        im.paste(p2, (int(cx + ccx * scale - p2.size[0] / 2),
                      int(gy - ccy * scale - p2.size[1] / 2)), p2)

    paste("Shadow.png", 0, 0.55)
    paste("Hair_Back.png", 0, 14.60)
    paste("Thigh_R.png", -1.15, 6.15)
    paste("Thigh_L.png", 1.15, 6.15)
    paste("Shin_R.png", -1.15, 2.35)
    paste("Shin_L.png", 1.15, 2.35)
    paste("Pelvis.png", 0, 8.80)
    paste("UpperArm_R.png", -2.85, 12.10)
    paste("UpperArm_L.png", 2.85, 12.10)
    paste("Forearm_R.png", -2.85, 9.75)
    paste("Forearm_L.png", 2.85, 9.75)
    paste("Torso_Back.png" if back else "Torso.png", 0, 11.60)
    if not back:
        paste("Neck.png", 0, 13.55)
        paste("Head_Front.png", 0, 15.05)
        paste("Bandana_Pink.png", 0, 16.00)
        paste("Eye_Open.png", -0.75, 15.18)
        paste("Eye_Open.png", 0.75, 15.18)
        paste("Mouth_Closed.png", 0, 14.08)
    paste("Hand_Fist_R.png", -2.85, 8.65 - size_u("Hand_Fist_R.png")[1] / 2)
    paste("Hand_Fist_L.png", 2.85, 8.65 - size_u("Hand_Fist_L.png")[1] / 2)
    return im


def header(d, W, title, sub):
    d.rectangle([0, 0, W, 92], fill=(30, 20, 60, 255))
    d.text((24, 14), title, font=fnt(44), fill=(255, 255, 255, 255))
    d.text((24, 62), sub, font=fnt(22, False), fill=(220, 200, 255, 255))


def footer(d, W, H, text):
    d.text((24, H - 34), text, font=fnt(20, False), fill=(90, 80, 70, 255))


# ---- SHEET 01: turnaround ---------------------------------------------------
W, H = 2400, 2000
sheet = Image.new("RGBA", (W, H), PAPER)
d = ImageDraw.Draw(sheet)
header(d, W, "BROTHERMAN — SHEET 01 : TURNAROUND",
       "Rig Jones 2  •  from the APPROVED v3 concept art  •  Sheet Jones v3, 2026-11-23")
front = assemble(78)
sheet.paste(front, (120, 130), front)
d.text((120, 1500), "FRONT — no bandana swap here:\nPINK bandana (first appearance)", font=fnt(26), fill=INK)
back = assemble(78, back=True)
sheet.paste(back, (760, 130), back)
d.text((760, 1500), "BACK — long blond hair to mid-back,\ntank back, no letters", font=fnt(26), fill=INK)
# approved concept reference panel
ref = Image.open(os.path.join(WD, "..", "brotherman",
      "media-generation-brotherman-v3-exact-bald-top-0-ede65965-a412-4980-9905-da0098352691.webp")).convert("RGBA")
ref.thumbnail((480, 1050))
sheet.paste(ref, (1460, 150), ref)
d.rectangle([1460, 150, 1460 + ref.size[0], 150 + ref.size[1]], outline=INK, width=4)
d.text((1460, 1230), "APPROVED CONCEPT — v3 exact bald top\n(owner: \"That's perfect, yeah\")\nsha256 8879ad70… — the art Rig Jones 2\nwas measured from. Bald top, long blond\nhair sides/back, spiral tie-dye,\nchampionship belt, blue lace-up boots.",
       font=fnt(26), fill=INK)
# bandana variants — HEAD-ONLY crops, right column under the concept text
for i, (bname, label) in enumerate([("Bandana_Pink.png", "PINK — first appearance"),
                                    ("Bandana_Blue.png", "BLUE — sometimes")]):
    hx = 1460 + i * 330
    hy = 1520
    him = Image.new("RGBA", (int(9.0 * 40), int(6.5 * 40)), (0, 0, 0, 0))
    ccx, gy = him.size[0] // 2, int(6.2 * 40)

    def _paste(nm, ccxx, ccyy):
        pp = part(nm)
        pp2 = pp.resize((int(pp.size[0] * 40 / 200), int(pp.size[1] * 40 / 200)), Image.LANCZOS)
        him.paste(pp2, (int(ccx + ccxx * 40 - pp2.size[0] / 2),
                        int(gy - (ccyy - 12.0) * 40 - pp2.size[1] / 2)), pp2)

    _paste("Hair_Back.png", 0, 14.60)
    _paste("Head_Front.png", 0, 15.05)
    _paste(bname, 0, 16.00)
    _paste("Eye_Open.png", -0.75, 15.18)
    _paste("Eye_Open.png", 0.75, 15.18)
    _paste("Mouth_Closed.png", 0, 14.08)
    him = him.crop((0, 0, him.size[0], int(6.2 * 40 - (13.0 - 12.0) * 40)))
    sheet.paste(him, (hx, hy), him)
    d.text((hx + 20, hy + 270), label, font=fnt(22), fill=INK)
d.text((1460, 1830), "NO bandana most of the time.", font=fnt(26), fill=INK)
footer(d, W, H, "BROTHERMAN — all caps, one word. 7 heads tall. Cape Jones reaches only to his chest (see v4-cape-correct).")
sheet.convert("RGB").save(os.path.join(OUT, "01-turnaround-v2.png"))
print("01-turnaround-v2.png", sheet.size)

# ---- SHEET 02: construction --------------------------------------------------
W, H = 2400, 1700
sheet = Image.new("RGBA", (W, H), PAPER)
d = ImageDraw.Draw(sheet)
header(d, W, "BROTHERMAN — SHEET 02 : CONSTRUCTION & PROPORTIONS",
       "Rig Jones 2  •  7 heads tall  •  shoulders 3 heads wide  •  locked likeness v2")
# crop the rest render to the figure itself, then scale to a fixed height
# so the 7-head ruler measures the FIGURE, not the empty frame
rest = Image.open(os.path.join(WD, "rest-v2-f0001.png")).convert("RGBA")
bbox = rest.getchannel("A").getbbox()
rest = rest.crop(bbox)
th = 1250
rest = rest.resize((int(rest.size[0] * th / rest.size[1]), th), Image.LANCZOS)
sheet.paste(rest, (200, 180), rest)
# red construction lines + head ruler: one head = figure height / 7
x0, y0 = 200, 180
fw, fh = rest.size
head = fh / 7.0
for k in range(8):
    y = int(y0 + k * head)
    d.line([(x0 - 80, y), (x0 + fw + 80, y)], fill=RED, width=3)
    d.text((x0 + fw + 90, y - 14), f"{k}", font=fnt(24), fill=RED)
d.text((x0 - 80, y0 - 40), "7 HEADS", font=fnt(26), fill=RED)
notes = [
    "DESIGN — LOCKED (owner 2026-11-23 07:17 EST):",
    "• Big muscular wrestler, 7 heads tall, shoulders 3 heads wide.",
    "• Head: bald on top, LONG BLOND hair at sides and back.",
    "  Strong jaw. Thick BLOND horseshoe mustache. Tanned skin.",
    "• BLUE tank #2B8FD4, BROTHERMAN in PINK #EC4D8C comic letters.",
    "• PINK + BLUE + PURPLE spiral tie-dye LONG TIGHTS.",
    "• Championship belt: black strap, big OVAL gold buckle.",
    "• White wristbands. BLUE boots, PINK laces.",
    "• Bandana: PINK first appearance, BLUE sometimes,",
    "  NO bandana most of the time. Changes only visibly.",
    "• Full-hair version ONLY for the old-him flashback gag.",
    "",
    "RIG — Gumball method:",
    "• One master symbol per view. transformationPoint at the",
    "  anatomical joint (shoulder, elbow, wrist, hip, knee, neck).",
    "• Swap = image change on ONE plane, in place — never stacked.",
    "• Socket-cut joints: ball on the lower piece, concave",
    "  socket on the upper piece. NO caps / discs / circles ever.",
    "• One hand per arm, wrist-to-wrist, fingers DOWN.",
    "• 26 bones, 44 planes. Hair + bandana tails follow-through.",
]
y = 170
for line in notes:
    d.text((1000, y), line, font=fnt(28 if line.startswith("DESIGN") or line.startswith("RIG") else 26,
           bold=line.startswith("DESIGN") or line.startswith("RIG")), fill=INK)
    y += 44
footer(d, W, H, "Rig Jones 1 (draft) was a cool first rig — saved as draft, NOT the likeness. Rig Jones 2 is drawn from the approved art.")
sheet.convert("RGB").save(os.path.join(OUT, "02-construction-v2.png"))
print("02-construction-v2.png", sheet.size)

# ---- SHEET 03: expressions / hands / colors ---------------------------------
W, H = 2400, 1700
sheet = Image.new("RGBA", (W, H), PAPER)
d = ImageDraw.Draw(sheet)
header(d, W, "BROTHERMAN — SHEET 03 : EXPRESSIONS • HANDS • COLORS",
       "Rig Jones 2  •  mouths and eyes are swap planes on one head")


def head_variant(mouth, eye, x, y, scale=52, wink=False):
    im = Image.new("RGBA", (int(9.0 * scale), int(6.0 * scale)), (0, 0, 0, 0))
    cx, gy = im.size[0] // 2, int(5.6 * scale)

    def paste(name, ccx, ccy):
        p = part(name)
        p2 = p.resize((int(p.size[0] * scale / 200), int(p.size[1] * scale / 200)), Image.LANCZOS)
        im.paste(p2, (int(cx + ccx * scale - p2.size[0] / 2),
                      int(gy - (ccy - 12.0) * scale - p2.size[1] / 2)), p2)

    paste("Hair_Back.png", 0, 14.60)
    paste("Head_Front.png", 0, 15.05)
    paste("Bandana_Pink.png", 0, 16.00)
    if wink:
        paste("Eye_Happy.png", -0.75, 15.18)
        paste("Eye_Open.png", 0.75, 15.18)
    else:
        paste(eye, -0.75, 15.18)
        paste(eye, 0.75, 15.18)
    paste(mouth, 0, 14.08)
    im = im.crop((0, 0, im.size[0], int(6.2 * scale - (13.0 - 12.0) * scale)))
    sheet.paste(im, (x, y), im)


heads = [("Mouth_Closed.png", "Eye_Open.png", "NEUTRAL", False),
         ("Mouth_Grin.png", "Eye_Open.png", "GRIN", False),
         ("Mouth_Shout.png", "Eye_Open.png", "SHOUT", False),
         ("Mouth_Smile.png", "Eye_Open.png", "WINK", True)]
for i, (m, e, label, wink) in enumerate(heads):
    x = 80 + i * 560
    head_variant(m, e, x, 130, wink=wink)
    d.text((x + 130, 560), label, font=fnt(30), fill=INK)

d.text((80, 640), "HANDS — one per arm, wrist at TOP, fingers DOWN (wrist-to-wrist):",
       font=fnt(30), fill=INK)
for i, (name, label) in enumerate([("Hand_Fist_R.png", "FIST"),
                                   ("Hand_Open_R.png", "OPEN"),
                                   ("Hand_Point_R.png", "POINT")]):
    p = part(name)
    p.thumbnail((420, 420))
    sheet.paste(p, (120 + i * 480, 700), p)
    d.text((120 + i * 480 + 120, 1130), label, font=fnt(30), fill=INK)

d.text((80, 1220), "PALETTE — LOCKED:", font=fnt(30), fill=INK)
pal = [("Skin", SKIN, "#D89B62"), ("Blond", BLOND, "#E8C25E"),
       ("Tank / boots", BLUE, "#2B8FD4"), ("Pink", PINK, "#EC4D8C"),
       ("Tie-dye purple", PURPLE, "#7B4BD6"), ("Belt gold", GOLD, "#E8B83A"),
       ("White", (255, 255, 255, 255), "#FFFFFF")]
x = 80
for label, col, hx in pal:
    c4 = col if len(col) == 4 else col + (255,)
    d.rectangle([x, 1280, x + 190, 1380], fill=c4, outline=INK, width=3)
    d.text((x, 1395), label, font=fnt(22), fill=INK)
    d.text((x, 1425), hx, font=fnt(22, False), fill=INK)
    x += 220
footer(d, W, H, "Eyes: white + blue iris + dark pupil. Mustache: thick blond horseshoe with ridge detail. No synthesized voice ever — owner records the line.")
sheet.convert("RGB").save(os.path.join(OUT, "03-expressions-hands-colors-v2.png"))
print("03-expressions-hands-colors-v2.png", sheet.size)
print("SHEETS V2 DONE")
