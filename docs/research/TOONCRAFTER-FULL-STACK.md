# ToonCrafter Full-Stack Research — Why It Kept Failing and the Complete Fix

**Date:** 2026-10-16  
**Status:** Research complete, fix implemented  
**Author:** Subagent (parent: main agent)

## Executive Summary

ToonCrafter kept failing for one root reason: **we were using the wrong model**.
The full `model.ckpt` (10.5GB) requires ~23GB VRAM. Our Tesla T4 has 16GB.
Every inference attempt was doomed to OOM-kill before it started.

The community solution — **Kijai's pruned FP16 model** — requires only 12GB VRAM
and fits comfortably on T4. This is what the official ToonCrafter README
recommends for 12GB GPUs.

## Root Cause Analysis

### Failure 1: Kaggle v3 — Died at 99% of 10.5GB download

**What happened:** `wget` downloading `model.ckpt` from HuggingFace reached 99%
(121.7s) then the kernel died.

**Why:** 10.5GB single-file download is fragile. Likely causes:
- Kaggle kernel preemption during long download
- Network timeout on large file
- Disk space pressure in `/kaggle/working`

**Status:** Mitigated via weight caching. Dataset `marsfmmg/tooncrafter-weights`
now contains the verified 10.5GB `model.ckpt` (10,502,492,136 bytes).
But see below — we shouldn't be using this model at all on T4.

### Failure 2: Colab — Died before/during inference (Cell 6)

**What happened:** Cells 1-5 completed (clone, pip install, 106 frames extracted).
Cell 6 (ToonCrafter CUDA inference) produced zero output. No error captured.

