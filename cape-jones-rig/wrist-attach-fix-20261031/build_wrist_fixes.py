"""Wrist-attachment fixes: Jeice serve (+ ball effect) and dance variants.

Serve: base = jei-01-base-for-swap (approved JEI-01 geometry, L arm top).
  OLD: Hand_3_Open centred (314,530), angle -20 -> wrist 70.6px from
       forearm end, tip 54.9px -> fingertip-first FAIL.
  FIXED: turn IN-PLANE to 164.7 deg (NO mirror, NO flip), centre
       (307.6,549.6), wrist lands 25px inside forearm end -> PASS.
       Ball effect re-applied OVER the new palm centre (orb follows palm).
  MOVE-ONLY CONTROL: same -20 angle, centre moved so wrist lands exactly
       on the forearm end -> passes the number, but the hand body then
       sits up over the gauntlet/upper arm. Kept so Mars can see why a
       pure move cannot fix a fingertip-first hand. NOT a fix candidate.

Dance variants: rebuilt from build_dance_variants.py geometry (same
poses, same angles), with two changes only:
  1. the built-in fist is erased (near-white pixels, radius 70 around
     fist centre + outward*30, i.e. the fist blob, not the whole forearm)
  2. the swapped hand is pasted so its WRIST point lands 20px inside
     the forearm end (fist centre - outward*20), fingers-up gesture
     preserved, angle 0, scale 1.7, NO mirror.
  Base-fist frames are rebuilt unchanged (built-in fist is continuous,
  no swapped hand, no defect) and counted as already-PASS.
"""
import os, math, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from check_wrist_attach import HANDS, check, centre_for_wrist, angle_for_direction, rot_vec

RIG = "/home/hatch/workspace/cape-jones-rig"
SLICED = os.path.join(RIG, "sliced")
LB = os.path.join(RIG, "ginyu-force-limits-broken-20261031")
DV = os.path.join(RIG, "fight-and-sheets-20261031", "dance-variants")
OUT = os.path.join(RIG, "wrist-attach-fix-20261031")
os.makedirs(OUT, exist_ok=True)

def erase_white(im, cx, cy, r):
    px = im.load()
    for y in range(max(0, int(cy - r)), min(im.size[1], int(cy + r))):
        for x in range(max(0, int(cx - r)), min(im.size[0], int(cx + r))):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                R, G, B, A = px[x, y]
                if A > 0 and R > 180 and G > 180 and B > 180:
                    px[x, y] = (0, 0, 0, 0)
    return im

# ---------------- serve ----------------
base = Image.open(os.path.join(LB, "jei-01-base-for-swap-20261031.png")).convert("RGBA")
F = (314.0, 517.0)
hand = Image.open(os.path.join(SLICED, "Hand_3_Open.png")).convert("RGBA")

# FIXED
c = Image.open(os.path.join(LB, "jei-01-base-for-swap-20261031.png")).convert("RGBA")
c = erase_white(c, 314, 530, 65)
D = (-0.263, 0.965)
a = angle_for_direction(D)
centre = centre_for_wrist("Hand_3_Open.png", a, 1.0, (F[0] - D[0] * 25, F[1] - D[1] * 25))
h = hand.rotate(a, expand=True, resample=Image.BICUBIC)
c.alpha_composite(h, (int(centre[0] - h.size[0] / 2), int(centre[1] - h.size[1] / 2)))
c.save(os.path.join(OUT, "jei-01-serve-open-palm-WRIST-FIXED-20261031.png"))
print("serve fixed: angle", round(a, 1), "centre", tuple(round(v, 1) for v in centre),
      "gate", check("Hand_3_Open.png", centre, a, 1.0, F))

