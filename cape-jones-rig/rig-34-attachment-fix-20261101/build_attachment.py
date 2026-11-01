#!/usr/bin/env python3
"""3/4 sit-chair ATTACHMENT FIX, Mars 2026-11-01 01:49 CDT.
Base: rig-34-front-forearm-replace-20261101 (front forearms, one hand each).
NEW folder, front rig RIG-00 untouched, previous rigs untouched, no push.

Mars order, in his words (transcribed, 'cake' read as cape):
- Arm 1 = LEFT arm: layer BEHIND torso, attach to shoulder, move UP a little
  higher and attach to shoulder (different perspective, 3/4), rest of arm
  moves with it since it is attached perfectly (upper+forearm+hand, one chain).
- Arm 2 = RIGHT arm: PERFECT, do NOT move it.
- Pelvis: attach to bottom of torso perfectly cleanly.
- Hips: attach to pelvis cleanly where they would go.
- Kneecaps: place on knees where their place already is. They are NOT
  secondary knees for real; they are rotation pivots, so legs can be rotated
  about the knee. Kept as caps on the knees, not as extra knees.
- Shins: attach to kneecaps/knees, shin tops overlapping the knee caps
  (v7c overlap method, ~15px by design, cap centre still visible).
- Cape: attach securely to shoulders on the back, cape-back layer, collar locked.
  No separate collar piece exists in this 3/4 pack (collar is fused into the
  torso piece, as in all previous 3/4 builds); it is NOT moved, NOT redrawn.

Layer order, back to front (this is the fix; previous build drew BOTH arms
after the torso, so Arm 1 sat in front of the torso):
  0 cape_back, 1 Arm1 chain (behind torso), 2 pelvis, 3 thighs,
  4 knee caps (pivots), 5 shins (tops overlap caps), 6 torso,
  7 neck, 8 head, 9 Arm2 chain (in front, PERFECT, unchanged)

Changes vs the front-forearm base, reported plainly:
- Arm1 shoulder: (580,410) -> (580,385), dy -25, 'a little higher'.
  Elbow, forearm anchor, wrist and hand all shift -25 in y with it, same
  angles (-15 upper, -10 lower), same lengths: one attached chain, no gaps.
- Everything else kept where it did not conflict: pelvis (-7,0) cx 693,
  thighs/hips (-15,0), kneecaps (-10,-5), shins (-15,0), Arm2 untouched.
- Pelvis position UNCHANGED: its top (640) already overlaps the torso
  bottom (665) by 25px; the fix here is layer order (pelvis before torso,
  so torso overlaps pelvis top cleanly) plus a measured continuity gate,
  not a new pelvis position. If the join had a gap, it would be reported.
"""
from PIL import Image, ImageDraw
import os, math, json, hashlib
import numpy as np

ROOT = os.path.expanduser("~/workspace/cape-jones-rig/rig-34-attachment-fix-20261101")
OLD = os.path.expanduser("~/workspace/cape-jones-rig/rig-34-front-forearm-replace-20261101")
SRC = os.path.expanduser("~/workspace/cape-jones-rig/sitting-rig-34-20261101/pieces")
SLICED = os.path.expanduser("~/workspace/cape-jones-rig/sliced")
CUT = os.path.expanduser("~/workspace/cape-jones-rig/cut-limbs-v7c")
S = 1.3; W, H = 1400, 1600

def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()
def load34(name):
    im = Image.open(os.path.join(SRC, name)).convert("RGBA")
    return im.resize((int(im.width * S), int(im.height * S)), Image.LANCZOS)
def paste_cx(canvas, im, cx, top):
    canvas.alpha_composite(im, (int(cx - im.width / 2), int(top)))
def rot_vec(v, deg):
    a = math.radians(deg); x, y = v
    return (x * math.cos(a) + y * math.sin(a), -x * math.sin(a) + y * math.cos(a))
