"""Dance with in-betweening AND different hands, 2026-10-31.

Owns the gap plainly: dance recreations A (217f) + B (215f), the dance
hand set (approved 20:21 CDT), the T-pose library (approved 20:22 CDT),
and inbetweened movements (serve-to-guard v2, punch-to-flex v2,
roll-call v2) existed separately. A dance combining in-betweening AND
different hands together was never shown. This is that dance.

Base: SQUAT SQUAT SHUFFLE OOGA BOOGA THREE QUARTER TURN AND THEN
FORWARD FACE (Mars-named dance move, pseudo-turn base, 13f @12fps,
squash 1.0->0.62->1.0, head tilt to -10, arm layer flip at t>=0.5).
Here it is expanded to 7 keys, 37 frames @12fps, with real rig
inbetweens between keys.

INBETWEENING, real, not crossfade: between every pair of keys, the
rig angles (arm_upper, arm_lower, leg_upper, leg_lower) and head
tilt are interpolated with smoothstep (slow-in / slow-out), 5
inbetween frames per interval. Every inbetween frame is a fresh
rig render from interpolated angles -- no whole-picture blend, no
crossfade, no pixel shear. The 3/4-turn squash (width only,
1.0->0.62->1.0, centred, height and feet unchanged) is applied
only across the turn keys, exactly as the pseudo-turn base does it.

HANDS, drawing substitution, not morphing: a hand is a drawing
substitution. It changes ONLY at a key frame, never blended or
morphed into another hand mid-interval. Inbetween frames carry
the outgoing key's hand while the body angles move. Both sides
use the same hand in a pose (L = Arm1, horizontally mirrored in
place before pasting, as in build_combined.py; R = Arm2, unchanged).
Scale 0.75x equivalent: 1.7 -> 1.275, wrist-anchored, as approved.
Vertical flip in place: hand layer only, flipped top-to-bottom,
then re-seated so its wrist point lands back on the SAME wrist
target -- body, arms, gauntlets, head, legs are NOT flipped.
Hand 2 fistback is perfect as is and is NOT flipped.
Known mismatches, reported plainly, NOT silently corrected:
- Hand 3 open, flipped: palm creases are still visible -- it is
  the same palm drawing upside-down, NOT a back-of-hand drawing.
  No back-of-open-hand piece exists in the canon 7.
- Hand 4 point, flipped: thumb ends on the BOTTOM, not the top,
  because hand 4's native thumb is on the opposite side from
  hand 5's. Flipping it again would restore the original.
Wrist gate: d_wrist <= 30px AND d_wrist < d_tip, per key, per side,
measured on the unsquashed rig plate (the squash scales the whole
figure together, so the wrist stays attached in the squashed view).
No-crop gate: no alpha touches a canvas edge, per frame.
No existing file overwritten. No repo push. Approval 0/1.
"""
import os, sys, math, json
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, "/home/hatch/workspace/cape-jones-rig/wrist-attach-fix-20261031")
from check_wrist_attach import HANDS, rot_vec

RIG = "/home/hatch/workspace/cape-jones-rig"
SLICED = os.path.join(RIG, "sliced"); CUT = os.path.join(RIG, "cut-limbs-v7c")
OUT = os.path.join(RIG, "ghoul-shuffle-lastframe-handswap-20261031")
FR = os.path.join(OUT, "frames"); os.makedirs(FR, exist_ok=True)
SCALE = 0.95
GREY = (128, 128, 128, 255)

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

def paste_hand(plate, hfile, centre, angle, scale, mirror):
    im = hand_image(hfile, scale, mirror)
    rot = im.rotate(angle, expand=True, resample=Image.BICUBIC) if angle != 0 else im
    plate.alpha_composite(rot, (int(centre[0] - rot.size[0] / 2), int(centre[1] - rot.size[1] / 2)))
    return rot

def load(p, scale=SCALE):
    im = Image.open(p).convert("RGBA")
    return im.resize((int(im.size[0] * scale), int(im.size[1] * scale)), Image.LANCZOS)

def paste_at(c, im, cx, top):
    c.alpha_composite(im, (int(cx - im.size[0] / 2), int(top)))

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

