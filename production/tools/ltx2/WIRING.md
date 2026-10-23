# LTX-2 — WIRING

**Upstream:** Lightricks/LTX-2 (main @ 2026-10-22, 9,848★, active — pushed 2026-10-18)
**What:** The first DiT-based audio-video foundation model that generates **synchronized audio and video in one model** — text-to-video, image-to-video, keyframe animation, video extension, plus native audio (dialogue/SFX/ambience baked into the generation, not dubbed after).
**Pipeline slot:** VIDEO GENERATION (successor generation). Sibling of `production/tools/ltx-video/` (LTX-Video v1, PR #186 — video-only DiT). LTX-2 is the synced-audio+video step up: one prompt produces picture AND sound together.

## LICENSE — READ BEFORE USE (own-eyes verified 2026-10-22)

The code AND the weights are under the **LTX-2 Community License Agreement** (LICENSE-2, dated 2026-01-05), NOT Apache/MIT. Verbatim from upstream LICENSE-2:

- Free to use, modify, and distribute, **including commercial use**, for entities with **annual revenue under $10,000,000**.
- Entities at/above $10M annual revenue must obtain a **paid Commercial Use Agreement** from Lightricks — unlicensed commercial use by them is "strictly prohibited" and a material breach.
- "Derivatives of LTX-2" (fine-tunes, distillations, models trained on its outputs) stay under this agreement.
- Data used to train LTX-2 is NOT licensed under this agreement.

Our operation is an indie creator well under the $10M threshold → free commercial use applies. **If the operation ever crosses $10M annual revenue, re-license before further use.** (Same caveat pattern as KittenTTS v2's $1M Stellon license.)

## Layout

```
production/tools/ltx2/
├── packages/
│   ├── ltx-core/       # model code: DiT transformer, video+audio VAEs, tiling, multigpu
│   ├── ltx-kernels/     # custom CUDA kernels (blockwise attention, VAE kernels)
│   ├── ltx-pipelines/  # user-facing pipelines: distilled, DFR, IC-LoRA, DubIt, two-stage
│   └── ltx-trainer/    # training code (not needed for inference)
├── pyproject.toml      # uv workspace
├── README.md           # upstream quick start (full)
├── CHANGELOG.md
├── MODELS-LTX-2.3.md   # LTX-2.3 weight list (older generation; 2.5 recommended)
└── WIRING.md           # this file
```

Stripped on pull: upstream `.claude/` agent-runbook housekeeping (132K, Claude-Code trainer scaffolding — not inference code). No `.github/` in upstream. No weights/binaries in tree (verified).

## Pipelines (all in packages/ltx-pipelines)

| Pipeline | Module | Use |
|---|---|---|
| **DistilledPipeline** | `ltx_pipelines.distilled` | Fast starting point, few-step distilled transformer |
| **DFRPipeline** | `ltx_pipelines.dfr_pipeline` | Production quality: distilled transformer + detailing IC-LoRA + spatial detailing pass (slower, more VRAM) |
| ICLoraPipeline | `ltx_pipelines.ic_lora` | IC-LoRA controlled generation (camera/detailer/pose/motion LoRAs) |
| DubItPipeline | — | Dubbing pipeline |
| Two-stage (TI2Vid / Keyframe / A2Vid) | — | Full dev transformer, highest control |

## Weights — GPU/KAGGLE SIDE ONLY, NEVER COMMITTED

Recommended: **LTX-2.5** from HuggingFace `Lightricks/LTX-2.5` (gated repo — accept terms, Read token). Quick-start set ≈ **66 GiB**:

```bash
hf download Lightricks/LTX-2.5 \
    diffusion_models/ltx-2.5-22b-distilled-transformer-bf16.safetensors \
    text_encoders/gemma4-12b-with-proj-ltx-2.5-bf16.safetensors \
    vae/ltx-2.5-video-vae-bf16.safetensors \
    vae/ltx-2.5-audio-vae-bf16.safetensors \
    latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors \
    --local-dir models/ltx-2.5
```

DFR production quality additionally needs the detailing IC-LoRA:
`Lightricks/LTX-2.5-22b-IC-LoRA-Pixel-Spatial-Upscaler/ltx-2.5-22b-ic-lora-pixel-spatial-upscaler-x2-1.0.safetensors`

Older generation **LTX-2.3** weights: HuggingFace `Lightricks/LTX-2.3` (see MODELS-LTX-2.3.md — single-file checkpoints bundling transformer + VAEs).

## Setup (GPU lane)

```bash
cd production/tools/ltx2
uv sync --extra natten   # natten = fastest diffusion-VAE backend (Linux+CUDA); skipped elsewhere, falls back to Triton/eager
```

## Usage — fast (DistilledPipeline)

```bash
uv run python -m ltx_pipelines.distilled \
    --transformer-path       models/ltx-2.5/diffusion_models/ltx-2.5-22b-distilled-transformer-bf16.safetensors \
    --text-encoder-path      models/ltx-2.5/text_encoders/gemma4-12b-with-proj-ltx-2.5-bf16.safetensors \
    --video-vae-path         models/ltx-2.5/vae/ltx-2.5-video-vae-bf16.safetensors \
    --audio-vae-path         models/ltx-2.5/vae/ltx-2.5-audio-vae-bf16.safetensors \
    --spatial-upsampler-path models/ltx-2.5/latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors \
    --num-frames 121 --seed 42 \
    --output-path output.mp4 \
    --prompt "A medium close-up ... he speaks with a deep male voice saying, 'I think it's so good.'"
```

Prompting rule: describe BOTH picture and sound in the prompt (who is on screen, what they say, in what voice/tone, plus ambience/SFX). The model renders them synchronized.

Low VRAM: add `--quantization fp8-cast --offload {cpu,disk}`. Defaults: 1024×1536 @ 24fps. UHD 4K: `--width 3840 --height 2176`.

## Usage — production quality (DFR)

Same flags as above but via `uv run python -m ltx_pipelines.dfr_pipeline`, adding:
`--detailing-lora models/ltx-2.5/loras/ltx-2.5-22b-ic-lora-pixel-spatial-upscaler-x2-1.0.safetensors`
Expect longer runtime and more VRAM than DistilledPipeline.

## Show-pipeline uses

- AI-generated scenes / b-roll with **native synced audio** (one shot, no separate dub step)
- Dialogue scenes: prompt the spoken lines directly; pair downstream with MuseTalk/LatentSync only if a specific character face must be preserved
- SFX/ambience beds: pair with MMAudio (`production/tools/audio/mmaudio/`) for foley the LTX-2 pass didn't nail
- Upscale LTX-2 outputs with Real-ESRGAN (`production/tools/realesrgan/`) for presentation renders

## Verification (this pull)

- 339/339 `.py` files `py_compile` clean
- Binary scan: 0 files >50MB, 0 weight files (`.safetensors/.bin/.pt/.pth/.onnx/.ckpt`) in tree
- Duplicate pre-check passed: repo tree has `ltx-video` (v1) but no `ltx2`/`ltx-2` code — new slot, not a duplicate
- License own-eyes verified on upstream LICENSE-2 raw text 2026-10-22 (see LICENSE section above)
