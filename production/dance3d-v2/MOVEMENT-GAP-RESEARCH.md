# Cape Jones — Movement Gap Research

**Status:** research + movement spec for the animation lanes. Companion to
`docs/production/CAPE-JONES-PRODUCTION-MODEL.md` (the production model doc;
at time of writing that file is in PR #265, not yet on main — when it merges,
add a back-link to this doc from it).

**Anchored to the owner's verbatim wording (2026-10-29).** Where any earlier
brief or paraphrase differs from these words, his words govern:

> "more motion, more animations and frames, in a simple dance, that's
> repetitive, but actually looks like a animation, even if it's funny or
> comical or not a good dance"

> "not enough like justice league animated series or space ghost level
> animations"

And his standing correction of the same day: "limited" does not mean stiff.
Economy comes from reuse and holds, not from stiffness. South Park
piece-sliding is below the Space Ghost bar itself.

---

## 1. What actually moves in the references

### Space Ghost Coast to Coast (the economy end)

- The show is a remix. Per its production record (Wikipedia, "Space Ghost
  Coast to Coast," Production), budget limits meant editor Michael Cahill
  recycled clips from the 1966 series and reorganized them on an Avid;
  "because the series remixed limited animation, editing took the most time
  in production."
- The total library was tiny: a contemporary trade write-up of the Crawford
  Communications post house (snard.com, "Space Ghost Tackles Talk") records
  "only a few different shots of Space Ghost used in all of the programs,"
  "less than 90 minutes of footage available," characters rotoscoped out of
  the old cartoons and composited onto a new miniature set.
- The movement range per shot is genuinely small — blink, a head turn, a
  hand raised to the power band (Achievers, "Why Space Ghost Coast to Coast
  Is Still the Weirdest Thing on TV"). What makes it read as animation
  instead of a slideshow:
  - **The poses are whole drawings.** The library is Alex Toth's 1966
    production art: full-body poses with strong silhouettes, drawn as one
    piece of cloth and body — never articulated segments.
  - **New poses were drawn for new business.** Animator C. Martin Croker
    hand-drew talk-show poses the action library didn't have (Space Ghost
    tapping his cue cards on the desk), on cel, deliberately without
    computer help "so that the old footage and new footage wouldn't look
    blatantly different" (Mental Floss, "15 Things You Might Not Know About
    Space Ghost Coast to Coast"; same account in the trade piece). New
    animation was then saved and reused in later programs.
  - **Holds are a performed joke, not an absence.** The camera lingers on a
    frozen face for seconds after a line (Achievers). The hold works because
    the pose being held is strong and the timing around it is edited —
    1,000+ edits per episode, three-plus days of editing (trade piece).
  - **Lip flap is a system** of "freezes, reverses, and pauses" looped to
    fake phonetics (trade piece) — even the cheapest element is sequenced,
    not static.

### Hanna-Barbera planned animation (the craft under Space Ghost)

- "Planned animation" ran at 12 or 8 distinct drawings per second — twos and
  threes at 24 fps (Illustration History, "Hanna-Barbera: The Architects of
  Saturday Morning"). Dialogue scenes often held poses on threes or fours
  while mouths moved on twos: **mixed timing per element** (Animation Timing
  encyclopedia entry).
- Bodies were split into layers (a head cel reused across bodies), and the
  split was hidden by design: collars and neckties exist "so the head could
  be easily separated onto its own cel without a seam line" (Iwao Takamoto,
  quoted in Illustration History). **The seam is designed out, never left
  visible.**
- Compensation for few drawings was "drawing clarity and timing": strong
  silhouettes and exaggerated key poses (Gallery Animation, on H-B
  production art).

### Justice League / Justice League Unlimited (the full end)

- Storyboards carry the movement. James Tucker came up as a storyboard
  artist and produced/boarded on Justice League; the DVD featurette
  "Storyboards for Justice" exists because the boards are where action was
  staged (Animated Views, JL Season One extras listing). Dan Riba directed
  across the whole DCAU run including Justice League 2001–2004 (director's
  own résumé, danriba.com).
- The producers' own post-mortem is about pose/business quality, not frame
  counts: writer-producer Rich Fogel attributed season one's weaker Superman
  to "a certain inattentiveness to the storyboarding... bits of business
  that had been successful in the past tended to get repeated a lot," fixed
  in season two by paying attention in the boards (Voices from Krypton,
  "Making the Animated Series," part 3). Bruce Timm's stated staging problem
  was keeping seven characters in motion at once and posing each power
  readably (ComicBookMovie, "Justice League Animated: Behind the Scenes").
- Designs are built to read in motion: Timm's characters are bold-lined,
  strong-shadowed, instantly recognizable silhouettes, and contemporary
  reviews consistently single out that "the way the characters moved,
  fought, and interacted felt authentic" (The Diplomariot, JL retrospective;
  Bruce Timm's design role is covered in "The Look of the League" featurette,
  Animated Views).

