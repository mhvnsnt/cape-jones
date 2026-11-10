# Cape Jones Render Looks (Show Lighting Presets)

**Owner rule (2026-10-29):** the show keeps a LIST of lighting looks and a
scene picks the one it wants. New looks get ADDED to the list — nothing gets
voted off. This file is that list.

## What a "look" is, in plain show terms

The lamps in the room do not change. A look is the film the scene is shot
on — how the camera develops the colors after the lights have done their
job. Same set, same lamps, different look = a different-feeling scene.

Stack order for a scene's color:

1. **The lights in the scene** — lamps, LED strips, blaster light
   (see `LED-CONTROLLER.md`, `DYNAMIC-RIM-BLASTER-LIGHTING.md`)
2. **The render look** — THIS list, picked per scene
3. **A finish grade on top, if the scene wants one** — `COLOR-GRADES.md`

Apply a look in Blender with `production/pipeline/render_looks.py`:

```
blender -b scene.blend --python production/pipeline/render_looks.py -- pale-wash
blender -b scene.blend --python production/pipeline/render_looks.py -- list
```

---

## LOOK 1 — PALE WASH *(the default)*

Flat, pale, washed-out color. The everyday look — normal rooms, daylight,
plain talking scenes. If a scene does not name a look, it is shot Pale Wash.

- **Technical:** Blender's built-in color management, view transform **AgX**.
  No special launch needed; works in any Blender session.

## LOOK 2 — DEEP SATURATION

Rich, punchy color. Walls go deep, the chair pops, blacks get blacker.
Night scenes, LED scenes, anything that should feel moody or loud.

- **Technical:** the ACES filmic pipeline. Blender must be LAUNCHED with
  the show's OCIO config, then the view transform is set to
  **ACES 1.0 - SDR Video**:
  ```
  OCIO=<repo>/tools/wired/fullstack/aces/cg-config-v2.1.0_aces-v1.3_ocio-v2.1.ocio \
    blender -b scene.blend --python production/pipeline/render_looks.py -- deep-saturation
  ```
  (If Blender was launched without the config, the script says so and
  prints this exact relaunch line instead of failing.)

---

## Proof

Both looks were rendered from the same frame of the final sitting scene
(frame 40, identical settings, 2026-10-29) before this list was written:
Pale Wash reads pale lavender-pink; Deep Saturation reads deep magenta
with a hot coral chair and a properly black cape. The owner saw both and
ruled: keep both, as presets.

## Adding a look

1. Give it the next number and a plain show name (what it feels like).
2. Write when a scene would pick it, in one or two lines.
3. Write the exact technical steps to apply it — no guessing later.
4. Render one proof frame next to Look 1 so the difference is visible.
