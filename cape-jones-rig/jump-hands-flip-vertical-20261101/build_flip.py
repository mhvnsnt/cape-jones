"""Hand 1 + Hand 2 VERTICAL FLIP IN PLACE — jump apex / arms-up frames.
Mars 2026-11-01 00:45 CDT, replying to jump apex old vs new contact:
"flip it to where the top is to the bottom and the bottom is to the top."

PLAIN PIECE NOTE (do not guess a library number):
- The jump-chain builder does NOT use separate canon hand pieces
  (sliced/Hand_1_Fist.png, Hand_2_FistBack.png are NOT in this chain).
- The two hands at apex are the distal FIST segments of the two
  lower-arm pieces in the chain:
    Hand A (figure left, screen left at apex) = Arm_Front_Lower.png (L)
    Hand B (figure right, screen right at apex) = Arm_Back_Lower.png (R)
  Both meet in the centre at apex, over the face (top_arms L,R).
- "Hand one and two" in this job = those two apex hands, A and B,
  NOT library Hand_1 / Hand_2. No library hand was flipped.

METHOD, exactly VERTICAL FLIP IN PLACE, following the T-pose hand-flip
precedent (hand-flips-vertical-inplace-20261031):
- Render the figure with the fist segment ERASED from the lower pieces
  (gauntlet kept, head/torso underneath preserved — no pixel erase on
  the finished frame, no radius-circle erase).
- Take the fist segment ONLY, as placed (rendered lower layer, fist
  pixels = projection along the arm direction >= wrist distance),
  flip that fist layer top-to-bottom in screen space (FLIP_TOP_BOTTOM),
  then re-seat it so its WRIST point lands back on the SAME wrist
  target. Wrist x unchanged, wrist y unchanged by construction.
  Only the fist moves; body, arms (gauntlet), head, legs do not flip.
- Applied ONLY to arms-up frames (top contains both L and R, frames
  15-44 in the jump-fix chain). All other frames are byte-identical
  to the jump-fix chain (copied, not re-rendered with a flip).
"""
import sys, os, json, math, subprocess, csv
sys.path.insert(0, "/home/hatch/workspace/cape-jones-rig/rig-chains-20261031")
import build_chains as bc
from PIL import Image
import numpy as np

R = "/home/hatch/workspace/cape-jones-rig"
OUT = "/home/hatch/workspace/cape-jones-rig/jump-hands-flip-vertical-20261101"
FR = os.path.join(OUT, "frames", "jump-hands-flipped")
os.makedirs(FR, exist_ok=True)
SCALE = bc.SCALE  # 0.95
# wrist split, native piece y, and wrist centre x (measured, see report)
SPLIT = {"L": 189, "R": 185}          # Front / Back lower, native y
WRIST_CX = {"L": 69, "R": 107}        # centre x of fist at split, native
BALL = {"L": (60, 222), "R": (99, 222)}
SH_ANCHOR = (76, 30)

def load_scaled(path):
    im = Image.open(path).convert("RGBA")
    return im.resize((max(1, int(im.size[0]*SCALE)), max(1, int(im.size[1]*SCALE))), Image.LANCZOS)

def lower_no_fist(path, side):
    """Lower piece with fist segment (y >= split, scaled) made transparent."""
    im = load_scaled(path).copy()
    arr = np.array(im)
    split_s = int(SPLIT[side]*SCALE)
    arr[split_s:, :, 3] = 0
    return Image.fromarray(arr, "RGBA")

LOWER_NOFIST = {
    "L": lower_no_fist(os.path.join(R, "cut-limbs-v7c", "Arm_Front_Lower.png"), "L"),
    "R": lower_no_fist(os.path.join(R, "cut-limbs-v7c", "Arm_Back_Lower.png"), "R"),
}
LOWER_ORIG = {
    "L": load_scaled(os.path.join(R, "cut-limbs-v7c", "Arm_Front_Lower.png")),
    "R": load_scaled(os.path.join(R, "cut-limbs-v7c", "Arm_Back_Lower.png")),
}

