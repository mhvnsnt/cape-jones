# ONE RIG FOR ALL ANGLES vs SEPARATE RIGS PER ANGLE — RESEARCH
## Cape Jones, Mars question 2026-11-01 00:56 CDT

Mars's question, verbatim:
> "We probably need to create a rig that does from the side and a rig from the three quarters and then the front rig can also be a back face and rig since it's from the you know certain perspective or can they all be one rig to some research and let me know"

Note on the truncated tail: Mars's follow-up line ends "before I need to create a side read probably on" — read here as "a side rig is probably needed first", flagged as interpretation, not a confirmed quote. No build was done in this job, no push, RIG-00 untouched. Approval 0/1 research separately.

## SHORT ANSWER — chat-ready

Yes, you need a separate view rig for side, and a separate view rig for three-quarter — AND they can all live in one master rig. Those are not opposites. That is the industry answer.

In plain words:
- **One skeleton / one system, many drawing sets.** The joints, the pose logic, the timing, the layer rules stay the same. What changes per angle is the *artwork* hung on those joints: a front head is not a side head, a front foot is not a side foot.
- **Front rig can NOT just be flipped / reused as a back rig.** Not honestly. The cape helps a lot, but the face, the chest emblem, the belt front, the hands and the feet all give it away. A back rig needs its own back-of-head, back-of-torso, and cape-front artwork. Mirroring the front gives you a front-facing character standing backwards — eyes on the back of his head.
- **Side is the next rig to build.** It does not exist yet, and walking / stepping / the shimmy-to-walk work needs it. Three-quarter sitting is already in progress from Mars's uploaded sheet (2026-11-01 00:54 CDT).
- **So: build per-angle view rigs, wire them into ONE master rig file/registry.** That is what Mars was already doing with RIG-00 / RIG-01 / RIG-02 — this research just names it and says it is the standard way.

## 1. THE STANDARD: A 5-VIEW TURNAROUND

A character turnaround / model sheet is the blueprint that keeps a character on-model from any angle. Standard views, in order around the body:

1. Front
2. 3/4 front (about 45°, often the most-used view in TV)
3. Side / profile (90°)
4. 3/4 back
5. Back

All five are drawn in the same neutral pose (T-pose / A-pose), at the same scale, with horizontal construction lines lining up head top, chin, eyes, shoulders, waist and feet across every view. If a detail moves height or vanishes between views, the turnaround has drifted and the rig built from it will drift too.

Cape Jones already has, in various states: front (RIG-00, locked), 3/4 front kits (fla-3quarter-front, lounge-3quarter-packs), 3/4 sitting (Mars upload, in build), back kits (fla-3quarter-back is 3/4 back, not a straight back), and 3D sitting three-quarter renders. A straight side rig and a straight back rig are the gaps.

## 2. WHAT "ONE RIG" MEANS IN INDUSTRY — THREE DIFFERENT THINGS

People say "one rig" and mean three different things. Only the first two are real in 2D:

### (a) One skeleton / bone hierarchy, view-specific attachments — YES, standard
Spine's documented pattern: one skeleton, different skins / attachments per view, switched in animation. The same bone names (shoulder, elbow, wrist, hip, knee, ankle) drive a front arm drawing in one skin and a side arm drawing in another skin. The alternative Spine documents — two completely separate skeletons, front and back, under one root, with visibility switched — is also used, but it is harder to turn mid-animation: if the character rotates during a shot, skin/attachment switching on one skeleton is smoother than swapping whole skeletons.

For Cape Jones's PIL/v7c system this maps directly: same pivot = ball-centre logic, same shoulder/hip anchors, same knee-feet and wrist rules, different piece PNGs per view. The builder already does this for poses (config dict changes angles, pieces stay). A view switch is a bigger config change: piece set + layer order + pivots per view.

### (b) One master file with view groups, switched as a group — YES, standard in Harmony
Toon Boom Harmony's multi-pose / Transformation-Switch structure: each pose (transformation chain) you rig inside the same element must be in a *separate subgroup*, all gathered by a Transformation-Switch node, named for the pose — e.g. front, side, quarter. A Master Controller then drives the visible group. Drawing substitution works the same way at part level: a hand layer holds dozens of hand drawings and exposes one at a time; a mouth layer holds mouth shapes per head angle (front mouths, 3/4 mouths, profile mouths are separate sets).

Key Harmony rule that applies to Cape Jones too: **pivots must match within an angle.** If you substitute a drawing while a part is rotating and the pivots differ, the part pops out of place. So each view needs its own pivot set, measured from that view's art — you cannot copy front pivots onto side art and expect it to track.

