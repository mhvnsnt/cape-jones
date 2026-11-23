# Gumball .fla — First-Hand Confirmation (Rig Jones 2 / Clean-Up Jones 1)

Opened first-hand 2026-11-23 from the downloaded zips (study only — no CN
art goes into show files):
- `GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla` — 1,740,533 B,
  sha256 `fb30f003a3ce91928240a1d7b7ba2dd2023dac710c73527b5d149ab9d3ac6bd4`,
  from Gumball_S2_Rigs.zip (686 MB).
- `GB202REMOTE_Sc094_Clean_V023_STN.fla` — 22,851,853 B, from
  CN-Leaks-001-gumball.zip (1.7 GB). Scene check only.
- Extraction note: the .fla's central directory is 54 bytes too long
  (old-Flash quirk) — `unzip` and Python `zipfile` both refuse it.
  Extracted by walking the LOCAL file headers instead
  (`/tmp/fla_extract.py` pattern). GB200 yielded 72 entries.

## What the files are
- GB200 is a puppet-library file: main timeline Scene 1, 25 fps,
  2730x1625, four layers holding the four view puppets (BACKVIEW,
  FLOPPED, STD_001, FRONTVIEW), one frame, duration 162.
- One master graphic symbol per view: `GB200_GUMBALL_PUPPET_001` (STD),
  `GB200_ORIGINAL_PUPPET_FRONTVIEW_v001`, BACKVIEW, FLOPPED masters.
- The scene file is 1920x1080, 25 fps, 9 layers. Sc094 is a NICOLE/Mom
  scene ("REMOTE" is the episode/scene code, not a remote prop in shot).

## CONFIRMED live (with the exact numbers)

### 1. .fla is a ZIP of XFL XML — CONFIRMED
`DOMDocument.xml` + `LIBRARY/*.xml`, namespace
`http://ns.adobe.com/xfl/2008/`. Symbols are `DOMSymbolItem`
(graphic), instances are `DOMSymbolInstance` with
`libraryItemName`, `loop`, `firstFrame`, `<matrix><Matrix …/></matrix>`,
`<transformationPoint><Point x y/></transformationPoint>`.

### 2. Swapping = loop="single frame" + firstFrame — CONFIRMED, extensively
Master puppet placements (all `loop="single frame"`):
- L_ARM: 27 placements, firstFrames 1,2,3,4,5,6,7,8,9,10,24,25,26,28,29,30,31,32,34,54,55
- R_ARM: 29 placements, firstFrames 1–11, 24–34, 53,54,55
- L_LEG / R_LEG: firstFrames 1–9
- BODYCOMP: firstFrames 1–10; HEADCOMP: 17,32,33,85–95; MOUTH: 17,18
- Scene file: Mom puppet placed `firstFrame="17" loop="loop"`, scale 0.53;
  "Mom angry run rough" cycle: 18 instances, `loop="play once"`,
  firstFrame stepping 6,7,8,9,10,11… — stepping firstFrame frame-by-frame
  IS how a cycle plays. That is the wheel-scroll mechanism in real use.

### 3. Mouth is ONE frame-addressed comp library — CONFIRMED, labels CORRECTED
`GB200_GB_MOUTH` (in HEADCOMP): 124 keyframes, sections in LABEL_01:
HAPPY_LIPSYNCH f0–16, SAD_LIPSYNCH f17–36, MOUTH_HOLD_POSE f37–78,
STD_EXTRA_MOUTH_FOR_LIPSYNCH f79–104, STD_LIPSYNCH_BIG_MOUTH_HAPPY
f105–121. LABEL_02 gives one viseme label per frame, e.g. HAPPY_REST,
HAPPY_B, HAPPY_ P,M, HAPPY_N,S, F, O_01/02/03, O,U,W, HAPPY_L_01/02,
HAPPY_A_01/02/03/05, HAPPY_A,I, HAPPY_CH,S, SAD_REST/B/P,M/N, TEETH_SMILE_01,
OPEN_SMILE_02, TEETH_SAD_01/02, OPEN_SAD_01, Pose_Extreme_Angry_01/02,
POse_extreme_happy_01, eating_mouth_01, GB200_CUTE_MOUTH_V001,
GB200_SCARED_MOUTH_BIG_CHEEK_V001, WHISTELING_MOUTH, HAPPY_TH_01, SAD_TH_01.
The mouth is placed in HEADCOMP with the SAME transformationPoint
(40.2, 9) at every keyframe — only the matrix tx/ty moves slightly.
CORRECTION to the earlier dissection: the label set is NOT "X_REST,
Blair A–H, O_ROUND, WIDE, HOLD_POSE" — that was a paraphrase. The real
set is the HAPPY/SAD viseme list above.