def limb_custom(c, im_scaled, joint, angle, anchor):
    ax, ay = anchor[0]*SCALE, anchor[1]*SCALE
    layer = Image.new("RGBA", c.size, (0,0,0,0))
    layer.alpha_composite(im_scaled, (int(joint[0]-ax), int(joint[1]-ay)))
    layer = layer.rotate(angle, center=joint, expand=False)
    c.alpha_composite(layer)
    return layer  # layer BEFORE rotation? no: this returns rotated layer? see below
# NOTE: bc.limb composites rotated layer into c and returns None; we need the
# rotated lower layer alone for fist masking, so re-implement it cleanly:
def limb_layer(im_scaled, joint, angle, anchor, size=(1100,1500)):
    ax, ay = anchor[0]*SCALE, anchor[1]*SCALE
    layer = Image.new("RGBA", size, (0,0,0,0))
    layer.alpha_composite(im_scaled, (int(joint[0]-ax), int(joint[1]-ay)))
    return layer.rotate(angle, center=joint, expand=False)

def figure_custom(c, cx, cfg, head_angle=0, top_arms=(), lower_map=None):
    # copy of bc.figure, with lower_map overriding lower pieces
    if lower_map is None: lower_map = {}
    bc.paste_at(c, bc.load(os.path.join(bc.BASE, "Cape_Back_Main.png")), cx, 410)
    hips = {"L": (cx-80, 740), "R": (cx+65, 740)}; shoulders = {"L": (cx-120, 445), "R": (cx+120, 445)}
    for side in ("L", "R"):
        hip = hips[side]; ball, hip_anchor = bc.LEG[side]; vec = (ball[0]-hip_anchor[0], ball[1]-hip_anchor[1])
        up, low, cap = bc.LEG_PIECES[side]
        bc.limb(c, os.path.join(bc.CUT, up), hip, cfg["leg_upper"][side], hip_anchor)
        knee = (hip[0]+bc.rot_vec(vec, cfg["leg_upper"][side])[0]*SCALE, hip[1]+bc.rot_vec(vec, cfg["leg_upper"][side])[1]*SCALE)
        bc.limb(c, os.path.join(bc.CUT, low), knee, cfg["leg_lower"][side], (ball[0], 0)); bc.cap_at(c, os.path.join(bc.CUT, cap), knee)
    elbows = {}
    for side in ("L", "R"):
        if side in top_arms: continue
        ball, sh_anchor = bc.ARM[side]; vec = (ball[0]-sh_anchor[0], ball[1]-sh_anchor[1]); up, _, _ = bc.ARM_PIECES[side]; sh = shoulders[side]
        bc.limb(c, os.path.join(bc.CUT, up), sh, cfg["arm_upper"][side], sh_anchor)
        elbows[side] = (sh[0]+bc.rot_vec(vec, cfg["arm_upper"][side])[0]*SCALE, sh[1]+bc.rot_vec(vec, cfg["arm_upper"][side])[1]*SCALE)
    bc.paste_at(c, bc.load(os.path.join(bc.BASE, "Pelvis.png")), cx, 680); bc.paste_at(c, bc.load(os.path.join(bc.BASE, "Cape_Collar.png")), cx, 370)
    bc.paste_at(c, bc.load(os.path.join(bc.BASE, "Torso_Chest.png")), cx, 400); bc.paste_at(c, bc.load(os.path.join(bc.BASE, "Belt_Overlay.png")), cx, 670)
    for side in ("L", "R"):
        if side in top_arms: continue
        _, low, cap = bc.ARM_PIECES[side]; ball, _ = bc.ARM[side]
        if side in lower_map:
            # custom lower, no-fist or original, via limb_layer
            lay = limb_layer(lower_map[side], elbows[side], cfg["arm_lower"][side], (ball[0], 0))
            c.alpha_composite(lay)
        else:
            bc.limb(c, os.path.join(bc.CUT, low), elbows[side], cfg["arm_lower"][side], (ball[0], 0))
        bc.cap_at(c, os.path.join(bc.CUT, cap), elbows[side])
    bc.paste_at(c, bc.load(os.path.join(bc.BASE, "Neck.png"), scale=1.05), cx, 360)
    head = bc.load(os.path.join(bc.BASE, "Head_Front.png"))
    if head_angle: head = head.rotate(head_angle, expand=True)
    c.alpha_composite(head, (int(cx-head.size[0]/2), int(331-head.size[1]/2)))
    for side in ("L", "R"):
        if side not in top_arms: continue
        ball, sh_anchor = bc.ARM[side]; vec = (ball[0]-sh_anchor[0], ball[1]-sh_anchor[1]); up, low, cap = bc.ARM_PIECES[side]; sh = shoulders[side]
        bc.limb(c, os.path.join(bc.CUT, up), sh, cfg["arm_upper"][side], sh_anchor)
        elbow = (sh[0]+bc.rot_vec(vec, cfg["arm_upper"][side])[0]*SCALE, sh[1]+bc.rot_vec(vec, cfg["arm_upper"][side])[1]*SCALE)
        if side in lower_map:
            lay = limb_layer(lower_map[side], elbow, cfg["arm_lower"][side], (ball[0], 0))
            c.alpha_composite(lay)
        else:
            bc.limb(c, os.path.join(bc.CUT, low), elbow, cfg["arm_lower"][side], (ball[0], 0))
        bc.cap_at(c, os.path.join(bc.CUT, cap), elbow)
    return c

