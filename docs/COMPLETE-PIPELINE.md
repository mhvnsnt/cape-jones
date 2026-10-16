# Cape Jones Complete Pipeline — "Studio in a Box"

**One command. FlipaClip drawings in. Finished animation out.**

```bash
~/workspace/tools/post-pipeline/cape_jones_pipeline.sh input.mp4 output.mp4 [options]
```

---

## Pipeline Stages

| Stage | Tool | What it does |
|-------|------|--------------|
| 1. Denoise | ffmpeg hqdn3d + deflicker | Removes phone camera noise, stabilizes flicker |
| 2. Line cleanup | `cleanup_lines.py` (OpenCV) | Smooths noise, crisps lines, preserves fills |
| 3. Interpolation | RIFE / ToonCrafter / ffmpeg | 12fps → 24fps AI inbetweening |
| 4. De-ghost | `deghost.py` | Removes interpolation ghosting on flat colors |
| 5. Upscale | Lanczos / ESPCN / RealESRGAN-anime | 2x resolution boost |
| 6. Sharpen | ffmpeg unsharp + color punch | Final detail enhancement |
| 7a. Energy blast | `energy_blast.py` | Wrist blaster VFX (beam/rings/freeze/burst) |
| 7b. LED lighting | `led_controller.py` | 8 animated LED presets |
| 8. QC | `finish.py` | Automated quality checks |
| 9. Color grade | `grades.py` (24 grades) | Signature Cape Jones look |
| 10. Audio mix | `finish.py` | Music + SFX mixing |
| 11. Encode | `finish.py` | Web/broadcast/master presets |

---

## Interpolation Options

| Method | Speed | Quality | When to use |
|--------|-------|---------|-------------|
| **RIFE** (default) | ~26s/pair CPU, 1.3min/216 pairs GPU | Good, some ghosting on flat colors | General use |
| **ToonCrafter** | 2-3hr/105 pairs GPU | Best for cartoons, generative | Hero shots, important scenes |
| **Fast** (ffmpeg) | Seconds | Preview quality | Quick checks |

**GPU rule:** Heavy lifting goes to Kaggle T4 (30 hrs/week). Never say "no GPU."

---

## Color Grades (24)

**Signature** (whites protected per model-sheet law):
- `cj-day` — Default. Punchy cartoon, violet cowl pop.
- `cj-night` — Dark variant for night scenes and ghost cave.
- `cj-trippy` — Saturated for trippy backgrounds.

**Model-sheet families:**
- `cj-royal` — Deep violet wash. Cape Jones in his element.
- `cj-ocean` — Cyan/blue beach vibe.
- `cj-ember` — Red/orange intensity.
- `cj-gold` — Warm victory/power-up glow.
- `cj-ghost` — Spooky green-teal. Supernatural.
- `cj-beach-day` — Bright Halloween-on-the-beach.
- `cj-beach-sunset` — Orange/pink golden hour.

**Outside/creative:**
- `outside-noir`, `outside-acid`, `outside-dusk`, `outside-storm`

**LED references:** `led-chill-blue`, `led-deep-purple`, `led-ember`, + 3 more

---

## LED Presets (8 animated)

Like a real RGB strip controller. Time-varying color washes.

| Preset | Effect | Default for |
|--------|--------|-------------|
| `purple-pulse` | Heartbeat breathe | Living room (his default) |
| `chill-blue` | Slow fade | Relaxed scenes |
| `sunset-cycle` | Orange→pink→purple | Evening vibe |
| `party-strobe` | Hard jump cuts | Party/funny moments |
| `ghost-mode` | Barely-perceptible teal drift | Ghost cave (locked) |
| `ocean-calm` | Gentle blue wave | Beach house |
| `ember-glow` | Fireplace flicker | Cozy/intimate |
| `rainbow-smooth` | Full spectrum cycle | Maximum chaos |

**Canon:** Ghost cave LED is locked to `ghost-mode`. He never changes it.
**The remote** is a story prop — he hits a button, room changes, acts like nothing happened.

---

## Effects

### Energy Blast (`energy_blast.py`)
For Cape Jones wrist blasters. Canon colors: white core, yellow/cyan corona.

```bash
# Standalone
python3 energy_blast.py --type beam --duration 2.0 --output blast.mp4

# Composite onto video at position
python3 energy_blast.py --type beam --base input.mp4 \
    --x 540 --y 960 --angle 0 --output out.mp4
```

Types: `beam` (force beam), `rings` (stun rings), `freeze` (ice ray), `burst` (radial)

### Stroke Reveal (`stroke_reveal.py`)
Neon write-on animation. For scary face/mask gag, chalkboard effects.

