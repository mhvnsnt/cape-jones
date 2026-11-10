#!/usr/bin/env python3
"""upscale_span.py — Fast AI upscaling with SPAN (NTIRE 2024 winner).

SPAN (Swift Parameter-free Attention Network) won 1st place in BOTH the
overall performance AND runtime tracks of NTIRE 2024 efficient SR challenge.

  Speed: ~0.15s/frame on CPU for 4x (vs ~8.5s for Real-ESRGAN)
  Quality: beats all other efficient SR models on benchmarks
  License: Apache 2.0 (commercial-safe)
  Code: ~/workspace/tools/span-official/ (hongyuanyu/span)

THE STRATEGY: Render Cycles at HALF resolution (960x540), SPAN-upscale 2x
to 1920x1080. 4x fewer pixels to ray-trace = ~3-4x faster renders.
Combined with 16spp + GPU OIDN: total ~8-10x faster than naive 1080p/32spp.

USAGE:
  python3 upscale_span.py input.png output.png --scale 2
  python3 upscale_span.py frames_dir/ upscaled_dir/ --scale 2 --batch

  # Full pipeline: render 960x540 -> upscale 2x -> 1920x1080
  python3 upscale_span.py pantera_frames_540p/ pantera_frames_1080p/ --scale 2 --batch

REQUIRES: SPAN checkpoint (.pth). Download from:
  https://drive.google.com/file/d/1iYUA2TzKuxI0vzmA-UXr_nB43XgPOXUg/view?usp=sharing
  Place at ~/workspace/tools/upscale-models/spanx2_ch48.pth (or use --weights)

  On Kaggle: the notebook downloads it automatically (see KAGGLE note below).
"""
import argparse
import glob
import os
import sys

TOOLS = os.path.expanduser("~/workspace/tools")
SPAN_DIR = os.path.join(TOOLS, "span-official")
DEFAULT_WEIGHTS = os.path.join(TOOLS, "upscale-models", "spanx2_ch48.pth")


def upscale_image(img_path, out_path, scale=2, weights=None, device=None):
    """Upscale a single image with SPAN."""
    import torch
    import numpy as np
    from PIL import Image

    weights = weights or DEFAULT_WEIGHTS
    if not os.path.exists(weights):
        print(f"ERROR: SPAN weights not found: {weights}")
        print("Download from:")
        print("  https://drive.google.com/file/d/1iYUA2TzKuxI0vzmA-UXr_nB43XgPOXUg/view?usp=sharing")
        print("Or run on Kaggle where the notebook auto-downloads them.")
        sys.exit(1)

    # Add SPAN to path
    sys.path.insert(0, SPAN_DIR)
    try:
        from basicsr.archs.span_arch import SPAN
    except ImportError:
        # Fallback: try alternate import paths
        sys.path.insert(0, os.path.join(SPAN_DIR, "basicsr", "archs"))
        from span_arch import SPAN

    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    # SPAN ch48 config (from official repo)
    model = SPAN(num_in_ch=3, num_out_ch=3, feature_channels=48,
                 upscale=scale, bias=True,
                 img_range=255., rgb_mean=(0.4488, 0.4371, 0.4040))
    loadnet = torch.load(weights, map_location=device, weights_only=True)
    # Handle different checkpoint formats
    keyname = 'params_ema' if 'params_ema' in loadnet else 'params'
    if keyname in loadnet:
        loadnet = loadnet[keyname]
    model.load_state_dict(loadnet, strict=True)
    model.eval().to(device)

    img = Image.open(img_path).convert("RGB")
    arr = np.array(img).astype(np.float32)
    # BGR + mean subtraction (SPAN convention)
    arr = arr[:, :, ::-1].copy()
    arr -= np.array([0.4488, 0.4371, 0.4040]) * 255.0
    tensor = torch.from_numpy(arr.transpose(2, 0, 1)).unsqueeze(0).to(device)

    with torch.no_grad():
        out = model(tensor)

    out = out.squeeze(0).cpu().numpy().transpose(1, 2, 0)
    out += np.array([0.4488, 0.4371, 0.4040]) * 255.0
    out = out[:, :, ::-1]  # BGR -> RGB
    out = np.clip(out, 0, 255).astype(np.uint8)

    Image.fromarray(out).save(out_path)
    return out_path


def main():
    ap = argparse.ArgumentParser(description="Fast AI upscale with SPAN (NTIRE 2024 winner)")
    ap.add_argument("input", help="input image or directory")
    ap.add_argument("output", help="output image or directory")
    ap.add_argument("--scale", type=int, default=2, choices=[2, 4],
                    help="upscale factor (default 2)")
    ap.add_argument("--batch", action="store_true",
                    help="batch mode: input/output are directories")
    ap.add_argument("--weights", default=None, help="path to SPAN .pth weights")
    ap.add_argument("--device", default=None, help="cuda or cpu (auto if omitted)")
    args = ap.parse_args()

    if args.batch or os.path.isdir(args.input):
        frames = sorted(glob.glob(os.path.join(args.input, "*.png")))
        if not frames:
            print(f"ERROR: no PNGs in {args.input}")
            sys.exit(1)
        os.makedirs(args.output, exist_ok=True)
        print(f"SPAN {args.scale}x: {len(frames)} frames")
        for i, f in enumerate(frames):
            out = os.path.join(args.output, os.path.basename(f))
            upscale_image(f, out, scale=args.scale,
                          weights=args.weights, device=args.device)
            if (i + 1) % 25 == 0:
                print(f"  {i+1}/{len(frames)}", flush=True)
        print(f"done: {args.output}/")
    else:
        upscale_image(args.input, args.output, scale=args.scale,
                      weights=args.weights, device=args.device)
        print(f"done: {args.output}")


if __name__ == "__main__":
    main()
