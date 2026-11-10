# Episode 1 M4 — Nosferatu music: final research log + clip-naming scheme

Date: 2026-10-24. Status: **OWNER DECISION FINAL — this is the music we're using.**

This document consolidates every Nosferatu finding from 2026-10-24 into one
record, so the M4 cue and its clip names rest on verified facts only.
It supersedes PR #239's "candidate, not proven" framing (recommend closing
#239 unmerged — its content is consolidated and corrected here). The E2
evidence note (PR #247) remains the primary waveform-evidence record;
this log is the synthesis, the decision record, and the naming scheme.

## Owner decisions (locked)

- **M4 = the literal music from the owner's video**: "Nosferatu 1922 |
  Full Movie | Free", channel Rollercoastersareprettycool, video ID
  E-2CH2_iGgc, runtime 1:24:27 (= 5,067 seconds).
- **2026-10-24: the owner will use this music either way.** It is no
  longer "a candidate" in any doc or credit — it is the music.
- **Names must be actual names only; NO invented names** (standing owner
  directive). Where no published name exists, clips are named from
  verified facts under the scheme below — never from invented titles.
- **Source audio locked**: `nosferatu-exact.mp3` (5,066.97 s, pulled
  directly from the exact video), owner ear-confirmed 2026-10-24 as
  "the audio I like and wanted and prefer."

## Recording identification (proven by waveform evidence)

- The owner's video audio **is** the Internet Archive transfer
  `Nosferatu1922VHS` audio — same recording/master, different encodes:
  - E2 waveform match: 6 probes spanning the film (300–4800 s),
    waveform r = +0.997–0.998 at a constant +36.3 ms encode offset;
    stereo fingerprint identical; log-spectrum correlation +0.9989.
  - Independent FFT verification (DoggByte): 13:18 window, peak
    r = +0.964 at −36.25 ms lag (same offset, opposite sign
    convention). An initial coarse lag grid falsely reported no match
    (waveform peaks here are ~1 ms wide; 50 ms steps stepped over the
    36 ms peak) — that false negative is corrected here and must not
    be repeated.
- Transfer facts (Archive metadata API, not guessed):
  - Item: `Nosferatu1922VHS` — "Nosferatu - A Symphony of Terror (1922)"
  - File: `Nosferatu (1922).mp4` (original), 2,273,066,572 bytes,
    5066.97 s, 640×480 h264 at 29.97 fps
  - Uploader: Geno_Cuddy@yahoo.com, 2016-03-21; collections
    vhsmovies/vhsvault
  - Description: "***** RIPPED FROM VHS ***** Audio Restored to 5.1
    Surround Sound." No publisher, label, or composer in the metadata.
- Score character: bright **synthesizer** score (spectral centroid
  ~2,000–2,500 Hz throughout), playing **continuously** — silence
  analysis found ZERO gaps ≥2 s at −45 dB across all 84 minutes, so
  there are no clean audio song breaks. Section boundaries for clips
  must follow film scenes at cut time, never audio gaps (none exist).

## Print lineage (identified)

- The picture is the **1947 MoMA print lineage**: Cinémathèque
  Française print → Cinémathèque Suisse → Czech export print →
  MoMA's 1947 English re-titling (1927 Futura font, Stoker names
  restored: Dracula, Renfield, Harker, Nina, Westenra, Lucy).
- Verified from a viewed frame of the transfer's title card:
  "1922 / NOSFERATU / Directed by F. W. MURNAU / (Acquired through the
  courtesy of La Cinémathèque Française)."
- Sources: Brentonfilm Part 3 (read in full) and the Wikisource
  transcription, matching the transfer's title card and cast list
  exactly; Movie-Censorship PD-vs-restored name table corroborates.

## What it is NOT (exclusions, each with its reason)

- **Schirmann / Internet Archive Alpha copy** — waveform NO-MATCH
  (r ≈ 0 across 6 probes); orchestral, not synth. The old 17-track
  set cut from this source is RETIRED; its Bernard-derived names
  must never be reused.
- **James Bernard (1997) score** — orchestral; no legally obtainable
  reference for direct comparison; its 14 published cue names do NOT
  apply to this video. (The earlier Bernard-named track set was
  therefore wrong in both audio and names.)
- **Hans Erdmann reconstructions** (Heller 1984, Anderson/Kessler
  1995, Müller/Plebuch 2013) — orchestral; excluded by the positive
  VHS evidence. No obtainable reference; cue lists do not apply.
