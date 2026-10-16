# EXPANSION-4: Continuous Research — 2026 Bleeding Edge + Established Tools

Date: 2026-10-16
Research completed via two parallel lanes. Full raw findings in `/tmp/track1-findings.md` and `/tmp/track2-findings.md`.

---

## TRACK 1: 2026 Bleeding Edge — PULLED

### 1. LayerInbetween (SIGGRAPH 2026) ⭐ TOP FIND
- **Path:** `~/workspace/tools/layerinbetween/`
- **URL:** https://github.com/MarkMoHR/LayerInbetween
- **What:** Automatic inbetweening from clean line drawings / rough sketches / multi-character line art. Vector-based stroke correspondence with OCCLUSION handling and automatic layering. Editable vector output. Multi-frame recursive prediction.
- **Why:** Direct upgrade over pixel interpolators (ToonCrafter/RIFE) for hand-drawn frames. Stroke-native = no pixel artifacts, editable output. Occlusion + multi-character support is what breaks pixel methods.
- **License:** Check repo (author's prior work is research-use; verify before commercial use).
- **Compute:** PyTorch + diffvg + SAM2; modest GPU for inference (no DiT). Kaggle T4 viable.
- **Status:** Pulled (9MB, code only). Weights download on Kaggle.

### 2. LTX-2.5 (Lightricks, Aug 2026) ⭐
- **Path:** `~/workspace/tools/ltx-2/`
- **URL:** https://github.com/Lightricks/LTX-2 / https://huggingface.co/Lightricks/LTX-2.5
- **What:** 22B open-weights video DiT. Synchronized VIDEO+AUDIO in one pass. NATIVE MULTISHOT (multiple connected shots, same character/voice/lighting, single inference). Diffusion video decoder (sharper faces/text). Distilled 8-step Fast checkpoint. Day-one ComfyUI support.
- **Why:** Direct upgrade from our LTX-Video. Multishot = whole scenes with cuts in one generation. Synced audio kills the separate SFX sync step for previz.
- **License:** LTX Community License — free commercial under $10M revenue. NO territorial exclusions. READ actual license before commercial use.
- **Compute:** Distilled ~12GB VRAM (T4 viable). Full 22B needs 24GB+.
- **Status:** Pulled code (6.4MB). Weights download on Kaggle (gated HF repo).

### 3. OmniColor (Mar 2026)
- **Path:** `~/workspace/tools/omnicolor/`
- **URL:** https://github.com/zhangxulu1996/OmniColor
- **What:** Multi-modal (reference image + text + hints) line-art colorization.
- **Why:** Colorize line-art keys from a single reference — cuts coloring labor dramatically.
- **Compute:** DiT-class, expect 12-24GB. Kaggle T4 with optimization.
- **Status:** Pulled (6.2MB, code only).

### 4. EverAnimate (May 2026)
- **Path:** `~/workspace/tools/everanimate/`
- **URL:** https://github.com/vita-epfl/EverAnimate / https://huggingface.co/epfl-vita/everanimate
- **What:** Rank-32 LoRA on Wan2.2-Animate-14B → minute-scale animation with persistent latent propagation. Fully open: code, training/inference, LoRA checkpoints, demo data.
- **Why:** PLUGS DIRECTLY INTO OUR WAN 2.2 STACK. Extends Wan2.2-Animate to minute-long coherent takes.
- **License:** Check repo; base Wan2.2 is Apache 2.0.
- **Compute:** Wan2.2-Animate-14B class (~24GB; LoRA is light).
- **Status:** Pulled (8.2MB, code only). LoRA downloads on Kaggle.

### 5. OPEN-TOON (Sept 2026, GPL-3.0)
- **Path:** `~/workspace/tools/open-toon/`
- **URL:** https://github.com/mijim/OPEN-TOON
- **What:** NEW open-source professional 2D animation desktop app. Drawing, rigging, compositing, production tools. Vector drawing + MyPaint brushes, timeline/X-sheet, onion skin, visual pose animation, editable motion curves, PNG sequence export.
- **Why:** Potential open replacement/augmentation for Krita/OpenToonz in the hand-drawn lane.
- **License:** GPL-3.0 (fine for internal production use).
- **Compute:** CPU desktop app.
- **Status:** Pulled (16MB source). Experimental builds available.

### 6. ComfyUI_VideoFX_Suite (Sept 2026, MIT)
- **Path:** `~/workspace/tools/comfyui-videofx-suite/`
- **URL:** https://github.com/CoderMayne/ComfyUI_VideoFX_Suite
- **What:** GPU-accelerated VFX, color grading, post-processing for video batches in ComfyUI. Cinematic/lens looks, retro/VHS-CRT, glitch, temporal/motion trails, stylized/thermal vision, atmosphere/film damage.
- **Why:** Post/finishing pass inside existing ComfyUI pipeline.
- **License:** MIT.
- **Status:** Pulled (1.4MB). Copy to `ComfyUI/custom_nodes/`.

### Already have (verified, not re-pulled)
- One-to-All Animation (CVPR 2026) — `~/workspace/tools/one-to-all-animation/`
- ToonComposer (ICLR 2026) — `~/workspace/tools/tooncomposer/`
- OpenMontage — `~/workspace/tools/openmontage/`

### EXCLUDED on license (documented, NOT pulled)
- **MiniMax H3 / Animating on Twos adapters / ComfyUI-H3-LongTake:** H3 Community License EXCLUDES US, EU, UK, South Korea. Owner is US-based → legally unusable. Verified via 8frame.co (2026-09-30).
- **TalkingPose (WACV 2026):** Research-only license. Documented only.
- **Wav2Lip:** Relicensed to non-commercial/research-only. Do NOT use.

### Failed to pull (network issues — retry on stable connection) — RESOLVED 2026-10-16
- InstanceAnimator (multi-instance sketch colorization) — https://github.com/YinHan-Zhang/InstanceAnimator — ✅ PULLED into `production/tools/InstanceAnimator/` (Apache-2.0, 4.1MB). NOTE: model weights are lost per author ("you need to retrain model"); code-only pull, train on Kaggle-side. Code was found staged in ~/workspace/tools/InstanceAnimator-main and moved into the repo.
- SCAIL-2 (skeleton-free animation) — ✅ recovered via PR #33 into `production/tools/SCAIL-2/`.
- LDF-VFI (CVPR 2026 generative interpolation) — ✅ recovered via PR #33 into `production/tools/LDF-VFI/`.

---

## TRACK 2: Established Tools — PULLED

### 7. GDQuest Krita Batch Exporter
- **Path:** `~/workspace/tools/krita-batch-exporter/`
- **URL:** https://github.com/GDQuest/krita-batch-exporter
- **What:** Batch-exports Krita layers/groups to files with naming rules, trim options, per-layer sizing.
- **Why:** Turns Krita into a proper asset factory for cutout rigs, sprite sheets, title cards.
- **License:** Open source (GDQuest).
- **Status:** Pulled (680KB). Install as Krita plugin.

### 8. FFmpeg Animation Filters Cheat Sheet (BUILT)
- **Path:** `~/workspace/tools/post-pipeline/ffmpeg-animation-filters.sh`
- **What:** 20 animation-specific FFmpeg filter recipes: smooth60 interpolation, celshade posterize, deband, denoise (fast/best), sharpen, deflicker, deshake, grade-pop, grade-warm, vignette, film grain, motion trails, zoompan (Ken Burns), high-quality GIF export, retro dithering, timecode burn-in, frei0r cartoon/edgeglow.
- **Why:** All filters already built into local FFmpeg. Zero downloads. Wired into pipeline.
- **Status:** Built, tested, executable. Pushed to cape-jones repo.

### Already have (verified, not re-pulled)
- Rhubarb Lip Sync — `~/workspace/tools/rhubarb/`
- Friction (motion graphics) — `~/workspace/tools/friction/`
- OpenFaceFX — `~/workspace/tools/openfacefx/`

### Documented for later (large downloads or server setup)
- **Kdenlive** (kdenlive.org, GPL-3.0) — Full multitrack NLE. The stack has NO NLE — biggest editorial gap. AppImage available. Pull when disk allows.
- **Ardour** (ardour.org, GPL-2.0) — Professional multitrack DAW for dialogue + score + final mix.
- **LMMS** (lmms.io, GPL-2.0) — FL-Studio-style beat maker. Matches owner's music background.
- **OpenColorIO** (opencolorio.org, Apache-2.0) — Industry color management. Fixes cross-app color drift.
- **OpenCue** (opencue.io, Apache-2.0) — Sony's render queue manager for multi-lane renders.
- **Glaxnimate** (glaxnimate.mattbas.org, GPL-3.0) — Vector motion graphics, Lottie export. Integrates with Kdenlive.
- **Aegisub** — Styled subtitle timing/typesetting for dialogue captions.
- **G'MIC** (gmic.eu, CeCILL) — Hundreds of cartoon/stylization filters for Krita/GIMP/CLI.
- **COA Tools 2** (github.com/hcqmaker/coa_tools2, GPL) — Blender 2D cutout rigging. URL needs verification.
- **CasparCG** (casparcg.com, GPL-3.0) — Broadcast graphics server for template-driven titles.
- **Surge XT** (GPL-3.0) — Synth for cartoon SFX stingers.
- **Freesound.org** — CC-licensed SFX library (resource, not software).

### Explicitly NOT recommended (stale/dead)
- TupiTube (2020, unmaintained), Enve (superseded by Friction), Wick Editor (upstream discontinued), Olive 0.2 (rewrite stalled).

---

## Pipeline Wiring

New script wired into `production/pipeline/`:
- `ffmpeg-animation-filters.sh` — 20 animation filter recipes, all local, zero GPU

Kaggle setup needed for GPU tools:
- LayerInbetween: PyTorch + diffvg + SAM2 env, download weights from repo
- LTX-2.5: download distilled checkpoint from HF (gated), ~12GB VRAM
- OmniColor: download weights from repo, DiT-class GPU
- EverAnimate: download LoRA from HF (epfl-vita/everanimate), plugs into Wan2.2-Animate-14B

## Disk Impact

Total new pulls: ~48MB (code only). All model weights download on Kaggle, not locally.
Disk: 80% (was 78%). Approaching 85% threshold — prioritize TeraBox offload.

## Repo Push

- `ffmpeg-animation-filters.sh` → `mhvnsnt/cape-jones` `production/pipeline/` (branch → PR → merge)
- This doc → `docs/research/EXPANSION-4.md`
