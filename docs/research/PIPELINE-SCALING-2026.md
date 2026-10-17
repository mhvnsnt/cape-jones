# Pipeline Scaling 2026 — Vertical + Horizontal Research

**Date:** 2026-10-16
**Purpose:** Find what we're missing vertically (deeper in current stack) and horizontally (adjacent tools) to make the Cape Jones pipeline faster and higher-quality. Quality first, speed second.

---

## VERTICAL SCALING — Deeper in Our Current Stack

### Stage 1: Interpolation (12fps → 24fps cartoon inbetweening)

**What we use:** ToonCrafter (SIGGRAPH Asia 2024) → LDF-VFI (CVPR 2026, pulled, needs T4 validation)

**2026 SOTA findings:**
- **LDF-VFI** (Peng et al., SJTU, CVPR 2026) — auto-regressive diffusion transformer, holistic sequence modeling. SOTA on VFI benchmarks. Apache-2.0 ✅. Already in `production/tools/ldf-vfi/`. **Action: validate on Kaggle T4.**
- **TheAnimeScripter 2.10.0** (active, updated Oct 2026) — NOT just RIFE. Now ships TensorRT engines, NVDEC decoding, CUDA graphs, `--smooth_dedup` (detects held frames on twos/threes), `--scenechange` (holds at hard cuts), anime depth (Limbo), anime segmentation. One-pass in-memory pipeline. **This is a production-grade anime interpolation tool we should evaluate as a RIFE replacement.**
- **Video2X 6.0.0** — complete C++ rewrite. "Blazing fast," Anime4K v4 + Real-ESRGAN + Real-CUGAN + RIFE via ncnn/Vulkan. Zero intermediate disk. **Candidate for local CPU preprocessing.**
- **rife-ncnn-vulkan** — real-time RIFE on GPU via Vulkan, no Python needed. Drop-in for interpolation pipelines.

**Gap:** We have no TensorRT-accelerated interpolation path. TheAnimeScripter's TensorRT engines could 2-3x our RIFE speed.

### Stage 2: AI Body Replacement (driving video → character performance)

**What we use:** Viggle-Animate (2026) — 124 frames in 26s, 6.1× faster than Wan2.2-Animate-14B.

**2026 SOTA findings:**
- **Viggle-Animate remains the speed king.** Nothing found beats it for our T4 constraints. Keep it.
- **One-to-All Animation** (CVPR 2026, Apache-2.0 ✅) — alignment-free character animation + pose transfer. **Runs on Kaggle T4 FREE** (1.3B model, 11 min for 10s 832×480). Has ComfyUI workflow. **Pulled into `production/tools/one-to-all-animation/`** — test as Viggle alternative for complex multi-character shots.
- **SCAIL-2** — already in repo. Direct visual conditioning (no pose skeletons), better on overlapping figures.
- **FramePrompt** (2026) — reframes animation as future sequence prediction using pretrained video DiT. +5.93% SSIM, +20.65% PSNR vs baseline. Code availability unclear — monitor.
- **Wan2.2-Animate-14B** — open weights but 6.1× slower than Viggle. Not pulled (strictly worse for us).

**Gap:** No fallback when Viggle fails. One-to-All gives us a second lane.

### Stage 3: Lip Sync

**What we use:** LatentSync (Apache-2.0) + MuseTalk (MIT) — documented, not yet wired into `finish.py`.

**2026 landscape (from pixazo.ai 2026 ranking + sync.so):**
| Model | Strength | License | Have it? |
|-------|----------|---------|----------|
| LatentSync | Visual fidelity (hero shots) | Apache-2.0 | ✅ documented |
| MuseTalk | Speed + balance (default) | MIT | ✅ documented |
| **Sonic** | **Emotional dubbing** (carries performance from audio) | ? | ❌ NEW — research license |
| **InfiniteTalk** | **Unlimited-length** talking video from single image | Apache-2.0 (per vanta) | ❌ NEW — find canonical repo |
| **EchoMimicV3** | Full-body/half-body on 12GB VRAM | Apache-2.0 (per vanta) | ❌ NEW — find canonical repo |
| Hallo3 | Long-form talking head | research-only path | ❌ documented, not pulled |
| **Kandinsky 6.0** | **Text-to-video + lip-synced dialogue in ONE pass** | MIT | ✅ already pulled (Expansion-5) |

