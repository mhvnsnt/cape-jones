# Dance recreation — original dances, rebuilt correctly (2026-10-31)

2D side only. 2.5D/3D effects are flavour only here; this is not a 3D project.

## 1. What "the original dance videos" are — identified, not guessed

Searched: dance-improved-20261031, dance-kneefeet-fix-20261031,
dance-kneefeet-fix-correction-20261031, dance-arm-snap-20261031,
mochiichao-combine-build-20261031, clips-v7c/dance, gap-close-sound-edit
dance sequence, and all rig *.md for a song title. No other Cape dance
video exists on disk as a rendered sequence.

| Candidate | File | Frames | Status before this task |
|---|---|---|---|
| Improved dance (main dance, 8-beat phrase) | dance-improved-20261031/dance-improved-20261031.gif/.mp4 | 63 keys, f001..f109 on twos | Built+viewed, NOT approved. Defects: weak/tangled kick f042, twist is a stand-in (no true torso twist), JoJo-tension gain shifts cape pink on twist frames, no beep audio, no background-life, no clean full-size final render. |
| Knee-feet v1 fix | dance-kneefeet-fix-20261031/dance-kneefeet-20261031.gif | 63 | SUPERSEDED — block-range FootIn was wrong in both directions. |
| Knee-feet CORRECTION | dance-kneefeet-fix-correction-20261031/dance-kneefeet-corrected-20261031.gif | 63 | APPROVED 100% PERFECT by Mars 2026-10-31 17:50-17:51 CDT. Per-frame rule: FootIn ONLY IF leg_upper L > 0 AND R < 0. |
| Arm-snap rebuild (LATEST corrected dance) | dance-arm-snap-20261031/dance-arm-snap-20261031.gif | 63 keys, f001..f109 | Built+viewed, approval 0/1. This is the knee-feet correction REBUILT with arm-front-snap (whole arm chain above torso on crossed frames, 21/63 frames snapped, 30 side-snaps). This is the base used for Recreation A. |
| Combine dance (108f version) | mochiichao-combine-build-20261031/dance-clip-combined-20261031.gif/.mp4 | 108, f000..f107 consecutive, 24fps | Built+viewed, approval 0/4 for the combine as a whole. Bright Pink JoJo Tension on twist frames 68-94 returning to base, device prop at lap NOT gripped (two-hand grip still owed), background-life loops separate. Base used for Recreation B. |
| Gap-close dance sequence edit | gap-close-sound-edit-20261031/dance-sequence-edited-20261031.mp4 | 109f edit | Built, carries the same weak-kick + stand-in twist defects, named in its own report. Not used as a base — it is an edit of the same material. |

There is NO separate "original dance video" file outside this lineage.
The Gumball "The Words" dance is a REFERENCE only (verified dance in a
show repo, beat grid ~14f @25fps ~107 BPM) — it is not a Cape video and
was not used as footage.

## 2. What was incorrect, and what this recreation corrects

Recreation A (main dance) starts from the arm-snap frames, so it already
carries, in order: (1) knee-feet per-frame correction (approved perfect),
(2) arm-front-snap (whole chain, per frame per side, gate >1000px
forearm-vs-torso overlap), (3) face/cowl snap where applicable — no
inbetween in this build introduces a new buried arm: inbetweens are
blends of two already-corrected neighbours, so layer order is inherited,
not re-decided. Hand-first rule: fists stay curled per the beat sheet;
no fist was swapped in this build (approved flipped fist is a punch
piece, not a dance piece — swapping it into the dance unasked would be
a change, not a correction, and is left as a future variant).

Retained defects, NOT hidden and NOT fixed by inbetweening:
- Kick at f042 remains weak/tangled in the source keys (legs cross) —
  an inbetween cannot straighten a kick. Reworked kick pose still owed 0/1.
- Twist (frames 69-82) remains an asymmetric-arms/legs stand-in — no
  true torso/head twist piece exists yet. True twist still owed 0/1.
- Recreation B retains: JoJo tension on twist frames, device-at-lap
  (not gripped) framing from the combine source, and its grey-canvas
  background (combine frames are RGB, not transparent).
