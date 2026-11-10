# led-3d — in-house 3D LED system

Our own `led3d.py` — the missing 3D half of the LED gag. (The existing
`production/pipeline/led_controller.py` grades 2D video with ffmpeg; this one
drives the actual 3D room.)

## The studio rule

One master control drives every LED element — strips, practical lights, screen
glow — so they can never drift out of sync. State lives on the **scene**:

- `LED_color` — RGBA master color (canon default `#731AE5` violet)
- `LED_brightness` — master dimmer, 0..3

`wire_strip_material("LEDStripMat")` and `wire_light("RoomLight")` add drivers
from these props **without touching anything else** in the materials — the
canon look is preserved, the color just becomes animatable.

## Use

```python
import led3d
led3d.setup_led_master()                       # canon violet default
led3d.wire_strip_material("LEDStripMat")       # LED_Back/Left/Right strips
led3d.wire_light("RoomLight")                  # the dominant violet wash
led3d.wire_light("HallLight", base_energy=60)  # optional

# full animations (keyframes the master props):
led3d.apply_preset("rainbow-cycle", 1, 250)    # party mode
led3d.gag_press_sequence(                      # remote gag:
    [(1,0,0,1), (0,1,0,1), (0,0,1,1)],         #   jump-cut colors...
    frames_per_color=48, party_tail_frames=240) #   ...then rainbow tail
```

Presets: `purple-pulse`, `chill-blue`, `ember-glow`, `ocean-calm`,
`rainbow-cycle`. The remote prop stays dumb — the TV/gag lane keys the master
props on press frames; every wired element follows.

**Verified 2026-10-17 by this lane (real run, Blender 4.5.3 LTS):**
master props created; strip material Emission color/strength driven;
point light color driven per-channel + energy = brightness × base
(proved via depsgraph evaluation: color (1,0,0), energy 150.0 at
brightness 0.5); rainbow-cycle preset keyed 25 color keys.

For the lighting lane: wire `LEDStripMat`, `RoomLight`, and the lamp lights,
then block out the gag with `gag_press_sequence()`.
