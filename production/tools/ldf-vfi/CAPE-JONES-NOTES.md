# LDF-VFI — Pulled for Cape Jones

**Source:** https://github.com/xypeng9903/LDF-VFI
**Paper:** "Towards Holistic Modeling for Video Frame Interpolation with Auto-regressive Diffusion Transformers" (CVPR 2026, Peng et al., SJTU)
**License:** Apache-2.0 (verified)
**Pulled:** 2026-10-16

## What it is

State-of-the-art video frame interpolation using an auto-regressive diffusion transformer. Unlike ToonCrafter (which processes frame triplets independently), LDF-VFI models the entire video sequence holistically for better temporal coherence.

Key innovations:
- Skip-concatenate sampling (prevents error accumulation in auto-regressive generation)
- Sparse local attention + tiled VAE (efficient long sequences, 4K without retraining)
- Conditional VAE decoder with multi-scale features from input video

## Why we pulled it

ToonCrafter is our current cartoon interpolation workhorse. LDF-VFI is the 2026 SOTA successor — better temporal consistency, handles large/complex motion better. Potential upgrade path.

## Status

**UNTESTED on our hardware.** Paper benchmarks on H100. Needs validation on Kaggle T4 before replacing ToonCrafter.

## Model weights

Download from https://huggingface.co/onecat-ai/LDF-VFI (not included in repo — too large).

## Next steps

1. Build Kaggle notebook for T4 testing
2. Compare quality vs ToonCrafter on Cape Jones expressions footage
3. If better and T4-viable, integrate into pipeline
