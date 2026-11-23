# BROTHERMAN — Sheet Jones + Rig Jones 1 + Test Videos — REPORT

**Workdir:** `~/workspace/_cape-jones-parking-lot-2d/brotheman/` (folder spelled `brotheman`;
character name is BROTHERMAN, all caps, one word).
**Date:** 2026-11-23. **Status: DONE — sheets, rig, movement test and scene test all
built, rendered, composited and verified own-eyes as whole videos.**

Nothing here was landed in the repo. Nothing in `rig/`, `v2/`, `v2-fixed/`,
`v2-mixed/`, or any Cape Jones rig/cut file was touched. No JANCTION JPY spent.
No 3D full render. No synthesized voice (owner-gated) — the line reads as an
on-screen speech card.

---

## 1. Deliverables

### Videos (the proof — watch the whole video, not just frames)

| File | What | Spec | Size | sha256 |
|---|---|---|---|---|
| `brotheman-movement-test.mp4` | Rig movement test: idle/blink, elbow-curl demo, knee squat with torso squash & stretch + overshoot, wave with finger/thumb wiggle + hair/bandana lag, settle | 1280×720, 24 fps, 4 s, silent, H.264 | 133,170 B | `4f64a335b4a1469a1c52e8dd532c3ff9355b5205964096aa29d4bd5e93b9bd1a` |
| `brotheman-test.mp4` | Scene test: BROTHERMAN on the V2 parking-lot plate next to Cape Jones (V2 rig plate, read-only stand-in for scale), idle → wave → point LEFT at Cape + talking mouths → squash hit on the point → wink → settle. Speech card: `BROTHERMAN: "You just gotta motherfucking keep up with the Joneses, brother."` (on screen 2.0–4.0 s) | 1280×720, 24 fps, 5 s, silent, H.264 | 169,855 B | `b6e096fbd00c7149ce09495e69817b91a56b45ac3983eed77b7c7081bcd9d31b` |

### Sheet Jones

| File | sha256 |
|---|---|
| `SHEET-JONES.md` | `b09c7a5f07ff37947e06245292aa2107aee522c7cdc2a1b1bd497a33ad34352d` |
| `sheets/01-turnaround.png` (+ `.webp`) | `daed6ad17b8a1de3e1d238f7c305c216843d01afee176d48fb5d4222a79ca141` |
| `sheets/02-construction.png` | `6e516b804f6d4b84bcb80d69f4367ca25357e0e4d7d6f12ee8be4ab62a1014de` |
| `sheets/03-expressions-hands-colors.png` | `41e06709facc4164f1d0700c24ccd3b1c75db5b03965bdfeb46fe589747e63` |

- **01-turnaround:** front/side/back, pink bandana on the front view, scale figure vs
  CORRECT Cape Jones (purple cowl, white eyes, white suit with purple V, white belt,
  long black cape, white gloves/boots — no jacket/lapels/black gloves).
- **02-construction:** T-pose, red construction lines, 7 heads tall, design-notes box
  with the locked likeness.
- **03-expressions-hands-colors:** Neutral / Grin / Shout / Wink; Fist / Open / Point
  hands drawn wrist-top, fingers-down, with white wristband; locked palette.
- Known generator artifacts, recorded in `SHEET-JONES.md`, NOT canon: sheet 03
  labels two different grins both "GRIN"; sheet 03 blond swatch reads `#E8C256`
  vs lock `#E8C25E`.

**Locked palette:** skin tanned `#D89B62`, blond `#E8C25E`, tank/boot blue `#2B8FD4`,
pink `#EC4D8C`, tie-dye purple `#7B4BD6`, white `#FFFFFF`, black `#000000`, belt
gold buckle `#E8B83A`.

### Rig Jones 1

