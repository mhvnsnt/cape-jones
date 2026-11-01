# Environmental Depth and Lighting — Shafts Improvement Report 20261031

## Preset, formally saved
- **Name: ENVIRONMENTAL DEPTH AND LIGHTING**
- Base: shafts-volumetric-upgrade-20261031 v2 proof, Mars approval 1/1 AS PRESET (not production-ready), 2026-10-31 20:35 CDT.
- Preset file: ENVIRONMENTAL-DEPTH-AND-LIGHTING-PRESET-20261031.json (in this folder).
- Rules that stay: shafts ALWAYS behind figure (shafts × (1 − figure_alpha), figure pasted on top); base art never recoloured; no-crop, edge alpha 0; do NOT claim 5 distinct columns unless measured mid-height runs = 5; do NOT claim a Blender Glare file unless it exists; do NOT claim Eevee unless the Eevee render file exists.

## Base v2, restated (not re-claimed as new)
- Blender 5.2.3 Cycles CPU, lights ABOVE, straight DOWN through 6 ceiling slats, gaps −3.0/−1.5/0/1.5/3.0, Sun down + 5 spots, warm columns BEHIND Cape, Cape in front.
- Mid-height columns measured: x 282–379, 494–604, 721–816; peak mean 54.8 vs valley 22.9.
- Shaft centre mean RGB (72.4, 62.8, 47.1) vs dark corner (22.9, 20.4, 18.8).
- Figure occlusion PASS: shaft-over-opaque-figure max difference 0.0.
- Defects carried forward, not hidden: slats dominate top; only 3/5 gaps read clearly, outer 2 too dim, top height only 1 column passes; no ground pools (floor removed in v2); CPU 32 samples, ~11 min for 1100×1500; dust corrected v2 radius 0.015 / 50 motes; Glare attempted NOT completed in v2; Eevee method only NOT run in v2; AE CC Light Rays PROXY only; Natron Sun Beams mapping only.

## 5 industry-standard things — run vs mapping, labelled
- **I1 Cycles re-render v3 — RUN, Blender 5.2.3 Cycles CPU.** Narrower slats 0.35 (was 0.55), thinner 0.15 (was 0.25), wider volume x 6.0, outer spots 12000, centre 8000, spot 32° (was 28°), Sun 5.0, samples 24, Cycles denoising ON. Result, measured same v2 method (rows 500–700, midpoint threshold): runs [172–232], [298–800], [866–927] — outer columns now appear, but centre 3 merged into one wide run. Mean RGB (56.0, 49.0, 40.3). **Verdict: partial, NOT 5-column separation.**
- **I1b Cycles re-render v3b — RUN, Blender 5.2.3 Cycles CPU.** Back to original slat width 0.55 / thickness 0.25, volume x 5.0, camera −14, spots 20° (was 28°), outer spots 12000, inner 6000, samples 24, denoising ON. Result, same method: mid runs [313–377], [497–601], [723–781] (3, same as v2); top runs [319–365], [513–586], [734–780] (3); lower runs include edge artefacts [0–55], [1046–1099] plus 3 centre. Outer profile values: x126 = 27.5, x974 = 28.0, vs valley ~13–14 — outer columns are low shoulders (~2× valley) but below the midpoint threshold (39.4). Mean RGB (27.4, 24.8, 24.4). **Verdict: 5-column separation STILL NOT achieved by the v2 gate. Do not claim 5 columns.**
- **I2 Eevee volumetric — ATTEMPTED, NOT RUN, no file exists.** Engine name corrected: BLENDER_EEVEE in 5.2 (not BLENDER_EEVEE_NEXT). Full-res 1100×1500 under xvfb-run: timeout 180 s, no file. Half-res 550×750 under xvfb-run: timeout 280 s, no file. Reason: headless Eevee volumetrics stall without GPU/GL here (libEGL missing in plain background runs; xvfb-run gets further but never finishes a volumetric render in these timeouts). **Do NOT claim an Eevee render. Eevee remains owed, on a GPU/display route.**
- **I3 Ground light pools — RUN, PIL composite pass.** Warm ellipses at feet_y 1282 (figure feet), centres 165/330/550/770/935, radii 150/110/70, alpha 90/120/140, Gaussian blur 18, drawn BEHIND figure (figure pasted after), never over figure. Proof: methods/I3-ground-pools-composite-20261031.png and composite-environmental-depth-lighting-v3-pools-20261031.png / v3b-pools variant. **Verdict: pools delivered as a composite pass, aligned to feet. True in-scene floor pools (Blender floor plane receiving light) still owed.**
- **I4 Blender Glare Fog Glow — RUN, file NOW EXISTS (this was the v2 blocker, fixed).** 5.2 API fix found by probing: compositor group must be created via bpy.data.node_groups.new('Comp','CompositorNodeTree') and assigned to scene.compositing_node_group (scene.node_tree does not exist in 5.2; Composite node type does not exist); File Output in 5.2 uses .directory / .file_name and file_output_items.new('RGBA','Image') — NOT base_path / file_slots (those do not exist in 5.2). Headless background runs abort (exit 134, libEGL); xvfb-run succeeds. Parameters: Type Fog Glow, Quality High, Threshold 0.6, Strength 0.5, Size 6. Output: shafts-glare-blender.exr (26 MB, saved by Blender as EXR despite item format PNG request) + shafts-glare-blender-20261031.png (1.5 MB, converted via Blender image.save_render). Glare PNG mean RGB (23.1, 20.4, 19.1), max 186. Effect viewed: subtle — bright centre column glows, overall image close to v2 shafts; Fog Glow at threshold 0.6 does not create a dramatic halo. **Verdict: Glare file output BROKEN → FIXED, file exists. Dramatic glow is NOT claimed.**
- **I5 Faster / cleaner pass — RUN (two parts).** (a) Cycles denoising ON in v3/v3b renders. (b) PIL gaussian sigma 1.0 denoise proxy on v2 shafts (methods/I5-denoised-faster-composite-20261031.png). **Verdict: denoised proofs delivered; a timed faster-Cycles comparison (samples/time) is NOT claimed — v3/v3b render times were not cleanly timed under concurrent renders.**

