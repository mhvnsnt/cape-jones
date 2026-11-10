# Clean shippable animations — 2026-11-01

## Correction applied, Mars 2026-11-01 13:55 / 13:56 CST

The banner and filename label were put on the wrong builds, and are removed
here. None of the builds below are that kind of build.

Narrow definition, Mars 2026-11-01 13:56 CST: that label applies ONLY to
an actual visual character from another show, or that character's
dialogue, when brought into our show. Nothing else is that.
Animation timing, animation structure, Cape Jones pieces, and the
A / B / C builds below are NOT that. No actual visual character from
another show, and no character dialogue from another show, is in any
build below, and none has been pulled in yet.

These are Cape Jones pieces only, arranged to donor timing/structure,
and are fine to ship as animation.

## Plain names only

- A = Smiling 9-layer structure
- B = Foster's punch/walk structure
- C = Smiling 5-layer structure

The arm-snap-fixed versions of A and C are the same builds, with only
one change: arms crossing the chest moved to on top of the torso.
Same poses, same timing, same sound, same background, nothing else
changed.

## Clean versions delivered

All 1100x750, 24fps, h264 + AAC, faststart, no banner on any frame,
no label in any new filename, same segments / timing / sound as the
original builds, arm-snap fix preserved in the two arm-snap-fixed
versions.

| Build | File | Frames | Video duration |
|---|---|---|---|
| A, Smiling 9-layer structure | A-SMILING-STRUCTURE-CLEAN-20261101.mp4 | 121 | 5.041667s |
| B, Foster's punch/walk structure | B-FOSTERS-STRUCTURE-CLEAN-20261101.mp4 | 164 | 6.833333s |
| C, Smiling 5-layer structure | C-SMILING-5LAYER-STRUCTURE-CLEAN-20261101.mp4 | 120 | 5.000000s |
| A, Smiling 9-layer structure, arm-snap-fixed | A-SMILING-STRUCTURE-ARM-SNAP-FIXED-CLEAN-20261101.mp4 | 121 | 5.041667s |
| C, Smiling 5-layer structure, arm-snap-fixed | C-SMILING-5LAYER-STRUCTURE-ARM-SNAP-FIXED-CLEAN-20261101.mp4 | 120 | 5.000000s |

MD5s:
- A clean: f9746ddac49aabab02e2845a2021a2fe
- B clean: 6d733f4e1d022a4574faf1ab3d8e7b10
- C clean: 2cc845a44b1a02ae5edcb806785ea76a
- A arm-snap-fixed clean: c9af0f19d05e10d3b8cb460eefd5a4f0
- C arm-snap-fixed clean: 13474f3e5eb79134add46bb4a965d7d9

Clean wav copies, same sound, no label in filename:
A-SMILING-STRUCTURE-20261101.wav, B-FOSTERS-STRUCTURE-20261101.wav,
C-SMILING-5LAYER-STRUCTURE-20261101.wav. GIF previews alongside each
MP4, same clean names. Builder: build_clean.py in this folder.

## Verification

- Filename check: no clean filename contains TEMPLATE or PLACEHOLDER.
  Checked by script, PASS for all 5 MP4s, 5 GIFs, 3 WAVs.
- Banner frame check: frame at 2s for each clean MP4, top strip
  y=5..50, x=300..800, fraction of near-black pixels = 0.000 for all
  5. The banner was a black box at y=10 in the old builds; it is
  gone in the clean builds. No banner text was re-added by the
  builder — the clean builder has no drawtext step at all.
- Frame counts match the original builds exactly: A 121, B 164,
  C 120, A arm-snap-fixed 121, C arm-snap-fixed 120.
- Flicker gate, whole-frame WCAG proxy, 12fps, threshold 25.5:
  A clean max jump 3.07, 0 flashes; B clean max jump 3.07, 0 flashes;
  C clean max jump 3.05, 0 flashes; A arm-snap-fixed clean max jump
  3.06, 0 flashes; C arm-snap-fixed clean max jump 3.06, 0 flashes.
  PASS, all 5.
- Arm-snap fix preserved: the arm-snap-fixed clean A and C were
  re-rendered from the arm-snap-fixed source videos, same segments
  as the arm-snap fix (A: 0-1.0, 1.5-2.5, 3.0-4.0, 4.5-5.58;
  C: 0-4.0), same 1s frozen stand, same original sound.

## Old bannered files — archived, not deleted

The 16 old bannered files (5 MP4s, 5 GIFs, 3 WAVs, 3 contact sheets)
are copied, untouched, in work/archived-bannered/ in this folder.
The originals in their original folders are also untouched and not
deleted, not overwritten. The clean versions are new dated files
only, in this folder.

## Still owed

- Mars approval of the clean versions: 0/1.
- Repo landing: local only, no PR claimed, not verified on main.
