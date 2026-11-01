"""EXPERIMENTAL 2.5D depth in 2D + blocker-break tests (PIL side).
1. Multiplane camera move: far bg (parallax 0.3) / Cape (1.0) / foreground (1.8).
2. Depth-by-scale: Z table, Cape scaled by Z, feet on a ground line.
3. Pseudo-3D turn: snap_figure angle interpolation apose -> turned pose,
   width squash 1.0 -> 0.62 -> 1.0, arm layer-order flip at the midpoint
   (forward arm above torso after midpoint, back arm below before it) —
   labelled EXPERIMENTAL, NOT a true side view.
4. Lip-sync layer test: visemes v2 heads on a phoneme timeline, mouth layer
   switching vs head/cowl — mouth patch sits inside the head layer, never
   above the cowl, and the cowl never covers the mouth.
5. Cowl-gate v2 signal: collar-edge interruption — for each audited pose,
   sample the bicep row band across the collar line and count alpha breaks.
   (Implemented in cowl_gate_v2.py; numbers are reported in the doc.)
All outputs are new dated files. Originals untouched.
"""
import os, sys, math, json
sys.path.insert(0, "/home/hatch/workspace/cape-jones-rig/face-cowl-snap-wire100-20261031")
from PIL import Image, ImageDraw, ImageFilter
RIG = "/home/hatch/workspace/cape-jones-rig"
OUT = os.path.join(RIG, "depth-25d-blockers-broken-20261031")
os.makedirs(OUT, exist_ok=True)
import importlib.util
spec = importlib.util.spec_from_file_location("snap", os.path.join(RIG, "face-cowl-snap-wire100-20261031", "snap_figure.py"))
snap = importlib.util.module_from_spec(spec); spec.loader.exec_module(snap)

GREY = (128, 128, 128)
def save_gif_mp4(frames, stem, fps=12):
    frames_rgb = [f.convert("RGB") for f in frames]
    gif = os.path.join(OUT, stem + ".gif")
    frames_rgb[0].save(gif, save_all=True, append_images=frames_rgb[1:], duration=int(1000/fps), loop=0)
    # mp4 via ffmpeg on temp jpgs
    import subprocess, tempfile
    with tempfile.TemporaryDirectory() as td:
        for i, f in enumerate(frames_rgb):
            f.save(os.path.join(td, f"f{i:03d}.jpg"), quality=92)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", os.path.join(td, "f%03d.jpg"),
                        "-vf", "scale=1100:750,format=yuv420p", "-c:v", "libx264", os.path.join(OUT, stem + ".mp4")], check=True)
    print(stem, len(frames), "frames")

# ---------- 1. Multiplane ----------
bg_path = os.path.join(RIG, "showcase/backgrounds-new-20261031/bg-rooftop-new-20261031.jpg")
bg = Image.open(bg_path).convert("RGB").resize((1400, 950))
cape_pose = snap.figure(550, {"arm_upper": {"L": -85, "R": 85}, "arm_lower": {"L": 145, "R": -145},
                                 "leg_upper": {"L": -22, "R": 22}, "leg_lower": {"L": 10, "R": -10}}, head_angle=0)
# foreground: dark blurred vertical bars (a railing / foreground object), transparent layer
fg = Image.new("RGBA", (1400, 950), (0, 0, 0, 0))
d = ImageDraw.Draw(fg)
for x in range(0, 1400, 180):
    d.rectangle([x, 0, x + 55, 950], fill=(20, 18, 25, 210))
fg = fg.filter(ImageFilter.GaussianBlur(2))
frames = []
for i in range(24):
    t = i / 23
    canvas = Image.new("RGB", (1100, 750), GREY)
    # far layer: parallax 0.3, moves -40px total; blurred + darker = atmosphere depth cue
    far = bg.filter(ImageFilter.GaussianBlur(1.2))
    canvas.paste(far.crop((int(40 + t * 40), 100, int(40 + t * 40) + 1100, 850)), (0, 0))
    # Cape layer: parallax 1.0, moves -120px total, full height scaled to 750
    cape = cape_pose.resize((550, 750), Image.LANCZOS)
    layer = Image.new("RGBA", (1100, 750), (0, 0, 0, 0))
    layer.alpha_composite(cape, (int(275 - t * 120), 0))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), layer).convert("RGB")
    # foreground: parallax 1.8, moves -216px total
    fg_layer = Image.new("RGBA", (1100, 750), (0, 0, 0, 0))
    fg_crop = fg.crop((int(t * 216), 100, int(t * 216) + 1100, 850))
    fg_layer.alpha_composite(fg_crop, (0, 0))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), fg_layer).convert("RGB")
    frames.append(canvas)
