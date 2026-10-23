# SkinTokens / TokenRig — Cape Jones wiring

**What:** TokenRig (from the SkinTokens project, VAST-AI-Research, MIT license —
commercial use allowed). Successor to UniRig (SIGGRAPH '25): a unified
autoregressive framework that takes ONE 3D mesh and outputs a complete rig —
skeleton hierarchy + dense per-vertex skinning weights — in a single token
sequence. 98%–133% better skinning accuracy than UniRig per the authors.
Upstream: https://github.com/VAST-AI-Research/SkinTokens (commit 273b691d, pulled 2026-10-17).

**Why here:** the owner-directed standing task is "auto-rig Tripo models
perfectly" (2026-10-17) — and this project is BY VAST (the Tripo makers), i.e.
trained by the same team that generates Tripo models. It is the best-known
open-source auto-rigger for AI-generated assets. It complements BlenRig 6
(blenrig6/): BlenRig is the artist-driven control rig; TokenRig is the
one-shot AI pass — use TokenRig for the first rig/skin, refine with BlenRig.

**Verified this lane (2026-10-17, own-eyes):**
- All `.py` files pass `python3 -m py_compile`.
- LICENSE is MIT (commercial use permitted) — license gate PASSED.
- `.git` stripped; code-only pull, 15MB; model weights were NOT pulled
  (they stay off local disk per law — see below).

## Requirements

- NVIDIA GPU with ≥14 GB VRAM (inference). Run on **Kaggle/Colab**, not the local VM.
- Python ≥3.11, CUDA ≥12.1, `uv` recommended. See upstream README for the
  exact torch/requirements install.

## Model weights (download on the GPU machine — NOT committed here)

`python download.py --model` pulls to `experiments/`:
- `articulation_xl_quantization_256_token_4` — TokenRig rigging model
  (trained on ArticulationXL 2.0 + VRoid Hub + ModelsResource, GRPO-refined, recommended)
- `skin_vae_2_10_32768` — FSQ-CVAE skin-weight tokenizer
- `models/` — Qwen3-0.6B config

Upstream Hugging Face: linked from the upstream README "Pretrained Models" section.

## Usage (Cape Jones model)

Single mesh in, fully rigged GLB out:

```bash
# full auto-rig + skin
python demo.py --input <cape-jones>.glb --output results/cape-jones-rigged.glb

# preserve Tripo textures + original scale
python demo.py --input <cape-jones>.glb --output results/cape-jones-rigged.glb --use_transfer

# batch
python demo.py --input 3d-assets/cape-jones/ --output results/ --use_transfer
```

**Skin onto an existing skeleton** (e.g. a BlenRig-generated armature):
```bash
python demo.py --input skeleton-only.glb --output results/cape-jones-skinned.glb --use_skeleton --use_transfer
```
This is the planned BlenRig × TokenRig combo: BlenRig guide → generate → export
skeleton → TokenRig skin weights → merge back.

## Cape Jones lane runbook

1. Input: the native Tripo GLB (0.925 m — DO NOT rescale, per scale canon).
   Keep meshes ≤ ~100k verts; decimate first if needed.
2. Run `demo.py --use_transfer` on the Kaggle GPU to keep textures/scale.
3. Import the result into Blender 4.0.2: check vertex groups per bone,
   especially **shoulder deformation** (the known failure: weights tear past
   15° arm raise — compare against the measured problem in
   `~/workspace/bannon-video-pipe/docs/AI_RIGGING_RESEARCH.md`).
4. Clean up / hand-paint residual zones, then hand the rig to the animation lane.
5. If Blender export complains: remove the `glTF_not_exported` node
   (documented upstream troubleshooting).

## Predecessor note

UniRig (MIT, https://github.com/VAST-AI-Research/UniRig) is the predecessor:
two-stage (skeleton → skinning) with separate scripts. TokenRig supersedes it
for our purposes. If TokenRig's single-pass weights underperform on a given
mesh, fall back to UniRig's two-stage pipeline as the documented alternative.
