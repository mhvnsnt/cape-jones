"""Rig-angle movement chains + rig successors, 2026-10-31 (Workstream 6).
Method (same v7c ball-centre pivot math as movements-interp-v2 build_interp_v2.py
and ginyu-force build_ginyu_force.py): EVERY frame is a fresh rig render from
interpolated joint angles. NO whole-picture blending, NO crossfade anywhere.
Easing easeInOutCubic (slow-in/slow-out). TWO labelled breakdowns per
transition: arc bulge +10deg on the largest-moving arm upper at j=3, and
follow-through +8deg on that arm's lower at j=5. Overshoot 5% beyond the last
key then settle, before the return. AIRBORNE height = whole-rig translation
of a SINGLE rig render (dy, rig px; video px = dy/2) -- never a blend of two
pictures. GROUNDED chains: dy=0 every frame, feet anchored on the video
ground line (apose feet bottom y=652 in the 1100x750 video frame).
Jump-to-shimmy is NOT built here: BLOCKED on Mars (see REPORT).
No existing file is overwritten; all outputs are in this folder.
"""
from PIL import Image, ImageDraw
import os, math, json, subprocess, csv
R = "/home/hatch/workspace/cape-jones-rig"
BASE = os.path.join(R, "sliced"); CUT = os.path.join(R, "cut-limbs-v7c")
OUT = os.path.join(R, "rig-chains-20261031")
FR = os.path.join(OUT, "frames"); os.makedirs(FR, exist_ok=True)
SCALE = 0.95
ARM = {"L": ((60, 222), (76, 30)), "R": ((99, 222), (76, 30))}
LEG = {"L": ((95, 314), (77, 40)), "R": ((100, 314), (84, 40))}
LEG_PIECES = {"L": ("Leg_Front_Upper.png", "Leg_Front_Lower.png", "Leg_Front_Cap.png"),
              "R": ("Leg_Back_Upper.png", "Leg_Back_Lower.png", "Leg_Back_Cap.png")}
ARM_PIECES = {"L": ("Arm_Front_Upper.png", "Arm_Front_Lower.png", "Arm_Front_Cap.png"),
              "R": ("Arm_Back_Upper.png", "Arm_Back_Lower.png", "Arm_Back_Cap.png")}
_cache = {}
def load(p, scale=SCALE):
    if p not in _cache:
        im = Image.open(p).convert("RGBA")
        _cache[p] = im.resize((max(1, int(im.size[0]*scale)), max(1, int(im.size[1]*scale))), Image.LANCZOS)
    return _cache[p]
def paste_at(c, im, cx, top): c.alpha_composite(im, (int(cx-im.size[0]/2), int(top)))
def limb(c, path, joint, angle, anchor):
    im = load(path); ax, ay = anchor[0]*SCALE, anchor[1]*SCALE
    layer = Image.new("RGBA", c.size, (0, 0, 0, 0))
    layer.alpha_composite(im, (int(joint[0]-ax), int(joint[1]-ay)))
    layer = layer.rotate(angle, center=joint, expand=False); c.alpha_composite(layer)
def cap_at(c, path, joint):
    im = load(path); c.alpha_composite(im, (int(joint[0]-im.size[0]/2), int(joint[1]-im.size[1]/2)))
def rot_vec(v, a):
    r = math.radians(a); x, y = v
    return (x*math.cos(r)+y*math.sin(r), -x*math.sin(r)+y*math.cos(r))
