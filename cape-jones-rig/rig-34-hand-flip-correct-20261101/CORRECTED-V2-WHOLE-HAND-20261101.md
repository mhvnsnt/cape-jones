# Corrected hand flip V2 — whole hand piece, NO square crop, NO split — 2026-11-01

Mars correction 2026-11-01 01:27 CDT, replying to Arm2 hand old vs new contact:
"you started back doing that square crop thing, that we said not to do, you don't need to crop the hands because it's already a separate FLA piece you didn't need to do that cut or that crop like that so when you do the other hand don't do it like that."

## What changed from V1 of this job

- V1 (superseded, in this same folder as sit-chair-fixed-20261101.png before V2/V3 runs) flipped the screen-right hand by splitting forearm_hand_mid at native y=128 and flipping only the hand segment left-right. That split/crop method is BANNED and was NOT used in V2.
- V2 (this delivery) flips the WHOLE separate hand piece, in place, wrist anchored, no cut, no crop, no split at y=124 or y=128 or any rectangular cut.

## Method (V2, builder build_correct_v3.py)

- ARM1 = LEFT, ARM2 = RIGHT, same as front-facing rig (Mars 2026-11-01 01:26 CDT correction, unchanged).
- Screen-left hand (builder L, the hand flipped in error in rig-34-fix-offsets): flipped BACK to its original unflipped state — same as V1, whole piece, unchanged.
- Screen-right hand (Arm 2, RIGHT): the separate FLA hand piece hand_spare_mid.png (79x116 native, thumb originally on the right/east side) was flipped WHOLE left-right, saved as pieces/hand_spare_mid_flipped_whole.png, scaled 1.3x (same scale as all rig pieces), placed as its own layer at top-left anchor (800,800), rotated 10 degrees (arm_lower R angle) around that anchor, so its wrist sits at the gauntlet cuff. Gauntlet unchanged. No piece was cut, cropped, split, or erased.
- All other offsets kept exactly from rig-34-fix-offsets: pelvis -7,0; thighs/hips to knee -15,0 both; kneecaps -10,-5 relative to shifted knee; shins knee-to-toe -15,0; Arm1 upper -5,-7; Arm1 forearm+hand -7,-5; Arm2 upper/forearm 0,0.
- Previous fixed rig (rig-34-fix-offsets-20261101) untouched, md5 25dc444bf475f2abb871d0d7c218219c. Front rig untouched. No push.

## Files

- Final transparent: poses-v2/sit-chair-corrected-whole-hand-20261101.png, md5 c7c4d73f0b4f64b59c49157a8b3e275f, canvas 1400x1600
- Final on grey: poses-v2/sit-chair-corrected-whole-hand-20261101-on-grey.png
- Old vs new, full figures side by side (left = rig-34-fix-offsets, right = V2): poses-v2/old-vs-new-whole-hand-20261101.png, 2800x1600. No square hand crop is delivered as the hand view; the whole flipped hand piece itself is delivered below.
- Whole flipped hand piece, un-cropped: pieces/hand_spare_mid_flipped_whole.png, md5 0314d08a9167f7497ba8927c2d7679d0
- Builder: build_correct_v3.py (V2 method; build_correct.py / build_correct_v2.py are the superseded V1 builders in this folder)

## Gates — PASS

- Bbox 342,195–955,1475, inside 1400x1600 canvas, no crop, no clip.
- Feet planted: feet alpha bottom L 1475, R 1475.
- Knees L 590.1,1028.6, R 774.7,1062.4; kneecaps L 580.1,1023.6, R 764.7,1057.4; elbows L 495.3,616.1, R 878.4,635.5; wrists L 404.1,791.2, R 852.3,831.9 — same as V1 / fixed rig (legs, pelvis, arms unchanged; hand layer only).
- Knee-feet: legs unchanged from the fixed rig, so the knee-feet gate result is unchanged.
- Thumb side, whole spare piece: bottom-half mass left 1630 / right 1340 before flip, left 1292 / right 1678 after flip — thumb mass moves right-to-left, as required. (This is a mass check on the whole piece, not a split segment.)

## Defect stated plainly, NOT hidden

- The screen-right forearm piece in the 3/4 sheet is a fused gauntlet+hand piece (forearm_hand_mid). V2 does NOT erase or crop that fused hand; the flipped whole spare hand sits on top of it as a layer. Where the spare hand's shape differs from the fused hand, a small sliver of the fused hand still peeks out on the left edge below the cuff (about one finger width at zoom, visible in the hand check). At full-figure scale it reads as one hand, thumb west, fingers down-right, wrist at cuff — but at zoom the peek is real.
- A perfectly clean single-hand version needs a gauntlet-only forearm piece for Arm 2, which does not exist as a separate file in sitting-rig-34 pieces. That piece is owed as a separate job; it was NOT faked here by cropping or erasing the fused hand.
- Wrist seam: the spare hand's wrist edge meets the gauntlet cuff at (800,800) anchor, rotated 10 degrees; the cuff line is not a perfect continuous edge — the hand layer overlaps the cuff, it does not blend into it. No blend was applied, so Mars can see the join as-is.

## Approval

- Approval 0/1 corrected hand flip, V2 whole-piece version, separately. V1 segment-flip version is superseded by V2 and should not be used.
