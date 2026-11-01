# Comparison tests — run sheet, second pass, 2026-11-01 (no repo push, no original touched)

Standing rule (COMPARISON-TESTS.md): a test counts ONLY when BOTH sides have a
viewed file. A one-sided test is 0/1, not a win. "Better" must name what is
better. Trial/subscription status must be logged per test — never test a tool
we do not legitimately have access to at that time.

## Counted result this job: 0/7 — UNCHANGED, and why that is not a stall

The parent task said "earlier 1/7 = 14%, 6/7 remaining". That 1/7 still could
NOT be located in COMPARISON-TESTS.md (0/7), clean-100 COMPARISON-RESULTS
(0/7 counted, 2 provisional method assessments explicitly NOT counted), or
TOOL-PASS-LOG / TRACKER / PROGRESS files. This job does NOT adopt 1/7.
If the parent's 1/7 means one provisional method assessment (T4 or T6),
that is a provisional 1/7, NOT a counted comparison — the two must not be
mixed. Counted comparisons stay 0/7 until a theirs-side file exists.

What DID advance this job (our side only, stated as our side only):
- T5 our-side blocker CLOSED: full-height Blender render now exists (below).
- T7 our-side demo loudness CLOSED: 5/5 demo cues measured (below).
- T4 our-side re-run: ALL PASS again (below).
- T2/T1/T3/T6 our-side fixtures re-verified by file/dimension/script checks.
None of these is a counted win. All 7 counted verdicts remain NOT RUN.

## Blocker common to all 7 counted tests (theirs side) — UNCHANGED

- Harmony is NOT installed on this VM; no installer file is in hand on the
  VM (toon-boom-install-attempt-20261031.md: no binary, no activation,
  trial NOT confirmed; Harmony 27 workstation is Windows/macOS only).
  Memory note 2026-11-01 01:10 CDT says a Toon Boom installer appeared in
  the user's BROWSER downloads (second copy downloading) — that is on the
  user's machine/browser, NOT on this VM, and this subagent cannot run a
  browser task to fetch or confirm it. No theirs-side file was invented.
- Animate / After Effects / Maya: likewise no binary on this VM, no trial
  logged. Trial status per test: UNKNOWN (not "day X/14") — never stated
  as a confirmed trial day.
- Route (parent/root delegation, not a generic subagent): live-browser task
  signed in as fmmg.mars@gmail.com ONLY, to confirm trial edition/start/end
  on the Toon Boom account and to obtain the installer; then a Windows/mac
  install or a Wine experiment with that real installer. No purchase, card
  entry, or cancellation was done or attempted here.

## Per-test verdicts (PASS/FAIL stated plainly)

1. Rig pose — COUNTED: NOT RUN (0/1) — FAIL to count, no Harmony pose file.
   OUR SIDE: READY, re-verified by file check this job:
   rig-apose-v7c-clean-transparent.png, 1100x1500 RGBA, 478,221 bytes.
   Fighting pose approval (15:00 CDT) is a prior tracker claim, cited, not
   re-eye-verified in this text-only job. Build spec when unblocked: same
   A-pose in Harmony, same pivots. Compare: joint pivots, limb attachment,
   silhouette. Verdict: NOT RUN.
2. Timeline / xsheet — COUNTED: NOT RUN (0/1) — FAIL to count.
   OUR SIDE: READY WITH CAVEAT, re-verified this job: xsheet JSON 24 frames
   @ 24fps, beats 1,7,13,19; ffmpeg-24f-beat-20261031.mp4 ffprobe 24 frames
   @ 24fps, 550x750. Caveat carried forward (in the JSON itself): Tahoma GUI
   scene open + render was NOT run. THEIR side: no Harmony xsheet. Verdict:
   NOT RUN.
3. Deformation — COUNTED: NOT RUN (0/1) — FAIL to count.
   OUR SIDE: READY (pieces present): cut-limbs-v7c/ 12 limb/cap pieces +
   OutFixed pieces in cut-limbs-v7c-gauntlet-out-fixed/. Pivot claim
   "ball-centre pivots 4/4 (2 elbows, 2 knees)" is a prior tracker claim,
   cited here, NOT re-measured this job (no pivot JSON was located in the
   cut-limbs folder). THEIR side: no Harmony deformation file. Verdict:
   NOT RUN.
4. Drawing substitution — COUNTED: NOT RUN (0/1) — FAIL to count.
   OUR SIDE: PASS, re-run this job: check_gauntlet_flip.py = ALL PASS
   (OutFixed exists both arms, per-row x-range preserved both arms,
   approved fixed pose exists, diff confined to gauntlet zone bbox
   x323-775 y433-565, diff 17,082 px). Provisional method assessment from
   clean-100 (NOT counted): EQUAL on method — swap preserves per-row
   x-ranges and puts panels outward/camera, as the documented method
   requires. What turns it counted: the same flip built in Harmony trial,
   file viewed side by side. Verdict: NOT RUN (our-side PASS only).
