# Pose Dialects — JoJo / Stand-user / Ginyu-style (2026-10-31)

Built ONLY from Cape Jones's own v7c rig pieces (ball-centre pivots, `joint_locked_rig_v7c.py`
method). No show character is shipped, no character art copied, no dialogue, no logo.
Pose languages and staging methods only, transform-only, as universe-language dialects/gags.

## Research (public sources, methods only)
- JoJo posing: extreme contrapposto — hips and shoulders torqued against each other into
  an S/Z silhouette, drawn from Renaissance sculpture (Michelangelo contrapposto) and
  women's fashion-magazine modelling (Araki, SPUR 2018 interview, as reported). Three
  interlocking ideas: (1) torque, (2) intentional hand choreography (splayed fingers,
  bent wrists, pointing as punctuation), (3) theatrical, fashion-forward silhouette.
  A pose is a poster frame: hold it, don't rush through it.
- Stand-user staging: the Stand is usually staged BEHIND / beside its user, often
  mirroring the user's pose, larger and looming, so the pair reads as one unit of power.
  User stays grounded and calm; the Stand does the exaggeration. Mirroring = same arm
  angles, same stance, offset behind.
- Ginyu-style / sentai roll-call: a 5-person team pose in the source, but the METHOD
  transfers solo: synchronized, chest-out, name-announcing beats, deliberately goofy
  and self-serious at the same time. Comedy comes from commitment — the pose is held
  dead-serious while being ridiculous. Solo version: roll-call beat (one arm up, other
  hand on hip, leg kicked out), squat with elbows out, dance shimmy with hips out.
  Timing: announce (hold 12f) -> snap to pose (2f) -> hold (12f+), like a sentai roll call.

## Industry-standard staging methods wired in
1. Contrapposto: hips and shoulders rotate opposite directions; weight on one leg.
2. S-curve / Z-silhouette: head, torso, hips, legs form a readable S or Z, no straight stack.
3. Hand choreography: fist vs open hand vs point changes the read; hands frame the face.
4. Mirrored pair staging: second figure behind, same angles, offset, silhouette colour.
5. Silhouette test: every pose must read in silhouette alone (checked on contact sheet).
6. Knee-feet rule (standing): knees-out -> toes-out, knees-in -> toes-in, checked visually
   on all 8 poses; no broken-knee read in the viewed contact sheet.
7. Hold timing: JoJo/Stand poses hold; Ginyu poses snap (2f) then hold (12f+) — see doc above.

## Poses built — 8/8, all viewed
Folder: `pose-dialects-20261031/`, builder `build_poses.py`, contact sheet
`pose-dialects-contact-20261031.png` (grey-128 background for viewing only; pose files
themselves are transparent).

JoJo-style — 3/3 (dialect: JOJO-POSE, dramatic/fashion):
- jojo-01-contrapposto-s-curve: arm U -75/40, arm L 125/-45, leg U -38/28, leg L 22/-18, head +12
- jojo-02-fashion-twist-point: arm U -115/65, arm L 85/-95, leg U -16/32, leg L 6/-28, head -10
- jojo-03-menacing-lean-hand-face: arm U -25/-88, arm L 35/145, leg U -42/12, leg L 32/-6, head +8

Stand-user pairs — 2/2 (dialect: STAND-PAIR, power reveal):
- stand-01-mirrored-pair: user + dark-purple (52,22,90) silhouette of his OWN rig behind,
  offset +180px, same flex angles both figures, mirrored staging
- stand-02-towering-behind: user crouched forward, silhouette behind with arms up (-150/150)
  — the Stand does the exaggeration, user stays grounded

Ginyu-style funny — 3/3 (dialect: GINYU-GAG, comedic pose/dance):
- ginyu-01-rollcall-chest-out: one arm straight up (-160), other hand to hip (95), leg kicked out
- ginyu-02-squat-elbows-out-goofy: wide squat (-45/45, lower 40/-40), elbows out, fists up
- ginyu-03-dance-shimmy-hips-out: arms up-out (-130/130), hips out (leg U -20/35)

## Honest limits
- Head tilt only (no true 3/4 head, no torso twist piece): the twist is carried by limbs +
  head tilt + leg torque, not a redrawn torso. A true torso-twist piece is still owed
  (same owed item as the dance twist).
- Stand silhouette is the SAME size as the user, not larger: the rig's SCALE is fixed at
  0.95 in the v7c builder, so "towering" is conveyed by arms-up + behind-offset, not by
  scale. A scaled-up stand figure needs a scale parameter in the builder (owed, small).