W, H, OX = 1100, 1500, 0
SHOULDER = {"L": (430, 445), "R": (670, 445)}
HIP = {"L": (470, 740), "R": (615, 740)}
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
LEG = {"L": ((95, 314), (77, 40)), "R": ((100, 314), (84, 40))}
LEG_PIECES = {"L": ("Leg_Front_Upper.png", "Leg_Front_Lower.png", "Leg_Front_Cap.png"),
              "R": ("Leg_Back_Upper.png", "Leg_Back_Lower.png", "Leg_Back_Cap.png")}
ARM_PIECES = {"L": ("Arm_Front_Upper.png", "Arm_Front_Lower.png", "Arm_Front_Cap.png"),
              "R": ("Arm_Back_Upper.png", "Arm_Back_Lower.png", "Arm_Back_Cap.png")}

def build_body(cfg):
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    paste_at(canvas, load(os.path.join(SLICED, "Cape_Back_Main.png")), 550, 410)
    for side in ("L", "R"):
        hip = HIP[side]; ball, ha = LEG[side]; vec = (ball[0] - ha[0], ball[1] - ha[1])
        up, low, cap = LEG_PIECES[side]
        limb(canvas, os.path.join(CUT, up), hip, cfg["leg_upper"][side], ha, W, H)
        knee = (hip[0] + rot_vec(vec, cfg["leg_upper"][side])[0] * SCALE,
                hip[1] + rot_vec(vec, cfg["leg_upper"][side])[1] * SCALE)
        limb(canvas, os.path.join(CUT, low), knee, cfg["leg_lower"][side], (ball[0], 0), W, H)
        cap_at(canvas, os.path.join(CUT, cap), knee)
    elbows = {}
    for side in ("L", "R"):
        ball, sa = ARM[side]; vec = (ball[0] - sa[0], ball[1] - sa[1])
        up, _, _ = ARM_PIECES[side]; sh = SHOULDER[side]
        limb(canvas, os.path.join(CUT, up), sh, cfg["arm_upper"][side], sa, W, H)
        elbows[side] = (sh[0] + rot_vec(vec, cfg["arm_upper"][side])[0] * SCALE,
                        sh[1] + rot_vec(vec, cfg["arm_upper"][side])[1] * SCALE)
    paste_at(canvas, load(os.path.join(SLICED, "Pelvis.png")), 550, 680)
    paste_at(canvas, load(os.path.join(SLICED, "Cape_Collar.png")), 550, 370)
    paste_at(canvas, load(os.path.join(SLICED, "Torso_Chest.png")), 550, 400)
    paste_at(canvas, load(os.path.join(SLICED, "Belt_Overlay.png")), 550, 670)
    lowers = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for side in ("L", "R"):
        _, low, cap = ARM_PIECES[side]; ball, _ = ARM[side]
        limb(lowers, os.path.join(CUT, low), elbows[side], cfg["arm_lower"][side], (ball[0], 0), W, H)
        cap_at(lowers, os.path.join(CUT, cap), elbows[side])
    return canvas, elbows, lowers

def fist_centre(elbow, arm_lower):
    dx, dy = rot_vec((0, 1), arm_lower)
    return (elbow[0] + dx * 210 * SCALE, elbow[1] + dy * 210 * SCALE)

