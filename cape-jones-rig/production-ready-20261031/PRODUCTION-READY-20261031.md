# PRODUCTION-READY + 10 THINGS WIRED 100% + FULL OWED LIST — 2026-10-31

Mars order, 17:52 CDT (resumed after an accidental stop): log ALL of this info to the
repo, document it, pull industry-standard stuff and wire it 100%, get it landed
(push-ready here — NO push made in this task; the landing batch pushes),
keep working, and answer: what else to be fully production ready, what else to
wire 100%, what is unfinished / owed / not-yet-owed, and what is in the todo list.

Status of THIS pack: 10/10 wired outputs built and viewed by the builder.
Mars approval of this pack: 0/1. Landing is not approval.

## 1) THE 10 WIRED THINGS — 10/10 built, viewed, spec + script

Folder: `production-ready-20261031/` — builder `build_production_ready.py`,
proof `proof-10-wired-20261031.png`, QC JSON `qc-10-wired-20261031.json`.
Base art is NEVER recoloured: every output composites OVER the clean plate.

1. **Pseudo-normal / depth relight** — `01-pseudo-normal-relight-20261031.png`
   Method: depth = blurred silhouette alpha; normal from depth gradient; light
   upper-left, cyan lit edge + cool shadow. HONEST LIMIT: pseudo-normal from
   silhouette depth, NOT a measured 3D normal pass. True normal/depth relight
   is an L5 item, still owed — this wires the working method, it does not fake L5.
2. **Volumetric shafts** — `02-volumetric-shafts-20261031.png`
   Cycles god-ray v2 background (density 0.35, anisotropy 0.6, spots 8000+4000+4000)
   + PIL shaft beams on top for this proof. Crisp-shaft pass still owed.
3. **Dust motes in volume** — `03-dust-motes-20261031.png`
   90 motes, seeded, in the shaft field. True Cycles volumetric motes still owed
   as a separate render; this wires the placement/brightness method.
4. **Side-weighted wrap** — `04-side-weighted-wrap-20261031.png`
   Rim strong on the left/backlit side, fading to the right. Full normal-weighted
   version needs the true normal pass (item 1 limit).
5. **Limb afterglow (punch)** — `05-limb-afterglow-punch-20261031.png`
   Soft-rim trail on the fighting pose, fading ghosts behind the arm.
   Afterglow is APPROVED as default preset; limb-specific punch application 0/1.
6. **Energy orbs snapped to fists** — `06-energy-orbs-snapped-fists-20261031.png`
   Yellow orbs just above/outside each raised fist in the arms-up pose, fists
   still visible below the orbs. Two fix passes were needed: v1 orbs covered the
   fists, v2 sat on the elbows; v3 (this file) sits above the fists. Snap is
   plate-scaled and viewed — re-measure on the full plate before a final shot.
   This is an energy-orb read only, NOT a Dragon Ball character.
7. **Running cycle + afterglow** — `07-running-cycle-afterglow-20261031.png`
   Walk contact/passing frames (4) as a cycle strip with afterglow trail.
   A true running animation (not walk frames) + flying afterglow are still owed.
8. **Lip-sync timeline** — `08-lipsync-timeline-20261031.png`
   Visemes v2 heads in order: rest, EE, AH, OH, OO, MBP, FV, SZ.
   Full 14-viseme timeline + a dialogue shot still owed.
9. **Storyboard / animatic** — `09-storyboard-animatic-20261031.png`
   6 panels: establish room 2.5x, arms-up pre-flex, punch −110 impact,
   dance groove, flying afterglow, flex true final. Drawn boards 0/30,
   animatics 0/30 — this wires the panel template, not the 30 boards.
10. **QC gate + title card** — `10-qc-gate-title-card-20261031.png`
    Gate: 0 pure-red label pixels, RGBA alpha present, plate untouched by rim
    layers, knee-feet per-frame gate 8/8 keyframes, new dated filename.
    Title card: "CAPE JONES". Per-shot QC still owed: 0/30.

## 2) FULLY PRODUCTION READY — checklist with counts + percentages

Production ready means: a shot can go from spec → render → QC → delivery
without a new method being invented mid-shot. By that test, NOT ready yet.

