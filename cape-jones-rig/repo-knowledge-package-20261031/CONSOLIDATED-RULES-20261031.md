# CONSOLIDATED STANDING RULES — Cape Jones (2026-10-31)

Consolidation only: meanings are NOT changed. Where a rule was later
corrected, the correction is shown and the superseded line is marked
SUPERSEDED, never silently deleted. Original doc paths are given for
every rule — read the original before disputing a summary.

## R1. ARM-FRONT-SNAP + FACE/COWL SNAP (Mars 2026-10-31 17:58 + 18:27 CDT)
Original: `ARM-FRONT-SNAP-RULE.md`; gate:
`face-cowl-snap-wire100-20261031/check_pose_snap.py`;
builder: `face-cowl-snap-wire100-20261031/snap_figure.py`.
- Chest-only: torso < arm < head. Arm crossing the torso/pecs (forearm
  vs torso > 1,000 px at 1100x1500) snaps WHOLE chain (upper + lower +
  elbow cap + fist) above the torso, momentarily, per arm, per frame.
  Out-to-side = 0-268 px, crossed = 1,538-8,969 px. Upper-arm overlap
  is NOT the test (always 4,000+ px at the shoulder).
- Face-crossing: torso < head < arm. Forearm/lower vs head > 5,000 px
  = face-snap. Arm covers part of the face/cowl BY DESIGN of the pose.
  SUPERSEDED for face arms only: the old "head stays above a snapped
  arm" line.
- Cowl / cape-collar-crossing: UPPER-ONLY (banned: whole-chain cowl —
  JoJo 02 L whole-chain test puts the fist over the face, a gate
  failure in reverse). Candidate: elbow > 50 px above shoulder AND
  upper vs collar > 1,000 px, PLUS eye-check, never automatic.
  Normal shoulder-attachment collar overlap is 3,451-4,830 px, which
  overlaps the candidate range — hence eye-check stays.
- Priority: face > cowl > chest. Chest alone is a WARNING, not an
  automatic fail: it fails only if eye-check says the upper IS eaten
  and no snap was applied.
- Gate command (mandatory pre-delivery, run from pose angles BEFORE
  rendering — a flat PNG cannot prove layer order after the fact):
  `python3 check_pose_snap.py --name <pose> --upperL <a> --lowerL <a>
  --upperR <a> --lowerR <a> --head <a> --applied "L:<snap>,R:<snap>"
  [--eye-check "<note>"] --out audit.csv`. Exit 0 = PASS, 1 = FAIL.
- Wire-100 audit (2026-10-31): 31 angle-known entries = 62 side-checks:
  face-snap 2/62 = 3%, cowl-candidate 9/62 = 15%, chest-snap 8/62 = 13%,
  no snap 43/62 = 69%; entries with any snap/candidate 13/31 = 42%,
  clean both sides 18/31 = 58%. Fixes built: Ginyu 03 cowl-upper,
  v7c-jump cowl-upper (both viewed). False positives logged, not
  "fixed": JoJo 02 L (fist beside head, 2,996 px), stand-02 shadow
  (flat silhouette, no collar piece), stand-02 user + v7c-flex chest
  (forearms already in front, uppers at sides).

## R2. KNEE-FEET RULE, BIDIRECTIONAL, PER-FRAME (Mars 2026-10-31
## 16:09-16:14 + correction 16:58 CDT)
Original: `KNEE-FEET-RULE.md`; correction folder:
`dance-kneefeet-fix-correction-20261031/` (APPROVED 100% perfect).
- Knees and feet ALWAYS point the same direction. Knees out -> feet
  out; knees in -> toes in; straight -> straight. Exception only:
  a deliberately broken leg, named in the shot spec.
- Anatomy: knee tracks over the 2nd toe; tibial rotation / foot
  progression angle; valgus AND varus are both misalignments — the
  knee is a hinge, any mismatch reads broken.
- Fix = foot rotation/substitution on its axis, ankle intact, no
  detached feet. In 2D = drawing substitution, whole lower-leg piece
  swapped (original <-> FootIn mirror, knee anchor Front 95->59,
  Back 100->127).
- GATE (supersedes block ranges): FootIn = True ONLY IF leg_upper
  L > 0 AND R < 0 on THAT frame. A block range with no per-frame
  table FAILS the gate. Audit table must list every rendered frame.
- Keyframe audit 8/8 PASS: f001 OUT/OUT, f015 IN/IN, f028 OUT/OUT
  (the corrected frame — v1 had flipped it inward wrongly),
  f042 IN/IN, f056 OUT/OUT, f069 OUT/OUT, f083 OUT/OUT, f097 OUT/OUT.
  Correction rebuilt 63 frames, changed 20/63 (17 flipped back
  outward, 3 newly inward at f9/11/13).

