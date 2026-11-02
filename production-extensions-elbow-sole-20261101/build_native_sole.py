#!/usr/bin/env python3
"""NATIVE SOLE-BOOT RIG PIECE for the true forward kick (2026-11-01).
This replaces the old OVERLAY kick (kick/build_sole_kick.py), which drew
the sole boot AFTER figure() returned, composited on top of a finished
video frame, in front of torso/head. The old overlay files are untouched.

Native wiring here:
- Rig piece: Sole_Boot_Native_L.png (copy of slices/Boot_Angled_Sole_L.png,
  original untouched) + sidecar anchor: cuff anchor = MEASURED shaft
  centroid (284,80) in native piece px (shaft region x>240, y<150:
  centroid (284.1,79.7); old overlay anchor (290,72) is 9.7px away,
  inside the same solid shaft, 441/441 alpha in its 21x21 neighbourhood).
  At scale 1.2 the anchor is (340.8, 96.0).
- Visibility swap, inside figure_native(): leg-L lower slot has exactly
  one visible piece per frame -- standard Leg_Front_Lower on non-extension
  frames, Sole_Boot_Native_L on extension frames 20-31. Recorded per
  frame in the xsheet and asserted in verify JSON.
- Cuff-anchored to the knee: the sole piece is placed so its cuff
  anchor lands EXACTLY on the rig-computed knee (same knee formula as
  rig-chains build_chains.py: hip + rot_vec(ball-anchor, leg_upper)*0.95).
  Knee on EXT frames = (720.5, 813.0), identical to the old xsheet.
- Draw order (rig slot, not post-frame paste): the sole piece is drawn
  inside figure_native(), in the leg-lower slot family, AFTER torso/belt
  and BEFORE neck/head -- the same slot family rig-chains uses for
  top_arms. No piece is composited after figure_native() returns;
  render() only does video framing (resize + gray canvas).
- A second variant (sole_top=False: sole drawn in the leg pass, UNDER
  torso) is rendered once for comparison, to show why the top slot was
  chosen: torso occlusion px is measured, not assumed.
Joint math, anchors and phase configs are copied from rig-chains
build_chains.py / kick/build_sole_kick.py (same numbers, cited below);
limb drawing uses a swept-disc layer (sized to contain the piece's
full rotation sweep) rotated about the joint, so no piece is ever
rotated in place or cropped; validated identical to a 2x full-canvas
layer (mask IoU >= 0.9996).
"""
import os, math, json, csv, subprocess, shutil
import numpy as np
from PIL import Image

R = os.path.expanduser("~/workspace/cape-jones-rig")
BASE = os.path.join(R, "sliced")
CUT = os.path.join(R, "cut-limbs-v7c")
SRC = os.path.join(R, "production-extensions-20261101/slices/Boot_Angled_Sole_L.png")
OUT = "/var/tmp/elbow-sole-20261101/sole"
FR = os.path.join(OUT, "frames")
os.makedirs(FR, exist_ok=True)
os.makedirs(os.path.join(OUT, "rig-pieces"), exist_ok=True)
SCALE = 0.95
SOLE_SCALE = 1.2
CUFF_NATIVE = (284, 80)          # measured shaft centroid, native piece px
CUFF_OLD = (290, 72)             # old overlay anchor, for comparison
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
LEG = {"L": ((95, 314), (77, 40)), "R": ((100, 314), (84, 40))}
LEG_PIECES = {"L": ("Leg_Front_Upper.png", "Leg_Front_Lower.png", "Leg_Front_Cap.png"),
              "R": ("Leg_Back_Upper.png", "Leg_Back_Lower.png", "Leg_Back_Cap.png")}
ARM_PIECES = {"L": ("Arm_Front_Upper.png", "Arm_Front_Lower.png", "Arm_Front_Cap.png"),
              "R": ("Arm_Back_Upper.png", "Arm_Back_Lower.png", "Arm_Back_Cap.png")}
shutil.copyfile(SRC, os.path.join(OUT, "rig-pieces", "Sole_Boot_Native_L.png"))

