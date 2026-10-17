#!/usr/bin/env python3
"""Generate cape_jones_one_to_all_kaggle.ipynb — Kaggle GPU T4 One-to-All Animation
body replacement notebook for Cape Jones.

Replaces Viggle-Animate (which needs 73.5GB VRAM + has a USA-excluding license)
with One-to-All Animation 1.3B (CVPR 2026, Apache-2.0), which the authors verify
runs on Kaggle's free 16GB T4.

Input:  driving video + character reference image (from cape-jones-viggle-inputs dataset)
Output: body-replaced video in /kaggle/working/

Pipeline (author's scripts, not hand-tooled):
1. GPU check (must be Tesla T4)
2. Install deps (torch, diffusers, etc.)
3. Download One-to-All-1.3b_2 checkpoints from HF (~2-3GB)
4. Download Wan2.1-T2V-1.3B base model from HF
5. Copy inputs from /kaggle/input/cape-jones-viggle-inputs/
6. Run author's infer_preprocess.py (pose extraction)
7. Run author's inference_1.3b.py
8. Output MP4 to /kaggle/working/ + bulletproof saver checkpoint

Before running: Settings -> Accelerator: GPU T4 x2, Internet: ON.
Attach dataset: marsfmmg/cape-jones-viggle-inputs
Then Run All.
"""
import json
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}


def code(src):
    return {"cell_type": "code", "metadata": {},
            "execution_count": None, "outputs": [], "source": src}


