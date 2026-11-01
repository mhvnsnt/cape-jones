#!/usr/bin/env python3
"""SIT-CHAIR MOVES + FIST REMOVAL + MODEL SCALE 5%, Mars 2026-11-01 01:00 CST.
Replying to hands scaled down 25% image:
  "Scale the mile by 5%. And also remove the fists from underneath them.
   The fists should be separate pieces and easy to just remove.
   The bottom two shins move them to the left 30 pixels.
   The two floating kneecaps move them to the left 15 pixels. And move
   them up 10 pixels. Move the pelvis to the left 20 pixels."

ASSUMPTION, stated plainly: 'mile' read as MODEL. The whole figure/model
is scaled UP 5% (1.05x), feet kept planted at y=1475. If Mars meant a
different piece, only that one scale needs redoing.

FIST REMOVAL, method, stated plainly (no lie):
  The v7c front lower PNGs (Arm_Front_Lower / Arm_Back_Lower) do NOT ship
  a separate fist file - the fist is the bottom portion of that one
  drawing. Previous builds drew that whole piece, then covered the fist
  with the open hand (which is why a sliver peeked out).
  In THIS builder the fist is treated as its own layer: the lower piece
  is split at the builder's existing wrist line (75% of the hand_end
  vector, the same wrist point every earlier builder used) into
  forearm-layer + fist-layer, and the fist layer is simply NOT drawn.
  No pixels are erased from the final figure, no hand is cropped or
  split, no fist is drawn underneath the open hand. The open hand is
  drawn whole, at the same centres as the scaledown build.
  If Mars wants a pre-cut gauntlet-only file saved separately, that is
  a one-line follow-up: pieces/forearm_no_fist_L.png / _R.png are the
  forearm layers used here (saved in this folder).

MOVES (base coordinates, before the 1.05x model scale):
  - Pelvis: cx 693 -> 673 (dx -20)
  - Shins, both: anchor = knee + (-30, 0) (dx -30 from the knee)
  - Kneecaps, both: old knee+(-10,-5) plus new (-15,-10) = knee+(-25,-15)
  - Hands: scaledown 1.0875x kept; after model scale, final hand scale
    = 1.0875 * 1.05 = 1.141875x native.
  - Everything else kept from the attachment-fix build: Arm1 behind
    torso, raised shoulder (580,385), Arm2 RIGHT perfect (shoulder
    815,403, upper 15, lower 10), cape on shoulders back, collar locked
    (fused into torso, not moved), thighs/hips unchanged, torso/neck/
    head unchanged.
  - Note: shins moved -30 from their knees, so shin tops now sit 30px
    left of the knee centres by order (join offset, reported, not hidden).
    Pelvis moved -20 while hips stay at 625/745 - both hips still sit
    inside the shifted pelvis bbox (564-782), so the hip-pelvis join
    stays inside, just shifted.

MODEL SCALE: whole base figure resized 1.05x, then pasted so ground
stays at y=1475: scaled size 1470x1680, paste offset (-35,-74).
Feet: 1475*1.05-74 = 1475. Top: 195*1.05-74 = 131. In canvas.
"""
from PIL import Image, ImageDraw
import os, math, json, hashlib
import numpy as np

ROOT = os.path.expanduser("~/workspace/cape-jones-rig/rig-34-scale5-fist-remove-moves-20261101")
SRC = os.path.expanduser("~/workspace/cape-jones-rig/sitting-rig-34-20261101/pieces")
SLICED = os.path.expanduser("~/workspace/cape-jones-rig/sliced")
CUT = os.path.expanduser("~/workspace/cape-jones-rig/cut-limbs-v7c")
PREV = os.path.expanduser("~/workspace/cape-jones-rig/rig-34-hands-scale-down25-20261101")
S = 1.3; W, H = 1400, 1600
MODEL = 1.05; HAND_S = 1.0875

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

