# Forearm / fist V3 — front-facing fist fix + Arm2 clean redo (2026-10-31)

## What was wrong (verified by viewing the V2 proof)
V2 proof panels 1-2 (V1 forearm, V2 Arm1): wrist at the forearm, knuckles facing
forward/down at the strike edge — correct, and Mars approved those two.
Panel 3 (V2 Arm2 different-angle fist): fingers UP, wrist cuff at the BOTTOM,
forearm above it — the fist is flipped 180 degrees against the forearm axis.
That is the upside-down fist Mars rejected. It is NOT approved.

## Fist source search — found / not found
- SEARCHED: sliced/Hand_1..7, pack1/Hand_1..13, sliced-clean group folders,
  cape-jones-flying sheet names, rig docs mentioning fist.
- FOUND (in-repo, his own rig): sliced/Hand_1_Fist.png — the good front-facing
  fist: 4 knuckles in descending arc, thumb wrapped ACROSS the front of the
  index/middle fingers, wrist cuff at the back. This is the base for V3.
- NOT FOUND: no separate "animated thing / saturation" fist file, and no
  additional front-facing fist beyond the 7 sliced hands. If Mars has that
  image elsewhere, name the file/folder and it replaces this base in V4.

## Industry-standard fist construction wired (methods, not copied art)
1. Knuckle order: index highest, then middle, ring, pinky descending — never flat.
2. Thumb wrap: thumb crosses the FRONT of the fingers, never behind, never on
   the wrong side. Arm2 (back arm): thumb on the image-left after orientation.
3. Wrist = attachment end, knuckles = strike end. On a foreshortened punch arm
   the knuckles sit at the strike edge (bottom of the piece), wrist at the
   forearm — the same orientation as the approved Arm1/Arm2 standard fists.
4. Wrist cap BEHIND the fist: only side arcs peek, never a ring across the
   fist face. Old fist fully erased below the cut (y=88) — no peek-through,
   no double fist.
5. Clean: largest-component filter (disconnected shards removed), interior
   black arc lines inpainted to fist colour (outlines kept, since outline
   pixels have a transparent neighbour).

## Files
- fist-front-facing-v3-20261031.png (150x182, upright: knuckles top, wrist bottom)
- forearm-v3-arm2-front-fist-20261031.png (249x240, new fist seated 22px into
  the wrist, cap behind, knuckles at strike edge, thumb left)
- forearm-v3-arm2-standard-clean-20261031.png (249x215, shard removed, cap arc softened)
- forearm-v3-arm1-clean-20261031.png (241x216, light clean pass, cap arc softened)
- proof-v2-vs-v3-fist-20261031.png (viewed)

## Honest residuals (not hidden)
- V3 Arm2 front-fist: the rotated fist's cuff still shows a small white block
  at the wrist-right (the cuff is wider than the forearm). It is the new fist's
  own cuff, NOT leftover old fist — the old fist was cut at y=88. It reads
  cleaner seated 22px deep, but a redrawn cuff matched to the gauntlet would
  remove it fully; that is a V4 polish item if Mars wants it.
- Standard pieces: the wrist joint ball remains (v7c joint language, not a
  defect I invented), and the cap arc is softened to a faint dotted line,
  not fully erased — erasing it fully would cut the fist outline.
- Pose integration of the new front fist into a full punch pose: still owed.
- Mars approval: 0/1. V2 diff-fist stays REJECTED.
