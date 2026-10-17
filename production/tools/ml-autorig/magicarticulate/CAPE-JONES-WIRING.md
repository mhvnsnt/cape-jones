# MagicArticulate — Cape Jones wiring

**What:** MagicArticulate (NTU + ByteDance Seed, CVPR 2025) — automatic
skeleton generation (auto-regressive transformer) + functional-diffusion
skinning-weight prediction. Turns a static mesh articulation-ready in
1–2 s on GPU. NOTE: this is the ByteDance Seed team, NOT Meta — earlier
notes saying "Meta's MagicArticulate" are wrong (corrected here).
Upstream: https://github.com/Seed3D/MagicArticulate (pulled 2026-10-17).
Paper: https://arxiv.org/abs/2502.12135
Project page: https://chaoyuesong.github.io/MagicArticulate

**Where it fits:** it is the predecessor of Puppeteer (same team) — same
auto-regressive skeleton core, older functional-diffusion skinning head.
In the weight bake-off it is a third ML opinion alongside TokenRig/UniRig
(best single-pass skin) and Puppeteer (video-guided animation). Strongest
as a fast skeleton-proposer: run MagicArticulate for the joint layout,
cross-check against UniRig/Puppeteer joints, then pick the best skeleton
and re-skin with the winner.

**Verified this lane (2026-10-17, own-eyes):**
- All 18 `.py` files pass `python3 -m py_compile`.
- `LICENSE` is **Apache-2.0** (read the file directly) — license gate PASSED.
- Code + scripts + one smoke-test example mesh, ~7MB total (demo media pruned
  per repo convention — dropped 42MB of example .obj meshes, kept `boy.obj`
  2.4MB as the smoke-test input, matching the Puppeteer lane's deer.obj
  precedent); model weights were NOT pulled (they stay off local disk per
  law — see below).
- `__pycache__` removed post-compile so it never lands in the commit.

## Requirements (GPU machine — Kaggle / Colab, NOT the local VM)

- Python 3.10, NVIDIA GPU (~4.6 GB VRAM for skeleton inference, 1–2 s/mesh).
- `pip install -r requirements.txt` (torch, transformers, mesh2sdf, pyrender…)
- Submodule: `third_partys/Michelangelo` (clone upstream `--recursive` on the
  GPU machine; `.gitmodules` lists it — not vendored here).

## Model weights (download on the GPU machine — NOT committed here)

`download.py` does it all via `huggingface_hub`:
- `Seed3D/MagicArticulate`: `skeleton_ckpt/checkpoint_trainonv2_hier.pth`
  and `skeleton_ckpt/checkpoint_trainonv2_spatial.pth` (2025.8.07 updated
  weights fix the mesh↔skeleton normalization bug — use the fresh ones).
- `Maikou/Michelangelo`: `checkpoints/aligned_shape_latents/shapevae-256.ckpt`
  → `third_partys/Michelangelo`.

## Usage (Cape Jones model)

Skeleton generation, from this directory:

```bash
python demo.py --input_dir ./examples \
    --pretrained_weights skeleton_ckpt/checkpoint_trainonv2_hier.pth \
    --save_name infer_results_demo_hier --input_pc_num 8192 \
    --save_render --apply_marching_cubes --hier_order
```

For Cape Jones: drop the model (OBJ) into `examples/` first.
`--apply_marching_cubes` fuses shells — the same remesh-fusion the Tripo
multi-shell finding requires (matches the afk-rig/Pinocchio handling).
`--save_render` writes preview renders so the GPU lane can prove joint
placement without pulling heavy outputs back.

Skinning follows the same functional-diffusion head as `evaluate.py`
/ `skeleton_models/` — the lane that needs skin weights runs that after
skeleton review.

## Kaggle proof job (queue behind UniRig/Puppeteer)

Enqueue via the repo's `production/pipeline/kaggle_queue.py` batch queue
(never hand-run) once the GPU lane is free:
- input: Cape Jones model (OBJ, shells fused)
- outputs: `cj_magicarticulate_skeleton.txt`, render previews
- then compare joint layouts vs UniRig / Puppeteer / TokenRig before the
  skinning bake-off pick.
