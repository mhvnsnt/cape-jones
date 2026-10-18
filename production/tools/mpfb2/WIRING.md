# MPFB2 — Pull + Wiring (Cape Jones)

**Pulled:** 2026-10-17 · `makehumancommunity/mpfb2`, commit `3af0cd5`, v2.0.18
**License:** code **GPL-3.0-or-later** (`LICENSE.CODE.md`), assets/data **CC0-1.0**
(`LICENSE.ASSETS.md`). Owner's rule on licenses: Quaternius-style approval is his
call — GPL-3.0 code is already precedented in this repo (AnimeEffects, BlenRig 6).
**Requires:** Blender 4.2+ (we run 4.5.3 LTS at `~/workspace/tools/blender-4.5/`).

## What was pulled (complete)

The full upstream tree: `src/mpfb/` (addon), `docs/`, `script_samples/`,
`test/`. No files removed. Key contents:
- `src/mpfb/data/3dobjs/base.obj` — 19,158-vert base human (CC0)
- `src/mpfb/data/targets/` — full morph-target library (bulk/height/shoulders/
  belly/limbs + face + all body parts + expressions)
- `src/mpfb/data/rigs/standard/` — `default` (163 bones), `mixamo` (52),
  `game_engine`, `cmu_mb`, `openpose` + precomputed `weights.*.json` (auto-skinning)
- `src/mpfb/services/animationservice.py` — BVH import, `make_cyclic`, Mixamo ops
- `src/mpfb/ui/operations/animops/operators/mapmixamo.py` — Mixamo bone mapper

## What was wired

**`3d-assets/cape-jones-rig/cape_jones_mpfb_wired.blend`** (built from
`cape_jones_rigged_w5r_clean.blend`, source untouched):
1. **5 semantic morphs driving the real CJ mesh** — MPFB target deltas
   transferred via KD-tree nearest-surface mapping onto `CapeJones_Body`
   (910,374 verts) as shape keys `MPFB_bulk`, `MPFB_height`, `MPFB_shoulders`,
   `MPFB_belly`, `MPFB_limbs`, each driven by a custom property
   (`mpfb_bulk` …) with a SINGLE_PROP driver. 0.0 = neutral, 1.0 = full morph.
   Morph definitions: bulk = macro weight+muscle + pectoral/waist targets;
   height = macro height; shoulders = shoulder-dist; belly = navel-out +
   waist-circ; limbs = limb length/scale targets (both sides).
2. **`MPFB_FullSkeleton`** — the 163-bone default rig (spine01–05, neck01–03,
   segmented twist limbs, full fingers/toes) scaled to CJ's 0.925 m, T-posed,
   in-scene as the full-skeleton reference base.
3. `MPFB_ReferenceBody` — the neutral MPFB human (scaled) for proportions.

## Scripts (all headless, zero hand-tooling)

- `mpfb_proof.py` — create human, apply morphs, add 163-bone rig, render.
  Run: `blender-4.5 -b --python mpfb_proof.py`
- `mpfb_wire_cj.py` — the transfer pipeline (morphs → CJ shape keys + drivers,
  skeleton import, save wired blend).
  Run: `blender-4.5 -b cape_jones_rigged_w5r_clean.blend --python mpfb_wire_cj.py`
- `mpfb_anim_proof.py` — visual proofs on the wired blend (morph sweep,
  skeleton X-ray, scripted knee/elbow/spine poses with auto sign-check,
  Mixamo-rig generation check).
  Run: `blender-4.5 -b cape_jones_mpfb_wired.blend --python mpfb_anim_proof.py`

Headless notes: MPFB2 is a Blender extension; headless use imports it from
`src/` with two mocks (`bpy.utils.extension_path_user`,
`mpfb.get_preference`) — no upstream files modified. Run under `xvfb-run -a`.

## Proof renders

`3d-assets/cape-jones-rig/mpfb_proofs/`:
- `A1_morph_bulk_shoulders.png`, `A2_morph_belly_height_limbs.png`
- `B_full_skeleton_163.png`
- `C1_deep_knee_bend.png`, `C2_elbow_90.png`, `C3_spine_twist_bend.png`

## For the rig/deformation lanes

- Port list: `docs/research/PARAMETRIC-BODY.md` §5 (PSD correctives, limb
  segmentation, 5-segment spine, anatomical joints, auto-skinning).
- The `weights.default.json` in `src/mpfb/data/rigs/standard/` is the free
  reference for twist-bone weight ramps.
- Mixamo path: generate the `mixamo` rig (`HumanService.add_builtin_rig(h, "mixamo")`),
  then `mapmixamo` — real Mixamo FBX files need an Adobe account (browser lane).
