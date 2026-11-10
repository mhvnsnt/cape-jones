# Gemini Pull — AI Video Tools for Cape Jones Pipeline

**Date:** 2026-10-16
**Source:** Tool recommendations from Gemini, vetted and pulled by agent

## Summary

| Tool | Status | Location | GPU | Notes |
|------|--------|----------|-----|-------|
| Wan 2.2 | ✅ Code cloned, Kaggle-ready | `tools/wan2.2/` | T4 w/ quantization | Backgrounds, Animate-14B for character replacement |
| LTX-Video | ✅ Code cloned, Kaggle-ready | `tools/ltx-video/` | T4 ✅ | Fast previz, 2B distilled = real-time |
| ComfyUI | ✅ Code cloned, Kaggle-ready | `tools/comfyui/` | T4 ✅ | Visual workflow hub for all AI video |
| ComfyUI VFI nodes | ⚠️ Documented, install on Kaggle | — | T4 ✅ | RIFE/FILM/GMFSS/FLAVR nodes (clone stalled locally, works on Kaggle) |
| Cascadeur | ⚠️ Needs browser download | — | N/A (desktop app) | 554MB Linux, free tier, physics-based 3D animation |
| OpenToonz | ⏭️ Skipped (have Tahoma2D) | — | N/A | Tahoma2D is the better-maintained fork, covers 95%+ |
| Mochi 1 | ⏭️ Skipped (documented) | — | ❌ Needs 20GB+ | Also bad for animation (photorealistic-optimized) |

## 1. Wan 2.2 (Alibaba) ✅