| File | Size | sha256 |
|---|---|---|
| `brotheman-rig.blend` (rest rig, frame 1) | 135,471 B | `a7f4a8d3870c8b65e0e07b58bbbb0318a70d761fa29738c0b7196ea648d724d7` |
| `brotheman-rig-move.blend` (movement test, 96 f / 4 s) | 141,075 B | `bf831a17fb812091b390c276d7ce170cec5ad6f9d93fb2ecb6a6f56479d9f48b` |
| `brotheman-rig-animated.blend` (scene test, 120 f / 5 s) | 140,613 B | `2bfea968b1c8329ad0d81f8523d410b71bab5ed7d276e31baf0d29b8e16cd057` |

**26 bones** (Cape V2 has 12): pelvis, torso, neck, head, hair, bandanaTail,
upperArmR/L, forearmR/L, handR/L, fingerR1–4, fingerL1–4, thumbR/L, thighR/L,
shinR/L. **44 planes.**
Layout (rig units, Y up, ground 0): head top 16.85, shoulders 13.3, elbow 10.8,
wrist 8.3, hip 7.6, knee 4.3, ankle 1.5. Camera ortho 34 at (0, 8.4, 20).
Blender 5.0.1, Cycles CPU, 16 samples, ~4–5 s/frame.

**Parts — 34 PNGs in `parts/`** (all transparent-alpha, built by `make_parts.py`):
Head_Front (one clean face outline, strong jaw, blond horseshoe), Hair_Back
(separate follow-through plane), Bandana_Pink / Bandana_Blue + BandanaTails_Pink /
BandanaTails_Blue (swaps), Eye_Open / Eye_Happy, 6 mouths (Closed, Smile, Grin,
Open, Shout, Frown), Neck, Torso (blue tank, BROTHERMAN in pink DejaVu Bold —
a stand-in for the Hulkamania-style display font; hand-lettering it is a
Clean-Up item), Pelvis (tie-dye + black belt + gold buckle), UpperArm / Forearm
per side (elbow overlap caps on BOTH pieces), Thigh / Shin per side (tie-dye +
knee caps; shin includes blue boot with pink laces, toe extended), Hand
Fist / Open / Point per side, Finger, Thumb, Shadow. `parts-contact.png` exists.

### Build scripts (all in `brotheman/`)

`make_parts.py`, `build_rig.py`, `choreo_move.py`, `choreo_scene.py`,
`make_speechcard.py`, `composite.sh`, `speechcard.png`. Rendered frames:
`frames/` (120, scene test), `frames_move/` (96, movement test), `rest-f0001.png`,
`verify/` (frames extracted from the finished mp4s).

---

## 2. Likeness lock — what was built, and what was changed

The owner's locked likeness of **2026-11-23 07:17 EST** was used exactly, do not
change: big muscular wrestler, strong jaw, thick BLOND horseshoe mustache, tanned
skin; BLUE tank top with "BROTHERMAN" in PINK Hulkamania-style font; PINK + BLUE +
PURPLE tie-dye LONG TIGHTS, white wristbands, BLUE boots with PINK laces; bald top
with LONG BLOND hair at sides/back as DEFAULT; PINK bandana on first appearance,
BLUE bandana sometimes, NO bandana most of the time; FULL-HAIR version ONLY for
old-him / flashback "this used to be me" gag; bandana changes ONLY visibly
(on-screen change) or as a noticed look-away joke — never random scene-to-scene.
Bandana is a swap layer in the rig (pink/blue/none), so continuity is enforceable
per shot.

**Superseded design (do NOT ship):** the first brief's teal bandana / dark
handlebar mustache / white tank / black trunks / teal wristbands version was built
first, then replaced in place the same day by locked-v2 files. Nothing teal ships.
The first brief also said "use Cape Jones palette as the base" — the lock
overrides it with BROTHERMAN's own pink/blue/purple.

**Trademark / likeness changes, and why:**
- No real-person likeness claim, no WWE branding, no "Hulk" name, no red/yellow
  Hogan colors — the archetype (big blond wrestler, horseshoe, bandana, "brother")
  is rendered as an original Cape-Jones-style character in BROTHERMAN's own
  pink/blue/purple palette, bald top with long blond hair (not a Hogan hairline),
  and the name BROTHERMAN.
- The tank lettering is a DejaVu Bold stand-in for the Hulkamania-style display
  font — a hand-lettered original wordmark is a Clean-Up item (see §5), so the
  rig does not ship a trace of any trademarked font.

