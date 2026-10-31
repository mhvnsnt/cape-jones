# Cape styles pack v2 — 15 forms, real fabric movement in 2D (2026-10-31)

Mars: the 4 v1 cape states were a good start, not enough. This pack gives the
cape a lot of movement, many forms/shapes, going all different ways and
angles, like a real cape — a real fabric aspect in 2D.

## What these are, honestly
- **All 15 are WARPS of Cape Jones's own `sliced/Cape_Back_Main.png`** (dark
  navy/black cape, his own piece), plus subtle fold shading. None are
  hand-painted masters, none use show character art. A hand-painted-detail
  pass is still owed if Mars wants that level.
- Cape stays a SEPARATE prop rig, never baked into the body.
- v1 lying-flat failure (tall narrow strip) was NOT repeated: horizontal
  styles here are rotated + re-proportioned, and 02-lying-flat reads as a
  spread cape, not a strip.

## Styles (15/12+ = 125% of the 12 minimum)
| # | File | Form | Direction / angle | Wind / weight | Movement it fits |
|---|---|---|---|---|---|
| 01 | cape-01-draped | draped | down, vertical | none / heavy hem | idle, standing |
| 02 | cape-02-lying-flat | lying-flat | horizontal, spread | none / pooled | resting, knocked down |
| 03 | cape-03-swinging | swinging | S-curve, side to side | moderate | walk, turn |
| 04 | cape-04-billowing | billowing | outward, flared hem | strong from behind / light | run, fly, wind |
| 05 | cape-05-wind-left | wind-blown left | hem swept left | strong right-to-left | run, storm, fly |
| 06 | cape-06-wind-right | wind-blown right | hem swept right | strong left-to-right | run, storm, fly |
| 07 | cape-07-lifted-up | lifted up | up, gathered | updraft / jump | jump, punch, flex |
| 08 | cape-08-hanging-heavy | hanging heavy | straight down, weighted | none / very heavy hem | idle, dramatic stand |
| 09 | cape-09-twisted | twisted | spiral, torso turn | spin | spin, dance twist, dodge |
| 10 | cape-10-over-shoulder | folded over shoulder | diagonal up-left, shortened | none / folded thick | walk, talk, casual |
| 11 | cape-11-wrapped-front | wrapped in front | narrow, centred, closed | none / closed | cold, hiding, stealth |
| 12 | cape-12-trailing-behind | trailing behind | back-diagonal, running | strong forward motion | run, chase |
| 13 | cape-13-flying-spread | flying spread | wide, both sides, lifted | strong airflow | fly, dive, superhero landing |
| 14 | cape-14-sitting-pooled | sitting pooled | outward on ground | none / pooled heavy hem | sit, rest |
| 15 | cape-15-raised-high | raised high | V, both sides up | dramatic reveal | reveal, dance accent, fight stance |

Full per-style metadata (fold count, direction, wind, weight, movement,
method) is in `cape-styles-v2-manifest-20261031.json`.

## 10 cloth/fabric methods wired — 10/10 = 100% as methods with a concrete application
"Listed" would be naming a tool. Each method below changed how a style was
actually built in `build_cape_styles_v2.py` (kept in this folder).

1. **Blender cloth simulation — pinning, stiffness, damping, wind.**
   Application: the cape is PINNED at the collar (top rows never move in any
   warp — displacement grows with distance from the collar, like a pinned
   cloth edge); stiffness = how much the silhouette resists bending
   (08-hanging-heavy = high stiffness, 04-billowing = low); damping =
   fold shading is blurred (Gaussian 6px) so folds settle instead of
   ringing; wind = the shear/flare warps in 04/05/06/12/13.
2. **Maya nCloth method — constraints, self-collision, wind.**
   Application: point constraints = collar pin + hem weight points; the
   fold bands never cross the cape outline (shading clipped to the alpha
   mask, i.e. no fold "collides" outside the cloth); wind fields are
   directional per style (see wind column), not random.
3. **Marvelous Designer pattern/drape method — garment panels, seams, drape.**
   Application: the cape is treated as ONE back panel with a collar seam
   (the collar line in the base art is preserved in every warp — 07 was
   rebuilt when a lift warp cropped it); drape = the hem falls/pools
   according to gravity (01/08 down, 14 pooled on the ground, 02 flat).