def render_custom(cfg, head=0, top=(), dx=0, dy=0, lower_map=None):
    c = Image.new("RGBA", (1100, 1500), (0,0,0,0))
    figure_custom(c, 550, cfg, head, top, lower_map)
    if dx or dy:
        d = Image.new("RGBA", (1100, 1500), (0,0,0,0)); d.alpha_composite(c, (dx, dy)); return d
    return c

def elbow_for(side, cfg):
    sh = {"L": (550-120, 445), "R": (550+120, 445)}[side]
    ball, sh_anchor = bc.ARM[side]; vec = (ball[0]-sh_anchor[0], ball[1]-sh_anchor[1])
    return (sh[0]+bc.rot_vec(vec, cfg["arm_upper"][side])[0]*SCALE,
            sh[1]+bc.rot_vec(vec, cfg["arm_upper"][side])[1]*SCALE)

def flipped_fist_layer(side, cfg):
    """Return (flipped_layer, wrist_master, fist_bbox_master, orig_bbox_master)."""
    elbow = elbow_for(side, cfg)
    ball, _ = bc.ARM[side]
    # original lower layer alone, rotated
    lay = limb_layer(LOWER_ORIG[side], elbow, cfg["arm_lower"][side], (ball[0], 0))
    arr = np.array(lay)
    alpha = arr[:,:,3] > 10
    # arm direction (unit, rot_vec preserves length)
    ad = bc.rot_vec((0,1), cfg["arm_lower"][side])
    # wrist distance from elbow, piece-local
    dx = WRIST_CX[side]-ball[0]; dy = SPLIT[side]
    wrist_dist = math.hypot(dx*SCALE, dy*SCALE)
    # projection of each pixel onto arm direction, from elbow
    ys, xs = np.where(alpha)
    vx = xs - elbow[0]; vy = ys - elbow[1]
    proj = vx*ad[0] + vy*ad[1]
    fist_mask = np.zeros_like(alpha); fist_mask[ys, xs] = proj >= (wrist_dist-2)
    fist = Image.new("RGBA", lay.size, (0,0,0,0))
    fa = np.array(fist); fa[fist_mask] = arr[fist_mask]; fist = Image.fromarray(fa, "RGBA")
    # wrist point, master coords
    wrist = (elbow[0]+ad[0]*wrist_dist, elbow[1]+ad[1]*wrist_dist)
    # flip full layer top-bottom, then re-seat wrist
    flipped = fist.transpose(Image.FLIP_TOP_BOTTOM)
    wrist_flipped_y = (lay.size[1]-1) - wrist[1]
    shift_dy = int(round(wrist[1]-wrist_flipped_y))
    shifted = Image.new("RGBA", lay.size, (0,0,0,0))
    # paste with shift, handling negative / positive
    if shift_dy >= 0:
        shifted.alpha_composite(flipped, (0, shift_dy))
    else:
        # crop top part of flipped that would move out
        crop = flipped.crop((0, -shift_dy, flipped.size[0], flipped.size[1]))
        shifted.alpha_composite(crop, (0, 0))
    def bbox_of(im):
        a = np.array(im.getchannel("A")) > 10
        if not a.any(): return None
        yy, xx = np.where(a); return [int(xx.min()), int(yy.min()), int(xx.max()), int(yy.max())]
    return shifted, wrist, bbox_of(fist), bbox_of(shifted)

