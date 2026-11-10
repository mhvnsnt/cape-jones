# scene-render — Cycles presets for the living room (in-house)

`scene_cycles_config.py` — render settings for the living-room interior on
Colab/Kaggle T4 GPUs. It **extends** `production/pipeline/cycles_speed_config.py`
(the character-animation presets); it does not duplicate it.

## Why a separate preset

The character presets are tuned for figures lit by area/emissive lights
(2 diffuse bounces, 1 volume bounce). An interior soaked in violet LED wash +
god-ray volumes needs:

| Setting | character "animation" | living_room |
|---|---|---|
| diffuse bounces | 2 | **4** (the LED wash lives on bounced light) |
| volume bounces | 1 | **2** (shafts + lamp haze) |
| volume_step_rate | 1.0 | **2.0** (halves marching cost; identical for soft haze) |
| volume_max_steps | 1024 | **256** |
| volume guiding | off | **on** (thin shafts converge faster) |

Everything else (16spp adaptive 0.05, GPU OIDN, persistent data) is inherited
unchanged from the proven base preset.

## Presets

- `living_room` — final look
- `living_room_preview` — blocking/timing (~4x faster; step rate 4.0)
- `living_room_hero` — close-ups (step rate 1.0, 32spp base)

## Use (render lane, headless)

```bash
$BLENDER -b 3d-assets/living_room.blend --python \
  tools/scene-render/scene_cycles_config.py -- living_room
# then render as usual
```

**Verified 2026-10-17 by this lane (real run, Blender 4.5.3 LTS):**
all three presets apply cleanly; settings asserted
(step_rate 2.0/4.0, diffuse 4/2, OIDN).

**Bug note for the pipeline lane:** `production/pipeline/cycles_speed_config.py`
sets `c.scrambling_distance = 'AUTOMATIC'`, but on 4.5.3 LTS that property is a
**float** → TypeError. This preset catches it and sets 1.0. The base script
should get a try/except (not changed here — pipeline lane owns that file).
