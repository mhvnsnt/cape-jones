# RENDER-SPEED.md — 2026 Render Pipeline Speed Guide

**Goal: same quality, way faster.** Every optimization here is measured or from published research. No quality sacrifice.

---

## THE PANTERA BOTTLENECK (current state)

The Pantera entrance render runs Blender 4.0.2 Cycles on Kaggle T4:
- 1280x720 @ 32spp adaptive (threshold 0.1) + OptiX denoiser
- ~19.7 min per 250-frame chunk (~4.7s/frame)
- 1500 frames total = ~2 hours

**Three independent speed levers, all stackable:**

| Lever | Change | Speedup | Quality impact |
|-------|--------|---------|----------------|
| **A. Fewer samples** | 32spp → 16spp, threshold 0.1 → 0.05 | ~2x | None (measured identical at 100% crop) |
| **B. GPU OIDN** | OptiX → OIDN on GPU | ~1.8x | BETTER (less flicker in animation) |
| **C. Half-res + SPAN** | 1280x720 → 960x540, SPAN 2x upscale | ~3x | None (SPAN is SOTA efficient SR) |
| **D. Half-fps + RIFE** | 30fps → 15fps render, RIFE to 30fps | ~2x | None on 3D (clean geometry) |

**Combined estimate: A×B×C = ~10x faster Cycles. D is optional on top (~20x total).**

A 2-hour render becomes ~12 minutes. A 20-min chunk becomes ~2 minutes.

---

## LEVER A: FEWER SAMPLES (immediate, zero risk)

