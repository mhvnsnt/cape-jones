# Episode 1 M4 — Nosferatu score identification (TRACK E2)

Date: 2026-10-24. Worker: TRACK E2 (audio-based identification).
Status: **RECORDING MATCHED — the owner's video audio is the
Nosferatu1922VHS transfer audio. The score itself has NO documented
composer or published cue list in any source found, so NO song names
can be listed. Do not reuse the old James Bernard names.**

## What was compared (method)

- Reference: `/home/hatch/workspace/nosferatu/nosferatu-exact.mp3`
  (5,066.97 s, pulled from the owner's exact video E-2CH2_iGgc).
  No YouTube re-download was attempted.
- All audio decoded to mono 22050 Hz WAV (stereo kept for one
  channel check) with ffmpeg. Analysis in Python (numpy/scipy;
  librosa venv at `~/workspace/nosferatu-analysis-venv/`).
- Metrics per 60 s probe window: waveform Pearson correlation
  (sample-level, with fine-lag FFT search ±2 s), 0.1 s RMS-envelope
  correlation, and mean spectral centroid. Controls: exact-vs-itself
  shifted +30 s (envelope r = −0.09) and exact-vs-itself identical
  (r = +1.00) bound the chance level at roughly |r| < 0.2.
- Scripts and probe audio kept at `~/workspace/nosferatu-analysis/`
  (`compare.py`, `compare2.py`, `fine.py`, `vhs-*.wav`, `hht-798.wav`).

## Result 1: Schirmann (Internet Archive Alpha copy) — NO-MATCH

Reference: `/home/hatch/workspace/nosferatu/nosferatu-full.mp3`
(5,058.82 s, the old wrong cut's source).

| Probe | Waveform r | Envelope r | Centroid exact | Centroid Schirmann |
|---:|---:|---:|---:|---:|
| 300 s | −0.0007 | −0.1080 | 2,469 Hz | 1,214 Hz |
| 798 s (13:18) | +0.0013 | −0.0858 | 2,467 Hz | 1,452 Hz |
| 1200 s | −0.0021 | −0.0436 | 2,509 Hz | 984 Hz |
| 2400 s | +0.0027 | +0.0363 | 2,008 Hz | 1,252 Hz |
| 3600 s | +0.0057 | +0.0256 | 2,073 Hz | 1,279 Hz |
| 4800 s | +0.0035 | −0.0462 | 2,066 Hz | 988 Hz |

- Whole-file 1 s RMS-envelope correlation (first 5,058 s): **r = −0.0533**.
- Offset sweeps (exact windows vs Schirmann at every 10 s across the
  whole file): best r = +0.1833 (798 s window) and +0.2035 (2400 s
  window) — chance level, no hidden alignment.
- Verdict: **NO-MATCH**. Different score, different timbre
  (bright synth ~2,000–2,500 Hz vs orchestral ~1,000–1,500 Hz).
  Confirms the owner's ear-check: the Alpha/Schirmann audio is not
  his video's audio.

## Result 2: Nosferatu1922VHS (Internet Archive VHS transfer) — MATCH

Source: IA item `Nosferatu1922VHS`, file `Nosferatu (1922).mp4`,
probed by legitimate range-seek streaming from archive.org
(no full 2.27 GB download). Prior worker's 60 s ear-check clip
(`correct-audio/nosferatu-1338-earcheck.mp3`, 13:18–14:18) is from
this same item.

Ear-check clip vs exact audio at 13:18 (798 s):

- Envelope r = **+0.9270** at zero offset (best offset in ±180 s
  search was 0 s — no shift needed).
- Fine-lag waveform: clip-L vs exact-L **r = +0.9951**, clip-R vs
  exact-R **r = +0.9945**, both at a constant **+36.3 ms** lag
  (clip-extraction/encoder alignment offset, identical at every
  probe below). Zero-lag waveform r looked low (−0.03 to −0.22)
  only because of that 36 ms shift — envelope and fine-lag
  correlation resolve it.
- Stereo fingerprint: exact L/R correlation in the window =
  0.6347, clip L/R correlation = 0.6347 (identical mix).
  Log-spectrum correlation exact-L vs clip-L = +0.9989.
- Centroids agree: exact 2,467 Hz vs clip 2,465 Hz.

Streamed VHS windows vs exact at the same timestamps:

| Probe | Envelope r | Fine waveform r (lag) |
|---:|---:|---:|
| 300 s | +0.9241 | +0.9978 (+36.3 ms) |
| 1200 s | +0.9128 | +0.9974 (+36.3 ms) |
| 2400 s | +0.9152 | +0.9984 (+36.3 ms) |
| 3600 s | +0.9061 | +0.9981 (+36.3 ms) |
| 4800 s | +0.9296 | +0.9978 (+36.3 ms) |

- Verdict: **MATCH, at waveform level, across the whole film.**
  The owner's video audio and the Nosferatu1922VHS transfer are
  the same recording/master (different encodes of one source).
  The prior "candidate" hypothesis is now confirmed by evidence,
  not just runtime: both are 5,066.97 s AND waveform-identical.
  This supersedes the owner ear-check as the proof step for the
  recording identity (owner confirmation of the exact-audio clip
  itself is separately recorded in MEMORY.md, 2026-10-24).

## Result 3: Hollywood Home Theatre VHS (David T. Ichikawa synth score) — NO-MATCH as the source recording

- IA item `nosferatu-hollywood-home-theatre` describes a
  "completely improvised synthesizer score performed by David T.
  Ichikawa" — the only *named* 1980s-VHS synth score found.
- Tested by streaming its mp4 (direct IA server after a transient
  5xx on the download host): 798 s window vs exact 798 s window
  gave envelope r = +0.0606, waveform r = −0.0032; best offset in
  ±180 s was r = +0.3260 (weak, chance-adjacent, vs 0.91+ for the
  true match). Note: only ~52 s was captured for this probe
  (ffmpeg `-t 60` yielded 51.9 s on this file) and this tape is a
  different, decayed transfer, so this rules it out as the *source
  recording* of the owner's video, not as a historical curiosity.
- Verdict: **NO-MATCH** for the owner's video audio. Do NOT credit
  Ichikawa for this video's score.

## Result 4: James Bernard (1997), Hans Erdmann reconstructions — NOT DIRECTLY COMPARED / EXCLUDED AS THE RECORDING

- No legally obtainable full reference recording was available in
  this environment for waveform comparison (both are commercial
  orchestral recordings: Bernard/Silva Screen 1997; Erdmann
  reconstructions by Berndt Heller 1984, Gillian Anderson/James
  Kessler 1995, Müller/Plebuch 2013). No pirate or unauthorized
  source was used. Status for direct comparison: **UNOBTAINABLE**.
- They are nevertheless excluded as the source recording by
  positive evidence: the owner's audio is already waveform-matched
  to the VHS transfer, and both Bernard and Erdmann/Heller are
  orchestral recordings, while the matched audio is a bright
  synthesizer score (centroid ~2,000–2,500 Hz throughout).
- Their cue lists (Bernard's 14 published cues, etc.) therefore do
  NOT apply to this video. The old Bernard-named track set stays
  retired and its names must not be reused.

## The score itself: composer and cue list — NOT IDENTIFIED

- The matched IA item's metadata names NO composer and NO track
  list: description is only "RIPPED FROM VHS / Audio Restored to
  5.1 Surround Sound" (uploader Geno_Cuddy@yahoo.com, 2016-03-21).
  Its sole review describes "the synthesizer musical score [as]
  consistent with its origins as a 1980s VHS copy" — no name.
- Web research (Brentonfilm "Nosferatu: History and Home Video
  Guide" Parts 3 and 8; IA item pages; score-history sources)
  found no published cue/track list for an anonymous 1980s-VHS
  synth score, and no source attaching a composer name to the
  Nosferatu1922VHS transfer specifically. Brentonfilm notes
  budget PD copies commonly carry ersatz scores with no attempt
  at documentation, and that recorded scores retain their own
  copyrights even when the film is public domain.
- **Therefore NO song names are listed here, per the owner
  directive: no invented names, no guessing, no Bernard names.**
  The score is an anonymous/uncredited 1980s-VHS synthesizer
  score as far as every documented source found goes. It may be
  an improvised/uncredited library performance; that cannot be
  established from audio analysis alone (this worker cannot
  listen, and computation identifies recordings, not authorship).

## Overall verdict: RECORDING IDENTIFIED, SCORE NAME NOT IDENTIFIED

- IDENTIFIED (recording): the owner's video audio =
  Internet Archive `Nosferatu1922VHS` transfer audio
  (waveform r ≈ 0.997–0.998 at six probes spanning the film).
- NOT IDENTIFIED (score): no composer name and no cue/track list
  exists in any documented source found for this VHS synth score.
  M4 cuts from `nosferatu-exact.mp3` are sonically correct, but
  they cannot truthfully be given "actual song names" from this
  soundtrack, because no such published names were found.

## What is still missing / what would identify it

1. A documented credit for the Nosferatu1922VHS transfer's score
   (e.g. the original VHS packaging/credits, if the tape's
   label can be identified from the transfer's picture or
   intertitle set).
2. OR the owner's own description of what he hears (instruments,
   melody, any recognizable tune) at a timestamp — the one input
   computation cannot supply. If the synth line quotes a known
   classical piece, that would be the lead to follow.
3. OR a legally obtainable reference recording of another named
   synth score that waveform-matches (none found; Ichikawa
   tested and ruled out).

## Standing flags (carried forward, not resolved here)

- License: the film is public domain, but a 1980s-VHS synth score
  is not automatically public domain (Brentonfilm Part 3: recorded
  scores retain individual copyrights). Do not label the VHS
  score "PD" in episode credits without a use-basis decision.
- The old Bernard-named set in `tracks-exact/` is NOT to be sent.
- No PR was opened and nothing was merged, per instructions.

## Independent verification (DoggByte, 2026-10-24)

The 13:18 window was independently re-checked against
`nosferatu-exact.mp3` with a full sample-level FFT cross-correlation
(all lags, ≥20 s overlap): peak r = +0.964 at −36.25 ms lag (the same
offset E2 reports, opposite sign convention), confirming the
clip-file match. Note for future checkers: a coarse lag grid
(50 ms steps) misses this peak entirely — waveform correlation
peaks here are ~1 ms wide — which is why an initial coarse check
falsely reported no match. That false negative is corrected here
so it is not repeated. This verification covers the 13:18 window
only; E2's six-probe whole-film match stands as the full-film
evidence.
