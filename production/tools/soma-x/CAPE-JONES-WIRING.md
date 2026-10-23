# SOMA-X — Cape Jones Wiring

**Upstream:** https://github.com/NVlabs/SOMA-X (`NVlabs/SOMA-X`, branch `main`, commit 56a3d957a549c66425b500fddf7f3183bc6fbdff — the v0.3.4 release)
**License:** Apache-2.0 (in-tree `LICENSE` own-eyes verified; GitHub SPDX badge `Apache-2.0`; README badge). Free AND commercial-safe.
**Pulled:** 2026-10-18 (overnight idle pipeline), code + scripts + docs only — no model assets.
**Cape Jones path:** `production/tools/soma-x/`
**Paper:** [SOMA: Unifying Parametric Human Body Models](https://arxiv.org/abs/2603.16858) (Jun Saito et al., NVIDIA)

## What it is

SOMA-X is NVIDIA's canonical, **differentiable** representation for parametric
human bodies and hands. It maps supported identity models to a shared SOMA
topology and rig convention so one animation/retargeting/geometry pipeline
works across model families. The headline for us: it unifies **5 backends**
(SOMA-Shape, MHR, SMPL-X, Anny, GarmentMeasurements) under **one 77-joint
skeleton + a single MLP pose-correctives model** — the best corrective tech in
the PARAMETRIC-BODY.md landscape, and the direct reference our
PSD-as-driven-shape-keys porting plan (§5.1) wants to study.

- **`SOMALayer`** — full-body model at mid / low / extra-low LODs (77 pose joints, shape components)
- **`SOMAHandLayer`** — wrist-local left/right hands at the same three LODs (25 pose joints, 20-component native hand identity)
- **Backends:** MHR (default high-fidelity body), SOMA native (PCA identity + body-part scaling), Anny (anthropometric, broad age coverage), SMPL/SMPL-H/SMPL-X (user-supplied licensed files — NOT redistributed), GarmentMeasurements (user-generated local PCA), MANO v1.2 (user-supplied)
- **NVIDIA Warp**-accelerated runtime skinning + fitting (GPU lane)
- **Pose inversion** (`soma/fitting/pose_inversion.py`, `pose_inversion_mhr.py`) — fit the model to observed poses
- **Procedural rig controls** (`soma/procedural_transforms.py`, `soma/reference_poses.py`, Maya reference under `tools/soma_procedural_maya/`)
- **I/O:** USD/NPZ (`soma/io.py`), batched skinning (`soma/geometry/batched_skinning.py`), skeleton transfer (`soma/geometry/skeleton_transfer.py`)
- **Tools:** `tools/mhr2soma.py`, `tools/pose_converter.py`, `tools/vis_pyrender.py`, `tools/hand/soma2mano.py`, shared animation-loading API (v0.3.4)
- v0.3.4 changelog: corrective model improved **around armpits and elbows** (our exact defect zones — fingertip/elbow/jaw fix lane), example animation shipped in USD

## Cape Jones use

1. **Corrective-model reference (primary).** The single MLP pose-correctives
   model is the scan-learned corrective library PARAMETRIC-BODY.md §5.1 wants
   as the reference port target (driven shape keys). v0.3.4 specifically
   improves armpit/elbow correctives — compare against MPFB's hand-authored
   targets and MHR's per-joint MLP correctives (already pulled in
   `production/tools/mhr/`).
2. **Backend-agnostic retargeting.** Map Simple Retarget Tool / mocap output
   onto SOMA's 77-joint skeleton once, then drive MHR / SOMA / Anny backends —
   one retarget, many bodies. Pair with
   [SOMA Retargeter](https://github.com/NVIDIA/soma-retargeter)
   (SOMA→Humanoid) for game-engine export.
3. **Pose inversion for fitting.** Fit SOMA pose+shape to our character scans /
   Tripo meshes as an anatomical prior before binding our own rigs.
4. **Hand lane.** `SOMAHandLayer` + MANO interop gives the face/hand lane a
   second reference alongside the pulled hand work.
5. **Related pulls to consider:** GEM-X (SOMA-based video pose estimation),
   Kimodo (controllable text-to-motion), BONES-SEED (motion dataset already in
   SOMA format) — all named in the upstream README; evaluate separately.

## GPU-lane build path (Kaggle / Colab)

SOMA-X is a **GPU-lane tool** — PyTorch + CUDA + NVIDIA Warp:

```bash
# On the GPU lane (Kaggle/Colab):
pip install py-soma-x          # or: pip install -e .  (this checkout)
# Assets download from Hugging Face nvidia/SOMA-X on FIRST USE
# (huggingface_hub cache) — GPU-side only, never committed.
python -c "
import torch
from soma import SOMALayer
body = SOMALayer(identity_model_type='mhr', device='cuda')
out = body(torch.zeros(1,77,3), torch.zeros(1, body.num_shape_components))
print(out.vertices.shape, out.joints.shape)
"
```

- **Model assets are NOT in this repo** (law: weights stay off local disk).
  The `assets/` dir here holds only Git-LFS **pointer files** (130-byte text) —
  they document provenance; the real `.npz`/`.pt`/`.usd` assets download from
  `https://huggingface.co/nvidia/SOMA-X` at runtime on the GPU lane.
- SMPL-X / MANO backends need user-licensed model files — never committed.
- CPU smoke test: `SOMALayer(..., device='cpu')` works (slow; correctness only).

## What's here vs upstream

- Kept: `soma/` (Python package, 124 files), `tools/`, `tests/`, `docs/`,
  `assets/` (LFS pointers only), `LICENSE`, `README.md`, `CHANGELOG.md`,
  `RELEASE.md`, `ATTRIBUTIONS.MD`, `pyproject.toml`, `requirements.txt`,
  `setup.py`, `Dockerfile`
- Dropped: `.git` (not a submodule), `__pycache__` (none shipped)
- No weights, no model binaries, no demo media binaries — largest file 90KB
  (`soma/fitting/pose_inversion.py`); total 2.3MB
- All 124 `.py` files pass `python3 -m py_compile`

## Lane comparison (corrective tech)

| Tool | Corrective approach | Cape Jones path |
|------|---------------------|-----------------|
| SOMA-X (this) | **Single MLP** pose correctives, unified 77-joint skeleton, Warp-accelerated | `production/tools/soma-x/` |
| MHR | MLP per joint, geodesic-sparsity masked (ATLAS heritage) | `production/tools/mhr/` |
| MPFB2 | Hand-authored corrective targets | `production/tools/mpfb2/` |
| W5r (ours) | Surface-heat-diffuse skinning (bakeoff winner) | bakeoff lane |

Study order for the §5.1 port: SOMA-X (unified single MLP) → MHR (per-joint
MLP) → MPFB (authored) — then distill into our driven-shape-key targets.
