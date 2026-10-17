#!/usr/bin/env python3
"""Generate cape_jones_tooncrafter_colab.ipynb — Google Colab T4 ToonCrafter
cartoon interpolation notebook for the Cape Jones expressions video.

This is the Colab port of production/kaggle/tooncrafter/gen_notebook.py.
Colab serves as a backup/parallel GPU lane alongside Kaggle.

Key differences from the Kaggle version:
- /kaggle/working/ -> /content/ (Colab's working dir)
- No Kaggle dataset cache -> model weights download from HuggingFace every run
  (10.5GB). Optional: mount Google Drive to cache weights across sessions.
- Colab-idiomatic `!` shell commands instead of subprocess.run
- File download: output via Colab's files.download() widget
- GPU: Runtime -> Change runtime type -> T4 GPU (free tier)

Input:  expressions-v2-noblack.mp4 (106 frames @ 12fps, 1080x1920, no black frames)
Output: 211 frames @ 24fps via ToonCrafter (cartoon-trained diffusion interpolation)

Account: fmmg.mars@gmail.com (owner's Google — Colab sign-in)
"""
import json
import os

RAW = ("https://raw.githubusercontent.com/mhvnsnt/cape-jones/"
       "main/production/kaggle/tooncrafter")
# expressions-v2-noblack.mp4 — same SHA as Kaggle version
VIDEO_SHA = "c039dff8332f4e9ae697e81eb36f709dc38b0303eb830a2d3e7903fc91b1e19a"


def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}


def code(src):
    return {"cell_type": "code", "metadata": {},
            "execution_count": None, "outputs": [], "source": src}


