"""Hand T-pose flatten: seat canon hands exactly how v7c gauntlet fists sit.

Old library demos (wrist-attach-fix-20261031, groove-a pose, arm_lower
-60/+60): hand angle 0 both sides, fingers-up (0,-1), scale 1.7.
Measured defects on that pose: finger direction 120 deg off the forearm
outward direction on BOTH sides; hand footprint 70% oversize vs the
v7c gauntlet fist it replaces (see measurements-20261031.json).

New T-pose (this folder): arm_upper/arm_lower L -90 / R +90, forearms
horizontal, fingers along the forearm axis, opposite signs per side:
  L (image-left, outward west (-1,0)): hand angle +90, finger (-1,0)
  R (image-right, outward east (+1,0)): hand angle -90, finger (+1,0)
Scale per hand = geometric mean of width-scale and length-scale to the
v7c gauntlet fist footprint on canvas (82 wide x 100 tall), NOT 1.7.
Canvas expanded to 1500x1500 with OX=+200 so the full horizontal
T-pose + hands fit with no crop (NO-CROP-WINDOW RULE, 2026-10-31).
Wrist target = forearm end - outward*20, so d_wrist = 20.0, gate PASS.
No mirror, no flip anywhere: rotation is in-plane only.
"""
import os, sys, math, json
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "/home/hatch/workspace/cape-jones-rig/wrist-attach-fix-20261031")
from check_wrist_attach import check, centre_for_wrist, rot_vec, HANDS

RIG = "/home/hatch/workspace/cape-jones-rig"
SLICED = os.path.join(RIG, "sliced"); CUT = os.path.join(RIG, "cut-limbs-v7c")
OUT = os.path.join(RIG, "hand-tpose-flatten-20261031")
W, H = 1500, 1500
OX = 200
SCALE = 0.95
SHOULDER = {"L": (430 + OX, 445), "R": (670 + OX, 445)}
HIP = {"L": (470 + OX, 740), "R": (615 + OX, 740)}
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
LEG = {"L": ((95, 314), (77, 40)), "R": ((100, 314), (84, 40))}
LEG_PIECES = {"L": ("Leg_Front_Upper.png", "Leg_Front_Lower.png", "Leg_Front_Cap.png"),
              "R": ("Leg_Back_Upper.png", "Leg_Back_Lower.png", "Leg_Back_Cap.png")}
ARM_PIECES = {"L": ("Arm_Front_Upper.png", "Arm_Front_Lower.png", "Arm_Front_Cap.png"),
              "R": ("Arm_Back_Upper.png", "Arm_Back_Lower.png", "Arm_Back_Cap.png")}
CFG = {"arm_upper": {"L": -90, "R": 90}, "arm_lower": {"L": -90, "R": 90},
       "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": 10, "R": -10}}
# scale per hand: geometric mean of width-scale (to 82) and length-scale (to 100)
SCALE_NEW = {
    "Hand_1_Fist.png": 1.04, "Hand_2_FistBack.png": 0.91, "Hand_3_Open.png": 0.82,
    "Hand_4_Point.png": 0.89, "Hand_5_Point2.png": 0.84, "Hand_6_Relaxed.png": 0.82,
    "Hand_7_Grip.png": 0.87,
}
ANGLE_NEW = {"L": 90, "R": -90}

def load(p, scale=SCALE):
    im = Image.open(p).convert("RGBA")
    return im.resize((int(im.size[0] * scale), int(im.size[1] * scale)), Image.LANCZOS)
def paste_at(c, im, cx, top): c.alpha_composite(im, (int(cx - im.size[0] / 2), int(top)))
def limb(c, path, joint, angle, anchor):
    im = load(path); ax, ay = anchor[0] * SCALE, anchor[1] * SCALE
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(im, (int(joint[0] - ax), int(joint[1] - ay)))
    layer = layer.rotate(angle, center=joint, expand=False); c.alpha_composite(layer)
def cap_at(c, path, joint):
    im = load(path); c.alpha_composite(im, (int(joint[0] - im.size[0] / 2), int(joint[1] - im.size[1] / 2)))

def build_body():
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    paste_at(canvas, load(os.path.join(SLICED, "Cape_Back_Main.png")), 550 + OX, 410)
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
    paste_at(canvas, load(os.path.join(SLICED, "Pelvis.png")), 550 + OX, 680)
    paste_at(canvas, load(os.path.join(SLICED, "Cape_Collar.png")), 550 + OX, 370)
    paste_at(canvas, load(os.path.join(SLICED, "Torso_Chest.png")), 550 + OX, 400)
    paste_at(canvas, load(os.path.join(SLICED, "Belt_Overlay.png")), 550 + OX, 670)
    lowers = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for side in ("L", "R"):
        _, low, cap = ARM_PIECES[side]; ball, _ = ARM[side]
        limb(lowers, os.path.join(CUT, low), elbows[side], CFG["arm_lower"][side], (ball[0], 0))
        cap_at(lowers, os.path.join(CUT, cap), elbows[side])
    return canvas, elbows, lowers

def fist_centre(elbow, arm_lower):
    dx, dy = rot_vec((0, 1), arm_lower)
    return (elbow[0] + dx * 210 * SCALE, elbow[1] + dy * 210 * SCALE)

def finish(plate, name):
    # transparent version for the no-crop gate, then grey viewing version
    plate.save(os.path.join(OUT, "frames", name.replace(".png", "-transparent.png")))
    bg = Image.new("RGBA", (W, H), (128, 128, 128, 255)); bg.alpha_composite(plate)
    bg.convert("RGB").save(os.path.join(OUT, name))

