# Preset doc (prepared, audit only) — ENVIRONMENTAL DEPTH AND LIGHTING

Prepared in Workstream C sweep 2026-10-31. This doc prepares the preset;
it does NOT re-render shafts, duplicate the separate 5+5 improvement agent,
or claim production readiness.

## Preset identity

- Name: ENVIRONMENTAL DEPTH AND LIGHTING
- Version: v2-base + v3-improvement-20261031
- Source: `shafts-volumetric-upgrade-20261031/` (v2 Cycles) +
  `shafts-environmental-depth-lighting-upgrade-20261031/` (v3 methods)
- Status: named preset exists. Approval as preset: see note below.
  **Production-ready: NO.**
- Axis note: this is a shafts / environmental lighting preset. It is NOT a
  shading preset and NOT a lighting level L0-L5. Shading != lighting.

## Approval note (exact)

- Preset JSON (`ENVIRONMENTAL-DEPTH-AND-LIGHTING-PRESET-20261031.json`):
  `status: preset_approved_1_of_1_as_preset_not_production_ready`,
  `improved_preset_approval: 0_of_1`.
- Reading adopted in this sweep (matching the sweep brief): approval 1/1
  **as a named preset only, NOT as production-ready**. The improved v3 set
  is 0/1. Do not present the v3 set as approved.

## What it is (in plain words)

Real volumetric light in Blender 5.2.3 Cycles on CPU: lights sit ABOVE Cape,
shine straight DOWN, pass through gaps between ceiling slats, and fall as
separate warm columns BEHIND him. Cape stands IN FRONT of the shafts.
Shafts never cover him. This replaces the G3 test (flat PIL rectangles
blur 0/1/3/6/8 drawn OVER the figure) — do NOT present the G3 sheet as
a volumetric result.

## Parameters (v2 base, measured)

- Canvas 1100x1500. Figure alpha bbox x222-879, y240-1282. No-crop PASS (edge alpha 0).
- Volume: Principled Volume density 0.28, anisotropy 0.7, colour (1.0,0.85,0.55).
- Lights: Sun down energy 4.0 colour (1.0,0.88,0.60) + 5 spots energy 6000
  colour (1.0,0.88,0.62), spot 28 deg, blend 0.5.
- Slats: 6, at z6.8. Gaps built: -3.0 / -1.5 / 0 / 1.5 / 3.0 (5 gaps).
- Dust: 50 motes radius 0.015 inside gap columns only (v1 radius 0.035 read as balls).
- Render: CPU Cycles, 32 samples, volume step 1.0, ~11 min for 1100x1500 v2.
- Shaft centre mean RGB (72.4,62.8,47.1) vs dark corner (22.9,20.4,18.8).
- Figure occlusion: shaft-over-opaque-figure max difference 0.0 (PASS by construction).

## v3 improvement parameters (from preset JSON, not re-run here)

- Slats narrower 0.35, thinner 0.15, wider volume, outer spots 12000,
  centre 8000, spot 32 deg, Sun 5.0, samples 24, Cycles denoising ON.
- I1 Cycles v3 re-render, I3 ground pools, I4 Blender Glare Fog Glow
  (Threshold 0.6, Strength 0.5, Size 6, Quality High; 5.2 API fix),
  I5 faster/cleaner (Cycles denoising + PIL Gaussian sigma 1.0 proxy on v2).
- X1 depth gradient (1.0 top to 0.55 bottom, cool shift 0.85/0.95/1.15),
  X2 flicker sweep (outer x1.35, centre x0.85), X3 dust streaks (120, seed 7),
  X4 caustic pools (noise sigma 4, blur 6), X5 edge softened (Gaussian sigma 3).

## Rules (must travel with the preset)

1. Shafts ALWAYS behind figure: shafts x (1 - figure_alpha), figure pasted
   on top at full opacity.
2. Base art never recoloured.
3. No-crop: canvas fits figure, edge alpha 0.
4. Do NOT claim 5 distinct columns unless a measured mid-height run = 5.
5. Do NOT claim a Blender Glare file unless it exists on disk.
6. Do NOT claim Eevee unless the Eevee render file exists.

## Audit defects (plain, as of this sweep — separate agent may supersede)

- v2: **3/5 columns clear at mid-height = 60%** (282-379, 494-604, 721-816;
  peak 54.8 vs valley 22.9). Top height only 1 column passes (slats block top).
  Outer 2 gaps too dim. Do NOT claim 5 shafts.
- v2: slats dominate top of frame (large black blocks); shafts fade/dim to bottom;
  no ground pools in v2 (floor removed, not fixed); Glare not completed in v2;
  Eevee not run in v2.
- Env audit: method composites present 9/10 — I1, I3, I4, I5, X1-X5 present;
  **I2 Eevee composite MISSING; no Eevee output file found on disk**,
  although Eevee scripts exist. Eevee remains NOT evidenced.
- Env audit: I3 pools now present as method + v3-pools composite (feet_y 1282,
  centres 165/330/550/770/935, blur 18, behind figure). I4 Glare file now exists
  (PNG + EXR). Those close the v2 file-existence defects only, not production readiness.
- Env audit: **v3 column measurement still fails 5-column separation:**
  runs [172-232], [298-800], [866-927] — middle run 502 px wide = centre merged,
  not 5 distinct columns. Peak 87.2 vs min 37.1. Do NOT claim v3 fixes separation.
- Per-shot shafts: 0/30. Preset existence is not per-shot production.

## How to get it back

- v2 shafts layer: `shafts-volumetric-upgrade-20261031/shafts-only-cycles-v2-20261031.png`
- v2 composite: `shafts-volumetric-upgrade-20261031/composite-shafts-behind-v2-20261031.png`
- v3 pools composite: `shafts-environmental-depth-lighting-upgrade-20261031/composite-environmental-depth-lighting-v3-pools-20261031.png`
- Method contacts: `shafts-environmental-depth-lighting-upgrade-20261031/final-contact-20261031.png`,
  `methods-contact-20261031.png`
- Preset JSON: `shafts-environmental-depth-lighting-upgrade-20261031/ENVIRONMENTAL-DEPTH-AND-LIGHTING-PRESET-20261031.json`
