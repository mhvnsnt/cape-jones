#!/usr/bin/env python3
"""render_half_interp.py — Render at half framerate, RIFE-interpolate to full.

THE STRATEGY: For smooth 3D animation, rendering at 15fps and AI-interpolating
to 30fps gives ~2x FEWER Cycles frames with visually identical motion.

Why this works for 3D renders (but was risky for cartoons):
  - 3D renders have real geometry + proper motion vectors. RIFE's optical flow
    tracks solid 3D objects cleanly (no flat textureless regions like white
    cartoon suits).
  - Character animation at 15fps keyframe density is plenty for RIFE — it's
    designed for exactly this (24fps -> 60fps etc).
  - RIFE on T4 GPU: ~1.3 min for 216 pairs. 750 pairs ≈ 4-5 min.
    vs ~20 min saved per 250-frame chunk on the Cycles side.

USAGE:
  # Step 1: Render at 15fps (set in Blender or via this script's --blender-flags)
  # Step 2: Interpolate back to 30fps:
  python3 render_half_interp.py frames_15fps/ output_30fps.mp4 --fps 30

  # Or process a directory of PNGs:
  python3 render_half_interp.py frames_15fps/ frames_30fps/ --as-pngs

REQUIRES: RIFE (we have rife-v46/ and rife425/ in ~/workspace/tools/).
On Kaggle T4, use the GPU RIFE notebook (1.3 min / 216 pairs).
"""
import argparse
import glob
import os
import subprocess
import sys

TOOLS = os.path.expanduser("~/workspace/tools")


def find_rife():
    """Locate a working RIFE inference script."""
    candidates = [
        (f"{TOOLS}/rife425/rife_interp.py", "rife425"),
        (f"{TOOLS}/rife-v46/inference_video.py", "rife-v46"),
    ]
    for path, name in candidates:
        if os.path.exists(path):
            return path, name
    return None, None


def interpolate_dir(input_dir, output, fps=30, rife_script=None, rife_name=None):
    """RIFE-interpolate all PNGs in input_dir 2x, write to output."""
    frames = sorted(glob.glob(os.path.join(input_dir, "*.png")))
    if len(frames) < 2:
        print(f"ERROR: need 2+ frames in {input_dir}, found {len(frames)}")
        sys.exit(1)

    print(f"RIFE 2x: {len(frames)} frames -> {len(frames)*2-1} frames @ {fps}fps")
    print(f"  using: {rife_name} ({rife_script})")

    if rife_name == "rife425":
        # rife425/rife_interp.py interface
        tmpdir = output + ".rife_tmp"
        os.makedirs(tmpdir, exist_ok=True)
        cmd = [sys.executable, rife_script,
               "--input", input_dir,
               "--output", tmpdir,
               "--scale", "2"]
        print("  cmd:", " ".join(cmd))
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print("RIFE FAILED:")
            print(r.stdout[-2000:])
            print(r.stderr[-2000:])
            sys.exit(1)
        interp_frames = sorted(glob.glob(os.path.join(tmpdir, "*.png")))
    else:
        # rife-v46/inference_video.py — needs a video input
        # First assemble input frames to a temp video
        tmpvid = output + ".input_tmp.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-v", "error",
            "-framerate", str(fps // 2),
            "-i", os.path.join(input_dir, "%05d.png"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", tmpvid,
        ], check=True)
        tmpdir = output + ".rife_tmp"
        os.makedirs(tmpdir, exist_ok=True)
        cmd = [sys.executable, rife_script,
               "--video", tmpvid,
               "--output", tmpdir,
               "--exp", "2"]
        print("  cmd:", " ".join(cmd))
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print("RIFE FAILED:")
            print(r.stdout[-2000:])
            print(r.stderr[-2000:])
            sys.exit(1)
        interp_frames = sorted(glob.glob(os.path.join(tmpdir, "*.png")))
        os.remove(tmpvid)

    print(f"  interpolated: {len(interp_frames)} frames")

    if output.endswith(".mp4"):
        subprocess.run([
            "ffmpeg", "-y", "-v", "error",
            "-framerate", str(fps),
            "-i", os.path.join(tmpdir, "%05d.png"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-crf", "17", output,
        ], check=True)
        print(f"  wrote: {output}")
    else:
        os.makedirs(output, exist_ok=True)
        for i, f in enumerate(interp_frames):
            os.rename(f, os.path.join(output, f"f{i:05d}.png"))
        print(f"  wrote {len(interp_frames)} PNGs to {output}/")

    # Cleanup
    import shutil
    shutil.rmtree(tmpdir, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(
        description="Render at 15fps, RIFE-interpolate to 30fps (2x speed on Cycles)")
    ap.add_argument("input", help="directory of 15fps PNG frames")
    ap.add_argument("output", help="output MP4 or PNG directory (30fps)")
    ap.add_argument("--fps", type=int, default=30, help="output fps (default 30)")
    args = ap.parse_args()

    rife_script, rife_name = find_rife()
    if not rife_script:
        print("ERROR: no RIFE found in ~/workspace/tools/ "
              "(need rife425/ or rife-v46/)")
        sys.exit(1)

    interpolate_dir(args.input, args.output, fps=args.fps,
                    rife_script=rife_script, rife_name=rife_name)


if __name__ == "__main__":
    main()