cells = [
md("""# Cape Jones — ToonCrafter on Google Colab (T4 GPU)

Interpolates `expressions-v2-noblack.mp4` (106 frames @ 12fps, 1080x1920,
**no black frames**) to 24fps using **ToonCrafter** (SIGGRAPH Asia 2024,
CUHK & Tencent, Apache-2.0) on a **Tesla T4 GPU**.

This is the **Colab backup/parallel lane** — same pipeline as the Kaggle
notebook (`production/kaggle/tooncrafter/`), adapted for Colab.

**Before running:** Runtime → Change runtime type → **T4 GPU**. Then
**Runtime → Run all**.

**Sign in with:** fmmg.mars@gmail.com (owner's Google account)

Pipeline:
1. GPU check (must be Tesla T4)
2. Clone ToonCrafter + pip install deps
3. Download model.ckpt from HuggingFace (~10.5GB, be patient)
4. Download input video from GitHub (SHA-256 verified)
5. Extract 106 frames, resize to 320x512 portrait, build 105 keyframe pairs
6. ToonCrafter inference on CUDA (105 pairs x 8 frames, take middle frame idx 4)
7. Interleave originals + middles → 211 frames @ 24fps MP4 → download
"""),

code('''# === Cell 1: GPU check ===
# Colab: Runtime → Change runtime type → T4 GPU
!nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
'''),

code('''# === Cell 2: Clone ToonCrafter + install deps ===
# NOTE (2026-10-16): decord REMOVED — no cp313 wheels (abandoned since 2022),
# only used in training/eval, never inference. transformers==4.48.3 (not 4.25.1)
# because 4.25.1 pins tokenizers<0.14 with no cp313 wheels.
!git clone --depth 1 https://github.com/Doubiiu/ToonCrafter.git /content/ToonCrafter 2>/dev/null || echo "ToonCrafter already cloned."
%cd /content/ToonCrafter
!pip install -q einops==0.3.0 omegaconf==2.1.1 pytorch_lightning==1.9.3 transformers==4.48.3 open_clip_torch==2.22.0 xformers timm kornia av moviepy
print("Deps installed.")
'''),

code('''# === Cell 3: ToonCrafter model weights from HuggingFace (~10.5GB) ===
# Colab has no dataset cache like Kaggle. Options:
#   A) Download every run (~10 min on Colab's bandwidth) — simple, default below
#   B) Mount Google Drive and cache: uncomment the Drive lines to persist weights
import os

# --- Optional Drive cache (uncomment to use) ---
# from google.colab import drive
# drive.mount('/content/drive')
# DRIVE_CKPT = "/content/drive/MyDrive/cape-jones-weights/tooncrafter_model.ckpt"
# ---

ckpt_dir = "/content/ToonCrafter/checkpoints/tooncrafter_512_interp_v1"
os.makedirs(ckpt_dir, exist_ok=True)
ckpt_path = os.path.join(ckpt_dir, "model.ckpt")
EXPECTED = 10502492136  # bytes, verified 2026-10-16

def _ok(p):
    return os.path.exists(p) and os.path.getsize(p) == EXPECTED

if _ok(ckpt_path):
    print(f"model.ckpt already present ({os.path.getsize(ckpt_path)/1e9:.1f} GB)")
# elif _ok(DRIVE_CKPT):  # Drive cache hit
#     import shutil
#     print("Copying from Drive cache...")
#     shutil.copy(DRIVE_CKPT, ckpt_path)
else:
    print("Downloading model.ckpt (10.5GB) from HuggingFace...")
    !wget -q --show-progress https://huggingface.co/Doubiiu/ToonCrafter/resolve/main/model.ckpt -O {ckpt_path}
    assert _ok(ckpt_path), "downloaded model.ckpt size mismatch"
    print(f"Downloaded ({os.path.getsize(ckpt_path)/1e9:.1f} GB)")
    # To cache on Drive for next time, uncomment:
    # import shutil; shutil.copy(ckpt_path, DRIVE_CKPT)
'''),

code(f'''# === Cell 4: Download input video from GitHub (SHA-256 verified) ===
import hashlib
url = "{RAW}/input-12fps-noblack.mp4"
out = "/content/input-12fps-noblack.mp4"
print(f"Downloading {{url}} ...")
!wget -q {{url}} -O {{out}}
h = hashlib.sha256(open(out, "rb").read()).hexdigest()
print(f"sha256: {{h}}")
assert h == "{VIDEO_SHA}", f"SHA MISMATCH! got {{h}}"
print("Video verified OK.")
'''),

code('''# === Cell 5: Extract frames + build 105 keyframe pairs ===
# ToonCrafter interp mode: each sample = 2 keyframes -> 8 frames (tuned).
# 105 pairs from 106 frames. Portrait: resize to 320x512.
import os

work = "/content/tc_input"
frames_dir = os.path.join(work, "frames")
prompt_dir = os.path.join(work, "prompts", "cape_jones")
for d in (frames_dir, prompt_dir):
    os.makedirs(d, exist_ok=True)

print("Extracting 106 frames...")
!ffmpeg -y -v error -i /content/input-12fps-noblack.mp4 -vsync 0 {frames_dir}/frame_%05d.png
n = len([f for f in os.listdir(frames_dir) if f.endswith(".png")])
print(f"{n} frames extracted (expect 106)")
assert n == 106, f"Expected 106 frames, got {n}"

print("Resizing to 320x512 and building 105 pairs...")
prompt_lines = []
for i in range(105):
    for tag, src_idx in (("a", i), ("b", i + 1)):
        src = os.path.join(frames_dir, f"frame_{src_idx+1:05d}.png")
        dst = os.path.join(prompt_dir, f"pair_{i:03d}_{tag}.png")
        !ffmpeg -y -v error -i {src} -vf scale=320:512 {dst}
    prompt_lines.append(f"cape jones cartoon character, pair {i}")

with open(os.path.join(prompt_dir, "prompts.txt"), "w") as f:
    f.write("\\n".join(prompt_lines) + "\\n")
print(f"105 pairs built in {prompt_dir}")
'''),

code('''# === Cell 6: ToonCrafter inference on CUDA ===
# 105 pairs -> 8 frames each (TUNED: was 16). Take middle frame (idx 4).
# ddim_steps=12 (TUNED: was 25). bs=1 for VRAM safety.
import time
t0 = time.time()
!cd /content/ToonCrafter && python3 scripts/evaluation/inference.py \\
    --seed 123 \\
    --ckpt_path checkpoints/tooncrafter_512_interp_v1/model.ckpt \\
    --config configs/inference_512_v1.0.yaml \\
    --savedir /content/tc_results \\
    --n_samples 105 \\
    --bs 1 \\
    --height 512 \\
    --width 320 \\
    --unconditional_guidance_scale 7.5 \\
    --ddim_steps 12 \\
    --ddim_eta 1.0 \\
    --prompt_dir /content/tc_input/prompts/cape_jones \\
    --text_input \\
    --video_length 8 \\
    --frame_stride 10 \\
    --timestep_spacing uniform_trailing \\
    --guidance_rescale 0.7 \\
    --perframe_ae \\
    --interp
elapsed = (time.time() - t0) / 60
print(f"\\nToonCrafter wall time = {elapsed:.1f} min")
print("Inference complete.")
'''),

code('''# === Cell 7: Extract middle frames + interleave + assemble 24fps MP4 ===
# From each 8-frame output, take frame idx 4 (true middle).
# [orig_0, mid_0, orig_1, mid_1, ...] = 211 frames @ 24fps.
import os, glob, shutil
from PIL import Image

results_base = "/content/tc_results"
sample_dirs = sorted(glob.glob(os.path.join(results_base, "*", "samples", "*")))
if not sample_dirs:
    sample_dirs = sorted(glob.glob(os.path.join(results_base, "**", "sample_*"),
                                   recursive=True))
print(f"Found {len(sample_dirs)} sample outputs (expect 105)")
assert len(sample_dirs) == 105, f"Expected 105 samples, got {len(sample_dirs)}"

out_dir = "/content/final_frames"
os.makedirs(out_dir, exist_ok=True)
frames_dir = "/content/tc_input/frames"

out_idx = 0
for i, sdir in enumerate(sample_dirs):
    orig = os.path.join(frames_dir, f"frame_{i+1:05d}.png")
    shutil.copy(orig, os.path.join(out_dir, f"out_{out_idx:05d}.png"))
    out_idx += 1
    tc_frames = sorted(glob.glob(os.path.join(sdir, "*.png")))
    assert len(tc_frames) == 8, f"Sample {i}: expected 8 frames, got {len(tc_frames)}"
    mid = Image.open(tc_frames[4]).convert("RGB").resize((1080, 1920), Image.LANCZOS)
    mid.save(os.path.join(out_dir, f"out_{out_idx:05d}.png"))
    out_idx += 1

shutil.copy(os.path.join(frames_dir, "frame_00106.png"),
            os.path.join(out_dir, f"out_{out_idx:05d}.png"))
out_idx += 1

print(f"{out_idx} frames assembled (expect 211)")
assert out_idx == 211, f"Expected 211 frames, got {out_idx}"

!ffmpeg -y -v error -framerate 24 -i {out_dir}/out_%05d.png \\
    -c:v libx264 -pix_fmt yuv420p -crf 18 \\
    /content/cape-jones-expressions-TOONCRAFTER-24fps.mp4
print("Wrote /content/cape-jones-expressions-TOONCRAFTER-24fps.mp4")
!ffprobe -v error -select_streams v:0 \\
    -show_entries stream=nb_frames,r_frame_rate,width,height \\
    -of default=noprint_wrappers=1 \\
    /content/cape-jones-expressions-TOONCRAFTER-24fps.mp4
'''),

code('''# === Cell 8: Download the finished video ===
# Colab has no "Save & Run All" — download the MP4 NOW before the session ends.
# (Colab sessions also time out! Don't rely on the file persisting.)
from google.colab import files
files.download("/content/cape-jones-expressions-TOONCRAFTER-24fps.mp4")
print("Download started. Save it to: ~/workspace/cape-jones-build/cape-jones-expressions-TOONCRAFTER.mp4")
print("Then run finish.py with the trippy grade + Orbiting Nebulas audio.")
'''),
]

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3",
                       "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10.0"},
        "colab": {"provenance": []},
    },
    "cells": cells,
}

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "cape_jones_tooncrafter_colab.ipynb")
with open(out_path, "w") as f:
    json.dump(nb, f, indent=1)
print(f"Wrote {out_path} ({len(cells)} cells)")

# compile-check every code cell (strip jupyter/colab magics + shell continuations)
for i, c in enumerate(cells):
    if c["cell_type"] == "code":
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        lines = []
        in_shell = False
        for l in src.splitlines():
            s = l.strip()
            if s.startswith(("%", "!")):
                in_shell = l.rstrip().endswith("\\")
                continue
            if in_shell:
                in_shell = l.rstrip().endswith("\\")
                continue
            lines.append(l)
        try:
            compile("\n".join(lines), f"<cell {i}>", "exec")
        except SyntaxError as e:
            print(f"SYNTAX ERROR in cell {i}: {e}")
            raise
print("All code cells compile OK.")
