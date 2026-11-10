#!/usr/bin/env python3
"""Cape Jones SIDE rig builder — 2026-11-01.

WHAT THIS IS
- A side (profile, facing-left default) view rig for Cape Jones, built as a
  NEW dated folder. RIG-00 front rig is read-only here and is never written.
- Piece honesty, per the standing rules (never claim a squashed front as a
  side; pivots measured from side art, not copied from front):
  * 1 piece is a SUBSTITUTION: side_head_cowl, cropped whole from the
    existing true side master (true-masters-20261031/02-true-master-side),
    native box (60,35)-(265,255), scaled x1.5, cut only at the shoulder
    line. Its bottom-right corner carries a fused cape-collar sliver from
    that same flat figure (the cape drape piece continues below it in
    assembly, so there is no gap). No squash, no mirror of a front head.
  * 17 pieces are NEW DRAWs: drawn at side proportions (narrow profile
    depth, NOT front widths scaled down) in the front-rig palette, traced
    to the side master's construction lines (head top, shoulder, waist,
    hip, knee, ankle, ground). Far-side pieces are new draws traced from
    the near silhouette and darkened (x0.72) — no native far-side drawing
    exists in the flat side reference (far limbs are hidden behind torso
    / cape there), so they are labelled stand-ins, not native art.
  * The front chest emblem is NOT drawn full-face on the side torso:
    in profile it is edge-on, so the torso carries only a narrow purple
    edge sliver at the chest front. A full diamond on a profile torso
    would be wrong and is not claimed.
- FK chains, pivots, layer order, ground gate, knee-feet rule and wrist
  rule follow the existing rig conventions (joint_locked_rig_v7c pivot =
  ball centre; sitting-rig-34 / wired-rig layer + gate pattern).

RUN: python3 build_side_rig.py
OUTPUTS: pieces/*.png, side-rig-manifest-20261101.json,
  poses/side-stand-left-20261101.png (+ -on-grey),
  poses/side-stand-right-20261101.png (mirror of left, stated),
  poses/side-walk-step-left-20261101.png (+ -on-grey),
  gates-20261101.json
"""
import json, math, os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.abspath(__file__))
PIECES = os.path.join(ROOT, "pieces")
POSE_DIR = os.path.join(ROOT, "poses")
os.makedirs(PIECES, exist_ok=True)
os.makedirs(POSE_DIR, exist_ok=True)

CANVAS = (1200, 1800)
GROUND = 1600
GREY = (128, 128, 128, 255)

# Front-rig palette, sampled from sliced/ pieces (see REPORT).
OUT = (10, 10, 12, 255)
SUIT = (254, 254, 254, 255)
SHADE = (178, 186, 199, 255)
PURPLE = (90, 40, 114, 255)
PURPLE_D = (66, 27, 84, 255)
CAPE = (22, 20, 25, 255)
CAPE_FOLD = (38, 34, 44, 255)
JOINT = (150, 155, 165, 255)
JOINT_C = (40, 40, 45, 255)

def dark(c, f=0.72):
    return (int(c[0]*f), int(c[1]*f), int(c[2]*f), 255)

def pal(far):
    if not far:
        return dict(suit=SUIT, shade=SHADE, purple=PURPLE, purple_d=PURPLE_D,
                    cape=CAPE, fold=CAPE_FOLD, out=OUT, joint=JOINT, jc=JOINT_C)
    return dict(suit=dark(SUIT), shade=dark(SHADE), purple=dark(PURPLE),
                purple_d=dark(PURPLE_D), cape=dark(CAPE), fold=dark(CAPE_FOLD),
                out=OUT, joint=dark(JOINT), jc=JOINT_C)

def capsule(d, x0, y0, x1, y1, fill, out, w=4):
    d.rounded_rectangle([x0, y0, x1, y1], radius=(x1-x0)//2, fill=fill,
                        outline=out, width=w)

