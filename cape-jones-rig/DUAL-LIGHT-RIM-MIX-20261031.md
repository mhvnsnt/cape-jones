# Dual-light rim-mix variants — see it in different ways (Mars, 2026-10-31)

## Rules this sheet obeys
- **15:48 correction:** cyan backlight god rays are for **cyan rim + gold LUT/overlay
  combined**, NOT for gold rim alone. Gold rim alone gets NO cyan backlight.
- **15:53 nuance (this task):** when cyan lights come from BEHIND him, the FRONT
  can also carry a MIX — gold rim lighting WITH cyan rim lighting AROUND the
  gold rim, layered. That is variant V3 below, and V5 is the same idea spread
  along the silhouette (gold front-facing edges, cyan back-facing edges).
- **Rim-colour rule:** rim follows the key/LUT hue family (±20°). A dual-light
  shot is the exception only because it NAMES both sources and which rim
  belongs to which — that naming is in the table below, per variant.
- Base pose for all 5: arms-up reference pose (FlexOut lowers, upper −70/70,
  lower 150/−150, legs −15/15), rebuilt transparent from
  `joint_locked_rig_v7c.py` geometry — `dual-light-variants-20261031/
  base-arms-up-transparent-20261031.png` (1100×1500, bbox x 222–879, y 240–1282).
  This pose is APPROVED as arms-up / pre-flex, NOT as a flex. True flex
  (fists rolled DOWN toward head/shoulders ~75°) is still owed.
- Colours: gold rim (255,180,80), gold bleed (255,120,0), cyan rim
  (0,200,255), cyan bleed (0,120,255), gold LUT gain (1.10,0.95,0.70).
  Background for all: dark (5,8,16). Rim technique (PIL): dilated-alpha rings
  — inner 0–2px, outer 2–5px — plus 5px bleed at 0.20 and a soft ground shadow.
  Base art is never recoloured; grade and rim are layers on top.

## Industry-standard dual-light methods used
1. **Three-point lighting** (key / fill / back-rim): the front key lights the
   face and chest; the back light separates the silhouette from the background
   as a rim. V1 uses only key + rim; V2/V5 add a true back light.
2. **Rim / backlight separation**: a back light placed behind and above the
   subject, aimed at the camera, draws the edge the key cannot reach. That is
   why cyan belongs on the back-facing edges in V5, not painted over the face.
3. **Edge-light layering (double rim)**: two rim passes at different widths —
   inner rim from the nearer/primary source, outer rim from the farther/
   secondary source. V3 (gold inner, cyan outer) and V4 (reverse) are this
   method made visible, so Mars can pick the order.
4. **Colour-temperature contrast (warm vs cool)**: warm key (~3200K gold) in
   front against a cool back light (~7000K+ cyan) reads as depth, not as two
   unrelated colours. The pair must stay in that warm-front / cool-back
   relationship, or the shot reads as a hue mismatch (the old cyan-rim-under-
   warm-grade bug).
5. **Volumetric god rays (Blender volume scatter + spot + occluders)**: a
   real shaft is light scattered in a volume and broken by occluders
   (pillars / character), NOT a flat fan wedge. The PIL fans in V2/V5 are
   DRAFT placeholders for this method — see the defect note below.
6. **Motivated light / light motivated by a source in the world**: every rim
   in the table names its source and direction. A rim with no source is a
   sticker, not lighting, and is not shipped.

## Variant table (all viewed by Muse, 2026-10-31)

| # | File | Key (front) | Rim | Back light | God rays | Viewed verdict |
|---|------|-------------|-----|------------|----------|----------------|
| V1 | `dual-light-variants-20261031/v1-gold-rim-only-20261031.jpg` | Warm gold, front | Gold only, inner+outer | NONE (correct per 15:48) | None | Clean. Gold rim reads all round the silhouette, no cyan anywhere. This is the gold-rim-alone baseline. |
| V2 | `dual-light-variants-20261031/v2-cyan-rim-gold-lut-cyan-godrays-draft-20261031.jpg` | Warm gold (gold LUT gain) | Cyan only | Cyan spot behind, above | PIL fan DRAFT | Concept reads (cyan rim + gold-graded body + cyan behind), BUT the ray fan is a flat solid cone, too wide, covering the lower frame — not broken shafts. DRAFT only, must be replaced by the Blender volumetric version. |
| V3 | `dual-light-variants-20261031/v3-gold-inner-cyan-outer-20261031.jpg` | Warm gold, front | Gold INNER 0–2px, cyan OUTER 2–5px around it | Cyan behind (glow only, no rays) | None | **The 15:53 mix, visible.** Gold hugs the body, cyan sits around the gold, clearest on head, fists, feet, cape edge. This is the layered front mix Mars described. Look at this one first for the mix. |
| V4 | `dual-light-variants-20261031/v4-cyan-inner-gold-outer-20261031.jpg` | Warm gold, front | Cyan INNER, gold OUTER (reverse of V3) | Warm glow behind | None | Comparison only. Reads warmer and softer than V3; the cyan sits closer to the body and the gold reads as halo. Included so the order can be picked, not as a second default. |
| V5 | `dual-light-variants-20261031/v5-mixed-silhouette-gold-front-cyan-back-draft-20261031.jpg` | Warm gold, front-left | Gradient: gold on left/front-facing edges → cyan on right/back-facing edges | Cyan spot behind, above | PIL fan DRAFT | Gradient works on arms, legs and feet (gold left, cyan right); head mixes to a grey-cyan. Same flat-cone ray defect as V2 — DRAFT rays only. |

