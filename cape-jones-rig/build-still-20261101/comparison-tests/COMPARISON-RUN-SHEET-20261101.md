# Comparison tests — run sheet + re-verification, 2026-11-01 (no repo push)

Standing rule (COMPARISON-TESTS.md): a test counts ONLY when BOTH sides have a
viewed file. A one-sided test is 0/1, not a win. "Better" must name what is
better. Trial/subscription status must be logged per test — never test a tool
we do not legitimately have access to at that time.

## Counted result this job: 0/7

Discrepancy flagged plainly: the parent task said "earlier 1/7 = 14% fully done".
That 1/7 could NOT be located in COMPARISON-TESTS.md (status 0/7, 2026-10-31
15:39 CDT), clean-100-20261031/stack-tests/COMPARISON-RESULTS-20261031.md
("Full counted result: 0/7", 2 provisional method assessments explicitly NOT
counted), TOOL-PASS-LOG.md, TRACKER-20261031.md, or PROGRESS-STATUS-20261031.md.
This job therefore reports the verified counted number, 0/7, and does NOT adopt
1/7. If the parent has a source for the 1/7, it is not in any of those files.

## Blocker common to tests 1-6 (theirs side)

- Harmony is NOT installed on this VM and no installer file is in hand
  (toon-boom-install-attempt-20261031.md: no binary, no activation, trial
  NOT confirmed; Harmony 27 workstation is Windows/macOS only, no Linux build).
- The 2026-11-01 00:30 CDT browser task (Mars: YES, use the payment method
  already on the Toon Boom account, start the trial) is the route to the
  installer + activation confirmation. As a subagent this job cannot run a
  browser task; the theirs-side builds below are ready to run the moment
  that task returns an installer + a confirmed activation.
- Animate / After Effects / Maya: likewise no binary on this VM, no trial
  logged. No theirs-side file was invented for any test.

## Per-test status (our side re-verified this job unless noted)

1. Rig pose — OUR side ready: rig-apose-v7c-clean-transparent.png (1100x1500,
   478,221 bytes, on disk) + v7c fighting pose (approved 15:00 CDT per tracker).
   THEIR side: no Harmony pose file. Build spec when unblocked: same A-pose
   in Harmony, same pivots. Compare: joint pivots, limb attachment, silhouette.
   Verdict: NOT RUN (0/1).
2. Timeline / xsheet — OUR side re-verified: clean-100 stack-tests/
   tahoma-cape-jones-24f/xsheet-beat-grid-20261031.json (24 frames @ 24fps,
   beats 1,7,13,19) + ffmpeg-24f-beat-20261031.mp4 (ffprobe this job: 24
   frames @ 24fps, 550x750). Caveat carried forward: Tahoma GUI scene open +
   render was NOT run in that batch (stated in the xsheet JSON itself).
   THEIR side: no Harmony xsheet. Build spec: same 24-frame beat, on twos.
   Compare: timing accuracy, hold readability. Verdict: NOT RUN (0/1).
3. Deformation — OUR side ready: cut-limbs-v7c/ (upper/lower/cap pieces) +
   v7c ball-centre pivots 4/4 (2 elbows, 2 knees, per tracker) + OutFixed caps.
   THEIR side: no Harmony deformation file. Build spec: same limb bend.
   Compare: seam, volume, joint ball. Verdict: NOT RUN (0/1).
4. Drawing substitution — OUR side RE-RUN this job: check_gauntlet_flip.py =
   ALL PASS (OutFixed exists both arms, per-row x-range preserved both arms,
   approved fixed pose exists, diff confined to gauntlet zone bbox
   x323-775 y433-565, diff 17,082 px) + pil-outfixed-vs-original-20261031.png
   (on disk). THEIR side: no Harmony swap file. Provisional method assessment
   from clean-100 (NOT counted): EQUAL on method — our swap preserves per-row
   x-ranges and puts panels outward/camera, as the documented method requires.
   What turns it counted: the same flip built in Harmony trial, file viewed
   side by side. Verdict: NOT RUN (0/1).
5. Export — OUR side re-verified: blender-compositor-apose-20261031.png
   (1100x1100 — NOT full height, see below) + ffmpeg-lut-neutral-apose-
   20261031.png (1100x1500) + ffmpeg-24f-beat-20261031.mp4. THEIR side: no
   Harmony export. Owed before this test can be compared even on our side:
   full-height Blender re-render (1100x1500, not 1100x1100). Compare: colour
   (LUT/rim/bleed), resolution, file size. Verdict: NOT RUN (0/1).
6. Colour — OUR side re-verified: showcase/lighting-level2-v2/
   level-2-v2-colored-warm-rim-20261031.png (1100x1500, 606,536 bytes, on
   disk; rim warm amber (255,180,80) + bleed orange (255,120,0) per
   RIM-COLOR-RULE.md; approved 15:11 CDT "perfect exactly" per clean-100).
   THEIR side: no Harmony/After Effects grade file. Provisional method
   assessment from clean-100 (NOT counted): EQUAL on method — rim hue family
   matches the grade, which is the documented industry rule; no pixel
   comparison exists yet. Verdict: NOT RUN (0/1).
7. Audio sync — OUR side partly re-verified: showcase/audio-cue-sheet-v2-
   20261031.jpg (193,609 bytes, on disk) + audio-cue-template.json (target
   -14 LUFS, "template only, no per-shot cue sheets built"). The tracker
   claims cue-sheet v2 + CSV/JSON 3/3; the CSV/JSON were NOT re-located in
   this job's search, so that 3/3 is cited as a prior claim, not re-verified.
   Owed: measured loudness per cue (clean-100: 0/5 cues measured). THEIR side:
   no tool cue sheet at 24fps. Build spec: same cue sheet at 24fps in their
   tool. Compare: frame accuracy. Verdict: NOT RUN (0/1).

## What is still owed for a counted comparison (unchanged, stated plainly)

- A legitimate Harmony trial install (or Animate/After Effects) with a logged
  trial day, and one built file per test (pose, xsheet, deformation, swap,
  export, grade, cue sheet) — all 7 theirs-side files.
- Full-height Blender re-render (1100x1500) before test 5 can be compared.
- Measured loudness per cue before test 7 can be compared.
- Until then the honest count stays 0/7, with 2 provisional method
  assessments (tests 4 and 6) explicitly NOT counted.

Approval 0/1 for the comparison-test run sheet separately (it reports status
and readiness; it does not claim any test won).
