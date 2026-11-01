# WRIST / HAND / FOREARM ATTACHMENT FIX — one by one (Mars, 2026-10-31 ~18:52 CDT)

Order, in Mars's words: open-palm serve needs industry-standard stuff to
attach the palm cleaner to the wrist, wired 100% so it is right the first
time — "you have the fingertips attached to the forearm where the wrist
should be attached to the forearm… you don't need to flip it or nothing,
you just need to move it and attach it where the wrist should be"; top
row #4 and bottom row #3 of the limits-broken contact are the same thing;
hand library + dance variants are the same thing, shown individually, fixed
one by one. No repo push in this task. Mars approval of every fix: 0/1.

## 1. Poses identified — by viewing, not by filename alone

Limits-broken contact = 2 rows x 5, in build order:
- Top row: 1 bur-03 mach kick, 2 cap-01 twist, 3 bur-01 twist,
  **4 = JEI-01 crusher serve open-palm**, 5 jei-03x point variant.
- Bottom row: 1 rec-02 blast, 2 bur-02 hurricane,
  **3 = JEI-01 crusher serve open-palm + ball effect**, 4 gul-02 time,
  5 cap-02 swap beam.
- So top-row #4 and bottom-row #3 are THE SAME hand attachment, twice:
  once plain, once with the energy ball. Fixing the base fixes both.
  (a) in the task = top-row #4 = bottom-row #3's base pose.

## 2. The defect, measured (not guessed)

All 7 canon hand pieces are native fingers-UP, wrist/cuff at the BOTTOM
(measured from alpha: bottom-14-row cuff centre vs topmost-row centre).
Old builders pasted the hand CENTRED on the fist position, unrotated:
- Serve old: Hand_3_Open centre (314,530), angle -20, scale 1.0.
  Forearm end (builder-recorded fist centre) (314,517).
  Wrist point (294,586): 70.6 px from forearm end.
  Fingertip point (335,473): 54.9 px from forearm end.
  -> Fingertips NEARER than wrist = fingertip-first. FAIL, exactly as Mars said.
- Dance old (all 18 swapped attachments): hand centre = fist centre,
  angle 0, scale 1.7. Wrist dangles 98.9 px (open), 104.7 px (point),
  101.0 px (relaxed) below the joint; the forearm end touches the hand's
  mid-palm/edge, not its wrist. -> Wrist nearer than tip, but 99-105 px
  away = straddling joint, wrist dangling. FAIL on distance (>30 px).
  Base-fist frames (built-in fist, no swap) have no defect: already PASS.

## 3. Industry-standard methods wired (gate + builder)

- Anatomy: wrist = carpus between radius/ulna and hand; the joint point,
  not the hand centre, is what meets the forearm end.
- Harmony / Animate: hand drawing parented at the wrist pivot; pivot is
  placed on the forearm end, drawing hangs off it.
- Blender Grease Pencil / Spine: bone end = wrist pivot, same rule.
- Traditional animation: wrist overlap — cuff overlaps the forearm end
  by ~one wrist width so the joint reads continuous.
- Gate (`check_wrist_attach.py`): PASS iff d_wrist <= 30 px AND
  d_wrist < d_tip. Measured on paste parameters (a flat PNG cannot
  separate hand alpha from arm alpha). Functions: `placed_points`,
  `check`, `centre_for_wrist` (centre that lands the wrist on a target),
  `angle_for_direction` (in-plane angle turning wrist->tip onto a direction).
- Fix rule, Mars's words honoured: MOVE the hand so its wrist lands on
  the forearm end. NO MIRROR, NO FLIP, ever in this task.
- One honest correction, stated plainly, not hidden: for the serve, a
  PURE move at the old -20 angle cannot fix a fingertip-first hand — the
  move-only control passes the number (wrist 0.0 px) but the hand body
  then sits up over the gauntlet/upper arm (viewed, in the contact).
  The serve fix therefore turns the hand IN-PLANE to 164.8 deg (rotation,
  not a mirror/flip) so the wrist end faces the forearm, then moves it.
  Dance fixes ARE pure moves (angle 0 kept, fingers-up gesture kept),
  exactly as Mars said. If Mars wants the serve literally move-only, the
  control file shows what that looks like — it is not presented as a fix.

## 4. Fixes, one by one — per-item table

