# FULL TV PRODUCTION ACCOUNTING — Cape Jones — 2026-10-31 (recomputed, evening)

**Status of this file:** NEW recomputation for `approval-pack-20261031/`.
It supersedes, as a current count, the stale file
`~/workspace/cape-jones-rig/FULL-PRODUCTION-ACCOUNTING.md` (dated 13:56 CDT
in the task brief). That stale file is **NOT quoted as current anywhere
below** — its numbers are not reused except where a count was re-verified
from disk for this run.

**No repo push was made by this accounting run. No number below is
invented.** Where a count could not be verified from disk, it is marked
**UNVERIFIED** and is not counted as verified.

## Corrections carried into this run (do not revert)

1. **Wired inventory: 24/41 = 59% stands.** From
   `wired-100-20261031/WIRED-INVENTORY-20261031.md`: wired–viewed output
   21/41 = 51%, wired–file-verified by re-parse 3/41 = 7%, total wired
   24/41 = 59%. Blocked + free replacement wired 12/41 = 29%.
   Partial 3/41 = 7%. Mars-only / push-only 2/41 = 5%.
   Installation alone is never wiring in that inventory, and it is not
   wiring here either.
2. **CJ-01 rim/bleed caveat WITHDRAWN.** The delivered CJ-01 Level 2 v2
   run reports rim max 0.89, bleed max 0.13. Pixel check on the delivered
   passes: rim pass 63,773 nonzero-alpha px (max 228), bleed pass
   52,970 nonzero-alpha px (max 34). An earlier run's 0.00 log line does
   NOT apply to the delivered file. The earlier refusal of the labelled
   punch file (8,420 red debug pixels, script refuses >100) stands as a
   correct refusal, not as a defect in the delivered file.
3. **PR #288 / #289 landed (253 files) — UNVERIFIED from disk.**
   The task brief states PR #288/#289 landed with 253 files. A workspace
   search found local records only for PR #286/#287 in
   `STATUS-20261031-1428.md` (292/294 = 99.3% verified on main at that
   time, with STATUS/TRACKER still owed as a micro-push). No local record
   of #288/#289 or of a 253-file verification was found in this run.
   The 253-file claim is therefore reported as **parent-supplied,
   UNVERIFIED**, and is **not** used as a verified numerator anywhere
   below. If the parent can point to the merge record, this line can be
   corrected to verified.
4. **Folder-name note.** There is no `hip-lower-20261031/` folder on
   disk. The hip-lower work lives in `reposes-v7c-clean/` (see §B) plus
   `HIP-LOWER-ANATOMY-20261031.md` and `build_hip_lower.py` at rig root.
   That is a location correction only; the work itself is counted below.

## Denominator — what 100% means here (read this first)

**100% = a show-ready pipeline AND 30 shots end-to-end, not just files
built.**

A shot counts toward 100% only when ALL of these hold for that shot:
clean (label-free) pose + final background + the lighting level recorded
in its spec + effects passes where its spec calls for them + a final
(not demo/synthesised) audio cue + Mars shot approval + delivery-frame /
safe-area conformance.

A pipeline block counts toward 100% only when it is built, viewed or
file-verified, AND (where Mars approval is the gate for that block)
approved. Built-but-unapproved work is real work — it is listed in full
in §B with approval 0/1 each — but it does **not** count as show-ready.
That is why the headline below is lower than any "files built" percentage.

**Scoring rule for the headline:** 20 show-ready blocks (§E), each scored
0–100% by its primary count (stated per block; estimates are labelled
ESTIMATE). Headline = mean of the 20 block scores. Built percentages are
given separately in §C and are NOT the headline.

## Headline — one honest percentage

**Show-ready: 855 / 20 = 42.75%, reported as 43%.**

That is NOT a claim that 43% of shots are done. Shots end-to-end are
0/30 = 0% (Block 20). The 43% is the mean of pipeline blocks, most of
which are part-built, plus a small number of fully approved blocks
(LUTs, technique index, rig joints). Any presentation that rounds this
up, drops Block 20, or substitutes a "files built" percentage for it
misrepresents this accounting.

