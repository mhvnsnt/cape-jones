# LIMITS-BROKEN PUSH 2 + TV PRODUCTION TRIAGE — 2026-10-31 (evening)

**Status, plainly. No approval, no landing claimed. Mars approval of this set: 0/1.**
- Method: free / open-source / own reverse-engineered methods only, local PIL + scipy + numpy on this VM. No cracking, no licence bypass, no proprietary copy, no paid run, no GPU run, no download/install in this task. Blender, Ghostscript and Ruffle were not found in PATH here, so no render/install is claimed for them. Ruffle remains owed via its official binary — that step was NOT attempted here, because this task was kept to already-installed local tools.
- No Kaggle/Colab run. The FMMG account (fmmg.mars@gmail.com) was NOT used, because no GPU run was approved or attempted. No other account was used.
- No repo push. No file Mars saw was overwritten. Base art untouched; all outputs are new dated files in this folder. Builder script: `build_push2.py` in this folder. Base: `rig-apose-v7c-clean-transparent.png` (1100×1500).
- Every image proof in `proofs/` was viewed by the builder in this task: 5/5 = 100% (P1, P2, P3, P4, P5).

## 1. TV PRODUCTION READINESS TRIAGE — focus change 2026-10-31 20:53 CDT

Work that does not block an episode/segment is **ADDITIVE/EXTRA, not a production blocker**. Push order in this task followed that rule: shot/audio/QC pushes first (P1, P3, P4, P5, P6), polish/tooling after (P2, G4/G7 polish), decision/labour templates last (G6, no break claimed).

### Limits-broken-all (20 limits) — production tier
| Tier | Count | Share | Limits |
|---|---|---|---|
| PRODUCTION-BLOCKING (episode/segment or a named shot cannot finish without it) | 7/20 | 35% | L01 masters, L11 finals frame size/safe areas, L12 final audio, L13 Arm1, L14 torso-twist master, L15 device-grip prop, L16 129-sheet eye pass |
| ADDITIVE / POLISH / VALIDATION / ALREADY BROKEN | 13/20 | 65% | L02, L03, L04, L05, L06, L07, L08, L09, L10, L17, L18, L19, L20 |
- L10 is episode-conditional: it is additive unless a Bonyu shot is actually ordered (and unless Mars clarifies Bonyu vs Captain Ginyu, whose poses are already approved).
- No experimental project removes L11, L12, or L16. Those need a Mars decision, a recording session, and human viewing respectively.

### Limits-broken-10×10 (7 groups) — production tier
| Tier | Count | Share | Groups |
|---|---|---|---|
| PRODUCTION-BLOCKING groups | 3/7 | 43% | G1 drawing masters, G5 motion/pose keys, G6 source/decision |
| ADDITIVE groups | 4/7 | 57% | G2 shading polish, G3 volumetric polish, G4 tooling validation, G7 gold-split polish |

## 2. COUNTS — PUSH 2 (honest, no re-labelling)

| Measure | Before push 2 | After push 2 | Change |
|---|---|---|---|
| 20 limits: BROKEN | 4/20 = 20% | 4/20 = 20% | 0 |
| 20 limits: PARTIAL | 10/20 = 50% | 10/20 = 50% | 0 |
| 20 limits: BLOCKED | 6/20 = 30% | 6/20 = 30% | 0 |
| 20 limits moved to a better status | — | 0/20 = 0% | — |
| 10×10 groups: fully BROKEN | 0/7 = 0% | 0/7 = 0% | 0 |
| 10×10 groups: PARTIAL | 5/7 = 71% | 5/7 = 71% | 0 |
| 10×10 groups: BLOCKED | 2/7 = 29% | 2/7 = 29% | 0 |
| 10×10 methods named | 140 | 140 (unchanged) | 0 |
| 10×10 methods run (prior task) | 103/140 = 74% | 103/140 = 74% | 0 new 10×10 methods; push 2 is sub-remainder work, not a recount |
| Push-2 attempts in this task | — | 7 (P1–P7) | — |
| Push-2 sub-remainders CLOSED | — | 3/7 = 43% | P1, P3, P5 (see §3) |
| Push-2 attempts narrowed but not closed | — | 2/7 = 29% | P4, P6 |
| Push-2 attempts confirming still weaker/blocked | — | 2/7 = 29% | P2, G6 templates |

