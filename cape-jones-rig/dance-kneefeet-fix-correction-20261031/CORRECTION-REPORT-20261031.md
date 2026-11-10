# Knee-Feet Fix CORRECTION — Improved Dance (Mars, 2026-10-31 16:58 CDT)

## What Mars flagged, in his words in substance
Top row, third frame of dance-kneefeet-contact-20261031.png: his feet are
supposed to be pointed OUTWARD because his knees are pointed OUTWARD.
The v1 fix pointed his feet inward on a frame where his knees are outward.
That frame is incorrect and must be fixed. The rule, both ways:
knees outward -> feet outward; knees inward -> feet inward.
Everything else in that contact sheet was good.

## Identification — the flagged frame is f028, Groove A
- Contact-sheet keyframes are 1, 15, 28, 42, 56, 69, 83, 97 (4 per row).
- Top row third = **f028 = Groove A**: leg_upper L -15, R +15 (thighs splayed,
  knees outside the hips, kneecaps outward).
- V1 fix had FootIn ON for f028 (block range 15-55), so its feet met inward
  at the centre. Wrong direction, fixed here: f028 now uses original lowers,
  feet apart and pointing outward, matching its outward knees.
- Foot-level proof for f028 is in dance-kneefeet-corrected-foot-crops-f028-20261031.png:
  left = v1 (feet together, toes inward), right = corrected (feet apart,
  left toe down-left, right toe down-right).

## Why the v1 fix was wrong — the block range, not one frame
V1 used FootIn ON as a BLOCK for frames 15-55 (groove + kick stretches).
Knee direction changes inside that stretch: Stride B is inward, Groove A is
outward, Groove B is inward, Kick is outward. A block therefore flips
outward-knee frames inward (the Mars complaint) and misses inward-knee
frames before frame 15. This correction replaces the block with a
PER-FRAME rule, read from that frame's own rig angles:
  FootIn = True  ONLY IF  leg_upper L > 0 AND leg_upper R < 0
  (both thighs angled toward the midline = both kneecaps inward)
  otherwise False (original lowers).
This is the thigh-angle sign, not knee-x minus hip-x: at rest the thigh
piece already sits slightly inboard of the hip, so x-offset alone misreads
straight legs as inward. The angle sign is the kneecap direction Mars
judges by eye.

## Per-frame audit — all 63 rendered frames (see per-frame-audit-20261031.csv)
- FootIn ON in the correction (14 frames): 9, 11, 13, 15, 17, 19, 21,
  36, 38, 40, 42, 43, 44, 45. All have both knees inward by the rule above.
- FootIn OFF (49 frames): every other rendered frame, knees outward or
  straight, original feet.
- CHANGED vs actual v1 rendered state: 20/63 frames.
  * Flipped back OUTWARD (v1 had them wrongly inward, 17 frames):
    23, 25, 27, 28, 30, 32, 34 (Groove A stretch, knees outward),
    46, 47, 48, 49, 50, 51, 52, 53, 54, 55 (Groove B -> Kick transition,
    knees uncrossing to outward).
  * Newly flipped INWARD (v1 missed them, block started at 15, 3 frames):
    9, 11, 13 (Stride A -> Stride B transition, knees had already crossed
    inward; these are NOT contact-sheet keyframes and were not flagged by
    Mars, they are a disclosed consequence of the per-frame rule, not a
    silent change).
  * UNCHANGED (43 frames), including every other contact-sheet keyframe:
    f001 OUT/OUT, f015 IN/IN, f042 IN/IN, f056 OUT/OUT, f069 OUT/OUT,
    f083 OUT/OUT, f097 OUT/OUT.
- Audit note, stated plainly: the builder's first-pass audit listed f015
  and f056 as changed because it used the first segment's FootIn flag for
  shared endpoints. In v1's actual rendered frames, endpoints are
  overwritten by the next segment, so v1 f015 was already FootIn and v1
  f056 was already original. Both are UNCHANGED in this correction; the
  CSV was corrected to match the actual rendered state.

