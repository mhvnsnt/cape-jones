# Study + workflow: arm/torso layering, arm crossing, and motion

Job: Mars 2026-11-01 16:20 CST — lock the snap-early Blender motion as
PERFECT, remember it, study anatomy and animation, and wire up aids
that help get better at it. This doc is the study. `motion_template.py`
in this folder is the wiring. The perfect clip itself was NOT touched.

Locked clip: `blender523-motion-arm-snap-early-20261101/blender523-legs-fixed-MOTION-SNAP-EARLY-20261101.mp4`
(see `LOCK-RECORD-20261101.md` for hashes). Study/template approval:
0/1 — Mars has not approved this study or template yet, and no new
perfect claim is made for them.

## 1. Why snap-sooner works — the one-sentence version

In an ortho cutout render, depth is ONLY the Z order of flat planes.
A plane that is behind the torso at the first frame of overlap will
read as eaten, no matter how good the pose is. So the layer change
must happen on the anticipation frame, before overlap, not at the
peak of the overlap. That is the whole fix: f13, not f25.

## 2. Torso occlusion, in plain terms

- Nearer occludes farther. There is no real depth in a 2D plane rig,
  so "in front" is a number: torso 0.08, arm 0.11, head 0.12.
  A 0.03 gap is enough in ortho, because ortho has no perspective
  falloff to blur the order — but it also means a 0.001 dip below
  torso Z on any single frame is a visible eat, not a soft edge.
- A crossed arm must read as ONE continuous chain:
  shoulder -> upper arm -> elbow -> forearm -> fist, with no break
  at the torso edge. A break at the torso edge is the tell: the
  upper arm went behind while the forearm stayed in front (the old
  2D last-3 failure), or the whole arm ramped up too late (the old
  Blender f25 failure). Both are layering failures, not pose failures.
- Staging check, before any render: at thumbnail size, can you still
  tell which arm is crossing and where its fist ends? If the fist
  or bicep disappears into the torso silhouette, the layering is
  wrong even if the pose numbers look right.
- Face crossing is a different stack, and must not be guessed from
  the chest stack: chest = torso < arm < head; face = torso < head
  < arm. The template keeps both numbers explicit so a builder
  cannot silently reuse the chest stack for a face cross.

## 3. Anatomy that governs an arm crossing the torso

Evidence labels are used honestly throughout this section:
- TEXTBOOK = standard human anatomy, well-established in anatomy
  teaching, not a new experiment run for this job.
- CLINICAL = peer-reviewed / clinical gait literature, cited, but
  it supports alignment, it is not a measurement of Cape Jones.
- PRACTICE = studio animation practice, formalised in books and
  taught widely, not lab-validated.
- LOCK = Mars-approved production rule for this rig, not a
  scientific claim.

### 3.1 Shoulder — ball and socket (TEXTBOOK)

The glenohumeral joint is a ball-and-socket joint: flexion/extension,
abduction/adduction, internal/external rotation, circumduction.
Practical consequence for a cross: the upper arm can swing across the
chest by horizontal adduction, and the shoulder itself does not need
to move for the arm to cross. If a cross looks like the shoulder
detached, the upper-arm pivot is wrong, not the shoulder joint.
Sources: standard upper-limb anatomy summaries, e.g.
http://calisthenicsassociation.org/lessons/upper-extremity-anatomy-complete-guide

### 3.2 Elbow — hinge, not a ball (TEXTBOOK)

The humeroulnar joint is a hinge: flexion and extension only, about
145 deg of flexion in textbook ranges. The elbow point trails
backward when the forearm flexes forward. Practical consequences:
- Elbows must point back/out, never forward/in reversed (standing
  rule R07). A reversed elbow reads instantly as broken.
- A forearm does NOT bend sideways at the elbow. Sideways movement
  of the fist comes from the shoulder, not from bending the elbow
  sideways.
- In a chest cross, the elbow is the corner of the chain. If the
  elbow cap/point vanishes behind the torso while the forearm
  stays visible, the chain is split — that is exactly what the
  whole-chain snap prevents.

### 3.3 Forearm — two bones, one rotation (TEXTBOOK)

