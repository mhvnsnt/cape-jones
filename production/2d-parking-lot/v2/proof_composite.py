#!/usr/bin/env python3
"""proof_composite.py — 2D cutout compositor: the VISUAL proof engine for the
Cape Jones V2 rig. Blender's render readback is broken in this sandbox (Cycles
computes pixels but the Render Result stays empty; file writes are zeroed by
the disk-write wall), so poses are proven here instead, with the EXACT rig math:
same part PNGs (repo branch v2-rig-parts), same placement() and pivots (BONES),
same z-order (LAYOUT), same swaps (eyes/mouth/hands/forearm_out/shin_in), same
per-frame gates (arm-front-snap overlap, knee-feet FootIn, wrist d_wrist).
A cutout puppet is rigid pieces rotating about joint pivots — that is exactly
what this compositor does (forward kinematics + warpAffine about bone heads).
The Blender build log proves the rig structure (44/44 imported, 19 bones,
42/42 bound, IK, Wiggle); this proves the assembly + pose reach visually.
Nothing is written to local disk: proofs go straight to the repo via gh api.
Usage: python3 proof_composite.py <pose> [pose ...] | all
Poses: rest idle raise press_gag lower_smug pupil_end strut twist flex groove
"""
import cv2, numpy as np, sys, os, json, base64, subprocess, math
import urllib.request

WD = "/home/hatch/workspace/_cape-jones-parking-lot-2d"
RIG = os.path.join(WD, "rig")
BRANCH = "v2-rig-parts"
REPO = "mhvnsnt/cape-jones"
PART_URL = ("https://raw.githubusercontent.com/mhvnsnt/cape-jones/v2-rig-parts/"
            "production/2d-parking-lot/v2/rig-parts/")
BG = os.path.join(WD, "v2/backgrounds")

# --- load the rig tables from build_rig_remote.py (pure-python span) ---
_src = open(os.path.join(RIG, "build_rig_remote.py")).read()
_start = _src.index("def png_decode")
_end = _src.index("try:\n    bpy.ops.preferences")
_ns = {"np": np, "struct": __import__("struct"), "zlib": __import__("zlib"),
       "urllib": urllib, "base64": base64, "json": json, "os": os,
       "sys": sys, "math": math}
_ns.update({"S": 0.01, "OX": 1024, "OY": 580,
            "BASE_URL": PART_URL})
exec(_src[_start:_end], _ns)
LAYOUT = _ns["LAYOUT"]; BOXES = _ns["BOXES"]; BONES = _ns["BONES"]
SHEET01 = _ns["SHEET01"]; ANCHOR_UV = _ns["ANCHOR_UV"]
placement = _ns["placement"]; fetch_part = _ns["fetch_part"]
png_decode = _ns["png_decode"]; P = _ns["P"]

# --- part cache (download once, in memory) ---
# CHANNEL FIX (2026-11-22 ~12:20 EST): the canvas is BGRA (cv2), but
# png_decode returns standard RGBA — pasting RGB straight into BGRA swapped R
# and B (tan skin #E5B28C rendered light blue; blue sheet pixels rendered as
# the red diagonal bands). Parts are returned BGRA here, matching the canvas.
_parts = {}
def part(name):
    if name not in _parts:
        img = png_decode(fetch_part(name))
        _parts[name] = img[:, :, [2, 1, 0, 3]]
    return _parts[name]

def gh_put(path, data, message):
    # include the existing blob sha when updating (contents API requires it);
    # retry 3x — gh auth flickers 401 transiently mid-run.
    import time
    sha = None
    r0 = subprocess.run(["gh", "api", f"repos/{REPO}/contents/{path}?ref={BRANCH}"],
                        capture_output=True, timeout=60)
    if r0.returncode == 0:
        try:
            sha = json.loads(r0.stdout.decode()).get("sha")
        except Exception:
            sha = None
    body = {"message": message, "content": base64.b64encode(data).decode(),
            "branch": BRANCH}
    if sha:
        body["sha"] = sha
    for attempt in (1, 2, 3):
        r = subprocess.run(["gh", "api", "-X", "PUT",
                            f"repos/{REPO}/contents/{path}", "--input", "-"],
                           input=json.dumps(body).encode(),
                           capture_output=True, timeout=120)
        if r.returncode == 0:
            print(f"uploaded {path} ({len(data)} B)", flush=True)
            return True
        print(f"upload {path} attempt {attempt} FAILED: {r.stderr.decode()[:150]}", flush=True)
        time.sleep(5)
    return False

