# Lighting Levels — Mars, 2026-10-31 14:42 CDT (standing system)

User approved all 30 LUTs (see lut-approval-checklist.json, all APPROVED 2026-10-31).
Those 30 are the BASE. Expanded spectrum LUTs are added on top, they do not replace the approved base.

## Colored lighting levels
- Level 0 — NO extra lighting at all. Base image only. No LUT, no rim, no shadow layer,
  no bleed, no god rays, no glow. This is the reference, not a grade.
- Level 1 — LUT / lighting change ONLY. Approved LUT (or expanded spectrum LUT, or a mix
  of LUTs when Mars asks for a mix) applied as colour grade only. No rim, no bleed,
  no shadow layer, no god rays, no glow. This is what "just LUTs" / "just lighting change" means.
- Level 2 — LUT + shadows + outer rim lights + color bleed + color key bleed + color keying.
  NO god rays. This is the correction Mars made in the same message: level 2 will NOT have god rays.
  Layers, in order: LUT grade, hard shadow (hue-shifted, cool blue-violet, not black),
  contact shadow (darkest band at feet), outer rim 2-4px (environment colour, Add),
  color bleed (edge band only, Screen, low opacity, never whole-suit tint),
  color key bleed (key colour bleeding into rim/glow only, suit stays its key colour).
- Level 3 — Level 2 + god rays + full effects. Everything in Level 2, PLUS:
  god rays (painted shafts, Screen/Add ~20%, gradient falloff, dust/occlusion),
  energy glow / bloom (Glare Fog Glow), volumetric cones, fog per depth plane,
  foreground, final grade. This is the full stack.

## Non-colored lighting levels (parallel set, same structure, no colour tint)
- Level 0 — No extra lighting at all. Base only.
- Level 1 — Neutral grade ONLY. Daylight / neutral LUT (gain 1,1,1), no hue shift.
  No rim colour, no bleed colour.
- Level 2 — Neutral shadows + white outer rim + white bleed (light wrap, no hue).
  No god rays. Shadow is still hue-shifted cool, but rim/bleed are white/neutral, not coloured.
- Level 3 — Level 2 neutral + white god rays + neutral glow + fog.
  God rays are white/neutral, not coloured.

## How to ask for it (so there is no guessing)
- "LUTs" / "lighting change" alone = Level 1, colored, unless Mars says non-colored.
- "Level 2" = Level 2 above, colored unless Mars says non-colored.
- "Level 3" = Level 3 above, colored unless Mars says non-colored.
- "Level 0" = no extra lighting, for comparison.
- A mix of LUTs = Level 1 with two LUTs blended, only when Mars asks for a mix,
  and the mix ratio is recorded in the shot spec, never guessed.

## What is NOT in any level
- Never recolour the base art. All lighting is layers on top.
- Rim is outer-only, 2-4px. No thick inner outline.
- Bleed is edge-band only, never whole-suit tint.
- God rays are never in Level 0, 1, or 2. Only Level 3.
