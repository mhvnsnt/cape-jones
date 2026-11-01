# Batch C — GIF previews + 12-principles + beat-sync prep — 2026-11-01

**Approval throughout: 0/1 (MP4s, shots, beat-sync decision). No approval claimed. No repo PR in this batch. No Mars-seen file overwritten; the old 0-byte `nosferatu-video5-20261101/video5-johnny-nosferatu-preview-20261101.gif` was left untouched (new GIFs live here, new names). Build scratch frames created for the C sample were removed after encoding; no delivered or Mars-seen file was deleted.**

## 1. GIF previews (all verified: decoded frame-by-frame, non-zero)

Made sequentially, one at a time, 480×270, 10 fps, first 10 s only, 128-colour palette — because the earlier full-length attempt OOMed (this VM had ~1.7 GB free at build time) and the old 0-byte GIF proves a full 211 s GIF is the wrong approach. GIFs are silent previews only; the MP4s remain the deliverables and their approval stays 0/1.

| Preview | Source MP4 | GIF | Size | Frames |
|---|---|---|---|---|
| Video 5 Nosferatu | `nosferatu-video5-20261101/video5-johnny-nosferatu-20261101.mp4` (211.0 s, 1920×1080, 24 fps) | `gifs/video5-johnny-nosferatu-preview-10s-20261101.gif` | 1,457,740 bytes | 100 (480×270, 10 fps, 10.0 s) |
| Dance fixed EN | `dance-flash-fix-20261101/dance-test-FIXED-v2-EN-full-SFX-FASTSTART-20261101.mp4` (75.789 s) | `gifs/dance-test-FIXED-v2-EN-preview-10s-20261101.gif` | 3,192,888 bytes | 100 (480×270, 10 fps, 10.0 s) |
| Dance fixed JP | `dance-flash-fix-20261101/dance-test-FIXED-v2-JP-full-SFX-FASTSTART-20261101.mp4` (75.789 s) | `gifs/dance-test-FIXED-v2-JP-preview-10s-20261101.gif` | 3,192,888 bytes | 100 (480×270, 10 fps, 10.0 s) |

Note, plainly: EN and JP GIFs are byte-identical (same md5) because the pair shares one visual and GIFs carry no audio — EN vs JP differ only in the vocal track, which a GIF cannot show. That is correct, not an encode error. The 10 s window covers ~2 dance loops, so all three environments (room → stage → night-city) appear.

## 2. Per-shot 12-principles checks, CJ-01–CJ-30

Full report: `principles/12-principles-per-shot-20261101.md` (30-row matrix + per-shot measured detail); machine-readable: `principles/12-principles-matrix-20261101.csv`; builder: `principles/build_principles_20261101.py`.
Basis per shot: that shot's own JSON numbers (canvas, char W×H, feet−ground, clipped, effect + effect px, rim px, shafts, dual-light) + its shot note + V6 spec holds. Verdicts: P / PA (partial) / F (fail) / NA (single still cannot show it).

| # | Principle | PASS | PARTIAL | FAIL | N/A | PASS % of assessable |
|---|---|---|---|---|---|---|
| 1 | Squash & stretch | 6 | 24 | 0 | 0 | 20.0% |
| 2 | Anticipation | 2 | 18 | 0 | 10 | 10.0% |
| 3 | Staging | 28 | 2 | 0 | 0 | 93.3% |
| 4 | Straight-ahead / pose-to-pose | 30 | 0 | 0 | 0 | 100.0% |
| 5 | Follow-through & overlap | 1 | 5 | 0 | 24 | 16.7% |
| 6 | Slow in & slow out | 0 | 0 | 0 | 30 | n/a (0 assessable) |
| 7 | Arcs | 4 | 18 | 0 | 8 | 18.2% |
| 8 | Secondary action | 13 | 17 | 0 | 0 | 43.3% |
| 9 | Timing | 0 | 22 | 0 | 8 | 0.0% |
| 10 | Exaggeration | 8 | 22 | 0 | 0 | 26.7% |
| 11 | Solid drawing | 27 | 3 | 0 | 0 | 90.0% |
| 12 | Appeal | 21 | 9 | 0 | 0 | 70.0% |

Totals, 360 cells: **PASS 140 (38.9%), PARTIAL 140 (38.9%), FAIL 0 (0.0%), N/A 80 (22.2%); PASS of assessable (280 cells) = 50.0%.**
Shots failing each principle: **none — FAIL = 0 for all 12 principles.** The gaps are PARTIAL, not FAIL, and are named per shot in the report: lowest PASS counts are CJ-05 and CJ-15 (2/12 each — CJ-05 placement + town call open; CJ-15 hover-plate stand-in), then CJ-25/CJ-26/CJ-29 (3/12). Highest: CJ-13/CJ-14 (7/12).
What is still owed (not hidden by FAIL=0): a consecutive-frame motion pass for slow-in/out (30/30 N/A), timing (0/30 PASS — spec holds written, durations unverified from stills), and follow-through lag (24/30 N/A); plus the open calls named in the report (CJ-05 street-vs-town, CJ-23/25/27 canonical room, CJ-15 foreshortened piece, CJ-18 seam candidate, CJ-29 night-city painting, dialogue/visemes post-episode). **Shot approval remains 0/30.**

## 3. Beat-sync preparation (NOT a decision)

Full prep: `beatsync/BEATSYNC-PREP-20261101.md` + `beatsync-timing-tables-20261101.csv` + `beatsync-option-tables-20261101.csv` + `beatsync_build_20261101.py`.
Song 152 BPM (192 beats, 48 bars, 75.789 s, beat 0.39474 s) vs visual ~107 BPM (beat 0.56075 s, 135.2 beats in 75.789 s); drift 0.750 beats/s if unchanged (56.8 beats by the end). Measured visual grid cross-check: 105.4 BPM mean slot; samples use nominal 107 (factor 1.42056) and say so.

| Option | Sample(s) | Effect |
|---|---|---|
| A re-time visual to 152 | `beatsync/option-A-retime-visual-152bpm-sample-20261101.mp4` (3.750 s, 480×270, loop speeded ×1.4206 + 152 BPM click) | Picture 42% faster; song untouched; flash gate must be re-run |
| B stretch audio to ~107 | `beatsync/option-B-stretch-audio-atempo-sample-20261101.mp3` (14.187 s, pitch preserved) + `option-B-stretch-audio-pitchdrop-sample-20261101.mp3` (14.206 s, −6.08 semitones) + `option-B-stretch-audio-muxed-sample-20261101.mp4` (5.271 s) | Song 75.789 s → 107.66 s; dance feel preserved; atempo artefacts vs key drop — listen before deciding |
| C re-grid visual | `beatsync/option-C-regrid-visual-sample-20261101.mp4` (86 frames, 3.583 s, 480×270, holds re-cut onto song beats + click) | Song untouched at 75.789 s; poses/order kept, holds re-cut (segments 14,13,14,27,14,14,14,13 → 10,8,10,20,8,10,10,10 frames); full re-cut + flash re-gate still owed |

Click reference: `beatsync/song-beat-click-152bpm-20261101.wav` (grid only, never for a final). Samples use the EN song + shared visual; JP timing is identical (same duration/BPM) so the tables apply to JP too, but no JP sample was rendered. **Mars decides; approval 0/1; nothing was applied to any final.**
