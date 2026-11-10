#!/usr/bin/env python3
"""Extra industry-standard wiring, all PIL/FFmpeg, all viewed outputs:
onion skin, motion smear, squash & stretch, lip-sync strip, painted-bg
composite shot, title-safe test, -14 LUFS normalization, xsheet CSV.
"""
import csv, json, os, subprocess
from PIL import Image, ImageFilter, ImageDraw
import numpy as np

RIG = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(RIG, "wired-100-20261031")
os.makedirs(OUT, exist_ok=True)

def greykey(path):
    im = Image.open(path).convert("RGBA")
    a = np.array(im).astype(int)
    mask = np.max(np.abs(a[:, :, :3] - 128), axis=2) > 12
    out = np.array(im); out[:, :, 3] = np.where(mask, 255, 0).astype(np.uint8)
    return Image.fromarray(out)

# 1. Onion skin: walk frames ghosted (previous frame at 35% alpha under current)
walk = os.path.join(RIG, "clips-v7c-clean-20261031/walk")
frames = sorted(os.listdir(walk))
onion = Image.new("RGB", (1100 * 2, 1500), (128, 128, 128))
prev = None
for i, fn in enumerate(frames[:2]):
    fr = greykey(os.path.join(walk, fn))
    fr.thumbnail((550, 750))
    base = Image.new("RGBA", (550, 750), (128, 128, 128, 255))
    if prev is not None:
        ghost = prev.copy(); ghost.putalpha(ghost.split()[3].point(lambda v: int(v * 0.35)))
        base.alpha_composite(ghost, (0, 0))
    base.alpha_composite(fr, (0, 0))
    onion.paste(base.convert("RGB"), (550 * i, 375))
    prev = fr
onion.save(os.path.join(OUT, "wired-onion-skin-walk-20261031.jpg"), quality=90)
print("onion skin written")

# 2. Motion smear: punch frame, directional blur along punch direction
punch = greykey(os.path.join(RIG, "clips-v7c-clean-20261031/punch/punch-09-impact-hold-v7c-clean.png"))
punch.thumbnail((550, 750))
smear = punch.filter(ImageFilter.GaussianBlur(2))
# directional: paste blurred copy offset +12px at 40% under sharp copy
canvas = Image.new("RGBA", (550, 750), (128, 128, 128, 255))
ghost = smear.copy(); ghost.putalpha(ghost.split()[3].point(lambda v: int(v * 0.4)))
canvas.alpha_composite(ghost, (12, 0)); canvas.alpha_composite(punch, (0, 0))
canvas.convert("RGB").save(os.path.join(OUT, "wired-motion-smear-punch-20261031.jpg"), quality=90)
print("motion smear written")

# 3. Squash & stretch: jump landing frame squashed 0.85Y / stretched 1.1X
jump_dir = os.path.join(RIG, "clips-v7c-clean-20261031/jump")
print("jump frames:", sorted(os.listdir(jump_dir)) if os.path.isdir(jump_dir) else "missing")
if os.path.isdir(jump_dir):
    jf = sorted(os.listdir(jump_dir))[0]
    jm = greykey(os.path.join(jump_dir, jf)); jm.thumbnail((550, 750))
    sq = jm.resize((int(550 * 1.1), int(750 * 0.85)))
    canvas = Image.new("RGBA", (550, 750), (128, 128, 128, 255))
    canvas.alpha_composite(sq, ((550 - sq.size[0]) // 2, 750 - sq.size[1]))
    canvas.convert("RGB").save(os.path.join(OUT, "wired-squash-stretch-jump-20261031.jpg"), quality=90)
    print("squash written")

# 4. Lip-sync strip: visemes v2 heads for "M-OO" (mbp -> oo -> rest), 3 heads
vis = os.path.join(RIG, "visemes-v2-20261031")
strip = Image.new("RGB", (480 * 3, 480), (128, 128, 128))
for i, fn in enumerate(["head-v2-07-mbp-20261031.png", "head-v2-06-oo-20261031.png", "head-v2-01-rest-20261031.png"]):
    h = Image.open(os.path.join(vis, fn)).convert("RGBA"); h.thumbnail((480, 480))
    strip.paste(h, (480 * i, 0), h)
strip.save(os.path.join(OUT, "wired-lipsync-moo-strip-20261031.jpg"), quality=90)
print("lipsync strip written")

# 5. Painted-bg composite shot: flying clean frame over painted flying bg
bg = Image.open(os.path.join(RIG, "clean-100-20261031/layouts/bg-flying-painted-20261031.jpg")).convert("RGBA")
fly = greykey(os.path.join(RIG, "clips-v7c-clean-20261031/flying/flying-13-soar-v7c-clean.png"))
fly.thumbnail((400, 545))
bg.alpha_composite(fly, ((1168 - 400) // 2, 100))
bg.convert("RGB").save(os.path.join(OUT, "wired-shot-flying-painted-bg-20261031.jpg"), quality=92)
print("flying painted-bg shot written")

# 6. Title-safe test: 90% action-safe / 80% title-safe guides (debug only) on the flying shot
shot = Image.open(os.path.join(OUT, "wired-shot-flying-painted-bg-20261031.jpg")).convert("RGB")
d = ImageDraw.Draw(shot)
W, H = shot.size
for frac, col in [(0.05, (255, 0, 0)), (0.10, (0, 255, 0))]:
    d.rectangle([W * frac, H * frac, W * (1 - frac), H * (1 - frac)], outline=col, width=3)
shot.save(os.path.join(OUT, "wired-title-safe-test-20261031.jpg"), quality=90)
print("title-safe written")

# 7. -14 LUFS normalization (linear, single pass) + re-measure
wav = os.path.join(RIG, "showcase/audio/cape-jones-audio-cues-demo.wav")
norm = os.path.join(OUT, "wired-audio-minus14lufs-20261031.wav")
if os.path.exists(wav):
    r = subprocess.run(["ffmpeg", "-y", "-i", wav, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:linear=true",
                        norm], capture_output=True, text=True)
    r2 = subprocess.run(["ffmpeg", "-i", norm, "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                        capture_output=True, text=True)
    txt = r2.stderr; j = txt[txt.find("{"):txt.rfind("}") + 1] if "{" in txt else "{}"
    try: data = json.loads(j)
    except Exception: data = {"raw": txt[-300:]}
    json.dump(data, open(os.path.join(OUT, "wired-audio-minus14lufs-measure-20261031.json"), "w"), indent=2)
    print("normalized audio measured:", data, "size:", os.path.getsize(norm) if os.path.exists(norm) else 0)

# 8. Xsheet CSV for the walk clip (frame, pose, hold, audio cue)
with open(os.path.join(OUT, "wired-xsheet-walk-20261031.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["frame", "pose", "hold_frames", "audio_cue", "notes"])
    for i, fn in enumerate(frames):
        w.writerow([1 + i * 12, fn.replace("-v7c-clean.png", ""), 12, "footstep" if i % 2 == 0 else "footstep-alt",
                    "walk clip, clean v7c, 24fps"])
print("xsheet written")
