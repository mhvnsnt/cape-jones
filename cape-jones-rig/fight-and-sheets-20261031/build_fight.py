"""Fighting animation builder — v7c rig, labels=False, transparent plates.
Keyframes interpolated; punch snap = 2-frame jump. Afterglow = past-position
soft-rim bands only, skipped when past frame == current frame (no static rim),
so rest frames decay to true zero after the 6-frame lag.
Fist note: uses v7c cut-limb lowers (gauntlet), NOT v5 flipped fist — v5 fist
integration into the v7c builder is still owed, stated in the report.
"""
import os, math, json
from PIL import Image, ImageFilter

BASE = "/home/hatch/workspace/cape-jones-rig/sliced"
CUT = "/home/hatch/workspace/cape-jones-rig/cut-limbs-v7c"
OUT = "/home/hatch/workspace/cape-jones-rig/fight-and-sheets-20261031"
os.makedirs(OUT + "/frames", exist_ok=True)
SCALE = 0.95
SHOULDER = {"L": (430, 445), "R": (670, 445)}
HIP = {"L": (470, 740), "R": (615, 740)}
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
LEG = {"L": ((95, 314), (77, 40)), "R": ((100, 314), (84, 40))}
LEG_PIECES = {"L": ("Leg_Front_Upper.png", "Leg_Front_Lower.png", "Leg_Front_Cap.png"),
              "R": ("Leg_Back_Upper.png", "Leg_Back_Lower.png", "Leg_Back_Cap.png")}
ARM_PIECES = {"L": ("Arm_Front_Upper.png", "Arm_Front_Lower.png", "Arm_Front_Cap.png"),
              "R": ("Arm_Back_Upper.png", "Arm_Back_Lower.png", "Arm_Back_Cap.png")}

def load(p, scale=SCALE):
    im = Image.open(p).convert("RGBA")
    return im.resize((int(im.size[0] * scale), int(im.size[1] * scale)), Image.LANCZOS)

def paste_at(c, im, cx, top):
    c.paste(im, (int(cx - im.size[0] / 2), int(top)), im)

def limb(c, path, joint, angle, anchor):
    im = load(path); ax, ay = anchor[0] * SCALE, anchor[1] * SCALE
    layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    layer.paste(im, (int(joint[0] - ax), int(joint[1] - ay)), im)
    layer = layer.rotate(angle, center=joint, expand=False)
    c.alpha_composite(layer)

def cap_at(c, path, joint):
    im = load(path)
    c.paste(im, (int(joint[0] - im.size[0] / 2), int(joint[1] - im.size[1] / 2)), im)

def rot_vec(v, angle_deg):
    a = math.radians(angle_deg); x, y = v
    return (x * math.cos(a) + y * math.sin(a), -x * math.sin(a) + y * math.cos(a))

def build(cfg):
    canvas = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    paste_at(canvas, load(os.path.join(BASE, "Cape_Back_Main.png")), 550, 410)
    for side in ("L", "R"):
        hip = HIP[side]; ball, hip_anchor = LEG[side]
        vec = (ball[0] - hip_anchor[0], ball[1] - hip_anchor[1])
        up, low, cap = LEG_PIECES[side]
        limb(canvas, os.path.join(CUT, up), hip, cfg["leg_upper"][side], hip_anchor)
        knee = (hip[0] + rot_vec(vec, cfg["leg_upper"][side])[0] * SCALE,
                hip[1] + rot_vec(vec, cfg["leg_upper"][side])[1] * SCALE)
        limb(canvas, os.path.join(CUT, low), knee, cfg["leg_lower"][side], (ball[0], 0))
        cap_at(canvas, os.path.join(CUT, cap), knee)
    elbows = {}
    for side in ("L", "R"):
        ball, sh_anchor = ARM[side]; vec = (ball[0] - sh_anchor[0], ball[1] - sh_anchor[1])
        up, _, _ = ARM_PIECES[side]; sh = SHOULDER[side]
        limb(canvas, os.path.join(CUT, up), sh, cfg["arm_upper"][side], sh_anchor)
        elbows[side] = (sh[0] + rot_vec(vec, cfg["arm_upper"][side])[0] * SCALE,
                        sh[1] + rot_vec(vec, cfg["arm_upper"][side])[1] * SCALE)
    paste_at(canvas, load(os.path.join(BASE, "Pelvis.png")), 550, 680)
    paste_at(canvas, load(os.path.join(BASE, "Cape_Collar.png")), 550, 370)
    paste_at(canvas, load(os.path.join(BASE, "Torso_Chest.png")), 550, 400)
    paste_at(canvas, load(os.path.join(BASE, "Belt_Overlay.png")), 550, 670)
    for side in ("L", "R"):
        _, low, cap = ARM_PIECES[side]; ball, _ = ARM[side]
        limb(canvas, os.path.join(CUT, low), elbows[side], cfg["arm_lower"][side], (ball[0], 0))
        cap_at(canvas, os.path.join(CUT, cap), elbows[side])
    paste_at(canvas, load(os.path.join(BASE, "Neck.png"), scale=1.05), 550, 360)
    paste_at(canvas, load(os.path.join(BASE, "Head_Front.png")), 550, 250)
    return canvas

