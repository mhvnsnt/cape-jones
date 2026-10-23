#!/usr/bin/env python3
"""
De-ghosting post-process for RIFE-interpolated animation frames.

Problem: RIFE was trained on real video. On flat cartoon colors (white suit,
purple cape, black bg), its optical flow can't track motion in textureless
regions, so it BLENDS instead of WARPING -> character appears semi-transparent.

Fix: For each interpolated frame M between keyframes A and B, detect pixels
where M looks like a blend of two very different A/B pixels (ghosting), and
snap them to whichever input is closer.

Usage:
    deghost.py <frames_dir> [--pattern "f*.png"] [--threshold 30] [--inplace]

    frames_dir: directory with sequential frames (key, interp, key, interp...)
    --threshold: min |A-B| difference to consider a pixel "in motion" (0-255)
    --inplace: overwrite interpolated frames (default: writes *_dg.png)

The script auto-detects which frames are interpolated: it assumes the pattern
is key, interp, key, interp... (RIFE --exp 1 output). Interpolated frames are
at odd indices.
"""

import argparse
import glob
import os
import sys

import cv2
import numpy as np


def deghost_frame(A, M, B, threshold=30):
    """
    De-ghost a single interpolated frame M given keyframes A and B.
    All inputs are float32 HxWx3 arrays in [0, 255].
    Returns de-ghosted frame as float32.
    """
    # How different are the inputs from each other?
    d_AB = np.abs(A.astype(np.float32) - B.astype(np.float32)).mean(axis=2)

    # Motion mask: pixels where A and B differ significantly
    motion = d_AB > threshold

    # Where M sits relative to A and B
    d_MA = np.abs(M.astype(np.float32) - A.astype(np.float32)).mean(axis=2)
    d_MB = np.abs(M.astype(np.float32) - B.astype(np.float32)).mean(axis=2)

    # Ghost test: M is roughly the midpoint of A and B
    # (a blend) rather than close to one of them (a warp)
    midpoint = (A.astype(np.float32) + B.astype(np.float32)) / 2.0
    d_Mmid = np.abs(M.astype(np.float32) - midpoint).mean(axis=2)

    # A pixel is ghosted if:
    #   1. It's in a motion region (A and B differ)
    #   2. M is closer to the midpoint than to either input
    #      (with some tolerance — use 0.6 * min(d_MA, d_MB) as the bar)
    nearest = np.minimum(d_MA, d_MB)
    ghosted = motion & (d_Mmid < 0.6 * nearest + 1.0) & (nearest > 5.0)

    # Snap ghosted pixels to the closer input
    use_A = d_MA <= d_MB
    out = M.astype(np.float32).copy()
    snap_mask = ghosted & use_A
    out[snap_mask] = A[snap_mask]
    snap_mask = ghosted & ~use_A
    out[snap_mask] = B[snap_mask]

    n_ghost = int(ghosted.sum())
    n_motion = int(motion.sum())
    return out, n_ghost, n_motion


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frames_dir", help="directory with sequential frames")
    ap.add_argument("--pattern", default="f*.png", help="frame filename glob")
    ap.add_argument("--threshold", type=int, default=30,
                    help="min |A-B| for motion detection (0-255)")
    ap.add_argument("--inplace", action="store_true",
                    help="overwrite interpolated frames in place")
    ap.add_argument("--suffix", default="_dg",
                    help="suffix for output files (unless --inplace)")
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.frames_dir, args.pattern)))
    if len(files) < 3:
        print(f"Need at least 3 frames, found {len(files)}", file=sys.stderr)
        sys.exit(1)

    # Load all frames
    frames = []
    for f in files:
        img = cv2.imread(f)
        if img is None:
            print(f"Could not read {f}", file=sys.stderr)
            sys.exit(1)
        frames.append(img.astype(np.float32))

    # Interpolated frames are at odd indices (RIFE --exp 1: key, interp, key...)
    total_ghost = 0
    total_motion = 0
    n_done = 0
    for i in range(1, len(frames) - 1, 2):
        A, M, B = frames[i - 1], frames[i], frames[i + 1]
        out, n_ghost, n_motion = deghost_frame(A, M, B, args.threshold)
        total_ghost += n_ghost
        total_motion += n_motion
        n_done += 1

        if args.inplace:
            out_path = files[i]
        else:
            base, ext = os.path.splitext(files[i])
            out_path = f"{base}{args.suffix}{ext}"
        cv2.imwrite(out_path, np.clip(out, 0, 255).astype(np.uint8))

        if n_done % 10 == 0 or n_done == 1:
            pct = 100.0 * n_ghost / max(n_motion, 1)
            print(f"  frame {i}: {n_ghost}/{n_motion} ghost px ({pct:.1f}%)",
                  flush=True)

    print(f"Done: {n_done} interpolated frames processed. "
          f"Total ghost pixels snapped: {total_ghost}")


if __name__ == "__main__":
    main()
