# Frame Interpolation Research for Hand-Drawn Animation

**Date:** 2026-10-16
**Problem:** RIFE v4 produces fading/flashing (ghosting) on hand-drawn line art.
**Test video:** cape-jones-build/cape-jones-flying-scene-v1.mp4 (12fps, no black frames)

## Root Cause (Verified with Own Eyes)

RIFE's interpolated frames show the character as **semi-transparent/ghosted** while
original keyframes are sharp. This creates a sharp-ghost-sharp-ghost flicker.

**Why:** RIFE was trained on real video (Vimeo90K). It uses optical flow to track
motion between frames. On line art:
- Large flat color regions (white suit, purple cape) have NO texture
- Optical flow cannot lock onto textureless regions
- RIFE's occlusion mask defaults to ~0.5 (blend) when flow is uncertain
- Result: cross-dissolve instead of motion warp = ghosting

The AnimeInterp paper (CVPR21) confirms this exact problem:
> "cartoons comprise lines and smooth color pieces. The smooth areas lack textures
> and make it difficult to estimate accurate motions on animation videos."

## Methods Tested

### 1. RIFE v4 (baseline)
- **Status:** Installed and working (`~/workspace/tools/rife-v46/`)
- **Quality on animation:** Ghosts on flat regions. Sharp on textured areas.
- **Speed:** ~26s per frame pair on CPU at 1080x1920
- **TTA=True:** Tested - does NOT fix ghosting. Same artifact.

### 2. RIFE with 2x upscale trick
- **Theory:** More pixels = more detail for flow to track
- **Result:** Too slow on CPU (timed out at 10 min for single pair at 2160x3840)
- **Verdict:** Impractical without GPU

### 3. AnimeInterp (CVPR21) - DESIGNED FOR THIS EXACT PROBLEM
- **Status:** Code cloned, but pretrained weights UNAVAILABLE
- **Why perfect:** Segment-Guided Matching specifically solves "lack of textures"
  by matching color pieces instead of relying on optical flow alone
- **Blocker:** Dropbox weight link returns 404. No mirrors found.
- **Repo:** https://github.com/lisiyao21/AnimeInterp

### 4. AnimeInbet (ICCV23) - Cartoon line art specific
- **Status:** Code cloned
- **Why not suitable:** Designed for black-and-white LINE DRAWINGS only,
  not full-color animation. Uses graph-based vertex matching.
- **Repo:** https://github.com/lisiyao21/AnimeInbet

### 5. GMFSS Fortuna - "Dedicated for Anime Video Frame Interpolation"
- **Status:** Installed, model downloaded (70MB union model, anime fine-tuned)
- **Result:** Works but EXTREMELY slow on CPU (15+ minutes per frame pair,
  timed out before completing single test)
- **Verdict:** Impractical without GPU. Would need ~8 hours for 3-second clip.
- **Location:** `~/workspace/tools/gmfss/`

### 6. FLAVR (WACV23) - Flow-agnostic
- **Status:** Code cloned, not tested (needs weights + setup)
- **Theory:** Uses 3D convolutions instead of optical flow, so it doesn't
  suffer from flow-failure on flat regions
- **Potential:** High - flow-free approach sidesteps the root cause
- **Repo:** https://github.com/tarun005/FLAVR

### 7. DAIN (CVPR19)
- **Status:** Not installed (older than RIFE, benchmarks show RIFE generally wins)
- **Verdict:** Unlikely to beat RIFE on this problem

### 8. EMA-VFI (CVPR23)
- **Status:** Not installed
- **Benchmarks:** Actually scores WORSE than RIFE on SNU-FILM (LPIPS 0.050 vs 0.028)
- **Verdict:** Not worth pursuing

## Benchmark Summary (from published papers)

| Method | SNU-FILM LPIPS↓ | Year | Animation-specific? |
|--------|-----------------|------|---------------------|
| RIFE | 0.028 | 2022 | No |
| EMA-VFI | 0.050 | 2023 | No |
| AMT | 0.125 | 2023 | No |
| BiM-VFI | 0.032 | 2025 | No |
| EDEN | 0.021 | 2025 | No |
| AnimeInterp | N/A (own dataset) | 2021 | **YES** |

## Recommended Path Forward

### Option A: Fix RIFE's ghosting with post-processing (PRACTICAL NOW)
Build a de-ghosting filter:
1. Run RIFE as before
2. Detect ghosted pixels (where interpolated frame is a blend of neighbors)
3. In ghosted regions, snap to nearest sharp source using edge information
4. This preserves RIFE's smooth motion where it works, fixes where it doesn't

### Option B: Get AnimeInterp working (BEST QUALITY, needs weights)
- Contact the authors or search for mirror of `anime_interp_full.ckpt`
- This is THE solution designed for exactly this problem
- Segment-guided matching would handle flat color regions correctly

### Option C: FLAVR (PROMISING, needs setup)
- Flow-free = no optical flow failure mode
- Need to download weights and set up inference
- Worth trying as alternative

### Option D: Hybrid RIFE + selective fallback (PRAGMATIC)
1. Run RIFE
2. Compute per-pixel "confidence" (how much blending occurred)
3. Where confidence is low (ghosted), use original frame duplicated
4. Result: smooth where RIFE works, sharp where it doesn't, no flicker

## What the User Should Know

The fading/flashing is NOT a bug - it's RIFE working as designed on data
it wasn't trained for. Real video has texture everywhere. Cartoons don't.
No flow-based method will fully solve this without animation-specific training.

The "don't be lazy" answer: **AnimeInterp is the right tool, but we can't get
the weights.** The practical answer: **hybrid approach (Option D)** gives the
best quality we can achieve today with available tools.

## Files
- This doc: `~/workspace/cape-jones-build/INTERPOLATION-RESEARCH.md`
- RIFE: `~/workspace/tools/rife-v46/`, `~/workspace/tools/rife425/`
- GMFSS: `~/workspace/tools/gmfss/` (too slow on CPU)
- AnimeInterp code: `~/workspace/tools/animeinterp/` (no weights)
- FLAVR code: `~/workspace/tools/flavr/` (not set up)
- Test outputs: `/tmp/tta_test/`