# --- replicate bc.build, capturing cfg/head/top/dx/dy per frame ---
keys = bc.JUMP_KEYS
for k in keys:
    if k["name"] in ("jump takeoff", "jump tuck apex"):
        k["top"] = ("L", "R")
# recompute dy like bc.build does
for k in keys:
    target_h = k.get("target_h", -k["dy"]//2)
    bottom0 = bc.measure_bottom(k["cfg"], k["head"], k["top"])
    k["dy"] = 2*((bc.GROUND_Y-target_h)-bottom0)
    k["height_video_px"] = target_h

captured = []  # per frame: cfg copy, head, top, dx, dy, kind, from, to
def add_frame(cfg, head, top, dx, dy, note, frm, to, t, e, height=None):
    captured.append({"cfg": {g: dict(cfg[g]) for g in cfg}, "head": head, "top": tuple(top),
                     "dx": dx, "dy": dy, "kind": note, "from": frm, "to": to, "height": height})
def transition(a, b):
    deltas = {s: abs(b["cfg"]["arm_upper"][s]-a["cfg"]["arm_upper"][s]) for s in ("L", "R")}
    big = max(deltas, key=deltas.get)
    for j in range(1, 8):
        t = j/8; e = bc.ease(t); cfg = bc.lerp_cfg(a["cfg"], b["cfg"], e)
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
# overshoot + settle + return (bc.build, non-cycle)
prev, last = keys[-2], keys[-1]
over = {g: dict(last["cfg"][g]) for g in last["cfg"]}
for g in ("arm_upper", "arm_lower"):
    for side in ("L", "R"):
        over[g][side] = prev["cfg"][g][side] + (last["cfg"][g][side]-prev["cfg"][g][side])*1.05
add_frame(over, last["head"], last["top"], last["dx"], last["dy"], "OVERSHOOT 5% beyond key", prev["name"], last["name"], 1.05, 1.05, height=last.get("height_video_px", 0))
add_frame(last["cfg"], last["head"], last["top"], last["dx"], last["dy"], "SETTLE back to key", last["name"], last["name"], 1.0, 1.0, height=last.get("height_video_px", 0))
transition(last, keys[0]); hold(keys[0])
print("captured frames", len(captured))
assert len(captured) == 62, len(captured)

# render
import shutil
orig_dir = "/home/hatch/workspace/cape-jones-rig/jump-chain-fix-20261101/frames/chain-jump-fixed"
gates = {"flipped_frames": [], "unchanged_frames": [], "wrist": {}, "fist_bbox": {}}
video_frames = []
for i, fr in enumerate(captured):
    is_arms_up = ("L" in fr["top"] and "R" in fr["top"])
    if is_arms_up:
        base = render_custom(fr["cfg"], fr["head"], fr["top"], fr["dx"], fr["dy"], lower_map=LOWER_NOFIST)
        wrists = {}
        for side in ("L", "R"):
            shifted, wrist, ob, nb = flipped_fist_layer(side, fr["cfg"])
            base.alpha_composite(shifted)
            wrists[side] = {"wrist_master": [round(v,1) for v in wrist], "orig_fist_bbox_master": ob, "flipped_fist_bbox_master": nb}
        gates["flipped_frames"].append(i); gates["wrist"][i] = wrists
        vf = bc.video_frame(base)
    else:
        # original jump-fix video frame, copied exactly
        src = os.path.join(orig_dir, f"chain-jump-fixed-{i:03d}.jpg")
        vf = Image.open(src).convert("RGB")
        gates["unchanged_frames"].append(i)
    video_frames.append(vf)
    vf.save(os.path.join(FR, f"jump-hands-flipped-{i:03d}.jpg"), quality=92)
print("flipped", gates["flipped_frames"])
print("unchanged", gates["unchanged_frames"])

# contacts + apex
from PIL import ImageDraw
# apex frame: find a tuck-apex hold frame — frame 32 in jump-fix
apex = video_frames[32]
orig_apex = Image.open(os.path.join(orig_dir, "chain-jump-fixed-032.jpg")).convert("RGB")
contact = Image.new("RGB", (1100, 800), (128,128,128))
contact.paste(orig_apex.resize((550,375)), (0,0)); contact.paste(apex.resize((550,375)), (550,0))
d = ImageDraw.Draw(contact)
d.text((10,380), "LEFT: jump-fix apex f32 (hands NOT flipped)", fill=(255,255,255))
d.text((560,380), "RIGHT: NEW apex f32 (hands 1+2 VERTICAL FLIP IN PLACE)", fill=(255,255,0))
# zoom crops around hands centre, video coords approx x 400-700, y 50-300
for (src, x0, label) in [(orig_apex, 0, "old hands zoom"), (apex, 550, "new hands zoom")]:
    crop = src.crop((380, 20, 720, 320)).resize((550, 265), Image.LANCZOS)
    contact.paste(crop, (x0, 410))
    d.text((x0+10, 680), label, fill=(255,255,255))
contact.save(os.path.join(OUT, "contacts-apex-old-vs-new-flipped-20261101.png"))
# full contact 10 tiles like bc
sheet = Image.new("RGB", (1100, 470), (128,128,128)); dd = ImageDraw.Draw(sheet)
idx = sorted(set([int(i*(len(video_frames)-1)/9) for i in range(10)]))
for k, ix in enumerate(idx):
    tile = video_frames[ix].resize((220,150)); x, y = (k%5)*220, (k//5)*235
    sheet.paste(tile, (x,y)); dd.text((x+4, y+152), f"f{ix:03d} {captured[ix]['kind'][:28]}", fill=(255,255,255))
sheet.save(os.path.join(OUT, "jump-hands-flipped-contact-20261101.png"))

# no-crop + diff gates
def video_bbox(im):
    a = np.array(im.convert("RGB")).astype(int); sil = (np.abs(a-128).sum(axis=2) > 40)
    ys, xs = np.where(sil); return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None
diffs = {}
for i in range(62):
    a = np.array(Image.open(os.path.join(orig_dir, f"chain-jump-fixed-{i:03d}.jpg")).convert("RGB")).astype(int)
    b = np.array(video_frames[i].convert("RGB")).astype(int)
    diffs[i] = int(((np.abs(a-b).sum(axis=2) > 30)).sum())
gates["diff_px_vs_jumpfix"] = diffs
gates["apex_bbox_new_video"] = video_bbox(apex)
gates["apex_bbox_old_video"] = video_bbox(orig_apex)
json.dump(gates, open(os.path.join(OUT, "gates-20261101.json"), "w"), indent=1)
print("diff flipped min/max", min(diffs[i] for i in gates["flipped_frames"]), max(diffs[i] for i in gates["flipped_frames"]))
print("diff unchanged max", max(diffs[i] for i in gates["unchanged_frames"]))
print("apex bbox old/new", gates["apex_bbox_old_video"], gates["apex_bbox_new_video"])

# encode videos
def encode(frames_list, fps, out_mp4, out_gif):
    txt = os.path.join(OUT, f"frames-{fps}.txt")
    with open(txt, "w") as fh:
        for i in range(len(frames_list)): fh.write(f"file '{FR}/jump-hands-flipped-{i:03d}.jpg'\n")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-r", str(fps),
                    "-i", txt, "-vf", "scale=1100:750", "-c:v", "libx264", "-pix_fmt", "yuv420p", out_mp4], check=True)
    small = [f.resize((550,375)) for f in frames_list]
    small[0].save(out_gif, save_all=True, append_images=small[1:], duration=int(1000/fps), loop=0)
encode(video_frames, 24, os.path.join(OUT, "jump-hands-flipped-1x-20261101.mp4"), os.path.join(OUT, "jump-hands-flipped-20261101.gif"))
encode(video_frames, 48, os.path.join(OUT, "jump-hands-flipped-2x-20261101.mp4"), os.path.join(OUT, "jump-hands-flipped-2x-20261101.gif"))
encode(video_frames, 72, os.path.join(OUT, "jump-hands-flipped-3x-20261101.mp4"), os.path.join(OUT, "jump-hands-flipped-3x-20261101.gif"))
print("DONE", len(video_frames))
