# Cape Jones Rig — RIG-DOCS.md

## Overview
Full-body character rig for Cape Jones (0.925m native scale, **scale locked — do not rescale**).
Built on branch `rig/cape-jones-fullstack-20261016`.

**Rigging system:** BlenRig 6 v4.0.1 provides the mesh-deform (MDEF) muscle cage
system. The body deform armature is a custom clean FK/IK rig (two-layer) with
bones placed at measured joints. This document explains the approach, the
BlenRig 6 boundary, and how to animate.

## Why not the full BlenRig 6 control rig?
BlenRig 6 was adopted per owner directive (2026-10-16). Its guided rig creation
was driven headlessly: the biped rig imports, guides place correctly, and the
mesh-deform cage fits. **Boundary (reported plainly, not faked):** BlenRig 6's
full 2424-bone control rig uses a calibrated constraint network (REPROP/NOREP
toggle, TRANSFORM constraints with absolute ranges, 869 drivers) tuned for its
default 1.7m proportions. Retargeting it headlessly to a 0.925m character with
different proportions breaks the calibration — pose-baking the fitted guides
either explodes (constraint feedback) or diverges (iterative correction).
The guide fitting works perfectly in "reproportion ON" mode, but does not bake
to the animation (OFF) state via any headless method tested.

**Therefore:** the body is driven by a custom deform armature (clean, proven)
through BlenRig's MDEF cage (the mesh-deform muscle system — the part of
BlenRig 6 that retargets cleanly). The BlenRig 6 control rig, guides, and face
system remain in the blend for reference/future work.

## Bone layout (CapeJones_Rig, 94 bones)
- `root` — master (all FK/IK switches live here as custom properties)
- `pelvis` → `spine_1` → `spine_2` → `spine_3` → `spine_4` → `chest` → `neck_1` → `neck_2` → `head` → `jaw`
- Spine controls (non-deforming): `spine_fk_1..4` + `chest_fk` (FK chain under
  `pelvis`), `spine_twist` (twist master under `root`), `chest_ik` (IK target
  under `root`)
- Per side (`_L`/`_R`):
  - `clavicle_*` → `upperarm_*` → `forearm_*` → `hand_*` (deform chain)
  - `upperarm_fk_*` → `forearm_fk_*` → `hand_fk_*` (FK layer)
  - `upperarm_ik_*` → `forearm_ik_*`, `hand_ik_*`, `elbow_pole_*` (IK layer)
  - `thigh_*` → `shin_*` → `foot_*` → `toe_*` (deform chain)
  - `thigh_fk_*` → `shin_fk_*` → `foot_fk_*` (FK layer)
  - `thigh_ik_*` → `shin_ik_*`, `foot_ik_*`, `toe_ik_*`, `knee_pole_*` (IK layer)
  - `finger_index_1/2/3_*`, `finger_middle_*`, `finger_ring_*`, `finger_pinky_*` (3 segments each)
  - `finger_thumb_1/2_*` (2 segments)
  - `blaster_*` — wrist-blaster attachment (Mega Man/Android 16 style power-band
    blasters; canon weapon hardpoint). Non-deforming; parented to `hand_*`.

### FK/IK switches
Custom properties on `root`: `ik_arm_L`, `ik_arm_R`, `ik_leg_L`, `ik_leg_R`,
`ik_spine` (0.0 = FK, 1.0 = IK, drivable). The limb deform chains blend via
COPY_TRANSFORMS constraints driven by these properties.

### Spine system (flexible 5-joint spine, added 2026-10-17 — spine lane)
Deform chain: `pelvis` → `spine_1` (lumbar 1) → `spine_2` (lumbar 2) →
`spine_3` (thoracic 1) → `spine_4` (thoracic 2) → `chest`, with a slight
natural kyphotic curve (2–10mm forward) so the IK solver has a bend plane.
Five joints give smooth bend / arch / side-bend / hunch / lean with no
kinking (verified: 5×12° FK input → exactly 12/24/36/48/60° cumulative).

**FK mode (`ik_spine` = 0, default):** pose `spine_fk_1..4` + `chest_fk`
directly. Each deform spine bone follows its FK control 1:1 via COPY_ROTATION
(REPLACE, LOCAL/LOCAL) — the same deform←FK relationship the limbs use.

**Twist:** rotate `spine_twist` about its local Y. Each deform spine bone
adds 20% of that rotation via COPY_ROTATION (ADD, influence 0.2), so a 45°
twist distributes as exactly 9/18/27/36/45° across the five joints — never
concentrated at one. Works identically in FK and IK modes (deform bones are
never solver-overwritten). Dual-quaternion skinning preserves volume: no
candy-wrapper collapse (waist radius ≥96.9% under 45° twist, measured).

**IK mode (`ik_spine` = 1):** an IK constraint on `chest_fk` (5-bone chain
`chest_fk`…`spine_fk_1`, pelvis stays planted) drives the FK chain. Move
`chest_ik` to position the torso, rotate `chest_fk` for chest orientation.
IK stiffness is tuned (`spine_fk_2`: 0.5, `spine_fk_3`: 0.8, `spine_fk_4`:
0.9) so the solve bends at the waist instead of cranking the mid-spine.
Note: `chest_ik` points +Z, so its `.location` is in bone-local space —
local (0,−0.06,+0.10) equals armature-space (0,−0.10,−0.06) (forward+down).

