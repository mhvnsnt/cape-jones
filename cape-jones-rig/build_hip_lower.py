"""HIP-LOWER FIX, Mars 2026-10-31 17:28-17:29 CDT.
Problem: in the over-exaggerated flex AND the deeper-squat exaggerated flex,
the hip joints sit TOO HIGH on the pelvis. The builder dipped the pelvis
(28px over-exaggerated, 52px deep squat) but kept HIP fixed at y740, so the
thigh tops sit high relative to the dropped pelvis.
Fix, BOTH sides, BOTH versions, new dated files only (true final untouched):
  - hip joint lowered 20px (y740 -> y760), both sides, still attached to pelvis
    (thigh top now sits inside the dropped pelvis piece, not above it)
  - knees EXACTLY where they were, feet EXACTLY where they were (ground y1299)
  - to keep the knee fixed with a lower hip, the thigh is re-angled to the
    same knee (tilt increases a few degrees, like bending on the knee) and
    foreshortened ~7-8% -- the front-view projection of a more-flexed hip
    (see HIP-LOWER-ANATOMY-20261031.md). Lower legs, knee caps, feet, arms,
    torso, pelvis, cape: unchanged from their source versions.
Anatomy (researched, not guessed): hip = femoral head in the acetabulum;
the acetabulum IS part of the pelvis, so the hip centre translates with the
pelvis in a squat -- it cannot stay fixed while the pelvis drops. Deep-squat
kinematics: hip flexion peaks ~120 deg, anterior pelvic tilt 15-33 deg
through the squat (MDPI overhead deep squat study). Full pelvis translation
(28/52px) is NOT applied here, because knees/feet are locked by Mars and
that would force 11-16% thigh shortening and change the approved squat
depth; 20px is the joint-seating correction Mars asked for -- "a little,
slightly", both versions already very close to perfect.
"""
from PIL import Image
import os, math
import numpy as np

RIG = "/home/hatch/workspace/cape-jones-rig"
BASE = os.path.join(RIG, "sliced")
CUT = os.path.join(RIG, "cut-limbs-v7c")
FLEX = os.path.join(RIG, "cut-limbs-v7c-flex-out")
OUT = os.path.join(RIG, "reposes-v7c-clean")
SCALE = 0.95
SHOULDER = {"L": (430, 445), "R": (670, 445)}
HIP_OLD = {"L": (470, 740), "R": (615, 740)}
HIP_DROP = 20
HIP = {"L": (470, 740 + HIP_DROP), "R": (615, 740 + HIP_DROP)}
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
LEG = {"L": ((95, 314), (77, 40)), "R": ((100, 314), (84, 40))}
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

def limb_layer(path, joint, angle, anchor, extra_scale=1.0):
    im = load(path)
    if extra_scale != 1.0:
        im = im.resize((int(im.size[0]*extra_scale), int(im.size[1]*extra_scale)), Image.LANCZOS)
        ax, ay = anchor[0]*SCALE*extra_scale, anchor[1]*SCALE*extra_scale
    else:
        ax, ay = anchor[0]*SCALE, anchor[1]*SCALE
    layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    layer.paste(im, (int(joint[0]-ax), int(joint[1]-ay)), im)
    return layer.rotate(angle, center=joint, expand=False)

def split_lower(path):
    im = Image.open(path).convert("RGBA")
    fa = np.array(im.copy()); fi = np.array(im.copy())
    fa[175:, :, 3] = 0; fi[:175, :, 3] = 0
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
    x0 = max(0, int(wrist[0]-radius)); x1 = min(1100, int(wrist[0]+radius))
    y0 = max(0, int(wrist[1]-radius)); y1 = min(1500, int(wrist[1]+radius))
    crop = canvas.crop((x0, y0, x1, y1)).convert("RGBA")
    a = np.array(crop); weak = a[:, :, 3] < 40; a[weak, 3] = 0
    canvas.paste(Image.fromarray(a), (x0, y0), Image.fromarray(a))
    return canvas

def solve_thigh(side, orig_angle, hip_new):
    """Return (new_angle, extra_scale, knee) with knee = original knee exactly."""
    ball, hip_anchor = LEG[side]
    vec = (ball[0]-hip_anchor[0], ball[1]-hip_anchor[1])
    hip_old = HIP_OLD[side]
    knee = (hip_old[0]+rot_vec(vec, orig_angle)[0]*SCALE,
            hip_old[1]+rot_vec(vec, orig_angle)[1]*SCALE)
    t = (knee[0]-hip_new[0], knee[1]-hip_new[1])
    base = (vec[0]*SCALE, vec[1]*SCALE)
    best = None
    for i in range(-9000, 9001):
        a = i/100.0
        r = rot_vec(base, a)
        # cosine of angle between r and t
        cosv = (r[0]*t[0]+r[1]*t[1])/(math.hypot(*r)*math.hypot(*t))
        if best is None or cosv > best[0]:
            best = (cosv, a)
    angle = best[1]
    scale = math.hypot(*t)/math.hypot(*base)
    return angle, scale, knee