For context only (not the headline): the same blocks scored on
built/viewed work alone, ignoring the Mars-approval gate, would be
materially higher — roughly two-thirds built. That built figure is
deliberately NOT presented as a single headline number here, because
the denominator for this task is show-ready, not built.

---

## (A) ALREADY APPROVED by Mars — approval 1/1 each (do not re-approve, do not re-open silently)

These are the approvals stated in the task brief and/or in
`STATUS-20261031-1428.md`. Approval here means Mars's approval of the
named item as shown — it does not approve neighbouring items, later
variants, or all 30 shots.

| # | Approved item | Scope / limit of the approval |
|---|---|---|
| A1 | True final flex, relaxed-clean — PERFECT | File `reposes-v7c-clean/true-final-flex-relaxed-clean-20261031.png`. The over-flex 75° full-final, the detached-fist final attempt, and the hip-lower squat variants are NOT this approval (see §B). |
| A2 | Eyes v4, in-mask fit — APPROVED | Pulled Robin (Day) eye shapes fitted to Head_Front's own mask openings, no second mask band, 0 black pixels in the v4 strips. This approves the in-mask method/fit, not every v4 expression strip as a final face, and not the strip-band overlay (which reads as a second mask rectangle). |
| A3 | JoJo v3 palettes / method — APPROVED | v3 nearest-base classification + delta remap, clamped, black outline never reassigned, as used in the gap-close-colour pose-shift sheet (BASE + TENSION + POWER + DREAM + BRIGHT PINK on the fighting pose). |
| A4 | LUTs — 70/70 = 100% | Base 30/30 + spectrum 24/24 + spectrum v2 16/16. Earlier 44/70 (at PR #286/#287 push time) is STALE — do not quote it. Clean grey-128 re-grades of the last 26 approvals are a separate rebuild if Mars wants them, not a new approval. On-disk `.cube` files total more than 70 by basename (104 unique basenames found recursively, including upgraded duplicates) — the approved set is 70, not 104. |
| A5 | Room scale — 2.5x = 100% | Room-only. Rig 950px tall, feet on floor, chair back at waist on the locked room sheet. Seated rule (standing − 0.2 → 2.3x seated) is approximate and still to be verified visually on a seated pose — it is NOT part of this approval. |
| A6 | Punch impact — −110 across-up = 100% | Locked copy `clips-v7c/punch-impact-locked-v7c.png`. The −70 across-down variant is separately approved only as a before/during/after-punch placement, NOT as the impact frame. |
| A7 | Gauntlet OutFixed — APPROVED | Per-row flip within each row's own alpha span, cuff y62–180, for arms-up / arms-in-front poses only. Regression `check_gauntlet_flip.py` 5/5 = 100%. The floating v1 flip is SUPERSEDED, do not use. A fist-mirrored variant would be a NEW piece to approve. |
| A8 | Arms-up pose / base — APPROVED | The FlexOut demo-pass pose as an arms-up pose (and as a fighting stance with arms very high, or as a pre-flex frame). It is NOT approved as a complete flex. |
| A9 | Forearm / head-34 v1 — APPROVED as v1 base | Forearm-head34 v2 construction (foreshortening 0.42x, fist 1.45x wide) and forearm-arm2-aligned method are the v1/v2 base. Later v4/v5 forearms and the head-34 v3/v3b kitbash are NOT covered by this — they are §B, approval 0/1. |
| A10 | JoJo atmosphere — APPROVED | Environment-only shift, background warm/purple, character base palette unchanged (`jojo-atmosphere-yellow-sky-20261031.jpg`). |
| A11 | JoJo bright pink tension — APPROVED | Combined golden-hour + JoJo tension, renamed BRIGHT PINK / PINK HOUR JoJo tension. The old "golden-hour" name for that file is SUPERSEDED. |
| A12 | Clean Level 2 (v1) + Level 2 v2 warm-rim — APPROVED | Clean Level 2 v1 approved; Level 2 v2 warm-rim (amber rim 255,180,80, bleed 5px/0.20) approved 15:11 CDT as "perfect exactly". The cyan-rim single-light version is NOT approved as a single-light grade — cyan rim is valid only in the dual-light case (see §D). |
| A13 | Fighting pose (renamed) + gauntlet-fixed fighting pose — APPROVED | `fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png` is the locked reference for arms-up-in-front poses. The old name "flex-hold" for this pose is SUPERSEDED. |
| A14 | JoJo colour-shift demo sheet + lighting-level demos — APPROVED | Demo sheet palettes as shown; coloured + non-coloured lighting demos. This does not approve every JoJo palette as canon for every shot — per-shot shifts still follow the shot spec / colour script. |
| A15 | Punch sequence frame −70 + flex anticipation frame — APPROVED as frames | −70 as a sequence placement (see A6); flex-anticipation / before-tighten frame as a before-flex frame. Neither is a final flex or a final shot. |

**Approved count in this section: 15 named approvals. Shots approved
as final shots: 0/30 = 0%.** No approval in §A approves a shot.

---

## (B) BUILT, unapproved — approval 0/1 each (every item below is 0% approved, however complete its build is)

Each bullet is one approval unit. "Built" means a file exists on disk
and was built/viewed or file-verified by its builder; it does not mean
Mars has seen or approved it.

### Rig / poses / pieces — built, 0/1 each
- Gap-close rig pack (necks 5/5, blank heads 5 + furious 1, feet 2/2,
  gauntlets 2/2, catalogue v2): built 100% as a pack, approval **0/1 = 0%**.
- Front-facing knuckle fist v4b + punch pose v4c (11/11 alignment QC
  pass in its own script): built, approval **0/1 = 0%**.
- True-final-flex v2 (gap-close re-implementation, relaxed spec):
  built, approval **0/1 = 0%** — distinct from the approved
  relaxed-clean file in A1; do not merge the two.
- Head-34 v3b kitbash + side-body stand-in v2 + back-body stand-in v2:
  built as labelled stand-ins/kitbash, approval **0/1 = 0%**; true
  hand-drawn masters 0/3 = 0% (3/4 head, side body, back body).
- Cape bone-chain diagram v2 + billowing cape as separate prop-rig
  layer + body-only / composite cape-pose pair: built, approval **0/1 = 0%**.
- Foreshortened forearms v2, Arm1 + Arm2 (2/2 = 100% built): approval **0/1 = 0%**.
- Forearm-fist v5 correction (forward-punch flipped + uppercut, 4/4
  pieces + proof): built, approval **0/1 = 0%**. V5 supersedes the
  upside-down Arm2 v2 fist; v3 remains classified as a palm-facing
  fist, not a punching fist.
- Hip-lower squat variants, 2/2 built (over-exaggerated + deep squat,
  hip y740 → y760, knees/feet unchanged, true final flex relaxed-clean
  untouched, md5-verified): approval **0/1 = 0% each**.
- Dance knee-feet corrected version (63 corrected frames on disk,
  before/after + contact + per-frame audit CSV): built, approval **0/1 = 0%**.
  Knee-feet rule itself is a gate, not an approval of this dance.
- Cape styles v2: 15/15 cape forms built (target was 12+): approval **0/1 = 0%**.
- Visemes v2: 14/14 heads + 14/14 patches built (mask-first method,
  OO/W before/after proof): approval **0/1 = 0%**. V1 remains REJECTED
  as hand-tooled; v2 does not inherit any v1 approval (there was none).
- Eyes v4 strips: 5/5 front expressions built (neutral, determined,
  angry, surprised, concentrating; 0 black pixels each): approval
  **0/1 = 0% as strips** — only the in-mask fit in A2 is approved.
  V1 eyes remain reclassified as COMEDIC RELIEF only.
- Device prop v2 (sheet + final-shot lap-scale proof, 10/10 methods
  claimed by its builder): built, approval **0/1 = 0%**; exact scale is
  a Mars-only decision (§D), so v2's 148px lap-scale figure is a
  proposal, not a lock.
- Model angles beyond A-scope: 3/4, side body, back body true masters
  0/3 = 0% built as masters (kitbash/stand-ins only, above).

### Colour / lighting / compositing — built, 0/1 each
- ACES 1.3 comparison (Blender Cycles, Standard vs ACES 1.3, same
  34-node/43-link tree; mean delta 25.34, max 49): built, approval **0/1 = 0%**.
  ACES 1.3 vs 2.0 like-for-like ranking: **0/1 = 0%** (different engine
  + display in the earlier 2.0 run, so no ranking is claimed).
- Room-at-2.5x Blender proof (Cycles, desk painting substituted for the
  missing KKGuh room painting; chair-back-at-waist NOT replicable on the
  substitute): built, approval **0/1 = 0%**. True KKGuh room background:
  **0/1 = 0% found on disk**.
- JoJo pose-shift sheet (4 palettes on fighting pose) + sequence colour
  script (5 beats, 216f = 9.0s at 24fps, hard-cut return rule): built
  under the approved v3 method (A3), approval of these sheets as
  shot-ready colour **0/1 = 0% each**.
- Level-3 PIL proof composites CJ-11 / CJ-19 / CJ-28 (3/3 built as PIL
  composites, explicitly NOT Blender): approval as Level 3 **0/1 = 0% each**.
  Blender (not PIL) Level-3 composites for CJ-11/19/28: **0/3 = 0%**.
- Painted-background shifted versions: TENSION + POWER only (2 palettes);
  other palettes **0% built** as painted versions. Clean painted street
  background: **0/1 = 0% found on disk** (batch-Auzjk not found).
- Background colour scripts, 4/4 scenes (room, street swatch-only,
  rooftop, alley): built as scripts, approval **0/1 = 0%**.
- Godray Level 4 candidate + gold-preserved v4/v5 variants + L4/L5 spec:
  built and viewed, approval **0/1 = 0%**; Mars's pick between gold read
  vs red read: **0/1 = 0%** (see §D).
- Blender composite wrap v4 relight (normal/depth/sideweight passes for
  apose, arms-up, fighting — 3/3 poses relit in scratch): built,
  approval **0/1 = 0%**; no wrap-v4 report file exists on disk, only
  `relight_normal_v4.py` + scratch passes.
- Wrap v3 experimental soft-on-halo variant
  (`wrap-v3-apose-exp-soft-on-halo-20261031`): built as an EXPERIMENT
  only, approval **0/1 = 0%**, and it is NOT the default stack (see §D).
- Afterglow (soft-rim-only motion trail, GIF + at-rest final frame +
  proof contact): built, approval **0/1 = 0%**. By construction it is
  motion-only: at rest the trail decays to zero, so it is not a resting
  glow.

### Sound / edit / TV — built, 0/1 each
- Edited sequences: punch 26f (1.08s) + dance beat-held sequence, 2/2
  MP4s built: approval **0/1 = 0% each**. Both use substitute plates
  for missing clean frames (punch windup/snap/recover are not new
  re-posed frames) — re-posed windup/snap/recover pass still owed
  **0/1 = 0%**.
- Sound demo mix + layer stack (dialogue / SFX / music / ambience /
  device-beep, −14 LUFS target): built as SYNTHESISED DEMO ONLY,
  approval **0/1 = 0%**; recorded/final audio **0%** (dialogue layer
  empty in the demo by its own JSON).
- Lipsync strip + timeline (sound-edit folder): built, approval **0/1 = 0%**.
- Safe-area overlay + camera-move sheet + background-consistency check
  (5/5 backgrounds PASS in its own check, layout passes 5/5 found):
  built, approval **0/1 = 0%**. Safe areas as a delivery lock are
  Mars-only (§D) — a test overlay is not an approved safe area.
- Storyboard 30-panel index + 6-panel punch storyboard + punch animatic
  (52 animatic frames on disk) + title card + credits template:
  built, approval **0/1 = 0% each**.
- EDL CJ-01..CJ-30 (30/30 entries, 332 frames total at 24fps, cuts only):
  built as a document, approval **0/1 = 0%**. Thumbnail status inside
  it: CLEAN POSE 20/30 = 67%, POSE PENDING 9/30 = 30%, NEW DIALOGUE
  COMPOSITE 1/30 = 3%.
- Principles matrix CJ-01..CJ-30 (30/30 as a matrix assignment):
  built, approval **0/1 = 0%**; visual proof inside it is 1/30 = 3%
  (CJ-01 only, reused sheets) — CJ-02..CJ-30 are assignments/gates,
  not visual proof.
- QC CJ-01..CJ-30: 27/30 PASS = 90%, 3/30 FAIL = 10% (CJ-05, CJ-06,
  CJ-26, all on the neutral-key rim-hue check, recorded as
  UNVERIFIABLE, not as hue mismatches). QC pass is not Mars approval:
  Mars shot approval remains **0/30 = 0%**.
- Effects wiring map: 12 systems total — wired 4/12 = 33%, proposed
  5/12 = 42%, unwired 2/12 = 17%, gate 1/12 = 8%. Shots with at least
  one wired system 10/30 = 33%; shots with no wired system 20/30 = 67%.
  Approval of the map/wiring as final: **0/1 = 0%**.
- Critique-learning log: 13 critique entries (C-01..C-13) logged with
  gates: built as a log, approval **0/1 = 0%** — a log entry is not an
  approval of the fix it describes.

---

## (C) BUILT in this accounting run vs STILL OWED

"This accounting run" = the recomputation itself plus the newer folders
it re-counted (gap-close-rig / colour / sound-edit / tv,
gap-audit-critique-log, wrap-v4, godray-level4, afterglow, hip-lower,
fist-v5-correction, dance-kneefeet-fix-correction, eyes-v4). This run
built no new art and pushed nothing; it re-verified and re-counted.
"Built in this run" below therefore means "verified present in the
newer folders counted by this run", not "created by the accounting
script".

### Built (verified present in the newer folders) — with built %
- Gap-close rig pack: built 100% as a pack (see §B counts).
- Gap-close colour: ACES 1.3 pair + comparison 100% built; room-2.5x
  Blender proof 100% built on a substitute background (see §B limit);
  JoJo pose shifts 100% built (4 palettes on 1 pose); sequence script
  100% built; Level-3 PIL composites 3/3 = 100% built as PIL;
  painted shifted versions 2 palettes built, remainder 0%.
- Gap-close sound-edit: edited sequences 2/2 = 100% built; sound stack
  + demo mix 100% built as demo; lipsync strip/timeline 100% built;
  background-consistency check 5/5 = 100% checked (own check).
- Gap-close TV: EDL 30/30 = 100% built as a document; QC 30/30 =
  100% checked (27 pass / 3 fail); storyboard index 30 panels +
  punch 6 panels 100% built; animatic punch 100% built (1 sequence);
  principles matrix 30/30 = 100% built as a matrix (visual proof
  1/30 = 3%).
- Critique log: 13/13 entries present as a log.
- Wrap v4: relight passes for 3/3 poses present in scratch (apose,
  arms-up, fighting); wrap-v4 report 0/1 = 0% present.
- Godray Level 4: candidate + gold-preserved v4/v5 + proof sheet
  100% built as candidates; L4 approval 0%.
- Afterglow: GIF + at-rest frame + proof contact 100% built as a
  motion-only demo.
- Hip-lower: 2/2 squat variants + before/after + leg crops present in
  `reposes-v7c-clean/`.
- Fist v5 correction: 4/4 pieces + proof present.
- Dance knee-feet correction: 63 frames + audit CSV present.
- Eyes v4: 5/5 strips + in-mask proof + angle sheet + face-top proof
  present; in-mask fit approved (A2), strips unapproved (§B).

### Still owed — every list below carries its percentage
- Shots end-to-end (all gates in the denominator): **0/30 = 0%**.
- Shots through the compositor stack (wired inventory + clean-100):
  **4/30 = 13%** (CJ-01, CJ-19, CJ-28, CJ-30, plus a flying painted-bg
  shot counted separately in the wired inventory, not as a fifth
  CJ shot); remaining **26/30 = 87%**.
- Shots with Mars approval: **0/30 = 0%**.
- Clean clip re-render: **0/17 clips = 0%** (labelled clips-v7c are
  DEBUG ONLY; clean-100 exposure clips are pose frames, not clean
  clip re-renders).
- Clean-slice batch: **0/184 unique branch sheets = 0%** as a batch
  (method 100%, single-sheet use 1 sheet, eye-view pass on sliced
  sheets still owed — wired item 38). The `sliced-clean` results JSON
  records piece counts per source sheet; it is not a batch delivery.
- JSFL run in real Adobe Animate: **0/1 = 0%** (Animate not on this VM;
  static v8 JSFL + timeline template exist only).
- Final painted backgrounds: **0/4 = 0%** (flying, rooftop, alley,
  desk — stand-in batch backgrounds and layout passes exist, finals
  do not). Layout passes themselves: **5/5 = 100%** found (4 painted
  + room).
- True hand-drawn masters: **0/3 = 0%** (3/4 head, side body, back body).
- Per-shot god-ray placement decisions: **30/30 = 100% decided**
  (9 Level-3 placements + 21 explicit Level-2 no-god-ray decisions) —
  decisions are not renders; Level-3 renders for those 9 shots are
  **0/9 = 0% as Blender renders** (PIL proofs exist for 3 of the 9).
- Per-shot tuning of Level 2 v2: **0/30 = 0%**.
- Per-shot LUT file paths made specific: CJ-09/CJ-10/CJ-16/CJ-17/CJ-21
  still carry a directory path instead of a specific `.cube` file in
  the QC notes — **5/30 = 17% of shots** need that fix before final
  delivery (LUT names themselves are in the approved 70 set, so this
  is a path fix, not a re-approval).
- Recorded/final audio: **0%** (cue sheet v2 + demo only; loudness
  measured on demo/wired audio only, not on final cues).
- Viewed Blender render as a final shot (as distinct from Blender
  proof/comparison renders): **0/30 = 0%** as final shots; Blender
  proof renders exist for ACES, room-2.5x, and wrap/godray tests.
- Comparison tests (use + learn + reverse-engineer + wire + test
  loop): **0/7 = 0% run** (Harmony/Animate trial-dependent tests
  pending; our side ready for tests 1/3/4/6 per STATUS, but readiness
  is not a run test).
- Opposition pair demo: **0/1 = 0%** (needs an antagonist plate).
- Flex clip retarget (Darwin dance → Cape Jones): **0/1 = 0%**.
- RAR5 full-leak walk (Gumball 86 parts): **0/1 = 0%**.
- Nick / Disney / PPG full downloads: listings only, **0% downloaded
  as full sets** in the counts verified here.
- Repo landing for this accounting run: **0 files verified on main
  by this run = 0%**; PR #288/#289 (253 files) is UNVERIFIED (§
  Corrections). Do not present local-folder presence as main-branch
  presence.

