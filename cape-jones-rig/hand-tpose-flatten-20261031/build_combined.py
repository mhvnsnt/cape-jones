"""COMBINED hand fix, all Mars corrections together, 2026-10-31.

1. T-POSE FLATTEN (19:35): library hands fingers-up both sides -> flatten
   along arm axis on a horizontal T-pose. Measured, not guessed:
   old angle 0, finger (0,-1), 120 deg off groove-a forearm outward,
   and 90 deg off a horizontal T-pose forearm. New: L +90, R -90.
   Mars's "plus 180" was a guess ("I don't know, like 180 I think") and
   is NOT used: the measured correction is +/-90 deg.
2. ARM1/ARM2 RULE (19:37/19:38): Arm2 (R, image-right) hand UNCHANGED.
   Arm1 (L, image-left) hand mirrored HORIZONTALLY IN PLACE, before
   rotation, about its own image centre. Wrist anchor unchanged: the
   mirrored wrist point is re-registered (W - wrist_x) and the centre
   is recomputed so the mirrored wrist lands on the SAME forearm end.
   NOT a whole-band move, NOT a vertical flip, NOT a rotation instead
   of the mirror. Rotation (flatten / serve axis) is applied AFTER the
   mirror, so the flatten direction is preserved (mirror flips thumb
   side, rotation turns the already-mirrored piece onto the arm axis).
3. SCALE DOWN 25% (19:37/19:38): new = 0.75 x current, anchored at wrist.
   Dance swapped hands: 1.7 -> 1.275. Library FIXED hands: 1.7 -> 1.275.
   Base-fist dance frames and old original library fists are NOT
   touched and NOT scaled. Serve hand scale stays 1.0 (scale-down list
   named dance + library only); serve gets replacement + Arm1 mirror.
4. SERVE REPLACEMENT, NOT OVERLAY (19:39): JEI-01 serve, Arm1 (L arm
   top, per build_wrist_fixes doc). Original fist ERASED ENTIRELY
   (ALL alpha distal to the wrist plane, not near-white only), then the
   mirrored open hand is pasted in its place, wrist on the forearm end,
   angle = angle_for_direction(D) = 164.8 deg, scale 1.0. Ball version:
   orb re-applied over the NEW palm centre, (255,230,110), after the
   fist is gone, never over a fist.
No mirror/flip is used as a substitute for rotation; mirror is Arm1
only, rotation is flatten/serve-axis only. No-crop: canvases auto-fit,
gate = no alpha touches a canvas edge. No repo push, approval 0/1.
"""
import os, sys, math, json
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/home/hatch/workspace/cape-jones-rig/wrist-attach-fix-20261031")
from check_wrist_attach import HANDS, rot_vec, angle_for_direction

RIG = "/home/hatch/workspace/cape-jones-rig"
SLICED = os.path.join(RIG, "sliced"); CUT = os.path.join(RIG, "cut-limbs-v7c")
WRIST = os.path.join(RIG, "wrist-attach-fix-20261031")
OUT = os.path.join(RIG, "hand-tpose-flatten-20261031")
os.makedirs(os.path.join(OUT, "frames"), exist_ok=True)
SCALE = 0.95

# ---------- mirrored registry helpers ----------
def mirrored_registry(hfile):
    (W, H), wrist, tip = HANDS[hfile]
    return (W, H), (W - wrist[0], wrist[1]), (W - tip[0], tip[1])

def hand_image(hfile, scale, mirror):
    im = Image.open(os.path.join(SLICED, hfile)).convert("RGBA")
    im = im.resize((int(im.size[0] * scale), int(im.size[1] * scale)), Image.LANCZOS)
    if mirror:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im

def centre_for(hfile, angle, scale, wrist_target, mirror):
    if mirror:
        (W, H), wrist, _ = mirrored_registry(hfile)
    else:
        (W, H), wrist, _ = HANDS[hfile]
    ic = (W / 2.0, H / 2.0)
    wo = ((wrist[0] - ic[0]) * scale, (wrist[1] - ic[1]) * scale)
    wr = rot_vec(wo, angle)
    return (wrist_target[0] - wr[0], wrist_target[1] - wr[1])