def joint_cap(d, cx, cy, r, p):
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=p["joint"], outline=p["out"], width=4)
    d.ellipse([cx-r*0.45, cy-r*0.45, cx+r*0.45, cy+r*0.45],
              fill=p["jc"], outline=p["out"], width=2)

# ---------------------------------------------------------------- pieces
# Each draw function returns (image, pivot_fraction). Pivot = rotation centre.

def draw_torso(far=False):
    p = pal(far); W, H = 230, 530
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    # Narrow profile torso: shoulder top -> chest front (left) bulge -> waist.
    d.polygon([(60, 10), (170, 10), (195, 60), (185, 220), (175, 420),
               (170, 520), (55, 520), (45, 380), (35, 200), (40, 60)],
              fill=p["suit"], outline=p["out"], width=4)
    # Chest / abdomen construction lines.
    d.arc([30, 120, 180, 260], 200, 340, fill=p["shade"], width=4)
    d.arc([40, 300, 175, 420], 200, 340, fill=p["shade"], width=3)
    # Emblem EDGE-ON: narrow purple sliver at chest front only. NOT a diamond.
    d.polygon([(38, 150), (58, 150), (52, 300), (36, 300)], fill=p["purple"],
              outline=p["out"])
    # Shoulder shading (back side).
    d.polygon([(150, 15), (195, 60), (185, 220), (150, 220), (140, 60)],
              fill=p["shade"])
    d.line([(150, 15), (150, 220)], fill=p["out"], width=3)
    return im, (0.5, 0.97)   # pivot: waist bottom-centre

def draw_pelvis(far=False):
    p = pal(far); W, H = 220, 210
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(30, 10), (190, 10), (195, 150), (160, 200), (60, 200),
               (25, 150)], fill=p["suit"], outline=p["out"], width=4)
    # Belt band + front buckle panel + purple hip tab (front = left).
    d.rectangle([20, 55, 200, 115], fill=p["suit"], outline=p["out"], width=4)
    d.rectangle([28, 65, 78, 105], fill=p["shade"], outline=p["out"], width=3)
    d.polygon([(28, 115), (78, 115), (72, 160), (34, 160)], fill=p["purple"],
              outline=p["out"])
    return im, (0.5, 0.10)   # pivot: hip root, top-centre

def draw_upper_arm(far=False):
    p = pal(far); W, H = 150, 280
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    capsule(d, 25, 40, 125, 275, p["suit"], p["out"])
    d.ellipse([20, 5, 130, 115], fill=p["suit"], outline=p["out"], width=4)
    d.rectangle([60, 30, 115, 70], fill=p["shade"], outline=p["out"], width=3)
    d.line([(45, 150), (105, 150)], fill=p["shade"], width=3)
    return im, (0.5, 0.18)   # pivot: shoulder ball centre

def draw_forearm(far=False):
    p = pal(far); W, H = 120, 280
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    capsule(d, 20, 10, 100, 200, p["suit"], p["out"])
    # Gauntlet cuff with two panels (front-rig gauntlet language).
    d.rectangle([12, 185, 108, 272], fill=p["suit"], outline=p["out"], width=4)
    d.rectangle([28, 200, 92, 232], fill=p["shade"], outline=p["out"], width=3)
    d.rectangle([28, 238, 92, 260], fill=p["shade"], outline=p["out"], width=3)
    d.line([(30, 120), (90, 120)], fill=p["shade"], width=3)
    return im, (0.5, 0.08)   # pivot: elbow, top-centre

def draw_hand(far=False):
    p = pal(far); W, H = 120, 155
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    # Profile fist: curled fingers at bottom, thumb bump on inner side.
    d.rounded_rectangle([15, 10, 105, 130], radius=30, fill=p["suit"],
                        outline=p["out"], width=4)
    for i, x in enumerate([28, 48, 68]):
        d.arc([x, 95, x+28, 140], 0, 180, fill=p["out"], width=3)
    d.ellipse([78, 55, 112, 95], fill=p["suit"], outline=p["out"], width=3)
    return im, (0.5, 0.10)   # pivot: wrist, top-centre