---

## (D) MARS-ONLY decisions — never to be silently decided

Each item below is approval **0/1 = 0%** until Mars decides it.
Builders may propose, label, and show variants; a proposal is not a
decision, and a variant file is not a lock.

1. **Delivery frame size + safe areas: 0/1 = 0%.** Character canvas
   1100×1500 is the rig default, NOT a delivery frame size. The
   delivery spec itself states frame size and safe areas are still to
   be set by Mars. The gap-close safe-area overlay is a test, not a lock.
2. **Canonical room ID: 0/1 = 0%.** Which room painting is canonical
   (KKGuh batch file not found on disk) and its palette are undecided.
   The room-2.5x Blender proof uses a desk-painting substitute and
   does not decide this.
3. **Parts-audit exceptions, 6: 0/6 = 0% decided.** Listed in
   `PARTS-LABEL-AUDIT-20261031.md` as pending Mars's decision, with
   9 mislabels corrected and 5 rejects / 8 missing-part groups
   alongside them. No exception is granted by this accounting.
4. **Device prop v2 exact scale: 0/1 = 0%.** V2 proposes lap scale
   (≈148px wide in the 1168px room shot, per its builder) against a
   v1 that read as furniture (≈295px vs ≈260px seated figure). The
   exact locked scale is Mars's, not the builder's.
