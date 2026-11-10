# Leg foot + arm inversion correction — Mars, 2026-10-31 10:18 CDT (v3 -> v4)

LEG, Mars was right, plainly:
- Screen-right leg = character's left leg. Its foot/toes were cut off
  by MY original zone, not by the sheet. Zone ended at sheet x=1935.
  Clean component detection on the full sheet finds that leg at
  [1772,332,1979,963] — foot extends to x=1979, 43px beyond my zone,
  1,108 pixels of toe in the foot y-range. That is the square-crop
  cut Mars saw.
- Fix, no new square crop: re-sliced by component (slice_clean.py,
  sheet finds the piece), then grafted only the missing toe back onto
  the ORIGINAL Leg_Back PNG (Leg_Back_GRAFTED.png, width 168 -> 228),
  so the shin stays the original, not a replaced clean leg. V4 feet
  show both toes complete and rounded.
- Left leg was not toe-cut (its toe points left, inside its zone).

ARMS, Mars was right, v3 did not invert them correctly:
- V3 right arm was Arm_Back flipped + rot -90 — wrong piece/orientation,
  not a true inversion of the left arm.
- V4 arms are both from the SAME Arm_Front piece, inverted as a pair:
  screen-left = Arm_Front flipped top-to-bottom then rot +90,
  screen-right = Arm_Front no flip then rot +90.
  Result, symmetric: shoulder inner / fist outer both sides,
  gauntlet pads on the BOTTOM (bottom of forearm facing down, as Mars
  said), fists knuckles-up, thumbs down both sides.
- If Mars meant pads on TOP (like the T-pose reference, pads on top),
  that is a single vertical flip of BOTH arms from v4 — say "pads top"
  and do not let me guess again.
File: assembly-preview-v4-20261031.png, v1/v2/v3 NOT overwritten.
Head lowered (v3) and cape layers (v2) unchanged in v4.