## R3. GAUNTLET FLIP RULE (Mars 2026-10-31 15:00 + 15:21-15:22 + 15:33 CDT)
Original: `GAUNTLET-FLIP-RULE.md`; regression:
`check_gauntlet_flip.py` 5/5 PASS; `pose_driven_swaps.json`.
- Approved fighting pose: gauntlet-out-fixed (cuff-only per-row mirror
  y62-180; fist y180+ and forearm y0-62 pixel-identical). A
  fist-mirrored variant would be a NEW piece to approve, not a
  correction. Whole-band flip v1 REJECTED (floating +44/-61 px).
- Perspective: forearm ROLL = pronation/supination = DRAWING
  SUBSTITUTION in 2D, not limb movement. Driver is the HAND, not arm
  height. Check hand FIRST every pose: (1) elbow position, (2)
  forearm direction, (3) hand shape fist vs flat, (4) palm/thumb
  direction, (5) cuff piece selected and why. If (3)/(4) missing,
  don't build.
- Fist curled, thumbs toward midline/palm to camera, arms up (flex,
  fighting) -> cuff tops OUTWARD, fist thumbs INWARD (OutFixed/FlexOut).
  Hands flat/open, fingers straight, pointed OUTWARD ("snake hands")
  -> cuff tops INWARD is correct — the ONLY arms-up inward case.
  Arms down in front -> tops may face inward.
- Arm 2 fist-up rule: if Arm 2's fist is ever UP, the top of the arm
  pad (gauntlet) must be FLIPPED, arm stays in the SAME spot, AND a
  fist/hand from a DIFFERENT ANGLE is owed for the extended arm.
- Terminology: top-to-bottom = VERTICAL flip, left-to-right =
  HORIZONTAL. ARM 1 = our left = Arm_Front, ARM 2 = our right =
  Arm_Back, LEG 1 = Leg_Front, LEG 2 = Leg_Back.

## R4. ARM ALIGNMENT GATE (delivered, viewed)
Original: `ARM-ALIGNMENT-RULE.md`; gate: `check_arm_alignment.py`.
- PASS requires BOTH |axis-angle delta| <= 10 degrees AND |fist offset
  delta| <= 10 px vs v7c reference. Arm2 aligned v3 PASS (axis 5.6
  degrees, offset delta +4.8 px); BAD v2 was sheared (axis ~23 degrees,
  fist -26 px kink). Arm1 straightening still owed (QC FAILs on angle
  alone, +18.2 degrees).

## R5. RIM-COLOR RULE (Mars 2026-10-31 15:02 CDT)
Original: `RIM-COLOR-RULE.md`; doc in rig root.
- Rim light follows the key / LUT colour — same hue family, within
  +/-20 degrees. When the colour changes, the rim changes with it.
  Cyan rim under warm golden-hour grade was a bug, fixed to warm
  amber (255,180,80) with orange bleed (255,120,0).
- ONLY exception: a specific power that calls for a specific rim
  colour overrides the grade rim for that shot only, recorded in the
  shot spec by power name + rim + bleed, never carried over. No power
  named yet, so no override is active.
- Rim layering (corrected 17:02 + 17:05 CDT): HARD rim line is KEPT;
  soft rim kept too; Mars used "soft rim" and "soft halo"
  INTERCHANGEABLY — SAME thing, one layer. Default stack: hard rim +
  ONE soft layer, together, or soft alone, or hard alone as control.
  A three-layer stack is NOT the default (one experimental variant
  exists, labelled test, approval 0/1).
- Dual-light correction (15:48 CDT): cyan backlight god rays ONLY for
  CYAN RIM + GOLD LUT/overlay combined. Gold rim ALONE gets NO cyan
  backlighting.

## R6. UNIVERSE COLOR LANGUAGE + JOJO (Mars 2026-10-31 15:11, 16:35-16:40 CDT)
Original: `UNIVERSE-COLOR-LANGUAGE.md`, `-V2`, `-V3`, `-V3-ADDENDUM`.
- Colour is the universe language. Dialect 1 = lighting-motivated
  (LUT/grade/rim, rim follows key). Dialect 2 = JoJo non-canon palette
  shifts, NOT from lighting, for vibe/atmosphere/tension/power/
  uncertainty, alone or combined with lighting, using approved
  palettes, triggered by a story beat, returning to canon base.
