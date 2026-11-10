"""Joint-locked rig v4, 2026-10-31 — corrections from Mars 11:52 CDT.
1. Hips: screen-right hip (character's left) was off to the right.
   Move it left 20px: HR 605 -> 585, and use the BACK leg pieces for
   the screen-right leg (Leg_Back_Upper/Lower), FRONT leg pieces for
   screen-left leg. Front-for-both was putting the back leg's hip
   in the wrong socket. HL stays (495,760).
2. Jump legs: bend TOWARD each other, not out into a split.
   Thighs slightly out, shins down-IN toward centre, feet under body.
   Was: lower -90/+90 (shins horizontal out). Now: lower +45/-45
   (shins down-in, feet close).
3. Arms raised: do NOT bend forearm alone. Raise the WHOLE arm as
   one unit from the shoulder, forearm follows upper, no separate
   elbow bend. Use the whole Arm_Front piece, pinned at the shoulder
   joint and rotated around it, for arms-up / jump arms.
   Cut-limb elbow bends stay only for true flex/bend poses.
All other v3 joints unchanged: shoulders (430,445)/(670,445),
hips (495,760)/(585,760), rotation end = joint + length*(sin,cos),
0 = straight down, positive = toward screen-right.
"""
from PIL import Image
import os, math, json
BASE = "/home/hatch/workspace/cape-jones-rig/sliced"
CUT = "/home/hatch/workspace/cape-jones-rig/cut-limbs"
OUT = "/home/hatch/workspace/cape-jones-rig/reposes"
SCALE = 0.95
SHOULDER = {"L": (430, 445), "R": (670, 445)}
HIP = {"L": (495, 760), "R": (585, 760)}
ARM_UPPER_LEN = (285-30)*SCALE
LEG_UPPER_LEN = (325-40)*SCALE
LEG_PIECES = {"L": ("Leg_Front_Upper.png", "Leg_Front_Lower.png", (77, 40), (77, 25)),
              "R": ("Leg_Back_Upper.png", "Leg_Back_Lower.png", (84, 40), (84, 25))}

def load(path, scale=SCALE):
    im = Image.open(path).convert("RGBA")
    return im.resize((int(im.size[0]*scale), int(im.size[1]*scale)), Image.LANCZOS)

def paste_at(canvas, im, cx, top):
    canvas.paste(im, (int(cx-im.size[0]/2), int(top)), im)

def limb(canvas, piece_path, joint, angle, anchor):
    im = load(piece_path)
    ax, ay = anchor[0]*SCALE, anchor[1]*SCALE
    layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    layer.paste(im, (int(joint[0]-ax), int(joint[1]-ay)), im)
    layer = layer.rotate(angle, center=joint, expand=False)
    canvas.alpha_composite(layer)

def end_joint(joint, length, angle):
    a = math.radians(angle)
    return (joint[0] + length*math.sin(a), joint[1] + length*math.cos(a))

def build(name, cfg, arms_whole=False):
    canvas = Image.new("RGBA", (1100, 1500), (128, 128, 128, 255))
    paste_at(canvas, load(os.path.join(BASE, "Cape_Back_Main.png")), 550, 410)
    for side in ("L", "R"):
        hip = HIP[side]
        up_name, low_name, hip_anchor, knee_anchor = LEG_PIECES[side]
        limb(canvas, os.path.join(CUT, up_name), hip, cfg["leg_upper"][side], hip_anchor)
        knee = end_joint(hip, LEG_UPPER_LEN, cfg["leg_upper"][side])
        limb(canvas, os.path.join(CUT, low_name), knee, cfg["leg_lower"][side], knee_anchor)
    elbows = {}
    if arms_whole:
        # Whole arms, pinned at shoulder, rotated as one unit.
        # Whole Arm_Front: shoulder anchor approx (76,30), length to fist ~ (511-30)*0.95
        for side in ("L", "R"):
            limb(canvas, os.path.join(BASE, "Arm_Front.png"), SHOULDER[side], cfg["arm_upper"][side], (76, 30))
    else:
        for side in ("L", "R"):
            sh = SHOULDER[side]
            limb(canvas, os.path.join(CUT, "Arm_Front_Upper.png"), sh, cfg["arm_upper"][side], (76, 30))
            elbows[side] = end_joint(sh, ARM_UPPER_LEN, cfg["arm_upper"][side])
    paste_at(canvas, load(os.path.join(BASE, "Pelvis.png")), 550, 680)
    paste_at(canvas, load(os.path.join(BASE, "Cape_Collar.png")), 550, 370)
    paste_at(canvas, load(os.path.join(BASE, "Torso_Chest.png")), 550, 400)
    paste_at(canvas, load(os.path.join(BASE, "Belt_Overlay.png")), 550, 670)
    if not arms_whole:
        for side in ("L", "R"):
            limb(canvas, os.path.join(CUT, "Arm_Front_Lower.png"), elbows[side], cfg["arm_lower"][side], (76, 20))
    paste_at(canvas, load(os.path.join(BASE, "Neck.png"), scale=1.05), 550, 360)
    paste_at(canvas, load(os.path.join(BASE, "Head_Front.png")), 550, 250)
    canvas.convert("RGB").save(os.path.join(OUT, name))
    print(name, "saved")

build("joint-apose-v4-20261031.png", {
    "arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": -20, "R": 20},
    "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": -10, "R": 10}})
build("joint-flex-v4-20261031.png", {
    "arm_upper": {"L": -25, "R": 25}, "arm_lower": {"L": 160, "R": -160},
    "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": -10, "R": 10}})
build("joint-punch-v4-20261031.png", {
    "arm_upper": {"L": -45, "R": 90}, "arm_lower": {"L": -45, "R": 90},
    "leg_upper": {"L": -20, "R": 20}, "leg_lower": {"L": -20, "R": 20}})
# Jump v4: arms WHOLE, up-out, no forearm bend. Legs tuck IN.
build("joint-jump-v4-20261031.png", {
    "arm_upper": {"L": -150, "R": 150}, "arm_lower": {"L": -150, "R": 150},
    "leg_upper": {"L": -20, "R": 20}, "leg_lower": {"L": 45, "R": -45}}, arms_whole=True)
build("joint-dance-v4-20261031.png", {
    "arm_upper": {"L": -60, "R": 60}, "arm_lower": {"L": -60, "R": 60},
    "leg_upper": {"L": -25, "R": 25}, "leg_lower": {"L": -25, "R": 25}})
build("joint-seated-v4-20261031.png", {
    "arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": -20, "R": 20},
    "leg_upper": {"L": -45, "R": 45}, "leg_lower": {"L": 0, "R": 0}})

json.dump({"version": "joint-locked-v4", "date": "2026-10-31",
    "shoulder_joints": SHOULDER, "hip_joints": HIP,
    "changes_vs_v3": ["HR hip 605->585 (20px left, screen-right hip was off right)",
                      "R leg uses Leg_Back pieces, L leg uses Leg_Front pieces",
                      "Jump legs tuck IN: lower +45/-45, not -90/+90 split",
                      "Jump/arms-up use whole Arm_Front pinned at shoulder, no forearm-only bend",
                      "Flex keeps cut-limb elbow bend (true bend pose)"],
    "rotation_rule": "end = joint + length*(sin(angle), cos(angle)), 0=down, positive=screen-right"},
    open("/home/hatch/workspace/cape-jones-rig/locked-joints-v4.json", "w"), indent=2)
print("v4 registry saved")
