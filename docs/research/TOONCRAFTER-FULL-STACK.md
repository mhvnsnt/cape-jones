# ToonCrafter Full-Stack Research — Why It Kept Failing and the Complete Fix

**Date:** 2026-10-16
**Status:** v4 — independently verified, 5 new bugs fixed, notebooks regenerated
**Author:** Subagent (parent: main agent)

## v4 (2026-10-16) — Independent Verification Pass

The v3 research below was re-verified claim-by-claim against primary sources
(actual code, APIs, and downloads — not docs about docs). The core diagnosis
(VRAM: wrong model) held up. But the v3 *fix itself* contained 5 bugs that
would have made the "fixed" notebook fail. All are fixed in this pass.

### Claims verified (evidence-tagged)

- **Full model needs ~24-27GB VRAM** — `verified` (official ToonCrafter README,
  line 224: "the model may consume about 24G~27G GPU memory in this
  implementation"). T4 (16GB) was always doomed. Root cause stands.
- **Pruned FP16 needs ~12GB** — `verified` (official README community table,
  line 266). Caveat found: that figure assumes **fp16 execution** (the ComfyUI
  path). Stock `inference.py` runs the model in fp32 — see Bug 5.
- **Input video SHA** — `verified` (downloaded
  `input-12fps-noblack.mp4` from `raw.githubusercontent.com`, 2,395,219 bytes;
  sha256 = `c039dff8332f4e9ae697e81eb36f709dc38b0303eb830a2d3e7903fc91b1e19a`,
  matches the notebook's assertion).
- **`marsfmmg/tooncrafter-weights` dataset seeded** — `verified` (Kaggle API:
  contains `model.ckpt`, 10,502,492,136 bytes, created 2026-10-17T00:38:54Z).
  **BUT:** this is the FULL model (OOM on T4). The notebook's cache-first path
  looks for `/kaggle/input/tooncrafter-weights-fp16/model.ckpt` — that dataset
  **does not exist**, so the cache always misses and the notebook falls back to
  the HuggingFace download. ACTION for parent: seed `tooncrafter-weights-fp16`
  (3.2GB converted .ckpt) via a CPU kernel so runs don't depend on the HF
  download.
- **prompt_dir layout** — `verified` (read `load_data_prompts()` in
  `scripts/evaluation/inference.py`: interp mode pairs `file_list[2*idx]` /
  `[2*idx+1]` from a sorted glob — our `pair_{i:03d}_a/b.png` + `prompts.txt`
  layout is correct).

### Bugs found in the v3 fix (all fixed in v4)

**BUG 1 — Wrong HuggingFace filename (would 404).**
v3 used `tooncrafter_512_interp-fp16.safetensors` (underscore), copied from the
official ToonCrafter README's community table. That link is **stale**: Kijai
renamed the file and the README was never updated. The real filename is
`tooncrafter_512_interp-pruned-fp16.safetensors` (hyphen).
Verified by 2 independent sources: the HF API repo listing
(`api/models/Kijai/DynamiCrafter_pruned` siblings) and Kijai's own
ComfyUI-DynamiCrafterWrapper `nodes.py` (lines 48, 56). The v3 notebook's
`wget` would have 404'd on every run. Lesson: the README is not the source of
truth — the file listing is.

**BUG 2 — Wrong file size (size guard would reject the real file).**
v3 said "~2.5GB (estimated)" and the `_ok()` guard accepted 2.0–3.0GB.
Measured via HTTP range request on the real file: **3,175,466,358 bytes
(3.18GB)**. The genuine download would have FAILED the guard. Guard is now
2.8–3.8GB (torch.save adds a few % pickle overhead over the safetensors).

**BUG 3 — `--n_samples 105` would generate 11,025 videos.**
In `inference.py`, `n_samples` = samples **per prompt** (default 1). The
prompt loop already iterates all 105 prompts in batches. Passing 105 =
105 samples × 105 prompts. Fixed to `--n_samples 1`.

**BUG 4 — Assembly cell looked in the wrong place for the wrong file type.**
v3 searched `<savedir>/*/samples/*` for per-sample PNG directories. Reality
(read `save_results_seperate()`): `save_results()` is commented out upstream,
so `samples/` stays empty; each prompt's output is ONE 8-frame MP4 written to
`<savedir>/samples_separate/pair_{i:03d}_a_sample0.mp4`. Assembly rewritten:
dump each MP4's 8 frames, take idx 4, upscale, interleave.

**BUG 5 — fp16 weights loaded into an fp32 model (VRAM risk).**
Kijai's wrapper runs the model in fp16 (`model.to(precision)`); the README's
12GB figure assumes this. Stock `inference.py` calls
`model.load_state_dict()` on an fp32 model, silently casting fp16→fp32
(~6.4GB weights + activations could push past 16GB on T4). v4 patches the
cloned repo's `run_inference()` to `model.half()` right after checkpoint load
(with an assert that fails loudly if upstream changes the anchor lines).

### What parent still needs to do (unchanged from v3, updated)

1. **Seed the FP16 Kaggle dataset:** download
   `tooncrafter_512_interp-pruned-fp16.safetensors` (3.18GB), convert with
   `production/kaggle/tooncrafter/convert_safetensors_to_ckpt.py` on a CPU
   kernel, upload as `marsfmmg/tooncrafter-weights-fp16`. (Until then the
   notebook downloads from HF every run — works, but slower and fragile.)
2. **Run the v4 notebook on Kaggle T4** (or the Colab lane) and verify one
   pair completes without OOM, then let the 105-pair run go (~45-60 min).
3. **Nothing in v3's core diagnosis changed** — fix ToonCrafter, don't replace
   it. RIFE ghosts on cartoons (owner rejected), LDF-VFI needs ~20GB (won't
   fit T4), AnimeInterp is flow-based/lower quality. ToonCrafter FP16 remains
   the best 2026 option for cartoon interpolation on 16GB VRAM.

### v4 verification checklist

- [x] Official README VRAM figures read from source (`verified`)
- [x] HF filename + size measured from live API/CDN (`verified`)
- [x] `inference.py` interp pairing, n_samples semantics, output paths read from source (`verified`)
- [x] Input video SHA re-hashed from GitHub raw (`verified`)
- [x] Kaggle weight dataset listing checked via API (`verified`)
- [x] Both notebook generators updated, notebooks regenerated, all cells compile (`verified`)
- [x] Generated notebooks spot-checked: correct URL, n_samples=1, samples_separate, half() patch (`verified`)
- [ ] FP16 dataset seeded on Kaggle (`unverified` — needs parent)
- [ ] Live T4 inference test (`unverified` — needs parent, GPU run)

---

## Executive Summary (v3 — retained)

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