- Image-interpolation ghosting: fast moves soften/double-edge slightly
  in inbetween frames (visible on the f015 strip, legs). This is the
  honest cost of image interpolation vs a rig re-pose; at 48fps it
  reads as motion blur, not as a broken limb, and no inbetween was
  shipped that breaks knee-feet or arm-snap direction.

## 3. New videos — viewed, timing preserved, higher frame density

Method: IMAGE-INTERPOLATION (alpha cross-blend t=0.5 between consecutive
timeline steps). Labelled as such everywhere — this is NOT a rig re-pose
and NOT a claim that new joint angles were drawn.

Recreation A — MAIN DANCE:
- Base: 63 arm-snap keys f001..f109 on twos -> filled to the 109-step
  grid -> 1 further inbetween per step = 217 frames.
- Playback: 48 fps, 4.52 s (same duration as the 109-step phrase at
  24fps on twos; drawings/sec doubled twice over the original 80ms GIF).
- Files: dance-recreation-main-20261031.mp4 (550x750, 48fps, 217f),
  dance-recreation-main-20261031.gif (440x600, ~50fps GIF timing).
- Contact: contact-a-transition-f015-20261031.png,
  contact-a-transition-kick-20261031.png (key -> inbetween -> key, viewed).

Recreation B — COMBINE DANCE:
- Base: 108 consecutive frames f000..f107 -> 1 inbetween per pair =
  215 frames.
- Playback: 48 fps, 4.48 s (same duration as 108f @24fps; drawings/sec
  doubled from 24 to 48).
- Files: dance-recreation-combine-20261031.mp4 (550x750, 48fps, 215f),
  dance-recreation-combine-20261031.gif (440x600, ~50fps GIF timing).
- Contact: contact-b-transition-20261031.png,
  contact-b-transition2-20261031.png (viewed).

Full-size inbetween frames: frames-a/ (217 PNG, 1100x1500),
frames-b/ (215 PNG, 1100x1500). Builder: build_recreation.py.

## 4. Audio — SILENT, with a swappable EN/JP slot (no song invented)

No song title, no English audio, no Japanese audio, and no lyric file
for a Cape Jones dance song exists in any rig doc or folder searched.
The only "song" hits on disk are unrelated: a Scooby-Doo ep. 607 song
animatic (show-repo audit, baked video timing only, not a Cape song)
and Mochiichao Academy "Dance, Song" lessons (a game-system label, not
a song). NEITHER was used, and no song or lyrics were invented here.

Videos are therefore delivered SILENT (no audio track), labelled as
such, with the audio slot documented in AUDIO-SLOT-EN-JP-20261031.md.
The SAME visual cut works for both language versions: same timing,
same edit points, audio is a track swap, not a rebuild.

MARS-ONLY INPUT NEEDED (1 item, blocks the EN/JP audio, not the visuals):
- The song: title / which song, AND either (a) the English audio file
  + the Japanese audio file, or (b) his instruction to source them.
  Until then, do not present any tone, beep, or demo cue as the song.
  (Existing demo tones / cue sheet are metronome/cue material only,
  not song audio, and were not mixed into these videos.)

## 5. 3D-side note (short, as ordered — 2D is the focus)

Methods from this build that also help the 3D side later, without
turning this into a 3D project: (1) timing-grid + inbetween method —
a 48fps interpolated cut gives the 3D side a denser timing reference
for retargeting keys; (2) per-frame rule tables (knee-feet, arm-snap)
as data — the same per-frame decisions map to bone/layer order in a
3D rig; (3) the EN/JP track-swap edit structure — audio tracks as
swappable layers, not baked edits, which is how a 3D cut would also
version languages. No 3D model, rig, or render was built here.

## 6. Approvals / limits
- Mars approval: Recreation A 0/1, Recreation B 0/1. NOT claimed approved.
- No repo push in this task.
- Still owed (unchanged): reworked kick 0/1, true torso twist 0/1,
  two-hand device grip 0/1, song EN+JP audio (Mars-only, above),
  background-life behind the main dance 0/1, clean full-size final
  render with lighting 0/1, rig-angle inbetweening (vs image
  interpolation) as a future pass 0/1.
