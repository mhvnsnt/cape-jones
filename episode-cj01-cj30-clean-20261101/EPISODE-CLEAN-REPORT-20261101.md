# Clean full episode CJ-01 to CJ-30 — 2026-11-01

Mars approval 2026-11-01 16:20 CST: clean shots CJ-01 to CJ-30 approved, 30/30.
This is the clean episode cut built from those approved shots only. Approval of
this episode cut itself: 0/1. Repo landing: local only, no PR claimed, not verified on main.

## Sources — ONLY clean plates, no erased versions
- CJ-01 to CJ-10: shots-CJ01-CJ10-layer-removed-20261101/finals/ (layer removal by code:
  labels layer off, elbow/knee cap layer off, plates re-rendered, shots re-composited).
- CJ-11 to CJ-30: shots-final-painted-bg-20261101/finals/ originals (0 debug orbs in their plates).
- NOT USED: shots-CJ01-CJ30-no-orbs-20261101/ erased/cropped versions, and NOT USED:
  superseded episode-cj01-cj30-picture-20261101.mp4 segments for CJ-01 to CJ-05.
- Clean source copies for this cut are in finals/ in this folder, originals untouched.

## Deliverables
- episode-cj01-cj30-clean-20261101.mp4 — 1920x1080, 24fps, 90.0s, 2160 frames, h264 + AAC,
  faststart, 39,085,468 bytes, md5 05c5a0ec7bb2fd07270cc16188992170, moov at 36.
- episode-cj01-cj30-clean-20261101-chat.mp4 — 960x540, 90.0s, h264 + AAC, faststart,
  8,729,599 bytes, md5 5e5ab274f0bcb944ca87deafefa30508, moov at 36.
- episode-audio-clean-20261101.wav — 90.0s, synthesized SFX + synthesized ambient pad bed,
  peak -1 dBFS, md5 9d3988999e0eb26cbd789bb2138ca99e.
- DIALOGUE-LINE-SHEET-20261101.md — dialogue slots for THIS episode, 30/30 listed, 0/30 filled.
- Builders: work/build_clean_episode.py, work/build_dialogue_sheet.py, work/encode.log, work/verify.log.

## Structure — same 90s structure as the picture version
30 shots x 3.0s in order CJ-01 to CJ-30, 72 frames each, first 12 frames of each segment
after the first are a cross-dissolve from the previous shot, slow camera zoom 1.00 to 1.03
alternating direction per segment, per-shot whole-final motion (punch lunge/thrust/recover,
walk drift+bob, dance bob+sway, flying drift, flex tighten pulse, jump arc, seated lean,
dialogue head-height bob only, rooftop slow push+sway). Taller finals fit to 1080 height and
pillarboxed on a blurred extension of the same image — never cropped, never squashed.
Lighting arc, scene-based, smoothed by dissolves (not one forced monotonic sunset line):
golden afternoon CJ-01 to CJ-04, neutral CJ-05 to CJ-06, warm town CJ-07, night alley CJ-08,
evening stage CJ-09 to CJ-11, flying day CJ-12 to CJ-15, plaza afternoon CJ-16 to CJ-20,
rooftop CJ-21 to CJ-22, indoor lamp CJ-23 to CJ-25, neutral CJ-26, red shout CJ-27,
sunset CJ-28, night city CJ-29, neon dual light CJ-30.

## What is animated vs what is still held — plainly
Animated: whole-final motion per shot against its painted background, camera zoom, dissolves.
Still held, NOT claimed: no new rig poses keyed inside a segment, no limb-level animation
(no elbow/knee bend change, no mouth change, no cape flutter, no walk-cycle leg swap),
no Blender EEVEE sequence, no Harmony sequence. Punch progression happens ACROSS
CJ-01 to CJ-02 to CJ-03, as the shot list is built. Dialogue shots have no voice, no lip
movement, no lines in the video.

## Audio — full, plainly labelled
- Synthesized SFX per shot type: punch whoosh/impact, walk footsteps, dance beat blips,
  flying wind, flex thump, jump whoosh/land, room hum, rooftop wind, neon hum.
- Synthesized ambient pad bed: low sine chords per scene block, labelled synthesized,
  NOT the Cape Jones Dance song, NOT donor/show audio, NOT a vocal track.
- No dialogue, no song, no donor audio, no show audio in this cut.
- Loudness measured by ffmpeg ebur128: integrated -22.1 LUFS. NOT -14 LUFS, NOT claimed locked.
  Peak -1 dBFS. A final -14 LUFS audio pass is still owed after dialogue is recorded.
- Flash gate, WCAG-inspired proxy only, NOT Harding/PEAT certified: 1080 samples at 12fps,
  max whole-frame mean luminance jump 10.90, 0 flashes over the 25.5 threshold, PASS as proxy only.

## Dialogue — answer to Mars's question
These dialogue slots ARE for THIS episode, CJ-01 to CJ-30, not for another project.
They are currently 0/30 filled, by design. Mars writes and records them.
Fill order: CJ-26 first (dialogue-neutral-unsure, 01:15-01:18), then CJ-27
(dialogue-shout-angry, 01:18-01:21), then the other 28 shots only if Mars wants a line there.
The line sheet lists every slot with shot, character (Cape Jones, alone in frame),
emotion/context from the shot spec, and a BLANK line for Mars to write/record.
No dialogue text is invented anywhere in this cut or sheet, and no blank is presented as a finished line.
Dialogue-primary slots: 2 (CJ-26, CJ-27). Action slots with no dialogue required in picture cut: 28.

## Still owed after this cut
1. Episode cut approval: 0/1.
2. Dialogue: 0/30 — Mars writes/records, CJ-26 first, then CJ-27.
3. Audio pass to -14 LUFS: 0/1 — after dialogue, not claimed now.
4. Picture Lock: 0/1. QC: 0/3 queues. Delivery: 0/1 — frame size / safe areas still Mars-set.
5. Full rig animation per shot: 0/30, separate pass, not claimed here.
6. Repo landing: local only in this folder.
