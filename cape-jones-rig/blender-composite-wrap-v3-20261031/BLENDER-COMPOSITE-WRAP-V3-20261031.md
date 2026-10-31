# Blender composite wrap v3 — internal light + background upgrade (Mars, 2026-10-31 17:01 CDT)

## Scope change, logged plainly
v2 kept the background unchanged per Mars's 16:30 correction ("more realistic"
= light/effects/god rays, NOT the background). v3 is a NEW workstream where
Mars explicitly asked to upgrade the background too. That supersedes the
16:30 rule FOR THIS WORKSTREAM ONLY. v2 files are untouched.

## What Mars asked (17:01)
1. Upgrade the background itself, same scene/composition, gold grade retained,
   brighter cyan shafts if that helps, verified aim/density (here: painted
   shafts, not a re-rendered Cycles volume — see Honest limits).
2. Light must affect the COLOR ON HIM and put SHADOWS on him around his
   outlines — not just a colored band around his outline.
3. INNER outlines of HIM (not lighting outlines): pec shadows, clothing folds,
   suit creases, cape folds hit realistically — lit side of a fold brighter,
   shadow side darker, pecs shaded by light direction, not flat white suit
   with only an outer rim.
4. Pull open-source methods to get to that level.

## RIM LAYERING RULE — CORRECTED 17:05 CDT (standing, supersedes 17:02 reading)
Mars used "soft rim" and "soft halo" INTERCHANGEABLY — he thought they were
the SAME thing, not two different layers. His original intent was NOT a
three-layer stack.
- DEFAULT stack: HARD rim line (kept, v1 3px style) + ONE soft layer
  (soft rim = soft halo, same thing). Hard + soft together, or soft alone
  sometimes, or hard alone as control.
- Just because the soft rim was made does NOT mean the hard rim line from
  before is eliminated. Remember this in the compositor stack doc and in
  every future rim build.
- EXPERIMENTAL VARIANT ONLY: one test showing soft rim on top of a soft
  halo as two separate layers. Shown to Mars; HE will tell us if he wants
  that or not. Do NOT make it the default, do NOT present it as what he
  originally meant.
- Differentiation kept visible in v3: hard rim uses a BRIGHT near-white cyan
  (180,245,255), dilate 3, no blur, factor 0.90 — a sharp bright core;
  soft rim uses cyan (0,200,255), dilate 6, blur 5, factor 0.60 — a wider glow.
  Stack bottom->top: ground spill, HARD, SOFT, plate, inner wrap, shaft haze.
  Hard-only = thin sharp line. Soft-only = wider soft glow. Full = bright
  core inside soft glow. Experimental = widest (extra dilate 12 / blur 12 /
  factor 0.30 halo under the soft rim).

## Open-source methods pulled (methods only, no proprietary code copied)
- Blender 5.2.3 LTS compositor (open source): SetAlpha + AlphaOver stack,
  Dilate/Erode, Gaussian Blur, SeparateColor alpha, MixRGB gold grade.
  Output path verified in v1/v2 (NodeGroupOutput, real render + write_still).
- 2D relighting / intrinsic-image idea (public research): single-image
  relighting is underconstrained without normals — Neural LightRig (CVPR,
  normal+material estimation from multi-light diffusion), GeoRelight
  (joint geometry + relighting), PIXLRelight (intrinsic conditioning from a
  path-traced coarse reconstruction). v3 does NOT run those models; it uses
  their shared, implementable core idea: separate the plate into albedo
  (kept) + shading (recomputed from a light direction) and recombine.
- Shape-from-shading / fold-relief approximation (classical, open):
  interior linework in the art IS the fold/crease map. Lit side of a line =
  offset toward the light, shadow side = offset away from the light.
  That is what v3 does, in PIL, before compositing.
- What a true version needs: a normal/depth pass. Blender can render one
  from a 3D rebuild (Cycles normal/depth passes, as in Blender data-gen
  pipelines for relighting datasets). A flat 2D plate has no normals, so
  v3's interior shading is an APPROXIMATION, not a physically exact relight.

## How v3 is built
- Background (painted, new file bg-upgraded-v3b): deep teal-navy to warm
  gold-green gradient, gold glow behind the character, brighter cyan shafts
  from upper-left (painted beams, blurred), ground pool under feet, white
  dust specks, vignette. Flattened to opaque (v3 first attempt left dust
  specks semi-transparent, which rendered as black dots — fixed in v3b).
  Gold grade on background only (Multiply 1.0, 0.86, 0.64) retained from v2.
