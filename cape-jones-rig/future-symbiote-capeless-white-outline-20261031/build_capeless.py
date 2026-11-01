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
OUT = os.path.join(ROOT, "future-symbiote-capeless-white-outline-20261031")
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

def build(cfg, cape=True, split_front=False):
    """Returns (canvas, behind, front) where behind excludes forearm lowers
    and front is forearm lowers only (both transparent RGBA)."""
    canvas = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    if cape:
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
    if cape:
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
# --- 1. Apose with-cape vs capeless, both blackened, piece removal ---
apose_cape, _, _ = build(APOSE, cape=True)
apose_nocape, _, _ = build(APOSE, cape=False)
for name, im in (("apose_with_cape", apose_cape), ("apose_capeless", apose_nocape)):
    print(name, bbox(im), int((np.asarray(im)[..., 3] > 10).sum()))
apose_cape_b, m_cape = blacken(apose_cape)
apose_cape_s, sym_cape = apply_symbol(apose_cape_b, m_cape)
apose_nocape_b, m_nocape = blacken(apose_nocape)
apose_nocape_s, sym_nocape = apply_symbol(apose_nocape_b, m_nocape)
visible_cape_px = int(((np.asarray(apose_cape)[..., 3] > 10) & ~(np.asarray(apose_nocape)[..., 3] > 10)).sum())
meas["apose"] = {
    "rebuilt_with_cape_alpha": int(m_cape.sum()), "rebuilt_with_cape_bbox": bbox(apose_cape),
    "rebuilt_capeless_alpha": int(m_nocape.sum()), "rebuilt_capeless_bbox": bbox(apose_nocape),
    "visible_cape_piece_px_removed": visible_cape_px,
    "old_rectangle_erase_px": 85752,
    "symbol_white_px_with_cape": sym_cape, "symbol_white_px_capeless": sym_nocape,
    "original_plate_alpha": 373846, "original_plate_bbox": (248, 253, 876, 1295),
}
apose_cape_s.save(os.path.join(OUT, "symbiote-apose-WITH-cape-20261031.png"))
apose_nocape_s.save(os.path.join(OUT, "symbiote-apose-CAPELESS-20261031.png"))
grey(apose_cape_s, os.path.join(OUT, "symbiote-apose-WITH-cape-20261031-on-grey.png"))
grey(apose_nocape_s, os.path.join(OUT, "symbiote-apose-CAPELESS-20261031-on-grey.png"))
print("apose visible cape px removed by piece omission:", visible_cape_px)

# --- 2. Cape-absorption animation: cape pieces shrink INTO the torso ---
# Build body stack without cape once (apose), then draw scaled cape pieces
# BEHIND it each frame, centre moving toward the chest (550,560).
body_nocape, _, _ = build(APOSE, cape=False)
body_nocape_b, m_body = blacken(body_nocape)
body_nocape_s, _ = apply_symbol(body_nocape_b, m_body)
cape_back = load(os.path.join(BASE, "Cape_Back_Main.png"))   # 466x791 at SCALE
cape_collar = load(os.path.join(BASE, "Cape_Collar.png"))    # 342x176
# original paste centres: back (550, 410+791/2=805), collar (550, 370+176/2=458)
def smoothstep(t):
    return t * t * (3 - 2 * t)