5. **Dual-light V3 vs V4 pick: 0/1 = 0%.** Variants built: v1 gold-rim
   only, v2 cyan-rim + gold LUT, v3 gold-inner/cyan-outer, v4
   cyan-inner/gold-outer, v5 mixed silhouette (7 JPG variants on
   disk). Mars picks the rim order; the dual-light correction (cyan
   backlight only when cyan rim combines with the gold LUT/overlay;
   gold rim alone gets NO cyan backlight) is a rule, not a pick.
6. **L3 / L4 approval: 0/1 = 0% each.** L3 PIL composites are not L3
   approval; L4 candidate and gold-preserved variants are not L4
   approval; the gold-read vs red-read pick is Mars's.
7. **Soft-on-halo experimental: 0/1 = 0%, experimental only.**
   Soft rim and soft halo are the SAME single layer in Mars's usage
   (corrected 17:05 CDT); the L4 double layer is hard rim + that one
   soft layer. A soft-on-soft test is an experimental variant, never
   the default stack, unless Mars says otherwise.
8. **Seated scale interpretation: 0/1 = 0% verified.** 2.5x → 2.3x
   (subtract 0.2) is the stated approximate rule; if the seated visual
   reads as a 20% reduction (→ 2.0x), that is a correction to log,
   not a silent change.
