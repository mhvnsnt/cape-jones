# Figure-matched room lighting — Cape Jones, 2026-10-31

Mars, 2026-10-31 22:08–22:09 CDT, replying to the shafts Environmental Depth
and Lighting final contact:
- "the lighting on him needs to change to match the rooms"
- "save those as four different separate presets" (shafts/lighting/god rays)
- "when he's in these different lighting scenarios, EVEN the colour lighting
  scenarios, the lighting must actually have an effect on him and on his body
  — on the wrinkles of his clothing, where you can see his muscles, and the
  lines — like how it is in comic books or really high quality TV shows,
  even the 2D ones. Pull in and wire up industry standard stuff for that 100%."

## Part 1 — FOUR separate shafts presets (NOT merged, NOT overwriting)

The existing Environmental Depth and Lighting preset is untouched. These four
are separate folders, each with its own spec JSON, its own room file and its
own composite file. Approval 0/1 for EACH preset separately.

| # | Preset | Room mean RGB | Source |
|---|--------|---------------|--------|
| 01 | SHAFTS V2 BASE | 28.9, 26.2, 25.3 | shafts-only-cycles-v2 + composite-shafts-behind-v2 |
| 02 | SHAFTS V3 CYCLES | 56.0, 49.0, 40.3 | shafts-only-cycles-v3 + I1-cycles-v3-composite |
| 03 | SHAFTS V3+POOLS IMPROVED FINAL | 71.7, 65.9, 60.7 | composite-environmental-depth-lighting-v3-pools |
| 04 | SHAFTS GLARE COMPOSITE | 23.1, 20.4, 19.1 | shafts-glare-blender + I4-glare-composite |

Full measured specs (lights, slats, columns, defects) are in each folder's
`PRESET-*.json`. Defects carried, not hidden: V2/V3 = only 3 columns read
clearly, NOT 5-column separation; V3+pools pools are a composite pass, not
true in-scene floor pools; Glare effect is subtle, not a dramatic halo;
Eevee render still 0 files; per-shot shafts 0/30.

## Part 2 — Figure-matched lighting, 8 scenarios

Base plate: shafts arms-up figure-only plate (1100×1500, figure bbox
222,240,879,1282, 374,366 alpha px). Base art is NEVER recoloured in place:
lighting lives on separate layers over a copy (tint, cel shading, shadow,
line-light, interior sheen, outer rim, bounce, glow). The clean base file
was only read, never written.

How the light lands ON HIM, not just the room — this is the whole point:
- **Outlines:** outer rim = dilate(figure,6) − figure, 34,446 px, rim colour
  = room key colour family (RIM-COLOR-RULE, hue ±20°; the ONLY exception is
  the dual-light cyan backlight, S6, which is a dual-light setup by rule).
- **Interior lines:** ink band = dark pixels within 3 px of a non-dark pixel,
  49,849 px. Thin pec, rib, ab, belt, gauntlet, cape-fold and cowl lines are
  all in this band, so they are recoloured toward the rim colour on the
  light side and toward the shadow colour on the away side — 80% blend, not
  a black line left untouched under a tint wash. Thick black cape interior
  is NOT in the band (it is not a line), so it does not get washed.
- **Muscles / clothing wrinkles:** this base plate's visible form lines are
  pecs, abs, belt, gauntlet segments and cape folds. There is no separate
  wrinkle piece in this plate; no wrinkle was invented. What is shown is
  those real lines carrying the light, per scenario.
- **Cel shading:** light factor is quantised into 3 bands (1.12 / 0.92 / 0.72)
  by direction — overhead = top bright, bottom shadowed; front = even;
  back = silhouette-edge bright. NOT a flat whole-figure tint wash.
- **Interior sheen:** inside-edge band (≤14 px from background) on the light
  side, following the form contour, at up to 38% rim colour.
- **Ground bounce:** S3 only, warm (255,180,80), rising to 45% in the bottom
  28% of figure height, from the pool rooms.
- **Glow:** S4 only, blurred rim proxy (PIL Gaussian 6, labelled proxy — the
  real Blender Glare file exists for the ROOM, not as a figure render).

