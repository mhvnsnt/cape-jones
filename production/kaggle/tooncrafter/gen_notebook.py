#!/usr/bin/env python3
"""Generate cape_jones_tooncrafter_kaggle.ipynb — Kaggle GPU T4 ToonCrafter
cartoon interpolation notebook for the Cape Jones expressions video.

Input:  expressions-v2-noblack.mp4 (106 frames @ 12fps, 1080x1920, no black frames)
Output: 211 frames @ 24fps via ToonCrafter (cartoon-trained diffusion interpolation)

Unlike RIFE (trained on real video), ToonCrafter (SIGGRAPH Asia 2024) is
specifically trained on cartoons — handles exaggerated non-linear motion and
dis-occlusion that flow-based methods ghost on.

Strategy: 105 adjacent frame pairs -> each generates 16 frames via ToonCrafter
interp mode -> take middle frame (idx 8) from each -> interleave with originals:
  [orig_0, mid_0, orig_1, mid_1, ...] = 211 frames @ 24fps

Portrait handling: input is 1080x1920. ToonCrafter's 512 model was trained at
512x320 (landscape) but the UNet is fully convolutional — we run at
--height 512 --width 320 (portrait).

Upload the .ipynb to Kaggle's notebook editor (browser lane).
"""
import json

BRANCH = "kaggle-tooncrafter"
RAW = (f"https://raw.githubusercontent.com/mhvnsnt/cape-jones/"
       f"{BRANCH}/production/kaggle/tooncrafter")
# expressions-v2-noblack.mp4
VIDEO_SHA = "c039dff8332f4e9ae697e81eb36f709dc38b0303eb830a2d3e7903fc91b1e19a"


def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}


def code(src):
    return {"cell_type": "code", "metadata": {},
            "execution_count": None, "outputs": [], "source": src}


