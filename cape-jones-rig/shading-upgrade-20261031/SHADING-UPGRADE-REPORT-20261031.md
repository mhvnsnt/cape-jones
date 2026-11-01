# G2 Shading Upgrade — Report, 2026-10-31
Approval: 0/1. No repo push. No existing file overwritten. Base art untouched.

## Mars was right, and why the old G2 looked the same
Old G2 `shade()` was a whole-canvas linear gradient centred on the canvas
(1100x1500), strength 0.5, multiplied inside the alpha only. The figure is
only 628 px wide (bbox x 248-875), so it saw only a small slice of that
gradient, and the white suit at 255 clipped the bright side. Result:
variants differed by ~10 R points at most, and the high-contrast variant
only crushed contrast — it did not shade a form. Reproduced here as
V1: half-mean delta -13.3, edge delta +0.5, visually almost identical
to the V0 control. That is the flaw, measured, not guessed.

## Two more honest corrections found while building this
1. **Normals from normalized depth do not work.** The first build here
   used depth normalized to 0..1; its gradient is ~0.02/px, so nx,ny were
   ~0.04 against nz=1 and the "Lambert" was nearly uniform darkening.
   The fix, used for all final variants: normals from the RAW distance
   transform in pixels (EDT changes ~1 px per px inward), Gaussian
   sigma 2, z-scale 1.5, then normalized. This is also why the old
   wrap-v4 relight (same normalized-depth math) was weaker than claimed.
2. **Half-mean left/right delta is the WRONG metric for pure form
   shading, and L02's +31.9 was not pure normal shading.** Every limb
   has a left edge and a right edge, and both halves of the figure
   contain both edges, so pure form shading cancels in the half-mean.
   L02's code multiplied by an explicit side weight (1.15 left of canvas
   centre, 0.85 right) — that side weight, not the normals, moved its
   half-mean to +31.9. Both metrics are therefore reported for every
   variant: half-mean delta (side-weight metric) AND edge delta
   (left-facing-pixel mean R minus right-facing-pixel mean R, normals
   nx < -0.3 vs nx > 0.3 — the true form-shading metric). A variant is
   NOT called real shading on half-mean alone.

## Method (all variants)
- Plate: rig-apose-v7c-clean-transparent.png, 1100x1500, figure bbox
  x 248-875, y 253-1294, centre x 561.5, mask 373,846 px.
- Depth: scipy EDT of alpha, minus interior dark-line creases
  (eroded mask, gray < 0.43, locally darker by > 0.12), Gaussian 3.
- Normals: raw EDT, Gaussian 2, (-dzdx*1.5, -dzdy*1.5, 1), normalized.
  ESTIMATED normals from silhouette + linework. No true 3D character
  model exists, so no variant here is a true 3D mesh normal pass.
- Shade range 0.35-1.00, never above 1.00, because the white suit
  cannot get brighter than 255 — brightening only clips.
- Light direction is stated per variant. KEY LEFT = light from the
  viewer's left, slightly above, vector (-0.80,-0.20,0.56).

## Measured results (R channel, figure-centre split)
| Variant | Light | Half-mean L / R | delta_R | Edge LF / RF | edge_delta_R | Verdict |
|---|---|---|---|---|---|---|
| V0 control | none | 133.5 / 137.0 | -3.4 | 133.4 / 131.6 | +1.8 | CONTROL, not shading |
| V1 old G2 gradient, reproduced | canvas gradient | 126.4 / 139.6 | -13.3 | 130.2 / 129.7 | +0.5 | FAIL as shading, proves old flaw |
| V2 Lambert LEFT strong | KEY LEFT | 87.0 / 83.2 | +3.8 | 121.6 / 47.7 | +73.9 | REAL form shading, FACETED on apose |
| V3 Lambert RIGHT strong | KEY RIGHT | 80.8 / 89.2 | -8.4 | 48.2 / 120.7 | -72.4 | Mirror of V2, FACETED |
| V4 Toon/cel LEFT 3-band | KEY LEFT | 90.3 / 87.0 | +3.3 | 127.8 / 52.2 | +75.6 | REAL cel shading, FACETED |
| V5 Three-point LEFT warm / RIGHT cool + rim | KEY LEFT warm, FILL RIGHT cool | 104.6 / 103.3 | +1.3 | 128.3 / 77.0 | +51.3 | REAL three-point, milder |
| V6 AO + Lambert LEFT | KEY LEFT, edges/creases dark | 71.7 / 68.2 | +3.5 | 101.1 / 39.4 | +61.8 | REAL AO + form, FACETED |
| V7 Form depth + figure-local side-weight LEFT | KEY LEFT | 96.7 / 79.4 | +17.4 | 107.4 / 67.3 | +40.1 | Side-weight moves half-mean, smoother |
| V8 Top light | KEY ABOVE | 77.1 / 78.9 | -1.8 | 73.7 / 74.8 | -1.1 | Correctly ~0 left/right: top light must not move it |
| V10 Combined normal + side-weight + AO LEFT | KEY LEFT | 87.2 / 69.5 | +17.7 | 92.9 / 63.3 | +29.6 | Combined, smoother than V2 |
| V9 Blender compositor LEFT | KEY LEFT | 92.8 / 92.7 | +0.1 | 104.1 / 76.5 | +27.6 | REAL Blender run, SMOOTH, weaker than PIL |
| HERO arms-up Lambert LEFT | KEY LEFT | 111.6 / 59.6 | +52.0 | 128.5 / 50.5 | +78.0 | Clean + strong on arms-up plate |

