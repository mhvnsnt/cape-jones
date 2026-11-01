#!/usr/bin/env python3
"""ANATOMY FIX BUNDLE 20261101 - Mars 2026-11-01 11:26-11:31 CST.
Cape Jones own pieces only, rig re-render (build_chains figure math), no show art.
1 FLEX WIDER: approach + hold 70-90deg wider from centreline above head.
   Old arms-up: upper -170/+170, elbow angle_from_up -5/+3deg, inter-arm ~8deg (acute).
   New wide-up: upper -100/+100, elbow angle_from_up -75/+73deg, delta +70deg.
   New flex hold: upper -85/+85, angle_from_up -90/+88deg, delta +85deg vs old arms-up,
   inter-arm ~178deg (obtuse). Fists still roll toward head/shoulders (lower 145/-145,
   fist far point above elbow, toward head), NOT outward away from head.
2 ARMS ACROSS CHEST: automatic sensor, forearm-vs-torso >1000px at 1100x1500
   (ARM-FRONT-SNAP-RULE.md). Chest snap = whole chain after torso, before neck/head.
   Face top (original top keys) = whole chain after head. Priority face > chest.
   This figure() is the wired-into-every-builder version: sensor runs per frame,
   never a block range, never manual.
3 ELBOWS: audit per key - elbow must be lateral/outward from shoulder
   (L elbow x < shoulder x, R elbow x > shoulder x), forearm flexes inward/up
   toward head/torso for flex, never reversed (fist outward-down past elbow).
4 LEGS, per frame, Mars exception for THIS bundle only (standing KNEE-FEET-RULE.md
   is NOT overwritten): gate = leg_upper L>0 AND R<0 (both thighs toward midline).
   If gate: LEG2 RIGHT foot TURNS (mirror R lower piece, anchor remapped
   width-ball, as in dance-kneefeet correction), LEG1 LEFT foot does NOT turn
   (no mirror, original lower kept, Mars: "it is fine as-is").
   If not gate: no turn, feet follow knees (outward/straight).
5 SIDE SHUFFLE: alternating lift-plant, L then R then L, not dx-slide together.
   Each step: lift (knee bent, foot up, weight on planted leg), move, plant,
   then other leg. Grounded except lifted foot moment.
Sound: original clip WAVs reused, not re-synthesised, peak unchanged.
Flicker: whole-frame WCAG proxy re-run on outputs (see gate script output).
"""
import os, sys, math, json, csv, subprocess
sys.path.insert(0, os.path.expanduser("~/workspace/cape-jones-rig/rig-chains-20261031"))
sys.path.insert(0, os.path.expanduser("~/workspace/cape-jones-rig/arm-front-snap-auto-20261101"))
import build_chains as bc
from arm_front_snap_sensor import sense_from_angles, torso_mask
from PIL import Image, ImageOps
import numpy as np

R = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(R, "anatomy-fix-bundle-20261101")
FR = os.path.join(OUT, "frames")
os.makedirs(FR, exist_ok=True)
BASE, CUT = bc.BASE, bc.CUT
SCALE = bc.SCALE

def angle_from_up(side, upper):
    ball, anch = bc.ARM[side]
    vec = (ball[0]-anch[0], ball[1]-anch[1])
    up = bc.rot_vec(vec, upper)
    sh = {"L": (430, 445), "R": (670, 445)}[side]
    elbow = (sh[0]+up[0]*SCALE, sh[1]+up[1]*SCALE)
    dx, dy = elbow[0]-sh[0], elbow[1]-sh[1]
    return math.degrees(math.atan2(dx, -dy)), elbow

def limb_mirror(c, path, joint, angle, anchor, mirror):
    if not mirror:
        bc.limb(c, path, joint, angle, anchor); return
    im = Image.open(path).convert("RGBA")
    im = im.resize((max(1, int(im.size[0]*SCALE)), max(1, int(im.size[1]*SCALE))), Image.LANCZOS)
    mir = ImageOps.mirror(im)
    ax = im.size[0] - anchor[0]*SCALE
    layer = Image.new("RGBA", c.size, (0, 0, 0, 0))
    layer.alpha_composite(mir, (int(joint[0]-ax), int(joint[1]-anchor[1]*SCALE)))
    layer = layer.rotate(angle, center=joint, expand=False)
    c.alpha_composite(layer)

