# 2D → 3D Translation Rules (owner 2026-10-17)

Translated from the owner's pasted 2D pipeline breakdown. The look he signs off in 2D is the spec the 3D pipeline must hit — one canon, two implementations.

Locked palette: `characters/sheets/03-color-lighting-vfx-key.jpg` / `characters/cape-jones.md` §"Locked palette — CURRENT".

## COMPOSITING → 3D Lighting

- **Rim light (2D):** cyan, 2–4px, separates the black cape from dark backgrounds.
- **Rim light (3D):** a real environment-driven rim/fill rig — the 2–4px drawn rim's equivalent. Black cape stays visible in the dark. (Full spec: `docs/lighting/DYNAMIC-RIM-BLASTER-LIGHTING.md`.)
- **Energy blasts:** white core **#FFFFFF** + yellow/cyan outer glow **#FFB300** on ADDITIVE emission, bleeding over line art. (The sheet's blaster colors are examples for when he's firing that color — see dynamic blaster lighting below.)
- **Environment color ONLY on rim lights and glow — NEVER tint the white suit.** The suit stays #FFFFFF blown out no matter what the scene is doing.

### Dynamic blaster lighting (owner 2026-10-17)

- **The blast's light BECOMES the scene lighting while it's firing:** creates the rim light on him, throws color into the environment, drives the color grade of the shot.
- **The sheet's blaster colors are just EXAMPLES for when it's that color.** Every blaster type/color gets its own lighting personality that takes over the scene while it fires — *"like how texture effects in Chowder"* (his words): Chowder made patterned textures its signature visual language; this show makes dynamic colored lighting its signature.
- **BUILD:** dynamic blaster-lighting rig — blaster color drives real 3D scene light (rim + spill + grade shift); 2D gets the composited equivalent. Same rules in 2D and 3D. Core show identity.
- Full spec: `docs/lighting/DYNAMIC-RIM-BLASTER-LIGHTING.md`, show bible §5A.

### Rim light = situational (owner 2026-10-17)

Motivated by the scene: space = blue/cyan rim; LED scenes = the LED lighting itself creates the rim; blaster firing = the blast's color is the rim. Same job everywhere (black cape visible in dark). 3D = real lights; 2D = drawn/composited rim. Both versions go hard in their own way. Full spec: show bible §5B, `docs/lighting/DYNAMIC-RIM-BLASTER-LIGHTING.md`.

## SHADING → Toon/Cel Shader

- Hard vector shadow shapes. No gradients. No soft AO.
- Suit stays blown out — no dirt passes, no multiply, hard shapes only.
- 2D composite shadow shapes become the 3D cel-shader thresholds (match by eye, not by math).

## CAPE

- 2D: cape lives on its own layer with spline controllers.
- 3D: separate cape mesh + cloth sim (rig lane already set this up — pin group, collision). Same rule: the cape is its own thing; it leads, the body follows a beat late.

## POSING RULE

- The white suit has NO internal detail — silhouettes must read instantly.
- Every key pose (idle, sitting, flight, blast) must be recognizable by OUTER SHAPE ALONE.
- Test every pose on black and on white before it ships (sheets 09–10 are the reference).

## AUDIO NOTE (flagged for the AUDIO lane)

- Voice + sound design do HALF the heavy lifting.
- Voice: dry, booming, authoritative delivery.
- Sound: sci-fi zaps, impacts, ship hum.
- Audio lane owns this — 2D/3D both mix to the same signature.
