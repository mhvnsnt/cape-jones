# Real-World Colored Lighting Research — for Cape Jones 2D Animation

> Goal: when Cape Jones turns on a blacklight, it FEELS like a real blacklight room.
> When he's under a purple streetlight, it feels like those defective LED streetlights.
> Real lighting physics, translated to 2D animation color work.

Owner reference material: screenshots of orange/yellow/red/purple/green LED bulbs,
UV blacklight bulbs, 44-key RGB LED strip remote, spinning disco party light,
blacklight room aesthetic (glow stars, neon posters).

---

## 1. The Purple Streetlight Phenomenon

### What happened
Starting ~2021, LED streetlights across 30+ US states and Canadian cities
turned vivid purple/blue instead of white. Reported in Milwaukee, Eau Claire,
Schaumburg IL, Palm Beach, Los Angeles, Bend OR, Boston corridors, Vancouver,
and others. Wikipedia documents it as "2020s purpling of streetlights."

### Root cause: phosphor delamination
White LEDs aren't actually white. The base LED chip emits **blue light**.
Manufacturers coat the chip with a **yellow phosphor layer** that absorbs some
blue and re-emits yellow — blue + yellow = perceived white ("cool white").

In defective batches (notably Acuity Brands / American Electric Lighting
fixtures), the silicone-phosphor layer **cracks, curls, or peels off** from heat
and environmental stress years after installation. With the yellow filter gone,
the **raw blue LED shines through unfiltered**.

### What it looks like
- From a distance: vivid **purple/violet**
- Up close: the chip itself is **blue** (municipal workers confirm this is a
  "vantage point" issue — purple is the distance blend)
- Spectral output shifts hard toward **blue-violet**; color rendering collapses
- Light output (brightness/lumens) is **unchanged** — same amount of light,
  wrong color
- Side effects: reduced contrast, eye strain, harder to distinguish objects
  and pedestrians; blue scatters more in atmosphere = more light pollution

### How the light falls on surroundings
- Everything under it takes on a **blue-violet cast** — asphalt looks purple,
  white cars look lavender, skin looks ghostly blue
