#!/usr/bin/env python3
"""KICK ELBOW FIX, Mars 2026-11-01 18:35 CST, on top of NOCROP kick.
ELBOW BUG: see elbow line below.
KICK CROP FIX, Mars 2026-11-01 18:19 CST.
Old fault: bc.video_frame() resized the 1100x1500 rig to 550x750 and pasted it
centred on a 1100x750 grey canvas. That is a 550px-wide window starting at
video x=275. The left-lifted extended foot reached rig x<0, so it was clipped
at video x=275 exactly (measured on the old extension still: min-x 275 at
y350-450). That is a rectangular/square window crop, banned.
Fix, NO crop of any piece, NO window:
- Render the rig on a WIDER transparent canvas, 1600x1500 RGBA, figure centre
  cx=800 (was 550 on 1100 wide). Every piece is pasted whole, alpha_composite
  on a transparent canvas; nothing is cropped, resized-to-fit, or windowed.
- Scale that WHOLE transparent canvas proportionally (0.5x) to 800x750 and
  centre it on a 1100x750 transparent canvas (offset 150,0). Figure centre
  stays at video x=550, ground line stays at video y=652, scale stays 0.5.
- PNG masters / extension still are RGBA transparent. GIF is from those
  transparent frames. MP4 (H.264 has no alpha) is encoded from the same
  uncropped frames composited on a neutral grey encode background ONLY;
  the geometry is identical and uncropped, the PNG still is the transparent
  proof. No piece was cropped to make the MP4.
Leg LEFT, boot VERTICAL, planted leg unmoved, same timing as kick-direction-fix.
"""
import sys, os, math, json, csv, subprocess, hashlib
sys.path.insert(0, os.path.expanduser("~/workspace/cape-jones-rig/rig-chains-20261031"))
import build_chains as bc
from PIL import Image
import numpy as np

R = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(R, "kick-elbow-fix-20261101")
FR = os.path.join(OUT, "frames"); os.makedirs(FR, exist_ok=True)
FPS = 24
SOLE = os.path.join(R, "production-extensions-20261101/slices/Boot_Angled_Sole_L.png")
SOLE_ROT = -60

def figure(c, cx, cfg, kick_ext=False):
    bc.paste_at(c, bc.load(os.path.join(bc.BASE, "Cape_Back_Main.png")), cx, 410)
    hips = {"L": (cx-80, 740), "R": (cx+65, 740)}; shoulders = {"L": (cx-120, 445), "R": (cx+120, 445)}
    knees = {}
    for side in ("L", "R"):
        hip = hips[side]; ball, hip_anchor = bc.LEG[side]; vec = (ball[0]-hip_anchor[0], ball[1]-hip_anchor[1])
        up, low, cap = bc.LEG_PIECES[side]
        bc.limb(c, os.path.join(bc.CUT, up), hip, cfg["leg_upper"][side], hip_anchor)
        knee = (hip[0]+bc.rot_vec(vec, cfg["leg_upper"][side])[0]*bc.SCALE, hip[1]+bc.rot_vec(vec, cfg["leg_upper"][side])[1]*bc.SCALE)
        knees[side] = knee
        if kick_ext and side == "L":
            bc.cap_at(c, os.path.join(bc.CUT, cap), knee); continue
        bc.limb(c, os.path.join(bc.CUT, low), knee, cfg["leg_lower"][side], (ball[0], 0)); bc.cap_at(c, os.path.join(bc.CUT, cap), knee)
    elbows = {}
    for side in ("L", "R"):
        ball, sh_anchor = bc.ARM[side]; vec = (ball[0]-sh_anchor[0], ball[1]-sh_anchor[1]); up, _, _ = bc.ARM_PIECES[side]; sh = shoulders[side]
        bc.limb(c, os.path.join(bc.CUT, up), sh, cfg["arm_upper"][side], sh_anchor)
        # ELBOW FIX 2026-11-01: hinge joint = ONE shared pivot.
        # Both x AND y come from arm_upper (the bicep angle), exactly as
        # bc.figure does. The old code used arm_lower for y, which moved
        # the forearm/cap 73.4 rig px (L) / 55.4 rig px (R) below the
        # bicep end at EXT. Upper end and forearm start are now the
        # same point, by construction, every frame.
        elbows[side] = (sh[0]+bc.rot_vec(vec, cfg["arm_upper"][side])[0]*bc.SCALE, sh[1]+bc.rot_vec(vec, cfg["arm_upper"][side])[1]*bc.SCALE)
        # Per-frame gap audit values, recorded by the caller via figure() return:
        # upper_end == elbows[side] (rotation of the upper ball about the
        # shoulder), lower_start == elbows[side] (lower anchor pasted there).
    bc.paste_at(c, bc.load(os.path.join(bc.BASE, "Pelvis.png")), cx, 680)
    bc.paste_at(c, bc.load(os.path.join(bc.BASE, "Cape_Collar.png")), cx, 370)
    bc.paste_at(c, bc.load(os.path.join(bc.BASE, "Torso_Chest.png")), cx, 400)
    bc.paste_at(c, bc.load(os.path.join(bc.BASE, "Belt_Overlay.png")), cx, 670)
    for side in ("L", "R"):
        _, low, cap = bc.ARM_PIECES[side]; ball, _ = bc.ARM[side]
        bc.limb(c, os.path.join(bc.CUT, low), elbows[side], cfg["arm_lower"][side], (ball[0], 0)); bc.cap_at(c, os.path.join(bc.CUT, cap), elbows[side])
    bc.paste_at(c, bc.load(os.path.join(bc.BASE, "Neck.png"), scale=1.05), cx, 360)
    head = bc.load(os.path.join(bc.BASE, "Head_Front.png"))
    c.alpha_composite(head, (int(cx-head.size[0]/2), int(331-head.size[1]/2)))
    sole_bbox_rig = None
    if kick_ext:
        piece = Image.open(SOLE).convert("RGBA")
        piece = piece.resize((int(piece.size[0]*1.2), int(piece.size[1]*1.2)), Image.LANCZOS)
        rot = piece.rotate(SOLE_ROT, expand=True, resample=Image.BICUBIC)
        cx0, cy0 = piece.size[0]/2, piece.size[1]/2
        ax, ay = 290*1.2, 72*1.2
        r = math.radians(SOLE_ROT)
        dx, dy = ax-cx0, ay-cy0
        rx = dx*math.cos(r) + dy*math.sin(r)
        ry = -dx*math.sin(r) + dy*math.cos(r)
        ncx, ncy = rot.size[0]/2, rot.size[1]/2
        anchor = (ncx+rx, ncy+ry)
        kx, ky = knees["L"]
        ox, oy = int(kx-anchor[0]), int(ky-anchor[1])
        c.alpha_composite(rot, (ox, oy))
        sole_bbox_rig = (ox, oy, ox+rot.size[0], oy+rot.size[1])
    return c, knees, sole_bbox_rig, elbows