| Area | Done / Total | % | What is missing |
|---|---|---|---|
| Rig + poses (approved) | 7 / 12 poses | 58% | Hip-lower flexes, Arm1 straightening, true 3/4 head/torso, side/back body, neck cylinders 0/5, blank/furious heads 0/6, separate feet, gauntlet-only |
| Clean pieces / slices | 140 / 184 sheets | 76% | Eye pass on 129 sheets; 44 sheets are backgrounds/reference, not rig pieces |
| Lighting levels L0–L3 | 3 / 3 levels defined, L3 built | 100% defined, 0/30 shots rendered | Per-shot L3 composites 0/30 |
| Levels L4/L5 (separate workstream, delivered 2026-10-31) | L4 candidate 1/1 built, L5 0/1 defined-not-built | L4 100% built, L5 0% built | Mars approval L4 0/1; crisp shafts, true normal, side-weighted wrap, per-shot colour tracking 0/30 |
| Preset packs | v5 + v6 2/2 defined | 100% defined | L4 as a new pack version (never a rename of v6) — Mars decision |
| Colour: LUTs | 70 / 70 | 100% approved | — |
| Colour: JoJo v3 palettes | 8 / 8 palettes + method | 100% approved | Full-colour cape versions of other 7 palettes 0/7, production renders 0/8, painted-bg versions 0/8, colour script 0/1, poses beyond A-pose 0/8 |
| Eyes | In-mask Robin 1/1 approved | 100% approved (in-mask only) | Full Robin library (all expressions/angles) 0/1, rounded animated cowl top 0/1, comedic band composite 0/1, Robin EPS pulls 0/5 |
| Fists | Forward punch flipped 1/1 approved, uppercut saved | 100% pieces approved | Full punch pose integration 0/1 |
| Dance | Knee-feet correction 1/1 approved, 100% perfect | 100% approved (improved dance) | Reworked kick 0/1, true torso twist 0/1, combine-dance FootIn fix 0/1, beep audio + Blender sparkles 0/1, clean full-size final + lighting 0/1 |
| Shots end-to-end | 0 / 30 | 0% | Specs 30/30 written; boards 0/30, animatics 0/30, renders 0/30, QC 0/30, edit 0/30 |
| Audio | Demo tones only, cue sheet v2 | 0% recorded | Recorded final audio 0%, dialogue shot 0/1 |
| Delivery | Spec 1/1 written | 100% written, 0% approved | Frame size + safe areas — MARS ONLY, not set |
| **Wired inventory (corrected)** | **24 / 41** | **59%** | CJ-01 rim/bleed caveat WITHDRAWN: delivered rim max 0.89, bleed max 0.13; rim pass 63,773 nonzero alpha max 228, bleed pass 52,970 nonzero alpha max 34 |

Overall: do NOT quote a single production-ready % as fact — the honest roll-up
is: pipeline defined and wired at 59% (24/41), approved hero pieces at 100%
for the items Mars has approved, final shots at 0/30 = 0%. The show is
buildable now; it is not finished.

## 3) EVERYTHING WIRED UP 100% — checklist

- Installed tools wired with a viewed Cape Jones output: Blender 5.2.3, Tahoma2D,
  Krita, Pencil2D, Synfig, FFmpeg, PIL — wired, deeper GUI tests still owed
  (Tahoma GUI render, Krita animation timeline, Synfig character rig,
  Pencil2D import/export, full-height Blender re-render, measured loudness).
- Comparison tests: 0/7 = 0% — blocked on legitimate their-side trial installs
  + viewed files. Toon Boom trial: Mars-only secure entry. Animate: enrollment
  unknown, JSFL not run.
- Free-stack / industry methods wired in this pack: 10/10 above.
- Still to wire 100%: show-repo rigs moving (Teen Titans + all repos audit,
  running), Robin library, wrap v4 true normal, L5, per-shot stacks 0/30.

## 4) UNFINISHED / OWED / NOT-YET-OWED — full list, counts + %

UNFINISHED (started, not finished):
- Exaggerated flex deeper squat + hip-lower versions: built, approval 0/2
- Wrap v3: built, approval 0/1; experimental soft-on-halo 0/1
- God-ray L3 V4/V5: built, approval 0/2; crisp shafts 0/1; gold-rim-alone L3 0/1
- L4 candidate: built, approval 0/1; gold-vs-red pick 0/1
- Afterglow running/flying applications: 0/2 (default + teleportation approved)
- Visemes v2: built, approval 0/1; mask-first on eyes/expressions 0/1
- Cape styles v2: built, approval 0/1; bone-chain rig in a pose 0/1; cape in a
  final shot with body 0/1
