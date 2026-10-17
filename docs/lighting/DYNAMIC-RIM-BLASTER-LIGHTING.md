# Dynamic Rim + Blaster Lighting (owner 2026-10-17)

Two refinements to the locked lighting canon, both owner-direct, both going in the same direction: **lighting follows the scene, not a fixed setup.** This is the show's signature visual device — *"like how texture effects in Chowder"* (his words): Chowder made patterned textures its signature visual language; this show makes dynamic colored lighting its signature.

Locked palette baseline lives in `characters/sheets/03-color-lighting-vfx-key.jpg` and `characters/cape-jones.md`. These rules sit on top of it.

## 1. Rim Light = Situational

His words: the rim light is SITUATIONAL, motivated by the scene.

- **In space / dark void:** blue/cyan rim (reference: sheets `09-hero-shot-black.png`, `10-hero-in-space.jpg`).
- **In LED scenes:** the LED lighting itself creates the rim. The remote-driven environment IS the rim source (see `LED-CONTROLLER.md`).
- **While a blaster fires:** the blast's color becomes the rim light (see §2 below).
- **Same job everywhere:** the black cape stays visible in dark settings. That's the one non-negotiable.

Implementation:
- **3D = REAL LIGHTS.** A dedicated environment-driven rim/fill rig, keyed to the environment. In space it's a blue/cyan rim rig; in LED scenes it keys to the LED preset; during blaster fire it keys to the blaster color. It is a real rig, not a drawn effect.
- **2D = drawn/composited rim.** Same rules, composited (cyan 2–4px on the void, environment-tinted rim elsewhere). Both versions go hard in their own way.
- **The suit never takes the tint.** Environment color applies to rim lights and energy glow ONLY — the white suit stays #FFFFFF blown out. (Matches the existing model-sheet law in `COLOR-GRADES.md`.)

## 2. Blaster Lighting Concept

His words: the sheet's blaster colors are just EXAMPLES for when it's that color. Like the rim light, everything depends on what color blaster he's firing in that scene.

- **The blast's light BECOMES the scene lighting while it's firing:** creates the rim light on him, throws color into the environment, drives the color grade of the shot.
- **Every blaster type/color gets its own lighting personality** that takes over the scene while it fires. White-core + #FFB300-amber (sheet 03) is the default personality; other colors = other personalities.
- **Same rules in 2D and 3D.**

### BUILD: dynamic blaster-lighting rig

- **3D:** blaster color drives real 3D scene light — rim + spill + grade shift. The blaster VFX event sends its color to the rim/fill rig (§1) and to the environment lights; the grade follows (see `COLOR-GRADES.md` signature grades — blast grades = personality presets per blaster color).
- **2D:** composited equivalent — additive glow layers + color grade keyed to the blast color, same timing (light takes over ON blast fire, releases after).
- Core show identity. Build it once, reuse for every blaster type/color.

## 3. Pipeline references

- Show bible: `docs/SHOW-BIBLE.md` §5A (signature device), §5B (situational rim).
- 2D→3D translation: `docs/pipeline/2D-TO-3D-RULES.md` §Compositing.
- LED environment source: `docs/lighting/LED-CONTROLLER.md`.
- Blaster types/colors: rig lane (`3d-assets/cape-jones-rig/`, blaster VFX lane).
