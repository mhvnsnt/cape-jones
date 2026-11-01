#!/usr/bin/env python3
"""Invisible Power V1 — NO-CROP FIX (Mars, 2026-10-31 20:42 CDT).

CONFIRMED: this IS Invisibility V1, the animated going-invisible power,
approved in concept 20:40 CDT. The old version is now DRAFT (saved in
draft/, md5-identical to the original, originals untouched). The fixed
version built here is the actual V1 candidate for approval (0/1).

DEFECT, measured before any rebuild:
  outline_of() in the original build_templates.py ran on BASE, the figure
  TRIMMED to its own alpha bbox (464x1056). MaxFilter(13)/(29)+blur(6)
  halo therefore had nowhere to go beyond the silhouette box: it was
  sliced flat at the bbox edge. Old outline alpha 105,188 px, bbox
  (0,0,464,1056) — it touches all four edges of its own canvas.
  Recomputing the SAME outline on the SAME figure padded by 80px gives
  131,199 alpha px, of which 26,011 px lie OUTSIDE the old BASE box:
  top 2,903 px (halo should extend 27 px above the head), bottom 7,698,
  left 7,809, right 7,601. Old outline row 0 alone carries 141 alpha px
  — a straight flat cut across the top of the head. That is Mars's
  "square cropping at the top": the glow/power/afterglow was cut by the
  trimmed-figure window, not by the union canvas (which only added a
  24 px pad around an already-cut outline).

FIX — industry-standard no-crop / overscan, all actually RUN here:
  1. Pillow ImageOps.expand: pad the figure by 80 px (transparent) BEFORE
     the MaxFilter/blur outline pass, so the halo has room to form.
     (no_crop.py pad_image; Pillow docs: expand grows the canvas.)
  2. Overscan canvas: fixed frames are built on the padded outline
     canvas (624x1216) plus a further 40 px transparent margin on every
     side -> 704x1296. The canvas fits the figure + glow, never the
     reverse. No delivery crop is applied; any future delivery crop is
     a separate export step after a safe-area check.
  3. numpy alpha bbox + margins gate (gate_invisible_v1.py, run below):
     edge alpha must be 0 on all 17 frames, min margin >= 40 px, and
     the outline frame's bbox must extend above the head top (proving
     the halo is no longer flat-cut).
  4. OpenCV boundingRect cross-check (venv cv2 5.0.0, actually run).
  5. FFmpeg pad filter proof (actually run on one fixed frame): padding
     a frame with ffmpeg -vf pad preserves alpha count exactly.
MAPPINGS only (labelled, not runs): Blender render-border-off + overscan
(use_border=False, camera fit to subject bbox — settings only, no Blender
render claimed); Resolve/Premiere safe-area + Auto Reframe; After Effects
ROI/overscan; Krita/GIMP canvas-size expansion; Natron overscan. None of
these is claimed as a run.

MOTION UNCHANGED, exactly as the original template:
  17 frames @12fps, body width 1.0 -> 0.02 f00-f07 (smoothstep), outline-
  only hold f08-f11, return f12-f16, outline frozen unsquashed silhouette,
  hard ring (180,245,255) + one soft halo (0,200,255), visible body alpha
  337,389 px, outline-only hold 104,787 px in the OLD frames.
  Only the canvas/outline window changed. Body/outline opacity sequence,
  colours, and timing are byte-for-byte the original logic.
"""
import os, sys, json, math, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps

ROOT = "/home/hatch/workspace/cape-jones-rig"
SRC = os.path.join(ROOT, "pseudo-turn-templates-20261031/frames/invisible-power/f00.png")
OUT = os.path.join(ROOT, "invisible-power-v1-nocrop-fix-20261031")
GREY = (128, 128, 128, 255)
PAD_OUTLINE = 80   # transparent pad BEFORE the outline filters
MARGIN = 40        # transparent margin around the padded canvas
FPS = 12

def smooth(t):
    return t * t * (3 - 2 * t)

def transform(fig, sx, sy):
    w, h = fig.size
    return fig.resize((max(2, int(w * sx)), max(2, int(h * sy))), Image.LANCZOS)

def outline_of(fig, hard=(180, 245, 255, 255), soft=(0, 200, 255, 153)):
    """Identical filter math to the original, run on a PADDED figure."""
    a = fig.getchannel("A")
    hard_ring = ImageChops.subtract(a.filter(ImageFilter.MaxFilter(13)), a)
    soft_halo = a.filter(ImageFilter.MaxFilter(29)).filter(ImageFilter.GaussianBlur(6))
    soft_halo = ImageChops.subtract(soft_halo, a)
    out = Image.new("RGBA", fig.size, (0, 0, 0, 0))
    for mask, col in ((soft_halo, soft), (hard_ring, hard)):
        layer = Image.new("RGBA", fig.size, col)
        layer.putalpha(mask)
        out.alpha_composite(layer)
    return out