- JoJo v3 = TRUE palette replacement, APPROVED: a shift BREAKS canon
  — world AND character colours change (flat colour reassignment by
  colour theory, shading as deltas, black outline never reassigned;
  PIL gain = Dialect 1, WRONG for Dialect 2). All v3 palettes/sheets
  APPROVED (TENSION, POWER, UNCERTAINTY, DREAM, DREAD, RESOLVE,
  ATMOSPHERE, OPPOSITION, BRIGHT PINK). Palettes are a living language.
- Base measured: cowl (90,39,114), skin (239,175,131), suit
  (255,255,255), suit shadow (178,186,199), cape (23,21,26).
- Combined image renamed BRIGHT PINK JOJO TENSION / PINK HOUR JOJO
  TENSION (never "golden hour").
- Cape+suit rule (16:35 CDT): in a shift, cape changes to a DIFFERENT
  FULL COLOR (not black, not dark tint); suit may stay white OR
  change — cool-first creative choice per beat, recorded in shot spec.
- JoJo language rule (16:39 CDT): shift is its own dialect, separate
  from lighting, CAN mix with lighting+effects and turn them UP —
  shot spec records shift alone / lighting alone / mixed + how.

## R7. LIGHTING LEVELS L0-L5 + PACKS v5/v6 + COLOUR-SHIFT RULE
Original: `LIGHTING-LEVELS.md`, `LIGHTING-LEVELS-VERBATIM-MARS-20261031.md`
(never edit), `LIGHTING-LEVELS-0-5.md`,
`godray-level4-20261031/LEVEL-4-5-SPEC-20261031.md`,
`godray-level5-20261031/PRESET-LEVEL-NAMING-CATALOG-20261031.md`.
- Mars verbatim: L0 none; L1 LUTs/lighting only; L2 shadows + outer
  rim + color bleed + color key bleed, NO god rays; L3 god rays + rim
  + full effects. Industry 0-5 extension in LEVELS-0-5.
- Level numbering rule (17:11 CDT): above L3 = Level 4, above that =
  Level 5, levels keep going up, never capped at L3, never call a
  higher mix "still L3". Visual anchor: L1/L2 may look like the V5
  BEFORE image; L3 looks like the V5 AFTER image; L4 is BEYOND the
  V5 after.
- L4 = all of L3 + >=3 of (interior directional light, hard+soft rim
  distinct, colour-preserved or measured/logged rims, foreground
  atmosphere/depth, gentler controlled bloom, ground light
  interaction). L4 candidate APPROVED as an L4 level (18:03 CDT).
- L5 = all of L4 + ALL of (crisp distinct shafts, true normal/depth
  interior shading, side-weighted wrap, full colour tracking,
  shot-to-shot consistency). L5 shot built (arms-up + apose, Blender
  5.2.3 compositor, crisp shafts 2-3 px edge, estimated-normal shading
  — true 3D-rebuild normal pass still owed), approval 0/1.
- Presets are a SEPARATE axis from levels (17:14-15 CDT): naming is
  exactly "lighting pack version five / six", NOT "lighting pack
  level". Pack v5 = V4/V5 BEFORE stack (pre-L3, L2-looking: flat rims,
  god-ray v1 density 0.12/spot 800, no bloom/spill). Pack v6 = V4/V5
  AFTER stack (the L3 stack: god-ray v2, Glare 0.75/6/0.35, default
  AgX). Levels axis = "go to level 0/1/2/3 in the lighting"; preset
  axis = "pull up lighting pack version five/six". L4 candidate is
  NOT pack v6 — if saved as a pack it gets a NEW pack version number.
- Colour-shift study + rule (17:14-15 CDT): study + log WHY overlays/
  comp change colour. Never call a colour the wrong colour once
  overlaid/changed. Every shot spec carries input_color +
  on_screen_color + mix_cause when they differ (within ~5/channel =
  "preserved"). Gold->red measured: input gold rim (255,180,80);
  L3 V4 on-screen core (204,162,114), cause = AgX view transform
  (split test Standard+Glare = (255,183,89), so Glare alone does NOT
  shift V4). V5 gold side on-screen (185,156,154) pinkish — second
  cause: split masks semi-transparent (max alpha 0.627) so gold mixes
  over cyan/teal in AlphaOver + bloom overlap at seam; view-transform
  fix alone does NOT fully fix V5 (opaque split rings still owed).
  Gold-preserved V4 (254,180,82) and V5 (216,161,159, still pinkish)
  are ACCEPTED as-is (Mars 18:03 CDT) — stop chasing perfect gold
  on V5. Same for gold-preserved V4.
