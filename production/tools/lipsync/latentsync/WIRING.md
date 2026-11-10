# LatentSync — WIRING.md

ByteDance LatentSync (audio-conditioned latent diffusion lip sync), pulled 2026-10-22
into `production/tools/lipsync/latentsync/` (cape-jones).

- **Upstream:** https://github.com/bytedance/LatentSync (depth-1 clone, 11MB code-only)
- **License:** Apache-2.0 — own-eyes verified on the upstream LICENSE file (commercial OK).
- **Weights stay OFF the repo/local disk:** UNet/SyncNet checkpoints are on Hugging Face
  (see upstream README "Inference" section). Download them Kaggle-side (see the
  weights rule in AGENTS.md) before running inference.
- **Env note:** 8GB VRAM minimum for v1.5, 18GB for v1.6 → Kaggle GPU lane only.
  Expects 25fps video + 16kHz audio.

## Why it's here (dialogue pipeline)

LatentSync takes an EXISTING rendered video + a NEW audio track and re-syncs ONLY the
mouth — it leaves the rest of the take alone. That makes it the lip-sync tool for the
show pipeline (e.g. Wizard Gang EP02 dialogue): render the scene, then apply voice
takes (Bill $aber, Onyx, Theory) to the same video without re-rendering.

## Quick start (on a GPU box with weights downloaded)

```bash
# weights: latentsync_unet.pt / whisper/tiny.pt (Hugging Face, Kaggle-side download)
python scripts/inference.py \
  --unet_config_path configs/unet/stage2.yaml \
  --inference_ckpt_path checkpoints/latentsync_unet.pt \
  --video_path <input.mp4> --audio_path <dialogue.wav> \
  --video_out_path out_synced.mp4
```

See upstream README.md for the Gradio app and training pipeline.
