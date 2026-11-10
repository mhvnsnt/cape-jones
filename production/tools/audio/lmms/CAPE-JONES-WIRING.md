# LMMS — Cape Jones Wiring

**What:** LMMS (Linux MultiMedia Studio) — free cross-platform music-production DAW.
**Slot:** **MUSIC COMPOSITION** — hand-composed beats, melodies, basslines, arrangements.
**Upstream:** https://github.com/lmms/lmms · pinned @ 4fde529fb37115c327daadac8506870e92724f3a
(HEAD 2026-10-19, 10,522 stars, not archived)
**License:** GNU GPL v2 (own-eyes verified on LICENSE.txt in this tree — the full
"GNU GENERAL PUBLIC LICENSE Version 2, June 1991" text). Free + commercial ✅
(same bar as Audacity/Glaxnimate/Flowblade).
**Location in repo:** `production/tools/audio/lmms/` (64MB, 4537 files, code-only;
0 binaries >50MB; stock sound library in `data/` kept — small presets/samples).
**Submodules intentionally empty:** 16 upstream submodules (`plugins/ZynAddSubFx/zynaddsubfx`,
`plugins/FreeBoy/game-music-emu`, `plugins/OpulenZ/adplug`, `plugins/Xpressive/exprtk`,
`src/3rdparty/jack2`, `doc/wiki`, etc.) were NOT initialized in this vendored tree
(build-time `git submodule update --init --recursive` fetches them upstream).

## Chain position (audio pipeline)

```
[compose] LMMS  ──stems/mix──┐
[generate] ACE-Step (music AI) ──stems──┤
[dialogue] tts → rvc → lipsync ────────┤
[sfx] mmaudio (video→foley) ────────────┤
                                         ▼
                              Audacity (edit/mix/master)
                                         ▼
                              Flowblade/melt (picture lock)
```

The audio chain already had AI **music generation** (ACE-Step) but no interactive
**music composition**. LMMS closes it: compose by hand, generate with ACE-Step, or
arrange ACE-Step stems inside LMMS. MIDI sequencing is the canonical input —
human performance/notation feeding the same downstream mix as the AI assets.

## Setup

```bash
# Dependencies (Debian/Ubuntu); vcpkg.json covers the Windows path
sudo apt install qtbase5-dev qttools5-dev qttools5-dev-tools libqt5svg5-dev \
  libsndfile1-dev libfftw3-dev libasound2-dev libpulse-dev libsdl2-dev \
  libxft-dev libxinerama-dev libxcb-util-dev libjack-jackd2-dev \
  libfluidsynth-dev libgig-dev libsoundio-dev stk wine wine-dev \
  libsamplerate0-dev libvorbis-dev libmp3lame-dev libmpg123-dev libogg-dev \
  libflac-dev libopus-dev libspeex-dev libstk0-dev libportaudio2 \
  portaudio19-dev liblrdf0-dev ladspa-sdk dssi-dev calf-plugins

git submodule update --init --recursive   # synth/plugin submodules (build-time only)
mkdir build && cd build && cmake .. && make -j$(nproc)
```

## Usage (headless batch — the automation story)

LMMS renders projects headlessly — the image equivalent of `melt`:

```bash
# Render a project to wav (no GUI):
lmms --render song.mmpz --output-format wav -o song.wav

# Render at specific sample rate / oversampling:
lmms --render song.mmpz -o song.wav --samplerate 48000 --oversampling 2

# Export a track's MIDI for interchange with other tools:
# (Song Editor → Export, or headless via --render with mid output)
```

Show-pipeline uses:
- **Theme/score composition:** write character themes, entrance music, stings as
  LMMS projects; render headlessly; stems → Audacity for dialogue ducking/mastering.
- **Beat backing for dialogue:** hip-hop beats under dialogue comps (owner's music world —
  beat-first workflow, not notation-first).
- **ACE-Step hybrid:** generate a motif with ACE-Step → import stems into LMMS →
  arrange/extend/humanize → render → downstream mix.
- **Sound-design loops:** synth patches (ZynAddSubFX, TripleOscillator) for
  whooshes/risers rendered to the SFX pool alongside mmaudio foley.

## Notes

- **GPL copyleft on the tool, not on your music:** compositions you create in LMMS
  are your own work. Distributing a *modified LMMS binary* triggers GPL source
  obligations; using it to make music does not.
- **Plugin licenses:** bundled synth submodules carry their own GPL-compatible
  licenses (ZynAddSubFX GPLv2+, Carla GPLv2+, GME LGPL) — all commercial-safe as tools.
- **No GPU needed:** LMMS is CPU-native — runs on this VM for smoke tests;
  heavy rendering still batchable anywhere.
- **Not to confuse with:** MuseScore (notation/engraving — the planned next pull
  in this slot), Ardour (linear multitrack — Audacity covers our DAW slot).