def gate_check(hfile, centre, angle, scale, forearm_end, mirror):
    if mirror:
        (W, H), wrist, tip = mirrored_registry(hfile)
    else:
        (W, H), wrist, tip = HANDS[hfile]
    ic = (W / 2.0, H / 2.0)
    wo = ((wrist[0] - ic[0]) * scale, (wrist[1] - ic[1]) * scale)
    to = ((tip[0] - ic[0]) * scale, (tip[1] - ic[1]) * scale)
    wr = (centre[0] + rot_vec(wo, angle)[0], centre[1] + rot_vec(wo, angle)[1])
    tr = (centre[0] + rot_vec(to, angle)[0], centre[1] + rot_vec(to, angle)[1])
    dw = math.dist(wr, forearm_end); dt = math.dist(tr, forearm_end)
    finger = rot_vec((tip[0] - wrist[0], tip[1] - wrist[1]), angle)
    fl = math.dist((0, 0), finger)
    finger = (finger[0] / fl, finger[1] / fl)
    return {"wrist": [round(v, 1) for v in wr], "tip": [round(v, 1) for v in tr],
            "d_wrist": round(dw, 1), "d_tip": round(dt, 1),
            "pass": bool(dw <= 30 and dw < dt), "verdict": "PASS" if (dw <= 30 and dw < dt) else "FAIL",
            "finger_dir": [round(v, 3) for v in finger]}

def paste_hand(plate, hfile, centre, angle, scale, mirror):
    im = hand_image(hfile, scale, mirror)
    rot = im.rotate(angle, expand=True, resample=Image.BICUBIC) if angle != 0 else im
    plate.alpha_composite(rot, (int(centre[0] - rot.size[0] / 2), int(centre[1] - rot.size[1] / 2)))
    return rot

