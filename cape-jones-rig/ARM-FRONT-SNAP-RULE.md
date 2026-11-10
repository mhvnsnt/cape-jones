# ARM-FRONT-SNAP RULE — standing, Mars 2026-10-31 17:58 CDT

## The problem Mars flagged (corrected dance GIF)
When his arms cross past the threshold of his torso/chest — where his
ribs and pecs start — his forearms and fists get EATEN by his torso:
drawn underneath his pecs, so the arm reads as detached or swallowed
at the chest line. The fix is a MOMENTARY layer snap, not a permanent
reorder.

## The rule
**When an arm's forearm crosses the torso threshold, that WHOLE arm
(upper + forearm + fist + elbow cap) snaps to the layer ABOVE the
torso for exactly as long as it is crossing — and returns to its normal
layer the moment it is out.**
- Arms out to the side: NO snap. Normal order stands.
- Arm in front of the chest/pecs/ribs: SNAP to front. The arm must read
  as one continuous chain shoulder -> elbow -> fist, in front of the
  chest, never cut in half by the pec line.
- This is per arm, per frame. One arm can be snapped while the other is
  not. A snap never carries over to the next pose, and never becomes
  the default layer order.

## Why the old order ate the arm (diagnosis, measured)
The v7c dance builder drew pieces in this order: upper arms BEFORE the
torso, forearms AFTER the torso. So on a crossed frame the forearm was
already in front — but the upper arm segment between shoulder and elbow
was hidden BEHIND the chest. The arm therefore read as a forearm
floating at the pec line with its shoulder connection eaten. The piece
that was eaten was the upper arm, not the fist. Snapping only the
forearm would change nothing; the whole chain must move.

## Threshold definition (measurable, not eyeballed)
- Torso zone = the Torso_Chest.png alpha mask, placed at centre-x 550,
  top 400, scale 0.95 (full-res bbox approx x402-698, y404-702). The
  pec/rib zone is the upper part of that mask, where ribs and pecs are
  drawn — crossing is judged against the whole torso mask, because a
  forearm entering it from the side is already crossing chest.
- Snap condition (gate): that side's forearm alpha overlaps the torso
  alpha by MORE THAN 1000 px at 1100x1500.
- Why 1000: measured on all 63 corrected-dance frames, out-to-side
  frames measure 0-268 px overlap, crossed frames measure ~1500-9000 px.
  The gap is wide; 1000 sits in the empty middle, so the gate does not
  flicker on shoulder-edge contact.
- Upper-arm overlap is NOT the test: upper arms always overlap the
  torso by 4000+ px at the shoulder attachment, crossed or not. Only
  forearm overlap discriminates.

## Snap duration and return
- Snap lasts ONLY while the condition holds on that frame. It is a
  momentary, per-frame decision, recomputed every frame from that
  frame's own pose — never a block range (same lesson as the knee-feet
  correction: a block range flips frames it should not).
- When the arm leaves the torso zone, it returns to normal order
  (upper behind torso, forearm in front) on the very next frame. No
  fade, no hold: the snap is a depth-order switch, and a switch that
  lingers past the crossing reads as a different pose.
- Head stays above a snapped arm — EXCEPT in the face-crossing case
  below (extension, Mars 2026-10-31 ~18:27 CDT, supersedes this line
  for face-crossing arms only). Cutout stacking order for a chest-only
  snapped arm is: cape-back, legs, torso, SNAPPED ARM, neck, head. An
  arm passes in front of the chest but behind the head — never over
  the face, UNLESS it is a face-crossing arm (see extension).

## Anatomy + animation basis (researched, methods only)
- In a real body, an arm swung across the chest is IN FRONT of the
  ribcage: the shoulder girdle protracts, the arm passes anterior to
  the pectoralis, and nothing of the chest occludes it. A 2D drawing
  that hides the upper arm behind the chest on that pose contradicts
  the body's own depth, which is why it reads as "eaten" rather than
  as a stylistic choice.
