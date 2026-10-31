"""Workstream C builder, 2026-10-31. Labels=False only. No recolour of base art
(except the opposition silhouette placeholder, which is a deliberate flat
silhouette kitbash, not Cape Jones art). No file here overwrites a version
Mars has seen; every output is a new dated file in this folder.

Method notes (see README in this folder for the full log):
- True flex: start from the APPROVED arms-up pose (upper -70/70, lower
  150/-150, elbows (253,493)/(849,487), FlexOut lowers). The fist is NOT
  rotated in piece space. It is rotated in POSE space: the forearm+gauntlet
  is drawn truncated at y=180, the fist crop (y>=165, FlexOut) is drawn as
  its own layer rotated about the POSE wrist point by arm_lower+roll, and
  an Arm cap (66px, same piece family as elbow/knee caps) is drawn centred
  on the pose wrist over the seam. Roll toward head = 75deg: L -75, R +75
  in PIL/rot_vec convention, so knuckles point toward the head, not up.
- Wrist pivot, piece coords: Front (57,175), Back (114,175) — gauntlet
  bottom / fist top, from alpha centreline (Front y170 centre 57, y180
  centre 63; Back y170 centre 115, y180 centre 114.5).
- Punch Arm2 variant: LOCKED -110 pose rebuilt clean (labels=False):
  upper L -90 / R 20, lower L -90 / R -110, legs -15/15. Arm2 (image-right,
  Arm_Back) keeps its exact shoulder/elbow/wrist. Its cuff is per-row
  mirrored (y62-180, per-row alpha span preserved, exactly the OutFixed
  method) and its baked side-profile fist is replaced by Hand_1_Fist
  (front-angle fist, a different angle) tilted -20deg about the wrist,
  knuckles up, with a wrist cap over the seam.
"""
from PIL import Image, ImageOps
import os, math, json

ROOT = "/home/hatch/workspace/cape-jones-rig"
BASE = os.path.join(ROOT, "sliced")
CUT = os.path.join(ROOT, "cut-limbs-v7c")
FLEXOUT = os.path.join(ROOT, "cut-limbs-v7c-flex-out")
OUT = "/home/hatch/workspace/cape-jones-rig/clean-100-20261031/flex-opposition"
SCALE = 0.95
SHOULDER = {"L": (430, 445), "R": (670, 445)}
HIP = {"L": (470, 740), "R": (615, 740)}
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
LEG = {"L": ((95, 314), (77, 40)), "R": ((100, 314), (84, 40))}
LEG_PIECES = {"L": ("Leg_Front_Upper.png", "Leg_Front_Lower.png", "Leg_Front_Cap.png"),
              "R": ("Leg_Back_Upper.png", "Leg_Back_Lower.png", "Leg_Back_Cap.png")}
ARM_PIECES = {"L": ("Arm_Front_Upper.png", "Arm_Front_Lower.png", "Arm_Front_Cap.png"),
              "R": ("Arm_Back_Upper.png", "Arm_Back_Lower.png", "Arm_Back_Cap.png")}
WRIST_PIECE = {"L": (57, 175), "R": (114, 175)}  # (x, y) in unscaled lower-piece coords
FLEXOUT_FILES = {"L": "Arm_Front_Lower_FlexOut.png", "R": "Arm_Back_Lower_FlexOut.png"}


def load(p, scale=SCALE):
    im = Image.open(p).convert("RGBA")
    return im.resize((int(im.size[0] * scale), int(im.size[1] * scale)), Image.LANCZOS)


def paste_at(c, im, cx, top):
    c.paste(im, (int(cx - im.size[0] / 2), int(top)), im)


def rot_vec(v, angle_deg):
    a = math.radians(angle_deg)
    x, y = v
    return (x * math.cos(a) + y * math.sin(a), -x * math.sin(a) + y * math.cos(a))


def limb_layer(canvas_w, canvas_h, path, joint, angle, anchor, scale=SCALE):
    """Return a full-canvas layer with `path` pasted at joint-anchor and
    rotated `angle` (PIL convention, same as joint_locked_rig_v7c) about joint."""
    im = load(path, scale)
    ax, ay = anchor[0] * scale, anchor[1] * scale
    layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    layer.paste(im, (int(joint[0] - ax), int(joint[1] - ay)), im)
    return layer.rotate(angle, center=joint, expand=False)