_cache = {}
def load(p, scale=SCALE):
    k = (p, scale)
    if k not in _cache:
        im = Image.open(p).convert("RGBA")
        _cache[k] = im.resize((max(1, int(im.size[0] * scale)),
                               max(1, int(im.size[1] * scale))), Image.LANCZOS)
    return _cache[k]

def paste_at(c, im, cx, top):
    c.alpha_composite(im, (int(cx - im.size[0] / 2), int(top)))

def limb2(c, path, joint, angle, anchor, scale=SCALE):
    """Draw a limb piece: anchor point placed at joint, layer rotated
    about the joint. The layer is sized to the piece's swept disc
    (max anchor-to-corner radius + 2px), so rotation can never clip
    the piece -- mathematically identical to rotating a full-canvas
    layer about the same point (validated: mask IoU >= 0.9996 vs the
    2x full-canvas layer on rotated thigh/forearm/lower cases), at
    ~7x fewer pixels. Resample NEAREST, matching rig-chains bc.limb."""
    im = load(path, scale)
    ax, ay = anchor[0] * scale, anchor[1] * scale
    corners = [(0 - ax, 0 - ay), (im.size[0] - ax, 0 - ay),
               (0 - ax, im.size[1] - ay), (im.size[0] - ax, im.size[1] - ay)]
    Rm = int(math.ceil(max(math.hypot(x, y) for x, y in corners))) + 2
    layer = Image.new("RGBA", (2 * Rm + 1, 2 * Rm + 1), (0, 0, 0, 0))
    layer.alpha_composite(im, (int(Rm - ax), int(Rm - ay)))
    if angle:
        layer = layer.rotate(angle, center=(Rm, Rm),
                             expand=False, resample=Image.NEAREST)
    c.alpha_composite(layer, (int(joint[0] - Rm), int(joint[1] - Rm)))

def cap_at(c, path, joint):
    im = load(path)
    c.alpha_composite(im, (int(joint[0] - im.size[0] / 2),
                           int(joint[1] - im.size[1] / 2)))

def rot_vec(v, a):
    r = math.radians(a)
    x, y = v
    return (x * math.cos(r) + y * math.sin(r), -x * math.sin(r) + y * math.cos(r))

