#!/usr/bin/env python3
"""V3 art prep, v2 (2026-11-23, after the handswap rejection).

CORRECTIONS (owner, 2026-11-23 10:40-10:42 EST) — owned, not defended:
1. NO joint caps/discs/circles, ever. The sibling handswap lane generated
   a literal white disc (rig/parts/Cap_disc.png) and stuck it on every
   joint — that is NOT in this build and never will be. This build's own
   fault was the same class of mistake in smaller form: the elbow/knee
   crops OVERLAPPED by +-8px, so the ball was drawn in BOTH pieces and
   read as a separate joint disc during the raise (doubled ball, ring).
   FIX: SOCKET CUT. Each joint is cut along the ball's OWN outline
   circle (fitted from the art, RMS ~1.1px): the ball belongs entirely
   to the lower piece, the upper piece ends in a concave socket of the
   same circle. No pixel is in both pieces, none is in neither — the
   two pieces together reproduce the one-piece art EXACTLY at rest
   (verified below by pixel diff), and the ball rotates inside its
   socket with no gap and no doubling at any angle. Nothing is added;
   the cut follows the art's own contour.
2. GUMBALL VERIFIED FIRST-HAND (GB200 .fla, opened 2026-11-23): there is
   NO cap/disc/ball-joint anywhere in GB200. L_ARM/R_ARM are ONE ARM
   layer of 24/26 keyframes, every keyframe a single DOMShape — the whole
   arm+hand redrawn per pose, elbow bend DRAWN not jointed. L_LEG/R_LEG
   are 10 DOMShape keyframes each. The ONLY limb split is at the
   SHOULDER, front/back: two instances sharing ONE transformationPoint
   (L (30.05, 47.75), R (29.95, 47)) — a back arm below the body layer
   and a front arm above it. The earlier claim that Gumball uses an
   "overlap-cap" was WRONG. Our translation: the split must be
   invisible — the two pieces must read as the one drawn limb. The
   socket cut is that translation for a cutout rig (Gumball redraws per
   pose; we cannot, so the cut follows the drawn ball's own circle).
3. INVISIBLE HAND SWAP (owner 10:42 EST). The old swap used 7 separate
   planes per side, each sized from its own art — cuff centre x varied
   37-64px between variants, so the hand TELEPORTED sideways up to
   0.24 units at every swap (a literal scene cut). FIX: ONE plane per
   side, one common canvas (132x144), every variant re-centred in the
   ART so the cuff sits at the same place (cuff centre x=66, cuff top
   row 0). Same plane, same pivot, same position — only the IMAGE on
   that plane changes. Mouths likewise on one common canvas (105x95).

Measured geometry (fitted from the art itself, RANSAC + Kasa circle
fit on the ball's dark outline, RMS ~1.1px):
- Arm_Front (153x511): elbow ball centre (58.9, 223.1) r=31.8,
  wrist pinch (63.5, 410). Plane 1.4535 x 4.8545, shoulder top 10.8.
  Elbow rig (-1.767, 8.681), wrist rig (-1.724, 6.905).
- Arm_Back (158x510): elbow ball centre (109.4, 275.5) r=41.2,
  wrist pinch (113.5, 410). Elbow rig (1.889, 8.183),
  wrist rig (1.928, 6.905).
- Leg_Front (155x637): knee ball centre (92.5, 299.1) r=37.5.
  Knee rig (-0.757, 5.109).
- Leg_Back (168x637): knee ball centre (101.7, 297.2) r=38.9.
  Knee rig (1.068, 5.127).
- rig_x(img_x) = anchor_x + (img_x - W/2)*0.0095; rig_y(img_y) =
  top_y - img_y*0.0095, where anchor_x/top_y are the V2 REST anchors
  (arm centre +-1.6, top 10.8; leg centre +-0.9, top 7.95).
- Hands: cuff centre x per variant measured (see output); common canvas
  132x144, cuff centre (66, 0). Grip finger centre measured on the
  common canvas for the remote grip check.
- Remote: device-only crop, unchanged from v1.

COPIES ONLY: nothing in rig/ is read-modify-written; every output lands
in v3-swap-system/art/ and is reproducible from the repo slices.
Writes v3-swap-system/art-geometry.json (single source of truth for
the build/verify scripts — no hand-copied constants).
"""
import json
import os
from PIL import Image
import numpy as np

