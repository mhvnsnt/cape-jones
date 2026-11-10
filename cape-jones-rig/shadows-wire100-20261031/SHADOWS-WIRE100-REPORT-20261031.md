# Shadows Wire-100 — 2026-10-31

Mars ordered 2026-10-31 23:24 CDT, replying to the shafts v4 grounded composite:
"Perfect now we need to pull in 5 industry standard for shadows and 5 experimental
for shadows and wire them up 100% cause those are really good lifts and we need
shadows on the ground and on our character to match"

## Approvals recorded, not re-asked
- Grounded main shafts composite APPROVED PERFECT 1/1 (Mars, this message, replying
  to that composite). That composite is untouched here.
- Floating shafts version stays NOT approved.
- Grounded final contact and grounded per-shot set stay 0/1 separately.
- Shadow system in this folder: approval 0/1 separately.

## Matching rule (the whole point)
One light per scenario, ground shadow AND character shadow from that SAME light:
same direction, same rim colour family (255,180,80 warm gold), shadow colour
never pure black — dark warm tint = mix(black, rim, 0.18) = (46,32,14).
Figure alpha is NEVER changed by any shadow layer. Ground layers sit BEHIND the
figure; character layers only darken RGB inside the figure (form/AO bands).

## Scenarios (both feet_y = 1400, ground line Gy = 1400, diff 0)
- A shafts overhead: shafts Eevee v4 room, clean apose plate placed at the same
  ground line (bbox 237,359,864,1400). Light from above, slight right (dx 30).
  Ground shadow 70,329 px, figure alpha 373,846 px.
- B golden-hour front-left: labelled test gradient room (NOT a prior render),
  S7 golden-hour lit plate (bbox 216,346,885,1400). Light from front-left (dx 120),
  so ground shadow falls to the right of the feet and character shadow is on the
  right/away side. Ground shadow 84,261 px, figure alpha 408,573 px.
- Honest base note: the grounded shafts composite itself is baked RGB with no
  separate figure layer, so the shadow test does NOT claim a pixel extraction
  from it — it recreates the same ground line, same shafts room, and a clean
  transparent plate at that ground line. The approved grounded composite itself
  is untouched.

## 5 industry-standard — ALL RUN
- I1 Contact shadow: dark ellipse at feet, wider than feet (1.16x), blur 10.
- I2 Cast / projected shadow: figure alpha squashed to 28% height, sheared by
  light dx, placed from the ground line, recolour to shadow tint.
- I3 Ambient occlusion: interior band, distance < 12 px inside the figure,
  darkened 25% (edge/crevice darkening, not a new drawing).
- I4 Form / cel shadow: gradient across the light axis, 1.0 lit side to
  0.72 (side light) / 0.78 (overhead, top lit to bottom dark).
- I5 Soft / PCF-like shadow: blurred union of contact + cast, blur 12,
  penumbra falloff — this is the ground shadow used in the FULL composites
  (not triple-stacked with I1+I2).

## 5 experimental — ALL RUN
- X1 Shaft-aligned shadow: cast shadow masked to the 5 v4 shaft columns
  [58,212],[267,418],[474,622],[679,832],[887,1041].
- X2 Depth-gradient shadow: cast alpha fades 1.0 to 0.25 with distance below feet.
- X3 Colour-bleed shadow: away-side shadow tinted warm (60,30,10) instead of
  neutral black — a variant of form, NOT stacked on top of I4.
- X4 Flicker / sway sequence: 3-frame GIF, cast offset -6 / 0 / +6 px
  (A and B sequences in scenarios/).
- X5 Ground-texture interaction: cast alpha reduced 30% where the floor pools
  band is bright (room mean > 110 in y1400-1500), so shadow follows the floor
  light instead of painting over pools flatly.

## Mapping only (NOT counted in the 10)
- Blender Cycles true 3D shadow pass: needs a 3D figure model, not run here.
- Ray-traced shadow map: no ray tracer run, PIL proxy only.
- True volumetric shadow: shaft volume shadow, PIL column mask proxy only.

## Gates
- Ground gate: feet 1400 = Gy 1400, diff 0, both scenarios, PASS.
- No-crop: figure inside canvas both scenarios, PASS. Occlusion: no figure
  pixel erased — figure alpha unchanged, character layers darken RGB only
  inside the figure; ground layers are behind the figure.
- First run finding, fixed in-run: ground shadow was too weak on the bright
  floor pools (hidden under feet at feet zoom). Fixed by widening contact
  ellipse, raising cast alpha 140 -> 190 and contact 150 -> 200, blur 18 -> 12.
  Ground shadow A grew 58,608 -> 70,329 px, B 73,945 -> 84,261 px, and the
  feet zoom now reads a dark band under and between the feet.

## Files
- Builder: build_shadows.py
- Measurements: measurements-shadow-wire100-20261031.json
- Scenarios: scenarios/*-full-shadow.png, *-no-shadow.png, *-X4-sequence.gif
- Methods (isolated, scenario A): methods/A-shafts-overhead-*.png
- Contacts: contacts/shadow-before-after-contact-20261031.png,
  contacts/shadow-methods-contact-20261031.png,
  contacts/light-direction-diagram-20261031.png,
  contacts/*-feet-zoom-20261031.png

No repo push. Grounded composite untouched. Shadow system approval 0/1.
