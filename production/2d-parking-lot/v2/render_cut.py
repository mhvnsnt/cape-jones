#!/usr/bin/env python3
"""render_cut.py — PURPLE LOT V2 cut renderer (2D, rig on twos).

Renders the 480-frame cut with the FIXED compositor (BGRA-correct parts,
sheet-level re-sliced alpha) at 1280x720, 24fps, silent, piping rawvideo
straight into ffmpeg (no per-frame files on disk).

Method (Metalocalypse/ATHF way): the COA cutout rig poses on twos — a new rig
pose every 2 frames, computer tweening (linear interpolation) between
keyframes; the cape follows through on a damped-spring sway (lag 1-2f,
overshoot, settle — the same principle as the Wiggle 2 RTX live sim, which
the Blender rig carries for real; here the spring is stepped per frame).
Backgrounds are the real painted lot plates; the sodium->purple lighting
shift is a background crossfade (the figure is NEVER graded — locked palette:
suit stays blown out, skin stays tan; a subtle rim-light band on the
streetlight side is the only figure tint). Grease-Pencil-drawn in-betweens
for the rig's gaps (squash & stretch, thumb press) are approximated here as
compositor transforms and logged as owed drawn work — see CHECKPOINT.

Usage: python3 render_cut.py [--out PATH] [--frames N] [--samples DIR]
  --frames N: render only the first N frames (smoke test).
  --samples DIR: also write sample PNGs (every 24f + key beats) for own-eyes.
Exit 0 + prints size/sha256/duration when the encode lands.
"""
import sys, os, json, math, subprocess, hashlib
sys.path.insert(0, "/home/hatch/workspace/_cape-jones-parking-lot-2d/rig")
import proof_composite as pc
import numpy as np, cv2, urllib.request

WD = "/home/hatch/workspace/_cape-jones-parking-lot-2d"
RIG = os.path.join(WD, "rig")
BGD = os.path.join(WD, "v2/backgrounds")
OUT_DEFAULT = os.path.join(WD, "v2/render/purple-lot-v2.mp4")
W, H = 1280, 720
FPS = 24
NFRAMES = 480
PART_URL = ("https://raw.githubusercontent.com/mhvnsnt/cape-jones/v2-rig-parts/"
            "production/2d-parking-lot/v2/rig-parts/")
CAPE_SY = 1.85  # cape vertical stretch about the shoulder anchor (hem -> ankles)

# --- framings at 1280x720 (0.625x the 2048x1152 proof framings) ---
WIDE = pc.Framing(34.375, 640, 463.75)
MEDIUM = pc.Framing(50.0, 640, 376.25)
MEDCLOSE = pc.Framing(70.0, 640, 430.0)
CLOSEUP = pc.Framing(106.25, 640, 312.5)

# --- part cache: cv2 decode -> BGRA (canvas-native, fast C decode) ---
_parts = {}
def part(name):
    if name not in _parts:
        data = urllib.request.urlopen(PART_URL + name + ".png", timeout=60).read()
        img = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        assert img is not None, f"decode fail {name}"
        _parts[name] = img
    return _parts[name]

def rot2d(deg):
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return np.array([[c, -s], [s, c]], dtype=np.float64)

def paste(layer, img, x0, y0):
    h, w = img.shape[0], img.shape[1]
    H, Wd = layer.shape[0], layer.shape[1]
    x1, y1 = int(round(x0)), int(round(y0))
    sx0, sy0 = max(0, -x1), max(0, -y1)
    dx0, dy0 = max(0, x1), max(0, y1)
    dx1, dy1 = min(Wd, x1 + w), min(H, y1 + h)
    if dx1 <= dx0 or dy1 <= dy0:
        return
    sx1, sy1 = sx0 + (dx1 - dx0), sy0 + (dy1 - dy0)
    src = img[sy0:sy1, sx0:sx1].astype(np.float32)
    dst = layer[dy0:dy1, dx0:dx1].astype(np.float32)
    a = (src[:, :, 3:4] / 255.0)
    out = src[:, :, :3] * a + dst[:, :, :3] * (1 - a)
    oa = np.maximum(src[:, :, 3], dst[:, :, 3])
    layer[dy0:dy1, dx0:dx1, :3] = out
    layer[dy0:dy1, dx0:dx1, 3] = oa