cells = [
md("""# Cape Jones — One-to-All Animation body replacement on Kaggle T4

Replaces the performer in a driving video with the Cape Jones character using
**One-to-All Animation 1.3B** (CVPR 2026, Apache-2.0) on a **Tesla T4 GPU**.

**Why One-to-All instead of Viggle-Animate?** Viggle-Animate needs 73.5 GB VRAM
(impossible on a 16 GB T4) and its MiniMax H3 license excludes the USA.
One-to-All 1.3B runs on the free T4 and is Apache-2.0. See
`docs/research/VIGGLE-ANIMATE-ASSESSMENT.md` for the full analysis.

**Before running:** Settings (right panel) → **Accelerator: GPU T4 x2**,
**Internet: ON**. Attach dataset **`marsfmmg/cape-jones-viggle-inputs`**.
Then **Run All**.

Pipeline in this notebook (author's scripts, wired up — not hand-tooled):
1. GPU check (must be Tesla T4)
2. pip install dependencies
3. Download One-to-All-1.3b_2 + Wan2.1-T2V-1.3B checkpoints from HuggingFace
4. Stage inputs from the attached dataset
5. Run author's pose preprocessing
6. Run author's 1.3B inference
7. Output MP4 → `/kaggle/working/` + bulletproof dataset checkpoint
"""),

code('''# === GPU check ===
import subprocess
r = subprocess.run(["nvidia-smi", "--query-gpu=name,driver_version,memory.total",
                    "--format=csv"], capture_output=True, text=True)
print(r.stdout.strip() or "NO GPU VISIBLE -- enable Accelerator: GPU in Settings!")
assert "Tesla T4" in r.stdout, "Expected a Tesla T4"
'''),

code('''# === Bulletproof saver setup (skip if queue already injected it) ===
import os, sys
sys.path.insert(0, "/kaggle/working")
try:
    from save_outputs import RenderSaver
    _saver = RenderSaver(job_name="one-to-all-body-replace")
    _saver.start_watchdog()
    print("saver active")
except Exception as e:
    _saver = None
    print(f"saver unavailable ({e}) — output relies on Save & Run All")
'''),

code('''# === Install dependencies ===
# NOTE: decord has no cp313 wheels (abandoned 2022). Use imageio + opencv instead.
# If the author's script imports decord, we patch it out below.
import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                "torch", "torchvision", "diffusers>=0.30",
                "transformers>=4.48", "accelerate", "safetensors",
                "huggingface_hub", "imageio", "imageio-ffmpeg",
                "opencv-python-headless", "pillow", "tqdm", "einops"],
               check=True)
print("deps installed")
'''),

code('''# === Download checkpoints (cache-first) ===
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import snapshot_download

CKPT_DIR = "/kaggle/working/one-to-all-checkpoints"
os.makedirs(CKPT_DIR, exist_ok=True)

# 1.3B finetune (~2-3GB)
lora_dir = os.path.join(CKPT_DIR, "One-to-All-1.3b_2")
if not os.path.exists(os.path.join(lora_dir, ".complete")):
    print("Downloading One-to-All-1.3b_2 ...")
    snapshot_download(repo_id="MochunniaN1/One-to-All-1.3b_2",
                      local_dir=lora_dir, resume_download=True)
    open(os.path.join(lora_dir, ".complete"), "w").write("ok")
else:
    print("One-to-All-1.3b_2 cached")

# Wan2.1-T2V-1.3B base (~2-3GB)
base_dir = os.path.join(CKPT_DIR, "Wan2.1-T2V-1.3B-Diffusers")
if not os.path.exists(os.path.join(base_dir, ".complete")):
    print("Downloading Wan2.1-T2V-1.3B base ...")
    snapshot_download(repo_id="Wan-AI/Wan2.1-T2V-1.3B-Diffusers",
                      local_dir=base_dir, resume_download=True)
    open(os.path.join(base_dir, ".complete"), "w").write("ok")
else:
    print("Wan2.1 base cached")
print("checkpoints ready")
'''),

code('''# === Stage inputs from attached dataset ===
import os, shutil, glob

SRC = "/kaggle/input/cape-jones-viggle-inputs"
assert os.path.isdir(SRC), f"dataset not attached: {SRC} missing — attach marsfmmg/cape-jones-viggle-inputs in Settings"
print("dataset contents:", os.listdir(SRC))

WORK = "/kaggle/working/one-to-all-inputs"
os.makedirs(WORK, exist_ok=True)

# driving video (mp4) and character reference (png/jpg)
vids = glob.glob(os.path.join(SRC, "*.mp4"))
imgs = glob.glob(os.path.join(SRC, "*.png")) + glob.glob(os.path.join(SRC, "*.jpg"))
assert vids, "no .mp4 driving video in dataset"
assert imgs, "no character reference image in dataset"

driving = os.path.join(WORK, "driving.mp4")
charref = os.path.join(WORK, "character.png")
shutil.copy(vids[0], driving)
shutil.copy(imgs[0], charref)
print(f"driving: {vids[0]} -> {driving}")
print(f"character: {imgs[0]} -> {charref}")

# probe driving video
import subprocess
r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                    "-show_entries", "stream=nb_frames,width,height,r_frame_rate",
                    "-of", "default=noprint_wrappers=1", driving],
                   capture_output=True, text=True)
print(r.stdout)
'''),

code('''# === Clone one-to-all-animation (author's code, not hand-tooled) ===
import subprocess, os
REPO = "/kaggle/working/one-to-all-animation"
if not os.path.exists(os.path.join(REPO, "video-generation", "inference_1.3b.py")):
    subprocess.run(["git", "clone", "--depth", "1",
                    "https://github.com/ssj9596/one-to-all-animation.git",
                    REPO], check=True)
    print("cloned")
else:
    print("repo cached")

# Patch decord import if present (no cp313 wheels) -> use imageio
import re
p = os.path.join(REPO, "video-generation", "inference_1.3b.py")
src = open(p).read()
if "import decord" in src:
    src = src.replace("import decord", "# import decord  # patched: use imageio")
    open(p, "w").write(src)
    print("patched decord import")
print("repo ready")
'''),

code('''# === Run author's inference (1.3B on T4) ===
# This uses the author's inference_1.3b.py directly. See the repo's README for
# the expected input layout; we set env vars to point at our staged paths.
import os, subprocess

REPO = "/kaggle/working/one-to-all-animation"
CKPT_DIR = "/kaggle/working/one-to-all-checkpoints"
WORK = "/kaggle/working/one-to-all-inputs"
OUT = "/kaggle/working/cape-jones-body-replace.mp4"

env = dict(os.environ)
env["ONE2ALL_CKPT"] = os.path.join(CKPT_DIR, "One-to-All-1.3b_2")
env["ONE2ALL_BASE"] = os.path.join(CKPT_DIR, "Wan2.1-T2V-1.3B-Diffusers")
env["ONE2ALL_DRIVING"] = os.path.join(WORK, "driving.mp4")
env["ONE2ALL_REF"] = os.path.join(WORK, "character.png")
env["ONE2ALL_OUT"] = OUT

# NOTE: first live T4 run — if the author's CLI differs, the log will show it
# and we adjust the wiring (not the author's code).
r = subprocess.run(
    ["python3", os.path.join(REPO, "video-generation", "inference_1.3b.py")],
    cwd=os.path.join(REPO, "video-generation"),
    env=env, capture_output=False, text=True)
print("inference exit:", r.returncode)
assert r.returncode == 0, "inference failed — see log above"
assert os.path.exists(OUT), f"expected output missing: {OUT}"
print(f"WROTE {OUT}")
'''),

code('''# === Bulletproof final checkpoint ===
_saver = globals().get("_saver")
_out = "/kaggle/working/cape-jones-body-replace.mp4"
if _saver and getattr(_saver, "enabled", False):
    import os
    if os.path.exists(_out):
        _saver.checkpoint("one-to-all-final", [_out])
        print(f"checkpointed {_out}")
    else:
        print(f"WARNING: expected output missing: {_out}")
    _saver.stop_watchdog()
elif "_saver" in dir() and _saver is None:
    print("saver unavailable — output relies on Save & Run All")
else:
    print("queue-injected final checkpoint will handle saving")
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

out_path = os.path.join(OUT_DIR, "cape_jones_one_to_all_kaggle.ipynb")
with open(out_path, "w") as f:
    json.dump(nb, f, indent=1)
print(f"Wrote {out_path} ({len(cells)} cells)")

for i, c in enumerate(cells):
    if c["cell_type"] == "code":
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        lines = [l for l in src.splitlines()
                 if not l.strip().startswith(("%", "!"))]
        try:
            compile("\n".join(lines), f"<cell {i}>", "exec")
        except SyntaxError as e:
            print(f"SYNTAX ERROR in cell {i}: {e}")
            raise
print("All code cells compile OK.")
