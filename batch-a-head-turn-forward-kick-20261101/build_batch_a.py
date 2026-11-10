#!/usr/bin/env python3
"""BATCH A — HEAD TURN + FORWARD KICK, Cape Jones, 2026-11-01.
New dated folder only. No repo PR in this batch. No Mars-seen file overwritten.
Sources read-only: sliced/ heads, cut-limbs-v7c/ limb pieces, rig-chains build_chains math.
Head turn: front head -> sliced/Head_Profile.png for turn frames only -> front head.
  Profile placed at the SAME centre as the front head (rig cx 550, cy 331, dy 0),
  chosen from the alignment test (dy -40 floated, dy +40/+70 sank into chest).
  No crossfade, no blend, no tilt passed off as a turn. Body identical all frames.
Kick: LEG1 (our left, Leg_Front) kicks, LEG2 (our right, Leg_Back) planted straight.
  Chamber = thigh raised (leg_upper L +55), shin folded (leg_lower L -40, tested).
  Extension = same thigh, standard lower SWAPPED for the foreshortened piece
  (resize-only reassembly, CJ-15 method), drawn AFTER torso/head so the boot
  sits in front, toward the viewer. Planted leg never moves, so its foot stays
  on the ground line with no dy compensation needed.
  Arms stay out to the sides, never crossing the torso, so arm-front-snap is
  not triggered in either clip (checked per frame, not assumed).
Knee-feet audit is per frame in the xsheet CSVs (see REPORT).
"""
import sys, os, math, json, csv, subprocess
sys.path.insert(0, os.path.expanduser("~/workspace/cape-jones-rig/rig-chains-20261031"))
import build_chains as bc
from PIL import Image
import numpy as np

R = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(R, "batch-a-head-turn-forward-kick-20261101")
FR = os.path.join(OUT, "frames"); os.makedirs(FR, exist_ok=True)
FPS = 24
KICK_PIECE = os.path.join(OUT, "kick-leg-foreshortened-piece-20261101.png")

def figure(c, cx, cfg, head_kind="front", kick_ext=False):
    """bc.figure with head swap + optional foreshortened kicking lower (LEG1)."""
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
            bc.cap_at(c, os.path.join(bc.CUT, cap), knee)  # cap now; foreshortened piece drawn last
            continue
        bc.limb(c, os.path.join(bc.CUT, low), knee, cfg["leg_lower"][side], (ball[0], 0)); bc.cap_at(c, os.path.join(bc.CUT, cap), knee)
    elbows = {}
    for side in ("L", "R"):
        ball, sh_anchor = bc.ARM[side]; vec = (ball[0]-sh_anchor[0], ball[1]-sh_anchor[1]); up, _, _ = bc.ARM_PIECES[side]; sh = shoulders[side]
        bc.limb(c, os.path.join(bc.CUT, up), sh, cfg["arm_upper"][side], sh_anchor)
        elbows[side] = (sh[0]+bc.rot_vec(vec, cfg["arm_upper"][side])[0]*bc.SCALE, sh[1]+bc.rot_vec(vec, cfg["arm_upper"][side])[1]*bc.SCALE)
    bc.paste_at(c, bc.load(os.path.join(bc.BASE, "Pelvis.png")), cx, 680)
    bc.paste_at(c, bc.load(os.path.join(bc.BASE, "Cape_Collar.png")), cx, 370)
    bc.paste_at(c, bc.load(os.path.join(bc.BASE, "Torso_Chest.png")), cx, 400)
    bc.paste_at(c, bc.load(os.path.join(bc.BASE, "Belt_Overlay.png")), cx, 670)
    for side in ("L", "R"):
        _, low, cap = bc.ARM_PIECES[side]; ball, _ = bc.ARM[side]
        bc.limb(c, os.path.join(bc.CUT, low), elbows[side], cfg["arm_lower"][side], (ball[0], 0)); bc.cap_at(c, os.path.join(bc.CUT, cap), elbows[side])
    bc.paste_at(c, bc.load(os.path.join(bc.BASE, "Neck.png"), scale=1.05), cx, 360)
    if head_kind == "front":
        head = bc.load(os.path.join(bc.BASE, "Head_Front.png"))
    else:
        head = bc.load(os.path.join(bc.BASE, "Head_Profile.png"))
    c.alpha_composite(head, (int(cx-head.size[0]/2), int(331-head.size[1]/2)))
    if kick_ext:
        # Foreshortened piece, top-centre anchored at the kicking knee, in front
        # of torso/head layer so the enlarged boot reads toward the viewer.
        piece = bc.load(KICK_PIECE)
        kx, ky = knees["L"]
        c.alpha_composite(piece, (int(kx-piece.size[0]/2), int(ky-15)))
    return c, knees

