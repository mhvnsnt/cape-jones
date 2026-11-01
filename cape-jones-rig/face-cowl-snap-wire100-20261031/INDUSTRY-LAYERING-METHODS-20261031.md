# Industry Layering Methods — pulled and wired for face/cowl/chest snaps (2026-10-31)

Methods only, no proprietary code, no show character, no dialogue, no logo.
Each method: source, method in one paragraph, exactly how it is wired into
OUR pipeline, and the proof. A method with no proof is labelled as such.

## 1. Toon Boom Harmony — Z-depth ordering + drawing substitution
Source: docs.toonboom.com, Harmony 24 Premium "Ordering in Z-Depth" and
Harmony 25 Essentials "Drawing Layer Substitution View"; plus the
Animate-to-Harmony cut-out guide (depth nudging chapter): layer order in
the Timeline IS render order, top over bottom, and a layer's Z position
can be nudged (micro-nudge, keyframed) to force it beneath or over other
layers without moving it in the Timeline or breaking its hierarchy —
the textbook example is a character placing hands behind the head and
then, in the same scene, placing them over the mouth, by keyframing
depth order. Drawing substitution (press [ / ] in the substitution view)
swaps the exposed drawing on a layer at a frame — the 2D equivalent of
our fist/cuff piece swaps.
Wired here: our snap IS a Z-nudge keyframe. Gate decision per side per
pose/frame maps 1:1 to a Harmony Z key: NO SNAP = normal Z, CHEST =
arm Z above torso and below head, FACE = arm Z above head, COWL =
upper-arm Z above collar only. The audit CSV (audit-wire100-20261031.csv)
is the Z-keyframe table: pose, side, gate numbers, applied snap.
Proof: gate output + fixed poses in this folder and in
pose-dialects-fix-face-cowl-20261031/ (viewed, before/after + crops).

## 2. Adobe Animate — layer parenting + reparenting at any time
Source: Adobe blog "Rigging Characters Using Layer Parenting" (Animate
2019) and Adobe Learn "Layer parenting": every body part on its own
layer, converted to a symbol, parented (hand -> forearm -> upper arm ->
torso, head -> neck -> torso), pivots moved to anatomically correct
hinges; a parent can be removed or changed at any time, and a part can
be reparented to a different layer for a pose.
Wired here: a snap is a TEMPORARY REPARENT for one pose/frame — the
flagged arm chain is reparented from "under torso/collar/head" to a
top-level layer for that pose only, then returned. Our builder's snap
passes (snap_figure.py: chest pass, cowl pass, face pass) are exactly
that reparent, implemented as render order, not as a permanent rig
change. The earlier Animate-side failure mode is also wired in as a
warning: arms parented inside Body cannot overlap Head at all unless
re-layered out of that parent (e.g. hands on the cheek for a scream) —
that is why a face snap must be an explicit re-layer, never an accident
of the default order.
Proof: snap_figure.py renders (ginyu-03 / v7c-jump cowl fixes, viewed)
and the JoJo 02 L counter-proof: a whole-chain reparent there COVERS
the face, so it is banned — see §8.

## 3. Godot cutout — Z property + RemoteTransform2D (order independent of hierarchy)
Source: docs.godotengine.org, "Cutout animation" (Godot 3.1 docs): depth
ordering problems are fixed by adjusting the Z property of any Node2D,
and RemoteTransform2D lets a node elsewhere in the hierarchy drive a
sprite, so visibility order becomes INDEPENDENT of the hierarchy —
"create a RemoteTransform2D node as a child of the torso, link it to
the arm/hand sprites, and animate the remote transforms."
Wired here: our snap passes do exactly this separation — the arm's
TRANSFORM (shoulder/elbow angles, pivots) is computed from the skeleton
as always, but its RENDER ORDER is decided separately by the gate, per
side per pose. snap_figure.py computes elbows from the arm angles first,
then draws each chain in its gate-decided pass. That is the Godot
principle in our own builder, with no Godot file needed.
Proof: snap_figure.py ginyu-03 test render matches the upper-only cowl
fix to within 36 px RGB-diff>20 (the 36 px are the elbow cap, which the
cowl pass correctly leaves in its normal position — see §8).

## 4. Spine — keyable draw order + asset cutting (round joints, draw hidden parts whole)
Source: Esoteric Software blog "How to cut your assets for animation"
and Spine draw-order documentation (as summarised in the Kodeco Spine
tutorial): draw order is a list, top of the list draws on top, and it
is KEYABLE per animation; assets must be drawn whole even where they
are usually covered, joints must end as close to a circle as possible
so no gap opens on rotation, and parts that pass in front of AND behind
an object must be on SEPARATE layers (or split at the join).
Wired here: (a) our audit CSV is a keyable draw-order table — one row
per pose per side, with the snap as the draw-order key for that pose;
(b) our v7c pieces already follow the asset rule — upper/lower pieces
are whole-limb crops from the ball centre with a circular cap, so a
snapped upper drawn over the collar does not reveal a trimmed edge or
a gap at the elbow; (c) the cowl refinement (§8) is the Spine split
rule applied: the upper arm (which passes in front of the collar) and
the lower arm (which does not pass in front of the head) are treated as
separate draw-order items, not one blanket chain.
Proof: ginyu-03 / jump cowl fixes — bicep continuous over the collar,
no gap at the elbow, no trimmed edge (viewed, crops in this folder).

