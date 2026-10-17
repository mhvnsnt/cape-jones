#!/usr/bin/env python3
"""Generate Viggle-Animate weight-seeding Kaggle notebooks.

Two notebooks (run in order):
  1. seed_viggle_small.ipynb — LoRA (0.94GB) + text_cond (3.7MB) + VAE (3.2GB)
     Publishes to marsfmmg/viggle-animate-weights as v1.
  2. seed_viggle_diffusion.ipynb — diffusion model (21GB) via HTTP Range
     in two ~10.5GB halves (exceeds 20GB kernel disk as a whole).
     Attaches v1, publishes combined as v2.

Zero local disk. Run: python3 gen_seed_viggle.py
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
DATASET_ID = "marsfmmg/viggle-animate-weights"

# Verified sizes 2026-10-16 via X-Linked-Size header
FILES_SMALL = [
    ("loras/viggle_animate_dmd_lora_r64.safetensors", 941893032,
     "https://huggingface.co/drbaph/Viggle-Animate-ComfyUI/resolve/main/loras/viggle_animate_dmd_lora_r64.safetensors"),
    ("text_cond/fixed_embed_fwd_anyframe.safetensors", 3713456,
     "https://huggingface.co/drbaph/Viggle-Animate-ComfyUI/resolve/main/text_cond/fixed_embed_fwd_anyframe.safetensors"),
    ("vae/minimax_h3_video_vae_int8_convrot.safetensors", 3171670912,
     "https://huggingface.co/Kijai/MiniMax-H3-experimental/resolve/main/minimax_h3_video_vae_int8_convrot.safetensors"),
]
DIFFUSION_URL = "https://huggingface.co/drbaph/Viggle-Animate-ComfyUI/resolve/main/diffusion_models/minimax_h3_ref2va_viggle_pruned_int8_convrot.safetensors"
DIFFUSION_SIZE = 21033720080
DIFFUSION_HALF = DIFFUSION_SIZE // 2  # 10516860040


def write_notebook(out_dir, name, kernel_id, cells, dataset_sources=None):
    os.makedirs(out_dir, exist_ok=True)
    nb = {
        "nbformat": 4, "nbformat_minor": 4,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.13"},
        },
        "cells": cells,
    }
    with open(os.path.join(out_dir, name + ".ipynb"), "w") as f:
        json.dump(nb, f, indent=1)
    meta = {
        "id": kernel_id, "title": kernel_id.split("/")[-1],
        "code_file": name + ".ipynb", "language": "python",
        "kernel_type": "notebook", "is_private": True,
        "enable_gpu": False, "enable_internet": True,
        "dataset_sources": dataset_sources or [],
        "competition_sources": [], "kernel_sources": [],
    }
    with open(os.path.join(out_dir, "kernel-metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"Wrote {out_dir}/")


def md_cell(lines):
    return {"cell_type": "markdown", "metadata": {}, "source": lines}


def code_cell(lines):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": lines}


# ---- Notebook 1: small files ----
files_py = "[\n" + ",\n".join(
    f'    ("{p}", {s},\n     "{u}")' for p, s, u in FILES_SMALL) + "\n]"

cells1 = [
    md_cell([
        "# Seed Viggle-Animate small weights\n",
        "\n",
        "Downloads LoRA + text_cond + VAE (~4.2GB) and publishes to\n",
        f"`{DATASET_ID}`. Run this first.\n",
    ]),
    code_cell([
        "# === Download small weight files ===\n",
        "import subprocess, os\n",
        "\n",
        "SEED = \"/kaggle/working/seed\"\n",
        f"FILES = {files_py}\n",
        "\n",
        "for relpath, expected, url in FILES:\n",
        "    out = os.path.join(SEED, relpath)\n",
        "    os.makedirs(os.path.dirname(out), exist_ok=True)\n",
        "    if os.path.exists(out) and os.path.getsize(out) == expected:\n",
        "        print(f\"SKIP {relpath} (already present)\")\n",
        "        continue\n",
        "    print(f\"Downloading {relpath} ({expected/1e9:.2f} GB)...\")\n",
        "    subprocess.run([\"wget\", \"-q\", \"--show-progress\", url, \"-O\", out], check=True)\n",
        "    actual = os.path.getsize(out)\n",
        "    assert actual == expected, f\"SIZE MISMATCH {relpath}: {actual} != {expected}\"\n",
        "    print(f\"  OK ({actual/1e9:.2f} GB)\")\n",
        "print(\"\\nAll small files downloaded and verified.\")\n",
    ]),
    code_cell([
        "# === Publish as dataset version ===\n",
        "import subprocess, json, os\n",
        "\n",
        "SEED = \"/kaggle/working/seed\"\n",
        f"DATASET_ID = \"{DATASET_ID}\"\n",
        "meta = {\"title\": \"Viggle-Animate Model Weights\", \"id\": DATASET_ID,\n",
        "        \"licenses\": [{\"name\": \"Apache-2.0\"}]}\n",
        "with open(os.path.join(SEED, \"dataset-metadata.json\"), \"w\") as f:\n",
        "    json.dump(meta, f, indent=2)\n",
        "print(\"Publishing (4GB, takes a few minutes)...\")\n",
        "r = subprocess.run([\"kaggle\", \"datasets\", \"version\", \"-p\", SEED,\n",
        "    \"-m\", \"Viggle small weights: LoRA + text_cond + VAE\"],\n",
        "    capture_output=True, text=True, timeout=3600)\n",
        "print((r.stdout or \"\")[-300:])\n",
        "assert r.returncode == 0, \"Publish FAILED: \" + (r.stderr or \"\")[-500:]\n",
        "print(\"Done.\")\n",
    ]),
]
write_notebook(os.path.join(BASE, "seed-output-viggle-small"),
               "seed_viggle_small", "marsfmmg/seed-viggle-small-weights", cells1)

# ---- Notebook 2: diffusion model in halves ----
cells2 = [
    md_cell([
        "# Seed Viggle diffusion model (21GB via Range halves)\n",
        "\n",
        "The diffusion model exceeds the 20GB kernel disk, so it's downloaded\n",
        "in two ~10.5GB halves via HTTP Range requests. Attaches the v1 dataset\n",
        "(small files) and publishes everything together as v2.\n",
        "Run AFTER seed_viggle_small.\n",
    ]),
    code_cell([
        "# === Download diffusion model in two halves ===\n",
        "import subprocess, os\n",
        "\n",
        "SEED = \"/kaggle/working/seed\"\n",
        "os.makedirs(SEED, exist_ok=True)\n",
        f"URL = \"{DIFFUSION_URL}\"\n",
        f"TOTAL = {DIFFUSION_SIZE}\n",
        f"HALF = {DIFFUSION_HALF}\n",
        "P1 = os.path.join(SEED, \"diffusion_models\", \"diffusion_part1.bin\")\n",
        "P2 = os.path.join(SEED, \"diffusion_models\", \"diffusion_part2.bin\")\n",
        "os.makedirs(os.path.dirname(P1), exist_ok=True)\n",
        "\n",
        "def dl_range(out, start, end):\n",
        "    if os.path.exists(out) and os.path.getsize(out) == (end - start + 1):\n",
        "        print(f\"SKIP {os.path.basename(out)} (present)\")\n",
        "        return\n",
        "    print(f\"Downloading bytes {start}-{end} ({(end-start+1)/1e9:.1f} GB)...\")\n",
        "    subprocess.run([\"curl\", \"-s\", \"--show-progress\",\n",
        "        \"-H\", f\"Range: bytes={start}-{end}\", URL, \"-o\", out], check=True)\n",
        "    sz = os.path.getsize(out)\n",
        "    assert sz == (end - start + 1), f\"SIZE MISMATCH: {sz}\"\n",
        "    print(f\"  OK ({sz/1e9:.2f} GB)\")\n",
        "\n",
        "dl_range(P1, 0, HALF - 1)\n",
        "dl_range(P2, HALF, TOTAL - 1)\n",
        "print(f\"\\nBoth halves done. Total: {(os.path.getsize(P1)+os.path.getsize(P2))/1e9:.1f} GB\")\n",
    ]),
    code_cell([
        "# === Reassemble + verify, then publish ===\n",
        "import subprocess, json, os, hashlib\n",
        "\n",
        "SEED = \"/kaggle/working/seed\"\n",
        f"DATASET_ID = \"{DATASET_ID}\"\n",
        "P1 = os.path.join(SEED, \"diffusion_models\", \"diffusion_part1.bin\")\n",
        "P2 = os.path.join(SEED, \"diffusion_models\", \"diffusion_part2.bin\")\n",
        "FULL = os.path.join(SEED, \"diffusion_models\",\n",
        "    \"minimax_h3_ref2va_viggle_pruned_int8_convrot.safetensors\")\n",
        "\n",
        "# Reassemble\n",
        "print(\"Reassembling diffusion model...\")\n",
        "with open(FULL, \"wb\") as out:\n",
        "    for p in [P1, P2]:\n",
        "        with open(p, \"rb\") as f:\n",
        "            while chunk := f.read(64*1024*1024):\n",
        "                out.write(chunk)\n",
        f"assert os.path.getsize(FULL) == {DIFFUSION_SIZE}, \"reassembly size wrong\"\n",
        "print(f\"Reassembled OK ({os.path.getsize(FULL)/1e9:.1f} GB)\")\n",
        "# Free disk before publish\n",
        "os.remove(P1); os.remove(P2)\n",
        "print(\"Halves removed, full file kept.\")\n",
        "\n",
        "# Publish (v1 small files are already in the dataset; this adds diffusion)\n",
        "# NOTE: `kaggle datasets version` replaces content — copy v1 files first.\n",
        "print(\"Copying v1 small files from attached dataset...\")\n",
        "subprocess.run([\"cp\", \"-r\", \"/kaggle/input/viggle-animate-weights/loras\",\n",
        "    os.path.join(SEED, \"loras\")], check=True)\n",
        "subprocess.run([\"cp\", \"-r\", \"/kaggle/input/viggle-animate-weights/text_cond\",\n",
        "    os.path.join(SEED, \"text_cond\")], check=True)\n",
        "subprocess.run([\"cp\", \"-r\", \"/kaggle/input/viggle-animate-weights/vae\",\n",
        "    os.path.join(SEED, \"vae\")], check=True)\n",
        "print(\"v1 files copied.\")\n",
        "\n",
        "meta = {\"title\": \"Viggle-Animate Model Weights\", \"id\": DATASET_ID,\n",
        "        \"licenses\": [{\"name\": \"Apache-2.0\"}]}\n",
        "with open(os.path.join(SEED, \"dataset-metadata.json\"), \"w\") as f:\n",
        "    json.dump(meta, f, indent=2)\n",
        "print(\"Publishing v2 (25GB, this takes a while)...\")\n",
        "r = subprocess.run([\"kaggle\", \"datasets\", \"version\", \"-p\", SEED,\n",
        "    \"-m\", \"Add diffusion model 21GB (reassembled from Range halves)\"],\n",
        "    capture_output=True, text=True, timeout=7200)\n",
        "print((r.stdout or \"\")[-300:])\n",
        "assert r.returncode == 0, \"Publish FAILED: \" + (r.stderr or \"\")[-500:]\n",
        "print(\"\\nDone. All Viggle weights cached.\")\n",
    ]),
]
write_notebook(os.path.join(BASE, "seed-output-viggle-diffusion"),
               "seed_viggle_diffusion", "marsfmmg/seed-viggle-diffusion",
               cells2, dataset_sources=["marsfmmg/viggle-animate-weights"])

print("\nNext steps:")
print("  1. cd seed-output-tooncrafter && kaggle kernels push -p .")
print("  2. cd seed-output-viggle-small && kaggle kernels push -p .")
print("  3. (after small completes) cd seed-output-viggle-diffusion && kaggle kernels push -p .")
