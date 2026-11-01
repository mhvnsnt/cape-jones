# Beat-sync PREPARATION ONLY — NOT a decision — 2026-11-01 (Batch C)

**Approval: 0/1. No option below was applied to any final. Mars decides. The EN/JP finals remain unsynced (152 BPM song vs ~107 BPM visual grid), as stated in the dance-flash-fix report.**

## The numbers (measured / sourced, not guessed)

- Song: 152 BPM, C major, 48 bars. Source: `cape-jones-flying/production/vocal-stack/song/song_data.py` (BPM=152) and `compose_song.py` ("152 BPM, 48 bars = 75.79 s"). Verified: 75.789 s × 152/60 = 192.0 beats = 48 bars exactly.
- Song beat = 60/152 = 0.39474 s; bar (4/4) = 1.57895 s.
- Visual grid: ~107 BPM nominal (task + 12-principles checklist: ~14-frame beat grid). Visual beat = 60/107 = 0.56075 s; 135.2 visual beats fit in 75.789 s.
- Measured cross-check (dance-flash-fix REPORT): v2 SFX events per 123-frame loop at frames 0,14,27,41,68,82,96,110; gaps 14,13,14,27 (= 2 beats),14,14,14,13-to-loop. Beat slots per loop = 9, mean slot 123/9 = 13.67 frames @24 fps = 0.569 s = 105.4 BPM. So the measured grid is 103–107 BPM depending on median vs mean. All samples below use the task nominal 107 BPM (factor 1.42056) and say so; using 105.4 BPM instead would give factor 1.442 — same direction, ~1.5% faster.
- Drift if nothing changes: song gains 0.750 beats per second on the visual. At 10 s: 7.5 beats apart; at 30 s: 22.5 beats; at 75.789 s: 56.8 beats (≈ 22.4 s of song beats). Full table: `beatsync-timing-tables-20261101.csv`.

## Option A — Re-time visual to 152 BPM (speed the picture up)

