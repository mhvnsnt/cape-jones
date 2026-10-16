#!/usr/bin/env python3
"""
Scene-aware frame interpolation for hand-drawn animation.

Problem: RIFE interpolates THROUGH scene cuts and black frames, creating
fades/ghosting between completely different shots.

Solution:
1. Detect scene cuts (large frame-to-frame differences, black frames)
2. Split into scenes
3. Run RIFE + de-ghosting WITHIN each scene only
4. Reassemble with hard cuts preserved

Usage:
    scene_aware_interp.py <input_frames_dir> <output_frames_dir>
        [--threshold 30.0]  # mean abs diff threshold for cut detection
        [--min_scene 3]      # minimum frames per scene
        [--black_thresh 10]  # mean brightness below this = black frame

    Input: sequential PNG frames (f%04d.png)
    Output: interpolated frames with scene cuts preserved
"""

import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile

import cv2
import numpy as np

RIFE_VENV = os.path.expanduser("~/workspace/tools/rife-venv/bin/python")
RIFE_SCRIPT = os.path.expanduser("~/workspace/tools/rife425/rife_interp.py")
DEGHOST_SCRIPT = os.path.expanduser("~/workspace/tools/post-pipeline/deghost.py")


def detect_scenes(frames_dir, pattern="f*.png", threshold=30.0,
                  black_thresh=10.0, min_scene=3):
    """Return list of (start_idx, end_idx) scene boundaries.
    
    Black frames are treated as separators and EXCLUDED from scenes —
    interpolation runs directly between content frames on either side.
    Returns (files, scenes, black_indices).
    """
    files = sorted(glob.glob(os.path.join(frames_dir, pattern)))
    if not files:
        raise ValueError(f"No frames found in {frames_dir}")

    # Load grayscale thumbnails for fast comparison
    thumbs = []
    is_black = []
    for f in files:
        img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Could not read {f}")
        small = cv2.resize(img, (160, 90))
        thumbs.append(small.astype(np.float32))
        is_black.append(small.mean() < black_thresh)

    black_indices = {i for i, b in enumerate(is_black) if b}

    # Find content runs (non-black sequences)
    # Only split on VERY large visual jumps (true scene changes, not animation motion)
    scenes = []
    run_start = None
    for i in range(len(files)):
        if not is_black[i]:
            if run_start is None:
                run_start = i
            elif i > run_start:
                # Check for hard cut from previous content frame
                # (skip over any black frames between them)
                prev_content = i - 1
                while prev_content > run_start and is_black[prev_content]:
                    prev_content -= 1
                if prev_content >= run_start:
                    diff = np.abs(thumbs[i] - thumbs[prev_content]).mean()
                    if diff > threshold * 4:  # very large = true scene change
                        scenes.append((run_start, i))
                        run_start = i
        # black frames: just skip, don't break the run
    # Trailing run
    if run_start is not None:
        # Collect all non-black frames from run_start to end
        content_indices = [j for j in range(run_start, len(files))
                           if not is_black[j]]
        if content_indices:
            scenes.append((content_indices[0], content_indices[-1] + 1))

    # Filter scenes to only include non-black frame ranges
    # (we'll extract just the content frames when interpolating)
    final_scenes = []
    for s, e in scenes:
        content = [j for j in range(s, e) if not is_black[j]]
        if len(content) >= 1:
            final_scenes.append((content[0], content[-1] + 1, content))

    return files, final_scenes, black_indices


def interpolate_scene_to(files, start, end, out_dir, tmp_base, out_start,
                         content_indices=None):
    """Run RIFE + de-ghost on a single scene's frames.
    Writes output starting at out_start index. Returns number of frames written.
    If content_indices provided, only those frames are used (black skipped).
    """
    if content_indices is not None:
        indices = content_indices
    else:
        indices = list(range(start, end))
    n = len(indices)
    if n < 2:
        # Single frame scene: copy as-is (doubled for 2x timing)
        for dup in range(2):
            shutil.copy(files[start],
                        os.path.join(out_dir, f"f{out_start + dup:04d}.png"))
        return 2

    # Stage frames for RIFE
    scene_in = os.path.join(tmp_base, f"scene_{start}_in")
    scene_out = os.path.join(tmp_base, f"scene_{start}_out")
    os.makedirs(scene_in, exist_ok=True)
    os.makedirs(scene_out, exist_ok=True)

    for j, idx in enumerate(indices):
        shutil.copy(files[idx], os.path.join(scene_in, f"f{j:04d}.png"))

    # RIFE interpolate (exp 1 = 2x)
    r = subprocess.run(
        [RIFE_VENV, RIFE_SCRIPT, scene_in, scene_out, "--exp", "1"],
        capture_output=True, text=True)
    if r.returncode != 0:
        print(f"RIFE failed on scene {start}-{end}: {r.stderr[:200]}",
              file=sys.stderr)
        # Fallback: copy originals at 2x spacing
        for j, idx in enumerate(range(start, end)):
            shutil.copy(files[idx],
                        os.path.join(out_dir, f"f{(start + j) * 2:04d}.png"))
        return n

    # De-ghost the RIFE output
    r = subprocess.run(
        [RIFE_VENV, DEGHOST_SCRIPT, scene_out,
         "--pattern", "f*.png", "--inplace", "--threshold", "30"],
        capture_output=True, text=True)
    if r.returncode != 0:
        print(f"De-ghost failed on scene {start}-{end}, using raw RIFE",
              file=sys.stderr)

    # Copy to output with sequential indices
    # RIFE exp 1: N input frames -> 2N-1 output frames
    out_files = sorted(glob.glob(os.path.join(scene_out, "f*.png")))
    for j, of in enumerate(out_files):
        shutil.copy(of, os.path.join(out_dir, f"f{out_start + j:04d}.png"))

    return len(out_files)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_dir", help="input frames directory")
    ap.add_argument("output_dir", help="output frames directory")
    ap.add_argument("--threshold", type=float, default=30.0)
    ap.add_argument("--min_scene", type=int, default=3)
    ap.add_argument("--black_thresh", type=float, default=10.0)
    args = ap.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    tmp_base = tempfile.mkdtemp(prefix="scene_interp_")

    try:
        files, scenes, black_indices = detect_scenes(
            args.input_dir, threshold=args.threshold,
            black_thresh=args.black_thresh, min_scene=args.min_scene)

        print(f"Detected {len(scenes)} content scenes "
              f"({len(black_indices)} black separator frames skipped):")
        total_out = 0
        out_idx = 0
        for s, e, content in scenes:
            print(f"  frames {s}-{e-1} ({len(content)} content frames)",
                  flush=True)
            n_out = interpolate_scene_to(
                files, s, e, args.output_dir, tmp_base, out_idx,
                content_indices=content)
            out_idx += n_out
            total_out += n_out

        print(f"Done: {total_out} output frames in {args.output_dir}")
    finally:
        shutil.rmtree(tmp_base, ignore_errors=True)


if __name__ == "__main__":
    main()