**Why no limit was re-labelled:** a sub-remainder closing does not close its parent limit while the parent's stated unblocker (hand-drawn master, true 3D normal pass, Cycles/GPU sequence, v7c-builder frame, V5 shot composite, vendor tool, Mars decision, human eye pass) is still outstanding. Claiming a re-label on a sub-remainder would repeat the exact inflation the 10×10 report refused.

## 3. PUSH RESULTS, ONE PER GROUP

### P1 — G1 drawing masters, production-blocking — SUB-REMAINDER CLOSED: profile head composited into side view
- Proof (viewed): `proofs/P1-G1-side-v2-profile-head-20261031.png`
- What was done: apose squished 0.45× (side-width), front-head area cleared, real `sliced/Head_Profile.png` pasted 120×200 at (490,253). Viewed result reads as a side-width figure with a profile face — the 10×10 remainder "face still front-facing" is closed for this derived view.
- What is NOT closed: torso, arms, legs and cape are still squished front art, not a hand-drawn side master. G1 stays PARTIAL. Next: segment-twist master sheet from chest/pelvis pieces (not whole-figure rotates), then a redrawn master if Mars commissions one.

### P2 — G2 true 3D shading, additive polish — CONFIRMED WEAKER, NOT AN IMPROVEMENT
- Proof (viewed): `proofs/P2-G2-distance-normal-sideweight-20261031.png`
- Method: scipy silhouette-distance transform + per-pixel side weight (left brighter, right darker), measured inside alpha.
- Measured: left mean R 135.4 vs right 131.2, delta +4.2. Compare: original L02 delta +31.9, no-shade control −0.8, 10×10 gradient also weaker than L02.
- Honest cause, stated not hidden: the white suit saturates at 255, so a left-brightening factor cannot lift it; only the right side can fall, and only slightly. This method does NOT reproduce L02 and must not replace it.
- G2 stays PARTIAL. Next, as in 10×10: original L02 silhouette-distance normal combined with per-limb depth layers, measured against the L02 delta — not against this weaker gradient.

### P3 — G3 volumetric / shafts, additive polish for 2D shots — SUB-REMAINDER CLOSED: shafts BEHIND the figure
- Proof (viewed): `proofs/P3-G3-shafts-behind-figure-20261031.png`
- Defect fixed: in the 10×10 test shafts were drawn OVER the figure. Here shafts are drawn on the background layer and the apose is pasted on top.
- Measured (corrected tint definition, B−R > 30 and B > G, so white suit is not miscounted as shaft): shaft-tint pixels total 339,170; outside figure alpha 339,126; inside figure alpha only 44 (edge anti-aliasing). Row y=200 (above the figure): 246 shaft pixels, 8 edge transitions = 4 sharp shafts.
- G3 stays PARTIAL (2D only). No Cycles volumetric shaft sequence and no GPU sequence exist (still 0/1). Next: tiled Cycles volume at full res, shafts behind the figure, A–B vs these sharp PIL shafts — GPU step needs specific Mars approval.

### P4 — G5 motion / pose keys, production-blocking — NARROWED, NOT CLOSED: Arm1 piece-only rotation spec
- Proof (viewed): `proofs/P4-G5-arm1-piece-rotation-20261031.png`
- What was done: `cut-limbs-v7c/Arm_Front_Upper.png` (153×320, alpha 22,331 px) shown original vs rotated, magnitude 18.2° (the Arm1 QC fail magnitude). Rotated piece alpha 21,881 px (edge resampling loss, expected for a PIL rotate).
- Honest limit, stated on the proof itself: this is a PIECE-ONLY rotation, NOT a v7c-builder frame. The 10×10 whole-figure rotate defect is avoided, but the builder-frame defect is not closed. Sign convention (PIL rotate direction vs the +18.2° QC sign) is NOT verified here — the builder must verify sign against the gate before applying it.
- Spec for the builder: Arm_Front piece, rotation magnitude 18.2°, gate ≤10° AND ≤10 px, builder frame still owed. G5 stays PARTIAL. Device-grip and foreshortened kick piece remain owed (see G5 remainder in 10×10 report).

