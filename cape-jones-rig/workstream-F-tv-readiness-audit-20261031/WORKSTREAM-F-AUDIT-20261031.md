# WORKSTREAM F — TV Production Readiness Audit — 2026-10-31

Scope: ~/workspace/cape-jones-rig/ only. No repo push. No deletions. No file overwritten.
This is an AUDIT only. No new scale, orientation, or ground-feet gate was built here,
because the ground-feet gate is already running under a separate agent and is NOT duplicated.
Mars picks are NOT decided here. Nothing below is claimed approved or landed beyond what
its own source file states.

## 0. Focus change applied (Mars, 2026-10-31 20:53 CDT)

PRODUCTION = work that blocks shots: feet planted, whole figure, furniture ratio.
ADDITIVES / EXTRAS = further orientation variants, labelled separately below.
A second orientation or a second scale candidate is a comparison / delivery extra,
not a second production lock — only the Mars-picked scale becomes production.

## 1. PRODUCTION — counts

| # | Production item | Built / gate | Mars approval |
|---|---|---|---|
| 1 | Room-scale lock definition: 2.5x standing, rig 950px, feet on floor, seated 2.3x; locked preview showcase/layout-pass-room-scaled-25x-20261031.jpg (1168x1060, head 268, feet 911, height 643, 643/950=0.677, 643/1060=60.7%) | Defined, measured | 1/1 (STATUS, 15:51 CDT) |
| 2 | Room-scale master 1920x1920: bbox (593,385)-(1327,1550), height 1165, feet 1550 on rug (179px below rug top ~1371, 32px below chair feet ~1518) | Hard gate scale+feet PASS 1/1 | 0/1 (room-scale-fix delivery) |
| 3 | Landscape A — locked 2.5x pull-back: final bbox (641,35)-(1278,1045), height 1010, ratio 1.423, whole, margins 35/35 | Scale gate PASS | 0/1 |
| 4 | Landscape B — 3.0x CANDIDATE pull-back: final bbox (639,29)-(1282,1051), height 1022, ratio 1.710, whole, margins 29/29 | Scale gate PASS (above minimum) | 0/1 |
| 5 | Portrait A — 2.5x planted: bbox (172,535)-(906,1700), height 1165, ratio 1.424, feet 1700, rug 0.624 | Scale gate PASS | 0/1 for A itself* |
| 6 | Portrait B — 3.0x CANDIDATE planted: bbox (99,302)-(980,1700), height 1398, ratio 1.709, feet 1700, rug 0.624 | Scale gate PASS | 0/1 |
| 7 | BARS PRESET ground anchor (multiplane-upgrade-20261031/): world ground Gy=700, feet 700, 24/24 test frames + 24/24 final frames = 48/48, no_clip 24/24 each | Measured PASS | See §4 discrepancy — NOT claimed 1/1 here |

* Portrait nuance, from its own report: the OLD portrait framing was approved 1/1 WITH
feet refinement owed. That 1/1 does NOT approve new A or B. Do not transfer it to them.

Mars approvals in this workstream, distinct deliverables: 1/8 = 12.5%
(only the lock definition, item 1). Gate-passing built candidates: 6/6 = 100%
(items 2–6 plus BARS feet measurement, item 7) — gate pass is NOT Mars approval.
Per-shot room-scale application beyond this arms-up proof: 0/30 = 0%.
Seated 2.3x landscape/portrait proof: 0/1 — not built in these folders (standing only).

## 2. PRODUCTION RULES VERIFIED (not re-decided)

- Feet anchor = alpha-bbox bottom on the world ground line. Scaling / camera growth
  goes ABOVE the anchor, never from the centre. BARS: paste_y 47 + bbox bottom 653 = 700.
  Landscape B: feet stay at scene 1550 while scale grows +20% (head 385 -> 152).
  Portrait A/B: same feet line 1700, scale is the only difference.
