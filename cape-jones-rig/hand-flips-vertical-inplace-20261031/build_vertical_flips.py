"""VERTICAL FLIP IN PLACE for hands 1,3,4,5,6,7 — Mars 2026-10-31 20:59-21:01 CDT.
Term, locked: VERTICAL FLIP IN PLACE = flip top-to-bottom, mirrored over
the horizontal axis, in place, without moving the part from the space it
is in, without rotating it, without swapping it to another part, without
moving it to another position.

Method, exactly:
- Rebuild the FINAL T-pose exactly as build_combined.py (1500x1500,
  OX=200, scale 1.275, L +90 / R -90, Arm1=L mirrored horizontally in
  place BEFORE rotation, Arm2=R unchanged, wrist target = forearm end
  minus outward x 20).
- Take the HAND ONLY as placed (scaled, Arm1-mirrored, flatten-rotated),
  transpose FLIP_TOP_BOTTOM, then re-seat it so its WRIST point lands
  back on the SAME wrist target. Nothing else moves: body, arms,
  gauntlets, head, legs are rebuilt identically, not flipped.
- Wrist re-seat math: original rotated hand centre C0, wrist offset
  (dx,dy) = gate wrist - C0. After a vertical flip the wrist offset is
  (dx,-dy). New centre = wrist_target - (dx,-dy). Hence d_wrist stays
  20.0 and d_tip is unchanged (dx same, |dy| to forearm end same).
- Hand 2 fistback is NOT built here: it is perfect as is, untouched.
- Hand 3 palm note is handled in the report, not by swapping pieces:
  a vertical flip swaps top/bottom, it cannot turn a palm drawing into
  a back-of-hand drawing. The flipped hand 3 still shows palm creases;
  that is reported as a mismatch against Mars's "top of hand showing",
  not hidden and not fixed by inventing a new piece.
"""
import os, sys, math, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "/home/hatch/workspace/cape-jones-rig/wrist-attach-fix-20261031")
from check_wrist_attach import HANDS, rot_vec

RIG = "/home/hatch/workspace/cape-jones-rig"
SLICED = os.path.join(RIG, "sliced"); CUT = os.path.join(RIG, "cut-limbs-v7c")
OLD = os.path.join(RIG, "hand-tpose-flatten-20261031")
OUT = os.path.join(RIG, "hand-flips-vertical-inplace-20261031")
os.makedirs(os.path.join(OUT, "frames"), exist_ok=True)
SCALE = 0.95

def mirrored_registry(hfile):
    (W, H), wrist, tip = HANDS[hfile]
    return (W, H), (W - wrist[0], wrist[1]), (W - tip[0], tip[1])

def centre_for(hfile, angle, scale, wrist_target, mirror):
    if mirror:
        (W, H), wrist, _ = mirrored_registry(hfile)
    else:
        (W, H), wrist, _ = HANDS[hfile]
    ic = (W / 2.0, H / 2.0)
    wo = ((wrist[0] - ic[0]) * scale, (wrist[1] - ic[1]) * scale)
    wr = rot_vec(wo, angle)
    return (wrist_target[0] - wr[0], wrist_target[1] - wr[1])

def gate_from_points(wrist_pt, tip_pt, forearm_end):
    dw = math.dist(wrist_pt, forearm_end); dt = math.dist(tip_pt, forearm_end)
    return {"wrist": [round(v, 1) for v in wrist_pt], "tip": [round(v, 1) for v in tip_pt],
            "d_wrist": round(dw, 1), "d_tip": round(dt, 1),
            "pass": bool(dw <= 30 and dw < dt), "verdict": "PASS" if (dw <= 30 and dw < dt) else "FAIL"}

def hand_image(hfile, scale, mirror):
    im = Image.open(os.path.join(SLICED, hfile)).convert("RGBA")
    im = im.resize((int(im.size[0] * scale), int(im.size[1] * scale)), Image.LANCZOS)
    if mirror:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im

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
def no_crop_gate(im):
    a = np.array(im.getchannel("A"))
    ys, xs = np.where(a > 10)
    touch = bool(ys.min() == 0 or ys.max() == im.size[1] - 1 or xs.min() == 0 or xs.max() == im.size[0] - 1)
    return {"pass": not touch, "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]}
def finish(plate, name):
    plate.save(os.path.join(OUT, "frames", name.replace(".png", "-transparent.png")))
    bg = Image.new("RGBA", plate.size, (128, 128, 128, 255)); bg.alpha_composite(plate)
    bg.convert("RGB").save(os.path.join(OUT, name))
    return no_crop_gate(plate)
def hand_bbox(layer):
    a = np.array(layer.getchannel("A"))
    ys, xs = np.where(a > 10)
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]

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

FLIP = [("1_fist", "Hand_1_Fist.png"), ("3_open", "Hand_3_Open.png"),
        ("4_point", "Hand_4_Point.png"), ("5_point2", "Hand_5_Point2.png"),
        ("6_relaxed", "Hand_6_Relaxed.png"), ("7_grip", "Hand_7_Grip.png")]
