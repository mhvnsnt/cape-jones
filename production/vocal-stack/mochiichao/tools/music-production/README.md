# Mochiichao Music Production — how the official title/intro tracks were made

This folder is the reproducible production process for the official tracks.
It is the exact method used in the Title Music lane, 2026-10-25, not a summary
written after the fact. The rendered WAVs that ship in the game are in
`public/audio/`; this folder is how they were built, so a later version can be
rebuilt, changed, and re-rendered the same way.

## Official tracks (Mars, 2026-10-25 ~22:48 CDT)

- Title: `public/audio/mochiichao-title-v3.wav` — OFFICIAL
- Intro: `public/audio/mochiichao-intro-v3.wav` — OFFICIAL

v2 files (`mochiichao-title-v2.wav`, `mochiichao-intro-v2.wav`) are LOCKED
DRAFTS: kept on main, not deleted, not wired as final. v1 files are drafts.
Boot = UI Art Option B. Press-start = M3 "Mochii Chirp". See
`docs/title-music-status.md` for the full chosen/draft table.

## Tools (all open source, used locally to render only — none shipped here)

- FluidSynth 2.3.4 (LGPL) — open SoundFont sampler.
- FluidR3_GM.sf2 — GM soundfont, Debian package `fluid-soundfont-gm`
  (142 MB, in `/usr/share/sounds/sf2/` on the build machine, NOT shipped).
- mido — open-source Python MIDI library, in a workspace venv
  (`python3 -m venv venv && venv/bin/pip install mido`).
- ffmpeg — stem mixing, EQ, compression, limiting, trimming, fades.
- Python 3 + numpy — waveform analysis (per-bar RMS/peak).

## Steps, in order

1. Research first, from the real game files. FireRed decomp MIDI, in the repo:
   `pokefirered-leafgreen/sound/songs/midi/mus_title.mid` and
   `mus_new_game_intro.mid`. Only aggregate structure was taken (tempo,
   track count, note counts, velocity ranges, density per bar, climax
   placement, intro sparsity). No Pokemon melody, note sequence, cry, or
   sample was copied, transcribed, or shipped.
2. v1 (PR #36): hand-coded Python waveform synth. Mars: title and intro
   "really suck", upgrade them, research how Pokemon does title/intro.
   Lesson recorded: do not hand-tool the synth again.
3. v2 (`compose_v2_midi.py`): original MIDI in D major with mido.
   Title: 140 BPM, 24 bars, 8 layers, 808 notes. Intro: 120 BPM, 12 bars,
   lead only 10 long notes, ends on A (dominant) → title D (tonic).
   Rendered with FluidSynth, no reverb/chorus, trimmed to exact bar length
   with a 0.2 s end fade. PR #59. Mars liked v2 and locked it as drafts.
4. v3 (`compose_v3.py`): layer ON TOP of v2, do not replace it. The script
   loads the v2 MIDI tracks exactly and appends new tracks.
   Title adds 580 notes: distortion guitar (GM 30), saw synth (81),
   synth brass (62), church organ (19, from phi bar 15), sub-bass (39),
   hip-hop drums. Intro adds 123 notes: distortion guitar, sub-bass,
   hip-hop drums only — no organ, no synth, per Mars.
   Golden ratio: phi bar = ceil(0.618 × bars) → title bar 15, intro bar 8.
   Those bars get the fullest hit (crash + all layers).
5. Stem mix (`render_mix_v3.sh`): render each layer group as its own stem
   MIDI (see `stem-*.mid`), then mix with ffmpeg:
   melody highpass 80 Hz; bass lowpass 250 Hz, vol 1.1; drums highpass
   40 Hz +2 dB at 5 kHz; guitar highpass 150 Hz +3 dB at 3 kHz, vol 0.9;
   synth highpass 200 Hz, vol 0.8; organ lowpass 5,000 Hz, vol 0.7.
   Master: compressor threshold -18 dB, ratio 2:1, attack 10 ms,
   release 100 ms; limiter 0.89 (-1 dB); final 0.2 s end fade to sample 0.
   PR #70. Mars: "those are awesome", make them official.
6. Verify before any PR: duration = exact bar multiple, 44,100 Hz, stereo,
   16-bit, first/last sample 0, peak under the limiter, per-bar RMS/peak
   measured (see `docs/title-music-v3-spec.md` for the numbers).

## Reproduce it

```bash
python3 -m venv venv && venv/bin/pip install mido
venv/bin/python compose_v2_midi.py      # writes mochiichao-*-v2.mid
venv/bin/python compose_v3.py           # loads v2 MIDI, writes v3 + stem MIDIs
bash render_mix_v3.sh                   # renders stems with FluidSynth, mixes with ffmpeg
```

Notes on the scripts as shipped: `compose_v2_midi.py` and `compose_v3.py`
write to the `OUT` directory set at the top of each file, and
`render_mix_v3.sh` changes into its own directory. Point those at your
checkout before running. The SoundFont path in the render script is the
Debian path above; change it if your soundfont lives elsewhere. Do not
ship the SoundFont itself in this repo.

## What NOT to do, from this production's own history

- Do not re-use the v1 hand-coded waveform synth for a new version.
- Do not ship a Pokemon melody, cry, sample, or direct_sound_sample file.
- Do not wire a draft as final. Wiring is a separate, explicit step, and
  the status doc (`docs/title-music-status.md`) is the authority on what
  is official vs draft at any time.
- Do not delete v1/v2 when a new version lands. New versions are new
  files; old versions stay as drafts/options unless Mars names a deletion.
