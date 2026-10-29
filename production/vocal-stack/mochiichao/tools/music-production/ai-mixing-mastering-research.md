# AI mixing / mastering + autotune research for the Mochiichao vocal chain

## What we are mixing on (no DAW, no FL Studio here)
- **ffmpeg** = the mixer console. Every plugin is a filter with numbers:
  EQ = `equalizer`, compressor = `acompressor`, limiter = `alimiter`,
  delay = `aecho`, chorus = `chorus`, de-esser = `deesser`, sidechain = `sidechaincompress`.
- **pyworld (WORLD vocoder)** = the autotune + formant engine. It splits a voice
  into pitch (F0), vocal-tract shape (spectral envelope), and breathiness, lets
  us change each separately, then resynthesizes. That separation is exactly why
  we can pitch up without going chipmunk.
- **rubberband** = pitch/time shifting for harmony layers.
- **Pedalboard (Spotify, open-source)** = real Python FX: Compressor, Limiter,
  Chorus, Reverb, HighpassFilter. Installed in the title-music venv (0.9.26).
  `pedalboard_master.py` is our mastering stage. MEASURED WARNING: on v16 it
  ran hot (limiter-only pass: peak 0.0 dBFS, LUFS -8.2, tail lifted) — verify
  peak/LUFS/tail after ANY Pedalboard pass before shipping.

## Autotune, in plain language (teach-back version)
- **Retune speed / glide:** how fast the pitch snaps to the note. 0 ms = instant
  robot (T-Pain / hyperpop). Slower = more human, more slide. Ours: 55 ms (v11-v15)
  -> **20 ms in v16 = humanize LESS**, more machine, more hyperpop.
  Antares "Humanize" is the same idea inverted: Humanize 0 = machine, 100 = keeps
  the singer's natural vibrato. We run the equivalent of Humanize ~0-10.
- **Key:** autotune must match the TRACK's key, not the vocal's best-fit key.
  Measured (2026-10-26): Mars's warped vocal pitch classes spread over all 12
  notes (3-5 secs each of 40) — best fits F major / A# major / D minor / G minor
  all tie at 70%, D major only 60%. But the title track IS D major, so D major
  is still the right autotune key: snapping to F major would fight the chords.
  The 40% of notes that move is what gives the hard-tuned hyperpop sound.
- **Formants (the AVANNA part):** formants = the size/shape of the vocal tract,
  what makes a voice sound male/female/big/small, separate from pitch.
  Chipmunk = pitch AND formants up together. Vocaloid = pitch way up, formants
  up LESS. Ours: pitch x2.73, formants x1.4 (v15) -> **x1.5 in v16 = more AVANNA**
  (female tract, clearer, less breathy). Breathiness 0.7 -> 0.5 in v16 for the
  "clearest/sweetest" AVANNA trait. Strong consonants = presence EQ, not a knob.
- **What autotune canNOT fix:** a note the singer didn't sing near, timing, or a
  bad arrangement. It moves pitch; it does not write melody.

## Mastering, in plain language
- **Mixing** = balancing the parts (vocal vs beat, EQ, space).
- **Mastering** = the final polish on the whole finished mix: gentle bus EQ,
  light compression (glue), and a LIMITER as the last wall so nothing clips.
  Our limiter sits at 0.89 (-1 dB) and the peak is 0.707 (-3 dB) — nothing clips.
- **LUFS** = how loud a song FEELS, streaming's loudness unit. Measured:
  v15/v16 = -10.2/-10.3 LUFS (between neptune -13.6 and PSO -7.7).
  PSO is crushed louder on purpose (commercial master); neptune is more dynamic.
  We sit between them — not under-mastered, not squashed. Louder is not better
  past the point where the tail and dynamics die (see Pedalboard warning above).

## More tools pulled in / researched (how each makes the song better)
| Tool | Open/free? | Use for this song |
|---|---|---|
| Demucs (Meta) | Open-source | Split a reference song into vocal/drums/bass/other stems, so we can study Yameii's vocal ALONE instead of guessing through the beat. Next: run on neptune (needs torch, CPU-slow, batch job). |
| Basic Pitch (Spotify) | Open-source | Audio -> MIDI notes. Turns a reference vocal into actual notes we can compare against our autotune targets. |
| Pedalboard (Spotify) | Open-source | Real FX chain in Python; mastering stage (installed + tested, see warning). |
| Matchering | Open-source | Reference matching: match our mix's loudness + tone curve to a reference (neptune). Last 5% only — it cannot fix a bad mix. |
| OpenUTAU + DiffSinger | Open-source | Real vocaloid-style singing synth (future: a true vocaloid voice for game tracks, not just transforming Mars's voice). |
| librosa / essentia / aubio | Open-source | Analysis: tempo, key, pitch, onsets — already used via aubio + our own FFT code. |
| Remiqora / StemDeck | Open-source apps | All-in-one local AI studios (generation, stems, DAW) — reference for workflow, not needed while our script chain works. |

## The honest limit
No plugin, AI or not, replaces the ear test: every version here is measured
(pitch median, dropouts, RMS, LUFS, tail) AND must pass Mars listening.
Meters catch my mistakes (v12's fake render, v16's hot master); they do not
approve a mix. Mars does.
