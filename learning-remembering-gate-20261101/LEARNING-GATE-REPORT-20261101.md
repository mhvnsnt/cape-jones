# Learning / Remembering Gate — 2026-11-01
Mars, 2026-11-01 11:31 CST: "stop making me repeat my stuff, you should be
learning as we go and not repeating the same mistakes a hundred times.
Pull in 10 top industry standard things and wire up to help you learn
and remember like for real."

## What was built (wired, not listed)
Folder: `learning-remembering-gate-20261101/`, originals untouched, no
clip/video overwritten, no repo push claimed in this task.

- [pre_delivery_gate.py](sandbox://workspace/cape-jones-rig/learning-remembering-gate-20261101/pre_delivery_gate.py) — mandatory gate, exit 0 PASS / 1 FAIL / 2 bad input. No --force flag exists on purpose.
- [check_before_ship.sh](sandbox://workspace/cape-jones-rig/learning-remembering-gate-20261101/check_before_ship.sh) — wrapper: `check_before_ship.sh <pose-table.json> <clip-id> [video.mp4]`. Run it BEFORE any clip/video is shown or sent. Exit 1 blocks delivery.
- [rules.json](sandbox://workspace/cape-jones-rig/learning-remembering-gate-20261101/rules.json) — 13 rules, single source of truth, version 20261101. Builders import these numbers; they are never copy-pasted per clip again.
- [CORRECTION-LOG-20261101.md](sandbox://workspace/cape-jones-rig/learning-remembering-gate-20261101/CORRECTION-LOG-20261101.md) — append-only correction log, 10 entries. A correction closes only when its regression fixture FAILs old and PASSes fixed.
- `fixtures/` — 8 regression pose tables. `test-output/` — per-fixture gate reports.

## The 10 industry-standard systems, wired
1. Aviation/NASA pre-flight checklist — all items checked, none skippable, one FAIL blocks delivery.
2. Software CI quality gate (GitHub Actions/Jenkins) — exit 1 blocks the pipeline; check_before_ship.sh is the pipeline step.
3. Toyota lean poka-yoke / Andon — a violation stops the line at that frame, with frame number and rule, not at the end.
4. Animation X-sheet / exposure sheet (Disney, Toon Boom Harmony) — a per-frame pose table is REQUIRED input. No table = exit 2, FAIL by missing table.
5. Broadcast QC, WCAG 2.3.1 / Harding-PEAT proxy — whole-frame flash check in video mode (see limit below).
6. Cut-out rig QA (Harmony Z-depth, Godot Behind-Parent, Spine draw order) — layer order is a per-frame keyable property, checked per arm per frame.
7. WHO surgical checklist / independent double-check — angle-mode sensor is authoritative; flat-video proxy is candidate only, never a verdict by itself.
8. Regression testing (pytest-style snapshots) — old bad fixtures must FAIL forever; a future build matching one fails even if nobody remembers why.
9. Aerospace/NASA CAPA lessons-learned — append-only correction log, closed only by a passing/failing fixture pair.
10. ADR / runbook knowledge base — versioned rules.json, one source, imported by the gate and by future builders.

## Rules enforced (all 13, every build)
R01 arm-front-snap: forearm_vs_torso >1000px at 1100x1500 => whole arm above torso, below head, per arm per frame, momentary only.
R02 face-snap: forearm_vs_head >5000px => arm above head.
R03 cowl: upper-only, candidate + eye-check only, whole-chain cowl BANNED.
R04 knee-feet per frame, bidirectional: knee direction == foot direction on THAT frame; FootIn only if leg_upper L>0 AND R<0; no block ranges.
R04b leg1/leg2 exception, Mars 2026-11-01 11:30 CST: LEG1 (LEFT) — do NOT rotate its foot past the threshold created on this clip, it is fine as-is. LEG2 (RIGHT) — when past the knee threshold and the knee goes inward, its foot MUST turn inward. Exception is leg1-only and must be flagged leg1_exception=true; it never excuses leg2.
R05 wrist: wrist distance <=30px AND wrist nearer than fingertip; wrist_cut banned; hands go WITH the wrist; fused assemblies stay whole.
R06 flex obtuse, Mars 2026-11-01 11:26 CST: flex_spread 100-160 deg. Below 100 = too acute, super-extreme overexerted flex, needs 70-90 deg wider from the middle above the head.
R07 elbow direction: elbows back/out, never forward/in; arm motion sign must match intended sign, never reversed.
R08 shuffle alternating steps: side-to-side shuffle must pick ONE leg up then step, alternating L,R,L,R, never same leg twice, never a slide with no lifted leg.
R09 grounded: feet planted unless labelled airborne (5px tolerance).
R10 cape two parts: collar + back separate; collar_dy == torso_dy; seated bottom pinned (bottom_dy == 0).
R11 no crop / no hand-draw: cropped, square_crop, or hand_drawn true FAILS.
R12 flicker: WCAG 2.3.1 whole-frame proxy, max 3 opposing luminance pairs >=25.5 in any 1s, no red flash.

## Test results — verified by running the gate
OLD (must FAIL, and did):
- old_eaten_arm: FAIL, 2 failures — L 4500px and R 3200px forearm_vs_torso, snap=False, arms EATEN by chest.
- old_acute_flex: FAIL, 1 failure — flex_spread 35 deg <100, too acute.
- old_wrong_foot: FAIL, 2 failures — leg2 knee=in, foot=out, past threshold, foot did not turn.
- old_elbow_reversed: FAIL, 4 failures — both elbows forward/in, both motion signs reversed.
- old_shuffle_no_lift: FAIL, 3 failures — step with no leg lifted (x2), same leg twice in a row.
- old_wrist_cut: FAIL, 3 failures — wrist cut, 80px distance, wrist not nearer than fingertip.
- Missing pose table: exit 2, FAIL by missing table.

FIXED (must PASS, and did):
- fixed_all: PASS, 0 failures — crossed arms snapped (chest layer), flex 120 deg (85 wider than the 35 deg acute fixture), leg2 knee=in foot=in past threshold, shuffle L then R each with its leg lifted.
- fixed_leg1_exception: PASS, 0 failures, 1 warning — leg1 knee=in foot=out excused ONLY because leg1_exception=true is flagged; leg2 correct in/in. Without the flag, the same row FAILS (see old_wrong_foot logic for leg2; leg1 without flag also fails R04).

## Honest limit — read this before quoting a PASS
The 8 movement-library MP4s were run in VIDEO mode only: whole-frame flash 0 failures and audio present on all 8. That is NOT an anatomy PASS. A flat video cannot prove layer order, knee direction, or elbow direction after the fact (ARM-FRONT-SNAP-RULE pipeline step). Those clips can only PASS this gate when their builders supply a per-frame pose table from the rig angles. Do not present the video-mode run as "all 8 clips pass the gate" — it is flash+audio only, and the test-output files for those runs used the fixed_all pose table as a placeholder, so they prove the video check, not the clips' anatomy.
Similarly, the dance-test forearm-box flash metric was NOT reused here: it is tuned to the 1920x1080 dance-test layout and trips on other layouts. This gate uses whole-frame flash only for video mode.

## How a future build uses it
1. Builder writes a per-frame pose table (schema is in pre_delivery_gate.py docstring) from rig angles, BEFORE rendering.
2. Run `./check_before_ship.sh pose-table.json <clip-id> [video.mp4]`.
3. Exit 0: may show/send. Exit 1: fix the listed frames, re-run. Exit 2: table missing/bad — fix the table.
4. New Mars correction: append one line to CORRECTION-LOG, add one rule to rules.json if it is new, add one old fixture (must FAIL) and one fixed fixture (must PASS). The correction is not closed until both fixtures behave that way.

## Still owed
- Pose tables for the 8 movement-library clips and for dance Videos 1-5, from their builders' rig angles — only then can those clips get a real anatomy PASS.
- Landing this folder to the repo (PR-only, verify on main) — not claimed here.
- Mars approval of the gate itself: 0/1.
