# ARM ALIGNMENT RULE (Mars, 2026-10-31 16:31 CDT — Arm2 was NOT lined up correctly)

Elbow -> wrist -> fist must stay on ONE column. A substituted fist/cuff must be
re-centred on that column, never pasted at its source-image coordinates, and a
foreshortening warp must never shear the column.

## Diagnosis that named it (measured, not eyeballed)
Source: v7c Arm_Back_Lower (158x288) vs forearm v2 Arm2 (249x215), alpha row-centre fits.
- Reference: forearm axis 4.1-4.8 deg from vertical, fist-minus-forearm offset -6.3 px.
- BAD v2 Arm2: forearm+cuff axis 23.3 deg (manual band) / 19.8 deg (QC band) — 5x the
  reference. Centreline drifts +34 px over y10-90, then the fist snaps back:
  fist centre 180.5 px vs forearm axis extrapolated to fist height 206.7 px = -26 px kink.
  The wrist cap floats ~35 px left of the axis, on the left edge of the cuff, not on the wrist.
  The cuff/gauntlet long axis is tilted with the shear, its panels diagonal.
- Why Arm1 looked "a bit better": its v2 piece is also sheared (12.4-16.8 deg), but its
  fist FOLLOWS the shear (offset delta vs its reference only +0.7 px), so it reads tilted
  but intact. Arm2's fist does NOT follow — broken column, hence "really bad".
- My first v3 attempt repeated a related error: placing segments by crop centre instead
  of art centre (original crop has ~32 px transparent left margin) put the forearm art
  19 px right of the fist. Fixed by art-centre correction (-19 px on shaft/cuff only).
- FIXED v3: forearm axis 5.6 deg (delta +0.8 deg vs reference), offset delta +4.8 px.
  QC verdict PASS. Fist is the original Back fist, unflipped, unrotated, cap behind fist.

## Pipeline gate — 100% (no arm piece ships without it)
Run for every new arm piece, against its v7c reference:
  python3 check_arm_alignment.py --piece <new.png> --reference cut-limbs-v7c/Arm_Back_Lower.png
  (Arm_Front pieces use Arm_Front_Lower.png as reference)
PASS requires BOTH: |axis-angle delta| <= 10 deg AND |fist-minus-forearm offset delta| <= 10 px.
FAIL = do not ship, do not show as fixed. Bands: forearm y 5-55%, fist y 60-98% of height,
so v7c lowers and foreshortened pieces use the same rule.
Absolute symmetry is NOT the test — a fist naturally sits off forearm centre by its
thumb-side asymmetry (Back -6.3 px, Front +20.8 px). The test is DELTA vs reference.

## Foreshortening construction (correct method, from this fix)
Shorten ONLY the shaft between elbow and cuff. Cuff and fist (closest to camera) stay
at full size. Stack all segments centred on ONE axis by ART centre, not crop centre.
Wrist cap centred on the axis, drawn BEFORE the fist, so only a small arc peeks.