- Device prop v2: built, approval 0/1 + exact scale — MARS ONLY
- Show templates: 7/7 templates, 0/7 final scenes = 0%
- Mochiichao combine: 0/4 approved; two-hand grip pose 0/1; crowd layer 0/1
- Effects v2: node setups 12/12, viewed frames 4/12 = 33%; per-shot specs 0/30;
  animated sequences 0/5; GPU volumetric sequence 0/1
- Clean-slice eye pass: 129 sheets owed

OWED (promised, not started as a final):
- Shots CJ-01–CJ-30 end-to-end: 0/30 = 0%; 12-principles checks 0/30; QC 0/30
- Boards 0/30, animatics 0/30, edit decision list 0/30, punch/dance edits 0/2
- Title card final 0/1, credits 0/1 (no names invented), archive set 0/1
- True hand-drawn 3/4 head/torso, side, back/3-4-back: 0/4
- Knee-feet retro-check walk/kick/flex/fight: 0/4 families
- Hand-drawn inward-foot lowers: 0/2
- JoJo items above: 0/7 + 0/8 + 0/8 + 0/1 + 0/8
- Room-at-2.5x Blender proof shot: 0/1; ACES 1.3 comparison: 0/1
- Messenger JoJo v3 send: 0/9 — blocked on Mars connecting Messenger
- Goodville repo identification: 0/1 — do NOT push to a guessed repo

NOT-YET-OWED (new items discovered in this audit — owed from now, not before):
- L5 definition items: crisp shafts, true normal interior, side-weighted wrap,
  per-shot colour tracking, shot-to-shot consistency: 0/5
- Gold-preserved V5 with opaque split rings: 0/1 (view-transform fix alone
  does not fix V5 — mask alpha max 0.627 mixes gold over cyan)
- Colour tracking fields on every shot spec (input_color + on_screen_color +
  mix_cause): 0/30 — standing rule from the gold-to-red study (cause: Blender
  AgX default view transform for V4; semi-transparent gold over cyan + bloom
  overlap at the seam for V5)
- Afterglow powers/variations off the base afterglow: 0/∞ (future, per beat)
- Spec archive index (this pack, part 5 below): 1/1 built here, landing pending
- Repo landing batch 2: in progress, verification pending

## 5) TODO LIST — reproduced, updated 2026-10-31

IN PROGRESS:
- Approval pack 100% of unapproved content + full production accounting to 100%
PENDING:
- Repo landing batch 2: everything on disk with no reason to hold, verified on main
- Wrap v4: true normal/depth relight, full-height, Cycles shafts, side-weighted
  wrap, true dust, rim-only proof
- L4/L5 framework + gold-to-red colour-shift study + Lighting Pack v5/v6 presets
  (framework + study + presets delivered separately 2026-10-31; approval pending)
- Effects Sunbeam Preset v1 saved + upgraded (orb snap, denoise, shaft masking)
- Afterglow default preset + teleportation variant + running/flying afterglow
  (default + teleportation approved; running/flying pending)
- Hip-lower flexes (over-exaggerated + deep squat, both sides, anatomy)
- Robin eyes 100% library + cape colour check + Teen Titans/all-repo animation audit
- Spec archive: all specs/info to repo so everything can be revisited/recreated
- 10 new industry-standard things wired 100% + production-ready checklist
  (THIS PACK: 10/10 built and viewed, approval 0/1)
BLOCKED — Mars only, never silently decided:
- Messenger JoJo v3 send 0/9: Mars must complete the Messenger connection
- Toon Boom trial: Mars must complete the secure entry for fmmg.mars@gmail.com
- Mars-only decisions: delivery frame size + safe areas, canonical room ID,
  parts exceptions 6, device exact scale, dual-light pick V3 vs V4, L3/L4 approvals
COMPLETED (this session, for the record — not in the active todo):
- Knee-feet correction: APPROVED 1/1, 100% perfect
- Fist v5 flipped forward punch: APPROVED 1/1
- Afterglow default preset: APPROVED 1/1
- Eyes v4 in-mask Robin fit: APPROVED 1/1
- True final flex relaxed-clean: APPROVED, perfect
- Repo PR #288 (253 files) + PR #289 (KNEE-FEET-RULE 7,514 bytes, SHA match):
  landed and verified on main
