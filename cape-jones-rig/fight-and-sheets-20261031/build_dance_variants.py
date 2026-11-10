"""Dance hand-swap system: same dance base poses, swapped hand pieces.
Base = v7c rig as built (gauntlet fist in the lower piece). Variants paste a
sliced hand piece (white glove, same art family) over the fist, centred at
the estimated fist centre: elbow + rot((0,1), arm_lower) * 210 * SCALE.
No hand is drawn, no angle changed, only the hand piece at the wrist end.
X-ray skeleton hands are NOT used here — they are a specialty layer, not
normal dance hands (see hand library doc).
"""
import os, math
from PIL import Image, ImageDraw
import sys
sys.path.insert(0, os.path.dirname(__file__))
# reuse build() by importing build_fight would run its SEQ, so duplicate core here
BASE = "/home/hatch/workspace/cape-jones-rig/sliced"
CUT = "/home/hatch/workspace/cape-jones-rig/cut-limbs-v7c"
OUT = "/home/hatch/workspace/cape-jones-rig/fight-and-sheets-20261031/dance-variants"
os.makedirs(OUT, exist_ok=True)
SCALE = 0.95
SHOULDER = {"L": (430, 445), "R": (670, 445)}
HIP = {"L": (470, 740), "R": (615, 740)}
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
LEG = {"L": ((95, 314), (77, 40)), "R": ((100, 314), (84, 40))}
LEG_PIECES = {"L": ("Leg_Front_Upper.png", "Leg_Front_Lower.png", "Leg_Front_Cap.png"),
              "R": ("Leg_Back_Upper.png", "Leg_Back_Lower.png", "Leg_Back_Cap.png")}
ARM_PIECES = {"L": ("Arm_Front_Upper.png", "Arm_Front_Lower.png", "Arm_Front_Cap.png"),
              "R": ("Arm_Back_Upper.png", "Arm_Back_Lower.png", "Arm_Back_Cap.png")}

def load(p, scale=SCALE):
    im = Image.open(p).convert("RGBA")
    return im.resize((int(im.size[0] * scale), int(im.size[1] * scale)), Image.LANCZOS)
def paste_at(c, im, cx, top): c.paste(im, (int(cx - im.size[0] / 2), int(top)), im)
def limb(c, path, joint, angle, anchor):
    im = load(path); ax, ay = anchor[0] * SCALE, anchor[1] * SCALE
    layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    layer.paste(im, (int(joint[0] - ax), int(joint[1] - ay)), im)
    layer = layer.rotate(angle, center=joint, expand=False); c.alpha_composite(layer)
def cap_at(c, path, joint):
    im = load(path); c.paste(im, (int(joint[0] - im.size[0] / 2), int(joint[1] - im.size[1] / 2)), im)
def rot_vec(v, a_deg):
    a = math.radians(a_deg); x, y = v
    return (x * math.cos(a) + y * math.sin(a), -x * math.sin(a) + y * math.cos(a))

def build(cfg):
    canvas = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    paste_at(canvas, load(os.path.join(BASE, "Cape_Back_Main.png")), 550, 410)
    for side in ("L", "R"):
        hip = HIP[side]; ball, ha = LEG[side]; vec = (ball[0] - ha[0], ball[1] - ha[1])
        up, low, cap = LEG_PIECES[side]
        limb(canvas, os.path.join(CUT, up), hip, cfg["leg_upper"][side], ha)
        knee = (hip[0] + rot_vec(vec, cfg["leg_upper"][side])[0] * SCALE,
                hip[1] + rot_vec(vec, cfg["leg_upper"][side])[1] * SCALE)
        limb(canvas, os.path.join(CUT, low), knee, cfg["leg_lower"][side], (ball[0], 0))
        cap_at(canvas, os.path.join(CUT, cap), knee)
    elbows = {}
    for side in ("L", "R"):
        ball, sa = ARM[side]; vec = (ball[0] - sa[0], ball[1] - sa[1])
        up, _, _ = ARM_PIECES[side]; sh = SHOULDER[side]
        limb(canvas, os.path.join(CUT, up), sh, cfg["arm_upper"][side], sa)
        elbows[side] = (sh[0] + rot_vec(vec, cfg["arm_upper"][side])[0] * SCALE,
                        sh[1] + rot_vec(vec, cfg["arm_upper"][side])[1] * SCALE)
    paste_at(canvas, load(os.path.join(BASE, "Pelvis.png")), 550, 680)
    paste_at(canvas, load(os.path.join(BASE, "Cape_Collar.png")), 550, 370)
    paste_at(canvas, load(os.path.join(BASE, "Torso_Chest.png")), 550, 400)
    paste_at(canvas, load(os.path.join(BASE, "Belt_Overlay.png")), 550, 670)
    for side in ("L", "R"):
        _, low, cap = ARM_PIECES[side]; ball, _ = ARM[side]
        limb(canvas, os.path.join(CUT, low), elbows[side], cfg["arm_lower"][side], (ball[0], 0))
        cap_at(canvas, os.path.join(CUT, cap), elbows[side])
    paste_at(canvas, load(os.path.join(BASE, "Neck.png"), scale=1.05), 550, 360)
    paste_at(canvas, load(os.path.join(BASE, "Head_Front.png")), 550, 250)
    return canvas, elbows