def render_figure(state, framing):
    """Render the rigged figure (no background) to a BGRA layer + silhouette.
    state: {angles, swaps, sway, cape, squash:(sx,sy), gag:{...}|None,
            blur_jones:bool}"""
    angles = dict(state.get("angles", {}))
    sway = state.get("sway", 0.0)
    fkmap = pc.fk(angles, framing, root_shift=state.get("root_shift", (0, 0)))
    vis = {n: v for n, (_z, _b, v) in pc.LAYOUT.items()}
    for n, v in state.get("swaps", {}).items():
        vis[n] = v
    cape_want = state.get("cape", "cape_hang")
    for c in ("cape_hang", "cape_sweep", "cape_billow", "cape_diag",
              "cape_settle", "cape_billow_pose"):
        vis[c] = (c == cape_want)
    zval = {n: z for n, (z, _b, _v) in pc.LAYOUT.items()}
    for side, snap in (("R", state.get("snap_R", False)),
                       ("L", state.get("snap_L", False))):
        if snap:
            for n in (f"upper_arm_{side}", f"forearm_{side}",
                      f"hand_glove_open_{side}",
                      f"fist_glove_h" if side == "R" else f"fist_glove_v",
                      f"hand_glove_point" if side == "R" else f"hand_glove_open_08",
                      f"forearm_{side}_out"):
                if n in zval:
                    zval[n] = 0.045
    order = sorted([n for n, v in vis.items() if v], key=lambda n: zval[n])
    canvas = np.zeros((H, W, 4), dtype=np.uint8)
    fscale = framing.K / 100.0
    sx_sq, sy_sq = state.get("squash", (1.0, 1.0))
    hsq = state.get("head_sq", 1.0)  # head-turn squash (CJ-PL-06/07), 1.0 = front
    for name in order:
        if name in ("hand_bare_gag", "remote_gag"):
            continue  # gag close-up props are placed by render_gag()
        img = part(name)
        h0, w0 = img.shape[0], img.shape[1]
        if name.startswith("cape_"):
            img = cv2.resize(img, None, fx=1.0, fy=CAPE_SY)
            h0, w0 = img.shape[0], img.shape[1]
        lx, lz = pc.placement(name, w0, h0)
        tl = framing.map(lx, lz)
        x0, y0 = tl[0], tl[1]
        img = cv2.resize(img, None, fx=fscale, fy=fscale)
        # driver pivot + total angle
        drv = pc.DRIVER.get(name)
        H0 = H1 = None
        total = 0.0
        if drv is not None:
            if name.startswith("cape_"):
                b = "Chest"
                H0 = pc.bone_head_rest_canvas(b, framing)
                H1, _t, total = fkmap[b]
                total = total + sway
            elif name == "torso":
                total = fkmap["Chest"][2]
                H0 = pc.bone_head_rest_canvas("Spine", framing)
                H1 = fkmap["Spine"][0]
            else:
                b = drv
                H0 = pc.bone_head_rest_canvas(b, framing)
                H1, _t, total = fkmap[b]
        # local layer: the part is pasted at its REST rect and then warped to
        # its POSED position inside this layer — so the bbox must cover BOTH
        # the rest corners and the rotated corners. (Bug found 2026-11-22:
        # covering only the rotated corners put the rest rect outside the
        # layer, the paste landed nowhere, and warpAffine's BORDER_TRANSPARENT
        # left uninitialized memory in the layer — stale head pixels and
        # noise showed up as floating mini-heads at the hand positions.)
        ph, pw = img.shape[0], img.shape[1]
        corners = np.array([[x0, y0], [x0 + pw, y0], [x0, y0 + ph],
                            [x0 + pw, y0 + ph]], dtype=np.float64)
        all_corners = corners
        if H0 is not None and (abs(total) > 0.01 or abs(sx_sq - 1) > 0.001
                               or abs(sy_sq - 1) > 0.001):
            R = rot2d(total)
            S = np.array([[sx_sq, 0], [0, sy_sq]], dtype=np.float64)
            if drv == "Head":
                # head turn: squash the Head-driven group horizontally about
                # the Head pivot (head, eyes, mouth share it — stay registered)
                S = S @ np.array([[hsq, 0.0], [0.0, 1.0]])
            M2 = R @ S
            rc = (H1.reshape(2, 1) + M2 @ (corners - H0).T).T
            # BUG D FIX (2026-11-22, calibrated by dot test): warpAffine's
            # content rotates by -total, NOT +total (a dot left of the pivot
            # lands DOWN-left at +80 in both pipelines; the arm drawing is a
            # horizontal band, so the proof's arms-down at +80 proves it).
            # The layer bbox must therefore cover the corners transformed by
            # the EFFECTIVE content rotation inv(M2) — the old code covered
            # only the +total corners, so for large rotations (arms +-80) the
            # real arm extent fell outside the layer and got clipped to a
            # shoulder blob (arms read as horizontal bars, hands invisible).
            # Include both rotations: belt and braces, costs nothing.
            Minv_b = np.linalg.inv(M2)
            rc_eff = (H1.reshape(2, 1) + Minv_b @ (corners - H0).T).T
            all_corners = np.vstack([corners, rc, rc_eff])
            lo = np.floor(all_corners.min(axis=0)).astype(int) - 2
            hi = np.ceil(all_corners.max(axis=0)).astype(int) + 2
        else:
            lo = np.array([int(math.floor(x0)) - 2, int(math.floor(y0)) - 2])
            hi = np.array([int(math.ceil(x0 + pw)) + 2, int(math.ceil(y0 + ph)) + 2])
        lo = np.maximum(lo, [0, 0])
        hi = np.minimum(hi, [W, H])
        lw, lh = int(hi[0] - lo[0]), int(hi[1] - lo[1])
        if lw <= 0 or lh <= 0:
            continue
        layer = np.zeros((lh, lw, 4), dtype=np.uint8)
        paste(layer, img, x0 - lo[0], y0 - lo[1])
        if H0 is not None and (abs(total) > 0.01 or abs(sx_sq - 1) > 0.001
                               or abs(sy_sq - 1) > 0.001):
            R = rot2d(total)
            S = np.array([[sx_sq, 0], [0, sy_sq]], dtype=np.float64)
            if drv == "Head":
                # head turn: squash the Head-driven group horizontally about
                # the Head pivot (head, eyes, mouth share it — stay registered)
                S = S @ np.array([[hsq, 0.0], [0.0, 1.0]])
            M2 = R @ S
            Minv = np.linalg.inv(M2)
            t = H1 - M2 @ H0
            # forward: p' = H1 + M2(p - H0); warpAffine needs inverse (dst->src).
            # In local coords (dst_local = p' - lo, src_local = p - lo):
            # src_local = Minv @ (dst_local + lo - t) - lo
            M = np.hstack([Minv, (Minv @ (lo - t) - lo).reshape(2, 1)]).astype(np.float32)
            # BORDER_CONSTANT (transparent) — never BORDER_TRANSPARENT: on an
            # empty/partial layer it leaves uninitialized memory in the
            # destination (stale pixels from earlier allocations).
            layer = cv2.warpAffine(layer, M, (lw, lh), flags=cv2.INTER_LINEAR,
                                   borderMode=cv2.BORDER_CONSTANT,
                                   borderValue=(0, 0, 0, 0))
        paste(canvas, layer, lo[0], lo[1])
    return canvas