def cap_at(c, path, joint, scale=SCALE):
    im = load(path, scale)
    c.paste(im, (int(joint[0] - im.size[0] / 2), int(joint[1] - im.size[1] / 2)), im)


def build_character(cfg, lower_dir=CUT, lower_files=None, bg="grey",
                    canvas_w=1100, canvas_h=1500, xoff=0,
                    forearm_truncate_y=None, fist_roll=None,
                    arm2_fist_swap=False, cape=True, belt=True, scale=SCALE,
                    truncate_sides=None):
    """cfg: arm_upper/lower, leg_upper/lower dicts L/R.
    fist_roll: {side: roll_deg_signed} -> pose-space fist roll (item 1/3).
    arm2_fist_swap: only side R, punch Arm2 front-fist swap (item 2).
    Returns (canvas, elbows, wrists). No labels, ever."""
    if bg == "grey":
        canvas = Image.new("RGBA", (canvas_w, canvas_h), (128, 128, 128, 255))
    else:
        canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

    def SX(x):
        return x + xoff

    if cape:
        paste_at(canvas, load(os.path.join(BASE, "Cape_Back_Main.png"), scale), SX(550), 410)
    # legs
    knees = {}
    for side in ("L", "R"):
        hip = (SX(HIP[side][0]), HIP[side][1])
        ball, hip_anchor = LEG[side]
        vec = (ball[0] - hip_anchor[0], ball[1] - hip_anchor[1])
        up, low, cap = LEG_PIECES[side]
        canvas.alpha_composite(limb_layer(canvas_w, canvas_h, os.path.join(CUT, up), hip, cfg["leg_upper"][side], hip_anchor, scale))
        knee = (hip[0] + rot_vec(vec, cfg["leg_upper"][side])[0] * scale,
                hip[1] + rot_vec(vec, cfg["leg_upper"][side])[1] * scale)
        knees[side] = knee
        canvas.alpha_composite(limb_layer(canvas_w, canvas_h, os.path.join(CUT, low), knee, cfg["leg_lower"][side], (ball[0], 0), scale))
        cap_at(canvas, os.path.join(CUT, cap), knee, scale)
    # upper arms
    elbows = {}
    for side in ("L", "R"):
        ball, sh_anchor = ARM[side]
        vec = (ball[0] - sh_anchor[0], ball[1] - sh_anchor[1])
        up, _, _ = ARM_PIECES[side]
        sh = (SX(SHOULDER[side][0]), SHOULDER[side][1])
        canvas.alpha_composite(limb_layer(canvas_w, canvas_h, os.path.join(CUT, up), sh, cfg["arm_upper"][side], sh_anchor, scale))
        elbows[side] = (sh[0] + rot_vec(vec, cfg["arm_upper"][side])[0] * scale,
                        sh[1] + rot_vec(vec, cfg["arm_upper"][side])[1] * scale)
    paste_at(canvas, load(os.path.join(BASE, "Pelvis.png"), scale), SX(550), 680)
    if cape:
        paste_at(canvas, load(os.path.join(BASE, "Cape_Collar.png"), scale), SX(550), 370)
    paste_at(canvas, load(os.path.join(BASE, "Torso_Chest.png"), scale), SX(550), 400)
    if belt:
        paste_at(canvas, load(os.path.join(BASE, "Belt_Overlay.png"), scale), SX(550), 670)
    # lower arms (+ pose-space fists)
    wrists = {}
    for side in ("L", "R"):
        _, low, cap = ARM_PIECES[side]
        ball, _ = ARM[side]
        fname = (lower_files or {}).get(side, low)
        src_dir = lower_dir
        full_path = fname if "/" in fname else os.path.join(src_dir, fname)
        full = load(full_path, scale)
        if forearm_truncate_y is not None and (truncate_sides is None or side in truncate_sides):
            # forearm+gauntlet only, truncated at y=180 (unscaled)
            trunc = full.crop((0, 0, full.size[0], int(forearm_truncate_y * scale)))
            layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
            layer.paste(trunc, (int(elbows[side][0] - ball[0] * scale), int(elbows[side][1] - 0)), trunc)
            layer = layer.rotate(cfg["arm_lower"][side], center=elbows[side], expand=False)
            canvas.alpha_composite(layer)
        else:
            canvas.alpha_composite(limb_layer(canvas_w, canvas_h, full_path, elbows[side], cfg["arm_lower"][side], (ball[0], 0), scale))
        cap_at(canvas, os.path.join(CUT, cap), elbows[side], scale)
        # pose wrist
        wx, wy = WRIST_PIECE[side]
        wvec = (wx - ball[0], wy - 0)
        wrists[side] = (elbows[side][0] + rot_vec(wvec, cfg["arm_lower"][side])[0] * scale,
                        elbows[side][1] + rot_vec(wvec, cfg["arm_lower"][side])[1] * scale)
    # pose-space fists (drawn after torso, before head — same order as v7c lowers)
    if fist_roll:
        for side, roll in fist_roll.items():
            _, low, cap = ARM_PIECES[side]
            ball, _ = ARM[side]
            src = load(os.path.join(FLEXOUT, FLEXOUT_FILES[side]), scale)
            crop_y0 = 165
            fist = src.crop((0, int(crop_y0 * scale), src.size[0], src.size[1]))
            wx, wy = WRIST_PIECE[side]
            piv = (wx * scale, (wy - crop_y0) * scale)
            layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
            layer.paste(fist, (int(wrists[side][0] - piv[0]), int(wrists[side][1] - piv[1])), fist)
            layer = layer.rotate(cfg["arm_lower"][side] + roll, center=wrists[side], expand=False)
            canvas.alpha_composite(layer)
            cap_at(canvas, os.path.join(CUT, cap), wrists[side], scale)
    if arm2_fist_swap:
        # side R only: front-angle fist, knuckles up, tilted -20deg about wrist
        hand = load(os.path.join(BASE, "Hand_1_Fist.png"), scale)
        # wrist point of Hand_1: bottom-centre of its wrist band
        hpiv = (hand.size[0] / 2, hand.size[1] - 4)
        layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        layer.paste(hand, (int(wrists["R"][0] - hpiv[0]), int(wrists["R"][1] - hpiv[1])), hand)
        layer = layer.rotate(-20, center=wrists["R"], expand=False)
        canvas.alpha_composite(layer)
        _, _, cap = ARM_PIECES["R"]
        cap_at(canvas, os.path.join(CUT, cap), wrists["R"], scale)
    paste_at(canvas, load(os.path.join(BASE, "Neck.png"), scale=scale * 1.05 / SCALE if False else 1.05), SX(550), 360)
    paste_at(canvas, load(os.path.join(BASE, "Head_Front.png"), scale), SX(550), 250)
    return canvas, elbows, wrists