## Contact-sheet keyframe audit (8/8 pass in the correction)
| Frame | Pose | Knees | Feet (corrected) | Verdict |
| 1 | Stride A | OUT | OUT | pass |
| 15 | Stride B | IN | IN | pass |
| 28 | Groove A | OUT | OUT | pass — THE CORRECTED FRAME |
| 42 | Groove B | IN | IN | pass |
| 56 | Kick | OUT | OUT | pass |
| 69 | Split | OUT | OUT | pass |
| 83 | Twist | OUT | OUT | pass |
| 97 | Arms-up | OUT | OUT | pass |

## Anatomy study (both directions — the lesson Mars ordered)
- The tibia tracks over the 2nd toe in EITHER direction: internal tibial
  rotation sends toes inward, external tibial rotation sends toes
  outward. Foot progression angle must match the knee's hinge plane.
- Valgus (knee-in / toe-out) and varus (knee-out / toe-in) are BOTH
  misalignments. The knee is a hinge; it cannot bend sideways, so ANY
  knee/foot direction mismatch reads as a broken joint, whichever way it
  points. That is why "always inward" creates the same broken read in
  reverse, and why the rule is bidirectional.
- Fix method unchanged from v1 (and still the gauntlet principle):
  transverse rotation in 2D is drawing substitution, not limb movement.
  Shin/knee position does not move; the whole lower-leg piece is swapped
  (original <-> FootIn mirror, knee anchor re-mapped: Front 95 -> 59,
  Back 100 -> 127), ankle intact, no detached feet. Mirroring also mirrors
  calf shading — the same honest trade as v1; hand-drawn inward-foot
  lowers (shading-perfect) are still owed 0/2 if wanted.
- Rule doc updated (append only, v1 text untouched):
  ../KNEE-FEET-RULE.md, "CORRECTION 2026-10-31 16:58 CDT" section,
  with the bidirectional rule and the per-frame gate. A block range with
  no per-frame table now FAILS the gate.

## Verification (viewed by me)
- Corrected contact sheet (8 keyframes) viewed: top row third now shows
  feet apart/outward, matching its outward knees; all other keyframes
  match v1's good frames.
- Before/after sheet viewed: top row = v1, bottom row = corrected, for
  f028 (changed), f042 (unchanged control), f015 (unchanged control).
  Only f028 differs, as it should.
- Foot-level crops for f028 viewed (see above): v1 inward vs corrected
  outward is unmistakable.
- No detached fists/feet in the viewed keyframes. GIF built from all 63
  corrected frames (80ms, 275x375) — not viewed frame-by-frame, same
  viewing status as the original clip. MP4 conversion was attempted and
  is NOT shipped: the first attempt produced a 0-byte file and the
  concat attempt produced a 0.12s file, both deleted, not claimed.
  GIF is the delivered clip; MP4 can be re-encoded from the frames folder
  by the parent if a phone-playable MP4 is needed.

## Files (new dated folder, v1 fix folder untouched)
- frames/dance-kneefeet-corrected-f001..f109.png (63 frames, transparent)
- dance-kneefeet-corrected-contact-20261031.png (8 keyframes)
- dance-kneefeet-corrected-before-after-20261031.png (v1 top / corrected
  bottom: f028, f042, f015)
- dance-kneefeet-corrected-foot-crops-f028-20261031.png (foot level, f028)
- dance-kneefeet-corrected-20261031.gif (63 frames)
- per-frame-audit-20261031.csv (all 63 frames, angles, direction, choice)
- build_corrected.py (builder, per-frame rule in its header)
- pieces/Leg_Front_Lower_FootIn.png, Leg_Back_Lower_FootIn.png (copies of
  v1 pieces, unchanged)
- CORRECTION-REPORT-20261031.md (this file)

## Still owed — not claimed done
- Mars approval of this correction: 0/1.
- Combine dance (108 frames): SAME class of defect audited in its groove
  pose, NOT fixed here — no builder script in its folder (same blocker as
  v1). Do not report combine as fixed.
- Hand-drawn inward-foot lowers (shading-perfect): 0/2.
- Retro-checking the knee-feet rule on walk, kick, flex, fight poses
  generally: rule written, retro-check 0/4 pose families.
- Repo push of this folder via the parent PR route (no commit made here).