- Level-3 threshold rule (16:21 CDT): V4-level mixing STARTS to get
  to Level 3. L3 requires ALL: bright volumetric rays, layered dual
  rim, bleed, light affecting shadows, more effects, motivated light.
  A mix that only looks L2 is NOT L3.
- Naming rule (18:03 CDT): Mars cannot tell some levels apart — name
  ALL presets/levels clearly with a visual difference sheet (plain
  words + side-by-side images) for every preset (Pack v5, Pack v6,
  Effects Sunbeam Preset v1, Default Afterglow Preset, Teleportation
  variant) and levels L0-L5. Catalog approval 0/1.

## R8. AFTERGLOW = SOFT RIM AS LIGHT TRAIL (Mars 17:36 + 17:38 + 17:49 CDT)
Original: `afterglow-20261031/`; presets:
`afterglow-videos-20261031/AFTERGLOW-SHOT-PRESETS-20261031.json/.md`.
- Identification (17:36 CDT): the loose light-shadow floating away
  from his outline in wrap v3 fighting = SOFT RIM (cyan (0,200,255),
  dilate 6, blur 5, 0.60), NOT hard rim, NOT a separate halo.
- Soft rim = light trail, NOT static (17:38 CDT): static soft rim
  looks ugly, makes him look not standing on the ground — like a
  shadow in the wrong place. It must MOVE when he moves: trail only
  in motion, fades, ZERO at rest.
- Afterglow test APPROVED (17:49 CDT): 18 frames, trail = past-position
  soft-rim bands, lag 6, fade 0.50/0.40/0.30/0.20/0.12/0.06, hold decay
  0.5/frame, final rest frame trail max 0.0078 (visually zero).
  Save as DEFAULT AFTERGLOW PRESET. Whole-body lateral glide version
  also reads as idle+moving at once = TELEPORTATION variant — save
  as-is as teleportation. That colour = his BASE afterglow colour;
  different powers/variations built off it later.
- Afterglow videos: real punch/fight limb move with afterglow as a
  VIDEO (approved -110 punch, trail behind fist/arm) + afterglow
  through Blender compositor per shot for all 30 shots CJ-01-CJ-30
  (no-motion shots = zero at rest, stated not faked). Punch video
  approval 0/1, shot videos 0/30. Shot presets 30/30 saved, with
  upgrade axes: scale_x/scale_y, expand_horizontal/expand_vertical,
  trail_lag_frames, trail_fade, power_effects (empty by default).
  Moving shots 15/30 = 50%, hold/still shots 15/30 = 50%.

## R9. COLOURED SHADOW MECHANIC / PRESET (Mars 2026-10-31 ~18:29 CDT)
Original: `pose-dialects-20261031/COLORED-SHADOW-MECHANIC-PRESET-20261031.md`
+ `COLORED-SHADOW-PRESET-20261031.json`.
- He is NOT a stand user. The thing behind him is a COLORED SHADOW:
  a flat, single-colour silhouette of his OWN rig, standing behind
  him, that acts like a stand and does its own thing behind him.
  Current colourway: purple silhouette (52,22,90), flat, no face,
  no costume detail. Position: behind, offset +180 px (stand-01).
  Behaviour: mirrors him sometimes (same flex angles), does its own
  thing other times (arms up while he crouches — shadow does the
  exaggeration, he stays grounded).
- Future use: to make ANY character ACT like a stand user for a beat,
  stage that character's own rig (or their FLA rig pieces) behind
  them as their coloured shadow. That is a staging choice for that
  beat, not a change to Cape's canon.

## R10. POSE DIALECTS (JoJo / Stand-pair / Ginyu-gag / Ginyu Force)
Original: `pose-dialects-20261031/POSE-DIALECTS-20261031.md`,
`ginyu-force-poses-20261031/GINYU-FORCE-POSE-STUDY-20261031.md`,
`ginyu-force-limits-broken-20261031/`.
- JOJO-POSE: dramatic, fashion, hold. Use sometimes, never as default
  stance. Contrapposto, S/Z silhouette, hand choreography, hold timing.
- STAND-PAIR: power reveal / power-up gag. Stand = silhouette of his
  own rig, never a show character, never named as a show Stand.
  Superseded by R9's name: COLORED SHADOW.
- GINYU-GAG: funny, comedic, pose/dance, roll-call timing
  (announce hold 12f -> snap 2f -> hold 12f+). Comedy beats only.
