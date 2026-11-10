# Character Sheets — LOCKED Build Specs (owner 2026-10-17)

These 10 sheets are the CURRENT locked canon for Cape Jones. They supersede all earlier color/concept material (see `characters/cape-jones.md` for the alternate-colorway log).

| # | File | Build spec |
|---|---|---|
| 01 | 01-tpose-turnaround.jpg | T-pose turnaround — construction baseline |
| 02 | 02-model-sheet-orthographic-turnaround.jpg | Orthographic model sheet turnaround |
| 03 | 03-color-lighting-vfx-key.jpg | **Color/lighting/VFX key — LOCKED PALETTE** (see below) |
| 04 | 04-action-flight-vfx-reference.jpg | Action / flight / VFX reference |
| 05 | 05-expression-eye-dart-matrix.jpg | Expression + eye-dart matrix; pupil-usage canon |
| 06 | 06-viseme-phoneme-mouth-matrix.jpg | Viseme/phoneme mouth matrix — dialogue rig spec |
| 07 | 07-character-parts-expressions.jpg | Character parts + expression variants |
| 08 | 08-body-parts-limbs-capes.jpg | Body parts, limbs, cape variants (hands = priority zone) |
| 09 | 09-hero-shot-black.png | Hero shot on black — rim-light read test |
| 10 | 10-hero-in-space.jpg | Hero in space — situational rim-light reference |

## Locked palette (from sheet 03)

- Suit base: pure white **#FFFFFF** — stays blown out, NO gradients or dirt passes, hard vector shapes, no multiply
- Cowl & logo: deep violet **#3E1473**
- Skin tone: warm mid-tone **#E5B28C**
- Cape & shadows: absolute black **#000000**
- Rim light: 2–4px; separates silhouette from void; environment bleed on rim ONLY
- Blaster FX: core blast pure white **#FFFFFF**, outer glow **#FFB300** (color dodge/add); energy & sparks overlap black line art
- Environment color bleed: suit stays white; tint goes strictly to outer rim + energy glow

## Rim light = situational (owner 2026-10-17)

Motivated by the scene, not a fixed color:
- Space / dark void: blue/cyan rim (sheets 09–10)
- LED scenes: the LED lighting itself creates the rim
- Blaster firing: the blast's color becomes the rim + scene light while it fires

Same job everywhere (black cape stays visible in the dark); 3D = real environment-driven rim/fill rig, 2D = drawn/composited rim. Full rules: `docs/lighting/DYNAMIC-RIM-BLASTER-LIGHTING.md`, `docs/pipeline/2D-TO-3D-RULES.md`.

## Pupil canon

Base = "Cape Ghost" (Space Ghost minus ears/proprietary bits): cowled mask, chin showing, **white eyes default**. He SOMETIMES gains cartoony irises/pupils for emphasis — not every time; plenty of big campy acting happens pupil-less. Sheet 05 is the pupil-usage matrix. Full canon: `docs/SHOW-BIBLE.md` §2A.
