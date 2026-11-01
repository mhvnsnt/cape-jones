# Correction log — append-only. NEVER rewrite, NEVER delete an entry.
# Rule: a Mars correction is closed ONLY when a regression fixture for it
# exists and the gate FAILS the old version and PASSES the fixed version.
# If a future build repeats a logged mistake, the gate fails it — Mars
# must not be the detector. That is the whole point of this log.
#
# Format: date | clip/move | Mars correction (verbatim gist) | rule_id | regression fixture | status
2026-10-31 16:09 CDT | improved dance f015/f042 | knees inward, feet outward reads broken, like hit in knees with baseball bat | R04 | fixtures/old_wrong_foot.json | CLOSED (gate test 20261101)
2026-10-31 16:58 CDT | dance-kneefeet v1 | block range 15-55 flipped outward-knee frame f028 inward; rule must be per-frame, bidirectional | R04 | fixtures/old_wrong_foot.json, fixtures/fixed_all.json | CLOSED (gate test 20261101)
2026-10-31 17:58 CDT | dance, arms across chest | arms eaten by torso/pecs; snap whole arm above torso momentarily, per arm per frame | R01 | fixtures/old_eaten_arm.json | CLOSED (gate test 20261101)
2026-10-31 ~18:27 CDT | pose dialects JoJo 03, Ginyu 01 | arm over face must go over head; bicep over cowl, upper only | R02,R03 | fixtures/old_eaten_arm.json | CLOSED (gate test 20261101)
2026-10-31 ~18:52 CDT, reaffirmed 2026-11-01 10:36 CST | side rig | hands go WITH wrist, never cut wrist, fused assembly stays whole, hand not placed separately from forearm | R05 | (wrist fixture in gate test: wrist_distance_px, wrist_cut) | CLOSED (gate test 20261101)
2026-11-01 11:25 CST | movement clips, crossed arms down across chest | arms crossing down across chest in front must go to TOP layer for that moment, not eaten by chest; automatic sense, wired 100% | R01 | fixtures/old_eaten_arm.json | CLOSED (gate test 20261101)
2026-11-01 11:26 CST | flex (Johnny flex clip) | flex motions 70-90 deg wider from middle above head, more obtuse; current both arms too acute, looks like super-extreme overexerted flex | R06 | fixtures/old_acute_flex.json | CLOSED (gate test 20261101)
2026-11-01 11:30 CST | anatomy-combination clip | arms across chest eaten again; wrong motions; elbows backwards / arms opposite direction; leg1 do NOT rotate foot past threshold (fine as-is); leg2 foot MUST turn when knee goes inward past knee threshold | R01,R04b,R07 | fixtures/old_wrong_foot.json, fixtures/old_elbow_reversed.json | CLOSED (gate test 20261101)
2026-11-01 11:31 CST | side-to-side shuffle clip | perfect except side-to-side must pick one leg up then step, alternating steps created yesterday; stop repeating same mistakes | R08 | fixtures/old_shuffle_no_lift.json | CLOSED (gate test 20261101)
2026-11-01 11:31 CST | all clips, system | stop making Mars repeat himself; learn as we go; pull 10 industry-standard learning systems and wire them for real | ALL | this gate itself, run_tests.py | CLOSED (gate test 20261101)
