# Cape Jones guard stance — ARM FIX v2 (2026-11-10, owner pt98u)

## Root cause of the "H" arms (measured, not guessed)
The rig, not the retarget math, caused it. In `3d-assets/cape-jones-rig/cape_jones_rigged_w5r_clean.blend`
(sha256 c7b578fc…ced5) the arm bone chain sits **one joint too far out** along the T-pose arm:

| rig joint (bone) | rig x | what is on the mesh at that x |
|---|---|---|
| clavicle tail / upperarm head ("shoulder") | 0.243 | the **elbow crease** |
| upperarm tail / forearm head ("elbow") | 0.376 | the **wrist** (end of the banded gauntlet) |
| forearm tail / hand head ("wrist") | 0.484 | the **fingertips** |
| (real shoulder joint, under the deltoid) | ~0.13 | no bone there |

The skin weights follow those bones (evidence/rootcause-arm-weights-vs-rig-joints.png). So `clavicle_L/R`
carries the whole deltoid and bicep. The source clavicle barely moves, so shoulder-to-bicep stays sideways like a T-pose.
"upperarm" swings the gauntlet and "forearm" swings the hand, so the rest of the arm hangs down. That is the H.
The v1 gate numbers prove the skin is the problem: the target **bone** direction matched the source, but the **mesh** upper arm was 69–74° off (median), with a lateral component of 0.99 (fully sideways).

## Fix (non-destructive; original blend untouched)
`tools/build_rig_v2.py` writes a NEW blend (`rig_v2_arms.blend`, sha256 5ed1ff8b…5bd3, stays on the box at
/workspace/cj3d/v2, ~95 MB, not committed). It does two things:
- Moves the deform, FK and IK arm bones (both sides) to the mesh's own joints: shoulder x=0.130, elbow 0.243, wrist 0.376, hand tip 0.440. The elbow poles move with them.
- Redistributes each vertex's existing TOTAL arm weight (clavicle+upperarm+forearm+hand) along the arm axis, using smooth blends at the joints. The clavicle→upperarm blend applies only near the arm axis, so the torso side stays on the clavicle. Per-vertex totals are preserved (max error 0.001), so the bind/rest shape is unchanged.
The retarget (`tools/cj_retarget.py`) is the same math as v1, so v1 can be reproduced on the old rig.

## Regression gate: `tests/test_guard_arms.py`
Run as `blender -b RIG.blend --python test_guard_arms.py -- stance.glb out.json`. It exits 1 on fail.
It measures the upper-arm direction (shoulder→elbow) in CHEST coordinates on 12 sampled guard frames for three things:
- the source skeleton;
- the target bones;
- the **evaluated Cape body mesh**, using landmark rings picked from the rest mesh's anatomy, not from the rig.

| check (per arm) | v1 original rig | v2 fixed rig |
|---|---|---|
| median source-vs-mesh angle ≤30° | L 74.2 / R 69.6 FAIL | L 5.0 / R 5.4 PASS |
| max source-vs-mesh angle ≤45° | 86.3 / 82.4 FAIL | 7.3 / 9.0 PASS |
| median mesh lateral component ≤0.6 (1.0 = T-pose sideways) | 0.999 / 0.990 FAIL | 0.18 / 0.18 PASS |
| bone-vs-mesh median ≤15° (skin follows bone) | 74.2 / 69.6 FAIL | 5.0 / 5.4 PASS |
| shoulder actually moves: mesh range ≥ max(3°, 0.5×source range) | 9.1° vs 62.8° FAIL | 64.9° vs 62.8° PASS |
The failing fixture (v1) exits 1 and the fixed rig exits 0. Both JSONs are in tests/.

## Honesty
- Motion is a STAND-IN: the Cyborg X FIGHT stance (CMU 13_17 boxing) from `fight/guard_stance/stance.glb` (sha256 19ee11b6…5049). It is NOT decoded Alisa T7 motion, and no Alisa attacks are used. The thighs are widened by +0.22 in x, as in v1.
- Set: a plain grey floor with a dark backdrop. It is NOT Jungle Outpost.
- CAPE CLOTH: NOT DONE (see below).

## Cape cloth status: built, baked, NOT acceptable yet
The visible cape is about 156 Tripo fragment islands (266k verts) fused into `CapeJones_Body`, plus a static `CapeJones_Cape` panel, so it can't be simulated directly.
`tools/build_cloth.py` builds a standard proxy setup:
- a 1,464-vert cloth proxy fitted to the cape;
- a top band pinned through armature weights transferred from the chest/spine/clavicle;
- a decimated, armature-driven collision body (12,488 verts) with self-collision;
- the hi-res fragments moved onto their own object and driven by Surface Deform, while the body masks them out.
Two full bakes (268 and 288 frames) ran. Both rode up and bunched at the shoulders during the guard
(evidence/cloth-*-FAILED*.png; proxy z-min climbs from 0.06 to about 0.66). A thin-collision test held at rest (stable)
but still rode up once he moved. I have not rendered any cloth into the video.

