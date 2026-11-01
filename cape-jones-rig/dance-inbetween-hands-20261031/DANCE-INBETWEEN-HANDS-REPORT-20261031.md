# Dance with in-betweening AND different hands — 2026-10-31

## Owned plainly
Mars, 2026-10-31 21:22 CDT: you never showed him any of the dances
with the in-betweening or with the different hands, like the work
got lazy and skipped all that. Owned: pieces existed separately —
dance recreations A (217f) + B (215f), dance hand set approved
20:21 CDT, T-pose library approved 20:22 CDT, inbetweened
movements (serve-to-guard v2, punch-to-flex v2, roll-call v2) —
but a dance combining in-betweening AND different hands together
was never shown. This folder is that dance, built from scratch
as a new clip. No old dance overwritten, no existing file overwritten.

## What was built
Base: SQUAT SQUAT SHUFFLE OOGA BOOGA THREE QUARTER TURN AND THEN
FORWARD FACE (Mars-named dance move, pseudo-turn base).
Expanded here to 7 keys, 37 frames, intended 12fps, 3.08s.
- 7 keys, 30 inbetweens, 5 inbetweens per interval.
- Inbetweening is REAL: every inbetween frame is a fresh rig
  render from smoothstep-interpolated rig angles (arm_upper,
  arm_lower, leg_upper, leg_lower) + head tilt. No crossfade,
  no whole-picture blend, no pixel shear.
- 3/4-turn squash (width only, 1.0 -> 0.62 -> 1.0, centred,
  height and feet unchanged) applied only across the turn keys
  (f18 -> f30, peak at f24), exactly as the pseudo-turn base.
- Hands are drawing substitutions: a hand changes ONLY at a
  key frame, never blended or morphed mid-interval. Inbetween
  frames carry the outgoing key's hand while the body moves.
  Both sides use the same hand per pose (L = Arm1, mirrored
  horizontally in place; R = Arm2, unchanged). Scale 1.275
  (0.75x of 1.7), wrist-anchored. Vertical flip in place: hand
  layer only, flipped top-to-bottom, wrist re-seated to the
  SAME wrist target; body/arms/gauntlets/head/legs NOT flipped.

## Per-pose table (hand + inbetween count)
| Frame | Pose | Hand (both sides) | Flip | Inbetweens after it |
|---|---|---|---|---|
| f00 | K0 SQUAT 1 | 1 Fist | VERTICAL FLIP IN PLACE | 5 (f01-f05) |
| f06 | K1 SQUAT 2 (deeper) | 7 Grip | VERTICAL FLIP IN PLACE | 5 (f07-f11) |
| f12 | K2 SHUFFLE | 5 Point2 | VERTICAL FLIP IN PLACE | 5 (f13-f17) |
| f18 | K3 OOGA BOOGA | 3 Open | VERTICAL FLIP IN PLACE | 5 (f19-f23) |
| f24 | K4 THREE QUARTER TURN | 4 Point | VERTICAL FLIP IN PLACE | 5 (f25-f29) |
| f30 | K5 BOOGA BOUNCE | 6 Relaxed | VERTICAL FLIP IN PLACE | 5 (f31-f35) |
| f36 | K6 FORWARD FACE | 2 FistBack | AS-IS, do NOT flip | 0 (end) |
All 7 canon hands used exactly once. Hand 2 is approved 1/1 as
is and was NOT flipped. Flipped hands here are the same
operation as the hand-flips workstream, re-applied wrist-anchored
in this builder; the flipped-hand versions themselves remain
approval 0/1 per hand in that workstream.

## Gates, measured
- Wrist gate: 14/14 PASS (7 keys x 2 sides), d_wrist 20.0px on
  every side, d_wrist < d_tip on every side (d_tip 106.9-175.7px).
  Measured on the unsquashed rig plate; the squash scales the
  whole figure together, so the wrist stays attached in the
  squashed view.
- No-crop gate: 37/37 PASS, no alpha touches a canvas edge.
- Viewed before reporting: GIF (37 frames, verified by PIL),
  7-key contact, and inbetween stills f03 (intermediate squat,
  fist hands) and f21 (mid-way to the turn, open hands, squash
  starting). The GIF read in the tool did not render an animation
  preview to the builder, but its frame count/size were verified
  and the contact + inbetween stills were viewed directly.

## Known mismatches / limits, stated plainly, not hidden
- Hand 3 open, flipped: palm creases are still visible -- it is
  the same palm drawing upside-down, NOT a back-of-hand drawing.
  No back-of-open-hand piece exists in the canon 7.
- Hand 4 point, flipped: thumb ends on the BOTTOM, not the top,
  because hand 4's native thumb is on the opposite side from
  hand 5's. Flipping it again would restore the original.
  Mars still needs to call hand 4: keep flipped (thumb bottom)
  or keep original (thumb top).
- Hand angle is fixed at 0, as in the approved dance FINALs:
  hands do NOT rotate to follow the forearm angle, so on angled
  forearms (e.g. f21) the hand hangs vertically while the forearm
  angles. Wrist attachment still passes; forearm-following hand
  rotation is NOT claimed and is still owed if Mars wants it.
- The turn is the pseudo-turn cheat (squash + rig angles), NOT
  a true side view: no true side torso/head piece exists.

## Files
- dance-inbetween-hands-20261031.gif (37f)
- dance-inbetween-hands-contact-20261031.png (7 keys)
- dance-inbetween-hands-xsheet-20261031.png (frame-by-frame timing chart)
- dance-inbetween-hands-20261031.json (frame table, wrist gates, no-crop)
- frames/f00.png ... f36.png (transparent rig plates) + fXX-view.png (grey views)
- build_dance.py (builder)

## Status
Approval 0/1 for the combined dance. No repo push. No old dance
overwritten. No existing file overwritten.
