# GROUNDED vs AIRBORNE RULE — 2026-10-31

Mars, 2026-10-31 20:37 CDT, replying to the BARS PRESET final ground proof:
"that is a great job, feet to the ground good, we need to continue doing
that anytime that is necessary unless we have floating or flying, when he
is walking or standing the ground needs to be detected well and his feet
need to be placed, but there are times where he levitates / chases / floats
/ flies, so we need to account for that."

## Standing ground rule (not invented here)
Feet anchor = figure alpha-bbox bottom on a world ground line; scaling and
camera moves grow/move ABOVE that anchor, never from centre.
BARS PRESET proof: screen 1100x750, world 1700x750, world ground line
Gy=700, feet anchor resized figure bbox bottom measured at 653 (not assumed
651), paste y=47, feet=700 every frame, 24/24 frames both variants, feet
centre x in world 849-850 constant ±1px, no-crop gate PASS all 24 frames
both variants.

## New rule from Mars — GROUNDED vs AIRBORNE
- GROUNDED (walking, standing, and any shot that is not labelled airborne):
  ground must be detected well and feet must be placed on it.
  Gate FAILS if feet are off ground in a grounded shot.
- AIRBORNE (floating, flying, levitating, chase/airborne moment):
  feet are NOT forced to ground. That is intentional, and the shot spec
  must label it AIRBORNE, with a stated height / flight line, otherwise
  it looks like a floating mistake.
- Do NOT force airborne poses to ground, and do NOT excuse a grounded
  floating mistake as airborne. A shot that says AIRBORNE but has its
  feet on the ground is a spec mismatch and FAILS: relabel GROUNDED.
- A shot with no mode label FAILS. There is no silent default.

## Gate numbers (ground_gate.py)
- Single ground line: PASS iff |feet_y - ground_y| <= 10 px at full
  resolution. 10 px is a measurement tolerance for anti-alias / LANCZOS
  fringe and dark foot outlines (proof G1: paste feet 700, measured light
  feet 693, offset -7, PASS; diff bbox bottom 699), NOT a licence to float.
- Rug/floor band: PASS iff rug_position in [0.55, 0.95], where
  rug_position = (feet_y - rug_far) / (rug_near - rug_far).
  Portrait: planted 1700 = 0.624 PASS, rug in front 168 px; old 1548 =
  0.284 FAIL, rug in front 320 px.
- AIRBORNE: PASS iff mode is AIRBORNE, height_px > tolerance, and a
  flight line is stated. Height = ground_y - feet_y (stated height in
  the proof: 180 px; measured feet 514, ground 700, measured height 186,
  difference 6 px = the same light-foot fringe).
- Sequence: GROUNDED feet_y spread <= 20 px across the sequence
  (BARS 24/24 spread 0, size walk 44/44 spread 0, size power 54/54 spread 0).
  AIRBORNE height jumps > 25% of figure height = WARNING (jitter reads
  as a floating mistake, not flight).
- Exit codes: 0 PASS, 2 FAIL loudly, 1 input error. A PASS on an
  auto-detected ground line alone is reported as PASS-ESTIMATE, never a
  clean PASS, and the shot spec must confirm the line before delivery.

## What the gate does NOT do
- It does not measure a contact shadow as a hard pass. Shadow is a cue
  only. In the synthetic proofs the 3 px dark ground line itself reads
  as a dark region at gap 6 px, so synthetic shadow numbers are NOT clean
  contact-shadow measurements. The clean contact-shadow example is the
  portrait planted proof: a separate labelled layer, soft black ellipse
  under each foot, 2 clusters, centre ~8 px below the feet, never baked
  into base art.
- It does not invent a ground line for a background it has never seen.
  Auto-detection (detect_ground_line) is an ESTIMATE: synthetic bg
  detected 700 (true line, confidence 0.013 — low, because the line is
  the only edge and the runner-up is close); KKGuh detected 436 with
  confidence 0.155, which is NOT a usable ground line for that room
  (rug far edge 1421 in master coords is the real reference there).
  A low-confidence auto-detect must never override a spec line or a
  rug band.