def render(cfg, head_kind="front", kick_ext=False):
    c = Image.new("RGBA", (1100, 1500), (0, 0, 0, 0))
    c, knees = figure(c, 550, cfg, head_kind, kick_ext)
    return bc.video_frame(c), knees

def silhouette_bottom(vf):
    a = np.asarray(vf.convert("RGB")).astype(int)
    sil = (np.abs(a-128).sum(axis=2) > 40)
    ys, _ = np.where(sil); return int(ys.max())

def save_clip(name, frames, meta):
    sub = os.path.join(FR, name); os.makedirs(sub, exist_ok=True)
    for i, f in enumerate(frames):
        f.save(os.path.join(sub, f"{name}-{i:03d}.jpg"), quality=92)
    with open(os.path.join(OUT, f"{name}-frames.txt"), "w") as fh:
        for i in range(len(frames)):
            fh.write(f"file '{sub}/{name}-{i:03d}.jpg'\n")
    mp4 = os.path.join(OUT, f"{name}-20261101.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-r", str(FPS),
                    "-i", os.path.join(OUT, f"{name}-frames.txt"), "-vf", "scale=1100:750",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", mp4], check=True)
    small = [f.resize((550, 375)) for f in frames]
    small[0].save(os.path.join(OUT, f"{name}-20261101.gif"), save_all=True, append_images=small[1:], duration=42, loop=0)
    with open(os.path.join(OUT, f"{name}-xsheet-20261101.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(meta[0].keys())); w.writeheader(); w.writerows(meta)
    return mp4

# ---------------- 1. HEAD TURN ----------------
STAND = bc.C((0, 0), (0, 0), (0, 0), (0, 0))
ht_frames, ht_meta = [], []
def ht_add(head_kind, note):
    vf, _ = render(STAND, head_kind)
    ht_frames.append(vf)
    ht_meta.append({"frame": len(ht_frames)-1, "head": head_kind, "head_source": "sliced/Head_Front.png" if head_kind == "front" else "sliced/Head_Profile.png",
                    "body": "front standing rig, unchanged", "note": note, "silhouette_bottom_video_px": silhouette_bottom(vf)})
for _ in range(12): ht_add("front", "KEY front stand")
for _ in range(18): ht_add("profile", "KEY head turn: side-facing head")
for _ in range(12): ht_add("front", "KEY front stand, returned")
ht_mp4 = save_clip("head-turn-true", ht_frames, ht_meta)

# ---------------- 2. FORWARD KICK ----------------
CHAMBER = bc.C((-25, 25), (30, -30), (70, 0), (-40, 0))  # thigh 70: tested 55/70/85, 70 puts boot in front of body, 85 reads as side kick
EXT = bc.C((-55, 45), (30, -30), (70, 0), (0, 0))  # thigh same as chamber; shin swapped for piece
def lerp(a, b, t):
    return {g: {s: a[g][s]+(b[g][s]-a[g][s])*t for s in ("L", "R")} for g in ("arm_upper", "arm_lower", "leg_upper", "leg_lower")}
def ease(t): return t*t*t*(t*(t*6-15)+10) if False else (t<0.5 and 4*t*t*t or 1-((-2*t+2)**3)/2)

k_frames, k_meta = [], []
def k_add(cfg, kick_ext, note, knee_note):
    vf, knees = render(cfg, "front", kick_ext)
    k_frames.append(vf)
    k_meta.append({"frame": len(k_frames)-1, "note": note,
                   "arm_upper_L": cfg["arm_upper"]["L"], "arm_upper_R": cfg["arm_upper"]["R"],
                   "arm_lower_L": cfg["arm_lower"]["L"], "arm_lower_R": cfg["arm_lower"]["R"],
                   "leg_upper_L_kick": cfg["leg_upper"]["L"], "leg_upper_R_planted": cfg["leg_upper"]["R"],
                   "leg_lower_L_kick": cfg["leg_lower"]["L"], "leg_lower_R_planted": cfg["leg_lower"]["R"],
                   "foreshortened_piece": "ON" if kick_ext else "OFF",
                   "knee_feet": knee_note,
                   "silhouette_bottom_video_px": silhouette_bottom(vf),
                   "kick_knee_rig_xy": f"{knees['L'][0]:.0f},{knees['L'][1]:.0f}"})
def k_hold(cfg, kick_ext, n, note, knee_note):
    for _ in range(n): k_add(cfg, kick_ext, note, knee_note)
def k_trans(a, b, n, kick_ext, note):
    for j in range(1, n+1):
        t = j/(n+1); e = ease(t)
        k_add(lerp(a, b, e), kick_ext, f"{note} inbetween t={t:.2f}",
              "planted R straight/straight; kicking L thigh raised, shin interpolating" if not kick_ext else "extension")
PLANTED = "planted LEG2 (our right) straight knee, straight/original toes: MATCH"
KICK_EXT_NOTE = "kicking LEG1 (our left): knee raised forward, foreshortened boot enlarged in front toward viewer: MATCH (forward/forward)"
CHAMBER_NOTE = "kicking LEG1: knee raised, shin folded in kick plane, foot follows shin (no sideways splay, no valgus/varus read); planted: MATCH"
k_hold(STAND, False, 6, "KEY stand", PLANTED)
k_trans(STAND, CHAMBER, 7, False, "stand->chamber")
k_hold(CHAMBER, False, 4, "KEY chamber", CHAMBER_NOTE)
k_trans(CHAMBER, EXT, 7, False, "chamber->extension (standard lower)")
k_hold(EXT, True, 8, "KEY forward kick extension, foreshortened piece ON", KICK_EXT_NOTE)
k_trans(EXT, CHAMBER, 7, False, "extension->chamber (standard lower returns)")
k_hold(CHAMBER, False, 3, "KEY chamber recover", CHAMBER_NOTE)
k_trans(CHAMBER, STAND, 7, False, "chamber->stand")
k_hold(STAND, False, 6, "KEY stand", PLANTED)
k_mp4 = save_clip("forward-kick-true", k_frames, k_meta)

# contact sheets
def contact(name, frames, picks, cols=4):
    rows = (len(picks)+cols-1)//cols
    sheet = Image.new("RGB", (1100//2*cols, 750//2*rows), (255, 255, 255))
    for i, p in enumerate(picks):
        sheet.paste(frames[p].resize((550, 375)), ((i % cols)*550, (i//cols)*375))
    sheet.save(os.path.join(OUT, f"{name}-contact-20261101.png"))
    return picks
ht_picks = [0, 11, 12, 20, 29, 30, 41]
contact("head-turn-true", ht_frames, ht_picks)
k_picks = [0, 5, 12, 16, 23, 27, 31, 38, 41, 48, 54]
contact("forward-kick-true", k_frames, k_picks, cols=4)
# head crops: front vs profile at video scale, 3x nearest on crop
for label, fidx in [("front", 0), ("profile", 20)]:
    vf = ht_frames[fidx]
    crop = vf.crop((480, 80, 620, 250)).resize((140*3, 170*3), Image.NEAREST)
    crop.save(os.path.join(OUT, f"head-turn-{label}-crop-20261101.png"))
# extension still, full frame
k_frames[27].save(os.path.join(OUT, "forward-kick-extension-still-20261101.png"))
ht_frames[20].save(os.path.join(OUT, "head-turn-profile-still-20261101.png"))

summary = {
  "head_turn": {"frames": len(ht_frames), "fps": FPS, "duration_s": round(len(ht_frames)/FPS, 2),
                "front_frames_0indexed": "0-11 and 30-41", "profile_frames_0indexed": "12-29",
                "profile_seconds": "0.50-1.25", "mp4": ht_mp4,
                "bottom_px_all": sorted(set(m["silhouette_bottom_video_px"] for m in ht_meta))},
  "kick": {"frames": len(k_frames), "fps": FPS, "duration_s": round(len(k_frames)/FPS, 2),
           "stand": "0-5, 49-54", "chamber": "13-16, 39-41", "extension_piece_ON": "24-31",
           "mp4": k_mp4, "bottom_px_all": sorted(set(m["silhouette_bottom_video_px"] for m in k_meta))},
}
json.dump(summary, open(os.path.join(OUT, "batch-a-summary-20261101.json"), "w"), indent=2)
print(json.dumps(summary, indent=2))