### (c) One single drawing set, rotated / squashed / warped to every angle — NO, not in 2D
This is the 3D assumption, and it fails in 2D. A 2D drawing has no hidden back side. Rotating a front torso 90° does not reveal a side torso; it squashes a front torso into a narrow strip. Warping / puppet-warp / deformation can cheat small turns (a head turning a few degrees, a torso twisting a little), and that is exactly what Cape Jones's existing "three-quarter pseudo turn" already is: an out-and-back cheat, turns 3/4 then back, NOT a full turn / side view. It works for a gag turn. It does not produce a true side or back view.

The 2.5D research exception proves the rule: systems that turn a single 2D drawing into a viewable-from-any-angle model do it by building a view-dependent 2.5D mesh and retargeting 3D motion onto it, with twisted-perspective correction — i.e. they add a model, they do not just rotate the drawing. Cape Jones already has a true 3D model in the repo (cape_jones_rigged.blend), which *can* render any angle — but the 2D show and the 3D show are separate projects by Mars's locked rule, so the 3D model is reference for the 2D turnaround, not a replacement for 2D view rigs.

## 3. CAN THE FRONT RIG ALSO BE THE BACK RIG? — MOSTLY NO

Mars's instinct — "since it's from a certain perspective" — is right about one thing: a back view is *closer* to a front view than a side view is, because the silhouette width, height and limb lengths are almost the same. That is why some cheap productions cheat a back view. But for Cape Jones specifically, the cheat fails on the details that identify him. Table, part by part:

| Part | Front art reused as back? | Why / why not |
|---|---|---|
| Silhouette / height / limb lengths | YES, roughly | Same construction lines, same scale. This is the only part that transfers cleanly. |
| Head / cowl | NO | Front cowl has face, white eyes, mouth, jaw. Back of cowl is plain purple, no face. Reusing front puts eyes on the back of his head. |
| Eyes / mouth / visemes | NO | All front-only. Back needs none of them. Lip-sync sets are per head angle in Harmony for this exact reason. |
| Torso / chest emblem | NO | Front torso has the purple chest emblem / diamond. Back torso has no emblem, and the cape covers most of it anyway. |
| Belt | PARTIAL, redrawn | Front belt has the belt buckle / overlay facing camera. Back belt is the strap continuation, no buckle face. |
| Cape — collar | NO, layer swap | Front: collar is a small piece at the neck, cape back hangs behind. Back: the cape IS the torso covering — big black back piece dominates, collar reads differently, layer order flips (cape in front of torso, not behind). |
| Cape — back piece | YES, and it helps | The big black Cape_Back_Main is the one piece that genuinely works in both views — it is why a back cheat *almost* looks plausible at small scale. Almost is not on-model. |
| Arms — upper / forearm | PARTIAL | Lengths transfer, but gauntlet panels, elbow balls and hand orientation are front-drawn. Back arms hang with palms / thumbs reversed. |
| Hands | NO | Front hands show palm / fingers / thumb side. Back hands show back-of-hand. The 7-canon-hand library is front-view; back hands are a new set. Mirroring a front hand does not make a back hand — it makes a mirrored front hand. |
| Legs / knees | PARTIAL | Lengths transfer, knee balls transfer as shapes, but knee bend direction and shin shading read differently from behind. |
| Feet / boots | NO | Front boots show toe / laces / boot front. Back boots show heel. Toe direction — the knee-feet rule — reverses: a foot pointing camera-left in front points camera-right when the body turns around, and the drawing itself is a heel, not a toe. |
| Layer order | NO, must flip | Front: far arm/leg behind torso, near arm/leg in front. Back: the *other* arm/leg is now near. CapeGP's 10-layer order (FaceSnapArm > Head > CowlUpperArm > Neck > ChestSnapArm > Torso > Collar > NormalArm > Legs > CapeBack) is a front-view order and cannot be reused as a back order. |

Verdict on front-as-back: usable as a *silhouette placeholder* for a distant / dark shot, never as a back rig. If Mars wants a back shot that holds up at full size, build a back view set. It is the second-cheapest view set after 3/4, precisely because the cape does most of the work — but the head and feet still have to be drawn.

## 4. WHAT ABOUT SIDE? — THE HARDEST CHEAT, THE MOST NEEDED RIG

Side / profile cannot be faked from front at all:

- **Head:** profile head is a new drawing — nose bridge, chin, single visible eye, cowl shape in profile. Front head squashed sideways is not a profile.
- **Torso:** narrow depth, not wide chest. Chest emblem disappears (it is on the front plane, edge-on from the side).
- **Arms/legs:** only one arm and one leg are fully visible; the far arm/leg are darker copies drawn *behind* the body (the standard cutout side-view trick, documented in rig examples). Front rig has both arms/legs side by side — there is no "far" copy to hide.
- **Feet:** profile boots, toe in one direction only, heel opposite. Walking / stepping reads entirely in profile — which is why a side rig matters for the walk cycle Mars wants after the shimmy.
- **Cape:** side drape, hanging behind the body in profile, not spread wide like the front back-piece.

