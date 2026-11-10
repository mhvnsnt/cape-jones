# Lighting Levels 0–5 — Mars wording + industry term, colored and non-colored

Mars's own system is Levels 0–3 (verbatim file: LIGHTING-LEVELS-VERBATIM-MARS-20261031.md).
This file does NOT replace that file. It extends it to 0–5 the way Mars asked on
2026-10-31 14:43 CDT: "go from like zero level zero to like a level five of lighting
and effects and have that one for color lighting and one for non-color lighting so
we'll have ten" — with his plain words beside the industry term for each level.

Counting, stated plainly so it is not fudged:
- Levels 1–5 × 2 types (colored + non-colored) = 10 graded levels.
- Level 0 is the single shared no-lighting reference. 10 + 1 = 11 chart rows.
- Counting Level 0 once per type gives 12 rows. Both counts are true; the chart
  below lists Level 0 once, shared, then 5 colored + 5 non-colored = 11 rows.

## The industry shape behind the labels

- Render passes / AOVs: a render is split into separate elements — beauty (the
  full image), diffuse, specular, reflection, shadow, ambient occlusion, mist/depth,
  volume, emission — so each can be tuned in compositing without re-rendering.
- Three-point lighting: key (main, shapes the form), fill (opposite, softer,
  controls how deep the shadows read), back/rim (behind, separates the subject
  from the background), plus bounce (indirect reflected light) and kick.
- Grading order: colour management first (ACES / Rec.709), then exposure +
  white balance, contrast, primary balance (lift/gamma/gain), secondary
  corrections (isolated colours, masks, keying/qualifiers), look/mood, then
  output transform and finishing. A LUT sits in that chain — conversion LUT
  before creative LUT, after primary correction — it is not the whole grade.

## Chart

### Level 0 — Plate / Raw / Beauty base — Mars: "no extra lighting at all"
Colored and non-colored: same. Base image only. No LUT, no rim, no shadow layer,
no bleed, no god rays, no glow. This is the reference, not a grade.

### Level 1 — Primary grade + Look LUT — Mars: "just LUTs / lighting change"
- Colored: approved LUT, spectrum LUT, or a mix of LUTs when Mars asks for a mix
  (ratio written in the shot spec). Colour only. No rim, no bleed, no shadow, no god rays.
- Non-colored: neutral grade only, gain 1,1,1, no hue shift. Looks the same as
  Level 0 on purpose — neutral is not a tint.

### Level 2 — Lighting passes — Mars: "shadows + outer rim + color bleed + color key bleed + color keying. NO god rays"
- Colored: Level 1 + key/fill/rim light passes, shadow pass + contact/AO,
  light wrap (= color bleed, edge band only, Screen, never whole-suit tint),
  secondary keying (isolated colour keys). Rim is outer-only, 2–4px, Add.
  God rays are NEVER in Level 2 — Mars corrected himself on this in the same
  message, and that correction stands.
- Non-colored: same layers, neutral/white values — neutral shadows, white rim,
  white light wrap, no hue. No god rays.

### Level 3 — Atmosphere / Volume passes — Mars: "god rays + rim + color bleed + a bunch of effects"
- Colored: Level 2 + god rays / volumetric shafts, mist/depth per plane, bloom/
  glare (Fog Glow), fog. This is where god rays first appear.
- Non-colored: Level 2 neutral + white god rays + neutral glow + fog.

### Level 4 — FX / Emission passes — NEW, above Mars's Level 3
- Colored: Level 3 + energy, sparks, beams, particles, specular highlights,
  wet-floor reflection, bounce/indirect diffuse — each as its own pass, so one
  effect can be turned up without re-rendering the shot.
- Non-colored: same passes in white/neutral — white energy/glow, white sparks,
  neutral reflection and bounce.

### Level 5 — Finishing / Master — NEW, the delivery pass
- Colored: Level 4 + secondary polish, grain, vignette, lens halation /
  chromatic fringe / depth of field, final output transform (Rec.709 gamma 2.4
  for delivery), delivery QC. Loudness target for audio on the same shot: -14 LUFS.
- Non-colored: same finishing, neutral — no hue is introduced at this stage.

## Rules that hold at every level
- Never recolour the base art. Light/shadow/bleed are separate layers on top.
- Rim is outer-only, 2–4px. No thick inner outline.
- Bleed is edge-band only, never whole-suit tint.
- A mix of LUTs is Level 1 only, only when Mars asks for a mix, ratio recorded.
- Approved 2026-10-31: base LUTs 30/30, spectrum sheet 4/4 LUTs 6/6
  (magenta-normal, magenta-deep, pink-normal, pink-deep, lime-normal, lime-deep),
  lighting demos colored + non-colored approved 2026-10-31 14:47 CDT.
  Spectrum sheets 1–3 (18/24) and spectrum v2 (16) are NOT approved yet.