- **Hollywood Home Theatre VHS (David T. Ichikawa)** — waveform
  NO-MATCH as the source recording. Do NOT credit Ichikawa.
- **Kartes Video Communications / Video Film Classics (1984)** —
  closest checked, still NOT a match (LOW confidence only): its
  documented score is 1950s horror stock music, not a continuous
  synth score, with no documented speed-corrected 84:27 runtime.
- **All other documented releases checked** — Alpha VHS 1995, Atlas
  Film German VHS 1981, Republic 1991, Kino/Shepard editions, Image
  LaserDisc/DVD, Arrow 1998 (Type O Negative), BFI/Universum/Divisa/
  Eureka restored editions: excluded on score, intertitles,
  runtime, or decade. Budget labels searched with zero indexed
  Nosferatu VHS hits: GoodTimes, Video Yesteryear, Congress Video,
  Vestron, Media Home Entertainment, Thorn EMI, Paragon, Sinister
  Cinema, Film Detective, Hollywood Movie Greats, Star Classics.

## Tape / composer / score title: NOT FOUND (stated honestly)

- No composer name and no track/cue list exists in any documented
  source found: not in the Archive metadata, not in Brentonfilm
  Parts 3/4/8, not in any collector catalog or database checked.
- Why: the MoMA print fed **over a thousand budget/bootleg tapes
  worldwide** (Brentonfilm: "it would be impossible, not to mention
  pointless, to discuss [them] in too much depth"). This transfer is
  most plausibly one of those uncataloged tapes.
- Picture inspection (17 frames: opening credits, final 3 minutes,
  mid-film samples, thumbnails): NO distributor logo, label card, or
  composer credit anywhere. The transfer opens directly on the title
  card and ends on a plain "The End" card.
- Identifier sites: Shazam no-match on 7 samples; AudioTag and Aha
  Music both dead at Cloudflare verification on this VM's browser
  environment (including the owner's own human taps) — no more
  upload-identifier-site loops.
- Remaining honest routes: (1) the physical tape's packaging/label;
  (2) the owner's own description of what they hear at a timestamp.
  Nothing else documentary remains unrun.

## License flag (carried, not a veto)

- The film and its English titles are public domain (MoMA print;
  titles not renewed after 28 years).
- Recorded scores retain their own individual copyrights
  (Brentonfilm Part 3: PD status "only applies to the direct
  derivatives of the completely silent 1947 MoMA print… All
  subsequent translations, restorations and recorded scores *retain
  their own individual copyrights*").
- This anonymous synth score's copyright status is therefore
  UNKNOWN and undocumented. Do NOT label it "PD" in episode credits
  without a use-basis decision. The owner's direction (use it either
  way) is recorded above; this flag governs credit wording, not
  whether the music is used.

## Clip-naming scheme (from verified information only)

Clips for M4 are named from the facts in this log — never from
invented song titles, never from Bernard cue names, never with a
composer credit unless/until one is verified:

> `Nosferatu (1922) — VHS synth score (Nosferatu1922VHS transfer, MoMA 1947 print) — [film section at cut time] — [mm:ss–mm:ss]`

- The `[film section]` is the story section the clip covers
  (e.g. opening, Hutter's journey, the castle, the voyage, the
  plague, the finale), identified at cut time from the film itself.
- The `[mm:ss–mm:ss]` is the clip's range in `nosferatu-exact.mp3`.
- Episode credit line (to be conformed at picture lock if a name is
  later verified): "Music: anonymous 1980s VHS synthesizer score, as
  heard in the Nosferatu1922VHS transfer of Nosferatu (1922, MoMA
  1947 print). Composer uncredited in all sources found."
- The old 17-track Bernard-named set stays retired. A new re-cut
  from `nosferatu-exact.mp3` follows this scheme; its section
  boundaries follow film scenes, since the music itself has no
  audio-gap boundaries.

## Sources

- E2 waveform-evidence note (PR #247):
  `docs/research/EP01-NOSFERATU-SCORE-IDENTIFICATION.md`
- Transfer picture inspection: `~/workspace/nosferatu-vhs-frames/`
  (17 frames + REPORT.md; title card viewed and transcribed)
- Catalog research: Brentonfilm Parts 3/4/8, Wikisource PD
  intertitles, Movie-Censorship PD-vs-restored table, Archive item
  `Nosferatu1922VHS` metadata
- Prior superseded record: PR #239 (candidate doc — recommend
  closing unmerged; consolidated and corrected here)