5. Export — COUNTED: NOT RUN (0/1) — FAIL to count (no Harmony export).
   OUR SIDE: PASS (new this job — prior our-side gap now closed):
   NEW full-height Blender render in this folder:
   blender-compositor-apose-fullheight-20261101.png, 1100x1500 RGBA,
   979,534 bytes, rendered with Blender 4.5.3 (tools-industry binary, not
   on PATH) from rig-apose-v7c-clean-transparent.png via the clean-100
   compositor script with ONLY resolution_y 1100->1500 and the output path
   changed (script: blender_fullheight_1500_v45.py; the 5.2.3 variant
   blender_fullheight_1500.py is kept, but 5.2.3 fails headless here on
   missing system libEGL.so.1 — that failure is logged, not hidden).
   Geometry check: opaque px render 373,846 = source 373,846, alpha
   differing px 0/1,650,000 — geometry pixel-exact, NOT a crop or a pad.
   Colour check: mean RGB source (135.1,133.3,137.8) vs render
   (108.5,107.2,110.6) — WORKBENCH render darkens uniformly (~0.80x),
   which is a render transform to compare, not a pixel copy. The old
   1100x1100 render (887,145 bytes) is NOT overwritten and is superseded
   for comparison purposes by this full-height file. Correction to the
   prior run sheet: Blender is NOT absent — 4.5.3/5.2.3 exist in
   ~/workspace/tools-industry/; the prior "owed re-render" is now done.
   Compare when unblocked: colour (LUT/rim/bleed), resolution, file size.
   Verdict: NOT RUN (our-side PASS only).
6. Colour — COUNTED: NOT RUN (0/1) — FAIL to count.
   OUR SIDE: READY, re-verified by file check this job:
   showcase/lighting-level2-v2/level-2-v2-colored-warm-rim-20261031.png,
   1100x1500 RGBA, 606,536 bytes; rim warm amber (255,180,80) + bleed
   orange (255,120,0) per RIM-COLOR-RULE.md. Provisional method assessment
   from clean-100 (NOT counted): EQUAL on method — rim hue family matches
   the grade, per the documented industry rule; no pixel comparison exists
   yet. THEIR side: no Harmony/After Effects grade file. Verdict: NOT RUN.
7. Audio sync — COUNTED: NOT RUN (0/1) — FAIL to count.
   OUR SIDE: PARTIAL-PASS for demo, re-verified + newly measured this job.
   Located this job (prior run sheet had NOT re-located them):
   showcase/audio/audio-cue-sheet-v2.csv + .json, 5 cues, all marked
   DEMO ONLY (synthesized tone/noise, not recorded audio). Cue-sheet JPG
   also present (2000x1100, 193,609 bytes). NEW measurement (ffmpeg
   loudnorm, per-cue slices of cape-jones-audio-cues-demo.wav, 5.96s):
   C1 punch-impact -10.31 LUFS (target -14, +3.69 hot), C2 fighting-stance
   whoosh -14.40 (-0.40), C3 walk steps -15.92 (-1.92), C4 jump rise
   -12.84 (+1.16), C5 dance beat -14.65 (-0.65); whole-file input -14.72
   LUFS, true peak -1.24 dBTP. So: demo cues measured 5/5 (was 0/5);
   PRODUCTION cues measured 0/5 (no production audio exists — the demo
   numbers must not be presented as production loudness). THEIR side: no
   tool cue sheet at 24fps. Compare when unblocked: frame accuracy.
   Verdict: NOT RUN (our-side demo measurement PASS only).

## Counts summary (do not mix them)

- Counted comparisons (both sides): 0/7 = 0%.
- Our-side PASS this job: T4, T5 (new full-height render) = 2/7 fully
  passing on our side; T7 demo measurement 5/5 cues (production 0/5).
- Our-side READY (fixture verified, no new run this job): T1, T2 (with
  Tahoma GUI caveat), T3 (pivot claim cited), T6 = 4/7.
- Provisional method assessments (NOT counted): T4 EQUAL, T6 EQUAL = 2.
- Theirs-side files: 0/7. Trial days logged: 0/7 (UNKNOWN, not day X/14).

## Still owed for a counted comparison (unchanged except T5/T7 our-side gaps)

- A legitimate Harmony trial install (or Animate/After Effects) with a
  logged trial day, and one built file per test (pose, xsheet, deformation,
  swap, export, grade, cue sheet) — all 7 theirs-side files.
- T2: Tahoma GUI scene open + render (our-side caveat, still open).
- T3: pivot re-measurement (4/4 claim needs a re-located pivot record).
- T7: production audio + per-cue measured loudness (demo is measured now).
- Until then the honest counted number stays 0/7, with 2 provisional
  method assessments explicitly NOT counted.

Approval 0/1 for this comparison run sheet separately (it reports status,
readiness, and two new our-side completions; it does not claim any test won).