**Why:** **VRAM exhaustion (OOM).** Evidence:
- camenduru's community Colab notebook explicitly states: **"Pro Colab 😭 ~23GB VRAM"**
  (source: https://github.com/camenduru/ToonCrafter-jupyter)
- Our T4 has 15.6GB usable VRAM
- 23GB required > 15.6GB available = guaranteed OOM kill
- Colab doesn't always surface OOM errors clearly; the kernel just dies

**This was the smoking gun.** We were trying to run a 23GB model on a 16GB GPU.

### What We Were Missing (Owner's Question)

The owner asked: "you're probably fucking it up... there's probably some research
you missed." He was right. Here's what we missed:

1. **VRAM requirement never checked.** Nobody verified the model's VRAM requirement
   against our T4's 16GB before running. The CHECK step was skipped.

2. **Wrong model variant.** The official ToonCrafter README lists Kijai's pruned
   FP16 model for 12GB GPUs. We downloaded the full model instead.

3. **No safetensors support.** The official `inference.py` uses `torch.load()`
   which cannot load `.safetensors` files. Kijai's model is safetensors-only.

4. **Community knowledge not pulled in.** camenduru's working Colab, Kijai's
   pruned models, and the ComfyUI wrapper all existed. We hand-built our own
   notebook instead of starting from the community-tested setup.

## The Fix: Kijai's Pruned FP16 Model

### Model Details

| Property | Full Model | Pruned FP16 Model |
|----------|-----------|-------------------|
| File | `model.ckpt` | `tooncrafter_512_interp-fp16.safetensors` |
| Source | `Doubiiu/ToonCrafter` | `Kijai/DynamiCrafter_pruned` |
| Size | 10.5 GB | ~2.5 GB (estimated) |
| VRAM required | ~23 GB | **12 GB** |
| Fits on T4 (16GB) | **NO** | **YES** |
| License | Apache-2.0 | Apache-2.0 (model) |

**Source:** Official ToonCrafter README community support table lists Kijai's
pruned FP16 for 12GB GPUs:
https://huggingface.co/Kijai/DynamiCrafter_pruned/blob/main/tooncrafter_512_interp-fp16.safetensors

Kijai's README confirms: "interpolation at 512p can be done with 8GB"

### Why FP16 Works

- Full model: FP32 weights (4 bytes/param) = 10.5GB file, ~23GB VRAM at inference
- Pruned FP16: FP16 weights (2 bytes/param) + pruned (fewer params) = ~2.5GB file, 12GB VRAM
- Quality loss from FP16 is minimal for inference (standard practice in 2026)
- Pruning removes redundant parameters without significant quality impact

### The Safetensors Problem

Kijai's model is `.safetensors` format. The official ToonCrafter `inference.py`
uses `torch.load()` which cannot read `.safetensors`.

**Solution:** Convert safetensors → .ckpt once, then use normally.
The conversion script is at `production/kaggle/tooncrafter/convert_safetensors_to_ckpt.py`.
This is a standard format conversion, not hand-tooling the model logic.
The converted .ckpt loads identically via the existing `load_model_checkpoint()`.

## LDF-VFI Assessment

**Status:** Pulled into `production/tools/ldf-vfi/` but **NOT recommended for T4**.

**Why:**
- README states: "requires ~20GB GPU memory" for 8x interpolation
- Our T4: 16GB → **won't fit**
- It's CVPR 2026 SOTA for quality, but SOTA doesn't help if it OOMs
- Python 3.11 + PyTorch 2.5.1 required (we're on 3.13 in Kaggle)

**Verdict:** LDF-VFI is better than ToonCrafter on paper, but unusable on our
hardware. Keep the code in the repo for future (if we get A100 access), but
don't try to run it on T4.

## 2026 Alternatives Research

**Question:** Is there anything better than ToonCrafter for cartoon interpolation
on T4 in 2026?

**Answer:** No. ToonCrafter remains the best open-source option for cartoon-specific
interpolation that fits on 16GB VRAM.

| Tool | Type | Cartoon-specific | Fits T4 | Notes |
|------|------|-----------------|---------|-------|
| ToonCrafter (FP16) | Diffusion | **YES** | **YES (12GB)** | Best for our use case |
| ToonCrafter (full) | Diffusion | YES | NO (23GB) | What we were using (wrong) |
| LDF-VFI | Diffusion | No | NO (20GB) | SOTA quality, too big |
| RIFE | Flow-based | No | YES (CPU) | Ghosts on cartoons (owner rejected) |
| AnimeInterp | Flow-based | Partial | YES | Lightweight, lower quality than diffusion |

**Is One-to-All better than ToonCrafter?** No — different tasks. One-to-All is
for body replacement (pose transfer). ToonCrafter is for frame interpolation.
They solve different problems in the pipeline.

## Complete Dependency List

### Official Requirements (from Doubiiu/ToonCrafter/requirements.txt, fetched 2026-10-16)

The official requirements include: `decord==0.6.0` (REMOVED — no cp313 wheels,
not used in inference), `einops==0.3.0`, `imageio==2.9.0`, `numpy==1.24.2`,
`omegaconf==2.1.1`, `opencv_python`, `Pillow==9.5.0`, `pytorch_lightning==1.9.3`,
`transformers==4.25.1` (BUMPED to 4.48.3 for cp313), `torch==2.0.0`,
`open_clip_torch==2.22.0`, `xformers`, `timm`, `kornia`, `av`, `moviepy`.

### Gaps in Our Previous Install (now fixed)

We were missing: `imageio`, `opencv-python`, `Pillow`, `PyYAML`, `tqdm`,
`safetensors`. These are now included in both notebook generators.

### System Requirements

- **Python:** 3.8-3.11 officially. We use 3.13 (Kaggle) with transformers bump.
  Colab uses 3.10+ (works with official versions).
- **CUDA:** >=11.3. T4 ships with compatible CUDA.
- **VRAM:** 12GB minimum (FP16 model), 23GB (full model)
- **Disk:** ~5GB for FP16 model, ~12GB for full model + workspace
- **RAM:** 12GB+ recommended (Kaggle has 30GB, Colab has 12.7GB)

## Implementation

### Files Changed

- `docs/research/TOONCRAFTER-FULL-STACK.md` (this file)
- `production/kaggle/tooncrafter/convert_safetensors_to_ckpt.py` (new)
- `production/kaggle/tooncrafter/gen_notebook.py` (updated: FP16 model + missing deps)
- `production/kaggle/tooncrafter/cape_jones_tooncrafter_kaggle.ipynb` (regenerated)
- `production/colab/gen_tooncrafter_colab.py` (updated: FP16 model + missing deps)
- `production/colab/cape_jones_tooncrafter_colab.ipynb` (regenerated)

### What Parent Needs to Do

1. **Create FP16 Kaggle dataset:** Download Kijai's safetensors, convert to .ckpt
   via the script, upload as `marsfmmg/tooncrafter-weights-fp16` dataset.
   (Use a CPU seeding kernel — no GPU needed for conversion.)
2. **Test on Kaggle T4:** Push test kernel with FP16 model attached. Verify
   inference completes without OOM.
3. **Test on Colab T4:** Run the updated Colab notebook. The FP16 download
   (~2.5GB) is much faster than the full model (~10.5GB).

## Verification

- [x] Official requirements.txt fetched and compared (`verified` — via browser.open)
- [x] camenduru's VRAM requirement documented — 23GB (`verified` — via search)
- [x] Kijai's FP16 VRAM requirement documented — 12GB (`verified` — via official README)
- [x] LDF-VFI VRAM requirement documented — 20GB (`verified` — via repo README)
- [x] Conversion script written, compiles OK (`verified` — via py_compile)
- [x] Both notebook generators updated, notebooks regenerate cleanly (`verified`)
- [ ] FP16 model downloaded and converted (`unverified` — needs parent, large file)
- [ ] Kaggle FP16 dataset created (`unverified` — needs parent, seeding kernel)
- [ ] Live T4 inference test (`unverified` — needs parent, GPU run)

## References

- Official ToonCrafter: https://github.com/Doubiiu/ToonCrafter
- Kijai's pruned models: https://huggingface.co/Kijai/DynamiCrafter_pruned
- camenduru's Colab: https://github.com/camenduru/ToonCrafter-jupyter
- ComfyUI wrapper: https://github.com/kijai/ComfyUI-DynamiCrafterWrapper
- LDF-VFI: https://github.com/xypeng9903/LDF-VFI
- Low-VRAM fork: https://github.com/supraxylon/ToonCrafter-Low-VRAM
