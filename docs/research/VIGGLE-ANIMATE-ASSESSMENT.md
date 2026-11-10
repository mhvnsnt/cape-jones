# Viggle-Animate Assessment — Why We're Pivoting

**Date:** 2026-10-16
**Status:** DEAD END for our use case — documented honestly per ANTI-SYCOPHANCY RULE
**Replacement:** One-to-All Animation (CVPR 2026, Apache-2.0)

## What Viggle-Animate Is

Viggle-Animate (HuggingFace `Viggle/Viggle-Animate`, 2026) is Viggle Research's open
release for character replacement in video from a single repainted frame. It replaces
the character in a driving video with whatever you paint into one of its frames —
no pose estimation, no segmentation, no masks. 124 frames in ~26s on one GPU.

## Why It Cannot Work For Us

### 1. VRAM: 73.5 GiB Required (we have 16 GiB)

From the official HuggingFace Space README (verified 2026-10-16):

> **Hardware.** The transformer is 62 GiB in bf16; with the VAEs that is 73.5 GiB
> on the card. ZeroGPU `xlarge` (96 GB) is required — `large` is 48 GB and cannot
> hold it.

Our GPUs:
- Kaggle T4: 16 GB VRAM
- Kaggle T4 x2: 16 GB each (not pooled for single-model inference)
- Colab T4: 16 GB VRAM
- Colab free tier: 16 GB VRAM

**73.5 GB > 16 GB. The model cannot load on any GPU we have access to.**
This is not a setup issue, not a configuration issue, not a "wire it up better"
issue. It is a physical hardware impossibility.

### 2. License: MiniMax H3 Community License EXCLUDES the USA

From `Viggle/Viggle-Animate` LICENSE (verified 2026-10-16):

> The weights are a Model Derivative of MiniMax H3, so the MiniMax H3 Community
> License applies to them.

The MiniMax H3 Community License defines "Excluded Territories" as:
**the European Union, the United Kingdom, the Republic of Korea, and the
United States of America.**

Our owner is in the USA. Using these weights would violate the license terms.

This is the same license exclusion we already documented for MiniMax H3 /
TalkingPose / Wav2Lip in the Expansion-4 license review (PR #17).

## What We Tried

Our hand-built Viggle-Animate notebook (production/ai-body-replace/) failed on
every Kaggle attempt:
- v1: pip dependency failures
- v2: dataset not attached (FileNotFoundError)
- v3: dataset attached but FileNotFoundError persisted

These failures were symptoms. The root cause is that even a "working" setup
could never load the 73.5 GB model on a 16 GB T4.

## The Pivot: One-to-All Animation

**One-to-All Animation** (CVPR 2026, Apache-2.0) — already in
`production/tools/one-to-all-animation/`:

| | Viggle-Animate | One-to-All 1.3B |
|---|---|---|
| VRAM needed | 73.5 GB | **16 GB (T4)** |
| License | MiniMax H3 (excludes USA) | **Apache-2.0** |
| Speed | 124 frames / 26s | 10s video / ~11 min on T4 |
| T4 verified | No (impossible) | **Yes, by authors** |

The authors explicitly state: "GPU-poor? Run One-to-All 1.3B + ComfyUI for free
on Kaggle's 16 GB T4."

## Evidence Tags

- 73.5 GB VRAM requirement: `verbatim` (copied from HF Space README)
- License exclusion of USA: `verbatim` (copied from HF LICENSE)
- Our T4 VRAM (16 GB): `verified` (nvidia-smi on Kaggle/Colab)
- One-to-All T4 support: `single-source` (author README claim, not yet tested by us)

## Next Steps

1. Build Kaggle notebook for One-to-All 1.3B (in progress)
2. Test on T4 with Cape Jones driving video
3. If quality suffices, replace Viggle-Animate in pipeline docs
4. Keep Viggle-Animate research for when we have 80GB+ GPU access
