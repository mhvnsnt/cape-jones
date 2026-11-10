# Production Science — the measured anatomy of a pro cartoon scene

*Companion to `production/dance-choreo/`. The choreography folder holds
**what** Darwin's dance is (the extracted keyframes). This folder holds
**how the scene works** — its sound, its timing math, and the production
machinery around it — measured from the same production files so Cape Jones
can be built to the same numbers. Commissioned 2026-11-02.*

**Scene under the microscope:** *The Amazing World of Gumball*, "The Words"
(GB214, season 2) — **Sc057** (wide hallway dance-strut, 198 frames) and
**Sc059** (twist close-up, 105 frames), both at **25 fps**, stage 1920×1080.

## The three studies

| Document | Question it answers | Headline numbers |
|---|---|---|
| [AUDIO-MAP.md](AUDIO-MAP.md) | How is the sound built, layered and synced? | One mono breakdown track per shot, cut to the exact frame count (44.1 kHz AIFF). Tempo **≈112 BPM**, beat = **13.4 frames**. The twist starts **on** an accent at frame 43. Working mix runs −16.6/−15.1 LUFS — mastering is a post job, not an animation job. |
| [MOVEMENT-MATH.md](MOVEMENT-MATH.md) | How fast does everything actually move? | Everyone is keyed **on twos** (83–92% of keyframes). Composite pose rates: lead **11–12.4/sec**, featured onlookers **10–11/sec**, background cast **6–8/sec**, extras ~1/sec. The twist: 27 keyframes on strict twos, frames 43–97. The camera approach is faked inside the puppet (head comp ×2.32 scale; screen area ×10.3). |
| [GAPS-AND-STANDARDS.md](GAPS-AND-STANDARDS.md) | What else does a production like this run on — and do we adopt it? | Ten aspects checked against file evidence: dope sheets (in-file as `chart` layers), bar sheets (`beat` layers), approved layout gate, versioned puppet library, color as a named stage, compositing, retakes/QC, broadcast loudness, field guides, sound breakdowns. Verdicts recorded per aspect. |

## Data (for rescanning)

- `data/movement-math.json` — every measured number in one machine-readable file.
- `data/movement-per-character.csv` — per-character rates, spacing profiles, holds.
- `data/audio-frame-rms.csv` — audio level for every frame of both tracks.
- `data/audio-events.csv` — every labeled audio/animation sync event, frame-precise.
- `chart-movement.svg` — one-page visual: pose rates per character, Darwin's
  approach growth curve, Sc057's accent map against the beat grid.
- `audio/GB214_WORDS_057_track.wav` / `audio/GB214_WORDS_059_track.wav` — the
  per-shot production tracks, recovered bit-exact from the FLAs (44.1 kHz,
  16-bit, mono). The only separable audio objects in the files.

## Vocabulary used across all three documents

- **pose change** — a frame where at least one part of a puppet gets a new
  authored keyframe state. **poses/sec** = pose changes per second of scene time.
- **on ones / twos / threes** — a keyframe held for 1 / 2 / 3 frames.
- **beat grid** — the measured pulse of the track: at 25 fps and ~112 BPM,
  one beat = 13.4 frames; **phrase figure** = the two-hit accent pattern
  repeating every 4 beats (~54 frames).
- **breakdown track** — the per-shot mono mix the sound/editorial department
  cuts for animators before animation begins.
- **chart layer / beat layer** — the in-FLA descendants of the paper dope
  sheet and bar sheet.

## Method in one paragraph

Everything was measured from the production files themselves: the FLA/XFL
documents (library items, layer/keyframe structure, media metadata, source
paths), the SWFs' tag structure (sound stream layout), the FLAs' internal
media stores (the original per-shot AIFF samples, recovered bit-exact), the
choreography JSON from `production/dance-choreo/`, and the rendered HD
frames (for Darwin's on-screen size). Where a number could not be measured,
the documents say so — e.g. the layout movies' embedded audio is documented
from its file metadata because its internal storage format could not be
decoded with the tools on hand.
