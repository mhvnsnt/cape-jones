# LTX-2 Distilled Smoke-Test — Kaggle GPU Runbook

**Date written:** 2026-10-23
**Code on repo:** `production/tools/ltx2/` (WIRING.md — read that first)
**Upstream:** Lightricks/LTX-2 @ 2026-10-22 (9,848★, pushed 2026-10-18)
**What it proves:** the pulled LTX-2 code + weights actually load on a GPU lane and produce one
synced audio+video clip end-to-end (DistilledPipeline, few-step). No production volume — one clip.

---

## 0. LICENSE — READ BEFORE ANY RUN (own-eyes verified 2026-10-22)

LTX-2 code AND weights are under the **LTX-2 Community License Agreement** (`production/tools/ltx2/LICENSE-2`,
dated 2026-01-05), NOT Apache/MIT. Verbatim from upstream LICENSE-2:

- Free to use, modify, distribute, **including commercial use**, for entities with **annual revenue under
  $10,000,000**.
- Entities at/above $10M annual revenue must obtain a **paid Commercial Use Agreement** from Lightricks —
  unlicensed commercial use by them is "strictly prohibited" and a material breach.
- "Derivatives of LTX-2" (fine-tunes, distillations, models trained on its outputs) stay under this agreement.
- The data used to train LTX-2 is NOT licensed under this agreement.

Our operation is an indie creator well under the $10M threshold → free commercial use applies.
**If the operation ever crosses $10M annual revenue, re-license before further use.**

## 1. WEIGHTS — GPU/KAGGLE SIDE ONLY, NEVER COMMITTED

Recommended: **LTX-2.5** from HuggingFace `Lightricks/LTX-2.5` (**gated repo — accept terms on HF, use a Read
token**). Quick-start set ≈ **66 GiB** (WIRING.md §Weights — copy the exact `hf download` block from there;
do NOT re-derive paths from memory).

DFR production quality additionally needs the detailing IC-LoRA from
`Lightricks/LTX-2.5-22b-IC-LoRA-Pixel-Spatial-Upscaler` — **skip it for the smoke test**.

Older generation: HF `Lightricks/LTX-2.3` single-file checkpoints (see `production/tools/ltx2/MODELS-LTX-2.3.md`).
The runbook works for 2.5 (recommended).

## 2. VRAM REALITY CHECK (read before booking GPU time)

The quick-start set is ≈66 GiB on disk: the 22B distilled transformer alone is ~44 GiB in bf16, plus the
gemma4-12b text encoder (~24 GiB). **These sizes are disk-weight facts; actual peak VRAM during a run is
NOT yet measured on our lanes** — the first smoke test must record it (`nvidia-smi` snapshot in the
notebook output) and this runbook must be updated with the real number.

What we know today:

| GPU lane | VRAM | Fits 22B distilled in bf16? |
|---|---|---|
| Kaggle T4×2 (free, 2 concurrent sessions) | 16 GB each | No (weights alone exceed it) |
| Kaggle P100 | 16 GB | No |
| Colab free T4 | ~15 GB | No |

Upstream's documented fit path for low VRAM is **`--quantization fp8-cast --offload {cpu,disk}`**
(WIRING.md §Usage). fp8 halves weight memory and offload spills layers to CPU/disk. The smoke test is
expected to be **slow** under offload — that is acceptable: the pass criterion is "it loads and produces a
synced clip", not "it renders fast".