**What:** Open-source video generation (Apache 2.0). Text-to-video, image-to-video, character animation.
**Repo:** https://github.com/Wan-Video/Wan2.2 (cloned to `tools/wan2.2/`, 18MB)
**Kaggle guide:** [tools/wan2.2/kaggle/KAGGLE-SETUP.md](sandbox://workspace/tools/wan2.2/kaggle/KAGGLE-SETUP.md)

**T4 Strategy:**
- **TI2V-5B** (5B dense) with FP8 quantization → fits ~12GB, runs on T4
- Use LightX2V quantized models or DiffSynth-Studio with FP8 + offload
- Q5 GGUF quants fit 8-12GB at reduced quality

**Cape Jones uses:**
1. **Trippy backgrounds** — Generate Wizard Gang-style animated backgrounds as video plates
2. **Beach environments** — "Halloween on the beach" animated backgrounds
3. **Ghost cave** — Dark atmospheric looping backgrounds
4. **Character replacement** — Wan2.2-Animate-14B does holistic movement/expression replication (rotoscope pipeline!)

**Key discovery:** Wan2.2-Animate-14B is specifically built for character animation and replacement. This is the AI body replacement tech the owner wants.

## 2. LTX-Video (Lightricks) ✅

**What:** DiT video model built for SPEED. The 2B distilled model generates 1216×704 video faster than real-time.
**Repo:** https://github.com/Lightricks/LTX-Video (cloned to `tools/ltx-video/`)
**Kaggle guide:** [tools/ltx-video/kaggle/KAGGLE-SETUP.md](sandbox://workspace/tools/ltx-video/kaggle/KAGGLE-SETUP.md)

**T4-Compatible models:**
- `ltxv-2b-0.9.6-distilled` — 2B params, ~8GB VRAM, **real-time** (5 sec video in 5 sec)
- `ltxv-2b-0.9.6` — 2B params, ~10GB VRAM, better quality
- `ltxv-13b-0.9.8-distilled-fp8` — 13B params, ~14GB VRAM, best quality on T4

**Skip:** LTX-2.x (needs 32GB+), LTX-2.5 (needs 80GB)

**Cape Jones uses:**
1. **Fast previz** — Test background vibes before committing to expensive Wan/ToonCrafter runs
2. **LED room ambience** — Quick animated color-cycling room backgrounds
3. **Rapid iteration** — Try 10 ideas in the time Wan does 1

**Speed comparison (T4):**
| Model | 5 sec 720p | Quality |
|-------|-----------|---------|
| LTX-Video 2B distilled | ~5 sec | Good (previz) |
| Wan 2.2 TI2V-5B FP8 | ~9 min | Excellent |
| ToonCrafter | 30-45 min | Best (cartoon-specific) |

**Rule:** LTX for speed/iteration → Wan for quality backgrounds → ToonCrafter for character interpolation.

## 3. ComfyUI ✅

**What:** Node-based visual workflow for AI pipelines. The de facto hub for open-source video.
**Repo:** https://github.com/comfyanonymous/ComfyUI (cloned to `tools/comfyui/`, 63MB)
**Kaggle guide:** [tools/comfyui/kaggle/KAGGLE-SETUP.md](sandbox://workspace/tools/comfyui/kaggle/KAGGLE-SETUP.md)

**Custom nodes:**
- **Frame Interpolation:** https://github.com/comfy-nodes/comfyui-frame-interpolation
  - RIFE VFI (4.0–4.9), FILM VFI, GMFSS Fortuna VFI, FLAVR VFI, IFRNet, AMT, STMFNet, MoMo
  - ⚠️ Local clone stalled on large files; install directly on Kaggle per setup guide
- **ComfyUI Manager:** https://github.com/ltdrdata/ComfyUI-Manager
- **WanVideoWrapper:** https://github.com/kijai/ComfyUI-WanVideoWrapper (optimized Wan for ComfyUI)

**Cape Jones workflows:**
1. **Interpolation comparison** — RIFE vs FILM vs GMFSS side-by-side on FlipaClip frames
2. **Background generation** — Text → Wan 2.2 → animated plate → composite in Natron
3. **Fast previz** — Text → LTX-Video → 5-sec background in 5 sec
4. **Upscaling chain** — Low-res → RealESRGAN → final

## 4. Cascadeur ⚠️ (Needs Browser Download)

**What:** Physics-based 3D character animation with AI-assisted posing. AutoPhysics suggests gravity-correct motion, AutoPosing fills limbs from control points.
**Download:** https://cascadeur.com/download (requires clicking through — no direct URL)
**Version:** 2026.2.3 (Oct 1, 2026), Linux 554MB

**Free tier:** Full animation toolset, but exports `.casc` format only (no FBX/DAE/USD).
**Paid:** Indie ($99/yr) / Pro ($399/yr) adds FBX export + commercial use.

**Cape Jones uses:**
1. **Reference animation** — Block out action sequences with believable body mechanics, then trace/rotoscope for 2D
2. **Fight scenes** — Physics-correct punches, falls, impacts as reference
3. **Flying poses** — Test cape/body physics for the flying scenes

**Action needed:** Parent agent — download from https://cascadeur.com/download (Linux version) via browser task. Install to `tools/cascadeur/`.

## 5. OpenToonz ⏭️ (Skipped — Have Tahoma2D)

**Decision:** We already have Tahoma2D, which is a fork of OpenToonz with more active development and additional features. OpenToonz doesn't ship official Linux binaries (Windows/Mac primarily). Building from source would take hours with uncertain results.

**What we'd gain from real OpenToonz:** GTS scanning tool (Windows only anyway), some different FX plugins.

**Verdict:** Tahoma2D covers 95%+ of OpenToonz functionality. Not worth the build hassle. If specific OpenToonz-only features are needed later, revisit.

## 6. Mochi 1 ⏭️ (Skipped — Too Heavy + Wrong Style)

**Why skipped:**
1. **VRAM:** Needs ~60GB single GPU, ~20GB with ComfyUI optimization. Kaggle T4 has 16GB. Doesn't fit.
2. **Style:** "Optimized for photorealistic styles so does not perform well with animated content." Wrong tool for cartoon work.
3. **Better alternatives:** Wan 2.2 and LTX-Video both outperform it for our use cases.

**Documented for completeness.** If we get access to bigger GPUs later, revisit.

## Pipeline Integration

### Updated Pipeline (2026)
```
FlipaClip drawings
    ↓
[flipaclip_post.sh] → denoise → line cleanup
    ↓
INTERPOLATION (pick one):
  ├── ToonCrafter (Kaggle GPU) → best cartoon quality, 30-45 min
  ├── RIFE (Kaggle GPU) → fast, 1.3 min, some ghosting
  └── ComfyUI VFI → compare RIFE/FILM/GMFSS side-by-side
    ↓
[finish.py] → de-ghost → QC → color grade → LED preset → audio mix
    ↓
BACKGROUNDS (pick one):
  ├── LTX-Video (Kaggle GPU) → fast previz, 5 sec
  ├── Wan 2.2 TI2V-5B (Kaggle GPU) → quality, 9 min
  └── Real photo (Gumball-style mixed media)
    ↓
Natron → composite character + background + effects
    ↓
Delivery (web/broadcast encode)
```

### New Capabilities
- **AI backgrounds:** Wan 2.2 and LTX-Video generate animated environment plates
- **Visual workflows:** ComfyUI for experimenting with interpolation models
- **Character replacement:** Wan2.2-Animate-14B for rotoscope/AI body replacement
- **Reference animation:** Cascadeur (once downloaded) for physics-correct action blocking

## Disk Usage
- wan2.2: 18MB (code only, models on Kaggle)
- ltx-video: <1MB (code only, models on Kaggle)
- comfyui: 63MB (code only, models on Kaggle)
- **Total new:** ~82MB
- **Disk:** 77% (was 76%)

All GPU models download on Kaggle, not locally. This keeps disk usage minimal.