# FIXED + ball effect (orb follows the palm, not the old screen position)
cb = c.copy()
lay = Image.new("RGBA", cb.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
pc = (int(centre[0]), int(centre[1]))  # palm centre
for r, col, w in [(70, (255, 230, 110, 90), 3), (48, (255, 230, 110, 255), 0)]:
    d.ellipse([pc[0] - r, pc[1] - r, pc[0] + r, pc[1] + r], fill=col)
d.ellipse([pc[0] - 18, pc[1] - 18, pc[0] + 18, pc[1] + 18], fill=(255, 250, 220, 255))
cb.alpha_composite(lay)
cb.save(os.path.join(OUT, "jei-01-serve-open-palm-ball-WRIST-FIXED-20261031.png"))
print("serve+ball fixed: orb at palm centre", pc, "(old orb (314,420) sat above old fingertips)")

# MOVE-ONLY CONTROL
cm = Image.open(os.path.join(LB, "jei-01-base-for-swap-20261031.png")).convert("RGBA")
cm = erase_white(cm, 314, 530, 65)
c2 = centre_for_wrist("Hand_3_Open.png", -20, 1.0, F)
h2 = hand.rotate(-20, expand=True, resample=Image.BICUBIC)
cm.alpha_composite(h2, (int(c2[0] - h2.size[0] / 2), int(c2[1] - h2.size[1] / 2)))
cm.save(os.path.join(OUT, "jei-01-serve-open-palm-MOVE-ONLY-CONTROL-20261031.png"))
print("serve move-only control: centre", tuple(round(v, 1) for v in c2),
      "gate", check("Hand_3_Open.png", c2, -20, 1.0, F),
      "NOTE: numeric PASS, hand body overlaps gauntlet — see crop")

# ---------------- dance variants (rebuild, wrist-first paste) ----------------
CUT = os.path.join(RIG, "cut-limbs-v7c")
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
def paste_at(c, im, cx, top): c.alpha_composite(im, (int(cx - im.size[0] / 2), int(top)))
def limb(c, path, joint, angle, anchor):
    im = load(path); ax, ay = anchor[0] * SCALE, anchor[1] * SCALE
    layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    layer.alpha_composite(im, (int(joint[0] - ax), int(joint[1] - ay)))
    layer = layer.rotate(angle, center=joint, expand=False); c.alpha_composite(layer)
def cap_at(c, path, joint):
    im = load(path); c.alpha_composite(im, (int(joint[0] - im.size[0] / 2), int(joint[1] - im.size[1] / 2)))

def build_plate(cfg):
    canvas = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    paste_at(canvas, load(os.path.join(SLICED, "Cape_Back_Main.png")), 550, 410)
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
    paste_at(canvas, load(os.path.join(SLICED, "Pelvis.png")), 550, 680)
    paste_at(canvas, load(os.path.join(SLICED, "Cape_Collar.png")), 550, 370)
    paste_at(canvas, load(os.path.join(SLICED, "Torso_Chest.png")), 550, 400)
    paste_at(canvas, load(os.path.join(SLICED, "Belt_Overlay.png")), 550, 670)
    # Lowers on their OWN layer: fist-blob erasing must never touch torso,
    # cape or head pixels (groove-b hands fold over the chest — erasing on
    # the full plate ate a torso chunk in v1; caught on eye-check, fixed).
    lowers = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    for side in ("L", "R"):
        _, low, cap = ARM_PIECES[side]; ball, _ = ARM[side]
        limb(lowers, os.path.join(CUT, low), elbows[side], cfg["arm_lower"][side], (ball[0], 0))
        cap_at(lowers, os.path.join(CUT, cap), elbows[side])
    return canvas, elbows, lowers

POSES = [
    ("groove-a", {"arm_upper": {"L": -60, "R": 60}, "arm_lower": {"L": -60, "R": 60},
                  "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": 10, "R": -10}}),
    ("groove-b", {"arm_upper": {"L": -115, "R": 85}, "arm_lower": {"L": 65, "R": -95},
                  "leg_upper": {"L": -16, "R": 6}, "leg_lower": {"L": 32, "R": -28}}),
    ("groove-c", {"arm_upper": {"L": -25, "R": 35}, "arm_lower": {"L": -88, "R": 145},
                  "leg_upper": {"L": -20, "R": 20}, "leg_lower": {"L": 15, "R": -15}}),
]
HANDS_DV = [("base-fist", None), ("open", "Hand_3_Open.png"),
            ("point", "Hand_4_Point.png"), ("relaxed", "Hand_6_Relaxed.png")]

