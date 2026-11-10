"""Size-transformation power + coming-forward walking template.
FEET-PLANTED RULE (core): the figure layer is transparent; every frame is
anchored by its own alpha bbox bottom, pasted so bbox bottom == GROUND_Y.
Scaling grows upward from the feet, never from the centre, never from the
plate bottom (plate margins are transparent and must not be the anchor).
NO-CROP RULE: canvas 1600x1800 fits the LARGEST (giant) figure with margin;
gate fails if any alpha touches a canvas edge.
Methods wired (see METHODS table in report):
 1. Perspective scaling / depth cueing (depth-by-scale, extended)
 2. Multiplane parallax (background blocks move at 0.3x figure scale change)
 3. Disney squash & stretch (subtle width squash mid-growth, feet unaffected)
 4. Walk-cycle contact / passing / down / up positions (Williams)
 5. 2D foot-plant anchor (stance-foot bbox bottom locked; NOT a true IK solver)
"""
import os, sys, math, json, importlib.util
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

RIG = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(RIG, "size-transformation-power-20261031")
os.makedirs(os.path.join(OUT, "frames-size"), exist_ok=True)
os.makedirs(os.path.join(OUT, "frames-walk"), exist_ok=True)

W, H = 1600, 1800
GROUND_Y = 1500
GREY = (128, 128, 128)
# Hero (scale 1.0) figure display height: 700px. Giant 2.0 -> 1400px, top=100.
HERO_H = 700

spec = importlib.util.spec_from_file_location(
    "snap", os.path.join(RIG, "face-cowl-snap-wire100-20261031", "snap_figure.py"))
snap = importlib.util.module_from_spec(spec); spec.loader.exec_module(snap)

def alpha_bbox(im):
    a = np.array(im.split()[3])
    rows = np.where(a.max(axis=1) > 10)[0]
    cols = np.where(a.max(axis=0) > 10)[0]
    return int(cols.min()), int(rows.min()), int(cols.max()), int(rows.max())

def anchor_layer(fig, scale, squash_x=1.0):
    """Return transparent layer W x H with fig scaled and feet on GROUND_Y."""
    # Scale whole plate so figure height == HERO_H * scale
    bx0, by0, bx1, by1 = alpha_bbox(fig)
    fig_h = by1 - by0 + 1
    plate_scale = (HERO_H * scale) / fig_h
    nw = max(1, int(fig.size[0] * plate_scale * squash_x))
    nh = max(1, int(fig.size[1] * plate_scale))
    scaled = fig.resize((nw, nh), Image.LANCZOS)
    sx0, sy0, sx1, sy1 = alpha_bbox(scaled)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cx = W // 2 - (sx0 + sx1) // 2
    top = GROUND_Y - sy1
    layer.alpha_composite(scaled, (cx, top))
    # measured feet y = bbox bottom of the placed layer
    lx0, ly0, lx1, ly1 = alpha_bbox(layer)
    return layer, {"feet_y": ly1, "bbox": [lx0, ly0, lx1, ly1],
                   "touches_edge": (lx0 <= 0 or ly0 <= 0 or lx1 >= W - 1 or ly1 >= H - 1),
                   "margin": min(lx0, ly0, W - 1 - lx1, H - 1 - ly1)}

def background(scale, cx_shift=0):
    """Grey video background + ground plane + distant blocks at 0.3x parallax.
    Proof-only ground line is drawn separately; this bg has a plain ground line
    (a scene element, not a debug marker)."""
    bg = Image.new("RGB", (W, H), GREY)
    d = ImageDraw.Draw(bg)
    # sky-to-ground split is just the ground line + a darker ground band
    d.rectangle([0, GROUND_Y, W, H], fill=(96, 96, 96))
    d.line([(0, GROUND_Y), (W, GROUND_Y)], fill=(255, 255, 255), width=3)
    # distant blocks: parallax 0.3 -- they drift outward 0.3x the figure's growth
    drift = int((scale - 1.0) * 0.3 * 400)
    for i, bx in enumerate([150, 450, 1050, 1350]):
        bw = 120 + 40 * (i % 2)
        x = bx - drift if bx < W // 2 else bx + drift
        d.rectangle([x, GROUND_Y - 180, x + bw, GROUND_Y], fill=(150, 150, 150))
    return bg