GUARD = {"arm_upper": {"L": -40, "R": 40}, "arm_lower": {"L": 120, "R": -120},
         "leg_upper": {"L": -15, "R": 15}, "leg_lower": {"L": 20, "R": -20}}
WINDUP2 = {"arm_upper": {"L": -40, "R": 20}, "arm_lower": {"L": 120, "R": 160},
           "leg_upper": {"L": -15, "R": 15}, "leg_lower": {"L": 20, "R": -20}}
IMPACT2 = {"arm_upper": {"L": -40, "R": -110}, "arm_lower": {"L": 120, "R": -110},
           "leg_upper": {"L": -20, "R": 20}, "leg_lower": {"L": 25, "R": -25}}
DOWN2 = {"arm_upper": {"L": -40, "R": -70}, "arm_lower": {"L": 120, "R": -70},
         "leg_upper": {"L": -20, "R": 20}, "leg_lower": {"L": 25, "R": -25}}
WINDUP1 = {"arm_upper": {"L": -20, "R": 40}, "arm_lower": {"L": -120, "R": -120},
           "leg_upper": {"L": -15, "R": 15}, "leg_lower": {"L": 20, "R": -20}}
JAB1 = {"arm_upper": {"L": -90, "R": 40}, "arm_lower": {"L": -90, "R": -120},
        "leg_upper": {"L": -20, "R": 20}, "leg_lower": {"L": 25, "R": -25}}
KICK = {"arm_upper": {"L": -40, "R": 40}, "arm_lower": {"L": 120, "R": -120},
        "leg_upper": {"L": -55, "R": 15}, "leg_lower": {"L": 15, "R": -20}}
BLOCK = {"arm_upper": {"L": -70, "R": 70}, "arm_lower": {"L": 140, "R": -140},
         "leg_upper": {"L": -35, "R": 35}, "leg_lower": {"L": 45, "R": -45}}

# (pose, frames, label) — interpolation between successive poses
SEQ = [(GUARD, 6, "guard"), (WINDUP2, 4, "punch2-windup"), (IMPACT2, 2, "punch2-snap"),
       (IMPACT2, 6, "punch2-impact-hold"), (DOWN2, 2, "punch2-across-down"),
       (GUARD, 4, "recover"), (WINDUP1, 3, "punch1-windup"), (JAB1, 2, "punch1-snap"),
       (JAB1, 4, "punch1-hold"), (GUARD, 4, "recover"), (KICK, 3, "kick-windup"),
       (KICK, 4, "kick-hold"), (GUARD, 4, "recover"), (BLOCK, 6, "block-dodge"),
       (GUARD, 10, "rest")]

def lerp(a, b, t):
    return {k: {s: a[k][s] + (b[k][s] - a[k][s]) * t for s in ("L", "R")} for k in a}

frames = []  # (label, plate)
for i, (pose, n, label) in enumerate(SEQ):
    prev = SEQ[i - 1][0] if i > 0 else pose
    for f in range(n):
        t = (f + 1) / n if i > 0 else 1.0
        # snap segments: jump straight to pose (no interpolation)
        cfg = pose if "snap" in label else lerp(prev, pose, t)
        frames.append((label, build(cfg)))
print("rig frames:", len(frames))
for i, (label, plate) in enumerate(frames):
    plate.save(f"{OUT}/frames/frame-{i:03d}.png")
    if i % 10 == 0 or label in ("kick-hold", "block-dodge", "punch2-impact-hold"):
        print(i, label, plate.size)

