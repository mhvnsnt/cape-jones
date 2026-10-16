# ToonCrafter on Kaggle GPU — Cape Jones Expressions Video

**Input:** `expressions-v2-noblack.mp4` (106 frames @ 12fps, 1080×1920, no black frames)
**Output:** 211 frames @ 24fps via ToonCrafter cartoon interpolation

## Why ToonCrafter Instead of RIFE?

RIFE was trained on **real video**. Its optical flow can't track motion in flat,
textureless cartoon regions (white suit, purple cape), so its occlusion mask
defaults to blending instead of warping = semi-transparent ghosted frames.

ToonCrafter ([SIGGRAPH Asia 2024](https://arxiv.org/abs/2405.17933), CUHK & Tencent,
Apache-2.0) is a diffusion model **specifically trained on cartoons**. It handles
the exaggerated non-linear motion and dis-occlusion common in animation that
flow-based methods fail on.

## How It Works

ToonCrafter's interp mode takes **2 keyframes** and generates **16 frames**
spanning between them. For 12fps → 24fps:

1. Extract 106 frames from input video
2. Build 105 adjacent pairs: (frame_0, frame_1), (frame_1, frame_2), ...
3. Each pair → ToonCrafter generates 16 frames on CUDA
4. Take the **middle frame** (idx 8) from each 16-frame output
5. Interleave: `[orig_0, mid_0, orig_1, mid_1, ...]` = 211 frames
6. Assemble to 24fps MP4

**Portrait handling:** Input is 1080×1920. ToonCrafter's 512 model was trained
at 512×320 (landscape), but the UNet is fully convolutional — we run at
`--height 512 --width 320` (portrait). Frames are resized to 320×512 for
inference, then the middle frames are upscaled back to 1080×1920 with Lanczos.

**Speed tradeoff:** `ddim_steps=25` (vs default 50) for reasonable Kaggle
session time. 105 pairs × ~1-2 min each ≈ 2-3 hours on T4.

## Files

| File | Description |
|------|-------------|
| `cape_jones_tooncrafter_kaggle.ipynb` | The Kaggle notebook (upload via File > Import) |
| `gen_notebook.py` | Generator script (regenerate the .ipynb after edits) |
| `README.md` | This file |

## Repo Assets (branch `kaggle-tooncrafter`)

| Path | Description |
|------|-------------|
| `production/kaggle/tooncrafter/input-12fps-noblack.mp4` | Input video (2.4MB, SHA-256 verified in notebook) |
| `production/kaggle/tooncrafter/cape_jones_tooncrafter_kaggle.ipynb` | Notebook copy |

## Browser Lane Runbook (for parent agent)

1. Open https://www.kaggle.com/code/new (signed in as marsfmmg)
2. File > Import Notebook → upload `cape_jones_tooncrafter_kaggle.ipynb`
3. Settings → **Accelerator: GPU T4 x2**, **Internet: ON**
4. **Run All** — record the ToonCrafter wall time printed by the inference cell
5. Download `/kaggle/working/cape-jones-expressions-TOONCRAFTER-24fps.mp4` from the file viewer
6. Save to `~/workspace/cape-jones-build/cape-jones-expressions-TOONCRAFTER.mp4`

## Expected Output

- 211 frames @ 24fps, 1080×1920, ~8.8 seconds
- Cartoon-native interpolation (no RIFE ghosting on flat colors)
- Compare side-by-side with the RIFE version to judge quality difference
