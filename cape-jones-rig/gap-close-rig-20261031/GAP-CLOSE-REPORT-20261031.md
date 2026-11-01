# Cape Jones GAP CLOSURE chunk A — gap-close-rig-20261031

All files in this folder are NEW. Nothing Mars has seen was overwritten or deleted.
No repo push was made. No show character art/name/dialogue/logo was copied:
all pieces are original Cape Jones rig pieces, methods only from other shows.
Labels appear on catalogue/sheet images ONLY, never baked into clean pieces.
Mars approval for everything here: 0 (built and viewed, not approved).

## Pre-existing work found first (not duplicated, not claimed)
- `forearm-fist-v4-20261031/` already contained a v4 knuckle fist + seated forearm
  (built 21:47-21:53, before this chunk). This chunk's v4/v4b/v4c fist and punch
  pose were drawn/built separately in this folder; the earlier folder is untouched.
- `build_true_final_flex_v2.py` + `reposes-v7c-clean/true-final-flex-relaxed-clean-20261031.png`
  already implemented the relaxed true-final. This chunk's flex v2 re-implements
  the same spec in this folder (v7c geometry, own code); the earlier files are untouched.
- `forearm-head34-v2-20261031/` (foreshortening 0.42x, fist 1.45x wide) and
  `forearm-arm2-aligned-20261031/` (alignment method) were used as METHOD sources only.

## 1. Missing pieces pack (all RGBA, non-empty, verified)
Necks (from sliced/Neck.png): neck-01 base, neck-02 short (0.70x), neck-03 long (1.35x),
neck-04 tilt-left (+15°), neck-05 tilt-right-long (1.20x, -15°).
Heads (from Head_Front, eyes/mouth zones repainted with sampled cowl/skin):
head-blank, head-blank-normal-eyes (original eye crops), head-blank-comedic-eyes
(round pupils — comedic relief only, C-08), head-blank-angry (slanted-brow vector eyes),
head-furious-faceangry-normaleyes (Face_Angry pasted, normal white eyes over its eyes).
Feet (ankle intact, crop from y230, ankle ~240-260): foot-left (Leg_Front lower),
foot-right (Leg_Back lower). Gauntlets (cuff band y70-190 from OutFixed lowers):
gauntlet-arm1, gauntlet-arm2.
Catalogue (deliverable): gap-close-missing-pieces-catalogue-v2-20261031.png
(the v1 catalogue is a superseded draft with bitmap-font labels).

## 2. Front-facing knuckle fist v4 (deliverable: v4b fist + v4c pose)
- gap-close-fist-v4b-knuckle-front-20261031.png — original vector: 4 merged knuckle
  bumps at TOP facing camera, thumb as a wide band wrapped ACROSS the front,
  wrist cuff at BOTTOM. No palm visible. NOT the v3 palm view, NOT a rotation of it.
- gap-close-punch-pose-v4c-20261031.png — v7c punch geometry (canvas widened to
  1300 so the fist is not edge-clipped), R forearm part only (native fist discarded,
  so NO double fist), v4b fist scaled to 155px wide and seated with 12px overlap,
  wrist cap BEHIND the fist masked to the forearm+fist union (side arcs only),
  wrist-row gap check: continuous x801-1221, zero gaps >5px.
- Superseded drafts kept, not deliverables: fist-v4 (first draw), punch-v4, punch-v4b
  (patch attempt — see defects fixed).

## 3. True-final-flex v2 (RELAXED — the existing full-final 75° pose is OVER-FLEX, untouched)
gap-close-true-final-flex-v2-20261031.png, built with v7c geometry (labels=False
equivalent: transparent canvas, no debug labels), FlexOut lowers split at y175,
wrist caps behind fists masked to the union, wrist zones cleaned (faint alpha <40 dropped).
Delta table vs the over-flex full-final (arm_upper -70/+70, arm_lower 135/-135, fist -75/+75):

| Spec item | Over-flex | This v2 | Delta | Hit? |
|---|---|---|---|---|
| Biceps angle toward head | -70 / +70 | -85 / +85 | +15° | YES, exactly |
| Forearm-wrist angle opened (fist angle) | -75 / +75 | -70 / +70 | +5° more open | YES, exactly |
| Lower-arm relaxation | 135 / -135 | 145 / -145 | +10° relaxed | Extra, part of "relaxed" |
| Wrists | — | FlexOut clenched fists seated AT the forearm junction, caps behind, seams cleaned | — | YES as seated+cleaned |
| Wrist caps | — | Behind fists, masked, no ring across fist face | — | YES |

Wording note (flagged, not hidden): the task summary said "wrists clenched", but a
later 16:46 correction recorded in build_true_final_flex_v2.py clarifies Mars's
"cleaned up" was misheard as "clenched" — do NOT roll the fists extra. This build
therefore applies NO extra fist roll: the fists are the clenched FlexOut fists,
seated at the junction and cleaned. If Mars wants extra roll, that is a new instruction.

## 4. 3/4 + side + back stand-ins (labelled, plainly)
- gap-close-head-34-v3b-kitbash-20261031.png + v3b sheet: DERIVED KITBASH, NOT a true
  hand-drawn 3/4 (far side 0.70x, near side 0.97x, far eye x0.80, bridge-occlusion
  strip x38-41). Construction lines are on the REFERENCE panel of the sheet only.