- Hands are fists (v7c pieces): JoJo hand choreography (splayed fingers, pointing) cannot
  be fully expressed with fist pieces alone — open-hand / point pieces exist in sliced/
  (Hand_3_Open, Hand_4_Point) but were not swapped in here; that swap is the next pass.
- Single-frame poses, not sequences: the Ginyu roll-call SEQUENCE (announce -> snap ->
  hold, 5 beats) and a JoJo pose-to-pose transition are not built here.

## Universe-language naming (for shot specs)
- JOJO-POSE: dramatic, fashion, hold. Use sometimes, never as his default stance.
- STAND-PAIR: power reveal / power-up gag. Stand = silhouette of his own rig, never a
  show character, never named as a show Stand.
- GINYU-GAG: funny, comedic, pose/dance, roll-call timing. Use for comedy beats only.

## Approval
Mars approval (updated 2026-10-31 ~18:29 CDT):
- JoJo 01 contrapposto S-curve: PERFECT, APPROVED 1/1.
- Stand 01 mirrored pair: PERFECT, APPROVED 1/1 — saved as the COLORED SHADOW
  mechanic/preset (see COLORED-SHADOW-MECHANIC-PRESET-20261031.md).
  He is NOT a stand user; the thing behind him is a purple silhouette of his
  own rig that acts like a stand and does its own thing behind him.
- Stand 02 towering-behind: 0/1, not separately approved yet.
- Ginyu 02 squat elbows-out goofy: SAVED + APPROVED 1/1 (Mars, 2026-10-31
  ~18:30 CDT: "yeah, save that… that's really good").
- JoJo 03 FACE-SNAP fixed version: PERFECT, APPROVED 1/1 (Mars, 2026-10-31
  ~18:34 CDT, replying to the face crop: "Perfect. That's perfect.
  Exactly like that."). Original JoJo 03 remains unapproved as originally
  built; the FACE-SNAP version is the approved one.
- Ginyu 01 COWL-SNAP fixed version: PERFECT, APPROVED 1/1 (Mars, 2026-10-31
  ~18:34 CDT, replying to the cowl crop: "That one's also perfect.
  Good job. That's perfect."). Original Ginyu 01 remains unapproved as
  originally built; the COWL-SNAP version is the approved one.
- Before/after face-cowl contact sheet: PERFECT x3, APPROVED 1/1 (Mars,
  2026-10-31 ~18:35 CDT, replying to the before/after sheet).
- Pose-dialects FIXED video (8 poses, FACE-SNAP + COWL-SNAP in):
  REALLY GOOD, APPROVED 1/1 as a pose video (Mars, 2026-10-31 ~18:37 CDT,
  replying to the fixed MP4). Inbetweening still owed: more fps, more
  inbetweening/interpolation, more drawings per second — that work is
  running separately and is NOT approved yet.
- Landing ordered 2026-10-31 ~18:37 CDT: "get all this landed" — push +
  land all recent work, verified on main.
- JoJo 02, Ginyu 03: approval status unchanged by that save.
- Whole-Ginyu-Force study ordered 2026-10-31 ~18:30 CDT: not just Ginyu
  poses — every Ginyu Force member's poses/alternatives, researched and
  wired 100% as Cape poses (methods only, no show character shipped).
- Face/cowl snap rule: REMEMBERED as standing, Mars 2026-10-31 ~18:34 CDT —
  research it + wire industry-standard layering 100% so the buried-arm
  mistake is not repeated and he does not have to repeat himself.
  Wire-up 100% workstream running (audit all poses, fix failures, pull
  Harmony/Animate/Godot/Spine/cel/Grease Pencil/OpenToonz methods).
  JoJo 03 and Ginyu 01 are in the face/cowl layering fix workstream.
No repo push in this task.

## Correction — face/cowl snap (Mars, 2026-10-31 ~18:27 CDT)
Mars flagged top row frame 3 (JoJo 03) and frame 6 (Ginyu 01) on the
contact sheet: the raised arm must go over torso AND face (JoJo 03)
and above the cowl/collar where the bicep was cut (Ginyu 01);
otherwise the set looks great / awesome. Fixed versions, new dated
files only, originals untouched, in
pose-dialects-fix-face-cowl-20261031/: JoJo 03 FACE-SNAP fixed +
Ginyu 01 COWL-SNAP fixed, before/after contact + face/cowl zoom
crops, gate script check_face_cowl_snap.py. Standing rule extended
in ARM-FRONT-SNAP-RULE.md (FACE/COWL SNAP EXTENSION): chest-only
= torso < arm < head; face-crossing = torso < head < arm; cowl-
crossing = raised bicep above collar. Fixed versions approval: 0/1.