### P5 — G7 gold split, additive polish — SUB-REMAINDER CLOSED for an apose frame, NOT for a V5 shot
- Proof (viewed): `proofs/P5-G7-gold-split-apose-20261031.png`
- What was done: on the real apose frame (not a synthetic rectangle), a gold test patch x 500–700, y 700–900, split opaquely at seam x=600 (figure-centre range 550–650 from the 10×10 sweep), 2 px seam marker excluded from measurement.
- Measured: gold median left (255, 180, 80) exactly equals input gold; right (255, 180, 80) exactly equals input gold. No semi-transparent overlap, no pink shift.
- Honest limit: the patch is a labelled TEST PATCH on an apose frame, not a V5 shot composite with split rings. The V5 full-shot opaque-split composite is still owed. G7 stays PARTIAL.

### P6 — G4 gates / tooling, additive validation — NARROWED: real apose gate measurements, 6/20
- Data: `proofs/P6-G4-real-gate-measurements-20261031.json`
- Real measurements on the apose (all measured here, none placeholder): alpha bbox (248, 253, 875, 1294), alpha px 373,846, figure 627×1041, centre x 561, red-label px 0, size 1100×1500. Coverage: 6/20 = 30% real, 14/20 = 70% still schema/placeholder.
- What is NOT measured here, and why: cowl collar-edge interruption, arm angle, fist offset, knee/foot angle need piece-separated renders, not a flat apose PNG. Those 14 remain NOT measured. G4 stays BLOCKED for its vendor/licence items (trial installs, Ruffle binary, Animate sign-in, Grease Pencil workstream report). Next, in 10×10 order: Ruffle binary install + render test first (cheapest unblocker, NOT attempted here), then Animate sign-in, then the GP workstream report.

### P7 — G6 source / decision, production-blocking — STILL BLOCKED, templates only, 0 breaks
- File: `G6-TEMPLATES-20261031.md` — 4/4 templates (Bonyu source intake, frame-size/safe-area decision sheet, recording session sheet, 129-sheet eye-pass batch sheet), 0/4 breaks.
- Counts unchanged: eye pass 0/129 sheets passed in this task, per-shot finals 0/30, final recorded audio 0%, Bonyu source 0. Naming templates does not break a decision/labour limit, and this report does not pretend otherwise.

## 4. STILL OWED / BLOCKED — AFTER PUSH 2

- Hand-drawn 3/4, side, back, and torso-twist masters: 0 (derived views only, now including a profile-headed side view).
- True 3D normal pass: 0 (L02 method remains the strongest measured side-weighting, delta +31.9; push-2 gradient is weaker, delta +4.2).
- Cycles volumetric shaft sequence / GPU volumetric sequence: 0/1 (2D shafts behind the figure are done; GPU step needs specific Mars approval).
- v7c-builder Arm1-fixed frame: 0 (piece-only spec + proof only; sign to verify).
- Clean single device prop PNG: 0 (L15 kitbash placeholder rectangle remains the only grip placement proof).
- Full V5-shot opaque gold split composite: 0 (apose test-patch split done, median exact).
- Ruffle render test: 0 (binary not in PATH, not installed here).
- JSFL run / Harmony-Animate comparison both sides (6/7 tests): 0 beyond the 1/7 Blender-side test already done.
- Grease Pencil .blend in this task: 0 (other workstream's deliverable; do not claim it here).
- Mars decisions: frame size + safe areas, final audio session, Bonyu source/call + Bonyu-vs-Ginyu clarification, licence decisions (OpenPose, ToonCrafter, Cascadeur/Plask/MoveAI, EbSynth, Natron fork).
- Eye pass: 129 sheets owed, 0 passed in this task.
- Experimental vendor runs: 25/25 still owed, all gated on specific Mars approval (see experimental deepened report).

## 5. HONEST-LIMITS-BREAK RULE, APPLIED HERE (not as a slogan)

Every limit above is stated as a limit we are about to break, with the exact next pull named — and where the pull is a GPU, vendor, decision, or human-labour unblocker, that unblocker is named instead of a fake break. Partial/blocked items were pushed only with free, open-source, or own reverse-engineered methods: PIL/scipy/numpy transforms of Cape's own art, a real sliced profile piece, and measurement — never cracking, licence bypass, or proprietary copying. No limit in this report is presented as a final stop, and no limit is presented as broken when its unblocker is still outstanding.