9. **Neutral-key rim rulings (CJ-05, CJ-06, CJ-26): 0/3 = 0% ruled.**
   QC fails them as UNVERIFIABLE (neutral key / white or grey rim,
   hue N/A by design), not as hue mismatches. Whether the neutral
   exception counts as a dual-light-style exception is Mars's ruling.
10. **JoJo canon per shot, spectrum/v2 grey-128 re-grades, and any
    per-shot LUT/rim/power override: 0% decided beyond §A.** The
    approved LUT set and the approved v3 method do not decide a given
    shot's shift, trigger, or return — the shot spec / colour script
    must record it, and Mars approves the shot.
11. **Goodville repo identity, Toon Boom / Animate purchase, and any
    repo push target: 0% decided in this run.** No push was made and
    no guessed repo is named as a target here.
12. **Any approval not listed in §A: 0%.** In particular, no shot,
    no viseme set, no cape style, no dance, no device, no L4 variant,
    and no gap-close folder as a whole is approved by implication
    from a neighbouring approval.

---

## (E) The 20 show-ready blocks behind the headline (arithmetic)

| # | Block | Primary count used | Show-ready score |
|---|---|---|---|
| 1 | Rig & joints | Pivots 4/4 = 100%, clean poses 6/6 = 100%, gauntlet regression 5/5 = 100% | 100% |
| 2 | Clean-cut batch | Batch 0/184 = 0% (method exists, batch does not) | 0% |
| 3 | Poses & model angles | Angles 2/5 = 40% (true masters 0/3) | 40% |
| 4 | Clips & timeline | Clean re-render 0/17 = 0%, edited sequences built with substitutes — ESTIMATE | 12% |
| 5 | Symbols / JSFL / tools | JSFL run in Animate 0/1 = 0% | 0% |
| 6 | Shot specs & QC | QC 27/30 = 90% (specs 30/30 and god-ray decisions 30/30 are documents, QC is the check) | 90% |
| 7 | Technique library index | Stage order + shot types + methods pulled, no characters | 100% |
| 8 | Asset manifest / repo landing | Snapshot exists; PR #288/#289 UNVERIFIED — ESTIMATE, not verified | 50% |
| 9 | Backgrounds & layouts | Layout passes 5/5 = 100%, final painted backgrounds 0/4 = 0% — mean | 50% |
| 10 | Visemes | Built 14/14 = 100%, approved 0/1 = 0% — show-ready counts approval | 0% |
| 11 | Eyes | In-mask fit approved 1/1, strips unapproved — ESTIMATE (method approved, set not final) | 50% |
| 12 | Cape styles | Built 15/15, approved 0/1 = 0% — show-ready counts approval | 0% |
| 13 | Colour / LUTs | Approved 70/70 = 100% | 100% |
| 14 | Lighting / compositing | L2 approved, shots through stack 4/30 = 13%, L3/L4 unapproved — ESTIMATE | 38% |
| 15 | Effects | Wired systems 4/12 = 33% | 33% |
| 16 | Audio | Cue sheet built, recorded/final audio 0% — ESTIMATE | 50% |
| 17 | Storyboard / animatic / EDL / principles | Documents 30/30, visual proof 1/30 = 3% — ESTIMATE | 50% |
| 18 | Delivery | Spec document built, frame size 0/1, safe areas 0/1 — 1/3 | 33% |
| 19 | Wired-100 pipeline | Wired 24/41 = 59% | 59% |
| 20 | Shots end-to-end (all gates) | Approved final shots 0/30 = 0% | 0% |