def render_gag(state, bg):
    """Close-up gag beat: blurred Jones behind (frame-left), big bare hand
    lifting slowly, remote at the thumb, click spark on press."""
    gag = state.get("gag", {})
    lift = gag.get("lift", 0.0)      # px the hand is still below its rest spot
    press = gag.get("press", 0.0)    # px the remote is pushed down (thumb press)
    spark = gag.get("spark", 0.0)    # 0..1 spark alpha
    canvas = bg.copy()
    # Jones behind, out of focus: idle figure at WIDE, blurred, at the RIGHT
    # edge (rendered once and cached — identical every gag frame). Right, not
    # left: with the hand anchored on its button the palm covers the left, and
    # the hand art leaves a clean hole at the right edge (part x>930 is empty).
    if not hasattr(render_gag, "_jones"):
        jones_state = {"angles": {"UpperArm.R": 80, "UpperArm.L": -80},
                       "swaps": {}, "cape": "cape_hang"}
        fig = render_figure(jones_state, WIDE)
        fig = cv2.GaussianBlur(fig, (0, 0), 6)
        fig = (fig.astype(np.float32) * np.array([0.85, 0.85, 0.85, 1.0])).astype(np.uint8)
        tmp = np.zeros((H, W, 4), dtype=np.uint8)
        paste(tmp, fig, 460, -40)
        render_gag._jones = tmp
    paste(canvas, render_gag._jones, 0, 0)
    # big bare hand, lifting — anchored on its BUILT-IN round button
    # (part ~(690,240), measured off the part art) at the spark point (700,250).
    # NO separate remote_gag paste: the hand part already holds the remote, and
    # the old copy was pasted 44x559px off the built-in remote (template match:
    # remote_gag is an exact crop of hand_bare_gag at (520,65)) — that offset
    # double-draw was the visible seam. Press dips the whole hand.
    hand = part("hand_bare_gag")
    fscale = CLOSEUP.K / 100.0
    hs = 1.35 * fscale
    hand = cv2.resize(hand, None, fx=hs, fy=hs)
    hx = 700 - int(round(690 * hs))
    hy = 250 - int(round(240 * hs)) + lift + press
    paste(canvas, hand, hx, hy)
    # click spark: 4-point star at the button (tracks the hand)
    if spark > 0:
        # spark sits ON the built-in round button (part ~(743,193), measured
        # off the f0199 render) — tracks the hand through lift/press.
        cx = int(round(hx + 743 * hs))
        cy = int(round(hy + 193 * hs))  # cv2.line needs ints (lift/press are lerped floats)
        col = (255, 255, 255, int(255 * spark))
        ov = np.zeros((H, W, 4), dtype=np.uint8)
        L = 26
        cv2.line(ov, (cx - L, cy), (cx + L, cy), col, 3, cv2.LINE_AA)
        cv2.line(ov, (cx, cy - L), (cx, cy + L), col, 3, cv2.LINE_AA)
        cv2.line(ov, (cx - 18, cy - 18), (cx + 18, cy + 18), col, 2, cv2.LINE_AA)
        cv2.line(ov, (cx - 18, cy + 18), (cx + 18, cy - 18), col, 2, cv2.LINE_AA)
        paste(canvas, ov, 0, 0)
    return canvas

