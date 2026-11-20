# Cape Jones — Pipeline Stage Map (Harmony + Free Stack)

Branch: `tools/free-stack-wireup-20261120` (no merge, no PR).
Binaries: release `harmony-equivalents-20261120` + release
`production-stack-free-20261120`, both on mhvnsnt/dream-girl.
This show's own pipeline doc: `production/pipeline/ANIMATION-PIPELINE-2026.md`
(Stage 1 Tahoma2D draw → Stage 2 Synfig rig/tween → Stage 3 RIFE/Kaggle-GPU
interpolate → Stage 4 OpenToonz composite → Stage 5 Finish
`FLIPACLIP-POST-PIPELINE.md` → Stage 6 Blender VSE / ffmpeg assembly).
Fetch + verify all 10 binaries: `bash tools/free-stack/fetch-verify.sh`.

## Standing rule

**Limited-animation cuts; rig/composite experiments.** These tools slot
into the existing Cape Jones pipeline above — they do not replace it.
Synfig carries a standing **eval gate** from the pipeline doc: prove it on
one Cape Jones shot (rig → 3 keys → tween → render) and document the
result before production use.

## Stage map — each tool's exact slot in the Cape Jones pipeline

| Tool | Version | Slot in this show's pipeline | Status |
|---|---|---|---|
| **Tahoma2D** (already in this repo's pipeline, NOT re-pulled) | 1.6.x pinned | **Stage 1 — Draw.** Primary 2D workhorse: hand-drawn frame-by-frame keys, Xsheet, raster/smart-raster/vector levels. | In pipeline |
| **Synfig Studio** | 1.5.5 | **Stage 2 — Rig & tween.** Vector keyframes + automatic tweening + bone/skeleton rigs; interpolation at the authoring level. Output PNG sequences → OpenToonz or straight to Finish. **Eval gate applies** (prove on one CJ shot first). Docs-only version already in this repo at `production/tools/synfig/README.md` (PR #165) — this binary lands alongside it. | LANDED |
| **Glaxnimate** | 0.6.0 | **Titles / motion graphics.** Vector motion design, Lottie + animated SVG export for title cards and UI motion; Kdenlive companion. Not character rigging. | LANDED |
| **Enve** | continuous d919d4d (2021-06-22) | **Spare vector / rigging seat.** Real and working, but **STALE upstream (last push 2022-09-25)** — Synfig is the live rigging pick. | LANDED (stale) |
| **Wick Editor** | 1.19.0 pre-release (2020-12-11) | **Quick vector cartoons + interactive.** Flash-style drawing, timeline, symbols, motion tweens, in-editor JavaScript. **Desktop builds stale since 2020** — web editor live. | LANDED (stale desktop) |
| **AniCraft** | 0.2.1 | **Animate-format interchange experiments.** Clean-room Adobe Animate reimplementation (XFL/FLA/SWF per project description). FLA-compat test against a real .fla still owed. | LANDED |
| **Pencil2D** | 0.7.2 | **Hand-drawn roughs / timing.** Lightweight raster+vector frame-by-frame, onion skin — roughs and timing tests feeding Stage 1 (Tahoma2D). | LANDED |
| **Rigby2D** | 0.5.1 | **Skeletal rig experiments.** 2D skeletal/mesh/IK/physics editor, JSON/.skel export — the live Spine/Moho cover, tried against Synfig for rigged cuts. Complement, not a pipeline replacement. | LANDED |
| **Olive** | 0.2.0-nightly (8ac191ce) | **Node-edit experiments only.** Alpha secondary NLE, upstream PAUSED — do NOT cut deadline work in it. | LANDED (alpha) |
| **Kdenlive** | 26.08.3 | **Finish — primary NLE alternative.** Cutting episodes, assembling renders, subtitles, colour — alongside the existing Finish chain (`FLIPACLIP-POST-PIPELINE.md`) and Blender VSE / ffmpeg assembly. | LANDED |
| **Douga** | build 1116 | **Pen-first cel timing (Windows-only).** Real dope sheet (keys, holds, loops, exposure on ones/twos) for hand-drawn timing work feeding Stage 1. Free exports carry a small "made with douga.app" watermark. | LANDED (Windows-only) |

## What this wire-up does NOT duplicate

- `production/tools/synfig/README.md` (PR #165, docs-only) and
  `production/tools/opentoonz/README.md` (PR #165, docs-only) stay where
  they are — this branch adds the Synfig **binary** under
  `tools/harmony/synfig/` and the rest of the stack; it does not re-stage
  the PR #165 docs.
- OpenToonz 1.8.0 stays docs-only (no Linux binary; Flatpak is the route);
  Tahoma2D carries the compositing role on Linux.
- AnimLab — already staged on branch `tools/animlab-wireup-20261120`,
  NOT re-staged here.

## GPU routes (owner law: no-GPU is never an excuse)

GPU-dependent work (Rigby2D EGL, Kdenlive OpenGL, RIFE interpolate)
runs on a working GPU source — **Kaggle GPU first** (validated live
2026-11-20: `kaggle kernels list --mine` returns marsfmmg's kernels;
T4/P100 free tier, 30 hrs/wk; RIFE already runs there per the pipeline
doc), **Colab second** (free-tier T4 notebook via browser). Lightning AI
is down until its watch reports recovery; Oracle Cloud free tier is
CPU-only and is not a GPU route. Never write "can't run here / no GPU on
this box" as a blocker — route the test to Kaggle.