This is also why Mars's "side rig probably" note matters: there is no side art set in the current rig inventory to swap in yet. A side rig is a *new drawing* job first, a rigging job second. Front pieces cannot be "replaced with side art" until that side art exists — the registry should record side art as OWED, not as a swap waiting to happen.

## 5. WHAT SWAPS, WHAT MUST BE REDRAWN — CAPE JONES TABLE

General rule, per view: **skeleton and rules swap for free; artwork swaps only within its own view.**

| Swaps for free across views | Must be redrawn per view | Notes |
|---|---|---|
| Joint logic: pivot = ball centre, FK shoulder→elbow→wrist, hip→knee→ankle | Head / face / cowl per view | Front, 3/4, side, back heads are four different drawings. |
| Pose logic: angles, timing, inbetweening, knee-feet rule, wrist-by-wrist-end rule | Hands per view (palm vs back vs profile) | 7 canon hands are front-view. Side/back hand sets are new. |
| Layer *rules*: collar locked, cape back is the moving cape part, arms-up over face | Feet / boots per view (toe vs heel vs profile) | Knee-feet rule still applies, but the foot drawing changes. |
| Colourways / effects: Dream recolour, Dual Charge rim, Crystal overlay | Torso: emblem front only, cape coverage back, narrow side | Overlay effects sit on top of any view rig — Crystal stays an effect, not a rig, per Mars. |
| Cape Consumed logic: layer omission, white outline on self-crossing | Cape: back piece (front view) vs cape-as-torso (back view) vs side drape | White-outline rule is view-independent; the outline shape is view-specific. |
| Timing / xsheet / ground / airborne gates | Layer order per view | Front order ≠ back order ≠ side order. Record order per view in the registry. |
| — | 3/4 foreshortening: one side narrower, limbs foreshortened toward camera | 3/4 is not "front squashed 20%". Foreshortened forearm (CJ-15 piece) is the proof: width ×1.30 / height ×0.47, fist ×1.69. |

## 6. RECOMMENDATION — HYBRID MASTER RIG (ONE SYSTEM, VIEW SETS)

**Build this, in this order:**

1. **ONE master rig system** — keep the registry Mars already has (RIG-00 front, RIG-01 sitting, RIG-02 Cape Consumed, RIG-03 Dream, RIG-04 Dual Charge, RIG-05 CapeGP, Crystal as effect). Add a VIEW field to every entry: front / 3/4-front / side / 3/4-back / back. Never overwrite RIG-00. A "rig" in the registry = one view set + its pivots + its layer order + its piece list. The master system = the registry + the shared builders (joint-locked rig, wrist gate, knee-feet gate, no-crop gate).
2. **3/4 sitting rig — finish first, already in progress.** Source: Mars's uploaded sheet 2026-11-01 00:54 CDT (1200×1648, md5 4dc11a3dc88b9bd0cba55bc156971ecb), plus repo fallback clean-F72A5 (pre-bent sitting legs). This is the 3/4-angle room rig Mars asked for.
3. **Side rig — build next.** Needed before: true walk cycle, side-stepping, any profile shot. First step is side art (profile head, profile torso, profile limbs, profile boots, side cape drape, far-side darker copies), then rig it with the same joint logic. Record side art as OWED until it exists.
4. **Back rig — build after side.** Cheaper than side (silhouette + cape carry it), but still needs back head, back torso, back hands, heel boots, flipped layer order. Do NOT ship a front-mirror as a back rig.
5. **3/4 back — last of the five.** Only needed when a shot turns past profile. Can reuse 3/4-front joint logic with new art.
6. **Turns between views — use the existing pseudo-turn cheat for small turns, and view-group switching for big turns.** A front→3/4→side turn in a shot is: hold front rig, cut / inbetween to 3/4 rig, cut / inbetween to side rig. Harmony does this with Transformation-Switch groups; Cape Jones's PIL system does it by swapping the piece set at a keyframe and inbetweening angles, never by warping one drawing into another view. Do not claim a warped front is a turn.

**What NOT to do:**
- Do not mirror front art and call it back art.
- Do not squash front art and call it side art.
- Do not overwrite RIG-00 with a view set. RIG-00 stays front-facing, always.
- Do not build five separate animation systems. One builder, one gate set, five piece sets.