| Scenario | Direction | Gain | Rim | Shadow | Lit mean RGB | Line-band mean light |
|----------|-----------|------|-----|--------|--------------|----------------------|
| S1 V2 warm overhead | overhead | 1.10,0.95,0.70 | 255,180,80 | 40,50,90 | 161.3,132.7,94.5 | 0.633 |
| S2 V3 warm overhead strong | overhead_centre | 1.15,0.98,0.72 | 255,190,90 | 40,50,90 | 169.8,140.0,99.9 | 0.652 |
| S3 V3+pools + bounce | overhead_centre | 1.12,0.96,0.71 | 255,185,85 | 42,52,92 | 171.7,140.1,98.2 | 0.652 |
| S4 Glare + glow | overhead | 1.10,0.95,0.70 | 255,180,80 | 40,50,90 | 156.9,128.8,91.4 | 0.633 |
| S5 Colour magenta-rose | front | 1.25,0.70,0.90 | 255,178,229 | 60,30,70 | 214.6,127.1,166.6 | 0.935 |
| S6 Colour cyan dual backlight | back | 0.90,1.05,1.15 | 0,200,255 | 20,40,70 | 94.9,149.5,175.5 | 0.744 |
| S7 Colour golden-hour front | front | 1.10,0.95,0.70 | 255,180,80 | 40,50,90 | 195.5,159.2,109.1 | 0.935 |
| S8 Colour cool-blue night | cool_front | 0.85,0.95,1.20 | 160,200,255 | 15,25,55 | 143.1,163.2,210.7 | 0.914 |

No-crop: every lit figure is on a padded 1260×1660 canvas (80 px pad),
padded edge alpha max = 0.0 on all 8. Rim/glow never touch the canvas edge.

## Industry-standard methods — run vs mapping, labelled

RUN (implemented in build_figure_matched_lighting.py, PIL/numpy/scipy):
1. Three-point lighting, rim follows key colour (RIM-COLOR-RULE).
2. Cel / toon shading bands (comic + 2D TV cel standard).
3. Comic-book ink lighting: line colour shifts with light, shadows in ink
   on the away side — the line is coloured, not left black under a wash.
4. Rim / backlight separation (dilate-mask rim).
5. Colour grading per light (per-channel gain = LUT-style grade; magenta
   gain 1.25,0.70,0.90 and golden gain 1.10,0.95,0.70 are documented values).
6. Bounce / fill from ground pools (S3).
7. Bloom / glow as a blurred-rim proxy (S4, labelled proxy).
8. Form shadow / ambient-occlusion-style edge and away-side darkening.

MAPPING ONLY (named, not claimed as run here):
9. Blender Cycles light passes / compositor relight of the figure — would
   need a 3D figure model; this figure is a 2D plate, so the relight here
   is the 2D form-gradient + cel implementation above, not a Cycles render.
10. Toon Boom Harmony / Animate shading and peg lighting — trials not
    confirmed, so mapping only, never claimed as a vendor file.
11. After Effects light / colour effects on the figure — proxy only.

## Honest limits, not hidden

- S1–S4 figure differences are SUBTLE, because all four shafts rooms are the
  same warm overhead light (different passes, not different colours). That
  is correct matching, not a failure — the strong differences are in the
  colour scenarios S5–S8, where the figure visibly turns pink / cyan /
  gold / blue, lines included.
- S4 lit mean is slightly LOWER than S1 (156.9 vs 161.3 red): the PIL glow
  blur premultiplies toward transparent black at the edge, so the glow
  darkens the edge band slightly instead of brightening the whole figure.
  The Glare room file itself is unaffected; the figure glow is edge-only.
- Colour rooms S5–S8 are NEW gradient test rooms built for this job
  (measured after building), NOT prior shafts renders. They are labelled
  colour scenarios, not claimed as old room files.
- No true 3D normal-map relight, no per-pose figure relight (this is the
  arms-up plate only), per-shot figure lighting 0/30, no animation
  sequence of the lighting changing over time (single frames per scenario).
- Contact labels on the torso-zoom sheet overlap the top of the tiles —
  labels are contact-only, not on the delivered figure files.

## Files

- Builder: build_figure_matched_lighting.py
- Report data: FIGURE-MATCHED-LIGHTING-REPORT-20261031.json
- Per-room contact: contact-per-room-20261031.png
- Torso zooms (pecs/ribs/clothing lines, all 8): contact-torso-zooms-20261031.png
- Layer proof S1 (base vs lit, torso + full): contact-layer-proof-S1-20261031.png
- Figures: figures/<scenario>-lit-transparent-20261031.png,
  figures/<scenario>-on-room-20261031.png, figures/<scenario>-on-grey-20261031.png
- Presets: presets/01-v2-base/, presets/02-v3-cycles/,
  presets/03-v3-pools/, presets/04-glare-composite/ (each: room + composite
  + PRESET-*.json)

## Status

- Figure-matched lighting set: approval 0/1.
- Four shafts presets: approval 0/1 EACH, separately.
- Environmental Depth and Lighting preset: untouched, approval stands separately.
- No repo push. No existing file overwritten. No base art recoloured.
