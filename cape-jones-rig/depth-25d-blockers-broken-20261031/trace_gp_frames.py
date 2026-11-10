"""Trace Cape v7c pieces into Grease Pencil stroke polylines, per pose frame.
EXPERIMENTAL. Method: cv2 largest external contour per source piece, approxPolyDP,
then the SAME joint/anchor/rotation math as snap_figure.py (v7c ball-centre pivots).
Output: gp_frames.json  {frame_no: {layer_name: [[[x_bl,y_bl],...], ...]}}
Blender units: x=(px-550)/100, y=(750-py)/100. No new art: every point comes from
an existing source piece's alpha contour. Strokes are OUTLINES only (no fill) —
that is the honest limit of this GP pass; filled GP art is a later pass.
Run with the cv2 venv: /tmp/cvvenv/bin/python trace_gp_frames.py
"""
import json, math, os, sys
sys.path.insert(0, "/tmp/cvvenv/lib/python3.12/site-packages")
import cv2, numpy as np

RIG = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(RIG, "depth-25d-blockers-broken-20261031")
BASE = os.path.join(RIG, "sliced"); CUT = os.path.join(RIG, "cut-limbs-v7c")
SCALE = 0.95
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
LEG = {"L": ((95, 314), (77, 40)), "R": ((100, 314), (84, 40))}
ARM_PIECES = {"L": ("Arm_Front_Upper.png", "Arm_Front_Lower.png", "Arm_Front_Cap.png"),
              "R": ("Arm_Back_Upper.png", "Arm_Back_Lower.png", "Arm_Back_Cap.png")}
LEG_PIECES = {"L": ("Leg_Front_Upper.png", "Leg_Front_Lower.png", "Leg_Front_Cap.png"),
              "R": ("Leg_Back_Upper.png", "Leg_Back_Lower.png", "Leg_Back_Cap.png")}

