# X4 Correlated Flicker-Sway — Research (Mars, 2026-10-31 23:48 CDT)

## Mars's observation, in plain words
In the old X4 GIF you can see the shadow on the ground moving, but you do
not see any shadow moving ON him. If a shadow is moving for three frames
above him, there should be shadows on him that move at the same angle the
light is coming from, moving at the same angle as the frames of the shadow
moving beneath him. Mars is right: the old X4 moved only the ground cast.

## What the old code actually did (verified, not guessed)
`shadows-wire100-20261031/build_shadows.py`, X4 loop: for each offset
(-6, 0, +6) it recomputed `ground_layers(canvas, feet_y, rim, light_dx+off)`
but reused the SAME character layers `cl["I4_form"]` built once. So:
ground cast shear changed per frame; form gradient, AO, rim did not.
That is a single-parameter bug, not a rendering subtlety: two layers were
driven by two different light values (one moving, one frozen).

## What the light actually does — the physics in one paragraph
There is ONE light. Everything else is that light, seen in three places:
1. **Cast shadow** — the figure blocks the light; the blocked light lands
   on the ground, on the opposite side from the light, sheared by the
   light's angle. Light moves right -> cast moves right, and longer/shorter
   as the light gets lower/higher.
2. **Form shadow** — the figure's own surface turns away from the light.
   The line between lit side and dark side is the **terminator**. Light
   moves right -> the terminator moves right across the body, the lit
   side grows on the right, the dark side grows on the left. The terminator
   is not a painted stripe; it is where the surface normal stops facing
   the light (N·L = 0, Lambert). Wrap lighting softens it (N·L + w)/(1 + w),
   it does not freeze it.
3. **Self-cast shadow** — one part of the body (arm, cape) blocks the light
   from another part (torso, legs). It moves with the same light vector,
   projected onto the body, not onto the ground.
4. **Rim / edge light** — the edge facing AWAY from the camera toward the
   light catches a bright rim. Light moves -> the rim band moves to the
   newly lit edge.
5. **Ambient occlusion** — darkening where surfaces touch or crease. This
   one is mostly view/contact driven, NOT light-direction driven: an
   armpit stays dark when the light sways a few pixels. AO may breathe
   slightly with the away-side darkness, but it must NOT translate across
   the body — claiming AO moves like a cast shadow would be wrong.
   In this pipeline AO is kept static except a small away-side breath
   (X-C2), and that limit is stated, not hidden.

So the correlation rule, the thing Mars is asking for, is:
**one light parameter, one frame, drives cast + form terminator +
self-cast + rim together, same direction, same timing, same sign.**
If the ground centroid moves +X and the terminator moves -X, the shot
is broken, however good each layer looks alone. That is why this rebuild
has a CORRELATION GATE (see measurements): ground centroid and form
terminator must both move monotonically, same sign, across the frames.
The old X4 FAILS that gate by construction (terminator delta = 0).

## Industry-standard methods wired here (all RUN)
- C1 Single-key-light parameter: one `light_dx` per frame, no independent
  ground/char light values. This is the three-point / key-light discipline
  from cinematography and CG lighting: the key light is one object in
  space, every shadow is its projection.
- C2 Form-shadow terminator tracking: terminator x = f(light azimuth).
  Here term_x = figure_centre + 2.0 * sway_offset, measured per frame at
  the half-max dark point (0.14), not eyeballed.
- C3 Self-cast shadow projection: caster mask shifted by the light
  vector (20 + 2*off px), intersected with the receiving body only.
- C4 Rim/edge-light side tracking: rim band masked to the lit side
  (x > term_x), so the rim band boundary moves with the light.
- C5 Shadow length/direction coupling: cast shear = light_dx * (y-Gy)/120,
  the same dx that moves the terminator, so cast length and form move
  together (cf. the sun-moving example: shadow direction and length are
  directly affected by the direction of the light source).

## Experimental methods wired here (all RUN)
- X-C1 Terminator-shifted cel gradient: 2 px of terminator travel per
  1 px of ground sway offset — visible at GIF scale without redrawing
  the figure.
- X-C2 Sway-phase AO breathing: away-side AO alpha scales with |off|;
  small, documented, AO does not translate.
- X-C3 Flicker-phase intensity: form dark max is held, but the lit-side
  rim alpha follows the sway phase so the bright edge breathes with
  the shadow (implemented via the rim mask boundary, not a global flash).
- X-C4 Correlation gate: a build gate that FAILS if ground centroid and
  terminator do not move the same sign. This gate would have caught the
  old X4 before delivery.
- X-C5 5-frame smoothstep sway: offsets -8/-4/0/+4/+8, same correlation,
  smoother than the 3-frame jump, for comparison.

## Mapping only (NOT claimed as runs)
- Blender Cycles true 3D shadow pass with a moving area light (would
  produce this correlation for free, but no Cycles render was run here).
- Ray-traced shadow map; a real 3D head with a measured Rembrandt
  triangle; motion-capture light rig. All would confirm the same rule;
  none is needed to prove the 2D correlation, which is measured here.

## Sources consulted (public web, 2026-10-31)
- Form vs cast shadow and the terminator: the two shadow types are
  distinguished in standard shading teaching — form shadow is the planes
  turning away from the light, cast shadow is the object blocking light
  onto another surface; the terminator is the edge between light and
  shadow zones.
- Light-direction / shadow-direction coupling: "the direction and size
  that the shadow takes is directly affected by the direction of the
  light source" (animated-shadow teaching example, sun moving -> shadow
  moves opposite and lengthens as the sun lowers).
- Key-light continuity: in CG/cinematography a key light is a fixed
  object in space; changing the shot angle without moving the light
  changes which side is lit, and lighting drift (light re-interpreted
  per frame) is a known failure mode — the fix is locking one lighting
  description across frames, which is exactly C1 here.