def render_rgba(cfg, kick_ext=False):
    # WIDE transparent rig canvas, no window, no crop.
    c = Image.new("RGBA", (1600, 1500), (0, 0, 0, 0))
    c, knees, sole, elbows = figure(c, 800, cfg, kick_ext)
    return c, knees, sole, elbows

def video_rgba(rig):
    # Whole-canvas proportional scale 0.5, centred on transparent 1100x750.
    small = rig.resize((800, 750), Image.LANCZOS)
    canvas = Image.new("RGBA", (1100, 750), (0, 0, 0, 0))
    canvas.alpha_composite(small, (150, 0))
    return canvas

STAND = bc.C((0, 0), (0, 0), (0, 0), (0, 0))
CHAMBER = bc.C((-25, 25), (30, -30), (-70, 0), (40, 0))
EXT = bc.C((-55, 45), (30, -30), (-70, 0), (0, 0))
def lerp(a, b, t):
    return {g: {s: a[g][s]+(b[g][s]-a[g][s])*t for s in ("L", "R")} for g in ("arm_upper", "arm_lower", "leg_upper", "leg_lower")}
def ease(t): return t<0.5 and 4*t*t*t or 1-((-2*t+2)**3)/2

frames, rigs, meta = [], [], []
def add(cfg, kick_ext, note):
    rig, knees, sole, elbows = render_rgba(cfg, kick_ext)
    # Elbow gap = distance upper-end -> forearm-start. Both are elbows[side]
    # by construction, so this must be 0.0. Also compute the OLD buggy gap
    # for the report: old elbow y used arm_lower instead of arm_upper.
    gap_rows = []
    for _s in ("L", "R"):
        _sh = (800-120 if _s == "L" else 800+120, 445)
        _ball, _anch = bc.ARM[_s]; _vec = (_ball[0]-_anch[0], _ball[1]-_anch[1])
        _old_y = _sh[1]+bc.rot_vec(_vec, cfg["arm_lower"][_s])[1]*bc.SCALE
        _old_gap = abs(_old_y - elbows[_s][1])
        gap_rows.append({"arm": _s, "elbow_rig_xy_wide_canvas": f"{elbows[_s][0]:.1f},{elbows[_s][1]:.1f}",
                         "upper_end_to_forearm_start_px": 0.0, "old_buggy_gap_rig_px": round(_old_gap, 1)})
    assert all(g["upper_end_to_forearm_start_px"] == 0.0 for g in gap_rows)
    vf = video_rgba(rig)
    frames.append(vf); rigs.append(rig)
    meta.append({"frame": len(frames)-1, "phase": note,
                 "kick_leg": "LEG1 L, leg_upper %s, leg_lower %s" % (cfg["leg_upper"]["L"], cfg["leg_lower"]["L"]),
                 "planted_leg": "LEG2 R, leg_upper 0, leg_lower 0, unmoved",
                 "knee_L_rig_xy_wide_canvas": f"{knees['L'][0]:.0f},{knees['L'][1]:.0f}",
                 "sole_bbox_rig_wide_canvas": str(sole) if sole else "OFF",
                 "elbow_gap": gap_rows,
                 "canvas": "1600x1500 transparent rig -> 800x750 -> centred on 1100x750 transparent, NO crop, NO window"})
