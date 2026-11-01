# EXPERIMENTAL — Grease Pencil pipeline: when a pose goes through GP vs the PIL/v7c builder

Status: EXPERIMENTAL, wired and used for proofs in this folder, not yet the
default for approved poses. Mars approval of the GP rig: 0/1. Originals
untouched; every GP output is a new dated file.

## What the GP rig is
- Blender 5.2.3 LTS, file `cape-gp-rig-experimental-20261031.blend`.
- One GreasePencil object, `CapeGP`, 10 layers in this exact front-to-back
  order: FaceSnapArm, Head, CowlUpperArm, Neck, ChestSnapArm, Torso, Collar,
  NormalArm, Legs, CapeBack. Layer `use_lights=False` so stroke colours read
  flat, like the 2D art.
- One material per layer (colour-coded for proof: Head purple, FaceSnapArm
  orange-red, CowlUpperArm gold, ChestSnapArm cyan, Torso near-white, Collar
  near-black, NormalArm/Legs pale, CapeBack dark purple).
- Every stroke is the traced outline (cv2 largest external contour,
  approxPolyDP, max 140 points) of an existing v7c source piece, placed by
  the SAME joint/anchor/rotation math as `snap_figure.py`. No new art drawn.
- Frames in the .blend: 1 = apose, 2 = mid (50% to true-final), 3 = true-final
  flex (documented angles, dip 28px), 4 = true-final hold, 10 = JoJo 03
  face-snap (R arm in FaceSnapArm layer, above Head).
- Builders: `trace_gp_frames.py` (trace + place) and `build_gp_blend.py`
  (Blender build + render). Render: Eevee, ortho camera scale 16, 550x750,
  grey world, under xvfb-run (bare headless aborts on missing libEGL).

## When to use GP vs PIL/v7c — the rule from this pass
- PIL/v7c builder (`snap_figure.py` / `joint_locked_rig_v7c.py`): DEFAULT
  for approved poses, clean plates, and anything that must match an
  already-approved file pixel-for-pixel. It is the production path.
- Grease Pencil: USE for (a) layer-order proofs — a snap decision can be
  seen as a layer stack, not just as a flat render; (b) motion tests where
  a pose needs to live inside Blender (compositor, camera, 2.5D depth);
  (c) any future pose where the layer tree itself is the deliverable
  (e.g. a Harmony/Animate port — GP layers map 1:1 to their layer stacks).
- GP is NOT yet used for: final clean plates (strokes are outlines only),
  coloured/filled character art, or any approved pose replacement. The
  approved true-final file is untouched; the GP version is a proof-of-use
  beside it, not a replacement.

## Proof-of-use (this pass, viewed)
- GP motion: apose -> mid -> true-final -> hold, 4 frames, GIF + MP4
  (`gp-motion-experimental-20261031.gif/.mp4`).
- GP true-final vs original: before/after sheet
  (`gp-true-final-before-after-experimental-20261031.png`) — left is the
  approved coloured original, right is the GP outline version. The GP
  version reads as the same pose in outline form; it is NOT a colour match
  and is not claimed as one.
- GP JoJo 03 face-snap: frame 10 render
  (`gp-jojo03-face-snap-experimental-20261031.png`) — R arm strokes sit
  in FaceSnapArm, above the Head layer, per the face-snap rule.
- Push-ready package for the landing workstream (do NOT push from here):
  this whole folder, with the .blend, gp_frames.json, both builders, the
  motion GIF/MP4, and this doc. Landing verifies by size+SHA on main.

## Honest limits of this GP pass (stated, not hidden)
1. Strokes are OUTLINES ONLY. No fills, no interior linework, no skin/
   suit/cape colour fills. A filled GP character is the next pass.
2. Stroke radius is fixed (0.035 Blender units); line weight does not yet
   vary by layer or by distance (depth-by-line-weight is a later pass).
3. The cape outline is large because Cape_Back_Main's contour is the whole
   cape silhouette — it reads correctly, but it dominates the line drawing.
4. GP rendering on this VM is slow (Eevee under xvfb, ~60-90s per frame in
   the probe runs; the 5-frame job took several minutes). GPU (Kaggle/Colab)
   is the free route for longer GP sequences.
5. GP operator `gpencil_add` does NOT exist in Blender 5.2 — the rig is
   built by creating `bpy.data.grease_pencils` directly and
   `drawing.add_strokes([sizes])` with `points[].position` / `radius`.
   That API difference is recorded here so the next builder does not waste
   a run on the old operator name.