- Interior shading (PIL, on the plate BEFORE Blender): directional gradient
  across the figure bbox — cyan backlight strength up to 0.20 on the
  upper-left side, gold front-key up to 0.10 on the right, weighted by
  pixel lightness so dark cape stays shadowed; form gradient top brighter /
  bottom slightly darker; fold relief — interior dark lines (luminance <110,
  >4px inside the alpha edge) get a lit offset (-4,-3, brightened x1.18 +
  cyan) and a shadow offset (+4,+3, darkened x0.72 + cool). Pure black
  outlines are NOT recoloured. Base art is otherwise untouched.
- Fighting pose plate: the clean fighting file is opaque grey-128, so it
  was keyed out (grey-128 -> transparent) before shading. That key is a
  plate-prep step, not a change to the pose.
- Blender stack (blender_composite_wrap_v3.py, 6 renders, all viewed):
  spill (dilate 8 / blur 6 / 0.20, shifted down 12px), hard, [experimental
  halo only in exp], soft, plate, inner wrap (erode -8 / blur 3 / 0.35),
  shaft haze (blurred BG masked to soft band / 0.18). EGL warnings in the
  log are harmless (same as v1/v2); all renders completed.

## Files (new folder blender-composite-wrap-v3-20261031/, v2 untouched)
- wrap-v3-apose-20261031.png + .blend — DEFAULT hard+soft, apose
- wrap-v3-armsup-20261031.png + .blend — DEFAULT, approved arms-up base
  (arms-up / pre-flex only, NOT a flex)
- wrap-v3-fighting-20261031.png + .blend — DEFAULT, fighting pose
  (fists up at shoulders; verified by 3x crop — at thumbnail it can
  misread as apose, it is not)
- wrap-v3-apose-soft-only-20261031.png + .blend — soft alone (valid variant)
- wrap-v3-apose-hard-only-20261031.png + .blend — hard alone (control)
- wrap-v3-apose-exp-soft-on-halo-20261031.png + .blend — EXPERIMENTAL
  ONLY, soft rim on top of a soft halo; Mars decides, not the default
- proof-v2-vs-v3-wrap-20261031.png — v2 apose | v3 apose | v3 arms-up |
  v3 fighting
- proof-rim-variants-20261031.png — full | soft-only | hard-only | exp
  (cropped, enlarged)
- proof-interior-detail-20261031.png — v2 chest | v3 chest (enlarged)
- scratch/: bg-upgraded-v3b, shaded plates (apose/armsup/fighting),
  build_assets.py, solid-brightcyan

## Pixel proof (honest, limited)
- v3 apose vs v2 apose: 202,808 pixels differ at colour distance >20 —
  that number is dominated by the NEW BACKGROUND, not by rim/interior
  alone, so it is NOT quoted as a rim-only proof.
- Rim differentiation is proven visually in proof-rim-variants, not by
  that pixel count: hard-only is a thin bright line, soft-only a wider
  glow, full a bright core inside soft, experimental the widest halo.
- Interior: at 640x360 the character is ~234px wide, so fold relief is
  1-2px and reads subtly in the render; at full plate size (fighting
  shaded plate, viewed) pec/abs/fold relief is clear. A full-height
  render would show interior shading more strongly than this 640x360
  composite does.

## Honest limits / still approximated
- Interior shading is a 2D approximation from linework + gradients. It is
  NOT a true normal-based relight: fold direction is inferred from line
  position, not measured surface orientation; pec shading follows the
  art's own pec lines, not a 3D chest. A true version needs a normal/depth
  pass from a 3D rebuild — still owed, not faked here.
- Shafts are painted beams in the upgraded background, not a re-rendered
  Cycles volumetric pass. A brighter-shaft Cycles render remains a
  separate owed item if Mars wants volumetric shafts brighter.
- Side-weighted wrap (stronger on the backlit side) still needs a
  normal/depth pass or side mask — not in v3.
- Dust in shafts: white specks in the painted background, not true
  volumetric dust motes.
- Gold-rim-alone version through this stack: 0/1 (this is the combined
  cyan+gold case only).
- Per-shot composites through this stack: 0/30.
- Mars approval: 0/1 for v3 frames, and 0/1 for the experimental
  soft-on-halo variant specifically (he decides whether he wants it).
- No repo push made in this task.
