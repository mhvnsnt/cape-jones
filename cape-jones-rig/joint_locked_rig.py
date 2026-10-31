"""Joint-locked Cape Jones rig, v3, 2026-10-31.
Industry-standard rule, per Mars 2026-10-31 11:42 CDT:
- Shoulder joints are FIXED to the torso. Hip joints are FIXED to the pelvis.
- A limb's shoulder/hip end is pinned at that joint, no matter the pose angle.
- A lower limb's elbow/knee end is pinned at the elbow/knee computed from
  the upper limb, so upper and lower can never float apart.
- Torso and pelvis do not move per pose in these tests, so joints are
  absolute canvas points. If torso/pelvis move, joints move with them
  (joints are defined relative to torso/pelvis origin, see registry).

Calibration, checked with a rotation test 2026-10-31:
- PIL rotate(angle) on screen: a downward vector (0,1) rotated by angle
  goes to (sin(angle), cos(angle)). So elbow/knee =
  joint + length * (sin(angle), cos(angle)), angle in degrees.
- Arm upper: shoulder anchor (76,30) unscaled, elbow anchor (76,285).
- Arm lower: elbow anchor (76,20) unscaled.
- Leg upper: hip anchor (77,40) unscaled, knee anchor (77,325).
- Leg lower: knee anchor (77,25) unscaled.
- All scaled 0.95. Upper arm length shoulder->elbow = (285-30)*0.95 = 242.
  Upper leg length hip->knee = (325-40)*0.95 = 271.
  Lower arm length elbow->wrist approx (251-20)*0.95 = 219, not needed
  for pinning (its top is pinned, its end follows).

Fixed joints (canvas 1100x1500, v8 torso/pelvis positions):
- Torso: cx 550, top 400, scaled 299x303 -> left 400, right 700, bottom 703.
- Pelvis: cx 550, top 680, scaled 218x123 -> left 441, right 659, bottom 803.
- Shoulder L (screen left): (430, 445) - inside torso, 30 in from left edge.
- Shoulder R (screen right): (670, 445) - inside torso, 30 in from right edge.
- Hip L: (495, 760) - inside pelvis.
- Hip R: (605, 760) - inside pelvis.
Layer order: cape, legs, arms, pelvis, collar, torso, belt, neck, head.
Limbs are UNDER torso/pelvis, so their joint ends tuck under the body
and cannot appear floating, even at extreme angles.
"""
from PIL import Image
import os, math, json
BASE = "/home/hatch/workspace/cape-jones-rig/sliced"
CUT = "/home/hatch/workspace/cape-jones-rig/cut-limbs"
OUT = "/home/hatch/workspace/cape-jones-rig/reposes"
SCALE = 0.95
SHOULDER = {"L": (430, 445), "R": (670, 445)}
HIP = {"L": (495, 760), "R": (605, 760)}
ARM_UPPER_LEN = (285-30)*SCALE
LEG_UPPER_LEN = (325-40)*SCALE

def load(path, scale=SCALE):
    im = Image.open(path).convert("RGBA")
    return im.resize((int(im.size[0]*scale), int(im.size[1]*scale)), Image.LANCZOS)

def paste_at(canvas, im, cx, top):
    canvas.paste(im, (int(cx-im.size[0]/2), int(top)), im)

def limb(canvas, piece_path, joint, angle, anchor):
    """Paste piece so anchor (x,y, scaled) sits at joint, then rotate
    the whole layer around joint by angle. Returns end joint for a
    following piece: joint + length*(sin,cos) is computed by caller."""
    im = load(piece_path)
    ax, ay = anchor[0]*SCALE, anchor[1]*SCALE
    layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    layer.paste(im, (int(joint[0]-ax), int(joint[1]-ay)), im)
    layer = layer.rotate(angle, center=joint, expand=False)
    canvas.alpha_composite(layer)

def end_joint(joint, length, angle):
    a = math.radians(angle)
    return (joint[0] + length*math.sin(a), joint[1] + length*math.cos(a))