anim_frames = []
for i in range(16):
    if i <= 1:
        s = 1.0
    elif i >= 13:
        s = 0.0
    else:
        s = 1.0 - smoothstep((i - 1) / 11.0)
    frame = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    if s > 0:
        for piece, ocx, ocy, tx, ty in ((cape_back, 550, 805, 550, 560),
                                        (cape_collar, 550, 458, 550, 500)):
            w, h = int(piece.size[0] * s), int(piece.size[1] * s)
            if w >= 2 and h >= 2:
                sc = piece.resize((w, h), Image.LANCZOS)
                cx = int(ocx + (tx - ocx) * (1 - s)); cy = int(ocy + (ty - ocy) * (1 - s))
                frame.paste(sc, (cx - w // 2, cy - h // 2), sc)
    frame.alpha_composite(body_nocape_s)
    anim_frames.append(frame)
    frame.save(os.path.join(OUT, "frames", f"cape-absorb-f{i:02d}-20261031.png"))
anim_frames[0].save(os.path.join(OUT, "cape-absorption-20261031.gif"), save_all=True,
                    append_images=anim_frames[1:], duration=160, loop=0)
# MP4 via ffmpeg if available
os.system(f"ffmpeg -y -loglevel error -framerate 6 -i {OUT}/frames/cape-absorb-f%02d-20261031.png "
          f"-vf scale=1100:1500 -c:v libx264 -pix_fmt yuv420p {OUT}/cape-absorption-20261031.mp4")
meas["animation"] = {"frames": 16, "fps_note": "6fps in MP4, 160ms in GIF",
                     "cape_scale": "1.0 f00-f01, smoothstep to 0 f02-f12, 0 f13-f15",
                     "cape_centre_moves_to": "back (550,805)->(550,560), collar (550,458)->(550,500)",
                     "method": "scale + move behind body, alpha stays 255 until gone — absorbed, NOT a fade",
                     "final_frame_equals_capeless": bool(np.array_equal(np.asarray(anim_frames[-1]), np.asarray(apose_nocape_s)))}

# --- 3. Arms-in-front pose, capeless, with white self-overlap outline ---
cross, cross_behind, cross_front = build(CROSS, cape=False)
cross_b, m_cross = blacken(cross)
cross_s, sym_cross = apply_symbol(cross_b, m_cross)
# blacken behind/front separately for the outline computation (same masks)
cross_behind_b, _ = blacken(cross_behind)
cross_front_b, _ = blacken(cross_front)
ring, ring_px, overlap_px, full_ring_px = white_outline(cross_front_b, cross_behind_b, width=4)
# Apply: white ring pixels on top of the blackened crossed pose
out = np.asarray(cross_s).copy()
out[ring, :3] = np.array([255, 255, 255], dtype=np.uint8)
out[ring, 3] = 255
cross_white = Image.fromarray(out, "RGBA")
# Also a no-outline control for comparison
cross_s.save(os.path.join(OUT, "symbiote-crossed-NO-outline-20261031.png"))
cross_white.save(os.path.join(OUT, "symbiote-crossed-WHITE-OUTLINE-20261031.png"))
grey(cross_s, os.path.join(OUT, "symbiote-crossed-NO-outline-20261031-on-grey.png"))
grey(cross_white, os.path.join(OUT, "symbiote-crossed-WHITE-OUTLINE-20261031-on-grey.png"))
# Detail crop: chest crossing zone, 2x
crop = cross_white.crop((300, 400, 800, 900)).resize((1000, 1000), Image.NEAREST)
crop_grey = Image.new("RGBA", crop.size, (128, 128, 128, 255)); crop_grey.alpha_composite(crop)
crop_grey.convert("RGB").save(os.path.join(OUT, "symbiote-crossed-white-outline-detail-20261031.png"))
meas["crossed"] = {
    "config": "v7c arm_upper L40/R-40, arm_lower L120/R-120, legs apose",
    "front_forearm_alpha_px": int((np.asarray(cross_front)[..., 3] > 10).sum()),
    "front_over_behind_overlap_px": overlap_px,
    "white_crossing_ring_px_width4": ring_px,
    "full_ring_px_width4_for_reference": full_ring_px,
    "ring_colour": (255, 255, 255),
    "ring_applies_to": "forearm lower pieces only (caps excluded); outline only where the ring touches the behind body",
    "symbol_white_px": sym_cross,
    "crossed_alpha": int(m_cross.sum()), "crossed_bbox": bbox(cross),
}
print("crossed:", meas["crossed"])

# --- 4. Contact sheet ---
from PIL import ImageDraw
def tile(im, tw=400):
    bg = Image.new("RGBA", (tw, int(tw * 1500 / 1100)), (128, 128, 128, 255))
    bg.alpha_composite(im.resize((tw, int(tw * 1500 / 1100))))
    return bg
items = [
    ("1 WITH cape (piece stack)", apose_cape_s),
    ("2 CAPELESS (pieces removed)", apose_nocape_s),
    ("3 Absorb mid (f07)", anim_frames[7]),
    ("4 Capeless crossed, NO outline", cross_s),
    ("5 Capeless crossed, WHITE outline", cross_white),
]
tw = 400; th = int(tw * 1500 / 1100)
sheet = Image.new("RGBA", (tw * 3, th * 2 + 60), (0, 0, 0, 255))
d = ImageDraw.Draw(sheet)
for i, (label, im) in enumerate(items):
    x = (i % 3) * tw; y = (i // 3) * (th + 30)
    sheet.alpha_composite(tile(im, tw), (x, y)); d.text((x + 4, y + th + 4), label, fill=(255, 255, 0))
sheet.convert("RGB").save(os.path.join(OUT, "symbiote-capeless-white-outline-contact-20261031.png"))
# Animation contact: f00, f04, f08, f12, f15
anim_items = [anim_frames[i] for i in (0, 4, 8, 12, 15)]
sheet2 = Image.new("RGBA", (tw * 5, th + 30), (0, 0, 0, 255)); d2 = ImageDraw.Draw(sheet2)
for i, im in enumerate(anim_items):
    sheet2.alpha_composite(tile(im, tw), (i * tw, 0)); d2.text((i * tw + 4, th + 4), f"absorb f{[0,4,8,12,15][i]:02d}", fill=(255, 255, 0))
sheet2.convert("RGB").save(os.path.join(OUT, "cape-absorption-contact-20261031.png"))

with open(os.path.join(OUT, "measurements-20261031.json"), "w") as f:
    json.dump(meas, f, indent=2)
print(json.dumps(meas, indent=2))
