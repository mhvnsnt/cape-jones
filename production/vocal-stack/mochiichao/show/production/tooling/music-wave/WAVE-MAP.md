# MUSIC & VOICE WAVE — MAP

Owner order (Jamar, 2026-10-28): tear down the audio giants' open tools and wire
them into the voice/music pipeline at 100%. This package is the result: two
Spotify tools wired and smoke-proven on real show audio, Whisper wired and
smoke-proven on real casting audio, an honest no-install verdict on Meta
AudioCraft, and the delivery-loudness standards teardown.

Home: `show/production/tooling/music-wave/`. Cross-references (read, never
edited by this pass): `tooling/voice-kit/` (Chatterbox/Kokoro render wiring),
`tooling/VOICE-WEIGHTS-MANIFEST.md`, `tooling/mouth-data/` (Rhubarb →
mouth-data), the ACE-Step staging manifest (`ace-step-stage/MANIFEST.md` on the
workbench; weights in TeraBox/Kaggle per the staging law), and the
UNIFIED-PIPELINE audio-before-picture flow with its FFmpeg loudnorm −14 LUFS
spine.

## Audit first — what the house already has (verified on main + disk, 2026-10-28)

| Piece | State | Evidence |
|---|---|---|
| Chatterbox TTS (MIT) | HAVE — weights staged byte-verified (3,191,966,992 B set), render wiring in `tooling/voice-kit/` (`render_voice.py`, render-queue schema) | VOICE-WEIGHTS-MANIFEST.md; `~/workspace/voice-weights-stage/` |
| Kokoro-82M (Apache-2.0) | HAVE — weights staged byte-verified (330,355,132 B set, 6 voice packs) | same manifest |
| Per-character voice design | HAVE as spec — `characters/{mochiko,hex,aeon}/character.yaml` carry VOICE-DESIGN params; reference-audio slots EMPTY (owner casting) | voice-weights-stage |
| ACE-Step (music generation) | HAVE weights, GAP first generation — staged model is **ACE-Step 1.5 XL Turbo**, 19,953,378,268 B byte-verified; no generation run yet | `ace-step-stage/MANIFEST.md` |
| Rhubarb lip-sync | HAVE — vendored in cape-jones; repo-side converter `tooling/mouth-data/rhubarb_to_mouthdata.py` + samples on main | tooling walk, 2026-10-28 |
| Loudness spine | HAVE — FFmpeg two-pass loudnorm at −14 LUFS / −1 dBTP; EP01's 20 finished beds all measure −14 ±1 LUFS, TP ≤ −0.9 (two by-design absence beds exempt) | `ep01-finish/audio/BEDS.md` |
| Effects/processing layer | **GAP → filled by this wave (Pedalboard)** | — |
| Audio→MIDI transcription | **GAP → filled by this wave (Basic Pitch)** | — |
| Speech→text QA | **GAP → filled by this wave (Whisper)** — a vendored Whisper copy exists inside `tooling/full-stack/musetalk/` for MuseTalk's audio features, but no standalone ASR/QA seat existed | tooling walk |

## The wave — per target

| # | Target | Licence (verified at source, 2026-10-28) | Bucket | Status |
|---|---|---|---|---|
| 1 | Spotify Pedalboard | GPL-3.0 (repo LICENSE/README; JUCE core dual GPLv3/commercial) | Open source (copyleft) | **WIRED + SMOKED** — see TEARDOWN-pedalboard.md, SMOKE-RECORDS.md §1 |
| 2 | Spotify Basic Pitch | Apache-2.0 (repo LICENSE/README) | Open source | **WIRED + SMOKED** — TEARDOWN-basic-pitch.md, SMOKE-RECORDS.md §2 |
| 3 | OpenAI Whisper | MIT — code AND weights (repo LICENSE) | Open source | **WIRED + SMOKED** — TEARDOWN-whisper.md, SMOKE-RECORDS.md §3 |
| 4 | Meta AudioCraft / MusicGen | Code MIT; **weights CC-BY-NC 4.0** (model cards, verbatim: "Code is released under MIT, model weights are released under CC-BY-NC 4.0") | Code open source; **weights free-but-restricted (non-commercial — outputs cannot ship)** | **NOT WIRED — verdict** (AUDIOCRAFT-VS-ACESTEP.md): no shippable gap vs the house ACE-Step seat |
| — | House ACE-Step 1.5 XL Turbo | MIT (HF card `license: mit` + ACE-Step-1.5 repo LICENSE; v1 was Apache-2.0) | Open source | HAVE (weights); first generation still owed — unchanged by this wave |
| 5 | Dolby / delivery loudness | Standards, not software (ITU-R BS.1770, EBU R128, ATSC A/85, platform specs) | n/a | **DOC** — DELIVERY-STANDARDS.md; the locked −14 LUFS target is NOT changed; proposals flagged as owner decisions |

## What the wired tools are FOR (house wiring)

- **Pedalboard** = the pipeline's scripted effects seat: voice-line polish
  chains for Chatterbox/Kokoro renders and bed sweetening, replacing ad-hoc
  per-tool processing. GPL-3.0 note: it is used as a *tool* in the pipeline;
  nothing GPL-licensed ships inside the game/show binaries.
- **Basic Pitch** = melody capture: hums, vocal-lead stems and ACE-Step beds →
  MIDI the score lane can edit, re-voice and register — the bridge between
  generated audio and the composed score.
- **Whisper** = the voice-pipe's *measurement* tool: QA transcripts of casting
  samples and TTS renders (did the line come out as written?), timing for the
  subtitle-ration workflow. Show law stands: subtitles appear only at important
  moments — Whisper measures; it does not subtitle everything. See
  TEARDOWN-whisper.md §Verdict.

## Smoke summary (full verbatim records in SMOKE-RECORDS.md)

- **Pedalboard §1:** voice chain on `voice-casting-samples/mochiko/candidate-1.wav`:
  peak 0.2810→0.5241, RMS 0.0518→0.0822, loudness −24.28 LUFS / −10.93 dBTP →
  **−20.08 LUFS / −5.50 dBTP**. Bed chain on the first 30 s of the EP01 OP bed:
  peak 0.8913→0.9150, RMS 0.1518→0.1815, −13.60 LUFS / −1.00 dBTP →
  **−12.18 LUFS / −0.75 dBTP** — measured caveat: Pedalboard's limiter is
  sample-peak, not true-peak, so the FFmpeg loudnorm spine stays the mandatory
  final stage (see SMOKE-RECORDS.md §1).
- **Basic Pitch §2:** on the first 30 s of the EP01 vocal-lead stem:
  **59 notes, MIDI 59–74 (B3–D5), 29.80 s span**; outputs
  `vocal_lead30_basic_pitch.mid` (4,630 B) + `.csv` (6,177 B, pitch-bend series
  included), via the ONNX backend — no TensorFlow needed.
- **Whisper §3:** on the Mochiko casting reference (6.675 s): one segment,
  mean no_speech_prob **0.215**, transcript "Good morning, Garden. The gate is
  open, the pond is calm, and everybody gets breakfast before anything else."
  Non-speech control (20 s of the EP01 N1 bed): 3 hallucinated segments
  ("DREAM / Ah / Uro"), mean no_speech_prob **0.574** — the no-speech gate is
  the house defence; Whisper measures, it never auto-subtitles.
