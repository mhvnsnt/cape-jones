# Depth-Anything-V2 — CAPE-JONES WIRING

Pulled 2026-10-22 (overnight-idle-pipeline) into `production/tools/depth-anything-v2/`.
Upstream: https://github.com/DepthAnything/Depth-Anything-V2 (arXiv 2406.09414, HKU/TikTok).

## What it is

Monocular depth estimation — single RGB image/video in, dense depth map out.
Significantly outperforms Depth Anything V1 on fine-grained detail; faster and more
accurate than SD-based depth models. Four encoders: `vits` (24.8M), `vitb` (97.5M),
`vitl` (335M), `vitg` (1.3B). Relative depth (default) plus metric-depth heads in
`metric_depth/` (absolute depth, indoor/outdoor variants incl. small/base).

## License

**Apache-2.0** — verified own-eyes in the pulled tree's `LICENSE` file. Commercial
use allowed. ✅

## Weights (NOT in repo — Kaggle/GPU side only)

The repo ships code + docs only (64MB, zero `.pt`/`.pth`/`.ckpt` files verified on
pull). Checkpoints download from HuggingFace at run time — the script expects
`checkpoints/depth_anything_v2_<encoder>.pth` in the working dir:

| Encoder | Checkpoint |
|---|---|
| vits | https://huggingface.co/depth-anything/Depth-Anything-V2-Small/resolve/main/depth_anything_v2_vits.pth |
| vitb | https://huggingface.co/depth-anything/Depth-Anything-V2-Base/resolve/main/depth_anything_v2_vitb.pth |
| vitl | https://huggingface.co/depth-anything/Depth-Anything-V2-Large/resolve/main/depth_anything_v2_vitl.pth |
| vitg | https://huggingface.co/depth-anything/Depth-Anything-V2-Giant/resolve/main/depth_anything_v2_vitg.pth |

Per the standing law, weights stay OFF local disk — download inside the Kaggle/Colab
lane's scratch, use, discard. Never commit a `.pth` to the repo.

## GPU-lane runbook

Requirements: `torch`, `torchvision`, `opencv-python`, `matplotlib` (see
`requirements.txt`; gradio only needed for `app.py`).

```bash
# single image / image dir -> depth visualizations
python run.py --img-path <image-or-dir> --encoder vitl --outdir ./vis_depth
python run.py --img-path frame.png --encoder vits --grayscale --pred-only

# video (uses run_video.py)
python run_video.py --input-video <mp4> --encoder vitb --outdir ./depth_frames

# metric (absolute) depth — see metric_depth/ README for checkpoint URLs
```

Depth Anything V2 is also in HuggingFace transformers
(`depth_anything_v2` model doc) and as a ComfyUI node family — both are
Kaggle-lane options when the raw script path is heavy.

## Cape Jones uses

- **Living-room scenes / sit-takes:** depth passes for depth-of-field and
  depth-based fog/haze, and for cleanly separating the character plate from the
  background plate in compositing.
- **Camera work:** depth-driven refocus racks on the 2D/walkthrough renders.
- **3D conversion research:** monocular depth is the input to 2D→3D/stereo
  experiments for the show cuts.
- **Scene QA:** depth maps make segmentation/placement errors (feet under floor,
  clipping geometry) pop out when the RGB looks "fine".

## Local verification (2026-10-22, this VM)

- 38/38 `.py` files pass `python3 -m py_compile`. ✅
- `run.py --help` NOT runnable locally — needs `torch` (GPU-lane tool by design,
  same as SOMA-X wiring). This is expected, not a defect.
- Zero weight/binary files in the pulled tree; nothing >50MB. ✅
