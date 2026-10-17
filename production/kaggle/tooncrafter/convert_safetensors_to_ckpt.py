#!/usr/bin/env python3
"""Convert Kijai's pruned FP16 safetensors to .ckpt format for ToonCrafter.

The official ToonCrafter inference.py uses torch.load() which cannot read
.safetensors files. This script converts once so the standard pipeline works.

Usage:
    python3 convert_safetensors_to_ckpt.py \
        --input tooncrafter_512_interp-fp16.safetensors \
        --output tooncrafter_512_interp_fp16.ckpt

Source: https://huggingface.co/Kijai/DynamiCrafter_pruned/blob/main/tooncrafter_512_interp-fp16.safetensors
License: Apache-2.0 (model weights)
VRAM: 12GB (vs 23GB for full model.ckpt) — fits on Tesla T4
"""
import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Convert safetensors to .ckpt for ToonCrafter")
    parser.add_argument("--input", required=True,
                        help="Input .safetensors file")
    parser.add_argument("--output", required=True,
                        help="Output .ckpt file")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ERROR: input not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading {args.input}...")
    try:
        from safetensors.torch import load_file
    except ImportError:
        print("Installing safetensors...", file=sys.stderr)
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                        "safetensors"], check=True)
        from safetensors.torch import load_file

    import torch

    state_dict = load_file(args.input, device="cpu")
    print(f"Loaded {len(state_dict)} tensors")

    # Wrap in the format inference.py expects: {"state_dict": {...}}
    # (load_model_checkpoint checks for "state_dict" key first)
    ckpt = {"state_dict": state_dict}

    print(f"Saving to {args.output}...")
    torch.save(ckpt, args.output)

    size_gb = os.path.getsize(args.output) / 1e9
    print(f"Done: {args.output} ({size_gb:.2f} GB)")
    print("VRAM requirement: ~12GB (fits on Tesla T4)")


if __name__ == "__main__":
    main()
