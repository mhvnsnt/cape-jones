# FULL TV PRODUCTION — accounting to 100%, 2026-10-31
Mars, 2026-10-31 13:17 CDT: stop counting only the small 100% pieces.
This file is the whole goal, every piece, with its percentage, so no small 100% makes it sound done.
Overall = average of the 21 items below. Counted items show their count. Estimates are labelled ESTIMATE.

## The 21 items, finished and unfinished
1. Rig hierarchy + joint locks v6 — 100% (v6, default lock, verified on main)
2. Clean cuts — 100% (slice_clean.py, wired)
3. Pose library v6 — 100% (6 poses + clip frames, viewed)
4. Timeline / clips — 85% (6 clips built: jump, punch, dance, flex, flying, walk; side-view walk and per-shot timelines left)
5. Symbol library + JSFL — 50% (static v8 JSFL + timeline JSFL template; NOT run in Animate here)
6. Shot spec + proof — 60% (templates + SHA manifest; per-shot specs 0, QC pending until Mars looks)
7. Technique library index — 100% (stage order + shot types, methods pulled, no characters)
8. Asset manifest — 100% snapshot (251 branch files, 184 unique images, as of 2026-10-31; drifts as new assets land)
9. Model sheets — 40% counted (2/5 angles: front full, profile head only; 3/4, side body, 3/4 back, back left)
10. Viseme / mouth chart — 20% (charts staged on branch; sliced viseme pieces 0/14, eye strips 0/8)
11. Background layout line art — 20% (5 line-art sheets staged; line-art versions of the 37 painted backgrounds 0/37)
12. Prop scale sheets — 11% counted (2/19 props with scale sheets)
13. Storyboards — 30% ESTIMATE (5 sheets staged; episode board total not set, so this is an estimate, not a count)
14. Exposure sheets — 67% counted (10/15: 10 staged, 5 variants left — walk, dance, power pose, landing, wave)
15. Layout passes — 0% (0/5 scenes: room, flying, rooftop, alley, desk)
16. Clean-up pipeline — 20% (cut tool only; ink-and-paint pipeline not built)
17. Effects design — 20% (cape wind + FX on flying sheet only; impacts, energy, lighting overlays as a set left)
18. Compositing templates — 0% (templates built in this package, see below — before this package it was 0%)
19. Grade LUTs — 0% (spec built in this package, final LUT files not graded/approved)
20. Audio cues — 10% (1 cue sheet claimed elsewhere, not in sheets inventory; cue template built in this package)
21. Delivery specs — 20% (fps 24 + canvas 1100x1500 defaults only; full delivery spec built in this package, not approved)

## Overall, before this package
Sum = 953 / 21 = 45% to full TV production. NOT 100%. That is the number to use.
Small 100% pieces (items 1, 2, 3, 7, 8) are 5/21 items — they do not make the goal done.

## What this package adds (templates, not final art)
- layout-passes-templates.json — 5 scenes, camera/staging/background placement fields
- cleanup-pipeline.md — clean-up / ink-and-paint steps for FLA pieces
- effects-design.md — cape, impact, energy, lighting overlay templates
- compositing-templates.md — compositing layers + order
- lut-spec.md — LUT spec (neutral/warm/cool intent, not final graded LUT files)
- audio-cue-template.json — cue sheet fields
- delivery-spec.md — resolution, frame rate, safe areas, delivery format fields
These move items 15, 16, 17, 18, 19, 20, 21 from template-absent to template-present.
Template-present is NOT production-complete. After this package, re-count those items at template level,
and the remaining blockers to true 100% are, plainly:
  - new art packs (model angles, viseme pieces, layout passes, effects) — generation, one pack at a time, shown before next
  - JSFL run in Animate — needs Animate, not available in this VM
  - QC — Mars looking at clip/shot frames
  - branch-to-main merge for the 251 branch files — that branch is not main yet, and merging it is a separate decision, not done by this package