- Ginyu Force: 5 core (Captain Ginyu, Jeice, Burter, Recoome, Guldo)
  + 1 former (Bonyu — withdrew because she hated posing, Kakarot
  simulation side-quest only, NOT part of the classic team pose).
  Roll-call order: Recoome -> Burter -> Jeice -> Guldo -> Captain
  (last, centre), final spread as unison beat. Formation order
  differs (Recoome, Jeice, Ginyu centre, Burter, Guldo) — do not
  confuse them. Solo borrowing = a sequence, not a team, never
  impersonation.
- Limits-broken work: Burter extended kick, segment torso twist,
  Jeice open-palm serve swap, per-member effects (Recoome blast,
  Burter hurricane, Jeice ball, Guldo time, Ginyu swap beam) — see
  Gaps Index for what is still labelled vs proven.

## R11. CLEAN-CUT RULE + IMAGE-CACHE + LABELS-DEBUG-ONLY
Original: `CLEAN-CUT-NOTES.md`, `CLEAN-SLICE-BATCH-20261031.md`,
`LABELS-ARE-DEBUG-ONLY.md`.
- Clean cuts using `slice_clean.py` in rig root (bg from corners,
  mask distance > 30, closing + hole fill, components by the sheet,
  rows by centre-y, 1px feather + fringe decontamination). rembg
  (venv `~/workspace/cape-jones-rig/venv`, u2netp) only per-piece as
  a check.
- Image-cache rule (15:04 CDT, re-confirmed 16:30 CDT): when showing
  a new version of an image, ALWAYS use a new dated/versioned
  filename — same filename = Mars's phone shows the cached old image.
  Always label every image NEW vs RE-SEND; never present a re-send
  as an improvement.
- Labels are debug only: red numbered ARM/LEG circles are tool/debug
  pieces, never part of a scene, never rim-lit. Part LABELS (what a
  piece IS) belong on reference/catalogue sheets only, never baked
  into clean scene pieces.

## R12. SHOW-BUILDING METHOD + PULL SCOPE (Mars 2026-10-31 15:18-15:27 CDT)
Original: `SHOW-BUILDING-METHOD.md`, `SHOW-REPO-DEEP-AUDIT-20261031.md`,
`WIRED-PULLS-20261031.md`.
- Build like Robot Chicken / South Park / Family Guy / Simpsons:
  reference + transformation, not theft. Pipeline: placeholder/test
  character -> kitbash + reskin -> redesign -> completely different
  original character, art style may stay similar (style != identity).
  Barred ONLY: exact likeness shipped as-is, character literally,
  name, script dialogue, logo.
- Pull ANYTHING from show repos (any type of move, anything helpful,
  not just dances) EXCEPT the ONLY barred five: (1) exact character
  likeness image shipped as-is, (2) using their character literally,
  (3) character name, (4) dialogue literally from their script,
  (5) brand image/logo. Character image may come over ONLY as
  production reference if edited/modified into a parody character
  or a whole different character before release — never shipped as
  their character. Flagged TRANSFORM-ONLY.
- Terminology: placeholder/test/stand-in (temp art, greyboxing) ->
  reskin = palette/texture only -> kitbash = parts combined ->
  redesign/rework = colors+parts+silhouette changed = completely
  different original character.
- License does NOT block eye pulls (Mars 16:53 CDT): "I don't care
  if the packs are licensed or not, or open licensed. I don't care
  about that." Record the source plainly and move on.
- Comparison loop, universal (15:39-15:40 CDT): for ANY tool and
  ANYTHING ELSE reverse-engineered — use theirs legitimately
  (trial/subscription), learn as we use it, reverse-engineer its
  methods, wire our own version as we use it, then comparison-test
  ours vs theirs (as good or better). 7 tests (rig pose, timeline/
  xsheet, deformation, drawing substitution, export, colour, audio
  sync); a test counts only when BOTH sides have a viewed file;
  "better" must name what is better. Tests run 0/7 (no their-side
  viewed files; blocked on legitimate Harmony/Animate trial installs).
  Tools in scope: Harmony, Animate, After Effects, Maya,
  OpenToonz/Tahoma2D, Blender, Wick/Brinimate, any future tool in
  FREE-FIRST-WIRING.md. A tool is not "done" until its comparison
  tests are run.

## R13. NEVER RECOLOUR BASE ART + VFX HAND-TOOL STOP + BLENDER VERSION
Original: `COLOR-LIGHTING-COMPOSITING-RESEARCH-20261031.md`,
`blender-composite-fix-20261031/`.
- Never recolour the base art (13:44 CDT): original untouched;
  light/shadow/bleed on separate layers (Screen/Add for light,
  Multiply hue-shifted for shadow).
- VFX hand-tool stop (13:40-13:43 CDT): no hand-drawn PIL VFX
  presented as production. Flat PIL VFX is draft only. Production
  VFX = Blender compositor + authored VFX, GPU run when needed.
