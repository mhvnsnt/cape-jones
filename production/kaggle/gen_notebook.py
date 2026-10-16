#!/usr/bin/env python3
"""Generate cape_jones_rife_kaggle.ipynb — Kaggle GPU T4 RIFE interpolation
notebook for the Cape Jones expressions video (12fps -> 24fps).

Races against the CPU pipeline currently running on the VM.
Upload the .ipynb to Kaggle's notebook editor (browser lane).
"""
import json

BRANCH = "kaggle-rife"
RAW = (f"https://raw.githubusercontent.com/mhvnsnt/cape-jones/"
       f"{BRANCH}/production/kaggle/rife")
VIDEO_SHA = "0f8ef914247cad0bdc06d3543117824ea7fb30926d35c176672337d63d9d56ed"
WEIGHTS_SHA = ("2b48d6f7c7c09c109ad50372e9d9dc722a75859dc20e8832a62826ecede35ad3")

MODEL_FILES = ["IFNet.py", "IFNet_2R.py", "IFNet_m.py", "RIFE.py",
               "laplacian.py", "loss.py", "refine.py", "refine_2R.py",
               "warplayer.py"]


def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}


def code(src):
    return {"cell_type": "code", "metadata": {},
            "execution_count": None, "outputs": [], "source": src}


cells = [
md("""# Cape Jones — RIFE interpolation on Kaggle T4 GPU

Interpolates `input-12fps.mp4` (217 frames @ 12fps, 1080x1920) to 24fps
using RIFE v4 on a **Tesla T4 GPU**. This is a speed race against the CPU
pipeline running on the VM — same input, same model, same `--exp 1`
(one interpolated frame per pair).

**Before running:** Settings (right panel) -> **Accelerator: GPU T4 x2**,
**Internet: ON**. Then **Run All**.

Pipeline in this notebook:
1. GPU check (must be Tesla T4)
2. pip deps (torch is preinstalled on Kaggle; ensure opencv)
3. Download input video + RIFE model code + weights from GitHub (SHA-256 verified)
4. Extract frames with ffmpeg
5. RIFE inference on CUDA (exp=1: 12fps -> 24fps)
6. Assemble 24fps MP4 with ffmpeg -> `/kaggle/working/` for download
"""),

code('''# === GPU check ===
import subprocess
r = subprocess.run(["nvidia-smi", "--query-gpu=name,driver_version,memory.total",
                    "--format=csv"], capture_output=True, text=True)
print(r.stdout.strip() or "NO GPU VISIBLE -- enable Accelerator: GPU in Settings!")
assert "Tesla T4" in r.stdout, "Expected a Tesla T4"
'''),

code('''# === Python deps ===
import subprocess, sys
# Kaggle ships torch+torchvision; make sure opencv is present
r = subprocess.run([sys.executable, "-c", "import torch, cv2; "
                    "print('torch', torch.__version__, '| cuda:', torch.cuda.is_available())"],
                   capture_output=True, text=True)
print(r.stdout.strip() or r.stderr.strip())
if r.returncode != 0 or "cv2" in r.stderr:
    subprocess.run([sys.executable, "-m", "pip", "-q", "install",
                    "opencv-python-headless"], check=True)
    print("installed opencv-python-headless")
import torch
assert torch.cuda.is_available(), "CUDA not available to torch -- check Accelerator setting"
print("CUDA device:", torch.cuda.get_device_name(0))
'''),

code(f'''# === Download RIFE package + input video (SHA-256 verified) ===
import hashlib, os, urllib.request
RAW = "{RAW}"
WORK = "/kaggle/working/rife"
os.makedirs(f"{{WORK}}/model", exist_ok=True)
os.makedirs(f"{{WORK}}/train_log", exist_ok=True)
os.makedirs(f"{{WORK}}/frames_in", exist_ok=True)

def fetch(url, dst, sha=None):
    if os.path.exists(dst) and sha:
        h = hashlib.sha256(open(dst, "rb").read()).hexdigest()
        if h == sha:
            print(f"cached OK: {{os.path.basename(dst)}}")
            return
    print(f"downloading {{os.path.basename(dst)}}...")
    urllib.request.urlretrieve(url, dst)
    if sha:
        h = hashlib.sha256(open(dst, "rb").read()).hexdigest()
        assert h == sha, f"SHA256 MISMATCH for {{dst}}: {{h}}"
    print(f"OK {{os.path.basename(dst)}} ({{os.path.getsize(dst)}} bytes)")

fetch(f"{{RAW}}/input-12fps.mp4", f"{{WORK}}/input-12fps.mp4", "{VIDEO_SHA}")
fetch(f"{{RAW}}/train_log/flownet.pkl", f"{{WORK}}/train_log/flownet.pkl", "{WEIGHTS_SHA}")
for mf in {MODEL_FILES}:
    fetch(f"{{RAW}}/model/{{mf}}", f"{{WORK}}/model/{{mf}}")
print("all assets ready")
'''),

code('''# === Extract frames (ffmpeg) ===
import subprocess, glob, os
WORK = "/kaggle/working/rife"
frames = glob.glob(f"{WORK}/frames_in/*.png")
if not frames:
    subprocess.run(["ffmpeg", "-y", "-v", "error",
                    "-i", f"{WORK}/input-12fps.mp4",
                    f"{WORK}/frames_in/f%04d.png"], check=True)
frames = sorted(glob.glob(f"{WORK}/frames_in/*.png"))
print(f"{len(frames)} frames extracted (expect 217)")
assert len(frames) == 217, "FRAME COUNT MISMATCH"
'''),

code('''# === RIFE inference on CUDA (12fps -> 24fps, exp=1) ===
import os, sys, glob, time
import cv2
import numpy as np
import torch

WORK = "/kaggle/working/rife"
sys.path.insert(0, f"{WORK}/model")
sys.path.insert(0, WORK)
from RIFE import Model

device = torch.device("cuda")
torch.set_grad_enabled(False)

def load_img(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    h, w = img.shape[:2]
    ph = ((h - 1) // 32 + 1) * 32
    pw = ((w - 1) // 32 + 1) * 32
    img = cv2.copyMakeBorder(img, 0, ph - h, 0, pw - w, cv2.BORDER_REFLECT)
    t = (torch.tensor(img.transpose(2, 0, 1)).to(device) / 255.).unsqueeze(0).float()
    return t, h, w

def save(t, h, w, path):
    img = t[0].detach().cpu().numpy().transpose(1, 2, 0)[:h, :w] * 255.
    cv2.imwrite(path, np.clip(np.round(img), 0, 255).astype(np.uint8))

model = Model()
model.load_model(f"{WORK}/train_log", -1)
model.eval(); model.device()
print("RIFE v4 loaded on", torch.cuda.get_device_name(0), flush=True)

files = sorted(glob.glob(f"{WORK}/frames_in/*.png"))
outdir = f"{WORK}/frames_out"
os.makedirs(outdir, exist_ok=True)

t0 = time.time()
out_idx = 1
I0, h, w = load_img(files[0])
save(I0, h, w, f"{outdir}/f{out_idx:04d}.png"); out_idx += 1
for i in range(len(files) - 1):
    I1, _, _ = load_img(files[i + 1])
    mid = model.inference(I0, I1)          # exp=1: one middle frame per pair
    save(mid, h, w, f"{outdir}/f{out_idx:04d}.png"); out_idx += 1
    save(I1, h, w, f"{outdir}/f{out_idx:04d}.png"); out_idx += 1
    I0 = I1
    if (i + 1) % 20 == 0:
        print(f"  {i+1}/{len(files)-1} pairs", flush=True)
mins = (time.time() - t0) / 60
outs = sorted(glob.glob(f"{outdir}/*.png"))
print(f"DONE: {len(outs)} frames out (expect 433), RIFE wall time = {mins:.1f} min", flush=True)
assert len(outs) == 433, "OUTPUT FRAME COUNT MISMATCH"
'''),

code('''# === Assemble 24fps MP4 ===
import subprocess, os, hashlib
WORK = "/kaggle/working/rife"
OUT = "/kaggle/working/cape-jones-expressions-KAGGLE-24fps.mp4"
subprocess.run(["ffmpeg", "-y", "-v", "error",
                "-framerate", "24", "-i", f"{WORK}/frames_out/f%04d.png",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-pix_fmt", "yuv420p", OUT], check=True)
h = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
print(f"{os.path.basename(OUT)}  {os.path.getsize(OUT)} bytes")
print(f"sha256: {h}")
r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                    "stream=r_frame_rate,nb_frames,duration",
                    "-of", "default=noprint_wrappers=1", OUT],
                   capture_output=True, text=True)
print(r.stdout.strip())
print("Download it from the notebook right-panel file viewer (/kaggle/working/).")
'''),
]

nb = {
    "nbformat": 4, "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10"},
        "kaggle": {"accelerator": "GPU", "internet": True},
    },
    "cells": cells,
}
out = "/home/hatch/workspace/cape-jones-build/kaggle-rife/cape_jones_rife_kaggle.ipynb"
import os as _os
_os.makedirs(_os.path.dirname(out), exist_ok=True)
json.dump(nb, open(out, "w"), indent=1)
print("wrote", out)
nb2 = json.load(open(out))
print(f"notebook valid: {len(nb2['cells'])} cells")
for i, c in enumerate(nb2["cells"]):
    src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
    if c["cell_type"] == "code":
        compile(src, f"<cell{i}>", "exec")
print("all code cells compile OK")
