# Lighting and Shadow Words — layman + technical, 2026-10-31

Mars ordered 2026-10-31 23:31 CDT: save the shadow methods as presets, wire lighting
from different angles and different light levels, with the shadows that come from
that, using whatever industry-standard words go with lighting and shadow stuff.
This doc is the word list for that system. Every word below is used in the
presets in `presets/` and in the angle x level cells in `angle_level/`.

Matching rule, carried over from shadows-wire100: one light per composite;
ground shadow AND character shadow from that SAME light; shadow colour never
pure black — dark warm tint (46,32,14) = mix(black, rim 255,180,80, 0.18);
figure alpha NEVER changed by a shadow layer; ground layers sit BEHIND the
figure; character layers darken RGB inside the figure only.

## The words

- **Key light** — Layman: the main light, the one that makes the shadows.
  Technical: the primary, strongest light in a scene; it sets shadow direction
  and the lit side. In this system: the single light per angle x level cell.
- **Fill light** — Layman: a weaker second light that softens the dark side,
  so shadows are not pitch black. Technical: a low-intensity light from the
  opposite side of the key, lifting shadow values without making its own
  hard shadow. In this system: NOT a second hard shadow — it is the reason
  our dark end never goes to 0 (form dark ends 0.55–0.92, never 0).
- **Rim light / back light** — Layman: a light from behind that draws a bright
  edge around the figure, so he pops off the background. Technical: a light
  behind the subject, toward camera; in our system it is the outer rim band
  in the rim colour family (255,180,80 warm gold). Back angle cells use the
  strongest rim reading, with the front darkest (dark end 0.55).
- **Ambient light** — Layman: the general light that is everywhere, no
  direction, so nothing is ever fully black. Technical: directionless base
  illumination. In this system: the room gradient + the 0.35 darkness floor —
  even Darkness cells still read, figure mean ~37–46, not 0.
- **Falloff** — Layman: how fast light gets weaker as you move away from it.
  Technical: intensity decreasing with distance / angle. In this system:
  X2 depth-gradient (cast alpha 1.0 → 0.25 with distance below feet) and
  the level gains (darkness 0.35 → intense 1.35).
- **Terminator** — Layman: the line on a body where light stops and shadow
  starts. Technical: the boundary between lit and unlit surface on a form.
  In this system: the gradient edge in I4 form shadow, where the 1.0 lit side
  crosses into the dark end.
- **Form shadow** — Layman: the dark side of the body itself, because the
  body blocks its own light. Technical: attached shadow on the unlit side of
  a form. In this system: I4, gradient across the light axis.
- **Cast shadow** — Layman: the shadow the body throws onto the ground or
  onto something else. Technical: projected shadow on another surface.
  In this system: I2, figure alpha squashed to 28% height, sheared by light dx.
- **Contact shadow** — Layman: the dark patch right where feet touch the
  ground, the thing that stops him looking like he is floating. Technical:
  the darkest, sharpest shadow at the contact point. In this system: I1,
  ellipse at feet, 1.16x feet width, blur 10.
- **Ambient occlusion (AO)** — Layman: the extra darkness in creases, joints
  and where parts meet, even without a strong light. Technical: interior
  darkening where surfaces are close together and ambient light cannot reach.
  In this system: I3, band <12px inside the figure, darkened 25%.
- **Umbra** — Layman: the fully dark middle of a shadow. Technical: the
  region in total shadow, no direct light. In this system: the centre of the
  contact ellipse / the darkest part of the cast.
- **Penumbra** — Layman: the soft, fading edge of a shadow. Technical: the
  partial-shadow edge where light is only partly blocked. In this system:
  I5 soft shadow, blur 12, and every blurred ground layer.
- **Soft shadow / PCF-like** — Layman: a shadow with a soft edge, not a hard
  cutout. Technical: penumbra from an area light, approximated here by
  blurring the union of contact + cast (I5). This is the ground shadow used
  in FULL composites, not triple-stacked with I1 + I2.
- **Hard shadow** — Layman: a shadow with a sharp edge, like noon sun.
  Technical: a point-light shadow with almost no penumbra. In this system:
  the unblurred cast before the I5 blur — a reference, not the default.
- **Light level / exposure** — Layman: how dark or bright the whole scene is.
  Technical: overall gain. In this system, measured: Darkness gain 0.35,
  Dim 0.55, Normal 0.85, Bright 1.15, Intense 1.35; shadow scale 0.55 / 0.75 /
  1.00 / 1.25 / 1.45; rim strength 0.40 / 0.60 / 1.00 / 1.20 / 1.40.
- **Light angle / light direction** — Layman: where the light is coming from.
  Technical: the light vector; it sets which side is lit and which way the
  ground shadow falls. In this system: overhead dx +30, front dx 0, back dx 0
  (front darkest), left dx +120 (shadow falls right), right dx −120 (shadow
  falls left), low dx +60 (lit from below), high dx +15 (steep top light).
- **Colour bleed / bounce light** — Layman: light bouncing off the floor or
  a coloured surface and tinting the dark side warm. Technical: indirect
  bounce illumination. In this system: X3 warm tint (60,30,10) on the away
  side, and X5 ground-texture interaction (shadow reduced 30% where floor
  pools are bright).
- **Shaft / volumetric light** — Layman: light you can see in the air, like
  sun through a window. Technical: visible light volume, not just light on
  a surface. In this system: X1, cast masked to the 5 v4 shaft columns.

## What is NOT claimed here

- No Blender Cycles true 3D shadow pass, no ray-traced shadow map, no true
  volumetric shadow — those were mapping only in shadows-wire100 and stay
  mapping only here. Everything in this folder is a PIL/numpy/scipy proxy
  with measured parameters, labelled as such.
- The room in every cell is a labelled TEST gradient room, not a prior
  render, so angle/level differences are comparable. No prior render is
  claimed as the room for these cells.
