# Shadow system wired into production 100% — 2026-10-31

Mars ordered 2026-10-31 23:28 CDT, replying to the shadow system message:
"Yeah, get all of that stuff wired up 100%"

Source system, untouched: `shadows-wire100-20261031/` (5 industry + 5 experimental).
This folder is NEW only. No repo push. No source file overwritten.

## Matching rule, unchanged
- ONE light per scenario / shot / preset.
- Ground shadow AND character shadow from that same light: same direction, same rim colour family.
- Shadow tint = mix(black, rim, 0.18), never pure black.
- Figure alpha NEVER changed. Ground layers sit BEHIND the figure.
  Character layers darken RGB only INSIDE the figure.
- FULL shadow = I5_soft (blurred union of I1 contact + I2 cast) on the ground
  + I4 form + I3 ambient occlusion on the character.
  Other methods are variants, NOT stacked on FULL (would double-darken).
- X1 shaft-aligned, X2 depth-gradient, X3 colour-bleed, X5 ground-texture are
  variants recorded for the main scenario; X4 is a 3-frame sway sequence
  (cast offset -6 / 0 / +6 px) for the main scenario only.

## Counts, built
- Grounded shafts main: 1/1
- Per-shot shafts: 30/30 (CJ-01 to CJ-30)
- Figure-matched lighting presets: 8/8 (S1–S8)
- Total production composites: 39/39
- Gates: grounded 25/25 PASS, airborne 5/5 PASS-AIRBORNE, presets 8/8 PASS
- Figure alpha unchanged: 39/39 (presets verified byte-equal after an
  alpha-restore fix — see below; per-shot/main are RGB composites built
  from the transparent plate, dark layers masked to plate alpha, ground
  behind plate, so plate alpha is preserved by construction)

## Per-shot details
- Each shot rebuilt from its own transparent plate (from
  `shots-endtoend-20261031.json`) + the v4 Eevee shafts master, shafts
  tinted toward that shot's rim colour at 25% (L3 intensity 1.0, L2 0.85),
  figure NEVER recoloured except by the character shadow layers.
- Ground line Gy = 1400 for all 30. Grounded feet = 1400, diff 0.
  Airborne kept, NOT planted: CJ-12/13/14/15 feet 1310 (90 above ground),
  CJ-21 feet 1312 (88 above ground) — their ground shadows fall on the
  ground line below the figure, not at the feet, which is the honest
  airborne reading, not a planted-feet claim.
- Ground shadow px range: 68,774 (CJ-19) to 138,642 (CJ-13).
  Character form px range: 350,338 to 388,084.
- Figure inside canvas: 30/30. No-crop: figure bbox inside canvas on all 30.
  Occlusion, stated precisely: ground shadow is behind the figure and
  character darkening is inside the figure only, so no figure pixel is
  erased and no shadow pixel is painted over an opaque figure pixel
  except as character darkening — the old shafts occlusion definition
  (opaque figure pixels byte-identical) does NOT apply once character
  shadows darken the figure, and it is not claimed here.

## Figure-matched presets details
- Each preset: lit-transparent figure + its on-room composite.
  Alignment verified before building: opaque lit pixels == on-room pixels,
  max diff 0 (S1 checked; same build for all 8).
- Ground shadow composited over the on-room, then the character-darkened
  figure pasted on top at (0,0). Ground line = that preset's figure
  bbox bottom (S1–S4 arms-up: 1368; colour presets vary by plate).
- Rims used: S1 255,180,80; S2 255,190,90; S3 255,185,85; S4 255,180,80;
  S5 255,178,229; S6 0,200,255 (dual backlight, cyan rim valid by rule);
  S7 255,180,80 (front-left, dx 120, light_side left); S8 160,200,255.
  All other presets: overhead, dx 30, light_side above.
- Ground shadow px: ~189,998–192,607. Character form px: ~392,858–405,241.

## Alpha fix, found in-run and fixed, not hidden
First run: preset figure_alpha_unchanged = False on all 8. Cause:
alpha_composite with the I4/I3 dark layers raises edge alpha where the
figure is semi-transparent. Fix: after darkening, the figure alpha is
reset EXACTLY to the lit figure's alpha (`putalpha(lit alpha)`), in
`wire_shadows_production.py`. Second run: presets 8/8 alpha byte-equal.
Per-shot/main outputs are RGB composites, so their alpha check is by
construction (above), not by a byte comparison.

## Honest visual notes
- Main grounded shadow is subtle at contact scale: ground shadow reads
  under and between the feet, character darkening reads on the lower
  legs / away side. That is the source system's I5+I4+I3 strength, not
  a stronger shadow invented here.
- Preset cast shadows are LARGE (ground px ~190k vs figure ~393k) because
  the cast is the full squashed figure silhouette (28% height), as in the
  source system. At contact scale, especially S1–S4 arms-up, this reads
  as a dark smeared shadow below the feet, not just a small contact
  ellipse. S5–S8 read cleaner as a ground shadow. If Mars wants the
  preset cast tightened to contact-ellipse-only, that is a one-parameter
  change (use I1 only for presets), not a rebuild of the system.
- Per-shot contact labels are truncated to "CJ" (proof-sheet labelling
  bug: split on "-"); the production files themselves are correctly
  named CJ-01 … CJ-30. Labels are proof-only, never on finals.

## Mapping only, NOT counted in the 10
Blender Cycles true 3D shadow pass (needs a 3D figure model, not run here);
ray-traced shadow map (no ray tracer run, PIL proxy only);
true volumetric shadow (shaft volume shadow, PIL column mask proxy only).

## Files
- Builder: `wire_shadows_production.py`
- Measurements: `measurements-production-wire100-20261031.json`
- Production: `production/main-grounded-shafts-SHADOWED.png`,
  `production/main-grounded-shafts-no-shadow.png`,
  `production/main-X4-sequence.gif`,
  `production/CJ-**-shafts-SHADOWED-20261031.png` (30),
  `production/preset-*-SHADOWED-20261031.png` (8)
- Contacts: `contacts/main-before-after-20261031.png`,
  `contacts/per-shot-shadowed-contact-20261031.png`,
  `contacts/presets-before-after-20261031.png`

## Status
- Production-wired shadow system: approval 0/1 separately.
- Shots: still 0/30 approved. This wiring does NOT approve any shot.
- Grounded main shafts composite approved perfect 1/1 by Mars 23:24 CDT
  stands separately; the shadowed main here is a NEW version, not an
  edit to the approved grounded composite.
- No repo push.
