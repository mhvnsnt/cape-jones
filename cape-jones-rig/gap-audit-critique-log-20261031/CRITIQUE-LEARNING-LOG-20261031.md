# Critique-Learning Log — Cape Jones (Mars, 2026-10-31)
## Purpose
Log every Mars critique once, with the anatomy / animation reason it was right,
the industry-standard fix, and the pipeline gate that now prevents a repeat —
so Mars does not have to repeat himself. New critiques append here; nothing
in this file is overwritten. Approval status is Mars's alone; this log does
not claim approval for any piece it describes.

Sources for the anatomy / animation principles (methods only, no copied art):
- Knee tracking: the knee tracks over the second toe; tibial rotation sets
  foot progression angle; external tibial torsion drives valgus / patellar
  maltracking. In animation terms: a hinge joint (knee) and its foot must
  share one rotational axis, or the leg reads broken.
- Forearm rotation: pronation / supination is radius crossing over ulna
  (palm down / palm up, ~180° arc), not a wrist twist. In 2D cutout this is
  DRAWING SUBSTITUTION — swap the cuff / fist piece — not a rotation of
  the limb piece.
- Fist closure (Hogarth, Drawing Dynamic Hands): in a tight fist the index
  proximal knuckle projects beyond the other knuckles; the thumb closes in
  opposition, its tip abutting the middle finger, thumb line running
  diagonally across the knuckles. A front-facing (punching) fist shows
  KNUCKLES to camera; a palm-facing fist shows PALM. They are different
  pieces, not rotations of each other.
- 12 Principles (Thomas & Johnston, The Illusion of Life): squash &
  stretch (volume constant), anticipation, staging (silhouette), pose-to-pose,
  follow-through / overlap, slow in-out, arcs, secondary action, timing,
  exaggeration, solid drawing, appeal. Smear frames: a fast move drawn as
  a stretched / multi-image frame, not a blur filter.

## Entries

### C-01 — Knee-feet rule (Mars, 2026-10-31 16:09-16:14)
- Mars said: knees and feet must point the same direction. In the improved
  dance, knees angled acutely inward while toes pointed elsewhere read as
  broken knees — "like someone hit him in the knees with a baseball bat."
  Fix frames 15 and 42 and any other inward-knee frames.
- Why right: knee = hinge over the ankle; the lower leg rotates on its
  axis (tibial rotation / foot progression angle). If the knee points in
  and the foot points out, the tibia is drawn twisted past its joint —
  the anatomy reads as injury, not style. Exception only: a leg actually
  broken in story.
- Fix: foot rotation / substitution on its axis, ankle joint intact, no
  detached feet. Dance-kneefeet fix built 2026-10-31 (before/after proof).
- Gate: KNEE-FEET-RULE.md — before any pose ships, check knee direction =
  foot direction FIRST, same angle. A pose failing this check is a defect,
  not a style choice, and does not ship.

### C-02 — Gauntlet flip / hand-first rule (Mars, 2026-10-31 15:21-15:33)
- Mars said: forearm roll is driven by the HAND, not by arm height.
  Check hand first every pose: elbow position, forearm direction, fist vs
  flat, palm / thumb direction, then cuff piece and why.
- Why right: pronation / supination changes which face of the forearm and
  hand the camera sees. In cutout you cannot rotate a flat piece into a
  new face — you must substitute the drawing. Flipping a whole band
  (v1) floated pieces +44/-61 px because it ignored the hand.
- Fix: per-row flip within each row's own alpha span only (OutFixed,
  cuff y62-180); fist and forearm pixel-identical. Approved OutFixed is
  cuff-only; a fist-mirrored variant is a NEW piece to approve.
- Gate: GAUNTLET-FLIP-RULE.md + check_gauntlet_flip.py (5/5 pass) +
  pose_driven_swaps.json. Rule in one line: hand first, then cuff.

### C-03 — Arm 2 fist upside-down (Mars, 2026-10-31 16:25-16:31)
- Mars said: the Arm 2 different-angle fist in forearm v2 is upside down,
  not a good fist. The other two fists were right. Arm 2 overall was done
  badly / not clean, and its forearm was not lined up correctly.
- Why right: a fist has a strike end (knuckles) and an attachment end
  (wrist). V2 put fingers up and cuff at the bottom against a forearm
  above it — strike end and attachment end reversed, a 180° flip against
  the forearm axis. No fist reads correctly with its wrist away from
  its arm.