**Cape Jones likeness rule** applied in every shot with him: purple cowl, white
eyes, tan lower face, white skin-tight suit with purple V, white belt, long black
cape, white gloves/boots. No jacket/lapels/black gloves. In the scene test Cape
appears only as the existing V2 plate `v2/check-f0001.png` (read-only, untouched)
for scale.

**Record note:** the likeness lock landed in repo main as PR #436, merge commit
`9d0c79f` (`docs/BROTHERMAN.md`, `HANDOFF.md`, `AGENTS.md`). The 5 reference webp
images are NOT in the repo yet (binary upload needed via a git-authenticated
machine / browser UI to `production/2d-parking-lot/brotherman/`) — do not claim
they are landed. This lane read the parallel likeness lane's concept images
(`~/workspace/_cape-jones-parking-lot-2d/brotherman/`, v3/v4 pink-bandana,
bald-top, no-bandana, cape-correct) for reference only; no files were copied —
all sheets and parts were built fresh here.

---

## 3. Gumball rig method — what was found, and what was applied

**Plainly: no Gumball `.fla` was opened on this VM.**

- The claimed source `~/workspace/agent-ops/fla-puppets-program-2026-10-30/gumball/`
  **does not exist** (no `~/workspace/agent-ops/` at all). No
  `~/workspace/toon-mash-studio/` either. No literal `.fla` files in the repo
  checkout or in the `gumball-full-leak-v1` git tag tree.
- The tag exists as commit `ed34dd39` (merge PR #404) in the repo checkout; its
  tree contains only a file list
  (`cape-jones-rig/gumball-full-leak-file-list-20261031.json`) and a summary
  (`cape-jones-rig/gumball-full-leak-rar5-summary-20261031.md`): a 43.52 GB
  remote RAR, 2,259 files, **138 `.fla` listed** (25 puppet, incl. family puppets
  versions 001–008 CS3/CS5, e.g. `GB200_ORIGINAL_PUPPET_DAD_VERSION_003.fla`),
  headers walked via HTTP range reads, NO download. The `.flash.json` files in
  the tag are QC verdict files (rules R01–R12), not rig structure.
- The Playbook line 22 cites Gumball S2 `.fla` rigs as reference-HAVE at
  `workspace/toon-mash-studio/animation-study/gumball-s2-rigs/` +
  `mhvnsnt/cn-gigaleak-gumball` (study only) — neither path exists on this VM.

**Method applied, from the repo docs (not from FLAs):**
- `JONES-VERSIONS.md` §4 (Gumball: layered rigs, swappable parts, real secondary
  motion; pose library / physical-comedy timing) and the repo's own rig rules
  R01–R12 (arm-front snap, face snap, knee-feet per frame, wrist, elbow direction,
  grounded, cape-two-parts).
- As built: a layered puppet with a fixed z-stack, swappable part libraries
  (hands Fist/Open/Point, 6 mouths, 2 eye states + wink, bandana pink/blue/none),
  real elbow + knee joints with overlap caps on both pieces, articulating fingers
  + thumbs (4 finger bones + thumb bone per hand), squash & stretch (torso scale
  keys with overshoot), secondary-motion follow-through on long hair and bandana
  tails (lagged bones, keyed overshoot), and clean-up done from the start so the
  rig already reads at Draw Jones / Video Jones level — a live Video Jones of
  BROTHERMAN, not a puppet substitute.
- Sheet Jones + Rig Jones + Clean-Up Jones were done TOGETHER: sheets match the
  rig, the rig is cleaned up from the start (see §5).

---

## 4. Own-eyes verification (whole videos watched, key frames checked)

**Hand log — CORRECT way (always), verified in every checked beat:**
wrist-to-wrist, same direction, fingers at far end, hands attached to the
forearm cuff, thumbs medial, no white boxes. The Point hand points LEFT at Cape
with the index finger extended; the Open hand waves with fingers + thumb spread;
fists sit at the wrist with fingers down. No upside-down hands, no floating
hands, no detached hands, no white-background boxes anywhere in either video.

**Movement test (4 s, dark background) — checked beats:**
- f24 elbow curl: forearm bends at a real elbow, overlap caps hold, no gap; Smile
  mouth between the mustache bars.
- f48 squat: knees bend outward gently, shins return to planted feet, torso
  squashes, effort Open mouth; no joint gaps.
- f72 wave: whole Open hand in frame, fingers + thumb spread, Happy eyes
  (closed arcs), Smile mouth, hair swept by the lag bone.
- Settle: returns to rest cleanly.

**Scene test (5 s, V2 parking-lot plate) — checked beats:**
- t=1.5 wave: BROTHERMAN waves, Cape stands correct in the plate.
- t=3.0 point + speech card: point LEFT at Cape, Shout mouth, speech card reads
  the whole line cleanly; BROTHERMAN is ~2× Cape's on-screen height (correct —
  he is much bigger and closer to camera).