cells = [
md("""# Cape Jones — ToonCrafter cartoon interpolation on Kaggle T4 GPU

Interpolates `expressions-v2-noblack.mp4` (106 frames @ 12fps, 1080x1920,
**no black frames**) to 24fps using **ToonCrafter** (SIGGRAPH Asia 2024,
CUHK & Tencent, Apache-2.0) on a **Tesla T4 GPU**.

**Why ToonCrafter instead of RIFE?** RIFE was trained on real video — its
optical flow can't track motion in flat, textureless cartoon regions (white
suit, purple cape), so it blends instead of warping = ghosting. ToonCrafter
is a diffusion model **trained on cartoons** — it handles the exaggerated
non-linear motion and dis-occlusion in animation natively.

**Before running:** Settings (right panel) -> **Accelerator: GPU T4 x2**,
**Internet: ON**. Then **Run All**.

Pipeline in this notebook:
1. GPU check (must be Tesla T4)
2. Clone ToonCrafter + pip install deps
3. Download model.ckpt from HuggingFace (~5GB, be patient)
4. Download input video from GitHub (SHA-256 verified)
5. Extract 106 frames, resize to 320x512 portrait, build 105 keyframe pairs
6. ToonCrafter inference on CUDA (105 pairs x 16 frames, take middle frame)
7. Interleave originals + middles -> 211 frames @ 24fps MP4 -> `/kaggle/working/`
"""),

code('''# === GPU check ===
import subprocess
r = subprocess.run(["nvidia-smi", "--query-gpu=name,driver_version,memory.total",
                    "--format=csv"], capture_output=True, text=True)
print(r.stdout.strip() or "NO GPU VISIBLE -- enable Accelerator: GPU in Settings!")
assert "Tesla T4" in r.stdout, "Expected a Tesla T4"
'''),

code('''# === Clone ToonCrafter + install deps ===
import subprocess, sys, os
if not os.path.isdir("/kaggle/working/ToonCrafter"):
    print("Cloning ToonCrafter...")
    subprocess.run(["git", "clone", "--depth", "1",
                    "https://github.com/Doubiiu/ToonCrafter.git",
                    "/kaggle/working/ToonCrafter"], check=True)
else:
    print("ToonCrafter already cloned.")
%cd /kaggle/working/ToonCrafter
# Kaggle ships torch+torchvision; install the rest (skip torch to save time)
print("Installing deps...")
subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                "decord==0.6.0", "einops==0.3.0", "omegaconf==2.1.1",
                "pytorch_lightning==1.9.3", "transformers==4.25.1",
                "open_clip_torch==2.22.0", "xformers", "timm",
                "kornia", "av", "moviepy"],
               check=True)
print("Deps installed.")
'''),

code('''# === Download ToonCrafter model weights from HuggingFace ===
import subprocess, os
ckpt_dir = "/kaggle/working/ToonCrafter/checkpoints/tooncrafter_512_interp_v1"
os.makedirs(ckpt_dir, exist_ok=True)
ckpt_path = os.path.join(ckpt_dir, "model.ckpt")
if os.path.exists(ckpt_path) and os.path.getsize(ckpt_path) > 4_000_000_000:
    print(f"model.ckpt already present ({os.path.getsize(ckpt_path)/1e9:.1f} GB)")
else:
    print("Downloading model.ckpt (~5GB) from HuggingFace — this takes a few minutes...")
    subprocess.run(["wget", "-q", "--show-progress",
                    "https://huggingface.co/Doubiiu/ToonCrafter/resolve/main/model.ckpt",
                    "-O", ckpt_path], check=True)
    print(f"Downloaded ({os.path.getsize(ckpt_path)/1e9:.1f} GB)")
'''),

code(f'''# === Download input video from GitHub (SHA-256 verified) ===
import subprocess, hashlib, os
url = "{RAW}/input-12fps-noblack.mp4"
out = "/kaggle/working/input-12fps-noblack.mp4"
print(f"Downloading {{url}} ...")
subprocess.run(["wget", "-q", url, "-O", out], check=True)
h = hashlib.sha256(open(out, "rb").read()).hexdigest()
print(f"sha256: {{h}}")
assert h == "{VIDEO_SHA}", f"SHA MISMATCH! got {{h}}"
print("Video verified OK.")
'''),

code('''# === Extract frames + build 105 keyframe pairs ===
# ToonCrafter interp mode: each sample = 2 keyframes -> generates 16 frames.
# We need 105 pairs from 106 frames. Portrait: resize to 320x512.
import subprocess, os, shutil

work = "/kaggle/working/tc_input"
frames_dir = os.path.join(work, "frames")
prompt_dir = os.path.join(work, "prompts", "cape_jones")
for d in (frames_dir, prompt_dir):
    os.makedirs(d, exist_ok=True)

# 1. Extract 106 frames at original res
print("Extracting frames...")
subprocess.run(["ffmpeg", "-y", "-v", "error",
                "-i", "/kaggle/working/input-12fps-noblack.mp4",
                "-vsync", "0",
                os.path.join(frames_dir, "frame_%05d.png")], check=True)
n = len([f for f in os.listdir(frames_dir) if f.endswith(".png")])
print(f"{n} frames extracted (expect 106)")
assert n == 106, f"Expected 106 frames, got {n}"

# 2. Resize to 320x512 portrait + build pairs
#    Pair i = (frame_i, frame_{i+1}) -> named pair_{i:03d}_a.png / _b.png
print("Resizing to 320x512 and building 105 pairs...")
prompt_lines = []
for i in range(105):
    for tag, src_idx in (("a", i), ("b", i + 1)):
        src = os.path.join(frames_dir, f"frame_{src_idx+1:05d}.png")
        dst = os.path.join(prompt_dir, f"pair_{i:03d}_{tag}.png")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src,
                        "-vf", "scale=320:512", dst], check=True)
    # prompt file: one line per sample (ToonCrafter uses it for n_samples count)
    prompt_lines.append(f"cape jones cartoon character, pair {i}")

with open(os.path.join(prompt_dir, "prompts.txt"), "w") as f:
    f.write("\\n".join(prompt_lines) + "\\n")
print(f"105 pairs built in {prompt_dir}")
'''),

code('''# === ToonCrafter inference on CUDA ===
# 105 pairs -> 16 frames each. We take the middle frame (idx 8) from each.
# ddim_steps=25 for speed (50 = slower, marginally better). bs=1 for VRAM safety.
import subprocess, time, os

t0 = time.time()
cmd = [
    "python3", "scripts/evaluation/inference.py",
    "--seed", "123",
    "--ckpt_path", "checkpoints/tooncrafter_512_interp_v1/model.ckpt",
    "--config", "configs/inference_512_v1.0.yaml",
    "--savedir", "/kaggle/working/tc_results",
    "--n_samples", "105",
    "--bs", "1",
    "--height", "512",
    "--width", "320",
    "--unconditional_guidance_scale", "7.5",
    "--ddim_steps", "25",
    "--ddim_eta", "1.0",
    "--prompt_dir", "/kaggle/working/tc_input/prompts/cape_jones",
    "--text_input",
    "--video_length", "16",
    "--frame_stride", "10",
    "--timestep_spacing", "uniform_trailing",
    "--guidance_rescale", "0.7",
    "--perframe_ae",
    "--interp",
]
print("Running ToonCrafter inference (105 pairs, this takes a while)...")
print(" ".join(cmd))
r = subprocess.run(cmd, cwd="/kaggle/working/ToonCrafter")
elapsed = (time.time() - t0) / 60
print(f"\\nToonCrafter wall time = {elapsed:.1f} min")
assert r.returncode == 0, "ToonCrafter inference FAILED"
print("Inference complete.")
'''),

code('''# === Extract middle frames + interleave + assemble 24fps MP4 ===
# From each 16-frame ToonCrafter output, take frame idx 8 (the true middle).
# Output sequence: [orig_0, mid_0, orig_1, mid_1, ...] = 211 frames @ 24fps.
import os, glob, shutil, subprocess
from PIL import Image

results_base = "/kaggle/working/tc_results"
# find the sample dirs (tooncrafter_512_interp_seed123 / sample_*)
sample_dirs = sorted(glob.glob(os.path.join(results_base, "*", "samples", "*")))
if not sample_dirs:
    # fallback: search recursively for per-sample frame dirs
    sample_dirs = sorted(glob.glob(os.path.join(results_base, "**", "sample_*"),
                                   recursive=True))
print(f"Found {len(sample_dirs)} sample outputs (expect 105)")
assert len(sample_dirs) == 105, f"Expected 105 samples, got {len(sample_dirs)}"

out_dir = "/kaggle/working/final_frames"
os.makedirs(out_dir, exist_ok=True)
frames_dir = "/kaggle/working/tc_input/frames"

out_idx = 0
for i, sdir in enumerate(sample_dirs):
    # original frame i (full-res 1080x1920)
    orig = os.path.join(frames_dir, f"frame_{i+1:05d}.png")
    shutil.copy(orig, os.path.join(out_dir, f"out_{out_idx:05d}.png"))
    out_idx += 1
    # ToonCrafter middle frame (320x512) -> upscale to 1080x1920 to match
    tc_frames = sorted(glob.glob(os.path.join(sdir, "*.png")))
    assert len(tc_frames) == 16, f"Sample {i}: expected 16 frames, got {len(tc_frames)}"
    mid = Image.open(tc_frames[8]).convert("RGB").resize((1080, 1920), Image.LANCZOS)
    mid.save(os.path.join(out_dir, f"out_{out_idx:05d}.png"))
    out_idx += 1

# final original frame (frame 106)
shutil.copy(os.path.join(frames_dir, "frame_00106.png"),
            os.path.join(out_dir, f"out_{out_idx:05d}.png"))
out_idx += 1

print(f"{out_idx} frames assembled (expect 211)")
assert out_idx == 211, f"Expected 211 frames, got {out_idx}"

# assemble 24fps MP4
subprocess.run(["ffmpeg", "-y", "-v", "error",
                "-framerate", "24", "-i", os.path.join(out_dir, "out_%05d.png"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                "/kaggle/working/cape-jones-expressions-TOONCRAFTER-24fps.mp4"],
               check=True)
print("Wrote /kaggle/working/cape-jones-expressions-TOONCRAFTER-24fps.mp4")

# verify
r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                    "-show_entries", "stream=nb_frames,r_frame_rate,width,height",
                    "-of", "default=noprint_wrappers=1",
                    "/kaggle/working/cape-jones-expressions-TOONCRAFTER-24fps.mp4"],
                   capture_output=True, text=True)
print(r.stdout)
'''),
]

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3",
                       "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10.0"},
    },
    "cells": cells,
}

out_path = "/home/hatch/workspace/cape-jones-build/kaggle-tooncrafter/cape_jones_tooncrafter_kaggle.ipynb"
with open(out_path, "w") as f:
    json.dump(nb, f, indent=1)
print(f"Wrote {out_path} ({len(cells)} cells)")

# compile-check every code cell
for i, c in enumerate(cells):
    if c["cell_type"] == "code":
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        # strip jupyter magics for compile check
        lines = [l for l in src.splitlines()
                 if not l.strip().startswith(("%", "!"))]
        try:
            compile("\n".join(lines), f"<cell {i}>", "exec")
        except SyntaxError as e:
            print(f"SYNTAX ERROR in cell {i}: {e}")
            raise
print("All code cells compile OK.")