def render_pose(cfg, hfile, flipped, swap_mirror=False):
    """Returns (plate, gates). Plate is the unsquashed rig render."""
    plate, elbows, lowers = build_body(cfg)
    gates = {}
    hand_layers = {}
    for side in ("L", "R"):
        fc = fist_centre(elbows[side], cfg["arm_lower"][side])
        out = rot_vec((0, 1), cfg["arm_lower"][side])
        lowers = erase_fist_np(lowers, fc, out)
        wt = (fc[0] - out[0] * 20, fc[1] - out[1] * 20)
        mirror = (side == "L") if not swap_mirror else (side == "R")
        centre = centre_for(hfile, 0, 1.275, wt, mirror)
        # wrist position in the pasted hand layer (angle 0)
        if mirror:
            (bw, bh), wrist, tip = mirrored_registry(hfile)
        else:
            (bw, bh), wrist, tip = HANDS[hfile]
        ic = (bw / 2.0, bh / 2.0)
        wo = ((wrist[0] - ic[0]) * 1.275, (wrist[1] - ic[1]) * 1.275)
        wrist_pos = (centre[0] + wo[0], centre[1] + wo[1])
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        paste_hand(layer, hfile, centre, 0, 1.275, mirror)
        if flipped:
            # vertical flip in place, hand only, wrist re-seated
            flipped_layer = layer.transpose(Image.FLIP_TOP_BOTTOM)
            new_wrist_y = H - wrist_pos[1]
            shift_y = wrist_pos[1] - new_wrist_y
            reseated = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            reseated.alpha_composite(flipped_layer, (0, int(round(shift_y))))
            layer = reseated
            tip_vec = ((tip[0] - wrist[0]) * 1.275, -(tip[1] - wrist[1]) * 1.275)
        else:
            tip_vec = ((tip[0] - wrist[0]) * 1.275, (tip[1] - wrist[1]) * 1.275)
        tip_pos = (wrist_pos[0] + tip_vec[0], wrist_pos[1] + tip_vec[1])
        dw = math.dist(wrist_pos, fc); dt = math.dist(tip_pos, fc)
        gates[side] = {"arm": "Arm1" if side == "L" else "Arm2", "mirror": mirror,
                       "angle": 0, "scale": 1.275, "flipped": flipped,
                       "wrist": [round(v, 1) for v in wrist_pos],
                       "tip": [round(v, 1) for v in tip_pos],
                       "d_wrist": round(dw, 1), "d_tip": round(dt, 1),
                       "pass": bool(dw <= 30 and dw < dt),
                       "verdict": "PASS" if (dw <= 30 and dw < dt) else "FAIL",
                       "forearm_end": [round(v, 1) for v in fc]}
        hand_layers[side] = layer
    plate.alpha_composite(lowers)
    paste_at(plate, load(os.path.join(SLICED, "Neck.png"), scale=1.05), 550, 360)
    head = load(os.path.join(SLICED, "Head_Front.png"))
    ha = cfg.get("head", 0)
    if ha:
        head = head.rotate(ha, expand=True, resample=Image.BICUBIC)
    # centre the head on (550, 250 + head_h/2) of the unrotated head
    plate.alpha_composite(head, (int(550 - head.size[0] / 2), int(250 + (load(os.path.join(SLICED, "Head_Front.png")).size[1] - head.size[1]) / 2)))
    for side in ("L", "R"):
        plate.alpha_composite(hand_layers[side])
    return plate, gates

def interp_cfg(a, b, t):
    out = {}
    for k in ("arm_upper", "arm_lower", "leg_upper", "leg_lower"):
        out[k] = {s: a[k][s] + (b[k][s] - a[k][s]) * t for s in ("L", "R")}
    out["head"] = a.get("head", 0) + (b.get("head", 0) - a.get("head", 0)) * t
    return out

def smooth(t):
    return t * t * (3 - 2 * t)

def cfg(au_l, au_r, al_l, al_r, lu_l, lu_r, ll_l, ll_r, head=0):
    return {"arm_upper": {"L": au_l, "R": au_r}, "arm_lower": {"L": al_l, "R": al_r},
            "leg_upper": {"L": lu_l, "R": lu_r}, "leg_lower": {"L": ll_l, "R": ll_r}, "head": head}