- gap-close-side-body-standin-sheet-v2-20261031.png: STAND-IN — profile head (real)
  + front torso/limbs in profile order; torso musculature still faces front.
- gap-close-back-body-standin-sheet-v2-20261031.png: STAND-IN — cape back (real) +
  a blank cowl-back PLACEHOLDER shape with NO face. It is not a back head.
- BLOCKER, stated plainly: a true hand-drawn 3/4 head, side body, and back body
  cannot be produced by warps/kitbash — warps cannot redraw linework. The kitbash
  and stand-ins above are the working replacements until hand-drawn masters exist.

## 5. Cape bone-chain
- gap-close-cape-bone-chain-diagram-v2-20261031.png: B0 neck -> B1 mid-back ->
  B2 mid-cape -> hem fan B3 L / B5 C / B4 R; each bone lags the one above by 1-2 frames.
- gap-close-cape-state-billowing-layer-20261031.png: billowing cape as a SEPARATE
  prop-rig layer (sine-wave warp of Cape_Back_Main).
- gap-close-cape-pose-body-only-20261031.png: body with NO cape baked in.
- gap-close-cape-pose-composite-20261031.png: body + cape state composited (viewed).

## 6. Foreshortened forward-flight forearm (deliverable: v2 files)
Method as forearm v2: shaft compressed 0.42x, cuff full height, fist 1.45x wide / 1.30x tall,
fist over forearm with 18px overlap, wrist cap behind fist.
- gap-close-foreshortened-forearm-arm1-v2-20261031.png (Arm1 built)
- gap-close-foreshortened-forearm-arm2-v2-20261031.png (Arm2 built, cap centred on
  the fist art's own centroid so it does not peek sideways)
- v1 files are superseded drafts (they compressed shaft+cuff together and read as a cuff stack).

## 7. Alignment QC script + results
alignment_qc_gap_close.py (run: `python3 alignment_qc_gap_close.py`;
full numbers in gap-close-qc-results-20261031.json).
- Punch v4c: 11/11 PASS — elbows 2.3/4.0px, wrists 2.0/10.4px, fist R 23.4px
  (threshold 30), cuffs 12.4/1.6px, all joints on-body.
- Flex v2: box-centroid deltas 29-49px on elbows/wrists/fists (thresholds 20/30)
  flagged, BUT this is a measurement bias, reported honestly: in the bent flex pose
  the mass centroid of upper+lower pieces in the box is not the joint centre
  (e.g. fist boxes also contain forearm below the fist, pulling the centroid ~45px down).
  The decisive checks pass: all flex elbow/wrist points lie ON opaque body, cuffs
  pass (10.6/8.1px), and the pose is placed by exact v7c geometry by construction.
  Do not read the flex box-centroid flags as a misaligned pose; the script keeps
  both numbers so the distinction is auditable.

## 8. Knee-feet QC
- Flex v2: PASS both legs — L knee_dir -62.0 / foot_dir -99.4 (both left/outward);
  R knee_dir +30.2 / foot_dir +84.6 (both right/outward). Ankle from v7c leg geometry
  (approximate to the lower piece's length); toe from pose alpha.
- Dance frame f015 (dance-improved, frame 15): silhouette method is INCONCLUSIVE —
  the legs CROSS at knee height (single silhouette interval x367-770 spanning the
  centre), so a centre split cannot assign feet to legs, and the naive split
  wrongly reported FAIL. Visual tracking through the cross (viewed): front leg
  knee and foot both point right, back leg knee and foot both point left —
  knees point the same direction as feet, PASS by visual tracking. The script now
  detects crossing and reports INCONCLUSIVE instead of a false FAIL.

## Defects found on own-eyes viewing and fixed
1. Fist v4: deep knuckle scallops + thumb as detached diamond + grey slab panel
   -> redrawn as v4b (shallow bumps, wide thumb band, shading clipped to silhouette).
2. Punch v4: fist at full 320px clipped at canvas edge + wrist-cap white block
   -> v4b patch, which then erased the forearm cuff leaving an 82px gap
   -> rebuilt from scratch as v4c (continuous, gap check 0 gaps >5px).
3. 3/4 v3: far-eye squeeze applied to the wrong zone (x6-26), leaving a double-eye
   smudge -> v3b squeezes the real far eye (x17-31).
4. Sheets v1: PIL bitmap font made titles/labels look merged -> v2 sheets use DejaVuSans TTF.
5. Bone-chain v1: hem joints chained across the hem with a floating centre dot
   -> v2 fans B2 -> each hem joint, centre dot on the hem.
6. Foreshortened v1: shaft+cuff compressed together, read as a cuff stack
   -> v2 compresses shaft only, cuff full height.
7. Foreshortened Arm2 v2: cap peeked sideways (fist art offset from crop centre)
   -> cap re-centred on the fist art's centroid.
8. QC: dance-frame silhouette FAIL was a crossed-leg artefact -> script detects
   crossing and reports INCONCLUSIVE; visual tracking reported separately.

## Still owed / not claimed
- Mars approval: 0 for every file here.
- True hand-drawn masters: 3/4 head, side body, back body (blocker: hand drawing;
  kitbash/stand-ins are the working replacements, not substitutes claimed as masters).
- No repo push (a separate push workstream lands this folder).
- Scripts in this folder: build_gap_close.py, fix_fist_punch.py, fix_sheets_head34.py,
  rebuild_punch.py, alignment_qc_gap_close.py (build/audit trail, not chat deliverables).