## 5. Traditional animation — cel stacking order, with a deliberate override
Source: traditional cutout / cel practice (as documented in the
cut-out guides above): puppets are built in layers with a deliberate
stacking order "so an arm can pass in front of the chest but behind
the head," limbs cut longer than needed with rounded pivots so no gap
opens at the joint. A cel stack is a physical order — you cannot
re-order one cel without lifting the whole stack, which is why the
default order must be right and overrides must be deliberate.
Wired here: the DEFAULT stack is written in ARM-FRONT-SNAP-RULE.md
(cape-back, legs, torso, arm, neck, head) and is never changed. A snap
is a documented OVERRIDE for one arm in one pose, with the gate number
as the reason, recorded in the audit CSV. No silent re-stacks.
Proof: default poses (apose, seated, dance rest) all gate NO SNAP and
are untouched in this audit — 43/62 side-checks = 69% NO SNAP.

## 6. Blender Grease Pencil — layer tree, view order top-to-bottom, per-layer parent
Source: docs.blender.org, Blender 5.2 LTS Manual, "Layers" (Grease
Pencil): objects are organised in a layer tree, view order is top to
bottom, a layer can only be in one group, layers can be moved by
drag-and-drop, a layer can have a parent object (inheriting its
transform, "especially useful when rigging for cut-out animation"),
and any layer can mask another.
Wired here: as a MAPPING TABLE, not a Grease Pencil file — our snap
passes map to a Grease Pencil layer tree as: FaceSnapArm (top) >
Head > CowlUpperArm > Neck > ChestSnapArm > Torso > Collar >
NormalArm > Legs > CapeBack (bottom), with the per-pose snap deciding
which pass a given arm's layers sit in. The mapping is in
snap_figure.py's pass order and in this doc.
Proof status — HONEST LIMIT: no Grease Pencil .blend rig was built in
this task, so the GP mapping is a documented port, not a viewed GP
file. A GP rig pass (layers + parent + a snapped pose) is owed if Mars
wants Grease Pencil as a delivery format; it is NOT claimed here.

## 7. OpenToonz / Tahoma2D — SO (stacking order) value, animated per frame
Source: OpenToonz 1.7.1 docs "Creating Movements" (Changing Stacking
Order of Columns/Layers) and Tahoma2D 1.6 docs "Creating Cutout
Animation": column stacking order sets which drawings sit on top, and
by editing the SO value it is possible to change AND ANIMATE the
compositing order without moving columns in the Xsheet — otherwise an
element that moves behind then in front of another must be exposed in
two different columns. Tahoma's Skeleton tool links sections with
pivots; the SO value is the depth key.
Wired here: our snap decision IS an SO value per side per pose/frame:
SO(normal) < SO(torso) < SO(chest) < SO(head) < SO(face), with
SO(cowl-upper) sitting between torso and head for the upper arm only.
The audit CSV records the SO-equivalent (applied snap) per side, and
the dance-arm-snap per-frame audit (arm-snap-audit-20261031.csv, 63
frames) is the frame-level SO table for the dance.
Proof: dance-arm-snap GIF + per-frame audit (prior task, viewed) and
this audit's CSV.

## 8. The refinement this audit proved — COWL IS UPPER-ONLY (new, wired)
Tested in this audit and now standing: a whole-chain cowl snap is
WRONG when the lower arm touches the head edge. JoJo 02 L (lower_vs_head
= 2,996 px, fist beside the head, NOT a face crossing) snapped
whole-chain puts the fist OVER the face — a gate failure in reverse.
The correct cowl snap moves ONLY the upper arm above the collar; the
lower arm stays in its normal position (after torso, before head).
check_pose_snap.py BANS cowl-whole (exit 1) and snap_figure.py has a
separate cowl pass that draws the upper only. Ginyu 01's original
whole-chain cowl fix is unaffected (its lower_vs_head = 0, so the two
implementations coincide there); ginyu-03 and jump use the upper-only
form. snap_figure.py vs the earlier whole-chain test render differs by
only 36 px RGB-diff>20 on ginyu-03 — those 36 px are the elbow cap,
correctly left in its normal position by the upper-only pass.

## NOT APPLICABLE — named, not silently skipped
- True 3D camera depth (Maya / 3D rigs): a 3D character's depth comes
  from camera distance, not draw order. Our rig is 2D cutout; there is
  no camera-depth axis to key, so 3D depth methods do not apply. The
  2D equivalent (Z-nudge / SO / draw order) is what is wired above.
- Auto lip-sync / audio-driven layer switching: changes WHICH drawing
  is exposed (mouth shapes), not the stacking order of limbs. It is
  already wired separately (visemes v2, mask-first) and does not touch
  arm layering.
- After Effects 3D layers / camera: same reason as Maya — a 3D-layer
  system is not our 2D cutout stack. After Effects 2D layer order is
  the same principle as §5 and adds nothing new, so it is not listed
  as a separate method.
