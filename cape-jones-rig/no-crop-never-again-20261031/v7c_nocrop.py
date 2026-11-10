#!/usr/bin/env python3
"""Full-scene migrated v7c apose, NO-CROP version, 2026-10-31.

Original: joint_locked_rig_v7c.py (NOT edited, NOT overwritten).
Migration principle (pad-canvas + trim, from no_crop.py):
  - Canvas starts padded: (1100+2*PAD, 1500+2*PAD), transparent.
  - Every absolute coordinate (shoulder, hip, paste centre, cap centre,
    joint) is shifted by +PAD, so the original limb() rotate with
    expand=False is safe: the pad holds the swing.
  - At save, trim to alpha bbox + 40px. Trimming transparent pixels
    is not cropping the figure.
  - Labels OFF (clean mode only), canvas transparent (not grey 128),
    so check_no_clip.py can actually PASS. The original grey canvas
    has alpha on every edge by construction and can never pass the
    alpha gate -- that is why the grey canvas is flagged in the
    migration table, not silently kept.
Pose: apose config from v7c.py, labels=False.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from no_crop import trim, edge_touch, margins

BASE = "/home/hatch/workspace/cape-jones-rig/sliced"
CUT = "/home/hatch/workspace/cape-jones-rig/cut-limbs-v7c"
OUT = "/home/hatch/workspace/cape-jones-rig/no-crop-never-again-20261031/renders/fullscene"
PAD = 400
SCALE = 0.95
SHOULDER = {"L": (430 + PAD, 445 + PAD), "R": (670 + PAD, 445 + PAD)}
HIP = {"L": (470 + PAD, 740 + PAD), "R": (615 + PAD, 740 + PAD)}
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
LEG = {"L": ((95, 314), (77, 40)), "R": ((100, 314), (84, 40))}
LEG_PIECES = {"L": ("Leg_Front_Upper.png", "Leg_Front_Lower.png", "Leg_Front_Cap.png"),
              "R": ("Leg_Back_Upper.png", "Leg_Back_Lower.png", "Leg_Back_Cap.png")}
ARM_PIECES = {"L": ("Arm_Front_Upper.png", "Arm_Front_Lower.png", "Arm_Front_Cap.png"),
              "R": ("Arm_Back_Upper.png", "Arm_Back_Lower.png", "Arm_Back_Cap.png")}


def load(p, scale=SCALE):
    im = Image.open(p).convert("RGBA")
    return im.resize((int(im.size[0] * scale), int(im.size[1] * scale)), Image.LANCZOS)


def paste_at(c, im, cx, top):
    c.paste(im, (int(cx - im.size[0] / 2), int(top)), im)


def limb(c, path, joint, angle, anchor):
    im = load(path); ax, ay = anchor[0] * SCALE, anchor[1] * SCALE
    layer = Image.new("RGBA", (1100 + 2 * PAD, 1500 + 2 * PAD), (0, 0, 0, 0))
    layer.paste(im, (int(joint[0] - ax), int(joint[1] - ay)), im)
    layer = layer.rotate(angle, center=joint, expand=False)  # safe: PAD holds the swing
    c.alpha_composite(layer)


def cap_at(c, path, joint):
    im = load(path)
    c.paste(im, (int(joint[0] - im.size[0] / 2), int(joint[1] - im.size[1] / 2)), im)


def rot_vec(v, angle_deg):
    a = math.radians(angle_deg); x, y = v
    return (x * math.cos(a) + y * math.sin(a), -x * math.sin(a) + y * math.cos(a))


def build(name, cfg):
    canvas = Image.new("RGBA", (1100 + 2 * PAD, 1500 + 2 * PAD), (0, 0, 0, 0))
    paste_at(canvas, load(os.path.join(BASE, "Cape_Back_Main.png")), 550 + PAD, 410 + PAD)
    for side in ("L", "R"):
        hip = HIP[side]; ball, hip_anchor = LEG[side]
        vec = (ball[0] - hip_anchor[0], ball[1] - hip_anchor[1])
        up, low, cap = LEG_PIECES[side]
        limb(canvas, os.path.join(CUT, up), hip, cfg["leg_upper"][side], hip_anchor)
        knee = (hip[0] + rot_vec(vec, cfg["leg_upper"][side])[0] * SCALE,
                hip[1] + rot_vec(vec, cfg["leg_upper"][side])[1] * SCALE)
        limb(canvas, os.path.join(CUT, low), knee, cfg["leg_lower"][side], (ball[0], 0))
        cap_at(canvas, os.path.join(CUT, cap), knee)
    elbows = {}
    for side in ("L", "R"):
        ball, sh_anchor = ARM[side]; vec = (ball[0] - sh_anchor[0], ball[1] - sh_anchor[1])
        up, _, _ = ARM_PIECES[side]; sh = SHOULDER[side]
        limb(canvas, os.path.join(CUT, up), sh, cfg["arm_upper"][side], sh_anchor)
        elbows[side] = (sh[0] + rot_vec(vec, cfg["arm_upper"][side])[0] * SCALE,
                        sh[1] + rot_vec(vec, cfg["arm_upper"][side])[1] * SCALE)
    paste_at(canvas, load(os.path.join(BASE, "Pelvis.png")), 550 + PAD, 680 + PAD)
    paste_at(canvas, load(os.path.join(BASE, "Cape_Collar.png")), 550 + PAD, 370 + PAD)
    paste_at(canvas, load(os.path.join(BASE, "Torso_Chest.png")), 550 + PAD, 400 + PAD)
    paste_at(canvas, load(os.path.join(BASE, "Belt_Overlay.png")), 550 + PAD, 670 + PAD)
    for side in ("L", "R"):
        _, low, cap = ARM_PIECES[side]; ball, _ = ARM[side]
        limb(canvas, os.path.join(CUT, low), elbows[side], cfg["arm_lower"][side], (ball[0], 0))
        cap_at(canvas, os.path.join(CUT, cap), elbows[side])
    paste_at(canvas, load(os.path.join(BASE, "Neck.png"), scale=1.05), 550 + PAD, 360 + PAD)
    paste_at(canvas, load(os.path.join(BASE, "Head_Front.png")), 550 + PAD, 250 + PAD)
    out = trim(canvas, pad=40)
    os.makedirs(OUT, exist_ok=True)
    out.save(os.path.join(OUT, name))
    print(name, out.size, "edge", edge_touch(out), "margins", margins(out),
          "gate", "PASS" if all(v == 0 for v in edge_touch(out).values()) else "FAIL")
    return out


if __name__ == "__main__":
    build("v7c-apose-nocrop-20261031.png",
          {"arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": -20, "R": 20},
           "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": -10, "R": 10}})
    # extreme-pose stress: arms/legs swung far, the case that clips on a fixed canvas
    build("v7c-extreme-nocrop-20261031.png",
          {"arm_upper": {"L": -160, "R": 160}, "arm_lower": {"L": 160, "R": -160},
           "leg_upper": {"L": -60, "R": 60}, "leg_lower": {"L": 80, "R": -80}})