def build(name, cfg):
    canvas = Image.new("RGBA", (1100, 1500), (128, 128, 128, 255))
    paste_at(canvas, load(os.path.join(BASE, "Cape_Back_Main.png")), 550, 410)
    # Legs, cut limbs, hip-locked
    for side in ("L", "R"):
        hip = HIP[side]
        upper_ang = cfg["leg_upper"][side]
        lower_ang = cfg["leg_lower"][side]
        limb(canvas, os.path.join(CUT, "Leg_Front_Upper.png"), hip, upper_ang, (77, 40))
        knee = end_joint(hip, LEG_UPPER_LEN, upper_ang)
        limb(canvas, os.path.join(CUT, "Leg_Front_Lower.png"), knee, lower_ang, (77, 25))
    # Arms, cut limbs, shoulder-locked. Upper arms UNDER torso (shoulder
    # tucked), lower arms OVER torso (forearm/fist in front, e.g. flex).
    # Elbow is pinned in both passes, so the joint cannot float.
    elbows = {}
    for side in ("L", "R"):
        sh = SHOULDER[side]
        upper_ang = cfg["arm_upper"][side]
        limb(canvas, os.path.join(CUT, "Arm_Front_Upper.png"), sh, upper_ang, (76, 30))
        elbows[side] = end_joint(sh, ARM_UPPER_LEN, upper_ang)
    paste_at(canvas, load(os.path.join(BASE, "Pelvis.png")), 550, 680)
    paste_at(canvas, load(os.path.join(BASE, "Cape_Collar.png")), 550, 370)
    paste_at(canvas, load(os.path.join(BASE, "Torso_Chest.png")), 550, 400)
    paste_at(canvas, load(os.path.join(BASE, "Belt_Overlay.png")), 550, 670)
    for side in ("L", "R"):
        limb(canvas, os.path.join(CUT, "Arm_Front_Lower.png"), elbows[side], cfg["arm_lower"][side], (76, 20))
    paste_at(canvas, load(os.path.join(BASE, "Neck.png"), scale=1.05), 550, 360)
    paste_at(canvas, load(os.path.join(BASE, "Head_Front.png")), 550, 250)
    canvas.convert("RGB").save(os.path.join(OUT, name))
    print(name, "saved")

# Angles: 0 = limb straight down. Positive = toward screen-right.
# Mirror: L and R are mirrors, so L angle = -R angle for symmetric poses.
# A-pose: arms down-out 20, legs down-out 10, straight limbs.
build("joint-apose-v3-20261031.png", {
    "arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": -20, "R": 20},
    "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": -10, "R": 10}})
# Flex: upper down-out 25, lower bent up-in: R lower -160 (up-left),
# L lower +160 (up-right). Fists end at chest sides, in front of torso.
build("joint-flex-v3-20261031.png", {
    "arm_upper": {"L": -25, "R": 25}, "arm_lower": {"L": 160, "R": -160},
    "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": -10, "R": 10}})
# Punch: R arm straight horizontal (90), L arm back (-45, lower -45),
# legs stepping (L -20, R 20).
build("joint-punch-v3-20261031.png", {
    "arm_upper": {"L": -45, "R": 90}, "arm_lower": {"L": -45, "R": 90},
    "leg_upper": {"L": -20, "R": 20}, "leg_lower": {"L": -20, "R": 20}})
# Jump: arms up-out (L -150, R 150), legs tucked (upper -30/+30,
# lower bent back: L -90, R 90 is knees bent, shins back-in).
build("joint-jump-v3-20261031.png", {
    "arm_upper": {"L": -150, "R": 150}, "arm_lower": {"L": -150, "R": 150},
    "leg_upper": {"L": -30, "R": 30}, "leg_lower": {"L": -90, "R": 90}})
# Dance: arms swinging opposite (L -60, R 60, lowers same), legs wide.
build("joint-dance-v3-20261031.png", {
    "arm_upper": {"L": -60, "R": 60}, "arm_lower": {"L": -60, "R": 60},
    "leg_upper": {"L": -25, "R": 25}, "leg_lower": {"L": -25, "R": 25}})
# Seated (lounge test): thighs forward-out in front view = upper 45,
# shins down: lower 0. This is a front-view seated approximation;
# a true recline still needs a reclined torso piece.
build("joint-seated-v3-20261031.png", {
    "arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": -20, "R": 20},
    "leg_upper": {"L": -45, "R": 45}, "leg_lower": {"L": 0, "R": 0}})

registry = {
    "version": "joint-locked-v3", "date": "2026-10-31", "canvas": [1100, 1500],
    "shoulder_joints": SHOULDER, "hip_joints": HIP,
    "anchors_unscaled": {"arm_upper_shoulder": [76, 30], "arm_upper_elbow": [76, 285],
                         "arm_lower_elbow": [76, 20], "leg_upper_hip": [77, 40],
                         "leg_upper_knee": [77, 325], "leg_lower_knee": [77, 25]},
    "lengths_scaled": {"arm_upper": ARM_UPPER_LEN, "leg_upper": LEG_UPPER_LEN},
    "rotation_rule": "end = joint + length * (sin(angle), cos(angle)), angle deg, 0 = straight down, positive = toward screen-right",
    "layer_order": ["Cape_Back_Main", "legs", "arms", "Pelvis", "Cape_Collar", "Torso_Chest", "Belt_Overlay", "Neck", "Head_Front"],
    "note": "Limbs under torso/pelvis, joints inside torso/pelvis, so joints cannot float apart. Torso/pelvis fixed in these tests; if they move, joints move with them."
}
json.dump(registry, open("/home/hatch/workspace/cape-jones-rig/locked-joints-v3.json", "w"), indent=2)
print("registry saved")
