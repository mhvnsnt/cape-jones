# Beat-Sync Presets — Cape Jones Dance — 2026-11-01

**Mars decision, 2026-11-01 17:33 CST: approve all three, save all three as presets,
choose A for this one, keep B and C as alternate presets to swap back to later
for tempo / speeds for dances.**

This index does NOT re-render any final. The samples below are the Batch C
one-loop demos already landed on main in PR #352 (Batch E, E5). No sample is
re-landed by this preset index. A full-length cut using any preset still needs
its own re-cut / re-time, plus a flash-gate re-run, before showing.

## The mismatch these presets fix

- Song: 152 BPM, C major, 48 bars, 75.789 s, 192 beats. Song beat = 0.39474 s.
- Visual grid: ~107 BPM nominal (measured 105.4 BPM on the v2 loop).
  Visual beat = 0.56075 s; 135.2 visual beats fit in 75.789 s.
- Drift if nothing changes: song gains 0.750 beats per second on the visual;
  56.8 beats apart by the end of 75.789 s.
- Source detail: `batch-c-gif-principles-beatsync-20261101/beatsync/BEATSYNC-PREP-20261101.md`
  (already on main, PR #352). Samples use EN song + the shared visual; JP timing
  is identical (same 75.789 s, same BPM), but no JP sample was rendered.

## Preset A — CHOSEN FOR THIS ONE

- Name: **Preset A — Re-time visual to 152 BPM**
- Status: **CHOSEN for this one (Mars, 2026-11-01 17:33 CST)**
- What changes: visual playback x 1.42056 (152/107). Dance 42% faster.
- Song: untouched — 152 BPM, 75.789 s, pitch unchanged, vocals natural.
- Visual: a 123-frame loop (5.125 s) becomes 86.6 frames (3.61 s).
  Full 75.789 s visual becomes 53.35 s of picture at song speed, so the loop
  repeats ~21.0 times instead of 14.8 to fill the song (or the cut is re-timed).
- Trade-off, plainly: snappier, but holds shorten and the on-2s feel may turn
  choppy; fast sections held to 2s in v2 for flash safety get faster again —
  flash gate MUST be re-run on the re-timed full video before any showing.
- Sample (already on main, PR #352):
  `batch-c-gif-principles-beatsync-20261101/beatsync/option-A-retime-visual-152bpm-sample-20261101.mp4`
  — 3.750 s, 480x270, 24 fps, h264 + AAC, 152 BPM click overlaid (grid
  reference only, never to be mixed into a final), 185,604 bytes.

## Preset B — ALTERNATE PRESET (not chosen for this one)

- Name: **Preset B — Stretch audio to ~107 BPM**
- Status: **ALTERNATE PRESET — saved to swap back to later, NOT chosen for this one**
- What changes: song tempo x 0.70395 (107/152). Visual stays at its current speed.
- Song: 75.789 s -> 107.66 s (+31.87 s). Dance loop repeats ~21.0 times
  instead of 14.8 to fill it (or a longer cut).
- Visual: unchanged speed, dance feel preserved exactly.
- Trade-off, plainly: dance feel preserved, but the song is no longer the
  152 BPM song. Atempo variant keeps pitch but has time-stretch artefacts
  (smearing on vocals/sibilants) at 0.70x, to be judged by ear. Resample
  variant has no stretch artefacts but drops pitch by -6.08 semitones
  (wrong key, slowed-down / record-dragging sound) — almost certainly not
  shippable as the song, included only so Mars can hear the difference.
- Samples (already on main, PR #352):
  - `batch-c-gif-principles-beatsync-20261101/beatsync/option-B-stretch-audio-atempo-sample-20261101.mp3`
    — pitch preserved, 14.187 s, 228,040 bytes.
  - `batch-c-gif-principles-beatsync-20261101/beatsync/option-B-stretch-audio-pitchdrop-sample-20261101.mp3`
    — pitch -6.08 semitones, 14.206 s, 228,040 bytes.
  - `batch-c-gif-principles-beatsync-20261101/beatsync/option-B-stretch-audio-muxed-sample-20261101.mp4`
    — one-loop visual + atempo audio head, 5.271 s, 284,236 bytes.

## Preset C — ALTERNATE PRESET (not chosen for this one)

- Name: **Preset C — Re-grid visual to song beats**
- Status: **ALTERNATE PRESET — saved to swap back to later, NOT chosen for this one**
- What changes: playback speed NOT changed uniformly. Each key / SFX event
  moves to its nearest song-beat frame (snapped to even frames, on-2s); holds
  between events absorb the shift.
- Song: untouched — 152 BPM, 75.789 s, tempo, pitch and length all stay.
- Visual: poses and order kept; phrase rhythm changes. Original segments
  14, 13, 14, 27, 14, 14, 14, 13 frames -> re-gridded segments
  10, 8, 10, 20, 8, 10, 10, 10 frames. The double-beat hold 41->68
  (27 frames) becomes 20 frames over 2 beats.
- Trade-off, plainly: song untouched and poses kept, but some holds shrink
  (e.g. 14 -> 8 frames). For a keys-only loop C lands very close to A,
  because the loop has no in-between motion, only holds. The difference
  matters once in-betweens exist: A speeds the motion itself, C only
  re-cuts the holds. Requires a real re-cut of the full 75.789 s
  (loop re-cut x ~21 song-beat loops), not just this demo; flash gate
  must be re-run, because shorter holds mean faster key changes.
- Sample (already on main, PR #352):
  `batch-c-gif-principles-beatsync-20261101/beatsync/option-C-regrid-visual-sample-20261101.mp4`
  — 86 frames, 3.583 s, 480x270, 24 fps, 152 BPM click overlaid
  (grid reference only), 179,284 bytes.
  Note: Mars reported at 17:34 CST that C would not play for him on first
  send; the parent re-sent C in chat. This file itself is unchanged
  from the Batch C sample verified on main in PR #352.

## How to swap presets later

1. Pick the preset by name (A, B, or C) — do not re-invent the numbers.
2. Apply only that preset's method to the full cut (A: uniform x1.42056;
   B: audio x0.70395, atempo unless Mars picks the pitch-drop variant;
   C: segment re-grid per `beatsync-option-tables-20261101.csv`).
3. Re-run the flash gate on the full re-timed / re-gridded video before
   showing it. Samples are 480x270 demos, not finals.
4. Record the new cut as a new dated file; never overwrite a Mars-seen
   version unless Mars explicitly authorises replacement.
5. A preset being saved here is NOT an approval of a full-length cut
   made with it. Full cuts are 0/1 until Mars sees and approves them.

## Files

- This index: `beatsync-presets-20261101/BEATSYNC-PRESETS-20261101.md`
- All samples and tables: already on main, PR #352, under
  `batch-c-gif-principles-beatsync-20261101/beatsync/` (see sample paths above).
- No deletions in this landing. No donor art, no show audio, no song
  re-master is claimed here.