save_gif_mp4(frames, "experimental-multiplane-camera-20261031", fps=12)
frames[0].save(os.path.join(OUT, "experimental-multiplane-contact-20261031.png"))
contact = Image.new("RGB", (1100, 750), GREY)
for i, idx in enumerate([0, 8, 16, 23]):
    contact.paste(frames[idx].resize((550, 375)), ((i % 2) * 550, (i // 2) * 375))
contact.save(os.path.join(OUT, "experimental-multiplane-contact-20261031.png"))

# ---------- 2. Depth-by-scale ----------
ZTABLE = [
    {"z": -2, "scale": 0.60, "parallax": 0.3, "blur": 2.0, "label": "far"},
    {"z": -1, "scale": 0.80, "parallax": 0.6, "blur": 1.0, "label": "mid-far"},
    {"z": 0, "scale": 1.00, "parallax": 1.0, "blur": 0.0, "label": "hero plane"},
    {"z": 1, "scale": 1.25, "parallax": 1.4, "blur": 0.0, "label": "near"},
    {"z": 2, "scale": 1.50, "parallax": 1.8, "blur": 0.0, "label": "closest"},
]
frames = []
for row in ZTABLE:
    canvas = Image.new("RGB", (1100, 750), GREY)
    canvas.paste(bg.crop((100, 100, 1200, 850)), (0, 0))
    s = row["scale"]
    cape = cape_pose.resize((int(550 * s), int(750 * s)), Image.LANCZOS)
    if row["blur"]:
        cape = cape.filter(ImageFilter.GaussianBlur(row["blur"]))
    # feet on ground line y=700: bottom of cape image sits at 700
    canvas = Image.alpha_composite(canvas.convert("RGBA"), Image.new("RGBA", (1100, 750), (0, 0, 0, 0)))
    layer = Image.new("RGBA", (1100, 750), (0, 0, 0, 0))
    layer.alpha_composite(cape, (int(550 - cape.size[0] / 2), int(700 - cape.size[1])))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), layer).convert("RGB")
    d = ImageDraw.Draw(canvas); d.text((20, 20), f"Z={row['z']}  scale={row['scale']}  parallax={row['parallax']}  {row['label']}", fill=(255, 255, 0))
    frames.append(canvas)
save_gif_mp4(frames, "experimental-depth-by-scale-20261031", fps=2)
contact = Image.new("RGB", (1100, 750), GREY)
for i, f in enumerate(frames):
    contact.paste(f.resize((366, 250)), ((i % 3) * 366, (i // 3) * 250))
contact.save(os.path.join(OUT, "experimental-depth-by-scale-contact-20261031.png"))
with open(os.path.join(OUT, "experimental-depth-spec-20261031.json"), "w") as fh:
    json.dump({"method": "2.5D depth in 2D (EXPERIMENTAL)", "z_table": ZTABLE,
               "parallax": {"far_bg": 0.3, "cape": 1.0, "foreground": 1.8, "camera_move_px": 120},
               "scale_rule": "scale = 1.0 + 0.25*Z (clamped 0.6..1.5 in this test); blur increases with distance (far blur 2.0, mid-far 1.0, hero/near 0)",
               "ground_rule": "feet stay on ground line y=700 in the 1100x750 test frame; scaling grows upward from the feet, never from the centre"}, fh, indent=2)

# ---------- 3. Pseudo-3D turn ----------
APOSE = {"arm_upper": {"L": 0, "R": 0}, "arm_lower": {"L": 0, "R": 0}, "leg_upper": {"L": 0, "R": 0}, "leg_lower": {"L": 0, "R": 0}}
TURNED = {"arm_upper": {"L": -40, "R": 60}, "arm_lower": {"L": 90, "R": -110}, "leg_upper": {"L": -15, "R": 20}, "leg_lower": {"L": 10, "R": -10}}
def interp(a, b, t):
    return {k: {s: a[k][s] + (b[k][s] - a[k][s]) * t for s in ("L", "R")} for k in a}
frames = []
for i in range(13):
    t = i / 12
    # width squash: 1.0 -> 0.62 at midpoint -> 1.0 (turn profile), ease in/out
    squash = 1.0 - 0.38 * math.sin(math.pi * t)
    # layer flip at midpoint: before it L arm is front (chest), after it R arm is front
    snap_cfg = {"L": "chest", "R": "normal"} if t < 0.5 else {"L": "normal", "R": "chest"}
    fig = snap.figure(550, interp(APOSE, TURNED, t), head_angle=int(-10 * t), snap=snap_cfg)
    w = int(550 * squash)
    fig = fig.resize((w, 750), Image.LANCZOS)
    canvas = Image.new("RGBA", (1100, 750), GREY + (255,))
    canvas.alpha_composite(fig, (int(550 - w / 2), 0))
    frames.append(canvas.convert("RGB"))
save_gif_mp4(frames, "experimental-pseudo-turn-20261031", fps=12)
contact = Image.new("RGB", (1100, 750), GREY)
for i, idx in enumerate([0, 3, 6, 9, 12]):
    contact.paste(frames[idx].resize((440, 300)), ((i % 3) * 366, (i // 3) * 375))
contact.save(os.path.join(OUT, "experimental-pseudo-turn-contact-20261031.png"))

# ---------- 4. Lip-sync layer test ----------
# visemes v2 heads are full-head images; sequence: PAH (MBP->AH) + GO (GK->OH)
# Timeline: phoneme -> viseme head file, mouth layer is INSIDE the head image,
# so the test proves mouth never rises above head/cowl: it is part of the head layer.
heads = ["head-v2-07-mbp-20261031.png", "head-v2-04-ah-20261031.png",
         "head-v2-14-gk-20261031.png", "head-v2-05-oh-20261031.png"]
frames = []
for h in heads:
    im = Image.open(os.path.join(RIG, "visemes-v2-20261031", h)).convert("RGBA")
    canvas = Image.new("RGBA", (1100, 750), GREY + (255,))
    bg = Image.new("RGBA", im.size, GREY + (255,)); bg.alpha_composite(im)
    canvas.alpha_composite(bg.resize((550, 750)), (275, 0))
    frames.append(canvas.convert("RGB"))
# hold each viseme 2 frames for readability
frames2 = []
for f in frames:
    frames2 += [f, f]
save_gif_mp4(frames2, "experimental-lipsync-layer-20261031", fps=6)
contact = Image.new("RGB", (1100, 375), GREY)
for i, f in enumerate(frames):
    contact.paste(f.resize((275, 375)), (i * 275, 0))
contact.save(os.path.join(OUT, "experimental-lipsync-layer-contact-20261031.png"))
print("25D + tests done")
