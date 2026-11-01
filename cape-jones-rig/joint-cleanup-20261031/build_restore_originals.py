"""True final flex (relaxed) + cleaned over-exaggerated flex.
Mars feedback 2026-10-31 16:40 CDT on full-final-flex-v7c-clean-20261031.png:
  over-exaggerated version is REALLY GOOD / REALLY CLOSE -> keep as its own frame,
  cleaned up around the wrists (new file, same pose otherwise).
  TRUE final flex: a little more relaxed in the arms + wrist cleanup, with:
    (1) biceps angle UP toward head ~15 deg more
    (2) wrists CLEANED UP at the wrist/forearm connection (CORRECTION 16:46 CDT:
        "clent up" was speech-to-text for CLEANED UP, not clenched. Do NOT roll
        the fists more, do NOT clench more. Clean seams only.)
    (3) forearm-to-wrist angle OPENED UP ~5 deg (more space, less acute fold)
Method: piece-level, never image-space rotation of the finished composite
(the image-space attempt on the first full-final was rejected: it erased
shoulder/cape pixels). Lower piece split at piece y=175/185 (10px overlap);
fist rotated in POSE space about the pose wrist point; wrist cap BEHIND
the fist (side arcs only, never a ring across the fist face); isolated
specks removed in the wrist box; alpha<30 dropped in the wrist zone only.
"""
from PIL import Image
import os, math
import numpy as np

RIG = "/home/hatch/workspace/cape-jones-rig"
BASE = os.path.join(RIG, "sliced")
CUT = os.path.join(RIG, "cut-limbs-v7c")
FLEX = os.path.join(RIG, "cut-limbs-v7c-flex-out")
OUT = os.path.join(RIG, "joint-cleanup-20261031", "restored")
SCALE = 0.95
SHOULDER = {"L": (430, 445), "R": (670, 445)}
HIP = {"L": (470, 740), "R": (615, 740)}
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
LEG = {"L": ((95, 314), (77, 40)), "R": ((100, 314), (84, 40))}
# FlexOut lower piece geometry (piece coords, unscaled):
# wrist pivot in piece, anchor x = ball[0] (lower anchor is (ball_x, 0))
WRIST = {"L": (79, 180), "R": (102, 180)}
LEG_PIECES = {"L": ("Leg_Front_Upper.png", "Leg_Front_Lower.png", "Leg_Front_Cap.png"),
              "R": ("Leg_Back_Upper.png", "Leg_Back_Lower.png", "Leg_Back_Cap.png")}
ARM_UP = {"L": "Arm_Front_Upper.png", "R": "Arm_Back_Upper.png"}
ARM_CAP = {"L": "Arm_Front_Cap.png", "R": "Arm_Back_Cap.png"}

def load(p, scale=SCALE):
    im = Image.open(p).convert("RGBA")
    return im.resize((int(im.size[0]*scale), int(im.size[1]*scale)), Image.LANCZOS)

def paste_at(c, im, cx, top):
    c.paste(im, (int(cx - im.size[0]/2), int(top)), im)

def rot_vec(v, angle_deg):
    a = math.radians(angle_deg); x, y = v
    return (x*math.cos(a) + y*math.sin(a), -x*math.sin(a) + y*math.cos(a))

def limb_layer(path, joint, angle, anchor):
    """Transparent layer with the piece placed at joint and rotated about joint."""
    im = load(path); ax, ay = anchor[0]*SCALE, anchor[1]*SCALE
    layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    layer.paste(im, (int(joint[0]-ax), int(joint[1]-ay)), im)
    return layer.rotate(angle, center=joint, expand=False)

