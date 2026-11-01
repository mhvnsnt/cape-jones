"""Hand-library demos: every canon hand on the same test arm (groove-a
pose, arms out), OLD centre-paste vs FIXED wrist-first paste, both hands.
Fist / FistBack / Point2 / Grip have no old dance-variant frame, so this
is their first before/after. Scale 1.7, angle 0, fingers-up gesture kept.
"""
import os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from check_wrist_attach import check, centre_for_wrist, rot_vec

RIG = "/home/hatch/workspace/cape-jones-rig"
SLICED = os.path.join(RIG, "sliced"); CUT = os.path.join(RIG, "cut-limbs-v7c")
OUT = os.path.join(RIG, "wrist-attach-fix-20261031")
SCALE = 0.95
SHOULDER = {"L": (430, 445), "R": (670, 445)}
HIP = {"L": (470, 740), "R": (615, 740)}
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
LEG = {"L": ((95, 314), (77, 40)), "R": ((100, 314), (84, 40))}
LEG_PIECES = {"L": ("Leg_Front_Upper.png", "Leg_Front_Lower.png", "Leg_Front_Cap.png"),
              "R": ("Leg_Back_Upper.png", "Leg_Back_Lower.png", "Leg_Back_Cap.png")}
ARM_PIECES = {"L": ("Arm_Front_Upper.png", "Arm_Front_Lower.png", "Arm_Front_Cap.png"),
              "R": ("Arm_Back_Upper.png", "Arm_Back_Lower.png", "Arm_Back_Cap.png")}
CFG = {"arm_upper": {"L": -60, "R": 60}, "arm_lower": {"L": -60, "R": 60},
       "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": 10, "R": -10}}

def load(p, scale=SCALE):
    im = Image.open(p).convert("RGBA")
    return im.resize((int(im.size[0] * scale), int(im.size[1] * scale)), Image.LANCZOS)
def paste_at(c, im, cx, top): c.alpha_composite(im, (int(cx - im.size[0] / 2), int(top)))
def limb(c, path, joint, angle, anchor):
    im = load(path); ax, ay = anchor[0] * SCALE, anchor[1] * SCALE
    layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    layer.alpha_composite(im, (int(joint[0] - ax), int(joint[1] - ay)))
    layer = layer.rotate(angle, center=joint, expand=False); c.alpha_composite(layer)
def cap_at(c, path, joint):
    im = load(path); c.alpha_composite(im, (int(joint[0] - im.size[0] / 2), int(joint[1] - im.size[1] / 2)))

def build():
    canvas = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    paste_at(canvas, load(os.path.join(SLICED, "Cape_Back_Main.png")), 550, 410)
    for side in ("L", "R"):
        hip = HIP[side]; ball, ha = LEG[side]; vec = (ball[0] - ha[0], ball[1] - ha[1])
        up, low, cap = LEG_PIECES[side]
        limb(canvas, os.path.join(CUT, up), hip, CFG["leg_upper"][side], ha)
        knee = (hip[0] + rot_vec(vec, CFG["leg_upper"][side])[0] * SCALE,
                hip[1] + rot_vec(vec, CFG["leg_upper"][side])[1] * SCALE)
        limb(canvas, os.path.join(CUT, low), knee, CFG["leg_lower"][side], (ball[0], 0))
        cap_at(canvas, os.path.join(CUT, cap), knee)
    elbows = {}
    for side in ("L", "R"):
        ball, sa = ARM[side]; vec = (ball[0] - sa[0], ball[1] - sa[1])
        up, _, _ = ARM_PIECES[side]; sh = SHOULDER[side]
        limb(canvas, os.path.join(CUT, up), sh, CFG["arm_upper"][side], sa)
        elbows[side] = (sh[0] + rot_vec(vec, CFG["arm_upper"][side])[0] * SCALE,
                        sh[1] + rot_vec(vec, CFG["arm_upper"][side])[1] * SCALE)
    paste_at(canvas, load(os.path.join(SLICED, "Pelvis.png")), 550, 680)
    paste_at(canvas, load(os.path.join(SLICED, "Cape_Collar.png")), 550, 370)
    paste_at(canvas, load(os.path.join(SLICED, "Torso_Chest.png")), 550, 400)
    paste_at(canvas, load(os.path.join(SLICED, "Belt_Overlay.png")), 550, 670)
    lowers = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    for side in ("L", "R"):
        _, low, cap = ARM_PIECES[side]; ball, _ = ARM[side]
        limb(lowers, os.path.join(CUT, low), elbows[side], CFG["arm_lower"][side], (ball[0], 0))
        cap_at(lowers, os.path.join(CUT, cap), elbows[side])
    return canvas, elbows, lowers

