# Meshroom — Cape Jones Wiring

**Source:** https://github.com/alicevision/Meshroom @ 7c6f5c5 (`develop`, shallow, 2026-10-18)
**License:** MPL-2.0 — own-eyes verified in `LICENSE-MPL2.md` / `COPYING.md`.
Free AND commercial-safe (MPL-2.0 is file-level copyleft: commercial use
permitted, larger works can stay proprietary).
**Pulled:** 2026-10-18 via overnight-idle-pipeline (code + scripts only, no binaries).
**Role:** the AUTO-SCANNING axis — the node-pipeline UX on top of the
AliceVision engine (see `../alicevision/`): digitize real props, costumes,
maquettes, and set reference into textured meshes for the show pipeline.

## What it is

Python + Qt node-graph application. Each node wraps an AliceVision binary
(`aliceVision_*`); graphs (`.mg` files) chain them into full
photogrammetry pipelines (camera tracking, photogrammetry, HDR, etc.).
8.5MB code-only pull: `meshroom/` (app), `bin/`, `localfarm/`, `docker/`,
`tests/`, doc sources (branding logos stripped).

## Cape Jones use

- Same targets as COLMAP (`../colmap/CAPE-JONES-WIRING.md`): suit greebles,
  fabric drape reference for the Wiggle-2 cape sim, living-room prop
  reconstruction, teardown-reference meshes.
- Prefer Meshroom over COLMAP when a repeatable node graph matters:
  save the `.mg` once, re-run headless on new photo sets via
  `meshroom_batch`.
- AliceVision's own `.mg` graph templates live in
  `../alicevision/meshroom/` (cameraTracking, photogrammetry, HDR stacks).

## Build / run path (GPU lane — Kaggle or Colab)

Meshroom itself is Python; the heavy lifting is the AliceVision binaries
(see `../alicevision/CAPE-JONES-WIRING.md` — build those on CUDA first),
then:

```bash
pip install -r requirements.txt
python bin/meshroom_batch --pipeline ../alicevision/meshroom/photogrammetry.mg \
    --input /path/to/photos --output /path/to/out
# GUI path (same machine, needs Qt + display): python bin/meshroom_photogrammetry
```

Do NOT build/run the dense pipeline on this VM (2 CPUs, no GPU).

## Notes

- `MESHROOM-UPSTREAM-AGENTS.md` / `MESHROOM-UPSTREAM-CLAUDE.md` are
  upstream's own agent guides (renamed from `AGENTS.md` / `CLAUDE.md` so
  they are never confused with repo law files).
- `docs/logo/` (upstream branding images) was pruned at pull time;
  technical doc sources in `docs/source/` kept.
- Nodes call out to AliceVision binaries at runtime — this repo vendors the
  pipeline code; binaries come from the GPU-lane build of `../alicevision/`.
