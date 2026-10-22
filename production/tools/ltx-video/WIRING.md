# LTX-Video — Wiring

**Source:** [Lightricks/LTX-Video](https://github.com/Lightricks/LTX-Video), main @ 2026-10-22
**License:** Apache-2.0 (own-eyes verified 2026-10-22 on upstream LICENSE raw text + on-disk copy). Free + commercial-safe.
**What:** First DiT-based video generation model — text-to-video, **image-to-video**, multi-keyframe conditioning, keyframe-based animation, video extension (forward/backward), video-to-video. Up to 50fps, native 4K, real-time DiT. This is the pull that closes the "video generation open hard gap" flagged in the Grok capability study: the first true generative-video model in `production/tools/`.
**Use case (show pipeline):** Animate stills — feed a storyboard frame / proof render / keyframe into image-to-video to generate motion plates for Wizard Gang / Cape Jones cuts. Keyframe conditioning = animate BETWEEN two drawn keyframes (classic animation workflow, now generative). Video extension = lengthen an existing clip forward/backward. Pair with `../realesrgan/` (upscale the output) and `../audio/audio-separator/` + `../audio/rvc/` (dialogue chain) for full generated scenes.

## GPU-side setup (weights are NEVER committed)

```bash
cd production/tools/ltx-video
pip install -e .            # torch>=2.1.0, diffusers, transformers, huggingface-hub
pip install -e ".[inference]"  # imageio[ffmpeg], av, torchvision (video I/O)
# Weights download on first run from HuggingFace: Lightricks/LTX-Video
# (also: distilled 13B/2B variants + quantized FP8 checkpoints on HF)
```

Kaggle/Colab lane: `pip install -e .` then the model pulls itself from HF on first `from_pretrained`. Nothing weight-like lives in this repo — 632KB code-only, biggest file 81KB.

## Inference

```bash
# text-to-video
python inference.py --prompt "A cartoon hero cape billowing in the wind, city skyline" \
    --height 768 --width 1152 --num_frames 121 --seed 42

# image-to-video (animate a still)
python inference.py --prompt "subtle camera push-in, cape fluttering" \
    --conditioning_media_paths /path/to/keyframe.png \
    --height 768 --width 1152 --num_frames 121
```

See `configs/` for pipeline YAMLs and `docs/` (upstream) for the full parameter reference. The `ltx_video/` package also exposes the Diffusers-compatible pipeline (`LTXVideoPipeline`) for notebook/ComfyUI use.

## Notes

- Code-only pull (632KB); no weights, no `.github` upstream, no binaries. 35/35 `.py` pass `py_compile`.
- Upstream announced **LTX-2** ([Lightricks/LTX-2](https://github.com/Lightricks/LTX-2)) — synchronized audio+video generation, IC-LoRA control, latent upsampler. When the audio chain needs generated sound with the video, evaluate LTX-2 as the follow-up pull; this LTX-Video pull stays as the stable video-only base.
- FP8 quantized checkpoints exist upstream for lower-VRAM GPUs (needs Q8 kernels per `ltx_video/inference.py`).
