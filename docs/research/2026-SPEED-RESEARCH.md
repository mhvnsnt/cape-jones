# 2026 Speed Research — Faster Video Production Without Quality Loss

**Date:** 2026-10-16
**Purpose:** Find 2026 cutting-edge tools to speed up Cape Jones video production. Quality is non-negotiable — speed only if quality holds.

---

## 1. Faster Cartoon Interpolation (Beyond ToonCrafter)

### Current: ToonCrafter (SIGGRAPH Asia 2024)
- Diffusion-based cartoon interpolation, trained on cartoons
- Our tuned config: 12 DDIM steps, 8-frame windows on T4
- **Problem:** pip install fails on Python 3.13 (tokenizers wheel build) — being fixed separately

### NEW: LDF-VFI (CVPR 2026) — STATE OF THE ART
- **Paper:** "Towards Holistic Modeling for Video Frame Interpolation with Auto-regressive Diffusion Transformers" (Peng et al., SJTU)
- **Paper:** https://arxiv.org/pdf/2601.14959v2
- **Code:** https://github.com/xypeng9903/LDF-VFI
- **License:** Apache-2.0 ✅ (verified via GitHub API)
- **Model:** https://huggingface.co/onecat-ai/LDF-VFI
- **What it does:** Auto-regressive diffusion transformer for VFI. Unlike ToonCrafter (frame-triplet based), LDF-VFI models the ENTIRE video sequence holistically — better temporal coherence, handles large/complex motion.
- **Key innovations:**
  - Skip-concatenate sampling (mitigates error accumulation in auto-regressive generation)
  - Sparse local attention + tiled VAE (efficient long sequences, 4K without retraining)
  - Conditional VAE decoder with multi-scale features from input video
- **Benchmarks:** SOTA on challenging VFI benchmarks, superior per-frame quality and temporal consistency vs both optical-flow and diffusion baselines
- **Caveat:** Paper benchmarks on H100. T4 viability untested — needs validation.
- **Verdict:** PULLED into `production/tools/ldf-vfi/` — test on Kaggle T4 as ToonCrafter alternative/upgrade
- **Project page:** https://xypeng9903.github.io/ldf-vfi-web/

### Also notable: AnimeInterp (CVPR 2021)
- **Code:** https://github.com/lisiyao21/AnimeInterp
- The foundational cartoon interpolation work. Segment-Guided Matching for textureless regions, Recurrent Flow Refinement for non-linear motion.
- Older than ToonCrafter but specifically designed for animation. Worth testing as a lightweight alternative.

---

## 2. Faster AI Body Replacement / Pose Transfer (Beyond Viggle-Animate)

### Current: Viggle-Animate (Viggle Research, 2026)
- 124 frames in 26s on one GPU, 3 forward passes (DMD-distilled)
- 6.1× faster than Wan2.2-Animate-14B on same hardware
- Already deployed to 6 repos. This is our workhorse.

### NEW: FramePrompt (2026)
- **Paper:** https://arxiv.org/pdf/2506.17301
- Surprising discovery: pretrained video diffusion transformers ALREADY have contextual capabilities for character animation — no architectural changes needed
- Structures input as: reference image + skeleton-guided motion + target video → reframes animation as future sequence prediction
- **Why it matters:** Structurally simpler, quicker to train, easier to deploy than Viggle-Animate. +5.93% SSIM, +20.65% PSNR, +34.95% LPIPS, +53.87% FVD vs baseline.
- **Verdict:** DOCUMENTED — code availability unclear, monitor for release. If code drops, test as Viggle alternative.

### Wan2.2-Animate-14B
- **Note:** Open weights ("best open-weights option" per wireflow.ai). But 6.1× SLOWER than Viggle-Animate.
- **Verdict:** NOT pulled — Viggle-Animate is strictly better for our use case.

### Bottom line for body replacement:
**Viggle-Animate remains the best 2026 option.** Nothing found beats it on speed+quality for our T4 constraints. Keep it.

---

## 3. GPU Render Optimization (Blender Cycles)

### Current: v4 pipeline (16spp + GPU OIDN)
- Already optimized: 32→16spp, GPU OIDN denoiser, ~10x speedup over baseline

