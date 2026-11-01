# PRESET + LEVEL NAMING CATALOG — plain words, what is different
Mars, 2026-10-31. Rule from Mars (17:14 CDT): packs and levels are
SEPARATE axes. A pack version number is never a level number.
Mars (18:03 CDT): gold-preserved V5 pinkish read is ACCEPTED — it looks
good, cool, fine. Do not keep chasing a perfect gold on V5. Same for
gold-preserved V4 above it — they look good. L4 candidate reads as a
DIFFERENT level — crazy, wild — and is treated as approved as L4.

## LEVELS — "go to level X in the lighting" (HOW MUCH lighting/effects)
- **Level 0 — "no light"**: plain plate, no LUT, no rim, no shadow,
  no rays. What you see: the character, flat, as drawn.
- **Level 1 — "LUT only"**: a LUT grade on the shot, nothing else.
  What you see: same character, colours shifted by the LUT family.
  No rim, no shadow, no rays.
- **Level 2 — "shadow + rim + bleed, no rays"**: shadows, outer rim,
  colour bleed and colour-key bleed. What you see: he has an outline
  glow and a shadow, but NO god rays, NO bloom, NO spill on his body.
  This is the "before" look in the L3 proof.
- **Level 3 — "rays + layered rim + full effects"** (the AFTER look):
  bright volumetric god rays, layered dual rim (cyan inner / gold
  outer, or the split), bleed, spill ON the character, ground + cast
  shadow, Glare bloom, haze, dust, gold-vs-cyan colour-temperature
  contrast. What you see vs L2: the room lights up, rays come down,
  his outline has TWO rim lines, light lands on him. God-ray v2 and
  L3 V4 live here. NOTE: in this pack the gold rim reads redder /
  pinker on screen (AgX view transform + semi-transparent split
  rings over cyan) — that read is beautiful and kept, and the
  gold-preserved version is kept alongside it. Mars picks per shot.
- **Level 4 — "beyond the after, crazy/wild"** (APPROVED as L4 by Mars,
  18:03 CDT): everything in L3, PLUS interior directional wash on his
  body, hard rim + soft halo kept distinct, colour-preserved rims
  (Standard view transform), foreground dust in front of him, and
  gentler controlled bloom. What you see vs L3: light is ON his body,
  not just around him; the rim has a sharp bright core inside a soft
  glow; dust floats in FRONT of him; the gold stays gold. This is
  the one Mars called crazy and wild — a different level at a glance.
- **Level 5 — "L4 + crisp + real direction + tracked"** (FIRST SHOT in
  godray-level5-20261031/): everything in L4, PLUS (1) crisp distinct
  shafts with hard edges, not soft glow + bands; (2) interior shading
  by estimated surface direction (dot of normal vs light, per pixel),
  so pecs and folds get a lit side and a shadow side that follow the
  light direction — not a flat wash; (3) side-weighted wrap — the glow
  is strongest on the backlit (left/cyan) side and fades toward the
  front (right/gold) side; (4) every colour tracked: input colour,
  on-screen colour, and mix cause, for every rim/bleed/shaft/spill;
  (5) the same stack reproduces on a second pose (apose frame) and
  re-renders pixel-identical. What you see vs L4: the shafts are
  sharp separate beams you can count; his chest and folds have real
  light-and-shadow sides; the glow hugs the backlit side harder.
  HONEST NOTE: the normal pass is ESTIMATED from the plate's own
  shading (shape-from-shading, per the L5 spec's "normal/depth pass
  or estimated normals") — it is direction-based per pixel, not a
  flat wash, but it is not a true 3D-rebuild normal pass. That
  distinction is stated, not hidden.

## PRESETS — "pull up lighting pack version X" (a SAVED STYLE/stack)
- **Lighting pack version five — "the before stack"**: the pre-L3,
  L2-looking stack. Flat rim rings, dark shaft bands (god-ray v1:
  density 0.12, spot 800, guessed aim), ground shadow only, no bloom,
  no spill on him, cream/gold LUT suit. Say it exactly: "pull up
  lighting pack version five". NEVER "lighting pack level five".
- **Lighting pack version six — "the after stack"**: the L3 stack.
  God-ray v2 (density 0.35, anisotropy 0.6, spots 8000+4000+4000,
  Track-To aim, 5 thin occluders, 60 dust motes), layer order
  bg → ground → cast → plate → bleed → spill → rim inner → rim
  outer → Glare fog glow (0.75/6/0.35), AgX default (which is why
  gold shifts in this pack). Say it exactly: "pull up lighting pack
  version six". Pack version six IS an L3 stack — it is not level 6.
- **Effects Sunbeam Preset v1 — "the spirit-bomb frame"**: the
  effects-v2 proof stack (Blender 5.2.3 Cycles, Glare Fog Glow +
  Sun Beams, volume density 0.02, anisotropy 0.5, warm haze, ground
  light pool, glowing aura orbs near the raised fists, dust in the
  air). Mars: really good light, really good sunbeams; reads like
  two double yellow spirit bombs — that goes hard. Saved as-is so
  it can always be gotten back to; upgrades get new versions.
- **Default Afterglow Preset — "the glow trail"** (APPROVED by Mars,
  17:49 CDT): soft rim (cyan, dilate 6, blur 5, 0.60) used as a MOTION
  trail only — lag 6 past positions, fade 0.50/0.40/0.30/0.20/0.12/
  0.06, decay 0.5/frame at rest, zero glow when standing still.
  Never a static halo: static looks ugly, like a shadow in the
  wrong place, like he is not standing on the ground.
- **Teleportation variant — "the idle glide"**: the same afterglow
  test, saved as its own variant, because it reads as standing idle
  AND moving at once — a teleportation thing. Really cool. Use it
  for teleportation, not as the default run/fly trail.
- **Base afterglow colour**: the default afterglow colour is his
  BASE afterglow colour. Running and flying afterglow, and different
  powers/variations, are built off this base later.

## GOLD vs RED/PINK — Mars's pick, settled for V5
- L3 V4 gold input (255,180,80) reads (204,162,114) on screen — cause:
  AgX view transform. Gold-preserved V4 reads (254,180,82).
- L3 V5 gold-left reads (185,156,154); gold-preserved V5 reads
  (216,161,159), still pinkish — cause: semi-transparent split ring
  (max alpha 0.627) over a cyan/teal environment + bloom overlap at
  the seam + AgX. Mars (18:03 CDT): that pinkish read is FINE, it
  looks good, cool. Accepted. No further chasing of perfect V5 gold.
- Rule stands for everything else: record input colour + on-screen
  colour + mix cause whenever they differ; "preserved" when within
  ~5/channel.