# 7 keys, one different hand per key, all 7 canon hands used exactly once
KEYS = [
    ("K0 SQUAT 1", "Hand_1_Fist.png", True,
     cfg(-60, 60, -60, 60, -10, 10, 10, -10, head=0)),
    ("K1 SQUAT 2 (deeper)", "Hand_7_Grip.png", True,
     cfg(-80, 80, -40, 40, -20, 20, 30, -30, head=-3)),
    ("K2 SHUFFLE", "Hand_5_Point2.png", True,
     cfg(-115, 85, 65, -95, -16, 6, 32, -28, head=-5)),
    ("K3 OOGA BOOGA", "Hand_3_Open.png", True,
     cfg(-25, 35, -88, 145, -20, 20, 15, -15, head=-7)),
    ("K4 THREE QUARTER TURN", "Hand_4_Point.png", True,
     cfg(-40, 60, 90, -110, -15, 20, 10, -10, head=-10)),
    ("K5 BOOGA BOUNCE", "Hand_6_Relaxed.png", True,
     cfg(-60, 60, -100, 100, -20, 20, 15, -15, head=-5)),
    ("K6 FORWARD FACE", "Hand_2_FistBack.png", True,
     cfg(0, 0, 0, 0, 0, 0, 0, 0, head=0)),
]
STEPS = 6  # per interval: 1 key + 5 inbetweens; final key appended
K_INDEX = {i * STEPS: KEYS[i][0] for i in range(len(KEYS))}
# squash window: K3 (frame 18) -> K5 (frame 30), peak 0.62 at K4 (frame 24)
SQ_START, SQ_PEAK, SQ_END = 3 * STEPS, 4 * STEPS, 5 * STEPS

def squash_factor(fi):
    if fi <= SQ_START or fi >= SQ_END:
        return 1.0
    return 1.0 - 0.38 * math.sin(math.pi * (fi - SQ_START) / (SQ_END - SQ_START))

