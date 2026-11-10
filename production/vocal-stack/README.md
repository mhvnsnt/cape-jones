# The vocal stack (brought over from Mochiichao, 2026-10-29)

Owner order: the Cape Jones dance song is sung with the Avanna / Vocaloid-style
vocal stack that lives in the Mochiichao repo. This folder is that stack,
copied over so Cape Jones production owns a copy. Source of truth stays the
Mochiichao repo; paths below are its exact repo paths.

## Where it lives in Mochiichao (verified by full-tree search, 2026-10-29)

- `tools/music-production/` — the working stack:
  - `avanna_style.py` — Avanna-style transform (WORLD vocoder; F0 shift,
    formant shift, breath reduction). Header states the rule: no Avanna
    voicebank is used, copied, or shipped — it transforms a guide vocal.
  - `avanna_style_autotune.py` … `avanna_style_autotune_v7.py` — WORLD +
    autotune generations.
  - `rubberband_autotune_v1.py` — the current lead method (v19): per-note
    Rubber Band autotune, feminine shift decoupled from pitch. No WORLD
    resynthesis on the lead.
  - `build_vocal_mix.sh` … `build_vocal_mix_v19.sh` — 19 generations of the
    vocal mix build (layering: lead / harmony / octave / overdub, presence
    EQ stack, de-esser, slapback, bit-crush parallel, master numbers).
  - `pedalboard_master.py`, `measure_lead_mix.py`, `reverse_engineer.py`,
    `README.md`, `ai-mixing-mastering-research.md`,
    `free-plugins-and-genre-research.md`.
- `show/production/tooling/music-wave/` — the digicore chain lane:
  `VOCAL-CHAIN-DIGITAL-FAIRY-YAMEII-DEKO-20DSP.md` (the Yameii/Deko
  hyperpop vocal chain teardown), `tools/digital_fairy_chain.py` (Pedalboard
  build of it: Avanna bus + human digi bus), `tools/pedalboard_chain.py`,
  `tools/custom_dsp.py`, `tools/transcribe_midi.py`, `tools/whisper_qa.py`,
  `WAVE-MAP.md`, `DELIVERY-STANDARDS.md`, `requirements.txt`.
- `docs/VOCALOID5-EXPANSION-ALL-THREE.md` — the Vocaloid 5 method teardown
  (Voice Color / control set, Avanna V3 in the V5 editor, FL Studio VSTi
  integration, sample-rate rules).
- `show/production/155-BATTLE-VOCAL-LAYERING.md` — vocal layering notes.
- Also in Mochiichao (not copied, audio): `public/audio/mixer/mixer-vocal-lead.wav`.

## What is NOT in either repo (honest)

- No Avanna voicebank, no VOCALOID5 installer, no .vsqx/.vpr project files.
  Verified by full-tree search: zero files of those types in Mochiichao.
- The owner's owned VOCALOID5 installer (2.64 GB) lives on his Windows/Mac
  seat only (per the VOCALOID5 expansion doc). The editor is Windows/Mac
  licensed software and does not run on the Linux production box.
- Avanna is an English voicebank. Japanese lyrics sung “Avanna-style” on
  this box = the repo's own open method above, applied to a Japanese guide
  vocal. See `song/README` notes in this PR's song folder for exactly what
  sang the dance song.

## Layout here

`mochiichao/` mirrors the source paths 1:1 so any file can be diffed
against the Mochiichao original. `song/` (added in this PR) is the Cape
Jones dance song built with this stack: lyrics, session/playlist, build
scripts, stems and mixes.
