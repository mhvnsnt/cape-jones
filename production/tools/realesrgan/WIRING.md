# Real-ESRGAN — Cape Jones wiring

4x AI upscaler for the show/game pipeline (pulled 2026-10-22, overnight pipeline).

- Source: https://github.com/xinntao/Real-ESRGAN (master HEAD)
- License: **BSD-3-Clause** (verified own-eyes). Free + commercial-safe.
- Stripped from vendored pull: `.github/` CI config. Nothing else.
- Code-only: 5.5MB. `weights/` holds a README pointer — models download
  separately on the GPU lane (Kaggle-side), NOT into this repo.

## GPU-side setup

```bash
pip install basicsr facexlib gfpgan   # requirements.txt
# get weights: RealESRGAN_x4plus, RealESRGAN_x4plus_anime_6B, realesr-general-x4v3
# place .pth files in weights/
```

## Usage

```bash
# single image / frames
python inference_realesrgan.py -n RealESRGAN_x4plus_anime_6B -i inputs/ --outscale 4
# video (frame-extract -> upscale -> reassemble)
python inference_realesrgan_video.py -i clip.mp4 -n realesr-general-x4v3
```

## Use cases

- Upscale gate7 1024px fallback renders → 2048/4096 presentation quality.
- Asset / proof-render upscaling.
- `inference_realesrgan_video.py` for the show video pipeline.
