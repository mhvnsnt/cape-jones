"""Joint-locked rig v5, 2026-10-31 — corrections from Mars 11:52 CDT.
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
HIP = {"L": (470, 740), "R": (615, 740)}  # v6: LEG 1 mirrored to LEG 2 visual centre (470, not 485), LEG 2 hip unchanged, perfect inverted mirror
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
    # ARM 1 = our left, GOOD, locked: Arm_Front, never flipped.
    # ARM 2 = our right, FIXED: Arm_Back, never flipped Front.
    # Flipping Front for Arm 2 was putting gauntlet/bicep/fist on the wrong side.
    ARM_PIECES = {"L": ("Arm_Front.png", "Arm_Front_Upper.png", "Arm_Front_Lower.png"),
                  "R": ("Arm_Back.png", "Arm_Back_Upper.png", "Arm_Back_Lower.png")}
    elbows = {}
    if arms_whole:
        for side in ("L", "R"):
            whole, _, _ = ARM_PIECES[side]
            limb(canvas, os.path.join(BASE, whole), SHOULDER[side], cfg["arm_upper"][side], (76, 30))
    else:
        for side in ("L", "R"):
            _, upper, _ = ARM_PIECES[side]
            sh = SHOULDER[side]
            limb(canvas, os.path.join(CUT, upper), sh, cfg["arm_upper"][side], (76, 30))
            elbows[side] = end_joint(sh, ARM_UPPER_LEN, cfg["arm_upper"][side])
    paste_at(canvas, load(os.path.join(BASE, "Pelvis.png")), 550, 680)
    paste_at(canvas, load(os.path.join(BASE, "Cape_Collar.png")), 550, 370)
    paste_at(canvas, load(os.path.join(BASE, "Torso_Chest.png")), 550, 400)
    paste_at(canvas, load(os.path.join(BASE, "Belt_Overlay.png")), 550, 670)
    if not arms_whole:
        for side in ("L", "R"):
            _, _, lower = ARM_PIECES[side]
            limb(canvas, os.path.join(CUT, lower), elbows[side], cfg["arm_lower"][side], (76, 20))
    paste_at(canvas, load(os.path.join(BASE, "Neck.png"), scale=1.05), 550, 360)
    paste_at(canvas, load(os.path.join(BASE, "Head_Front.png")), 550, 250)
    # NUMBER LABELS, per Mars: ARM 1 = our left, ARM 2 = our right,
    # LEG 1 = our left, LEG 2 = our right. Same sides for arms/legs.
    from PIL import ImageDraw
    d = ImageDraw.Draw(canvas)
    def label(x, y, text):
        d.ellipse((x-28, y-28, x+28, y+28), fill=(255, 0, 0, 255), outline=(255, 255, 255, 255), width=3)
        d.text((x-7, y-10), text, fill=(255, 255, 255, 255))
    # Near shoulders (Arm 1 left, Arm 2 right) and near hips (Leg 1 left, Leg 2 right)
    label(340, 430, "1")  # ARM 1
    d.text((300, 470), "ARM 1", fill=(255, 0, 0, 255))
    label(760, 430, "2")  # ARM 2
    d.text((720, 470), "ARM 2", fill=(255, 0, 0, 255))
    label(400, 820, "1")  # LEG 1
    d.text((360, 860), "LEG 1", fill=(255, 0, 0, 255))
    label(700, 820, "2")  # LEG 2
    d.text((660, 860), "LEG 2", fill=(255, 0, 0, 255))
    canvas.convert("RGB").save(os.path.join(OUT, name))
    print(name, "saved")

build("joint-apose-v6-20261031.png", {
    "arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": -20, "R": 20},
    "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": -10, "R": 10}})
build("joint-flex-v6-20261031.png", {
    "arm_upper": {"L": -25, "R": 25}, "arm_lower": {"L": 160, "R": -160},
    "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": -10, "R": 10}})
build("joint-punch-v6-20261031.png", {
    "arm_upper": {"L": -45, "R": 90}, "arm_lower": {"L": -45, "R": 90},
    "leg_upper": {"L": -20, "R": 20}, "leg_lower": {"L": -20, "R": 20}})
# Jump v4: arms WHOLE, up-out, no forearm bend. Legs tuck IN.
build("joint-jump-v6-20261031.png", {
    "arm_upper": {"L": -150, "R": 150}, "arm_lower": {"L": -150, "R": 150},
    "leg_upper": {"L": -20, "R": 20}, "leg_lower": {"L": 45, "R": -45}}, arms_whole=True)
build("joint-dance-v6-20261031.png", {
    "arm_upper": {"L": -60, "R": 60}, "arm_lower": {"L": -60, "R": 60},
    "leg_upper": {"L": -25, "R": 25}, "leg_lower": {"L": -25, "R": 25}})
build("joint-seated-v6-20261031.png", {
    "arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": -20, "R": 20},
    "leg_upper": {"L": -45, "R": 45}, "leg_lower": {"L": 0, "R": 0}})

json.dump({"version": "joint-locked-v6", "date": "2026-10-31",
    "shoulder_joints": SHOULDER, "hip_joints": HIP,
    "changes_vs_v3": ["HR hip 605->585 (20px left, screen-right hip was off right)",
                      "R leg uses Leg_Back pieces, L leg uses Leg_Front pieces",
                      "Jump legs tuck IN: lower +45/-45, not -90/+90 split",
                      "Jump/arms-up use whole Arm_Front pinned at shoulder, no forearm-only bend",
                      "Flex keeps cut-limb elbow bend (true bend pose)"],
    "rotation_rule": "end = joint + length*(sin(angle), cos(angle)), 0=down, positive=screen-right"},
    open("/home/hatch/workspace/cape-jones-rig/locked-joints-v6.json", "w"), indent=2)
print("v4 registry saved")
