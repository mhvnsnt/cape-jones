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