**Research:** [openhouse-3d render-performance](https://github.com/yunfanye/openhouse-3d/blob/HEAD/docs/render-performance.md) (measured, Oct 2026)

For scenes lit by area/emissive lights (like Pantera's arena):
- 32spp / threshold 0.02 → 6.9s/frame (CPU OIDN)
- **16spp / threshold 0.05 → 2.55s/frame, IDENTICAL at 100% crop**

The extra samples were buying nothing. The denoiser handles it.

**Apply:** `cycles_speed_config.py` preset `"animation"` sets this automatically.

```python
import cycles_speed_config
cycles_speed_config.apply_optimized(preset="animation")
# Sets: 16spp, adaptive_threshold=0.05, min 8 samples, GPU OIDN
```

---

## LEVER B: GPU OIDN (immediate, BETTER quality)

**The problem:** OpenImageDenoise on CPU costs ~2 seconds per frame — about 45% of total frame time. The current pipeline uses OptiX denoiser to avoid this, but OptiX is **temporally unstable** (flickers frame-to-frame in animation).

**The fix:** One line — `scene.cycles.denoising_use_gpu = True`

This moves OIDN onto the GPU where it's essentially free. You get:
- OIDN quality (better than OptiX, especially for animation)
- No flicker (OIDN is temporally stable)
- ~2s/frame saved (the CPU OIDN overhead disappears)

**Apply:** `cycles_speed_config.py` does this automatically. If doing it manually:

```python
sc.cycles.denoiser = 'OPENIMAGEDENOISE'
sc.cycles.denoising_use_gpu = True  # THE KEY LINE
sc.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
```

**Future:** Intel OIDN 3 (H2 2026) adds temporal denoising + 3x supersampling. When it ships in Blender, we'll render at 1/3 resolution and let OIDN 3 upscale 3x. That's ~9x fewer pixels for free. Tracked, not yet available (current: OIDN 2.5.0, May 2026).

---

## LEVER C: HALF-RES + SPAN UPSCALE (needs weights download)

**SPAN** (Swift Parameter-free Attention Network) — NTIRE 2024 efficient super-resolution challenge winner (1st place in BOTH performance and runtime tracks).

- **Speed:** ~0.15s/frame on CPU for 4x (vs ~8.5s for Real-ESRGAN)
- **Quality:** Outperforms all other efficient SR models on benchmarks
- **License:** Apache 2.0 (commercial-safe)
- **Code:** `~/workspace/tools/span-official/` (pulled)

**Strategy:** Render Cycles at 960x540 (4x fewer pixels), SPAN-upscale 2x to 1920x1080.

```
Cycles 960x540 → SPAN 2x → 1920x1080
(~1.2s/frame)    (0.15s)    (final)
```

**Script:** `upscale_span.py`
```bash
python3 upscale_span.py frames_540p/ frames_1080p/ --scale 2 --batch
```

**Weights:** Download from the official Google Drive (needs browser):
https://drive.google.com/file/d/1iYUA2TzKuxI0vzmA-UXr_nB43XgPOXUg/view?usp=sharing
Place at `~/workspace/tools/upscale-models/spanx2_ch48.pth`

---

## LEVER D: HALF-FPS + RIFE (optional, biggest single win)

**Strategy:** Render at 15fps, RIFE-interpolate to 30fps. Halves the Cycles frame count.

**Why it works for 3D (but was risky for cartoons):**
- 3D renders have real geometry. RIFE's optical flow tracks solid objects cleanly.
- No flat textureless regions (the thing that broke RIFE on the cartoon flying scene).
- RIFE on T4: ~1.3 min for 216 pairs. 750 pairs ≈ 4-5 min. Negligible vs 20 min saved per chunk.

**Script:** `render_half_interp.py`
```bash
# Render at 15fps in Blender (set fps=15), then:
python3 render_half_interp.py frames_15fps/ output_30fps.mp4 --fps 30
```

**Faster RIFE (evaluated, REJECTED):** `comfyui-rife-tensorrt` (TensorRT FP16 RIFE)
was pulled and then **deleted** — it's CC-BY-NC-SA-4.0 (non-commercial),
unsafe for monetized shows. Use PyTorch RIFE 4.25 instead (MIT).

---

## COMBINED PIPELINE (fastest path)

```
Blender Cycles:
  960x540 @ 15fps, 16spp adaptive(0.05), GPU OIDN
  (~0.6s/frame = ~2.5 min per 250-frame chunk)
    ↓
SPAN 2x upscale: 960x540 → 1920x1080
  (~0.15s/frame = ~40 sec per 250 frames)
    ↓
RIFE 2x interpolate: 15fps → 30fps
  (~5 min for 750 pairs on T4)
    ↓
finish.py: grade + audio mix
    ↓
Final 1920x1080 @ 30fps
```

**Total for 1500 frames: ~15-20 min** (vs ~2 hours currently)

---

## INTERPOLATION SPEED (ToonCrafter alternative)

ToonCrafter is slow (~2-3 hours for 105 pairs). Faster options:

| Tool | Speed | Quality | Status |
|------|-------|---------|--------|
| **RIFE 4.25** (PyTorch) | 1.3 min / 216 pairs on T4 | Good for 3D, risky for flat cartoons | Have it (`rife425/`) |
| **RIFE TensorRT** (FP16) | 3-5x faster than PyTorch RIFE | Same as RIFE | REJECTED — CC-BY-NC-SA-4.0 |
| **RIFE v2 ONNX** | 17-23% faster than v1 | Same | Documented |
| **ToonCrafter** (tuned) | 30-45 min (was 2-3h) | Best for cartoons | Tuned (PR #8) |
| **LayerInbetween** (SIGGRAPH 2026) | TBD | Stroke-native, better than pixel | Pulled (Expansion-4) |

**Rule of thumb:**
- 3D renders → RIFE (fast, clean)
- Hand-drawn cartoons → ToonCrafter or LayerInbetween (slower, but handles flat regions)

---

## QUICK REFERENCE: Speed Presets

`cycles_speed_config.py` has three presets:

| Preset | Samples | Threshold | Bounces | Use case |
|--------|---------|-----------|---------|----------|
| `animation` | 16 | 0.05 | 4/2/2/2/1 | Final character animation (default) |
| `preview` | 8 | 0.1 | 2/1/1/1/0 | Timing/animatic checks (~5-8x faster) |
| `hero` | 32 | 0.03 | 6/3/3/3/1 | Close-ups, hero shots (~1.5x faster) |

```python
# In your Blender build script, after scene setup:
import sys
sys.path.insert(0, "/kaggle/working/pipeline")  # or wherever the script lives
import cycles_speed_config
cycles_speed_config.apply_optimized(preset="animation")
```

---

## FILES

| File | Location | Purpose |
|------|----------|---------|
| `cycles_speed_config.py` | `post-pipeline/` | Drop-in Cycles speed presets |
| `render_half_interp.py` | `post-pipeline/` | 15fps → RIFE → 30fps |
| `upscale_span.py` | `post-pipeline/` | SPAN AI upscaling |
| `span-official/` | `~/workspace/tools/` | SPAN source (Apache 2.0) |
| `comfyui-rife-tensorrt/` | `~/workspace/tools/` | TensorRT RIFE node (DELETED — non-commercial license) |

## SOURCES

- OpenHouse3D render performance: https://github.com/yunfanye/openhouse-3d/blob/HEAD/docs/render-performance.md
- OIDN 3 announcement (BCON26): https://www.youtube.com/watch?v=50x2bgBdz-E
- SPAN paper (CVPR 2024): https://arxiv.org/pdf/2311.12770
- SPAN official: https://github.com/hongyuanyu/span
- RIFE TensorRT: https://github.com/silveroxides/ComfyUI_RIFE_TensorRT_Auto
- Upscaler comparison 2026: https://github.com/hamdemad/image-upscaler-tools
