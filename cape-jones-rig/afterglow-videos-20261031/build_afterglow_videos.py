"""Afterglow videos — Default Afterglow Preset, limb + per-shot.
Preset (approved 17:49 CDT): soft rim = soft halo, ONE layer, cyan (0,200,255)
default; dilate 6, blur 5; lag 6; fade 0.50/0.40/0.30/0.20/0.12/0.06;
hold decay 0.5 per frame -> visually zero at rest. Light-trail rule:
trail ONLY in motion, never static, zero at rest.
Punch video: approved v5 Arm2 FLIPPED forward-punch forearm (knuckles top,
unrotated) ONLY — limb-specific, not whole body. Path: windup -> snap extend
across-up (-110) -> impact hold (trail decays) -> recover -> rest hold (zero).
Shot videos: per CJ-01..CJ-30, trail colour = that shot's rim colour
(parsed from shot-specs JSON); plate = clean apose transparent plate.
Moving shots slide; hold/still shots hold with a decaying tail into the
hold (no NEW trail generated while still) and final frames at zero.
PIL generates trail layers + plate layers; Blender compositor composites
them (see blender_composite_afterglow.py) — Blender pass is separate.
"""
import json, re, os
from PIL import Image, ImageFilter
import numpy as np

R = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = f"{R}/afterglow-videos-20261031"
BG = (18, 18, 28, 255)
TRAIL = [0.50, 0.40, 0.30, 0.20, 0.12, 0.06]
W, H = 640, 360

def soft_band(alpha, dilate=6, blur=5):
    d = alpha.filter(ImageFilter.MaxFilter(dilate*2+1)).filter(ImageFilter.GaussianBlur(blur))
    band = np.clip(np.array(d, dtype=np.int16) - np.array(alpha, dtype=np.int16), 0, 255).astype(np.uint8)
    return Image.fromarray(band, "L")

def parse_rim(s):
    if isinstance(s, list) and len(s) >= 3:
        return tuple(int(x) for x in s[:3])
    if isinstance(s, str):
        m = re.findall(r"(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})", s)
        if m:
            return tuple(int(x) for x in m[0])
    return (0, 200, 255)

def trail_frame(canvas_bg, piece, positions, fi, color, hold_start=None):
    """positions: list of (x,y) per frame. Returns (trail_layer, plate_pos)."""
    canvas = Image.new("RGBA", (W, H), canvas_bg)
    a = piece.split()[3]
    band = soft_band(a)
    decay = 1.0
    if hold_start is not None and fi >= hold_start:
        decay = 0.5 ** (fi - hold_start + 1)
    for lag, f in enumerate(TRAIL, start=1):
        if fi - lag < 0:
            continue
        px, py = positions[fi - lag]
        glow = Image.new("RGBA", piece.size, (color[0], color[1], color[2], 0))
        glow.putalpha(band.point(lambda v: int(v * f * decay)))
        canvas.alpha_composite(glow, (px, py))
    return canvas

# ---------- PUNCH LIMB VIDEO ----------
fore = Image.open(f"{R}/forearm-fist-v5-correction-20261031/forearm-v5-arm2-forward-punch-flipped-20261031.png").convert("RGBA")
fw, fh = fore.size
scale = 200 / fw
fore_s = fore.resize((200, int(fh * scale)), Image.LANCZOS)
pw, ph = fore_s.size
# path (top-left of forearm piece): windup right/low -> snap left/up -> impact -> recover -> rest
punch_pos = [(400, 150), (400, 150), (400, 150),   # windup hold (no trail yet)
             (350, 125), (300, 100), (250, 75), (210, 60),  # snap extend
             (210, 60), (210, 60), (210, 60), (210, 60),    # impact hold, trail decays
             (260, 85), (320, 115), (380, 140),              # recover
             (380, 140), (380, 140), (380, 140), (380, 140)]  # rest hold, zero
