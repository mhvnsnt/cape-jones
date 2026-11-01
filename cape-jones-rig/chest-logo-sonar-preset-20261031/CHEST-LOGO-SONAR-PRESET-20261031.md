# CHEST LOGO SONAR — Preset, 2026-10-31

Ordered by Mars 2026-10-31 21:07 CDT, replying to the Transformation #4 contact diagram tile (origin + radial rings around the chest emblem).

Mars's idea: that diagram tile could be one of his powers, like a chest logo sonar thing, if made visual. Filed as BOTH:
- POWER preset — because he has superpowers.
- GADGET preset — because he is kind of a cyborg and has a gadget costume.
Same visual, two categories, stated plainly. Neither category was picked silently.

## Spec
- Origin: chest emblem centre (551, 491), measured from the Transformation #4 plate work (purple emblem piece, bbox x539-562 y475-510, centroid 550.8, 491.1). Not guessed.
- Rings: 3 rings, staggered 1/3 cycle, expanding outward from the emblem.
- Radius: 30px to 420px, fading alpha 255 to 0, width 6px (early) / 4px (late), plus a faint inner line.
- Colour: cyan (0, 200, 255), with a pulsing white-centre emblem dot (14-20px).
- Timing: 24 frames @ 12fps, 2.0s, 1 full pulse cycle, looping.
- Layer: separate effect layer, composited over the base plate. Base art never recoloured, never baked. Grey in GIF/contact is display-only; frames/ are transparent RGBA masters.
- Source plate: rig-apose-v7c-clean-transparent.png, 1100x1500.

## Files
- chest-logo-sonar-20261031.gif (animated proof, 24f)
- chest-logo-sonar-contact-20261031.png (frames 0, 6, 12, 18)
- chest-logo-sonar-effect-only-20261031.png (effect layer alone)
- chest-logo-sonar-preset-20261031.json (spec)
- build_sonar.py (builder)
- frames/ (24 transparent masters)

## Status
Approval 0/1. No repo push (landing is a separate step). Not a canon story effect claim — this is a visual preset, power/gadget filing only.
