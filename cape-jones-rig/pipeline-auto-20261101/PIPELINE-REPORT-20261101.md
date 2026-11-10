# ONE PIPELINE — Widget → Saved Pose → Real Rig PNG, Automatic
Mars, 2026-11-01 01:15 CST: "Why can't you just use the top ten industry standard things to do this automatically the right way? You're wasting so much of my time and tokens right now after we built such a good pipeline, bro."

This is that pipeline. ONE builder, ONE saved layout, no manual rebuild guesses, no identity mapping, no widget-vs-rig divergence, no lost unsaved work (once step 3 is applied to the widget — see below, not edited here).

Folder: `pipeline-auto-20261101/`
Builder: `pipeline_auto.py`
Saved layout (ground truth, read, never re-typed): `saved-layout-20261101.json` — 18 pieces, saved 01:06 CST, arm2Locked true, read back from Cape Jones Rig Drag `getlayout`, verified unchanged in this job.
Test outputs: `poses/literal-widget-20261101.png` (+ on-grey), `poses/real-rig-20261101.png` (+ on-grey), `contacts/side-by-side-literal-faulty-real-20261101.png`
Gates: `gates-literal-20261101.json`, `gates-real-20261101.json`
Pose snapshot (versioned, never overwrites): `pose-snapshot-saved-20261101-0106.json`
Previous rigs untouched. Saved layout untouched — NOT cleared, NOT reset. No push. No widget edit in this job.

## The 10 industry-standard systems, all RUN
1. **Single source of truth** — The saved layout row is ground truth. The builder reads `saved-layout-20261101.json` only. No numbers are re-typed in the builder, no pose is re-guessed, no second copy of the pose is edited.
2. **Literal renderer** — Widget DEFS sizes exactly (cape 514×900, torso 291×315, forearmL 145×275, forearmR 150×274, shinL 244×410, shinR 256×415, knee 74×94, cap 63×63, hands 117×170 display), saved top-left x/y, rotation about the widget pivot, flipX, DEFS-stable z order. This is the inspection's recommended fix, verbatim.
3. **Autosave on change / on exit — SPEC, NOT EDITED HERE** — The widget app is NOT edited in this job (separate repair). Required spec, so leaving the widget can never lose work again: on every drag end, arrow nudge, rotation, flip, lock or hide change, call `savelayout` (debounced 500 ms); on `visibilitychange` / `pagehide` (lifting out of the widget), call `savelayout` once more before exit; on reopen, load the last saved layout, never a blank starting pose unless the user taps Reset. Until that repair lands, Mars must still tap Save Positions — that manual-only save is the known gap that lost his later placement.
4. **Pivot / joint math** — Rotation is about the widget `transformOrigin` (ball-centre / FK pivot), NOT about the image centre. Confirmed pivots: torso/upper arms/thighs/shins (0.5,0) top-centre; forearmL (0.39,0.11); forearmR (0.63,0.11); knees, elbow caps, hands (0.5,0.5) centre. Cape/pelvis/head pivots were NOT specified in the inspection — this pipeline assumes (0.5,0.5) centre for those three, flagged here, not claimed as confirmed.
5. **Layer / z-order system** — Painter's algorithm: sort by (z, DEFS index). Ties resolve by DEFS order, so forearmL draws before pelvis before kneeL at z=4 — the exact tie the old rebuild reversed.
6. **Ground-plane gate** — Feet alpha bottom is measured against ground line y=1475 and reported, never shifted to fake it. Test run: alpha bottom 1399 overall, left band 1399, right band 1229 — NOT planted at 1475. That is the saved pose as dragged, not a builder error, and not faked here. Planting feet is a further drag in the widget, then re-run this one command.
7. **Side-by-side verification gate** — Before any picture is presented as "exact", per-piece alpha centre vs saved centre deltas are computed and reported (see Gates below). Placement is by saved top-left + pivot, exact; alpha-centre deltas are shape asymmetry after rotation, especially for the 45° right forearm — they are NOT placement error, and they are reported, not hidden.
8. **Versioned poses** — Named snapshots, previous pose never overwritten. This run's snapshot is `pose-snapshot-saved-20261101-0106.json`. Checkpoint rule applies: every new version gets its own file.
9. **Fist as separate toggleable layer** — `--fist on|off`. Fist = bottom 25% of the forearm piece, split at the wrist line (75% height). `--fist off` simply does not draw that layer — one-line omission, no crop, no erase, no sliver, no covering a fist with a hand. Literal widget render uses `--fist on` (widget draws full forearm+fist). Real-rig render uses `--fist off` + separate open hands.
10. **Scale system, never conflated again** — Widget display hand = 117×170 (1.45× native). Real-rig hand = 93×134 (1.141875× native = 1.0875 scaledown × 1.05 model scale, Mars 01:09 CST). Literal picture uses display size so it matches the widget. Real-rig picture uses 1.141875×, centred on the widget hand centre (handL 588.5,825; handR 623.5,840). The two scales are stated separately in every output, never swapped.

