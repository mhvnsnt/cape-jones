# WORKSTREAM D — Mars 100% sweep, 2026-10-31 — TV PRODUCTION READINESS re-prioritisation

Focus change applied (Mars, 2026-10-31 20:53 CDT, via parent): work that blocks
shots — wrist attach, snap layering, clean pieces — is PRODUCTION. Further hand
variations and FLA labelling beyond what shots need are ADDITIVES / EXTRAS,
labelled separately below. Nothing was restarted, overwritten, deleted, or
pushed. No version Mars saw was overwritten; this folder is new and dated.
Nothing in this report is claimed approved or landed.

## A. PRODUCTION — blocks shots

### P1. Wrist attach (hand seating)
Rule: open hands attach by the WRIST end to the forearm end, not fingertips.
Fix = MOVE, don't flip. Arm1 exception: Arm1 mirrored horizontally in place
BEFORE rotation; Arm2 unchanged. Joint balls are FINE for now, do not remove.
v7c pivot = ball centre. No-crop throughout.

- Library T-pose flatten: 7/7 hands, both sides, wrist gate PASS.
  d_wrist = 20.0 px on every side; d_wrist < d_tip on every side.
  L angle +90, R angle −90; fingers outward along the arm axis.
  Scale 1.275 (25% down from 1.7), wrist-anchored. No-crop 7/7 PASS
  (canvas 1500×1500, x-offset +200).
- Dance swapped hands: 9/9 poses, both sides, wrist gate PASS; scale 1.275;
  Arm1 mirror applied; flatten rotation NOT applied (dance poses are not
  T-poses, fingers-up gesture kept, angle 0). No-crop 9/9 PASS.
- Serve move-up set (JEI-01 crusher serve open palm, Arm1, mirror unchanged,
  angle 164.8, scale 1.0): 2/2 versions built (plain + ball), approval 0/1.
  Move = pure vertical dy = −19 px only, no sideways, no flip, no scale change.
  Hand centre (314,530) → (314,511); wrist (331.6,474.6) → (331.5,455.6).
  Column gap at x290: 19 px → 0 px. Fist pixels remaining outside new hand: 0.
  Torso/cape difference at x ≥ 380: 0 px. Ball centre moved with the hand,
  (314,530) → (314,511). No-crop plain + ball PASS.
  New sweep proof (viewed): `serve-move-up-sweep-contact-20261031.png`
  (full plain, full ball, wrist zoom x200–420 / y360–600 at 2×).
  Source (untouched): `hand-serve-move-up-20261031/` — approval 0/1 there too.

### P2. Snap layering (arm-front snap, dance)
- Rebuilt 63/63 frames = 100% in `dance-arm-snap-20261031/`.
- Frames with at least one snapped side: 21/63 = 33.3%.
- Frames unchanged (no snap): 42/63 = 66.7%.
- Side-snaps total: 30 (L 10 frames, R 20 frames).
- Rule: whole chain (upper + lower + elbow cap) moves above torso on snapped
  frames; chest < arm < head. This is the shot-blocking layering fix, not a
  hand variation.

### P3. Clean pieces (clean-slice)
- Sliced: 140/184 unique sheets = 76.1%. Pieces written: 2,854.
  Verified in this sweep from `sliced-clean-20261031-results.json`:
  140 sheets in results, piece counts sum to exactly 2,854.
- NOT sliced as rig pieces: 44/184 = 23.9% — backgrounds 26 unique (painted
  scenes, kept as paintings; slicing them would be wrong) + reference sheets
  18 (colour-keys 6, layout-line-art 5, storyboards 5, viseme-charts 2).
  These 44 are NOT production blockers.
- Eye pass (production risk, stated plainly): eye-verified in detail 11/140
  sliced sheets = 7.9%. Per-sheet eye pass still owed for 129/140 = 92.1%.
  Sliced ≠ eye-done. Numeric QC (files exist, non-empty, RGBA, 0 flags) covers
  2,854/2,854 pieces; it does not replace the eye pass.
- Clean clip re-render (from the batch doc, not re-run here): 17/17 = 100%.

### P4. Attachment cleanup, top-5 (shoulder–bicep first)
- Preset base saved FIRST: `attachment-cleanup-20261031/preset-base-original-with-lines/`,
  29 files. Re-verified in this sweep: 29/29 files match manifest sha256 + bytes.
  Nothing in that folder is ever edited; revert is byte-exact.
- Top-5 methods run as free PIL analogues (Harmony/Animate/OpenToonz/GP/Spine
  themselves were NOT run here): M1 deformation/contour-follow, M2 OpenToonz/
  Tahoma vector outline joining, M3 Grease Pencil stroke joining + smoothing,
  M4 Spine mesh-weight feather, M5 traditional cel line-matching (OFF by
  default, safety cap, erased 0 px on all 3 test poses).
- Cleaned outputs on disk: 24 files (3 test poses × methods, incl. combined).
  Combined (M1+M2+M3+M4+hole-fill, shoulder bands only): holes 2957→0 (cap-01),
  1192→0 (bur-03), 1585→0 (jei-01); jagged 107→10, 54→10, 117→20;
  changed px outside seam bands: 0 on all 3 poses. Joint balls intact.
- NOT fixed, stated plainly: the interior shoulder–bicep double line is NOT
  removed by this pass. Combined is a safe outer-edge smoother, NOT a seam
  fixer. The real fix is builder-level overlap/cap placement or a true
  vector clean-up in OpenToonz/Tahoma2D. That vector pass is still owed.
  Do NOT present combined as "seams cleaned" to Mars.