WD = "/home/hatch/workspace/_cape-jones-parking-lot-2d"
SRC = f"{WD}/rig/parts/sliced"
RIGP = f"{WD}/rig/parts"
OUT = f"{WD}/v3-swap-system/art"
os.makedirs(OUT, exist_ok=True)
SCALE = 0.0095  # rig units per px (0.95 scale / 100)

GEOM = {"balls": {}, "wrists": {}, "planes": {}, "hands": {}, "remote": {}}


def load(p):
    return Image.open(p).convert("RGBA")


def save(im, name):
    im.save(os.path.join(OUT, name))
    print(f"  {name}: {im.size} bbox={im.getbbox()}")


def socket_split(im, cx, cy, r):
    """Split an image into upper/lower pieces along the ball's outline
    circle. Ball (cx, cy, r) belongs entirely to the LOWER piece; the
    UPPER piece ends in a concave socket of the same circle.
    Exact partition: lower owns {dist <= r} U {y > cy}; upper owns
    {y < cy, dist > r}. No pixel in both, none in neither."""
    a = np.array(im).astype(int)
    H, W = a.shape[0], a.shape[1]
    yy, xx = np.mgrid[0:H, 0:W]
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    lower_owns = (dist <= r) | (yy > cy)
    upper = im.copy()
    lower = im.copy()
    ua = np.array(upper)
    la = np.array(lower)
    ua[lower_owns] = (0, 0, 0, 0)
    la[~lower_owns] = (0, 0, 0, 0)
    return Image.fromarray(ua), Image.fromarray(la)


def check_partition(src, upper, lower, up_box, lo_box):
    """Paste both pieces back at their original positions; the result
    must equal the source EXACTLY (max diff 0). Proves the cut is clean:
    no pixel lost, none doubled."""
    canvas = Image.new("RGBA", src.size, (0, 0, 0, 0))
    # alpha_composite (NOT paste-with-mask: that squares partial alpha
    # on anti-aliased edges). The pieces are disjoint by construction,
    # so compositing reproduces the source exactly.
    canvas.alpha_composite(upper, (up_box[0], up_box[1]))
    canvas.alpha_composite(lower, (lo_box[0], lo_box[1]))
    # Compare only the rows the two pieces cover (up_top..lo_bot). The
    # source below the wrist (rows 410..511) is the old DRAWN FIST,
    # deliberately excluded — the forearm ends at the cuff, the hand is
    # its own slot. For the legs the pieces cover the whole image.
    y0, y1 = up_box[1], lo_box[1] + lower.size[1]
    sa = np.asarray(src).astype(int)[y0:y1]
    ca = np.asarray(canvas).astype(int)[y0:y1]
    assert (sa[:, :, 3] == ca[:, :, 3]).all(), "alpha partition not exact!"
    vis = sa[:, :, 3] > 0
    d = np.abs(sa[:, :, :3] - ca[:, :, :3])[vis]
    print(f"    partition check: alpha exact, visible RGB max diff "
          f"{d.max() if d.size else 0} (want 0)")
    assert d.max() == 0, "socket partition is not exact!"
    return True


