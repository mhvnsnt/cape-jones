# MHR — Cape Jones Wiring

**Upstream:** https://github.com/facebookresearch/MHR (`facebookresearch/MHR`, branch `main`, commit d96fafa33bbf018647c70c3525e91f53e79d2a14)
**License:** Apache-2.0 (in-tree `LICENSE` own-eyes verified; GitHub SPDX badge `Apache-2.0`). Free AND commercial-safe.
**Pulled:** 2026-10-18 (overnight idle pipeline), code + scripts + docs only — no model assets.
**Cape Jones path:** `production/tools/mhr/`

## What it is

MHR (Momentum Human Rig) is Meta's parametric 3D human body model — the
"different org's GNM" named in `docs/research/PARAMETRIC-BODY.md`. It builds on
the ATLAS (Meta + CMU, ICCV 2025) paradigm and adds artist-friendly rigging:

- **18,439 verts, 127 joints, 7 LODs** (LOD 0–6)
- **45 identity / 204 pose / 72 FACS expression parameters** (decoupled skeleton + shape)
- **Sparse non-linear pose correctives** — MLP per joint, geodesic-sparsity masked (no long-range bleed). This is the exact technology our deformation lane wants: elbow/knee collapse fixes learned from scans, not hand-authored.
- **Dual solver:** GPU (PyTorch, differentiable) and CPU (PyMomentum)
- **SAM 3D Body perception** integration (Meta)
- Tools: `mhr_visualization` (Colab notebook), `mhr_smpl_conversion` (MHR↔SMPL/SMPL-X), `mhr_LOD_conversion`, `mhr_create_segmentation`

## Cape Jones use

1. **Deformation reference (primary).** MHR's `corrective_blendshapes_lodN.npz`
   (per LOD, ships with the model assets) is the *learned* corrective library our
   PSD-as-driven-shape-keys porting plan (PARAMETRIC-BODY.md §5.1) wants as
   reference. Compare against MPFB's hand-authored corrective targets — MHR shows
   what scan-learned MLP correctives look like for the same joints (elbow, knee,
   shoulder, hip).
2. **Anatomical joint placement (§5.4).** MHR's decoupled skeleton (77-joint
   ATLAS heritage, 127 in the rig) is a second anatomical reference alongside
   MPFB's skeleton for re-deriving our joint centers.
3. **Pose prior / fitting.** 45-identity + 204-pose parameterization is a strong
   generative prior for retargeting mocap (Simple Retarget Tool output) onto
   Cape Jones proportions.
4. **SMPL-X bridge.** `tools/mhr_smpl_conversion/` converts MHR↔SMPL/SMPL-X —
   lets us ingest SMPL-X mocap datasets into the MHR/MHR-Rigify workflow without
   touching MPI's registration-walled model files.

## GPU-lane build path (Kaggle / Colab)

MHR is a **GPU-lane tool** — PyTorch + CUDA for inference and training:

```bash
# On the GPU lane (Kaggle/Colab):
pip install mhr pymomentum-gpu torch   # or: pixi install  (recommended upstream)
mhr-download-assets                     # pulls assets.zip from the MHR GitHub release
python demo.py                           # generates test mesh, compares vs TorchScript
```

- **Model assets are NOT in this repo** (law: weights stay off local disk).
  Download on the GPU lane with `mhr-download-assets`
  (source: `https://github.com/facebookresearch/MHR/releases/latest/download/assets.zip`,
  see `mhr/download_assets.py` for the exact mechanism).
- TorchScript-only shortcut: `pip install mhr` + `mhr-download-assets --member
  assets/mhr_model.pt` — LOD 1 only, no codebase needed.
- Interactive: `tools/mhr_visualization/` has a Colab notebook.

## What's here vs upstream

- Kept: `mhr/` (Python package), `demo.py`, `docs/`, `scripts/`,
  `tests/`, `tools/`, `pyproject.toml`, `pixi.lock`, `README.md`, `LICENSE`,
  `images/`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`
- Stripped: `.github/` (CI/workflows not needed in-repo)
- No AGENTS.md/CLAUDE.md/MUSE.md upstream files existed — nothing renamed
- All Python files pass `py_compile`; no binaries >2MB; no weights (assets are
  runtime-downloaded, see above)

## Notes

- PyTorch >= 3.11, `pymomentum >= 0.1.90` required at runtime (pip: `pymomentum-cpu`
  / `pymomentum-gpu`; pip install is upstream-marked experimental — prefer Pixi).
- `trimesh >= 4.8.3` needed only for the conversion/segmentation tools.
- This pull closes the PARAMETRIC-BODY.md "Pull-ready (not yet local — disk)" row
  for MHR (was blocked on the 85% disk gate; pulled at 68%).
