# Studio-Grade Pull — 2026 Animation Tools & Research

Date: 2026-10-16
Purpose: Pull in production-grade tools, studio open-source releases, and
cutting-edge research for the Cape Jones animation pipeline.

## Key Finding: We're Ahead of Toon Boom

Toon Boom Harmony — the industry standard for 2D animation — has **"no
AI-assisted in-betweening or motion generation (as of 2026)"** (per third-party
workflow analysis). Our ToonCrafter pipeline puts us ahead of the commercial
industry standard for AI interpolation.

## Pulled Tools

### AI Interpolation / Inbetweening

| Tool | Paper | Status | Notes |
|------|-------|--------|-------|
| **ToonCrafter** | SIGGRAPH Asia 2024 | ✅ In pipeline | Cartoon-trained diffusion interpolation. Tuned v2: 12 steps, 8 frames/pair, ~4x faster |
| **ToonCrafter FP16** | Community (Kijai) | 📝 Documented | `tooncrafter_512_interp-fp16.safetensors` — half VRAM (12GB vs 24GB), faster inference. URL: `huggingface.co/Kijai/DynamiCrafter_pruned` |
| **ToonCrafter Sketch Guidance** | Community (mattyamonaca) | ⬇️ Cloning | `~/workspace/tools/tooncrafter-sketch/` — sketch-guided interpolation |
| **Framer** | arXiv 2410.18978 | ⬇️ Cloning | `~/workspace/tools/framer/` — Interactive frame interpolation with demo |
| **AnimeInterp** | CVPR 2021 | ✅ Have it | `~/workspace/tools/animeinterp/` — segment-guided matching for animation |
| **AnimeInbet** | ICCV 2023 | ✅ Have it | `~/workspace/tools/animeinbet/` — vector-graph line inbetweening, no ghosting by design |
| **RIFE** | — | ✅ In pipeline | Fast flow-based fallback (1.3 min on T4 vs 30-45 min ToonCrafter) |

### Character Animation / Pose Transfer

| Tool | Paper | Status | Notes |
|------|-------|--------|-------|
| **One-to-All Animation** | CVPR 2026 | ✅ Cloned | `~/workspace/tools/one-to-all-animation/` — alignment-free character animation + pose transfer. **Runs on Kaggle T4 free.** Directly relevant to the rotoscope/AI body replacement work. |

### Studio Open-Source Releases

| Studio | Tool | Relevance |
|--------|------|-----------|
| **DreamWorks** | OpenMoonRay 2.40 | Production path-tracer, ASWF hosted. 3D-focused, not directly useful for 2D but industry-grade. |
| **DreamWorks** | OpenVDB / NanoVDB | Volumetric data. Useful if we do 3D/VFX elements. |
| **Sony Pictures Imageworks** | OpenColorIO | Color management — **directly useful** for consistent color grading across pipeline. |
| **Disney** | Ptex, SeExpr | Texture/painting. SeExpr could be useful for procedural animation effects. |
| **Netflix** | Blender funding | Netflix Animation is now a Blender Corporate Patron (€240k/yr). Validates Blender Grease Pencil as production-grade 2D. |
| **Studio Ghibli / Dwango** | OpenToonz + GTS | OpenToonz is the open-source version of Toonz (used by Ghibli). GTS scanning tool included. **We should evaluate OpenToonz for the pipeline.** |

### 2D Animation Software (Open Source)

| Tool | Status | Notes |
|------|--------|-------|
| **OpenToonz** | 📝 Evaluate | Ghibli's tool, open-sourced by Dwango. Xsheet workflow, vectorization, FX compositing. The "pro" 2D option. |
| **OpenToonz Morevna Edition** | 📝 Evaluate | Community fork with SVG support, UI improvements. |
| **Tahoma2D** | ✅ Have it | We have it but it segfaults headless. GUI use only. |
| **Krita** | ✅ Have it | Already in pipeline for drawing/painting. |
| **Blender Grease Pencil** | ✅ Have it | Netflix-backed, production-proven for 2D. We have Blender + addons. |

## Papers With Code (2024-2026)

From Awesome-AI4Animation (ICCVW 2025) and Papers With Code:

### Inbetweening / Interpolation
- **ToonCrafter** (TOG 2024) — our primary ✅
- **Framer: Interactive Frame Interpolation** (arXiv 2410.18978) — interactive control, has demo ⬇️
- **AnimeInbet / Deep Geometrized Cartoon Line Inbetweening** (ICCV 2023) — vector-based ✅
- **AnimeInterp** (CVPR 2021) — segment-guided ✅

### Character Animation
- **One-to-All Animation** (CVPR 2026) — pose transfer, Kaggle-ready ✅
- **KeyFace** (CVPR 2025) — audio-driven facial animation. Relevant for lip-sync.

### Colorization
- **BasicPBC** (CVPR 2024) — AI paint-bucket ✅ (already have it)

## Pipeline Integration Status

### Wired In (Production Ready)
1. FlipaClip → frame extraction
2. RIFE (Kaggle T4, 1.3 min) → fast interpolation fallback
3. ToonCrafter (Kaggle T4, 30-45 min tuned) → quality interpolation
4. De-ghosting → cleanup
5. Upscaling (RealESRGAN anime) → 2x/4x
6. Line cleanup → OpenCV pipeline
7. Audio → Audacity, music library

### To Wire In (Next)
1. **ToonCrafter FP16** — swap model in notebook for ~2x speedup
2. **Framer** — evaluate as interactive alternative
3. **One-to-All Animation** — build rotoscope/body-replacement pipeline
4. **OpenToonz** — evaluate as compositing/finishing tool
5. **OpenColorIO** — standardize color management across pipeline

## ToonCrafter FP16 Upgrade

The FP16 pruned model (`tooncrafter_512_interp-fp16.safetensors`, ~2.5GB vs ~5GB)
can replace the full model in our Kaggle notebook:

```python
# In gen_notebook.py, cell 3, replace:
"https://huggingface.co/Doubiiu/ToonCrafter/resolve/main/model.ckpt"
# With:
"https://huggingface.co/Kijai/DynamiCrafter_pruned/resolve/main/tooncrafter_512_interp-fp16.safetensors"
```

**Expected:** ~1.5-2x faster inference, half the VRAM. Quality should be
near-identical (pruned + quantized, not retrained).

**TODO:** Test FP16 vs full model quality on Cape Jones frames before switching
production to FP16.

## References
- Awesome-AI4Animation: `~/workspace/tools/awesome-ai4animation/`
- ToonCrafter: `~/workspace/tools/tooncrafter/`
- FP16 model: https://huggingface.co/Kijai/DynamiCrafter_pruned
- One-to-All: `~/workspace/tools/one-to-all-animation/`
- Framer: `~/workspace/tools/framer/` (cloning)