def save(canvas, name):
    p = os.path.join(OUT, name)
    canvas.convert("RGB").save(p)
    print(p, canvas.size)
    return p


# ---------------- item 1: true flex, roll 75 ----------------
FLEX_CFG = {"arm_upper": {"L": -70, "R": 70}, "arm_lower": {"L": 150, "R": -150},
            "leg_upper": {"L": -15, "R": 15}, "leg_lower": {"L": -10, "R": 10}}
flex, elbows, wrists = build_character(
    FLEX_CFG, lower_dir=FLEXOUT, lower_files=FLEXOUT_FILES,
    forearm_truncate_y=180, fist_roll={"L": -75, "R": 75})
print("flex elbows", elbows, "wrists", wrists)
save(flex, "true-flex-pose-space-wristcap-20261031.png")
# wrist-zoom QC (crop around both wrists, enlarged; QC only, not a shot)
zoom = flex.crop((230, 240, 870, 470)).resize((1280, 460), Image.NEAREST)
zoom.convert("RGB").save(os.path.join(OUT, "true-flex-pose-space-wristcap-20261031-WRIST-ZOOM-QC.png"))
print("wrist zoom saved")

# ---------------- item 3: flex clip, Darwin beat grid retarget ----------------
# Beat: ~107 BPM -> 13.46f/beat at 24fps. Twos-snapped keyframes 1, 15, 29, 43.
CLIP_FRAMES = [
    ("flex-clip-20261031-f01-preflex-roll0.png", 0),
    ("flex-clip-20261031-f15-roll25.png", 25),
    ("flex-clip-20261031-f21-roll50.png", 50),
    ("flex-clip-20261031-f29-trueflex-roll75.png", 75),
    ("flex-clip-20261031-f37-trueflex-hold-roll75.png", 75),
    ("flex-clip-20261031-f43-release-roll50.png", 50),
    ("flex-clip-20261031-f51-release-roll0.png", 0),
]
clip_imgs = []
for fname, roll in CLIP_FRAMES:
    c, _, _ = build_character(
        FLEX_CFG, lower_dir=FLEXOUT, lower_files=FLEXOUT_FILES,
        forearm_truncate_y=180, fist_roll={"L": -roll, "R": roll})
    save(c, os.path.join("frames-flex-clip", fname))
    clip_imgs.append(c)