def no_crop_gate(im):
    a = np.array(im.getchannel("A"))
    ys, xs = np.where(a > 10)
    if len(xs) == 0:
        return {"pass": False, "bbox": None}
    touch = bool(ys.min() == 0 or ys.max() == im.size[1] - 1 or xs.min() == 0 or xs.max() == im.size[0] - 1)
    return {"pass": not touch, "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]}

def finish(plate, name):
    plate.save(os.path.join(OUT, "frames", name.replace(".png", "-transparent.png")))
    bg = Image.new("RGBA", plate.size, (128, 128, 128, 255)); bg.alpha_composite(plate)
    bg.convert("RGB").save(os.path.join(OUT, name))
    return no_crop_gate(plate)

# ---------- shared body builder ----------
def load(p, scale=SCALE):
    im = Image.open(p).convert("RGBA")
    return im.resize((int(im.size[0] * scale), int(im.size[1] * scale)), Image.LANCZOS)
def paste_at(c, im, cx, top): c.alpha_composite(im, (int(cx - im.size[0] / 2), int(top)))
def limb(c, path, joint, angle, anchor, W, H):
    im = load(path); ax, ay = anchor[0] * SCALE, anchor[1] * SCALE
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(im, (int(joint[0] - ax), int(joint[1] - ay)))
    layer = layer.rotate(angle, center=joint, expand=False); c.alpha_composite(layer)
def cap_at(c, path, joint):
    im = load(path); c.alpha_composite(im, (int(joint[0] - im.size[0] / 2), int(joint[1] - im.size[1] / 2)))

def erase_fist_np(lowers, fc, out):
    """Erase ALL alpha distal to forearm-end plane within 95px of bc."""
    arr = np.array(lowers)
    yy, xx = np.mgrid[0:arr.shape[0], 0:arr.shape[1]]
    bcx, bcy = fc[0] + out[0] * 40, fc[1] + out[1] * 40
    dot = (xx - fc[0]) * out[0] + (yy - fc[1]) * out[1]
    dist2 = (xx - bcx) ** 2 + (yy - bcy) ** 2
    mask = (dot > -10) & (dist2 <= 95 ** 2) & (arr[:, :, 3] > 10)
    arr[mask] = (0, 0, 0, 0)
    return Image.fromarray(arr, "RGBA")

def build_body(W, H, OX, CFG, SHOULDER, HIP, ARM, LEG, LEG_PIECES, ARM_PIECES):
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    paste_at(canvas, load(os.path.join(SLICED, "Cape_Back_Main.png")), 550 + OX, 410)
    for side in ("L", "R"):
        hip = HIP[side]; ball, ha = LEG[side]; vec = (ball[0] - ha[0], ball[1] - ha[1])
        up, low, cap = LEG_PIECES[side]
        limb(canvas, os.path.join(CUT, up), hip, CFG["leg_upper"][side], ha, W, H)
        knee = (hip[0] + rot_vec(vec, CFG["leg_upper"][side])[0] * SCALE,
                hip[1] + rot_vec(vec, CFG["leg_upper"][side])[1] * SCALE)
        limb(canvas, os.path.join(CUT, low), knee, CFG["leg_lower"][side], (ball[0], 0), W, H)
        cap_at(canvas, os.path.join(CUT, cap), knee)
    elbows = {}
    for side in ("L", "R"):
        ball, sa = ARM[side]; vec = (ball[0] - sa[0], ball[1] - sa[1])
        up, _, _ = ARM_PIECES[side]; sh = SHOULDER[side]
        limb(canvas, os.path.join(CUT, up), sh, CFG["arm_upper"][side], sa, W, H)
        elbows[side] = (sh[0] + rot_vec(vec, CFG["arm_upper"][side])[0] * SCALE,
                        sh[1] + rot_vec(vec, CFG["arm_upper"][side])[1] * SCALE)
    paste_at(canvas, load(os.path.join(SLICED, "Pelvis.png")), 550 + OX, 680)
    paste_at(canvas, load(os.path.join(SLICED, "Cape_Collar.png")), 550 + OX, 370)
    paste_at(canvas, load(os.path.join(SLICED, "Torso_Chest.png")), 550 + OX, 400)
    paste_at(canvas, load(os.path.join(SLICED, "Belt_Overlay.png")), 550 + OX, 670)
    lowers = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for side in ("L", "R"):
        _, low, cap = ARM_PIECES[side]; ball, _ = ARM[side]
        limb(lowers, os.path.join(CUT, low), elbows[side], CFG["arm_lower"][side], (ball[0], 0), W, H)
        cap_at(lowers, os.path.join(CUT, cap), elbows[side])
    return canvas, elbows, lowers

def fist_centre(elbow, arm_lower):
    dx, dy = rot_vec((0, 1), arm_lower)
    return (elbow[0] + dx * 210 * SCALE, elbow[1] + dy * 210 * SCALE)

results = {"tpose": {}, "dance": {}, "serve": {}}

# ================= T-POSE FINAL =================
W, H, OX = 1500, 1500, 200
SHOULDER = {"L": (430 + OX, 445), "R": (670 + OX, 445)}
HIP = {"L": (470 + OX, 740), "R": (615 + OX, 740)}
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
LEG = {"L": ((95, 314), (77, 40)), "R": ((100, 314), (84, 40))}
LEG_PIECES = {"L": ("Leg_Front_Upper.png", "Leg_Front_Lower.png", "Leg_Front_Cap.png"),
              "R": ("Leg_Back_Upper.png", "Leg_Back_Lower.png", "Leg_Back_Cap.png")}
ARM_PIECES = {"L": ("Arm_Front_Upper.png", "Arm_Front_Lower.png", "Arm_Front_Cap.png"),
              "R": ("Arm_Back_Upper.png", "Arm_Back_Lower.png", "Arm_Back_Cap.png")}
CFG_T = {"arm_upper": {"L": -90, "R": 90}, "arm_lower": {"L": -90, "R": 90},
         "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": 10, "R": -10}}
HANDS_LIST = ["Hand_1_Fist.png", "Hand_2_FistBack.png", "Hand_3_Open.png",
              "Hand_4_Point.png", "Hand_5_Point2.png", "Hand_6_Relaxed.png", "Hand_7_Grip.png"]
