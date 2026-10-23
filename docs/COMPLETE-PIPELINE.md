# Cape Jones Complete Pipeline — "Studio in a Box"

**One command. FlipaClip drawings in. Finished animation out.**

```bash
production/pipeline/cape_jones_pipeline.sh input.mp4 output.mp4 [options]
```

---

## Full Pipeline Flow

```
Storyboarder → animatic_builder.py → timed animatic
  → [keyframes] → ToonComposer / ToonCrafter (Kaggle GPU) → animation
  → scene_aware_interp.py → black-frame-safe interpolation
  → TheAnimeScripter → anime upscale/restore (optional)
  → anime_fx.py → speed lines / impact frames / screen shake
  → retro_fx.py → VHS/CRT retro look (optional)
  → energy_blast.py → wrist blaster VFX
  → stroke_reveal.py → neon write-on effects
  → led_scene_assembler.py → LED remote scenes (3 frames → full scene)
  → finish.py → QC + color grade + LED preset + audio mix + encode
  → social_export.sh → TikTok / Shorts / Instagram delivery
```

**Batch mode:** `batch_process.sh <input_dir> <output_dir> [grade] [led_preset]` — runs the full pipeline on every video in a folder.

---

## Pipeline Stages (detail)

| Stage | Tool | What it does |
|-------|------|--------------|
| 0. Animatic | `animatic_builder.py` | Storyboard images + timing CSV → timed 1080p MP4 with temp audio |
| 1. Denoise | ffmpeg hqdn3d + deflicker | Removes phone camera noise, stabilizes flicker |
| 2. Line cleanup | `cleanup_lines.py` (OpenCV) | Smooths noise, crisps lines, preserves fills |
| 3. Interpolation | RIFE / ToonCrafter / ToonComposer | 12fps → 24fps AI inbetweening (see below) |
| 3b. Scene-aware | `scene_aware_interp.py` | Strips black separator frames BEFORE interpolation |
| 4. De-ghost | `deghost.py` | Removes interpolation ghosting on flat colors |
| 5. Upscale | Lanczos / ESPCN / RealESRGAN-anime | 2x resolution boost |
| 6. Sharpen | ffmpeg unsharp + color punch | Final detail enhancement |
| 7a. Anime FX | `anime_fx.py` | Speed lines, impact flash, screen shake |
| 7b. Retro FX | `retro_fx.py` | VHS tracking, CRT scanlines, chromatic aberration |
| 7c. Energy blast | `energy_blast.py` | Wrist blaster VFX (beam/rings/freeze/burst) |
| 7d. Stroke reveal | `stroke_reveal.py` | Neon write-on (scary face gag, chalkboard) |
| 7e. LED scene | `led_scene_assembler.py` | 3 frames → full LED remote scene |
| 7f. LED lighting | `led_controller.py` | 15 animated LED presets |
| 8. QC | `finish.py` | Automated quality checks |
| 9. Color grade | `grades.py` (32 grades) | Signature Cape Jones look |
| 10. Audio mix | `finish.py` | Music + SFX mixing |
| 11. Encode | `finish.py` | Web/broadcast/master presets |
| 12. Social | `social_export.sh` | TikTok 9:16, IG 1:1, IG 4:5 |

---

## Interpolation Options

| Method | Speed | Quality | When to use |
|--------|-------|---------|-------------|
| **RIFE** (default) | ~26s/pair CPU, 1.3min/216 pairs GPU | Good, some ghosting on flat colors | General use |
| **ToonCrafter** | 2-3hr/105 pairs GPU (tuned: 30-45min) | Best for cartoons, generative | Hero shots, important scenes |
| **ToonComposer** | ~5min/81 frames GPU | Keyframe → full shot, 3.4s per 2 keyframes | Draw 2 frames, get a shot |
| **Fast** (ffmpeg) | Seconds | Preview quality | Quick checks |

**GPU rule:** Heavy lifting goes to Kaggle T4 (30 hrs/week). Never say "no GPU."

**Black frame rule:** ALWAYS strip black separator frames before interpolation (`scene_aware_interp.py` or manually). Feeding black frames to an interpolator produces flashing/ghosting.

---

## ToonComposer — Keyframe Workflow

ToonComposer generates 81 frames (3.4s @ 24fps) from 2+ keyframes. You draw the moments, AI draws the movement.

**Controls:**
1. **Frame count** — how long the shot is (24=short, 48=medium, 81=max)
2. **Keyframe placement** — which frame number each drawing lands on
3. **Text prompt** — describe the action ("face shifts from tired to surprised")
4. **CFG scale** — how strongly to follow the prompt

**Episode math:** 5 min = 7,200 frames. At ~3.4s per 2 keyframes, ~88 shots (~176 keyframes) = a full episode. You're not drawing 7,200 frames.