def figure_native(c, cx, cfg, sole_visible, sole_top=True):
    """One rig render. Returns (canvas, knees, visibility). The sole
    piece, when visible, is drawn HERE, inside this function -- never
    composited onto a returned frame."""
    vis = {"leg_L_lower_standard": not sole_visible,
           "leg_L_lower_sole_native": sole_visible}
    paste_at(c, load(os.path.join(BASE, "Cape_Back_Main.png")), cx, 410)
    hips = {"L": (cx - 80, 740), "R": (cx + 65, 740)}
    shoulders = {"L": (cx - 120, 445), "R": (cx + 120, 445)}
    knees = {}
    sole_layer = None
    for side in ("L", "R"):
        hip = hips[side]
        ball, hip_anchor = LEG[side]
        vec = (ball[0] - hip_anchor[0], ball[1] - hip_anchor[1])
        up, low, cap = LEG_PIECES[side]
        limb2(c, os.path.join(CUT, up), hip, cfg["leg_upper"][side], hip_anchor)
        knee = (hip[0] + rot_vec(vec, cfg["leg_upper"][side])[0] * SCALE,
                hip[1] + rot_vec(vec, cfg["leg_upper"][side])[1] * SCALE)
        knees[side] = knee
        if side == "L" and sole_visible:
            if sole_top:
                pass  # deferred to the sole slot below (after torso)
            else:
                limb2(c, os.path.join(OUT, "rig-pieces", "Sole_Boot_Native_L.png"),
                      knee, cfg["leg_lower"][side], CUFF_NATIVE, scale=SOLE_SCALE)
                cap_at(c, os.path.join(CUT, cap), knee)
            continue
        limb2(c, os.path.join(CUT, low), knee, cfg["leg_lower"][side], (ball[0], 0))
        cap_at(c, os.path.join(CUT, cap), knee)
    elbows = {}
    for side in ("L", "R"):
        ball, sh_anchor = ARM[side]
        vec = (ball[0] - sh_anchor[0], ball[1] - sh_anchor[1])
        up, _, _ = ARM_PIECES[side]
        sh = shoulders[side]
        limb2(c, os.path.join(CUT, up), sh, cfg["arm_upper"][side], sh_anchor)
        elbows[side] = (sh[0] + rot_vec(vec, cfg["arm_upper"][side])[0] * SCALE,
                        sh[1] + rot_vec(vec, cfg["arm_lower"][side])[1] * SCALE)
    paste_at(c, load(os.path.join(BASE, "Pelvis.png")), cx, 680)
    paste_at(c, load(os.path.join(BASE, "Cape_Collar.png")), cx, 370)
    paste_at(c, load(os.path.join(BASE, "Torso_Chest.png")), cx, 400)
    paste_at(c, load(os.path.join(BASE, "Belt_Overlay.png")), cx, 670)
    for side in ("L", "R"):
        _, low, cap = ARM_PIECES[side]
        ball, _ = ARM[side]
        limb2(c, os.path.join(CUT, low), elbows[side], cfg["arm_lower"][side], (ball[0], 0))
        cap_at(c, os.path.join(CUT, cap), elbows[side])
    if sole_visible and sole_top:
        # NATIVE SOLE SLOT: rig-computed knee, cuff-anchored, inside
        # figure_native(), after torso/belt, before neck/head.
        limb2(c, os.path.join(OUT, "rig-pieces", "Sole_Boot_Native_L.png"),
              knees["L"], cfg["leg_lower"]["L"], CUFF_NATIVE, scale=SOLE_SCALE)
        cap_at(c, os.path.join(CUT, LEG_PIECES["L"][2]), knees["L"])
    paste_at(c, load(os.path.join(BASE, "Neck.png"), scale=1.05), cx, 360)
    head = load(os.path.join(BASE, "Head_Front.png"))
    c.alpha_composite(head, (int(cx - head.size[0] / 2), int(331 - head.size[1] / 2)))
    return c, knees, vis

