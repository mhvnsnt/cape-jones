# CAPE-JONES-WIRING.md — Open-Sora (HPC-AI Tech)

**Upstream:** https://github.com/hpcaitech/Open-Sora · pulled 2026-10-23 (idle pipeline)
**Stars:** 29,873 · **pushed upstream:** 2026-04-09 · **license:** Apache-2.0 ✅ (own-eyes verified on upstream LICENSE raw text 2026-10-23: "Apache License / Version 2.0, January 2004"; same file vendored here as `LICENSE`)
**Scope:** code-only, 1.9MB, 96/96 `.py` pass `py_compile`. 0 binaries >50MB, 0 weight files. Upstream `.github/workflows/` stripped per repo convention.

## What it is
Open-Sora is a full-stack open-source text-to-video system (HPC-AI Tech): DiT (diffusion transformer) video generation with t2v, image-to-video (i2v_head), and training/tuning scripts for the diffusion, VAE, and text-encoder stages. Compared to the two other video-gen slots already in this repo:
- **LTX-Video** (`production/tools/ltx-video/`, PR #186) — fast DiT t2v/i2v, video-only
- **LTX-2** (`production/tools/ltx2/`, PR #199) — synced audio+video in one pass (LTX-2 Community License, <$10M revenue caveat)
- **Open-Sora** (this) — the research-grade alternative: full training stack, multi-resolution configs (256px/768px), CPU offload flags, Gradio demo, Apache-2.0 with no revenue caveat

## Setup (GPU lane — Kaggle/Colab)
Weights live on HuggingFace (hpcaitech/Open-Sora / Open-Sora-v1.2) — download GPU-side only, NEVER committed.
```bash
cd production/tools/open-sora
pip install -r requirements.txt
# torchrun inference, 256px example (GPU):
torchrun --nproc_per_node 1 --standalone scripts/diffusion/inference.py \
  configs/diffusion/inference/t2i2v_256px.py --save-dir samples --prompt "raining, sea"
# image-to-video with a reference frame:
torchrun --nproc_per_node 1 --standalone scripts/diffusion/inference.py \
  configs/diffusion/inference/t2i2v_256px.py --cond_type i2v_head \
  --prompt "..." --ref assets/texts/i2v.png
# 768px production quality (multi-GPU):
torchrun --nproc_per_node 8 --standalone scripts/diffusion/inference.py \
  configs/diffusion/inference/t2i2v_768px.py --save-dir samples --prompt "raining, sea"
# memory-constrained single GPU:
... --offload True
```
## Show-pipeline uses
1. **Teaser/short renders** — t2v for Cape Jones promo clips and beat boards.
2. **Keyframe extension** — i2v_head takes a finished Blender proof still and extends it into motion (natural pair with `production/tools/ldf-vfi/` frame interpolation for 24→60fps smoothing).
3. **Style experiments** — full training stack (`scripts/diffusion/train.py`) allows fine-tuning a house style on the show's own renders (GPU lane, big job).
4. **Storyboard animatics** — 256px fast pass for pre-vis, 768px for final.

## Lane notes
- This lane is the Apache-2.0 "no revenue caveat" pick: if the project's commercial status ever outgrows LTX-2's $10M clause, Open-Sora is the drop-in legal-safe slot.
- `gradio/app.py` is a ready Gradio demo — the owner can run it on a GPU lane and prompt from a browser.
- Docs live under `docs/` (training guide, data processing, evaluation).
- Inference deps come from `requirements.txt` — lane installs, not the repo.
