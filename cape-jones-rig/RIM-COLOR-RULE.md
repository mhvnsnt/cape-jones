# Rim-colour rule — rim follows the key / LUT colour (Mars, 2026-10-31 15:02 CDT)

## The bug Mars caught
Level 2 v2 colored used a warm golden-hour grade but a cyan rim
(0,200,255). Cyan is hue ~190°, warm golden is hue ~30° — a different
colour family, so the rim read as a separate, wrong light. That is now
a bug, not a style choice.

## Industry rule
Three-point lighting: the back / rim light separates the subject, and
its colour temperature must match the key and fill for a balanced scene
— "make sure the color temperature matches your key and fill lights."
Standard guidance is also: ensure all lights have the same colour
temperature to avoid colour casts, and use gels to bring fixtures to
the same temperature. A rim is often warm (yellow/orange, ~3500K) when
the key is warm, not a fixed colour regardless of the scene.
Colour temperature in Kelvin: tungsten warm 2700–3200K looks orange,
daylight 5500–6500K looks blue-white. Warm light reads intimate/safe/
nostalgic/dangerous, cool reads alienation/cold — so a mismatched rim
also changes the mood, not just the outline.

## Rule, in one line
Rim colour = key / LUT colour family. When the colour changes, the rim
changes with it. Hue within ±20° of the key colour. Rim is the lighter,
brighter version of that family; bleed/halo is the darker, more
saturated version of the same family. Shadow colour is the only
contrast exception: it stays cool (fill side), it is not the rim.

## Locked values (2026-10-31)
- Colored, golden-hour: gain (1.10, 0.95, 0.70), rim (255,180,80)
  warm amber, bleed (255,120,0) orange, shadow cool blue-violet.
  File: showcase/lighting-level2-v2/level-2-v2-colored.png (rebuilt
  15:02 CDT, rim now warm, viewed).
- Non-colored, neutral: gain (1.0, 1.0, 1.0), rim (255,255,255)
  neutral white, bleed (255,255,255), shadow cool blue-violet.
- Future LUTs: rim hue = that LUT's hue. Example, from the approved
  LUTs: magenta-rose gain (1.25,0.70,0.90) -> rim in the magenta-rose
  family (255,178,229 range), never cyan, never a fixed colour.
  The exact rim for a new LUT is written into its shot spec before
  it is used, not guessed at render time.

## Power override — the ONLY exception
If a shot uses a specific power that calls for a specific rim colour,
that power's colour overrides the grade rim FOR THAT SHOT ONLY.
- The builder supports it: apply_lighting_level2_v2.py
  --power-rim R,G,B --power-name NAME
- The shot spec must record: power name, rim RGB, bleed RGB, LUT,
  and that it is an override. The output colour spec
  (showcase/lighting-level2-v2/level-2-v2-colors.json) has a
  power_override field for exactly this.
- An override never changes the default table above, and never
  carries over to the next shot. No power is named yet (0 named
  powers), so no override is active — do not invent one.

## Wiring
- apply_lighting_level2_v2.py: rim_col is set per grade (warm amber
  / neutral white), internal line light uses the same rim_col, so
  lines, rim, and bleed all move together when the grade changes.
- Every future lighting script must take rim from the grade / shot
  spec, never from a hardcoded fixed colour. A script with a fixed
  rim colour fails review.

## DUAL-LIGHT / TERTIARY LEVEL — correction to the above (Mars, 2026-10-31 15:13 CDT)
The cyan rim is NOT always a bug. It is a bug ONLY in a single-light
setup where the rim is supposed to match the one key.
TERTIARY LEVEL (third level of colour grading, after key and fill/bleed):
- Front light: warm gold, key, from in front of him. Grade gain
  (1.10, 0.95, 0.70), warm amber rim/bleed on the front-lit side.
- Back light: cool cyan (0,200,255), from behind him, radiating
  like god rays. This is a SECOND, named light source, not a
  mismatched rim. Its rays are a separate volume pass (Level 3
  atmosphere), and its rim is the back rim.
- GOD-RAY SETUP (Mars, 15:13 CDT): cyan rays radiating from behind
  him + different warm gold rays from in front of him. Demo proof:
  showcase/dual-light-cyan-back-godrays-warm-front-v2-20261031.png
  (cyan wedges 12 x 30°, blurred 18px, opacity 90/255, centre
  (560,802); warm gold diagonal beams opacity 70/255, blurred 25px,
  layered over the back rays, under the character). This PIL version
  is a DRAFT setup proof only — production god rays are Blender
  volumetric (separate back volume + front volume passes), not PIL
  wedges, per the VFX hand-tool stop.
- A dual-light shot spec MUST name both sources: front key (colour,
  temperature, direction), back source (colour, temperature,
  direction, ray type), and which rim belongs to which source.
  A shot that lists only one source and uses the other source's
  rim colour is still a mismatch — the difference is the record,
  not just the colour.
