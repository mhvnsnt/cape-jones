# AliceVision — Cape Jones Wiring

**Source:** https://github.com/alicevision/AliceVision @ 3afba20 (`develop`, shallow, 2026-10-18)
**License:** MPL-2.0 — own-eyes verified in `LICENSE-MPL2.md` / `COPYING.md`;
libmv-derived code under MIT (`LICENSE-MIT-libmv.md`). Free AND
commercial-safe (file-level copyleft; commercial use permitted).
**Pulled:** 2026-10-18 via overnight-idle-pipeline (code + scripts only, no binaries).
**Role:** the AUTO-SCANNING axis — the C++ SfM/MVS **engine** underneath
Meshroom (`../meshroom/`): the binaries that turn photo sets into dense
textured meshes.

## What it is

Production-grade photogrammetry framework (Mikros Image / VFX lineage):
`src/aliceVision/` modules (feature extraction, SfM, MVS, meshing,
texturing, HDR), each exposed as an `aliceVision_*` CLI binary; `meshroom/`
holds the `.mg` node-graph templates that chain them; `pyTests/` has the
Python test suite. 79MB code-only pull — no binaries, no model weights
(classical CV + CUDA kernels, no ML weight files to fetch).

## Cape Jones use

- Build once on a GPU lane → `aliceVision_*` binaries → Meshroom nodes
  (`../meshroom/`) or direct CLI for prop/costume/maquette digitization.
- `.mg` templates in `meshroom/` cover: photogrammetry, camera tracking
  (incl. depth/lidar variants), HDR imaging, distortion/color calibration.
- Output meshes feed the show pipeline: set dressing, teardown reference,
  base meshes for character pieces.

## Build / run path (GPU lane — Kaggle or Colab)

Dense MVS wants CUDA. Do NOT build on this VM (2 CPUs, no GPU). One-time
build on a GPU machine:

```bash
# deps via vcpkg (see vcpkg.json) or system packages: Eigen, Boost,
# OpenImageIO, Alembic, OpenCV, Ceres, CUDA toolkit
cmake -B build -DCMAKE_BUILD_TYPE=Release \
  -DALICEVISION_BUILD_MESHROOM=OFF
cmake --build build -j"$(nproc)"
# binaries land in build/.../bin as aliceVision_*
```

Then point Meshroom at them, or call directly:

```bash
aliceVision_cameraInit --imageFolder /path/to/photos --sensorDb ... --output sfm.json
# ... featureExtraction -> imageMatching -> SfM -> MVS -> meshing -> texturing
```

## Notes

- The `.spi3d` LUT files under `src/aliceVision/image/share/` are upstream
  color-science data assets shipped with the source (not model weights);
  required at runtime, kept deliberately.
- `docs/doxygen/` kept (API doc sources); upstream `docs/img/` technical
  figures kept (small, referenced by docs).
- Third-party code notes live in the upstream LICENSE files; fetched
  dependencies are declared in `vcpkg.json`.