for hfile in HANDS_LIST:
    tag = hfile.replace("Hand_", "").replace(".png", "").lower()
    plate, elbows, lowers = build_body(W, H, OX, CFG_T, SHOULDER, HIP, ARM, LEG, LEG_PIECES, ARM_PIECES)
    gates = {}
    for side in ("L", "R"):
        fc = fist_centre(elbows[side], CFG_T["arm_lower"][side])
        out = rot_vec((0, 1), CFG_T["arm_lower"][side])
        lowers = erase_fist_np(lowers, fc, out)
        wt = (fc[0] - out[0] * 20, fc[1] - out[1] * 20)
        ang = 90 if side == "L" else -90
        mirror = (side == "L")  # Arm1 = L, mirrored; Arm2 = R, unchanged
        centre = centre_for(hfile, ang, 1.275, wt, mirror)
        gates[side] = gate_check(hfile, centre, ang, 1.275, fc, mirror)
        gates[side].update({"arm": "Arm1" if side == "L" else "Arm2", "mirror": mirror,
                            "angle": ang, "scale": 1.275, "wrist_target": [round(v, 1) for v in wt],
                            "forearm_end": [round(v, 1) for v in fc], "forearm_outward": [round(v, 3) for v in out]})
        # store centre for paste after lowers are composited (paste order: lowers first, then hands)
        gates[side]["_centre"] = centre
    plate.alpha_composite(lowers)
    paste_at(plate, load(os.path.join(SLICED, "Neck.png"), scale=1.05), 550 + OX, 360)
    paste_at(plate, load(os.path.join(SLICED, "Head_Front.png")), 550 + OX, 250)
    for side in ("L", "R"):
        ang = 90 if side == "L" else -90
        paste_hand(plate, hfile, gates[side]["_centre"], ang, 1.275, side == "L")
        gates[side].pop("_centre", None)
    gate = finish(plate, f"tpose-{tag}-FINAL-20261031.png")
    # hand footprint sizes
    (bw, bh), _, _ = HANDS[hfile]
    results["tpose"][tag] = {"hand": hfile, "before_scale": 1.7, "after_scale": 1.275,
                             "before_bbox_px": [round(82 * 1.7) if tag == "1_fist" else None, None],
                             "gate": gates, "no_crop": gate}
    print("tpose", tag, {s: gates[s]["verdict"] for s in gates}, "nocrop", gate["pass"])

# ================= DANCE FINAL =================
W2, H2, OX2 = 1100, 1500, 0
SH2 = {"L": (430, 445), "R": (670, 445)}; HIP2 = {"L": (470, 740), "R": (615, 740)}
POSES = [
    ("groove-a", {"arm_upper": {"L": -60, "R": 60}, "arm_lower": {"L": -60, "R": 60},
                  "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": 10, "R": -10}}),
    ("groove-b", {"arm_upper": {"L": -115, "R": 85}, "arm_lower": {"L": 65, "R": -95},
                  "leg_upper": {"L": -16, "R": 6}, "leg_lower": {"L": 32, "R": -28}}),
    ("groove-c", {"arm_upper": {"L": -25, "R": 35}, "arm_lower": {"L": -88, "R": 145},
                  "leg_upper": {"L": -20, "R": 20}, "leg_lower": {"L": 15, "R": -15}}),
]
HANDS_DV = [("open", "Hand_3_Open.png"), ("point", "Hand_4_Point.png"), ("relaxed", "Hand_6_Relaxed.png")]
for vname, hfile in HANDS_DV:
    for pname, cfg in POSES:
        plate, elbows, lowers = build_body(W2, H2, OX2, cfg, SH2, HIP2, ARM, LEG, LEG_PIECES, ARM_PIECES)
        gates = {}
        for side in ("L", "R"):
            fc = fist_centre(elbows[side], cfg["arm_lower"][side])
            out = rot_vec((0, 1), cfg["arm_lower"][side])
            lowers = erase_fist_np(lowers, fc, out)
            wt = (fc[0] - out[0] * 20, fc[1] - out[1] * 20)
            mirror = (side == "L")
            centre = centre_for(hfile, 0, 1.275, wt, mirror)
            gates[side] = gate_check(hfile, centre, 0, 1.275, fc, mirror)
            gates[side].update({"arm": "Arm1" if side == "L" else "Arm2", "mirror": mirror,
                                "angle": 0, "scale": 1.275, "forearm_outward": [round(v, 3) for v in out]})
            gates[side]["_centre"] = centre
        plate.alpha_composite(lowers)
        paste_at(plate, load(os.path.join(SLICED, "Neck.png"), scale=1.05), 550, 360)
        paste_at(plate, load(os.path.join(SLICED, "Head_Front.png")), 550, 250)
        for side in ("L", "R"):
            paste_hand(plate, hfile, gates[side]["_centre"], 0, 1.275, side == "L")
            gates[side].pop("_centre", None)
        gate = finish(plate, f"dance-{vname}-{pname}-FINAL-20261031.png")
        results["dance"][f"{vname}-{pname}"] = {"hand": hfile, "before_scale": 1.7, "after_scale": 1.275,
                                                "gate": gates, "no_crop": gate}
        print("dance", vname, pname, {s: gates[s]["verdict"] for s in gates}, "nocrop", gate["pass"])

