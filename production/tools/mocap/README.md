# Markerless Motion Capture Tools

## SAM-Body4D (`sambody4d/`)

**Training-free, temporally-consistent 4D human mesh recovery from video** — single
command video→motion for the show animation pipeline (owner directive: "AI logic,
animations that look good and work on him").

- Source: https://github.com/gaomingqi/sam-body4d (pulled 2026-10-22, master HEAD)
- License: **MIT** (top-level). Vendored deps keep their own licenses:
  - `models/sam3/` → Meta SAM License (custom, royalty-free; use/distribute/modify
    allowed; non-transferable; terminates on IP litigation against Meta)
  - `models/sam_3d_body/dinov3/` → Meta DINO License (same class)
  - `models/diffusion_vas/` → MIT
  - None restrict commercial use (verified 2026-10-22; not CC-BY-NC/AGPL).
- Occlusion-robust, multi-human, works under camera motion.

### Setup (one-time, GPU side — weights stay OFF this disk)

Weights download on the GPU lane (Kaggle/Colab). SAM 3 and SAM 3D Body require
prior Hugging Face access approval; log in once, then:

```bash
huggingface-cli login
python sambody4d/scripts/setup.py --ckpt-root /path/to/checkpoints
```

Manual weights: `facebook/sam3`, `facebook/sam-3d-body-dinov3`,
`Ruicheng/moge-2-vitl-normal`, Depth-Anything-V2-Large, Diffusion-VAS —
paths in `sambody4d/configs/body4d.yaml` (set `paths.ckpt_root` only).

### Usage

```bash
cd production/tools/mocap/sambody4d
python scripts/offline_app.py --input_video <clip.mp4> --output_dir ./outputs
# input may also be a directory of .jpg/.png frames
```

Outputs 4D body meshes per frame (see `runtime.output_dir` in `body4d.yaml`).
Gradio demo: `python app.py`.
