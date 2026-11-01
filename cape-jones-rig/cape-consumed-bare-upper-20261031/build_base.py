"""Capeless all-black symbiote + white self-overlap outline.
Mars 2026-10-31 20:52 CDT. FUTURE ONLY, NOT V2, NOT canon. No repo push.
Method: rebuild the v7c layer stack on a transparent canvas, omitting the
actual cape pieces (Cape_Back_Main + Cape_Collar) for the capeless version,
instead of the old rectangle erase (y>=600 outside x380-720).
White-outline rule: in the all-black form, a front body part crossing in
front of another body part gets a WHITE outline on the crossing edge.
"""
import os, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(ROOT, "cape-consumed-bare-upper-20261031")
os.makedirs(os.path.join(OUT, "frames"), exist_ok=True)
BASE = os.path.join(ROOT, "sliced"); CUT = os.path.join(ROOT, "cut-limbs-v7c")
SCALE = 0.95
SHOULDER = {"L": (430, 445), "R": (670, 445)}; HIP = {"L": (470, 740), "R": (615, 740)}
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
LEG = {"L": ((95, 314), (77, 40)), "R": ((100, 314), (84, 40))}
LEG_PIECES = {"L": ("Leg_Front_Upper.png", "Leg_Front_Lower.png", "Leg_Front_Cap.png"),
              "R": ("Leg_Back_Upper.png", "Leg_Back_Lower.png", "Leg_Back_Cap.png")}
ARM_PIECES = {"L": ("Arm_Front_Upper.png", "Arm_Front_Lower.png", "Arm_Front_Cap.png"),
              "R": ("Arm_Back_Upper.png", "Arm_Back_Lower.png", "Arm_Back_Cap.png")}
APOSE = {"arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": -20, "R": 20},
         "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": -10, "R": 10}}
CROSS = {"arm_upper": {"L": 40, "R": -40}, "arm_lower": {"L": 120, "R": -120},
         "leg_upper": {"L": -10, "R": 10}, "leg_lower": {"L": -10, "R": 10}}

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
    return layer  # rotated forearm/upper layer alone (for front-mask work)

def cap_at(c, path, joint):
    im = load(path); c.paste(im, (int(joint[0] - im.size[0] / 2), int(joint[1] - im.size[1] / 2)), im)

def rot_vec(v, angle_deg):
    a = math.radians(angle_deg); x, y = v
    return (x * math.cos(a) + y * math.sin(a), -x * math.sin(a) + y * math.cos(a))

def build(cfg, cape_mode="both", split_front=False):
    """Returns (canvas, behind, front) where behind excludes forearm lowers
    and front is forearm lowers only (both transparent RGBA)."""
    canvas = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    if cape_mode in ("both",):
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
    if cape_mode in ("both", "collar"):
        paste_at(canvas, load(os.path.join(BASE, "Cape_Collar.png")), 550, 370)
    paste_at(canvas, load(os.path.join(BASE, "Torso_Chest.png")), 550, 400)
    paste_at(canvas, load(os.path.join(BASE, "Belt_Overlay.png")), 550, 670)
    behind = canvas.copy()
    front = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    for side in ("L", "R"):
        _, low, cap = ARM_PIECES[side]; ball, _ = ARM[side]
        fl = limb(canvas, os.path.join(CUT, low), elbows[side], cfg["arm_lower"][side], (ball[0], 0))
        front.alpha_composite(fl)
        cap_at(canvas, os.path.join(CUT, cap), elbows[side])
    paste_at(canvas, load(os.path.join(BASE, "Neck.png"), scale=1.05), 550, 360)
    paste_at(canvas, load(os.path.join(BASE, "Head_Front.png")), 550, 250)
    # behind must also include neck/head (they are above forearms in the stack,
    # but do not overlap the chest-crossing forearms; including them keeps the
    # behind mask complete for overlap measurement).
    paste_at(behind, load(os.path.join(BASE, "Neck.png"), scale=1.05), 550, 360)
    paste_at(behind, load(os.path.join(BASE, "Head_Front.png")), 550, 250)
    return canvas, behind, front

def alpha_count(im):
    a = np.asarray(im)[..., 3] > 10
    return int(a.sum()), (tuple(int(v) for v in Image.open(im.filename).split()[-1].getbbox()) if False else None)

def bbox(im):
    b = np.asarray(im)[..., 3] > 10
    ys, xs = np.where(b)
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1) if len(xs) else None

def blacken(im):
    a = np.asarray(im).copy()
    m = a[..., 3] > 10
    a[m, :3] = np.array([18, 18, 22], dtype=np.uint8)
    return Image.fromarray(a, "RGBA"), m

def apply_symbol(im, mask):
    a = np.asarray(im).copy()
    yy, xx = np.mgrid[0:1500, 0:1100]
    diamond = (np.abs(xx - 557) / 18.0 + np.abs(yy - 502) / 42.0) <= 1.0
    zone = np.zeros_like(mask); zone[460:546, 540:576] = True
    sel = mask & zone & diamond
    a[sel, :3] = np.array([255, 255, 255], dtype=np.uint8)
    return Image.fromarray(a, "RGBA"), int(sel.sum())

def white_outline(front_im, behind_im, width=4):
    """White outline on the crossing edge only: dilate(front)-front,
    restricted to pixels touching the behind body. Returns (image, counts)."""
    f = np.asarray(front_im)[..., 3] > 10
    b = np.asarray(behind_im)[..., 3] > 10
    from scipy.ndimage import binary_dilation
    dil_f = binary_dilation(f, iterations=width)
    ring = dil_f & ~f
    # crossing ring: ring pixels that lie on/adjacent to behind body
    dil_b = binary_dilation(b, iterations=2)
    cross_ring = ring & dil_b
    overlap = f & b
    return cross_ring, int(cross_ring.sum()), int(overlap.sum()), int(ring.sum())

def grey(im, path):
    bg = Image.new("RGBA", im.size, (128, 128, 128, 255))
    bg.alpha_composite(im); bg.convert("RGB").save(path)

meas = {}
