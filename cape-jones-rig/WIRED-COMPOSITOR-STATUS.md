# Wired compositor — status, 2026-10-31

This is a pipeline test, not a final shot, and not 100% overall.
Read the counts, not a headline percentage.

## What was built (no repo push, no merge, no deletions)
- `compositor-stack-spec.json` — stack order + 6 conditions.
- `apply_compositor.py` — runnable PIL stack, same order and layer names.
- `blender-compositor-stack.py` — Blender 5.2.3 LTS node builder.
- `compositor-stack-night-city.blend` — node tree, verified by reopening.
- `rig-apose-v6-transparent.png` — chroma-keyed apose (grey 128 -> alpha 0).
  Pipeline intermediate only. Red rig-label circles are still in it;
  they were NOT painted over, so composites are tests, not final shots.
- `showcase/composited-<condition>-20261031.jpg` — 6 outputs, all viewed
  in final form by the builder before this status was written.

## Honest counts
- Research sections wired as runnable PIL layers: 8/10 fully, 2/10 partial.
  - Fully wired (8): 1 colour keys, 2 rim, 3 bleed, 4 internal line lighting
    (PIL, masked to lit side), 5 node tools (Blender tree, see below),
    8 wet reflection, 9 fog per plane, 10 hard + contact shadow.
  - Partial (2): 6 LUT/ACES/delivery — .cube trilinear + sRGB JPG delivery
    ARE wired, ACES Input/Output transform is NOT (needs a colour-managed
    tool; not claimed). 7 god rays — gradient-shaft layer IS wired and its
    alpha was verified (250 at shaft centre), but in warm-interior it blends
    with existing window light and does not read as a distinct shaft;
    distinct per-shot shaft placement is still owed.
- Conditions in spec: 6/6.
- Conditions tested and viewed in final form: 6/6 = 100% of the spec.
  daylight (town bfSpz), night-city (skyline ywOUG), warm-interior (hall rzOMM),
  golden-hour (beach yFJdx), neon-alley-pink-cyan (night city giKK3),
  blue-warehouse (warehouse MvYdV).
- Conditions applied to actual shots: 0/30 = 0%.
  These 6 are apose pipeline tests, not clip frames. No punch/walk/jump/
  dance/flying/dialogue shot has been run through this stack yet.
- Final LUT approvals: 0/30. The .cube files used are templates, not finals.
- Blender node tree: VERIFIED as a file, NOT as a render.
  `compositor-stack-night-city.blend`, reopened: group
  CapeJonesCompositorStack, 18 nodes, 22 links, LUT_PATH text block present.
  No Blender render was produced or viewed, so no Blender render is claimed.
  Blender 5.2 API corrections found by probe (not guessed): Mix/Math are
  ShaderNodeMixRGB/ShaderNodeMath (CompositorNodeMixRGB/Math are undefined
  in 5.2), DilateErode Size is an INT (positive = dilate), Glare Type is
  the string 'Fog Glow', ColorBalance lift/gain are sockets (unused here;
  tint is a MixRGB MULTIPLY), Blur Size is a 2-item vector.
- Overall: NOT 100%. Stack code is complete for its order, but shots
  applied 0/30, LUT finals 0/30, and per-shot tuning (below) is still owed.

## Fixes made after viewing (not claimed as first-pass perfect)
1. First run: hard shadow was a full offset duplicate — read as a ghost
   on bright backgrounds. Replaced with a ground-flattened shadow
   (silhouette squashed to 25% height, laid at the feet).
2. First run: contact strip was a full-width bar — read as a black plank.
   Replaced with two blurred foot pads, 0.4 Multiply.
3. First run: bleed band rim+8 at 0.28 made the night-city halo too thick.
   Tightened to rim+5, night-city/warm-interior bleed to 0.20.
4. First run: daylight feet landed on the road. Floor fraction moved
   0.78 -> 0.73, feet now on the sidewalk in the final image.
5. Rim is outer-only, 2-4 px (daylight/night-city/warm/neon/blue 3 px,
   golden-hour 4 px), Add. Bleed is edge-band only, Screen, never a
   whole-suit tint. Base art was never recoloured; light/shadow/rim/bleed
   are separate layers over an untouched copy.

## Gated honestly (skipped, not faked)
- Wet reflection: applied 5/6, SKIPPED warm-interior (no wet floor
  established for that hall interior).
- God rays: applied 3/6 (warm-interior, golden-hour, blue-warehouse),
  SKIPPED daylight, night-city, neon-alley (no volumetric source
  established there). Golden-hour shafts ARE visible; warm-interior
  shafts blend with window light (see partial above).
- Energy core: NO fake gauntlet blast was drawn. Bloom/glow in this stack
  is only a blur of existing bright areas, Add, low opacity.
- Foreground: none in this test (no foreground plate was supplied).

## Still owed
- Run actual clip frames (not just apose) through the stack: 0/30 shots.
- Per-shot tuning: rim/bleed/shadow direction and opacity per shot,
  per-side internal-light masks in Blender (scalar there now),
  per-plane fog in Blender (PIL only now), per-shot god-ray placement.
- ACES transform in a colour-managed tool; final LUT approvals 0/30.
- A clean character plate without rig-label circles, for final shots
  (the apose source used here carries the labels by design).
- A viewed Blender render (node tree only is verified so far).

## Files NOT touched
No room layout files and no layout-pass-room files were modified in
this task. Backgrounds used were town, skyline, hall, beach, night city,
and warehouse — not the room background.