# contact sheet: thumbnails in frame order, no text on characters, no labels
thumb_w, thumb_h = 314, 429
sheet = Image.new("RGB", (thumb_w * 4, thumb_h * 2), (128, 128, 128))
for i, c in enumerate(clip_imgs):
    th = c.convert("RGB").resize((thumb_w, thumb_h), Image.LANCZOS)
    sheet.paste(th, ((i % 4) * thumb_w, (i // 4) * thumb_h))
sheet.save(os.path.join(OUT, "flex-clip-20261031-contact-sheet.png"))
print("contact sheet saved")
timing = {
    "clip": "flex-clip-20261031", "fps": 24, "rig": "joint_locked_rig_v7c, labels=False",
    "source_timing": "beat ~14f @25fps (~107 BPM), on twos; retargeted to 24fps = 13.46f/beat",
    "beat_grid_ideal_24fps": [1, 14.5, 27.9, 41.4, 54.8],
    "keyframes_twos_snapped": [
        {"frame": 1, "pose": "pre-flex (approved arms-up)", "roll_deg": 0},
        {"frame": 15, "pose": "tighten in-between", "roll_deg": 25},
        {"frame": 21, "pose": "tighten in-between", "roll_deg": 50},
        {"frame": 29, "pose": "TRUE FLEX peak", "roll_deg": 75},
        {"frame": 37, "pose": "TRUE FLEX hold (same drawing as f29)", "roll_deg": 75},
        {"frame": 43, "pose": "release in-between", "roll_deg": 50},
        {"frame": 51, "pose": "release to pre-flex", "roll_deg": 0},
    ],
    "note": "Timing only is retargeted. No show character art, names, dialogue or logos are used. This is NOT the old fighting-pose flex clip: pose is the double-bicep true flex (upper -70/70, lower 150/-150), not the fighting pose (upper -25/25, lower 160/-160, fists in front of chest).",
    "arms_up": {"arm_upper": {"L": -70, "R": 70}, "arm_lower": {"L": 150, "R": -150}, "elbows": {"L": [253, 493], "R": [849, 487]}},
    "legs": {"leg_upper": {"L": -15, "R": 15}, "leg_lower": {"L": -10, "R": 10}},
}
with open(os.path.join(OUT, "flex-clip-20261031-timing.json"), "w") as f:
    json.dump(timing, f, indent=2)
print("timing saved")

# ---------------- item 2: punch Arm2 fist-angle variant ----------------
def per_row_mirror(src_path, dst_path):
    """OutFixed method: mirror cuff rows y62-180 within each row's own alpha
    span, so per-row x-range is exactly preserved. Returns diff stats."""
    from PIL import Image as _I
    import numpy as _np
    im = _I.open(src_path).convert("RGBA")
    a = _np.array(im)
    for y in range(62, 180):
        row = a[y, :, 3]
        xs = _np.where(row > 10)[0]
        if len(xs) < 2:
            continue
        x0, x1 = xs.min(), xs.max()
        span = a[y, x0:x1 + 1].copy()
        a[y, x0:x1 + 1] = span[::-1]
    out = _I.fromarray(a)
    out.save(dst_path)
    orig = _np.array(_I.open(src_path).convert("RGBA")).astype(int)
    new = a.astype(int)
    d = (_np.abs(orig - new).max(axis=2) > 10)
    ys, xs = _np.where(d)
    print("flip diff px", int(d.sum()), "bbox", (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())) if len(xs) else None)
    # per-row x-range check
    bad = 0
    for y in range(62, 180):
        o = _np.where(orig[y, :, 3] > 10)[0]
        n = _np.where(new[y, :, 3] > 10)[0]
        if len(o) and len(n) and (o.min() != n.min() or o.max() != n.max()):
            bad += 1
    print("per-row x-range violations y62-180:", bad)
    return dst_path


flip_path = per_row_mirror(
    os.path.join(CUT, "Arm_Back_Lower.png"),
    os.path.join(OUT, "pieces", "Arm_Back_Lower_PunchA2_Flip_20261031.png"))
PUNCH_CFG = {"arm_upper": {"L": -90, "R": 20}, "arm_lower": {"L": -90, "R": -110},
             "leg_upper": {"L": -15, "R": 15}, "leg_lower": {"L": 15, "R": -15}}
punch, pelbows, pw = build_character(
    PUNCH_CFG, lower_dir=CUT,
    lower_files={"L": "Arm_Front_Lower.png", "R": flip_path},
    forearm_truncate_y=180, arm2_fist_swap=True, truncate_sides={"R"})
print("punch elbows", pelbows, "wrists", pw)
save(punch, "punch-arm2-fist-angle-variant-20261031.png")

# ---------------- item 4: opposition demo ----------------
# Cape: LOCKED punch, mirrored so it punches RIGHT toward the opponent.
# Rendered on a 1300-wide transparent canvas (centre +100) so the extended
# fist is not cut off at the edge, then flipped horizontally as a whole.
cape_wide, _, _ = build_character(PUNCH_CFG, bg="transparent", canvas_w=1300, xoff=100)
cape_mirrored = ImageOps.mirror(cape_wide)
# Opponent: SILHOUETTE / PLACEHOLDER only, kitbashed from Cape's own rig
# pieces, then flattened to one flat colour. No cape, no belt, no face,
# no purple, no white suit — it is a shape, not a second Cape Jones.
OPP_CFG = {"arm_upper": {"L": -25, "R": 50}, "arm_lower": {"L": 160, "R": 50},
           "leg_upper": {"L": -20, "R": 20}, "leg_lower": {"L": -20, "R": 20}}
opp, _, _ = build_character(OPP_CFG, bg="transparent", cape=False, belt=False, scale=0.90)
opp_rgba = opp.convert("RGBA")
arr = __import__("numpy").array(opp_rgba)
sil = __import__("numpy").zeros_like(arr)
sil[:, :, 3] = arr[:, :, 3]
sil[:, :, 0] = 38
sil[:, :, 1] = 44
sil[:, :, 2] = 58
opp_sil = Image.fromarray(sil)
# opponent alone, on grey, for inspection (not a character design)
opp_grey = Image.new("RGBA", (1100, 1500), (128, 128, 128, 255))
opp_grey.alpha_composite(opp_sil)
opp_grey.convert("RGB").save(os.path.join(OUT, "opposition-placeholder-silhouette-alone-20261031.png"))
print("opponent alone saved")
# wide staging: Cape (cropped 150px from the left after mirroring, so its
# centre sits at x=500 and its fist at x~1068) + opponent at x=950, y=+30
# (the 0.90 scale shortens its legs ~30px, so +30 re-aligns its feet).
wide = Image.new("RGBA", (2000, 1500), (128, 128, 128, 255))
cape_crop = cape_mirrored.crop((150, 0, 1300, 1500))
wide.alpha_composite(cape_crop, (0, 0))
wide.alpha_composite(opp_sil, (950, 30))
wide.convert("RGB").save(os.path.join(OUT, "opposition-demo-20261031.png"))
print("opposition saved", wide.size)