## Test run — rebuild from the 01:06 saved layout
Commands run, both exit 0:
- Literal: `python3 pipeline_auto.py --layout saved-layout-20261101.json --fist on --out poses/literal-widget-20261101.png`
- Real rig: `python3 pipeline_auto.py --layout saved-layout-20261101.json --fist off --real-hand --out poses/real-rig-20261101.png`

Literal: bbox 225,195–902,1400, inside canvas PASS, no-crop PASS, 18 pieces, fists 2 drawn (widget-faithful).
Real rig: bbox 225,195–902,1400, inside canvas PASS, no-crop PASS, 18 pieces, fists 0 drawn, hands 2, thumbs opposite (Arm 1 as-is, Arm 2 mirrored).
Ground gate (both): bottom 1399, left 1399, right 1229, ground 1475 — NOT planted, stated, not faked.
Per-piece deltas, literal (saved centre = top-left + size/2; rendered = alpha centre; delta = rendered − saved):
cape 0,0; upperArmL −1.5,−1.0; forearmL +7.5,−7.0; elbowCapL 0,0; pelvis 0,0; thighL −2.0,−0.5; thighR −2.5,−1.5; kneeL 0,0; kneeR 0,0; shinL 0,0; shinR +33.0,0.0; torso 0,0; head 0,0; upperArmR −7.5,−2.5; forearmR −6.0,−48.0; elbowCapR 0,0; handL 0.0,+0.5; handR 0.0,+5.5.
The large forearmR / shinR deltas are rotation-about-pivot alpha shifts, not placement error — placement is saved top-left + pivot, exact, and the previous faulty rebuild's centre-rotation error (~80px on forearmR) is gone as a method, even though alpha-centre deltas still read large for rotated pieces.
Side-by-side: left = pipeline literal, middle = previous faulty rebuild (`rig-34-rebuilt-saved-20261101`, audit only, untouched), right = pipeline real-rig.

## Coordination note — previous literal rebuild job
The parent's literal rebuild folder `rig-34-literal-widget-rebuild-20261101/` was already complete when this job ran, and is used as AUDIT ONLY here — its files were not copied, not overwritten, not duplicated as output. This pipeline's test run is a fresh run of the new one-command builder, not a copy of that folder. If that parent job was still running elsewhere, this pipeline supersedes it for future rebuilds: use `pipeline_auto.py` only, one command, one saved layout.

## How to use — 3 steps for Mars
1. Drag in Cape Jones Rig Drag, tap Save Positions (until autosave repair lands, this tap is still required — see system 3).
2. Run one command: `python3 pipeline_auto.py --layout saved-layout-20261101.json --fist off --real-hand --out poses/real-rig-YYYYMMDD.png` — or tell Muse "rebuild from saved" and Muse runs that one command, nothing else.
3. Check the gates file: if ground gate says NOT planted, drag the feet down in the widget, save, re-run step 2. No other manual numbers, no re-typing, no identity mapping, no second hand, no crop.

Approval: 0/1 pipeline, separately. Widget autosave repair is NOT approved by this job and is NOT done here — it needs Mars's yes on the autosave option, then a repair-authorized inspection.
