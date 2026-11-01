# DIALOGUE-FILL TEMPLATE — per-shot slots for all 30 shots, 2026-10-31

How to use: one row per shot. A row is OPENED at picture lock (Phase 3) with
shot + slot timecode + speaker, and the LINE left BLANK for Mars (Phase 4).
A blank line is not an incomplete shot — shots marked SILENT-OK are finished
visual beats with no line. Do NOT invent a line to fill a blank row.
The machine-readable version is `DIALOGUE-FILL-TEMPLATE-20261031.csv`
(same rows, same blank lines).

Fields per row: Shot | Pose/clip (from shot spec) | Dialogue class |
Slot TC in/out (fill at picture lock) | Speaker (fill at lock/spotting) |
Intent (fill at spotting) | LINE (Mars only, Phase 4) | Take selected |
Viseme pass done? | QC result (Phase 6 queue A).

| Shot | Pose / clip | Class | Slot TC | Speaker | Intent | LINE (Mars only) | Take | Viseme? | QC |
|---|---|---|---|---|---|---|---|---|---|
| CJ-01 | Punch windup, hold 6f | SILENT-OK | | | | | | | |
| CJ-02 | Punch extend-snap, hold 2f | SILENT-OK | | | | | | | |
| CJ-03 | Punch impact-hold, hold 12f (LOCKED impact frame) | SILENT-OK | | | | | | | |
| CJ-04 | Punch recover, hold 6f | SILENT-OK | | | | | | | |
| CJ-05 | Punch across-down placement | SILENT-OK (+ rim ruling, Phase 6 queue B) | | | | | | | |
| CJ-06 | Walk contact LEG1, hold 12f, loop | SILENT-OK (+ rim ruling, Phase 6 queue B) | | | | | | | |
| CJ-07 | Walk passing, hold 12f, loop | SILENT-OK | | | | | | | |
| CJ-08 | Walk cycle, alley night | SILENT-OK | | | | | | | |
| CJ-09 | Dance-a, hold 12f, loop | SILENT-OK | | | | | | | |
| CJ-10 | Dance-b, hold 12f, loop | SILENT-OK | | | | | | | |
| CJ-11 | Dance repeat / combined finale | SILENT-OK (tempo slot: Phase 5, see QC doc §C) | | | | | | | |
| CJ-12 | Flying hovering, hold 12f | SILENT-OK | | | | | | | |
| CJ-13 | Flying soaring, arms out, hold 12f | SILENT-OK | | | | | | | |
| CJ-14 | Flying diving, arms up, hold 12f | SILENT-OK | | | | | | | |
| CJ-15 | Flying forward-flight, foreshortened | SILENT-OK | | | | | | | |
| CJ-16 | Flex anticipation / before-tighten | SILENT-OK | | | | | | | |
| CJ-17 | Arms-up reference pose | SILENT-OK | | | | | | | |
| CJ-18 | True flex, double-bicep | SILENT-OK | | | | | | | |
| CJ-19 | Fighting pose, forward bicep curl (dual-light) | SILENT-OK | | | | | | | |
| CJ-20 | Fighting stance, arms up high | SILENT-OK | | | | | | | |
| CJ-21 | Jump crouch + takeoff | SILENT-OK | | | | | | | |
| CJ-22 | Jump tuck + landing, cape wind | SILENT-OK | | | | | | | |
| CJ-23 | Lounge / seated pose in room | SILENT-OK | | | | | | | |
| CJ-24 | Desk shot, seated at desk | SILENT-OK | | | | | | | |
| CJ-25 | Room standing, handheld gag device | SILENT-OK | | | | | | | |
| CJ-26 | Dialogue, neutral / unsure beat | DIALOGUE-PRIMARY (+ rim ruling, Phase 6 queue B) | | | | | | | |
| CJ-27 | Dialogue, shout / angry beat | DIALOGUE-PRIMARY | | | | | | | |
| CJ-28 | Rooftop sunset | SILENT-OK | | | | | | | |
| CJ-29 | Rooftop night city | SILENT-OK | | | | | | | |
| CJ-30 | Alley neon dual-light | SILENT-OK | | | | | | | |

Counts: 30/30 rows templated = 100%. Dialogue-primary: 2/30 (CJ-26, CJ-27).
Silent-OK optional slots: 28/30. Lines filled here: 0/30 = 0% — by design;
lines are Mars's Phase 4 step, not this workstream's.

Scratch rule: any placeholder line used during Phases 2–3 must be entered
with the word SCRATCH in the LINE column and replaced at Phase 4. A final
mix containing a SCRATCH line fails Phase 6 queue A.