The proximal and distal radioulnar joints are pivots: the radius
rotates around the ulna to give pronation/supination, about 180 deg
total range in textbook summaries. Practical consequences:
- A fist can turn palm-down to palm-up without the elbow moving.
  That is a forearm rotation, and in a flat rig it reads as the
  fist/gauntlet turning, not as the forearm bending.
- The wrist is the end of that chain: open hands attach by the
  WRIST end to the forearm end, hands go WITH the wrist, never cut
  (standing rule R05). A fist that stays behind while the forearm
  moves is a wrist failure, not a snap failure — check wrist
  separately from Z.

### 3.4 Torso, hips, and the rest of the chain (TEXTBOOK + LOCK)

- The hip joint sits in the pelvis (femoral head in the acetabulum),
  so when the pelvis drops in a squat the hip centre drops with it
  (internal note `HIP-LOWER-ANATOMY-20261031.md`: hip y740 -> y760,
  20 px, knees and feet locked). The same logic applies upward:
  the shoulder girdle moves with the torso, so a collar that does
  not move with the torso is a rigging failure (standing cape rule:
  collar/top moves with shoulders/torso, bottom pinned when seated).
- Legs in this rig are whole pieces rotating around hip sockets
  (legs-fixed lock: hips Leg1 (470,740), Leg2 (615,740), pivot
  offset (0,0), scale 0.93). Whole-leg rotation makes shins slant
  outward where a cut-leg apose has near-vertical shins — a known,
  disclosed limit, not a reason to silently cut limbs in Blender.
  Cut limbs are a separate decision.

### 3.5 Knee-feet — the rule the template actually checks (CLINICAL + LOCK)

Universal rule, Mars 2026-11-01 12:07 CST, reaffirmed in the locked
rules: knees direction == toes direction, per frame, both legs.
Knees inward -> toes inward; knees outward -> toes outward.
Exception ONLY when Mars names a specific pose as an exception.