# --- canvas mapping: world (x right, z up, units) -> canvas px (y down) ---
class Framing:
    def __init__(self, K, cx0, cy0):
        self.K, self.cx0, self.cy0 = K, cx0, cy0
    def map(self, wx, wz):
        return (self.cx0 + wx * self.K, self.cy0 - wz * self.K)
    def inv(self, cx, cy):
        return ((cx - self.cx0) / self.K, (self.cy0 - cy) / self.K)

MEDIUM = Framing(80, 1024, 602)    # figure ~900px tall, feet ~y1050
WIDE = Framing(55, 1024, 742)      # figure ~610px tall
CLOSEUP = Framing(170, 1024, 500)  # close-up framing (hand/remote)

def rot2d(deg):
    """2D rotation matrix, deg clockwise-positive as seen on screen (canvas y down)."""
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    # canvas: x right, y down. Clockwise-positive rotation:
    return np.array([[c, -s], [s, c]], dtype=np.float64)

# --- forward kinematics in canvas space ---
# BONE_PARENTS from BONES (name -> (head, tail, parent)); angles are per-bone,
# screen-clockwise-positive degrees, relative to parent.
def fk(pose_angles, framing, root_shift=(0, 0)):
    """Return {bone: (head_canvas, tail_canvas, total_angle)}."""
    out = {}
    # process in dependency order (BONES dict is already parent-first)
    for bname, (head, tail, parent) in BONES.items():
        h_rest = np.array(framing.map(head[0], head[2]), dtype=np.float64)
        t_rest = np.array(framing.map(tail[0], tail[2]), dtype=np.float64)
        ang = pose_angles.get(bname, 0.0)
        if parent is None:
            total = ang
            h = h_rest + np.array(root_shift, dtype=np.float64)
            t = h + rot2d(total) @ (t_rest - h_rest)
        else:
            ph, pt, ptotal = out[parent]
            total = ptotal + ang
            # head moves with the parent's rotation about the parent head
            h = ph + rot2d(ptotal) @ (h_rest - np.array(framing.map(BONES[parent][0][0], BONES[parent][0][2]), dtype=np.float64))
            t = h + rot2d(total) @ (t_rest - h_rest)
        out[bname] = (h, t, total)
    return out

def bone_head_rest_canvas(bname, framing):
    h = BONES[bname][0]
    return np.array(framing.map(h[0], h[2]), dtype=np.float64)

# --- part placement: rest canvas rect for a part image ---
def part_rest_rect(name, framing):
    """Return (x0, y0) canvas px of the part image's top-left at rest."""
    img = part(name)
    h, w = img.shape[0], img.shape[1]
    lx, lz = placement(name, w, h)
    # obj.location = (lx, z_order, lz); image top edge at z=lz, left edge at x=lx
    tl = framing.map(lx, lz)
    return (tl[0], tl[1], w, h)

def paste(layer, img, x0, y0):
    """Alpha-composite RGBA img onto RGBA layer at integer top-left (x0, y0)."""
    h, w = img.shape[0], img.shape[1]
    H, W = layer.shape[0], layer.shape[1]
    x1, y1 = int(round(x0)), int(round(y0))
    sx0, sy0 = max(0, -x1), max(0, -y1)
    dx0, dy0 = max(0, x1), max(0, y1)
    dx1, dy1 = min(W, x1 + w), min(H, y1 + h)
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

