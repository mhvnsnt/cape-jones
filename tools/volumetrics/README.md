# volumetrics — god-ray / atmosphere kit (in-house, CC0-equivalent)

Our own `godray_kit.py` — two-mode god-ray system for Blender 4.x Cycles,
studied from how the industry does it (see `docs/research/SCENE-FULLSTACK.md`
§3), written as original bpy code. No add-on install needed: the `.blend` gets
native objects, materials, and drivers, so it renders on the Kaggle/Colab lanes
with zero dependencies.

## The two modes

| Mode | What | Cost | When |
|---|---|---|---|
| `build_fake_shaft()` | Cone mesh, Emission → Volume output: fresnel edge fade × length fade × animated noise breakup; matching Spot light does the real illumination | ~10x cheaper than true volume, no fireflies | Window shafts, lamp beams — the default |
| `build_true_volume_box()` | Box with Principled Volume, driver-driven `fog_density` | Expensive (one per room max) | Soft room haze that must catch shadows |

Both expose **one master custom property** on a control empty
(`shaft_strength` / `fog_density`) — drivers wire it to every input, so the
lighting lane keys ONE property per beam.

## Presets (tuned to SCENE-CANON)

```python
import godray_kit
godray_kit.window_shafts()  # 3 warm beams through the right-wall window
godray_kit.lamp_haze()      # soft true-volume glow at the floor lamp
```

Window shafts aim from the window opening (x=3.5, opening 1.4×1.1 @ z=1.6) down
toward the rug/recliner area — per canon positions.

## Verify

```bash
xvfb-run -a env -u PYTHONPATH <blender-4.5> -b \
  --python tools/volumetrics/godray_kit.py -- --verify
```

**Verified 2026-10-17 by this lane (real run, Blender 4.5.3 LTS):**
fake shaft + true volume build OK (drivers, Track To, no-shadow flags all
asserted), 32px Cycles render of both volume shaders compiled and wrote PNG.

Quirk found: in a freshly `nodes.clear()`-ed tree, `Noise.inputs["W"]` name
lookup can KeyError until the tree updates — the kit sets `noise_dimensions`
explicitly and falls back to socket index 1.