def fist_centre(elbow, arm_lower):
    dx, dy = rot_vec((0, 1), arm_lower)
    return (elbow[0] + dx * 210 * SCALE, elbow[1] + dy * 210 * SCALE)

audit = []
for vname, hfile in HANDS_DV:
    for pname, cfg in POSES:
        plate, elbows, lowers = build_plate(cfg)
        hand_pastes = []
        if hfile:
            hand = Image.open(os.path.join(SLICED, hfile)).convert("RGBA")
            hand = hand.resize((int(hand.size[0] * 1.7), int(hand.size[1] * 1.7)), Image.LANCZOS)
            for side in ("L", "R"):
                fc = fist_centre(elbows[side], cfg["arm_lower"][side])
                out = rot_vec((0, 1), cfg["arm_lower"][side])
                # erase built-in fist blob ON THE LOWERS LAYER ONLY: ALL alpha
                # distal to the forearm-end plane (dot > -10) within 95px of
                # fist blob centre. Torso/cape/head are not in this layer, so
                # they cannot be eaten (v1 bug, groove-b chest hole, fixed).
                px = lowers.load()
                bc = (fc[0] + out[0] * 40, fc[1] + out[1] * 40)
                for y in range(max(0, int(fc[1] - 120)), min(1500, int(fc[1] + 120))):
                    for x in range(max(0, int(fc[0] - 120)), min(1100, int(fc[0] + 120))):
                        dot = (x - fc[0]) * out[0] + (y - fc[1]) * out[1]
                        if dot > -10 and (x - bc[0]) ** 2 + (y - bc[1]) ** 2 <= 95 ** 2:
                            px[x, y] = (0, 0, 0, 0)
                # wrist target: 20px inside forearm end along arm axis
                wt = (fc[0] - out[0] * 20, fc[1] - out[1] * 20)
                centre = centre_for_wrist(hfile, 0, 1.7, wt)
                hand_pastes.append((centre, hand))
                g_old = check(hfile, fc, 0, 1.7, fc)
                g_new = check(hfile, centre, 0, 1.7, fc)
                audit.append([f"{vname}-{pname}-{side}", hfile, "OLD centre-paste",
                              round(g_old["d_wrist"], 1), round(g_old["d_tip"], 1), g_old["verdict"],
                              "FIXED wrist-first",
                              round(g_new["d_wrist"], 1), round(g_new["d_tip"], 1), g_new["verdict"]])
        plate.alpha_composite(lowers)
        paste_at(plate, load(os.path.join(SLICED, "Neck.png"), scale=1.05), 550, 360)
        paste_at(plate, load(os.path.join(SLICED, "Head_Front.png")), 550, 250)
        for centre, hand in hand_pastes:
            plate.alpha_composite(hand, (int(centre[0] - hand.size[0] / 2),
                                         int(centre[1] - hand.size[1] / 2)))
        bg = Image.new("RGBA", (1100, 1500), (128, 128, 128, 255))
        bg.alpha_composite(plate)
        bg.convert("RGB").save(os.path.join(OUT, f"dance-{vname}-{pname}-WRIST-FIXED-20261031.png"))
        print(vname, pname, "saved")
import csv
with open(os.path.join(OUT, "wrist_gate_dance_audit.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["item", "hand", "old_method", "old_d_wrist", "old_d_tip", "old_verdict",
                "new_method", "new_d_wrist", "new_d_tip", "new_verdict"])
    w.writerows(audit)
print("dance audit rows:", len(audit))