### Where Cape Jones sits on this range (owner-set bar)

Economical like Space Ghost — small pose library, reuse, holds, editing does
the heavy lifting — but every pose at Justice League drawing standard:
whole-body, strong silhouette, weight in it. Few drawings is allowed.
Stiff, weak, or broken drawings are not.

---

## 2. What our two v1 dance builds do instead (measured)

Method note: all numbers below were measured on the shipped files
(`cj-dance-proof-2d-v1.mp4`, 1920×1080, 24 fps, 504 frames;
`cj-dance-proof-3d-v1.mp4`, 960×540, 24 fps, 480 frames) on 2026-10-29.
Frame-step analysis at full frame rate; travel measured on grayscale frames
resized to 480×270, character box taken from the motion mask against a
per-pixel median background, "foot band" = bottom 18% of the character box,
"torso band" = 28–55% of the character box. A correction to an earlier draft
of this analysis is recorded in §5 — read it before quoting any number from
an earlier version.

### 2D build (PR #266)

- **The whole dance is 4 drawings.** Per-frame step differences cycle
  change / 0 / 0 across the day section: 4 drawings held 3 frames each
  (on threes), a 12-frame / 0.5 s loop, tiled for 21 s. There are no
  in-between drawings at all — each drawing cuts to the next.
- **The legs do not dance.** Foot-band centroid travel across the loop:
  **4.0% of body width**. Torso-band travel: **16.7%**. The feet move about a
  quarter as much as the torso (ratio ≈ 0.24). On zoomed frames the legs are
  two planted, symmetrical columns: no knee bend, no weight transfer, feet
  never leave or cross the floor line. All visible motion is in the torso
  and arms.
- **Arms rotate as pieces.** The swing is a shoulder-pivot rotation of a
  separated arm piece; the shoulder, chest and head do not join in, so the
  gesture has no line of action through the body.
- **Cape integrity failures (zoom-verified, frame ~2 s, day section).** A
  sky-colored through-hole at one shoulder where the arm piece meets the
  torso, with a slit continuing down the cape; a detached black shard
  floating off the other shoulder; thin dangling slivers along the cape hem;
  and the two cape halves do not meet between the legs — background shows
  through the middle. This is the extraction/alpha-hole class. (Root cause,
  owner-identified 2026-10-29: v1 was extracted from
  `characters/sheets/01-tpose-turnaround.jpg`, the 3D rig's T-pose
  turnaround, whose cape splits became the 2D cape's holes. His standing
  ruling: build 2D from the drawn 2D art — `characters/design-sheet.png` and
  sheets 04/07/08. The 01 turnaround is banned as an animation/likeness
  source.)

### 3D build (PR #267)

- **8 poses, zero in-betweens.** Per-frame step differences are 0.00 inside
  each pose and spike every 6 frames: 8 held poses stepped across a 48-frame
  loop, no interpolation between them.
- **The whole body barely travels.** Torso-band travel **7.7% of body
  width**, foot-band **8.1%** — the feet keep up with the torso (ratio
  ≈ 1.05), but the absolute amount of motion is roughly half the 2D build's
  torso travel. It reads as a gentle sway, which matches the build lane's
  own report ("the foot taps read subtle... a gentle side-to-side groove").
- The cape is a static mesh shape in the loop: it does not swing, settle, or
  react to the pose changes.

### The pattern

Both builds spent their economy in the wrong place. The references cut
**drawing count** and protect **drawing quality and weight**. Our builds cut
both: few drawings AND weak, stiff, or broken ones.

---

## 3. Gap list

Each gap: what the reference does → what we do → the tool/method already in
our repos that closes it. Per the owner's free-game rule, use the full craft
and tooling already staged before inventing anything.

**G1 — Drawing count per loop is below the floor.**
Reference: even SGC2C's desk library is dozens of whole poses per character,
reused; H-B cycles were drawn cycles, not 4 stills. Ours: 4 drawings (2D),
8 stepped poses (3D).
Closes with: the drawn pose library built from the owner's drawn 2D art
(`characters/design-sheet.png`, sheets 04/07/08 — never the banned 01
turnaround); Wan/VACE likeness-held animation off those sheets (the
mochiichao-accel kernel, Mochiichao repo PRs #102/#108; owner's speed-test
verdict stands: quality/slow settings, not the fast setup) to generate real
intermediate frames instead of cuts; for 3D, pose the cape-jones rig
(`3d-assets/cape-jones-rig/`) on twos with real in-betweens, or retarget
CMU mocap (`3d-assets/animation/mocap-cmu/`) for weight and knees, then
limit the timing in the render, not in the posing.

