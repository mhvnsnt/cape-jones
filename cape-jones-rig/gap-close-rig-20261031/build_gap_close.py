"""Cape Jones GAP CLOSURE chunk A — gap-close-rig-20261031.
Original Cape Jones rig pieces only; methods only from other shows.
Labels go on catalogue/sheet images only, never baked into clean pieces.
All outputs are NEW files in this folder; nothing Mars has seen is overwritten.
Geometry constants (shoulder/hip/ball anchors, SCALE) are the v7c rig geometry,
re-implemented here (joint_locked_rig_v7c.py was read first; its build() is NOT
imported, because importing it re-runs its own builds into reposes-v7c).
"""
from PIL import Image, ImageDraw, ImageFilter
import os, math, json
import numpy as np

RIG = "/home/hatch/workspace/cape-jones-rig"
OUT = "/home/hatch/workspace/cape-jones-rig/gap-close-rig-20261031"
BASE = os.path.join(RIG, "sliced")
CUT = os.path.join(RIG, "cut-limbs-v7c")
FLEX = os.path.join(RIG, "cut-limbs-v7c-flex-out")
OUTFIX = os.path.join(RIG, "cut-limbs-v7c-gauntlet-out-fixed")
SCALE = 0.95
SHOULDER = {"L": (430, 445), "R": (670, 445)}
HIP = {"L": (470, 740), "R": (615, 740)}
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
LEG = {"L": ((95, 314), (77, 40)), "R": ((100, 314), (84, 40))}
LEG_PIECES = {"L": ("Leg_Front_Upper.png", "Leg_Front_Lower.png", "Leg_Front_Cap.png"),
              "R": ("Leg_Back_Upper.png", "Leg_Back_Lower.png", "Leg_Back_Cap.png")}
ARM_UP = {"L": "Arm_Front_Upper.png", "R": "Arm_Back_Upper.png"}
ARM_LOW = {"L": "Arm_Front_Lower.png", "R": "Arm_Back_Lower.png"}
ARM_CAP = {"L": "Arm_Front_Cap.png", "R": "Arm_Back_Cap.png"}

def load(p, scale=SCALE):
    im = Image.open(p).convert("RGBA")
    return im.resize((int(im.size[0]*scale), int(im.size[1]*scale)), Image.LANCZOS)

def load1(p):
    return Image.open(p).convert("RGBA")

def paste_at(c, im, cx, top):
    c.paste(im, (int(cx-im.size[0]/2), int(top)), im)

def rot_vec(v, a_deg):
    a = math.radians(a_deg); x, y = v
    return (x*math.cos(a)+y*math.sin(a), -x*math.sin(a)+y*math.cos(a))

def limb_layer(path, joint, angle, anchor, scale=SCALE):
    im = load(path, scale); ax, ay = anchor[0]*scale, anchor[1]*scale
    layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    layer.paste(im, (int(joint[0]-ax), int(joint[1]-ay)), im)
    return layer.rotate(angle, center=joint, expand=False)

def limb_layer_w(path, joint, angle, anchor, W, scale=SCALE):
    im = load(path, scale); ax, ay = anchor[0]*scale, anchor[1]*scale
    layer = Image.new("RGBA", (W, 1500), (0, 0, 0, 0))
    layer.paste(im, (int(joint[0]-ax), int(joint[1]-ay)), im)
    return layer.rotate(angle, center=joint, expand=False)

def cap_at(c, path, joint):
    im = load(path)
    c.paste(im, (int(joint[0]-im.size[0]/2), int(joint[1]-im.size[1]/2)), im)

def trim(im):
    a = np.array(im)[:, :, 3] > 10
    ys, xs = np.where(a)
    if len(xs) == 0: return im
    return im.crop((xs.min(), ys.min(), xs.max()+1, ys.max()+1))

def save(im, name):
    p = os.path.join(OUT, name); im.save(p); print("saved", name, im.size)
    return p

def verify(path):
    im = Image.open(path); a = np.array(im.convert("RGBA"))[:, :, 3]
    assert im.mode == "RGBA" and (a > 10).sum() > 0, path
    return (a > 10).sum()

# ---------------------------------------------------------------- 1. MISSING PIECES
# --- neck cylinders x5 from sliced/Neck.png
neck = load1(os.path.join(BASE, "Neck.png"))
neck_specs = [
    ("neck-01-base-20261031.png", lambda im: im),
    ("neck-02-short-20261031.png", lambda im: im.resize((im.size[0], int(im.size[1]*0.70)), Image.LANCZOS)),
    ("neck-03-long-20261031.png", lambda im: im.resize((im.size[0], int(im.size[1]*1.35)), Image.LANCZOS)),
    ("neck-04-tilt-left-20261031.png", lambda im: im.rotate(15, expand=True, resample=Image.BICUBIC)),
    ("neck-05-tilt-right-long-20261031.png", lambda im: im.resize((im.size[0], int(im.size[1]*1.20)), Image.LANCZOS).rotate(-15, expand=True, resample=Image.BICUBIC)),
]
neck_files = []
for name, fn in neck_specs:
    out = fn(neck.copy()); save(out, "gap-close-" + name); neck_files.append("gap-close-" + name)

# --- blank heads x5 from Head_Front
head = load1(os.path.join(BASE, "Head_Front.png"))
COWL = (92, 40, 115, 255); SKIN = (238, 174, 128, 255)
def blank_head():
    im = head.copy(); d = ImageDraw.Draw(im)
    # eye band: cowl purple over both eye openings (x15-105, y64-90), keep outline/nose
    d.rectangle((16, 64, 104, 90), fill=COWL)
    # mouth zone: skin over mouth line (x32-88, y124-146)
    d.rectangle((32, 124, 88, 146), fill=SKIN)
    return im
