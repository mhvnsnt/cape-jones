# Shadow / lighting presets — improved pipelines + new directions
Date: 2026-10-31. Folder: shadow-lighting-presets-improved-20261031/
Approved source: shadow-presets-angle-level-20261031/ — READ-ONLY here, untouched.
Approved versions stay APPROVED 1/1 (preset index, angle-level grid, presets 10/10,
X3 colour-bleed, X4 flicker-sway, X5 ground-texture, per Mars 2026-10-31 23:41 CDT).
Everything in this folder is NEW: v2 improved versions, new directions, new methods.
No repo push by this task.

## AO + underlight, plainly
- Ambient occlusion (AO) = darkening in crevices and where parts touch
  (eye sockets, cowl folds, armpits, belt shadow, joints). That IS part of the
  dark dramatic comic/cartoon look Mars meant.
- Flashlight-under-the-face itself = UNDERLIGHT / UPLIGHT, a low upward key
  light. It works WITH AO: uplight lights chin/jaw/cheeks from below, AO keeps
  the crevices dark. Both are in the same pipeline here, not substitutes.

## 1. Improved pipelines v2 — 10/10, all RUN
- I1v2 contact-core: contact ellipse + hard dark core (blur 4, alpha 235) inside
  the soft ellipse. Sharper foot contact, still soft edge.
- I2v2 cast-taper: cast squashes 28% and narrows with distance (taper factor
  down to 0.55), instead of a uniform-width shear.
- I3v2 AO-graded: band 20px, darken up to 0.35, graded by depth — deeper
  crevice (small distance-transform) darker, fading to 0 at the band edge.
  Old AO was flat 12px / 0.25.
- I4v2 form-wrap: smoothstep terminator + wrap light leaking past the
  terminator (0.15), instead of a linear gradient stopping dead.
- I5v2 soft-core-taper: I1v2 + I2v2 union, blur 12. The FULL ground shadow v2.
- X1v2 shaft-dapple: cast masked to the 5 v4 shaft columns PLUS figure
  dapple — figure 0.92 inside columns, 0.78 between (darker between shafts).
- X2v2 depth-fade-blur: cast fades 1.0→0.25 with distance AND blur grows
  with distance (near sharp, far blur 20), instead of fade alone.
- X3v2 colour-bleed-bounce: warm away-side tint (60,30,10) PLUS warm floor
  bounce tint (255,180,80 at 0.6) on the ground contact. Approved X3 untouched.
- X4v2 flicker-sway-5f: 5-frame sequence, offsets -8/-4/0/+4/+8 px, alpha
  breathing 0.90/0.97/1.0/0.97/0.90, 200ms. Approved X4 (3-frame) untouched.
  Approved X4 original GIF, for Mars to see: see links in parent report
  (shadow-presets-angle-level-20261031/presets/flicker-sway-shadow/sample.gif).
- X5v2 ground-texture-graded: cast reduction graded continuously with floor
  brightness (0→0.30 into the floor band), instead of a binary >110 threshold.
  Approved X5 untouched.

## 2. New directions — 7 files
- underlight: key from below, dark_end 0.55, dx 0.
- underlight-darkness: same, gain 0.55, dark_end 0.45 — the dark dramatic set.
- underlight-left / underlight-right: uplight sheared ±60px.
- low-back-rim: rim/backlight from below-behind, front darkest.
- spot-dramatic: steep above-front spot, dark_end 0.60, gain 0.85.
- AO-plus-uplight-combined: underlight form + strong AO (band 24, darken 0.45).
- Face zooms: face-zoom-combined.png and face-zoom-underlight.png
  (crop x380-760, y340-700, 2x). Lower face lit from below, cowl top darker.

## 3. New methods — 5 industry + 5 experimental, all RUN
Industry:
- NI1 three-point: key left + fill + rim combined (form dark_end 0.78 + AO 0.20).
- NI2 chiaroscuro-Rembrandt: strong side key (dark_end 0.55) + bright patch
  on the away cheek (head area, ~620,520, scaled 1.35).
- NI3 kicker-edge: cool edge band (120,180,255, alpha 90) on the opposite
  side of the figure (EDT<10, x>centre). Visible as a blue edge at contact scale.
- NI4 spotlight-cone: visible light cone in the air (255,200,120, alpha 45,
  blur 15) from above, figure lit under it.
- NI5 temperature-split: warm tint (255,170,90) on the left, cool tint
  (120,170,255) on the right, up to alpha 40 each.
Experimental:
- NX1 halftone-shadow: ground shadow as comic dots (12px grid, dot radius
  by cast alpha). Dots read at full resolution; at contact scale they merge
  into a solid-looking shadow — stated, not hidden.
- NX2 ink-outline-shadow-side: shadow-side outline thickened (EDT<22, x>centre,
  dark tint alpha 160). Visible as a heavier right-side outline.
- NX3 glow-underlight: warm glow halo below the face (255,140,40, blur 40)
  + uplight form + AO.
- NX4 shadow-breathing-4f: ground shadow pulses 0.94/1.0/1.06/1.0, 250ms.
- NX5 mood-purple-shadow: cast recoloured purple-black (40,20,70).

## Gates — PASS
- Canvas 1100x1500 on every composite; feet 1400 = ground line 1400 in all
  direction composites; figure bbox inside canvas.
- Figure alpha unchanged by construction: every composite pastes the same
  CANVAS plate; character layers are black-alpha overlays, ground layers sit
  behind the figure, no figure pixel is erased.
- Room here is the same labelled TEST gradient room as the angle-level system,
  not a prior render, so comparisons stay comparable.

## Honest limits — stated, not hidden
- Underlight shift is SUBTLE at full-body scale on this white-suit apose plate:
  the suit dominates, so underlight vs overhead reads mainly as lower-body
  brightening + top darkening. The face zoom is where chin-from-below vs
  cowl-top-dark reads. A stronger horror underlight would need a darker
  surrounding room + a tighter face plate, not a stronger gradient on this plate.
- AO-plus-uplight combined vs plain underlight look near-identical at face-zoom
  scale: strong AO adds crevice depth, but the face is small and already
  line-heavy. The difference is in the body crevices (armpits, belt, joints),
  not a redrawn face.
- All methods here are 2D-plate proxies (distance-transform pseudo-normals),
  not true 3D renders, no ray tracer, no Blender Cycles pass claimed.
- NI1 three-point is a combined gradient proxy, not three separate Blender
  lights; NI2's cheek patch is a placed bright zone, not a measured Rembrandt
  triangle from a 3D head.
- No Blender / ray-traced / true volumetric pass is claimed for this set.

## Approvals
- Approved presets (index, grid, 10/10, X3, X4, X5): APPROVED 1/1, untouched.
- Improved pipelines v2: approval 0/1 separately.
- New directions + new methods: approval 0/1 separately.
- Improved versions are NEW, not silent replacements of approved versions.