- Production default Blender 5.2.3 LTS. Blender 5.2 compositor facts
  (verified): `CompositorNodeComposite` UNDEFINED in 5.2 (no output);
  saving .blend alone produces NO image (needs real render,
  `use_compositing=True`, `write_still=True`); MixRGB Add with small
  Factor crops to a strip — fix = rim via SetAlpha + AlphaOver.
  Newly created Material Output nodes are INACTIVE in 5.2 (reuse
  original Output or black frames); Sun Beams is a Glare TYPE not a
  node; Glare outputs only the glow pass so original must be added
  back; libEGL missing on VM -> Eevee aborts, Cycles CPU is the
  working replacement (run under xvfb-run).

## R14. RIG BASICS + JOINT CLEANUP FOR LATER
Original: `joint_locked_rig_v7c.py`, `cut-limbs-v7c/`,
`reposes-v7c-clean/`, `joint-cleanup-20261031/`.
- v6 approved T-pose/A-pose lock but DO NOT USE for bent arms/legs
  (pivots wrong). Measured ball centres: Arm_Back elbow (99,222)
  R~30, Arm_Front elbow (~60-62,222) R~30, Leg_Front knee (95,314)
  R~26, Leg_Back knee (100,314) R~26.
- v7c: pivot = ball centre, parent trimmed at ball, child =
  whole-limb crop from ball centre, single circular cap. Clean mode:
  `labels=False`. Clean poses in `reposes-v7c-clean/` (6), clean
  plate `rig-apose-v7c-clean-transparent.png`, clips in `clips-v7c/`.