**Sum = 100+0+40+12+0+90+100+50+50+0+50+0+100+38+33+50+50+33+59+0
= 855. 855 / 20 = 42.75% → 43% show-ready.**

Blocks marked ESTIMATE (4, 8, 11, 14, 16, 17) are judgement means of
the counts stated in their rows, not fresh counts. Changing any one
estimate by ±10 points moves the headline by only ±0.5 points, so the
headline does not hinge on any single estimate — it hinges on Blocks
2, 5, 10, 12 and 20 being 0%, which are counts, not estimates.

## What would move the headline honestly

- A Mars shot approval moves Block 20 only when the shot passes ALL
  denominator gates; a single approved pose does not move Block 20.
- A Mars decision in §D moves the affected block only (e.g. frame
  size moves Block 18; a dual-light pick moves Block 14's variant
  choice, not its shot-through-stack count).
- A verified PR #288/#289 merge record would move Block 8 from
  ESTIMATE 50% to a verified figure and remove the UNVERIFIED flag —
  it would not by itself move Block 20.
- Finishing the clean-slice batch (0/184 → 184/184) or the clean clip
  re-render (0/17 → 17/17) would move Blocks 2 and 4 respectively, by
  their counts, not by assertion.

## Sources re-checked for this run (no other sources used for counts)