If fp8-cast + offload still OOMs on a 16 GB card, the fallback is a **heavier lane** (Colab A100 if the
owner's tier provides one, Lightning AI, or another paid GPU) — do NOT spend a week fighting the 16 GB
ceiling. Record the outcome either way.

## 3. NOTEBOOK RUNBOOK (Kaggle, cell by cell)

Create a new Kaggle notebook: **Settings → Accelerator: GPU T4×2**, **Internet: ON** (needed for HF + pip),
Language: Python. Persist nothing in Quick Save — see §6.

**Cell 1 — base packages**

```python
!pip install -q uv huggingface_hub
import os
os.environ["HF_TOKEN"] = ""  # <-- paste your HF READ token (gated Lightricks/LTX-2.5 repo)
```

**Cell 2 — repo code (sparse, no history)**

```python
!git clone --depth 1 --filter=blob:none --sparse https://github.com/mhvnsnt/cape-jones /kaggle/working/cj
!git -C /kaggle/working/cj sparse-checkout set production/tools/ltx2
```

**Cell 3 — environment**

```bash
%%bash
cd /kaggle/working/cj/production/tools/ltx2
uv sync --extra natten   # natten = fastest diffusion-VAE backend (Linux+CUDA); falls back to Triton/eager elsewhere
```

`uv sync` on Kaggle typically takes 10–25 min. If `natten` fails to build on the kernel's CUDA, re-run with
plain `uv sync` and note the fallback in the output.

**Cell 4 — weights (≈66 GiB download; Kaggle internal network is fast, expect ~15–30 min)**

Use the exact `hf download` block from WIRING.md §Weights (copy it verbatim — do not re-derive paths).
Target dir: `/kaggle/working/models/ltx-2.5`. Confirm with `du -sh` afterwards.

**Cell 5 — the smoke test (DistilledPipeline, reduced)**

Start SMALL: 25 frames at reduced resolution. The point is a working load + synced A/V, not a pretty clip.

```bash
%%bash
cd /kaggle/working/cj/production/tools/ltx2
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv  # record the lane
uv run python -m ltx_pipelines.distilled \
    --transformer-path       /kaggle/working/models/ltx-2.5/diffusion_models/ltx-2.5-22b-distilled-transformer-bf16.safetensors \
    --text-encoder-path      /kaggle/working/models/ltx-2.5/text_encoders/gemma4-12b-with-proj-ltx-2.5-bf16.safetensors \
    --video-vae-path         /kaggle/working/models/ltx-2.5/vae/ltx-2.5-video-vae-bf16.safetensors \
    --audio-vae-path         /kaggle/working/models/ltx-2.5/vae/ltx-2.5-audio-vae-bf16.safetensors \
    --spatial-upsampler-path /kaggle/working/models/ltx-2.5/latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors \
    --quantization fp8-cast --offload cpu \
    --width 768 --height 448 --num-frames 25 --seed 42 \
    --output-path /kaggle/working/ltx2-smoke-001.mp4 \
    --prompt "A medium close-up of a cartoon boxer in a gym, he speaks in a deep male voice saying, 'One more round.' Gym ambience, a bell rings at the end."
```

Prompting rule (WIRING.md): describe BOTH picture and sound — who is on screen, what they say, in what
voice/tone, plus ambience/SFX. The model renders them synchronized.

**Cell 6 — verify + publish outputs (same session, do not wait)**

```python
from IPython.display import Video, Audio
Video("/kaggle/working/ltx2-smoke-001.mp4", width=512)
```

Then immediately publish the outputs as a dataset version (**Pattern B** from
`docs/research/KAGGLE-SAVE-RESEARCH.md` — zero re-run cost, survives session death):

```bash
%%bash
mkdir -p /kaggle/working/ltx2-smoke-out && cp /kaggle/working/ltx2-smoke-001.mp4 /kaggle/working/ltx2-smoke-out/
cd /kaggle/working && kaggle datasets version -p ltx2-smoke-out -m "ltx2 distilled smoke test 2026-10-23"
```

Notebooks run as the authenticated owner — no API keys needed for this. The queue-side
`kaggle_queue.py` lane can then pull the dataset and push second copies to GitHub releases + TeraBox.

## 4. SUCCESS CRITERIA

The smoke test PASSES if, with own eyes on the output:

1. The model stack **loads without OOM** under the flags in §3 (record peak `nvidia-smi` memory used).
2. `ltx2-smoke-001.mp4` **exists and plays** — picture AND audio in one file (LTX-2's whole point vs
   the video-only LTX-Video v1 in `production/tools/ltx-video/`).
3. The spoken line is **audibly present and roughly lip-aligned** to the on-screen figure (no
   frame-accurate metric needed — own-eyes grade).
4. The dataset version from §6 Cell 6 **exists with the mp4 attached** (check the dataset's Versions tab).

If any criterion fails, record the exact error + flags + lane (T4/P100, fp8/offload settings) in the
handoff or a new issue — **do not silently retry with different magic numbers**. Three failed attempts
across runs → mark `needs_owner` per the checkpoint protocol.

## 5. AFTER A PASS — what unlocks

- Scale up: `--num-frames 121`, full 1024×1536 defaults, seed sweeps for show b-roll.
- DFR production-quality pass (`uv run python -m ltx_pipelines.dfr_pipeline` + detailing IC-LoRA).
- Wire outputs into the show pipeline: LTX-2 synced dialogue scenes feed downstream only when a specific
  character face must be preserved (MuseTalk/LatentSync), MMAudio for foley the LTX-2 pass didn't nail,
  Real-ESRGAN for presentation upscales (WIRING.md §Show-pipeline uses).
- **Update this doc** with the measured peak VRAM (§2 table) and the actual wall-clock time — replace the
  estimates with our numbers.

## 6. KAGGLE OUTPUT DISCIPLINE (standing law from 2026-10-16 incident)

- **Never rely on Quick Save.** It saves code only — 0 output files. The 2026-10-16 incident lost 4 Pantera
  render chunks (~8 GPU-hours) this way.
- **Save & Run All** (commit) re-executes the whole notebook and captures up to 20 GB of `/kaggle/working/`.
- **Pattern B (primary):** publish a dataset version from INSIDE the notebook right after the clip lands —
  survives session death, no re-run.
- Sessions die on ~20 min idle and 12h hard limit — the smoke test must finish and publish inside one
  session, or be split into resumable cells.

---

*Companion docs: `production/tools/ltx2/WIRING.md` (code, commands, license verbatim),
`docs/research/KAGGLE-SAVE-RESEARCH.md` (output-preservation patterns from the 2026-10-16 incident).*