**Key insight:** No single model wins. 2026 best practice = route each shot to the best model for that shot. Our pipeline should support: MuseTalk (fast default) → LatentSync (hero shots) → Sonic (emotional dialogue) → InfiniteTalk (long takes).

**Gap:** LatentSync/MuseTalk not yet wired as `finish.py --lipsync`. Sonic/InfiniteTalk/EchoMimicV3 need license verification + canonical repo discovery.

### Stage 4: Color Grading / Color Science

**What we use:** 32 static grades in `grades.py` (ffmpeg-based) + 15 LED presets. Ad-hoc, no color management.

**2026 findings:**
- **OpenColorIO (OCIO)** — BSD-3-Clause, Academy Software Foundation. The industry standard used by DaVinci Resolve, Nuke, Maya, Blender, Houdini. Blender 4.5+ supports OCIO natively including ACES.
- **Our gap:** `finish.py` does ad-hoc ffmpeg color. Studio-grade = OCIO-managed pipeline with ACEScg working space, display transforms, look transforms.
- **Blender Conference 2026** (Mark Boorer talk): full Hollywood VFX color pipeline guide using Blender + OCIO — plate linearisation, neutral grading, CDL grading, display transforms.

**Action:** Wire OCIO config into the pipeline. Start with Blender's built-in OCIO + ACES, add CDL grading support to `finish.py`. This is the single biggest "good → studio-grade" upgrade for color.

### Stage 5: Upscaling

**What we use:** RealESRGAN (anime models) + SPAN (weights pending).

**2026 SOTA:**
- **SeedVR2** — 2026 SOTA for video enhancement with temporal consistency. Multiple sources cite it as the new standard.
- **FlashVSR** — real-time diffusion VSR, one-step streaming ~17 FPS on A100.
- **STCDiT** (CVPR 2026) — spatio-temporally consistent diffusion Transformer for VSR.
- **VOSR 2.0** (CVPR 2026) — blur→clear, best for poster text restoration.
- **RealESRGAN** — still the practical standard for anime. Not dethroned, just joined.
- **ivanmicai/anime-upscaling** (MIT ✅) — self-hosted web UI + HTTP API for bulk anime upscaling (video2x, Real-ESRGAN, Anime4K, RealCUGAN, RIFE, FFmpeg, GPU + Docker). **Pulled into `production/tools/anime-upscaling/`** — gives us a batch upscaling service.

**Gap:** No temporal-consistency-aware upscaling. SeedVR2/FlashVSR would reduce flicker on upscaled animation.

### Stage 6: Denoising

**What we use:** GPU OIDN (v4 pipeline).

**2026 findings:** OIDN remains the standard. No new denoiser dethrones it for animation in 2026. Our v4 pipeline (16spp + GPU OIDN) already captures the main win.

### Stage 7: GPU Optimization (T4-specific)

**What we use:** FP16, tuned DDIM steps, pruned models.

