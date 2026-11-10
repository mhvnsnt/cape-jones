# Viggle-Animate Working Setup — Research

**Date:** 2026-10-16
**Status:** Complete working system pulled in

## The Problem

My hand-built Viggle-Animate notebook never worked end-to-end. It failed on:
- Dataset mounting (FileNotFoundError)
- Model downloads (99% then fail)
- Dependency issues

The owner was right: I was prototyping when I should pull in a whole working system.

## What I Found

The community already solved this. Three complete, working systems:

### 1. aireet/viggle-animate-workflow (PRIMARY)
**Source:** https://github.com/aireet/viggle-animate-workflow

"Viggle-Animate in one ComfyUI node, on an INT8 checkpoint, with automatic attention routing."

- **9-node ComfyUI workflow** — complete, tested
- **INT8 quantized checkpoint** — runs on 12GB VRAM (T4 compatible)
- **Example inputs/outputs included** — proves it works
- **Settings:** 6 steps, 124 frames, flow shift 3/3

**Location in repo:** `production/ai-body-replace/viggle-working/aireet-workflow/`

### 2. saganaki22/comfyui-viggle-animate-h3 (ComfyUI Nodes)
**Source:** https://github.com/saganaki22/comfyui-viggle-animate-h3

ComfyUI custom nodes for Viggle-Animate. Apache 2.0 licensed (the nodes, not the weights).

**Location in repo:** `production/ai-body-replace/viggle-working/comfyui-nodes/`

### 3. thefrizzy1/the_frizzy1-workflows (Complete Download List)
**Source:** https://github.com/thefrizzy1/the_frizzy1-workflows

Complete workflow JSON + exact download list with file sizes and tested configuration.

**Tested on:** RTX 3060 12GB, 32GB RAM, ComfyUI 0.37.4

**Location in repo:** `production/ai-body-replace/viggle-working/frizzy-workflow/`

## Required Model Files

All from HuggingFace (too large for GitHub, use Kaggle Datasets or direct download):

| File | Source | Size | Destination |
|------|--------|------|-------------|
| minimax_h3_ref2va_viggle_pruned_int8_convrot.safetensors | drbaph/Viggle-Animate-ComfyUI | 21.0 GB | `ComfyUI/models/diffusion_models/` |
| viggle_animate_dmd_lora_r64.safetensors | drbaph/Viggle-Animate-ComfyUI | 0.9 GB | `ComfyUI/models/loras/` |
| fixed_embed_fwd_anyframe.safetensors | drbaph/Viggle-Animate-ComfyUI | ~0 GB | `ComfyUI/models/text_cond/` |
| minimax_h3_video_vae_fp16.safetensors | Comfy-Org/MiniMax-H3 | 5.2 GB | `ComfyUI/models/vae/` |

**Total:** ~27 GB

## Key Settings (from tested workflows)

- **Steps:** 4-6 (more over-sharpens)
- **CFG:** 1.0
- **Shift:** 3.0 (ModelSamplingMiniMaxH3 — base default of 12 is WRONG)
- **Frames:** 124 @ 24fps
- **Resolution:** Multiple of 32 on both axes

## ⚠️ LICENSE WARNING

**The Viggle-Animate weights are released under the MiniMax H3 Community License, NOT Apache 2.0 or MIT.**

- Inference code: Apache 2.0 ✓
- Model weights: MiniMax H3 Community License ⚠️

**What this means:**
The MiniMax H3 Community License has geographic restrictions. Per our earlier research (2026-10-16), the H3 license **EXCLUDES US/EU/UK/South Korea**.

**The owner is in the US (Nashville, TN).**

This is a serious legal consideration. The owner previously wanted Viggle-Animate deployed, but the license may prohibit commercial use in the US.

**Recommendation:** 
1. Read the full license at https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE
2. Owner should decide if he wants to proceed given the geographic restriction
3. Document the decision

**This is NOT legal advice.** I'm flagging the issue; the owner decides.

## Why This Works (vs My Hand-Built Notebook)

1. **Community-tested** — Multiple people have this running
2. **Complete** — All nodes, all configs, all settings
3. **Quantized** — INT8 checkpoint fits on T4 (12GB)
4. **Documented** — Exact file list, exact settings, tested hardware

My notebook was trying to reinvent this from scratch. That was the mistake.

## Next Steps

1. **License decision** — Owner reviews H3 license, decides to proceed or not
2. **Model download** — Get the 27GB of weights (Kaggle Dataset or direct)
3. **ComfyUI setup** — Install ComfyUI + the custom nodes on Kaggle/Colab
4. **Test run** — Run the aireet workflow with our inputs
5. **Wire into pipeline** — Once working, integrate with `finish.py`

## Sources

- Official model: https://huggingface.co/Viggle/Viggle-Animate
- Official research: https://viggle.ai/research/viggle-animate-character-replacement-from-a-repainted-frame
- aireet workflow: https://github.com/aireet/viggle-animate-workflow
- ComfyUI nodes: https://github.com/saganaki22/comfyui-viggle-animate-h3
- Weights: https://huggingface.co/drbaph/Viggle-Animate-ComfyUI
- VAEs: https://huggingface.co/Comfy-Org/MiniMax-H3