**G2 — Lower-body stiffness (named class).**
Reference: weight transfer is what sells limited animation — H-B walk/run
cycles and Toth's action poses all plant, bend, and shift. Ours: 2D feet
travel 4.0% of body width against the torso's 16.7%; legs symmetrical, knees
locked, no weight shift.
Closes with: dance/action poses drawn or posed feet-first (contact, passing,
rebound) from the drawn sheets; mocap retarget (CMU pack) for the 3D rig's
legs; Wan/VACE generation from a start/end pose pair that actually steps,
instead of an in-place arm loop.

**G3 — Gestures don't involve the body.**
Reference: Timm-boarded action is staged whole-body; Tucker's boards and
Fogel's season-two fix were about business reading through the full figure.
Ours: arms pivot at the shoulder as separate pieces; chest, shoulders and
head stay locked and symmetrical.
Closes with: pose construction rule in §4 (line of action, counter-pose);
in 3D, key the chest/shoulder/head bones with the arms on the existing
85-bone rig instead of arm-only keys; in 2D/VACE, choose start/end poses
whose silhouettes differ in the whole body, not just the arms.

**G4 — Cape/cloth integrity (named class): cloth reads as one solid piece
in every frame, or the frame fails.**
Reference: H-B designed seams out (collars hiding cel splits); Toth's cape
is one shape in every drawing. Ours (2D): through-hole + slit at one
shoulder, detached shard at the other, hem slivers, halves not meeting
between the legs — the extraction/alpha-hole class, the same family as the
splits previously found in the 3D rig's cape. Ours (3D): cape never moves.
Closes with: source from the drawn 2D art per the owner's ruling (kills the
hole class at the root); any extracted piece gets an alpha audit — zoom
crops at both shoulders, the hem, and between the legs, on every pose,
before animation; 3D cape gets cloth behaviour (Blender cloth on the rig's
cape, or hand-keyed swing/settle curves) instead of a frozen mesh.

**G5 — Holds without performance.**
Reference: SGC2C holds land because the held pose is strong and the edit
times it; H-B held bodies while mouths/eyes worked on twos. Ours: holds are
just the loop's low drawing count; nothing is timed, nothing plays during a
hold (no blink, no head settle, no cape settle).
Closes with: treat holds as beats in the edit (the SGC2C lesson — editing
took the most production time there); add the cheap secondary layer to every
hold: blink cycle, head micro-settle, cape settle — all reusable stock once
built.

**G6 — No secondary motion anywhere.**
Reference: capes, cloth and props keep moving after the body stops in both
reference shows; it's most of what makes limited work feel alive. Ours:
cape static in both builds; nothing overshoots or settles.
Closes with: follow-through keys on the rig (3D) and a drawn/VACE cape pass
(2D) offset 2–4 frames behind the body; one reusable settle cycle per
character, banked like SGC2C banked new animation.

**G7 — Weak, symmetrical poses.**
Reference: strong silhouette + exaggerated key pose is the documented H-B
compensation for few drawings; Timm designs for silhouette first. Ours:
front-on, mirror-symmetric, arms at matching angles — a T-pose's family
tree, which is literally where the 2D art came from.
Closes with: the pose rules in §4 applied at pose-selection time (in the
sheets, the rig keys, and the VACE start/end frames); asymmetric by default.

---

## 4. Movement spec — Cape Jones

Anchored to the owner's verbatim ask quoted at the top. "Simple" and
"repetitive" are in his words and stay. "Stiff" is not in his words and goes.

**Minimum readable movement (a dance loop, and by extension any action):**
1. The loop is built from **at least 8 distinct whole-body poses** (a real
   cycle: contact / passing / rebound on both sides), shot on twos or
   threes. Four drawings is a draft, not a loop.
2. **Feet participate.** Across one loop the foot band must travel at least
   half as far as the torso band (measured per §5's method; the v1 2D build
   measures ≈ 0.24 and fails; the v1 3D build passes this ratio at ≈ 1.05).
3. **The body actually goes somewhere.** Torso-band travel of at least ~10%
   of body width across a dance loop (v1 3D measures 7.7% and fails; v1 2D
   measures 16.7% and passes). A sway under that floor is not a dance.
4. **Weight is visible:** at least one clear weight transfer per loop —
   a knee bend, a hip shift, a foot lift or step. If a viewer can't say
   which foot he's standing on in a given pose, the pose fails.
5. **Every gesture is whole-body:** arms move with shoulder, chest and head
   counter-movement. Arm-only rotation of a separated piece is not a
   gesture.

**Pose strength rules:**
6. Silhouette first: a pose must read in solid black. If it doesn't read
   filled-in, it doesn't ship.
7. Asymmetric by default: matching mirror angles on both arms/legs are
   banned outside a deliberate, brief comedy beat.
