#!/usr/bin/env python3
"""
ldf_vfi_wrapper.py — wiring for LDF-VFI.

Tool lives at production/tools/LDF-VFI/ (pulled via PR #33).
Requires ~20GB GPU and the pretrained weights from HuggingFace:
  https://huggingface.co/onecat-ai/LDF-VFI

Usage:
  python ldf_vfi_wrapper.py input.mp4 output_dir/ \
      --model /path/to/LDF-VFI/transformer \
      --vae /path/to/LDF-VFI/Wan2.1_VAE_cond_v2.pth \
      --temporal-sf 2

Defaults match the upstream quick_start/generate.sh (temporal_sf=8).
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


TOOL_ROOT = Path(__file__).resolve().parents[2] / "tools" / "LDF-VFI"


def main():
    ap = argparse.ArgumentParser(description="LDF-VFI wrapper")
    ap.add_argument("input", help="Input video or folder of videos")
    ap.add_argument("output_dir", help="Output directory")
    ap.add_argument("--model", required=True, help="Path to LDF-VFI transformer weights")
    ap.add_argument("--vae", required=True, help="Path to Wan2.1_VAE_cond_v2.pth")
    ap.add_argument("--temporal-sf", type=int, default=2,
                    help="Temporal scale factor (2-16, default 2 for 12->24)")
    ap.add_argument("--sp-size", type=int, default=1, help="Sequence parallel size")
    args = ap.parse_args()

    if not TOOL_ROOT.exists():
        print(f"LDF-VFI not found at {TOOL_ROOT}", file=sys.stderr)
        print("Expected: production/tools/LDF-VFI/ (PR #33)", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.model) or not os.path.exists(args.vae):
        print("Model or VAE path missing. Download from https://huggingface.co/onecat-ai/LDF-VFI")
        sys.exit(1)

    generate = TOOL_ROOT / "generate.py"
    if not generate.exists():
        print(f"generate.py missing: {generate}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    # Mirror the args from quick_start/generate.sh
    cmd = [
        "accelerate", "launch",
        "--num_machines=1", "--num_processes=1",
        str(generate),
        f"--model_path={args.model}",
        "--attention_type=slide_chunk_all_block_2x1x1",
        "--temporal_upsample=nearest",
        "--num_frames=60",
        "--vae_type=wan2_1_cond_v2",
        f"--vae_path={args.vae}",
        "--vae_batch_size=16",
        "--tile_min_h=256", "--tile_min_w=256", "--tile_min_t=20",
        "--tile_stride_h=192", "--tile_stride_w=192",
        "--spatial_compression_ratio=8",
        "--temporal_compression_ratio=4",
        "--sampling_steps=16",
        "--t_shift=8",
        f"--data={args.input}",
        f"--temporal_sf={args.temporal_sf}",
        f"--output_dir={args.output_dir}",
        "--fps=30",
        f"--sp_size={args.sp_size}",
    ]
    print("Running LDF-VFI:")
    print(" ".join(cmd))
    r = subprocess.run(cmd, cwd=TOOL_ROOT)
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
