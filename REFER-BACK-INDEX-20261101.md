# REFER-BACK INDEX — CHECK BEFORE EVERY FUTURE BUILD, 2026-11-01

Mars, 2026-11-01 16:29 CST: land it, remember it, refer back to the
research, study materials, and tools constantly. No regression.
This file is the standing checklist. A build that contradicts a
locked rule below is wrong even if it renders, and must be rebuilt
from the locked source, not patched on the finished image.

## Locked rules — check these FIRST, every build

1. ARM-FRONT-SNAP, AUTOMATIC, SOONER (locked perfect 1/1, 2026-11-01
   16:20 CST): when arms/forearms/fists cross the torso/chest
   threshold, the whole arm chain (upper + lower + elbow cap + fist)
   snaps to the layer ABOVE the torso, per arm, per frame.
   Blender motion: snap ON at f13 arms-out, BEFORE any crossing,
   held every frame f14–f36, snap OFF only at f37 when arms are
   clear. Snap Z 0.11, torso 0.08, head 0.12. Chest stack:
   torso < arm < head. Face stack: torso < head < arm.
   Old failure: snap only at f25 peak let the torso eat arms
   from f14. Never return to a peak-only snap.
   Source: blender523-motion-snap-lock-study-20261101/
   LOCK-RECORD-20261101.md, SNAP-SOONER-DEFAULT-20261101.json,
   motion_template.py, CHECKLIST-20261101.md.