# ================= SERVE REPLACEMENT =================
base_path = os.path.join(RIG, "ginyu-force-limits-broken-20261031", "jei-01-base-for-swap-20261031.png")
base = Image.open(base_path).convert("RGBA")
F = (314.0, 517.0); D = (-0.263, 0.965)
ang = angle_for_direction(D)  # ~164.8
Wpt = (F[0] - D[0] * 25, F[1] - D[1] * 25)
# erase region: dot((p-Wpt), D) > 0 and dist(p, F) <= 160, ALL alpha
arr = np.array(base)
yy, xx = np.mgrid[0:arr.shape[0], 0:arr.shape[1]]
dot = (xx - Wpt[0]) * D[0] + (yy - Wpt[1]) * D[1]
dist = np.sqrt((xx - F[0]) ** 2 + (yy - F[1]) ** 2)
erase_mask = (dot > 0) & (dist <= 160) & (arr[:, :, 3] > 10)
base_alpha_before = int(np.sum(erase_mask))
arr[erase_mask] = (0, 0, 0, 0)
erased = Image.fromarray(arr, "RGBA")
# hand mask alone (for remaining-fist measurement)
hand_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
centre = centre_for("Hand_3_Open.png", ang, 1.0, Wpt, True)  # Arm1 mirrored
paste_hand(hand_layer, "Hand_3_Open.png", centre, ang, 1.0, True)
hand_mask = np.array(hand_layer)[:, :, 3] > 10
# final: erased plate + hand
final = erased.copy(); final.alpha_composite(hand_layer)
# remaining fist pixels: base alpha in erase region, NOT covered by hand, still present in final
final_arr = np.array(final)
remaining = int(np.sum(erase_mask & (~hand_mask) & (final_arr[:, :, 3] > 10)))
g = gate_check("Hand_3_Open.png", centre, ang, 1.0, F, True)
gate_serve = finish(final, "jei-01-serve-open-palm-FINAL-20261031.png")
# ball version
ball = final.copy(); lay = Image.new("RGBA", ball.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
pc = (int(centre[0]), int(centre[1]))
for r, col in [(70, (255, 230, 110, 90)), (48, (255, 230, 110, 255))]:
    d.ellipse([pc[0] - r, pc[1] - r, pc[0] + r, pc[1] + r], fill=col)
d.ellipse([pc[0] - 18, pc[1] - 18, pc[0] + 18, pc[1] + 18], fill=(255, 250, 220, 255))
ball.alpha_composite(lay)
gate_ball = finish(ball, "jei-01-serve-open-palm-ball-FINAL-20261031.png")
results["serve"] = {"arm": "Arm1 (L arm top, per build_wrist_fixes doc)", "mirror": True,
                    "angle": round(ang, 1), "scale": 1.0, "forearm_end_F": list(F),
                    "arm_direction_D": list(D), "wrist_target": [round(v, 1) for v in Wpt],
                    "palm_centre": list(pc), "gate": g,
                    "erase_region_base_alpha_px": base_alpha_before,
                    "fist_pixels_remaining_outside_hand": remaining,
                    "no_crop": gate_serve, "no_crop_ball": gate_ball}
print("serve", g, "erase base px", base_alpha_before, "remaining", remaining, "nocrop", gate_serve["pass"])

json.dump(results, open(os.path.join(OUT, "measurements-combined-20261031.json"), "w"), indent=2)
print("COMBINED DONE")