- t=4.5 settle: card gone (correct, 2.0–4.0 s only), wink beat landed, arms down,
  both characters correct.

**Two defects found by own-eyes checking and FIXED before delivery (not hidden):**
1. First render: the wave hand went ABOVE the frame (arm at -2.40/-2.55 rad).
   Fixed by re-posing the wave to -1.95/-2.05 rad in both choreos and re-rendering
   all 216 frames (~20 min). Hand is fully in frame in the delivered videos.
2. First render: the squat read knock-kneed (thigh ±0.20, shin ±0.45 — too much
   counter-rotation). Fixed to thigh ±0.15, shin ±0.30; it now reads as a proper
   cartoon crouch.

**Technical:** Blender 5.0.1, Cycles CPU, 16 samples. EEVEE does NOT work on this
VM (libEGL.so.1 missing; Chromium's libEGL lacks `eglGetCurrentDisplay`), so
both videos are Cycles CPU renders — same as the Cape V2 pipeline. Rotation
sign: limb bones point down (-Y); negative Z rotation swings toward -X (viewer's
left). Hand-swap lesson carried over: keyframe `hide_render` at f1 for
fingers/thumb, or pre-f25 frames hold f25's value. Bugs fixed during the build:
flipped `_L` images saved at 2× from the supersampled canvas (now `flip()` flips
the saved file); tie-dye outline helpers used transparent fill `(0,0,0,0)` which
erases in PIL (now outline-only helpers); tie-dye is a mottled blob wash
(random seed 7) + small spiral centres — reads as tie-dye, not targets.

---

## 5. Clean-Up Jones level of BROTHERMAN Rig Jones 1

Rig Jones 1 is already cleaned up from the start — that is the point. What it
already has (the bar): real elbow/knee joints with overlap caps, articulating
fingers + thumbs, 6-mouth + eye/wink library, bandana swap layer, hair/bandana
follow-through bones, squash & stretch with overshoot, fixed z-stack, 34 clean
parts with consistent line weight, no gaps, no white boxes, pre-delivery hand
check at every beat.

**Still open for BROTHERMAN (his own Clean-Up list, not Cape's):**
- Hand-letter the BROTHERMAN tank wordmark (currently DejaVu Bold stand-in).
- Hand-paint the tie-dye swirls (currently procedural mottled wash + spiral
  centres — reads fine at test-video scale, wants a painter's pass at close-up).
- 3/4 head + profile head swaps (sheets have side/back; rig is front-only).
- COA Tools 2 / deformer + peg workflow, Wiggle 2 cloth on bandana tails,
  EEVEE render path (blocked on libEGL on this VM), line boil.
- Knee-tracking tuning on the squat (knees should track over the feet; the
  current crouch is good, not yet perfect).
- FULL-HAIR old-him / flashback variant and BLUE bandana variant as rigged swaps
  (bandana swaps exist; full-hair is sheets-only for now).

---

## 6. THE CAPE JONES CATCH-UP PLAN — BROTHERMAN's rig as the example

The bar was: when BROTHERMAN's rig is put next to Cape's Rig Jones 1 / V2 rig,
BROTHERMAN's rig must look SO advanced that Cape's rig is the one that needs to
play catch-up. It does. This section is the proper plan for the next Cape Jones
Clean-Up Jones work, after BROTHERMAN's rig is proven. **Do NOT touch Cape's rig
files from this lane; this is the plan for the Cape lane.** Levels use the
Jones Model ladder: Rig Jones 2 = Clean-Up Jones 1, Rig Jones 3 = Clean-Up
Jones 2, and so on. (The existing V3→V6 ladder in `JONES-VERSIONS.md` already
names most of these items — BROTHERMAN's rig proves each one works in the same
Blender pipeline, so the items below are ordered by "where to start", not by
re-debating them.)

### C1. Real elbow joints — Rig Jones 2 (Clean-Up Jones 1) — START HERE
- **What BROTHERMAN does better:** upper arm + forearm as separate bones with
  overlap caps on BOTH pieces; the elbow bends without a gap at any angle
  (proven in the elbow-curl beat, movement test f24).
- **What Cape's rig needs:** Cape V2 has one-piece arms — shoulder rotation only.
  Re-slice each arm into upper + forearm with elbow overlap caps, add a forearm
  bone per side, re-key the raise/click beats.
- **Where to start:** the re-slice. PR #430's 44 parts already have elbow cuts —
  take their PARTS, not their broken cut. Rebuild from the locked T-pose v8 art,
  same as BROTHERMAN's `make_parts.py` → `build_rig.py` flow.
- **Proof:** re-render the dance-test arm raise; elbow must hold at every frame.

### C2. Real knee joints — Rig Jones 2 (Clean-Up Jones 1) — START WITH C1
- **What BROTHERMAN does better:** thigh + shin as separate bones with knee
  overlap caps; the squat bends without a gap (movement test f48).
- **What Cape's rig needs:** Cape V2 has one-piece legs — hip rotation only.
  Re-slice each leg into thigh + shin with knee caps, add a shin bone per side.
- **Where to start:** same re-slice pass as C1, same art source. Do arms and legs
  in one Rig Jones 2 pass — they are the same job.
- **Proof:** a squat/crouch test like BROTHERMAN's movement test; knees track over
  the feet.

### C3. Articulating fingers + thumbs — Rig Jones 2 (Clean-Up Jones 1) — AFTER THE V3 HAND FIX
- **What BROTHERMAN does better:** 4 finger bones + 1 thumb bone per hand, finger
  and thumb planes, finger wiggle keys on the wave (movement test f72).
- **What Cape's rig needs:** Cape has 7 static hand swaps and no finger bones.
  The V3 hand/remote fix only corrects orientation — it does not add fingers.
- **Where to start:** after the V3 hand fix lands, add finger/thumb bones to the
  swap hands and finger planes to the Open and Point hands first (those are the
  ones the camera sees move).
- **Proof:** a wave beat with visible finger wiggle, no floating fingers.

### C4. Fixed z-stack + joint overlap-cap build rule — Rig Jones 2 (process, starts immediately)
- **What BROTHERMAN does better:** a written layer order enforced at build time;
  every joint has an overlap cap on both pieces, so no joint ever gaps.
- **What Cape's rig needs:** Cape's parts were placed ad hoc; the mixed cut broke
  partly because layering was not enforced. Write the layer order + overlap-cap
  rule into `RIG-REPORT.md` and `build_rig.py` and enforce it at build time.
- **Where to start:** `rig/build_rig.py` — add the cap rule before the next re-slice.
- **Proof:** a joint-gap check on every beat of the next cut.

### C5. Pre-delivery hand check as a gate — every version (process, starts immediately)
- **What BROTHERMAN does better:** the hand log (correct vs incorrect, §4) is
  checked at every beat before delivery — wrist-to-wrist, fingers at far end,
  no upside-down/floating hands, no white boxes.
- **Where to start:** adopt BROTHERMAN's §4 checklist as the gate for every Cape
  cut, starting with the V3 hand-fix proof video.
- **Proof:** the V3 proof video passes the checklist at every beat.

### C6. Mouth library + eye library as real swaps — Rig Jones 3 (Clean-Up Jones 2)
- **What BROTHERMAN does better:** 6 mouth shapes (Closed, Smile, Grin, Open,
  Shout, Frown) + Eye_Open / Eye_Happy + wink, as hide_render swaps keyed to the
  dialogue (scene test talking beat).
- **What Cape's rig needs:** Cape has pupil overlays and no mouth library.
  (This is a V5 ladder item; BROTHERMAN proves it in the same pipeline.)
- **Where to start:** sheet 05 eye-dart matrix + Playbook sprite library — draw
  the 6 mouths + 3 eye states from the locked Cape face art, wire as swaps.
- **Proof:** a talking beat with mouth shapes changing on the dialogue, blink and
  wink on the beat.

### C7. Squash & stretch — Rig Jones 3 (Clean-Up Jones 2)
- **What BROTHERMAN does better:** torso scale keys with overshoot on the squat
  and on the point hit (scene test squash on the point).
- **What Cape's rig needs:** Cape has no squash & stretch. (V6 ladder item.)
- **Where to start:** the click gag beat (f169–205) — squash on the click, stretch
  on the release. One beat proves the technique; then roll it across the cut.
- **Proof:** the click beat visibly squashes and stretches without the rig breaking.

### C8. Secondary-motion follow-through — Rig Jones 3 (Clean-Up Jones 2)
- **What BROTHERMAN does better:** hair and bandana-tail bones with lagged keys
  and overshoot — the hair visibly sweeps on the wave and the point.
- **What Cape's rig needs:** Cape's cape is a 2-bone spring with no lag keys on
  anything else. (V5/V6 ladder item.)
- **Where to start:** add lag/overshoot keys to the existing capeTop/capeTip bones
  in the V2 cut's dance test; Wiggle 2 comes after the keys prove the motion.
- **Proof:** the cape visibly lags and settles after a turn in the dance test.

### C9. Swappable accessory layer — Rig Jones 3 (Clean-Up Jones 2)
- **What BROTHERMAN does better:** bandana pink/blue/none as a swap layer, so
  continuity is enforceable per shot.
- **What Cape's rig needs:** Cape's cowl is baked into the head — no swappable
  accessory layer. Split the head art so the cowl is its own plane; eye swaps
  and cowl variants become swappable.
- **Where to start:** split the head art in the next re-slice (with C1/C2).
- **Proof:** a cowl/eye swap keyed mid-cut without re-rendering the head.

### C10. Pose library — Rig Jones 3 (Clean-Up Jones 2)
- **What BROTHERMAN does better:** named keys (idle / wave / point / talk) that
  can be re-used across shots.
- **What Cape's rig needs:** Cape's keys are embedded in the cut; there is no
  reusable pose library.
- **Where to start:** extract the V2 cut's dance-test beat poses into named poses.
- **Proof:** a new beat built from library poses only, no fresh keying.

### Order of work (the plan, in one line)
Rig Jones 2 (Clean-Up Jones 1): **C1 + C2 + C3 + C4 + C5** — re-slice arms/legs
with joints and caps, add fingers, enforce the layer/cap rule, gate every cut
with the hand checklist. Then Rig Jones 3 (Clean-Up Jones 2): **C6 + C7 + C8 +
C9 + C10** — mouth/eye library, squash & stretch, follow-through, accessory
swaps, pose library. BROTHERMAN's rig files are the reference implementation for
every item — open `brotheman-rig.blend` next to Cape's rig and copy the structure,
not the look.

---

## 7. Notes

- BROTHERMAN appears in the SECOND full episode, never episode 1. The first full
  episode (Cape into the game into Immortal Kombat, mix of 2D and 3D) is not made
  yet — this lane did not put him in it.
- He calls everyone "brother", everyone calls him "brother".
- The V2 parking-lot plate `v2/check-f0001.png` was used read-only as the scene
  background; the plate's Cape Jones is the correct likeness.
- No hand/remote fix lane work and no leap lane work was touched.
- Nothing was landed in the repo from this lane.
