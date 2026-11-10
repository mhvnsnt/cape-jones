# SITTING RIG v1 + RIG SYSTEM REGISTRY — 2026-11-01

Folder: `sitting-rig-20261101/`. No original touched, no repo push.
Approval 0/1 sitting rig + 0/1 rig system/registry separately.

## 1. The sheet — plainly, no invented name

NO sheet is literally named "three quarter sitting sheet" anywhere searched
(`sliced-68`, `transparent-plates-grok-full-sweep`, `sliced/`, `fla-packs`).
Closest real sheets, all verified on disk:

- `fla-packs/lounge-3quarter-packs/clean-*.jpg` — 11 sheets, byte-duplicates of
  `fla-packs/lounge-packs/lounge-*.jpg` (duplicate_md5_of in the 68-sheet manifest).
  Transparent plate example: `transparent-plates-grok-full-sweep-20261031/plates/fla-packs/lounge-DGb2j.png`
  Kit, by sliced piece (sliced-68 `sheets/fla-packs/lounge-DGb2j/MANIFEST.json`):
  Row1_1 head 112x169, Row2_1 arm 87x333, Row2_2 torso 308x376, Row2_3 arm 85x333,
  Row2_4 leg 109x500, Row2_5 leg 110x500, Row2_6 cape 509x688,
  Row3_1..4 hands 104-122 x 137-139. All MIXED/UNCLASSIFIED in that manifest —
  the mapping above is by plate position/size, matching the viewed plate.
  That kit IS the v7c sliced kit at plate scale, not a sitting-only pose.
- `fla-packs/fla-3quarter-front.png` (1792x1008) / `fla-3quarter-back.png` — kits,
  standing, joint balls visible, NOT sitting.
- Sitting poses that already existed: `reposes-v7c-clean/joint-seated-v7c-clean.png`
  (lotus seated, v7c), CJ-23 lotus plate, canonical-room chair seated figure
  (legs forward, hands together, in the pink wingback chair).

MISSING PART, plainly: a true 3/4 foreshortened thigh/shin piece (thigh toward
camera, chair view) does NOT exist in any FLA kit found. The 3/4 chair view below
is a front-rig pose + room-plate TEST composite, NOT a new foreshortened leg piece.
No piece was faked or hand-drawn. A hand-drawn 3/4 thigh/shin piece is owed if
Mars wants a true 3/4 chair rig, as a separate explicit job.

## 2. Sitting rig v1 — built, poseable, not a flat plate

Builder: `build_sitting_rig.py` — v7c limb logic copied from
`joint_locked_rig_v7c.py` (pivot = ball centre; scale 0.95; labels=False on finals).
Pieces: `sliced/` (Cape_Back_Main, Cape_Collar, Torso_Chest, Pelvis, Belt_Overlay,
Neck, Head_Front) + `cut-limbs-v7c/` (Arm/Leg Upper/Lower/Cap, both sides).
Rules: wrist = wrist end of lower arm (hands are in the lower-arm pieces as drawn,
no hand cut/paste here); knee-feet: knees+feet same direction, analytic knee
positions recorded in `gates-20261101.json`, not a block range; cape collar locked,
cape back is the only moving cape part; seated anchor = seat, NOT floor
(the transparent rig has no chair — feet do NOT touch a floor line in the rig
alone; in a chair composite the seat carries the figure, chair feet carry the seat).

Poses, 1100x1500 transparent, all inside canvas, gates PASS:
- sit-lotus: arms -20/20, lower -20/20; legs upper -60/60, lower 80/-80.
  This is the v7c seated config, reissued clean/transparent. Bbox 225,253-877,1198,
  alpha 370,140px. Knees L (253.1,885.0) R (848.0,857.0). Elbows L (353.3,611.2) R (752.9,608.9).
- sit-chair-lap: arms upper -20/20, lower +50/-50 (forearms inward to lap centre,
  hands together at lap — first build used -70/70 and splayed arms outward, caught
  by viewing and fixed); legs upper -45/45, lower 55/-55 (thighs splayed, shins
  folding to feet together in front). Bbox 270,253-838,1198, alpha 339,355px.
  Knees L (298.0,936.2) R (809.8,913.3). Elbows L (353.3,611.2) R (752.9,608.9).
- sit-lean-forward: torso shifted +20px, arms lower +45/-45 (hands to knees),
  legs upper -50/50, lower 65/-65. Bbox 273,253-872,1198, alpha 351,631px.
  Knees L (301.6,920.4) R (844.2,895.7). Elbows L (345.6,595.4) R (800.1,592.0).

To change a pose, change the config dict in `build_sitting_rig.py` and re-run —
that is the rig, not a one-off picture. GIF cycles lotus -> chair-lap -> lean ->
chair-lap -> lotus, 500ms, as a poseability proof.

