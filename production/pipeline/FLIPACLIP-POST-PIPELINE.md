# FlipaClip Post-Production Pipeline

**Purpose:** Take hand-drawn FlipaClip animations (phone app, 12fps) and make them broadcast-quality.

**Workflow:** User draws on FlipaClip → sends video → this pipeline → professional output.

**Tools location:** `~/workspace/tools/post-pipeline/`

---

## The Pipeline (5 Stages)

Run everything with one command:
```bash
~/workspace/tools/post-pipeline/flipaclip_post.sh input.mp4 output.mp4
# Add --upscale flag for neural upscale (use when source is <720p):
~/workspace/tools/post-pipeline/flipaclip_post.sh input.mp4 output.mp4 --upscale
```

### Stage 1: Denoise + Deflicker (ffmpeg)
Hand-drawn frames have grain and brightness flicker between frames.
```
hqdn3d=1.5:1.5:6:6    # High-quality 3D denoiser (spatial + temporal)
deflicker=size=5       # Smooths luminance variation across frames
```

### Stage 2: Line Cleanup (OpenCV)
`cleanup_lines.py` — the custom tool:
- **Bilateral filter:** Smooths flat color areas while preserving every edge and color. Purple stays purple, black stays black.
- **Thin-line detection:** Finds dark pixels, then EXCLUDES large connected blobs (those are fills like the cowl/cape, not lines). Only operates on structures <4000px.
- **Pinhole fill:** Tiny morphological close fills micro-gaps in lines.
- **Crisp redraw:** Thin lines repainted in near-black for punch.

**Critical:** Never recolors fills. v1 of this script turned the purple cowl black — fixed by excluding large components.

### Stage 4: Upscale 2x
- **Default (fast):** Lanczos resample — 0.2s/frame. Good for 1080p sources.
- **`--upscale` flag (neural):** ESPCN x4 → Lanczos downscale to 2x. ~6s/frame on CPU. Use for low-res phone exports. Model: `models/ESPCN_x4.pb` (OpenCV dnn_superres).

### Stage 3: Frame Interpolation 12fps → 24fps (RIFE AI)
**Default:** RIFE v4 (Real-Time Intermediate Flow Estimation) neural interpolation.
AI-estimated optical flow produces dramatically smoother, artifact-free inbetweens
vs ffmpeg — verified pixel-perfect middles on small/medium cartoon motion.
**Runs at source resolution BEFORE upscale.** ~26s/pair on CPU (~14 min for 3 sec).
Tools: `~/workspace/tools/rife-venv/` (PyTorch CPU), `~/workspace/tools/rife425/rife_interp.py`,
model: RIFE v4 HD weights in `~/workspace/tools/rife-v46/train_log/flownet.pkl`.

**`--fast` flag:** falls back to ffmpeg minterpolate for quick previews:
```
minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir
```
~2.5 min for 3 sec. Lower quality — visible warping on fast cartoon motion.

**Known limit:** like all flow-based methods, RIFE ghosts on extreme teleports
(character jumping across screen in one frame). Normal animation motion is clean.

### Stage 5: Sharpen + Color Punch (ffmpeg)
```
unsharp=5:5:0.8          # Light sharpening (luma only)
eq=saturation=1.1:contrast=1.03  # Slight color pop
```

---

## Compositing

### Quick compositing (ffmpeg)
For layering character over backgrounds, cards, etc.:
```bash
# Character with alpha over background
ffmpeg -i background.mp4 -i character_alpha.mp4 \
  -filter_complex "[0:v][1:v]overlay=0:0" output.mp4

# Concat segments (intro card + animation + end card)
ffmpeg -i intro.mp4 -i main.mp4 -i outro.mp4 \
  -filter_complex "[0:v]setsar=1[a];[1:v]setsar=1[b];[2:v]setsar=1[c];[a][b][c]concat=n=3:v=1:a=0" \
  output.mp4
```

### Full compositing (Natron)
**Natron 2.5.0** — open-source After Effects/Nuke alternative. Node-based compositing.
- Location: `~/workspace/tools/post-pipeline/natron/` (after download completes)
- Use for: complex multi-layer comps, color grading, effects chains
- GUI app — needs display for interactive use

### 3D / Advanced compositing (Blender)
Blender 4.0.2 already at `~/workspace/tools/blender/` — run with `xvfb-run`:
```bash
xvfb-run -a ~/workspace/tools/blender/blender-4.0.2-linux-x64/blender -b
```
Use the Compositor for node-based video compositing, or Grease Pencil for 2D animation.

---

## Background Separation (Matting)

**NEVER use chroma key on animation.** (Owner law 2026-10-15.)

| Method | When to use |
|--------|-------------|
| **RVM** (Robust Video Matting) | AI matting for video — separates character from background by shape, not color. In `~/workspace/tools/rvm/`. |
| **rembg** | AI background removal for still images. In `~/workspace/tools/rembg-venv/`. |
| **Manual rotoscoping** | Last resort for tricky shots. |

---

## Tool Status

| Tool | Status | Location |
|------|--------|----------|
| ffmpeg (denoise, interp, comp) | ✅ Working | system |
| cleanup_lines.py | ✅ Working, tested | `tools/post-pipeline/` |
| ESPCN upscaler | ✅ Working, tested | `tools/post-pipeline/models/` |
| flipaclip_post.sh | ✅ Working, tested | `tools/post-pipeline/` |
| RIFE (AI frame interpolation) | ✅ Working, tested | `tools/rife-venv/`, `tools/rife425/rife_interp.py` |
| RIFE v4 HD weights | ✅ Downloaded | `tools/rife-v46/train_log/flownet.pkl` |
| RVM (video matting) | ✅ Installed | `tools/rvm/` |
| rembg (image matting) | ✅ Installed | `tools/rembg-venv/` |
| Natron 2.5.0 | ⬇️ Downloading | `tools/post-pipeline/natron/` |
| Blender 4.0.2 | ✅ Installed | `tools/blender/` |
| Real-ESRGAN | ❌ Skipped | Needs GPU; ESPCN covers CPU use case |
| RIFE | ❌ Skipped | Needs GPU + PyTorch; minterpolate covers CPU |

---

## Performance Notes (CPU-only VM, no GPU)

| Operation | Speed |
|-----------|-------|
| Line cleanup | ~1s/frame |
| Lanczos 2x upscale | 0.2s/frame |
| ESPCN neural upscale | ~6s/frame |
| 12→24fps interpolation | ~4s/frame |
| **Full pipeline (3s video)** | **~8-10 minutes** |

For longer videos, consider batching overnight or using a GPU machine.
