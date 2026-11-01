# Knee-Feet Fix — Improved Dance (Mars, 2026-10-31 16:09-16:10 CDT)

## Rule (standing, in Mars's own one sentence)
YOUR KNEES AND FEET ARE ALWAYS POINTING IN THE SAME DIRECTION.
If his kneecaps start to go inward, his toes need to go inward as well.
Exception only: unless his legs get broken or something.
Full rule doc: ../KNEE-FEET-RULE.md (already existed in the rig root; research
and fix method appended there, not overwritten).

## Problem named properly
Knee-foot misalignment / valgus tracking failure: genu valgum (knock-knee,
knees collapse toward the midline) + external tibial rotation (shin twists
outward, foot points out while the knee points in). Industry rule behind it:
the tibia tracks over the 2nd toe; foot progression angle must match the
knee's hinge plane; internal tibial rotation sends toes inward, external
rotation sends toes outward. The knee is a hinge — it cannot bend sideways —
so a knee-in / toe-out pose reads as broken knees, like someone hit him in
the knees with a baseball bat (Mars's words, and the read is correct).

## What was fixed
- Improved dance, 63 frames rebuilt from its builder (fix_dance.py, same
  rig/config as dance-improved-20261031/build_dance.py).
- FootIn lower pieces (pieces/): whole-piece horizontal mirrors of
  Leg_Front_Lower (toe left -> right, knee anchor 95 -> 59) and
  Leg_Back_Lower (toe right -> left, anchor 100 -> 127). Shin/knee position
  does NOT move; the foot is substituted on its axis, like the gauntlet/fist
  roll rule. Ankle joint intact, no detached feet. Trade, stated honestly:
  mirroring the whole lower also mirrors its calf shading side. A
  hand-drawn inward-foot lower (shading-perfect) is still owed if wanted.
- FootIn ON for frames 15-55 (27 rendered frames: groove + kick segments,
  knees inward). FootIn OFF for frames 1-13 and 56-109 (knees outward,
  original toes outward = matching). Swap happens on keyframes 15 and 56 —
  a drawing-substitution pop, stated, not hidden.

## Verification (viewed, at foot level — not just full-figure scale)
- f042 kick, foot-level crops: BEFORE left toe left / right toe right
  (splayed outward). AFTER both toes point down toward the midline.
  Fixed, verified.
- f015 groove, foot-level crops: BEFORE left toe left / right toe right
  (splayed outward). AFTER feet together, toes pointing down-left together
  (crossover direction, no outward splay). Fixed for the named defect.
  Honest note: in this crossed pose the fixed feet point together in the
  crossover direction, NOT pigeon-toed at each other (left toe right +
  right toe left) — pointing them at each other in a crossed step would
  twist both ankles and read more broken, not less. If Mars wants
  pigeon-toed there, that is a further variant to build, not a failure
  of this fix.
- Full fixed contact sheet (8 keyframes) viewed; no detached fists/feet
  in the keyframes. GIF built from all 63 fixed frames, not viewed
  frame-by-frame (same as the original clip's viewing status).

## Files
- frames/dance-kneefeet-f001..f109.png (63 frames, transparent)
- dance-kneefeet-contact-20261031.png (8 keyframes)
- dance-kneefeet-before-after-20261031.png (f015 + f042, before/after)
- dance-kneefeet-20261031.gif (63 frames, 80ms) + .mp4 (phone-playable)
- pieces/Leg_Front_Lower_FootIn.png, Leg_Back_Lower_FootIn.png
- fix_dance.py (builder)

## Still owed (not claimed done)
- Mars approval of this fix: 0/1.
- Combine dance (108 frames): SAME defect audited in its groove pose
  (contact sheet pose 2, legs crossed, feet splayed outward). NOT fixed
  here, honestly: that clip has no builder script in its folder, so it
  cannot be rebuilt from rig config the way this one was. Fixing it needs
  either its builder located/reconstructed, or a new combine-dance build
  with the FootIn rule applied. Do not report combine as fixed.
- Hand-drawn (non-mirrored) inward-foot lowers, if shading-perfect
  pieces are wanted: 0/2.
- Applying the knee-feet check to walk, kick, flex, fight poses generally:
  rule is written in KNEE-FEET-RULE.md; retro-checking those poses is 0/4
  pose families.
- Repo push of dance-kneefeet-fix-20261031/ via the parent PR route.