# ---- arms: socket cut at the elbow ball ---------------------------------
# (source, ball (cx, cy, r), wrist_y, anchor_x, top_y)
ARM = {
    "R": ("Arm_Front.png", (58.9, 223.1, 31.8), 410, -1.6, 10.8),
    "L": ("Arm_Back.png", (109.4, 275.5, 41.2), 410, 1.6, 10.8),
}
for side, (fname, (cx, cy, r), wrist_y, ax, top_y) in ARM.items():
    im = load(os.path.join(SRC, fname))
    W, H = im.size
    upper, lower = socket_split(im, cx, cy, r)
    # Crop to the useful rows: upper 0..cy+r, lower cy-r..wrist.
    up_top, up_bot = 0, int(round(cy + r)) + 1
    lo_top, lo_bot = int(round(cy - r)), wrist_y
    up_crop = upper.crop((0, up_top, W, up_bot))
    lo_crop = lower.crop((0, lo_top, W, lo_bot))
    save(up_crop, f"upperArm_{side}.png")
    save(lo_crop, f"forearm_{side}.png")
    check_partition(im, up_crop, lo_crop, (0, up_top), (0, lo_top))
    # Rig pivots from the fitted ball / wrist pinch (measured).
    wrist_cx = {"R": 63.5, "L": 113.5}[side]
    elbow_rig = (ax + (cx - W / 2) * SCALE, top_y - cy * SCALE)
    wrist_rig = (ax + (wrist_cx - W / 2) * SCALE, top_y - wrist_y * SCALE)
    GEOM["balls"][f"elbow{side}"] = {"cx": cx, "cy": cy, "r": r,
                                     "rig": elbow_rig}
    GEOM["wrists"][side] = {"cx": wrist_cx, "y": wrist_y, "rig": wrist_rig}
    # Plane centres (top-anchored, as V2 did).
    up_h = up_crop.size[1] * SCALE
    lo_h = lo_crop.size[1] * SCALE
    lo_top_y = top_y - lo_top * SCALE
    GEOM["planes"][f"UpperArm{side}"] = {
        "size": [up_crop.size[0] * SCALE, up_h],
        "center": [ax, top_y - up_h / 2],
        # ball centre in plane-local coords (from plane centre).
        "ball_local": [(cx - W / 2) * SCALE,
                       (up_crop.size[1] / 2 - cy) * SCALE]}
    GEOM["planes"][f"Forearm{side}"] = {
        "size": [lo_crop.size[0] * SCALE, lo_h],
        "center": [ax, lo_top_y - lo_h / 2],
        "ball_local": [(cx - W / 2) * SCALE,
                       (lo_crop.size[1] / 2 - (cy - lo_top)) * SCALE]}
    print(f"  arm {side}: elbow rig {elbow_rig} wrist rig {wrist_rig} "
          f"upper {up_crop.size} forearm {lo_crop.size}")

# ---- legs: socket cut at the knee ball -----------------------------------
LEG = {
    "R": ("Leg_Front.png", (92.5, 299.1, 37.5), -0.9, 7.95),
    "L": ("Leg_Back.png", (101.7, 297.2, 38.9), 0.9, 7.95),
}
for side, (fname, (cx, cy, r), ax, top_y) in LEG.items():
    im = load(os.path.join(SRC, fname))
    W, H = im.size
    upper, lower = socket_split(im, cx, cy, r)
    up_top, up_bot = 0, int(round(cy + r)) + 1
    lo_top, lo_bot = int(round(cy - r)), H
    up_crop = upper.crop((0, up_top, W, up_bot))
    lo_crop = lower.crop((0, lo_top, W, lo_bot))
    save(up_crop, f"thigh_{side}.png")
    save(lo_crop, f"shin_{side}.png")
    check_partition(im, up_crop, lo_crop, (0, up_top), (0, lo_top))
    knee_rig = (ax + (cx - W / 2) * SCALE, top_y - cy * SCALE)
    GEOM["balls"][f"knee{side}"] = {"cx": cx, "cy": cy, "r": r,
                                    "rig": knee_rig}
    up_h = up_crop.size[1] * SCALE
    lo_h = lo_crop.size[1] * SCALE
    lo_top_y = top_y - lo_top * SCALE
    GEOM["planes"][f"Thigh{side}"] = {
        "size": [up_crop.size[0] * SCALE, up_h],
        "center": [ax, top_y - up_h / 2],
        "ball_local": [(cx - W / 2) * SCALE,
                       (up_crop.size[1] / 2 - cy) * SCALE]}
    GEOM["planes"][f"Shin{side}"] = {
        "size": [lo_crop.size[0] * SCALE, lo_h],
        "center": [ax, lo_top_y - lo_h / 2],
        "ball_local": [(cx - W / 2) * SCALE,
                       (lo_crop.size[1] / 2 - (cy - lo_top)) * SCALE]}
    print(f"  leg {side}: knee rig {knee_rig} "
          f"thigh {up_crop.size} shin {lo_crop.size}")

