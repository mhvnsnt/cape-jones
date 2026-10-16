# Cape Jones LED Lighting Controller

## The Concept

Cape Jones has RGB LED strip lights in his house — the real kind, like Govee or Philips Hue strips. When he's inside, he hits a button on the controller and the room lighting changes colors. Slow fades, pulses, strobes, full cycles.

This isn't just a visual trick. It's a **story device**. The LED controller is a physical object in his house. He picks up the remote, hits a button, the room changes. The audience sees him do it.

His remote is the standard **44-key IR remote** (the kind that comes with RGB 5050 strips). The presets below map 1:1 to its real modes.

## The Presets

### Original 8 (LED strip classics)

| Preset | Real LED Mode | Vibe | When to Use |
|--------|--------------|------|-------------|
| `chill-blue` | FADE | Slow blue-cyan fade | Cup-lift thinker moment, relaxing |
| `purple-pulse` | PULSE/BREATHE | Violet heartbeat | **Default.** Him just vibing at home |
| `sunset-cycle` | FADE | Orange→pink→purple→blue | Evening wind-down |
| `party-strobe` | JUMP/STROBE | Hard rapid color jumps | Baked Jones scenes, parties |
| `ghost-mode` | FADE (slow) | Eerie teal-green drift | Ghost cave, Nosferatu vibing |
| `ocean-calm` | FADE | Blue-teal water waves | Daytime chilling, beach house feel |
| `ember-glow` | FLICKER | Fireplace warm flicker | Cozy night scenes |
| `rainbow-smooth` | FADE (full) | Full spectrum cycle | Montages, demo mode energy |

### New: 44-Key Remote Modes (exact matches)

| Preset | Remote Button | What It Does | When to Use |
|--------|--------------|--------------|-------------|
| `strobe-white` | FLASH | White strobe on/off | Alarm, shock, "what the fuck" moments |
| `jump3-rgb` | JUMP3 | Red → Green → Blue, hard cuts | Abrasive, attention-grabbing |
| `jump7-color` | JUMP7 | 7 colors, hard cuts | Party chaos |
| `fade3-rgb` | FADE3 | Red → Green → Blue, smooth | Gentler than jump |
| `auto-cycle` | AUTO | Drifts through all dynamic modes | Set-and-forget background vibe |

### New: Real-World Light Sources (animated)

| Preset | Source | What It Does | When to Use |
|--------|--------|--------------|-------------|
| `blacklight-flicker` | UV blacklight | Violet haze + faint mains flicker | Blacklight party scenes |
| `streetlight-hum` | Purple streetlight | Constant wrong-color blue-violet, barely-perceptible hum | Exterior night scenes |

### Static Grades (single-frame, for thumbnails/reference)

These live in `grades.py` — use with `finish.py --grade`:

| Grade | Source |
|-------|--------|
| `purple-streetlight` | Defective LED streetlight (phosphor delamination) |
| `blacklight-purple` | UV blacklight room |
| `bulb-orange` / `bulb-yellow` / `bulb-red` / `bulb-purple` / `bulb-green` | Colored LED bulbs |
| `disco-party` | Dark base for disco overlay (dots composited separately) |

Full research: [REAL-LIGHTING-RESEARCH.md](REAL-LIGHTING-RESEARCH.md)

## Usage

```bash
# Apply a preset to a video
python3 ~/workspace/tools/post-pipeline/led_controller.py input.mp4 output.mp4 --preset purple-pulse

# Speed it up or slow it down (1.0 = default)
python3 ~/workspace/tools/post-pipeline/led_controller.py input.mp4 output.mp4 --preset chill-blue --speed 0.5

# List all presets
python3 ~/workspace/tools/post-pipeline/led_controller.py --list
```

## How It Works (Technical)

Each preset is an ffmpeg filter chain using time-varying expressions:

- **`hue=h='...'`** — hue rotation driven by `t` (timestamp). Sine waves for smooth FADE modes, `floor()` step functions for JUMP/strobe.
- **`eq=brightness='...'`** — brightness pulsing for BREATHE effects.
- Base grade from `grades.py` sets the starting color, then the time-varying filters animate it.

Example — purple-pulse:
```
hue=h='275+10*sin(2*PI*t/8)',eq=brightness='0.03*sin(2*PI*t/8)'
```
Hue oscillates ±10° around violet (275°) over 8 seconds. Brightness breathes in sync.

## The Controller Prop

In the show, the LED controller is a small black remote on his coffee table. When he hits a button:
1. Close-up of his thumb pressing the button (or just the click sound)
2. Room lighting shifts to the new preset
3. He reacts (or doesn't — sometimes he doesn't even notice)

This is a running visual gag. The room can completely change mood mid-conversation and he just keeps talking.

## LED Positions in the House

- **Living room**: Strip behind the TV, strip along the ceiling cove, floor lamp with smart bulb
- **Kitchen**: Under-cabinet strips
- **Bedroom**: Headboard strip
- **Ghost cave**: Single flickering teal strip (always on ghost-mode, he never changes it)
- **Bathroom**: He forgot to put LEDs here. It's just a normal harsh white bulb. He hates it.

## Rules

1. **In-house = LED presets.** When he's inside, the lighting comes from the controller.
2. **He controls it.** The audience should see or hear him change it (button click, remote in hand, voice command).
3. **Ghost cave is always ghost-mode.** He doesn't touch that one.
4. **Outside = creative grades**, not LED presets. Different system entirely.
5. **The joke**: the lights change dramatically and he acts like nothing happened.
