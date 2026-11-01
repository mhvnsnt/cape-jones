# Arm + head correction — Mars, 2026-10-31 10:15 CDT (v2 -> v3)

1. Head lowered "just a little" to attach to neck: Head_Front top
   200 -> 230 in the 1100x1500 assembly canvas (30px down). Head bottom
   now 393, neck top 360, overlap 33px — jaw sits on the neck cylinder,
   no gap. Neck and cape layers unchanged from v2.
2. Arms swapped AND flipped, not just swapped: v2 was screen-left =
   Arm_Back rot -90, screen-right = Arm_Front rot +90.
   V3 is screen-left = Arm_Front flipped top-to-bottom then rot +90,
   screen-right = Arm_Back flipped top-to-bottom then rot -90.
   Why the flip matters, tested: swap-only (v3a, discarded) puts the
   gauntlet pads on TOP and the fists upside down (knuckles down).
   Swap+flip (v3b, shipped) keeps shoulder inner / fist outer, with
   gauntlet pads on the BOTTOM and fists knuckles-up, on both sides.
   That is the "bottom facing down" reading used for v3.
   If Mars meant arms down at his sides (not out in T-pose), that is a
   different pose, not a flip — say so and v4 will be an A-pose, not
   another T-pose rotation.
File: assembly-preview-v3-20261031.png, v1/v2 NOT overwritten.
