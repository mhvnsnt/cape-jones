# Lighting + Shadows Research — how light works on a surface, and how shadows follow it
Mars ordered 2026-10-31 23:30 CDT, replying to the shadow before/after contact.
Shadow system status: LOOKING GOOD SO FAR, not full approval. This is an improvement, not a replacement.

## Layman's version — read this first
- Light has a direction, like a lamp on one side. The side facing the lamp is bright, the side turned away is dark, and the line between them is called the terminator.
- Light does not stop dead at the terminator in real life. It wraps around the edge a little, so the dark side is not pitch black right at the border. That is wrap lighting.
- A shiny surface (belt, gauntlet, eyes) throws a bright spot back at you — a specular highlight. Rougher surfaces spread that spot wide; smoother surfaces make it tight and bright.
- Thin parts let light through a little — think an ear or a cape edge backlit. The edge glows warm. That is subsurface / translucency.
- Light gets weaker as it travels away from the lamp. Near is brighter, far is dimmer. That is falloff — in physics, inverse-square: brightness ~ 1 / distance², artists soften it so it does not go black too fast.
- A scene is never lit by one lamp alone. The sky above gives a cool light, the ground below bounces a warm light back up. That split is hemisphere ambient: cool top, warm bottom.
- A shadow is not just a dark blob. Where a thing touches the ground, its shadow is hard and dark. Farther away from the thing, the shadow gets softer and lighter — because a real lamp has size, and light leaks around the edges. The fully dark centre is the umbra, the soft edge is the penumbra. Penumbra width grows with caster-to-ground distance and with lamp size. The sun in the sky is about 0.5 degrees across — that is why sun shadows are fairly sharp.
- A part of a body can shadow another part of the same body: an arm shadows the chest, a cape shadows the legs. That is self-cast shadow, and it must point the same way as the ground shadow, from the same lamp.
- If a shadow is projected toward a vanishing point, it stretches and narrows as it goes away — perspective shadow, not a straight shear.
- Two lamps make two shadows, one per lamp, in different colours/directions, overlapping darker where they cross. One lamp, one shadow, is the simple case; dual-light is the double case.
- Light coming through columns, slats, or leaves makes stripes: bright where light gets through, dark where it is blocked. That pattern must land on the ground AND on the figure in the same columns — dappled light.

## Technical version — real numbers
- Lambert diffuse: brightness = max(0, N·L). Wrap diffuse: (N·L + w) / (1 + w), w = 0.5 here. At N·L = 0 (terminator) Lambert = 0, wrap = 0.33 — light bleeds past 90 degrees. RenderMan-on-Film / Godot Lambert Wrap use the same idea: wrap end beyond 90 degrees softens the terminator, simulating an area light.
- Blinn-Phong specular: specular = (max(0, N·H))^m, H = halfway between light and view, m = shininess/exponent. Higher m = tighter highlight. Here, as a 2D-plate proxy (no true normal map exists for this plate, stated plainly): specular is placed on flat, light-coloured interior surfaces (white > 180, EDT > 0.35 — white-suit EDT max is only 0.56, the thickest figure part is the black cape at EDT 1.0, so a 0.7 threshold gave 0 px and was rejected in-run, not hidden).
- Subsurface: light enters, scatters, exits nearby and on the far side of thin parts. Proxy here: edge band EDT < 10 px on the away side (u < 0) gets a warm (255,90,40) bleed at 0.55. Honest limit: legs are thin, so much of a leg qualifies as "thin edge" — L3 reads strong on thin limbs, not just on a 1-px rim.
- Distance falloff: physical 1/d², artist-softened here to 1 / (1 + (d/900)²), normalised to gain 0.65–1.20 across the figure (near gain 1.001, far gain 0.705 measured).
- Hemisphere ambient: ambient = sky*(1-t) + ground*t, t = vertical position 0 top → 1 bottom, sky (160,200,255), ground (255,180,80), blended at 0.25. Measured top mean (148.4,144.0,159.2), bottom mean (155.4,140.8,124.5).
- Umbra / penumbra: umbra = fully blocked, penumbra = partially blocked. Penumbra width ∝ (caster-receiver distance) / (light angular size). PCSS (percentage-closer soft shadows) is the industry method: blocker search, then penumbra radius = (receiver depth − blocker depth) / blocker depth × light size, then a PCF kernel of that radius. Contact hardening = the same rule in words: hard near contact, soft far away.
- Self-cast: a caster mask shifted by the light vector, intersected with the receiver (the same figure), darkened only inside the figure. Here: side caster (arms/cape, y < 1000, x outside 400–700) shifted +40 px, intersected with torso/legs = 24,156 px. First attempt (whole figure shifted 20 px) darkened 336,091 px = 90% of the figure and was rejected, not delivered.
- Perspective shadow: per-pixel map x' = x + 0.35×(Gy − y), y' = Gy − 0.18×(Gy − y), closing + blur 8. Blurred shadow 94,437 px. This is a 2D projection proxy, not a ray-traced shadow map — stated, not claimed as a render.
- Dual-light shadows: two squashed casts, warm (46,32,14) at +60 px and cyan (20,80,110) at −60 px, blurred 10, overlapping band darker. Warm 65,589 px, cyan 64,152 px (blurred counts).
- Dappled: shaft columns [58,212],[267,418],[474,622],[679,832],[887,1041] — figure bright ×1.08 inside columns, dark ×0.78 between; ground shadow only in the y ≥ 1340 band, only between columns. First attempt painted stripes over the whole canvas background and was rejected, not delivered.