# ---- hands: ONE common canvas, cuff re-centred in the ART ----------------
# Canvas 132x144, cuff centre at (66, 0). Every variant pasted so its
# cuff centre lands at canvas x=66 and its cuff top at row 0. The plane
# is then the same size/position for every variant — only the image
# changes. (Old fault: cuff centre x varied 37-64px between variants,
# so the hand jumped up to 0.24 units sideways at every swap.)
CANVAS_W, CANVAS_H, CUFF_X = 132, 144, 66
HAND_NAMES = ["Fist", "FistBack", "Open", "Point", "Point2", "Relaxed", "Grip"]
for side, suffix in (("R", "rot180"), ("L", "flip")):
    for n in range(1, 8):
        src = os.path.join(
            RIGP, f"Hand_{n}_{HAND_NAMES[n-1]}_{suffix}.png")
        im = load(src)
        a = np.asarray(im).astype(int)
        alpha = a[:, :, 3] > 10
        rows = np.where(alpha.any(axis=1))[0]
        top = int(rows.min())
        cuff_rows = rows[:6]
        xs = np.where(alpha[cuff_rows].any(axis=0))[0]
        cuff_cx = (xs.min() + xs.max()) / 2
        canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        canvas.paste(im, (round(CUFF_X - cuff_cx), -top), im)
        save(canvas, f"Hand_{side}_{n}.png")
        print(f"    Hand_{side}_{n} {HAND_NAMES[n-1]}: cuff_cx={cuff_cx:.1f} "
              f"-> canvas offset x={round(CUFF_X - cuff_cx)}")
        if HAND_NAMES[n - 1] == "Grip":
            # Finger centre of the Grip variant on the common canvas:
            # opaque centroid of the bottom 40% (the fingers). The
            # remote grip point must land here.
            ca = np.asarray(canvas).astype(int)
            calpha = ca[:, :, 3] > 10
            fy = int(CANVAS_H * 0.6)
            ys, fxs = np.where(calpha[fy:, :])
            GEOM["hands"][f"Grip_{side}_finger_canvas"] = [
                float(fxs.mean()), float(ys.mean() + fy)]
            print(f"    Grip_{side} finger centre on canvas: "
                  f"({fxs.mean():.1f}, {ys.mean() + fy:.1f})")
GEOM["hands"]["canvas"] = [CANVAS_W, CANVAS_H]
GEOM["hands"]["cuff"] = [CUFF_X, 0]

# ---- mouths: ONE common canvas, centred ----------------------------------
MC_W, MC_H = 105, 95
for mn in ["Closed", "Open", "Shout", "Smile", "Teeth"]:
    im = load(os.path.join(SRC, f"Mouth_{mn}.png"))
    canvas = Image.new("RGBA", (MC_W, MC_H), (0, 0, 0, 0))
    canvas.paste(im, ((MC_W - im.size[0]) // 2, (MC_H - im.size[1]) // 2), im)
    save(canvas, f"Mouth_{mn}.png")
GEOM["mouth_canvas"] = [MC_W, MC_H]

# ---- eyes (unchanged — shared-object variants, passed own-eyes) ----------
for f in ("Mouth_Closed.png", "Mouth_Open.png", "Mouth_Shout.png",
          "Mouth_Smile.png", "Mouth_Teeth.png"):
    pass  # mouths are rebuilt above on the common canvas
save(load(os.path.join(SRC, "Eye_White_L.png")), "Eye_L.png")
save(load(os.path.join(SRC, "Eye_R.png")) if os.path.exists(os.path.join(SRC, "Eye_R.png"))
     else load(os.path.join(SRC, "Eye_White_R.png")), "Eye_R.png")
save(load(os.path.join(SRC, "Eyes_AngryStrip.png")), "Eyes_AngryStrip.png")
save(load(os.path.join(SRC, "Face_Angry.png")), "Face_Angry.png")

# ---- remote: device only (unchanged from v1) ------------------------------
rem = load(os.path.join(RIGP, "Remote_fixed_v2.png"))
dev = rem.crop((14, 0, 68, 158))
px = dev.load()
for y in range(0, 70):
    for x in range(36, 54):
        r, g, b, a = px[x, y]
        if a > 10 and r + g + b > 650:
            px[x, y] = (0, 0, 0, 0)
save(dev, "Remote_Device.png")
print("  remote device: crop (14,0,68,158) of Remote_fixed_v2, glove fingers "
      "erased in x>48,y<55; grip point (46,70) in-crop")

# ---- everything else: straight copies ------------------------------------
for f in ("Torso_Chest.png", "Pelvis.png", "Belt_Overlay.png", "Neck.png",
          "Head_Front.png", "Head_Profile.png", "Leg_Front.png", "Leg_Back.png",
          "Cape_Back_Main.png", "Cape_Collar.png"):
    save(load(os.path.join(SRC, f)), f)
for f, dst in (("Pupil.png", "Pupil.png"), ("Shadow.png", "Shadow.png")):
    save(load(os.path.join(RIGP, f)), dst)

json.dump(GEOM, open(f"{WD}/v3-swap-system/art-geometry.json", "w"), indent=1)
print("GEOMETRY -> v3-swap-system/art-geometry.json")
print("ART PREP V2 DONE ->", OUT)