Clinical grounding, honestly labelled: the second-toe test and
foot-progression angle are real clinical gait measures — a plumb
line from the tibial tuberosity is compared with the second
metatarsal / second toe to judge tibial torsion, and toe-out angle
during gait is related to knee loading in published work (Chang et
al., Ann Rheum Dis 2007, toe-out angle and medial tibiofemoral
osteoarthritis progression: https://pmc.ncbi.nlm.nih.gov/articles/PMC1994298/).
That literature supports "knee and foot should track together" as
an alignment principle. It does NOT prove a cartoon rig's exact
pixel threshold, and this doc does not claim it does. The rig's
threshold (per-frame table, no block-range excuse) is a LOCK.

Grounded rule (LOCK): feet planted unless the shot is labelled
airborne; a planted foot more than 5 px off the ground line fails
in the template's pose-table gate.

## 4. Animation principles, applied to this exact 48-frame clip

Source: the 12 principles formalised by Disney animators Frank
Thomas and Ollie Johnston in *The Illusion of Life* (1981), from
decades of studio practice. That is PRACTICE, not lab science, and
the internal checklist `12-PRINCIPLES-CHECKLIST-20261031.md` already
wires all 12 for Cape Jones. The ones that decide whether a cross
reads cleanly are:

| Principle | What it means here, concretely |
|---|---|
| Anticipation | f13 arms-out IS the anticipation for the cross, and it is also the snap frame. A layer change hidden inside the anticipation reads as intentional; a layer change halfway through the move reads as a pop. Snap on anticipation, never on impact. |
| Arcs | Fists travel on curves, not straight lines. A fist that moves in a straight line across the chest looks mechanical; check the fist path in the exposure sheet / frame sequence, not just the two end poses. |
| Slow in & slow out | More frames (denser spacing) at the start and end of a move, fewer in the middle. The locked clip holds the crossed pose and eases into flex; a linear ramp into the cross would make the snap itself look like the move. |
| Follow-through & overlapping action | Secondary pieces lag the body by 1-2 frames and settle after it. Cape is the test here: if the cape stops on exactly the same frame as the arms, the move looks dead. Cape lag is a separate check from arm Z. |
| Staging | One idea per shot/segment. In f25 the idea is "arms crossed on top of the chest" — if the torso eats a bicep, the idea is gone, however good the flex that follows is. |
| Timing | Frame counts are the performance. Locked timeline: f1 rest, f13 arms-out, f25 crossed peak, f37 flex 120 deg wide, f48 shuffle. Changing the snap frame without changing the timeline is a layering fix; changing the timeline is a new performance and needs a new approval. |
| Solid drawing | Volume and joint placement stay consistent across poses. Joint pivots at ball centres (v7c), whole limbs, no detached fists, no floating gauntlets. A Z fix must never be used to hide a volume break. |
| Exaggeration | Push past realism for clarity, but not past the rig: flex is 120 deg wide (obtuse, LOCK R06, 100-160 deg gate), not an acute pinch and not an over-wide split. |
| Squash & stretch, pose-to-pose, secondary action, appeal | Still apply to the full clip (see internal checklist), but they do not decide the snap. Do not let a 12-principle checklist become an excuse to skip the one gate that failed before: per-frame Z. |

## 5. Blender FK / Z-layering aids, wired

Cutout practice (PRACTICE, from Blender cutout workflows): layered
image planes, each parented to a bone, with depth set by Z offset
from the camera; Grease Pencil layer order is a separate system and
cannot be keyframed the way plane Z can, which is why this rig
keys plane location-Z, not Grease Pencil stroke order.
Reference workflows: https://copyprogramming.com/howto/how-to-install-cutout-animation-tools
(planes as images, bone parenting, Z-depth layering) and the
Blender Artists Grease Pencil layering discussion noting that
2D stroke order cannot be animated inside one Grease Pencil object
the way plane Z can: https://blenderartists.org/t/grease-pencil-2d-3d-layering/1543546

Aids wired in `motion_template.py`, all tested in this job:

1. **Snap-sooner defaults** — SNAP_ON=13, CROSS_START=14,
   CROSS_END=36, SNAP_OFF=37, SNAP_Z=0.11, TORSO_Z=0.08, HEAD_Z=0.12.
   A future builder changes these only by naming a new crossing
   window, and the gate still requires snap ON before that window.
2. **Dense hold keys** — one Z key per frame through the crossing
   window, not sparse keys at peak only. In Blender 5.2 the layered
   action API does not expose the old fcurve interpolation the
   same way (the test run logged FLATTEN_NOTE for both arms); the
   dense keys are the guarantee, and the script says so instead of
   pretending a flatten call worked.
3. **Per-frame snap gate** — evaluates both arm Z values at every
   crossing frame after keying, requires torso < arm < head, exits
   2 on any bad frame. Tested: PASS on a copy of the overlay-locked
   blend; FAIL (exit 2) when SNAP_Z was forced to 0.05, below torso.
4. **Timeline markers** — SNAP_ON, CROSS_START, CROSS_END, SNAP_OFF
   are written into the blend's timeline, so the snap is visible
   without opening a script.
5. **Guide hiding** — GP_/LBL_ overlay objects are hidden for clean
   renders by default (HIDE_GUIDES=1), so a guide can never leak
   into a final the way debug orbs did in 2D.
6. **Pose-table gates, honest about absence** — knee-feet and
   grounded are checked ONLY if a POSE_JSON per-frame table is
   supplied. Without one they report NOT_CHECKED, never PASS.
   Tested: a pose table with leg1 knee left / toe right at f25
   failed the gate with exit 2.
7. **Whole-chain report** — the gate JSON lists exactly which arm
   objects were keyed, so a future split-chain build cannot pass
   by keying one piece and claiming the chain.
8. **No in-place editing** — the script refuses to run without
   BLEND_OUT, and it saves to that path only. It must never be
   pointed at the locked perfect blend.

## 6. Start-from-here workflow for the next Blender motion build

1. Copy `motion_template.py` into the new dated folder. Never edit
   the template in the study folder in place for a single clip;
   copy it, so the study folder stays the reference.
2. Copy the source blend to a NEW dated folder. Never open the
   locked snap-early blend as the working file.
3. Write the crossing window down first: snap-on frame, crossing
   start, crossing end, snap-off frame, and the pose at snap-off
   that proves the arms are clear. If snap-off pose still overlaps
   the torso, the window is wrong — move snap-off, do not lower Z.
4. If the move has legs, write the per-frame pose table FIRST
   (knee_dir, toe_dir, foot_y, airborne per leg per frame), and
   pass it as POSE_JSON. No table = no knee-feet or grounded claim.
5. Run the template headless. Render ONLY if the gate JSON says
   overall PASS. A NOT_CHECKED knee-feet gate means the build is
   not ready to claim those rules, not that they passed.
6. Eye-check, in order: first crossing frame (arms already on top),
   crossed peak (continuous chain, biceps on top), snap-off frame
   (arms clear, wide flex, no pop), and one frame either side of
   each. Then check feet, cape lag, and head layer.
7. Save the gate JSON with the build, under a new dated name.
   A build without its gate JSON is unverified, not done.
8. Show it to Mars. Perfect is his word after seeing it, never the
   gate's word. The gate can only say "no layering failure found
   by these checks" — it cannot say "perfect".

## 7. What NOT to do — the failures this lock exists to prevent

- Do NOT key snap only at the crossed peak (the f25 failure).
- Do NOT re-layer a flat MP4 and claim the rig was fixed; a flat
  video cannot be re-layered, only re-rendered from the rig.
- Do NOT erase, crop, or inpaint a piece out of a finished image;
  remove the layer in the source builder and re-render (the
  CJ-01 to CJ-10 layer-removal correction, 2026-11-01 15:59 CST).
- Do NOT use a block range or a single-frame sample as a knee-feet
  check; per-frame tables only.
- Do NOT claim a gate that did not run. NOT_CHECKED is a real
  status, and it stays in the JSON.
- Do NOT overwrite a Mars-seen version. New dated file, every time.

## 8. Sources used, in order

Internal first (repo/workspace, already in hand):
- `blender523-motion-arm-snap-early-20261101/` — locked clip, blend,
  builder `fix_snap_early.py`, `snap-early-verify.json`
- `blender523-overlay-locked-20261101/` — overlay rig, placement table
- `blender523-legs-fixed-20261101/` — legs-fixed perfect placements
- `learning-remembering-gate-20261101/rules.json` — R01-R12, including
  R01 arm-front-snap, R02 face-snap, R04/R04b knee-feet universal,
  R05 wrist, R06 flex obtuse, R07 elbow direction, R09 grounded,
  R10 cape two parts, R11 no-crop, R12 flicker proxy
- `12-PRINCIPLES-CHECKLIST-20261031.md` — 12 principles, Cape Jones gates
- `HIP-LOWER-ANATOMY-20261031.md` — hip centre moves with pelvis
- `anatomy-fix-bundle-20261101/` — flex wide, arm-snap sensor, elbow fix

External, then applied to the rig (not copied as art or dialogue):
- Upper-limb anatomy (shoulder ball-and-socket, elbow hinge ~145 deg,
  radioulnar pivot pronation/supination): http://calisthenicsassociation.org/lessons/upper-extremity-anatomy-complete-guide
- The 12 principles, Thomas & Johnston, *The Illusion of Life* (1981):
  https://omebly.com/blog/12-principles-of-animation/
- Toe-out / knee loading and second-toe alignment (CLINICAL, see 3.5):
  https://pmc.ncbi.nlm.nih.gov/articles/PMC1994298/
- Blender cutout planes, bone parenting, Z-depth layering (PRACTICE):
  https://copyprogramming.com/howto/how-to-install-cutout-animation-tools
- Grease Pencil 2D vs 3D layering limits (PRACTICE):
  https://blenderartists.org/t/grease-pencil-2d-3d-layering/1543546

## 9. Still owed, plainly (not claimed here)

- A landing batch for this study folder, if Mars wants it in repo
  (PR-only, verified on main; this job is local only, no PR).
- A true sole-view boot for an unambiguous foot-toward-camera kick
  (Batch A gap, separate from this lock).
- Cut upper/lower limbs in Blender, if Mars ever wants shins
  near-vertical in Blender instead of whole-leg rotation — a
  separate decision, deliberately not done in legs-fixed.
- A per-frame pose-table generator for Blender rigs, so knee-feet
  and grounded gates can run on Blender motion without a hand-written
  table. Until then, those gates stay NOT_CHECKED on Blender builds
  without a table, by design.
