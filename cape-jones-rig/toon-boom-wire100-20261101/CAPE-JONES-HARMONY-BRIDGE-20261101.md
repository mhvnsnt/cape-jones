# Cape Jones → Harmony Bridge
Base pose: ORIGINAL DEFAULT SITTING POSE, authored by Mars himself,
rig-34-locked-default-sitting-20261101, from APPROVED PERFECT wired
rig-34-disassembled-wired-20261101 + neck. Whole pieces only, no piece
crop, large-temp rotate only (the bicep lesson: in-place PIL rotate
clipped 25.7% of Arm 2 bicep; Harmony peg rotation must be checked the
same way — pivot + canvas, never a rectangle clip).

## Canvas / scene settings (to set in Harmony, not assumed)
- Rig canvas in our builders: 1400×1600. Harmony scene: set camera to
  match the sitting pose framing, then set a separate TV scene
  (1920×1280, ground 1180, for room shots) — do NOT mix the 1400×1600
  rig canvas with the 1920×1280 shot canvas. That mix was a past error.
- Frame rate: 24 fps (all our chains, sit-idle 48f = 2.00s).
- Ground: widget ground y=1475 on the 1400×1600 rig canvas. In Harmony,
  set the ground line as a guide, check feet against it, never shift the
  figure in post to fake it — a further drag in the widget, save, re-import.

## Node map (18 pieces + neck = 19 nodes, + 1 composite)
Order = DEFS-stable z order. Peg per piece, drawing under peg, except
where noted. Arm1 = LEFT, Arm2 = RIGHT (Mars correction 2026-11-01 01:26).
Arm1 behind torso, Arm2 in front. Cape backmost, collar fused in torso,
locked, NOT moved/redrawn/invented.

| z | Piece | Harmony node | Peg pivot (ox,oy) | Saved xy / rot | Chain / joint |
|---|---|---|---|---|---|
| 0 | cape_back 514×900 | Cape-P / Cape | (0.5,0.5) assumed* | 360,330 / 0° | cape, shoulders-back |
| 1 | upper_arm_L 125×237 | Arm1-Upper-P / Arm1-Upper | (0.5,0) | 490,390 / 5° | arm1, shoulderL |
| 2 | thigh_bent_R 218×299 | Leg2-Thigh-P / Leg2-Thigh | (0.5,0) | 590,750 / 6° | leg2, hipR |
| 3 | thigh_bent_L 230×267 | Leg1-Thigh-P / Leg1-Thigh | (0.5,0) | 400,710 / 2° | leg1, hipL |
| 4 | forearm_L 145×275 | Arm1-Forearm-P / Arm1-Forearm | (0.39,0.11) | 455,580 / -15° | arm1, elbowL |
| 4 | pelvis_belt 218×181 | Pelvis-P / Pelvis | (0.5,0.5) assumed* | 565,650 / 0° | spine, pelvis |
| 4 | knee_ball_L 74×94 | Leg1-Knee-P / Leg1-Knee | (0.5,0.5) | 380,885 / 0° | leg1, knee pivot, NOT a secondary knee |
| 5 | elbow_cap_L 63×63 | Arm1-ElbowCap-P | (0.5,0.5) | 465,580 / 0° | arm1, elbow cap |
| 6 | shin_boot_L 244×410 | Leg1-Shin-P / Leg1-Shin | (0.5,0) | 225,945 / 0° | leg1, ankleL |
| 6 | shin_boot_mid 256×415 | Leg2-Shin-P / Leg2-Shin | (0.5,0) | 395,985 / -10° | leg2, ankleR |
| 7 | knee_ball_R 74×94 | Leg2-Knee-P / Leg2-Knee | (0.5,0.5) | 560,950 / 0° | leg2, knee pivot |
| 8 | torso 291×315 | Torso-P / Torso | (0.5,0) | 550,370 / 0° | spine, torso, collar fused |
| 8.5 | neck 101×82 rendered | Neck-P / Neck | centre | centre x700, top 330 | head, front-view piece, 1.05×, NOT squashed |
| 9 | head_cowl 130×196 | Head-P / Head | (0.5,0.5) assumed* | 635,195 / 0° | spine, head |
| 10 | upper_arm_R 112×256 | Arm2-Upper-P / Arm2-Upper | (0.5,0) | 805,420 / 15° | arm2, shoulderR, PERFECT, do not move |
| 11 | forearm_R 150×274 | Arm2-Forearm-P / Arm2-Forearm | (0.63,0.11) | 685,650 / 45° | arm2, elbowR |
| 12 | elbow_cap_R 63×63 | Arm2-ElbowCap-P | (0.5,0.5) | 775,610 / 0° | arm2, elbow cap |
| 13 | hand_spare_L 117×170 | Arm1-Hand-P / Arm1-Hand | (0.5,0.5) | 530,740 / -46° | arm1, wristL, as-is, thumb east |
| 13 | hand_spare_L mirrored 117×170 | Arm2-Hand-P / Arm2-Hand | (0.5,0.5) | 565,755 / 70° | arm2, wristR, mirrored, thumb west |

