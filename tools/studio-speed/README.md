# Studio speed stack — faster renders, no quality loss, quality up

Owner directive 2026-10-24 22:10 CDT: use GPU and whatever speeds this up
so video does not take four hours, pull in better tools than FFmpeg alone
for the motion/interpolation step, wire it in, push + merge cleanly with
no clobbering, then start using it.

## The stack (in render order)

1. **Cycles on GPU** (`gpu_render.py`) — Kaggle main, Colab T4 second,
   local CPU fallback only. Local CPU measured ~4 min/frame at 480x270
   32spp for the sit scene; that rate makes video impossible locally.
2. **Adaptive sampling + denoise** (`gpu_render.py`) — adaptive threshold
   0.01 stops clean tiles early; OptiX denoise on NVIDIA GPU, OIDN
   otherwise. Fewer wasted samples, same clean finish.
3. **Auto-framing camera** (`auto_camera.py`, copied from the workspace
   studio rig) — bbox-measured distance/target, framing self-checked
   (all 8 corners inside the frame) BEFORE GPU time is spent. No more
   render-then-discover-crop cycles.
4. **RIFE frame interpolation** (`interpolate.py`, MIT,
   hzwer/ECCV2022-RIFE, staged in the workspace opensource-pulls lane) —
   render at 12fps, interpolate to 24fps. Half the frames rendered,
   smoother motion than FFmpeg minterpolate. Honest fallback: if RIFE
   weights/GPU are unavailable, FFmpeg minterpolate runs instead and the
   output says so. Never claim RIFE ran when it did not.
5. **FFmpeg final encode** (`interpolate.py`) — H.264, yuv420p
   (phone-compatible), CRF 18, faststart. FFmpeg is the encoder here,
   not the interpolation quality step.
6. **Flamenco 3.9.3** (already installed in the workspace farm lane) —
   frame-parallel distribution when more than one worker is available.

## What was deliberately NOT pulled

- Real-ESRGAN upscaling: rendering natively on GPU at delivery
  resolution preserves more quality than rendering small and upscaling.
  Upscaling is a rescue tool, not a speed tool for this pipeline.
- Full ASWF source clones: Blender already bundles USD/OCIO/OIIO/EXR/VDB.

## Existing repo neighbours (not clobbered)

- `tools/camera-match/` and `tools/upscale-denoise/` are README-only
  stubs; this directory complements them, it does not replace them.
- `tools/render-manager/` keeps its own install script; this stack
  plugs into a render manager's frame output, it does not replace it.
