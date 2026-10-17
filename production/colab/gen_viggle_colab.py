#!/usr/bin/env python3
"""Generate cape_jones_viggle_colab.ipynb — Google Colab T4 Viggle-Animate
AI body replacement notebook.

This is the Colab port of production/ai-body-replace/gen_notebook.py.
Colab serves as a backup/parallel GPU lane alongside Kaggle.

Key differences from the Kaggle version:
- /kaggle/working/ -> /content/ (Colab's working dir)
- No Kaggle dataset cache -> models download from HuggingFace every run (~25GB)
  Optional: mount Google Drive to cache weights across sessions.
- File upload: Colab's files.upload() widget (no Kaggle file panel)
- Colab-idiomatic `!` shell commands
- Output: files.download() widget (Colab sessions time out — download immediately)

WHAT THIS DOES:
    driving video (you doing motion) + reference image (Cape Jones)
    -> Cape Jones performing YOUR motion. Free, unlimited, no paywall.

Account: fmmg.mars@gmail.com (owner's Google — Colab sign-in)

MODELS (from HuggingFace, ~25GB total):
- diffusion: drbaph/Viggle-Animate-ComfyUI (21GB pruned INT8)
- lora:      viggle_animate_dmd_lora_r64.safetensors (0.94GB)
- text_cond: fixed_embed_fwd_anyframe.safetensors
- vae:       Kijai/MiniMax-H3-experimental (3.17GB INT8)

VRAM: T4 16GB. Pruned INT8 + --lowvram works. ~5-10 min per 124-frame clip.
"""
import json
import os

RAW = ("https://raw.githubusercontent.com/mhvnsnt/cape-jones/"
       "main/production/ai-body-replace")


def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}


def code(src):
    return {"cell_type": "code", "metadata": {},
            "execution_count": None, "outputs": [], "source": src}