## UPDATE 2026-11-10 ~1:45 PM CDT: v3 cloth + adoption status (evidence-based)
**Arm-fix adoption**
- Every consumer in this folder now refuses the raw rig. `tools/cj_retarget.py` `prep_target()` stops with `REFUSED` unless the rig carries `cj_arm_fix`, which `build_rig_v2.py` writes. `tools/render_guard.py` checks the same thing.
- Verified: render_pose on the raw rig exits 1 (REFUSED). The arm gate exits 1 on the raw rig and 0 on the fixed rig.
- `tools/guard_shot_pipeline.sh` is the gate-first entry point. Run with `STOP_AFTER_GATE=1` it passed end to end (raw rig FAIL, fixed rig PASS).
- **NOT adopted repo-wide:** the repo blend `3d-assets/cape-jones-rig/cape_jones_rigged_w5r*.blend` is unchanged and still defective. Older scripts elsewhere in the repo that load it directly do not get this guard, and CI does not run Blender. See `3d-assets/cape-jones-rig/W5R-ARM-JOINTS-DEFECT-READ-FIRST.md`. The permanent repo-wide fix is still PENDING. It needs either the fixed blend committed (95 MB, over the 90 MB rule) or the other consumers moved onto this pipeline.

**Cloth v3 (`tools/bake_v3.py` + `tools/capsules.py`)**
- Collision now uses 14 per-bone ellipsoids sized from the body mesh, instead of the decimated fragment shell (that shell is what pushed the cape up and through him).
- Self-collision ON. Friction 0. Time scale 1.
- Grounding: the pelvis is shifted per frame so the lowest sole sits at the floor (z = 0). v1/v2 floated for the whole shot.
- The bake covers 288/288 frames. It hangs full length and swings; see `evidence/cloth-v3-*.png`, `v2-v3/`, `checkframes/v3-*`.

**Penetration (`tools/pen_test.py`, `tests/penetration/*.json`)** = share of cape verts inside the leg ellipsoids, on 8 frames:

| test | old skin-bound cape (median / max) | v3 cloth (median / max) |
|---|---|---|
| inside 0.9× ellipsoid (legs+pelvis+torso) | 0.008% / 0.12% | 0.0% / 0.24% |
| inside 1.15× ellipsoid (legs only) | 0.026% / 0.23% | 0.0% / 0.93% |

v3 is clean on 6 of 8 frames, but WORSE than the old cape on the knee-raise frames 150 and 270 (same source frame).
This metric also did NOT reproduce the reviewer's "heavy" thigh cut-through on v2, so it is too weak to prove a pass.
Status: penetration NOT proven fixed.
Other known v3 defects: the cape reads narrower than the original; small shard artifacts from the fused Tripo fragments; the cloth does not loop.

## UPDATE 2026-11-10 ~2:15 PM CDT: shared guarded loader + consumer migration (coverage INCOMPLETE)
- `tools/cj_arm_guard.py` is the single shared loader. `ensure_arm_fix()` does one of three things:
  - no-op if the rig is already marked fixed;
  - repairs the rig **in memory** if it shows the measured w5r signature (upperarm head |x|≈0.243, forearm head ≈0.376). The file on disk is untouched;
  - **refuses** anything else.
  `build_rig_v2.py` is now a thin wrapper over it. `cj_retarget.prep_target()` auto-repairs through it (`CJ_AUTO_ARM_FIX=1` default; set 0 to refuse instead, verified REFUSED).
- Migrated consumers: see `tests/CONSUMERS.json`. These are `production/dance-proof-3d-v6/fix_breathe.py` and this folder's retarget/render tools.
  `fix_breathe.py` was NOT run end to end: its w5r_idle input was not downloaded (disk rule), so it is unverified whether that blend has the same signature. If it doesn't, the loader now refuses loudly.
- Tests:
  - `tests/test_consumers.py` (static): PASS. The unmigrated `fix_breathe.py` fails it (negative fixture).
  - `tests/test_guard_arms.py` on the raw rig: exit 1.
  - `tests/test_guard_arms.py` with `CJ_PRE_GUARD=1` (cold start through the shared loader): exit 0, with values identical to the saved v2 rig (`tests/consumer-runs/*.json`).
- **Remaining bypasses (NOT migrated):**
  - spine-lane (4 scripts; a rig-construction lane);
  - deform-wave2 audit;
  - cape build/sim lane scripts;
  - 39 `.scratch/lane3` scripts;
  - sitting-rig scripts (excluded by owner rule);
  - `production/tools/**` (3,606 scripts, NOT scanned; the repo tree listing was truncated);
  - any manual or GUI use of the repo blend, which is still the defective file.
  - Also unverified: whether `w5r.blend` / `w5r_idle*.blend` share the same signature.
- => The permanent fix covers the guard/fight pipeline in this folder plus `fix_breathe.py`. It is **NOT global**.
