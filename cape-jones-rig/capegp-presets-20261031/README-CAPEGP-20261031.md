# CapeGP — Cape Jones Grease Pencil Layer Rig

**Formal name, use everywhere: CapeGP.** Do not invent a different name.
Approval of this preset pack: **0/1**. No repo push made from here.
Originals untouched; every output in this folder is a new dated file.

## What CapeGP is
- Blender 5.2.3 LTS, one Grease Pencil object named `CapeGP`.
- 10 layers, front-to-back, exactly:
  `FaceSnapArm > Head > CowlUpperArm > Neck > ChestSnapArm > Torso > Collar > NormalArm > Legs > CapeBack`
- One colour-coded material per layer (same colours as the original GP rig):
  FaceSnapArm orange-red, Head purple, CowlUpperArm gold, Neck skin,
  ChestSnapArm cyan, Torso near-white, Collar near-black, NormalArm pale,
  Legs pale-blue, CapeBack dark purple. Layer `use_lights=False`, flat like 2D art.
- Every stroke is the traced outline (cv2 largest external contour,
  approxPolyDP, max 140 points) of an existing v7c source piece, placed by
  the SAME joint/anchor/rotation math as `snap_figure.py`. No new art drawn.
- Strokes are outlines only. No colour fills, no interior linework yet.
  Those are the next passes, stated as owed, not claimed here.

## Pipeline rule — state this in every CapeGP doc
- **PIL/v7c (`snap_figure.py` / `joint_locked_rig_v7c.py`) is DEFAULT**
  for approved poses, clean plates, and anything that must match an
  already-approved file pixel-for-pixel. It is the production path.
- **CapeGP is USED for:** (a) layer-order proofs — a snap decision seen as
  a layer stack, not just a flat render; (b) motion tests where a pose
  needs to live inside Blender (compositor, camera, 2.5D depth);
  (c) any pose where the layer tree itself is the deliverable
  (e.g. a Harmony/Animate port — CapeGP layers map 1:1 to their layer stacks).
- **CapeGP is NOT used for:** final clean plates (outlines only),
  coloured/filled character art, or any approved pose replacement.

## Presets — each runnable, each with a proof frame
Built by `build_capegp_presets.py` (trace) + `build_capegp.py` (Blender).
`capegp_all_presets.blend` holds all six frames in one file for layer
inspection. **Proof renders are NOT from that file:** in a multi-frame GP
object, a layer with no keyframe at a frame HOLDS its previous frame, so
snap layers from earlier presets leaked into later preset renders (found
on viewing the first contact sheet: JOINT_SMOOTH showed held chest/face
layers). Proof renders `preset-0001.png … preset-0006.png` are therefore
rendered from single-preset blends (`single-NAME.blend`, built by
`render_single_presets.sh`), one frame each, no holdover. The all-presets
file stays in the pack for inspection only, with this warning on it.

| # | Preset | Pose config | Arm layers (L / R) | Proof |
|---|--------|-------------|--------------------|-------|
| 1 | NORMAL | APOSE, 0° | NormalArm / NormalArm | preset-0001.png |
| 2 | APOSE_FLEX | TRUE_FINAL flex, dip 28px | NormalArm / NormalArm | preset-0002.png |
| 3 | FACE_SNAP | JOJO03, head 8°, R face | NormalArm / FaceSnapArm (whole R chain above Head) | preset-0003.png |
| 4 | COWL_SNAP | TRUE_FINAL flex, dip 28px, both cowl | CowlUpperArm upper + NormalArm lower, both sides — **COWL IS UPPER-ONLY** | preset-0004.png |
| 5 | CHEST_SNAP | arms-forward-across-chest, both chest | ChestSnapArm whole chain, both sides, above Torso | preset-0005.png |
| 6 | JOINT_SMOOTH | TRUE_FINAL flex, dip 28px, Chaikin x2 on every stroke | NormalArm / NormalArm | preset-0006.png |