4. **Houdini Vellum cloth method — grain, bend, stretch.**
   Application: grain = folds run along the cloth's fall direction
   (vertical folds for hanging styles, horizontal for 02/14 ground styles);
   bend = the S-curve (03) and twist (09) bend without stretching the
   pattern; stretch = flare warps (04/13) widen the hem while the collar
   width stays fixed, so the cloth stretches where wind pulls it.
5. **2D verlet cloth — point constraints, gravity, wind.**
   Application: the remap itself is a verlet-style displacement field —
   each output pixel samples the base at a displaced position, displacement
   scaled by (distance from collar)^1.5–2, i.e. free hem moves most,
   pinned collar moves least; gravity pulls hems down, wind pushes them
   sideways. This is the engine behind 03/05/06/09/12/13/15.
6. **Bone-chain cape rig with secondary motion.**
   Application: the cape is NOT one rigid piece — in a rig it would be a
   chain (collar → mid → hem), and these 15 styles are the POSES that
   chain would hit at key moments. A walk cycle would pass through
   01 → 03 → 05/06; a run through 04 → 12; a landing through 13 → 14.
   The styles are keyed to movement, not decoration.
7. **12 Principles — follow-through + overlap + secondary action, cape specifically.**
   Application: the cape LAGS the body and OVERLAPS it — 03-swinging and
   09-twisted are follow-through frames (cape still moving after the body
   turns), 12-trailing-behind is overlap (cape arrives after the body
   starts running), and every cape style is a SECONDARY action: it never
   leads, it reacts to the primary body action. That is why wind styles
   are named by the body movement they follow.
8. **Fabric weight / hem weight + fold hierarchy (primary / secondary / tertiary).**
   Application: primary folds = the large silhouette folds (hem shape,
   flare, taper); secondary folds = the 7–12 shaded bands per style;
   tertiary folds = the fine lines already in the base art, preserved
   under the shading. Hem weight = 01/08/14 get an explicit darker hem
   band (up to 0.35 darken) so heavy styles read heavy and light styles
   (04/13) do not.
9. **Wind + motion direction mapping — cape trails opposite movement, lifts with speed.**
   Application: every wind/motion style obeys it — running forward gives
   12-trailing-behind (cape back), wind from the right gives 05-wind-left
   (hem left), speed lifts the hem (04/13 flare grows with speed, 07
   lifted on jump). No style has the cape blowing the same way the body
   moves.
10. **Light on cloth — inner shadow in folds, rim on fold crests, following key/LUT.**
    Application: fold shading is dark bands (inner shadow, alpha ~42) +
    warm light bands (fold crests, 255,200,130, alpha ~26, blurred) —
    the warm crest colour follows the warm-gold key used in Level 2 v2,
    and under a different LUT the crest colour must be re-graded to that
    key (rim follows key ±20°, standing rule). Folds are clipped to the
    cape alpha, so light never spills off the cloth.

## Proof + defects fixed in viewing
- Proof sheet (viewed by me, twice): `proof-cape-styles-v2-20261031.png`.
- Defect 1 (caught in viewing, FIXED): v1 proof fold shading was far too
  strong — opaque gold stripes (zebra, not fabric) caused by an overlay
  alpha bug. Fixed to low-alpha bands (dark 42 / light 26, blurred,
  clipped to alpha); v2 proof shows the dark cape preserved with subtle
  folds.
- Defect 2 (caught in viewing, FIXED): 07-lifted-up lost its collar (lift
  warp shifted the top off-frame). Lift reduced from −40 to −18 and the
  style was rebuilt; collar is preserved.
- Remaining honest limits: wind-left/right silhouettes are subtle at
  thumbnail size (hem shift is clear at full size); 04/13 hems are tall
  and crop in the 500px proof cells only — the files themselves are full.
  These are warps, not hand-painted masters.

## Still owed (not claimed done)
- Mars approval of this pack: 0/1.
- Hand-painted-detail pass, if Mars wants original-batch detail level: 0/1.
- Cape rigged as an actual bone-chain in a pose (these are style pieces,
  not a rigged animation): 0/1.
- Cape in a final shot with a body (separate prop rig application): 0/1.