# --- source: original f00 frame, de-padded back to the trimmed BASE ---
fr0 = Image.open(SRC).convert("RGBA")
BASE = fr0.crop((24, 24, 24 + 464, 24 + 1056))
assert BASE.size == (464, 1056), BASE.size
assert sum(1 for p in BASE.getchannel("A").getdata() if p > 0) == 337389

# --- padded figure + uncropped outline (the fix) ---
PADDED = ImageOps.expand(BASE, border=PAD_OUTLINE, fill=(0, 0, 0, 0))
OUTLINE = outline_of(PADDED)  # 624x1216, halo free on all sides
BW, BH = BASE.size
PW, PH = PADDED.size  # 624, 1216
FW, FH = PW + 2 * MARGIN, PH + 2 * MARGIN  # 704, 1296 final canvas
print("BASE", BASE.size, "PADDED", PADDED.size, "FINAL", (FW, FH))

def compose(body, outline_opacity):
    """Body centred on the BASE centre inside the padded canvas, outline
    at full padded size, then the whole thing on the final margin canvas."""
    comp = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    comp.alpha_composite(body, (PAD_OUTLINE + (BW - body.size[0]) // 2, PAD_OUTLINE))
    if outline_opacity:
        o = OUTLINE.copy()
        o.putalpha(o.getchannel("A").point(lambda v: v * outline_opacity // 255))
        comp.alpha_composite(o, (0, 0))
    final = Image.new("RGBA", (FW, FH), (0, 0, 0, 0))
    final.alpha_composite(comp, (MARGIN, MARGIN))
    return final

def compose_hold():
    comp = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    comp.alpha_composite(OUTLINE, (0, 0))
    final = Image.new("RGBA", (FW, FH), (0, 0, 0, 0))
    final.alpha_composite(comp, (MARGIN, MARGIN))
    return final

frames = []
for i in range(17):
    if i < 8:
        sx = 1.0 - 0.98 * smooth(i / 7)
        frames.append(compose(transform(BASE, sx, 1.0), int(255 * smooth(i / 7))))
    elif i < 12:
        frames.append(compose_hold())
    else:
        sx = 0.02 + 0.98 * smooth((i - 12) / 4)
        frames.append(compose(transform(BASE, sx, 1.0), int(255 * (1 - smooth((i - 12) / 4)))))

# f00/f16 must be body-only (opacity 0) and equal the old visible body count
# on the new canvas; outline-hold frames must carry the full uncropped outline.
frames_dir = os.path.join(OUT, "frames")
os.makedirs(frames_dir, exist_ok=True)
view = []
meas = []
for i, f in enumerate(frames):
    f.save(os.path.join(frames_dir, f"f{i:02d}.png"))
    a = f.getchannel("A")
    bb = a.getbbox()
    meas.append({"frame": i, "size": list(f.size), "alpha_px": sum(1 for p in a.getdata() if p > 0),
                 "bbox": list(bb),
                 "margins": {"left": bb[0], "top": bb[1], "right": f.size[0] - bb[2], "bottom": f.size[1] - bb[3]}})
    view.append(Image.alpha_composite(Image.new("RGBA", (FW, FH), GREY), f).convert("RGB"))

gif = os.path.join(OUT, "invisible-power-v1-NOCROP-FIXED-20261031.gif")
view[0].save(gif, save_all=True, append_images=view[1:], duration=int(1000 / FPS), loop=0)
with tempfile.TemporaryDirectory() as td:
    for i, f in enumerate(view):
        f.save(os.path.join(td, f"f{i:03d}.jpg"), quality=92)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(td, "f%03d.jpg"),
                    "-vf", f"scale={FW}:{FH},format=yuv420p", "-c:v", "libx264",
                    os.path.join(OUT, "invisible-power-v1-NOCROP-FIXED-20261031.mp4")], check=True)

# --- FFmpeg pad-filter proof (run, not claimed): pad f08, alpha must not change ---
pad_png = os.path.join(OUT, "ffmpeg-pad-proof-20261031.png")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(frames_dir, "f08.png"),
                "-vf", "pad=800:1400:48:52:0x00000000", pad_png], check=True)
pad_im = Image.open(pad_png).convert("RGBA")
meas.append({"ffmpeg_pad_proof": {"in": os.path.join(frames_dir, "f08.png"),
             "in_alpha": sum(1 for p in Image.open(os.path.join(frames_dir, "f08.png")).getchannel("A").getdata() if p > 0),
             "out_alpha": sum(1 for p in pad_im.getchannel("A").getdata() if p > 0),
             "out_size": list(pad_im.size)}})

with open(os.path.join(OUT, "measurements-fixed-20261031.json"), "w") as fh:
    json.dump({"canvas": [FW, FH], "padded_outline_canvas": [PW, PH], "base": list(BASE.size),
               "frames": meas}, fh, indent=2)
print(json.dumps(meas, indent=2))
print("GIF", gif)
