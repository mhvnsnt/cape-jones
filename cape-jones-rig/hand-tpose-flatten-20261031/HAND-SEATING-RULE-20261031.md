# HAND-SEATING-RULE — 2026-10-31 (combined corrections, approval 0/1)

Folder: `hand-tpose-flatten-20261031/`. Builder: `build_combined.py`.
Contacts: `library-before-after-contact-20261031.png`,
`dance-before-after-contact-20261031.png`,
`serve-before-after-contact-20261031.png`.
Measurements: `measurements-combined-20261031.json`.
No repo push. No existing file overwritten. Base-fist frames and old
original library fists are untouched, not scaled, not mirrored.

## 1. The defect, measured (not guessed)
- Previous wrist fix seated hands at the wrist end (wrist distance
  20.0px, gate PASS) but kept angle 0, fingers-up, on BOTH sides.
- On groove-a (arm_lower L -60 / R +60, forearm outward
  L (-0.866, 0.500), R (+0.866, 0.500)), finger direction (0,-1) sat
  120.0 degrees off the forearm outward direction on both sides.
- On a horizontal T-pose (arm_lower L -90 / R +90, forearm outward
  L (-1,0), R (+1,0)), finger-up hands stick straight up on both
  sides instead of flattening along the arm.
- Mars's "plus 180" (2026-10-31 19:35 CDT) was his own guess
  ("I don't know, like 180 I think"). The measured correction from
  angle 0 is +/-90 degrees, NOT 180. Do not quote 180 as the target.