- Joint-cleanup for LATER (Mars 17:04 CDT): elbow/knee round joint
  balls are FINE for now — do NOT remove now, they help understand
  the rig. LATER goal: make him look less like an action figure by
  cleaning up those round joints. Tooling built
  (`joint-cleanup-20261031/clean_joints.py` + tests on COPIES only,
  never on approved poses), logged READY-FOR-LATER; actual cleanup
  on approved poses only when Mars says go (0/1). Minor wrist-meets-
  fist polish accepted as "good enough" fallback. Tool findings:
  taper FAILS on flex elbows (endpoint joints — guard returns 0 px);
  cap omission alone does NOT de-ball an elbow (round shape is in
  the pieces' own rounded ends); a real de-ball pass needs tapered
  piece ends. Incident (plain ownership): first cap-omit run
  overwrote approved true final + over-exaggerated files, then
  restored them — true final md5 verified 03d282c8... identical.

## R15. ROOM SCALE + SEATED SCALE (Mars 15:34 CDT)
Original: `showcase/layout-pass-room-scaled-25x-20261031.jpg`.
- Room scale locked 2.5x = 1/1: rig 950 px tall, feet on floor,
  chair back at his waist. Room ONLY (batch-KKGuh); other
  backgrounds' scale "pretty good," do NOT change.
- Seated scale rule (approximate, verify visually): seated =
  standing factor - 0.2 (2.5x -> 2.3x seated).
- Canonical room ID still open 0/1: is batch-KKGuh canonical?
  Note: batch-KKGuh was NOT found on disk in a later pass and the
  locked room sheet carries a labelled character, so the room-at-
  2.5x Blender proof used a desk-painting substitute — chair-back-
  at-waist NOT claimed against the substitute; true-room re-check
  still owed.

## R16. FISTS, EYES, VISEMES, CAPES (summary — see originals)
- Fist v3 = palm-facing / upward-facing ONLY, NOT a punching fist
  (Mars 16:41 CDT: a front-facing fist shows KNUCKLES, no palm).
  Fist v4 REJECTED (17:05-17:06 CDT): PIL vector shapes = hand-tooled
  in effect, NOT generated/pulled. Fist v5 = Mars's own upload
  (two front-facing fists, knuckles top, near-white, beige bg) —
  pulled + cut out + desaturated to 15% chroma + fitted, NOT
  generated, NOT vector. First seating rotated 180 degrees =
  UPSIDE DOWN for a forward punch — that orientation is an
  UPPERCUT. Flipped forward punch APPROVED (17:48 CDT); uppercut
  set saved separately.
- Eyes: strips WITH pupils = COMEDIC RELIEF EYES only (he only
  sometimes has pupils, for comedic effect). Normal eyes =
  Batman/Teen Titans-like, white angular, strong lids/brow, normally
  NO pupils. Eyes v3 = hand-tooled vector -> FALLBACK/DRAFT/
  PLACEHOLDER/REFERENCE ONLY, never approved normal eyes. NO extra
  black outline rule (16:50 CDT): pulled shape sits IN his own mask
  openings, cowl IS the mask, no second mask layer/ring. Eyes v4 =
  REAL pulled shapes — Teen Titans repo, ROBIN Day.jpg model sheet
  head close-up white eye blobs extracted verbatim — in-mask fit
  APPROVED / PERFECT (17:30 CDT). Generic superhero eyes rule
  (17:32 CDT): almost any superhero with white angular eyes fits.
  Facetop ears-off = NO as face top (3D Batman photo mask, not 2D
  animated Batman) — keep ONLY as a parody prop (Halloween gag).
  Rounded animated cowl top still owed 0/1.
- Visemes v1 REJECTED for approval (15:59 CDT, too hand-tooled; fix
  for O/OO/W = cover previous mouth AND cheek lines with skin colour
  first, then draw new mouth on clean skin). Visemes v2 COMPLETE,
  built + viewed, NOT approved (mask-first method, 14/14 shapes).
- Capes: v1 states good for light movement only. Cape styles v2
  COMPLETE, 15 forms, approval 0/1. Cape bone-chain diagram + pose
  composite built (B0 neck -> B1 -> B2 -> hem fan, lag 1-2f, cape
  NOT baked into body). Still owed: bone-chain rigged in an actual
  pose 0/1, cape in final shot with body 0/1.

## R17. TRACKER + TOOL-PASS LOG + SHOW-AS-DONE + CHAT-VIEWABLE
Original: `TOOL-PASS-LOG.md`, `TRACKER-20261031.md`,
`STATUS-20261031-1428.md` (append-only).
- Tracker + tool-pass log (Mars 15:26-15:32 CDT): in EVERY message,
  name all tools being pulled in and their percentages, and what
  percentage everything is at; list EVERYTHING (todo + completion +
  percentages) every time, never partial lists; every pass shown to
  Mars must say "this is me using this and this" — all tools/
  resources of every pass named in the chat message AND logged in
  TOOL-PASS-LOG.md.
- Show-as-done rule (15:45 CDT): show anything that needs to be
  shown, show ALL of it that can be shown visually or audio-wise,
  show it AS IT GETS DONE — visuals in chat, audio as links.
- Chat-viewable rule (corrected 16:25-16:29 CDT): STOP sending file
  types that cannot be previewed in chat. Non-viewable files go in
  the repo / plain text only, NEVER as chat file links.
- Re-presentation rule (18:01 CDT): anything that is Mars's pick or
  needs Mars's approval must be SHOWN AGAIN in chat (embedded) —
  Mars does not know where those files are otherwise.
  Already-approved items show as approved, not re-asked.
- Critique-learning (16:40 CDT): learn from every critique, research
  the WHY in anatomy/animation, pull industry-standard fixes, log it
  all in the repo so Mars doesn't repeat himself. Log:
  `gap-audit-critique-log-20261031/CRITIQUE-LEARNING-LOG-20261031.md`,
  13/13 entries (C-01 knee-feet ... C-13 never recolour base art).

## R18. MOCHIICHAO CANON LIMIT (Mars 15:36 + 16:06 CDT)
Original: `MOCHIICHAO-COMBINE-20261031.md`.
- Cape Jones / Space Jones has a DIFFERENT canon/show language than
  Mochiichao. Bring only a little Mochiichao aspect/soul (like the
  Western Heart aspect). No canon merge, no Mochiichao roster/world/
  story/battle numbers, no Mochiichao species as itself in a Cape
  background.
- Scope limit: Mochiichao goes deeper ONLY in an episode/scene about
  him playing it, or shorts where Mochiichao characters might appear
  and dance with him — those need full rigs/FLAs/cut-out pieces and
  come LATER, after placeholder characters from other shows are
  pulled and wired.
- Handheld gag device (GBA + Tamagotchi mix) is ALWAYS in his pocket
  even though he has no visible pockets (hand to hip/cape fold,
  appears/vanishes off-screen, never a pocket opening/bulge/flap).

## R19. AUDIO + EFFECTS + TV PRODUCTION STACK
Original: `EFFECTS-DESIGN-V2-20261031.md`, `TV-PRODUCTION-STACK-20261031.md`,
`gap-close-sound-edit-20261031/`.
- Audio delivery: when sending audio, do NOT send audio in chat —
  send LINKS in chat. Demo tones only so far; recorded final audio
  0%. Sound layer stack 5 layers -> 5 cues, -14 LUFS target;
  gap-audit mixed demo measured -16.27 LUFS, TP -1.39, LRA 8.50 —
  NOT -14, honestly named `measured`.
- Effects v2: 12/12 VFX systems each with a real Blender node setup
  (volumetric god rays, bloom/spill, haze, particles, impact
  shockwave+flash, fire/energy aura, water/reflection, smoke/steam,
  motion blur/speed lines from joint paths, DOF/lens, electricity,
  effect shadow casting). Proof frame viewed — systems with a viewed
  frame 4/12 (god rays, bloom/spill, dust, ground pool+shadow).
  Mars verdict (17:47 CDT): REALLY GOOD light, REALLY GOOD sunbeams;
  arms-up reads like "two double yellow spirit bombs" (energy orbs
  at raised fists — a read, not a character). Save v2 stack EXACTLY
  as Effects Sunbeam Preset v1 (versioned, reproducible), THEN
  upgrade it (orb snap to fists, denoise, shaft masking).
- TV production stack: documents complete (10/10 diagrams); fully
  wired 3/10 = 30%, partially 7/10 = 70%. Shot specs 30/30 (CJ-01-
  CJ-30, JSON+MD, all Mars approval PENDING) + god-ray decisions
  30/30 = 9 Level-3 placements + 21 explicit L2 no-god-ray decisions.

## R20. INBETWEENING + 2.5D DEPTH (Mars 2026-10-31 18:36 + 18:42 CDT)
Original: `inbetween-20261031/`; 2.5D work (separate workstream, see
Gaps Index — its folder is a landing-batch item, not in this package
as a finished system until its report lands).
- Inbetweening = more drawings per second, transitioning frames
  BETWEEN motions, more frames per action and per second, to make
  it look cleaner. Keys -> breakdowns -> inbetweens, easing
  (slow-in/slow-out), arcs, timing charts. Standards: 12 fps on
  twos vs 24 fps on ones; TV 24/25/30 fps.
- Extrapolation vs interpolation, labelled: inbetweens =
  interpolation BETWEEN keys; extrapolation = extending a motion
  BEYOND a key (overshoot, follow-through). Use both correctly.
- Cutout inbetweening = interpolating joint angles/positions
  between key poses, not redrawing. Image interpolation (alpha
  blend between pose images) must be LABELLED as image
  interpolation, NOT rig inbetweening — never fake a rig pass.
- 3D camera depth IN 2D (Mars 18:42 CDT, rejecting "not applicable"
  as final): 2.5D / multiplane methods — Disney multiplane camera,
  parallax layers, depth-by-scale, depth-by-blur/atmosphere, Z-order
  as a depth axis, Blender camera + Grease Pencil in 2D, After
  Effects 3D camera on 2D layers, Spine/Moho depth / mesh warping
  for pseudo-3D turn. Experimental until proven, labelled
  EXPERIMENTAL, never production-proven until viewed + approved.

## R21. ADR / LIVING DOCUMENTATION (pulled in this package, 2026-10-31)
Method: Architecture Decision Records (ADR) — a short, dated record
per major decision: context, decision, consequences, status
(accepted / superseded). Wired here as `ADR-20261031.md` (8 records)
+ this package's rule that every future standing rule change gets
an ADR entry, not a silent edit. Onboarding README pattern: a new
worker reads README -> MEMORY-NOTE -> CONSOLIDATED-RULES ->
APPROVALS -> GAPS, in that order, before touching a builder.
Living documentation rule: docs are updated in the SAME task that
changes the thing they describe, or the task is not done.

## R22. PERCENTAGE + AUTONOMOUS CONTINUATION + PUSH-THEN-CLEAN
(see README-INDEX for full text; summarised here so no worker misses
them)
- Percentage rule (2026-10-25): item — X% done, with the count
  behind it (e.g. 7/16 = 44%). Never "not done" without a percentage.
  If you cannot count it, say what you counted and what you did not,
  and give your best counted estimate labelled as an estimate.
- Autonomous continuation (2026-10-25): keep working without
  stopping, without making Mars repeat himself; surface results,
  blockers, and Mars-only decisions first, never silently decide them.
- Push-then-clean (2026-10-27, expanded 2026-10-31 17:41 + 17:50):
  everything on disc 100% into its repo if there is absolutely no
  reason not to, PR-only, 0 deletions unless Mars approved that exact
  deletion, no force-push, merge gate, confirm in repo by remote API
  size+SHA / blob-SHA on main after merge, only then clean the
  verified local copy. Never delete our work; checkpoint files never
  deleted; uncertain = keep + report. Save ALL specs + information
  of everything done to the repo so it can always be revisited or
  recreated (2026-10-31 17:50 CDT).