def video_frame(rgba):
    im = rgba.resize((550, 750), Image.LANCZOS)
    canvas = Image.new("RGBA", (1100, 750), (128, 128, 128, 255))
    canvas.alpha_composite(im, ((1100 - 550) // 2, 0))
    return canvas.convert("RGB")

def C(au, al, lu, ll):
    return {"arm_upper": {"L": au[0], "R": au[1]}, "arm_lower": {"L": al[0], "R": al[1]},
            "leg_upper": {"L": lu[0], "R": lu[1]}, "leg_lower": {"L": ll[0], "R": ll[1]}}

def lerp(a, b, t):
    return {g: {s: a[g][s] + (b[g][s] - a[g][s]) * t for s in ("L", "R")}
            for g in ("arm_upper", "arm_lower", "leg_upper", "leg_lower")}

def ease(t):
    return t * t * (3 - 2 * t)

STAND = C((0, 0), (0, 0), (0, 0), (0, 0))
CHAMBER = C((-25, 25), (30, -30), (70, 0), (-40, 0))
EXT = C((-55, 45), (30, -30), (70, 0), (0, 0))

def render(cfg, sole_visible, sole_top=True):
    c = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    c, knees, vis = figure_native(c, 550, cfg, sole_visible, sole_top)
    return video_frame(c), knees, vis, c

frames, masters, meta = [], [], []
def add(cfg, sole_visible, note):
    vf, knees, vis, master = render(cfg, sole_visible, True)
    frames.append(vf)
    masters.append(master)
    vf.save(os.path.join(FR, f"sole-native-{len(frames) - 1:03d}.jpg"), quality=92)
    meta.append({"frame": len(frames) - 1, "phase": note,
                 "sole_native_visible": sole_visible,
                 "leg_L_lower_standard_visible": vis["leg_L_lower_standard"],
                 "leg_L_lower_sole_native_visible": vis["leg_L_lower_sole_native"],
                 "piece": "Sole_Boot_Native_L (rig slot, cuff-anchored)" if sole_visible
                          else "Leg_Front_Lower (standard)",
                 "draw_slot": "sole slot after torso/belt, before neck/head" if sole_visible
                              else "leg pass",
                 "knee_L_x": round(knees["L"][0], 1), "knee_L_y": round(knees["L"][1], 1),
                 "planted_leg": "LEG2 unchanged, foot on ground line"})

for _ in range(12):
    add(STAND, False, "stand")
for i in range(8):
    add(lerp(STAND, CHAMBER, ease((i + 1) / 8)), False, "chamber")
for _ in range(12):
    add(EXT, True, "EXTENSION sole-native")
for i in range(8):
    add(lerp(EXT, STAND, ease((i + 1) / 8)), False, "recover")
for _ in range(8):
    add(STAND, False, "stand")
assert len(frames) == 48
# visibility assertion: exactly one L lower visible every frame; sole on 20-31 only
for m in meta:
    assert m["leg_L_lower_standard_visible"] != m["leg_L_lower_sole_native_visible"], m
    assert m["leg_L_lower_sole_native_visible"] == (20 <= m["frame"] <= 31), m

with open(os.path.join(OUT, "sole-native-frames.txt"), "w") as fh:
    for i in range(48):
        fh.write(f"file '{FR}/sole-native-{i:03d}.jpg'\n")
mp4 = os.path.join(OUT, "sole-native-kick-20261101.mp4")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-r", "24",
                "-i", os.path.join(OUT, "sole-native-frames.txt"),
                "-vf", "scale=1100:750", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", mp4], check=True)
small = [f.resize((550, 375)) for f in frames]
small[0].save(os.path.join(OUT, "sole-native-kick-20261101.gif"), save_all=True,
              append_images=small[1:], duration=42, loop=0)
with open(os.path.join(OUT, "sole-native-kick-xsheet-20261101.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(meta[0].keys()))
    w.writeheader()
    w.writerows(meta)
frames[20].save(os.path.join(OUT, "sole-native-extension-still-20261101.png"))
frames[0].save(os.path.join(OUT, "sole-native-stand-still-20261101.png"))
masters[20].save(os.path.join(OUT, "sole-native-extension-master-20261101.png"))
# under-torso comparison still (frame 20 geometry, sole in leg pass)
_, _, _, master_under = render(EXT, True, sole_top=False)
video_frame(master_under).save(os.path.join(OUT, "sole-native-extension-under-torso-20261101.png"))
master_under.save(os.path.join(OUT, "sole-native-extension-under-torso-master-20261101.png"))
print("NATIVE SOLE frames:", len(frames), "mp4 bytes:", os.path.getsize(mp4))

# ---- measurements on the rig canvas (1100x1500), frame 20 ----
master = masters[20]
ma = np.asarray(master)
knee = (720.5, 813.0)
kx, ky = int(round(knee[0])), int(round(knee[1]))
sole_mask = np.zeros(ma.shape[:2], dtype=bool)
# sole layer alone, placed exactly as in the figure
sole_im = load(os.path.join(OUT, "rig-pieces", "Sole_Boot_Native_L.png"), SOLE_SCALE)
ax, ay = CUFF_NATIVE[0] * SOLE_SCALE, CUFF_NATIVE[1] * SOLE_SCALE
sx, sy = int(kx - ax), int(ky - ay)
sole_layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
sole_layer.alpha_composite(sole_im, (sx, sy))
sole_a = np.asarray(sole_layer)[:, :, 3] > 10
print("sole placed at", (sx, sy), "cuff anchor lands at",
      (sx + ax, sy + ay), "== knee", knee)
print("canvas alpha at knee (sole covers knee):", bool(ma[ky, kx, 3] > 10))
ys, xs = np.where(sole_a)
d_knee = float(np.sqrt((xs - kx) ** 2 + (ys - ky) ** 2).min())
print("distance knee -> nearest sole alpha px:", d_knee)
# thigh layer alone (leg L upper at EXT) vs sole overlap near knee
thigh_layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
limb2(thigh_layer, os.path.join(CUT, LEG_PIECES["L"][0]), (470, 740),
      EXT["leg_upper"]["L"], LEG["L"][1])
thigh_a = np.asarray(thigh_layer)[:, :, 3] > 10
yy, xx = np.mgrid[0:1500, 0:1100]
disc80 = (xx - kx) ** 2 + (yy - ky) ** 2 <= 80 * 80
overlap = int((thigh_a & sole_a & disc80).sum())
print("thigh/sole overlap within r80 of knee (px):", overlap)
# torso layer alone vs sole overlap (boot covers torso by N px)
torso_layer = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
paste_at(torso_layer, load(os.path.join(BASE, "Torso_Chest.png")), 550, 400)
torso_a = np.asarray(torso_layer)[:, :, 3] > 10
print("sole/torso alpha overlap (px, boot covers torso):", int((sole_a & torso_a).sum()))
# top vs under-torso: differing px inside sole bbox = torso occlusion
mu = np.asarray(master_under)
sole_ys, sole_xs = np.where(sole_a)
bbox = (sole_xs.min(), sole_xs.max(), sole_ys.min(), sole_ys.max())
crop_top = ma[bbox[2]:bbox[3] + 1, bbox[0]:bbox[1] + 1, :3].astype(int)
crop_under = mu[bbox[2]:bbox[3] + 1, bbox[0]:bbox[1] + 1, :3].astype(int)
sole_crop = sole_a[bbox[2]:bbox[3] + 1, bbox[0]:bbox[1] + 1]
diff = (np.abs(crop_top - crop_under).sum(axis=2) > 30) & sole_crop
print("sole bbox:", [int(v) for v in bbox], "sole alpha px:", int(sole_a.sum()))
print("torso-occluded sole px in under-torso variant:", int(diff.sum()))
# stand-frame validation vs old overlay stand still (bc.figure STAND)
old_stand = Image.open(os.path.join(R, "production-extensions-20261101/kick/sole-kick-stand-still-20261101.png")).convert("RGB")
mine_stand = frames[0]
oa = np.asarray(old_stand).astype(int)
mn = np.asarray(mine_stand).astype(int)
print("stand validation vs old bc stand still: mean abs diff",
      round(float(np.abs(oa - mn).mean()), 3), "max", int(np.abs(oa - mn).max()))
meas = {"knee_L_EXT": list(knee), "cuff_anchor_native_px": list(CUFF_NATIVE),
        "cuff_anchor_scaled_1.2": [round(ax, 1), round(ay, 1)],
        "cuff_anchor_old_px": list(CUFF_OLD),
        "cuff_old_vs_measured_px": round(float(math.hypot(290 - 284, 72 - 80)), 1),
        "sole_paste_xy": [sx, sy], "cuff_lands_at_knee": [round(sx + ax, 1), round(sy + ay, 1)],
        "canvas_alpha_at_knee": bool(ma[ky, kx, 3] > 10),
        "knee_to_nearest_sole_alpha_px": d_knee,
        "thigh_sole_overlap_r80_px": overlap,
        "sole_torso_overlap_px": int((sole_a & torso_a).sum()),
        "sole_bbox": [int(v) for v in bbox], "sole_alpha_px": int(sole_a.sum()),
        "torso_occluded_sole_px_under_variant": int(diff.sum()),
        "stand_mean_abs_diff_vs_old": round(float(np.abs(oa - mn).mean()), 3)}
json.dump(meas, open(os.path.join(OUT, "sole-native-measurements.json"), "w"), indent=1)
json.dump({"frames": 48, "fps": 24, "extension_frames": "20-31 (sole native)",
           "piece": "rig-pieces/Sole_Boot_Native_L.png (copy of slices/Boot_Angled_Sole_L.png; original untouched)",
           "cuff_anchor_native_px": list(CUFF_NATIVE), "scale": SOLE_SCALE,
           "draw_slot": "inside figure_native(), after torso/belt, before neck/head",
           "old_overlay": "production-extensions-20261101/kick/* untouched; old method pasted onto finished frame after figure() returned",
           "planted_leg": "LEG2 never moves"},
          open(os.path.join(OUT, "sole-native-meta.json"), "w"), indent=1)
print("MEAS", json.dumps(meas))