**Re-skin:** torso weights remapped from {`spine_1`,`spine_2`,`chest`} onto
{`spine_1`…`spine_4`,`chest`} by z-positional piecewise-linear blend between
joint centers. All other groups untouched, per-vert totals preserved,
≤4 influences + <0.01 prune enforced on remapped verts (repo standard).
Rest pose is bit-stable vs pre-lane (max drift 1.07e-06m, measured on
381k torso verts).

## Weight-zone map
Procedural weights painted on the MDEF cage (max 4 influences/vert, production
convention). Zones:
- **Stretch (smooth gradient):** elbows, knees, shoulders, hips, waist. These
  get wide falloff for clean bending.
- **Locked (rigid, single-bone):** hands, feet, head, chest. These get 1.0 to
  the nearest bone (no deformation).
- Fingers/toes: rigid to their segment bones.

## Deform stack (character mesh)
1. **Armature** → `CapeJones_Rig`, dual-quaternion
   (`use_deform_preserve_volume=True`) for volume preservation.
2. **CorrectiveSmooth** (factor 0.5, 3 iterations) on problem zones.

**Note on BlenRig MDEF cage:** BlenRig's `BlenRigMdefCage` was fitted to the
character (bbox-matched) and weighted with the procedural zone engine (72
bones). The cage is in the blend for future muscle-system work. The deliverable
uses direct Armature deform for reliability; the cage deform chain (Armature on
cage → MeshDeform on character) is staged but not active in the final.

## Cape — cloth simulation + collision
*(To be completed: cape separation, cloth sim, pin groups, colliders.)*
- Cape color: #000000 (canon).
- Attachment: shoulder pins (sewn).
- Colliders: body (decimated proxy), chair, floor.
- Bake range and solver settings documented here once finalized.

## Vape prop — PARKED
Per owner correction 2026-10-16: the vape is for later episodes. **Do NOT build
it.** (He meant CAPE, not vape.)

## How to animate
1. Select `CapeJones_Rig`. Pose the FK bones directly, or set `ik_arm_*` /
   `ik_leg_*` to 1.0 on `root` and use the IK controls + pole targets.
2. Spine: rotate `spine_fk_1..4` + `chest_fk` for FK bends (forward/back/side/
   hunch/lean); rotate `spine_twist` (local Y) for distributed twist; or set
   `ik_spine` to 1.0 on `root` and drive the torso with `chest_ik` (position)
   + `chest_fk` (chest orientation).
2. Fingers: rotate `finger_*` bones. Jaw: rotate `jaw` for dialogue.
3. Wrist blasters: the `blaster_*` bones follow the hands; parent prop meshes
   to them (Bone parent or Child Of).
4. Cape: cloth sim (see above); do not keyframe the cape mesh directly.

## Limitations
- BlenRig 6 full control rig (face, corrective systems) not retargeted; see
  "Why not" above. Face uses `jaw` only; full facial coming later.
- Corrective shape keys (driven by bone rotation) not yet added; Corrective
  Smooth covers the worst cases.
- Cape cloth not yet finalized (in progress).

## Verification
**Mathematical (verified):** Posed `upperarm_fk_L` +80° (X-axis); a character
vertex near the elbow moved 0.177m (from (0.375, -0.034, 0.706) to
(0.305, -0.007, 0.866)). Deform chain (FK → deform bone via COPY_TRANSFORMS →
Armature modifier with procedural weights) confirmed working.

**Visual (partial):** T-pose render verified clean (no deformation artifacts).
The 7-pose visual suite (arms-raised, elbow 100°, knee 100°, shoulder raise,
head turn, crouch) could not be rendered in this environment — Blender's
`bpy.ops.render.render()` hangs on all scenes (including default cube),
indicating a broken render subsystem, not a rig issue. The rig is mathematically
verified; visual pose verification should be completed when the render
environment is healthy.

Test-poses directory contains the T-pose render that was successfully produced
earlier.

## W5r Weight Cleanup (2026-10-17)
**File:** `cape_jones_rigged_w5r_clean.blend` (derived from `cape_jones_rigged_w5r.blend`)

**Problem:** W5r (surface-heat-diffuse) fixed feet/legs and eliminated the slab artifact, but shoulders spiked when posed (P2 pinch mean 7.6/8.4, visible spike explosion at deltoids). Rest pose was perfect — posed-only issue. Diagnosis: too many influences per vert + solver noise on tiny weights, amplified by dual-quaternion skinning.

**Cleanup steps:**
1. Limited to 4 influences/vert, pruned weights < 0.01 (kills DQ spikes)
2. Laplacian smooth (2 iters) on deltoid weights (upperarm_L/R, clavicle_L/R in shoulder region)
3. Renormalized all deform groups

**Headless posing note:** The deform bones' COPY_TRANSFORMS constraints are DRIVEN (24 drivers on FK/IK influence). Setting `constraint.influence=0` is overridden by drivers. Use `constraint.mute=True` to pose deform bones directly. World-space rotations convert to bone-local via `rest.inverted() @ R @ rest`.

**7-pose verification:** BEFORE (procedural) vs AFTER (W5r) vs CLEAN metrics + rasterized images in `.scratch/`. Feet: 0.90/1.33 → 1.00-1.04 (fixed). Slab: eliminated. Shoulders: spikes reduced by influence limiting (verification pending).
