# Cape Jones hallway parody — GB214 "The Words" Sc057 + Sc059

Cape Jones placed in Darwin's hallway dance slot, driven by the extracted
choreography (`../dance-gumball-darwin-words-sc057-sc059.json` + `../hallway-study-data.json`).
1920x1080, 25 fps, 303 frames (Sc057 198 + Sc059 105), production audio
(audio057 under Sc057, audio059 under Sc059, trimmed to frame durations).
MP4 is fragmented-MP4 (empty_moov) because this build lane encodes to a pipe;
it plays in browsers/players as-is and can be faststart-remuxed losslessly.
(Recovery build: encoded per scene to pipes — each scene blob persisted to
GitHub the moment it finished, after two runs were killed by VM reboots —
then joined with the ffmpeg concat demuxer, stream copy, no re-encode.)

## What drove each Cape Jones part
- **Root (position/scale):** Darwin's orange-pixel bbox measured per frame from
  the HD renders — bottom-center = feet anchor, bbox height = CJ figure height,
  sampled on twos. Sc057 height grows 95px -> 244px across the shot.
- **Head:** Darwin's head-comp keyframes — rotation from the matrix (atan2(b,a)),
  scale (relative, exponent 0.55), tx/ty normalized around the track median.
- **Legs:** Darwin's leg symbol keyframes (Layer 22 / Layer 23) — rotation from
  symbol matrices where a symbol instance exists, held pose-to-pose. In Sc057
  the clean-leg symbol track is sparse (the wide-shot legs were hand-drawn), so
  a bbox-aspect spread (measured bbox width/height) fills the stride there.
- **Torso:** lean derived from the extracted head-comp rotation (x0.35) plus
  root-velocity tilt. Derived, not a separate Darwin torso track.
- **Arms — GAP:** no fin/arm symbol track exists on either main puppet timeline
  (Sc057/Sc059 arms are hand-drawn 'rough arms' shape passes with no per-part
  transform to extract; the rough shapes' signal was not usable as a rotation
  track in this build). CJ's arms ride the torso and counter-rotate from the
  extracted head-comp rotation. This is derived coupling, NOT extracted arm
  choreography — named here as the build's biggest honest gap.
- **Cape — PROCEDURAL (disclosed):** Darwin has no cape; his tail was never
  placed in these puppets. CJ's cape is a pendulum lagging the root track's
  horizontal velocity. The one procedural piece in the build.
- **Flip / twist (Sc059):** both Darwin placements are flipped (negative a) and
  CJ is mirrored to match. In the twist (f43-97), CJ's whole-figure scaleX
  follows the measured bbox aspect vs its wind-up baseline; at the deepest
  squash (<0.5) he mirrors — a back-view suggestion. **GAP: CJ has no back-view
  head** (the source swaps in a drawn back-view head fragment); the front head
  is kept, mirrored.
- **Darwin removal:** orange mask (R>200, 90<G<190, B<90) dilated, plus green-shoe
  and median-difference pixels inside his expanded bbox (extended below the bbox,
  where his green shoes hang). Sc057: masked pixels are inpainted from the frame
  itself per frame (Telea). RECOVERY ITERATION: the first build filled Sc057 from
  the temporal median, but visual QA of that build proved the median itself is a
  Darwin ghost (he occupies the dance zone in most samples) and it smeared orange
  around CJ while his shoes survived below the bbox — the fill was changed to
  inpaint and the plate region extended downward; the median is kept only as a
  difference reference. Sc059's Darwin never leaves his area, so his plate is the
  temporal median with his union mask inpainted once (Telea) — sound there
  because inpaint discards the median inside the union. Head-symbol rotations
  beyond +/-90 deg in the source track (the symbol's back-view flips, atan2
  ~ +/-180) are folded to the equivalent near-level tilt — CJ has no back-view
  head (same gap as the Sc059 twist); the first build applied them raw and CJ
  tumbled upside-down at the Sc057 finale. Onlookers, crowd, hallway and
  framecounter stay because the plates are built from the frames themselves.

## Verification (numeric, this lane cannot write local media files)
- Distinct (head, leg_l, leg_r) poses across 303 frames: 71
- CJ skin-tone pixels present in every frame where the source dancer is on screen (min per frame): 147914 — 7 Sc059 entry frames have no Darwin in the source at all (he enters from off-screen right), so those frames are the clean plate with no CJ, by design.
- Max residual Darwin-orange pixels in any cleaned plate: 0
- Max residual shoe-green pixels in any Sc057 plate region: 1163 (new metric from the recovery iteration; the first build never measured the shoes)
- MP4 bytes: 2386447 · Contact sheet: `cape-jones-hallway-parody-sheet-20261102.png` (9 frames)
- Full per-frame stats were printed by the build run and are summarized in the PR body.

## Puppet
`cj_puppet/` — the working Cape Jones puppet as used: full-canvas part layers
(1198x1111, alpha respected; transparent pixels carry white RGB but alpha 0),
`pivots.json`, and `puppet.json` (slots, anchor, canon colours). Sock layers are
included for completeness; they sit at shoulder height in the source art and
were not placed in this build.