cells = [
md("""# Cape Jones — Viggle-Animate AI Body Replacement on Google Colab (T4 GPU)

**What this does:** Upload a video of yourself doing something + a picture of
Cape Jones → the notebook puts Cape Jones on your body, doing your exact
motion. **Free. Unlimited. No paywall. No 24-hour wait.**

This is the **Colab backup/parallel lane** — same pipeline as the Kaggle
notebook (`production/ai-body-replace/`), adapted for Colab.

**Before running:** Runtime → Change runtime type → **T4 GPU**. Then
**Runtime → Run all**.

**Sign in with:** fmmg.mars@gmail.com (owner's Google account)

**How to use:**
1. Run all cells (takes ~20-30 min first time — downloads ~25GB of models)
2. When you see **"👆 UPLOAD YOUR FILES HERE"**, upload:
   - `driving_video.mp4` — video of YOU doing the motion (under 10 sec)
   - `character.png` — picture of Cape Jones
3. Run the remaining cells → download your video

**Pipeline:**
1. GPU check (must be Tesla T4)
2. Install ComfyUI + Viggle-Animate custom nodes
3. Download quantized models from HuggingFace (~25GB)
4. ⏸️ **YOU upload driving_video.mp4 + character.png**
5. Run Viggle-Animate workflow via ComfyUI API (headless)
6. Download output video → `cape-jones-body-replace.mp4`
"""),

code('''# === Cell 1: GPU check ===
# Colab: Runtime → Change runtime type → T4 GPU
!nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
'''),

code('''# === Cell 2: Install ComfyUI + Viggle-Animate nodes ===
!git clone --depth 1 https://github.com/comfyanonymous/ComfyUI.git /content/ComfyUI 2>/dev/null || echo "ComfyUI already cloned."
!pip install -q torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
!pip install -q -r /content/ComfyUI/requirements.txt
!git clone --depth 1 https://github.com/Saganaki22/ComfyUI-Viggle-Animate-H3.git /content/ComfyUI/custom_nodes/ComfyUI-Viggle-Animate-H3 2>/dev/null || echo "Viggle nodes already cloned."
!git clone --depth 1 https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git /content/ComfyUI/custom_nodes/ComfyUI-VideoHelperSuite 2>/dev/null || echo "VHS already cloned."
!pip install -q -r /content/ComfyUI/custom_nodes/ComfyUI-VideoHelperSuite/requirements.txt
print("ComfyUI + nodes installed.")
'''),

code('''# === Cell 3: Download Viggle-Animate models from HuggingFace (~25GB) ===
# Colab has no dataset cache like Kaggle. Options:
#   A) Download every run (~15-20 min) — simple, default below
#   B) Mount Google Drive and cache: uncomment the Drive lines
import os

# --- Optional Drive cache (uncomment to use) ---
# from google.colab import drive
# drive.mount('/content/drive')
# DRIVE_MODELS = "/content/drive/MyDrive/cape-jones-weights/viggle"
# ---

BASE = "/content/ComfyUI/models"
DMODEL = os.path.join(BASE, "diffusion_models")
LORA = os.path.join(BASE, "loras")
TCOND = os.path.join(BASE, "text_cond")
VAE = os.path.join(BASE, "vae")
for d in [DMODEL, LORA, TCOND, VAE]:
    os.makedirs(d, exist_ok=True)

MODELS = [
    ("minimax_h3_ref2va_viggle_pruned_int8_convrot.safetensors", DMODEL, 21033720080,
     "https://huggingface.co/drbaph/Viggle-Animate-ComfyUI/resolve/main/diffusion_models/minimax_h3_ref2va_viggle_pruned_int8_convrot.safetensors"),
    ("viggle_animate_dmd_lora_r64.safetensors", LORA, 941893032,
     "https://huggingface.co/drbaph/Viggle-Animate-ComfyUI/resolve/main/loras/viggle_animate_dmd_lora_r64.safetensors"),
    ("fixed_embed_fwd_anyframe.safetensors", TCOND, 3713456,
     "https://huggingface.co/drbaph/Viggle-Animate-ComfyUI/resolve/main/text_cond/fixed_embed_fwd_anyframe.safetensors"),
    ("minimax_h3_video_vae_int8_convrot.safetensors", VAE, 3171670912,
     "https://huggingface.co/Kijai/MiniMax-H3-experimental/resolve/main/minimax_h3_video_vae_int8_convrot.safetensors"),
]

for fname, ddir, expected, url in MODELS:
    out = os.path.join(ddir, fname)
    if os.path.exists(out) and os.path.getsize(out) == expected:
        print(f"OK {fname} already present ({os.path.getsize(out)/1e9:.1f} GB)")
    else:
        print(f"Downloading {fname} ({expected/1e9:.1f} GB)...")
        !wget -q --show-progress {url} -O {out}
        assert os.path.getsize(out) == expected, f"size mismatch for {fname}"
        print(f"OK {fname} done")

print("All models ready.")
'''),

md("""## 👆 UPLOAD YOUR FILES HERE

Run the next cell, then upload when prompted:

1. **`driving_video.mp4`** — video of YOU doing the motion (under 10 sec, MP4)
2. **`character.png`** — picture of Cape Jones (PNG or JPG, front-facing works best)
"""),

code('''# === Cell 4: Upload your files ===
from google.colab import files
import os, shutil

print("Upload driving_video.mp4 and character.png when prompted...")
uploaded = files.upload()

for fname in uploaded:
    dst = f"/content/{fname}"
    # files.upload() saves to cwd; ensure it's in /content
    if os.path.exists(fname) and fname != dst:
        shutil.move(fname, dst)
    print(f"Uploaded: {fname} ({os.path.getsize(dst)/1e6:.1f} MB)")

# Normalize names
if os.path.exists("/content/driving_video.mp4"):
    print("OK driving_video.mp4")
else:
    # try to find any mp4
    mp4s = [f for f in os.listdir("/content") if f.endswith(".mp4")]
    if mp4s:
        shutil.copy(f"/content/{mp4s[0]}", "/content/driving_video.mp4")
        print(f"OK using {mp4s[0]} as driving_video.mp4")

char = None
for ext in [".png", ".jpg", ".jpeg", ".JPG", ".PNG"]:
    for f in os.listdir("/content"):
        if f.lower().endswith(ext) and "driving" not in f.lower():
            char = f"/content/{f}"
            break
    if char:
        break
assert char, "Upload a character image (PNG/JPG)!"
print(f"OK character image: {char}")
'''),

code(f'''# === Cell 5: Set up ComfyUI inputs + download workflow ===
import os, shutil, subprocess, time, sys

COMFY = "/content/ComfyUI"
INPUT_DIR = os.path.join(COMFY, "input")
os.makedirs(INPUT_DIR, exist_ok=True)

shutil.copy("/content/driving_video.mp4", os.path.join(INPUT_DIR, "driving_video.mp4"))

# Find and copy character image
CHAR_FILE = None
for f in os.listdir("/content"):
    fl = f.lower()
    if fl.endswith((".png", ".jpg", ".jpeg")) and "driving" not in fl:
        CHAR_FILE = f
        shutil.copy(f"/content/{{f}}", os.path.join(INPUT_DIR, f))
        break
print(f"Character file: {{CHAR_FILE}}")

# Download pre-built workflow from repo
WF_URL = "{RAW}/viggle_workflow_api.json"
WF_DST = "/content/viggle_workflow_api.json"
!wget -q {{WF_URL}} -O {{WF_DST}}
print("Workflow loaded.")

# Start ComfyUI headless (--lowvram for T4)
print("Starting ComfyUI server...")
server = subprocess.Popen(
    [sys.executable, "main.py", "--listen", "127.0.0.1", "--port", "8188",
     "--lowvram", "--disable-auto-launch"],
    cwd=COMFY, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(25)
print("ComfyUI server running.")
'''),

code('''# === Cell 6: Run Viggle-Animate via ComfyUI API ===
import json, urllib.request, time, os, uuid, shutil, glob

with open("/content/viggle_workflow_api.json") as f:
    workflow = json.load(f)

for node_id, node in workflow.items():
    if node.get("class_type") == "VHS_LoadVideo":
        for k in node.get("inputs", {}):
            if "video" in k.lower():
                node["inputs"][k] = "driving_video.mp4"
    if node.get("class_type") == "LoadImage":
        node["inputs"]["image"] = CHAR_FILE

client_id = str(uuid.uuid4())

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_history(prompt_id):
    req = urllib.request.Request(f"http://127.0.0.1:8188/history/{prompt_id}")
    return json.loads(urllib.request.urlopen(req).read())

print("Queueing Viggle-Animate workflow...")
resp = queue_prompt(workflow)
prompt_id = resp['prompt_id']
print(f"Prompt ID: {prompt_id}")
print("Rendering... (~5-10 min for 124 frames)")

start = time.time()
while True:
    time.sleep(15)
    hist = get_history(prompt_id)
    if prompt_id in hist:
        status = hist[prompt_id].get('status', {})
        if status.get('completed', False):
            break
    elapsed = (time.time() - start) / 60
    print(f"  ... still rendering ({elapsed:.1f} min)")

print("Done! Finding output...")
OUT_DIR = "/content/ComfyUI/output"
found = None
for root, dirs, files_ in os.walk(OUT_DIR):
    for f in sorted(files_, reverse=True):
        if f.endswith('.mp4'):
            found = os.path.join(root, f)
            break
    if found:
        break

assert found, "No output MP4 found!"
dst = "/content/cape-jones-body-replace.mp4"
shutil.copy(found, dst)
print(f"Output saved: {dst} ({os.path.getsize(dst)/1e6:.1f} MB)")
'''),

code('''# === Cell 7: Download the finished video ===
# Colab sessions time out — download NOW, don't rely on the file persisting.
from google.colab import files
files.download("/content/cape-jones-body-replace.mp4")
print("Download started.")
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
                        "cape_jones_viggle_colab.ipynb")
with open(out_path, "w") as f:
    json.dump(nb, f, indent=1)
print(f"Wrote {out_path} ({len(cells)} cells)")

# compile-check (strip magics + shell continuations)
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
