# CAPE JONES + CHARLIE — FIRST PLACEHOLDER SIDE-CHARACTER INTERACTION
## ACTUAL DONOR CHARACTER PLACEHOLDER — DO NOT SHIP AS-IS — RESKIN PENDING
## Mars 2026-11-01 16:23 CST. Local only, no repo landing, no donor art shipped.

## What this is
First animated appearance on screen of a placeholder side character with Cape Jones.
Picked first: Charlie (Smiling Friends), because his XFL was already pulled and parsed
(9 top layers, 18 symbols). Cape Jones and Charlie are SEPARATE rigs, never merged.
Charlie's rig is NOT put on Cape Jones. No reskin in this job — Mars will say what to
change/edit about Charlie next, to make him a different original character.

## Running list
PLACEHOLDER-SIDE-CHARACTERS-LIST-20261101.md — 10 entries, Charlie YES animated,
Pim / Frankie / Randy NO not yet animated, Gumball / Darwin / Disney / Nickelodeon /
Foster's reels / Vault unsorted NO not yet pulled, not yet animated. Reskin 0 for all,
ship as final 0 for all, donor dialogue 0 lines, donor audio 0 streams.

## Charlie rig — own separate 2D layer rig, from his XFL
Source: actual-donor-placeholders-20261101/work/charlie_xfl, Charlie.xml, Animate 22.
Method: schematic XFL vector re-render (build_charlie_layers.py, adapted from the
prior render_xfl2.py), NOT an Animate render, NOT a Harmony render. No finished image
was edited; layers are rendered from the XFL shapes, grouped by Charlie's own top layers.
Layers, back to front, in charlie_layers/ (common canvas 984x1735, same as the prior
rig sheet render):
- Charlie_Back_Arm.png — bbox (117,544)-(328,966), 6,085 opaque px
- Charlie_Legs.png — bbox (308,1169)-(940,1696), 13,387 opaque px
- Charlie_Back_Hoodie.png — bbox (553,426)-(807,554), 2,985 opaque px
- Charlie_Head.png — bbox (39,40)-(729,622), 24,181 opaque px (hat, brows, pupils, mouth, scalp nested inside Head)
- Charlie_Body.png — bbox (321,887)-(946,1298), 9,644 opaque px
- Charlie_direct.png — bbox (39,374)-(399,612), 1,127 opaque px (body_thingies shapes)
- Charlie_Front_Arm.png — bbox (536,640)-(758,985), 2,771 opaque px
Torso Move symbol: its one shape is isFloating + alpha 0 in the XFL, so it renders
nothing here, same as the prior rig sheet. Charlie's torso in this re-render is
outline-only, not a filled white shape — that is why the test stage is light, not dark:
on a dark stage the torso interior reads as stage colour. No white torso fill was
invented as a new piece.

## Cape Jones rig — own rig, untouched
rig-apose-v7c-clean-transparent.png (1100x1500, bbox 248,253-876,1295), scaled to
720px tall in this test. Whole-plane moves only in this test (walk, bob, lean);
no Cape Jones piece was cut or changed here.

## Animation — animated, not stills
cape-jones-charlie-interaction-20261101.mp4 — 1920x1080, 24fps, 96 frames, 4.0s,
H.264 + AAC, 388,174 B, md5 7f379225a2c39588366511ee3d2ff90f, faststart moov box
at offset 32 (payload at 40), size 3,649 B, before mdat.
GIF: cape-jones-charlie-interaction-20261101.gif — 480x270, 48 frames, ~12.5fps
avg (80/90 ms frame delays; ffprobe 25/2), 4.0s, 585,418 B,
md5 37edf5762b8a7b63e7d7034192ef5e13.
Contact sheet: contact-sheet-charlie-interaction-20261101.png — 1920x1080 RGB,
298,680 B, md5 cc465e2e05ff5306c385564f8434314a (frames 1, 24, 36, 60, 72, 96).
SFX: interaction-sfx-20261101.wav — 4.0s, synthesized only (footstep thumps,
wave blips), 176,444 B, md5 687c6e8e3a03bbd89bff0569cd8a6c46. No dialogue,
no donor audio, no song.
Timeline:
- f1-f24 (0.0-1.0s): Cape Jones walks in from left to x=430, bobbing, feet on ground.
  Charlie idle, small bob.
- f25-f48 (1.0-2.0s): Cape Jones stops, leans toward Charlie. Charlie head turns
  -6 deg toward Cape Jones, front arm raises to -35 deg (wave start).
- f49-f72 (2.0-3.0s): Charlie reacts — head nod, front arm waves -25 +/- 20 deg,
  body bounce. Cape Jones nods back.