### 2026 findings:
- **OpenImageDenoise GPU acceleration** is the key 2026 improvement — already in our pipeline. Denoising at interactive rates on RTX GPUs.
- **Blender 5.1.2** exists (spotted in 2026 tutorials) — we use 4.5.12 LTS. Worth testing 5.x for Cycles improvements, but LTS stability matters for production.
- **OptiX denoiser** is faster but "less suited for animations, because not temporally stable" (Blender docs). We correctly use OIDN for animation.
- **Cloud render farms:** JANCTION Render (Japan) offers Blender GPU rendering at ~0.89 JPY/frame for 1080p/128spp, with free trial credit (100 JPY no card). NOT free-tier sustainable, but documented as overflow option.

### Verdict:
Our v4 pipeline already captures the main 2026 wins (GPU OIDN + low-spp). No changes needed. Future: test Blender 5.x.

---

## 4. Faster Diffusion (2026 Techniques)

### FSVideo (ByteDance, Feb 2026)
- **Paper:** https://arxiv.org/pdf/2602.02092
- **Project:** https://kingofprank.github.io/fsvideo/
- 14B DiT + 14B upsampler, **42.3× faster than Wan2.1-I2V-14B-720P**
- Key: highly-compressed latent space (64×64×4), layer memory design, few-step upsampler
- 5s 720×1280 video in 18.8s on 2×H100
- **Verdict:** DOCUMENTED — no public code repo found (paper + project page only). If code releases, evaluate immediately. The compression technique is the future.

### FastHunyuan / FastVideo (Hao AI Lab)
- **Code:** https://github.com/hao-ai-lab/FastVideo (Apache-2.0 ✅)
- **Model:** https://huggingface.co/FastVideo/FastHunyuan
- Consistency-distilled HunyuanVideo: 6 steps instead of 50 = **8× speedup**
- Runs on single RTX 4090 with NF4 quantization (20GB VRAM)
- **License:** Code Apache-2.0; model under tencent-hunyuan-community license
- **Verdict:** DOCUMENTED — primarily text-to-video, not directly our interpolation use case. The distillation technique is worth studying for our pipelines.

### DraftAttention2 (Sep 2026)
- **Paper:** https://arxiv.org/abs/2609.32628v1
- Low-resolution-guided mixed-precision attention for fast video diffusion
- **Verdict:** DOCUMENTED — research-stage, no code yet. Watch.

### Real-time video generation (survey)
- **Article:** https://medium.com/@aminfadaeinejad.edu/real-time-video-generation-how-distillation-and-rolling-forcing-get-us-to-interactive-frame-rates-1c39f4c1774d
- Two converging lines: (1) Step Distillation, (2) Streaming Auto-Regressive generation
- **Verdict:** Useful background for future pipeline design.

---

## 5. What Was Pulled In

| Tool | License | Location | Status |
|------|---------|----------|--------|
| LDF-VFI | Apache-2.0 ✅ | `production/tools/ldf-vfi/` | Pulled, needs T4 testing |

## 6. What Was Documented (Not Pulled)

| Tool | Reason |
|------|--------|
| FSVideo | No public code (paper only) |
| FastHunyuan | Text-to-video, not our use case (technique noted) |
| FramePrompt | Code availability unclear |
| Wan2.2-Animate | 6.1× slower than Viggle-Animate |
| DraftAttention2 | Research-stage, no code |

## 7. Recommendations

1. **Test LDF-VFI on Kaggle T4** as ToonCrafter successor — if it runs on T4 and beats ToonCrafter quality, switch
2. **Keep Viggle-Animate** — still the 2026 speed king for body replacement
3. **Keep v4 render pipeline** — already captures 2026 denoiser wins
4. **Watch FSVideo** — if code releases, the 42× speedup technique could revolutionize our pipeline
5. **Fix ToonCrafter pip install** (separate lane) — still our current workhorse until LDF-VFI is validated

---

## Sources

- LDF-VFI paper: https://arxiv.org/pdf/2601.14959v2
- LDF-VFI code: https://github.com/xypeng9903/LDF-VFI
- FSVideo paper: https://arxiv.org/pdf/2602.02092
- FSVideo project: https://kingofprank.github.io/fsvideo/
- FramePrompt paper: https://arxiv.org/pdf/2506.17301
- FastVideo: https://github.com/hao-ai-lab/FastVideo
- Viggle-Animate: https://viggle.ai/research/viggle-animate-character-replacement-from-a-repainted-frame
- DraftAttention2: https://arxiv.org/abs/2609.32628v1
- Real-time video survey: https://medium.com/@aminfadaeinejad.edu/real-time-video-generation-how-distillation-and-rolling-forcing-get-us-to-interactive-frame-rates-1c39f4c1774d