Controls: arms-up control (no shade) half-mean delta +0.2, edge -6.5,
so the hero's +52.0 half-mean is a +51.8 move from shading, not a
baseline asymmetry. Apose control half-mean -3.4, edge +1.8.

## Viewed verdict (contact sheet viewed by the builder)
- V2/V3/V4/V6 now look clearly different from V0/V1 — that part of
  Mars's complaint is fixed — BUT they carry visible faceting /
  mottling on the apose plate, the same faceting L02 warned about.
  Do NOT ship V2/V4 apose as a clean production relight.
- Cleanest usable variants: V9 Blender (smooth, +27.6 edge), V7/V10
  side-weighted (smoother, +17.4/+17.7 half-mean), and the HERO
  arms-up Lambert (clean, +52.0 half-mean, +78.0 edge). The method
  works cleanly on the arms-up plate; the apose faceting is a
  plate-specific problem (dense interior linework + narrow limbs),
  not a proof the method is wrong.
- V9 Blender note: first run used an sRGB normal map (edge +25.7);
  second run used Non-Color (edge +27.6). The remaining gap to PIL
  V2 (+73.9) is NOT fully isolated — likely Blender view-transform
  compression in the compositor output pipeline. V9 is reported at
  its measured +27.6, not claimed equal to PIL.

## Tools wired, honestly
- PIL/numpy/scipy relight: REAL RUN, script build_shading_upgrade.py,
  explicit light vectors, ambient 0.35, diffuse 0.65, AO, cel bands,
  three-point tints, side-weight — all measured above.
- Blender 5.2.3 compositor: REAL RUN, script
  blender_compositor_shading.py, .blend saved, xvfb-run required
  (bare headless aborts on missing libEGL — noted, not hidden).
  Node chain: Image (plate) + Image (normal map, Non-Color) ->
  SeparateColor -> Math MULTIPLY x2 / SUBTRACT 1 (to -1..1) ->
  Math MULTIPLY by light components -> ADD -> MAXIMUM 0 / MINIMUM 1
  -> MULTIPLY 0.65 -> ADD 0.35 -> per-channel Math MULTIPLY with
  plate -> CombineColor -> SetAlpha (plate alpha) -> output.
  Probed node names: MixRGB/Mix do NOT exist in 5.2.3 compositor
  groups; CombineColor does.
- Industry methods wired as real runs: directional Lambert form
  shading, toon/cel band shading, three-point key/fill/rim, ambient
  occlusion + crease darkening, depth/form shading, figure-local
  side-weighted wrap, normal-from-depth / shape-from-silhouette,
  Blender compositor N.L relight.
- Method mappings only, NOT separate runs, do not quote as runs:
  Blender Shader-to-RGB toon shader (represented by V4 cel bands),
  subsurface scattering (represented only by V5 rim/wrap tinting).

## No-crop check
All 11 apose variants + hero: size 1100x1500 unchanged, alpha mask
identical to base, pixels lost 0, edge alpha 0. Canvas fits the
figure; nothing was cropped. (No rotation was applied in this task,
so the check is mask identity, not a lean test.)

## Still owed
- True 3D character model normal pass: 0/1 (the real unblocker for
  clean, facet-free form shading on every plate).
- Clean apose production relight without faceting: 0/1 (V9/V7/V10
  are the closest, apose V2 is not clean).
- Per-shot shading: 0/30.
- Blender V9 vs PIL gap investigation (view-transform isolation):
  0/1.
- Subsurface scattering as a separate run: 0/1. Blender
  Shader-to-RGB toon shader as a separate run: 0/1.
