# Ginyu Force — honest limits, BROKEN (Mars, 2026-10-31 ~18:38 CDT)

Order: "any of the honest limits, pull in any industry standard stuff to
help you break past those limits and make them not limitations anymore and
get it wired up 100% and then show me." No repo push in this task.
Mars approval of this limits-broken set: 0/1.

## 1. BURTER MACH KICK — BROKEN
- Old: BUR-03 leg upper 50 / lower -70 = ~120 deg knee bend, foot dangling.
- New: `bur-03-mach-kick-extended-20261031.png` — leg upper 65 / lower 60,
  knee flexion ~5 deg, leg fully extended to the side, foot at the end of
  the leg pointing along the leg axis. Industry method: cutout leg
  extension — re-pose existing upper/lower pieces to a near-straight
  angle instead of a bent one, knee joint handled per the knee-feet rule
  (knee, ankle and foot on the same leg axis, no broken-knee read).
  No straight-leg piece was needed: the existing pieces straighten when
  their angles match. No new leg was drawn.
- Fix in v2: first build clipped the foot at the canvas edge; reframed
  with figure centre cx=470 so the whole extended foot fits in 1100px.
- Check: standing foot planted, kicking foot along the leg, silhouette
  reads as a kick, not a raised bent leg.

## 2. TRUE TORSO TWIST — BROKEN as segment-twist (see remaining gap)
- Old: twist carried only by limbs + head tilt + leg torque; torso itself
  did not twist.
- New: `cap-01-twist-segment-20261031.png` (chest rotated -12 deg,
  shoulder line tilted 20px, pelvis/belt unrotated) and
  `bur-01-twist-segment-20261031.png` (chest +8 deg, tilt -16px).
  Industry method: cutout segment twist — torso as separate upper
  (chest) and lower (pelvis/belt) segments counter-rotated, the standard
  cutout answer to torso twist without redrawing the torso (Harmony /
  Animate / Spine segment rigging: chest and pelvis are separate
  deformable segments, shoulders counter-pose against hips).
- Search result, plainly: NO separable torso piece was found in the
  sheet library. B-model 3/4, side and back sheets are WHOLE-FIGURE
  pieces (Row1_1, 523-1106px wide, one full figure each), not cut torso
  pieces, so there is no pulled 3/4 torso to wire in. The fighting /
  hand-library workstream is cutting those sheets, but a cut torso
  piece does not exist yet.
- Remaining gap, stated not hidden: a true redrawn 3/4 torso MASTER
  still does not exist. Segment-twist breaks the "torso itself doesn't
  twist" limit; it does not create a redrawn master, and none is
  claimed. If Mars wants a redrawn master, that is a hand-drawn item,
  which he has banned as a presented solution — segment-twist is the
  correct industry cutout answer, and it is now the default twist
  method in the builder (`chest_rot` + `shoulder_tilt` parameters).

## 3. HANDS ARE FISTS — BROKEN (serve + point)
- Old: Jeice serve staged with a fist where the staging uses an open palm.
- New: `jei-01-crusher-serve-open-palm-20261031.png` — pulled piece
  `sliced/Hand_3_Open.png` (white gloved open hand, same suit style)
  substituted at the serving hand (centre ~(314,530), rotated -20 deg
  to match the forearm). Method: drawing substitution, the industry
  cutout hand system (Harmony/Animate hand swap libraries: fist, open,
  point, grip are separate drawings swapped per pose). The old fist
  was removed by erasing only near-white pixels (R,G,B > 180) inside
  a 65px radius of the fist centre, so dark cape behind it is untouched.
  Hand-first rule applied: hand shape (open palm) drives the read, and
  the serving arm stays on the top layer (face/cowl snap: never buried).
- Correction found while doing this, stated plainly: original JEI-03
  does NOT point up-out as its study description said — its lower
  angle 40 bends the fist inward to the chest. So JEI-03 was NOT
  force-swapped (its fist overlaps the torso, and a point swap there
  would erase torso). Instead a NEW variant was built:
  `jei-03x-point-variant-20261031.png` — lower angle -160 puts the
  hand up-left and isolated, pulled piece `sliced/Hand_4_Point.png`
  substituted (centre ~(157,134), rotated 35 deg), finger pointing up.
  Labelled VARIANT, not a correction of JEI-03's description.
