# Practical-RIFE — Wiring

**Source:** https://github.com/hzwer/Practical-RIFE (upstream HEAD `bbfd2ea90910`, pulled 2026-10-22)
**License:** MIT (Copyright (c) 2021 hzwer) — own-eyes verified against the upstream LICENSE file on 2026-10-22. Commercial use OK.
**What it is:** Video frame interpolation (RIFE: Real-Time Intermediate Flow Estimation) + video enhancement (SAFA: Scale-Adaptive Feature Aggregation) by the RIFE paper author.
**Pipeline use case:** 2x/4x frame-rate conversion and slow-motion for show video renders and episode output; pairs with `production/tools/realesrgan/` (upscale) and `production/tools/mocap/sambody4d/` (video-to-motion).

## Usage

```bash
cd production/tools/rife
pip install -r requirements.txt   # torch, opencv-python, moviepy, sk-video, tqdm

# Video frame interpolation (2x example)
python3 inference_video.py --multi=2 --video=input.mp4

# Image interpolation (two frames -> in-between frame)
python3 inference_img.py --img frame0.png frame1.png

# Video enhancement (SAFA space-time super-resolution)
python3 inference_video_enhance.py --video=input.mp4
```

## Weights rule

Pretrained RIFE/SAFA model weights are NOT committed here. Download GPU-side into
`train_log/` (the `--model` dir default) from the upstream release assets before running.
Same convention as `production/tools/realesrgan/` (weights/ is a pointer, models download GPU-side).

## Model versions

v4.26 = latest; v4.25 = default for most scenes; v4.22 = best for diffusion-generated
video; Lite versions for low-resource machines. Switch with `--model` / per upstream README.

## Verification on pull

- `python3 -m py_compile inference_video.py inference_img.py inference_img_SR.py inference_video_enhance.py` — clean (2026-10-22)
- Code-only pull: 3.0M total (incl. 3.0M demo images). No .pth/.ckpt/.bin, no .github, no file >10MB.
- Vendored `model/pytorch_msssim` ships with the upstream repo (loss module) — no extra license found; same MIT tree.

## Notes

- `sk-video` in requirements needs system ffmpeg; on this VM use the existing ffmpeg in PATH.
- For ncnn/Vulkan portable binaries instead of PyTorch, see nihui/rife-ncnn-vulkan (license not verified — check before pulling).