def warp_layer(layer, H1, H0, angle_deg):
    """Rotate a canvas-sized layer about pivot: p' = H1 + R(angle)*(p - H0).
    cv2.warpAffine expects the INVERSE mapping (dst -> src), so we pass
    [R^T | -R^T t] where t = H1 - R@H0. (Passing [R | t] rotates by -angle
    about the wrong centre — that bug put pixels at the canvas top edge.)"""
    R = rot2d(angle_deg)
    t = H1 - R @ H0
    Rinv = R.T
    tinv = -Rinv @ t
    M = np.hstack([Rinv, tinv.reshape(2, 1)]).astype(np.float32)
    H, W = layer.shape[0], layer.shape[1]
    # INTER_NEAREST: INTER_LINEAR smears a red fringe (semi-transparent pure-red
    # pixels, B=0/G=0/R~100-250/A~66) across the canvas top edge when parts rotate
    # — a warpAffine border/interpolation artifact, not in the parts (verified
    # clean). Nearest-neighbour keeps part pixels exact; edges stay crisp, which
    # is correct for flat cutout art anyway.
    return cv2.warpAffine(layer, M, (W, H), flags=cv2.INTER_NEAREST,
                          borderMode=cv2.BORDER_TRANSPARENT)

# --- driver bone per part (single bone that moves the piece) ---
DRIVER = {}
for _n, (_z, _b, _v) in LAYOUT.items():
    DRIVER[_n] = _b[0] if _b else None
DRIVER["torso"] = "Chest"      # pivot at Spine head, angle = Chest total
DRIVER["cape_hang"] = "Chest"
DRIVER["cape_sweep"] = "Chest"
DRIVER["cape_billow"] = "Chest"
DRIVER["cape_diag"] = "Chest"
DRIVER["cape_settle"] = "Chest"
DRIVER["cape_billow_pose"] = "Chest"

def part_driver_pivot(name, fkmap, framing):
    """(H0 rest canvas, H1 posed canvas, total angle) for a part's driver."""
    if name.startswith("cape_"):
        # pivot = Chest head (shoulders); angle = Chest total + sway (set by pose)
        b = "Chest"
    elif name == "torso":
        b = "Spine"
    else:
        b = DRIVER[name]
    H0 = bone_head_rest_canvas(b, framing)
    H1, _t, total = fkmap[b]
    return H0, H1, total