assert len(punch_pos) == 18
punch_frames = []
for fi, (x, y) in enumerate(punch_pos):
    # hold decay starts at first impact-hold frame (index 7) and again at rest (14)
    decay = 1.0
    if 7 <= fi <= 10:
        decay = 0.5 ** (fi - 6)
    if fi >= 14:
        decay = 0.5 ** (fi - 13)
    canvas = Image.new("RGBA", (W, H), BG)
    a = fore_s.split()[3]; band = soft_band(a)
    for lag, f in enumerate(TRAIL, start=1):
        if fi - lag < 0: continue
        px, py = punch_pos[fi - lag]
        glow = Image.new("RGBA", (pw, ph), (0, 200, 255, 0))
        glow.putalpha(band.point(lambda v: int(v * f * decay)))
        canvas.alpha_composite(glow, (px, py))
    canvas.alpha_composite(fore_s, (x, y))
    punch_frames.append(canvas.convert("RGB"))
    canvas.save(f"{OUT}/frames_punch/punch-frame-{fi:02d}.png")
punch_frames[0].save(f"{OUT}/punch-limb-afterglow-20261031.gif", save_all=True,
                     append_images=punch_frames[1:], duration=100, loop=0)
# contact: windup, snap mid, impact, rest
sheet = Image.new("RGB", (640*4+30, 360+40), (255, 255, 255))
for i, idx in enumerate([2, 5, 7, 17]):
    sheet.paste(punch_frames[idx], (i*650, 20))
sheet.save(f"{OUT}/punch-limb-afterglow-contact-20261031.png")
print("punch frames", len(punch_frames))

# ---------- PER-SHOT VIDEOS ----------
plate = Image.open(f"{R}/rig-apose-v7c-clean-transparent.png").convert("RGBA")
w, h = plate.size; nw = int(w * 300 / h); plate = plate.resize((nw, 300), Image.LANCZOS)
pw2, ph2 = plate.size
specs = json.load(open(f"{R}/clean-100-20261031/shots/shot-specs-30-20261031.json"))["shots"]
moving = {"CJ-02","CJ-05","CJ-06","CJ-07","CJ-08","CJ-09","CJ-10","CJ-11","CJ-12",
          "CJ-13","CJ-14","CJ-15","CJ-21","CJ-22","CJ-04"}
results = []
for s in specs:
    sid, slug = s["shot_id"], s["slug"]
    color = parse_rim(s.get("rim_color"))
    if sid in moving:
        xs = [60 + i*24 for i in range(6)] + [204]*6
    else:
        xs = [180]*12  # hold: no new trail; tail decays into hold
    pos = [(x, 30) for x in xs]
    frames = []
    for fi, (x, y) in enumerate(pos):
        decay = 1.0
        if fi >= 6:
            decay = 0.5 ** (fi - 5)
        canvas = Image.new("RGBA", (W, H), BG)
        a = plate.split()[3]; band = soft_band(a)
        for lag, f in enumerate(TRAIL, start=1):
            if fi - lag < 0: continue
            px, py = pos[fi - lag]
            glow = Image.new("RGBA", (pw2, ph2), (color[0], color[1], color[2], 0))
            glow.putalpha(band.point(lambda v: int(v * f * decay)))
            canvas.alpha_composite(glow, (px, py))
        canvas.alpha_composite(plate, (x, y))
        frames.append(canvas.convert("RGB"))
    d = f"{OUT}/frames_shots/{sid}"
    os.makedirs(d, exist_ok=True)
    for fi, fr in enumerate(frames):
        fr.save(f"{d}/{sid}-frame-{fi:02d}.png")
    frames[0].save(f"{OUT}/{sid}-{slug}-afterglow-20261031.gif", save_all=True,
                   append_images=frames[1:], duration=100, loop=0)
    # measure on-screen trail colour: sample brightest trail pixel in frame 5 (moving) or frame 2 tail
    results.append({"shot_id": sid, "slug": slug, "rim_input": color,
                    "moving": sid in moving, "frames": len(frames),
                    "lighting": s["lighting_level"], "god_ray": s["god_ray_decision"][:60]})
    print(sid, slug, color, "moving" if sid in moving else "hold")
json.dump(results, open(f"{OUT}/shot-afterglow-index-20261031.json", "w"), indent=1)
print("shots done", len(results))