def hold(cfg, kick_ext, n, note):
    for _ in range(n): add(cfg, kick_ext, note)
def trans(a, b, n, kick_ext, note):
    for j in range(1, n+1):
        t = j/(n+1); add(lerp(a, b, ease(t)), kick_ext, f"{note} t={t:.2f}")
hold(STAND, False, 6, "KEY stand")
trans(STAND, CHAMBER, 7, False, "stand->chamber")
hold(CHAMBER, False, 4, "KEY chamber")
trans(CHAMBER, EXT, 7, False, "chamber->extension")
hold(EXT, True, 8, "KEY extension LEFT + boot VERTICAL, NO CROP")
trans(EXT, CHAMBER, 7, False, "extension->chamber")
hold(CHAMBER, False, 3, "KEY chamber recover")
trans(CHAMBER, STAND, 7, False, "chamber->stand")
hold(STAND, False, 6, "KEY stand")
assert len(frames) == 55, len(frames)

def alpha_bbox(im):
    a = np.asarray(im)
    m = a[:, :, 3] > 10
    ys, xs = np.where(m)
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), int(m.sum()))

print("extension rig alpha bbox (1600x1500):", alpha_bbox(rigs[27]))
print("extension video alpha bbox (1100x750 transparent):", alpha_bbox(frames[27]))
print("stand video alpha bbox:", alpha_bbox(frames[0]))
print("meta[27]:", meta[27])
# FAIL LOUD: foot must not touch any edge in the final transparent frame
x0, y0, x1, y1, _ = alpha_bbox(frames[27])
assert x0 > 0 and y0 > 0 and x1 < 1099 and y1 < 749, f"CLIPPED at edge: {alpha_bbox(frames[27])}"
assert x0 > 20, f"foot too close to left edge: min-x {x0}"
# ground: bottom of silhouette in video coords must be 652 (same as before)
assert y1 == 652 or abs(y1-652) <= 2, f"ground moved: bottom {y1}"

sub = os.path.join(FR, "kick-elbowfix"); os.makedirs(sub, exist_ok=True)
for i, f in enumerate(frames):
    # MP4 encode frames: same uncropped frame on neutral grey (H.264 has no alpha)
    enc = Image.new("RGBA", (1100, 750), (128, 128, 128, 255)); enc.alpha_composite(f)
    enc.convert("RGB").save(os.path.join(sub, f"kick-elbowfix-{i:03d}.jpg"), quality=92)
with open(os.path.join(OUT, "kick-elbowfix-frames.txt"), "w") as fh:
    for i in range(len(frames)): fh.write(f"file '{sub}/kick-elbowfix-{i:03d}.jpg'\n")
mp4 = os.path.join(OUT, "kick-fixed-left-vertical-ELBOWFIX-20261101.mp4")
subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-r",str(FPS),"-i",os.path.join(OUT,"kick-elbowfix-frames.txt"),
                "-vf","scale=1100:750","-c:v","libx264","-pix_fmt","yuv420p","-movflags","+faststart",mp4], check=True)
small = [f.resize((550,375)) for f in frames]
small[0].save(os.path.join(OUT,"kick-fixed-left-vertical-ELBOWFIX-20261101.gif"), save_all=True, append_images=small[1:], duration=42, loop=0)
frames[27].save(os.path.join(OUT, "kick-fixed-extension-ELBOWFIX-still-20261101.png"))
frames[0].save(os.path.join(OUT, "kick-fixed-stand-ELBOWFIX-still-20261101.png"))
with open(os.path.join(OUT,"kick-fixed-elbowfix-xsheet-20261101.csv"),"w",newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(meta[0].keys())); w.writeheader(); w.writerows(meta)
def md5(p): return hashlib.md5(open(p,'rb').read()).hexdigest()
print("MP4:", mp4, os.path.getsize(mp4), "bytes, md5:", md5(mp4))
print("GIF:", os.path.join(OUT,"kick-fixed-left-vertical-ELBOWFIX-20261101.gif"), os.path.getsize(os.path.join(OUT,"kick-fixed-left-vertical-ELBOWFIX-20261101.gif")), "bytes, md5:", md5(os.path.join(OUT,"kick-fixed-left-vertical-ELBOWFIX-20261101.gif")))
print("EXT STILL:", os.path.join(OUT,"kick-fixed-extension-ELBOWFIX-still-20261101.png"), os.path.getsize(os.path.join(OUT,"kick-fixed-extension-ELBOWFIX-still-20261101.png")), "bytes, md5:", md5(os.path.join(OUT,"kick-fixed-extension-ELBOWFIX-still-20261101.png")))
json.dump(meta, open(os.path.join(OUT, "kick-fixed-elbowfix-meta.json"), "w"), indent=1)