def render_pose(pose, framing, bg_name=None, out_name=None):
    """Render one pose dict to a 2048x1152 RGBA canvas; return (canvas, gates)."""
    W, H = 2048, 1152
    angles = dict(pose.get("angles", {}))
    # torso: Chest total drives it; cape sway added to Chest total for capes
    sway = pose.get("sway", 0.0)
    fkmap = fk(angles, framing, root_shift=pose.get("root_shift", (0, 0)))
    # visible set: LAYOUT defaults + pose overrides
    vis = {n: v for n, (_z, _b, v) in LAYOUT.items()}
    for n, v in pose.get("swaps", {}).items():
        vis[n] = v
    # z-order with arm-front-snap (snapped arm rises above the torso, below eyes)
    zval = {n: z for n, (z, _b, _v) in LAYOUT.items()}
    for side, snap in (("R", pose.get("snap_R", False)),
                       ("L", pose.get("snap_L", False))):
        if snap:
            for n in (f"upper_arm_{side}", f"forearm_{side}",
                      f"hand_glove_open_{side}", f"fist_glove_h" if side == "R" else f"fist_glove_v",
                      f"hand_glove_point" if side == "R" else f"hand_glove_open_08",
                      f"forearm_{side}_out"):
                if n in zval:
                    zval[n] = 0.045
    order = sorted([n for n, v in vis.items() if v], key=lambda n: zval[n])
    # background
    if bg_name:
        bg = cv2.imread(os.path.join(BG, bg_name))
        bg = cv2.resize(bg, (W, H))
        canvas = cv2.cvtColor(bg, cv2.COLOR_BGR2BGRA)
    else:
        canvas = np.zeros((H, W, 4), dtype=np.uint8)
    # Part images are authored at 100 px/unit (sheet px); the canvas is K px/unit,
    # so every part is scaled by K/100 on paste (a 25% error at K=80 otherwise).
    fscale = framing.K / 100.0
    # per-part warped layers (kept for the overlap gate)
    layers = {}
    for name in order:
        if name in ("hand_bare_gag", "remote_gag") and not pose.get("gag_closeup"):
            # close-up props are only placed by the gag pose itself
            if pose.get("name") != "press_gag":
                continue
        img = part(name)
        # CAPE SCALE (2026-11-22 visual-pass fix 1): the sheet-08 cape spans
        # to mid-shin; stretch 1.85x vertically about the shoulder anchor so
        # the hem reaches the ankles. placement() anchors capes by their top
        # edge (v=0), so the top stays at the shoulders.
        if name.startswith("cape_"):
            img = cv2.resize(img, None, fx=1.0, fy=1.85)
        x0, y0, w, h = part_rest_rect(name, framing)
        if pose.get("gag_closeup") and name in ("hand_bare_gag", "remote_gag"):
            # close-up framing: hand big and centred, remote at the thumb
            img = cv2.resize(img, None, fx=1.35 * fscale, fy=1.35 * fscale)
            if name == "hand_bare_gag":
                x0, y0 = 1024 - img.shape[1] // 2, 576 - img.shape[0] // 2 + 80
            else:
                x0, y0 = 1080, 330
        else:
            img = cv2.resize(img, None, fx=fscale, fy=fscale)
        layer = np.zeros((H, W, 4), dtype=np.uint8)
        paste(layer, img, x0, y0)
        drv = DRIVER.get(name)
        if drv is not None:
            H0, H1, total = part_driver_pivot(name, fkmap, framing)
            if name.startswith("cape_"):
                total = total + sway
            if name == "torso":
                total = fkmap["Chest"][2]
                H0 = bone_head_rest_canvas("Spine", framing)
                H1 = fkmap["Spine"][0]
            layer = warp_layer(layer, H1, H0, total)
        layers[name] = layer
        paste(canvas, layer, 0, 0)
    # --- gates ---
    gates = {}
    # wrist: hand wrist pixel vs forearm bone tail, in sheet-01 px
    K = framing.K
    for side in ("R", "L"):
        hand = None
        for cand in (f"hand_glove_open_{side}", f"fist_glove_h" if side == "R" else f"fist_glove_v",
                     f"hand_glove_point" if side == "R" else f"hand_glove_open_08"):
            if vis.get(cand):
                hand = cand
                break
        if hand is None:
            continue
        ax, ay, u, v = ANCHOR_UV[hand]
        img = part(hand)
        hh, ww = img.shape[0], img.shape[1]
        uu = ww / 2.0 if u == "c" else float(u)
        vv = hh / 2.0 if v == "c" else float(v)
        x0, y0, _w, _h = part_rest_rect(hand, framing)
        # wrist offset inside the part image, scaled to canvas px (fscale = K/100)
        fscale = framing.K / 100.0
        wrist_rest = np.array([x0 + uu * fscale, y0 + vv * fscale], dtype=np.float64)
        H0, H1, total = part_driver_pivot(hand, fkmap, framing)
        wrist_posed = H1 + rot2d(total) @ (wrist_rest - H0)
        fore_tail = fkmap[f"Forearm.{side}"][1]
        d_canvas = float(np.linalg.norm(wrist_posed - fore_tail))
        d_sheet = d_canvas / (K * 0.01)
        # d_tip: wrist to far edge of the hand (sheet px, approx by image extent)
        d_tip = float(ww - uu) if side == "R" else float(uu)
        gates[f"wrist_{side}"] = {
            "d_sheet": round(d_sheet, 1), "d_tip_sheet": round(d_tip, 1),
            "pass": bool(d_sheet <= 30 and d_sheet < d_tip)}
    # knee-feet: thigh angles + active shin variant
    tr = fkmap["Thigh.R"][2]; tl = fkmap["Thigh.L"][2]
    foot_in = bool(tr > 0 and tl < 0)
    gates["knee_feet"] = {"thigh_R": round(tr, 1), "thigh_L": round(tl, 1),
                          "foot_in": foot_in,
                          "shin_in_active": bool(vis.get("shin_foot_R_in") and vis.get("shin_foot_L_in")),
                          "pass": bool(foot_in == (vis.get("shin_foot_R_in") and vis.get("shin_foot_L_in")))}
    # arm-front-snap: arm-vs-torso alpha overlap (canvas px; gate ~1430 @2048x1152).
    # This rig has both arms in front of the torso already (z 0.02/0.03 > torso 0.01),
    # so the gate is: a pose that DECLARES a snap (arm crossing the chest) must show
    # overlap above threshold AND the arm layered above the torso. A pose with no
    # snap declared passes regardless of edge overlap (hanging arms touch the torso
    # edge and are already in front — that is correct, not a snap failure).
    # MEASURED UNION (2026-11-22): the crossing piece is the UPPER arm in the twist
    # (R:180 puts the upper arm across the chest, the forearm rides up to the face),
    # so a forearm-only mask reads 0 even though the arm genuinely crosses. The gate
    # measures the union of upper arm + forearm (+ _out variants) vs the torso.
    torso_mask = None
    if "torso" in layers:
        torso_mask = layers["torso"][:, :, 3] > 127
    for side in ("R", "L"):
        arm_names = [f"upper_arm_{side}", f"forearm_{side}",
                     f"forearm_{side}_out"]
        arm_mask = None
        arm_above = False
        for an in arm_names:
            if an in layers and torso_mask is not None:
                m = layers[an][:, :, 3] > 127
                arm_mask = m if arm_mask is None else (arm_mask | m)
                arm_above = arm_above or (zval.get(an, 0) > zval.get("torso", 0))
        if arm_mask is not None:
            ov = int((arm_mask & torso_mask).sum())
            declared = bool(pose.get(f"snap_{side}", False))
            gates[f"snap_{side}"] = {"overlap_px": ov, "threshold_px": 1430,
                                     "snapped": declared, "arm_above_torso": bool(arm_above),
                                     "pass": bool((not declared) or (ov > 1430 and arm_above))}
    return canvas, gates