def rim_light(canvas, fig_layer, t_purple, side="right"):
    """Rim-only figure tint: a 2-3px band on the streetlight side of the
    silhouette, sodium-orange -> purple across the shift. The suit stays
    blown out; only the rim takes the tint."""
    sil = (fig_layer[:, :, 3] > 10).astype(np.uint8)
    if sil.sum() == 0:
        return canvas
    dil = cv2.dilate(sil, np.ones((3, 3), np.uint8))
    rim = (dil - sil).astype(bool)
    ys, xs = np.where(sil)
    cx = xs.mean()
    if side == "right":
        rim[:, :int(cx)] = False
    # sodium orange BGR (70,150,255) -> purple BGR (220,90,200)
    c0 = np.array([70.0, 150.0, 255.0])
    c1 = np.array([220.0, 90.0, 200.0])
    col = c0 * (1 - t_purple) + c1 * t_purple
    a = 0.18  # was 0.35 — read as a dirty brown outline around the figure
    canvas_bgr = canvas[:, :, :3].astype(np.float32)
    canvas_bgr[rim] = canvas_bgr[rim] * (1 - a) + col * a
    canvas[:, :, :3] = canvas_bgr.astype(np.uint8)
    return canvas

# --- timeline: keyframes (frame, state). Angles lerp between keys; swaps,
# cape variant, framing and gag params switch at the key frame. Poses are
# sampled on twos: frames 2k-1 and 2k share the pose sampled at 2k-1.
# R = viewer-left / his right = the remote arm. ---
IDLE = {"UpperArm.R": 80, "UpperArm.L": -80}  # arms DOWN at sides (signs flipped 2026-11-22: -80/+80 renders arms UP)
KEYS = [
    # S1 f1-72 WIDE cold open — breathing idle
    (1,   {"framing": "WIDE", "angles": dict(IDLE), "cape": "cape_hang"}),
    (25,  {"framing": "WIDE", "angles": dict(IDLE, Chest=2, Head=-2),
           "root_shift": (0, -3), "cape": "cape_hang"}),
    (49,  {"framing": "WIDE", "angles": dict(IDLE, Head=1),
           "root_shift": (0, 0), "cape": "cape_hang"}),
    (71,  {"framing": "WIDE", "angles": dict(IDLE), "cape": "cape_hang"}),
    # S2 f73-120 MEDIUM hand to remote
    (73,  {"framing": "MEDIUM", "angles": dict(IDLE), "cape": "cape_hang"}),
    (97,  {"framing": "MEDIUM", "angles": {"UpperArm.R": 80, "Forearm.R": -20,
                                            "UpperArm.L": -80},
           "swaps": {"remote_small": True}, "cape": "cape_hang"}),
    (119, {"framing": "MEDIUM", "angles": {"UpperArm.R": 80, "Forearm.R": -20,
                                            "UpperArm.L": -80},
           "swaps": {"remote_small": True}, "cape": "cape_hang"}),
    # S3 f121-168 MEDIUM raise, cape-first
    (121, {"framing": "MEDIUM", "angles": {"UpperArm.R": 80, "Forearm.R": -20,
                                            "UpperArm.L": -80},
           "swaps": {"remote_small": True}, "cape": "cape_hang"}),
    (145, {"framing": "MEDIUM", "angles": {"UpperArm.R": -80, "Forearm.R": -15,
                                            "UpperArm.L": -80},
           "swaps": {"remote_small": True}, "cape": "cape_sweep"}),
    (167, {"framing": "MEDIUM", "angles": {"UpperArm.R": -80, "Forearm.R": -20,
                                            "UpperArm.L": -80},
           "swaps": {"remote_small": True}, "cape": "cape_billow",
           "squash": (0.98, 1.03)}),
    # S4 f169-205 CLOSEUP glove gag: bare hand lifts slowly, click, spark
    (169, {"framing": "CLOSEUP", "gag": {"lift": 90, "press": 0, "spark": 0}}),
    (185, {"framing": "CLOSEUP", "gag": {"lift": 25, "press": 0, "spark": 0}}),
    (193, {"framing": "CLOSEUP", "gag": {"lift": 0, "press": 0, "spark": 0}}),
    (199, {"framing": "CLOSEUP", "gag": {"lift": 0, "press": 8, "spark": 1.0},
           "squash": (1.03, 0.97)}),
    (205, {"framing": "CLOSEUP", "gag": {"lift": 0, "press": 8, "spark": 0.4}}),
    # S5 f206-312 WIDE HERO lighting shift (bg xfade f206-253) + lower
    (207, {"framing": "WIDE", "angles": {"UpperArm.R": -80, "Forearm.R": -15,
                                          "UpperArm.L": -80},
           "swaps": {"remote_small": True}, "cape": "cape_billow"}),
    (231, {"framing": "WIDE", "angles": {"UpperArm.R": -80, "Forearm.R": -15,
                                          "UpperArm.L": -80},
           "swaps": {"remote_small": True}, "cape": "cape_billow"}),
    (253, {"framing": "WIDE", "angles": {"UpperArm.R": -80, "Forearm.R": -15,
                                          "UpperArm.L": -80},
           # BUG E FIX: was cape_settle — but cape_settle's BOX is (0,0,1296,1616),
           # the whole sheet, not a real part; it rendered as a 446px-wide ground
           # drape at f253. Billow is a real part, correctly placed shoulders->feet.
           "swaps": {"remote_small": True}, "cape": "cape_billow"}),
    (279, {"framing": "WIDE", "angles": {"UpperArm.R": -20, "Forearm.R": -10,
                                          "UpperArm.L": -80, "Head": 8},
           "swaps": {"remote_small": True, "mouth_halfsmile": True,
                     "mouth_neutral": False, "eyes_smug_sideeye": True,
                     "eyes_white_default": False}, "cape": "cape_hang"}),
    (311, {"framing": "WIDE", "angles": {"UpperArm.R": 40, "Forearm.R": -10,
                                          "UpperArm.L": -80, "Head": 8},
           "swaps": {"remote_small": True, "mouth_halfsmile": True,
                     "mouth_neutral": False, "eyes_smug_sideeye": True,
                     "eyes_white_default": False}, "cape": "cape_hang"}),
    # S6 f313-379 MEDIUM arm down, satisfied (remote stays in the lowered hand)
    (313, {"framing": "MEDIUM", "angles": {"UpperArm.R": 80, "Forearm.R": -10,
                                            "UpperArm.L": -80, "Head": 8},
           "swaps": {"remote_small": True, "mouth_halfsmile": True,
                     "mouth_neutral": False, "eyes_smug_sideeye": True,
                     "eyes_white_default": False},
           "cape": "cape_hang"}),
    (351, {"framing": "MEDIUM", "angles": {"UpperArm.R": 80, "Forearm.R": -10,
                                            "UpperArm.L": -80, "Head": 6, "Chest": 1},
           "swaps": {"remote_small": True, "mouth_halfsmile": True,
                     "mouth_neutral": False, "eyes_smug_sideeye": True,
                     "eyes_white_default": False},
           "cape": "cape_hang"}),
    (379, {"framing": "MEDIUM", "angles": {"UpperArm.R": 80, "Forearm.R": -10,
                                            "UpperArm.L": -80, "Head": 8},
           "swaps": {"remote_small": True, "mouth_halfsmile": True,
                     "mouth_neutral": False, "eyes_smug_sideeye": True,
                     "eyes_white_default": False},
           "cape": "cape_hang"}),
    # S7 f380-468 MEDIUM CLOSE nod + pupil button
    (381, {"framing": "MEDCLOSE", "angles": {"UpperArm.R": 80, "Forearm.R": -10,
                                              "UpperArm.L": -80, "Head": 8},
           "swaps": {"remote_small": True, "mouth_halfsmile": True,
                     "mouth_neutral": False, "eyes_smug_sideeye": True,
                     "eyes_white_default": False},
           "cape": "cape_hang"}),
    (405, {"framing": "MEDCLOSE", "angles": {"UpperArm.R": 80, "Forearm.R": -10,
                                              "UpperArm.L": -80, "Head": 14, "Chest": 1},
           "swaps": {"remote_small": True, "mouth_halfsmile": True,
                     "mouth_neutral": False, "eyes_smug_sideeye": True,
                     "eyes_white_default": False},
           "cape": "cape_hang", "squash": (1.01, 0.98)}),
    (419, {"framing": "MEDCLOSE", "angles": {"UpperArm.R": 80, "Forearm.R": -10,
                                              "UpperArm.L": -80, "Head": -2},
           "swaps": {"remote_small": True, "mouth_halfsmile": True,
                     "mouth_neutral": False, "eyes_smug_sideeye": True,
                     "eyes_white_default": False},
           "cape": "cape_hang"}),
    (429, {"framing": "MEDCLOSE", "angles": {"UpperArm.R": 80, "Forearm.R": -10,
                                              "UpperArm.L": -80, "Head": 8},
           "swaps": {"remote_small": True, "mouth_halfsmile": True,
                     "mouth_neutral": False, "eyes_smug_sideeye": True,
                     "eyes_white_default": False},
           "cape": "cape_hang"}),
    (431, {"framing": "MEDCLOSE", "angles": {"UpperArm.R": 80, "Forearm.R": -10,
                                              "UpperArm.L": -80, "Head": 8},
           "swaps": {"remote_small": True, "mouth_halfsmile": True,
                     "mouth_neutral": False, "eyes_pupil_center": True,
                     "eyes_white_default": False},
           "cape": "cape_hang"}),
    (441, {"framing": "MEDCLOSE", "angles": {"UpperArm.R": 80, "Forearm.R": -10,
                                              "UpperArm.L": -80, "Head": 8},
           "swaps": {"remote_small": True, "mouth_halfsmile": True,
                     "mouth_neutral": False, "eyes_pupil_audience": True,
                     "eyes_white_default": False},
           "cape": "cape_hang"}),
    (467, {"framing": "MEDCLOSE", "angles": {"UpperArm.R": 80, "Forearm.R": -10,
                                              "UpperArm.L": -80, "Head": 8},
           "swaps": {"remote_small": True, "mouth_halfsmile": True,
                     "mouth_neutral": False, "eyes_pupil_audience": True,
                     "eyes_white_default": False},
           "cape": "cape_hang"}),
]
FRAMINGS = {"WIDE": WIDE, "MEDIUM": MEDIUM, "MEDCLOSE": MEDCLOSE, "CLOSEUP": CLOSEUP}