- % of frame is BANNED as a landscape gate. The landscape gate (check_scale_gate.py)
  FAILS loudly (exit 2) if final height <1000px in 1920x1080 OR figure-to-chair
  ratio <1.42 OR figure not whole, and prints "% -of-frame height alone is NEVER a
  scale pass". Proof the old gate was broken: reverted landscape 655px / ratio 1.193
  and old landscape frame-ratio 0.601 both show a frame-% pass hiding a furniture
  regression (-16.2% figure-vs-room, 1.424 -> 1.193). The room-scale master gate
  (0.607 + feet-on-rug) is MASTER-only and must NOT be quoted as a landscape gate.
- Whole figure, not silent shrink: room-scale figure 1165px exceeds the 1080 protected
  square by 85px, so a centre-crop landscape cuts head 35px + feet 50px. The fix in
  these folders is a pull-back WINDOW (figure + room together), never a figure-only
  shrink back to the old 709px floating figure (old: feet 49px above rug top, 196px
  above chair feet).
- Reverted landscape (655px, ratio 1.193, -510px / -43.8% vs master): REJECTED, 0/1,
  do not reuse as a delivery.

## 3. MARS-BLOCKED — DO NOT DECIDE

- 2.5x vs 3.0x: BLOCKED. "Up 0.5" is ambiguous in the source reports themselves:
  either 2.5x WAS the up-0.5 step from 2.0x, or correct = 2.5 + 0.5 = 3.0x.
  3.0x is labelled CANDIDATE in both landscape and portrait folders. Do NOT assert 3.0x.
  Visible difference is furniture ratio (1.423 vs 1.710, +20.0%), NOT final pixel
  height alone (1010 vs 1022 landscape, +1.2%, because the pull-back window grows).
- Chair-back at waist: GATE = WARNING with numbers, never a faked PASS.
  Master: chair-back top ~700 (visual estimate) vs waist ~1002, diff 302px.
  Forcing waist = chair-back with feet on floor (1550) needs height
  (1550-700)/0.47 = 1809px, head at -161, off-frame.
  Portrait: waist A ~1152 (diff 452px), B ~1043 (diff 343px) vs chair-back ~700.
  At NO feet-on-floor scale in this arms-up crop does chair-back equal waist.
  Owed clarification (not assumed): apose layout-pass composition, chair armrest,
  or a seated pose.
- Canonical room pictures: BLOCKED / still owed. See §5.

## 4. GROUND-FEET GATE — AUDIT ONLY, NO DUPLICATION

A separate agent is already running the ground-feet gate. Nothing in this folder
rebuilds it. Audited from multiplane-upgrade-20261031/ only:

- Final bars: 28px wide, alpha 140, every 260px, blur 1.0.
  Test bars (comparison only): 55px, alpha 210, every 180px, blur 2.0.
- World ground Gy=700, feet_y_screen = feet_y_world = 700 on all 24 test frames
  and all 24 final frames (48/48), verified from feet-measurements-20261031.json.
  No-crop gate checks CAPE ALPHA pixels (1100x750 screen), not the canvas; all pass.
- Grounded-vs-airborne rule (governing rule, to apply — not a second gate built here):
  GROUNDED: feet on the ground line; the gate FAILS if a grounded figure's feet are
  off the ground. AIRBORNE: the shot is labelled airborne with its height / flight
  line stated; feet are NOT forced down to the ground line. Forcing airborne feet
  down would be the same class of fake as forcing chair-back to waist.
  Note on evidence: the BARS preset itself is a GROUNDED rooftop case (feet 700);
  it demonstrates the grounded half. No airborne proof is claimed from that folder.
- DISCREPANCY FLAGGED, not papered over: BARS-PRESET-METHODS-20261031.md says
  "EXPERIMENTAL preset, approval 0/1" and "Original multiplane test = WORKS, real
  2.5D depth, APPROVED as a depth test, NOT approved as a final shot", with
  "Still owed: Mars approval 0/1 (upgraded preset, feet fix, final bars pick)".
  This audit therefore does NOT report the upgraded BARS PRESET as APPROVED 1/1.
  The depth-test approval and the upgraded-preset approval are different items.
  Also: bars-preset-20261031.json fps is 12 (24 FRAMES, not 24fps) — do not confuse
  the 24-frame count with the show's 24fps rate used for the dual videos.