### 4. Eyes are lid swaps plus SEPARATE pupils — CONFIRMED
`GB200_GB_EYESCOMP` / `GB200_GB_EYESCOMP_SYMBOL`: LABEL_01 sections
STD_EYES f0–8, CLOSED_EYES f9–25, STD_SPECIAL_EXPRESSIONS f26–85,
EXT_SPECIAL_EXPRESSION f86–104, BIG_CHEEK_STD_EYES_001 f105–124,
SPECIAL_POSE_WHISTELING f125–159; LABEL_02 per-frame labels
(STANDARD_EYES_01–04, eyes_Closed_HAPPY_01, Eyes_CLOSED_02…).
Layers: WHITE_MASK_01/02 (white of eye), CLEAN_EYES_LINES (lid lines),
EYEBROWS, and CLEAN_PUPILS as its OWN layer (56 keyframes, 36 shapes) —
pupils live apart from the lids, so they move/swap independently.
CORRECTION: the earlier "OPEN/HALF/SHUT, never a squash" was a
paraphrase — the real structure is frame-labeled lid/white shapes, and
SQUASH_HEAD exists as a HEADCOMP pose label. Squash is a real thing
they do; "never a squash" is wrong.

### 5. Pivots (transformationPoint) — CONFIRMED with nuance
- LEGS: EXACTLY ONE pivot each — L_LEG (10.55, 3.35) across 29
  placements; R_LEG (25.5, 4.25) across 16. Legs never shift.
- BODYCOMP: 3 distinct, two within 0.05 — (37.5, 125.15) dominant.
- L_ARM: 3 distinct, two within 0.05 — (13, 8.25) dominant.
- HEAD: 2 distinct within 0.05 — (146.25, 114.05). EAR2: 2 within 0.1.
- BUT: HEADCOMP 8 distinct tp, R_ARM 6, TAIL 8, EAR1 7 — the head,
  R-arm, tail and one ear DELIBERATELY shift registration for
  extreme/acting poses. Rule as built: pivots are stable for standard
  poses; extremes may re-register. The earlier "identical across ALL
  keyframes" was too blanket — true for legs/body, approximate for
  arms, not true for head/tail extremes.
- FRONTVIEW master: L_ARM and L_ARMFRONT share ONE tp (30.05, 47.75);
  R_Arm and R_ArmFRONT share ONE tp (29.95, 47) — front/behind arm
  variants pivot at the same shoulder point. Legs one pivot each.

### 6. Arms/hands — CORRECTED from the earlier dissection
The arms are NOT "upper arm + forearm+hand as separate symbols with
the elbow pivot between them." Each arm (L_ARM, R_ARM) is ONE graphic
symbol whose ARM layer holds 24–26 keyframes of DRAWN SHAPES — the
whole arm+hand is re-drawn per frame; the elbow bend is drawn, not
jointed. Hand variants are LABELED FRAMES of the arm comp:
- L_ARM (12): f25 EXPLAINING, f26 SHRUG_SHOULDER, f27 POINTING_FINGER,
  f28 EATING_ARM, f29 ARMS_ON_TABLE, f30 EXT_FORCING_EXPLAINING_HANDS,
  f31 SHOUTING_ARM, f32 HAND_ON_TABLE_CHEEK, f33 POINTING_HAND_V002,
  f34 SCARED_HAND, f54 FIST_CLOSED_EXTREME_POSE, f55 HAPPY_FIST
- R_ARM (14): f24 FIST_CLOSED_PERS, f26 SHRUG_SHOULDER, f27
  POINTING_FINGER, f28 EATING_ARM_BEHIND, f29 ARMS_ON_TABLE, f30
  EXT_FORCING_EXPLAINING_HANDS, f31 SHOUTING_HAND_BEHIND, f32
  THINKING_HAND, f33 POINTING_HAND_V002, f34 SCARED_HAND, f53
  HAND_ON_FOREHEAD, f54 FIST_CLOSED_EXTREME_POSE, f55 HAPPY_FIST
- The two sides' frame maps DIFFER (offset by one, different poses) —
  per-side sets, not mirror copies. Legs have NO labels (frames 1–9,
  un-named).
- PROPS layer: the SANDWICH prop attaches to a specific arm frame
  (L_ARM f28) with a full rotation/scale matrix — a prop rides a pose
  frame, exactly how V3's remote rides the Grip frames.