Files:
- poses/sit-lotus-20261101.png, poses/sit-chair-lap-20261101.png,
  poses/sit-lean-forward-20261101.png (+ -on-grey versions)
- sitting-rig-poses-20261101.gif
- contacts/sitting-rig-contact-joints-20261101.png (joint circles = PROOF ONLY,
  finals carry no debug circles)
- sitting-rig-on-empty-room-plate-TEST-20261101.png — TEST ONLY: chair-lap rig
  placed on the approved empty 2D room plate (canonical-room-2d-from-3d-20261101.png),
  chair area, height 300px. NOT a measured canonical-room scale, NOT a CJ-23
  replacement. A first composite attempt on the canonical chair crop was DELETED
  on sight: that crop already contains the baked canonical seated figure, so it
  doubled the figure — a clean chair crop must come from an empty plate, never
  by erasing a baked figure (layer-removal rule).

## 3. Rig system registry

- RIG-00 DEFAULT ORIGINAL RIG — v7c apose rig. Builder `joint_locked_rig_v7c.py`,
  pieces `sliced/` + `cut-limbs-v7c/`, canvas 1100x1500, scale 0.95,
  shoulders L (430,445) R (670,445), hips L (470,740) R (615,740),
  arm ball centres L (60,222) R (99,222), leg ball centres L (95,314) R (100,314),
  arm lower anchor (ball_x, 0), leg lower anchor (ball_x, 0).
  UNTOUCHED by this job. Every other rig below is a variant of, or an overlay
  on, this rig — none of them replaces it.
- RIG-01 SITTING RIG (NEW, this job) — poses above, builder
  `sitting-rig-20261101/build_sitting_rig.py`. Same pieces, same pivots,
  seated configs only. This is the sitting version of him.
- RIG-02 CAPE CONSUMED — DIFFERENT RIG, not default, not a colourway.
  All-black form, WHITE OUTLINE mandatory whenever body crosses in front of
  itself. Variants: BARE (both cape pieces ABSENT: Cape_Back_Main + Cape_Collar
  omitted as layers, never rectangle-erased) and NON-BARE UPPER ONLY / COLLAR
  (collar PRESENT, back ABSENT). Source: `cape-consumed-bare-upper-20261031/`,
  `future-symbiote-capeless-white-outline-20261031/` (capeless white-outline
  family, same layer-omission method). FUTURE ONLY, not V2/canon, per-shot 0/30.
- RIG-03 DREAM COLOURWAYS — colourway variants of RIG-00, NOT new geometry.
  Dream 1 (white suit, magenta cape), Dream 2 (gold suit, magenta cape),
  Dream 3-10, Dream 11-18 (each part coloured independently, rim own colour
  in 11-18). Source: `dream-dual-saved-20261101/presets/`,
  `dream-variations-11-18-20261101/presets/`. Same base
  `rig-apose-v7c-clean-transparent.png`, nearest-base-colour recolour,
  dist>110 untouched, black outline never reassigned, rim thin 6px outer-only.
- RIG-04 GOLD V6 / DUAL CHARGE — colourway + rim variant, NOT new geometry.
  V6 standalone, V5 stays V5, replaces nothing. Seam x650 right, locked.
  Powers, CANON (Mars 2026-11-01 00:37 CDT): DUAL CHARGE THIN (rim 6px),
  DUAL CHARGE MEDIUM (rim 12px), DUAL CHARGE HEAVY (rim 20px).
  Source: `gold-split-rim-upgrade-20261031/`.
- RIG-05 CapeGP — Grease Pencil layer rig, Blender 5.2.3, 10 layers
  (FaceSnapArm > Head > CowlUpperArm > Neck > ChestSnapArm > Torso > Collar >
  NormalArm > Legs > CapeBack), strokes traced from v7c, no new art.
  Source: `capegp-presets-20261031/`. Layer-order proofs / Blender motion only;
  PIL/v7c is the default for clean plates.
- EFFECT, NOT A RIG — CRYSTAL / CRYSTALLIZATION. Preset 8 / P8-06 normal-map
  look, applied as an OVERLAY on RIG-00 (and, by extension, on RIG-01).
  Transformations #1 feet-up sweep, #2 facet creep (APPROVED), #3 vein-first +
  shard spikes + dust (APPROVED), #4 chest-emblem origin (551,491) (APPROVED).
  It does NOT need its own rig, per Mars's reading — it is an effect, not a
  separate body. Source: `crystallization-preset8-power-20261031/`,
  `crystal-cape-jones-v2-transformation-4-chest-emblem-20261101/`.

How to start a new rig from here: copy `build_sitting_rig.py`, change only the
config dict (angles + shift), keep pieces/pivots/rules identical, save as a new
RIG-0N entry in this registry with its source pieces listed. Never overwrite
RIG-00, never rename a variant as default.