- Fix: forearm-fist-v3 — front-facing Hand_1_Fist as base, wrist meets
  forearm, knuckles at strike edge, thumb wrapped across the front,
  wrist cap BEHIND the fist, old fist fully erased (cut y=88).
  Arm2 alignment diagnosed separately (centres / axes vs Arm 1 + v7c
  geometry) and rebuilt aligned, with an alignment QC script wired in.
- Gate: wrist-attachment check — wrist end must touch the forearm, cap
  behind, single fist, no peek-through — on every fist piece, before
  any punch pose is built from it.

### C-04 — Fist v3 is a palm-facing fist, not a front-facing punching fist
  (Mars, 2026-10-31 16:41)
- Mars said: v3 shows the palm. A front-facing fist shows the knuckles
  to the front; you do not see the palm. Save v3 as a palm-facing fist,
  not a punching fist. Generate an actual front-facing fist, knuckles
  at the top, facing you. (Perspectiving the palm fist into a punch
  fist is possible, but not preferred.)
- Why right: Hogarth fist closure — knuckles are the striking face.
  A palm view and a knuckle view are different drawings (different
  visible surfaces, different thumb wrap), not one drawing rotated.
  Calling a palm view a punching fist teaches the rig the wrong piece
  for every punch that follows.
- Fix: rename / reclassify v3 as palm-facing (do not delete it — it is
  a valid piece for a palm / open-hand beat); build a new front-facing
  punching fist piece with knuckles top, facing camera, thumb wrapped
  across the front, wrist at the back. V4 task, separate from v3.
- Gate: fist-view naming rule — every fist piece is named by what the
  camera sees (knuckle-front / palm / back / side), never just "fist".
  A punch pose may only use a knuckle-front piece.

### C-05 — Full final flex: biceps +15, wrist clench, wrist angle +5,
  clean wrists; over-flex vs true final flex (Mars, 2026-10-31 16:40)
- Mars said: the full final flex is really good / really close, and can
  be used as a different frame — an OVER-EXAGGERATED flex, when he
  over-flexes this far. The actual true final flex is a little more
  relaxed in the arms and cleaned up around the wrists: biceps need to
  angle up toward his head about 15° more, wrists need to be clenched
  up where wrist connects to forearm, the acuteness between forearm
  and wrist opened up about 5° (a little more space there), and the
  area around the wrists cleaned up. Even the over-flex frame needs
  wrist cleanup.
- Why right: a double-bicep flex is biceps brachii shortening (elbow
  flexion + shoulder flexion) with the forearm supinated and the wrist
  in a tight, clenched fist — the wrist is a transitional block, not a
  loose hinge. If the wrist-forearm angle is too acute, the fist reads
  folded / broken; if the cap ring crosses the fist face, the joint
  reads detached. Exaggeration (Principle 10) is a range, not one pose:
  the over-flex is the pushed extreme, the true final is the held pose.
- Fix: true-final-flex v2 (owed, new dated file, 30° and full-final
  untouched): biceps +15° toward head, wrist clenched at the forearm
  junction, forearm-wrist angle +5° more open, wrist caps behind fists
  and cleaned. Full-final (75°) reclassified as OVER-FLEX frame.
- Gate: flex poses are named by their place in the range (anticipation
  / true-final / over-flex), never just "flex". Wrist-seam check (cap
  behind, no ring across fist face, no gap rows) on every flex frame.

### C-06 — Cape under a JoJo shift: dark-tint superseded by full colour
  (Mars, 2026-10-31 16:14, 16:35)
- Mars said: a JoJo shift BREAKS canon — world colours AND character
  colours change; he cannot stay base with an overlay on top. Later:
  the cape would probably change from black to a different colour also;
  the suit might stay white or might change sometimes; creators do it
  by feel / what would look cool.
- Why right: JoJo's method (Araki: no canon character palette; David
  Production re-paints character flats + costume + environment together
  per beat) is palette REPLACEMENT, not grading. A gain / overlay
  preserves base hues — that is Dialect 1 (lighting), not Dialect 2.
  A dark tint of black is barely a change at all; it does not read as
  "rules have bent."
- Fix: V3 palette replacement (each part reassigned a new flat colour,
  shading carried as deltas, black outline never reassigned) + V3
  addendum: cape = full colour, suit = white OR changed, choice =
  cool-first per beat, recorded in shot spec.
