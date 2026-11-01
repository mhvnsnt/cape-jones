# WORKSTREAM B SWEEP — TV PRODUCTION READINESS — 2026-10-31

Folder: `workstream-b-sweep-20261031/` (this folder only, plus the audited
source folders it cites). No repo push. No deletions of any Mars-seen file.
One internal rename only: an unshown NMP-01 draft still was renamed to its
superseded name (see §4), never deleted, never shown to Mars.

Focus change applied (Mars 2026-10-31 20:53 CDT): this report is ordered by
TV PRODUCTION READINESS. §1 = what blocks episodes/segments (shots
end-to-end, per-shot movement proofs). §2 = additives/extras (further pose
variants, NOT blockers). §3–§5 = the evidence behind both. Nothing in §2 is
counted as closing a §1 gap, and nothing in §1 is padded with §2 items.

Ground rule applied (Mars 2026-10-31 20:56 CDT, not re-decided):
AIRBORNE = flying, floating, levitating, JUMPING, fight-motion-off-ground,
chase-airborne — labelled AIRBORNE with a stated height/flight line, feet
NOT forced to ground. Walking/standing = GROUNDED-default, feet planted;
a grounded proof that floats FAILS the gate. No grounded floating is
excused as "airborne". Every proof in this sweep carries its label in §5.

Stills approved ≠ videos approved. That rule is applied to every count
below: a still's approval never counts as its video's approval.

---

## 1. PRODUCTION GAP — what blocks episodes/segments

### 1a. Shots end-to-end (the 30 CJ shots)

| Measure | Count | % |
|---|---|---|
| CJ shots in shot-specs-30 | 30 | — |
| Shots with a movement file on disk (afterglow CJ-01..30 GIF+MP4) | 30/30 | 100% |
| Shots Mars-approved (shot-specs file itself: "NONE claimed… all PENDING") | 0/30 | 0% |

Existence is not approval. The 30/30 files are proofs awaiting Mars's look,
not approved shots. This workstream does not approve shots; it supplies
movement proofs toward them.

### 1b. Pose-to-pose movement chains the shots need (rig-angle proofs)

Shots need movement, not just stills. The 30 shots group into 6 movement
chains. A chain counts as PROVEN only when a rig-angle (not image-interp)
version exists AND is Mars-approved. Partial = rig version exists, unapproved
or caveated.

| Chain | Shots | Rig-angle proof | Status |
|---|---|---|---|
| Punch chain | CJ-01..05 | punch-to-flex v2 (punch→fight→flex) | PARTIAL — 0/1 approved, punch+fight measured-estimates, flex 28px dip missing |
| Walk cycle | CJ-06..08 | none in this workstream | OWED — DEPENDENCY: coming-forward walk layer fix running separately, NOT duplicated here; walk proofs must pass the grounded gate after that fix |
| Dance chain | CJ-09..11 | none (image-interp dance videos only) | OWED |
| Flying chain (AIRBORNE) | CJ-12..15 | none (clip/afterglow playback only) | OWED |
| Flex/fight chain | CJ-16..20 | punch-to-flex v2, partial (see punch chain) | PARTIAL (same proof, counted once) |
| Jump chain (AIRBORNE) | CJ-21..22 | none as rig; jump-to-shimmy rig re-key | BLOCKED on Mars (see §6) |

- Complete rig-angle chain proofs: 0/6 = 0%.
- Partial rig-angle chain proofs: 1/6 = 17% (punch-to-flex v2).
- Chains with no rig-angle proof at all: 5/6 = 83%.

### 1c. Rig-angle successors to the 9 poses-as-movements videos

- Movements with a rig-angle successor: 3/9 = 33% (serve-to-guard v2+v3,
  punch-to-flex v2, rollcall-snap-to-spread v2 — all 0/1 approved).
- Movements with NO rig-angle successor: 6/9 = 67% (jump, jump-clean,
  shimmy, ginyu-force, pose-dialects, jump-to-shimmy).
- Video approvals across all versions: 0/12 = 0% (9 v1 image-interp + 3 v2
  rig; v3 is a 13th video, also 0/1 — see §3).

### 1d. Production-gap summary (this workstream's scope)