# afterglow: past-position soft rims, cyan (0,200,255), dilate 6 blur 5
import numpy as np
from PIL import ImageFilter as IF
FADE = [0.50, 0.40, 0.30, 0.20, 0.12, 0.06]
BG = (18, 18, 28)
def rim_of(plate):
    a = plate.split()[3]
    dil = a.filter(IF.MaxFilter(13))
    rim = Image.new("RGBA", plate.size, (0, 0, 0, 0))
    # rim = dilated minus original
    import PIL.ImageChops as Ch
    d = Ch.subtract(dil, a)
    rim_arr = np.zeros((plate.size[1], plate.size[0], 4), dtype=np.uint8)
    da = np.array(d)
    rim_arr[..., 0] = 0; rim_arr[..., 1] = 200; rim_arr[..., 2] = 255; rim_arr[..., 3] = da
    r = Image.fromarray(rim_arr, "RGBA").filter(IF.GaussianBlur(5))
    return r

plates = [p for _, p in frames]
labels = [l for l, _ in frames]
out_frames = []
for i, plate in enumerate(plates):
    comp = Image.new("RGBA", (1100, 1500), BG + (255,))
    for lag, fade in enumerate(FADE, 1):
        j = i - lag
        if j < 0: break
        # skip trail from a frame identical to current (no static rim)
        diff = np.mean(np.abs(np.array(plates[j].split()[3], dtype=int) - np.array(plate.split()[3], dtype=int)))
        if diff < 0.5: continue
        r = rim_of(plates[j])
        ra = np.array(r); ra[..., 3] = (ra[..., 3].astype(float) * fade).astype(np.uint8)
        comp.alpha_composite(Image.fromarray(ra, "RGBA"))
    comp.alpha_composite(plate)
    out_frames.append(comp.convert("RGB"))
    out_frames[-1].save(f"{OUT}/frames/afterglow-{i:03d}.jpg", quality=90)
print("afterglow frames:", len(out_frames))
# mirrored-angle shot: flip the impact+guard frames, labelled mirrored
mir = []
for idx in [16, 17, 18, 19, 20, 21]:  # impact hold region approx
    mir.append(out_frames[idx].transpose(Image.FLIP_LEFT_RIGHT))
# 3/4-front true angle plate
plate34 = Image.open("/home/hatch/workspace/cape-jones-rig/sliced-clean-20261031/B-model/model-sheet-3quarter-front-set2/model-sheet-3quarter-front-set2_r1c1.png") if os.path.exists("/home/hatch/workspace/cape-jones-rig/sliced-clean-20261031/B-model/model-sheet-3quarter-front-set2/model-sheet-3quarter-front-set2_r1c1.png") else None
if plate34 is None:
    import glob
    fs = glob.glob("/home/hatch/workspace/cape-jones-rig/sliced-clean-20261031/B-model/model-sheet-3quarter-front-set2/*.png")
    print("3/4 files:", fs)
    plate34 = Image.open(fs[0]).convert("RGBA") if fs else None
if plate34 is not None:
    c = Image.new("RGBA", (1100, 1500), BG + (255,))
    w, h = plate34.size; s = min(900 / w, 1300 / h)
    p2 = plate34.resize((int(w * s), int(h * s)), Image.LANCZOS)
    c.alpha_composite(p2, ((1100 - p2.size[0]) // 2, (1500 - p2.size[1]) // 2))
    plate34_img = c.convert("RGB")
    print("3/4 plate:", plate34.size, "->", p2.size)
else:
    plate34_img = None

seq = out_frames + mir + ([plate34_img] * 12 if plate34_img is not None else [])
small = [f.resize((550, 750), Image.LANCZOS) for f in seq]
small[0].save(f"{OUT}/fight-afterglow-20261031.gif", save_all=True, append_images=small[1:], duration=42, loop=0)
# contact sheet of key frames
keys = [(0, "guard"), (10, "punch2-windup"), (12, "punch2-impact"), (22, "across-down"),
        (30, "punch1-jab"), (40, "kick"), (48, "block"), (len(out_frames) - 1, "rest-zero")]
sheet = Image.new("RGB", (1100, 1500), (128, 128, 128))
from PIL import ImageDraw
d = ImageDraw.Draw(sheet)
for k, (idx, lab) in enumerate(keys):
    im = out_frames[idx].resize((275, 375), Image.LANCZOS)
    x = (k % 4) * 275; y = (k // 4) * 375
    sheet.paste(im, (x, y)); d.text((x + 8, y + 8), lab, fill=(255, 255, 0))
sheet.save(f"{OUT}/fight-contact-20261031.png")
json.dump({"frames_rig": len(frames), "frames_afterglow": len(out_frames), "mirrored": len(mir),
           "angle34": plate34_img is not None, "total_seq": len(seq), "labels": labels},
          open(f"{OUT}/fight-manifest-20261031.json", "w"), indent=2)
print("total seq:", len(seq))