## Audit — what we already had, so the new 10 are provably new
Old lighting: 70 LUTs, rim = dilate(figure,6) − figure, cel bands 1.12/0.92/0.72, ink band recoloured 80% toward rim/shadow, interior sheen ≤14 px up to 38% rim, ground bounce 45% in bottom 28%, dual-light rim, shafts, Glare.
Old shadows I1–I5: I1 contact ellipse; I2 cast squash + shear; I3 AO interior band <12 px, 25%; I4 form cel gradient; I5 soft PCF blurred union.
Old shadows X1–X5: X1 shaft-column mask on a cast; X2 depth alpha fade 1.0→0.25; X3 warm colour-bleed variant of form; X4 flicker sway −6/0/+6; X5 pool-bright cast reduction 30%.
New 10 below are none of those: wrap is not cel bands; specular is not sheen; subsurface is not ink band; falloff is not a LUT gain; hemisphere is not ground bounce (hemisphere is a full top-to-bottom ambient split, bounce was bottom 28% only); self-cast is not AO (AO is an interior edge band, self-cast is one part shadowing another); contact hardening is not a single blurred union (it is three ellipses, sharp+dark near, soft+light far); perspective is not shear (it is a per-pixel vanishing-point map); dual-light double shadow is not dual-light rim (rim is on the figure edge, double shadow is two ground casts); dappled is not X1 (X1 masked a cast to columns, dappled modulates figure brightness AND ground band in the same columns).

## New methods, with parameters
LIGHTING — L1 Wrap diffuse w=0.5, lit-side gain 0.982, away-side gain 0.557. L2 Blinn-Phong proxy, spec >0.1 = 4,528 px. L3 Subsurface thin-edge, edge 175,406 px, bleed 82,334 px, (255,90,40) at 0.55. L4 Distance falloff, 1/(1+(d/900)²), near 1.001, far 0.705. L5 Hemisphere ambient, sky (160,200,255) → ground (255,180,80) at 0.25.
SHADOWS — S1 Self-cast, 24,156 px, 0.35 darken, side caster +40 px. S2 Contact hardening (PCSS proxy), three ellipses: (260×28, alpha 200, blur 4), (340×38, 150, 12), (430×50, 90, 24), ground 66,621 px. S3 Perspective, map above, blurred 94,437 px. S4 Dual-light double shadow, warm +60 / cyan −60, blur 10. S5 Dappled, columns above, figure ×1.08 / ×0.78, ground band y≥1340 only, 71,551 px.

## Gates
Ground: feet_y = 1400, Gy = 1400, diff 0, all ground methods, PASS. No-crop: figure bbox inside 1100×1500, PASS. Occlusion: ground layers are behind the figure, character layers darken RGB only inside the figure, figure alpha unchanged in every lighting method (373,846 px throughout), occlusion 0 by construction. Base plate: rig-apose-v7c-clean-transparent.png, 1100×1500, bbox 248,253,875,1294, shifted +106 for ground proofs so feet = 1400.

## Sources consulted (public, not repo-private)
- Wrap lighting / Lambert Wrap: Godot StandardMaterial3D docs, RenderMan-on-Film (Rob Bredow), GPU Gems 2 subsurface chapter (wrap as part of SSS).
- Blinn-Phong / subsurface: Blinn 1977, Torrance-Sparrow microfacet model, Hanrahan-Krueger SSS, standard shading surveys (Phong / Blinn-Phong / Cook-Torrance / Ward).
- Penumbra / PCSS / contact hardening: PlayCanvas shadow docs (PCF vs PCSS), Godot DirectionalLight angular distance (sun ~0.5°), DigiPen shadow-rendering thesis (umbra/penumbra, light size × distance).
- Inverse-square falloff, hemisphere ambient (sky/ground lights): standard physically-based lighting practice, as in the RenderMan ambient-occlusion sky/ground setup.