- Toon Boom Harmony cut-out rigging (docs.toonboom.com, "How to Rig a
  Cut-out Character"): the order of layers in the Timeline is the
  render order, top over bottom, and "should you need to change a
  layer's order while animating, you can nudge this layer's position
  on the Z-axis to override the layer order and force it to appear
  beneath or over other layers." That Z nudge, keyed per frame, IS
  this snap in Harmony terms.
- Godot cutout documentation (docs.godotengine.org, cutout animation):
  a node can change its visual depth relative to its parent DURING an
  animation (keyframable "Behind Parent" / Z property), e.g. an arm
  pulled from behind the back to in front of the body must change
  depth mid-motion. Depth is a per-frame property, not a rig constant.
- Traditional cutout practice: puppets are built in layers with a
  deliberate stacking order "so an arm can pass in front of the chest
  but behind the head," with limbs cut longer than needed and rounded
  at the pivot so no gap opens at the joint when the piece rotates.
  The snap preserves that order: chest < arm < head.
- Industry-standard method wired here (free, in our own builder):
  alpha-mask overlap test per side per frame (forearm mask vs torso
  mask) + whole-chain re-layer above the torso. No proprietary code,
  no Harmony/Animate file needed; the same gate ports directly to a
  Harmony Z-nudge keyframe or a Tahoma2D layer-order keyframe when
  those rigs are used (snap ON = arm layer above torso, snap OFF =
  normal order), because the decision is a measured number, not a
  guess from angles.

## Pipeline gate
- Every pose/clip that puts an arm across the chest MUST carry a
  per-frame arm-snap audit (frame, side, overlap px, snapped Y/N).
- A clip with NO audit, or with a block-range snap, FAILS the gate.
- A frame where a forearm overlaps the torso by >1000 px and the
  upper arm is still drawn behind the torso FAILS the gate (eaten arm).
- A frame where an arm is snapped while its forearm overlap is
  <=1000 px FAILS the gate (snap without a crossing reads as the arm
  floating in front of the body for no reason).

## FACE / COWL SNAP EXTENSION — standing, Mars 2026-10-31 ~18:27 CDT
Mars flagged the pose-dialects contact sheet, top row frame 3 (JoJo 03
menacing-lean-hand-to-face) and frame 6 (Ginyu 01 roll-call chest-out):
"his arm parts need to go over his torso and over his face like his
hand and his forearm and his bicep need to be on the top layer because
he's lifting his arm so high up that it's covering his face" and, for
frame 6, "his arm has went up so high that it now should be on the
layer above his cowl and his cowl is covering up where his bicep is
which is not a correct layering." Otherwise the set looks great /
awesome. This extension exists so he never has to repeat it.

### The rule (three cases, per arm, never a whole-pose blanket reorder)
1. CHEST-ONLY (original rule): forearm crosses torso, face not
   crossed. Order: cape-back, legs, torso, SNAPPED ARM, neck, head.
   (torso < arm < head)
2. FACE-CROSSING: the arm is lifted so high / so far forward that its
   forearm + fist cross IN FRONT OF the face. Order: cape-back, legs,
   torso, neck, head, SNAPPED ARM. (torso < head < arm) — the arm
   covers part of the face/cowl BY DESIGN of the pose. The face still
   reads where the arm does not cover it; the arm must read as one
   continuous chain shoulder -> elbow -> fist over the face, never
   as a fist floating beside the head with its arm eaten behind it.
3. COWL / CAPE-COLLAR-CROSSING: a raised upper arm passes in front of
   the cowl / cape-collar at the shoulder, so the bicep must sit ABOVE
   the collar layer, not under it. Order for that arm: above torso,
   collar, neck and head (same top layer as a face snap; it changes
   nothing where the arm does not overlap the head). The buried
   segment here is the BICEP (upper arm, drawn before the collar in
   the old builder order), not the fist — moving only the forearm
   would change nothing, the whole chain must move, same as the
   chest case.

In all three cases the snap is momentary / per-pose: it applies to
that flagged arm, in that pose, only. It never becomes the default
order, and it never moves the other arm.

### Why the old order ate these arms (diagnosis, measured)
Old v7c builder order: upper arms BEFORE torso/collar, lower arms
AFTER torso/collar but BEFORE neck/head. So:
- JoJo 03, Arm_Back (R, our right): upper -88 / lower 145. Lower
  (forearm+fist) vs head = 7,941 px; upper vs collar = 19,172 px;
  lower vs torso = 2,143 px; neck overlap 5,621 px (lower) +
  2,317 px (upper). In the original, only a white fist peeks out
  beside the top of the head — the forearm and bicep are eaten
  behind head, neck and collar. Buried: whole R chain.
- Ginyu 01, Arm_Front (L, our left): upper -160 / lower -20.
  Upper vs collar = 5,097 px; lower vs head = 0 px; lower vs collar
  = 0 px; lower vs torso = 0 px. In the original, the raised bicep
  is cut by the black cape-collar at the shoulder while the forearm
  and fist (already drawn after the collar) read fine. Buried:
  upper arm (bicep) only — but the fix still moves the WHOLE chain
  to the top, so the chain stays continuous and no new seam opens.
  The "cowl" in Mars's words is the black cape-collar/shoulder
  piece at the shoulder (Cape_Collar.png); the purple head cowl
  itself has 0 px overlap with this arm, stated plainly.
- Other arms untouched: JoJo 03 L lower vs head = 0 px; Ginyu 01 R
  lower vs head = 0 px, elbow 164 px BELOW its shoulder (not raised).

### Gate (measured, not eyeballed)
Builder check: pose-dialects-fix-face-cowl-20261031/
check_face_cowl_snap.py — per side, per pose, from the pose angles:
lower-vs-head, upper-vs-collar, lower-vs-torso, elbow height vs
shoulder. Run it on every pose that puts an arm near the head or
raised above the shoulder; keep its output with the pose.
- FACE-SNAP (numeric): forearm/lower vs head > 5,000 px. Gap in the
  measured singles: flagged JoJo 03 R = 7,941 px; next highest
  single-pose value is JoJo 02 L = 2,996 px (edge contact beside
  the head, fist outside the head — NOT a face crossing, NOT
  snapped in this task); all other singles = 0 px. 5,000 sits in
  the empty middle, so the gate does not flicker on side contact.
- COWL-CANDIDATE (numeric flag + eye-check, NEVER automatic):
  elbow above its shoulder by > 50 px AND upper vs collar
  > 1,000 px. Collar overlap alone does NOT decide: unflagged arms
  measure 3,451–4,774 px upper-vs-collar at a normal shoulder
  attachment, and raised-but-unburied arms (e.g. Ginyu 03, elbows
  129–134 px above shoulder) also flag as candidates. A cowl snap
  is applied only when the eye-check confirms the bicep is actually
  interrupted/cut by the collar — as Mars confirmed for Ginyu 01 L.
- CHEST-SNAP (unchanged): forearm vs torso > 1,000 px, face not
  crossed. Priority when more than one gate fires: FACE > COWL >
  CHEST, because a face snap already puts the arm above torso and
  collar as well.
- A pose where a forearm overlaps the head by > 5,000 px and the arm
  is still drawn behind the head FAILS the gate (eaten face arm).
  A pose where an arm is put above the head with lower-vs-head
  <= 5,000 px FAILS the gate (arm over the face for no reason).

### Anatomy + animation basis (researched, methods only)
- Anatomy: when an arm is raised and brought forward across the
  face, the shoulder girdle protracts (scapula slides forward
  around the ribcage, serratus anterior) and the arm is ANTERIOR to
  the face in depth — nothing of the head occludes a limb that is
  physically in front of it. Drawing the head over such an arm
  contradicts the body's own depth, which is why it reads as
  amputated/eaten rather than as a stylistic choice. Sources used:
  serratus-anterior / scapular protraction + upward rotation for
  overhead elevation (standard anatomy references, e.g. the
  serratus-anterior action summaries returned in research).
- Cutout layering: Toon Boom Harmony docs ("How to Rig a Cut-out
  Character"; "About Ordering Layers"; "Ordering in Z-Depth") —
  timeline layer order IS render order, top over bottom, and a
  layer's Z position can be nudged mid-animation to force it
  beneath or over other layers, keyed per frame. The textbook
  example is exactly this: a character can place hands behind the
  head and then, in the same scene, place them over the mouth, by
  keyframing depth order, without swapping timeline layers.
- Traditional cutout: puppets are built in layers with a deliberate
  stacking order "so an arm can pass in front of the chest but
  behind the head" — that default is correct for chest crossings
  and is precisely what must be OVERRIDDEN for a face crossing,
  where the intended depth is arm-in-front-of-head. The Adobe
  Animate community layer discussion makes the same point from
  the other side: arms parented inside Body cannot overlap Head
  at all unless they are re-layered out of that parent for the
  pose (e.g. hands on the cheek for a scream) — the fix is a
  per-pose re-layer, not a permanent rig change.
- Method wired here (free, in our own builder): whole-chain
  re-layer above head/collar for the flagged arm only, at the
  original angles, no redrawn art. Same gate ports to a Harmony
  Z-nudge keyframe or a Tahoma2D layer-order keyframe (face snap
  ON = arm layer above head, OFF = normal order).

### First application (2026-10-31)
- pose-dialects-fix-face-cowl-20261031/: JoJo 03 FACE-SNAP fixed
  (25,994 px changed vs original — the previously hidden chain
  now drawn over head/collar/torso) + Ginyu 01 COWL-SNAP fixed
  (8,465 px changed — the previously cut bicep now drawn over the
  collar). Originals untouched. Before/after contact + face-zone
  and cowl-zone zoom crops viewed. Mars approval of the fixed
  versions: 0/1. No repo push in this task.
- Honest limits: in the JoJo 03 fix the forearm covers the
  viewer's-right eye area — that is the pose's own design (hand
  to face), not a layering error; making the eye visible would
  need a pose-angle change, not a layer change, and no angle was
  changed here. In the Ginyu 01 fix the bicep now sits over the
  black collar edge — that is the correction, not a defect. The
  cowl gate remains candidate+eye-check, not fully automatic (see
  gate above). JoJo 02 L (2,996 px edge contact) was NOT changed
  in this task — Mars did not flag it, and it reads as an arm
  beside the head, not in front of the face; it is noted here so
  it can be asked about, not silently fixed.

## WIRE-100 REFINEMENTS + PIPELINE STEP — standing, 2026-10-31 (Mars: "get all that wired up 100%")
Full audit, fixes and industry methods:
face-cowl-snap-wire100-20261031/WIRE100-REPORT-20261031.md and
INDUSTRY-LAYERING-METHODS-20261031.md. Audit: 31 angle-known entries,
62 side-checks — FACE 2/62 = 3% (JoJo 03 R, already fixed), COWL-CANDIDATE
9/62 = 15%, CHEST 8/62 = 13%, NO SNAP 43/62 = 69%.
- COWL IS UPPER-ONLY (new, standing). The buried segment in a collar
  crossing is the bicep; the lower arm stays in its normal position.
  Whole-chain cowl is BANNED: JoJo 02 L (lower_vs_head 2,996, fist
  beside the head, not a face crossing) snapped whole-chain puts the
  fist OVER the face — viewed, a gate failure in reverse. Ginyu 01's
  original whole-chain cowl fix is unaffected (its lower_vs_head = 0,
  so the two implementations coincide there). New upper-only fixes:
  Ginyu 03 (both arms) and v7c-jump (both arms), bicep notch at the
  collar removed, face untouched, approval 0/1 each.
- CHEST IS A WARNING, not an automatic FAIL. lower_vs_torso > 1000
  flags a pose for eye-check; it FAILs only if the eye-check says the
  upper IS eaten and no snap was applied (stand-02 user and v7c-flex
  prove the not-eaten case: forearms already in front, uppers at the
  sides). Dance chest snaps stand because the dance audit proved the
  eaten upper there, per frame.
- COWL GATE STAYS candidate + eye-check, never fully automatic:
  normal shoulder-attachment collar overlap (3,451–4,830 px in this
  audit) overlaps the candidate range, so the number alone cannot
  decide. JoJo 02 L and the stand-02 shadow figures (flat silhouette,
  no collar piece) are logged false positives / N/A, NOT fixed.
- PIPELINE STEP (mandatory, pre-delivery): face-cowl-snap-wire100-
  20261031/check_pose_snap.py — run from the pose ANGLES before
  rendering (a flat PNG cannot prove layer order after the fact).
  Exit 0 = PASS, exit 1 = FAIL (face snap missing, cowl candidate
  without eye-check, banned cowl-whole, or a face snap with no gate
  reason). snap_figure.py is the snap-aware builder new poses use
  (normal / chest / cowl-upper / face passes, per side). The frozen
  approved-pose builders (joint_locked_rig_v7c.py, build_poses.py)
  are NOT edited — the gate sits in front of them, because editing a
  frozen builder risks changing an approved pose.
- Industry methods wired: Harmony Z-depth + drawing substitution,
  Animate layer parenting/reparenting, Godot Z + RemoteTransform2D,
  Spine keyable draw order + asset cutting, traditional cel stacking,
  Blender Grease Pencil layer tree (mapping only, no GP file claimed),
  OpenToonz/Tahoma2D SO value. Not-applicable methods named with
  reasons in the methods doc (true 3D camera depth, auto lip-sync).

## First application (2026-10-31)
- dance-arm-snap-20261031/: corrected dance rebuilt with the snap.
  See SNAP-REPORT-20261031.md there for frame counts, before/after
  and GIF. Old correction folder untouched. Approval 0/1.
- This rule applies going forward to EVERY pose, clip and shot, not
  just the dance: punch, fight, flex, walk, and any future rig.
