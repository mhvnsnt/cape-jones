# SHADING SET TWO — DEFINITELY WORKS

Label, exactly as Mars said it (2026-10-31 19:49 CDT): **DEFINITELY WORKS**.
Source: shading-upgrade-20261031/, V0-V10 + HERO arms-up, stats copied here as
shading-upgrade-stats-20261031.json. Original untouched.
Base: rig-apose-v7c-clean-transparent.png, 1100x1500, mask 373,846 px, centre x561.5.
Metrics: BOTH half-mean delta (side-weight metric) AND edge delta
(left-facing nx<-0.3 mean R minus right-facing nx>0.3 mean R, the true form metric).
Normals are ESTIMATED from silhouette distance + interior linework, not a true 3D mesh pass.
That unblocker is still owed and is stated, not hidden.

## Why this set works where Set One did not
Old G2 used a whole-canvas gradient centred on the canvas; the figure saw only a small
slice and the white suit clipped. Set Two computes shading PER PIXEL from an estimated
normal field (raw distance transform in pixels, EDT ~1 px/px, sigma 2, z-scale 1.5),
with a stated light vector and a shade range 0.35-1.00 (never above 1.00, because the
white suit cannot get brighter than 255). V1 in this set reproduces the old G2 flaw:
half-mean -13.3, edge +0.5, FAIL as shading.

## Cleanest usable variants (use these first)
- **V9 Blender compositor LEFT — SMOOTH, edge +27.6, half +0.1.** Real Blender 5.2.3
  compositor N.L run, Non-Color normal map. Gap to PIL V2 (+73.9) not fully isolated,
  likely view-transform compression; reported at measured +27.6, not claimed equal to PIL.
- **V7 form depth + side-weight LEFT — smoother, half +17.4, edge +40.1.**
- **V10 combined normal + side-weight + AO LEFT — smoother, half +17.7, edge +29.6.**
- **HERO arms-up Lambert LEFT — CLEAN + STRONG, half +52.0, edge +78.0.**
  Arms-up no-shade control was half +0.2, edge -6.5, so +52.0 is a +51.8 move from shading.

## Warning that stays inside Set Two (does NOT change the DEFINITELY WORKS label)
Apose V2/V4 (and V3/V6) are FACETED on the apose plate — dense interior linework +
narrow limbs — and do NOT ship as a clean production relight on apose. The method works;
the apose plate facets. Use V9/V7/V10 on apose, and Lambert on arms-up, for clean output.

## Full table (Set Two core)
| Variant | Left R | Right R | Half delta R | Left-facing R | Right-facing R | Edge delta R |
|---|---|---|---|---|---|---|
| V0-control-no-shade | 133.5 | 137.0 | -3.4 | 133.4 | 131.6 | +1.8 |
| V1-old-G2-gradient-reproduced | 126.4 | 139.6 | -13.3 | 130.2 | 129.7 | +0.5 |
| V2-lambert-LEFT-strong | 87.0 | 83.2 | +3.8 | 121.6 | 47.7 | +73.9 |
| V3-lambert-RIGHT-strong | 80.8 | 89.2 | -8.4 | 48.2 | 120.7 | -72.4 |
| V4-toon-cel-LEFT-3band | 90.3 | 87.0 | +3.3 | 127.8 | 52.2 | +75.6 |
| V5-three-point-LEFT-warm-RIGHT-cool | 104.6 | 103.3 | +1.3 | 128.3 | 77.0 | +51.3 |
| V6-AO-plus-lambert-LEFT | 71.7 | 68.2 | +3.5 | 101.1 | 39.4 | +61.8 |
| V7-form-depth-plus-sideweight-LEFT | 96.7 | 79.4 | +17.4 | 107.4 | 67.3 | +40.1 |
| V8-top-light | 77.1 | 78.9 | -1.8 | 73.7 | 74.8 | -1.1 |
| V10-combined-normal-sideweight-AO-LEFT | 87.2 | 69.5 | +17.7 | 92.9 | 63.3 | +29.6 |
| V9-blender-compositor-lambert-LEFT | 92.8 | 92.7 | +0.1 | 104.1 | 76.5 | +27.6 |