- Base files kept for reproducibility: `jei-01-base-for-swap-`,
  `jei-03-base-for-swap-`, `jei-03x-point-variant-base-`.

## 4. NO ENERGY EFFECTS — BROKEN as PIL effect layers (5/5)
- Poses untouched: every effect is a separate PIL layer composited over
  the original pose; no pose pixel was recoloured. Colours tracked
  (input -> on-screen sample at the effect centre):
  - REC blast `rec-02-eraser-blast-effect-20261031.png`: beam cone
    (255,120,40) from the mouth + orb (255,220,120) at the end.
    On-screen orb centre (255,220,120) = preserved (opaque orb).
  - BUR hurricane `bur-02-hurricane-swirl-effect-20261031.png`:
    swirl arcs (160,220,255) + white, radii 260-470 around the body.
    Honest note: outer rings read faint at contact-sheet size; inner
    cyan arcs read clearly.
  - JEI ball `jei-01-crusher-ball-effect-20261031.png`: orb
    (255,230,110) above the open palm, Sunbeam-orb method (orb snapped
    to the hand, glow ring, sparkles). On-screen (255,230,110).
  - GUL time `gul-02-time-freeze-effect-20261031.png`: clock rings
    (120,180,255) + 12 tick marks, centred on the upper body.
    Honest note: rings are centred on the upper body, not on the
    hands alone — the hands are forward, the rings read as a
    time-freeze field around him.
  - CAP swap beam `cap-02-swap-beam-effect-20261031.png`: purple beam
    arc (170,90,255) + orb (220,180,255) above the head, between the
    spread hands. Honest note: the arc reads as a top beam, not a
    hand-to-hand line — its endpoints sit near the raised hands, not
    touching them.
- Remaining gap, stated not hidden: these are PIL effect layers,
  labelled as such, NOT Blender compositor renders. The Blender
  upgrade (Sunbeam Preset v1 / Glare / volumetric shafts per effect)
  is still owed and is not claimed here.

## 5. BONYU CANONICAL POSE — STANDS (source reason, not technical)
- No source found documents a canonical Bonyu signature pose. Her
  documented trait is that she hates posing and quit over it.
- This limit is NOT broken by any method, and no canonical Bonyu pose
  was invented or claimed as canonical. Bonyu stays trait-derived
  and labelled (BON-01/02/03 in the original study).
- What would change it: a source documenting a Bonyu pose, or Mars's
  own call to design one. Either would be recorded as the source, not
  presented as found canon.

## 6. DUPLICATE SHEET — RESOLVED by labelling, no deletion
- `bon-contact-20261031.png` and `bonyu-contact-20261031.png` are
  BYTE-IDENTICAL (md5 14b9b2791a6f83db6c0712c7a8608186, both files).
- Resolution: `bonyu-contact-20261031.png` is the CANONICAL Bonyu
  sheet; `bon-contact-20261031.png` is a DUPLICATE REFERENCE to the
  same 3 poses, not a 19th pose and not a separate sheet. Neither file
  was deleted (both were in the delivered study; deleting a file Mars
  has seen is banned). Future references use bonyu-contact only.

## Checks passed (viewed)
- Silhouette: all 10 new singles read in silhouette on the contact
  sheet (grey-128 viewing background only).
- Knee-feet: kick leg straight with foot along the leg axis; standing
  foot planted; Guldo-style crouches unchanged.
- Arm/face/cowl snap: Jeice serve arm and point-variant arm are top
  layer, never buried under the cowl; no raised arm in the new set is
  buried; Guldo guards were already top-layered in the original set.
- No file Mars saw was overwritten: every new file is in the new
  dated folder `ginyu-force-limits-broken-20261031/`.

## Wired 100% — preset update
- `GINYU-FORCE-PRESET-UPDATE-20261031.json`: straight-kick angles
  (65/60), segment-twist parameters (chest_rot, shoulder_tilt),
  hand-swap pieces (Hand_3_Open, Hand_4_Point with centres/angles),
  effect presets per member with input colours. Future poses use
  these by default: straight legs for kicks, segment-twist for
  torso counter-rotation, hand substitution from sliced/ instead of
  defaulting to fists, effects as separate layers.
- Builders: `build_limits_broken.py`, `build_v2.py`, `build_effects.py`
  in the same folder. Original study files untouched.
