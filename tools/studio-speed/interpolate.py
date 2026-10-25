"""Frame interpolation + final encode for studio video.

Why this exists (owner directive 2026-10-24 22:10 CDT): FFmpeg alone is
fine for encoding, but its minterpolate is not the best motion
interpolation available. RIFE (Real-Time Intermediate Flow Estimation,
MIT, hzwer/ECCV2022-RIFE) produces cleaner intermediate frames from
optical flow. Pipeline: render at HALF the delivery fps on GPU, let RIFE
double the frames, encode with FFmpeg. Half the render time, smoother
motion, no resolution loss.

Usage:
  python3 interpolate.py --frames /tmp/frames --fps-in 12 --fps-out 24 \
    --rife ~/workspace/ep1-farm/opensource-pulls/rife --out /tmp/sit_orbit.mp4

Behaviour (honest fallback chain):
  1. If RIFE + model weights are present and a CUDA GPU is available,
     run RIFE inference_video.py (exp=2 for 2x).
  2. Otherwise fall back to FFmpeg minterpolate (mi_mode=mci) — the
     tool the owner already knows works — and say so in the output.
     Never claim RIFE ran when it did not.
  3. Final encode is always FFmpeg: H.264, yuv420p (phone-compatible),
     faststart (streamable before fully downloaded), CRF 18 (high
     quality, not the default 23).
"""
import argparse, os, subprocess, sys, glob

ap = argparse.ArgumentParser()
ap.add_argument("--frames", required=True)
ap.add_argument("--fps-in", type=int, default=12)
ap.add_argument("--fps-out", type=int, default=24)
ap.add_argument("--rife", default="")
ap.add_argument("--out", required=True)
a = ap.parse_args()

frames = sorted(glob.glob(os.path.join(a.frames, "*.png")))
if len(frames) < 2:
    raise SystemExit(f"interpolate: fewer than 2 frames in {a.frames}")
print(f"interpolate: {len(frames)} source frames, {a.fps_in} -> {a.fps_out} fps")

def run(cmd):
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)

interp_dir = os.path.join(a.frames, "interp")
os.makedirs(interp_dir, exist_ok=True)
used = "ffmpeg-minterpolate"
# RIFE path: weights live in <rife>/train_log by default in the repo's
# inference_video.py; only attempt when that directory has a .pkl.
rife_ok = False
if a.rife:
    import torch  # noqa: F401  (only needed for the RIFE path)
    train_log = os.path.join(a.rife, "train_log")
    weights = glob.glob(os.path.join(train_log, "*.pkl")) if os.path.isdir(train_log) else []
    if weights and subprocess.run(["nvidia-smi"], capture_output=True).returncode == 0:
        rife_ok = True
if rife_ok:
    run([sys.executable, os.path.join(a.rife, "inference_video.py"),
         "--video", a.frames, "--exp", str(a.fps_out // a.fps_in),
         "--fps", str(a.fps_out), "--out", interp_dir])
    used = "RIFE"
    src = interp_dir
else:
    print("interpolate: RIFE unavailable (no weights/GPU) — falling back to FFmpeg minterpolate, stated honestly")
    run(["ffmpeg", "-y", "-framerate", str(a.fps_in), "-i", os.path.join(a.frames, "frame_%04d.png"),
         "-vf", f"minterpolate=fps={a.fps_out}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart",
         os.path.join(interp_dir, "interp.mp4")])
    src = interp_dir
    # minterpolate path already encoded; just copy to final out
    run(["cp", os.path.join(interp_dir, "interp.mp4"), a.out])
    print(f"interpolate: done via {used} -> {a.out}")
    sys.exit(0)
# RIFE path: frames in interp_dir -> final encode
run(["ffmpeg", "-y", "-framerate", str(a.fps_out), "-i", os.path.join(src, "frame_%04d.png"),
     "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", a.out])
print(f"interpolate: done via {used} -> {a.out}")
