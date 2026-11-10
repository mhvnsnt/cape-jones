#!/usr/bin/env python3
"""
instance_animator_wrapper.py — wiring for InstanceAnimator.

Tool lives at production/tools/InstanceAnimator/ (pulled via PR #33).
NOTE: Author says model weights are lost — you must retrain.
This wrapper calls the documented inference entry point when weights exist.

Usage:
  python instance_animator_wrapper.py \
      --base sketch.mp4 \
      --canvas canvas.png \
      --out colored.mp4 \
      --model /path/to/Wan2.1-Fun-14B-Control

Or mock mode (UI test only):
  python instance_animator_wrapper.py --mock
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


TOOL_ROOT = Path(__file__).resolve().parents[2] / "tools" / "InstanceAnimator"


def main():
    ap = argparse.ArgumentParser(description="InstanceAnimator wrapper")
    ap.add_argument("--base", help="Sketch video or frames")
    ap.add_argument("--canvas", help="Canvas guidance image")
    ap.add_argument("--out", help="Output video")
    ap.add_argument("--model", help="Path to Wan2.1-Fun-14B-Control weights")
    ap.add_argument("--mock", action="store_true", help="Run web UI in mock mode")
    args = ap.parse_args()

    if not TOOL_ROOT.exists():
        print(f"InstanceAnimator not found at {TOOL_ROOT}", file=sys.stderr)
        print("Expected: production/tools/InstanceAnimator/ (PR #33)", file=sys.stderr)
        sys.exit(1)

    if args.mock:
        print("Launching InstanceAnimator web UI in mock mode...")
        subprocess.run([
            sys.executable, str(TOOL_ROOT / "interface" / "web_app.py"), "--mock"
        ], cwd=TOOL_ROOT)
        return

    # Real inference path (weights required)
    if not args.model or not os.path.exists(args.model):
        print("Model weights missing. Author note: 'model weight has been loss, you need to retrain model.'")
        print("Set --model to a trained checkpoint, or use --mock.")
        sys.exit(1)

    # Documented entry point
    predict = TOOL_ROOT / "inference" / "predict_video_decouple.py"
    if not predict.exists():
        print(f"Inference script missing: {predict}", file=sys.stderr)
        sys.exit(1)

    print(f"Running InstanceAnimator inference via {predict}")
    print("NOTE: Edit model path inside predict_video_decouple.py if needed.")
    # The upstream script expects internal config edits; we just invoke it.
    r = subprocess.run([sys.executable, str(predict)], cwd=TOOL_ROOT)
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