- Still owed for BARS: final bars pick (test vs final), per-shot multiplane 0/30,
  Blender multiplane render (scene construction only, .blend saved, no render claimed).

## 5. CANONICAL ROOM — PLACEHOLDER, NEVER CANONICAL

batch-KKGuh is the STAND-IN / placeholder background in all four folders
(dual-orientation spec, room-scale fix, landscape fix, portrait fix — each report
states this explicitly). It is NEVER called canonical in those reports, and this
audit does not call it canonical either. Canonical room = a different room Mars
has pictures of; pictures still pending. All floor / chair / rug numbers above
(rug top ~1371, chair feet ~1518, chair-back ~700, chair height 818 in portrait)
are KKGuh-stand-in measurements and must be re-measured in the canonical room
once its pictures arrive. Do not recolour the stand-in toward a guessed canonical.

## 6. ADDITIVES / EXTRAS — labelled separately, NOT production blockers

Dual-orientation spec (dual-orientation-20261031/, Mars approval 0/1):
verified dims — master 1920x1920, landscape 1920x1080 (crop y420-1500),
portrait 1080x1920 (crop x420-1500), protected square 1080x1080 (420-1500 both axes),
24fps H.264 videos verified by ffprobe for landscape + portrait (room-scale videos
also 24fps). Proof figure (old, pre-room-scale) was whole in both orientations
because it lived inside the protected square — that proof is SUPERSEDED for room
shots by the 1165px room-scale figure, which does NOT fit the protected square.
Extras in this spec (not shot blockers): protected-square method as a general rule,
square pull-back export, blurred-pillarbox backup (subject 608px tall in portrait),
blind/tracked-crop comparison (method C, caution), 4K x2 scaling, platform safe-zone
overlays (portrait safe box 97-842 x 288-1482; ads bottom 672), and the
industry-tool mapping (Premiere Auto Reframe / Resolve Smart Reframe / Final Cut
Smart Conform — mapped, NOT run). These may proceed in parallel but do not unblock
or replace the Mars scale pick, the chair-back clarification, or canonical pictures.

## 7. VIEWED PROOFS (this audit)

- dual-landscape-scale-fix-20261031/before-after-contact-20261031.png — viewed:
  left reverted small/floating, middle 2.5x planted, right 3.0x planted, labels match §1.
- dual-portrait-feet-planted-20261031/before-after-contact-20261031.png — viewed:
  old mid-rug feet 1548, A + B both feet 1700, B larger vs furniture.
- dual-orientation-room-scale-fix-20261031/before-after-contact-20261031.png — viewed:
  old floating vs new room-scale, both orientations.
- multiplane-upgrade-20261031/bars-preset-final-ground-proof-20261031.png — viewed:
  figure on the red world-ground line y=700, final bars in front.
- Dimensions re-checked by script (not by eye alone): all dual / room-scale /
  landscape / portrait PNG sizes match §1/§6; dual + room-scale MP4s are 24fps H.264.

## 8. STILL OWED (in priority order, production first)

1. Mars pick: 2.5x lock vs 3.0x candidate — BLOCKED, approval 0/1 for the picked version.
2. Mars clarification: chair-back-at-waist in this crop — BLOCKED.
3. Mars canonical-room pictures, then re-measure floor/chair/scale — BLOCKED.
4. Per-shot room-scale application: 0/30 = 0%.
5. Seated 2.3x proof in landscape/portrait: not built here.
6. BARS final bars pick + per-shot multiplane 0/30 (separate ground-feet agent's gate).
7. Dual-orientation spec approval: 0/1 (extra, not a shot blocker once §8.1–8.3 close).
8. No repo push / landing: separate step, not done here.
