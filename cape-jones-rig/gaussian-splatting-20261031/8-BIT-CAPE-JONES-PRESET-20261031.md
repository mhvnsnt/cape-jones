# 8-BIT CAPE JONES PRESET — DEFAULT, DO NOT REPLACE

Mars order, 2026-10-31 20:17 CDT, replying to the Gaussian splat turn sequence GIF:
"Save that preset as 8 bit Cape Jones preset so anytime I ask for 8 bit Cape Jones
that's the version you give me."

## The version, exactly
- Look: dotted / point-splat Cape, front + turn -40 to +40 degrees and back.
- Files (source of truth, in gaussian-splatting-20261031/):
  - splat-turn-sequence-20261031.gif — 9 frames, -40 to +40 and back, THE preset visual
  - splat-contact-20261031.png — front, turn -35, turn +35, 2DGS flattened, mip
  - splat-front-20261031.png
  - splat-turn-minus35-20261031.png, splat-turn-plus35-20261031.png
- Source plate: rig-apose-v7c-clean-transparent.png (1100x1500), base art untouched.
- Builder: build_splats.py — CPU, PIL + numpy + scipy, no GPU.
- Parameters: 5,846 Gaussians, stride 8 over solid alpha, sigma 3.2, opacity 0.85,
  perspective focal 900, depth-sorted far-to-near alpha compositing.
- Depth: SYNTHETIC bulge proxy (distance-transform, max 81.9 px toward camera).
  NOT a true multi-view reconstruction, NOT a scanned back, NOT a measured depth map.
- Measurements: plate alpha 373,846 px, front splat alpha 250,408 px, IoU 0.647.
  The gap is stride 8 sampling holes. This is a splat-point proof, NOT a clean-plate
  replacement. Do not ship it as a clean plate.

## Honest label
Mars calls this "8 bit". The look is a Gaussian-splat point field, not a true
8-bit sprite / pixel-art conversion with a fixed palette and pixel grid. Call it
"8-bit Cape Jones preset (Gaussian splat point look)" when accuracy matters, and
give Mars THIS version whenever he asks for 8-bit Cape Jones, unless he asks for
a different, labelled version.

## Tool name — keep it as it is
- Tool: Gaussian Splatting, builder build_splats.py in gaussian-splatting-20261031/.
- Do NOT rename the tool to something else. Call it by its name: Gaussian Splatting.
- Upgraded versions are labelled DIFFERENTLY and organized DIFFERENTLY, in their
  own dated folders, never overwriting this preset. Example pattern:
  8BIT-V2-..., 8BIT-V3-..., each with its own report, parameters, and proofs.
- This preset file is V1, the default. Upgrades do NOT replace V1 unless Mars
  explicitly says a new version replaces it.

## Mars's reading of V1 (2026-10-31 20:19 CDT, replying to the turn sequence)
1. It looks like it is partially rotating three-quarters, then rotating back the
   other direction three-quarters, like in a 3D space. That matches the motion:
   -40 to +40 degrees and back, out-and-back, like the THREE-QUARTER PSEUDO TURN,
   not a full turn, not a true back view.
2. It almost looks like it is walking, almost taking steps towards the camera.
   That is a reading of the motion, not a walk cycle: the depth-bulge rotation
   shifts the legs and feet alternately as the set turns, which reads as steps
   toward the viewer. No true walk keys were used in V1, so never call V1 a walk
   cycle. A stepping-toward-camera variant, if built, is a separate labelled
   upgrade, measured against V1, not a relabel of V1.

## When Mars asks for 8-bit Cape Jones
1. Give him THIS version first (turn sequence GIF + front + contact).
2. Only then offer a labelled upgrade, if one exists, by its own version label.
3. Never invent a new 8-bit look on the spot and call it the preset.