## 7. ANSWER TO EACH PART OF MARS'S QUESTION, PLAINLY

- "Do we need a rig from the side?" — **Yes.** No side rig exists, side art does not exist yet, and it cannot be faked from front.
- "And a rig from the three quarters?" — **Yes, and it is already being built** (3/4 sitting, from Mars's sheet).
- "Can the front rig also be a back rig, since it's from a certain perspective?" — **No, not honestly.** Silhouette and cape almost work; head, emblem, hands and feet fail. Build a back set, reuse the skeleton.
- "Can they all be one rig?" — **Yes, as one master rig system with view sets inside it.** One skeleton/logic, five drawing sets, switched as a group. That is the Harmony Transformation-Switch / Spine skin pattern, and it is exactly how the existing RIG-00…RIG-05 registry already works — it just needs a VIEW field added.

## SOURCES

- Toon Boom Harmony 20, About Structure for Multi-pose Deformation Rigs: each pose rigged in the same element must be a separate subgroup gathered by a Transformation-Switch node; rename subgroups front, side, quarter, etc. — https://docs.toonboom.com/help/harmony-20/premium/deformation/about-structure-multi-pose-deformation-rig.html
- Toon Boom Harmony 21, About Rig Structure and Master Controllers — https://docs.toonboom.com/help/harmony-21/premium/master-controller/about-rig-structure.html
- Toon Boom Harmony 24, About Swapping Drawings: cut-out animation uses several drawings on the same layers, swapped by exposure; mouths and hands are the classic examples — https://docs.toonboom.com/help/harmony-24/advanced/cut-out-animation/about-swap-drawing.html
- Toon Boom Harmony 24, About Character Preparation for a Multi-pose Deformation Rig: keep head, hands, feet, facial features on separate layers so drawing substitution can swap them without distorting limbs — https://docs.toonboom.com/help/harmony-24/premium/deformation/about-character-prep-multi-pose-deformation-rig.html
- Toon Boom Harmony 24, Setting Multiple Drawing Pivots: same drawing pivots on extra parts from the same angle, or a substituted drawing pops out of place while rotating — https://docs.toonboom.com/help/harmony-24/advanced/rigging/set-multiple-drawing-pivot.html
- Character Turnarounds: standard five views front, 3/4 front, side, 3/4 back, back, same neutral pose, construction lines across views — https://binus.ac.id/bandung/dkv/2025/11/04/character-turnarounds-understanding-form-in-2d-space/
- Character Turnaround guide: five views at one scale, same stance, check every detail lands at the same height in each frame — https://www.dreampixelforge.com/blog/character-turnaround
- Spine, Specifications of using two skeletons for one character: separate skeletons = separate exports, switched by visibility; unified alternative = front/back bone hierarchies under one root, or same bones with skin/attachment switching — https://en.esotericsoftware.com/forum/d/24046-specifications-of-using-two-skeletons-for-one-spine-character/1
- Spine forum, isometric monster front/back: separate skeletons are clearer to work on, single skeleton with skins is more efficient and smoother for mid-animation view changes — https://vi.esotericsoftware.com/forum/d/27002-isometric-monster-unity-multiple-animation/4
- 2D Character Animation methods: a side-view-only rotation rig fails for front walk because front/back arm and leg movement needs perspective scaling, not just rotation — https://medium.com/@jiesih/2d-character-animation-part-2-exploring-methods-of-2d-animation-b57a735729f5
- Cartoon Animator / 3D-to-2D: once you go 2D you lose the ability to view from any angle unless you make and rig the angles you need yourself — https://www.animationandvideo.com/2021/09/create-2d-animated-characters-with-3d.html?showComment=1637855089378
- 2.5D Character Rigs (arXiv): single-drawing 2.5D models need a view-dependent mesh and retargeting, not just rotation of the drawing — https://arxiv.org/html/2502.17866v1
- Cape Jones local sources (not web): sitting-rig-20261101/RIG-REGISTRY-20261101.md (RIG-00…RIG-05, Crystal as effect); joint_locked_rig_v7c.py (pivot = ball centre); pseudo-turn pack (out-and-back cheat, not a full turn); CJ-15 foreshortened forearm piece (width ×1.30 / height ×0.47).

## OPEN ITEMS FROM THIS RESEARCH (no build claimed)

- Side art set: OWED, no side head / torso / limbs / boots / side cape in the current rig inventory.
- Back art set: OWED as a full set (back head, back torso, back hands, heel boots, flipped layer order).
- VIEW field: add to the rig registry for every RIG entry.
- Mars's truncated "side read probably on": confirm whether he meant "side rig probably [needed] first" — this research assumes that reading, flagged above.
