# COMPARISON TESTS — ours vs theirs, as good or better (Mars, 2026-10-31 15:39 CDT, standing)

Method: while we build our own version, we keep USING theirs (legitimate trial/subscription), keep LEARNING their stuff as we use it, keep REVERSE-ENGINEERING it, and keep WIRING UP our own version as we use theirs. Then we run COMPARISON TESTS to see if ours is just as good as theirs, or better. Not cracking, not copying code — methods only, tested side by side.

## UNIVERSAL SCOPE (Mars, 2026-10-31 15:40 CDT, standing)
This loop applies to ANY tool we reverse engineer, and ANYTHING ELSE we reverse engineer — not just Harmony. Every tool gets the same treatment: use it legitimately, learn as we use it, reverse-engineer its methods, wire our own version as we use it, and comparison-test ours vs theirs. Tools in scope so far: Toon Boom Harmony, Adobe Animate, Adobe After Effects, Autodesk Maya, OpenToonz/Tahoma2D methods, Blender methods, Wick Editor/Brinimate methods, and any future tool added to FREE-FIRST-WIRING.md. A tool is not "done" until its comparison tests are run — listing it is not wiring it.

## Test matrix (each test: theirs result, ours result, verdict: worse / equal / better, with file names)
1. Rig pose — same pose built in Harmony (trial) and in v7c rig. Compare: joint pivots, limb attachment, silhouette.
2. Timeline / xsheet — same 24-frame beat (Darwin beat ~14f @25fps, on twos) in Harmony and in OpenToonz/Tahoma2D/JSFL timeline. Compare: timing accuracy, hold readability.
3. Deformation — same limb bend in Harmony deformation vs our v7c pivot + cap method. Compare: seam, volume, joint ball.
4. Drawing substitution — same hand/gauntlet flip (pose-driven swap) in Harmony vs our FlexOut/OutFixed pieces. Compare: per-row preservation, panel facing.
5. Export — same shot exported from Harmony and from Blender compositor + FFmpeg. Compare: colour (LUT/rim/bleed), resolution, file size.
6. Colour — same grade in Harmony/After Effects method vs our Level 2 v2 + LUTs. Compare: rim hue family, bleed falloff, shadow.
7. Audio sync — same cue sheet at 24fps in their tool vs our cue sheet (-14 LUFS). Compare: frame accuracy.

## Rules
- A test is only counted when BOTH sides have a viewed file. A one-sided test is 0/1, not a win.
- "Better" must name what is better (faster, cleaner seam, truer colour, fewer steps) — not just "ours is better".
- Trial/subscription status must be logged per test (trial day X/14, or subscribed) — never test a tool we do not legitimately have access to at that time.
- Results go in TOOL-PASS-LOG.md per pass, and here per test.

## Status 2026-10-31 15:39 CDT
Tests run: 0/7. Harmony trial started, method study pending — comparison tests begin when the trial lands. Our side is ready for tests 1, 3, 4, 6 (v7c rig, FlexOut, Level 2 v2, LUTs 70/70).