def compose(layer, scale):
    bg = background(scale).convert("RGBA")
    return Image.alpha_composite(bg, layer).convert("RGB")

def smooth(t):
    return t * t * (3 - 2 * t)  # smoothstep slow-in / slow-out

def interp_cfg(a, b, t):
    return {k: {s: a[k][s] + (b[k][s] - a[k][s]) * smooth(t) for s in ("L", "R")}
            for k in a}

def save_gif_mp4(frames_rgb, stem, fps=24):
    gif = os.path.join(OUT, stem + ".gif")
    frames_rgb[0].save(gif, save_all=True, append_images=frames_rgb[1:],
                       duration=int(1000 / fps), loop=0)
    import subprocess, tempfile
    with tempfile.TemporaryDirectory() as td:
        for i, f in enumerate(frames_rgb):
            f.save(os.path.join(td, f"f{i:03d}.jpg"), quality=92)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps),
                        "-i", os.path.join(td, "f%03d.jpg"),
                        "-vf", f"scale={W}:{H},format=yuv420p", "-c:v", "libx264",
                        os.path.join(OUT, stem + ".mp4")], check=True)
    print(stem, len(frames_rgb), "frames")

def contact(frames_rgb, path, cols=6):
    rows = math.ceil(len(frames_rgb) / cols)
    tw, th = W // cols, H // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), GREY)
    for i, f in enumerate(frames_rgb):
        sheet.paste(f.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
    sheet.save(path)
    return sheet

def proof_with_ground(frames_rgb, path, label):
    """Proof only: red ground line + feet marker, NOT on the clean composite."""
    proof = frames_rgb[len(frames_rgb) // 2].copy()
    d = ImageDraw.Draw(proof)
    d.line([(0, GROUND_Y), (W, GROUND_Y)], fill=(255, 0, 0), width=5)
    d.text((20, 20), label, fill=(255, 255, 0))
    d.text((20, 60), f"ground line y={GROUND_Y} (red, proof only)", fill=(255, 255, 0))
    proof.save(path)

# ---------------- 1. SIZE-TRANSFORMATION POWER ----------------
APOSE = {"arm_upper": {"L": 0, "R": 0}, "arm_lower": {"L": 0, "R": 0},
         "leg_upper": {"L": 0, "R": 0}, "leg_lower": {"L": 0, "R": 0}}
apose = snap.figure(550, APOSE)

# Key scales with segment frame counts: (scale, frames, label)
segments = [(0.5, 6, "SMALL-HOLD"), (1.0, 12, "GROW-TO-NORMAL"),
            (2.0, 12, "GROW-TO-GIANT"), (2.0, 6, "GIANT-HOLD"),
            (1.0, 12, "SHRINK-TO-NORMAL"), (1.0, 6, "NORMAL-HOLD")]
size_frames, size_meas = [], []
cur = 0.5
for target, n, label in segments:
    start = cur
    for i in range(n):
        t = (i + 1) / n if n > 1 else 1.0
        s = start + (target - start) * smooth(t) if target != start else target
        # Disney squash: width dips to 0.97 mid-segment, back to 1.0 at keys
        squash_x = 1.0 - 0.05 * math.sin(math.pi * t) if target != start else 1.0
        layer, m = anchor_layer(apose, s, squash_x=squash_x)
        size_frames.append(compose(layer, s))
        m.update({"frame": len(size_frames) - 1, "scale": round(s, 4),
                  "squash_x": round(squash_x, 4), "phase": label})
        size_meas.append(m)
    cur = target
save_gif_mp4(size_frames, "size-transformation-power-20261031")
contact(size_frames, os.path.join(OUT, "size-transformation-power-contact-20261031.png"))
proof_with_ground(size_frames, os.path.join(OUT, "size-transformation-power-proof-ground-20261031.png"),
                   "SIZE POWER: feet on red ground line at every scale (proof only)")
# Clean transparent plates at small / giant extremes
for name, s in [("size-small-20261031.png", 0.5), ("size-giant-20261031.png", 2.0)]:
    layer, _ = anchor_layer(apose, s)
    layer.save(os.path.join(OUT, name))
for i, f in enumerate(size_frames):
    f.save(os.path.join(OUT, "frames-size", f"f{i:03d}.jpg"), quality=92)

# ---------------- 2. COMING-FORWARD WALK ----------------
CONTACT_L = {"arm_upper": {"L": 20, "R": -20}, "arm_lower": {"L": -30, "R": 30},
             "leg_upper": {"L": -28, "R": 22}, "leg_lower": {"L": 5, "R": 15}}
PASSING = {"arm_upper": {"L": 0, "R": 0}, "arm_lower": {"L": -10, "R": 10},
           "leg_upper": {"L": 0, "R": 5}, "leg_lower": {"L": 15, "R": 5}}
CONTACT_R = {"arm_upper": {"L": -20, "R": 20}, "arm_lower": {"L": 30, "R": -30},
             "leg_upper": {"L": 22, "R": -28}, "leg_lower": {"L": 15, "R": 5}}
# Walk keys in order, with a scale that grows as he comes forward.
# Last key returns to CONTACT_L so the cycle loops; scale keeps growing to 1.6.
walk_keys = [(CONTACT_L, 0.70, "CONTACT-L"), (PASSING, 0.95, "PASSING"),
             (CONTACT_R, 1.20, "CONTACT-R"), (PASSING, 1.40, "PASSING"),
             (CONTACT_L, 1.60, "CONTACT-L")]
walk_frames, walk_meas = [], []
SEG = 10
for ki in range(len(walk_keys) - 1):
    cfg_a, s_a, lab_a = walk_keys[ki]
    cfg_b, s_b, lab_b = walk_keys[ki + 1]
    for i in range(SEG):
        t = i / SEG
        cfg = interp_cfg(cfg_a, cfg_b, t)
        s = s_a + (s_b - s_a) * smooth(t)
        fig = snap.figure(550, cfg)
        layer, m = anchor_layer(fig, s)
        walk_frames.append(compose(layer, s))
        phase = lab_a if i == 0 else ("INBETWEEN" if i < SEG else lab_b)
        # Down/up: frames just after contact read as DOWN, mid-segment as UP
        if i == 2:
            phase = "DOWN"
        elif i == 5:
            phase = "UP"
        m.update({"frame": len(walk_frames) - 1, "scale": round(s, 4),
                  "phase": phase, "from": lab_a, "to": lab_b})
        walk_meas.append(m)
# Final key hold, 4 frames at CONTACT-L, scale 1.60
fig = snap.figure(550, CONTACT_L)
for _ in range(4):
    layer, m = anchor_layer(fig, 1.60)
    walk_frames.append(compose(layer, 1.60))
    m.update({"frame": len(walk_frames) - 1, "scale": 1.60,
              "phase": "CONTACT-L-HOLD", "from": "CONTACT-L", "to": "CONTACT-L"})
    walk_meas.append(m)
save_gif_mp4(walk_frames, "coming-forward-walk-20261031")
contact(walk_frames, os.path.join(OUT, "coming-forward-walk-contact-20261031.png"))
proof_with_ground(walk_frames, os.path.join(OUT, "coming-forward-walk-proof-ground-20261031.png"),
                   "COMING-FORWARD: stance foot on red ground line each step (proof only)")
for i, f in enumerate(walk_frames):
    f.save(os.path.join(OUT, "frames-walk", f"f{i:03d}.jpg"), quality=92)

# ---------------- Measurements + gate ----------------
def gate(meas, name):
    feet = [m["feet_y"] for m in meas]
    touches = [m["frame"] for m in meas if m["touches_edge"]]
    return {"template": name, "frames": len(meas),
            "feet_y_min": min(feet), "feet_y_max": max(feet),
            "feet_y_spread_px": max(feet) - min(feet),
            "feet_y_all": feet,
            "touches_edge_frames": touches,
            "min_margin_px": min(m["margin"] for m in meas),
            "PASS": (max(feet) - min(feet) <= 1) and not touches}

report = {
    "power": "SIZE-TRANSFORMATION",
    "templates": {
        "size_transformation": {
            "scales": [0.5, 1.0, 2.0, 1.0], "frames": len(size_frames), "fps": 24,
            "easing": "smoothstep slow-in/slow-out per segment",
            "squash_x": "1.0 at keys, 0.95 mid-growth segment (Disney squash, feet unaffected)",
            "canvas": [W, H], "ground_y": GROUND_Y, "hero_height_px": HERO_H,
            "gate": gate(size_meas, "size_transformation"),
        },
        "coming_forward_walk": {
            "keys": ["CONTACT-L@0.70", "PASSING@0.95", "CONTACT-R@1.20",
                     "PASSING@1.40", "CONTACT-L@1.60", "CONTACT-L-HOLD@1.60"],
            "frames": len(walk_frames), "fps": 24,
            "easing": "smoothstep rig-angle interpolation between walk keys",
            "canvas": [W, H], "ground_y": GROUND_Y, "hero_height_px": HERO_H,
            "gate": gate(walk_meas, "coming_forward_walk"),
        },
    },
    "feet_planted_rule": "Every frame anchored by its own alpha bbox bottom == ground_y; "
                          "scaling grows upward from the feet, never from centre or plate bottom.",
    "no_crop_rule": "Canvas 1600x1800 fits giant (2.0x) with margin; gate fails on edge touch.",
    "background_note": "GIF/MP4 are on grey-128 video background for playback; the figure "
                       "layer itself is transparent (see clean PNG plates). Ground-line "
                       "red marker appears on proof images only, never on clean composites.",
    "methods": [
        {"name": "Perspective scaling / depth cueing", "source": "depth-by-scale test, scale=1.0+0.25*Z, extended to power scale 0.5-2.0",
         "wired": "anchor_layer() scale parameter, measured feet_y per frame", "run": "real"},
        {"name": "Multiplane parallax", "source": "depth test multiplane camera, far 0.3 / cape 1.0 / foreground 1.8",
         "wired": "background() distant blocks drift at 0.3x figure scale change", "run": "real (simple blocks, not a full multiplane render)"},
        {"name": "Disney squash and stretch", "source": "Disney 12 principles",
         "wired": "width squash 0.95 mid-growth segment, feet anchor recomputed after squash", "run": "real"},
        {"name": "Walk-cycle contact / passing / down / up", "source": "Williams, Animator's Survival Kit walk positions",
         "wired": "walk keys CONTACT-L/PASSING/CONTACT-R + DOWN/UP phase labels in measurements", "run": "real (rig-angle interpolation, not hand-drawn keys)"},
        {"name": "2D foot-plant anchor (IK-style, not a solver)", "source": "foot-locking / IK foot plant concept, 2D anchor method",
         "wired": "bbox-bottom anchor to ground_y every frame; stance foot is bbox bottom", "run": "real, labelled NOT a true IK solver"},
    ],
    "honest_limits": [
        "Walk keys are rig-angle configs written for this template, not measured from an existing walk clip; the walk clips on disk are RGB full-canvas, not transparent rig poses, so they could not be used as keys.",
        "Coming-forward has no true walk-cycle keys from the sheets and no background parallax render beyond simple blocks; background parallax for a full scene is still owed.",
        "MP4/GIF use a grey video background; only the figure layer and the two clean PNG plates are transparent.",
    ],
    "size_measurements": size_meas,
    "walk_measurements": walk_meas,
}
with open(os.path.join(OUT, "size-transformation-measurements-20261031.json"), "w") as fh:
    json.dump(report, fh, indent=2)
print(json.dumps({k: v["gate"] for k, v in report["templates"].items()}, indent=2))