def split_lower(path):
    """Return (forearm layer-piece, fist layer-piece) in piece coords, 10px overlap."""
    im = Image.open(path).convert("RGBA")
    fore = im.copy(); fist = im.copy()
    fa = np.array(fore); fi = np.array(fist)
    fa[175:, :, 3] = 0          # forearm keeps y<175
    fi[:175, :, 3] = 0          # fist keeps y>=175 (overlap zone 175-185 kept in both)
    # NOTE: overlap is 175..185 in the ORIGINAL piece split used by the
    # full-final builder (forearm y<185, fist y>=175); here forearm is cut
    # at 175 and fist at 175 so the seam is a single clean line, then the
    # fist is NOT seated deeper and NOT rolled extra (correction 16:46 CDT:
    # cleaned up only). The 10px overlap zone keeps the seam gap-free.
    return Image.fromarray(fa), Image.fromarray(fi)

def rotated_piece(piece, joint, angle, anchor):
    im = piece.resize((int(piece.size[0]*SCALE), int(piece.size[1]*SCALE)), Image.LANCZOS)
    ax, ay = anchor[0]*SCALE, anchor[1]*SCALE
    layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    layer.paste(im, (int(joint[0]-ax), int(joint[1]-ay)), im)
    return layer.rotate(angle, center=joint, expand=False)

def cap_at(c, path, joint):
    im = load(path)
    c.paste(im, (int(joint[0]-im.size[0]/2), int(joint[1]-im.size[1]/2)), im)

def clean_wrist_zone(canvas, wrist, radius=70):
    """Wrist cleanup, wrist zone only: drop faint fringe alpha and isolated specks."""
    x0 = max(0, int(wrist[0]-radius)); x1 = min(1100, int(wrist[0]+radius))
    y0 = max(0, int(wrist[1]-radius)); y1 = min(1500, int(wrist[1]+radius))
    crop = canvas.crop((x0, y0, x1, y1)).convert("RGBA")
    a = np.array(crop)
    # drop faint fringe (alpha < 40) in the zone only
    weak = a[:, :, 3] < 40
    a[weak, 3] = 0
    canvas.paste(Image.fromarray(a), (x0, y0), Image.fromarray(a))
    return canvas