def figure(c, cx, cfg, head_angle=0, top_arms=()):
    paste_at(c, load(os.path.join(BASE, "Cape_Back_Main.png")), cx, 410)
    hips = {"L": (cx-80, 740), "R": (cx+65, 740)}; shoulders = {"L": (cx-120, 445), "R": (cx+120, 445)}
    for side in ("L", "R"):
        hip = hips[side]; ball, hip_anchor = LEG[side]; vec = (ball[0]-hip_anchor[0], ball[1]-hip_anchor[1])
        up, low, cap = LEG_PIECES[side]
        limb(c, os.path.join(CUT, up), hip, cfg["leg_upper"][side], hip_anchor)
        knee = (hip[0]+rot_vec(vec, cfg["leg_upper"][side])[0]*SCALE, hip[1]+rot_vec(vec, cfg["leg_upper"][side])[1]*SCALE)
        limb(c, os.path.join(CUT, low), knee, cfg["leg_lower"][side], (ball[0], 0)); cap_at(c, os.path.join(CUT, cap), knee)
    elbows = {}
    for side in ("L", "R"):
        if side in top_arms: continue
        ball, sh_anchor = ARM[side]; vec = (ball[0]-sh_anchor[0], ball[1]-sh_anchor[1]); up, _, _ = ARM_PIECES[side]; sh = shoulders[side]
        limb(c, os.path.join(CUT, up), sh, cfg["arm_upper"][side], sh_anchor)
        elbows[side] = (sh[0]+rot_vec(vec, cfg["arm_upper"][side])[0]*SCALE, sh[1]+rot_vec(vec, cfg["arm_upper"][side])[1]*SCALE)
    paste_at(c, load(os.path.join(BASE, "Pelvis.png")), cx, 680); paste_at(c, load(os.path.join(BASE, "Cape_Collar.png")), cx, 370)
    paste_at(c, load(os.path.join(BASE, "Torso_Chest.png")), cx, 400); paste_at(c, load(os.path.join(BASE, "Belt_Overlay.png")), cx, 670)
    for side in ("L", "R"):
        if side in top_arms: continue
        _, low, cap = ARM_PIECES[side]; ball, _ = ARM[side]
        limb(c, os.path.join(CUT, low), elbows[side], cfg["arm_lower"][side], (ball[0], 0)); cap_at(c, os.path.join(CUT, cap), elbows[side])
    paste_at(c, load(os.path.join(BASE, "Neck.png"), scale=1.05), cx, 360)
    head = load(os.path.join(BASE, "Head_Front.png"))
    if head_angle: head = head.rotate(head_angle, expand=True)
    c.alpha_composite(head, (int(cx-head.size[0]/2), int(331-head.size[1]/2)))
    for side in ("L", "R"):
        if side not in top_arms: continue
        ball, sh_anchor = ARM[side]; vec = (ball[0]-sh_anchor[0], ball[1]-sh_anchor[1]); up, low, cap = ARM_PIECES[side]; sh = shoulders[side]
        limb(c, os.path.join(CUT, up), sh, cfg["arm_upper"][side], sh_anchor)
        elbow = (sh[0]+rot_vec(vec, cfg["arm_upper"][side])[0]*SCALE, sh[1]+rot_vec(vec, cfg["arm_upper"][side])[1]*SCALE)
        limb(c, os.path.join(CUT, low), elbow, cfg["arm_lower"][side], (ball[0], 0)); cap_at(c, os.path.join(CUT, cap), elbow)
    return c
def render(cfg, head=0, top=(), dx=0, dy=0):
    c = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0)); figure(c, 550, cfg, head, top)
    if dx or dy:
        d = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0)); d.alpha_composite(c, (dx, dy)); return d
    return c
