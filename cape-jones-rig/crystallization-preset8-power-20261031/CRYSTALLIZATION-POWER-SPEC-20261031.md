# CRYSTALLIZATION POWER — spec, 2026-10-31

**Name (Mars, 2026-10-31): CRYSTALLIZATION. Preset: VISUAL PRESET 8.**
**Status: pack approval 0/1. Name and preset number are Mars's. This is NOT
approved as a final shot, and it is NOT a story claim.**

## What the power IS, as ordered
The crystalline look itself, taken from the apose normal map's pink/cyan
faceted colours and shapes. When the power is ON, Cape looks like the
faceted crystal in P8-06 (facets + edges + glints) or P8-08 (with an
outside-only cyan rim). When it is OFF, he looks normal — the base plate,
unchanged. Turning it on/off is shown as a transition, not just a still:
feet-up sweep, 0% → 20% → 40% → 60% → 80% → 100% crystallised
(`frames/crystal-transition-*-pct.png`, GIF
`crystallization-power-transition-20261031.gif`).

## What is NOT claimed
- Hardness, sharpness, reflectivity, damage resistance, or any other
  story effect: Mars said the look "can be like" a power and named it
  Crystallization. Those effects are CANDIDATES ONLY, listed below,
  until Mars says more. Do not write them into a shot spec as canon.
- The source normal map is NOT a rendered crystal character. It is an
  estimated normal map (silhouette + linework). The preset reproduces
  its LOOK as facets; it does not claim a true 3D crystal render of Cape.
- Full facet variants lose face/eyes/muscle detail inside the silhouette
  (see preset JSON honest limit). P8-07 mix-base preserves detail and is
  the variant to use when the face must stay readable.

## Candidate effects (labelled candidates, NOT canon)
1. Crystal armour read — hard faceted surface, no damage claim.
2. Glint / sparkle on facet edges — visual only.
3. Refraction tint — 50% mix variant, visual only.
4. Rim-light power read — outside-only cyan rim, visual only.

## How to use it in a shot (template)
1. Start on the base plate (power OFF, 0%).
2. Run the feet-up sweep over 6 frames (or longer for a full shot;
   the 6-frame GIF is a proof, not a shot timing).
3. Hold at P8-06 (default) or P8-08 (rim version) for the powered beat.
4. Reverse the sweep to turn it OFF. Base art is never overwritten;
   the power is an overlay layer, removable at any point.

## Parameters
See `VISUAL-PRESET-8-20261031.json`: facet spacing default 48px
(coarse 80px, fine 28px), palette measured cyan-left (42,126,207),
pink-right (213,123,206), centre (128,136,219), vivid boost 1.6,
edge (20,20,40) 1px, glint white alpha 230 at left-facing facet
centroids, rim cyan (0,200,255) outside-only 6px.
