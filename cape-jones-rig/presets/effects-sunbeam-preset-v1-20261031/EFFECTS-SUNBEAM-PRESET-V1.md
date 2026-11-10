# EFFECTS SUNBEAM PRESET v1 — saved exactly, reproducible (Mars, 2026-10-31 17:47 CDT)

Mars's verdict on the effects v2 proof frame: really good light, really good
sunbeams, really good. The arms-up frame reads like he is about to do two
double yellow spirit bombs — energy orbs at raised fists. That read is an
energy-orb read only: NOT a Dragon Ball character, no Dragon Ball asset,
no branding shipped.

## Preset identity

- Name: **Effects Sunbeam Preset v1**
- Sits in the preset system alongside Lighting Pack Version 5 (V4/V5
  BEFORE stack) and Lighting Pack Version 6 (V4/V5 AFTER stack). Presets
  are a separate axis from lighting Levels 0-3 (and 4, 5 as upgraded).
  Mars can say "pull up Effects Sunbeam Preset v1" and this stack is
  what comes back.
- Source frame: `showcase/effects-v2-proof-20261031/effects-v2-proof-blender-20261031.png`
  (640x480, sha256 9e22ff59f27986f570a1531abe4446b6b80c7bdb31a3aeea2ed594e38d8566f6)
- Source script, byte copy in this folder:
  `blender_effects_v2_proof.py` (sha256 be8f78353b8286e8c550123a822adc7b4d17b04dec5f7df12b272d60697982c0)
- Character plate copy in this folder: `arms-up-rgba-20261031.png`
  (arms-up reference pose, FlexOut lowers, upper -70/70, lower 150/-150,
  clean, labels=False, base art untouched, used as emissive billboard).
- Original proof file and original script are UNTOUCHED by this preset
  save. Re-running the copied script reproduces the preset frame.

## Exact parameters (v1, as built)

- Blender: 5.2.3 LTS, engine CYCLES, device CPU, compositor device CPU
  (headless VM: GPU/EGL aborts, so CPU is the reproducible path).
- Render: 640x480, 100%, 32 samples, use_denoising False,
  volume_bounces 2, PNG.
- World: Background colour (0.02, 0.015, 0.03), strength 0.6.
- Camera: location (0, -8.5, 0.5), rotation (90, 0, 0) degrees.
- Ground: plane size 30 at (0, 0, -3.2), Principled Base Color
  (0.10, 0.08, 0.07), Roughness 1.0, receives shadow + light pool.
- Character billboard: plane size 1, scale (2.2, 3.0, 1.0),
  rotation (90, 0, 0), Emission Strength 1.0, texture Alpha mixed
  through Transparent BSDF (no card rectangle), blend BLEND.
- System 1, volumetric god rays: Volume cube scale (8, 7, 5),
  Volume Principled Density 0.02, Anisotropy 0.5, Colour (1.0, 0.75, 0.45).
  Spot "GodRaySpot" at (5.5, -2.0, 5.5), tracked to origin,
  energy 3000, colour (1.0, 0.70, 0.32), spot_size 55 deg, blend 0.4,
  use_shadow True, shadow_soft_size 0.5.
- System 2, aura bloom + spill: spheres radius 0.22 at (-0.9, 0, 1.3)
  and (0.9, 0, 1.3), Emission colour (1.0, 0.70, 0.30), Strength 8.0.
  Point "AuraPoint" at (0, -0.5, 1.3), energy 800, same colour,
  shadow_soft_size 0.8.
- System 3, dust: emitter cube size 8 at (0, 0, 1.0), 80 particles,
  lifetime 250, emit VOLUME, physics NO, instance icosphere radius
  0.02, Emission (1.0, 0.8, 0.5), Strength 2.0.
- Compositor (CPU, original Output reused — in Blender 5.2 a newly
  created Material Output is INACTIVE and renders black):
  Render Layers -> Glare Fog Glow (Threshold 0.8, Size 8, Strength 0.5)
  -> Mix ADD with original -> Glare Sun Beams (Threshold 0.8,
  Strength 0.4, Sun Position (0.78, 0.82)) -> Mix ADD
  -> Bright/Contrast (Bright 0.05, Contrast 0.10) -> Viewer.
  Glare nodes output ONLY the glow pass in 5.2, so the original must
  be added back or a chained stack goes black. Composite node is gone
  in 5.2; Mix is ShaderNodeMix (Factor inputs[0], A inputs[6],
  B inputs[7], Result outputs[2]). write_still=True writes the file;
  in-memory Render Result stays (0,0) headless.
- Grade: warm, rim follows key hue family +-20 deg.

## Known v1 defects (carried, not hidden — fixed in the upgrade, not here)

- Aura orbs sit slightly high/wide of the fists (snap owed).
- Visible Cycles noise at 32 samples (denoise / higher samples owed).
- Volume haze reads uniform rather than shaft-shaped (shaft masking owed).

## How to get it back

Run the copied script in this folder with Blender 5.2.3:
`blender -b --python blender_effects_v2_proof.py`
(change OUT/CHAR paths in the copy if the folder moves; parameters
above are the preset, not the paths).