POSES = [
    ("groove-a", {"arm_upper": {"L": -60, "R": 60}, "arm_lower": {"L": -60, "R": 60},
                  "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": 10, "R": -10}}),
    ("groove-b", {"arm_upper": {"L": -115, "R": 85}, "arm_lower": {"L": 65, "R": -95},
                  "leg_upper": {"L": -16, "R": 6}, "leg_lower": {"L": 32, "R": -28}}),
    ("groove-c", {"arm_upper": {"L": -25, "R": 35}, "arm_lower": {"L": -88, "R": 145},
                  "leg_upper": {"L": -20, "R": 20}, "leg_lower": {"L": 15, "R": -15}}),
]
HANDS = [("base-fist", None),
         ("open", os.path.join(BASE, "Hand_3_Open.png")),
         ("point", os.path.join(BASE, "Hand_4_Point.png")),
         ("relaxed", os.path.join(BASE, "Hand_6_Relaxed.png"))]

def fist_centre(elbow, arm_lower):
    dx, dy = rot_vec((0, 1), arm_lower)
    return (elbow[0] + dx * 210 * SCALE, elbow[1] + dy * 210 * SCALE)

for vname, hpath in HANDS:
    vframes = []
    for pname, cfg in POSES:
        plate, elbows = build(cfg)
        if hpath:
            hand = Image.open(hpath).convert("RGBA")
            hand = hand.resize((int(hand.size[0] * 1.7), int(hand.size[1] * 1.7)), Image.LANCZOS)
            for side in ("L", "R"):
                fc = fist_centre(elbows[side], cfg["arm_lower"][side])
                plate.alpha_composite(hand, (int(fc[0] - hand.size[0] / 2), int(fc[1] - hand.size[1] / 2)))
        bg = Image.new("RGBA", (1100, 1500), (128, 128, 128, 255))
        bg.alpha_composite(plate)
        img = bg.convert("RGB"); vframes.append(img)
        img.save(f"{OUT}/{vname}-{pname}-20261031.png")
    small = [f.resize((550, 750), Image.LANCZOS) for f in vframes]
    seq = []
    for f in small: seq += [f] * 4
    seq[0].save(f"{OUT}/dance-variant-{vname}-20261031.gif", save_all=True, append_images=seq[1:], duration=125, loop=0)
    print(vname, "done")

# contact: rows = variants, cols = poses
sheet = Image.new("RGB", (3 * 367, 4 * 500), (128, 128, 128)); d = ImageDraw.Draw(sheet)
for ri, (vname, _) in enumerate(HANDS):
    for ci, (pname, _) in enumerate(POSES):
        im = Image.open(f"{OUT}/{vname}-{pname}-20261031.png").resize((367, 500), Image.LANCZOS)
        sheet.paste(im, (ci * 367, ri * 500)); d.text((ci * 367 + 8, ri * 500 + 8), f"{vname} / {pname}", fill=(255, 255, 0))
sheet.save(f"{OUT}/dance-variants-contact-20261031.png")
print("contact done")