def draw_thigh(far=False):
    p = pal(far); W, H = 150, 300
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(20, 10), (130, 10), (120, 290), (35, 290)], fill=p["suit"],
              outline=p["out"], width=4)
    d.ellipse([25, 5, 125, 85], fill=p["suit"], outline=p["out"], width=4)
    d.line([(40, 150), (110, 150)], fill=p["shade"], width=3)
    return im, (0.5, 0.10)   # pivot: hip, top-centre

def draw_shin(far=False):
    p = pal(far); W, H = 110, 260
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    capsule(d, 15, 10, 95, 250, p["suit"], p["out"])
    d.line([(30, 120), (80, 120)], fill=p["shade"], width=3)
    d.arc([25, 150, 85, 220], 200, 340, fill=p["shade"], width=3)
    return im, (0.5, 0.06)   # pivot: knee, top-centre

def draw_boot(far=False):
    p = pal(far); W, H = 230, 95
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    # Profile boot, toe LEFT (facing direction), heel block right, flat sole.
    d.polygon([(10, 55), (55, 25), (150, 15), (205, 25), (218, 55),
               (218, 82), (10, 82)], fill=p["suit"], outline=p["out"], width=4)
    d.rectangle([10, 68, 218, 82], fill=p["shade"], outline=p["out"], width=3)
    d.rectangle([168, 55, 218, 82], fill=p["shade"], outline=p["out"], width=3)
    d.ellipse([128, 5, 172, 49], fill=p["joint"], outline=p["out"], width=3)
    d.ellipse([142, 19, 158, 35], fill=p["jc"], outline=p["out"], width=2)
    return im, (0.65, 0.25)  # pivot: ankle circle centre

def draw_cape(far=False):
    p = pal(False); W, H = 300, 1080
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    # Side drape: hangs from shoulders behind the body, hem below knees.
    d.polygon([(20, 10), (180, 10), (230, 120), (260, 500), (275, 900),
               (250, 1060), (180, 1040), (110, 1060), (40, 1030),
               (10, 600), (5, 200)], fill=p["cape"], outline=p["out"], width=4)
    for x in [70, 130, 190]:
        d.line([(x, 60), (x+30, 1020)], fill=p["fold"], width=4)
    return im, (0.45, 0.02)  # pivot: shoulders, top-centre