def contour(path, max_pts=140):
    import PIL.Image as P
    im = np.array(P.open(path).convert("RGBA"))
    alpha = (im[:, :, 3] > 10).astype(np.uint8) * 255
    cnts, _ = cv2.findContours(alpha, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        return []
    c = max(cnts, key=cv2.contourArea)
    approx = cv2.approxPolyDP(c, 2.5, True).reshape(-1, 2)
    pts = [(float(x), float(y)) for x, y in approx]
    if len(pts) > max_pts:
        step = len(pts) / max_pts
        pts = [pts[int(i * step)] for i in range(max_pts)]
    return pts

_cache = {}
def C(path):
    if path not in _cache:
        _cache[path] = contour(path)
    return _cache[path]

def rot(v, a_deg):
    r = math.radians(a_deg); x, y = v
    return (x * math.cos(r) + y * math.sin(r), -x * math.sin(r) + y * math.cos(r))

def to_bl(p):
    return [round((p[0] - 550) / 100, 4), round((750 - p[1]) / 100, 4)]

def xform(pts, joint, angle, anchor, scale=SCALE):
    ax, ay = anchor[0] * scale, anchor[1] * scale
    out = []
    for (x, y) in pts:
        vx, vy = x * scale - ax, y * scale - ay
        rx, ry = rot((vx, vy), angle)
        out.append(to_bl((joint[0] + rx, joint[1] + ry)))
    out.append(out[0])  # close the stroke
    return out

def paste(pts, cx, top, scale=SCALE):
    # piece image size needed for centring: recover from contour bounds is wrong;
    # use actual image size via PIL
    from PIL import Image as P
    return pts  # placeholder, replaced below

from PIL import Image as P
def paste_pts(path, pts, cx, top, scale=SCALE, rot_deg=0, rot_centre=None):
    w, h = P.open(path).size
    w, h = w * scale, h * scale
    out = []
    for (x, y) in pts:
        px, py = cx - w / 2 + x * scale, top + y * scale
        if rot_deg and rot_centre:
            rx, ry = rot((px - rot_centre[0], py - rot_centre[1]), rot_deg)
            px, py = rot_centre[0] + rx, rot_centre[1] + ry
        out.append(to_bl((px, py)))
    out.append(out[0])
    return out

def build_frame(cx, cfg, head_angle=0, snap=None, dip=0):
    snap = snap or {}
    layers = {n: [] for n in ["FaceSnapArm", "Head", "CowlUpperArm", "Neck", "ChestSnapArm",
                              "Torso", "Collar", "NormalArm", "Legs", "CapeBack"]}
    def add(layer, poly):
        if len(poly) >= 3:
            layers[layer].append(poly)
    # Cape back
    p = os.path.join(BASE, "Cape_Back_Main.png")
    add("CapeBack", paste_pts(p, C(p), cx, 410 + dip))
    # Legs
    hips = {"L": (cx - 80, 740 + dip), "R": (cx + 65, 740 + dip)}
    for side in ("L", "R"):
        hip = hips[side]; ball, hip_anchor = LEG[side]
        vec = (ball[0] - hip_anchor[0], ball[1] - hip_anchor[1])
        up, low, cap = LEG_PIECES[side]
        pu = os.path.join(CUT, up); pl = os.path.join(CUT, low); pc = os.path.join(CUT, cap)
        add("Legs", xform(C(pu), hip, cfg["leg_upper"][side], hip_anchor))
        knee = (hip[0] + rot(vec, cfg["leg_upper"][side])[0] * SCALE,
                hip[1] + rot(vec, cfg["leg_upper"][side])[1] * SCALE)
        add("Legs", xform(C(pl), knee, cfg["leg_lower"][side], (ball[0], 0)))
        # cap: centre at knee
        cw, ch = P.open(pc).size
        add("Legs", paste_pts(pc, C(pc), knee[0] + cw * SCALE / 2, knee[1] - ch * SCALE / 2))
    # Arm uppers (snap-aware placement into layers, like snap_figure)
    shoulders = {"L": (cx - 120, 445 + dip), "R": (cx + 120, 445 + dip)}
    elbows = {}
    for side in ("L", "R"):
        ball, sh_anchor = ARM[side]
        vec = (ball[0] - sh_anchor[0], ball[1] - sh_anchor[1])
        up, _, _ = ARM_PIECES[side]; sh = shoulders[side]
        elbows[side] = (sh[0] + rot(vec, cfg["arm_upper"][side])[0] * SCALE,
                        sh[1] + rot(vec, cfg["arm_upper"][side])[1] * SCALE)
        s = snap.get(side, "normal")
        layer = {"face": "FaceSnapArm", "cowl": "CowlUpperArm", "chest": "ChestSnapArm"}.get(s, "NormalArm")
        if s != "face":
            # face uppers are drawn in face pass (after head) — same geometry, different layer
            add(layer, xform(C(os.path.join(CUT, up)), sh, cfg["arm_upper"][side], sh_anchor))
        else:
            add("FaceSnapArm", xform(C(os.path.join(CUT, up)), sh, cfg["arm_upper"][side], sh_anchor))
    # Torso stack
    for name, top, layer in [("Pelvis.png", 680 + dip, "Torso"), ("Cape_Collar.png", 370 + dip, "Collar"),
                             ("Torso_Chest.png", 400 + dip, "Torso"), ("Belt_Overlay.png", 670 + dip, "Torso")]:
        p = os.path.join(BASE, name); add(layer, paste_pts(p, C(p), cx, top))
    # Arm lowers + caps (face lowers go to FaceSnapArm, others NormalArm unless chest)
    for side in ("L", "R"):
        s = snap.get(side, "normal")
        _, low, cap = ARM_PIECES[side]; ball, _ = ARM[side]
        layer = {"face": "FaceSnapArm", "chest": "ChestSnapArm"}.get(s, "NormalArm")
        add(layer, xform(C(os.path.join(CUT, low)), elbows[side], cfg["arm_lower"][side], (ball[0], 0)))
        pc = os.path.join(CUT, cap); cw, ch = P.open(pc).size
        add(layer, paste_pts(pc, C(pc), elbows[side][0] + cw * SCALE / 2, elbows[side][1] - ch * SCALE / 2))
    # Neck + Head
    p = os.path.join(BASE, "Neck.png"); add("Neck", paste_pts(p, C(p), cx, 360 + dip, scale=1.05))
    p = os.path.join(BASE, "Head_Front.png")
    w, h = P.open(p).size; w, h = w * SCALE, h * SCALE
    add("Head", paste_pts(p, C(p), cx, 331 + dip - h / 2, rot_deg=head_angle, rot_centre=(cx, 331 + dip)))
    return layers

APOSE = {"arm_upper": {"L": 0, "R": 0}, "arm_lower": {"L": 0, "R": 0},
         "leg_upper": {"L": 0, "R": 0}, "leg_lower": {"L": 0, "R": 0}}
TRUE_FINAL = {"arm_upper": {"L": -85, "R": 85}, "arm_lower": {"L": 145, "R": -145},
              "leg_upper": {"L": -22, "R": 22}, "leg_lower": {"L": 10, "R": -10}}
JOJO03 = {"arm_upper": {"L": -25, "R": -88}, "arm_lower": {"L": 35, "R": 145},
          "leg_upper": {"L": -42, "R": 12}, "leg_lower": {"L": 32, "R": -6}}

def interp(a, b, t):
    out = {}
    for k in a:
        out[k] = {s: a[k][s] + (b[k][s] - a[k][s]) * t for s in ("L", "R")}
    return out

frames = {}
frames["1"] = build_frame(550, APOSE)
frames["2"] = build_frame(550, interp(APOSE, TRUE_FINAL, 0.5), dip=14)
frames["3"] = build_frame(550, TRUE_FINAL, dip=28)
frames["4"] = build_frame(550, TRUE_FINAL, dip=28)
frames["10"] = build_frame(550, JOJO03, head_angle=8, snap={"R": "face"})
with open(os.path.join(OUT, "gp_frames.json"), "w") as f:
    json.dump(frames, f)
for k, v in frames.items():
    print(k, {layer: len(polys) for layer, polys in v.items() if polys})
print("wrote gp_frames.json")