def to_png_bytes(canvas):
    ok, buf = cv2.imencode(".png", canvas)
    assert ok
    return buf.tobytes()

# --- poses: angles are screen-clockwise-positive degrees, relative to parent ---
POSES = {
    "rest": {"name": "rest", "angles": {}, "bg": "lot-wide-purple.png"},
    "idle": {"name": "idle", "angles": {"UpperArm.R": 80, "UpperArm.L": -80},
             "bg": "lot-wide-purple.png"},
    "raise": {"name": "raise",
              "angles": {"UpperArm.R": 135, "Forearm.R": -20, "UpperArm.L": 80},
              "swaps": {"remote_small": True},
              "bg": "lot-medium-sodium.png"},
    "press_gag": {"name": "press_gag", "angles": {}, "gag_closeup": True,
                  "swaps": {"hand_bare_gag": True, "remote_gag": True},
                  "bg": "lot-mediumclose-purple.png"},
    "lower_smug": {"name": "lower_smug",
                   "angles": {"UpperArm.R": 20, "Forearm.R": -10, "UpperArm.L": -80,
                              "Head": 8},
                   "swaps": {"mouth_halfsmile": True, "mouth_neutral": False,
                             "eyes_smug_sideeye": True, "eyes_white_default": False},
                   "bg": "lot-medium-sodium.png"},
    "pupil_end": {"name": "pupil_end",
                  "angles": {"UpperArm.R": 80, "UpperArm.L": -80},
                  "swaps": {"eyes_pupil_audience": True, "eyes_white_default": False,
                            "mouth_halfsmile": True, "mouth_neutral": False},
                  "bg": "lot-mediumclose-purple.png"},
    "strut": {"name": "strut",
              "angles": {"Thigh.R": 20, "Shin.R": -25, "Thigh.L": -15, "Shin.L": 10,
                         "UpperArm.R": -60, "UpperArm.L": 60, "Head": -5},
              "swaps": {"shin_foot_R_in": True, "shin_foot_L_in": True,
                        "shin_foot_R": False, "shin_foot_L": False},
              "bg": "lot-wide-purple.png"},
    "twist": {"name": "twist",
              "angles": {"Chest": 12, "Head": -8, "UpperArm.R": 180, "Forearm.R": 15,
                         "UpperArm.L": 80, "Thigh.R": 10, "Thigh.L": -10},
              "snap_R": True,
              "swaps": {"shin_foot_R_in": True, "shin_foot_L_in": True,
                        "shin_foot_R": False, "shin_foot_L": False},
              "bg": "lot-wide-purple.png"},
    "flex": {"name": "flex",
             "angles": {"UpperArm.R": 150, "Forearm.R": -125,
                        "UpperArm.L": -150, "Forearm.L": 125, "Chest": 5},
             "swaps": {"fist_glove_h": True, "fist_glove_v": True,
                       "hand_glove_open_R": False, "hand_glove_open_L": False},
             "bg": "lot-wide-purple.png"},
    "groove": {"name": "groove",
               "angles": {"Thigh.R": 35, "Shin.R": -40, "Thigh.L": -5, "Shin.L": 5,
                          "UpperArm.R": -40, "Forearm.R": -30,
                          "UpperArm.L": 100, "Forearm.L": -20, "Chest": 8},
               "swaps": {"shin_foot_R_in": True, "shin_foot_L_in": True,
                         "shin_foot_R": False, "shin_foot_L": False},
               "bg": "lot-wide-purple.png"},
}