- Shot approvals: 0/30 = 0%.
- Complete rig chain proofs: 0/6 = 0%.
- Serve-to-guard rig final (v3, §3): delivered, approval 0/1.
- Jump-to-shimmy rig: 0/1, BLOCKED on Mars say-so — NOT built (§6).
- The single biggest production lever in this workstream is NOT new poses:
  it is Mars decisions on the proofs already delivered (v3, v2s, 30 shot
  files) plus the two running dependencies (walk fix, invisible-power
  no-crop fix). New poses (§2) close 0% of the gap above by design.

---

## 2. ADDITIVES / EXTRAS — NOT blockers (do not count toward §1)

| Additive | Built | Approved |
|---|---|---|
| 4 new movement poses (§4) | 4/4 = 100% | 0/4 = 0% |
| Pseudo-turn variant templates verified (§5) | 7/7 gate PASS = 100% | pack 0/1; base-as-dance-move 1/1; other 6 templates 0/6 as Mars approvals |
| Poses-as-movements v1 interim videos (proofs, not finals) | 9/9 exist = 100% | 0/9 = 0% as videos |

Verification ≠ approval, everywhere in this report. A gate PASS means the
file measures clean on the stated check; it does not mean Mars approved it.

---

## 3. SERVE-TO-GUARD v3 — PRODUCTION movement (new, rig-angle)

Files: `move-serve-to-guard-v3-20261031.gif` / `.mp4`,
`move-serve-to-guard-v3-20261031-contact-20261031.png` (VIEWED),
`move-serve-to-guard-v3-20261031-xsheet-20261031.csv`,
`frames/serve-to-guard-v3/` (55 transparent masters),
`serve-to-guard-v3-20261031.json`, `serve-to-guard-v3-ghost-20261031.json`,
builder `build_sweep.py` + `rebuild_v3.py`.

- 55 frames @24fps = 2.29s. GROUNDED: feet planted, vertical translation
  0 on every frame (gated, asserted in the builder).
- Sequence: apose hold 3 → serve (7 inbetweens) → serve hold 5 → guard
  (7) → guard hold 5 + overshoot + settle → fight (7) → fight hold 5 +
  overshoot + settle → apose return (7) → apose hold 3.