* Cape/pelvis/head pivots were NOT in the widget inspection; the pipeline
assumes centre for those three. Verify in-app via Show Attribute
Information and correct the CSV before first render — do not claim
confirmed.

## Joint locks → Harmony (locked together, NOT frozen in space)
- SHOULDER→TORSO: upper pegs parented to torso peg (Arm1 behind, Arm2 in front, via z, not via parenting order).
- ELBOW→BICEP / ELBOW→FOREARM: elbow caps at elbows, forearm pegs child
  of elbow, via Bone/Curve deformer OR peg hierarchy — test both in-app,
  keep the one that does NOT deform the hand (Kinematic Output for hands).
- FOREARM→WRIST→HAND: hand peg child of forearm peg, wrist anchored at
  forearm end, NOT fingertip end. Arm1 as-is, Arm2 mirrored.
- HIP→PELVIS / HIP→KNEE / KNEE→SHIN: thigh pegs child of pelvis, knee
  pivots as rotation points, shin pegs child of knee pivots, shin tops
  overlap caps by design (v7c).
- CAPE→BACK: cape peg backmost, locked to shoulder placement.
- NECK→HEAD: neck peg child of head peg, exactly as front view.

## Drawing substitutions (Harmony drawing layers, not PIL paste)
- Hands: open hand (saved) ↔ fist (whole forearm+fist piece, NOT a
  wrist-line split — that split was rejected as a cut). Until a native
  gauntlet-only forearm exists, fist substitution = whole forearm swap.
- Mouths: MBP, AH, GK, GAP, REST + jaw drops (0/16/8/10/0) — see
  mouth-jaw-movement. AH and SMILE34 cleaned, approved 1/1.
- Eyes: Robin library 25/25, approved; V4 in-mask approved perfect.
  Pack4 strips with pupils = comedic relief only.
- Colourways (NOT new geometry): Dream 1–18, Dual Charge thin/medium/
  heavy (6/12/20px rim), Crystal Form (Preset 8 / P8-06 overlay), Cape
  Consumed (future only). Colourway = palette swap, never a re-draw.

## Palette (Cape Jones, measured, from our docs)
- Outer Cape: PMS BLACK. Inner Cape: PMS 115c yellow (255,225,82).
- Eyes: WHITE. Shirt / gloves / pants: Green PMS 336c.
- Coloured Shadow (separate, NOT a rig): dark purple (52,22,90).
- Rim default: warm amber (255,180,80), bleed (255,120,0); rim follows
  key/LUT hue ±20°. Cyan rim only in dual-light (warm gold key front +
  cool cyan back), never under a single warm grade.
Palette is shipped as `palette/cape-jones-palette.csv` in the pack;
import it via Harmony's palette editor in-app, then verify RGB values
match this list before first render.

## What is NOT in the bridge yet (owed, not faked)
- Side art / side rig, back art / back rig, 3/4-back rig, VIEW field.
- Native separate fist file, native gauntlet-only forearm file.
- A verified .tpl — save it inside Harmony after first import.
- A verified .plt — import the CSV palette in-app, save, then export
  the .plt from Harmony and replace the CSV as the canonical palette.