- f73-f96 (3.0-4.0s): both settle to idle, grounded.
Stage: simple light test stage, ground line y=950, NOT a painted background.
Charlie feet land on the ground line (canvas foot y1696 scaled +15px correction
applied after the first render floated 15px above ground). Cape Jones feet on
ground line; walk bob is a bounce, not a lift, both grounded throughout, no
airborne label needed.
Top banner burned into every frame: "TEST ONLY - CHARLIE = ACTUAL DONOR
CHARACTER PLACEHOLDER - DO NOT SHIP AS-IS - RESKIN PENDING".

## Still off, plainly — do NOT hide this
- XFL schematic gaps carry over: head sits apart from the torso outline, torso is
  outline-only, pants/legs fills are partial in the layer re-render (the prior
  whole-figure rig sheet reads more solid because it was drawn on white). This
  animation looks like a schematic test, not a finished Animate render.
- A true Animate/Harmony render of Charlie would close the head/body assembly
  and fill the torso/pants — that needs a real Animate/Harmony binary, not
  available in this job, and no render was faked.
- Charlie's front-arm wave rotates the whole Front Arm layer about its top
  pivot; it is a layer rotation, not a bent-elbow FK pose. Legs do not walk;
  Charlie stays planted while Cape Jones walks in.
- Cape Jones does not gesture with a separate arm piece in this test; his
  wave is a whole-plane lean/bob. A Cape Jones arm-wave piece swap is a
  follow-up if Mars wants it.

## Files
- build_charlie_layers.py, build_interaction.py (builders, in this folder)
- charlie_layers/ (7 layer PNGs above)
- frames/frame_001.png - frame_096.png
- contact-sheet-charlie-interaction-20261101.png (frames 1, 24, 36, 60, 72, 96)
- cape-jones-charlie-interaction-20261101.mp4 / .gif / interaction-sfx-20261101.wav
- PLACEHOLDER-SIDE-CHARACTERS-LIST-20261101.md

## Verification — finish-all job, 2026-11-01 16:52 CST (no rebuild; files as built 22:37 UTC)
Re-measured, all pass, no video rebuilt:
- MP4 decodes clean (ffmpeg -f null, DECODE_OK); ffprobe: H.264 1920x1080,
  24/1 fps, 96 frames, 4.000s; AAC mono 22050 Hz, 4.000s; single video + single
  audio stream, no second audio/dialogue stream.
- Faststart: ftyp 32 B at 0, moov box at offset 32 (3,649 B), before mdat.
- Animated, not stills: all 96 frame thumbnails unique (96/96). Thumbnail mean
  abs diff: f1-vs-f2 1.25, f1-vs-f12 11.97, f1-vs-f24 12.06, f24-vs-f48 1.71,
  f48-vs-f60 1.33, f60-vs-f72 0.83, f72-vs-f96 1.27, f1-vs-f96 11.92 — walk-in
  movement large, idle/wave phases small but non-zero.
- Separate rigs: build_interaction.py loads Charlie only from charlie_layers/
  (7 PNGs, common canvas 984x1735, bboxes/opaque px re-measured and matching
  the layer list above) and Cape Jones only from rig-apose-v7c-clean-transparent.png
  (1100x1500, bbox 248,253-876,1295, untouched, 468 KB, 20261031). Pasted as
  separate planes; no Charlie piece merged onto Cape Jones, no Cape Jones piece cut.
- Grounded: ground line y=950 sampled (60,50,40) in f1/f48/f96; builder aligns
  both characters' feet to y=950, bob is a downward bounce (feet at or just below
  the line), never a lift above it — no airborne frames, no airborne label needed.
- Banner present in sampled frames (black bar, top row y=10): "TEST ONLY -
  CHARLIE = ACTUAL DONOR CHARACTER PLACEHOLDER - DO NOT SHIP AS-IS - RESKIN PENDING".
  No dialogue text in frames beyond the banner/footer labels; SFX wav is mono
  22050 Hz, 4.0s, 88,200 frames, max amp 9,490, synthesized tones only per builder
  (footsteps + blips) — no donor audio, no speech stream.
- Side-character list re-checked: 10 entries — Charlie YES animated; Pim, Frankie,
  Randy NO not yet animated; Gumball, Darwin, Disney, Nickelodeon, Foster's reels,
  Cartoon Vault unsorted NO not yet pulled / not yet animated. Reskin 0, ship 0
  for all; donor dialogue 0 lines, donor audio 0 streams for all.
- Corrections made in this verification only (report text, not media): moov
  offset 36 -> 32 (payload 40); GIF 12fps -> ~12.5fps avg, 48 frames; contact
  sheet size/md5 added. Media md5s unchanged from the original report.
- Deletions in this job: 0. Reskin: 0. Repo landing: none. Donor art stays local.

## Status
- Approval: 0/1 — Mars has not seen this interaction yet.
- Reskin: 0 — Charlie is NOT reskinned here. Next step is Mars's call: what to
  change/edit about Charlie to make him a different original character.
- Repo landing: local only, no PR claimed, not verified on main. Donor art
  stays out of the public game repo.
- Originals untouched: actual-donor-placeholders-20261101/ and Cape Jones
  rig-apose files unchanged.
