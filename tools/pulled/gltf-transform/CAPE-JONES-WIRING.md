# gltf-transform — Cape Jones wiring

**What:** glTF-Transform v4.5.1 (donmccurdy/glTF-Transform) — the industry-standard
glTF 2.0 SDK + CLI for JavaScript/TypeScript: `inspect`, `validate`, `copy`,
`optimize`, `dedup`, `prune`, `merge`, `partition`, plus Draco/meshopt/WebP
compression and a scriptable transform API. MIT license.

Pulled 2026-10-20 by the overnight idle pipeline (full source tree vendored at
`tools/pulled/gltf-transform/`, 16MB — code only, no built artifacts).

**Why here:** every Tripo pull lands as a GLB and the pipeline had no pinned,
repo-local glTF tooling — lanes were reaching for `npx gltf-transform` ad-hoc
(unpinned version, needs network + disk for the npm cache). This pins v4.5.1 in
the repo as the canonical GLB gate: validate every pulled model, inspect
vertex/draw-call budgets before wiring into the roster, optimize (dedup/prune/
meshopt) before shipping to the game.

**Verified this lane (2026-10-20, functional — pinned version):**
- `LICENSE.md` in-tree = MIT; repo metadata confirms MIT. License gate PASSED.
- `@gltf-transform/cli@4.5.1` (exact vendored version) `--version` → `4.5.1`;
  `--help` lists inspect/validate/copy/optimize/dedup/prune/merge/partition.
- `inspect` on a real pipeline asset
  (`tripo-recovery/kronos_attire1_default.glb/muscular_warrior_3d_model.glb`,
  19MB): parsed clean — glTF 2.0, gltfpack-generated, KHR_mesh_quantization +
  EXT_meshopt_compression, 5,873,772 render verts / 1,000,377 upload verts.
- `validate` on the same asset: **0 errors**, 1 warning
  (MESH_PRIMITIVE_GENERATED_TANGENT_SPACE — runtime tangent generation may be
  non-portable), 1 info (EXT_meshopt_compression not validator-supported).
- Duplicate check: `pygltflib` was only *evaluated* (rig-tools-new, 2026-10-08),
  never vendored — this is the first pinned glTF tool in the repo. No overlap.

**License:** MIT — commercial use allowed.

## Setup

```bash
# Option A — published CLI, pinned to the vendored version (recommended for lanes):
npm install -g @gltf-transform/cli@4.5.1
gltf-transform --help

# Option B — build from the vendored source:
cd tools/pulled/gltf-transform
npm install        # NOT committed to the repo
npm run build
node packages/cli/bin/cli.js --help
```

## Common lane commands

```bash
# Gate every Tripo pull before wiring:
gltf-transform validate model.glb
gltf-transform inspect model.glb          # vertex/draw-call budget

# Shrink for the game build:
gltf-transform optimize in.glb out.glb --compress meshopt --texture-compress webp
gltf-transform dedup in.glb out.glb      # drop duplicated accessors/textures
gltf-transform prune in.glb out.glb      # strip unreferenced properties
```

## Contents

| Path | What |
|---|---|
| `packages/cli/` | CLI (`gltf-transform`) |
| `packages/core/` | Document/Scene-graph SDK |
| `packages/functions/` | Transform functions (optimize, dedup, prune, …) |
| `packages/extensions/` | KHR/EXT extension support |
| `LICENSE.md` | MIT license |

## Limits

- CLI runs on Node 20+; heavy `optimize` passes are CPU-bound — big Tripo
  models (5M+ verts) may want the Kaggle lane instead of this VM.
- Draco compression needs `@gltf-transform/extensions` + draco3d at runtime
  (not vendored); meshopt path is dependency-light and preferred here.
- Model weights/binaries policy: the vendored tree is code only; never commit
  `node_modules/` or built `dist/` output.