```bash
python3 stroke_reveal.py drawing.png output.mp4 \
    --strokes strokes.json --glow-color cyan --duration 3.0
```

### Chowder Patterns
`~/workspace/cape-jones-build/chowder-fx/` — Greenblatt's fixed-pattern technique.
Character has holes, moves over static pattern. Authentic Chowder look.

---

## Audio

**Soundtracks** (in repo: `docs/soundtracks/SOUNDTRACKS.md`):
- **Intro:** Nosferatu (1922) score
- **Outro/Action:** "Ghost Surf Rock" by Loyalty Freak Music
- **Trippy/Space:** "Orbiting Nebulas Grand Symphony" (StockTune, free)

**SFX Library:** `~/workspace/tools/sfx/` (organized by category)

**Mixing:** Built into pipeline via `--audio` and `--audio-volume`

---

## Character Building

**Vector parts:** `~/workspace/cape-jones-build/vector-workflow/raster_to_vector.py`
- vtracer: raster → SVG conversion
- For puzzle-piece assembly from Space Ghost EPS sheets

**Model sheet cutting:** rembg + Inkscape pipeline
- `~/workspace/tools/rembg-venv/` — AI background removal
- `~/workspace/tools/inkscape-1.4.4/` — vector editing

**Rigs:** Tahoma2D (cutout), Blender Grease Pencil (2D in 3D space)

**Assembly methods:**
- **Puzzle-piece** (old-school): pieces slot into cutouts, automated fitting
- **Stacking** (new): character on top of cape, no cutout alignment

---

## Rotoscoping / AI Body Replacement

**Pose extraction:** `~/workspace/tools/mocap/mediapipe_pose.py`
**Body replacement:** `~/workspace/tools/body-replace/` (various tools)

Owner films himself → pose extracted → Cape Jones mapped onto motion.

---

## Environments

**House design:** `docs/environments/HOUSE-DESIGN.md` (in cape-jones repo)
- ATHF-vibe boring exterior, living room with LEDs, ghost cave behind bookshelf

**Mixed media:** `docs/environments/MIXED-MEDIA-GUIDE.md`
- Gumball method: 2D characters on real photo backgrounds
- Ed Edd n Eddy: expressive non-realistic color philosophy
- Chowder: pattern fills for environments

---

## Delivery Presets

| Preset | CRF | Use for |
|--------|-----|---------|
| `web` | 23 | Social media, quick sharing |
| `broadcast` | 18 | High quality, episodes |
| `master` | 12 | Archive, further editing |

---

## Quick Reference

```bash
# List everything
cape_jones_pipeline.sh --list-grades
cape_jones_pipeline.sh --list-led

# Basic finished segment
cape_jones_pipeline.sh in.mp4 out.mp4 \
    --grade cj-royal --audio music.mp3

# Full production with effects
cape_jones_pipeline.sh in.mp4 out.mp4 \
    --grade cj-trippy --led party-strobe \
    --blast beam --blast-x 540 --blast-y 960 \
    --audio nebulas.mp3 --preset broadcast

# Vibe segment (LED loop, no one is animated but the lights)
cape_jones_pipeline.sh in.mp4 out.mp4 \
    --grade cj-night --led purple-pulse --led-speed 0.5 \
    --audio nosferatu.mp3 --preset web
```

---

## Tool Locations

| Category | Path |
|----------|------|
| Pipeline scripts | `~/workspace/tools/post-pipeline/` |
| Interpolation | `~/workspace/tools/rife-v46/`, `~/workspace/tools/tooncrafter/` |
| Color/lighting | `~/workspace/tools/post-pipeline/grades.py`, `led_controller.py` |
| Effects | `~/workspace/tools/post-pipeline/energy_blast.py`, `stroke_reveal.py` |
| Audio | `~/workspace/tools/sfx/`, `~/workspace/cape-jones-build/music/` |
| Character | `~/workspace/cape-jones-build/vector-workflow/` |
| Body replace | `~/workspace/tools/body-replace/` |
| Mocap | `~/workspace/tools/mocap/` |
| Upscale models | `~/workspace/tools/upscale-models/` |
| Kaggle notebooks | `~/workspace/cape-jones-build/kaggle-rife/`, `kaggle-tooncrafter/` |

---

## Laws That Govern This Pipeline

- **NO-CHROMA-KEY-ON-ANIMATION** — AI matting only, never chroma key on characters
- **NO-HAND-TOOLING-EDITS** — Rebuild from clean state, never paint over
- **CHECK-HIS-COMPUTE-FIRST** — Kaggle GPU for heavy lifting, never say "no GPU"
- **ARCHIVE LAW** — Archive originals stay byte-identical; edits on copies only
- **THINK-BIG** — Production-grade, never prototype when he asked for production
