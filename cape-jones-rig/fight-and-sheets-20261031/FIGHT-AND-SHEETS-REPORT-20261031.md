# FIGHTING ANIMATION + SHEET CUTOUT/LABELING + HAND LIBRARY — 2026-10-31

Orders: Mars 2026-10-31 ~18:33 CDT (fighting + finish sheets) and ~18:35 CDT
(hands priority + dance variants). Additional approval noted: face/cowl
before/after sheet = PERFECT 1/1, both fixed versions approved 18:34 CDT
(jojo-03 FACE-SNAP, ginyu-01 COWL-SNAP).

## 0) SAVED AS FIRST EXAMPLE (not a full-scene approval)
SAVED-AS-FIRST-EXAMPLE-20261031.md in this folder. Punch-limb afterglow
(afterglow-videos-20261031, GIF+MP4, 24f, Blender 5.2.3, v5 Arm2 flipped
forearm, windup/snap -110/impact/recover/rest, trail in motion only,
final frame true zero) is saved as a GOOD FIRST EXAMPLE only. It is NOT
approval of a full fighting scene.

## 1) INVENTORY — Mars's "300 sheets" reconciled, plainly
- Image files in study clone sheets/ (READ-ONLY, never written there): 245
- Unique by MD5: 184. Exact-duplicate copies: 61 (content already sliced
  under the other path, no content lost).
- Sliced clean (slice_clean.py): 140/184 unique = 76%, 2,854 pieces.
- File paths not in the slice manifest: 105 = 61 duplicates + 44 unique
  unsliced. Those 44 = backgrounds 26 (painted scenes, kept as paintings —
  slicing them into rig pieces would be wrong) + reference sheets 18
  (color-keys 6, layout-line-art 5, storyboards 5, viseme-charts 2).
- So: Mars's "like 300" is CLOSE but high for the study clone alone:
  245 files on disk, 184 unique sheets. There is no hidden 300-sheet
  source in the study clone. If he has ~55 more sheets elsewhere (another
  folder, uploads, FLA packs not in this clone), those are NEEDS-MARS-INPUT
  — point at them and they get cut next. Do NOT claim 300 from this disk.
- Per-group sliced pieces: C-variations 1,238; F-fla-packs 648; A-root 471;
  D-xray-angle-ref 302; E-exposure 110; G-props 78; B-model 7 (single full
  figures, correct, not a failure).
- Eye-verified sheets: 11 previously (see CLEAN-SLICE-BATCH doc) + new
  hand-sheet contacts in this task. Per-sheet eye pass still owed on the
  remaining sliced sheets — numeric QC is not eye-done. Do not claim
  eye-done for the whole batch.

## 2) CUTOUT + LABELING — what was finished, what is provisional
- Cutout: 100% of sliceable unique sheets are already cut (140/140).
  The 44 unsliced uniques are NOT rig sheets and were correctly NOT cut.
  No new full-sheet cut was needed; the new cuts in this task are the
  hand sheets (section 4).
- Labeling index: piece-label-index-20261031.json — all 2,854 pieces,
  with size, opaque px, white/dark/purple/skin/green percentages and a
  PROVISIONAL colour label. Provisional counts: WHITE-SUIT 910 (32%),
  BLACK-CAPE/COLLAR 614 (22%), COWL/HEAD-PURPLE 203 (7%), SKIN/FACE 60 (2%),
  XRAY-SKELETON 7 (0.2%), MIXED/UNCLASSIFIED 1,060 (37%).
- Honest status: this index is PROVISIONAL, not eye-labelled. A colour
  bucket is not a body-part label. Full eye labelling of 2,854 pieces
  (which part, which side, which angle, good vs mislabeled vs reject)
  is NOT finished in this task and must not be claimed as finished.
  What IS finished: the index, the hand library labels (section 4),
  and the parts-audit baseline carried forward (75/75 parts audited,
  9 mislabels corrected, 5 rejects, 6 exceptions pending Mars).
- NEEDS-MARS-INPUT: (a) the ~55 sheets beyond the 245 on disk, if they
  exist elsewhere; (b) parts-audit exceptions 6; (c) sheet-08 hand eye
  labels (19); (d) exposure-strip column split for per-frame exposure
  pieces (strips slice as one tall piece — timing reference, not rig
  sources, as before).

## 3) FIGHTING ANIMATION — real sequence, whole body, afterglow on all limbs
Files: fight-afterglow-20261031.gif + .mp4, fight-contact-20261031.png,
frames/ (rig plates + afterglow jpgs), build_fight.py, fight-manifest.
- Sequence (front rig, v7c, labels=False): guard 6f -> punch-2 windup 4f
  -> snap 2f -> impact hold 6f (Arm2 -110 across-up, APPROVED impact)
  -> across-down 2f (-70 sequence frame) -> recover 4f -> punch-1 windup
  3f -> snap 2f (Arm1 -90 jab) -> hold 4f -> recover 4f -> kick windup
  3f -> kick hold 4f -> recover 4f -> block/dodge hold 6f -> rest 10f.
  Rig frames 64, afterglow frames 64, + 8 true-hold decay frames (final
  frame measured 0.0 mean diff vs a clean plate = true zero), then
  mirrored-angle shot 6f + true 3/4-front plate 12f = 90 frames total
  in the video. First build's final frame still showed a rim because
  the "rest" segment was still interpolating from block to guard — that
  was caught on viewing, fixed with the 8-frame decay tail, and the
  contact sheet was rebuilt and re-viewed.
