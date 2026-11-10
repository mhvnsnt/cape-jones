# GOD-RAY + LEVEL-3 BUILD REPORT (20261031)

## Correction applied (Mars, 16:30 CDT)
Realism = LIGHT, EFFECTS, and GOD RAYS only. NOT the background painting.
No painted background was repainted or altered here. The v2 file is a
volumetric LIGHT layer behind the unchanged arms-up plate; the plate itself
is untouched (detail, cowl, suit, cape all intact in both L3 outputs).

## God-ray v2 — measured, not claimed
- Engine: Blender 5.2.3 LTS, Cycles CPU (EEVEE aborts headless on this VM:
  exit 134, libEGL missing; Cycles CPU renders fine).
- Settings: Principled Volume density 0.35 (v1: 0.12), anisotropy 0.6,
  3 cyan spots Track-To camera: main 8000 + left/right 4000 each (v1: 800,
  guessed rotation), 5 thin occluder bars, 60 dust motes (emission spheres).
- Render: 550x750, 64 samples, ~13 min, then Lanczos-upscaled to 1100x1500
  for compositing (same method as v1, stated plainly).
- Pixel proof (550x750): v2 mean RGB (17.0, 69.7, 78.0) vs v1 (2.5, 27.2, 46.8);
  bright pixels >200: v2 10,645 vs v1 0; cyan-ish pixels: v2 85,867 vs v1 0
  under the same threshold (v1's bands were dark blue, below that threshold).
- Viewed: bright teal volumetric wash with a bright top-left shaft area,
  dark occluder bands, white dust dots. HONEST LIMIT: shaft separation is
  SOFT, not crisp distinct crepuscular rays — the volume reads as glow +
  bands, not hard-edged shafts. A sharper-shaft pass (narrower occluder gaps,
  higher anisotropy directionality, verified spot aim per shaft) is still
  owed if Mars wants crisp rays.

## L3 V4 + V5 — Blender compositor only
- Compositor: Blender 5.2.3, CPU compositor (GPU compositor also aborts
  headless: scene.render.compositor_device must be 'CPU'; Glare in 5.2 is
  socket-driven, not glare_type/threshold attributes — both fixed by probe).
- Layer order: god-ray light -> ground shadow -> cast shadow -> plate
  (untouched) -> bleed -> shaft spill on character -> rim inner -> rim
  outer -> Glare fog glow (threshold 0.75, size 6, strength 0.35).
- V4 L3: inner cyan (0-2px) / outer gold (2-5px), cyan bleed, cyan+gold
  spill on character. Viewed: detailed plate intact, gold outer line +
  cyan inner line visible on head, fists, feet, cape edge, bloom halo,
  ground + cast shadow to the right.
- V5 L3: gold-left / cyan-right split on inner + outer rims, gold+cyan
  bleed, cyan+gold spill. Viewed: split reads clearly, meeting at centre
  head and cape hem; bloom mixes pinkish at the centre seam (honest artifact
  of gold+cyan bloom overlapping, not hidden).
- First composite attempt FAILED and was fixed, not shipped: rim masks
  were dilated silhouettes (full figure) instead of true rings, so the
  first V4/V5 covered the whole figure in flat gold/cyan. Fixed by
  ring = dilate(outer) - dilate(inner); rerun viewed correct.
- PIL in this folder made helper masks/solids/proof-sheet assembly ONLY;
  the shots themselves were composited in Blender. The proof sheet is a
  PIL assembly of already-rendered shots, labelled as such.

## 10 methods wired — 10/10 with application
1. Density tuning — 0.12 -> 0.35, in v2 render.
2. Anisotropy — 0.6 forward scatter, in v2 render.
3. Spot aim verified — Track To camera, not guessed rotation.
4. Spot energy / multiple spots — 8000 + 4000 + 4000.
5. Occluder design — 5 thin bars, not walls.
6. Crepuscular structure — shafts + gaps + falloff (soft in v2, see limit).
7. Bloom / fog glow — Blender Glare node after composite.
8. Light bleed / spill — edge bleed + shaft spill clipped to plate alpha.
9. Shadow interaction — ground shadow + offset blurred cast shadow +
   spill on character, so light and shadow answer each other.
10. Haze + dust — dust motes in volume + dark world for contrast.
Plus colour-temperature contrast (warm gold front ~3200K vs cool cyan back
~7000K+) and motivated light (every rim/bleed/shaft names its source in
the spec). All methods only — no proprietary code, no cracking.

## Files
- godray-bg-v2-20261031.png (550x750, Cycles) + godray-bg-v2-1100x1500.png
- v4-level3-20261031.png + .blend, v5-level3-20261031.png + .blend
- proof-before-after-l3-20261031.png (viewed)
- LEVEL-3-SPEC-20261031.md, blender_godray_v2_cycles.py,
  blender_composite_l3.py, make_masks.py (+ corrected ring masks)

## Still owed — NOT claimed done
- Mars approval: 0/2 (V4 L3, V5 L3 built + viewed by agent only; Mars decides
  whether either reads as true L3).
- Crisp-shaft pass for v2 (see limit above): 0/1.
- Gold-rim-alone L3 (no cyan backlight) through this stack: 0/1 — V4/V5
  here are combined-case only, per the 15:48 dual-light correction.
- Per-shot L3 composites: 0/30. Repo push: parent's PR route, no commit here.
