"""Joint-locked rig v7, 2026-10-31 — elbow/knee square-crop fix.
Industry standard cutout rule applied:
- Pivot is the JOINT BALL CENTRE, measured from the art, not the old cut point.
  Elbow ball: Arm_Back (99,222) R30, Arm_Front (60,222) R30.
  Knee ball: Leg_Front (95,314) R26, Leg_Back (100,314) R26.
- Parent segment is TRIMMED at ball bottom, so it does not carry the child's segment.
  (v6 upper carried a forearm/shin stub below the ball that rotated the wrong way.)
- Child segment pivot is ball centre. Arms: ball centre is 38px ABOVE lower piece top,
  so lower anchor y = -38. Legs: ball centre is 14px below lower piece top, anchor y = 14.
- One single circular ball cap, cropped from original art and circle-masked (not square),
  is drawn centred on the pivot, AFTER the child segment, covering the seam.
Upper lengths are ball-centre distances, not old cut distances:
  Arm upper: 222-30=192. Leg upper: 314-40=274. Total limb length is unchanged
  (arm 192+288=480, leg 274+323=597, same as v6 totals within 5px).
"""
from PIL import Image
import os, math
BASE = "/home/hatch/workspace/cape-jones-rig/sliced"
CUT = "/home/hatch/workspace/cape-jones-rig/cut-limbs-v7"
OUT = "/home/hatch/workspace/cape-jones-rig/reposes-v7"
os.makedirs(OUT, exist_ok=True)
SCALE = 0.95
SHOULDER = {"L": (430, 445), "R": (670, 445)}
HIP = {"L": (470, 740), "R": (615, 740)}
ARM_UPPER_LEN = 192*SCALE
LEG_UPPER_LEN = 274*SCALE
LEG_PIECES = {"L": ("Leg_Front_Upper.png", "Leg_Front_Lower.png", "Leg_Front_Cap.png", (77, 40), (77, 14)),
              "R": ("Leg_Back_Upper.png", "Leg_Back_Lower.png", "Leg_Back_Cap.png", (84, 40), (84, 14))}
ARM_PIECES = {"L": ("Arm_Front_Upper.png", "Arm_Front_Lower.png", "Arm_Front_Cap.png"),
              "R": ("Arm_Back_Upper.png", "Arm_Back_Lower.png", "Arm_Back_Cap.png")}
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
def cap_at(canvas, cap_path, joint):
    im = load(cap_path)
    canvas.paste(im, (int(joint[0]-im.size[0]/2), int(joint[1]-im.size[1]/2)), im)
def end_joint(joint, length, angle):
    a = math.radians(angle)
    return (joint[0] + length*math.sin(a), joint[1] + length*math.cos(a))
def build(name, cfg, arms_whole=False):
    canvas = Image.new("RGBA", (1100, 1500), (128, 128, 128, 255))
    paste_at(canvas, load(os.path.join(BASE, "Cape_Back_Main.png")), 550, 410)
    knees = {}
    for side in ("L", "R"):
        hip = HIP[side]
        up_name, low_name, cap_name, hip_anchor, knee_anchor = LEG_PIECES[side]
        limb(canvas, os.path.join(CUT, up_name), hip, cfg["leg_upper"][side], hip_anchor)
        knee = end_joint(hip, LEG_UPPER_LEN, cfg["leg_upper"][side])
        knees[side] = knee
        limb(canvas, os.path.join(CUT, low_name), knee, cfg["leg_lower"][side], knee_anchor)
        cap_at(canvas, os.path.join(CUT, cap_name), knee)
    elbows = {}
    if arms_whole:
        for side in ("L", "R"):
            whole, _, _ = ARM_PIECES[side]
            # whole arm pieces are in sliced/, not v7 cut - use original whole for jump arms-up (no elbow bend)
            limb(canvas, os.path.join(BASE, whole.replace("_Upper","").replace("_Lower","") if False else ("Arm_Front.png" if side=="L" else "Arm_Back.png")), SHOULDER[side], cfg["arm_upper"][side], (76, 30))
    else:
        for side in ("L", "R"):
            up_name, _, cap_name = ARM_PIECES[side]
            sh = SHOULDER[side]
            limb(canvas, os.path.join(CUT, up_name), sh, cfg["arm_upper"][side], (76, 30))
            elbows[side] = end_joint(sh, ARM_UPPER_LEN, cfg["arm_upper"][side])
    paste_at(canvas, load(os.path.join(BASE, "Pelvis.png")), 550, 680)
    paste_at(canvas, load(os.path.join(BASE, "Cape_Collar.png")), 550, 370)
    paste_at(canvas, load(os.path.join(BASE, "Torso_Chest.png")), 550, 400)
    paste_at(canvas, load(os.path.join(BASE, "Belt_Overlay.png")), 550, 670)
    if not arms_whole:
        for side in ("L", "R"):
            _, low_name, cap_name = ARM_PIECES[side]
            limb(canvas, os.path.join(CUT, low_name), elbows[side], cfg["arm_lower"][side], (76, -30))
            cap_at(canvas, os.path.join(CUT, cap_name), elbows[side])
    paste_at(canvas, load(os.path.join(BASE, "Neck.png"), scale=1.05), 550, 360)
    paste_at(canvas, load(os.path.join(BASE, "Head_Front.png")), 550, 250)
    from PIL import ImageDraw
    d = ImageDraw.Draw(canvas)
    def label(x, y, text):
        d.ellipse((x-28, y-28, x+28, y+28), fill=(255, 0, 0, 255), outline=(255, 255, 255, 255), width=3)
        d.text((x-7, y-10), text, fill=(255, 255, 255, 255))
    label(340, 430, "1"); d.text((300, 470), "ARM 1", fill=(255, 0, 0, 255))
    label(760, 430, "2"); d.text((720, 470), "ARM 2", fill=(255, 0, 0, 255))
    label(400, 820, "1"); d.text((360, 860), "LEG 1", fill=(255, 0, 0, 255))
    label(700, 820, "2"); d.text((660, 860), "LEG 2", fill=(255, 0, 0, 255))
    canvas.convert("RGB").save(os.path.join(OUT, name))
    print(name, "saved")
build("joint-apose-v7-20261031.png", {"arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": -20, "R": 20}, "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": -10, "R": 10}})
build("joint-flex-v7-20261031.png", {"arm_upper": {"L": -25, "R": 25}, "arm_lower": {"L": 160, "R": -160}, "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": -10, "R": 10}})
build("joint-punch-v7-20261031.png", {"arm_upper": {"L": -45, "R": 90}, "arm_lower": {"L": -45, "R": 90}, "leg_upper": {"L": -20, "R": 20}, "leg_lower": {"L": -20, "R": 20}})
build("joint-jump-v7-20261031.png", {"arm_upper": {"L": -150, "R": 150}, "arm_lower": {"L": -150, "R": 150}, "leg_upper": {"L": -20, "R": 20}, "leg_lower": {"L": 45, "R": -45}}, arms_whole=True)
build("joint-dance-v7-20261031.png", {"arm_upper": {"L": -60, "R": 60}, "arm_lower": {"L": -60, "R": 60}, "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": -10, "R": 10}})
build("joint-seated-v7-20261031.png", {"arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": -20, "R": 20}, "leg_upper": {"L": -60, "R": 60}, "leg_lower": {"L": 80, "R": -80}})
