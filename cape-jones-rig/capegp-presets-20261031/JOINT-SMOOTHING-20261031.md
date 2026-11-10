# CapeGP joint smoothing — JOINT_SMOOTH preset

**Goal, in Mars's words:** CapeGP should help smooth out where the joints
attach and everything, so a joint does not read as a hard action-figure
ball or a seam break in motion. This preset is a first, measured step on
that goal, not a claim that joints are finished.

## What was actually built
- JOINT_SMOOTH = TRUE_FINAL flex, dip 28px, same layers as APOSE_FLEX
  (NormalArm 6, Head 1, Neck 1, Torso 3, Collar 1, Legs 6, CapeBack 1),
  but every stroke polyline passed through **Chaikin corner-cutting x2**
  (Q = 0.75·P + 0.25·next, R = 0.25·P + 0.75·next, closed ring, re-closed).
  Implemented in `build_capegp_presets.py` (`chaikin()`), run on traced data.
- Why Chaikin and not a taper: GP strokes here are OUTLINES. A filled-
  silhouette taper (clean_joints.py corridor taper) clips silhouette pixels
  outside a limb corridor — that operation has no meaning on an outline
  polyline, and shrinking the outline would move the line, not smooth it.
  Chaikin is the correct outline operation: it rounds the approxPolyDP
  corners without moving the stroke's overall path. That distinction is
  stated here so the next pass does not apply the wrong tool.

## Measurements (traced data, APOSE_FLEX vs JOINT_SMOOTH)
- Total stroke points: 631 → 2,467 (Chaikin doubles points per iteration,
  631 × ~4 = 2,524, minus closure handling = 2,467; expected, not an error).
- Mean turn angle per segment (roughness): 48.33° → 12.16°, **−74.8%**.
  A lower mean turn = a smoother polyline, fewer jagged contour steps.
- Max turn angle: 180.0° in both — this is the closure point
  (last point = first point, direction reverses by construction), not a
  real corner. It is reported so nobody quotes "max 180°" as a failure.
- Stroke bbox: APOSE_FLEX x −3.33..3.64, y −5.78..5.14;
  JOINT_SMOOTH x −3.31..3.63, y −5.78..5.12 — the smoothed path stays
  within 0.02 Blender units of the unsmoothed path. Smoothing did NOT
  move the figure or shrink it.
- Honest limit: Chaikin smooths the CONTOUR, it does not remove the
  ball-cap seam between upper and lower pieces, and it does not taper a
  joint. In motion, the joint still reads as two overlapping outlines
  meeting at a ball centre — smoother outlines, same joint construction.
  A true joint de-balling pass (tapered piece ends, cap omission at
  build time) is the later pass already documented in joint-cleanup, and
  it applies to filled poses, not to outline-only GP. Do not present
  JOINT_SMOOTH as "joints cleaned" — it is "outlines smoothed".

## Joint-cleanup method reference (read, not re-run here)
`joint-cleanup-20261031/clean_joints.py` — tested on COPIES only, ready
for later, never applied to approved poses in place:
1. Speck removal (<40px detached components).
2. Seam masking (cap masked to limb union, dilated 3px).
3. Corridor taper (ball-to-taper, PCA axis, median cross-section).
4. Cap omission at build time (upper + lower overlap, no ball drawn).
Wrist polish from that work removed 12/0/0 px on 3 flexes and was visually
indistinguishable — the recommendation there was to keep the good-enough
approved versions. That caution applies here too: smoothing is a preset
to test, not a replacement for an approved pose.

## Before / after in motion
- Proof renders: preset-0002.png (APOSE_FLEX, unsmoothed) vs
  preset-0006.png (JOINT_SMOOTH, Chaikin x2) — same pose, same layers,
  only the stroke polylines differ. View both side by side; the difference
  is subtle at 550×750 (contour steps are small) and that subtlety is
  honest — Chaikin is a refinement, not a redesign.
- Motion context: the original GP motion (apose → mid → true-final → hold,
  depth package) is the motion this smoothing would apply to next. A
  smoothed motion sequence (all 4 motion frames through Chaikin) is still
  owed — this preset proves the method on one frame first, per the
  staged/prototyped/tested-here-first plan.
- Seam / gap pixels: NOT measurable on outline-only GP renders in the
  same way as on filled poses (there is no filled silhouette to count
  gap pixels in). No gap-pixel number is claimed here; the numbers above
  (point count, mean turn, bbox) are the measurable ones for outlines.
  Claiming a gap-pixel improvement on outlines would be fake precision.
