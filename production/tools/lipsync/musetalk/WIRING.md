# MuseTalk — Wiring

**Source:** [TMElyralab/MuseTalk](https://github.com/TMElyralab/MuseTalk) (Tencent Music Entertainment Group, Lyra Lab), master @ 2026-10-22
**License:** MIT (own-eyes verified 2026-10-22 on upstream LICENSE — Copyright (c) 2024 Tencent Music Entertainment Group). Commercial use OK.
Vendored deps per the license appendix: sd-vae-ft-mse (MIT), whisper (MIT), face-parsing.PyTorch (MIT), DWpose (Apache-2.0), face-alignment (BSD-3-Clause) — all commercial-friendly.
**What:** Real-time high-quality audio-driven lip-sync. Takes an EXISTING video of a person talking + a new audio track, repaints the mouth/lower face (256x256 latent inpaint) so lips match. Rest of footage untouched (head, eyes, background preserved). Single-step latent inpainting (not multi-step diffusion) — 30fps+ on a V100; on a 4GB laptop GPU (RTX 3050 Ti, fp16) ~5 min per 8s clip per upstream README. 1.5 (spatio-temporal sampling, perceptual+GAN+sync loss) is the recommended version.
**Use case (show pipeline):** The lightweight lip-sync path — re-sync the mouth of an existing take to a voice track WITHOUT re-rendering. Cheaper VRAM than `../latentsync/` (8GB min for LatentSync 1.5 / 18GB for 1.6) at the cost of 256px face-region sharpness — for close-ups consider a follow-up Real-ESRGAN/GFPGAN pass (`../realesrgan/`).

## GPU-side setup (weights are NEVER committed)

```bash
cd production/tools/lipsync/musetalk
sh download_weights.sh        # pulls ~2GB+ from HuggingFace (TMElyralab/MuseTalk, stabilityai/sd-vae-ft-mse, openai whisper, DWpose, face-parse-bisent, syncnet) into ./models/
pip install -r requirements.txt   # CUDA + cuDNN host assumed
```

## Inference (batch)

```bash
sh inference.sh v1.5 normal     # uses configs/inference/*.yaml — video_path/audio_path/result_dir
# or directly:
python scripts/inference.py --inference_config configs/inference/test.yaml \
    --result_dir <out> --unet_model_path models/musetalkV15/unet.pth \
    --version v15 --use_float16
```

## Realtime

```bash
sh inference.sh v1.5 realtime    # streams — live avatars / streaming
# or: python scripts/realtime_inference.py --inference_config configs/inference/realtime.yaml ...
```

25fps source video + 16kHz audio recommended to match training.

## Notes
- Code-only pull (19MB); no weights, no `.github` upstream.
- Gradio demo: `python app.py`.