def lerp(a, b, t):
    return a + (b - a) * t

def state_at(frame):
    """Interpolated pose state at 1-based frame, sampled on twos."""
    f = 1 + 2 * ((frame - 1) // 2)  # quantize to odd frames (twos)
    f = min(f, 468)
    # surrounding keys
    k1 = KEYS[0]
    k2 = KEYS[-1]
    for i, (kf, _) in enumerate(KEYS):
        if kf <= f:
            k1 = KEYS[i]
        if kf >= f:
            k2 = KEYS[i]
            break
    f1, s1 = k1
    f2, s2 = k2
    t = 0.0 if f2 == f1 else (f - f1) / (f2 - f1)
    t = max(0.0, min(1.0, t))
    out = {}
    # angles: lerp across all keys present in either
    a1 = s1.get("angles", {})
    a2 = s2.get("angles", {})
    out["angles"] = {k: lerp(a1.get(k, 0.0), a2.get(k, 0.0), t)
                     for k in set(a1) | set(a2)}
    # root_shift: lerp
    r1 = s1.get("root_shift", (0, 0))
    r2 = s2.get("root_shift", (0, 0))
    out["root_shift"] = (lerp(r1[0], r2[0], t), lerp(r1[1], r2[1], t))
    # discrete: swaps/cape/framing follow the key that STARTED at or before f
    # (the k1 key), except at exact key frames where the new key applies.
    if f == f2 and f2 != f1:
        out["swaps"] = dict(s2.get("swaps", {}))
        out["cape"] = s2.get("cape", "cape_hang")
        out["framing"] = s2.get("framing", "MEDIUM")
    else:
        out["swaps"] = dict(s1.get("swaps", {}))
        out["cape"] = s1.get("cape", "cape_hang")
        out["framing"] = s1.get("framing", "MEDIUM")
    # squash: only at exact key frames that define it
    out["squash"] = s2.get("squash", (1.0, 1.0)) if f == f2 else s1.get("squash", (1.0, 1.0))
    # head turn (CJ-PL-06/07): the head eases into a 3/4 turn during the lower
    # (f253-279) and holds it through the smug/ending beats. The rig has no
    # turned-head part; the turn is a horizontal squash of the Head-driven
    # group (head, eyes, mouth) about the Head pivot — the closest the rig
    # reaches. If it reads as a narrow head instead of a turn, revert to 1.0.
    if f <= 253:
        out["head_sq"] = 1.0
    elif f >= 279:
        out["head_sq"] = 0.88
    else:
        out["head_sq"] = 1.0 - 0.12 * (f - 253) / 26.0
    # gag: lerp lift/press/spark between gag keys
    g1 = s1.get("gag")
    g2 = s2.get("gag")
    if g1 is not None or g2 is not None:
        gg1 = g1 or {"lift": 0, "press": 0, "spark": 0}
        gg2 = g2 or {"lift": 0, "press": 0, "spark": 0}
        out["gag"] = {k: lerp(gg1.get(k, 0), gg2.get(k, 0), t) for k in ("lift", "press", "spark")}
    else:
        out["gag"] = None
    out["_keyframe"] = f1
    return out

def load_bg(name):
    bg = cv2.imread(os.path.join(BGD, name))
    assert bg is not None, f"bg missing {name}"
    return cv2.resize(bg, (W, H))

def bg_at(frame, bgs):
    """Background BGR frame: plates + sodium->purple crossfade f206-253."""
    if frame <= 72:
        return bgs["wide-sodium"]
    if frame <= 205:
        return bgs["medium-sodium"]
    if frame <= 253:
        t = (frame - 206) / 47.0
        return cv2.addWeighted(bgs["wide-sodium"], 1 - t, bgs["wide-purple"], t, 0)
    if frame <= 312:
        return bgs["wide-purple"]
    return bgs["mediumclose-purple"]

def t_purple_at(frame):
    if frame <= 205:
        return 0.0
    if frame <= 253:
        return (frame - 206) / 47.0
    return 1.0

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT_DEFAULT)
    ap.add_argument("--frames", type=int, default=NFRAMES)
    ap.add_argument("--samples", default=os.path.join(WD, "v2/render/samples"))
    args = ap.parse_args()
    nframes = args.frames
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    os.makedirs(args.samples, exist_ok=True)
    bgs = {
        "wide-sodium": load_bg("lot-wide-sodium.png"),
        "wide-purple": load_bg("lot-wide-purple.png"),
        "medium-sodium": load_bg("lot-medium-sodium.png"),
        "mediumclose-purple": load_bg("lot-mediumclose-purple.png"),
    }
    print("backgrounds loaded", flush=True)
    # warm the part cache (all parts the cut uses)
    for nm in list(pc.LAYOUT.keys()):
        if pc.LAYOUT[nm][2] or nm in ("cape_sweep", "cape_billow", "cape_settle",
                                      "remote_small", "hand_bare_gag", "remote_gag",
                                      "eyes_smug_sideeye", "eyes_pupil_center",
                                      "eyes_pupil_audience", "mouth_halfsmile"):
            part(nm)
    print(f"parts cached: {len(_parts)}", flush=True)
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
           "-r", str(FPS), args.out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    # cape sway spring (lag 1-2f, overshoot, settle)
    sway, sway_v = 0.0, 0.0
    prev_chest = 0.0
    prev_armR = 80.0  # IDLE R arm is +80 (arms down) since the 2026-11-22 sign fix
    sample_frames = {1, 24, 48, 72, 73, 96, 119, 121, 144, 167, 169, 185, 199,
                     205, 207, 229, 253, 254, 279, 311, 313, 351, 379, 381, 405,
                     419, 429, 431, 441, 452, 467, 474}
    log = []
    for f in range(1, nframes + 1):
        if f >= 469:
            frame = np.zeros((H, W, 3), dtype=np.uint8)
            proc.stdin.write(frame.tobytes())
            if f in sample_frames:
                try:
                    if not cv2.imwrite(os.path.join(args.samples, f"f{f:04d}.png"), frame):
                        print(f"sample f{f} write returned False (wall?)", flush=True)
                except Exception as e:
                    print(f"sample f{f} write failed ({e})", flush=True)
            continue
        st = state_at(f)
        # spring drive: cape lags body angular velocity
        chest = st["angles"].get("Chest", 0.0)
        armR = st["angles"].get("UpperArm.R", -80.0)
        dchest = chest - prev_chest
        darmR = armR - prev_armR
        prev_chest, prev_armR = chest, armR
        target = max(-12.0, min(12.0, -0.9 * dchest * 2 - 0.12 * darmR))
        sway_v += 0.22 * (target - sway) - 0.30 * sway_v
        sway += sway_v
        st["sway"] = sway
        framing = FRAMINGS[st["framing"]]
        bg = bg_at(f, bgs)
        if st.get("gag") is not None:
            canvas = render_gag(st, cv2.cvtColor(bg, cv2.COLOR_BGR2BGRA))
            frame = cv2.cvtColor(canvas, cv2.COLOR_BGRA2BGR)
        else:
            fig = render_figure(st, framing)
            canvas = cv2.cvtColor(bg, cv2.COLOR_BGR2BGRA)
            paste(canvas, fig, 0, 0)
            canvas = rim_light(canvas, fig, t_purple_at(f))
            frame = cv2.cvtColor(canvas, cv2.COLOR_BGRA2BGR)
        proc.stdin.write(frame.tobytes())
        if f in sample_frames:
            try:
                if not cv2.imwrite(os.path.join(args.samples, f"f{f:04d}.png"), frame):
                    print(f"sample f{f} write returned False (wall?)", flush=True)
            except Exception as e:
                print(f"sample f{f} write failed ({e})", flush=True)
        if f % 48 == 0 or f == 1:
            print(f"frame {f}/{nframes} key={st['_keyframe']} "
                  f"framing={st['framing']} cape={st.get('cape')} sway={sway:.1f}",
                  flush=True)
        log.append({"f": f, "key": st["_keyframe"], "framing": st["framing"],
                    "cape": st.get("cape"), "sway": round(sway, 2),
                    "angles": {k: round(v, 1) for k, v in st["angles"].items()}})
    proc.stdin.close()
    rc = proc.wait()
    print(f"ffmpeg rc={rc}", flush=True)
    assert rc == 0, "ffmpeg failed"
    try:
        with open(os.path.join(WD, "v2/render/pose-log.json"), "w") as fh:
            json.dump(log, fh)
    except Exception as e:
        print(f"pose-log write failed ({e}) — video already encoded", flush=True)
    data = open(args.out, "rb").read()
    print(f"OUT {args.out} {len(data)} B sha256={hashlib.sha256(data).hexdigest()}",
          flush=True)
    print("RENDER DONE", flush=True)

if __name__ == "__main__":
    main()