Layer counts (from `capegp_presets_frames.json`, verified by the builder):
NORMAL 19 strokes, APOSE_FLEX 19, FACE_SNAP 19 (FaceSnapArm 3 = R upper+lower+cap,
NormalArm 3 = L chain), COWL_SNAP 19 (CowlUpperArm 2 = both uppers,
NormalArm 4 = both lowers+caps), CHEST_SNAP 19 (ChestSnapArm 6 = both chains),
JOINT_SMOOTH 19 (same layers as APOSE_FLEX, smoothed points only).

## How to use CapeGP for a new character
1. Cut that character's pieces the same way (clean slices, ball-centre pivots).
2. Write that character's pose config the same shape as APOSE / TRUE_FINAL /
   JOJO03 in `build_capegp_presets.py` (arm_upper/arm_lower/leg_upper/leg_lower
   per side, plus a snap map per side: normal / face / cowl / chest).
3. Run the trace builder, then `build_capegp.py --preset YOUR_PRESET`.
4. Check the proof: layer order in the .blend, then the render, then the
   no-crop gate (below). Do not ship a character whose proof fails the gate.
5. Keep the layer tree identical (same 10 layer names, same order) so a
   preset, a Harmony port, and an Animate port all read the same stack.

## No-crop gate (standing rule, 2026-10-31 19:22 CDT)
Cape has a transparent background, so he needs NO crop window around him
or around any piece. Canvas fits the figure, never the figure fits the window.
Check, measured on the preset stroke data (Blender units, ortho frame
x ±8, y ±10.9 at 550×750, ortho_scale 16):
NORMAL x −2.29..2.28, y −5.56..4.97; APOSE_FLEX x −3.33..3.64, y −5.78..5.14;
FACE_SNAP x −2.69..2.28, y −5.55..5.06; COWL_SNAP same as APOSE_FLEX;
CHEST_SNAP x −2.90..3.25, y −5.56..4.97; JOINT_SMOOTH x −3.31..3.63, y −5.78..5.12.
**All 6/6 fit with margin — no preset clips the figure.** Rendered proofs
are also checked: no stroke alpha touches a canvas edge (see report).
Renders here use `film_transparent=True`, so the figure background is
transparent, not a grey box.

## Staging / prototype / test plan — HERE FIRST (Mars's order)
CapeGP is used often going forward, but ONLY after it passes testing here.
It is NOT pushed to any other repo yet, and it is NOT claimed as used in
other repos. Order:
1. **Staged here:** this folder — builders, frames JSON, all-presets .blend,
   six proof renders, this README, methods table, joint-smoothing doc,
   save-all list. Landing (separate workstream) may push this folder when
   it is ready; this task itself makes no repo push.
2. **Prototyped here:** the six presets above, plus the original motion
   (apose → mid → true-final → hold) from the depth package, which is
   listed in the save-all list and stays the motion proof.
3. **Tested here, must pass before any other repo use:**
   - T1 layer order: .blend layers are exactly the 10 names in order, and
     each preset's arm strokes sit in the layer its preset names (counts above).
   - T2 proof viewed: all six preset renders viewed by the builder, no
     missing limb, no stroke in the wrong colour layer.
   - T3 no-crop: stroke bbox fits the ortho frame with margin (above) and
     rendered alpha touches no canvas edge.
   - T4 pipeline rule: no CapeGP render is presented as an approved clean
     plate; PIL/v7c files are untouched (verified by the builder not writing
     outside this folder, and by the original depth folder being unmodified).
   - T5 new-character dry run: one other character's pieces traced through
     the same builder with the same layer tree, proof viewed, before CapeGP
     is called a multi-character tool (T5 is still owed — see report).
4. **Only after T1–T4 pass (and T5 for multi-character claims)** may CapeGP
   be staged into another 2D-animation repo, with this README carried over
   unchanged, name unchanged.

## Still owed (not claimed here)
- GP colour fills, interior linework, line-weight-by-depth (next GP passes).
- T5 new-character dry run (above).
- CapeGP use in any other repo (after testing here first).
- Per-shot CapeGP layer proofs (0/30 shots) and long GP sequences (free GPU route).
- Approval of this preset pack: 0/1.