## Continuation wired into Set Two (this task, build_sets.py, 20 new variants + 2 arms-up checks)
All 20 new variants are PIL runs on the same Set Two normal field, in new-variants/,
stats in new-variants-stats-20261031.json, contact in
shading-set-two-continuation-contact-20261031.png. 10 industry-standard (N01-N10) +
10 experimental (X01-X10), plus 2 arms-up checks. X10 inverse is TEST ONLY, do NOT ship.
Faceting verdict, viewed: the new apose variants still show mottling/faceting on apose
(including the smoothed X01/X07), while the arms-up checks are clean — same plate
pattern as Set Two core. So smoothing helps the number (X01 edge +61.5, X07 edge +65.0,
vs V2 +73.9) but does NOT by itself make apose facet-free. Clean apose production
relight remains owed, via a true 3D normal pass, not by another PIL smoothing pass.

### Continuation table
| Variant | Left R | Right R | Half delta R | Edge delta R |
|---|---|---|---|---|
| N01-half-lambert-LEFT | 94.6 | 90.6 | +4.0 | +75.6 |
| N02-wrap-light-LEFT | 98.9 | 97.0 | +1.9 | +55.3 |
| N03-rim-only-LEFT | 106.5 | 106.2 | +0.3 | +43.9 |
| N04-cel-5band-LEFT | 90.5 | 86.3 | +4.2 | +81.9 |
| N05-sss-approx-LEFT | 94.1 | 91.7 | +2.4 | +47.7 |
| N06-gradient-mesh-LEFT | 114.6 | 94.3 | +20.3 | +4.9 |
| N07-specular-LEFT | 88.0 | 83.9 | +4.1 | +75.7 |
| N08-hemisphere-ambient | 102.5 | 102.1 | +0.4 | +37.5 |
| N09-cast-shadow-falloff | 84.7 | 80.8 | +3.9 | +71.9 |
| N10-shader-to-rgb-equiv-LEFT | 95.3 | 92.5 | +2.8 | +70.8 |
| X01-edge-aware-LEFT | 87.0 | 83.5 | +3.5 | +61.5 |
| X02-depth-dark-LEFT | 68.7 | 65.4 | +3.3 | +58.6 |
| X03-linework-aware-LEFT | 86.8 | 82.9 | +3.9 | +73.8 |
| X04-chromatic-wrap-LEFT | 93.6 | 90.0 | +3.6 | +73.9 |
| X05-dual-key-cross | 112.9 | 115.1 | -2.2 | +16.6 |
| X06-diagonal-light | 84.2 | 81.3 | +2.9 | +54.5 |
| X07-multiscale-smooth-LEFT | 87.0 | 83.4 | +3.6 | +65.0 |
| X08-per-zone-LEFT | 83.5 | 80.0 | +3.5 | +71.3 |
| X09-rim-AO-power | 79.4 | 76.2 | +3.2 | +63.1 |
| X10-inverse-TEST-ONLY | 92.3 | 100.9 | -8.6 | -72.0 |
| X01-edge-aware-ARMS | 111.4 | 60.0 | +51.4 | +75.3 |
| X07-multiscale-ARMS | 111.5 | 59.9 | +51.6 | +75.9 |

### What ran vs what is a mapping (continuation)
- RUN in PIL/numpy/scipy: all 20 new variants + 2 arms-up checks above, including
  Half-Lambert, wrap, rim, cel 5-band, SSS APPROXIMATION, gradient mesh, Blinn-Phong
  specular proxy, hemisphere ambient, cast-shadow falloff proxy, Shader-to-RGB
  EQUIVALENT, edge-aware smooth, depth-dark, linework-aware, chromatic wrap,
  dual-key cross, diagonal light, multiscale smooth, per-zone proxy, rim+AO combo,
  inverse test.
- NOT a separate run, labelled as such: true volumetric subsurface scattering
  (needs a 3D mesh; N05 is a PIL approximation only), Blender Shader-to-RGB node
  (N10 is a PIL ramp equivalent only), true limb segmentation for X08 (y-band proxy
  only), guided/bilateral filtering for X01 (gaussian-smooth proxy only).
- Blender compositor N.L itself was already a real run in Set Two core (V9), not
  re-run here; the continuation is PIL on the same normal field.

## Still owed (not claimed)
- True 3D character model normal pass: 0/1 — the real unblocker for clean, facet-free
  form shading on every plate.
- Clean apose production relight without faceting: 0/1 (V9/V7/V10 are closest).
- Per-shot shading: 0/30.
- Blender V9 vs PIL gap investigation (view-transform isolation): 0/1.
- True volumetric SSS as a separate run: 0/1. Blender Shader-to-RGB toon as a
  separate run: 0/1.
Approval: 0/1 for the sets + continuation. No repo push. No original overwritten.