- Gate: Dialect 2 check — a shift sheet must show character colours
  changed, not just the background, and must name trigger + scope +
  duration + return-to-base, or it is not a shift, it is a grade.

### C-07 — JoJo language is its own dialect, and it can MIX with
  lighting / effects (Mars, 2026-10-31 16:39)
- Mars said: approved on all of these — tension, hot pink, pink-violet,
  world differences, all of that. When we change how he looks and how
  the world looks in JoJo segments, that can go hand in hand with the
  lighting language, but it is separate from that, and it can create
  segments WITH that too. It has its own language and dialect times,
  and times where it mixes with lighting, colour bleed, rim lights,
  god rays — when it mixes, it mixes crazy, it turns all of it up.
- Why right: a colour dialect and a lighting system are different
  axes (what colours ARE vs how light FALLS on them). Collapsing them
  into one system forces every shift to be a lighting change and every
  lighting change to be a shift, which kills both. Kept separate, they
  compose: a shift sets the palette, lighting sets rim / bleed / rays
  IN the shifted palette (rim follows the SHIFTED key, ±20°).
- Fix: UNIVERSE-COLOR-LANGUAGE V3 + addendum; shot specs carry BOTH a
  shift field and a lighting field, each with its own return rule.
- Gate: a shot spec with a shift must still pass the rim rule under
  the shifted key, and a lighting-only shot must not be labelled a
  JoJo shift. Mixed shots are labelled MIXED, not one or the other.

### C-08 — Eyes: dark side flipped to the Arm 1 side; normal eyes are
  white angular, comedic eyes are the pupil set (Mars, 2026-10-31
  16:00, 16:27)
- Mars said: Pack 4 eye strips are NOT his normal eyes — they are
  COMEDIC RELIEF eyes (the ones with pupils; he only sometimes has
  pupils, for comedic effect only). Normal eyes are Batman-like /
  Teen Titans-like: white angular, strong lids / brow, normally NO
  pupils. Later, three times: v2 darkened the WRONG end segment — the
  dark side / shadow goes on the ARM 1 side; flip it.
- Why right: an eye strip is read by its lid / brow line and by which
  end carries shadow (the side away from the key light, and the side
  that matches the head's facing). Shadowing the wrong end flips the
  light direction on the face and breaks the head's volume. And a
  pupil set used as the default changes the character's identity —
  pupils are a performance choice, not a default.
- Fix: eyes-normal-superhero-v3 — dark end flipped to Arm 1 side,
  pulled-back band end, tapered ends, proof on Head_Front + v2-vs-v3
  before/after; v1 pupil strips saved as COMEDIC RELIEF only.
- Gate: EYE-RULES-NORMAL-VS-COMEDIC — normal / serious / action =
  v3, no pupils ever; comedic beat only = v1 pupils; unsure = normal.
  Dark-side check against the Arm 1 side on every eye proof.

### C-09 — Visemes v1 too hand-tooled; mask-first fix (Mars, 2026-10-31
  15:59)
- Mars said: visemes v1 are too hand-tooled; good start, not good
  enough. For O / OO / W circular mouths: the previous mouth must be
  MORE covered with skin colour first — mouth line AND cheek lines
  covered where the new mouth sits — then the new circular mouth
  drawn on clean skin.
- Why right: drawing substitution only works if the old drawing is
  fully removed first. Pasting a new mouth over old linework leaves
  ghost lines (show-through), which reads as a dirty drawing, not a
  new mouth shape. Toon Boom mouth-chart method: the base head
  carries NO mouth; each viseme is a clean swap onto a clean base.
- Fix: visemes v2 — layer order head base -> SKIN MASK (gradient
  inpaint of the mouth zone, feathered elliptical mask) -> new mouth
  -> outline; clean head base with no mouth as a reusable layer.
  OO true circle 92 px, W true circle 72 px, previous line gone.
- Gate: mask-first rule — no viseme ships unless its before/after
  proof shows zero old-mouth line inside the mouth zone. The same
  mask-first method is owed for eye strips / expressions.

### C-10 — Flat PIL VFX are stickers, not effects; production VFX =
  Blender compositor (Mars, 2026-10-31 13:40-13:43, 15:44)
