# COLMAP — Cape Jones Wiring

**Source:** https://github.com/colmap/colmap @ f202e4e (shallow, 2026-10-18)
**License:** new BSD (BSD-3-Clause) — own-eyes verified in `LICENSE`
(Copyright 2016 ETH Zurich and UNC Chapel Hill; 2016–2026 The COLMAP Contributors).
Free AND commercial-safe.
**Pulled:** 2026-10-18 via overnight-idle-pipeline (code + scripts only, no binaries).
**Role:** the AUTO-SCANNING axis — digitize real props, costumes, maquettes, and
set reference into textured meshes for the show pipeline.

## What it is

General-purpose Structure-from-Motion (SfM) + Multi-View Stereo (MVS)
photogrammetry pipeline. One C++17 binary (`colmap`) with many subcommands,
a Qt GUI, and Python bindings (`pycolmap`, in `python/` + `src/pycolmap/`).
12k+ stars, industry-standard, actively maintained.

## Cape Jones use

- Photograph a physical prop / costume piece / maquette from many angles.
- Run SfM + dense MVS to get a textured mesh (OBJ/PLY out).
- Feed the mesh into the show pipeline: teardown-reference, set dressing,
  or a base for character pieces (Cape Jones suit parts, BlenRig targets).
- Typical targets: Cape Jones suit greebles, real-world fabric drape
  reference for the Wiggle-2 cape sim, living-room prop reconstruction.

## Build / run path (GPU lane — Kaggle or Colab)

COLMAP dense reconstruction wants CUDA. Do NOT build on this VM (2 CPUs,
no GPU). Build once on a GPU machine and cache the artifact:

```bash
# deps: Eigen, Ceres, Boost, Qt (GUI optional), CUDA toolkit
cmake -B build -DCMAKE_BUILD_TYPE=Release -DGUI_ENABLED=OFF
cmake --build build -j"$(nproc)"
# or use the prebuilt Docker image in docker/
```

Python path: `pip install pycolmap` (or `pycolmap-cuda12` for CUDA wheels)
and script against it from the lane's existing `ml-autorig/` notebooks.

## Minimal CLI flow (photo set → textured mesh)

```bash
colmap automatic_reconstructor \
  --workspace_path /path/to/workspace \
  --image_path /path/to/photos \
  --dense 1
# output: workspace/dense/fused.ply (point cloud), meshed-poisson.ply (mesh)
```

## Notes

- `COLMAP-UPSTREAM-AGENTS.md` is COLMAP's own agent guide (renamed from the
  upstream `AGENTS.md` so it is never confused with repo law files).
- Bundled third-party code lives in `src/thirdparty/` (VLFeat, SiftGPU,
  PoissonRecon, LSD); fetched deps (PoseLib, faiss, ONNX Runtime) are listed
  in `vcpkg.json` — license note in the COLMAP LICENSE applies.
- No weights to download: COLMAP is classical CV, no ML model files.
- Docs-only extras: upstream `doc/` kept (1.9M).
