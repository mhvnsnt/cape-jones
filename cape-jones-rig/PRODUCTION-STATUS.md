# PRODUCTION STATUS — Cape Jones, 2026-10-31, verified counts
Default lock: joint-locked v6. Main rig is on main in cape-jones-rig/.
Branch staged assets are on feature/character-parts-expansions-20261031, NOT on main yet.

## Branch inventory, checked by API + local SHA, 2026-10-31
- characters/sheets/ total: 251 files, 245 image files, 184 unique images = 75% unique, 35 duplicate groups
- fla-packs: 104 files (not 87 — 87 was the count before xray/angle packs landed)
- backgrounds: 38 files (37 jpg + README.md)
- props: 19 jpg files
- variations: 42 files (action 25, flying 13, references 2, root 2)
- model-sheets: 7 files, color-keys: 6 files, layout-line-art: 5 files, storyboards: 5 files,
  exposure-sheets: 10 files, viseme-charts: 2 files, prop-scale-sheets: 2 files, root sheets: 11 files
- Duplicate note, plain: file counts are NOT unique assets. Dance = JoJo = JoJo-2 (tripled),
  lounge = lounge-3quarter = backgrounds (tripled), several props = backgrounds.

## What's done, staged, and left — by production stage
Pre-production — STAGED on branch, 5/5 categories present:
  model sheets (7), color keys (6), layout line art (5), prop scale sheets (2), storyboards (5)
  Caveat: model sheets are staged sheets, not yet locked to v6 rig for all angles.
  Angles in rig: front full, profile head only = 2/5 = 40%. 3/4, side body, 3/4 back, back still to make as rig pieces.
Production — PARTLY:
  exposure sheets: 10 staged, additional variants (walk, dance, power pose, landing, wave) left
  layout passes: left (room, flying, rooftop, alley, desk scenes)
  clean-up pipeline: left (slice_clean.py is the cut tool, not a full clean-up/ink-and-paint pipeline)
  viseme charts: staged (2 charts + root matrix), sliced viseme pieces: 0/14, eye strips: 0/8
  effects design: partly (cape wind physics + FX on flying sheet, not a full effects set)
  shot specs: templates NOW built (shot-spec-templates.json, 8 shot types) — per-shot specs still to write per shot
  clips/timelines: 6 clips built and rendered (jump, punch, dance, flex, flying, walk) on v6 rig
Post-production — LEFT:
  compositing templates, grade LUTs, audio cues (1 cue sheet claimed elsewhere, not in sheets inventory),
  delivery specs (fps 24 and canvas 1100x1500 are rig defaults, not a delivery spec yet)

## System wiring — 2026-10-31
Fully wired: 5/7 = 71% (rig v6, clean cuts, pose library, timeline/clips, technique index)
Partly wired: 2/7 = 29% (JSFL timeline template, untested in Animate; shot spec + SHA manifest, QC pending)
With this package (manifest + shot templates + timeline examples + this status doc):
  pipeline pieces built: 4/4 = 100% of the non-image handoff package.
  Full TV production wiring: NOT 100% yet — the left items above are the remainder, counted here, not hidden.