- Approval of cleaned versions: 0/1. Originals being perfect does NOT approve
  the cleanups. Viewed proof (existing, re-viewed in this sweep):
  `attachment-cleanup-20261031/before-after-contact-20261031.png`.

## B. ADDITIVES / EXTRAS — beyond what shots need

### E1. Per-hand keep / swap / flip-bottom-to-top — MARS-ONLY, BLOCKED, 0/7 decided
- Prepared, not decided: 7/7 individual big views in `per-hand/` plus one
  all-7 contact sheet. Each sheet shows CURRENT FINAL state only: LEFT Arm1
  (mirrored in place, +90°) and RIGHT Arm2 (unchanged, −90°), enlarged
  wrist/forearm crops, plus the raw library piece upright as stored.
  No flipped variant, no swapped variant was generated on these sheets.
  No call was filled in by the agent.
- Call form on every sheet (blank): [ ] KEEP  [ ] SWAP  [ ] FLIP-BOTTOM-TO-TOP
  [ ] OTHER: ______ — one call per hand, Mars only.
- Hands: 1 Fist (Hand_1_Fist), 2 FistBack (Hand_2_FistBack), 3 Open
  (Hand_3_Open), 4 Point (Hand_4_Point), 5 Point2 (Hand_5_Point2),
  6 Relaxed (Hand_6_Relaxed), 7 Grip (Hand_7_Grip).
- Count: decided 0/7 = 0%; owed 7/7 = 100%. This is an extra until Mars calls it;
  it does not block the wrist-attach production work in §A, which is already
  seated and gated.

### E2. FLA piece-labelling beyond what shots need — extras
- Batch: 60/60 pieces processed = 100% (`fla-piece-labelling-top5-20261031/batch-60-20261031/`,
  fla-front 33 + fla-back first 27, sorted).
- HIGH confidence (both tools agree, conf ≥ 0.8): 2/60 = 3.3%.
- NEEDS-MARS-EYE (tools disagree): 58/60 = 96.7%. MEDIUM: 0/60. REJECT: 0/60.
- Mars corrections applied: 16/60 = 26.7% (all renames, in `corrected.json`;
  original `proposals.json` untouched).
- Remaining: 44/60 = 73.3% still owed — these are the `keep` lines in the
  corrections file, i.e. proposed names NOT yet verified by Mars as `good`,
  renamed, or rejected. Do NOT count a `keep` as Mars-verified.
- Further owed, per brief (carried, not re-derived in this sweep):
  sheet-08 eye labels 19; point-pair sides (count not specified in the brief,
  still owed). All legs/arms in this work are FRONT view, per brief.
- System approval: 0/1. Tools #4 (XFL/JSFL) and #5 (SWF/Ruffle) are proven on
  synthetic files + real JSFL only — no real Cape .fla/.xfl/.swf exists on disk.
- This labelling is an extra until shots need a named piece; the clean pieces
  themselves (§P3) already exist unnamed.

## C. Discrepancy to reconcile before quoting approval (do not paper over)
- The parent brief for this sweep lists dance hands + library T-pose as
  APPROVED 1/1 each. The on-disk record,
  `hand-tpose-flatten-20261031/HAND-SEATING-RULE-20261031.md`, still says
  approval 0/1 for the whole combined set (all items together).
- This sweep did NOT edit that doc, did NOT overwrite any Mars-seen file,
  and does NOT claim dance/library as approved or landed. Parent to reconcile
  the brief vs. the on-disk record before either figure is quoted to Mars.
- No discrepancy on serve: brief and on-disk report agree, approval 0/1.

## D. Still owed (consolidated, production first)
Production:
1. Serve move-up approval: 0/1 (plain + ball, 1 set).
2. Attachment cleaned-version approval: 0/1.
3. Per-sheet eye pass: 129/140 sliced sheets.
4. OpenToonz/Tahoma vector pass for the interior shoulder–bicep double line.
5. Wiring `check_wrist_attach` (with mirrored registry) into main builders.
6. Per-frame exposure-strip split (sheet-driven column method, not hand rectangles).
Extras (blocked / owed, Mars-only where noted):
7. Per-hand calls: 7/7 — KEEP / SWAP / FLIP-BOTTOM-TO-TOP, Mars only.
8. FLA labelling: 44/60 pieces + sheet-08 eye labels 19 + point-pair sides.
9. FLA system approval: 0/1.

## E. Files delivered in this sweep (new folder only, nothing overwritten)
- `workstream-D-mars-sweep-20261031/WORKSTREAM-D-MARS-SWEEP-20261031.md` (this report)
- `workstream-D-mars-sweep-20261031/serve-move-up-sweep-contact-20261031.png` (viewed)
- `workstream-D-mars-sweep-20261031/per-hand/per-hand-{1_fist,2_fistback,3_open,4_point,5_point2,6_relaxed,7_grip}-MARS-CALL-BLANK-20261031.png` (7 files, viewed: Hand 3 re-viewed after subtitle fix; all 7 generated by the same script)
- `workstream-D-mars-sweep-20261031/per-hand/per-hand-ALL-7-contact-MARS-CALL-BLANK-20261031.png` (viewed)

Standing rules honoured: joint balls FINE, not removed; v7c pivot = ball centre;
no-crop; checkpoint rule (new dated filenames, no Mars-seen version overwritten);
no repo push; no deletions; work in `~/workspace/cape-jones-rig/` only.