def load_front_lower_no_fist(side):
    """Return (forearm_layer, fist_layer_not_drawn).
    Split at the wrist line: 75% of the piece height from the top.
    The fist layer is saved for audit but NEVER composited."""
    name = "Arm_Front_Lower.png" if side == "L" else "Arm_Back_Lower.png"
    im = Image.open(os.path.join(CUT, name)).convert("RGBA")
    im = im.resize((int(im.width * 0.95), int(im.height * 0.95)), Image.LANCZOS)
    cut = int(im.height * 0.75)
    forearm = im.crop((0, 0, im.width, cut))
    fist = im.crop((0, cut, im.width, im.height))
    forearm.save(f"{ROOT}/pieces/forearm_no_fist_{side}.png")
    fist.save(f"{ROOT}/pieces/fist_OMITTED_{side}.png")
    return forearm, fist

def load_neck():
    im = Image.open(os.path.join(SLICED, "Neck.png")).convert("RGBA")
    bb = im.split()[3].getbbox(); crop = im.crop(bb)
    nw = 101; nh = int(round(crop.height * nw / crop.width))
    return crop.resize((nw, nh), Image.LANCZOS)

def front_forearm_no_fist(canvas, fa, fa_anchor, angle, side):
    """v7c ball-centre anchor, fist layer omitted. Returns wrist, hand_end."""
    ball_x = {"L": 60 * 0.95, "R": 99 * 0.95}[side]
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(fa, (int(fa_anchor[0] - ball_x), int(fa_anchor[1] - 30)))
    layer = layer.rotate(angle, center=fa_anchor, expand=False, resample=Image.BICUBIC)
    canvas.alpha_composite(layer)
    cap_name = "Arm_Front_Cap.png" if side == "L" else "Arm_Back_Cap.png"
    cap = Image.open(os.path.join(CUT, cap_name)).convert("RGBA")
    cap = cap.resize((int(cap.width * 0.95), int(cap.height * 0.95)), Image.LANCZOS)
    canvas.alpha_composite(cap, (int(fa_anchor[0] - cap.width / 2), int(fa_anchor[1] - cap.height / 2)))
    # hand_end geometry from the FULL piece (needed for hand centres);
    # only the forearm portion is drawn.
    full_h = int(fa.height / 0.75)
    topa = {"L": 0.66, "R": 0.69}[side]
    hv = rot_vec(((0.20 - topa) * fa.width if side == "L" else (0.25 - topa) * fa.width,
                  full_h - 15), angle)
    hand_end = (fa_anchor[0] + hv[0], fa_anchor[1] + hv[1])
    wrist = (fa_anchor[0] + (hand_end[0] - fa_anchor[0]) * 0.75,
             fa_anchor[1] + (hand_end[1] - fa_anchor[1]) * 0.75)
    return wrist, hand_end

SHOULDER_R = (815, 403)   # Arm2 RIGHT, perfect, unchanged
SHOULDER_L = (580, 385)   # Arm1 LEFT, behind torso, raised (attachment fix)
HIP = {"L": (625, 780), "R": (745, 780)}
PELVIS_CX = 673           # was 693, dx -20
CFG = {"arm_upper": {"L": -15, "R": 15}, "arm_lower": {"L": -10, "R": 10},
       "leg_upper": {"L": -8, "R": 6}, "leg_lower": {"L": 0, "R": 0}}
BALL = {"L": 0.27, "R": 0.51}
SHIN_DX = -30
KNEECAP_OFF = (-25, -15)  # old (-10,-5) + new (-15,-10)

canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))