def build(name, cfg, dip=28):
    canvas = Image.new("RGBA", (1100, 1500), (128, 128, 128, 255))
    paste_at(canvas, load(os.path.join(BASE, "Cape_Back_Main.png")), 550, 410)  # NOT dipped: hem unchanged
    # legs (feet planted, unchanged by dip)
    for side in ("L", "R"):
        hip = HIP[side]; ball, hip_anchor = LEG[side]
        vec = (ball[0]-hip_anchor[0], ball[1]-hip_anchor[1])
        up, low, cap = LEG_PIECES[side]
        canvas.alpha_composite(limb_layer(os.path.join(CUT, up), hip, cfg["leg_upper"][side], hip_anchor))
        knee = (hip[0]+rot_vec(vec, cfg["leg_upper"][side])[0]*SCALE,
                hip[1]+rot_vec(vec, cfg["leg_upper"][side])[1]*SCALE)
        canvas.alpha_composite(limb_layer(os.path.join(CUT, low), knee, cfg["leg_lower"][side], (ball[0], 0)))
        cap_at(canvas, os.path.join(CUT, cap), knee)
    # dipped upper body: pelvis, collar, torso, belt, neck, head + shoulders
    paste_at(canvas, load(os.path.join(BASE, "Pelvis.png")), 550, 680+dip)
    paste_at(canvas, load(os.path.join(BASE, "Cape_Collar.png")), 550, 370+dip)
    paste_at(canvas, load(os.path.join(BASE, "Torso_Chest.png")), 550, 400+dip)
    paste_at(canvas, load(os.path.join(BASE, "Belt_Overlay.png")), 550, 670+dip)
    elbows, wrists = {}, {}
    for side in ("L", "R"):
        ball, sh_anchor = ARM[side]; vec = (ball[0]-sh_anchor[0], ball[1]-sh_anchor[1])
        sh = (SHOULDER[side][0], SHOULDER[side][1]+dip)
        canvas.alpha_composite(limb_layer(os.path.join(CUT, ARM_UP[side]), sh, cfg["arm_upper"][side], sh_anchor))
        elbows[side] = (sh[0]+rot_vec(vec, cfg["arm_upper"][side])[0]*SCALE,
                        sh[1]+rot_vec(vec, cfg["arm_upper"][side])[1]*SCALE)
        # pose wrist point: elbow + rotated (wrist_pivot - lower_anchor) * SCALE
        wvec = (WRIST[side][0]-ball[0], WRIST[side][1]-0)
        wrists[side] = (elbows[side][0]+rot_vec(wvec, cfg["arm_lower"][side])[0]*SCALE,
                        elbows[side][1]+rot_vec(wvec, cfg["arm_lower"][side])[1]*SCALE)
    for side in ("L", "R"):
        ball, _ = ARM[side]
        fore_piece, fist_piece = split_lower(os.path.join(FLEX, "Arm_Front_Lower_FlexOut.png" if side == "L" else "Arm_Back_Lower_FlexOut.png"))
        fore = rotated_piece(fore_piece, elbows[side], cfg["arm_lower"][side], (ball[0], 0))
        canvas.alpha_composite(fore)
        cap_at(canvas, os.path.join(CUT, ARM_CAP[side]), elbows[side])  # elbow cap (existing language)
        fist = rotated_piece(fist_piece, elbows[side], cfg["arm_lower"][side], (ball[0], 0))
        # pose-space fist rotation about the wrist point, no extra seating/roll
        fist_rot = fist.rotate(cfg["fist"][side], center=wrists[side], expand=False)
        # wrist cap BEHIND fist, MASKED to the forearm+fist union (dilated 3px):
        # it fills the seam only. An unmasked cap ball peeking into the
        # background behind the fist was caught on viewing the wrist crops
        # and is exactly the unclean wrist look Mars flagged.
        cap_layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
        cap_im = load(os.path.join(CUT, ARM_CAP[side]))
        cap_layer.paste(cap_im, (int(wrists[side][0]-cap_im.size[0]/2),
                                 int(wrists[side][1]-cap_im.size[1]/2)), cap_im)
        union = np.array(fore)[:, :, 3] | np.array(fist_rot)[:, :, 3]
        union_im = Image.fromarray((union > 0).astype(np.uint8)*255).filter(
            __import__("PIL.ImageFilter", fromlist=["MaxFilter"]).MaxFilter(7))
        ca = np.array(cap_layer); ma = np.array(union_im)
        ca[:, :, 3] = np.where(ma > 0, ca[:, :, 3], 0)
        canvas.alpha_composite(Image.fromarray(ca))
        canvas.alpha_composite(fist_rot)
    paste_at(canvas, load(os.path.join(BASE, "Neck.png"), scale=1.05), 550, 360+dip)
    paste_at(canvas, load(os.path.join(BASE, "Head_Front.png")), 550, 250+dip)
    for side in ("L", "R"):
        canvas = clean_wrist_zone(canvas, wrists[side])
    canvas.convert("RGB").save(os.path.join(OUT, name))
    print(name, "wrists:", {k: (round(v[0]), round(v[1])) for k, v in wrists.items()},
          "elbows:", {k: (round(v[0]), round(v[1])) for k, v in elbows.items()})
    return wrists

# OVER-EXAGGERATED, cleaned: same pose as full-final, wrist cleanup only
over_wrists = build("full-final-flex-over-exaggerated-cleaned-20261031.png",
    {"arm_upper": {"L": -70, "R": 70}, "arm_lower": {"L": 135, "R": -135},
     "fist": {"L": -75, "R": 75},
     "leg_upper": {"L": -22, "R": 22}, "leg_lower": {"L": 10, "R": -10}})
# TRUE FINAL, relaxed: biceps +15 toward head, lowers relaxed 10 deg,
# fist angle opened 5 deg, wrists cleaned up only (no clench, no extra roll)
true_wrists = build("true-final-flex-relaxed-clean-20261031.png",
    {"arm_upper": {"L": -85, "R": 85}, "arm_lower": {"L": 145, "R": -145},
     "fist": {"L": -70, "R": 70},
     "leg_upper": {"L": -22, "R": 22}, "leg_lower": {"L": 10, "R": -10}})
print("OVER wrists", over_wrists)
print("TRUE wrists", true_wrists)