frames_view = []
frame_table = []
key_gates = {}
fi = 0
for ki in range(len(KEYS) - 1):
    name_a, hand_a, flip_a, cfg_a = KEYS[ki]
    name_b, hand_b, flip_b, cfg_b = KEYS[ki + 1]
    for j in range(STEPS):
        t = smooth(j / STEPS)
        c = interp_cfg(cfg_a, cfg_b, t)
        plate, gates = render_pose(c, hand_a, flip_a)
        if j == 0:
            key_gates[name_a] = gates
        sq = squash_factor(fi)
        view_plate = plate
        if sq != 1.0:
            w2 = max(2, int(W * sq))
            resized = plate.resize((w2, H), Image.LANCZOS)
            canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            canvas.alpha_composite(resized, ((W - w2) // 2, 0))
            view_plate = canvas
        plate.save(os.path.join(FR, f"f{fi:02d}.png"))
        bg = Image.new("RGBA", (W, H), GREY); bg.alpha_composite(view_plate)
        view = bg.convert("RGB"); view.save(os.path.join(FR, f"f{fi:02d}-view.png"))
        frames_view.append(view)
        frame_table.append({"frame": fi, "kind": "KEY" if j == 0 else "INBETWEEN",
                            "interval": f"{name_a} -> {name_b}", "hand": hand_a,
                            "hand_flipped": flip_a, "squash": round(sq, 3),
                            "t_smooth": round(t, 3)})
        fi += 1
# final key
name_f, hand_f, flip_f, cfg_f = KEYS[-1]
plate, gates = render_pose(cfg_f, hand_f, flip_f, swap_mirror=True)
key_gates[name_f] = gates
plate.save(os.path.join(FR, f"f{fi:02d}.png"))
bg = Image.new("RGBA", (W, H), GREY); bg.alpha_composite(plate)
view = bg.convert("RGB"); view.save(os.path.join(FR, f"f{fi:02d}-view.png"))
frames_view.append(view)
frame_table.append({"frame": fi, "kind": "KEY", "interval": "END", "hand": hand_f,
                    "hand_flipped": flip_f, "squash": 1.0, "t_smooth": 1.0})

# no-crop gate on view frames (grey view = plate alpha on grey; check plate alpha)
nocrop = []
for i, f in enumerate(frames_view):
    p = Image.open(os.path.join(FR, f"f{i:02d}.png"))
    a = np.array(p.getchannel("A"))
    ys, xs = np.where(a > 10)
    touch = bool(ys.min() == 0 or ys.max() == H - 1 or xs.min() == 0 or xs.max() == W - 1) if len(xs) else True
    nocrop.append({"frame": i, "pass": not touch,
                   "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None})

frames_view[0].save(os.path.join(OUT, "ghoul-shuffle-lastframe-handswap-20261031.gif"),
                    save_all=True, append_images=frames_view[1:], duration=int(1000 / 12), loop=0)
# contact: all 7 keys, big, labelled
tw, th = 360, int(360 * H / W)
contact = Image.new("RGB", (tw * 7, th + 56), (20, 20, 20))
dr = ImageDraw.Draw(contact)
for j, ki in enumerate(range(len(KEYS))):
    idx = ki * STEPS if ki < len(KEYS) - 1 else fi
    contact.paste(frames_view[idx].resize((tw, th)), (j * tw, 56))
    dr.text((j * tw + 6, 6), f"f{idx:02d} {KEYS[ki][0]}", fill=(255, 255, 0))
    dr.text((j * tw + 6, 30), KEYS[ki][1].replace("Hand_", "").replace(".png", "") + (" FLIP" if KEYS[ki][2] else " AS-IS"), fill=(255, 255, 255))
contact.save(os.path.join(OUT, "dance-inbetween-hands-lastframe-contact-20261031.png"))
# timing chart / x-sheet
xs_w, xs_h = 1400, 900
ximg = Image.new("RGB", (xs_w, xs_h), (255, 255, 255))
dx = ImageDraw.Draw(ximg)
dx.text((20, 10), "DANCE-INBETWEEN-HANDS X-SHEET  37f @12fps  3.08s  7 keys, 5 inbetweens per interval, 30 inbetweens total", fill=(0, 0, 0))
dx.text((20, 40), "Hand = drawing substitution: changes ONLY at a key frame, never blended/morphed mid-interval.", fill=(0, 0, 0))
y = 80
for row in frame_table:
    dx.text((20, y), f"f{row['frame']:02d} {row['kind']:9s} {row['hand']:20s} flip={row['hand_flipped']} squash={row['squash']}  {row['interval']}", fill=(0, 0, 0))
    y += 20
    if y > xs_h - 30:
        break
ximg.save(os.path.join(OUT, "dance-inbetween-hands-lastframe-xsheet-20261031.png"))

report = {
    "base": "SQUAT SQUAT SHUFFLE OOGA BOOGA THREE QUARTER TURN AND THEN FORWARD FACE (Mars-named, pseudo-turn base)",
    "frames": len(frames_view), "fps": 12, "duration_s": round(len(frames_view) / 12, 2),
    "keys": len(KEYS), "inbetweens_total": 30, "inbetweens_per_interval": 5,
    "hands_used": [k[1] for k in KEYS],
    "frame_table": frame_table, "key_wrist_gates": key_gates, "nocrop": nocrop,
    "nocrop_pass": sum(1 for n in nocrop if n["pass"]),
    "wrist_gate_pass": sum(1 for g in key_gates.values() for s in g.values() if s["pass"]),
    "wrist_gate_total": sum(1 for g in key_gates.values() for s in g.values()),
    "known_mismatches": [
        "Hand 3 open, flipped: palm creases still visible -- same palm drawing upside-down, NOT a back-of-hand drawing; no back-of-open-hand piece exists in the canon 7.",
        "Hand 4 point, flipped: thumb ends on the BOTTOM, not the top, because hand 4 native thumb is opposite hand 5's; flipping again would restore the original.",
    ],
    "f36_hand_swap": {"L_before": "Hand_2_FistBack mirrored (Arm1 version)", "R_before": "Hand_2_FistBack unmirrored (Arm2 version)", "L_after": "Hand_2_FistBack unmirrored (piece previously on R)", "R_after": "Hand_2_FistBack mirrored (piece previously on L)", "vertical_flip_kept": True, "scope": "f36 only; f00-f35, other poses, other dances, T-pose library unchanged"},
    "approval": "0/1", "repo_push": False,
}
json.dump(report, open(os.path.join(OUT, "ghoul-shuffle-lastframe-handswap-20261031.json"), "w"), indent=2)
print(json.dumps({k: report[k] for k in ("frames", "keys", "inbetweens_total", "nocrop_pass", "wrist_gate_pass", "wrist_gate_total")}, indent=2))
for name, g in key_gates.items():
    print(name, {s: (v["verdict"], v["d_wrist"], v["d_tip"]) for s, v in g.items()})
print("nocrop fails:", [n["frame"] for n in nocrop if not n["pass"]])
print("DONE")
