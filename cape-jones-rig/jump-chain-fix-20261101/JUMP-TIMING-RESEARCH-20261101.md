# Jump timing research — 2026-11-01

Question from Mars, 2026-11-01 00:40 CDT: the jump chain is too slow, how many
frames should a jump have, speed it up ~2x or ~3x without cutting any motions
or frames out.

## What the sources actually say (no single canonical number)

Sources are general animation guides, searched 2026-11-01. None of them gives
one magic "a jump is N frames" for every character — timing depends on weight,
height, and whether holds/return are counted. Ranges below are what the
sources do agree on, at 24 fps:

- Full simple jump example (anticipation + jump + landing, 2 seconds):
  ~48 frames at 24 fps.
  Source: https://www.jklmn.top/posts/the-jklmn-guide-to-anticipation-animating-a-jump-with-a-simple-cat-and-couch-analogy
  Same source, live timing: crouch ~0.3-0.5s (7-12f), the jump itself
  ~0.2-0.3s (5-7f) for the launch portion.
- Phase breakdown (action only, no holds):
  anticipation 8-12f, airborne 16-24f, landing recovery 6-10f.
  Total action: 30-46 frames.
  Source: https://educationalvoice.co.uk/animation-best-practices-2/
- Key-pose example (keys only, not a full duration):
  standing 0, knees bent 5, takeoff 10, mid-air 15, landing 20, standing 25.
  Source: https://www.reilsolar.com/pdf/concept-of-frames-in-animation-how-to-set-frames-for-animating-body-in-dimension-3d/
- Gravity rule (Disney / PoAP, at 24 fps): everything falls 1 foot in
  6 frames, so a 1-foot jump takes 6 frames up to apex and 6 frames back
  down. Height sets airborne time; taller jump = more frames, not faster
  playback.
  Source: http://algarcia.org/Talks/PoAP_Slides.pdf
- Principles behind all of the above: squash and stretch, anticipation,
  timing and spacing — Williams, The Animator's Survival Kit; Lasseter's
  12 principles summary at
  https://courses.cs.washington.edu/courses/cse458/20au/content/exercises/animation_principles.html
  (about five key poses make a jump read: anticipation crouch, takeoff,
  apex, fall, landing recovery).

## How the old chain compares

Old chain-jump: 62 frames @24fps = 2.58s total, including apose holds,
per-key holds (4-5f each), 7 inbetweens per transition, overshoot + settle,
and a return to apose.
- Single jump, crouch hold to land hold (f10-f49): 40 frames = 1.67s.
- Airborne part, takeoff to land (f22-f49): ~28 frames, inside the
  16-24f airborne range plus landing holds.
- So the old chain is NOT wildly over-framed for a full loop — it feels
  slow because every key is held 4-5 frames and the whole loop returns
  to apose. Speeding up playback (Mars's own suggestion, 2x/3x) fixes
  the feel without re-timing keys or cutting a single motion.

## What was done here (no frames cut)

Same 62 frames, same keys, same angles, same flight line
(crouch 0px -> takeoff 30px -> tuck apex 100px -> land 0px).
Only playback rate changes:
- 1x: 62f @24fps = 2.58s (layer-fix reference only)
- 2x: 62f @48fps = 1.29s
- 3x: 62f @72fps = 0.86s
MP4 frame counts verified by ffprobe: 62/62/62. No motion, key, or frame
was deleted. GIFs are previews only: GIF encoding collapses identical
hold frames (43 seekable frames, same as the original GIF) and rounds
durations to 10ms steps, so GIF totals are 2.51s / 1.24s / 0.71s — the
3x GIF actually runs ~3.5x. Judge speed on the MP4s, not the GIFs.