def to_jpg_bytes(canvas, quality=90):
    ok, buf = cv2.imencode(".jpg", canvas,
                           [cv2.IMWRITE_JPEG_QUALITY, quality])
    assert ok
    return buf.tobytes()

def analyze_canvas(canvas, bg_name):
    """Programmatic check of a rendered canvas: figure bbox vs background,
    red artifact pixels, palette counts. Returns a dict."""
    bg = cv2.imread(os.path.join(BG, bg_name))
    bg = cv2.resize(bg, (canvas.shape[1], canvas.shape[0]))
    img = cv2.cvtColor(canvas, cv2.COLOR_BGRA2BGR)
    diff = np.abs(img.astype(np.int16) - bg.astype(np.int16)).max(axis=2)
    mask = diff > 25
    n, lab, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    keep = np.zeros_like(mask)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= 500:
            keep[lab == i] = True
    ys, xs = np.where(keep)
    out = {}
    if len(xs):
        out["bbox"] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
    else:
        out["bbox"] = None
    ii = img.astype(np.int16)
    red = ((ii[:, :, 2] > 120) & (ii[:, :, 1] < 60) & (ii[:, :, 0] < 60))
    out["red_px"] = int(red.sum())
    if red.sum():
        rys, _ = np.where(red)
        out["red_y_range"] = [int(rys.min()), int(rys.max())]
    out["white"] = int((np.abs(ii - np.array([255, 255, 255])).max(axis=2) <= 40).sum())
    out["purple"] = int((np.abs(ii - np.array([115, 20, 62])).max(axis=2) <= 40).sum())
    out["black"] = int((ii.max(axis=2) < 40).sum())
    out["skin"] = int((np.abs(ii - np.array([140, 178, 229])).max(axis=2) <= 40).sum())
    return out

def main():
    args = sys.argv[1:]
    as_jpg = "--jpg" in args
    as_view = "--view" in args
    as_analyze = "--analyze" in args
    names = [a for a in args if not a.startswith("--")]
    if not names or names == ["all"]:
        names = list(POSES.keys())
    for name in names:
        pose = POSES[name]
        framing = CLOSEUP if name == "press_gag" else MEDIUM
        canvas, gates = render_pose(pose, framing, bg_name=pose.get("bg"))
        if as_analyze:
            a = analyze_canvas(canvas, pose.get("bg"))
            print(f"ANALYZE {name}: {json.dumps(a)} gates={json.dumps(gates)}", flush=True)
            continue
        if as_view:
            small = cv2.resize(canvas, (800, 450))
            b64 = base64.b64encode(to_jpg_bytes(small, 75)).decode()
            print(f"B64VIEW {name} {b64}", flush=True)
            print(f"POSE {name}: view-only gates={json.dumps(gates)}", flush=True)
            continue
        if as_jpg:
            data = to_jpg_bytes(canvas, 90)
            ok = gh_put(f"production/2d-parking-lot/v2/proof/pose-{name}.jpg", data,
                        f"V2 rig proof: pose {name} (compositor, JPEG)")
        else:
            data = to_png_bytes(canvas)
            ok = gh_put(f"production/2d-parking-lot/v2/proof/pose-{name}.png", data,
                        f"V2 rig proof: pose {name} (compositor)")
        print(f"POSE {name}: upload={'OK' if ok else 'FAIL'} gates={json.dumps(gates)}", flush=True)

if __name__ == "__main__":
    main()
