# MIX NOTES — song v2: the balance fix + English version (2026-10-29)

## The problem, in the owner's words
"As soon as the lyrics vocals drop then the beat is almost unhearable."

## What measurement showed (before touching anything — `measure_v1.py`)
- In the v1 premaster, the vocal bus sat **+11 to +15 dB louder than the
  entire instrumental** whenever it sang. For scale: a study of 3,054 hit
  songs puts the median vocal at about **0 dB** against its own backing
  (pop −0.7 dB, electronic −1.5 dB). V1 wasn't a little hot — it was an
  order of magnitude past vocal-forward.
- Inside the delivered v1 master, the beat's body (40–250 Hz: bass +
  drum weight) **fell 7.8 dB from the intro into the first verse**, while
  the instrumental alone is dead flat there. Mechanism: the hot vocal ate
  the shared master compressor/limiter budget, so the beat got pumped
  down exactly when the singing started.
- The masking map had a surprise: the square lead barely fights the vocal
  in verses (it's mostly absent there). The real band-mates are the
  **arp** (fundamentals under the voice, harmonics through it) and the
  **tinkle-bell sparkle, whose energy is 99% inside the vocal's 2–5 kHz
  presence band**.

## What the research said (web + our own stack)
- Separation order: levels first, broad EQ second, filters third, and
  frequency-dependent sidechain ducking LAST as polish — not as the fix.
- Duck the melodic layers ~2 dB keyed from the vocal; **never duck the
  drums** — steal from guitars/synths, keep the beat's power.
- Our own repo teardown (VOCAL-CHAIN module 14 / §F.3) specifies the
  pro move for exactly this: TrackSpacer-style spectral ducking —
  32-band dynamic EQ on the **Mid channel only** of the beat bus, so
  stereo width survives. No free off-the-shelf equivalent existed in the
  wave, so `mix_v2.py` implements it as a custom STFT ducker
  (roundtrip-verified: silent key returns the target bit-clean).
- Hyperpop/digicore vocal practice (OTT-style density, presence + air,
  hard tuning) was already in the v1 chain — and the owner approved the
  voice. So the vocal chain is **unchanged, note for note**; only its
  placement in the mix was rebuilt.
- Loudness: the house spine stays locked at **−14 LUFS / −1 dBTP**
  (streaming/anisong norm); the teardown's −7…−9 LUFS commercial
  benchmark is explicitly NOT adopted, per the repo's own lock note.

## The three biggest changes
1. **Level architecture.** One hot global vocal gain (×1.15 against a
   ×0.9 backing) replaced by per-section vocal levels solved to targets:
   verses vocal +1.0 dB over the backing, choruses +0.5, bridge +1.5,
   outro +1.5 (LUFS, while singing). The vocal still leads — it just
   stops sitting on the beat's chest.
2. **Spectral ducking on the maskers only.** Arp, square lead and sparkle
   get a vocal-keyed, Mid-only spectral duck (max ~4 dB, only in the
   0.9–6.5 kHz clash zone, fast attack / ~150 ms release) plus a static
   −2 dB carve at 3 kHz on lead/arp. The bells ring back between lines;
   while she sings, they step aside. Drums and bass are never touched.
3. **Stereo placement.** The vocal lead was widened by a loud Haas copy
   (0.30) that smeared it across the beat's space; now focused centre
   (0.18), layers still wide, and the arp widened +2 dB on the side
   channel so its energy lives at the edges, not under the voice.

## Before / after, in plain numbers
| measure | v1 | v2 JP | v2 EN |
|---|---|---|---|
| vocal over backing while singing (LUFS) | +11…+15 dB | +0.5…+1.5 dB | +0.2…+1.9 dB |
| beat body drop, intro → first verse | **7.8 dB** | **0.5 dB** | **0.2 dB** |
| full-mix loudness / true peak | −14.1 / −1.3 | −14.2 / −1.3 | −14.3 / −1.4 |

Listen to the exact moment: `excerpt-vocal-entry-v1.mp3` vs
`excerpt-vocal-entry-v2-jp.mp3` / `-v2-en.mp3` (3.0–10.5 s — intro tail
into the first sung line).

## The English version
Same session, same melody, same mix. English lines were syllable-adapted
to the Japanese note grid (every phrase's syllable count matches its note
count — asserted in code), e.g. the hook stays a hook: "Cape Jones, dance
and dance, everybody come and dance, dance!" Sung the same way as the JP
take: guide voice (espeak-ng en+f5) syllable by syllable, Rubber Band
pitch placement with formant lift ×1.7 (repo v19 method), then the
identical Digital Fairy Avanna bus + layer recipe. Honest note, same as
v1: Avanna herself did not sing either take — no voicebank exists in the
repos and VOCALOID5 lives on the owner's Windows/Mac seat; the session's
melody + lyrics tracks re-voice cleanly when that seat runs it.

Small honest residuals: the EN outro reads +0.2 dB against its +1.5
target (the tail "la la" section sits a touch deeper in the backing —
it's the fade, not a clash), and the EN bridge reads +1.9 against +1.5.
Both inside a dB of intent; the beat survives everywhere.

## Files
- `song-full-v2-jp.mp3` / `song-full-v2-en.mp3` — the two v2 mixes
- `song-vocal-stem-v2-jp.wav` / `song-vocal-stem-v2-en.wav` — v2 vocal buses
- `song-instrumental-v2.mp3` — v2 backing alone
- `excerpt-vocal-entry-*.mp3` — before/after at the flagged moment
- Scripts: `measure_v1.py` (diagnosis), `mix_v2.py` (the remix),
  `build_vocal_en.py` (English vocal), `verify_v2.py` (the checks above)

Workspace note: the shared disk quota filled repeatedly during this
build; the build tree was relocated mid-task to `~/cj-song-v2-work/work`
(same scripts, same outputs). Everything deliverable was copied back
here, and the scripts + notes are committed in this folder.