def fist_centre(elbow, arm_lower):
    dx, dy = rot_vec((0, 1), arm_lower)
    return (elbow[0] + dx * 210 * SCALE, elbow[1] + dy * 210 * SCALE)

HANDS = ["Hand_1_Fist.png", "Hand_2_FistBack.png", "Hand_3_Open.png",
         "Hand_4_Point.png", "Hand_5_Point2.png", "Hand_6_Relaxed.png", "Hand_7_Grip.png"]
for hfile in HANDS:
    tag = hfile.replace("Hand_", "").replace(".png", "").lower()
    hand = Image.open(os.path.join(SLICED, hfile)).convert("RGBA")
    hand = hand.resize((int(hand.size[0] * 1.7), int(hand.size[1] * 1.7)), Image.LANCZOS)
    # OLD: centre-paste, no erase (the old dance method)
    plate, elbows, lowers = build(); plate.alpha_composite(lowers)
    paste_at(plate, load(os.path.join(SLICED, "Neck.png"), scale=1.05), 550, 360)
    paste_at(plate, load(os.path.join(SLICED, "Head_Front.png")), 550, 250)
    for side in ("L", "R"):
        fc = fist_centre(elbows[side], CFG["arm_lower"][side])
        plate.alpha_composite(hand, (int(fc[0] - hand.size[0] / 2), int(fc[1] - hand.size[1] / 2)))
    bg = Image.new("RGBA", (1100, 1500), (128, 128, 128, 255)); bg.alpha_composite(plate)
    bg.convert("RGB").save(os.path.join(OUT, f"library-{tag}-OLD-centre-paste-20261031.png"))
    # FIXED: erase fist blob on lowers layer, wrist-first paste
    plate, elbows, lowers = build()
    pastes = []
    for side in ("L", "R"):
        fc = fist_centre(elbows[side], CFG["arm_lower"][side])
        out = rot_vec((0, 1), CFG["arm_lower"][side])
        px = lowers.load(); bc = (fc[0] + out[0] * 40, fc[1] + out[1] * 40)
        for y in range(max(0, int(fc[1] - 120)), min(1500, int(fc[1] + 120))):
            for x in range(max(0, int(fc[0] - 120)), min(1100, int(fc[0] + 120))):
                if (x - fc[0]) * out[0] + (y - fc[1]) * out[1] > -10 and \
                   (x - bc[0]) ** 2 + (y - bc[1]) ** 2 <= 95 ** 2:
                    px[x, y] = (0, 0, 0, 0)
        wt = (fc[0] - out[0] * 20, fc[1] - out[1] * 20)
        pastes.append(centre_for_wrist(hfile, 0, 1.7, wt))
    plate.alpha_composite(lowers)
    paste_at(plate, load(os.path.join(SLICED, "Neck.png"), scale=1.05), 550, 360)
    paste_at(plate, load(os.path.join(SLICED, "Head_Front.png")), 550, 250)
    for centre in pastes:
        plate.alpha_composite(hand, (int(centre[0] - hand.size[0] / 2), int(centre[1] - hand.size[1] / 2)))
    bg = Image.new("RGBA", (1100, 1500), (128, 128, 128, 255)); bg.alpha_composite(plate)
    bg.convert("RGB").save(os.path.join(OUT, f"library-{tag}-WRIST-FIXED-20261031.png"))
    print(tag, "old d_wrist ~", round(check(hfile, (0, 0), 0, 1.7, (0, 0))["d_wrist"], 1),
          "(centre-paste offset; see audit for per-frame values)")
print("library demos done")