- What changes: visual playback × 1.42056 (152/107). A 123-frame loop (5.125 s) becomes 86.6 frames (3.61 s). Full 75.789 s visual becomes 53.35 s of picture at song speed, so the loop repeats 21.0 times instead of 14.8 to fill the song (or the cut is re-timed; that re-cut is Mars's call, not done here).
- Sample: `option-A-retime-visual-152bpm-sample-20261101.mp4` — one loop from `dance-test-FIXED-v2-one-loop-20261101.mp4` (125-frame file incl. GOP tail) speeded uniformly, scaled to 480×270, with a 152 BPM click track overlaid (click = song beat grid, not the song). ffprobe: 3.750 s, 480×270, 24 fps, h264 + AAC. Event mapping (uniform speedup): original SFX frames 0,14,27,41,68,82,96,110 → 0,9.9,19.0,28.9,47.9,57.7,67.6,77.4 — each within ~2 frames of a song beat. Full table: `beatsync-option-tables-20261101.csv`.
- Trade-offs, plainly: dance gets 42% faster — snappier, but holds shorten and the on-2s feel may turn choppy; any future in-betweens also speed up. Pitch untouched (picture only). No audio change, so vocals stay natural. Risk: fast sections that were already held to 2s in v2 for flash safety get faster again — flash gate must be re-run on the re-timed full video before any showing.

## Option B — Stretch audio to ~107 BPM (slow the song down)

- What changes: song tempo × 0.70395 (107/152). Full song 75.789 s → 107.66 s (+31.87 s). Visual stays at its current speed; to fill 107.66 s the dance loop repeats ~21.0 times instead of 14.8 (extra ~32 s of picture, or a longer cut — Mars's call).
- Samples (EN mix, first 10 s of song → 14.19 s stretched):
  - `option-B-stretch-audio-atempo-sample-20261101.mp3` — ffmpeg `atempo` (pitch preserved, phase-vocoder). ffprobe: 14.187 s. Trade-off: pitch stays, but time-stretch artefacts (smearing on vocals/sibilants) at 0.70× are audible; quality must be judged by ear.
  - `option-B-stretch-audio-pitchdrop-sample-20261101.mp3` — resample only (`asetrate`), pitch drops 12·log2(107/152) = −6.08 semitones (about a tritone-plus down: a C becomes roughly F♯ below). ffprobe: 14.206 s. Trade-off: no stretch artefacts, but the song is now in the wrong key and vocals sound slowed-down/record-dragging — almost certainly not shippable as the song, included only so Mars can hear the difference.
  - `option-B-stretch-audio-muxed-sample-20261101.mp4` — one-loop visual (480×270) + atempo-stretched audio head. ffprobe: 5.271 s. Shows visual beats landing near stretched beats (~0.561 s grid).
- Trade-offs, plainly: dance feel preserved exactly, but the song is no longer the 152 BPM song — tempo, energy, and (in the resample variant) key all change; a 107.66 s version is a different cut length than the 75.789 s finals; vocal intelligibility under atempo at 0.70× is the thing to listen for.

## Option C — Re-grid visual (keep song at 152, re-cut holds onto song beats)

- What changes: playback speed NOT changed uniformly. Each key/SFX event is moved to its nearest song-beat frame (snapped to even frames, on-2s), and the holds between events absorb the shift. Event mapping: original frames 0,14,27,41,68,82,96,110, loop-return 123 → song-beat frames 0,10,18,28,48,56,66,76,86 (beats 0,1,2,3,5,6,7,8,9 — beat 4 is a held beat, as in the original). Per-event shifts (snapped minus original, cumulative because the loop compresses): 0, -4, -9, -13, -20, -26, -30, -34, -37 frames (see CSV). The meaningful per-segment hold changes are: original segments 14,13,14,27,14,14,14,13 frames -> re-gridded segments 10,8,10,20,8,10,10,10 frames.
- Sample: `option-C-regrid-visual-sample-20261101.mp4` — the 123-frame loop re-cut by segment-wise frame remapping (poses unchanged, holds shortened/lengthened per the segment table above), 86 frames, 3.583 s, 480×270, 24 fps, with the 152 BPM click overlaid. Note honestly: for this keys-only loop, C lands very close to A (uniform speedup) — because the loop has no in-between motion, only holds. The difference matters once in-betweens exist: A would speed the motion itself, C only re-cuts the holds.
- Trade-offs, plainly: song untouched (tempo, pitch, length all stay 75.789 s); dance phrase keeps its poses and order, but some holds shrink (e.g. the 14→27 segment, 13 frames, becomes 8 frames) and the double-beat hold 41→68 (27 frames) becomes 20 frames over 2 beats — the phrase rhythm changes even though the speed knob was never touched. Requires a real re-cut of the full 75.789 s (loop re-cut × ~21 song-beat loops), not just this one-loop demo; flash gate must be re-run, because shorter holds mean faster key changes.

## Side-by-side (one loop, for Mars to compare)

| Option | Loop length | Song length | Pitch | What moves |
|---|---|---|---|---|
| A re-time visual | 3.61 s (86.6 f) | 75.789 s unchanged | unchanged | picture faster ×1.4206 |
| B stretch audio | 5.125 s unchanged | 107.66 s (+31.87 s) | preserved (atempo) or −6.08 semitones (resample) | song slower ×0.7040 |
| C re-grid visual | 3.58 s (86 f, demo) | 75.789 s unchanged | unchanged | holds re-cut onto song beats |

## Not decided here

- Which option, if any. Whether the re-cut/re-time applies to the EN mix, JP mix, or both (samples use EN song + the shared visual; JP timing is identical — same 75.789 s, same BPM — so the tables apply to JP too, but no JP sample was rendered; say so if asked).
- Whether a hybrid (e.g. re-grid + slight tempo nudge) is wanted — not sampled, would need Mars's parameters.
- Flash-gate re-check on any re-timed/re-gridded full video: owed before showing, not done here (samples are 480×270 demos, not finals).
- Click track: `song-beat-click-152bpm-20261101.wav` (1000 Hz pings at 0, 0.395, 0.789, … 3.947 s) is a grid reference only, never to be mixed into a final.

## Files in this folder

- `BEATSYNC-PREP-20261101.md` (this file), `beatsync_build_20261101.py`, `beatsync-timing-tables-20261101.csv`, `beatsync-option-tables-20261101.csv`, `song-beat-click-152bpm-20261101.wav`, `option-A-*.mp4`, `option-B-*.mp3`, `option-B-*-muxed-*.mp4`, `option-C-*.mp4`. All samples scaled to 480×270 where video; finals remain the 1920×1080 MP4s.
