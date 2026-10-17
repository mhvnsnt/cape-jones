#!/usr/bin/env python3
"""Generate the ToonCrafter weight-seeding Kaggle notebook.

Downloads model.ckpt (~10.5GB) from HuggingFace inside Kaggle and publishes
it as a dataset version to marsfmmg/tooncrafter-weights. Zero local disk.

Run: python3 gen_seed_tooncrafter.py
Then: kaggle kernels push -p ./seed-output/
"""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed-output-tooncrafter")
os.makedirs(OUT, exist_ok=True)

HF_URL = "https://huggingface.co/Doubiiu/ToonCrafter/resolve/main/model.ckpt"
DATASET_ID = "marsfmmg/tooncrafter-weights"
EXPECTED_SIZE = 10502492136  # bytes, verified 2026-10-16 via X-Linked-Size

cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Seed ToonCrafter weights to Kaggle dataset\n",
            "\n",
            "Downloads `model.ckpt` (~10.5GB) from HuggingFace and publishes it as\n",
            f"`{DATASET_ID}`. Run once. Future notebooks attach the dataset instead\n",
            "of re-downloading.\n",
        ],
    },
    {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# === Download model.ckpt from HuggingFace ===\n",
            "import subprocess, os\n",
            "\n",
            "SEED = \"/kaggle/working/seed\"\n",
            "os.makedirs(SEED, exist_ok=True)\n",
            f"URL = \"{HF_URL}\"\n",
            f"EXPECTED = {EXPECTED_SIZE}\n",
            "OUT_PATH = os.path.join(SEED, \"model.ckpt\")\n",
            "\n",
            "if os.path.exists(OUT_PATH) and os.path.getsize(OUT_PATH) == EXPECTED:\n",
            "    print(f\"model.ckpt already present ({os.path.getsize(OUT_PATH)/1e9:.1f} GB) — skipping download\")\n",
            "else:\n",
            "    print(f\"Downloading model.ckpt ({EXPECTED/1e9:.1f} GB) from HuggingFace...\")\n",
            "    subprocess.run([\"wget\", \"-q\", \"--show-progress\", URL, \"-O\", OUT_PATH], check=True)\n",
            "    actual = os.path.getsize(OUT_PATH)\n",
            "    print(f\"Downloaded: {actual/1e9:.2f} GB\")\n",
            "    assert actual == EXPECTED, f\"SIZE MISMATCH: got {actual}, expected {EXPECTED}\"\n",
            "    print(\"Size verified.\")\n",
        ],
    },
    {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# === Publish as dataset version ===\n",
            "import subprocess, json, os\n",
            "\n",
            "SEED = \"/kaggle/working/seed\"\n",
            f"DATASET_ID = \"{DATASET_ID}\"\n",
            "\n",
            "# Write dataset metadata (required for `kaggle datasets version`)\n",
            "meta = {\n",
            "    \"title\": \"ToonCrafter Model Weights\",\n",
            "    \"id\": DATASET_ID,\n",
            "    \"licenses\": [{\"name\": \"Apache-2.0\"}],\n",
            "}\n",
            "with open(os.path.join(SEED, \"dataset-metadata.json\"), \"w\") as f:\n",
            "    json.dump(meta, f, indent=2)\n",
            "print(\"Metadata written.\")\n",
            "\n",
            "# Publish (kernel is pre-authenticated as notebook owner)\n",
            "print(\"Publishing dataset version (this takes a while for 10GB)...\")\n",
            "r = subprocess.run(\n",
            "    [\"kaggle\", \"datasets\", \"version\", \"-p\", SEED,\n",
            "     \"-m\", \"ToonCrafter model.ckpt 10.5GB — seeded from HuggingFace\"],\n",
            "    capture_output=True, text=True, timeout=3600)\n",
            "print(r.stdout[-500:] if r.stdout else \"\")\n",
            "print(r.stderr[-500:] if r.stderr else \"\")\n",
            "assert r.returncode == 0, \"Dataset publish FAILED\"\n",
            "print(\"\\nDone. Weights are now cached at\", DATASET_ID)\n",
        ],
    },
]

nb = {
    "nbformat": 4,
    "nbformat_minor": 4,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.13"},
    },
    "cells": cells,
}

ipynb_path = os.path.join(OUT, "seed_tooncrafter_weights.ipynb")
with open(ipynb_path, "w") as f:
    json.dump(nb, f, indent=1)
print(f"Wrote {ipynb_path}")

meta = {
    "id": "marsfmmg/seed-tooncrafter-weights",
    "title": "seed-tooncrafter-weights",
    "code_file": "seed_tooncrafter_weights.ipynb",
    "language": "python",
    "kernel_type": "notebook",
    "is_private": True,
    "enable_gpu": False,
    "enable_internet": True,
    "dataset_sources": [],
    "competition_sources": [],
    "kernel_sources": [],
}
with open(os.path.join(OUT, "kernel-metadata.json"), "w") as f:
    json.dump(meta, f, indent=2)
print(f"Wrote kernel-metadata.json")
print(f"\nNext: cd {OUT} && kaggle kernels push -p .")