blank = blank_head(); save(blank, "gap-close-head-blank-20261031.png")
# normal eyes: original Head_Front eye crops pasted back onto blank
normal = blank.copy()
for box in [(20, 68, 50, 84), (69, 68, 99, 84)]:
    normal.paste(head.crop(box), box[:2], head.crop(box))
save(normal, "gap-close-head-blank-normal-eyes-20261031.png")
# comedic eyes: round white eyes with pupils (pupil set = comedic relief only, C-08)
comedic = blank.copy(); d = ImageDraw.Draw(comedic)
for cx in (35, 84):
    d.ellipse((cx-13, 66, cx+13, 84), fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=2)
    d.ellipse((cx-5, 71, cx+5, 81), fill=(0, 0, 0, 255))
save(comedic, "gap-close-head-blank-comedic-eyes-20261031.png")
# angry eyes: white angular eyes with slanted black brow/lid (original vector)
angry = blank.copy(); d = ImageDraw.Draw(angry)
for x0, slant in [(22, 1), (71, -1)]:
    d.polygon([(x0, 78), (x0+26, 78), (x0+26, 68), (x0, 74)], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
    d.polygon([(x0-2, 66), (x0+28, 66+slant*0), (x0+28, 60), (x0-2, 64)], fill=(0, 0, 0, 255))
    # slanted brow: thick line sloping down toward centre
    d.line([(x0-2, 64), (x0+28, 70 if slant == 1 else 58)], fill=(0, 0, 0, 255), width=4)
save(angry, "gap-close-head-blank-angry-20261031.png")
# furious: Face_Angry pasted onto blank, then normal v3-language white eyes over its eyes
furious = blank.copy()
fa = load1(os.path.join(BASE, "Face_Angry.png"))
fa_r = fa.resize((104, 87), Image.LANCZOS)
furious.paste(fa_r, (8, 52), fa_r)
for box in [(20, 68, 50, 84), (69, 68, 99, 84)]:
    furious.paste(head.crop(box), box[:2], head.crop(box))
save(furious, "gap-close-head-furious-faceangry-normaleyes-20261031.png")
head_files = ["gap-close-head-blank-20261031.png", "gap-close-head-blank-normal-eyes-20261031.png",
              "gap-close-head-blank-comedic-eyes-20261031.png", "gap-close-head-blank-angry-20261031.png",
              "gap-close-head-furious-faceangry-normaleyes-20261031.png"]

# --- separate feet: Leg lowers cropped from y230 (above ankle ~240-260, ankle intact)
foot_files = []
for side, src, name in [("L", "Leg_Front_Lower.png", "gap-close-foot-left-20261031.png"),
                        ("R", "Leg_Back_Lower.png", "gap-close-foot-right-20261031.png")]:
    im = load1(os.path.join(CUT, src)).crop((0, 230, 1000, 1000))
    save(trim(im), name); foot_files.append(name)

# --- gauntlet-only pieces: cuff crops from OutFixed lowers (cuff band y70-190)
gauntlet_files = []
for src, name in [("Arm_Front_Lower_OutFixed.png", "gap-close-gauntlet-arm1-20261031.png"),
                  ("Arm_Back_Lower_OutFixed.png", "gap-close-gauntlet-arm2-20261031.png")]:
    im = load1(os.path.join(OUTFIX, src)).crop((0, 70, 1000, 190))
    save(trim(im), name); gauntlet_files.append(name)

# --- catalogue sheet (LABELS ON SHEET ONLY)
def sheet(items, cols, cell_w, cell_h, title, fname):
    rows = math.ceil(len(items)/cols)
    W, H = cols*cell_w, rows*(cell_h+34)+54
    s = Image.new("RGBA", (W, H), (128, 128, 128, 255)); d = ImageDraw.Draw(s)
    d.text((12, 12), title, fill=(255, 255, 255, 255))
    for i, (path, label) in enumerate(items):
        r, c = divmod(i, cols); x, y = c*cell_w, 54+r*(cell_h+34)
        im = Image.open(path).convert("RGBA"); im.thumbnail((cell_w-16, cell_h-16), Image.LANCZOS)
        s.paste(im, (x+(cell_w-im.size[0])//2, y+(cell_h-im.size[1])//2), im)
        d.text((x+8, y+cell_h+4), label, fill=(255, 255, 0, 255))
    save(s, fname); return fname

cat_items = [(os.path.join(OUT, f), f.replace("gap-close-", "")) for f in neck_files + head_files + foot_files + gauntlet_files]
sheet(cat_items, 4, 280, 220, "GAP-CLOSE MISSING PIECES — catalogue sheet (labels on sheet only, never on pieces)", "gap-close-missing-pieces-catalogue-20261031.png")

# ---------------------------------------------------------------- 2. FRONT-FACING KNUCKLE FIST v4 (original vector)
# Standalone orientation: knuckles at TOP facing camera, thumb wrapped across FRONT,
# wrist/gauntlet cuff at BOTTOM. Merged silhouette: body + 4 knuckle bumps = one shape.
W, H = 320, 340
sil = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(sil)
sd.rounded_rectangle((70, 110, 250, 300), radius=42, fill=255)
for cx in (102, 140, 178, 216):
    sd.ellipse((cx-26, 62, cx+26, 128), fill=255)
sd.rectangle((118, 282, 202, 330), fill=255)  # wrist cuff block
sil_blur = sil.filter(ImageFilter.GaussianBlur(1))
outline = Image.new("RGBA", (W, H), (0, 0, 0, 0))
mask_d = sil.filter(ImageFilter.MaxFilter(9))
od = ImageDraw.Draw(outline)
od.bitmap((0, 0), mask_d, fill=(0, 0, 0, 255))
fist = Image.new("RGBA", (W, H), (0, 0, 0, 0))
fist.alpha_composite(outline)
body = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(body)
bd.bitmap((0, 0), sil, fill=(255, 255, 255, 255))
# cool-grey shading on left + lower edge (original shading, not baked rim)
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); shd = ImageDraw.Draw(sh)
shd.rounded_rectangle((70, 110, 118, 300), radius=20, fill=(190, 196, 205, 160))
shd.rectangle((70, 262, 250, 300), fill=(205, 210, 218, 120))
body.alpha_composite(sh)
fist.alpha_composite(body)
d = ImageDraw.Draw(fist)
# knuckle seams: short faint grey ticks only, below each knuckle bump
for cx in (102, 140, 178, 216):
    d.line([(cx-14, 128), (cx+14, 128)], fill=(150, 155, 165, 255), width=3)
    d.line([(cx, 118), (cx, 132)], fill=(150, 155, 165, 255), width=2)
# thumb wrapped ACROSS the front: wedge from right side to rounded tip at centre-front
d.polygon([(250, 168), (196, 196), (168, 216), (186, 238), (232, 222), (254, 196)], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
d.line([(196, 196), (186, 238)], fill=(0, 0, 0, 255), width=3)  # tip crease
d.line([(232, 222), (254, 196)], fill=(0, 0, 0, 255), width=2)
# finger-curl lines on lower fist (faint, no black bars)
for y in (246, 268):
    d.arc((96, y-18, 224, y+18), start=20, end=160, fill=(150, 155, 165, 255), width=3)
# wrist cuff seam
d.line([(118, 282), (202, 282)], fill=(0, 0, 0, 255), width=3)
d.line([(118, 306), (202, 306)], fill=(160, 165, 175, 255), width=2)
fist_path = save(fist, "gap-close-fist-v4-knuckle-front-20261031.png")
# fist geometry for seating: wrist point = centre of cuff bottom block
FIST_WRIST = (160, 306)
# knuckle centroid check
fa_ = np.array(fist)[:, :, 3] > 10
ys_, xs_ = np.where(fa_[:140, :])
print("fist knuckle-zone centroid", round(float(xs_.mean()), 1), round(float(ys_.mean()), 1),
      "wrist point", FIST_WRIST)

# ---------------------------------------------------------------- 2b. PUNCH POSE with v4 fist (canvas widened to 1300 so the R fist is not edge-clipped)
def build_punch():
    W2 = 1300
    DX = 100  # body centre 650 instead of 550
    c = Image.new("RGBA", (W2, 1500), (0, 0, 0, 0))
    def pat(im, cx, top): c.paste(im, (int(cx-im.size[0]/2), int(top)), im)
    def limb2(path, joint, angle, anchor):
        im = load(path); ax, ay = anchor[0]*SCALE, anchor[1]*SCALE
        layer = Image.new("RGBA", (W2, 1500), (0, 0, 0, 0))
        layer.paste(im, (int(joint[0]-ax), int(joint[1]-ay)), im)
        return layer.rotate(angle, center=joint, expand=False)
    def cap2(path, joint):
        im = load(path); c.paste(im, (int(joint[0]-im.size[0]/2), int(joint[1]-im.size[1]/2)), im)
    pat(load(os.path.join(BASE, "Cape_Back_Main.png")), 550+DX, 410)
    cfg_u = {"L": -20, "R": 20}; cfg_l = {"L": -20, "R": 20}
    # legs (punch cfg leg_upper -20/20, leg_lower -20/20)
    knees = {}
    for side in ("L", "R"):
        hip = (HIP[side][0]+DX, HIP[side][1]); ball, ha = LEG[side]
        vec = (ball[0]-ha[0], ball[1]-ha[1])
        c.alpha_composite(limb2(os.path.join(CUT, LEG_PIECES[side][0]), hip, cfg_u[side], ha))
        knee = (hip[0]+rot_vec(vec, cfg_u[side])[0]*SCALE, hip[1]+rot_vec(vec, cfg_u[side])[1]*SCALE)
        knees[side] = knee
        c.alpha_composite(limb2(os.path.join(CUT, LEG_PIECES[side][1]), knee, cfg_l[side], (ball[0], 0)))
        cap2(os.path.join(CUT, LEG_PIECES[side][2]), knee)
    pat(load(os.path.join(BASE, "Pelvis.png")), 550+DX, 680)
    pat(load(os.path.join(BASE, "Cape_Collar.png")), 550+DX, 370)
    pat(load(os.path.join(BASE, "Torso_Chest.png")), 550+DX, 400)
    pat(load(os.path.join(BASE, "Belt_Overlay.png")), 550+DX, 670)
    elbows, wrists = {}, {}
    for side in ("L", "R"):
        ball, sh_a = ARM[side]; vec = (ball[0]-sh_a[0], ball[1]-sh_a[1])
        sh = (SHOULDER[side][0]+DX, SHOULDER[side][1])
        c.alpha_composite(limb2(os.path.join(CUT, ARM_UP[side]), sh, {"L": -45, "R": 90}[side], sh_a))
        elbows[side] = (sh[0]+rot_vec(vec, {"L": -45, "R": 90}[side])[0]*SCALE,
                        sh[1]+rot_vec(vec, {"L": -45, "R": 90}[side])[1]*SCALE)
    # L arm: native lower
    c.alpha_composite(limb2(os.path.join(CUT, ARM_LOW["L"]), elbows["L"], -45, (ARM["L"][0][0], 0)))
    cap2(os.path.join(CUT, ARM_CAP["L"]), elbows["L"])
    # R arm: forearm part ONLY of Arm_Back_Lower (split at y178; native fist discarded — no double fist)
    low_r = load1(os.path.join(CUT, ARM_LOW["R"]))
    fa_ = np.array(low_r); fa_[178:, :, 3] = 0
    fore_r = Image.fromarray(fa_)
    im = fore_r.resize((int(fore_r.size[0]*SCALE), int(fore_r.size[1]*SCALE)), Image.LANCZOS)
    ax, ay = ARM["R"][0][0]*SCALE, 0
    layer = Image.new("RGBA", (W2, 1500), (0, 0, 0, 0))
    layer.paste(im, (int(elbows["R"][0]-ax), int(elbows["R"][1]-ay)), im)
    layer = layer.rotate(90, center=elbows["R"], expand=False)
    c.alpha_composite(layer)
    cap2(os.path.join(CUT, ARM_CAP["R"]), elbows["R"])
    # wrist point: elbow + rotated (wrist pivot - lower anchor) * SCALE; pivot (114,180) in Arm_Back_Lower
    wvec = (114-ARM["R"][0][0], 180)
    wrists["R"] = (elbows["R"][0]+rot_vec(wvec, 90)[0]*SCALE, elbows["R"][1]+rot_vec(wvec, 90)[1]*SCALE)
    # wrist cap BEHIND the v4 fist
    cap2(os.path.join(CUT, ARM_CAP["R"]), wrists["R"])
    # v4 fist: standalone knuckles-up; rotate so knuckles point along forearm axis (to the right).
    # PIL rotate(-90) = clockwise: up -> right. Verify empirically below.
    for ang in (-90, 90):
        t = fist.rotate(ang, expand=True)
        a = np.array(t)[:, :, 3] > 10; ys, xs = np.where(a)
        print("fist rotate", ang, "centroid", round(float(xs.mean()), 1), round(float(ys.mean()), 1), "size", t.size)
    fist_rot = fist.rotate(-90, expand=True)
    # wrist point in rotated fist: rotate FIST_WRIST about fist centre
    cx0, cy0 = fist.size[0]/2, fist.size[1]/2
    # PIL rotate(-90) clockwise: (x,y) rel centre -> (cy_rel, -cx_rel) in image coords? compute via transform of point
    # Use PIL's own mapping: rotate a test image with a dot — do it numerically with affine inverse instead:
    # For rotate(angle) PIL uses: new = R(-angle) * old for CCW-positive display. Empirically verify by centroid:
    # knuckle zone in rotated image should be to the RIGHT of the wrist zone.
    a = np.array(fist_rot)[:, :, 3] > 10
    # wrist block in original is bottom centre; after CW rotation it is left centre.
    # Locate the cuff seam (darkest horizontal band) — simpler: wrist point = left-centre of rotated bbox
    ys, xs = np.where(a)
    wrist_rot = (xs.min()+22, (ys.min()+ys.max())/2)
    print("fist_rot wrist estimate", wrist_rot, "bbox", xs.min(), xs.max(), ys.min(), ys.max())
    flayer = Image.new("RGBA", (W2, 1500), (0, 0, 0, 0))
    flayer.paste(fist_rot, (int(wrists["R"][0]-wrist_rot[0]), int(wrists["R"][1]-wrist_rot[1])), fist_rot)
    c.alpha_composite(flayer)
    # L wrist (native)
    wvec_l = (79-ARM["L"][0][0], 180)
    wrists["L"] = (elbows["L"][0]+rot_vec(wvec_l, -45)[0]*SCALE, elbows["L"][1]+rot_vec(wvec_l, -45)[1]*SCALE)
    pat(load(os.path.join(BASE, "Neck.png"), scale=1.05), 550+DX, 360)
    pat(load(os.path.join(BASE, "Head_Front.png")), 550+DX, 250)
    # fist centre in pose: centroid of fist_rot placed
    fa2 = np.array(flayer)[:, :, 3] > 10; ys2, xs2 = np.where(fa2)
    fist_centre = (float(xs2.mean()), float(ys2.mean()))
    joints = {"elbows": {k: [round(v[0], 1), round(v[1], 1)] for k, v in elbows.items()},
              "wrists": {k: [round(v[0], 1), round(v[1], 1)] for k, v in wrists.items()},
              "fist_R_centre": [round(fist_centre[0], 1), round(fist_centre[1], 1)],
              "knees": {k: [round(v[0], 1), round(v[1], 1)] for k, v in knees.items()}}
    save(c, "gap-close-punch-pose-v4-20261031.png")
    with open(os.path.join(OUT, "gap-close-punch-pose-v4-joints-20261031.json"), "w") as f:
        json.dump(joints, f, indent=2)
    print("punch joints", joints)
    return c, joints
punch_img, punch_joints = build_punch()

# ---------------------------------------------------------------- 3. TRUE-FINAL-FLEX v2 (relaxed)
# Full-final (OVER-FLEX, untouched elsewhere): arm_upper -70/+70, arm_lower 135/-135, fist -75/+75.
# True-final v2 here: arm_upper -85/+85 (+15 toward head), arm_lower 145/-145 (relaxed),
# fist -70/+70 (+5 opened, more space at forearm-wrist angle). Fists are the FlexOut
# clenched fists, seated at the forearm junction, caps BEHIND fists, wrist zones cleaned.
# NOTE on wording: a later 16:46 correction clarified "cleaned up", not extra roll/clench —
# so no extra fist roll is applied; the fists remain clenched and are cleaned, not re-rolled.
def build_flex():
    c = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0)); dip = 28
    def pat(im, cx, top): c.paste(im, (int(cx-im.size[0]/2), int(top)), im)
    def limb_p(path, joint, angle, anchor):
        im = load(path); ax, ay = anchor[0]*SCALE, anchor[1]*SCALE
        layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
        layer.paste(im, (int(joint[0]-ax), int(joint[1]-ay)), im)
        return layer.rotate(angle, center=joint, expand=False)
    def cap_p(path, joint):
        im = load(path); c.paste(im, (int(joint[0]-im.size[0]/2), int(joint[1]-im.size[1]/2)), im)
    pat(load(os.path.join(BASE, "Cape_Back_Main.png")), 550, 410)
    knees = {}
    for side in ("L", "R"):
        hip = HIP[side]; ball, ha = LEG[side]; vec = (ball[0]-ha[0], ball[1]-ha[1])
        c.alpha_composite(limb_p(os.path.join(CUT, LEG_PIECES[side][0]), hip, {"L": -22, "R": 22}[side], ha))
        knee = (hip[0]+rot_vec(vec, {"L": -22, "R": 22}[side])[0]*SCALE,
                hip[1]+rot_vec(vec, {"L": -22, "R": 22}[side])[1]*SCALE)
        knees[side] = knee
        c.alpha_composite(limb_p(os.path.join(CUT, LEG_PIECES[side][1]), knee, {"L": 10, "R": -10}[side], (ball[0], 0)))
        cap_p(os.path.join(CUT, LEG_PIECES[side][2]), knee)
    pat(load(os.path.join(BASE, "Pelvis.png")), 550, 680+dip)
    pat(load(os.path.join(BASE, "Cape_Collar.png")), 550, 370+dip)
    pat(load(os.path.join(BASE, "Torso_Chest.png")), 550, 400+dip)
    pat(load(os.path.join(BASE, "Belt_Overlay.png")), 550, 670+dip)
    cfg_u = {"L": -85, "R": 85}; cfg_l = {"L": 145, "R": -145}; cfg_f = {"L": -70, "R": 70}
    WRIST = {"L": (79, 180), "R": (102, 180)}
    elbows, wrists, fist_centres = {}, {}, {}
    for side in ("L", "R"):
        ball, sh_a = ARM[side]; vec = (ball[0]-sh_a[0], ball[1]-sh_a[1])
        sh = (SHOULDER[side][0], SHOULDER[side][1]+dip)
        c.alpha_composite(limb_p(os.path.join(CUT, ARM_UP[side]), sh, cfg_u[side], sh_a))
        elbows[side] = (sh[0]+rot_vec(vec, cfg_u[side])[0]*SCALE, sh[1]+rot_vec(vec, cfg_u[side])[1]*SCALE)
        wvec = (WRIST[side][0]-ball[0], WRIST[side][1]-0)
        wrists[side] = (elbows[side][0]+rot_vec(wvec, cfg_l[side])[0]*SCALE,
                        elbows[side][1]+rot_vec(wvec, cfg_l[side])[1]*SCALE)
    for side in ("L", "R"):
        ball, _ = ARM[side]
        src = load1(os.path.join(FLEX, "Arm_Front_Lower_FlexOut.png" if side == "L" else "Arm_Back_Lower_FlexOut.png"))
        fa_ = np.array(src); fi_ = np.array(src)
        fa_[175:, :, 3] = 0; fi_[:175, :, 3] = 0
        fore_p, fist_p = Image.fromarray(fa_), Image.fromarray(fi_)
        def rot_piece(piece, joint, angle, anchor):
            im = piece.resize((int(piece.size[0]*SCALE), int(piece.size[1]*SCALE)), Image.LANCZOS)
            ax, ay = anchor[0]*SCALE, anchor[1]*SCALE
            layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
            layer.paste(im, (int(joint[0]-ax), int(joint[1]-ay)), im)
            return layer.rotate(angle, center=joint, expand=False)
        fore = rot_piece(fore_p, elbows[side], cfg_l[side], (ball[0], 0))
        c.alpha_composite(fore)
        cap_p(os.path.join(CUT, ARM_CAP[side]), elbows[side])
        fist_l = rot_piece(fist_p, elbows[side], cfg_l[side], (ball[0], 0))
        fist_rot = fist_l.rotate(cfg_f[side], center=wrists[side], expand=False)
        # wrist cap BEHIND fist, masked to forearm+fist union (dilated) so no ring crosses the fist face
        cap_layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
        cap_im = load(os.path.join(CUT, ARM_CAP[side]))
        cap_layer.paste(cap_im, (int(wrists[side][0]-cap_im.size[0]/2), int(wrists[side][1]-cap_im.size[1]/2)), cap_im)
        union = (np.array(fore)[:, :, 3] > 0) | (np.array(fist_rot)[:, :, 3] > 0)
        union_im = Image.fromarray((union.astype(np.uint8))*255).filter(ImageFilter.MaxFilter(7))
        ca = np.array(cap_layer); ma = np.array(union_im)
        ca[:, :, 3] = np.where(ma > 0, ca[:, :, 3], 0)
        c.alpha_composite(Image.fromarray(ca))
        c.alpha_composite(fist_rot)
        a = np.array(fist_rot)[:, :, 3] > 10; ys, xs = np.where(a)
        fist_centres[side] = (float(xs.mean()), float(ys.mean()))
    pat(load(os.path.join(BASE, "Neck.png"), scale=1.05), 550, 360+dip)
    pat(load(os.path.join(BASE, "Head_Front.png")), 550, 250+dip)
    # wrist-zone cleanup: drop faint fringe alpha <40 in a 70px box around each wrist
    for w in wrists.values():
        x0, y0 = max(0, int(w[0]-70)), max(0, int(w[1]-70))
        x1, y1 = min(1100, int(w[0]+70)), min(1500, int(w[1]+70))
        crop = c.crop((x0, y0, x1, y1)).convert("RGBA"); arr = np.array(crop)
        weak = arr[:, :, 3] < 40; arr[weak, 3] = 0
        c.paste(Image.fromarray(arr), (x0, y0), Image.fromarray(arr))
    save(c, "gap-close-true-final-flex-v2-20261031.png")
    joints = {"elbows": {k: [round(v[0], 1), round(v[1], 1)] for k, v in elbows.items()},
              "wrists": {k: [round(v[0], 1), round(v[1], 1)] for k, v in wrists.items()},
              "fists": {k: [round(v[0], 1), round(v[1], 1)] for k, v in fist_centres.items()},
              "knees": {k: [round(v[0], 1), round(v[1], 1)] for k, v in knees.items()},
              "cfg": {"arm_upper": cfg_u, "arm_lower": cfg_l, "fist": cfg_f}}
    with open(os.path.join(OUT, "gap-close-true-final-flex-v2-joints-20261031.json"), "w") as f:
        json.dump(joints, f, indent=2)
    print("flex joints", joints)
    return c, joints
flex_img, flex_joints = build_flex()

# ---------------------------------------------------------------- 4. 3/4 + SIDE + BACK stand-ins
# 3/4 head v3 kitbash: construction-guided asymmetric warp of the front head.
# Far side = image-left, compressed 0.70; near side = image-right, 0.97;
# far eye squeezed a further 0.80; bridge-occlusion strip at the nose bridge.
# This is a DERIVED KITBASH, NOT a true hand-drawn 3/4 — said plainly on the sheet.
def warp_34(im):
    W0, H0 = im.size  # 119x172, centre x=59
    left = im.crop((0, 0, 59, H0)).resize((41, H0), Image.LANCZOS)   # far, 0.70
    right = im.crop((59, 0, W0, H0)).resize((58, H0), Image.LANCZOS)  # near, 0.97
    out = Image.new("RGBA", (100, H0), (0, 0, 0, 0))
    out.paste(left, (0, 0), left); out.paste(right, (41, 0), right)
    # far eye squeeze: far eye now approx x8-22, y68-84 -> squeeze to 0.80 width about its centre
    eye = out.crop((6, 66, 26, 86))
    eye_s = eye.resize((16, 20), Image.LANCZOS)
    # clear original far-eye zone with cowl purple, then paste squeezed eye
    d = ImageDraw.Draw(out); d.rectangle((6, 66, 26, 86), fill=COWL)
    out.paste(eye_s, (8, 66), eye_s)
    # bridge-occlusion strip: darken a 4px strip at the nose bridge (x38-41, y65-95)
    arr = np.array(out).astype(np.int16)
    strip = (np.arange(100)[None, :] >= 38) & (np.arange(100)[None, :] <= 41)
    rows = (np.arange(H0)[:, None] >= 65) & (np.arange(H0)[:, None] <= 95)
    zone = strip & rows
    for ch in range(3):
        arr[:, :, ch] = np.where(zone & (arr[:, :, 3] > 10), (arr[:, :, ch]*0.65).astype(np.int16), arr[:, :, ch])
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
head34 = warp_34(head)
save(head34, "gap-close-head-34-v3-kitbash-20261031.png")
# 3/4 sheet: kitbash + construction reference (lines on REFERENCE panel only)
s34 = Image.new("RGBA", (900, 420), (128, 128, 128, 255)); d = ImageDraw.Draw(s34)
d.text((12, 10), "3/4 HEAD v3 — DERIVED KITBASH, NOT a true hand-drawn 3/4 (labels on sheet only)", fill=(255, 255, 0, 255))
big = head34.resize((200, 344), Image.LANCZOS); s34.paste(big, (40, 50), big)
ref = head34.resize((200, 344), Image.LANCZOS); s34.paste(ref, (300, 50), ref)
d2 = ImageDraw.Draw(s34)
d2.line([(300+82, 50), (300+82, 394)], fill=(255, 0, 0, 255), width=2)  # centre line (reference panel only)
d2.line([(300, 50+150), (500, 50+150)], fill=(255, 0, 0, 255), width=2)  # eye line
d2.text((560, 80), "Far side (image-left) 0.70x", fill=(255, 255, 255, 255))
d2.text((560, 110), "Near side 0.97x; far eye x0.80", fill=(255, 255, 255, 255))
d2.text((560, 140), "Bridge-occlusion strip x38-41", fill=(255, 255, 255, 255))
d2.text((560, 170), "Clean piece (left) has NO lines.", fill=(255, 255, 255, 255))
d2.text((560, 200), "BLOCKER for a true 3/4: needs a", fill=(255, 255, 255, 255))
d2.text((560, 230), "hand-drawn master; warps cannot", fill=(255, 255, 255, 255))
d2.text((560, 260), "redraw linework. This kitbash", fill=(255, 255, 255, 255))
d2.text((560, 290), "is the working replacement.", fill=(255, 255, 255, 255))
save(s34, "gap-close-head-34-v3-sheet-20261031.png")

# Side-body STAND-IN sheet: profile head + front torso/arms/legs arranged in profile order.
side = Image.new("RGBA", (1400, 900), (128, 128, 128, 255)); d = ImageDraw.Draw(side)
d.text((12, 10), "SIDE BODY — STAND-IN ONLY (labels on sheet only). True hand-drawn side torso/legs are NOT built; see note.", fill=(255, 255, 0, 255))
prof = load1(os.path.join(BASE, "Head_Profile.png"))
side.paste(prof, (180, 60), prof)
torso = load1(os.path.join(BASE, "Torso_Chest.png")); torso_s = torso.resize((220, 223), Image.LANCZOS)
side.paste(torso_s, (150, 300), torso_s)
arm_l = load1(os.path.join(CUT, "Arm_Front_Lower.png")); arm_s = arm_l.resize((107, 202), Image.LANCZOS)
side.paste(arm_s, (330, 330), arm_s)
leg_l = load1(os.path.join(CUT, "Leg_Front_Lower.png")); leg_s = leg_l.resize((109, 226), Image.LANCZOS)
side.paste(leg_s, (190, 520), leg_s)
d.text((620, 120), "What this is: profile head (real piece) +", fill=(255, 255, 255, 255))
d.text((620, 150), "front torso/limbs placed in profile order.", fill=(255, 255, 255, 255))
d.text((620, 180), "It stages a side view; it is NOT a side", fill=(255, 255, 255, 255))
d.text((620, 210), "drawing — torso musculature still faces front.", fill=(255, 255, 255, 255))
d.text((620, 260), "Missing for a true side body:", fill=(255, 255, 255, 255))
d.text((620, 290), "- side torso, side pelvis, side legs", fill=(255, 255, 255, 255))
d.text((620, 320), "- side feet, side cape drape", fill=(255, 255, 255, 255))
d.text((620, 350), "BLOCKER: hand-drawn side master.", fill=(255, 255, 255, 255))
save(side, "gap-close-side-body-standin-sheet-20261031.png")

# Back-body STAND-IN sheet: cape back + mirrored torso + blank cowl-back placeholder (NO face on the back).
back = Image.new("RGBA", (1400, 900), (128, 128, 128, 255)); d = ImageDraw.Draw(back)
d.text((12, 10), "BACK BODY — STAND-IN ONLY (labels on sheet only). No back-of-head piece exists; placeholder used, plainly marked.", fill=(255, 255, 0, 255))
cape = load1(os.path.join(BASE, "Cape_Back_Main.png")); cape_s = cape.resize((343, 583), Image.LANCZOS)
back.paste(cape_s, (120, 180), cape_s)
# blank cowl-back placeholder: purple rounded shape, no face, no eyes
ph = Image.new("RGBA", (120, 170), (0, 0, 0, 0)); pd = ImageDraw.Draw(ph)
pd.rounded_rectangle((4, 4, 116, 166), radius=50, fill=(92, 40, 115, 255), outline=(0, 0, 0, 255), width=4)
back.paste(ph, (240, 60), ph)
d.text((620, 120), "Cape back = real piece (Cape_Back_Main).", fill=(255, 255, 255, 255))
d.text((620, 150), "Head = PLACEHOLDER cowl-back shape only.", fill=(255, 255, 255, 255))
d.text((620, 180), "It is NOT a back head and carries NO face.", fill=(255, 255, 255, 255))
d.text((620, 210), "Torso here is the cape itself; a true back", fill=(255, 255, 255, 255))
d.text((620, 240), "torso (shoulder blades, back suit seams)", fill=(255, 255, 255, 255))
d.text((620, 270), "does not exist in the sliced set.", fill=(255, 255, 255, 255))
d.text((620, 320), "BLOCKER: hand-drawn back master.", fill=(255, 255, 255, 255))
save(back, "gap-close-back-body-standin-sheet-20261031.png")

# ---------------------------------------------------------------- 5. CAPE BONE-CHAIN
cape_full = load1(os.path.join(BASE, "Cape_Back_Main.png"))
diag = Image.new("RGBA", (1100, 1000), (128, 128, 128, 255))
cape_d = cape_full.resize((490, 833), Image.LANCZOS); diag.paste(cape_d, (60, 90), cape_d)
d = ImageDraw.Draw(diag)
d.text((12, 10), "CAPE BONE-CHAIN — diagram (labels on sheet only). Lag 1-2 frames behind the body.", fill=(255, 255, 0, 255))
# joints along the cape in diagram coords (cape placed at x60-550, y90-923)
joints_c = [("B0 neck", (305, 130)), ("B1 mid-back", (305, 380)), ("B2 mid-cape", (305, 620)),
            ("B3 hem-L", (110, 880)), ("B4 hem-R", (500, 880)), ("B5 hem-C", (305, 910))]
prev = None
for name, (x, y) in joints_c:
    if prev: d.line([prev, (x, y)], fill=(255, 0, 0, 255), width=4)
    d.ellipse((x-18, y-18, x+18, y+18), fill=(255, 0, 0, 255), outline=(255, 255, 255, 255), width=3)
    prev = (x, y)
for i, (name, (x, y)) in enumerate(joints_c):
    d.text((x+24, y-8), name, fill=(255, 255, 255, 255))
d.text((620, 150), "Chain: neck -> mid-back -> mid-cape", fill=(255, 255, 255, 255))
d.text((620, 180), "-> hem L / C / R (fan).", fill=(255, 255, 255, 255))
d.text((620, 230), "Follow-through: each bone lags the", fill=(255, 255, 255, 255))
d.text((620, 260), "one above it by 1-2 frames; hem", fill=(255, 255, 255, 255))
d.text((620, 290), "moves last and farthest.", fill=(255, 255, 255, 255))
d.text((620, 340), "Cape is a SEPARATE prop-rig layer:", fill=(255, 255, 255, 255))
d.text((620, 370), "body file + cape file + composite", fill=(255, 255, 255, 255))
d.text((620, 400), "are delivered separately. Cape is", fill=(255, 255, 255, 255))
d.text((620, 430), "NOT baked into the body.", fill=(255, 255, 255, 255))
save(diag, "gap-close-cape-bone-chain-diagram-20261031.png")
# cape state as separate prop-rig layer: billowing cape = Cape_Back_Main with a sine wave warp
def wave_warp(im, amp=18, waves=1.5):
    arr = np.array(im); H0, W0 = arr.shape[:2]; out = np.zeros_like(arr)
    for y in range(H0):
        shift = int(amp * math.sin(2*math.pi*waves*y/H0) * (y/H0))
        out[y] = np.roll(arr[y], shift, axis=0)
        # rolled-in pixels from the opposite edge are wrong on transparent edges: clear wrapped columns
        if shift > 0: out[y, :shift, 3] = 0
        elif shift < 0: out[y, shift:, 3] = 0
    return Image.fromarray(out)
cape_state = wave_warp(cape_full)
save(cape_state, "gap-close-cape-state-billowing-layer-20261031.png")
# body-only (v7c apose, labels=False, cape omitted) + composite
def build_body_only():
    c = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    def pat(im, cx, top): c.paste(im, (int(cx-im.size[0]/2), int(top)), im)
    def limb_p(path, joint, angle, anchor):
        im = load(path); ax, ay = anchor[0]*SCALE, anchor[1]*SCALE
        layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
        layer.paste(im, (int(joint[0]-ax), int(joint[1]-ay)), im)
        return layer.rotate(angle, center=joint, expand=False)
    def cap_p(path, joint):
        im = load(path); c.paste(im, (int(joint[0]-im.size[0]/2), int(joint[1]-im.size[1]/2)), im)
    for side in ("L", "R"):
        hip = HIP[side]; ball, ha = LEG[side]; vec = (ball[0]-ha[0], ball[1]-ha[1])
        c.alpha_composite(limb_p(os.path.join(CUT, LEG_PIECES[side][0]), hip, {"L": -10, "R": 10}[side], ha))
        knee = (hip[0]+rot_vec(vec, {"L": -10, "R": 10}[side])[0]*SCALE, hip[1]+rot_vec(vec, {"L": -10, "R": 10}[side])[1]*SCALE)
        c.alpha_composite(limb_p(os.path.join(CUT, LEG_PIECES[side][1]), knee, {"L": -10, "R": 10}[side], (ball[0], 0)))
        cap_p(os.path.join(CUT, LEG_PIECES[side][2]), knee)
    pat(load(os.path.join(BASE, "Pelvis.png")), 550, 680)
    pat(load(os.path.join(BASE, "Cape_Collar.png")), 550, 370)
    pat(load(os.path.join(BASE, "Torso_Chest.png")), 550, 400)
    pat(load(os.path.join(BASE, "Belt_Overlay.png")), 550, 670)
    elbows = {}
    for side in ("L", "R"):
        ball, sh_a = ARM[side]; vec = (ball[0]-sh_a[0], ball[1]-sh_a[1])
        sh = SHOULDER[side]
        c.alpha_composite(limb_p(os.path.join(CUT, ARM_UP[side]), sh, {"L": -20, "R": 20}[side], sh_a))
        elbows[side] = (sh[0]+rot_vec(vec, {"L": -20, "R": 20}[side])[0]*SCALE, sh[1]+rot_vec(vec, {"L": -20, "R": 20}[side])[1]*SCALE)
        c.alpha_composite(limb_p(os.path.join(CUT, ARM_LOW[side]), elbows[side], {"L": -20, "R": 20}[side], (ball[0], 0)))
        cap_p(os.path.join(CUT, ARM_CAP[side]), elbows[side])
    pat(load(os.path.join(BASE, "Neck.png"), scale=1.05), 550, 360)
    pat(load(os.path.join(BASE, "Head_Front.png")), 550, 250)
    return c
body_only = build_body_only()
save(body_only, "gap-close-cape-pose-body-only-20261031.png")
comp = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
cape_layer = load(os.path.join(BASE, "Cape_Back_Main.png"), scale=1.0)  # not used; state layer placed below body
comp.alpha_composite(Image.new("RGBA", (1100, 1500), (0, 0, 0, 0)))
# place cape state (original size 490x833) centred at 550, top 410, BEHIND body
cape_placed = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
cape_placed.paste(cape_state, (int(550-cape_state.size[0]/2), 410), cape_state)
comp.alpha_composite(cape_placed)
comp.alpha_composite(body_only)
save(comp, "gap-close-cape-pose-composite-20261031.png")

# ---------------------------------------------------------------- 6. FORESHORTENED FORWARD-FLIGHT FOREARM
# Same method as forearm v2: forearm segment compressed 0.42x, fist enlarged 1.45x wide / 1.30x tall,
# fist over forearm with 18px overlap, wrist cap behind fist. Arm1 + Arm2 both built.
def foreshorten(src_path, out_name):
    src = load1(src_path)  # Arm lower, fist zone y178+
    fore = src.crop((0, 0, src.size[0], 178))
    fist_z = src.crop((0, 178, src.size[0], src.size[1]))
    fore_c = fore.resize((fore.size[0], int(178*0.42)), Image.LANCZOS)
    fist_c = fist_z.resize((int(fist_z.size[0]*1.45), int(fist_z.size[1]*1.30)), Image.LANCZOS)
    Hc = fore_c.size[1] + fist_c.size[1] - 18
    Wc = max(fore_c.size[0], fist_c.size[0]) + 20
    out = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
    out.paste(fore_c, ((Wc-fore_c.size[0])//2, 0), fore_c)
    # wrist cap behind fist: white ball with black outline at the seam
    d = ImageDraw.Draw(out); cy = fore_c.size[1]-9
    d.ellipse(((Wc//2)-26, cy-26, (Wc//2)+26, cy+26), fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=3)
    out.paste(fist_c, ((Wc-fist_c.size[0])//2, fore_c.size[1]-18), fist_c)
    save(trim(out), out_name)
    return out_name
fs1 = foreshorten(os.path.join(CUT, "Arm_Front_Lower.png"), "gap-close-foreshortened-forearm-arm1-20261031.png")
fs2 = foreshorten(os.path.join(CUT, "Arm_Back_Lower.png"), "gap-close-foreshortened-forearm-arm2-20261031.png")

# ---------------------------------------------------------------- verification
print("=== VERIFY (RGBA, non-empty) ===")
for f in sorted(os.listdir(OUT)):
    if f.endswith(".png"):
        p = os.path.join(OUT, f)
        try:
            n = verify(p); print(f, "OK opaque=", n)
        except Exception as e:
            print(f, "FAIL", e)