**2026 findings:**
- **TensorRT** = 2-5x speedup on diffusion models (NVIDIA's own numbers: up to 5x vs PyTorch). FP16 via TensorRT is the safe default; INT8 needs calibration.
- **kash6/t4-diffusion** — T4-first TensorRT pipeline for Stable Diffusion. **NOT pulled: NO license, 0 stars.** Documented as reference only.
- **Key insight for Kaggle:** TensorRT engine builds need host RAM. Kaggle T4 has 16GB VRAM but limited host RAM — engine builds may OOM. FP16 PyTorch is the safe default; TensorRT is for when we have headroom.

**Gap:** No TensorRT path for our diffusion workloads. Worth testing on Kaggle when we have a stable pipeline.

### Stage 8: Audio / Dialogue / Music

**What we use:** Extensive TTS stack (Piper, KittenTTS, StyleTTS 2, CosyVoice 2, LuxTTS, etc.), Demucs/UVR5, ACE-Step/Stable Audio.

**2026 findings:** Our audio stack is comprehensive. No major gaps found in this research pass. The **Kandinsky 6.0** one-pass video+audio+lipsync is the most interesting new capability for dialogue shots.

---

## HORIZONTAL SCALING — Branching Outward

### H1: Automated QC

**FIND: autoqc-app/autoqc** — Automated video QC platform. 15 AI-powered checks:
- 8 video checks (parallel frame analysis)
- 5 audio checks (loudness EBU R128, clipping, noise, silence, clarity — shared Silero VAD timeline)
- Platform compliance: YouTube, TikTok, Instagram, Broadcast TV (one-click)
- PDF reports, timeline errors

**License:** Has free tier (10 min/month). Open-core model — verify what's open vs paid before pulling.
**Verdict:** DOCUMENTED. Our `finish.py` has basic QC; autoqc would give us broadcast-grade automated QC. Evaluate the open-source components.

### H2: Batch Upscaling Service

**FIND: ivanmicai/anime-upscaling** (MIT ✅) — Self-hosted web UI + HTTP API for bulk anime video upscaling. Wraps video2x, Real-ESRGAN, Anime4K, RealCUGAN, RIFE, FFmpeg with GPU acceleration + Docker Compose. Pipeline editor UI.

**Verdict:** PULLED into `production/tools/anime-upscaling/`. Gives us a batch upscaling service for the whole episode.

### H3: Full AI Video Engine (Reference Architecture)

**FIND: itsjwill/vanta** (MIT, 37K stars) — Open-source AI video engine built on Remotion. Voice cloning, AI avatars (MuseTalk, LatentSync, InfiniteTalk), animated captions, text-to-video (Wan 2.2/LTX), AI music, video editor, timeline, 100+ transitions. "Free Synthesia/HeyGen/Runway/CapCut/Descript/ElevenLabs alternative."

**Verdict:** NOT pulled (it's a full app framework, not a pipeline tool). DOCUMENTED as reference architecture — its integration patterns for MuseTalk/LatentSync/InfiniteTalk are worth studying when we wire lip sync.

### H4: Pipeline Orchestration (Beyond kaggle_queue)

**Current:** `kaggle_queue.py` — custom-built, works, has validation + saver injection + claim gates (PR #47).

**2026 landscape:**
- **Flamenco** — Blender's own render farm (already documented). Go binaries, no DB, web dashboard. Best for Blender render distribution.
- **OpenCue** — Sony Imageworks + Google. Scales to 150K cores. Overkill for us now, but the design patterns (job → tasks → workers) are what we want.
- **MoneyPrinterTurbo** (MIT) — full AI video pipeline: script → footage → TTS → subtitles → render. Interesting for automated assembly, but not our workflow.

**Verdict:** Our `kaggle_queue.py` is the right tool for Kaggle GPU orchestration. No replacement needed. Flamenco remains the answer for Blender render distribution (already documented).

### H5: Faster Previews / Real-Time Feedback

**Gap:** No fast preview path. Every iteration requires a full pipeline run.

**2026 options:**
- **rife-ncnn-vulkan** — real-time RIFE interpolation, no Python. Could give us instant interpolation previews.
- **Anime4K** (libplacebo shaders) — real-time anime upscaling. Instant upscale previews.
- **OpenReel Video** (MIT, already pulled per CLOUD-RESEARCH) — "open-source CapCut", 4K/WebGPU. Browser-based editing with real-time preview.

**Action:** Wire rife-ncnn-vulkan + Anime4K into a `--preview` mode for `flipaclip_post.sh` — fast draft, slow final.

### H6: Character Consistency (for AI-generated shots)

**2026 methodology:** Reference-image conditioning is the standard. Character bible → locked reference → reuse across shots.

**Relevant tools:**
- **HunyuanVideo** — "consistency king" but needs 80GB VRAM + has license restrictions. Not for us.
- **Wan2.1** (Apache-2.0) — quality benchmark, 1.3B fits in 16GB. Worth testing for background/scene generation.
- **One-to-All Animation** — our pick for pose transfer consistency (already pulled).

**Our advantage:** Cape Jones is built from real vector parts, not AI generation. Character consistency is solved by construction — we don't need AI to keep him consistent. This only matters for AI-generated backgrounds/scenes.

### H7: Background Generation

**2026 landscape:** Mostly commercial (Maxsa AI, Neolemon). Open-source path = Stable Diffusion + AnimateDiff, Wan2.1.

**Verdict:** We have the tools (SD ecosystem in ai-video/). No new pull needed. Document the background-generation workflow using existing tools.

---

## QUALITY: Good → Studio-Grade

### The three biggest upgrades:

1. **OCIO color management** (Stage 4) — single biggest quality jump. Ad-hoc ffmpeg grades → ACEScg working space + display transforms + CDL grading. This is what separates "YouTube" from "studio."

2. **Temporal consistency** (Stages 1+5) — LDF-VFI for interpolation + SeedVR2/FlashVSR for upscaling. Reduces the flicker/ghosting that marks AI-processed video.

3. **Automated QC** (H1) — autoqc's 15 checks or our own expanded `finish.py` QC. Catches what eyes miss at 2 AM.

### Quality checklist for every deliverable:
- [ ] OCIO-managed color (when wired)
- [ ] Temporal consistency verified (no flicker on flat colors)
- [ ] Platform compliance checked (YouTube/TikTok/Instagram specs)
- [ ] Audio loudness compliant (EBU R128)
- [ ] Claim gate passed (evidence attached)

---

## WHAT WAS PULLED IN

| Tool | License | Location | Status |
|------|---------|----------|--------|
| One-to-All Animation | Apache-2.0 ✅ | `production/tools/one-to-all-animation/` | Cloned (90M), needs Kaggle T4 test |
| ivanmicai/anime-upscaling | MIT ✅ | `production/tools/anime-upscaling/` | Cloned (3.6M), needs Docker deploy |

## HONEST EXCLUSIONS (documented, NOT pulled)

| Tool | Reason |
|------|--------|
| kash6/t4-diffusion | NO license, 0 stars. Reference only. |
| Sonic (lip sync) | License unverified, canonical repo not found. Monitor. |
| InfiniteTalk | Apache-2.0 per vanta README, but canonical repo not located. Monitor. |
| EchoMimicV3 | Apache-2.0 per vanta README, but canonical repo not located. Monitor. |
| itsjwill/vanta | Full app framework (37K stars, MIT) — reference architecture, not a pipeline tool. |
| autoqc-app/autoqc | Open-core model, free tier only 10 min/month. Evaluate open components. |
| HunyuanVideo | 80GB VRAM requirement + license restrictions. Not for T4. |
| Wan2.2-Animate-14B | 6.1× slower than Viggle-Animate. Strictly worse for us. |

---

## NEXT ACTIONS

1. **Validate LDF-VFI on Kaggle T4** — is it actually faster/better than ToonCrafter for our cartoon?
2. **Test One-to-All Animation on Kaggle T4** — validate the 1.3B model as Viggle alternative
3. **Wire OCIO into finish.py** — start with Blender's built-in config + ACES
4. **Evaluate TheAnimeScripter 2.10.0** — TensorRT engines could replace our RIFE path
5. **Build --preview mode** — rife-ncnn-vulkan + Anime4K for instant drafts
6. **Wire lip sync routing** — MuseTalk (default) → LatentSync (hero) → Sonic (emotional, when licensed)
7. **Locate canonical repos** for InfiniteTalk, EchoMimicV3, Sonic — verify licenses, pull if clean