- `FULL-PRODUCTION-ACCOUNTING.md` — stale, not quoted as current.
- `wired-100-20261031/WIRED-INVENTORY-20261031.md` — 24/41 = 59%,
  CJ-01 rim/bleed correction as above.
- `gap-close-rig-20261031/GAP-CLOSE-REPORT-20261031.md`
- `gap-close-color-20261031/GAP-CLOSE-COLOR-REPORT-20261031.md`
- `gap-close-sound-edit-20261031/` (edited-sequences, sound-layer-stack,
  effects-wiring-map, background-consistency-check JSON/MD)
- `gap-close-tv-20261031/` (EDL, QC JSON/MD, principles matrix,
  storyboard/animatic files on disk)
- `gap-audit-critique-log-20261031/CRITIQUE-LEARNING-LOG-20261031.md`
  (13 entries)
- `blender-composite-wrap-v4-20261031/` (script + scratch passes, no report)
- `godray-level4-20261031/LEVEL-4-5-SPEC-20261031.md`
- `afterglow-20261031/build_afterglow.py` + outputs
- `reposes-v7c-clean/` hip-lower files + `HIP-LOWER-ANATOMY-20261031.md`
- `forearm-fist-v5-correction-20261031/README-V5-CORRECTION.md`
- `dance-kneefeet-fix-correction-20261031/CORRECTION-REPORT-20261031.md`
- `eyes-normal-superhero-v4-20261031/EYES-V4-REPORT-20261031.md` + manifest
- `clean-100-20261031/shots/` (shot specs 30, god-ray placement 30,
  delivery spec), `STATUS-20261031-1428.md`, `TRACKER-20261031.md`,
  `PARTS-LABEL-AUDIT-20261031.md`, `device-prop-v2-20261031/`,
  `dual-light-variants-20261031/`.

*End of accounting — 2026-10-31. Next recomputation must re-verify
every count from disk again; do not carry these percentages forward
without re-checking.*
