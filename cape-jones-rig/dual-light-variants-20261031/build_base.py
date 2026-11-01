#!/usr/bin/env python3
"""Rebuild arms-up reference pose (FlexOut lowers) on a TRANSPARENT canvas.
Replicates joint_locked_rig_v7c.py build() exactly (anchors, SCALE 0.95,
upper -70/70, lower 150/-150, legs -15/15), labels=False, no grey bg.
Output: base-arms-up-transparent-20261031.png (1100x1500 RGBA)."""
from PIL import Image
import os, math
R = "/home/hatch/workspace/cape-jones-rig"
BASE = os.path.join(R, "sliced"); CUT = os.path.join(R, "cut-limbs-v7c")
FLEX = os.path.join(R, "cut-limbs-v7c-flex-out")
OUT = os.path.join(R, "dual-light-variants-20261031")
os.makedirs(OUT, exist_ok=True)
SCALE = 0.95
SHOULDER = {"L": (430, 445), "R": (670, 445)}; HIP = {"L": (470, 740), "R": (615, 740)}
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
LEG = {"L": ((95, 314), (77, 40)), "R": ((100, 314), (84, 40))}
LEG_PIECES = {"L": ("Leg_Front_Upper.png", "Leg_Front_Lower.png", "Leg_Front_Cap.png"),
              "R": ("Leg_Back_Upper.png", "Leg_Back_Lower.png", "Leg_Back_Cap.png")}
ARM_PIECES = {"L": ("Arm_Front_Upper.png", "Arm_Front_Lower.png", "Arm_Front_Cap.png"),
              "R": ("Arm_Back_Upper.png", "Arm_Back_Lower.png", "Arm_Back_Cap.png")}
FLEX_LOWER = {"L": "Arm_Front_Lower_FlexOut.png", "R": "Arm_Back_Lower_FlexOut.png"}
CFG = {"arm_upper": {"L": -70, "R": 70}, "arm_lower": {"L": 150, "R": -150},
       "leg_upper": {"L": -15, "R": 15}, "leg_lower": {"L": -15, "R": 15}}

def load(p, scale=SCALE):
    im = Image.open(p).convert("RGBA")
    return im.resize((int(im.size[0] * scale), int(im.size[1] * scale)), Image.LANCZOS)
def paste_at(c, im, cx, top):
    c.paste(im, (int(cx - im.size[0] / 2), int(top)), im)
def limb(c, path, joint, angle, anchor):
    im = load(path); ax, ay = anchor[0] * SCALE, anchor[1] * SCALE
    layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    layer.paste(im, (int(joint[0] - ax), int(joint[1] - ay)), im)
    layer = layer.rotate(angle, center=joint, expand=False)
    c.alpha_composite(layer)
def cap_at(c, path, joint):
    im = load(path)
    c.paste(im, (int(joint[0] - im.size[0] / 2), int(joint[1] - im.size[1] / 2)), im)
def rot_vec(v, a_deg):
    a = math.radians(a_deg); x, y = v
    return (x * math.cos(a) + y * math.sin(a), -x * math.sin(a) + y * math.cos(a))

canvas = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
paste_at(canvas, load(os.path.join(BASE, "Cape_Back_Main.png")), 550, 410)
for side in ("L", "R"):
    hip = HIP[side]; ball, hip_anchor = LEG[side]
    vec = (ball[0] - hip_anchor[0], ball[1] - hip_anchor[1])
    up, low, cap = LEG_PIECES[side]
    limb(canvas, os.path.join(CUT, up), hip, CFG["leg_upper"][side], hip_anchor)
    knee = (hip[0] + rot_vec(vec, CFG["leg_upper"][side])[0] * SCALE,
            hip[1] + rot_vec(vec, CFG["leg_upper"][side])[1] * SCALE)
    limb(canvas, os.path.join(CUT, low), knee, CFG["leg_lower"][side], (ball[0], 0))
    cap_at(canvas, os.path.join(CUT, cap), knee)
elbows = {}
for side in ("L", "R"):
    ball, sh_anchor = ARM[side]; vec = (ball[0] - sh_anchor[0], ball[1] - sh_anchor[1])
    up, _, _ = ARM_PIECES[side]; sh = SHOULDER[side]
    limb(canvas, os.path.join(CUT, up), sh, CFG["arm_upper"][side], sh_anchor)
    elbows[side] = (sh[0] + rot_vec(vec, CFG["arm_upper"][side])[0] * SCALE,
                    sh[1] + rot_vec(vec, CFG["arm_upper"][side])[1] * SCALE)
paste_at(canvas, load(os.path.join(BASE, "Pelvis.png")), 550, 680)
paste_at(canvas, load(os.path.join(BASE, "Cape_Collar.png")), 550, 370)
paste_at(canvas, load(os.path.join(BASE, "Torso_Chest.png")), 550, 400)
paste_at(canvas, load(os.path.join(BASE, "Belt_Overlay.png")), 550, 670)
for side in ("L", "R"):
    _, _, cap = ARM_PIECES[side]; ball, _ = ARM[side]
    limb(canvas, os.path.join(FLEX, FLEX_LOWER[side]), elbows[side], CFG["arm_lower"][side], (ball[0], 0))
    cap_at(canvas, os.path.join(CUT, cap), elbows[side])
paste_at(canvas, load(os.path.join(BASE, "Neck.png"), scale=1.05), 550, 360)
paste_at(canvas, load(os.path.join(BASE, "Head_Front.png")), 550, 250)
canvas.save(os.path.join(OUT, "base-arms-up-transparent-20261031.png"))
print("saved base", canvas.size)