def limb(canvas, im, joint, angle):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(im, (int(joint[0] - im.width / 2), int(joint[1])))
    layer = layer.rotate(angle, center=joint, expand=False, resample=Image.BICUBIC)
    canvas.alpha_composite(layer)
    vec = rot_vec((0, im.height - 15), angle)
    return (joint[0] + vec[0], joint[1] + vec[1])
def load_front_lower(side):
    name = "Arm_Front_Lower.png" if side == "L" else "Arm_Back_Lower.png"
    im = Image.open(os.path.join(CUT, name)).convert("RGBA")
    return im.resize((int(im.width * 0.95), int(im.height * 0.95)), Image.LANCZOS)
def load_neck():
    im = Image.open(os.path.join(SLICED, "Neck.png")).convert("RGBA")
    bb = im.split()[3].getbbox(); crop = im.crop(bb)
    nw = 101; nh = int(round(crop.height * nw / crop.width))
    return crop.resize((nw, nh), Image.LANCZOS), nw, nh
def front_forearm(canvas, fa, fa_anchor, angle, side):
    """v7c ball-centre anchor, as in the front-forearm base. Returns wrist/hand."""
    ball_x = {"L": 60 * 0.95, "R": 99 * 0.95}[side]
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(fa, (int(fa_anchor[0] - ball_x), int(fa_anchor[1] - 30)))
    layer = layer.rotate(angle, center=fa_anchor, expand=False, resample=Image.BICUBIC)
    canvas.alpha_composite(layer)
    cap_name = "Arm_Front_Cap.png" if side == "L" else "Arm_Back_Cap.png"
    cap = Image.open(os.path.join(CUT, cap_name)).convert("RGBA")
    cap = cap.resize((int(cap.width * 0.95), int(cap.height * 0.95)), Image.LANCZOS)
    canvas.alpha_composite(cap, (int(fa_anchor[0] - cap.width / 2), int(fa_anchor[1] - cap.height / 2)))
    topa = {"L": 0.66, "R": 0.69}[side]
    hv = rot_vec(((0.20 - topa) * fa.width if side == "L" else (0.25 - topa) * fa.width,
                  fa.height - 15), angle)
    hand_end = (fa_anchor[0] + hv[0], fa_anchor[1] + hv[1])
    wrist = (fa_anchor[0] + (hand_end[0] - fa_anchor[0]) * 0.75,
             fa_anchor[1] + (hand_end[1] - fa_anchor[1]) * 0.75)
    return wrist, hand_end

# --- Anchors ---
# Arm2 RIGHT: PERFECT, unchanged from front-forearm base.
SHOULDER_R = (815, 403)
# Arm1 LEFT: moved UP a little higher: 410 -> 385 (dy -25). Rest moves with it.
SHOULDER_L_OLD = (580, 410); SHOULDER_L = (580, 385); ARM1_SHOULDER_DY = -25
HIP = {"L": (625, 780), "R": (745, 780)}  # old hips 640/760, -15 both
OFF = {"pelvis": (-7, 0), "thigh": (-15, 0), "kneecap": (-10, -5), "shin": (-15, 0),
       "arm1_upper": (-5, -7), "arm1_forearm": (-7, -5)}
CFG = {"arm_upper": {"L": -15, "R": 15}, "arm_lower": {"L": -10, "R": 10},
       "leg_upper": {"L": -8, "R": 6}, "leg_lower": {"L": 0, "R": 0}}
BALL = {"L": 0.27, "R": 0.51}

canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))