results = {}
for tag, hfile in FLIP:
    plate, elbows, lowers = build_body(W, H, OX, CFG_T, SHOULDER, HIP, ARM, LEG, LEG_PIECES, ARM_PIECES)
    per_side = {}
    layers = {}
    for side in ("L", "R"):
        fc = fist_centre(elbows[side], CFG_T["arm_lower"][side])
        out = rot_vec((0, 1), CFG_T["arm_lower"][side])
        lowers = erase_fist_np(lowers, fc, out)
        wt = (fc[0] - out[0] * 20, fc[1] - out[1] * 20)
        ang = 90 if side == "L" else -90
        mirror = (side == "L")
        c0 = centre_for(hfile, ang, 1.275, wt, mirror)
        # original rotated hand layer (for bbox + wrist/tip offsets)
        im = hand_image(hfile, 1.275, mirror)
        rot = im.rotate(ang, expand=True, resample=Image.BICUBIC) if ang != 0 else im
        # original wrist/tip from registry math
        if mirror:
            (bw, bh), wrist, tip = mirrored_registry(hfile)
        else:
            (bw, bh), wrist, tip = HANDS[hfile]
        ic = (bw / 2.0, bh / 2.0)
        wo = ((wrist[0] - ic[0]) * 1.275, (wrist[1] - ic[1]) * 1.275)
        to = ((tip[0] - ic[0]) * 1.275, (tip[1] - ic[1]) * 1.275)
        wr_off = rot_vec(wo, ang); tr_off = rot_vec(to, ang)
        wrist_pre = (c0[0] + wr_off[0], c0[1] + wr_off[1])
        tip_pre = (c0[0] + tr_off[0], c0[1] + tr_off[1])
        # VERTICAL FLIP IN PLACE: flip rotated layer top-bottom, re-seat wrist
        flipped = rot.transpose(Image.FLIP_TOP_BOTTOM)
        c_new = (wt[0] - wr_off[0], wt[1] - (-wr_off[1]))
        wrist_post = (c_new[0] + wr_off[0], c_new[1] - wr_off[1])
        tip_post = (c_new[0] + tr_off[0], c_new[1] - tr_off[1])
        # hand-layer bboxes in canvas coords, pre and post
        def layer_bbox(layer_img, centre):
            tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            tmp.alpha_composite(layer_img, (int(centre[0] - layer_img.size[0] / 2), int(centre[1] - layer_img.size[1] / 2)))
            return hand_bbox(tmp)
        bbox_pre = layer_bbox(rot, c0)
        bbox_post = layer_bbox(flipped, c_new)
        per_side[side] = {
            "arm": "Arm1" if side == "L" else "Arm2", "mirror_horizontal_inplace": mirror,
            "angle": ang, "scale": 1.275, "operation": "VERTICAL FLIP IN PLACE",
            "wrist_target": [round(v, 1) for v in wt], "forearm_end": [round(v, 1) for v in fc],
            "centre_pre": [round(v, 1) for v in c0], "centre_post": [round(v, 1) for v in c_new],
            "centre_shift_px": [round(c_new[0] - c0[0], 1), round(c_new[1] - c0[1], 1)],
            "gate_pre": gate_from_points(wrist_pre, tip_pre, fc),
            "gate_post": gate_from_points(wrist_post, tip_post, fc),
            "finger_dir_pre": [round(v, 3) for v in (tr_off[0] - wr_off[0], tr_off[1] - wr_off[1])] ,
            "hand_bbox_pre": bbox_pre, "hand_bbox_post": bbox_post,
            # distances from wrist y to hand bbox top/bottom: these SWAP under a vertical flip
            "wrist_to_bbox_top_pre": round(wrist_pre[1] - bbox_pre[1], 1),
            "wrist_to_bbox_bottom_pre": round(bbox_pre[3] - wrist_pre[1], 1),
            "wrist_to_bbox_top_post": round(wrist_post[1] - bbox_post[1], 1),
            "wrist_to_bbox_bottom_post": round(bbox_post[3] - wrist_post[1], 1),
        }
        # finger dir unit
        fx, fy = tr_off[0] - wr_off[0], tr_off[1] - wr_off[1]; fl = math.hypot(fx, fy)
        per_side[side]["finger_dir_pre"] = [round(fx / fl, 3), round(fy / fl, 3)]
        per_side[side]["finger_dir_post"] = [round(fx / fl, 3), round(-fy / fl, 3)]
        layers[side] = (flipped, c_new)
    plate.alpha_composite(lowers)
    paste_at(plate, load(os.path.join(SLICED, "Neck.png"), scale=1.05), 550 + OX, 360)
    paste_at(plate, load(os.path.join(SLICED, "Head_Front.png")), 550 + OX, 250)
    for side in ("L", "R"):
        lay, cen = layers[side]
        plate.alpha_composite(lay, (int(cen[0] - lay.size[0] / 2), int(cen[1] - lay.size[1] / 2)))
    gate = finish(plate, f"tpose-{tag}-VERTICAL-FLIP-INPLACE-20261031.png")
    results[tag] = {"hand": hfile, "operation": "VERTICAL FLIP IN PLACE", "gate": per_side, "no_crop": gate}
    print(tag, {s: per_side[s]["gate_post"]["verdict"] for s in per_side}, "nocrop", gate["pass"],
          "centre_shift", {s: per_side[s]["centre_shift_px"] for s in per_side})

json.dump(results, open(os.path.join(OUT, "measurements-vertical-flip-20261031.json"), "w"), indent=2)
print("DONE")