- Angles/shots: Shot A = front v7c rig (all motions). Shot B = mirrored
  front — LABELLED mirrored, NOT a true camera angle. Shot C = true
  3/4-front model-sheet plate (B-model, single full figure) as a still
  cutaway — no trail, because it does not move (zero at rest, per rule).
  A true 3/4 or side or back FIGHT animation does not exist yet: the
  angle sheets give full-figure plates, not jointed rig pieces for those
  angles, so a jointed 3/4 fight cannot be built from existing pieces
  without inventing pieces — that is stated, not substituted.
- Afterglow: Default Afterglow Preset applied to the WHOLE body in
  motion (past-position soft rims, cyan (0,200,255), dilate 6 blur 5,
  fade 0.50/0.40/0.30/0.20/0.12/0.06, skipped when past frame == current
  frame so holds have no static rim). Final rest frame = true zero
  (10 rest frames > 6-frame lag).
- Punch identity note, plainly: the fight's cross punch reads as the
  approved locked punch silhouette (one arm out left, one bent at the
  chest), but the arm doing the crossing in this build is Arm2, whereas
  the locked file's extending arm is Arm1. The silhouette matches; the
  arm identity does not — full punch-pose integration with the approved
  v5 flipped fist is still owed, as before.
- Kick note, plainly: the "kick" segment reads as a wide low stance,
  NOT an extended kick. A front-view leg rotated in the v7c builder
  swings sideways, it does not foreshorten forward. A true forward kick
  needs a foreshortened leg piece (still owed, 0/1) — the segment is
  labelled kick-stance in the final contact, not a kick, and a real
  kick is still owed.
- Fist note: fight uses v7c cut-limb lowers (gauntlet), NOT v5 flipped
  fist — v5 fist integration into the v7c builder is still owed.
  Front-facing fist in the fight = gauntlet fist, not palm (palm fist
  v3 is a separate palm-facing piece, never used here).
- Checks: knee-feet (legs in guard/kick/block keep knees/feet same
  direction by construction; kick leg is extended, not crossed),
  arm-front-snap + face/cowl snap (no punch arm crosses the face in
  this sequence — Arm2 -110 is across-up over the torso, the approved
  impact, and the builder order keeps it as in the approved locked
  punch; block forearms stay below the chin), no red label pixels
  (labels=False), no Mars-seen file overwritten (all new dated folder).

## 4) HAND LIBRARY + DANCE VARIANTS
Full doc: hand-library/HAND-LIBRARY-20261031.md. Summary:
- Canon hands (sliced/): 7/7 GOOD — fist, fist-back, open, point,
  point2, relaxed, grip.
- X-ray skeleton hands (new cut, this task): 19 pieces, 3 sheets,
  eye-verified contacts — SPECIALTY ONLY, never normal dance hands.
- Sheet-08 hand row: 19 small pieces PROVISIONAL + 1 reject (a 1522x3
  title line, not a hand).
- Extracted total: 45 hand pieces. GOOD 26 (7 canon + 19 x-ray specialty),
  PROVISIONAL 19, REJECT 1. Still owed: sheet-08 eye labels 19 + side
  confirmation for the point pair + unisolated hand components inside
  the wider 2,854-piece batch (not counted as extracted until isolated).
- Dance-variant system: dance-variants/ — same groove base poses, hand
  swapped at the wrist end only (fist centre = elbow + rot((0,1),
  arm_lower)*210*SCALE, hand scaled 1.7x to cover the built-in fist).
  3 groove poses x 4 hand sets (base-fist, open, point, relaxed) =
  12 frames + 4 GIFs + contact, viewed. Main dances stay MAIN
  (dance-improved / dance-kneefeet-corrected, 63f); variants are
  different hand-motion reads on the same base, not replacements.
  Limits: groove-b legs cross (source pose angles, not the hand swap);
  groove-b hands land near the face because the forearms cross in
  front — that is the pose, not a layering bug; open/point hands are
  larger than the fist and cover the wrist cap, which reads cleanly
  at contact-sheet size.

## Approvals (Mars approves — none claimed here)
- Face/cowl before/after sheet: APPROVED 1/1 (Mars, 18:34-18:35 CDT).
  JoJo-03 FACE-SNAP + Ginyu-01 COWL-SNAP: APPROVED 1/1 each (18:34 CDT).
- Punch-limb afterglow: SAVED as first example only (not scene approval).
- Fighting animation: 0/1. Hand library: 0/1. Dance variants: 0/1.
- No repo push in this task.
