# SITTING SAGA — where the finished chair work lives (2026-10-23)

The work that got Cape Jones sitting in the chair is DONE and stored. The
scene files are too big for the git tree (165MB to 833MB each), so they live
on this repo's GitHub Releases. This doc is the index that ties them
together. If a scene is not listed here, it is not the canonical one.

## The canonical chain

Each step builds on the one before it. Start from the final and work back
only if you need an earlier stage.

| Step | Scene | Release | Main asset | Size |
|---|---|---|---|---|
| 1. Placed (canon) | `scene_anim_placed3.blend` | `sitcanon-anim-placed-20261020` | `scene_anim_placed3.blend` | 172,551,169 B |
| 2. Recliner mechanism | `scene_recliner_mech.blend` | `recliner-mech-20261023` | `scene_recliner_mech.blend` | 164,790,998 B |
| 3. Cape cloth bake | `scene_capebaked.blend` | `cape-bake-20261023` | `scene_capebaked.blend` | 828,433,505 B |
| 4. FINAL still scene | `scene_final.blend` | `sitting-final-20261023` | `scene_final.blend` | 832,635,494 B |

Intermediates (stage A/B splits, weld stages, bake scenes) are on release
`sitting-saga-intermediates-20261023` (7 .blend files). Older sitting takes
(Oct 19 worktrees) are on releases `sitting-wt-sitcanon-20261019`,
`sitting-wt-autoseat-20261019`, `sitting-wt-mocapsit-20261019`.

## Pull any scene back

```bash
gh release download sitting-final-20261023 -R mhvnsnt/cape-jones -p "scene_final.blend"
gh release download recliner-mech-20261023 -R mhvnsnt/cape-jones -p "scene_recliner_mech.blend"
gh release download cape-bake-20261023 -R mhvnsnt/cape-jones -p "scene_capebaked.blend"
gh release download sitcanon-anim-placed-20261020 -R mhvnsnt/cape-jones -p "scene_anim_placed3.blend"
```

## Proof renders (on the same releases)

- Final: `FINAL_front_f40_v1.png` + `MERGE_check_f40_v1.png` on
  `sitting-final-20261023`. The final front render was strip-rendered and
  feather-composited because hard-cut seams showed at full res.
- Recliner: `mech_r0_v1.png`, `mech_r50_v1.png`, `mech_r100_v1.png` on
  `recliner-mech-20261023`.
- Cape bake: `capebake_front_f40_v1.png` + `capebake_closeup_f40_v1.png` on
  `cape-bake-20261023`.

## Canon values (do not re-derive)

- Sitting placement: px = -0.135, py = -0.315, ry = -64. He sits ON the
  chair, facing the TV/table direction, not the camera.
- Living room Position 1 is the default: TV and shelf backs against the
  wall. Position 2 (TV and shelf facing the chair) is a saved alternate.
- The TV plays where the camera/audience can see it. He sits off to the
  side not really watching. That is the gag. Do not "fix" it.

## Recliner mechanism

One driver runs the whole mechanism: `recliner_rig["recline"]`, 0 to 1.

- Backrest rotates -26 degrees, shank -50 degrees, foot pad counter-rotates
  to stay level.
- Measured at frame 40: pad to shin gap 0.4 to 1.7 mm at every step from 0
  to 1. Contact, never intersection.
- Foot lift at full recline: +137 mm / +134 mm.
- GOTCHA: headless Blender 4.0.2 drivers go stale. Call
  `update_tag(refresh={'DATA'})` before `view_layer.update()` or the rig
  renders in its old pose.

## Cape bake

- 81 frames baked into `scene_capebaked.blend`, `is_baked=True`, zero
  out-of-bounds verts across all frames.
- Bake v1 failed. The v2 weld fix landed it. The cape drapes off the
  shoulders, bunches behind him on the chair, and pools at his hip and
  beside the chair.
- `scene_final.blend` = the recliner-mech scene with the baked cape merged
  in. The cape was split from the body positionally (282,518 verts) and the
  baked `CapeJones_Cape` appended with its cache intact. Frame-40 cape
  bounds are identical before and after the merge. Recline = 0 in the
  final still. Action and placement untouched.

## Mesh-repair pipeline (PR #167, merged 2026-10-23)

The seam-averaging and repair pipeline that made placed3 trustworthy is on
main: `average_seams.py` (exact-coincidence 1e-5 grid clustering) and
`verify_repair.py` with the weight-plausibility audit gate. End-to-end
`run_pipeline.py` on placed3 reproduces the canonical numbers: 30,077
clusters (max 4), 6,369 audit-flagged verts (0.007), p99 separation 0.004,
`repaired_ok=true`.

## Build scripts

The scripts that built stages 2 to 4 (recliner stages, cape bake, final
merge, compositing, diagnostics) are in this repo at
`production/sitting-saga-20261023/scripts/`. They ran locally in
`~/workspace/sitcanon-work/` and `~/workspace/capebake-work/` and were
landed here 2026-10-23 so the work is reproducible from the repo alone.

## Rules that came out of this saga

- NO-SPARSE-COMMIT LAW: never commit or push from a sparse or partial
  checkout without verifying the working tree against the branch's real
  tree. (A sparse-checkout commit wiped this repo's main on 2026-10-23.
  Recovered same day, PR #220. The law is in AGENTS.md.)
- Big scene files go on Releases, never in the git tree, and every release
  gets an index entry in the repo the day it ships. A deliverable with no
  trace on main does not count as delivered.