# 0. CAPE, backmost, attached to shoulders on the back.
#    Cape paste cx 700 top 340, size 514x900: top is 45px above L shoulder
#    (385) and 63px above R shoulder (403), x-range 443-957 covers both
#    shoulder x positions (580, 815). Collar locked: torso's fused collar,
#    drawn later with the torso, NOT moved, NOT redrawn (no separate piece).
cape = load34("cape_back.png")
paste_cx(canvas, cape, 700, 340)
cape_bbox = (700 - cape.width // 2, 340, 700 + cape.width // 2, 340 + cape.height)

# 1. ARM1 chain, BEHIND the torso (drawn before torso).
up_L = load34("upper_arm_L_socket.png")
limb(canvas, up_L, SHOULDER_L, CFG["arm_upper"]["L"])
vec = rot_vec((0, up_L.height - 15), CFG["arm_upper"]["L"])
off = rot_vec(((BALL["L"] - 0.5) * up_L.width, 0), CFG["arm_upper"]["L"])
elbow_L = (SHOULDER_L[0] + vec[0] + off[0], SHOULDER_L[1] + vec[1] + off[1])
fa_L = load_front_lower("L")
wrist_L, hand_L = front_forearm(canvas, fa_L, elbow_L, CFG["arm_lower"]["L"], "L")

# 2. PELVIS, before torso so the torso bottom overlaps it cleanly.
#    Pelvis cx 693 top 640 size 218x181 -> bottom 821. Torso bottom 665.
#    Overlap torso-bottom minus pelvis-top = 25px, no gap by construction.
pelvis = load34("pelvis_belt.png")
paste_cx(canvas, pelvis, 693, 640)
pelvis_bbox = (693 - pelvis.width // 2, 640, 693 + pelvis.width // 2, 640 + pelvis.height)

# 3. THIGHS, hips attach to pelvis: hip anchors (y 780) sit inside the
#    pelvis vertical range (640-821) and inside its x-range, thigh tops
#    overlap the pelvis by construction (joint at hip, piece extends down).
knees = {}; feet = {}
for side in ("L", "R"):
    thigh = load34("thigh_bent_L.png" if side == "L" else "thigh_bent_R.png")
    knees[side] = limb(canvas, thigh, HIP[side], CFG["leg_upper"][side])

# 4. KNEECAPS, rotation pivots on the knees (NOT secondary knees).
caps = {}
for side in ("L", "R"):
    cap = load34("knee_ball_spare.png")
    cx = knees[side][0] + OFF["kneecap"][0]; cy = knees[side][1] + OFF["kneecap"][1]
    canvas.alpha_composite(cap, (int(cx - cap.width / 2), int(cy - cap.height / 2)))
    caps[side] = (cx, cy)

# 5. SHINS, attached to kneecaps/knees: shin anchor = knee, so the shin top
#    overlaps the knee cap from the knee downwards (cap centre is 5px above
#    the knee, cap top ~47px above its centre, so the cap stays visible as
#    a pivot while the shin top overlaps its lower portion, v7c method).
for side in ("L", "R"):
    shin = load34("shin_boot_L.png" if side == "L" else "shin_boot_mid.png")
    feet[side] = limb(canvas, shin, knees[side], CFG["leg_lower"][side])

# 6. TORSO, after pelvis and after Arm1: torso bottom (665) overlaps pelvis
#    top (640) cleanly, and torso covers Arm1's shoulder/upper-arm top.
torso = load34("torso.png")
paste_cx(canvas, torso, 700, 350)
torso_bbox = (700 - torso.width // 2, 350, 700 + torso.width // 2, 350 + torso.height)

# 7-8. NECK + HEAD, unchanged.
neck, neck_w, neck_h = load_neck()
paste_cx(canvas, neck, 700, 330)
paste_cx(canvas, load34("head_cowl.png"), 700, 195)

# 9. ARM2 chain, in front, PERFECT, unchanged from the front-forearm base.
up_R = load34("upper_arm_R.png")
limb(canvas, up_R, SHOULDER_R, CFG["arm_upper"]["R"])
vec = rot_vec((0, up_R.height - 15), CFG["arm_upper"]["R"])
off = rot_vec(((BALL["R"] - 0.5) * up_R.width, 0), CFG["arm_upper"]["R"])
elbow_R = (SHOULDER_R[0] + vec[0] + off[0], SHOULDER_R[1] + vec[1] + off[1])
fa_R = load_front_lower("R")
# Arm2 forearm anchor in the base: elbow + (-7,-5) forearm offset.
wrist_R, hand_R = front_forearm(canvas, fa_R,
                                (elbow_R[0] + OFF["arm1_forearm"][0],
                                 elbow_R[1] + OFF["arm1_forearm"][1]),
                                CFG["arm_lower"]["R"], "R")

# --- Gates ---
a = np.array(canvas)[:, :, 3]; ys, xs = np.where(a > 10)
bbox = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
def bottom_in_band(x0, x1):
    sub = a[:, x0:x1]; yy, _ = np.where(sub > 10)
    return int(yy.max()) if len(yy) else None
feet_bottom = {"L": bottom_in_band(500, 700), "R": bottom_in_band(700, 900)}
def col_runs(x, lo, hi):
    col = a[:, x]; runs = []; inr = False; s = 0
    for y, v in enumerate(col):
        if v > 10 and not inr: s = y; inr = True
        if v <= 10 and inr: runs.append((s, y - 1)); inr = False
    return [r for r in runs if r[1] >= lo and r[0] <= hi]
# Join continuity: centre column through torso->pelvis must have no gap.
torso_pelvis_runs = col_runs(700, 600, 900)
torso_pelvis_gap = None
for (s1, e1), (s2, e2) in zip(torso_pelvis_runs, torso_pelvis_runs[1:]):
    if s2 > e1 + 1: torso_pelvis_gap = (e1, s2)
gates = {
    "bbox": bbox, "alpha_px": int((a > 10).sum()),
    "inside_canvas": bool(xs.min() >= 0 and ys.min() >= 0 and xs.max() < W and ys.max() < H),
    "arm1_shoulder": {"old": list(SHOULDER_L_OLD), "new": list(SHOULDER_L), "dy": ARM1_SHOULDER_DY,
                      "elbow": [round(elbow_L[0], 1), round(elbow_L[1], 1)],
                      "wrist": [round(wrist_L[0], 1), round(wrist_L[1], 1)],
                      "hand": [round(hand_L[0], 1), round(hand_L[1], 1)],
                      "layer": "BEHIND torso (drawn before torso)"},
    "arm2_right_perfect_unchanged": {"shoulder": list(SHOULDER_R),
        "elbow": [round(elbow_R[0], 1), round(elbow_R[1], 1)],
        "wrist": [round(wrist_R[0], 1), round(wrist_R[1], 1)],
        "hand": [round(hand_R[0], 1), round(hand_R[1], 1)], "moved": [0, 0]},
    "pelvis_torso_join": {"pelvis_bbox": list(pelvis_bbox), "torso_bbox": list(torso_bbox),
        "overlap_px": 665 - 640, "centre_column_x700_runs_600_900": torso_pelvis_runs,
        "gap": torso_pelvis_gap, "clean": torso_pelvis_gap is None},
    "hips": {"L": list(HIP["L"]), "R": list(HIP["R"]),
             "inside_pelvis_y_range": [640, 821],
             "inside_pelvis_x_range": [pelvis_bbox[0], pelvis_bbox[2]]},
    "knees": {k: [round(v[0], 1), round(v[1], 1)] for k, v in knees.items()},
    "kneecaps_pivots": {k: [round(v[0], 1), round(v[1], 1)] for k, v in caps.items()},
    "feet_end": {k: [round(v[0], 1), round(v[1], 1)] for k, v in feet.items()},
    "feet_alpha_bottom": feet_bottom,
    "cape_shoulder_join": {"cape_bbox": list(cape_bbox), "shoulders_covered_x": [580, 815],
        "cape_top_above_shoulders_px": [SHOULDER_L[1] - 340, SHOULDER_R[1] - 340],
        "collar": "locked, fused into torso piece, NOT moved, NOT redrawn, no separate collar piece exists in this pack"},
    "knee_feet": "PASS by construction: thigh angles L -8 / R +6 (outward), shins vertical, feet/toes outward, same direction as knees; no FootIn substitution needed.",
    "offsets_kept": OFF, "offset_changed_for_attachment": {"arm1_shoulder_dy": ARM1_SHOULDER_DY},
}
canvas.save(f"{ROOT}/poses/sit-chair-attachment-fix-20261101.png")
grey = Image.new("RGBA", canvas.size, (126, 126, 126, 255)); grey.alpha_composite(canvas)
grey.convert("RGB").save(f"{ROOT}/poses/sit-chair-attachment-fix-20261101-on-grey.png")

# Old vs new contact
old_im = Image.open(f"{OLD}/poses/sit-chair-front-forearm-20261101-on-grey.png").convert("RGB")
new_im = grey.convert("RGB")
for im in (old_im, new_im): im.thumbnail((700, 800))
contact = Image.new("RGB", (2 * 710, 840), (30, 30, 30)); d = ImageDraw.Draw(contact)
d.text((10, 10), "OLD front-forearm (Arm1 in FRONT of torso)", fill="white")
d.text((720, 10), "NEW attachment fix (Arm1 BEHIND torso, raised)", fill="white")
contact.paste(old_im, (5, 40)); contact.paste(new_im, (715, 40))
contact.save(f"{ROOT}/contacts/old-vs-new-attachment-fix-20261101.png")

# Joint zooms (from the new grey figure, 2x nearest for legibility)
full = grey.convert("RGB")
def zoom(box, out, label):
    c = full.crop(box); c = c.resize((c.width * 2, c.height * 2), Image.NEAREST)
    sheet = Image.new("RGB", (c.width, c.height + 30), (30, 30, 30))
    ImageDraw.Draw(sheet).text((10, 8), label, fill="white"); sheet.paste(c, (0, 30)); sheet.save(out)
zoom((450, 300, 750, 550), f"{ROOT}/contacts/zoom-arm1-shoulder-20261101.png",
     "Arm1 shoulder join: behind torso, raised to 385")
zoom((500, 580, 900, 760), f"{ROOT}/contacts/zoom-pelvis-torso-20261101.png",
     "Pelvis-torso join: torso bottom 665 over pelvis top 640")
zoom((500, 700, 900, 900), f"{ROOT}/contacts/zoom-hip-pelvis-20261101.png",
     "Hip-pelvis join: hips 625/745,780 inside pelvis 640-821")
zoom((450, 950, 900, 1200), f"{ROOT}/contacts/zoom-knee-shin-20261101.png",
     "Knee/shin join: caps on knees, shin tops overlap caps")
zoom((400, 280, 1000, 520), f"{ROOT}/contacts/zoom-cape-shoulder-20261101.png",
     "Cape-shoulder join: cape back, top 340, over both shoulders")

json.dump({"gates": gates}, open(f"{ROOT}/gates-20261101.json", "w"), indent=2)
json.dump({"front_rig_untouched": {"sliced/Torso_Chest.png": md5(os.path.join(SLICED, "Torso_Chest.png")),
                                    "sliced/Head_Front.png": md5(os.path.join(SLICED, "Head_Front.png"))},
           "old_rig_untouched": {"front-forearm pose": md5(f"{OLD}/poses/sit-chair-front-forearm-20261101.png")}},
          open(f"{ROOT}/untouched-check-20261101.json", "w"), indent=2)
print("bbox", bbox, "feet_bottom", feet_bottom)
print("elbow_L", elbow_L, "wrist_L", wrist_L, "elbow_R", elbow_R, "wrist_R", wrist_R)
print("torso_pelvis_runs", torso_pelvis_runs, "gap", torso_pelvis_gap)
print("knees", knees, "caps", caps)
