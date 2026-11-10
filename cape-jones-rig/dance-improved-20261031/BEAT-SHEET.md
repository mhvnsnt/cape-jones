# Improved Dance Scene — Beat Sheet (Mars, 2026-10-31)
Status: BUILT + VIEWED, NOT APPROVED. Mars approves it. Not a final shot.
Folder: dance-improved-20261031/ — frames/ (63 PNGs, transparent, labels=False),
dance-improved-20261031.gif (63 frames, 275x375, 80ms), dance-improved-contact-20261031.png,
build_dance.py (builder, adapted from joint_locked_rig_v7c.py).

## Spec base
MOCHIICHAO-COMBINE-20261031.md §2 + arms-up reference pose (approved as
arms-up/pre-flex, NOT a flex) + punch-style accent (NOT the locked -110 still file).

## Tempo / grid (24 fps, ~107 BPM)
Beat = 13-14 frames. Beat starts: 1, 15, 28, 42, 56, 69, 83, 97, 110.
Keyframes on twos, except the snap into the kick (42-56) which is on ones.
Holds: split hold 6 frames (56-61, inside the segment), arms-up hold 12 frames
(83-95, inside the twist->arms-up return), final breath hold to 110.

## Phrase (8 beats, frames 1-110, rendered 1-109)
| Beat | Frames | Move | Pose / hand check |
|---|---|---|---|
| 1 | 1-14 | Stride in A->B | Arms swing opposite legs, fists curled, arms NOT up -> original lowers. Bounce 0 -> -6, dx -20 -> +20 (fake-perspective travel). |
| 2 | 15-27 | Stride B -> Groove A | Groove crouch, bounce -14. Fists, arms mid -> original lowers. |
| 3 | 28-41 | Groove A -> Groove B | Hips/shoulders alternate, bounce -8. Original lowers. |
| 4 | 42-55 | Kick beat (SNAP, on ones) | Leg kick + punch-style arm snap (AU -45/90, AL -45/90). Sparkle pops at 42. DEFECT: see below — legs cross, kick not clearly forward. |
| 5 | 56-68 | Split stance, hold 6 | Arms-up anticipation pose, fists curled, arms UP -> FlexOut both sides (cuff tops outward, fist thumbs inward). Bounce -18. Sparkle pops at 56. |
| 6 | 69-82 | Twist beat | Asymmetric arms/legs, FlexOut on the up arm only. JOJO-TENSION gain (1.20,0.70,1.30) on these frames ONLY, returning to base on the hold. Sparkle pops at 69. LIMIT: v7c torso/head are fixed pastes, so no true torso twist is drawn — this is an asymmetric-arms/legs twist stand-in, not a drawn torso twist. |
| 7 | 83-96 | Arms-up hold / anticipation | Approved arms-up pose, FlexOut both sides, bounce -12. Sparkle pops at 83. This is ANTICIPATION, not a flex. |
| 8 | 97-110 | Return / breath | Arms-up -> A-pose rest, bounce to 0. Stamina fade: return is smaller than the twist, per the spec's Endurance fade. |

## Temperament / kawaii layer (as movement data, not creatures)
- Bounce on every beat (walkbob-style, scaled to the beat).
- Sparkle pops on accent beats 42, 56, 69, 83 — flat marker shapes, NOT production VFX.
- Device beep as metronome: NOTED in this sheet only. No beep audio was recorded or built in this clip — audio is a separate, owed step.
- No Mochiichao species on stage. No third-party character, name, dialogue, or logo.

## What was viewed (by the builder, before reporting)
- Contact sheet (8 key frames): dance-improved-contact-20261031.png — viewed.
- Full-res frame 42 (kick) and frame 69 (twist-beat start / split end): viewed.
- GIF: built from all 63 rendered frames, not frame-by-frame viewed.

## Defects found honestly — do NOT ship as done
1. KICK IS WEAK (frame 42): legs cross at knees/ankles and read tangled; the kick leg is not clearly extended forward. The leg-angle signs in front view do not produce a clean forward kick in this rig. Owed: a reworked kick pose (different leg angles, or a foreshortened-leg piece) before this clip is final.
2. TWIST IS A STAND-IN (frames 69-82): torso and head cannot twist in the v7c rig (fixed pastes). The twist reads as an arms-up squat with a colour shift, not a torso twist. Owed: a torso/head twist piece or a 3/4 torso before a true twist ships.
3. JOJO-TENSION SHIFT SHIFTS THE WHOLE FIGURE (frames 69-82): gain applies to cape as well as suit/skin, so the cape goes pink-purple. That matches the demo palette behaviour, but Mars should confirm whether the cape should stay black under a shift.
4. NO DETACHED FISTS in viewed frames: elbow/knee caps hold, fists stay attached in frames 1, 15, 28, 42, 56, 69, 83, 97. That part passed.
5. TRUE FLEX NOT USED: correctly — the arms-up pose is anticipation only. True flex remains 0/1 pending the seam fix, and was not faked here.
6. PUNCH LOCK NOT REUSED AS A FILE: the punch-style accent is a rig config, not the locked -110 across-up still. The locked punch file is a separate approved still.

## Still owed
- Mars approval of this dance: 0/1.
- Reworked kick pose: 0/1.
- True torso/head twist piece: 0/1.
- Device beep audio + sparkle production VFX (Blender, not flat markers): 0/1.
- Background-life pass behind the dance (room/street/forest): 0/1.
- Clean final render at full size with lighting (Level 2 v2 / Blender): 0/1.
- Repo push of dance-improved-20261031/ (parent's PR route; no commit made here).