Serve (forearm end (314,517), overlap 25 px into forearm):
| item | old d_wrist / d_tip | fix applied | new d_wrist / d_tip | gate |
|---|---|---|---|---|
| jei-01 serve open-palm (top-row #4) | 70.6 / 54.9 FAIL | turn in-plane -20 -> 164.8 deg, centre (307.6,549.6), wrist 25 px inside forearm end, NO mirror | 25.0 / 99.6 | PASS |
| jei-01 serve + ball (bottom-row #3) | same hand, same FAIL | same base fix; orb re-applied OVER the new palm centre (307,549), (255,230,110) — ball follows the palm, not the old screen position (314,420), which sat above the old fingertips | 25.0 / 99.6 (hand) | PASS |
| serve MOVE-ONLY CONTROL | — | angle kept -20, centre (331.6,461.6) so wrist lands exactly on forearm end | 0.0 / 124.6 numeric PASS | NOT a fix: hand overlaps gauntlet, viewed |

Dance variants (3 grooves x 3 swapped hands x 2 sides = 18 attachments,
9 frames; wrist target = forearm end - outward*20, angle 0, scale 1.7,
fingers-up gesture kept, built-in fist erased on the LOWERS LAYER ONLY):
| frame | old d_wrist (both sides) | new d_wrist (both sides) | gate |
|---|---|---|---|
| open groove-a/b/c | 98.9 | 20.0 | PASS 6/6 |
| point groove-a/b/c | 104.7 | 20.0 | PASS 6/6 |
| relaxed groove-a/b/c | 101.0 | 20.0 | PASS 6/6 |
| base-fist groove-a/b/c (no swap) | already continuous | unchanged | PASS 6/6 (already) |

Hand library (test arm = groove-a pose, both hands, scale 1.7, angle 0):
| hand | old d_wrist | fixed d_wrist | note |
|---|---|---|---|
| Hand_1_Fist | 71.2 | 20.0 | first before/after for this hand |
| Hand_2_FistBack | 89.9 | 20.0 | first before/after |
| Hand_3_Open | 98.9 | 20.0 | same defect as dance open |
| Hand_4_Point | 104.7 | 20.0 | same defect as dance point |
| Hand_5_Point2 | 104.5 | 20.0 | first before/after |
| Hand_6_Relaxed | 101.0 | 20.0 | same defect as dance relaxed |
| Hand_7_Grip | 90.7 | 20.0 | first before/after |

Counts: attachments fixed 20/20 = 100% (2 serve + 18 dance).
Files fixed 11/11 = 100% (2 serve + 9 dance frames).
Library demos 7/7 hands, old + fixed each = 14 singles.
Base-fist frames rebuilt unchanged 3/3 (no defect to fix).
Full audit: `wrist_gate_dance_audit.csv` (18 rows), `wrist_gate_serve.csv`.

## 5. Two build bugs caught on eye-check, fixed, not hidden

1. Near-white-only fist erase missed the shaded grey built-in fist,
   leaving grey remnants below the moved dance hands. Fixed: erase ALL
   alpha distal to the forearm-end plane within 95 px of the fist blob.
2. That erase on the full plate ate a torso chunk in groove-b (hands fold
   over the chest). Fixed: lowers are built on their own layer, the erase
   runs on that layer only, torso/cape/head are never in it. Groove-b
   re-viewed clean, torso intact.

## 6. What was NOT fixed / not counted

- Sheet-08 provisional hands (19 small icons, not eye-labelled, not
  swappable) and x-ray skeleton hands (19, specialty only, never swapped
  into a pose): no pose defect exists for them, so no pose fix is claimed.
  Their wrist points are defined by the same registry method whenever a
  future swap uses them — they are not counted in the 20/20 above.
- JEI-03x point variant: not flagged by Mars, not in the contact rows
  named, not changed. If its wrist is checked later, it goes through the
  same gate.
- Serve hand's cuff now shows a dark cuff ring at the wrist (the hand
  piece's own cuff outline, rotated to the joint). That is the cuff, not
  an erase artifact, and it reads as the wrist joint. If Mars wants it
  softer, that is a separate cuff-cleanup pick, not claimed here.

## 7. Files (new dated folder only; originals untouched)

Folder: wrist-attach-fix-20261031/
- check_wrist_attach.py, build_wrist_fixes.py, build_library_demos.py
- wrist_gate_serve.csv, wrist_gate_dance_audit.csv
- jei-01-serve-open-palm-WRIST-FIXED-20261031.png
- jei-01-serve-open-palm-ball-WRIST-FIXED-20261031.png
- jei-01-serve-open-palm-MOVE-ONLY-CONTROL-20261031.png (NOT a fix)
- dance-{base-fist,open,point,relaxed}-{groove-a,groove-b,groove-c}-WRIST-FIXED-20261031.png (12)
- library-{1_fist,2_fistback,3_open,4_point,5_point2,6_relaxed,7_grip}-{OLD-centre-paste,WRIST-FIXED}-20261031.png (14)
- serve-before-after-contact-20261031.png, dance-fixed-contact-20261031.png,
  library-before-after-contact-20261031.png
- this report.

## 8. Honest limits — stated as limits about to be broken, not final stops

Per the standing HONEST-LIMITS-BREAK RULE (Mars, 2026-10-31 19:02 CDT):
every limit below is owed a 10-industry + 10-experimental break pass,
wired 100% — that pass is NOT in this task and is flagged as next work,
not presented as done:
- Fingers-along-arm vs fingers-up gesture choice: this task kept the
  dance fingers-up gesture and turned the serve hand along its arm.
  A gesture-direction variant (hand rotated to arm axis for dance too)
  is a Mars pick, not decided here.
- Wrist-point registry is measured from alpha bands, not from a rig
  bone file — a Harmony/Animate/Grease-Pencil bone-parented version of
  the same gate would remove the manual registry step.
- Serve cuff ring (see §6) and any future hand swap still need the gate
  run BEFORE delivery — the gate exists, but it is not yet a mandatory
  pre-delivery step in the main builders (that wiring is owed).

Mars approval of every fix in this folder: 0/1. Do NOT claim approved.
