# GNM — Provenance & Pull Notes

**Upstream:** https://github.com/google/GNM (Google LLC)
**Pulled:** 2026-10-17 (lane: gnm-head, subagent 66ff6258) via shallow clone of `main`
at commit `5cf11d785a38a83597e64ad0b6d15950bcd6b390`.
**License:** Apache License 2.0 (`LICENSE` in this folder) — commercial use OK.
Per the license we retain the copyright notice and state our changes in this file.

## What was pulled

The GNM Python package source (`gnm/shape/`): the NumPy/JAX/PyTorch/TensorFlow
parametric head-model implementations, data loaders, semantic sampler code,
fitting utils, and visualization helpers. 73 files, 788K — **code and docs only.**

## What was deliberately NOT pulled (stripped)

- `gnm/shape/data/semantic_sampler/*.h5` — pre-trained CVAE decoder weights.
- `gnm/shape/data/textures/edgeflow_bw_4k.png` — model texture.
- `gnm/shape/assets/readme/*.gif` — demo media.
- Model *weights* (the actual PCA bases / template mesh): these are NOT in the git
  repo at all. `gnm_data_loader.py` downloads them on first use from Hugging Face
  Hub / Kaggle Models into `~/.cache/gnm/models/`. We did not download them —
  no disk hoarding, and our cartoon face can't consume scan-learned bases anyway.

## Why it is here

Study reference for the GNM-style parametric face rig in
`3d-assets/face-rig/cj_parametric_face.py` (our own original code). The technique
studied: template mesh + linear identity/expression blendshape bases +
4-joint LBS (eyes/neck/head) + semantic expression sampling. See
`docs/research/GNM-HEAD.md` for the full study.

## Related, NOT pulled (documented per license rules)

- **Nathan Dickson — "GNM Head Importer" for Blender** (free download, Blender 5.1+):
  https://nathandickson365.gumroad.com/l/GNMImporter
  License is unstated on the product page (all rights reserved implied) and it
  requires a Gumroad checkout. Not vendored. Concept studied from public
  coverage (slider-driven GNM params in the Blender viewport); we built our own
  parametric UI instead (`3d-assets/face-rig/`).