def figure2(c, cx, cfg, head=0, chest_top=(), face_top=(), foot_mirror=()):
    bc.paste_at(c, bc.load(os.path.join(BASE, "Cape_Back_Main.png")), cx, 410)
    hips = {"L": (cx-80, 740), "R": (cx+65, 740)}
    shoulders = {"L": (cx-120, 445), "R": (cx+120, 445)}
    knees = {}
    for side in ("L", "R"):
        hip = hips[side]; ball, hip_anchor = bc.LEG[side]
        vec = (ball[0]-hip_anchor[0], ball[1]-hip_anchor[1])
        up, low, cap = bc.LEG_PIECES[side]
        bc.limb(c, os.path.join(CUT, up), hip, cfg["leg_upper"][side], hip_anchor)
        knee = (hip[0]+bc.rot_vec(vec, cfg["leg_upper"][side])[0]*SCALE,
                hip[1]+bc.rot_vec(vec, cfg["leg_upper"][side])[1]*SCALE)
        knees[side] = knee
        limb_mirror(c, os.path.join(CUT, low), knee, cfg["leg_lower"][side], (ball[0], 0), side in foot_mirror)
        bc.cap_at(c, os.path.join(CUT, cap), knee)
    elbows = {}
    for side in ("L", "R"):
        if side in chest_top or side in face_top: continue
        ball, sh_anchor = bc.ARM[side]
        vec = (ball[0]-sh_anchor[0], ball[1]-sh_anchor[1])
        up, _, _ = bc.ARM_PIECES[side]; sh = shoulders[side]
        bc.limb(c, os.path.join(CUT, up), sh, cfg["arm_upper"][side], sh_anchor)
        elbows[side] = (sh[0]+bc.rot_vec(vec, cfg["arm_upper"][side])[0]*SCALE,
                        sh[1]+bc.rot_vec(vec, cfg["arm_upper"][side])[1]*SCALE)
    bc.paste_at(c, bc.load(os.path.join(BASE, "Pelvis.png")), cx, 680)
    bc.paste_at(c, bc.load(os.path.join(BASE, "Cape_Collar.png")), cx, 370)
    bc.paste_at(c, bc.load(os.path.join(BASE, "Torso_Chest.png")), cx, 400)
    bc.paste_at(c, bc.load(os.path.join(BASE, "Belt_Overlay.png")), cx, 670)
    # chest snap: whole chain after torso, before head
    for side in ("L", "R"):
        if side not in chest_top: continue
        ball, sh_anchor = bc.ARM[side]
        vec = (ball[0]-sh_anchor[0], ball[1]-sh_anchor[1])
        up, low, cap = bc.ARM_PIECES[side]; sh = shoulders[side]
        bc.limb(c, os.path.join(CUT, up), sh, cfg["arm_upper"][side], sh_anchor)
        elbow = (sh[0]+bc.rot_vec(vec, cfg["arm_upper"][side])[0]*SCALE,
                 sh[1]+bc.rot_vec(vec, cfg["arm_upper"][side])[1]*SCALE)
        bc.limb(c, os.path.join(CUT, low), elbow, cfg["arm_lower"][side], (ball[0], 0))
        bc.cap_at(c, os.path.join(CUT, cap), elbow)
    for side in ("L", "R"):
        if side in chest_top or side in face_top: continue
        _, low, cap = bc.ARM_PIECES[side]; ball, _ = bc.ARM[side]
        bc.limb(c, os.path.join(CUT, low), elbows[side], cfg["arm_lower"][side], (ball[0], 0))
        bc.cap_at(c, os.path.join(CUT, cap), elbows[side])
    bc.paste_at(c, bc.load(os.path.join(BASE, "Neck.png"), scale=1.05), cx, 360)
    head_im = bc.load(os.path.join(BASE, "Head_Front.png"))
    if head: head_im = head_im.rotate(head, expand=True)
    c.alpha_composite(head_im, (int(cx-head_im.size[0]/2), int(331-head_im.size[1]/2)))
    for side in ("L", "R"):
        if side not in face_top: continue
        ball, sh_anchor = bc.ARM[side]
        vec = (ball[0]-sh_anchor[0], ball[1]-sh_anchor[1])
        up, low, cap = bc.ARM_PIECES[side]; sh = shoulders[side]
        bc.limb(c, os.path.join(CUT, up), sh, cfg["arm_upper"][side], sh_anchor)
        elbow = (sh[0]+bc.rot_vec(vec, cfg["arm_upper"][side])[0]*SCALE,
                 sh[1]+bc.rot_vec(vec, cfg["arm_upper"][side])[1]*SCALE)
        bc.limb(c, os.path.join(CUT, low), elbow, cfg["arm_lower"][side], (ball[0], 0))
        bc.cap_at(c, os.path.join(CUT, cap), elbow)
    return c