- Method, plainly: EVERY frame is a fresh render through snap.figure
  (the face-cowl-snap-wire100 builder, real snap passes). NO whole-picture
  blending, NO crossfade anywhere. Easing easeInOutCubic (industry
  slow-in/slow-out). TWO labelled breakdowns per transition (arc bulge
  +10° on the largest-moving arm upper at j=3; follow-through +8° on that
  arm's lower at j=5). Overshoot 5% beyond key + settle are REAL frames.
  Snap union per inbetween, priority face > cowl > chest > normal.
- How v3 improves on v2 (not just "v3"): v2 used its own simplified
  builder with a top-arm UNION approximation, not snap.figure passes;
  v2 had ONE breakdown per transition and smoothstep easing; v3 uses the
  real snap builder, easeInOutCubic, TWO breakdowns, and a union-canvas
  no-crop frame (788×1148, edge alpha 0, gated) instead of v2's fixed
  1100×750 video frame.
- Keys: serve JEI-01 and guard GUL-03 are Ginyu-builder exact. Fight is
  STILL a measured estimate ±15° — v2's caveat is NOT fixed here, because
  no builder-exact fight config exists on disk. Replacing it needs a
  measured config from the approved fighting file or a builder-exact
  config; that is still-owed agent work, not silently swapped.
- Snap status, stated exactly: fight = NONE (recovered gate: PASS, NO SNAP
  both sides, eye-check "fists near head, not over face; elbows out" —
  an earlier draft of this build used chest for fight and was CORRECTED
  to the recovered gate before delivery). Serve L cowl and guard L/R
  chest are ASSIGNED (Ginyu builder top + COWL-SNAP upper-only rule;
  guard arms cross the torso), NOT gate-verified — snap check still owed
  for serve/guard. Face > cowl > chest priority held in every inbetween.
- Ghost measurement (same method as v2's measure_ghost.py; v3 mid =
  serve→guard arc-breakdown frame f19; serve key f12, guard key f26):
  double-edge ratio 1.05 (≈ one figure; v1 1.32, v2 1.01 quoted from the
  v2 report), wash 17.5% (v1 96.2%, v2 17.2% quoted). Absolute pixel
  counts are NOT comparable across versions (v3 masters are full-res,
  356,707px silhouette; v2 measured 550×750 video frames) — only the
  ratios are compared. Residual wash is solid different-colour pieces at
  boundaries (e.g. black cape where the key had white suit), not a
  second figure; the viewed contact shows one solid figure per frame.
- Approval: v3 0/1. NOT claimed approved or landed.
- Approval wording conflict, flagged not resolved: the poses-as-movements
  report says all its videos are 0/1, while the interp-v2 report says
  "v1 stays APPROVED as-is". This sweep counts serve-to-guard video
  approval as 0/1 for v2/v3 and does NOT treat the v1 wording as a video
  approval; the parent should confirm with Mars which reading is right.
- Timing chart: the xsheet CSV lists all 55 frames (kind, from/to, t,
  eased value, note). Contact tiles: f00 apose KEY, f13, f27 guard/fight,
  f41, f54 apose KEY (VIEWED).

## 4. FOUR NEW MOVEMENT POSES — ADDITIVES (new, distinct, rig-angle)

Each: apose → pose → apose rig movement (27 frames @24fps = 1.13s,
7 inbetweens per transition, 2 breakdowns, overshoot+settle, GROUNDED,
no-crop edge 0, xsheet). Key still (transparent + grey view) + GIF + MP4
+ contact per pose; combined contact
`new-movement-poses-4-contact-20261031.png` (VIEWED). Approval 0/4.

| Pose | Angles (au/al/lu/ll, L/R) | Snap | Distinct from (checked against 18 Ginyu + 8 dialect + flex/fight/punch/jump/walk/fly/dance/seated stills) |
|---|---|---|---|
| NMP-01 HERO-LAND CROUCH | au (30,-70), al (20,60), lu (-35,60), ll (20,-40), head 8 | L chest | Not jump-land (arms-up), not gul-01 compact crouch (symmetric, both hands out) |
| NMP-02 SKY-POINT SALUTE | au (-170,60), al (10,120), lu (-15,25), ll (10,-10), head -12 | none | Not jei-03 side-point (sideways), not cap-01 entrance |
| NMP-03 PROWL STEP | au (-90,40), al (30,90), lu (-70,30), ll (70,-20), head 6 | L chest | Not gul-02 focus (symmetric hands out), not bur-01 dash (upright lean) |
| NMP-04 OVERHEAD SMASH WINDUP | au (-170,170), al (20,-20), lu (-45,45), ll (30,-30), head 6 | none | Not cap-02 spread (arms sideways), not flex (arms bent at sides) |

- NMP-01 CORRECTION, stated plainly: the first NMP-01 angle set
  (lu -75/60, ll 80/-50) read as a tucked-foot crouch — one foot off the
  ground line. That version is superseded (still preserved as
  `nmp-01-hero-land-crouch-key-still-v1-tucked-foot-superceded-20261031.png`,
  movement rebuilt, never shown to Mars). The delivered NMP-01 uses
  lu (-35,60), ll (20,-40): braced land, BOTH feet planted (viewed).
- NMP-03 foot note: it is a MID-STEP pose — one foot is raised because
  that IS the step. The figure is not floating (translation 0, anchored
  to the ground line); the raised foot is the step itself, not a
  grounded-stance failure. It is labelled mid-step, not a planted stance.
- NMP-02/NMP-04: both feet planted (viewed).
- These 4 are ADDITIVES. They close 0% of §1. They are not re-labels:
  each is a new rig angle set with its own movement video, not a renamed
  existing pose.

## 5. AUDIT + VERIFICATION (labelled, not approved)

### 5a. Poses-as-movements v1 — 9 videos, IMAGE-interpolation, NOT rig-angle

MP4 frame counts by ffprobe (authoritative; GIF view copies can drop
identical hold frames). Total on disk 458 frames including the clean
jump rebuild (the source report's "420" counts 8 videos, excluding the
clean rebuild's 38 — both numbers are stated so the difference is visible).

| Video | Frames | Method | Ground label | Note |
|---|---|---|---|---|
| jump-cowl-snap-movement | 46 | image-interp (crossfade + translation) | AIRBORNE — apex +100px over ground line; flight line crouch→takeoff→apex→tuck→land | DEFECT: baked-in red debug label dots — use clean version |
| jump-cowl-snap-movement-clean | 38 | image-interp | AIRBORNE — apex +100px; same flight line | CLEAN (no debug dots) — the jump to show |
| shimmy-cowl-snap-movement | 70 | image-interp (crossfade + sway) | GROUNDED | hips ±40px, ±3°, 2 cycles; mid-blend ghost — honest limit |
| ginyu-force-movement | 64 | image-interp | GROUNDED | roll-call order Recoome/Burter/Jeice/Guldo/Captain/spread |
| pose-dialects-movements | 108 | image-interp | GROUNDED | all 8 dialect poses, neutral between each; stand pairs aspect-preserved |
| move-punch-to-flex | 33 | image-interp | GROUNDED | punch → fight → flex |
| move-jump-to-shimmy | 33 | image-interp | MIXED: AIRBORNE land → GROUNDED shimmy | land, shimmy, shimmy (shimmy twice); rig re-key BLOCKED (§6) |
| move-serve-to-guard | 33 | image-interp | GROUNDED | serve → guard → fight; rig successors v2, v3 |
| move-rollcall-snap-to-spread | 33 | image-interp | GROUNDED | entrance → crossed command → spread; rig successor v2 |

Video approvals: 0/9 = 0%. Stills approved ≠ videos approved.

### 5b. Movements-interp-v2 — 3 videos, rig-angle (v2 builder), 0/3 approved

serve-to-guard v2: 43f; punch-to-flex v2: 41f; rollcall v2: 41f (ffprobe).
Caveats carried from the v2 report, not hidden: punch+fight measured
estimates ±15°, flex 28px dip not applied, v2 used the simplified builder
(not snap.figure) — which is exactly what v3 (§3) improves on for
serve-to-guard only. Punch-to-flex v2 and rollcall v2 have NO v3 yet.

### 5c. Pseudo-turn pack — 7/7 verified (gate), approvals split

Verified from the existing transparent masters (no re-render):
frame counts, GIF frames, MP4 presence, canvas, edge alpha. All 7:
edge alpha 0 → no-crop union-canvas gate PASS. Combined contact
`pseudo-turn-7-verified-contact-20261031.png` (VIEWED; contact tiles are
uniformly scaled for sheet layout, so per-tile aspect is NOT preserved
in the contact — the GIF/MP4 masters themselves are undistorted).

| Template | Masters | GIF | Canvas | Gate | Mars approval |
|---|---|---|---|---|---|
| pseudo-turn (BASE) | 13 | 13 | 652×1110 | PASS | 1/1 AS DANCE MOVE ONLY (see below), pack 0/1 |
| stretch-power | 13 | 13 | 512×1526 | PASS | 0/1 |
| thin-power | 13 | 13 | 512×1156 | PASS | 0/1 |
| invisible-power (original template) | 17 | 17 | 512×1104 | PASS | 0/1 |
| cheat-turn-a-depth-dark | 13 | 13 | 652×1108 | PASS | 0/1 |
| cheat-turn-b-bend-mirror | 13 | 13 | 652×1110 | PASS | 0/1 |
| sheet-animated-turn-attempt | 15 | 15 | 512×1110 | PASS | 0/1 |

- Base-as-dance-move: SQUAT SQUAT SHUFFLE OOGA BOOGA THREE QUARTER TURN
  AND THEN FORWARD FACE, approval 1/1 for that base AS A DANCE MOVE only
  (Mars 2026-10-31 20:39 CDT). It does NOT approve the whole pack (0/1),
  and it does NOT make the base a true turn: it is a 3/4 out-and-back
  cheat, not a full turn, not a true side view. True side torso/head
  piece and true hand-drawn turn master remain owed separately (0/1 each).
- INVISIBLE-POWER distinction, stated plainly: this verification's
  union-canvas gate PASS does NOT clear the outline-halo cut defect
  found by the separate invisible-power V1 no-crop fix workstream
  (outline trimmed to the figure bbox before the union canvas, halo
  sliced flat). That fix is running separately and is NOT duplicated
  here; this sweep's PASS covers the union canvas only, and the fixed
  V1 (not the original template) is the V1 candidate. Do not quote this
  verification as clearing the halo cut.
- Per-pose application of the templates: still owed — templates are
  parameterised for any angle set, but only the apose base was rendered
  in the pack (0/N poses beyond base, not counted as a percentage
  because N is unbounded; the owed item is "apply to the poses Mars
  picks", not a fixed count).

---

## 6. STILL OWED + BLOCKED ON MARS (percentages on every unfinished list)

BLOCKED ON MARS (do not build without his say-so):
- Jump-to-shimmy rig re-key: 0/1. Its v1 land key is a rendered clip
  frame with no builder config on disk, and its sequence repeats shimmy
  twice. Re-keying (apose→shimmy through the rig builder) changes the
  sequence. NOT built in this sweep, as instructed.
- Serve-to-guard v3 approval: 0/1 (Mars's look).
- New poses approval: 0/4 = 0%.
- Pseudo-turn pack approval: 0/1 (base-as-dance-move 1/1 does not cover it).
- Shot approvals: 0/30 = 0%.

STILL OWED (agent work, not Mars-blocked):
- Rig-angle versions for 6/9 v1 movements (67%): jump, jump-clean,
  shimmy, ginyu-force, pose-dialects, jump-to-shimmy (the last also
  Mars-blocked above — both labels apply).
- Rig chain proofs: complete 0/6 (0%), partial 1/6 (17%).
- v3 equivalents for punch-to-flex and rollcall: 0/2 = 0% (snap.figure
  rebuilds with the v3 method; fight/punch estimates and flex dip
  caveats carry until fixed).
- Builder-exact fight config (or measured config from the approved
  fighting file): 0/1. Until then every rig fight key stays a
  measured estimate ±15° and must stay labelled.
- Flex 28px dip parameter in the rig builder: 0/1 (rig flex reads ~28px
  taller than approved flex until added).
- Serve/guard snap gate checks: 0/2 (assigned, not verified — §3).
- True side torso/head piece: 0/1; true hand-drawn turn master: 0/1.
- Per-shot movement proofs to Mars-approval: 0/30 = 0% (files exist
  30/30, approvals 0/30).
- Per-shot lip-sync, audio, storyboards, QC: OUTSIDE this workstream's
  scope — not counted here, not claimed.

DEPENDENCIES (running separately, NOT duplicated here):
- Coming-forward walk layer fix (walk shots CJ-06..08): running
  separately; walk movement proofs in this sweep are not rebuilt.
- Invisible-power V1 no-crop fix: running separately; the original
  template is verified here only for its union canvas (§5c).

INCIDENT LOG (not hidden): the first full build run of this sweep
(build_sweep.py, v3 + 4 poses in one process) died mid-render with no
new-pose output and no surviving process (likely memory pressure: it
held all 55 v3 frames while rendering poses, alongside a concurrent
v3 rebuild). No file was lost: v3 had already been rebuilt separately
with the corrected fight snap, and the 4 poses were then rebuilt
separately, one at a time with memory released between poses
(build_new_poses.py, 27 frames each, all delivered). If a future run
combines sequences, build one sequence per process.

## Files delivered this sweep (all in workstream-b-sweep-20261031/)

- move-serve-to-guard-v3-20261031.gif / .mp4 / -contact / -xsheet
  (VIEWED), frames/serve-to-guard-v3/ (55 masters)
- nmp-01/02/03/04-*-movement-20261031.gif / .mp4 / -contact / -xsheet,
  *-key-still(-grey)-20261031.png, frames/nmp-*/ (27 masters each),
  new-movement-poses-4-contact-20261031.png (VIEWED)
- pseudo-turn-7-verified-contact-20261031.png (VIEWED)
- serve-to-guard-v3-20261031.json, serve-to-guard-v3-ghost-20261031.json,
  new-poses-20261031.json, verification-audit-20261031.json
- Builders: build_sweep.py, rebuild_v3.py, build_new_poses.py,
  measure_ghost_v3.py, verify_templates.py
- This report: WORKSTREAM-B-REPORT-20261031.md

Approval claimed by this sweep: NONE. Everything new is 0/1 unless Mars
already approved it (only the dance-move base, 1/1 as a dance move).
No repo push. No file Mars has seen was overwritten.