## 5 experimental things — all RUN as PIL composites on v2/v3, viewed
- **X1 Depth gradient:** shaft brightness 1.0 top → 0.55 bottom, cool shift (0.85, 0.95, 1.15). Proof: methods/X1-depth-gradient-composite-20261031.png.
- **X2 Flicker sweep (one frame):** outer columns ×1.35, centre ×0.85. Proof: methods/X2-flicker-sweep-composite-20261031.png. NOT an animated flicker sequence.
- **X3 Dust streaks:** 120 vertical streaks inside columns, seed 7, blurred. Proof: methods/X3-dust-streaks-composite-20261031.png. Reads as gold vertical lines at the sides — experimental, not a natural dust look; labelled as such.
- **X4 Caustic pools:** noise-dappled pools (gaussian noise sigma 4) at feet, blur 6. Proof: methods/X4-caustic-pools-composite-20261031.png.
- **X5 Edge softened:** shafts gaussian sigma (3,3,0) then re-masked behind figure; measured runs unchanged [283–379], [494–604], [721–815]. Proof: methods/X5-edge-softened-composite-20261031.png.

## Improved final composites (all shafts masked behind figure, figure on top)
- composite-environmental-depth-lighting-v3-pools-20261031.png — v3 shafts + pools.
- composite-environmental-depth-lighting-v3b-pools-20261031.png — v3b shafts + pools.
- methods/I4-glare-composite-20261031.png — Blender Glare layer + figure.

## What is still NOT fixed, plainly
- 5-column separation: NOT achieved. v2 = 3 runs, v3 = 3 runs (centre merged), v3b = 3 runs (outer low shoulders only). Next attempt, if ordered, needs a different occluder/light design (e.g. separate volume per column, or outer spots aimed/angled, or a wider camera with the figure re-framed) — not another spot-energy tweak, which was tried twice.
- Ceiling slats still dominate the top in v3/v3b composites (large black blocks, viewed).
- Eevee render: 0 files, still owed on a GPU/display route.
- True in-scene ground pools (Blender floor receiving light): still owed; pools here are a composite pass.
- Per-shot shafts: 0/30. Full GPU volumetric sequence: not run.
- No-crop / occlusion for new composites: shafts masked by (1 − figure_alpha) by construction, figure pasted on top; edge-alpha gate was PASS on v2 base and the same construction was reused — a fresh numeric gate run on every new composite was NOT run, so do not quote a new gate PASS for them.

## Approval / landing
- Improved preset approval: **0/1**.
- No repo push made by this task; landing is a separate step.
- No existing file overwritten; no base art recoloured.

## Addendum — Eevee retry after engine-name fix
- After the report above, build_eevee.py was corrected (BLENDER_EEVEE_NEXT → BLENDER_EEVEE, the correct 5.2 engine name) and re-run full-res 1100×1500 under xvfb-run with a 180 s timeout.
- Result: EXIT 124 (timeout), no shafts-eevee-20261031.png file created. The script progressed past world/material setup (deprecation warnings only) but never finished a volumetric render.
- Verdict unchanged: Eevee ATTEMPTED, NOT RUN, 0 files. It remains owed on a GPU/display route, not a timeout tweak.