def render2(cfg, head=0, chest_top=(), face_top=(), foot_mirror=(), dx=0, dy=0):
    c = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    figure2(c, 550, cfg, head, chest_top, face_top, foot_mirror)
    if dx or dy:
        d = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0)); d.alpha_composite(c, (dx, dy)); return d
    return c

def C(au, al, lu, ll): return bc.C(au, al, lu, ll)
def K(name, cfg, head=0, top=(), dy=0, dx=0, hold=5):
    return {"name": name, "cfg": cfg, "head": head, "top": top, "dy": dy, "dx": dx, "hold": hold, "target_h": -dy//2}
APOSE = K("apose", C((0, 0), (0, 0), (0, 0), (0, 0)), 0, (), 0, 0, 3)
SHIM = C((-130, 130), (-60, 60), (-20, 35), (30, -20))

FLEX_KEYS = [APOSE,
    K("flex anticipation WIDE", C((-70, 70), (80, -80), (-22, 22), (10, -10)), 0, (), 0, 0, 5),
    K("arms up WIDE (was arms up reference)", C((-100, 100), (20, -20), (-20, 20), (10, -10)), 0, (), 0, 0, 5),
    K("true flex double bicep WIDE hold", C((-85, 85), (145, -145), (-22, 22), (10, -10)), 0, (), 0, 0, 5),
    K("fighting forward bicep curl", C((-65, 50), (120, -70), (-20, 20), (10, -10)), 0, (), 0, 0, 5),
    K("fighting stance arms up high", C((-150, 150), (30, -30), (-20, 20), (10, -10)), 0, ("L", "R"), 0, 0, 5)]

DANCE_KEYS = [APOSE,
    K("dance A", C((-90, 90), (90, -90), (-30, 30), (20, -20)), 8, (), 0, 0, 5),
    K("shimmy centre", SHIM, 10, (), 0, 0, 4),
    K("shuffle step L (lift)", C((-130, 130), (-60, 60), (-15, 15), (70, -5)), 10, (), 0, -30, 3),
    K("shuffle plant L", C((-130, 130), (-60, 60), (-35, 20), (20, -10)), 10, (), 0, -30, 3),
    K("shuffle step R (lift)", C((-130, 130), (-60, 60), (20, 15), (10, -70)), 10, (), 0, 0, 3),
    K("shuffle plant R", C((-130, 130), (-60, 60), (20, -35), (-10, 20)), 10, (), 0, 0, 3),
    K("shuffle step L (lift) 2", C((-130, 130), (-60, 60), (-15, 15), (70, -5)), 10, (), 0, -30, 3),
    K("shuffle plant L 2", C((-130, 130), (-60, 60), (-35, 20), (20, -10)), 10, (), 0, -30, 3),
    K("shimmy centre", SHIM, 10, (), 0, 0, 4),
    K("dance B", C((-150, 60), (-20, 120), (-35, 35), (20, -20)), -8, (), 0, 0, 5),
    K("dance combined finale", C((-170, 170), (20, -20), (-40, 40), (25, -25)), 0, ("L", "R"), 0, 0, 5)]

PUNCH_KEYS = [APOSE,
    K("punch windup", C((-40, 40), (60, -60), (-20, 20), (10, -10)), -5, (), 0, 0, 5),
    K("punch extend/snap", C((-160, 20), (0, -110), (-20, 20), (10, -10)), 0, (), 0, 0, 5),
    K("punch impact locked", C((-110, 20), (10, -110), (-20, 20), (10, -10)), 0, (), 0, 0, 5),
    K("punch recover / fight", C((-65, 65), (140, -140), (-20, 20), (10, -10)), 0, (), 0, 0, 5),
    K("punch across-down placement", C((-70, 40), (80, -40), (-20, 20), (10, -10)), 0, (), 0, 0, 5)]

CROSS_KEYS = [APOSE,
    # CORRECTED 20261101: upper (-20,+20) elbows OUT to sides, forearms (90,-90)
    # cross chest. The earlier (20,-20) config was REVERSED: elbows inward
    # (+48/-42 from shoulder), forearms overshooting to 750/357. Elbow audit
    # now requires L elbow < shoulder, R elbow > shoulder, except when the
    # upper arm is near-vertical (angle_from_up within 10deg of 0, arms-up
    # transition, elbow above shoulder, not lateral).
    K("arms crossed down across chest", C((-20, 20), (90, -90), (-20, 20), (10, -10)), 0, (), 0, 0, 5),
    K("arms crossed down hold", C((-20, 20), (90, -90), (-20, 20), (10, -10)), 0, (), 0, 0, 5)]

def build(name, keys, n_inb=7):
    # ground compensation like build_chains: silhouette bottom -> 652 video
    def bottom(cfg, head, top):
        vf = bc.video_frame(render2(cfg, head, (), top, ()))
        a = np.asarray(vf.convert("RGB")).astype(int)
        sil = (np.abs(a-128).sum(axis=2) > 40)
        ys, _ = np.where(sil); return int(ys.max())
    for k in keys:
        target_h = k.get("target_h", 0)
        b0 = bottom(k["cfg"], k["head"], k["top"])
        k["dy"] = 2*((652-target_h)-b0); k["height_video_px"] = target_h
    frames, meta = [], []
    def add(cfg, head, face_top, dx, dy, note, frm, to, t, e, height=None):
        snap = sense_from_angles(cfg)
        chest = tuple(s for s in ("L", "R") if snap[s][0] and s not in face_top)
        gate_in = cfg["leg_upper"]["L"] > 0 and cfg["leg_upper"]["R"] < 0
        foot_mirror = ("R",) if gate_in else ()
        # elbow audit
        elb = {}
        for s in ("L", "R"):
            ang, el = angle_from_up(s, cfg["arm_upper"][s]); elb[s] = ang
            shx = 430 if s == "L" else 670
            elb[s+"_lateral_ok"] = (el[0] < shx) if s == "L" else (el[0] > shx)
        frames.append(bc.video_frame(render2(cfg, head, chest, face_top, foot_mirror, dx, dy)))
        meta.append({"frame": len(frames)-1, "kind": note, "from": frm, "to": to, "t": round(t, 2), "eased": round(e, 2),
                     "dx_rig": dx, "dy_rig": dy, "height_video_px": height if height is not None else -dy//2,
                     "snap_L_px": snap["L"][1], "snap_R_px": snap["R"][1],
                     "snap_L": bool(snap["L"][0]), "snap_R": bool(snap["R"][0]),
                     "chest_top": ",".join(chest), "face_top": ",".join(face_top),
                     "leg_upper_L": cfg["leg_upper"]["L"], "leg_upper_R": cfg["leg_upper"]["R"],
                     "leg_lower_L": cfg["leg_lower"]["L"], "leg_lower_R": cfg["leg_lower"]["R"],
                     "knee_gate_inward_Lpos_Rneg": gate_in,
                     "foot_turn_L": False, "foot_turn_R": bool(gate_in),
                     "foot_turn_note": "LEG1 LEFT no turn (Mars exception, this bundle only); LEG2 RIGHT mirror turn if gate" if gate_in else "gate off: no foot turn, feet follow knees",
                     "elbow_angle_from_up_L": round(elb["L"], 1), "elbow_angle_from_up_R": round(elb["R"], 1),
                     "elbow_lateral_ok_L": elb["L_lateral_ok"], "elbow_lateral_ok_R": elb["R_lateral_ok"],
                     "arm_upper_L": cfg["arm_upper"]["L"], "arm_upper_R": cfg["arm_upper"]["R"],
                     "arm_lower_L": cfg["arm_lower"]["L"], "arm_lower_R": cfg["arm_lower"]["R"]})
    def transition(a, b):
        deltas = {s: abs(b["cfg"]["arm_upper"][s]-a["cfg"]["arm_upper"][s]) for s in ("L", "R")}
        big = max(deltas, key=deltas.get)
        for j in range(1, n_inb+1):
            t = j/(n_inb+1); e = bc.ease(t); cfg = bc.lerp_cfg(a["cfg"], b["cfg"], e)
            head = a["head"]+(b["head"]-a["head"])*e
            face = tuple(sorted(set(a["top"]) | set(b["top"])))
            dx = int(a["dx"]+(b["dx"]-a["dx"])*e); dy = int(a["dy"]+(b["dy"]-a["dy"])*e); tag = "inbetween"
            if j == 3:
                cfg["arm_upper"][big] += 10 if b["cfg"]["arm_upper"][big] >= a["cfg"]["arm_upper"][big] else -10
                tag = "BREAKDOWN arc +10deg largest-moving arm upper"
            if j == 5:
                cfg["arm_lower"][big] += 8 if b["cfg"]["arm_lower"][big] >= a["cfg"]["arm_lower"][big] else -8
                tag = "BREAKDOWN follow-through +8deg that arm lower"
            h = a.get("height_video_px", 0)+(b.get("height_video_px", 0)-a.get("height_video_px", 0))*e
            add(cfg, head, face, dx, dy, tag, a["name"], b["name"], t, e, height=int(round(h)))
    def hold(k, note="KEY hold"):
        for _ in range(k["hold"]):
            add(k["cfg"], k["head"], k["top"], k["dx"], k["dy"], note, k["name"], k["name"], 0, 0, height=k.get("height_video_px", 0))
    hold(keys[0])
    for i in range(len(keys)-1):
        transition(keys[i], keys[i+1]); hold(keys[i+1])
    # overshoot arms only, then return
    prev, last = keys[-2], keys[-1]
    over = {g: dict(last["cfg"][g]) for g in last["cfg"]}
    for g in ("arm_upper", "arm_lower"):
        for s in ("L", "R"):
            over[g][s] = prev["cfg"][g][s] + (last["cfg"][g][s]-prev["cfg"][g][s])*1.05
    add(over, last["head"], last["top"], last["dx"], last["dy"], "OVERSHOOT 5% beyond key", prev["name"], last["name"], 1.05, 1.05, height=last.get("height_video_px", 0))
    add(last["cfg"], last["head"], last["top"], last["dx"], last["dy"], "SETTLE back to key", last["name"], last["name"], 1.0, 1.0, height=last.get("height_video_px", 0))
    transition(last, keys[0]); hold(keys[0])
    return frames, meta

def save(name, frames, meta, wav_src):
    sub = os.path.join(FR, name); os.makedirs(sub, exist_ok=True)
    for i, f in enumerate(frames): f.save(os.path.join(sub, f"{name}-{i:03d}.jpg"), quality=92)
    with open(os.path.join(OUT, f"{name}-frames.txt"), "w") as fh:
        for i in range(len(frames)): fh.write(f"file '{sub}/{name}-{i:03d}.jpg'\n")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-r", "24",
                    "-i", os.path.join(OUT, f"{name}-frames.txt"), "-i", wav_src,
                    "-vf", "scale=1100:750", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-shortest", "-movflags", "+faststart",
                    os.path.join(OUT, f"{name}-20261101.mp4")], check=True)
    small = [f.resize((550, 375)) for f in frames]
    small[0].save(os.path.join(OUT, f"{name}-20261101.gif"), save_all=True, append_images=small[1:], duration=42, loop=0)
    with open(os.path.join(OUT, f"{name}-xsheet-20261101.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(meta[0].keys())); w.writeheader(); w.writerows(meta)
    print(name, len(frames), f"{len(frames)/24:.2f}s", "snap_frames", sum(1 for m in meta if m["snap_L"] or m["snap_R"]),
          "foot_turn_R_frames", sum(1 for m in meta if m["foot_turn_R"]), flush=True)
    return len(frames)

if __name__ == "__main__":
    src_wav = os.path.join(R, "movement-library-clips-20261101")
    jobs = [
        ("anatomy-flex-wide", FLEX_KEYS, os.path.join(src_wav, "07-johnny-bravo-flex-dance.wav")),
        ("anatomy-dance-shuffle", DANCE_KEYS, os.path.join(src_wav, "05-scooby-song-step.wav")),
        ("anatomy-punch-cross", PUNCH_KEYS, os.path.join(src_wav, "03-fosters-pose-swap-gesture.wav")),
        ("anatomy-cross-down", CROSS_KEYS, os.path.join(src_wav, "07-johnny-bravo-flex-dance.wav")),
    ]
    out = {}
    for name, keys, wav in jobs:
        f, m = build(name, keys)
        out[name] = save(name, f, m, wav)
    json.dump(out, open(os.path.join(OUT, "bundle-index-20261101.json"), "w"), indent=2)
    print("DONE", out)