---

## Color Grades (32)

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

**Real lighting** (from owner's 2026-10-16 research):
- `purple-streetlight` — the defective phosphor-delamination streetlight look
- `blacklight-purple` — UV blacklight, white suit glows blue-white
- `bulb-orange`, `bulb-yellow`, `bulb-red`, `bulb-purple`, `bulb-green` — colored LED bulbs
- `disco-party` — spinning disco ball light

**LED references:** `led-chill-blue`, `led-deep-purple`, `led-ember`, `led-ghost-teal`, `led-party`, `led-sunset`, + more

---

## LED Presets (15 animated)

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
| `strobe-white` | White flash strobe | Impact moments |
| `jump3-rgb` | RGB jump (real remote mode) | — |
| `jump7-color` | 7-color jump (real remote mode) | — |
| `fade3-rgb` | RGB fade (real remote mode) | — |
| `auto-cycle` | Auto mode (real 44-key remote) | — |
| `blacklight-flicker` | UV flicker | Blacklight scenes |
| `streetlight-hum` | Defective purple streetlight | Outside night |

**Canon:** Ghost cave LED is locked to `ghost-mode`. He never changes it.
**The remote** is a story prop — he hits a button, room changes, acts like nothing happened.
**`--speed`** multiplier on all presets.

---

## Effects

### Anime FX (`anime_fx.py`)
```bash
python3 anime_fx.py --speed-lines -o out.mp4              # radial manga speed lines
python3 anime_fx.py --impact --frames 5 -o out.mp4        # impact flash + starburst
python3 anime_fx.py --shake-input in.mp4 -o out.mp4       # screen shake for hits
python3 anime_fx.py --speed-overlay in.mp4 -o out.mp4     # speed lines over video
```

### Retro FX (`retro_fx.py`)
```bash
python3 retro_fx.py --vhs -o out.mp4 in.mp4               # VHS tracking + noise
python3 retro_fx.py --crt -o out.mp4 in.mp4               # scanlines + phosphor glow
python3 retro_fx.py --vhs --crt --intensity 0.7 -o out.mp4 in.mp4
```

### Energy Blast (`energy_blast.py`)
For Cape Jones wrist blasters. Canon colors: white core, yellow/cyan corona.
```bash
python3 energy_blast.py --type beam --duration 2.0 --output blast.mp4
python3 energy_blast.py --type beam --base input.mp4 --x 540 --y 960 --output out.mp4
```
Types: `beam` (force beam), `rings` (stun rings), `freeze` (ice ray), `burst` (radial)

### Stroke Reveal (`stroke_reveal.py`)
Neon write-on animation. For scary face/mask gag, chalkboard effects.
```bash
python3 stroke_reveal.py drawing.png output.mp4 --strokes strokes.json --glow-color cyan --duration 3.0
```

### LED Scene Assembler (`led_scene_assembler.py`)
3 frames → full LED remote scene. Color changes sync on thumb press.
```bash
python3 led_scene_assembler.py sit.png press.png release.png \
  --sequence purple-pulse chill-blue ember-glow ghost-mode \
  --party rainbow-smooth --duration 2 --party-duration 15 \
  --output led_scene.mp4
```

### Chowder Patterns
Greenblatt's fixed-pattern technique. Character has holes, moves over static pattern. Authentic Chowder look.

---

## AI Body Replacement

**Viggle-Animate** (open-source, Kaggle T4): `production/ai-body-replace/`
- Upload driving video (you doing motion) + character image
- Get character performing your exact motion
- Free, unlimited, no paywalls

**Other tools:** `~/workspace/tools/body-replace/` — motion-mirror, mimicmotion, musepose, dwpose (CPU)

---

## Lip Sync

- **LatentSync** (ByteDance) — AI lip sync on animated characters, Kaggle GPU
- **OpenFaceFX** (CPU) — audio + transcript → viseme curves → OpenToonz/Tahoma2D
- **MuseTalk** — backup option

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

**Vector parts:** raster → SVG via vtracer
- For puzzle-piece assembly from Space Ghost EPS sheets

**Model sheet cutting:** rembg + Inkscape pipeline

**Rigs:** Tahoma2D (cutout), Blender Grease Pencil (2D in 3D space)

**Assembly methods:**
- **Puzzle-piece** (old-school): pieces slot into cutouts, automated fitting
- **Stacking** (new): character on top of cape, no cutout alignment

---

## 3D Segments

**Living room scene:** `~/workspace/cape-jones-build/3d-assets/living_room.blend`
- Full room, furniture, LED strips (color-animated), LED remote on coffee table
- 15s LED cycle: purple → blue → red → green → party → purple

**Rig script:** `rig_cape_jones.py` — imports Tripo3D GLB, builds 17-bone armature, sitting pose

---

## Environments

**House design:** `docs/environments/HOUSE-DESIGN.md`
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

**Social export** (`social_export.sh`):
```bash
bash social_export.sh finished.mp4 out/                    # all presets
bash social_export.sh finished.mp4 out/ tiktok            # just TikTok
bash social_export.sh finished.mp4 out/ tiktok --focus-top # bias crop up
```

---

## Quick Reference

```bash
# List everything
python3 finish.py --list-grades
python3 led_controller.py --list

# Basic finished segment
bash cape_jones_pipeline.sh in.mp4 out.mp4 --grade cj-royal --audio music.mp3

# LED scene from 3 frames
python3 led_scene_assembler.py sit.png press.png release.png \
  --sequence purple-pulse chill-blue ember-glow --party rainbow-smooth \
  --output led_scene.mp4

# Batch process a folder
bash batch_process.sh input_dir/ output_dir/ cj-night purple-pulse

# Social delivery
bash social_export.sh finished.mp4 social_out/
```

---

## Tool Locations

| Category | Repo path | Local path |
|----------|-----------|------------|
| Pipeline scripts | `production/pipeline/` | `~/workspace/tools/post-pipeline/` |
| Kaggle notebooks | `production/kaggle/` | `~/workspace/cape-jones-build/kaggle-*/` |
| AI body replace | `production/ai-body-replace/` | `~/workspace/cape-jones-build/kaggle-viggle/` |
| Tripo pull tool | `production/tools/tripo-pull/` | `~/workspace/tools/tripo-pull/` |
| Color/lighting | `production/pipeline/grades.py`, `led_controller.py` | same |
| Docs | `docs/` | `~/workspace/cape-jones-build/` |

## Kaggle GPU Queue — Bulletproof Render Pipeline

**Never lose a render again.** `production/pipeline/kaggle_queue.py` manages all
Kaggle GPU jobs with automatic bulletproof saving and claim verification.

```bash
# Add a job (bulletproof saving ON)
python3 production/pipeline/kaggle_queue.py add \
  --notebook production/kaggle/tooncrafter/cape_jones_tooncrafter_kaggle.ipynb \
  --title "Cape Jones ToonCrafter expressions" \
  --save-dataset marsfmmg/cape-jones-tooncrafter-outputs \
  --outputs "cape-jones-expressions-TOONCRAFTER-24fps.mp4" \
  --gh-repo mhvnsnt/cape-jones --gh-release-tag tooncrafter-v1

# Queue commands
python3 production/pipeline/kaggle_queue.py tick      # one pass (systemd timer runs every 15 min)
python3 production/pipeline/kaggle_queue.py status    # show all jobs
python3 production/pipeline/kaggle_queue.py hold "reason"  # pause new starts
python3 production/pipeline/kaggle_queue.py release   # resume
python3 production/pipeline/kaggle_queue.py retry <job-id>
```

**What the queue does automatically (CHECK-RESEARCH-WIRE-DO):**

1. **CHECK** — `validate_job()` before every push: notebook exists, all code
   cells compile, title resolves to the kernel slug (Kaggle API 400s otherwise),
   dataset slugs are well-formed. Invalid jobs fail fast with a clear error —
   never a wasted GPU run.

2. **WIRE (bulletproof saver)** — Every pushed notebook gets:
   - `save_outputs.py` shipped alongside it in the kernel
   - A saver-setup cell injected after the leading markdown (imports
     `RenderSaver`, starts the watchdog if `KAGGLE_SAVE_DATASET` is set)
   - A final-checkpoint cell as the last cell (checkpoints expected outputs)
   - `KAGGLE_SAVE_DATASET` env var set from `--save-dataset`

   **Why:** Kaggle "Quick Save" does NOT preserve `/kaggle/working` files —
   only "Save & Run All" (commit) does. The 2026-10-16 incident lost 4 render
   chunks (16+ GPU hours) to this. The in-kernel saver publishes a Kaggle
   dataset version after EVERY checkpoint via `kaggle datasets version`
   (kernels are pre-authenticated as the notebook owner — no secrets needed).
   Dataset versions survive session death. Quick Save doesn't.
   Full research: `docs/research/KAGGLE-SAVE-RESEARCH.md`.

3. **VERIFY** — When a job completes, the completion report runs through
   `claim_gate.py` before the "done" notification goes out. Evidence = the
   downloaded output files. A blocked gate flags the job with
   `verification_warning` instead of silently reporting success.
   Full research: `docs/research/AGENT-CONFABULATION-RESEARCH.md`.

4. **Second copies** — After outputs download, they're pushed to GitHub
   releases and/or TeraBox (`--gh-repo`, `--gh-release-tag`, `--terabox-dir`).
   Credentials live on the VM, never in the kernel.

**Faster interpolation (2026):** `production/tools/ldf-vfi/` — LDF-VFI
(CVPR 2026, SOTA, Apache-2.0), pulled in as a ToonCrafter successor candidate.
Needs T4 validation before replacing ToonCrafter in the queue.
Research: `docs/research/2026-SPEED-RESEARCH.md` (PR #46).

---

## Studio Architecture — How Everything Connects

The full map: GPU lanes, orchestration, reliability, research, and dev tools
wired into one studio. **`docs/STUDIO-ARCHITECTURE.md`** is the canonical doc.

- **GPU lanes:** Kaggle (primary, queue-automated) → Colab (backup/parallel,
  `production/colab/`) → Lightning AI (tertiary). Same notebooks ported across
  lanes — a failing Kaggle job falls back to Colab with no code changes.
- **Orchestration:** `kaggle_queue.py` — validate → push (with bulletproof
  saver injected) → monitor → download → claim-gate → second copies
  (GitHub release / TeraBox).
- **Reliability (always on):** `claim_gate.py` blocks unverified "done";
  `verify_claim.py` checks files/PRs/releases; `contradiction_probe.py` asks
  "what would prove this false?"; `checkpoint_audit.py` finds stale work;
  `save_outputs.py` publishes dataset versions from inside every kernel.
- **Research:** `research.py` (never guess from training data) →
  `docs/research/` → pull in → wire up → PR. Master index:
  `docs/research/RESEARCH-INDEX.md`.
- **Dev tools:** Aider (terminal pair programmer, `.aider.conf.yml`),
  code-server (browser VS Code, phone-accessible), OpenCode/Gemini CLI
  (documented alternatives). Setup: `docs/research/DEVENV-SETUP.md`.
- **Config:** everything in the repo (see STUDIO-ARCHITECTURE.md §6).
  Queue *state* is the one VM-local exception (live operational state).
- **Failure recovery:** every component has a documented recovery path
  (STUDIO-ARCHITECTURE.md §7) — including Kaggle→Colab fallback and
  resume-from-dataset-version after session death.

**Order of operations (law):** CHECK → RESEARCH → WIRE → DO. Never reversed.

---

## Laws That Govern This Pipeline

- **NO-CHROMA-KEY-ON-ANIMATION** — AI matting only, never chroma key on characters
- **NO-HAND-TOOLING-EDITS** — Rebuild from clean state, never paint over
- **CHECK-HIS-COMPUTE-FIRST** — Kaggle GPU for heavy lifting, never say "no GPU"
- **ARCHIVE LAW** — Archive originals stay byte-identical; edits on copies only
- **THINK-BIG** — Production-grade, never prototype when he asked for production
- **BLACK-FRAME RULE** — Strip black separators before interpolation, always
- **VERIFY-BEFORE-CLAIMING** — Check the source of truth yourself; tag confidence
- **CHECK-RESEARCH-WIRE-DO** — Check first, research the gap, wire the fix, then do
- **NEVER-QUICK-SAVE** — Quick Save preserves zero output files; bulletproof saver or Save & Run All only

## EP01 V6 + 60fps Final (2026-10-23)

- **Root cause of the v5 leftovers:** the detector's white-fraction guard (frac < 0.4) rejected exactly the suit-overlap frames — the viggle.ai watermark sat on his white suit at left torso ~35–57.5s and right ~101.5–103s / ~106.5–108.5s / ~127.5–129.5s / ~135–136s. (Failure mode addendum: `production/watermark-removal/README.md`, PR #218.)
- **v6 LaMa re-pass** with glyph-only detection ran on the v5 clean master (kernel marsfmmg/cape-jones-wm-v3); fill counts 1307L/2495R matched the independent relaxed scan exactly.
- **Own-eyes verified** clean at every former failure window (102s cape edge, 108s, 128s legs, 37s torso, 54s torso, 18.5s) — watermark gone, line art intact.
- **METRIC CONFOUND (lesson):** the glyph score reads 0.5–0.99 over plain white costume even when fully clean — over bright subjects only EYES adjudicate, never the score alone.
- **RIFE rebuilt on v6** (kernel marsfmmg/cape-jones-rife-v6): 5009→10017 frames, 60fps, 166.96s, audio muxed; spot frames verified.
- **Files:** final phone copy `cape-jones-EP01-FINAL-60fps-phone.mp4` (52MB); masters live on Kaggle (datasets marsfmmg/cape-jones-episode-v5-wm + cape-jones-v6-clean-rife) — treat Kaggle as the masters' home, local as cache.
- **LIP SYNC:** owner removed it from EP01 (2026-10-21) — do NOT chase timestamps for EP01.