## Shot-spec fields per variant (copy into a shot spec to use one)
- V1: `{lut: golden-hour, key: warm-gold-front, rim: gold(255,180,80), bleed: gold(255,120,0), back: none, godrays: none}`
- V2: `{lut: golden-hour, key: warm-gold-front, rim: cyan(0,200,255), bleed: cyan(0,120,255), back: cyan-spot-behind-above, godrays: cyan-volumetric}`
- V3: `{lut: golden-hour, key: warm-gold-front, rim_inner: gold(255,180,80), rim_outer: cyan(0,200,255), bleed: gold(255,120,0), back: cyan-glow-behind, godrays: none}`
- V4: `{lut: golden-hour, key: warm-gold-front, rim_inner: cyan(0,200,255), rim_outer: gold(255,180,80), bleed: cyan(0,120,255), back: warm-glow-behind, godrays: none}`
- V5: `{lut: golden-hour, key: warm-gold-front-left, rim: gradient-gold-to-cyan-by-facing, bleed: mixed, back: cyan-spot-behind-above, godrays: cyan-volumetric}`

## What is still owed (not claimed done)
- **Blender volumetric god-ray re-issues of V2 and V5 (0/2):** a Blender
  5.2.3 EEVEE render of a cyan volume-scatter background was attempted in
  this task; the first attempt failed on an engine enum (`BLENDER_EEVEE_NEXT`
  does not exist in 5.2.3 — correct name is `BLENDER_EEVEE`), the corrected
  render was still running when this doc was written. Until it lands and is
  viewed, V2/V5 rays stay labelled DRAFT. The flat fan is NOT production.
- **Mars approval of all 5 variants (0/5 approved):** built and viewed by
  Muse only. Mars picks the mix order (V3 vs V4) and the silhouette split (V5).
- **Production shot using the picked variant (0/1):** no final shot has been
  rendered with a picked variant yet. The separate Blender-compositor-fix
  workstream (Alpha Over background-mode failure) is the route to a true
  Blender composite; a PIL composite is never claimed as one.
- **True flex (0/1):** unchanged by this task — fists rolled DOWN toward
  head/shoulders ~75°, not outward, seam fix still owed.

## Builders
- `dual-light-variants-20261031/build_base.py` — transparent arms-up rebuild
- `dual-light-variants-20261031/build_variants.py` — the 5 PIL variants
- `dual-light-variants-20261031/blender_godrays.py` — Blender EEVEE volumetric
  background attempt (engine name corrected to BLENDER_EEVEE)

## ADDENDUM 2026-10-31 21:06 CDT — Blender-background re-issues landed
- Blender 5.2.3 EEVEE render completed (5 min, EGL warnings harmless, file
  saved `/tmp/godray-bg-20261031.png`, 399,391 bytes, 550×750 upscaled to
  1100×1500): volume-scatter cube + cyan spot + 3 dark pillar occluders.
  Viewed: dark blue vertical shaft bands, pillars breaking the light —
  NOT bright cyan rays (density 0.12 / spot energy 800 too weak for bright
  shafts), but a real Blender background, and far more realistic than the
  flat PIL fan cone.
- Re-issues, both viewed:
  - V2 Blender-bg: `dual-light-variants-20261031/v2-cyan-rim-gold-lut-blender-bg-20261031.jpg`
    — cyan rim pops against the dark shaft bands, character well separated.
  - V5 Blender-bg: `dual-light-variants-20261031/v5-mixed-silhouette-blender-bg-20261031.jpg`
    — gold-left / cyan-right gradient rim still reads over the shaft bands.
- Status change: Blender god-ray BACKGROUND is now 1/1 rendered and used
  (version 1, dark shafts). Bright cyan shafts (higher density / spot
  energy, verified spot aim) are still owed as version 2 — the current bg
  is honest version 1, not claimed as bright god rays.
- PIL fan drafts of V2/V5 are SUPERSEDED by these Blender-bg versions for
  presentation, but kept in the folder for comparison — do not delete.
