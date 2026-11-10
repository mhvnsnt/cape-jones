# Visual Preset 8 + Crystallization Power — report, 2026-10-31

**Folder:** `crystallization-preset8-power-20261031/`
**Approval: 0/1 for the preset + power pack. No repo push. No existing file
overwritten. Base plates untouched.**

## Source, stated plainly
Mars replied to the apose normal map
(`shading-upgrade-20261031/normal-map-apose-20261031.png`) — pink/cyan
faceted colours and shapes — and ordered it saved as Visual Preset 8 and
as his Crystallization Power. That map is NOT a rendered crystal
character: it is an estimated normal map from silhouette distance +
linework (raw EDT, sigma 2, z-scale 1.5, same as the shading upgrade).
This pack reproduces its LOOK as facets. It does not claim a true 3D
crystal render of Cape, and the power's name/number are Mars's, not a
final-shot approval.

## Measured palette (from the apose normal map, inside the figure mask)
- Cyan, left-facing mean (nx < -0.3, 147,083 px): (42, 126, 207)
- Pink, right-facing mean (nx > 0.3, 144,521 px): (213, 123, 206)
- Centre mean (|nx| <= 0.3, 82,242 px): (128, 136, 219)
- All-figure mean (373,846 px): (127, 127, 209)
- Vivid boost palette (saturation 1.6, labelled as a boost, not a
  measurement): cyan (0, 200, 255), pink (255, 110, 210),
  purple (140, 120, 255)

## What was built (real runs, PIL/numpy/scipy, builder `build_crystallization.py`)
- 8 variants × 2 plates (apose + arms-up), each as transparent PNG +
  grey-view copy: P8-01 faithful, P8-02 vivid, P8-03 coarse (80px),
  P8-04 fine (28px), P8-05 edges, P8-06 glints (default power-on look),
  P8-07 50% mix with base, P8-08 outside-only cyan rim.
- Facet counts, spacing 48px default: apose 308 facets, arms-up 308
  facets (same seed/grid over different bboxes); coarse apose 112,
  arms-up 126; fine apose 874, arms-up 912.
- Alpha: copied verbatim from each plate. Appose mask 373,846 px
  (alpha > 128). Arms-up alpha > 0 count 376,907 identical to the
  plate, including 7,222 feather pixels (0 < alpha <= 128). An early
  check reported arms-up alpha as not preserved — that was a check bug
  (mask threshold alpha > 128 = 369,685 px), not a loss; corrected in
  `measurements-20261031.json`.
- Power transition: 6 frames, feet-up sweep 0/20/40/60/80/100%,
  plus GIF `crystallization-power-transition-20261031.gif`.
- Contacts: `preset8-apose-contact-20261031.png`,
  `preset8-armsup-contact-20261031.png` (viewed by me).
- Blender reference: `blender-crystal-gem-reference-20261031.png` —
  REAL Blender 5.2.3 Cycles run (32 samples, xvfb-run, faceted
  icosphere, Principled glass-ish material, flat shading). It is a
  MATERIAL REFERENCE ONLY: a blue-grey gem, not Cape, not pink/cyan,
  not the power. Do not present it as Cape crystallised.

## Methods wired — 20 total, run vs mapping labelled
### Industry-standard, 10/10 RUN
1. Normal mapping — source map + per-plate EDT normals.
2. Voronoi facet generation — scipy cKDTree, jittered grid ±35%.
3. Low-poly / flat shading — one flat colour per facet.
4. Cel / flat facet shading — quantized flat facets.
5. Fresnel-style edge rim — outside-only, dilate-minus-mask, 6px.
6. Specular glint — white dots at left-facing facet centroids.
7. Refraction / glass tint — 50% facet + 50% base mix.
8. Edge outline — facet-boundary lines, (20,20,40), 1px.
9. Blender Cycles Principled glass — real gem render above.
10. Compositor overlay layering — preset as an overlay on a copy,
    base never recoloured permanently.

### Experimental, 6 RUN / 4 MAPPING
11. Crystal growth transition sweep — RUN, feet-up 0–100%.
12. Facet colour quantization to the measured palette — RUN.
13. Facet size ladder (coarse/fine) — RUN, 80/48/28px.
14. Glint sparkle (static dots) — RUN; animated sparkle NOT run.
15. Normal-direction palette mapping — RUN (left cyan / right pink).
16. Voronoi seed jitter variation — RUN, seed 7.
17. Depth-based facet darkening — MAPPING ONLY, not a separate run
    (facet colour is already normal-based).
18. Facet displacement / shard offset — MAPPING ONLY, not run.
19. Iridescence hue shift — MAPPING ONLY (vivid variant is a
    saturation boost, not a hue shift; labelled as such).
20. Power on/off transition frames — RUN, 6 frames.

Counts: 16/20 actually run, 4/20 mappings, labelled above. No vendor
tool is claimed to have run when it did not.

## Honest limits / still owed
- Full facet variants are SILHOUETTE crystals: face, eyes, muscle
  lines, and cape/body separation are lost inside the flat facet fill.
  P8-07 mix-base is the detail-preserving variant; use it when the
  face must stay readable.
- Arms-up facets read as a strong left-cyan / right-pink split — that
  is the normal-direction mapping, not a hand-painted crystal design.
- True 3D crystal model of Cape: 0/1 — no true 3D character model
  exists (same unblocker as the shading upgrade).
- Per-shot power application: 0/30. Animated glint sparkle: 0/1.
- Preset + power pack approval: 0/1. No repo push made.