8. Line of action: every pose has one curve through head, spine and hips;
   poses are checked against it before in-betweens are made.
9. Exaggerate the key, not the noise: the extreme poses go further than
   feels safe; the in-betweens stay quiet.

**What may stay held or reused (the economy that is allowed):**
10. Poses, cycles, blinks, cape settles and whole shots may be banked and
    reused across episodes — that is the SGC2C model. New business gets new
    poses drawn for it (the Croker rule), and the new poses join the bank.
11. Holds may run long when the edit times them as a beat. A hold is a
    timing choice, never a missing-drawing accident.
12. Mixed timing per element is allowed and encouraged: bodies on twos or
    threes, mouths and small secondary motion on twos.

**What may never be stiff (hard fails at review):**
13. Legs planted symmetrical with locked knees while the torso "dances."
14. A head that never turns, tilts, or settles.
15. A cape that is frozen, or — worse — not one solid piece: any through-
    hole, slit, detached shard, hem sliver, or gap between the cape halves
    in any frame fails the frame. Zoom-check both shoulders, the hem, and
    between the legs on every pose before animation (see G4).
16. Piece-sliding: a body part translating or rotating as a rigid cut-out
    across a pose change, South Park style. Pose changes are drawn (or
    VACE-generated with likeness held), not slid.
17. A loop so short it reads as a GIF sticker rather than a performance:
    if the cycle is under ~1 second, it needs a variation beat (flip,
    settle, or second cycle) inside the scene.

**Acceptance checks (run on every delivery):**
- Full-frame-rate step analysis: count distinct drawings and hold lengths;
  confirm the timing matches the spec above.
- Travel measurement per §5 (foot band vs torso band) on one full loop.
- Zoom crops: both shoulders, cape hem, between the legs — cape integrity.
- Silhouette pass: fill three poses solid black; all three must read.

---

## 5. Measurement appendix — method and a correction

**Method (use exactly this, so numbers stay comparable):** take one full
loop inside one lighting section; grayscale; resize to 480×270; character
box from the motion mask (pixels differing from the per-pixel median frame
by >20). Foot band = bottom 18% of the box; torso band = 28–55% of the box.
Travel = range (max − min) of the band's mask-centroid x across the loop,
expressed as % of character-box width. Pixel-energy ratios (mean absolute
per-frame change per region) were also computed and are **not** used by the
spec: they miscount the 2D build, whose loose cape layer generates
lower-region change-energy (full-frame ratio 1.55; character-box ratio 1.27)
while its legs stay planted. Energy is not weight; travel is closer to it,
and the zoom checks decide ties.

**Correction to the earlier draft of this analysis (2026-10-29):** an
earlier version paired a pass/fail rule — "fails when the quiet half of the
body measures under 0.5× the loudest region" — with two numbers, 0.35 and
0.13, presented as the two builds' ratios. That pairing was wrong twice
over. (a) 0.35 is the **3D build's** full-frame pixel-energy ratio only
(lower 0.178 vs upper 0.513); it was mislabeled as the 2D build's — the 2D
build's ratios under the same method are 1.55 (full frame) and 1.27
(character box), i.e. it passes the stated rule while failing the owner's
eyes, which is what exposed the instrument. (b) 0.13 was never a body-half
ratio under any method run; it matches the 3D loop's baseline per-frame step
value. Both numbers are withdrawn as evidence. The spec's quantitative
checks (§4, items 2–3) are the travel measurements above: 2D foot travel
4.0% vs torso 16.7% (ratio ≈ 0.24, fails item 2); 3D foot travel 8.1% vs
torso 7.7% (ratio ≈ 1.05, passes item 2; torso 7.7% fails item 3). Rule and
numbers now agree, and each failing verdict matches what the eye sees.

**Sources:** Wikipedia, "Space Ghost Coast to Coast" (Production);
snard.com, "Space Ghost Tackles Talk" (Crawford Communications trade
write-up); Mental Floss, "15 Things You Might Not Know About Space Ghost
Coast to Coast"; Achievers, "Why Space Ghost Coast to Coast Is Still the
Weirdest Thing on TV"; Illustration History, "Hanna-Barbera: The Architects
of Saturday Morning"; Animation Timing (encyclopedia entry), on ones/twos/
threes; Gallery Animation, on H-B production art; Animated Views, "Justice
League: Season One" (extras: "The Look of the League," "Storyboards for
Justice"); Voices from Krypton, "Justice League Exclusive: Making the
Animated Series" part 3 (Rich Fogel, James Tucker, Bruce Timm);
ComicBookMovie, "Justice League Animated: Behind the Scenes" part 1 (Bruce
Timm); danriba.com, Dan Riba résumé; The Diplomariot, "Justice League
Animated Series: A Timeless Superhero Classic."