def draw_cap(name, r):
    p = pal(False); d0 = r*2
    im = Image.new("RGBA", (d0, d0), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    joint_cap(d, r, r, r-3, p)
    return im, (0.5, 0.5)

def build_head_substitution():
    """SUBSTITUTION: whole crop from the true side master, x1.5, no squash."""
    src = os.path.expanduser(
        "~/workspace/cape-jones-rig/true-masters-20261031/"
        "02-true-master-side-20261031.png")
    im = Image.open(src).convert("RGBA").crop((60, 35, 265, 255))
    w, h = im.size
    im = im.resize((int(w*1.5), int(h*1.5)), Image.LANCZOS)
    # Trim the flat figure's shoulder-line cut: below 84% of the piece keep
    # only the neck column (frac 0.30-0.75), so the crop's straight bottom
    # edge does not draw a horizontal bar across the torso. The cape drape
    # piece (backmost layer) continues below the neck in assembly.
    W, H = im.size
    px = im.load()
    for y in range(int(H*0.84), H):
        for x in range(W):
            if not (int(W*0.30) <= x <= int(W*0.75)):
                px[x, y] = (0, 0, 0, 0)
    return im, (0.58, 0.89)  # pivot: neck base centre

PIECE_DEFS = [
    ("side_head_cowl", "SUBSTITUTION", build_head_substitution),
    ("side_torso", "NEW DRAW", lambda: draw_torso(False)),
    ("side_pelvis_belt", "NEW DRAW", lambda: draw_pelvis(False)),
    ("side_upper_arm_near", "NEW DRAW", lambda: draw_upper_arm(False)),
    ("side_forearm_gauntlet_near", "NEW DRAW", lambda: draw_forearm(False)),
    ("side_hand_fist_near", "NEW DRAW", lambda: draw_hand(False)),
    ("side_thigh_near", "NEW DRAW", lambda: draw_thigh(False)),
    ("side_shin_near", "NEW DRAW", lambda: draw_shin(False)),
    ("side_boot_near", "NEW DRAW", lambda: draw_boot(False)),
    ("side_cape_drape", "NEW DRAW", lambda: draw_cape(False)),
    ("side_upper_arm_far", "NEW DRAW (far-side stand-in, darkened)",
     lambda: draw_upper_arm(True)),
    ("side_forearm_gauntlet_far", "NEW DRAW (far-side stand-in, darkened)",
     lambda: draw_forearm(True)),
    ("side_hand_fist_far", "NEW DRAW (far-side stand-in, darkened)",
     lambda: draw_hand(True)),
    ("side_thigh_far", "NEW DRAW (far-side stand-in, darkened)",
     lambda: draw_thigh(True)),
    ("side_shin_far", "NEW DRAW (far-side stand-in, darkened)",
     lambda: draw_shin(True)),
    ("side_boot_far", "NEW DRAW (far-side stand-in, darkened)",
     lambda: draw_boot(True)),
    ("side_elbow_cap_near", "NEW DRAW", lambda: draw_cap("elbow", 32)),
    ("side_knee_cap_near", "NEW DRAW", lambda: draw_cap("knee", 35)),
]

def rot_xy(x, y, deg):
    """PIL rotate() is CCW-positive; a downward limb rotating CCW swings
    its foot toward the LEFT, i.e. forward for a left-facing figure.
    FK endpoint math must use the same convention."""
    r = math.radians(deg)
    return (x*math.cos(r) - y*math.sin(r), x*math.sin(r) + y*math.cos(r))

# Segment lengths (rig px) between pivots.
LEN = dict(upper=260, fore=260, thigh=280, shin=262)
# Boot geometry: boot piece alpha bottom is 58px below its ankle pivot, so
# a straight leg (hip 1000 + thigh 280 + shin 262 = ankle 1542) plants the
# boot bottom exactly on ground 1600. This is measured, not assumed.

def fk_chain(origin, angles, lengths):
    """Return joint points for a chain hanging down from origin.
    angles[i] = PIL-CCW degrees of segment i relative to its parent."""
    pts = [origin]; cum = 0.0
    for a, L in zip(angles, lengths):
        cum += a
        dx, dy = rot_xy(0, L, cum)
        pts.append((pts[-1][0]+dx, pts[-1][1]+dy))
    return pts

def paste_rotated(canvas, piece, pivot_frac, joint, deg):
    """Paste piece so its pivot lands on joint, rotated deg about the pivot."""
    pw, ph = piece.size
    px, py = pivot_frac[0]*pw, pivot_frac[1]*ph
    tmp = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    tmp.alpha_composite(piece, (int(joint[0]-px), int(joint[1]-py)))
    tmp = tmp.rotate(deg, center=(joint[0], joint[1]), resample=Image.BICUBIC)
    canvas.alpha_composite(tmp)
    # Rotated alpha bbox of this piece alone, for gates.
    a = tmp.getchannel("A").getbbox()
    return a

def assemble(pose):
    """pose: dict of joint angles (PIL-CCW deg, forward-left = positive).
    Returns (image, joints_dict, piece_bboxes)."""
    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    pieces = {}
    for name, _kind, fn in PIECE_DEFS:
        im, pf = fn()
        pieces[name] = (im, pf)
        if name == "side_head_cowl":
            im.save(os.path.join(PIECES, name + "-20261101.png"))
        else:
            im.save(os.path.join(PIECES, name + "-20261101.png"))
    # Anchors (rig px). Waist shared by pelvis; torso sits slightly forward
    # of the hip line so the chest front reads left of the near arm (as in
    # the side master, where the chest protrudes forward of the arm).
    waist = (600, 920)
    torso_joint = (565, 920)
    neck = (600, 400)
    shoulder_n = (600, 460); shoulder_f = (652, 460)
    hip_n = (600, 1000); hip_f = (616, 1000)
    cape_anchor = (640, 400)  # cape top tucks under neck/torso top (406)
    # FK joints.
    arm_n = fk_chain(shoulder_n, [pose["arm_n_up"], pose["arm_n_fore"]],
                     [LEN["upper"], LEN["fore"]])
    arm_f = fk_chain(shoulder_f, [pose["arm_f_up"], pose["arm_f_fore"]],
                     [LEN["upper"], LEN["fore"]])
    leg_n = fk_chain(hip_n, [pose["leg_n_thigh"], pose["leg_n_shin"]],
                     [LEN["thigh"], LEN["shin"]])
    leg_f = fk_chain(hip_f, [pose["leg_f_thigh"], pose["leg_f_shin"]],
                     [LEN["thigh"], LEN["shin"]])
    joints = dict(waist=waist, torso_joint=torso_joint, neck=neck,
                  shoulder_n=shoulder_n,
                  shoulder_f=shoulder_f, hip_n=hip_n, hip_f=hip_f,
                  elbow_n=arm_n[1], wrist_n=arm_n[2],
                  elbow_f=arm_f[1], wrist_f=arm_f[2],
                  knee_n=leg_n[1], ankle_n=leg_n[2],
                  knee_f=leg_f[1], ankle_f=leg_f[2])
    # Layer order, back to front (side view: far limbs behind torso,
    # near limbs in front of torso, head on top, cape backmost).
    order = [
        ("side_cape_drape", cape_anchor, 0),
        ("side_upper_arm_far", shoulder_f, pose["arm_f_up"]),
        ("side_forearm_gauntlet_far", arm_f[1],
         pose["arm_f_up"] + pose["arm_f_fore"]),
        ("side_hand_fist_far", arm_f[2],
         pose["arm_f_up"] + pose["arm_f_fore"] + pose["hand_f"]),
        ("side_thigh_far", hip_f, pose["leg_f_thigh"]),
        ("side_shin_far", leg_f[1],
         pose["leg_f_thigh"] + pose["leg_f_shin"]),
        ("side_boot_far", leg_f[2],
         pose["leg_f_thigh"] + pose["leg_f_shin"] + pose["boot_f"]),
        ("side_pelvis_belt", waist, 0),
        ("side_torso", torso_joint, pose["torso"]),
        ("side_thigh_near", hip_n, pose["leg_n_thigh"]),
        ("side_knee_cap_near", leg_n[1], 0),
        ("side_shin_near", leg_n[1],
         pose["leg_n_thigh"] + pose["leg_n_shin"]),
        ("side_boot_near", leg_n[2],
         pose["leg_n_thigh"] + pose["leg_n_shin"] + pose["boot_n"]),
        ("side_upper_arm_near", shoulder_n, pose["arm_n_up"]),
        ("side_elbow_cap_near", arm_n[1], 0),
        ("side_forearm_gauntlet_near", arm_n[1],
         pose["arm_n_up"] + pose["arm_n_fore"]),
        ("side_hand_fist_near", arm_n[2],
         pose["arm_n_up"] + pose["arm_n_fore"] + pose["hand_n"]),
        ("side_head_cowl", neck, pose["head"]),
    ]
    bboxes = {}
    for name, joint, deg in order:
        im, pf = pieces[name]
        bboxes[name] = paste_rotated(canvas, im, pf, joint, deg)
    return canvas, joints, bboxes

POSE_DEFS = {
    "side-stand-left": dict(torso=0, head=0,
        arm_n_up=2, arm_n_fore=4, hand_n=0,
        arm_f_up=2, arm_f_fore=4, hand_f=0,
        leg_n_thigh=0, leg_n_shin=0, boot_n=0,
        leg_f_thigh=0, leg_f_shin=0, boot_f=0),
    "side-walk-step-left": dict(torso=0, head=0,
        arm_n_up=-14, arm_n_fore=6, hand_n=0,   # near arm swings back
        arm_f_up=14, arm_f_fore=6, hand_f=0,    # far arm swings forward
        leg_n_thigh=24, leg_n_shin=-38, boot_n=14,  # near leg steps forward,
        # swing boot raised (knee bent forward-left, toe still left)
        leg_f_thigh=0, leg_f_shin=0, boot_f=0),     # far leg straight planted
    # NOTE: an earlier draft bent the planted leg's knee backward (+15.9
    # offset, toe-left) and the knee-feet gate correctly FAILED it. The
    # planted leg is straight here; only the swing leg bends, forward.
}

def check_gates(name, joints, bboxes, pose):
    g = {}
    # Ground gate: planted boots on ground; walk-step swing boot raised.
    for key, pname_ in [("boot_n", "side_boot_near"),
                        ("boot_f", "side_boot_far")]:
        bb = bboxes[pname_]
        g[key + "_bottom"] = bb[3] if bb else None
        g[key + "_on_ground"] = (bb is not None and abs(bb[3] - GROUND) <= 3)
    if name == "side-walk-step-left":
        # Swing (near) boot must be ABOVE ground, planted (far) boot ON it.
        g["swing_boot_raised"] = (bboxes["side_boot_near"][3] < GROUND - 20)
        g["planted_boot_on_ground"] = g["boot_f_on_ground"]
    # Knee-feet rule (profile form): toe direction is left by construction
    # (boot toe is the left end of the boot piece); knee must not point
    # right of the hip-ankle line. Straight knees pass.
    def knee_forward(hip, knee, ankle):
        # Signed horizontal offset of knee from the hip-ankle line.
        return knee[0] - (hip[0] + ankle[0]) / 2
    kn = knee_forward(joints["hip_n"], joints["knee_n"], joints["ankle_n"])
    kf = knee_forward(joints["hip_f"], joints["knee_f"], joints["ankle_f"])
    g["knee_n_offset"] = round(kn, 1); g["knee_f_offset"] = round(kf, 1)
    # Forward = left = negative x offset (knee left of midline) or ~straight.
    g["knee_feet_match_n"] = kn <= 5
    g["knee_feet_match_f"] = kf <= 5
    # Wrist rule: hands are placed exactly at FK wrist joints by construction;
    # gate records the wrist joints so a checker can verify no detachment.
    g["wrist_n"] = [round(v, 1) for v in joints["wrist_n"]]
    g["wrist_f"] = [round(v, 1) for v in joints["wrist_f"]]
    g["wrist_rule_by_construction"] = True
    # No-crop: every piece bbox inside canvas.
    g["all_inside_canvas"] = all(
        bb and 0 <= bb[0] and 0 <= bb[1] and bb[2] <= CANVAS[0]
        and bb[3] <= CANVAS[1] for bb in bboxes.values())
    g["canvas"] = CANVAS; g["ground_y"] = GROUND
    return g

def main():
    manifest = {"canvas": CANVAS, "ground_y": GROUND,
                "facing_default": "LEFT (toe-left, nose-left, matching model-side)",
                "front_rig_untouched": True, "no_push": True,
                "pieces": [], "chains": {
                    "spine": "pelvis -> torso -> head",
                    "arm_near": "shoulder_n -> elbow_n -> wrist_n -> hand_n",
                    "arm_far": "shoulder_f -> elbow_f -> wrist_f -> hand_f",
                    "leg_near": "hip_n -> knee_n -> ankle_n -> boot_n",
                    "leg_far": "hip_f -> knee_f -> ankle_f -> boot_f",
                    "cape": "parented to torso/shoulders, backmost layer, rotation 0"},
                "layer_order_back_to_front": [
                    "side_cape_drape", "side_upper_arm_far",
                    "side_forearm_gauntlet_far", "side_hand_fist_far",
                    "side_thigh_far", "side_shin_far", "side_boot_far",
                    "side_pelvis_belt", "side_torso", "side_thigh_near",
                    "side_knee_cap_near", "side_shin_near", "side_boot_near",
                    "side_upper_arm_near", "side_elbow_cap_near",
                    "side_forearm_gauntlet_near", "side_hand_fist_near",
                    "side_head_cowl"],
                "rules": {
                    "knee_feet": "In profile, knee direction and toe direction "
                        "must match: toe-left boots require knees forward-left "
                        "or straight, never right/back of the hip-ankle line "
                        "(except a deliberately broken leg named in the shot spec).",
                    "wrist": "Hand pivot sits exactly on the FK wrist joint "
                        "(forearm end); hands are never free-placed.",
                    "ground": "Planted boot bottom == ground y (1600) within 3px; "
                        "a swing boot in walk-step is raised, stated, not faked flat.",
                    "no_squash": "No front piece was squashed into a side piece. "
                        "Front emblem appears only as an edge sliver on the side torso."}}
    for pname, kind, fn in PIECE_DEFS:
        im, pf = fn()
        manifest["pieces"].append({
            "name": pname, "kind": kind,
            "file": f"pieces/{pname}-20261101.png",
            "size": list(im.size), "pivot_fraction": list(pf)})
    gates = {}
    for pname, pose in POSE_DEFS.items():
        img, joints, bboxes = assemble(pose)
        img.save(os.path.join(POSE_DIR, pname + "-20261101.png"))
        grey = Image.new("RGBA", CANVAS, GREY)
        grey.alpha_composite(img)
        grey.convert("RGB").save(os.path.join(POSE_DIR, pname + "-20261101-on-grey.png"))
        gates[pname] = check_gates(pname, joints, bboxes, pose)
        gates[pname]["joints"] = {k: [round(v, 1) for v in val]
                                  for k, val in joints.items()}
        gates[pname]["figure_alpha_bbox"] = list(
            img.getchannel("A").getbbox() or [])
        print(pname, "bbox", gates[pname]["figure_alpha_bbox"],
              "gates", {k: v for k, v in gates[pname].items()
                        if k not in ("joints",)})
    # Right-facing stand = horizontal mirror of the left stand (stated mirror,
    # not a new draw and not a re-rig: same pieces, same pivots, flipped).
    left = Image.open(os.path.join(POSE_DIR, "side-stand-left-20261101.png"))
    right = left.transpose(Image.FLIP_LEFT_RIGHT)
    right.save(os.path.join(POSE_DIR, "side-stand-right-20261101.png"))
    grey = Image.new("RGBA", CANVAS, GREY); grey.alpha_composite(right)
    grey.convert("RGB").save(os.path.join(
        POSE_DIR, "side-stand-right-20261101-on-grey.png"))
    gates["side-stand-right"] = {
        "method": "horizontal mirror of side-stand-left (stated, not a new draw)",
        "figure_alpha_bbox": list(right.getchannel("A").getbbox() or []),
        "all_inside_canvas": True}
    with open(os.path.join(ROOT, "side-rig-manifest-20261101.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    with open(os.path.join(ROOT, "gates-20261101.json"), "w") as f:
        json.dump(gates, f, indent=1)
    print("pieces:", len(manifest["pieces"]))

if __name__ == "__main__":
    main()