- Shadows stay hard (it's still a point source)
- No warm tones survive — reds go muddy, yellows go green-grey
- The "halo" around the fixture is deep violet

### For Cape Jones (grade: `purple-streetlight`)
- Exterior night scenes: single overhead source, deep blue-violet wash
- Kill warm tones (reds muddy, yellows desaturated)
- Keep brightness high but shift spectrum — NOT a dark grade, a WRONG-COLOR grade
- Skin goes pale blue-lavender; the white suit picks up violet tint
  (this is one of the few grades allowed to tint the suit — it's the whole point)
- Story use: Cape Jones flying past a row of purple streetlights, confused
  why the city looks like a nightclub. Comedy gold.

---

## 2. Blacklight / UV Lighting

### How it works
A blacklight is a lamp engineered to emit **UV-A (320–400 nm)** — invisible to
the human eye — while blocking most visible light. Two designs:
- **Tube blacklight**: fluorescent tube with a special phosphor coating that
  absorbs harmful UV-B/UV-C and passes UV-A, plus a dark "black" glass that
  blocks visible light
- **Incandescent blacklight bulb**: normal bulb with filters absorbing
  everything except UV-A, infrared, and a little visible violet

The room goes **near-dark**. What you see is a faint purple/blue ambient glow
from the small amount of visible violet that leaks through.

### Fluorescence: why things glow
Fluorescent materials **absorb invisible UV photons and instantly re-emit them
as lower-energy visible photons**. The glow stops the instant the UV source is
removed (that's fluorescence; phosphorescence lingers).

What glows under blacklight:
- **White clothing/cotton** → bright blue-white (optical brighteners in detergent)
- **Neon/fluorescent posters, highlighters** → intense saturated color pop
- **Teeth** → yellowish-white glow
- **Petroleum jelly, some plastics** → blue
- **Tonic water (quinine)** → blue-white
- **Non-fluorescent materials** → appear BLACK or near-black

### The blacklight room aesthetic
- Walls/posters: neon art EXPLODES with color against near-black surroundings
- Glow-in-the-dark stars on ceiling: soft green dots floating in darkness
- White objects become light sources (a white t-shirt glows like a lamp)
- Everything else drops to silhouette
- Ambient color: deep violet-purple haze, very low overall brightness
- Contrast is EXTREME — glowing objects vs. pitch black

### For Cape Jones (grade: `blacklight-purple` + animated `blacklight-party`)
- Crush overall brightness hard; lift ONLY blues/violets/purples
- Whites in the scene (his suit!) should BLOOM blue-white — this is the
  money shot: Cape Jones's white suit glowing under blacklight while
  everything else goes dark
- Neon poster colors: push saturation to max on magentas, greens, oranges
- Skin: goes pale with violet cast, teeth glow slightly
- Animated variant: subtle UV flicker (blacklights have a faint mains flicker)
- Story use: Cape Jones walks into a blacklight party. His suit lights up
  like a ghost. Everyone stares. He has no idea why. "What the fuck, man?"

---

## 3. Colored Bulb Lighting Physics

### How a colored bulb lights a room
A colored LED bulb emits a **narrow spectrum** — mostly one hue. Unlike white
light (broad spectrum), it can only illuminate what reflects that wavelength.

Key physics for 2D replication:
- **Walls/furniture** take on the bulb color strongly — a red bulb makes white
  walls look red, beige carpet look dark red-brown
- **Skin** shifts dramatically: under red light skin goes orange-red; under
  green light skin goes sickly olive; under blue/purple skin goes corpse-pale
- **Shadows** stay neutral-dark (shadow = absence of light, no color to reflect)
- **Falloff**: brightness drops with distance from bulb (inverse square), so
  near-bulb surfaces are saturated bright, far corners go dark and muddy
- **Complementary colors die**: under a red bulb, anything blue or green in
  the room goes nearly black (nothing to reflect)

### Per-color notes (from owner's reference screenshots)

**Orange bulb** (Halloween/party):
- Warm amber wash, ~2000K feel. Cozy but eerie.
- Whites go peach/orange. Blues go dark brown-black.
- The classic "porch light on Halloween night" look.
- Grade: `bulb-orange`

**Yellow bulb** (bug light / vintage):
- Slightly less saturated than orange. Warm golden.
- Skin looks healthy-warm, almost tanned.
- Whites go cream. Still kills blues.
- Grade: `bulb-yellow`

**Red bulb** (darkroom / horror / "sleep" bulbs):
- Deep red wash. Everything is red or black — no other hues survive.
- Skin goes deep orange-red, looks feverish.
- White text on paper: red paper, black text — readability drops.
- The "developing photos" / horror movie look.
- Grade: `bulb-red`

**Purple/violet bulb**:
- Violet wash with blue undertones. Club/boudoir feel.
- Whites go lavender. Warm colors (red/orange/yellow objects) go muddy brown.
- Skin goes pale lavender-grey — corpse-like but glamorous.
- Grade: `bulb-purple`

**Green bulb** (St. Patrick's / horror):
- Sickly green wash. The "night vision" / toxic look.
- Skin goes olive-green — instantly reads as "sick" or "alien."
- Reds go dark brown-black. Whites go mint.
- Grade: `bulb-green`

### For Cape Jones
- Each bulb color = a static grade in grades.py
- The comedy: Cape Jones screwing in different colored bulbs, not understanding
  why the room looks "wrong." Or: someone else changes his bulbs as a prank.
- His white suit is the perfect "screen" — it shows EVERY color shift purely,
  making the lighting change unmistakable even in 2D.

---

## 4. LED Strip Light Modes (44-Key Remote)

Researched from the actual 44-key IR remote protocol (RGB 5050 strips).
The remote in the owner's screenshot is the standard 44-key layout.

### Static modes
- **20 static colors** (dimmable, 8 brightness steps): red, green, blue, white,
  orange, yellow, cyan, purple, pink, etc.
- **DIY slots**: 6 user-programmable custom colors
- In animation: these are the static `led-*` grades (already built)

### Dynamic modes (the important ones for animation)
| Remote label | What it does | Animation equivalent |
|---|---|---|
| **FLASH** | White strobe flash, speed adjustable | Hard brightness oscillation, white |
| **STROBE** | Color strobe (current color flashing on/off) | Brightness square wave on tinted grade |
| **JUMP3** | Red → Green → Blue, hard cuts, cycling | Discrete hue jumps, 3 stops |
| **JUMP7** | 7 colors, hard cuts, cycling | Discrete hue jumps, 7 stops |
| **FADE3** | Red → Green → Blue, smooth crossfade | Sine hue rotation, 3-color range |
| **FADE7** | 7 colors, smooth crossfade | Sine hue rotation, full range |
| **SMOOTH** | Full RGB spectrum, smooth continuous | Sine hue rotation, full 360° |
| **AUTO** | Cycles through all dynamic modes automatically | Meta-preset: switch presets every N seconds |

Speed: 10 levels (remote has QUICK/SLOW buttons). Our `--speed` multiplier
maps to this.

### Already built → new additions
- FADE3/FADE7 → existing `chill-blue`, `sunset-cycle`, `rainbow-smooth` ✓
- JUMP3/JUMP7 → existing `party-strobe` ✓ (uses floor() for hard cuts)
- **NEW**: `strobe-white` (FLASH mode), `jump3-rgb`, `fade3-rgb` as dedicated
  presets matching the remote exactly
- **NEW**: `auto-cycle` — switches between presets every 8 seconds, like
  hitting AUTO on the remote

---

## 5. Disco / Spinning Party Light

### How it works
The owner's screenshot shows the classic rotating disco ball light: a faceted
dome (or mirror ball) with internal RGB LEDs. As it rotates, it throws
**dozens of small colored dots/beams** across walls and ceiling — red, green,
blue spots that sweep and rotate.

### Visual characteristics
- NOT a room wash — it's **discrete spots** of saturated color on surfaces
- Spots rotate around the room (typically 1–3 RPM)
- Colors: primarily red, green, blue (separate LEDs, not mixed)
- Between spots: room stays dark
- The light fixture itself glows and is a visual focal point
- Motion is mechanical-steady, not organic

### For 2D animation (effect: `disco-party`)
This needs a different approach than a color grade — it's an **overlay effect**:
1. Base: dark room grade (low brightness, desaturated)
2. Overlay: animated colored dots (radial gradients, screen/add blend mode)
   - ~30-50 dots, red/green/blue
   - Dots orbit around a center point over time
   - Dot size pulses slightly
3. Implementation: generate as a separate animated overlay layer in Natron,
   or as an ffmpeg `geq` expression (expensive — better as pre-rendered loop)

For the pipeline: `disco-party` is a two-pass effect. Pass 1: dark grade.
Pass 2: composite the rotating dot overlay. Documented as a Natron setup
until we build the ffmpeg version.

---

## 6. 2D Animation Lighting Techniques (Studio Research)

### How the pros fake 3D light in 2D

**Light pools (the #1 technique)**
- Paint the scene dark, then "cut out" pools of light where sources hit
- In compositing: black multiply layer with soft-edged holes (radial gradients)
  at each light source position, set to Screen or Add
- Katana Zero / indie games use this exact method with subtract blend modes
- For Cape Jones: draw the room normally, overlay a dark violet multiply layer,
  punch light pools with radial gradients where the LED strips are

**Warm/cool contrast (the Ghibli rule)**
- Shadows: blue-greens, blue-violets, deep blues
- Highlights: desaturated yellows, warm ambers, rich reds
- NEVER shadow with black — always with a cool color
- Light source color determines highlight hue; ambient determines shadow hue
- This is already the philosophy behind our grade families

**Rim light as light-source storytelling**
- The show bible already locks this: rim light color = environment light color
- Under orange bulb: orange rim. Under blacklight: violet-blue rim.
- This single rule sells the lighting more than any grade

**Volumetrics / atmosphere**
- Light beams, dust motes, haze — drawn as soft translucent shapes
- Under a streetlight: a cone of slightly-lighter air with floating dust
- Under disco light: no volumetrics (spots are too small/fast)
- Cheap to draw, massive atmosphere payoff

**Day-for-night (the film trick, adapted)**
- Take a day scene → crush highlights, push blue, keep light sources true
- For animation: the "dusk for night" variant keeps practical lights
  (streetlights, windows) reading correctly while everything else goes blue

**Selective saturation (the colorist's scalpel)**
- Instead of grading the whole frame, target specific hues
- Example: purple streetlight grade = crush red/yellow saturation, boost blue
- ffmpeg `hue` + `eq` per-channel, or `colorchannelmixer` (what we use)

**What anime does for night streetlight scenes**
- Deep blue base (#1a2340 range), warm orange practical lights
- Light pools are HARD-edged near the source, soft at distance
- Characters under streetlight: top-lit warm, everything else blue shadow
- Reflections on wet ground: vertical streak of the light color (easy win)

### Cape Jones lighting rules (production)
1. Every light source gets a color. Every rim light matches it.
2. Shadows are always a cool color, never black.
3. The white suit is the "light meter" — it shows the audience exactly
   what color the light is. Protect this readability.
4. One dominant source per shot. Two max. More = mud.
5. Animated lights (LED, disco, strobe) animate the GRADE, not the drawing.
   The drawing stays clean; the light moves in post.

---

## Reference Images

Saved in `docs/lighting/references/`:
- (Owner's screenshots — the 10 bulb/lighting reference images he sent 2026-10-16)
- Purple streetlight examples (to be captured)
- Blacklight room examples (to be captured)

## Grades Built From This Research

| Grade | Source | File |
|---|---|---|
| `purple-streetlight` | Defective LED streetlights | grades.py |
| `blacklight-purple` | UV blacklight rooms | grades.py |
| `bulb-orange` | Orange LED party bulb | grades.py |
| `bulb-yellow` | Yellow bug/vintage bulb | grades.py |
| `bulb-red` | Red sleep/darkroom bulb | grades.py |
| `bulb-purple` | Purple LED bulb | grades.py |
| `bulb-green` | Green LED bulb | grades.py |
| `disco-party` | Spinning RGB party light | grades.py (base) + Natron |

## Animated Presets Built From This Research

| Preset | Remote mode | File |
|---|---|---|
| `strobe-white` | FLASH | led_controller.py |
| `jump3-rgb` | JUMP3 | led_controller.py |
| `jump7-color` | JUMP7 | led_controller.py |
| `fade3-rgb` | FADE3 | led_controller.py |
| `auto-cycle` | AUTO | led_controller.py |
| `blacklight-flicker` | (UV mains flicker) | led_controller.py |