def build(name, cfg, dip, shift=0):
    canvas = Image.new("RGBA", (1100, 1500), (128, 128, 128, 255))
    paste_at(canvas, load(os.path.join(BASE, "Cape_Back_Main.png")), 550, 410)
    knees = {}
    for side in ("L", "R"):
        hip = HIP[side]
        angle, escale, knee = solve_thigh(side, cfg["leg_upper"][side], hip)
        knees[side] = knee
        up, low, cap = LEG_PIECES[side]
        canvas.alpha_composite(limb_layer(os.path.join(CUT, up), hip, angle, LEG[side][1], extra_scale=escale))
        canvas.alpha_composite(limb_layer(os.path.join(CUT, low), knee, cfg["leg_lower"][side], (LEG[side][0][0], 0)))
        cap_at(canvas, os.path.join(CUT, cap), knee)
        print(f"  {side} thigh: old_angle={cfg['leg_upper'][side]} new_angle={angle:.2f} "
              f"foreshorten={escale:.3f} knee=({knee[0]:.0f},{knee[1]:.0f}) hip=({hip[0]},{hip[1]})")
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
        wvec = (WRIST[side][0]-ball[0], WRIST[side][1]-0)
        wrists[side] = (elbows[side][0]+rot_vec(wvec, cfg["arm_lower"][side])[0]*SCALE,
                        elbows[side][1]+rot_vec(wvec, cfg["arm_lower"][side])[1]*SCALE)
    for side in ("L", "R"):
        ball, _ = ARM[side]
        fore_piece, fist_piece = split_lower(os.path.join(FLEX, "Arm_Front_Lower_FlexOut.png" if side == "L" else "Arm_Back_Lower_FlexOut.png"))
        fore = rotated_piece(fore_piece, elbows[side], cfg["arm_lower"][side], (ball[0], 0))
        canvas.alpha_composite(fore)
        cap_at(canvas, os.path.join(CUT, ARM_CAP[side]), elbows[side])
        fist = rotated_piece(fist_piece, elbows[side], cfg["arm_lower"][side], (ball[0], 0))
        fist_rot = fist.rotate(cfg["fist"][side], center=wrists[side], expand=False)
        cap_layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
        cap_im = load(os.path.join(CUT, ARM_CAP[side]))
        cap_layer.paste(cap_im, (int(wrists[side][0]-cap_im.size[0]/2),
                                 int(wrists[side][1]-cap_im.size[1]/2)), cap_im)
        union = np.array(fore)[:, :, 3] | np.array(fist_rot)[:, :, 3]
        from PIL import ImageFilter
        union_im = Image.fromarray((union > 0).astype(np.uint8)*255).filter(ImageFilter.MaxFilter(7))
        ca = np.array(cap_layer); ma = np.array(union_im)
        ca[:, :, 3] = np.where(ma > 0, ca[:, :, 3], 0)
        canvas.alpha_composite(Image.fromarray(ca))
        canvas.alpha_composite(fist_rot)
    paste_at(canvas, load(os.path.join(BASE, "Neck.png"), scale=1.05), 550, 360+dip)
    paste_at(canvas, load(os.path.join(BASE, "Head_Front.png")), 550, 250+dip)
    for side in ("L", "R"):
        canvas = clean_wrist_zone(canvas, wrists[side])
    if shift:
        # Replicates the original deep-squat delivery shift: the deeper leg
        # bend shortens vertical projection, so the finished figure was
        # shifted down 29px to plant feet at y1299. Without it the deep
        # version floats at y1270 -- same correction, applied last.
        shifted = Image.new("RGBA", (1100, 1500), (128, 128, 128, 255))
        shifted.paste(canvas, (0, shift), canvas)
        canvas = shifted
    canvas.convert("RGB").save(os.path.join(OUT, name))
    print(name, "saved")

# OVER-EXAGGERATED (source: full-final-flex-over-exaggerated-cleaned): dip 28
build("full-final-flex-over-exaggerated-hip-lower-20261031.png",
    {"arm_upper": {"L": -70, "R": 70}, "arm_lower": {"L": 135, "R": -135},
     "fist": {"L": -75, "R": 75},
     "leg_upper": {"L": -22, "R": 22}, "leg_lower": {"L": 10, "R": -10}}, dip=28)
# DEEP SQUAT (source: full-final-flex-exaggerated-deep-squat): dip 52
build("full-final-flex-exaggerated-deep-squat-hip-lower-20261031.png",
    {"arm_upper": {"L": -70, "R": 70}, "arm_lower": {"L": 135, "R": -135},
     "fist": {"L": -75, "R": 75},
     "leg_upper": {"L": -34, "R": 34}, "leg_lower": {"L": 28, "R": -28}}, dip=52, shift=29)
