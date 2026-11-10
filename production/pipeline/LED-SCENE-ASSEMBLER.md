# LED Scene Assembler — 3 Drawings → Finished Vibe Segment

## What it is
You draw **3 frames**. The script builds the whole LED remote scene:
Cape Jones sitting, pressing the button, room color changing on every press,
ending on party mode (slow spectrum rotation).

**No GPU. All CPU ffmpeg. 3 drawings → minutes of scene.**

## The 3 frames (draw in FlipaClip, export as PNG)
1. `sit.png` — sitting in chair, holding the remote, thumb resting
2. `press.png` — thumb pressing the remote button
3. `release.png` — thumb lifting off the button

All 3 should be the same size (1080×1920 like your other videos).

## Run it

**Pick your colors:**
```bash
python3 ~/workspace/tools/post-pipeline/led_scene_assembler.py \
  sit.png press.png release.png led_scene.mp4 \
  --sequence purple-pulse chill-blue ember-glow ocean-calm rainbow-smooth
```

**Or go random (a different color every press):**
```bash
python3 ~/workspace/tools/post-pipeline/led_scene_assembler.py \
  sit.png press.png release.png led_scene.mp4 \
  --random 6 --duration 2.5
```

**Full control:**
```bash
python3 ~/workspace/tools/post-pipeline/led_scene_assembler.py \
  sit.png press.png release.png led_scene.mp4 \
  --sequence purple-pulse chill-blue rainbow-smooth \
  --duration 4 \           # seconds sitting in each color
  --party-duration 15 \    # seconds of party mode at the end
  --audio music.mp3        # music underneath
```

## Options
| Flag | What it does |
|------|--------------|
| `--sequence` | Preset names in order (see list below) |
| `--random N` | Pick N random presets (no repeats back-to-back) |
| `--seed 42` | Lock the random picks so they're reproducible |
| `--duration` | Seconds per color (default: 3.0) |
| `--party-duration` | Seconds of party hold at end (default: 10, 0 = skip) |
| `--party-preset` | Which preset is the party mode (default: rainbow-smooth) |
| `--no-party` | Skip the party ending entirely |
| `--speed` | LED animation speed multiplier (2.0 = twice as fast) |
| `--fps` | Output framerate (default: 24) |
| `--audio` | Music/SFX file to mix under |
| `--list` | Show all 15 presets |

## The 15 presets
```
purple-pulse      His default — violet breathing
chill-blue        Slow blue-cyan fade (thinker moment)
sunset-cycle      Orange → pink → purple → blue
ocean-calm        Blue-teal waves (beach house)
ember-glow        Fireplace flicker
ghost-mode        Eerie teal drift (ghost cave)
rainbow-smooth    Full spectrum slow cycle (THE party mode)
auto-cycle        Cycles through modes like the real remote
jump3-rgb         Hard cuts: red → green → blue
jump7-color       7 hard color jumps
fade3-rgb         Smooth red → green → blue fade
party-strobe      Rapid strobe jumps (Baked Jones scenes)
strobe-white      White strobe
blacklight-flicker UV blacklight buzz
streetlight-hum   The defective purple streetlight
```

## How the sync works
Each color segment = sit in the current color → **press (color changes HERE)**
→ release in the new color. The grade switches exactly on the press frame,
so it reads as the button doing it.

The party hold at the end has no more presses — he just sits there while
the spectrum slowly rotates, like a real LED strip on demo mode.

## In the pipeline
```
FlipaClip (3 frames) → led_scene_assembler.py → finish.py → delivery
```
After assembling, run `finish.py` on the output for the signature grade
+ audio mix, same as any other scene.