### 7. Joints — NO caps/discs anywhere (verified first-hand 2026-11-23)
Parsed `GB200_GB_L_ARM.xml`, `GB200_GB_R_ARM.xml`,
`GB200_GB_L_LEG.xml`, `GB200_GB_R_LEG.xml` and the FRONTVIEW master
`GB200_ORIGINAL_PUPPET_FRONTVIEW_v001.xml` directly from
`gumball-study/gb200-xfl/`:
- L_ARM: layers LABELS (14 keyframes, 12 named poses), **ARM: 24
  keyframes, ALL DOMShape (24)** — drawn vector shapes, ZERO symbol
  instances, ZERO discs/caps. PROPS: 11 keyframes, 1 symbol instance
  (the sandwich). R_ARM: ARM: 26 keyframes, ALL DOMShape (26). L_LEG:
  L_LEGS: 10 keyframes, ALL DOMShape (10). R_LEG: R_LEG: 10 keyframes,
  ALL DOMShape (10).
- FRONTVIEW master layer order (front→back): HIDE_NECK,
  GB_frontview_Head_comp, GB_L_ARM_FRONT, GB_R_ARM_FRONT,
  GB_Frontview_body, GB_Frontview_L_ARM, GB_frontview_R_arm,
  GB_frontview_R_Leg, GB_frontview_L_leg, GB_frontview_Tail. Each arm
  is TWO instances sharing ONE transformationPoint at the shoulder —
  L_ARM (30.05, 47.75) and L_ARMFRONT (30.05, 47.75), R (29.95, 47) —
  a back arm below the body layer and a front arm above it. The
  front/back split is at the SHOULDER, NOT at the elbow. There is no
  elbow piece at all.
- **There is NO symbol named *CAP*, *DISC*, *BALL*, *JOINT*, or
  *CIRCLE* anywhere in the whole GB200 library.** Full symbol list:
  arms (L_ARM, R_ARM, FRONTVIEW L_ARM, L_ARMFRONT, R_Arm,
  R_ArmFRONT), legs, BODYCOMP, HEADCOMP, EYESCOMP, MOUTH, TAIL,
  EAR1/2, PROPS (SANDWICH), LINES, Tweens. **Gumball does NOT use
  caps/discs — the owner's doubt is confirmed by the real file. The
  earlier claim that Gumball uses an "overlap-cap" was WRONG.**
- Gumball's actual joint method: **the limb is one drawn shape per
  pose; the joint is drawn, not assembled; the only split is shoulder
  front/back sharing one pivot, with the arm's top tucking BEHIND the
  body.** Our cutout translation: the split must be invisible — the
  two pieces must read as the one drawn limb. V3's socket cut (the
  ball's own outline circle, ball in the lower piece, concave socket
  in the upper piece, no pixel in both, none in neither) is that
  translation: the cut follows the art's own contour, nothing is added.

## What this means for V3 (Rig Jones 2 / Clean-Up Jones 1)
- KEEP: slot addressing (one slot, one visible, replace in place,
  index = frame) — the mechanism is exactly Gumball's.
  cj_set_slot / wheel operator = firstFrame addressing.
- KEEP: anatomical pivots, constant across frames — matches Gumball's
  standard-pose rule (legs exact, body/L-arm near-exact). V3's bone
  heads are measured from the art itself (shoulder/elbow/wrist/hip/
  knee/neck); the verifier enforces joint continuity.
- KEEP: pupils as a separate toggle (V3 eyes slot: Normal vs Pupils,
  pupils are their own planes) — matches CLEAN_PUPILS.
- KEEP: NO caps, ever. Gumball uses no cap/disc/ball-joint anywhere
  (§7 above — verified first-hand, not from notes). The V3 joins are
  socket cuts along the art's own ball circles; the verifier enforces
  ball == socket at every frame. The handswap lane's literal white
  disc (`rig/parts/Cap_disc.png`, placed at every joint by
  `rig/build_rig_handswap.py`) is NOT Gumball's method and is NOT in
  this build. The owner was right to doubt it.
- HONEST DELTA 1 (hands): V3 swaps separate hand planes onto a
  forearm; Gumball draws arm+hand per frame. V3's way is correct for
  a cutout rig (our art is sliced that way; PR #430's 44 parts do the
  same). A per-frame drawn arm+hand set is a Rig Jones 3 step, not a
  V3 blocker.
- HONEST DELTA 2 (mouth): V3 has 5 mouth variants (Closed/Open/Shout/
  Smile/Teeth) as full lower-face crops; Gumball has a 124-frame viseme
  library. A fuller viseme library is a Rig Jones 3 step.
- HONEST DELTA 3 (cape): Gumball has no cape on this puppet (TAIL is
  the closest analogue, and it re-registers per pose). V3's one-piece
  skin-weighted cape is our own system, built to the owner's rule
  (hangs from torso, trails motion, never lifts with the arm).
- Frame rate note: GB200 is 25 fps; the show is 24 fps. No change.

## Files (study only, never in show files)
- `gumball-study/GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla`
- `gumball-study/gb200-xfl/` (72 extracted XFL entries)
- `gumball-study/GB202REMOTE_Sc094_Clean_V023_STN.fla`
- `gumball-study/gb202-xfl/` (67 extracted XFL entries)
