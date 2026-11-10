# Pipeline Scaling — New Tools Wiring Guide

**Date:** 2026-10-16
**Source:** PIPELINE-SCALING-2026 research (docs/research/PIPELINE-SCALING-2026.md)

## Tools Pulled In

### 1. One-to-All Animation (CVPR 2026)
- **Location:** `production/tools/one-to-all-animation/`
- **License:** Apache-2.0 ✅
- **Source:** https://github.com/ssj9596/One-to-All-Animation
- **What:** Alignment-free character animation + pose transfer. No pose skeletons needed — learns directly from visual inputs.
- **Why:** Second lane for AI body replacement alongside Viggle-Animate. Better on overlapping figures and occlusions.
- **Kaggle T4:** 1.3B model runs on free T4 (11 min for 10s 832×480 video). ComfyUI workflow available.
- **Next:** Build Kaggle notebook for T4 testing. Compare vs Viggle-Animate on Cape Jones driving footage.
- **Status:** Cloned, NOT yet tested on Kaggle.

### 2. Anime Upscaling Service (ivanmicai/anime-upscaling)
- **Location:** `production/tools/anime-upscaling/`
- **License:** MIT ✅
- **Source:** https://github.com/ivanmicai/anime-upscaling
- **What:** Self-hosted web UI + HTTP API for bulk anime video processing. Wraps video2x, Real-ESRGAN, Anime4K, RealCUGAN, RIFE, FFmpeg. GPU acceleration + Docker Compose. Pipeline editor UI.
- **Why:** Batch upscaling service for full episodes. Replaces ad-hoc upscale scripts with a proper job queue.
- **Next:** Docker Compose deploy for batch episode upscaling. Wire into `finish.py` as `--upscale-service` option.
- **Status:** Cloned, NOT yet deployed.

## Tools Documented (NOT Pulled — Honest Exclusions)

| Tool | Reason |
|------|--------|
| kash6/t4-diffusion | NO license, 0 stars. Reference only. |
| Sonic (lip sync) | License unverified, canonical repo not found. |
| InfiniteTalk | Apache-2.0 per vanta README, canonical repo not located. |
| EchoMimicV3 | Apache-2.0 per vanta README, canonical repo not located. |
| itsjwill/vanta (37K⭐ MIT) | Full app framework — reference architecture, not a pipeline tool. |
| autoqc-app/autoqc | Open-core, free tier 10 min/month. Evaluate open components. |
| HunyuanVideo | 80GB VRAM + license restrictions. Not for T4. |
| Wan2.2-Animate-14B | 6.1× slower than Viggle-Animate. Strictly worse. |

## Quality Upgrades (Research → Implementation Backlog)

1. **OCIO color management** — biggest "good → studio-grade" jump. Wire Blender's OCIO + ACES into `finish.py`. Add CDL grading support.
2. **Temporal consistency** — validate LDF-VFI on T4 (interpolation) + evaluate SeedVR2/FlashVSR (upscaling).
3. **Lip sync routing** — MuseTalk (fast default) → LatentSync (hero shots) → wire as `finish.py --lipsync`.
4. **Preview mode** — rife-ncnn-vulkan + Anime4K shaders for instant `--preview` drafts in `flipaclip_post.sh`.
5. **TheAnimeScripter 2.10.0** — evaluate TensorRT engines as RIFE replacement.

## Next Actions

- [ ] Kaggle T4 test: One-to-All Animation 1.3B on Cape Jones footage
- [ ] Kaggle T4 test: LDF-VFI vs ToonCrafter (from 2026-SPEED-RESEARCH)
- [ ] Deploy anime-upscaling service via Docker Compose
- [ ] Wire OCIO into finish.py
- [ ] Build --preview mode with rife-ncnn-vulkan
- [ ] Locate canonical repos for Sonic, InfiniteTalk, EchoMimicV3