## 2. Wrist pivot (always)
- Hands attach by the WRIST end to the forearm end (2026-10-31
  18:52 CDT wrist rule: MOVE, don't flip, for attachment).
- Wrist target = forearm end minus outward x 20px (inside the
  forearm), i.e. d_wrist = 20.0 by construction in the T-pose and
  dance builds. Serve is the exception, see §6: it is
  centre-matched to the fist, so its wrist anchor is the cuff
  bottom (11.3px), not the old fist-centre gate.
- Wrist gate still applies after every change (mirror, scale, rotation):
  PASS iff d_wrist <= 30px AND d_wrist < d_tip.
- All 7 T-pose hands x both sides and all 9 dance hands x both
  sides: PASS (see measurements JSON). Serve: see §6 for the two
  numbers, plainly.

## 3. Per-side rotation signs — T-pose flatten
- Arm1 = image-left (our left, Arm_Front). Arm2 = image-right
  (our right, Arm_Back). "Front/Back" is limb identity, not view.
- T-pose: arm_upper L -90 / R +90, arm_lower L -90 / R +90,
  legs upper -10/+10, lower +10/-10, builder scale 0.95.
- Hand angle L = +90, hand angle R = -90. Opposite signs, one plus,
  one minus, exactly as Mars described. Finger direction after
  rotation: L approx (-1, 0), R approx (+1, 0) — along the arm axis,
  outward on both sides, not up, not inward. Measured per hand in
  the JSON (L x-component -0.992 to -1.000, R +0.992 to +1.000;
  small y-component from the native wrist-tip x offset, <= 0.12).
- Rotation is in-plane only (PIL rotate). It is NOT a mirror and
  does NOT substitute for the Arm1 mirror below.

## 4. Arm1 / Arm2 rule (2026-10-31 19:37 + 19:38 CDT)
- Arm2's hand is correct as is. DO NOT change Arm2.
- Arm1's hand must be inverted on the HORIZONTAL axis, staying in
  the SAME place, like the forearm flip earlier.
- Implementation, plainly: mirror the hand piece left-right about
  its OWN image centre (FLIP_LEFT_RIGHT), BEFORE rotation.
  Re-register the wrist point as (W - wrist_x, wrist_y) and recompute
  the paste centre so the mirrored wrist lands on the SAME forearm
  end. The wrist anchor is unchanged; the thumb/palm side swaps.
- NOT a whole-band move, NOT a vertical flip, NOT a rotation in
  place of the mirror. Rotation (flatten / serve axis) is applied
  AFTER the mirror, so the flatten direction is preserved.
- Applies to: library T-pose hands (Arm1 = L, mirrored; Arm2 = R,
  unchanged), dance swapped hands (same), and serve (Arm1, see §6).
  It does NOT apply to built-in gauntlet fists or base-fist frames
  (no swapped hand there — nothing to mirror).

## 5. Scale down 25% (2026-10-31 19:37:43 + 19:38 CDT)
- New size = 0.75 x current, anchored at the wrist, so the wrist
  stays on the forearm end (centre recomputed for the new scale).
- Dance swapped hands: 1.7 -> 1.275. Library FIXED hands: 1.7 -> 1.275.
- Per-hand pixel sizes (native alpha bbox x scale; before -> after):
  Hand_1_Fist 139x170 -> 105x127; Hand_2_FistBack 146x209 -> 110x157;
  Hand_3_Open 167x226 -> 125x170; Hand_4_Point 133x238 -> 99x178;
  Hand_5_Point2 151x238 -> 113x178; Hand_6_Relaxed 163x228 -> 122x171;
  Hand_7_Grip 162x206 -> 121x154. Dance hands use the Open / Point /
  Relaxed rows above. Old scale was 1.7 = 70% oversize vs the
  gauntlet fist footprint on canvas (82 wide x 100 tall) for Hand_1
  at the old size; Mars's ordered fix is 25% down from 1.7, not a
  re-measure to fist size — the 1.275 size is what Mars ordered,
  recorded here as ordered, not as "matched to fist".
- DO NOT TOUCH, DO NOT SCALE: dance top-row base-fist grooves a, b,
  c (correct as-is); library old original default fists (perfect
  as-is). Those tiles appear in the contacts as UNTOUCHED, not as
  new files.
- Dance poses are NOT T-poses (groove-a/b/c, diagonal and folded
  arms), so their fingers-up gesture is kept (angle 0) — the
  flatten rotation applies on the T-pose only. Dance hands get the
  scale-down and the Arm1 mirror, not a flatten rotation. Do not
  silently change a dance pose that is not a T-pose.

## 6. Serve replacement, not overlay (2026-10-31 19:39 + 19:39:51 CDT)
- Serve = JEI-01 crusher serve open palm, plain and ball versions.
- Arm: Arm1 (L arm top, per build_wrist_fixes doc). So the Arm1
  horizontal in-place mirror applies here too; Arm2 rule would have
  left it alone, but this is Arm1, so it is mirrored.
- Orientation was already correct and is kept: arm direction
  D = (-0.263, 0.965), hand angle = angle_for_direction(D) = 164.8
  degrees, scale 1.0 (the 25% list named dance + library only).
- Position was not correct, fixed by REPLACEMENT in v3 (v1 and v2
  were discarded before Mars saw them — v1 used a 160px disc that
  ate a wedge out of the torso/cape; v2 used wrist-inside placement
  that left a visible gap to the cuff): the original fist is erased
  ENTIRELY — all alpha in the tight fist rectangle x200-365,
  y475-610 (3,730 base alpha px erased; torso/cape starts at x~397,
  alpha difference in x>=380 is 0), not near-white only (the old
  overlay method left grey fist remnants). Then the mirrored open
  hand is pasted with its CENTRE exactly at the fist centre
  (314, 530) — literally "where the fist is", not 19px south of it
  as the old wrist-inside placement was. Hand wrist lands at
  (331.6, 474.6), 11.3px from the cuff bottom, so the hand meets
  the gauntlet with no gap. Finger direction (-0.252, 0.968) along
  the arm axis D = (-0.263, 0.965).
- Fist pixels remaining in the erased rectangle, outside the new
  hand mask: 0. The hand is NOT overlaid over a fist; there is no
  fist under it. A 310px cuff rim in y465-475 above the rectangle
  is the preserved gauntlet cuff, not fist — it is intentionally
  kept, and the hand's wrist sits against it.
- Honest numbers on the gate, plainly: wrist-to-fist-centre is
  58.1px, because the fist centre is not the wrist anchor (the
  hand's own wrist-to-centre distance is 58.2px by construction).
  The old wrist gate (d_wrist <= 30px to the fist centre) does NOT
  apply to a centre-matched replacement — measuring it that way
  would force the hand back off the fist. Wrist-to-cuff-bottom is
  11.3px, which is the anatomically correct anchor, and PASS.
  Open hand is longer than the fist (141px vs ~100px), so its
  fingertips reach to y~595 vs the fist's ~560 — that is the hand
  piece's own length, not a placement error.
- Ball version: orb re-applied over the NEW palm centre (314, 530),
  colour (255,230,110) with (255,250,220) centre, AFTER the fist
  was removed, never over a fist. Mars said even an overlay would
  be perfect; replacement is the instruction, and replacement is
  what was built.

## 7. No-crop window (standing 2026-10-31 19:22 CDT)
- Transparent background, canvas fits the full figure, no clipping.
- T-pose canvas expanded to 1500x1500 with x-offset +200 (on the
  original 1100-wide canvas a true T-pose would clip: left hand tip
  near x -34, right hand tip near x 1134). Dance 1100x1500, serve
  1100x1500 (original plates).
- Gate on transparent plates: no alpha touches a canvas edge.
  T-pose 7/7 PASS, dance 9/9 PASS, serve plain + ball PASS.
  Example T-pose bbox (Hand_1): (151, 253)-(1347, 1311) inside 1500.

## 8. What is still owed
- Mars approval for the whole combined set: 0/1 (this folder, all
  items together — do not deliver a version missing any one).
- Dance scale question from the original task is now ANSWERED by
  Mars's 25% order (1.275) for dance — no longer open, but approval
  of the result is still 0/1.
- Wiring check_wrist_attach (with the mirrored registry) as a
  mandatory pre-delivery step in the main builders: still owed, not
  done here (the gate was run here, not wired into main builders).
- No repo push made for this folder (landing workstream scope).
- Superseded intermediate: the first T-pose builder
  (build_tpose_flatten.py, scales ~0.82-1.04, no mirror) was killed
  before it finished (6/7 flattened, grip flattened missing) and is
  NOT the deliverable. The FINAL files are the ones from
  build_combined.py, with the mirror and 1.275 scale.