# 0. Cape back, shoulders on the back, collar locked (fused in torso).
cape = load34("cape_back.png"); paste_cx(canvas, cape, 700, 340)
cape_bbox = (700 - cape.width // 2, 340, 700 + cape.width // 2, 340 + cape.height)

# 1. Arm1 chain, BEHIND torso, forearm WITHOUT fist layer.
up_L = load34("upper_arm_L_socket.png")
limb(canvas, up_L, SHOULDER_L, CFG["arm_upper"]["L"])
vec = rot_vec((0, up_L.height - 15), CFG["arm_upper"]["L"])
off = rot_vec(((BALL["L"] - 0.5) * up_L.width, 0), CFG["arm_upper"]["L"])
elbow_L = (SHOULDER_L[0] + vec[0] + off[0], SHOULDER_L[1] + vec[1] + off[1])
fa_L, _fist_L = load_front_lower_no_fist("L")
wrist_L, hand_L = front_forearm_no_fist(canvas, fa_L, elbow_L, CFG["arm_lower"]["L"], "L")

# 2. Pelvis, moved left 20, before torso.
pelvis = load34("pelvis_belt.png"); paste_cx(canvas, pelvis, PELVIS_CX, 640)
pelvis_bbox = (PELVIS_CX - pelvis.width // 2, 640, PELVIS_CX + pelvis.width // 2, 640 + pelvis.height)

# 3. Thighs (unchanged anchors).
knees = {}
for side in ("L", "R"):
    thigh = load34("thigh_bent_L.png" if side == "L" else "thigh_bent_R.png")
    knees[side] = limb(canvas, thigh, HIP[side], CFG["leg_upper"][side])

# 4. Kneecaps, floating caps moved -15, -10 from their old spot.
caps = {}
for side in ("L", "R"):
    cap = load34("knee_ball_spare.png")
    cx = knees[side][0] + KNEECAP_OFF[0]; cy = knees[side][1] + KNEECAP_OFF[1]
    canvas.alpha_composite(cap, (int(cx - cap.width / 2), int(cy - cap.height / 2)))
    caps[side] = (cx, cy)

# 5. Shins, moved left 30 from the knees (anchor = knee + (-30,0)).
feet = {}
for side in ("L", "R"):
    shin = load34("shin_boot_L.png" if side == "L" else "shin_boot_mid.png")
    anchor = (knees[side][0] + SHIN_DX, knees[side][1])
    feet[side] = limb(canvas, shin, anchor, CFG["leg_lower"][side])

# 6. Torso, neck, head (unchanged).
torso = load34("torso.png"); paste_cx(canvas, torso, 700, 350)
torso_bbox = (700 - torso.width // 2, 350, 700 + torso.width // 2, 350 + torso.height)
paste_cx(canvas, load_neck(), 700, 330)
paste_cx(canvas, load34("head_cowl.png"), 700, 195)

# 9. Arm2 chain, in front, PERFECT, forearm WITHOUT fist layer.
up_R = load34("upper_arm_R.png")
limb(canvas, up_R, SHOULDER_R, CFG["arm_upper"]["R"])
vec = rot_vec((0, up_R.height - 15), CFG["arm_upper"]["R"])
off = rot_vec(((BALL["R"] - 0.5) * up_R.width, 0), CFG["arm_upper"]["R"])
elbow_R = (SHOULDER_R[0] + vec[0] + off[0], SHOULDER_R[1] + vec[1] + off[1])
fa_R, _fist_R = load_front_lower_no_fist("R")
wrist_R, hand_R = front_forearm_no_fist(canvas, fa_R,
                                        (elbow_R[0] - 7, elbow_R[1] - 5),
                                        CFG["arm_lower"]["R"], "R")

# 10. Separate open hands, scaledown 1.0875x, same centres as scaledown build.
#     Centres are the fist centres from the hands-replace build; the fist
#     itself is NOT drawn, so the hand is the only hand, no sliver.
fist_centres = {"L": (479, 791), "R": (909, 827)}
spare = Image.open(os.path.join(SRC, "hand_spare_L.png")).convert("RGBA")
spare = spare.resize((int(spare.width * HAND_S), int(spare.height * HAND_S)), Image.LANCZOS)
mirrored = spare.transpose(Image.FLIP_LEFT_RIGHT)
spare.save(f"{ROOT}/pieces/hand_arm1_10875.png"); mirrored.save(f"{ROOT}/pieces/hand_arm2_mirrored_10875.png")
hand_bboxes = {}
def place(hand, centre, angle):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(hand, (int(centre[0] - hand.width / 2), int(centre[1] - hand.height / 2)))
    layer = layer.rotate(angle, center=centre, expand=False, resample=Image.BICUBIC)
    canvas.alpha_composite(layer)
    a = np.array(layer)[:, :, 3]; ys, xs = np.where(a > 10)
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
hand_bboxes["L"] = place(spare, fist_centres["L"], 6)
hand_bboxes["R"] = place(mirrored, fist_centres["R"], 0)

# 11. MODEL SCALE 1.05x, feet kept planted at y=1475.
scaled = canvas.resize((int(W * MODEL), int(H * MODEL)), Image.LANCZOS)
final = Image.new("RGBA", (W, H), (0, 0, 0, 0))
OX, OY = -35, -74
final.alpha_composite(scaled, (OX, OY))
def tf(pt):
    return [round(pt[0] * MODEL + OX, 1), round(pt[1] * MODEL + OY, 1)]
def tf_bbox(bb):
    xs = [bb[0] * MODEL + OX, bb[2] * MODEL + OX]; ys = [bb[1] * MODEL + OY, bb[3] * MODEL + OY]
    return [int(min(xs)), int(min(ys)), int(max(xs)), int(max(ys))]

final.save(f"{ROOT}/poses/sit-chair-scale5-fist-removed-20261101.png")
grey = Image.new("RGBA", final.size, (126, 126, 126, 255)); grey.alpha_composite(final)
grey.convert("RGB").save(f"{ROOT}/poses/sit-chair-scale5-fist-removed-20261101-on-grey.png")

# Gates on the final figure.
a = np.array(final)[:, :, 3]; ys, xs = np.where(a > 10)
bbox = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
def bottom_in_band(x0, x1):
    sub = a[:, x0:x1]; yy, _ = np.where(sub > 10)
    return int(yy.max()) if len(yy) else None
feet_bottom = {"L": bottom_in_band(450, 700), "R": bottom_in_band(700, 950)}
gates = {
    "assumption_mile": "READ AS MODEL: whole figure scaled UP 1.05x, feet planted at 1475. If Mars meant a different piece, only that scale needs redoing.",
    "model_scale": MODEL, "paste_offset": [OX, OY],
    "pelvis": {"old_cx": 693, "new_cx": PELVIS_CX, "dx": -20, "bbox_base": list(pelvis_bbox), "bbox_final": tf_bbox(pelvis_bbox)},
    "shins": {"dx_from_knee": SHIN_DX, "note": "Shin tops now sit 30px left of knee centres by order - join offset, not hidden."},
    "kneecaps": {"old_off_from_knee": [-10, -5], "move": [-15, -10], "new_off_from_knee": list(KNEECAP_OFF),
                 "caps_base": {k: [round(v[0], 1), round(v[1], 1)] for k, v in caps.items()},
                 "caps_final": {k: tf(v) for k, v in caps.items()}},
    "knees_base": {k: [round(v[0], 1), round(v[1], 1)] for k, v in knees.items()},
    "fists": {"drawn": 0, "method": "Fist treated as its own layer at the wrist line (75% of lower-piece height); that layer was NOT composited. Fist audit files in pieces/fist_OMITTED_L.png and _R.png are the omitted layers, saved for audit, not drawn.",
              "source_note": "v7c lower PNGs ship no separate fist file; the fist is the bottom portion of that drawing. No pixels were erased from the final figure, no hand was cropped/split, no fist is drawn underneath the open hand."},
    "hands": {"count": 2, "scale_before_model": HAND_S, "scale_after_model": round(HAND_S * MODEL, 6),
              "centres_base": fist_centres, "centres_final": {k: tf(v) for k, v in fist_centres.items()},
              "bboxes_base": hand_bboxes, "bboxes_final": {k: tf_bbox(v) for k, v in hand_bboxes.items()},
              "arm1_left": "hand_spare_L as-is, rotate +6, thumb east/right",
              "arm2_right": "hand_spare_L MIRRORED, rotate 0, thumb west/left, opposite Arm 1"},
    "arm2_right_perfect": {"shoulder": list(SHOULDER_R), "moved_except_ordered": "Arm2 hand fist removal applies; Arm2 arm itself unchanged."},
    "arm1_left": {"shoulder": list(SHOULDER_L), "layer": "BEHIND torso"},
    "bbox_final": bbox, "feet_alpha_bottom": feet_bottom,
    "ground": 1475, "inside_canvas": bool(xs.min() >= 0 and ys.min() >= 0 and xs.max() < W and ys.max() < H),
    "knee_shin_gap_note": "Pre-existing knee/shin centre-column gap from the attachment fix is unchanged in kind; shin move -30 shifts it left, it does not close it. Not silently fixed.",
    "prev_untouched": {"scaledown_pose_md5": md5(f"{PREV}/poses/sit-chair-hands-scaledown25-20261101.png")},
}
json.dump(gates, open(f"{ROOT}/gates-20261101.json", "w"), indent=2)

# Contacts: old vs new, both hands, hand zooms (final coords).
full = grey.convert("RGB")
old_im = Image.open(f"{PREV}/poses/sit-chair-hands-scaledown25-20261101-on-grey.png").convert("RGB")
for im in (old_im, full): im.thumbnail((700, 800))
contact = Image.new("RGB", (2 * 710, 840), (30, 30, 30)); d = ImageDraw.Draw(contact)
d.text((10, 10), "OLD hands 1.0875x, fists underneath, pelvis 693", fill="white")
d.text((720, 10), "NEW model 1.05x, NO fists, pelvis 673, shins -30, caps -15/-10", fill="white")
contact.paste(old_im, (5, 40)); contact.paste(full, (715, 40))
contact.save(f"{ROOT}/contacts/old-vs-new-scale5-fist-removed-20261101.png")

def zoom(box, out, label):
    c = full.crop(box); c = c.resize((c.width * 2, c.height * 2), Image.NEAREST)
    sheet = Image.new("RGB", (c.width, c.height + 30), (30, 30, 30))
    ImageDraw.Draw(sheet).text((10, 8), label, fill="white"); sheet.paste(c, (0, 30)); sheet.save(out)
hc_L = tf(fist_centres["L"]); hc_R = tf(fist_centres["R"])
zoom((int(hc_L[0]) - 100, int(hc_L[1]) - 140, int(hc_L[0]) + 100, int(hc_L[1]) + 160),
     f"{ROOT}/contacts/hand1-new-zoom-20261101.png", "Arm1 LEFT open hand, NO fist underneath")
zoom((int(hc_R[0]) - 100, int(hc_R[1]) - 140, int(hc_R[0]) + 100, int(hc_R[1]) + 160),
     f"{ROOT}/contacts/hand2-new-zoom-20261101.png", "Arm2 RIGHT open hand MIRRORED, NO fist underneath")
c1 = full.crop((int(hc_L[0]) - 100, int(hc_L[1]) - 140, int(hc_L[0]) + 100, int(hc_L[1]) + 160))
c2 = full.crop((int(hc_R[0]) - 100, int(hc_R[1]) - 140, int(hc_R[0]) + 100, int(hc_R[1]) + 160))
sheet = Image.new("RGB", (c1.width + c2.width + 20, max(c1.height, c2.height) + 30), (30, 30, 30)); d = ImageDraw.Draw(sheet)
d.text((10, 8), "Arm1 LEFT hand, no fist", fill="white"); d.text((c1.width + 20, 8), "Arm2 RIGHT hand mirrored, no fist", fill="white")
sheet.paste(c1, (0, 30)); sheet.paste(c2, (c1.width + 20, 30)); sheet.save(f"{ROOT}/contacts/both-hands-new-20261101.png")
print(json.dumps(gates, indent=2))