- Mars said: no hand-drawn PIL VFX presented as production. Flat
  coloured lines and circles are stickers, not effects. A real effect
  must (1) look real, (2) affect the world (spill light, cast shadow,
  kick dust), (3) bring atmosphere (haze, glow, flash, fog).
- Why right: an effect that sits ON TOP of a frame without interacting
  with its light, shadow, or atmosphere breaks the frame's lighting
  continuity — the eye reads it as a sticker because it has no
  physical relationship to the scene. Volumetric / compositor effects
  have that relationship by construction (they are light in the
  scene, not paint on the picture).
- Fix: Effects v2 (12 VFX systems, Blender compositor / volumetric);
  PIL VFX labelled DRAFT only, never production. Blender compositor
  fix: Composite node is undefined in Blender 5.2, compositor only
  runs on a real render with use_compositing + write_still; rim via
  SetAlpha + AlphaOver, not a small-Factor MixRGB Add.
- Gate: production-effect test — does it spill onto the character /
  ground, cast or affect a shadow, and change the atmosphere? If any
  answer is no, it is a draft, not a production effect.

### C-11 — Image cache: new version = new dated filename, never
  overwrite (Mars, 2026-10-31 15:04, 16:30; re-send incident 16:29-16:31)
- Mars said: when showing a new version of an image, ALWAYS use a new
  dated / versioned filename — same filename = his phone shows the
  cached old image. Re-sends of the same files, presented as if they
  were improvements, were correctly spotted by Mars as the old
  rejected images.
- Why right: this is a delivery / caching fact, not a taste point.
  A phone image cache keys on filename / URL; reusing a name serves
  the old bytes. Presenting a re-send as an improvement destroys
  trust in every later "new version" claim.
- Fix: checkpoint / version-lock rule — every version its own dated
  checkpoint, logs append only, monotonic versions, newest approved
  edit is current. Every message labels images NEW vs RE-SEND.
- Gate: version-lock check — a file Mars has seen is never overwritten;
  a new version ships under a new dated filename, or it does not ship.

### C-12 — Labels are debug only; chat-viewable delivery only
  (Mars, 2026-10-31 14:51, 16:25-16:29)
- Mars said: red numbered ARM / LEG circles are tool / debug pieces,
  never part of a scene, never rim-lit. Part LABELS belong on
  reference / catalogue sheets only, never baked into clean scene
  pieces. And: stop sending file types that cannot be previewed in
  chat. Non-viewable files (blend, json, md, html, scripts, docs,
  folders) go in the repo / are mentioned in plain text only, never
  as chat file links. Remote-storage links are download links, not
  viewable links — in chat, send visuals as embedded images that show
  right in the chat; audio stays links-only.
- Why right: a debug label baked into a scene piece contaminates every
  shot built from it (the label becomes part of the character). And a
  delivery the phone cannot preview is not a delivery — it is a chore.
- Fix: label gate — clean renders refuse plates with >100 pure-red
  pixels; catalogue sheets carry labels, pieces do not. Chat delivery
  rule: embedded images in chat, links only for audio.
- Gate: label gate + chat-viewable check on every delivery. A clean
  piece with a label pixel, or a chat message with a download link
  posing as a view, fails the gate.

### C-13 — Never recolour the base art; light / shadow / bleed on
  separate layers (Mars, 2026-10-31 13:44)
- Mars said: original art untouched; light / shadow / bleed on
  separate layers (Screen / Add for light, Multiply hue-shifted for
  shadow).
- Why right: a LUT / grade multiplies what is there; it does not paint
  over it. Baking a grade into the base destroys the canon palette
  and makes every later grade compound on a corrupted base.
- Fix: LUT-first pipeline, rim / bleed / shadow as separate layers;
  base palette measured (cowl 90,39,114; skin 239,175,131; suit white;
  cape 23,21,26) and never edited in place.
- Gate: base-art check — a graded render must be reproducible from
  the untouched base + named LUT + named rim / bleed, or it is not
  a valid grade.

## How to use this log
1. Before building a pose, piece, shift, or effect, read the entries
   that touch it (knee-feet for any leg pose, hand-first for any arm
   pose, fist-view for any punch, wrist-seam for any flex, Dialect 2
   for any shift, mask-first for any mouth / eye swap).
2. Run the named gate. A failed gate is a defect to fix, not a note
   to ship with.
3. When Mars corrects something again, append a new entry here — do
   not edit an old entry's "Mars said" text, and do not make him
   repeat the correction to get it logged.