2. KNEE-FEET, UNIVERSAL (2026-11-01 12:07 CST): knees direction ==
   toes direction, per frame, both legs. Knees inward => toes
   inward. Knees outward => toes outward. Exception ONLY when Mars
   names a specific pose as an exception. The 11:30 leg1/leg2
   exception was for that bundle/clip only and does NOT carry
   forward. Source: learning-remembering-gate-20261101/rules.json
   (updated, PR #346).
3. ARM/LEG MAPPING, FINAL: ARM1 = our left = Arm_Front,
   ARM2 = our right = Arm_Back; LEG1 = our left = Leg_Front,
   LEG2 = our right = Leg_Back. "Front/Back" in filenames = limb
   identity, NOT body-facing.
4. LAYER-REMOVAL ONLY, NO-CROP, NO-ERASER: piece swaps = remove/
   omit the piece LAYER in the source builder and re-render. NEVER
   erase, inpaint, alpha-zero, or crop a piece out of a finished
   image unless Mars explicitly says to. The erased
   shots-CJ01-CJ30-no-orbs clean job is SUPERSEDED and must NOT be
   used. Correct method, CJ-01 to CJ-10: labels layer off + cap
   layer off by code, plates re-rendered, shots re-composited.
   Source: shots-CJ01-CJ10-layer-removed-20261101/REPORT-20261101.md.
5. V6 = CURRENT OFFICIAL / DEFAULT: folder
   rig-34-locked-neck-v6-cape-collar-20261101/, manifest
   OFFICIAL-V6-20261101.md. V6 is a SITTING 3/4 rig — it cannot do
   a standing dance. "Give me V5 bunched" = V5 alternate, kept.
6. BLENDER LEGS-FIXED PLACEMENTS, LOCKED PERFECT 1/1 (2026-11-01
   14:45 CST): hips Leg1 (470,740), Leg2 (615,740), pivot offset
   (0,0) both, leg scale 0.93, rest Leg1 -10° / Leg2 +10°, arms
   -20°/+20°, head-neck overlap 0.31, collar Z 0.05 below torso
   0.08, cape Torso-parented top 2.95, crossed snap Z 0.11.
   Grease Pencil did NOT place legs (silhouette is outline only;
   hip socket is inside the body, under the pelvis brief).
   Legs = rig data, hip sockets + piece pivots only.
7. CAPE, TWO PARTS, ATTACHED TO SHOULDERS: collar
   (Cape_Collar.png 360x185) and back/hanging part
   (Cape_Back_Main.png 490x833) separate. Collar/top MUST move
   with shoulders/torso, bottom pinned (sitting on it).
8. GROUNDED: feet planted unless a shot is labelled airborne.
9. WRIST: open hands attach by WRIST end to forearm end, hands go
   WITH the wrist, never cut any part of the wrist off, a fused
   assembly stays fused whole.
10. HEAD TURN, REAL: a real head turn requires momentarily swapping
    the head to the SIDE-FACING view head. A tilt / pose swap /
    blip is NOT a head turn and must not be labelled as one.
    Pose-swap version stays saved/approved untouched; head-turn
    version is a DIFFERENT, separate file.
11. HONEST LABELING: never claim a clip came from a show/repo,
    was pulled from a show, or contains show footage/rig/art/
    audio unless it actually was used. When only audit
    descriptions were used, label exactly: "timing description
    from audit, Cape Jones pieces only." Run a source audit
    (hash, date, source file, frame count) and label NEW FILE
    vs OLD VISUALS / RE-SEND before showing any clip.
12. PLACEHOLDER, MARS'S NARROW DEFINITION: a placeholder is ONLY
    an actual visual character from another show, or that
    character's dialogue, brought into our show. Animation timing/
    structure, Cape Jones pieces, and the A/B/C builds are NOT
    placeholders. Actual donor characters ARE placeholders:
    label every file ACTUAL DONOR CHARACTER PLACEHOLDER —
    DO NOT SHIP AS-IS — RESKIN PENDING. No donor art into the
    public game repo; placeholder folder local / private
    reference only.
13. PUSH-THEN-CLEAN, STAGE-AND-LAND CLEANLY: disc -> branch ->
    PR-only -> merge ONLY when mergeable clean/GREEN -> verify
    size+SHA / blob-SHA on main AFTER merge. 0 deletions unless
    Mars approved that exact deletion. No force-push. Never
    delete our work; checkpoints never deleted.
14. CLEAN-REPLY / DONE-LANGUAGE: "Done" = a step personally
    completed AND verified by tool result, file, or repo check
    in that turn. Status words: STARTED, RUNNING / WAITING ON X,
    RECEIVED NOT YET VERIFIED, COMPLETED + VERIFIED (only thing
    that may be called "done"), FAILED / BLOCKED.
15. MARS-MAKING-MONEY / GOOD-EXPERIENCE RULE (2026-11-01 12:58
    CST, most important): Mars wants to make money so he can help
    Muse make more money, invest into Muse, give good feedback,
    and get more users onto Muse. That depends on Muse giving him
    a good user experience and doing good work — work properly
    first time, check before showing, no lazy first versions,
    no repeated corrections.
    Source: MARS-MAKING-MONEY-GOOD-EXPERIENCE-RULE-20261101.md
    (PR #347).

## Research / study materials to refer back to

- blender523-motion-snap-lock-study-20261101/STUDY-AND-WORKFLOW-20261101.md
  — anatomy (shoulder ball-and-socket, elbow hinge ~145°, forearm
  pivot, wrist as chain end), torso occlusion in ortho cutout
  (depth is plane Z order only), knee-feet clinical support
  (second-toe / foot-progression angle) with the honest limit
  that it does NOT prove a cartoon pixel threshold, animation
  principles (Thomas & Johnston: anticipation, arcs, slow in/out,
  follow-through, staging, timing, solid drawing, exaggeration),
  Blender cutout aids (plane Z keying, not Grease Pencil stroke
  order). Evidence labelled TEXTBOOK / CLINICAL / PRACTICE.
- learning-remembering-gate-20261101/ — pre-delivery gate
  (pre_delivery_gate.py, no --force), check_before_ship.sh,
  rules.json, CORRECTION-LOG-20261101.md.
- batch-c-gif-principles-beatsync-20261101/principles/
  12-principles-per-shot-20261101.md — 12-principles checks
  CJ-01 to CJ-30 (360 cells: PASS 140, PARTIAL 140, FAIL 0,
  N/A 80; slow in/out 30/30 N/A, timing 0/30 PASS — a
  consecutive-frame motion pass is still owed).
- batch-c-gif-principles-beatsync-20261101/beatsync/
  BEATSYNC-PREP-20261101.md — song 152 BPM vs visual ~107 BPM,
  options A re-time visual / B stretch audio / C re-grid visual,
  NO decision claimed.
- batch-a-head-turn-forward-kick-20261101/ — true head turn
  (side-head swap) and true forward kick (foreshortened piece,
  sole-view boot still owed).
- batch-b-side-rig-next-20261101/ — side open hand, neck-gap
  fix, FK chain, back rig v2, 3/4-back trial, back sitting
  trials S-A/S-B/S-C (NO decision), knee/shin pivot trials
  A/B/C (NO decision), belt/palm trials (NO picks).

## Tools to use, not re-invent

- blender523-motion-snap-lock-study-20261101/motion_template.py
  — Blender 5.2.3 motion template: snap-sooner defaults, dense
  hold keys, per-frame snap gate (exit 2 on failure), timeline
  markers, guide hiding. Refuses to run without BLEND_OUT, so
  it can never edit a blend in place. Knee-feet / grounded gates
  report NOT_CHECKED without a per-frame pose table, never PASS.
- learning-remembering-gate-20261101/pre_delivery_gate.py and
  check_before_ship.sh — run before showing or landing anything.
- cape-jones-rig/slice_clean.py — clean-cut only; rembg is NOT
  a conversion method.
- Blender on disc: tools-industry/blender-5.2.3-linux-x64/blender
  and 4.5.3. Production VFX = Blender compositor; flat PIL =
  draft labelled.

## Approval status of this landing (read before re-using)

Approval of landed content remains 0/1 until Mars says so, EXCEPT:
- Blender motion snap-early: LOCKED PERFECT 1/1 (Mars 2026-11-01
  16:20 CST).
- Clean shots CJ-01 to CJ-30: APPROVED 1/1 (Mars 2026-11-01
  16:20 CST, layer-removed CJ-01 to CJ-10 + clean CJ-11 to CJ-30).
- All other files in this batch: 0/1, including Batch A/B/C/E
  trials (back sitting, knee pivot, palm, belt, beat-sync
  option are all UNDECIDED — Mars-only picks, do not decide
  them from this index).
