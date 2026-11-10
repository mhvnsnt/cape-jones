# Comparison tests — Workstream G, 2026-10-31

Standing rule (COMPARISON-TESTS.md): a test counts ONLY when BOTH sides have a
viewed file. A one-sided test is 0/1, not a win. "Better" must name what is
better. Trial/subscription status must be logged per test — never test a tool
we do not legitimately have access to at that time.

## Full counted result: 0/7

No Harmony, Animate, After Effects, or Maya file exists on the "their" side in
this batch, and no Harmony/Animate trial install was verified here (no binary,
no trial day logged — trial status is UNKNOWN in this batch, not "day X/14").
So no test below is counted as a full win, equal, or loss. Anything else would
be inventing their side.

## Per-test status (our side = viewed file unless noted; their side = absent)

1. Rig pose — OUR side ready: rig-apose-v7c-clean-transparent.png (478,221 bytes,
   on main, size-matched) + reposes-v7c-clean fighting pose (approved 15:00 CDT).
   THEIR side: no Harmony pose file. Verdict: NOT RUN (0/1).
2. Timeline / xsheet — OUR side run this batch: tahoma-cape-jones-24f/ (24 frames
   + xsheet JSON, beats 1,7,13,19) and ffmpeg-24f-beat-20261031.mp4 (ffprobe:
   24 frames @ 24fps). THEIR side: no Harmony/Animate xsheet file.
   Verdict: NOT RUN (0/1). Our timeline operation alone is proven, not compared.
3. Deformation — OUR side ready: v7c ball-centre pivots 4/4 + round-masked caps
   (cut-limbs-v7c/*, OutFixed pieces). THEIR side: no Harmony deformation file.
   Verdict: NOT RUN (0/1).
4. Drawing substitution — OUR side run this batch: pil-outfixed-vs-original-20261031.png
   + per-row span check 289/289 + check_gauntlet_flip.py 5/5 PASS, driver
   |arm_lower| >= 120 + forearm in front (pose_driven_swaps.json).
   THEIR side: NO rendered file — but the industry METHOD is documented in
   GAUNTLET-FLIP-RULE.md (Toon Boom multi-pose drawing substitution + Maya pose
   deformer / Blender corrective shape keys). Provisional method assessment
   (NOT counted): EQUAL on method — our swap preserves per-row x-ranges exactly
   and puts panels outward/camera, which is what the documented method requires.
   What would turn this into a counted test: the same flip built in Harmony
   trial and its file viewed side by side.
5. Export — OUR side run this batch: blender-compositor-apose-20261031.png
   (VIEWED, 887,145 bytes) + ffmpeg-lut-neutral-apose-20261031.png (VIEWED) +
   ffmpeg-24f-beat-20261031.mp4. THEIR side: no Harmony/Blender-vs-Harmony export
   pair. Verdict: NOT RUN (0/1). Note: Blender render here is 1100x1100 vs
   source 1100x1500, so even our side needs a full-height re-render before any
   export comparison.
6. Colour — OUR side: showcase/lighting-level2-v2/level-2-v2-colored-warm-rim-20261031.png
   (606,536 bytes, on main size-matched, APPROVED 15:11 CDT "perfect exactly"),
   rim warm amber (255,180,80) + bleed orange (255,120,0), rim follows key
   within ±20° (RIM-COLOR-RULE.md). THEIR side: NO Harmony/After Effects grade
   file. Provisional method assessment (NOT counted): EQUAL on method — our rim
   hue family matches the grade, which is the documented industry rule; no
   pixel-for-pixel grade comparison exists yet.
7. Audio sync — OUR side: showcase/audio-cue-sheet-v2-20261031.jpg + CSV/JSON,
   -14 LUFS target, demo 6.0s (synthesized tones only, DEMO ONLY; loudness
   measured 0/5 cues). THEIR side: no tool cue sheet at 24fps.
   Verdict: NOT RUN (0/1).

## What is still owed for a counted comparison

- A legitimate Harmony trial install (or Animate/After Effects) with a logged
  trial day, and one built file per test (pose, xsheet, deformation, swap,
  export, grade, cue sheet) — all 7 their-side files. Until then the honest
  count stays 0/7, with 2 provisional method assessments (tests 4 and 6) that
  are explicitly NOT counted.
- Full-height Blender re-render (1100x1500) before test 5 can be compared.
- Measured loudness (0/5 cues measured) before test 7 can be compared.
