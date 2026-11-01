"""Snap-aware figure builder — the pipeline's render step for snap poses.
Layer passes, per arm, never a whole-pose blanket reorder:
  normal pass:  upper before torso/collar, lower after torso, before head
  chest pass:   whole chain after torso, BEFORE head   (torso < arm < head)
  cowl pass:    UPPER ONLY after collar/torso, lower stays normal
                (bicep above collar; lower never lifted over the head
                by a cowl snap — whole-chain cowl is BANNED, JoJo 02 L)
  face pass:    whole chain AFTER head                 (torso < head < arm)
Use check_pose_snap.py FIRST to get the decision per side, then pass it
here as snap={"L": "cowl", "R": "chest"} etc. Approved-pose builders are
NOT edited by this file; this is the builder new poses use, and the
reference implementation of the snap for Harmony/Animate/Tahoma ports
(see INDUSTRY-LAYERING-METHODS-20261031.md for the per-tool mapping).
Same v7c pieces, same angles, no redrawn art.
"""
import os, math
from PIL import Image
BASE = "/home/hatch/workspace/cape-jones-rig/sliced"
CUT = "/home/hatch/workspace/cape-jones-rig/cut-limbs-v7c"
SCALE = 0.95
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
LEG = {"L": ((95, 314), (77, 40)), "R": ((100, 314), (84, 40))}
LEG_PIECES = {"L": ("Leg_Front_Upper.png", "Leg_Front_Lower.png", "Leg_Front_Cap.png"),
              "R": ("Leg_Back_Upper.png", "Leg_Back_Lower.png", "Leg_Back_Cap.png")}
ARM_PIECES = {"L": ("Arm_Front_Upper.png", "Arm_Front_Lower.png", "Arm_Front_Cap.png"),
              "R": ("Arm_Back_Upper.png", "Arm_Back_Lower.png", "Arm_Back_Cap.png")}

def load(p, scale=SCALE):
    im = Image.open(p).convert("RGBA")
    return im.resize((max(1, int(im.size[0] * scale)), max(1, int(im.size[1] * scale))), Image.LANCZOS)

def paste_at(c, im, cx, top):
    c.alpha_composite(im, (int(cx - im.size[0] / 2), int(top)))

def limb(c, path, joint, angle, anchor):
    im = load(path); ax, ay = anchor[0] * SCALE, anchor[1] * SCALE
    layer = Image.new("RGBA", c.size, (0, 0, 0, 0))
    layer.alpha_composite(im, (int(joint[0] - ax), int(joint[1] - ay)))
    layer = layer.rotate(angle, center=joint, expand=False); c.alpha_composite(layer)

def cap_at(c, path, joint):
    im = load(path); c.alpha_composite(im, (int(joint[0] - im.size[0] / 2), int(joint[1] - im.size[1] / 2)))

def rot_vec(v, a):
    r = math.radians(a); x, y = v
    return (x * math.cos(r) + y * math.sin(r), -x * math.sin(r) + y * math.cos(r))

def figure(cx, cfg, head_angle=0, snap=None):
    snap = snap or {}
    c = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    paste_at(c, load(os.path.join(BASE, "Cape_Back_Main.png")), cx, 410)
    hips = {"L": (cx - 80, 740), "R": (cx + 65, 740)}
    shoulders = {"L": (cx - 120, 445), "R": (cx + 120, 445)}
    for side in ("L", "R"):
        hip = hips[side]; ball, hip_anchor = LEG[side]
        vec = (ball[0] - hip_anchor[0], ball[1] - hip_anchor[1])
        up, low, cap = LEG_PIECES[side]
        limb(c, os.path.join(CUT, up), hip, cfg["leg_upper"][side], hip_anchor)
        knee = (hip[0] + rot_vec(vec, cfg["leg_upper"][side])[0] * SCALE,
                hip[1] + rot_vec(vec, cfg["leg_upper"][side])[1] * SCALE)
        limb(c, os.path.join(CUT, low), knee, cfg["leg_lower"][side], (ball[0], 0))
        cap_at(c, os.path.join(CUT, cap), knee)
    elbows = {}
    for side in ("L", "R"):
        ball, sh_anchor = ARM[side]
        vec = (ball[0] - sh_anchor[0], ball[1] - sh_anchor[1])
        up, _, _ = ARM_PIECES[side]; sh = shoulders[side]
        elbows[side] = (sh[0] + rot_vec(vec, cfg["arm_upper"][side])[0] * SCALE,
                        sh[1] + rot_vec(vec, cfg["arm_upper"][side])[1] * SCALE)
        if snap.get(side) in ("face", "cowl", "chest"):
            continue  # drawn in its snap pass below, not here
        limb(c, os.path.join(CUT, up), sh, cfg["arm_upper"][side], sh_anchor)
    paste_at(c, load(os.path.join(BASE, "Pelvis.png")), cx, 680)
    paste_at(c, load(os.path.join(BASE, "Cape_Collar.png")), cx, 370)
    paste_at(c, load(os.path.join(BASE, "Torso_Chest.png")), cx, 400)
    paste_at(c, load(os.path.join(BASE, "Belt_Overlay.png")), cx, 670)
    for side in ("L", "R"):
        if snap.get(side) in ("face",):
            continue
        _, low, cap = ARM_PIECES[side]; ball, _ = ARM[side]
        limb(c, os.path.join(CUT, low), elbows[side], cfg["arm_lower"][side], (ball[0], 0))
        cap_at(c, os.path.join(CUT, cap), elbows[side])
    for side in ("L", "R"):  # chest pass: whole chain, above torso, below head
        if snap.get(side) == "chest":
            up, low, cap = ARM_PIECES[side]; ball, sh_anchor = ARM[side]; sh = shoulders[side]
            limb(c, os.path.join(CUT, up), sh, cfg["arm_upper"][side], sh_anchor)
            limb(c, os.path.join(CUT, low), elbows[side], cfg["arm_lower"][side], (ball[0], 0))
            cap_at(c, os.path.join(CUT, cap), elbows[side])
    for side in ("L", "R"):  # cowl pass: UPPER ONLY above collar
        if snap.get(side) == "cowl":
            up, _, _ = ARM_PIECES[side]; ball, sh_anchor = ARM[side]; sh = shoulders[side]
            limb(c, os.path.join(CUT, up), sh, cfg["arm_upper"][side], sh_anchor)
    paste_at(c, load(os.path.join(BASE, "Neck.png"), scale=1.05), cx, 360)
    head_im = load(os.path.join(BASE, "Head_Front.png"))
    if head_angle:
        head_im = head_im.rotate(head_angle, expand=True)
    c.alpha_composite(head_im, (int(cx - head_im.size[0] / 2), int(331 - head_im.size[1] / 2)))
    for side in ("L", "R"):  # face pass: whole chain above head
        if snap.get(side) == "face":
            up, low, cap = ARM_PIECES[side]; ball, sh_anchor = ARM[side]; sh = shoulders[side]
            limb(c, os.path.join(CUT, up), sh, cfg["arm_upper"][side], sh_anchor)
            limb(c, os.path.join(CUT, low), elbows[side], cfg["arm_lower"][side], (ball[0], 0))
            cap_at(c, os.path.join(CUT, cap), elbows[side])
    return c