def erase_fist(lowers, fc, out):
    px = lowers.load(); bc = (fc[0] + out[0] * 40, fc[1] + out[1] * 40)
    for y in range(max(0, int(fc[1] - 120)), min(H, int(fc[1] + 120))):
        for x in range(max(0, int(fc[0] - 120)), min(W, int(fc[0] + 120))):
            if (x - fc[0]) * out[0] + (y - fc[1]) * out[1] > -10 and \
               (x - bc[0]) ** 2 + (y - bc[1]) ** 2 <= 95 ** 2:
                px[x, y] = (0, 0, 0, 0)

results = {}
# 0. Base-fist T-pose reference: built-in gauntlet fists, no swap
plate, elbows, lowers = build_body(); plate.alpha_composite(lowers)
paste_at(plate, load(os.path.join(SLICED, "Neck.png"), scale=1.05), 550 + OX, 360)
paste_at(plate, load(os.path.join(SLICED, "Head_Front.png")), 550 + OX, 250)
finish(plate, "tpose-base-fist-reference-20261031.png")
results["base_fist"] = {"elbows": {k: [round(v, 1) for v in val] for k, val in elbows.items()}}

HANDS_LIST = ["Hand_1_Fist.png", "Hand_2_FistBack.png", "Hand_3_Open.png",
              "Hand_4_Point.png", "Hand_5_Point2.png", "Hand_6_Relaxed.png", "Hand_7_Grip.png"]
for hfile in HANDS_LIST:
    tag = hfile.replace("Hand_", "").replace(".png", "").lower()
    new_scale = SCALE_NEW[hfile]
    # --- OLD PARAMS on T-pose (control): angle 0, scale 1.7, wrist-fixed
    plate, elbows, lowers = build_body(); pastes = []
    for side in ("L", "R"):
        fc = fist_centre(elbows[side], CFG["arm_lower"][side])
        out = rot_vec((0, 1), CFG["arm_lower"][side])
        erase_fist(lowers, fc, out)
        wt = (fc[0] - out[0] * 20, fc[1] - out[1] * 20)
        pastes.append((hfile, centre_for_wrist(hfile, 0, 1.7, wt), 0, 1.7, wt, fc))
    plate.alpha_composite(lowers)
    paste_at(plate, load(os.path.join(SLICED, "Neck.png"), scale=1.05), 550 + OX, 360)
    paste_at(plate, load(os.path.join(SLICED, "Head_Front.png")), 550 + OX, 250)
    hand = Image.open(os.path.join(SLICED, hfile)).convert("RGBA")
    hand_old = hand.resize((int(hand.size[0] * 1.7), int(hand.size[1] * 1.7)), Image.LANCZOS)
    for _, centre, _, _, _, _ in pastes:
        plate.alpha_composite(hand_old, (int(centre[0] - hand_old.size[0] / 2), int(centre[1] - hand_old.size[1] / 2)))
    finish(plate, f"tpose-{tag}-OLD-PARAMS-20261031.png")
    # --- NEW flattened
    plate, elbows, lowers = build_body(); pastes = []; gate = {}
    for side in ("L", "R"):
        fc = fist_centre(elbows[side], CFG["arm_lower"][side])
        out = rot_vec((0, 1), CFG["arm_lower"][side])
        erase_fist(lowers, fc, out)
        wt = (fc[0] - out[0] * 20, fc[1] - out[1] * 20)
        ang = ANGLE_NEW[side]
        centre = centre_for_wrist(hfile, ang, new_scale, wt)
        pastes.append((side, centre, ang, wt, fc))
        g = check(hfile, centre, ang, new_scale, fc)
        gate[side] = {"angle": ang, "scale": new_scale, "wrist_target": [round(v, 1) for v in wt],
                      "forearm_end_fist_centre": [round(v, 1) for v in fc],
                      "d_wrist": round(g["d_wrist"], 1), "d_tip": round(g["d_tip"], 1),
                      "verdict": g["verdict"],
                      "finger_dir": [round(v, 3) for v in rot_vec((0, -1), ang)],
                      "forearm_outward": [round(v, 3) for v in out]}
    plate.alpha_composite(lowers)
    paste_at(plate, load(os.path.join(SLICED, "Neck.png"), scale=1.05), 550 + OX, 360)
    paste_at(plate, load(os.path.join(SLICED, "Head_Front.png")), 550 + OX, 250)
    hand = Image.open(os.path.join(SLICED, hfile)).convert("RGBA")
    hand_new = hand.resize((int(hand.size[0] * new_scale), int(hand.size[1] * new_scale)), Image.LANCZOS)
    for side, centre, ang, _, _ in pastes:
        rot = hand_new.rotate(ang, expand=True, resample=Image.BICUBIC)
        plate.alpha_composite(rot, (int(centre[0] - rot.size[0] / 2), int(centre[1] - rot.size[1] / 2)))
    finish(plate, f"tpose-{tag}-FLATTENED-20261031.png")
    results[tag] = {"hand": hfile, "new_scale": new_scale, "old_scale": 1.7,
                    "scale_ratio_new_vs_old": round(new_scale / 1.7, 3),
                    "gate": gate}
    print(tag, "new scale", new_scale, "gate", {s: gate[s]["verdict"] for s in gate})

json.dump(results, open(os.path.join(OUT, "measurements-tpose-20261031.json"), "w"), indent=2)
print("done")