def video_frame(rgba):
    im = rgba.resize((550, 750), Image.LANCZOS)
    canvas = Image.new("RGBA", (1100, 750), (128, 128, 128, 255)); canvas.alpha_composite(im, ((1100-550)//2, 0)); return canvas.convert("RGB")
def C(au, al, lu, ll):
    return {"arm_upper": {"L": au[0], "R": au[1]}, "arm_lower": {"L": al[0], "R": al[1]},
            "leg_upper": {"L": lu[0], "R": lu[1]}, "leg_lower": {"L": ll[0], "R": ll[1]}}
def lerp_cfg(a, b, t):
    return {g: {s: a[g][s]+(b[g][s]-a[g][s])*t for s in ("L", "R")} for g in ("arm_upper", "arm_lower", "leg_upper", "leg_lower")}
def ease(t): return t*t*t*(t*(t*6-15)+10) if False else (t*t*(3-2*t) if False else (t<0.5 and 4*t*t*t or 1-((-2*t+2)**3)/2))
# easeInOutCubic above (smoothstep fallback avoided; cubic branch is the one used)
def K(name, cfg, head=0, top=(), dy=0, dx=0, hold=5, src=""):
    return {"name": name, "cfg": cfg, "head": head, "top": top, "dy": dy, "dx": dx, "hold": hold, "src": src,
            "target_h": -dy//2}  # designed height above ground, video px; dy is recomputed per build
APOSE = K("apose", C((0, 0), (0, 0), (0, 0), (0, 0)), 0, (), 0, 0, 3, "v2 builder exact")
EXACT = "Ginyu builder exact"; EST = "MEASURED-ESTIMATE +/-15deg (labelled, not builder-exact)"
GROUND_Y = 652  # video-frame ground line: apose silhouette bottom, measured
def measure_bottom(cfg, head, top):
    import numpy as np
    vf = video_frame(render(cfg, head, top, 0, 0))
    a = np.asarray(vf.convert("RGB")).astype(int)
    sil = (np.abs(a-128).sum(axis=2) > 40)
    ys, _ = np.where(sil)
    return int(ys.max())
def build(name, keys, n_inb=7, label="", flight=""):
    """keys: ordered list; first key is the start (held), last key is the final
    key (held + overshoot + settle), then return to keys[0] (apose for most
    chains; for walk the list itself ends back at CONTACT-A so return is skipped).
    HIP-DROP COMPENSATION (added after the jump test showed crouch bottom 598
    vs ground 652 with fixed hips): each key's dy is recomputed so its
    silhouette bottom sits at GROUND_Y minus its designed height. Grounded
    keys (height 0) therefore plant on the ground line instead of floating
    when their legs bend; airborne keys sit at their stated height, measured
    from the silhouette bottom, not from the nominal dy. Single-rig-render
    translation only, no blending."""
    for k in keys:
        target_h = k.get("target_h", -k["dy"]//2)
        bottom0 = measure_bottom(k["cfg"], k["head"], k["top"])
        k["dy"] = 2*((GROUND_Y-target_h)-bottom0)
        k["height_video_px"] = target_h
    frames = []; meta = []; masters = []
    cycle = keys[-1]["name"] == keys[0]["name"] and len(keys) > 1
    def add_frame(cfg, head, top, dx, dy, note, frm, to, t, e, height=None):
        masters.append(render(cfg, head, top, dx, dy))
        frames.append(video_frame(masters[-1]))
        meta.append({"frame": len(frames)-1, "kind": note, "from": frm, "to": to, "t": round(t, 2),
                     "eased": round(e, 2), "dy_rig": dy, "dx_rig": dx,
                     "height_video_px": height if height is not None else -dy//2, "label": label})
    def transition(a, b):
        deltas = {s: abs(b["cfg"]["arm_upper"][s]-a["cfg"]["arm_upper"][s]) for s in ("L", "R")}
        big = max(deltas, key=deltas.get)
        for j in range(1, n_inb+1):
            t = j/(n_inb+1); e = ease(t); cfg = lerp_cfg(a["cfg"], b["cfg"], e)
            head = a["head"]+(b["head"]-a["head"])*e
            top = tuple(sorted(set(a["top"]) | set(b["top"])))
            dx = int(a["dx"]+(b["dx"]-a["dx"])*e); dy = int(a["dy"]+(b["dy"]-a["dy"])*e); tag = "inbetween"
            if j == 3:
                cfg["arm_upper"][big] += 10 if b["cfg"]["arm_upper"][big] >= a["cfg"]["arm_upper"][big] else -10
                tag = "BREAKDOWN arc +10deg largest-moving arm upper"
            if j == 5:
                cfg["arm_lower"][big] += 8 if b["cfg"]["arm_lower"][big] >= a["cfg"]["arm_lower"][big] else -8
                tag = "BREAKDOWN follow-through +8deg that arm lower"
            h = a.get("height_video_px", 0)+(b.get("height_video_px", 0)-a.get("height_video_px", 0))*e
            add_frame(cfg, head, top, dx, dy, tag, a["name"], b["name"], t, e, height=int(round(h)))
    def hold(k, note="KEY hold"):
        for _ in range(k["hold"]):
            add_frame(k["cfg"], k["head"], k["top"], k["dx"], k["dy"], note, k["name"], k["name"], 0, 0, height=k.get("height_video_px", 0))
    hold(keys[0])
    for i in range(len(keys)-1):
        transition(keys[i], keys[i+1]); hold(keys[i+1])
    if not cycle:
        # overshoot 5% beyond last key away from previous key, then settle
        prev, last = keys[-2], keys[-1]
        # Arm-only overshoot: legs stay at the last key so planted feet do not
        # dip below the ground line (a whole-cfg 1.05 overshoot pushed sampled
        # bottoms to 670 vs ground 652 in the first build).
        over = {g: dict(last["cfg"][g]) for g in last["cfg"]}
        for g in ("arm_upper", "arm_lower"):
            for side in ("L", "R"):
                over[g][side] = prev["cfg"][g][side] + (last["cfg"][g][side]-prev["cfg"][g][side])*1.05
        add_frame(over, last["head"], last["top"], last["dx"], last["dy"], "OVERSHOOT 5% beyond key", prev["name"], last["name"], 1.05, 1.05, height=last.get("height_video_px", 0))
        add_frame(last["cfg"], last["head"], last["top"], last["dx"], last["dy"], "SETTLE back to key", last["name"], last["name"], 1.0, 1.0, height=last.get("height_video_px", 0))
        transition(last, keys[0]); hold(keys[0])
    return frames, meta, masters

def save_video(name, frames, meta, masters, ground_y=652):
    sub = os.path.join(FR, name); os.makedirs(sub, exist_ok=True)
    for i, f in enumerate(frames): f.save(os.path.join(sub, f"{name}-{i:03d}.jpg"), quality=92)
    for i, m in enumerate(masters):
        # master PNGs: only key + breakdown frames, to keep disk sane
        if meta[i]["kind"] in ("KEY hold",) and i % 5 == 0: pass
    small = [f.resize((550, 375)) for f in frames]
    small[0].save(os.path.join(OUT, f"{name}-20261031.gif"), save_all=True, append_images=small[1:], duration=42, loop=0)
    with open(os.path.join(OUT, f"{name}-frames.txt"), "w") as fh:
        for i in range(len(frames)): fh.write(f"file '{sub}/{name}-{i:03d}.jpg'\n")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-r", "24",
                    "-i", os.path.join(OUT, f"{name}-frames.txt"), "-vf", "scale=1100:750",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", os.path.join(OUT, f"{name}-20261031.mp4")], check=True)
    with open(os.path.join(OUT, f"{name}-xsheet-20261031.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(meta[0].keys())); w.writeheader(); w.writerows(meta)
    # contact: 10 tiles, ground line drawn at ground_y (video coords) on tiles only
    idx = sorted(set([int(i*(len(frames)-1)/9) for i in range(10)]))
    sheet = Image.new("RGB", (1100, 470), (128, 128, 128)); d = ImageDraw.Draw(sheet)
    for k, ix in enumerate(idx):
        tile = frames[ix].resize((220, 150)); x, y = (k % 5)*220, (k // 5)*235
        sheet.paste(tile, (x, y)); d.line([(x, y+int(ground_y*150/750)), (x+220, y+int(ground_y*150/750))], fill=(255, 0, 0), width=2)
        d.text((x+4, y+152), f"f{ix:03d} {meta[ix]['kind'][:28]}", fill=(255, 255, 255))
        d.text((x+4, y+168), f"h={meta[ix]['height_video_px']}px {meta[ix]['label']}", fill=(255, 255, 0))
    sheet.save(os.path.join(OUT, f"{name}-contact-20261031.png"))
    print(name, len(frames), "frames", f"{len(frames)/24:.2f}s", flush=True)
    return len(frames)

# ---- key configs ----
# Punch chain (GROUNDED, CJ-01..05) -- punch/fight measured-estimates as in v2
PUNCH_KEYS = [APOSE,
    K("punch windup", C((-40, 40), (60, -60), (-20, 20), (10, -10)), -5, (), 0, 0, 5, EST),
    K("punch extend/snap", C((-160, 20), (0, -110), (-20, 20), (10, -10)), 0, (), 0, 0, 5, EST),
    K("punch impact locked", C((-110, 20), (10, -110), (-20, 20), (10, -10)), 0, (), 0, 0, 5, EST),
    K("punch recover / fight", C((-65, 65), (140, -140), (-20, 20), (10, -10)), 0, (), 0, 0, 5, EST),
    K("punch across-down placement", C((-70, 40), (80, -40), (-20, 20), (10, -10)), 0, (), 0, 0, 5, EST)]
# Walk chain (GROUNDED cycle, CJ-06..08) -- measured-estimate walk angles
W_A = K("walk contact A", C((30, -30), (-20, 20), (-45, 30), (20, -10)), 0, (), 0, 0, 3, EST)
W_PA = K("walk passing A", C((15, -15), (-10, 10), (-5, 20), (10, -5)), 0, (), 0, 0, 3, EST)
W_B = K("walk contact B", C((-30, 30), (20, -20), (30, -45), (-10, 20)), 0, (), 0, 0, 3, EST)
W_PB = K("walk passing B", C((-15, 15), (10, -10), (20, -5), (-5, 10)), 0, (), 0, 0, 3, EST)
WALK_KEYS = [W_A, W_PA, W_B, W_PB, W_A, W_PA, W_B, W_PB, W_A]
# Dance chain (GROUNDED, CJ-09..11) incl. shimmy sway section
SHIM = C((-130, 130), (-60, 60), (-20, 35), (30, -20))
DANCE_KEYS = [APOSE,
    K("dance A", C((-90, 90), (90, -90), (-30, 30), (20, -20)), 8, (), 0, 0, 5, EST),
    K("shimmy centre", SHIM, 10, (), 0, 0, 4, EXACT + " (Ginyu 03)"),
    K("shimmy sway left", SHIM, 10, (), 0, -30, 3, EXACT + " + rig dx sway, single render"),
    K("shimmy sway right", SHIM, 10, (), 0, 30, 3, EXACT + " + rig dx sway, single render"),
    K("shimmy centre", SHIM, 10, (), 0, 0, 4, EXACT + " (Ginyu 03)"),
    K("dance B", C((-150, 60), (-20, 120), (-35, 35), (20, -20)), -8, (), 0, 0, 5, EST),
    K("dance combined finale", C((-170, 170), (20, -20), (-40, 40), (25, -25)), 0, ("L", "R"), 0, 0, 5, EST)]
SHIMMY_KEYS = [APOSE,
    K("shimmy centre", SHIM, 10, (), 0, 0, 5, EXACT + " (Ginyu 03)"),
    K("shimmy sway left", SHIM, 10, (), 0, -30, 4, EXACT + " + rig dx sway"),
    K("shimmy sway right", SHIM, 10, (), 0, 30, 4, EXACT + " + rig dx sway"),
    K("shimmy centre", SHIM, 10, (), 0, 0, 5, EXACT + " (Ginyu 03)")]
# Flying chain (AIRBORNE, CJ-12..15) -- heights: video px above ground line
FLY_KEYS = [APOSE,
    K("flying hover", C((-150, 150), (-20, 20), (-40, 40), (60, -60)), 0, ("L", "R"), -120, 0, 5, EST),
    K("flying soar", C((-170, 170), (10, -10), (-50, 50), (70, -70)), -12, ("L", "R"), -200, 0, 5, EST),
    K("flying dive", C((-60, 60), (40, -40), (-20, 20), (30, -30)), -20, (), -80, 0, 5, EST),
    K("flying forward foreshortened", C((-120, 120), (0, 0), (-45, 45), (50, -50)), -10, (), -160, 0, 5, EST),
    K("flying hover return", C((-150, 150), (-20, 20), (-40, 40), (60, -60)), 0, ("L", "R"), -120, 0, 5, EST)]
# Flex/fight chain (GROUNDED, CJ-16..20) -- flex 28px dip NOT applied (same v2 caveat)
FLEX_KEYS = [APOSE,
    K("flex anticipation", C((-40, 40), (80, -80), (-22, 22), (10, -10)), 0, (), 0, 0, 5, EST),
    K("arms up reference", C((-170, 170), (10, -10), (-20, 20), (10, -10)), 0, ("L", "R"), 0, 0, 5, EST),
    K("true flex double bicep (NO 28px dip, labelled)", C((-85, 85), (145, -145), (-22, 22), (10, -10)), 0, (), 0, 0, 5, EST + "; dip missing as in v2"),
    K("fighting forward bicep curl", C((-65, 50), (120, -70), (-20, 20), (10, -10)), 0, (), 0, 0, 5, EST),
    K("fighting stance arms up high", C((-150, 150), (30, -30), (-20, 20), (10, -10)), 0, ("L", "R"), 0, 0, 5, EST)]
# Jump chain (AIRBORNE, CJ-21..22) -- flight line + heights in xsheet
JUMP_KEYS = [APOSE,
    K("jump crouch", C((-30, 30), (90, -90), (-60, 60), (70, -70)), 5, (), 0, 0, 5, EST),
    K("jump takeoff", C((-90, 90), (30, -30), (-40, 40), (40, -40)), -5, (), -60, 0, 4, EST),
    K("jump tuck apex", C((-150, 150), (60, -60), (-70, 70), (100, -100)), -10, (), -200, 0, 5, EST),
    K("jump land (crouch)", C((-30, 30), (90, -90), (-60, 60), (70, -70)), 5, (), 0, 0, 5, EST)]
# Ginyu rollcall successor (GROUNDED, builder-exact rollcall configs)
GINYU_KEYS = [APOSE,
    K("Recoome rollcall", C((-120, 120), (-40, 40), (-50, 45), (25, -25)), 10, ("L", "R"), 0, 0, 5, EXACT),
    K("Burter rollcall", C((-90, 90), (0, 0), (-35, 35), (20, -20)), 8, ("L", "R"), 0, 0, 5, EXACT),
    K("Jeice rollcall", C((-80, 80), (130, -130), (-20, 20), (10, -10)), 14, (), 0, 0, 5, EXACT),
    K("Guldo rollcall", C((-50, 50), (90, -90), (-55, 55), (55, -55)), 8, (), 0, 0, 5, EXACT),
    K("Captain rollcall", C((-100, 10), (30, 90), (-40, 35), (15, -15)), -8, ("L",), 0, 0, 5, EXACT),
    K("Captain spread", C((-150, 150), (-20, 20), (-35, 35), (20, -20)), 0, ("L", "R"), 0, 0, 5, EXACT)]
# Pose-dialects successor (GROUNDED, builder-exact singles; stand pairs = user figure only, labelled)
def D(name, cfg, head, top=()):
    return K(name, cfg, head, top, 0, 0, 4, EXACT)
DIAL_KEYS = [APOSE]
for nm, cfg, hd, tp in [
    ("JoJo 01 contrapposto", C((-75, 40), (125, -45), (-38, 28), (22, -18)), 12, ()),
    ("JoJo 02 fashion twist", C((-115, 65), (85, -95), (-16, 32), (6, -28)), -10, ()),
    ("JoJo 03 menacing lean", C((-25, -88), (35, 145), (-42, 12), (32, -6)), 8, ("R",)),
    ("Ginyu 01 chest out", C((-160, 20), (-20, 95), (-45, 20), (10, -10)), -6, ("L",)),
    ("Ginyu 02 squat", C((-70, 70), (140, -140), (-45, 45), (40, -40)), 0, ()),
    ("Ginyu 03 shimmy", SHIM, 10, ()),
    ("Stand 01 user figure only (stand figure omitted, labelled)", C((-60, 60), (130, -130), (-25, 25), (12, -12)), 0, ()),
    ("Stand 02 user figure only (stand figure omitted, labelled)", C((-35, 35), (60, -60), (-30, 30), (35, -35)), 6, ())]:
    DIAL_KEYS.append(D(nm, cfg, hd, tp)); DIAL_KEYS.append(K("apose neutral between", C((0, 0), (0, 0), (0, 0), (0, 0)), 0, (), 0, 0, 2, "v2 builder exact"))
DIAL_KEYS = DIAL_KEYS[:-1]  # drop trailing neutral; return transition ends on apose anyway

if __name__ == "__main__":
    import sys
    jobs = [
        ("chain-punch", PUNCH_KEYS, 7, "GROUNDED", ""),
        ("chain-walk", WALK_KEYS, 5, "GROUNDED", ""),
        ("chain-dance", DANCE_KEYS, 7, "GROUNDED", ""),
        ("chain-flying", FLY_KEYS, 7, "AIRBORNE", "flight line: ground->hover 60px->soar 100px->dive 40px->forward 80px->hover 60px->land"),
        ("chain-flex-fight", FLEX_KEYS, 7, "GROUNDED", ""),
        ("chain-jump", JUMP_KEYS, 7, "AIRBORNE", "flight line: crouch 0px->takeoff 30px->tuck apex 100px->land 0px"),
        ("successor-shimmy", SHIMMY_KEYS, 7, "GROUNDED", ""),
        ("successor-ginyu-force", GINYU_KEYS, 7, "GROUNDED", ""),
        ("successor-pose-dialects", DIAL_KEYS, 5, "GROUNDED", ""),
    ]
    only = sys.argv[1:] or None
    results = {}
    for name, keys, n_inb, label, flight in jobs:
        if only and name not in only: continue
        f, m, masters = build(name, keys, n_inb=n_inb, label=label, flight=flight)
        n = save_video(name, f, m, masters)
        results[name] = {"frames": n, "fps": 24, "seconds": round(n/24, 2), "label": label, "flight": flight,
                         "keys": [{"name": k["name"], "src": k["src"], "dy_rig": k["dy"], "height_video_px": k.get("target_h", 0)} for k in keys]}
    json.dump(results, open(os.path.join(OUT, "chains-index-20261031.json"), "w"), indent=1)
    print("INDEX WRITTEN", results)
