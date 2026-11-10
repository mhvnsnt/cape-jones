# Coming-forward walk — KNEE-FEET FIX — 2026-10-31

Mars, 2026-10-31 23:03 CDT, replying to the walk elbow fixed GIF:
"when the thigh goes inward and the knee goes inward, the toe should
switch the direction it's pointing in. You didn't do that in this
video and that's a rule that we had locked in a lot in all of the
different movements and stuff. That was supposed to be universal."

Mars was right, and the elbow approval stands for elbows only.
This walk is NOT fully approved until the knee-feet fix is seen.

## Easy way to say it

Knees and feet point the same way. Knees in, toes in. Knees out,
toes out. If the knee points in and the foot still points out, the
leg reads broken. That was the defect in this walk.

## 1. Audit of the elbow-fixed walk, 44 frames, per leg

Angle convention: 0 = straight down, + = viewer's right (east),
- = viewer's left (west). A leg's thigh is INWARD when it angles
toward the midline: L upper > 0, R upper < 0. OUTWARD is the reverse
sign. STRAIGHT is exactly 0 (original lower, do not flip).

Leg keys (unchanged): CONTACT-L leg_upper L -28 / R +22 (both
OUTWARD), PASSING 0 / +5 (straight/outward), CONTACT-R +22 / -28
(both INWARD). Interpolated with the walk's own smoothstep.

Per-leg audit (thigh sign only, no exception): 34 / 88 leg-frames
mismatch, 19 / 44 frames with any mismatch (f11-29). L mismatches
19 (f11-29), R mismatches 15 (f13-27). The elbow walk used original
lowers on every frame, so every inward-thigh leg-frame failed.

## 2. Caught before delivery: the crossed-leg exception

A first build applied the per-leg rule literally to all 19 frames.
Viewing it caught a real error: at CONTACT-R (f20) the legs are
CROSSED — L knee screen-x 583.4 > R knee screen-x 506.2 — so the
original feet already point toward each other (inward by eye).
Mirroring them there flipped both toes OUTWARD and broke the key
frame. That build was NOT delivered; it was corrected here.

Revised, eye-correct rule, measured per frame from analytic knee
screen-x (hip + thigh vector, SCALE 0.95; L hip (470,740), vector
(18,274); R hip (615,740), vector (16,274)):
- Knees NOT crossed (L knee x < R knee x) AND thigh inward ->
  FootIn mirrored lower for that leg, toe switches.
- Knees CROSSED (L knee x > R knee x, f17-23) -> original lowers.
  Feet already point inward by crossing; mirroring breaks them.
- Thigh outward or straight -> original lowers.

Revised audit (this is the gate that shipped): 20 / 88 leg-frames
mismatch in the old walk, 12 / 44 frames (f11-16 and f24-29).
Breakdown: f11-12 L only, f13-16 both, f24-27 both, f28-29 L only.
Crossed f17-23 are PASS in the old walk, not failures.

## 3. The fix

Only the leg lower piece changes, per leg per frame, by drawing
substitution (whole lower piece mirrored, ankle intact, never a
foot cut off and pasted, never hand-tooled smearing):
- Front (L) original toe west -> FootIn toe east; mirrored knee
  anchor 59 (original 95).
- Back (R) original toe east -> FootIn toe west; mirrored knee
  anchor 127 (original 100).
Pieces: dance-kneefeet-fix-correction-20261031/pieces/
Leg_Front_Lower_FootIn.png / Leg_Back_Lower_FootIn.png.

Changed frames: 12 (f11-16, f24-29). Identical frames: 32
(including crossed f17-23 and all outward frames), verified by
saved-JPG comparison, 0 px diff > 30 on identical frames.
Arm angles identical on all 44 frames (elbow fix preserved exactly).
Feet: y 1500 on all 44 frames, spread 0, no edge touch, min margin
299 px. Canvas, scales, timing, snap passes unchanged.
Anchoring: old frame's plate scale + horizontal placement, vertical
re-anchored so feet stay planted on 1500 (the FootIn foot's lowest
row differs by up to 16 plate px on L-only frames; a fixed top
would float that foot ~15 screen px, so the ground rule takes
precedence — stated, not hidden).

Gate proof (kneefeet_gate.py, exit 0/1):
- OLD walk: FAIL, 20 mismatches, frames f11-16, f24-29.
- NEW walk: PASS, 0 mismatches, 88 / 88 leg-frames.
The gate runs BEFORE rendering in the builder and refuses the
build on FAIL. That is the universal wiring, not a post-hoc check.

## 4. Universal wiring: 5 industry-standard + 5 experimental, 100%

INDUSTRY (all RUN in this folder):
1. FK leg chain (hip -> thigh -> knee -> lower -> foot/toe),
   mirror of the arm chain. Knee is COMPUTED from hip + thigh
   angle, never hand-placed; lower is pasted AT the computed knee;
   toe direction is then decided by the gate. RUN in
   kneefeet_gate.py (LegChain) + kneefeet_figure.py.
2. Per-frame, per-leg knee-feet gate, pre-build, exit non-zero on
   mismatch. No block ranges (the v1 dance mistake: FootIn on
   frames 15-55 flipped outward-knee frames inward). RUN in
   kneefeet_gate.py, used by build_kneefeet_fix.py.
3. Drawing substitution for transverse rotation: whole lower piece
   mirrored, ankle intact, with its mirrored knee anchor. RUN
   (FootIn pieces above).
4. Keyframe foot orientation (Animator's Survival Kit / Disney 12
   principles): foot substitution changes only at sign-crossing
   frames, thigh angle interpolates smoothly, no smearing between
   keys. RUN (footin table is derived from interpolated thigh
   angles, switch frames listed in kneefeet_audit.csv).
5. Gait/anatomy rule: tibia tracks over the 2nd toe; knee is a
   hinge, it cannot bend sideways; valgus (knee-in/toe-out) and
   varus (knee-out/toe-in) are BOTH misalignments. RUN as the gate
   criterion (sources in KNEE-FEET-RULE.md).

EXPERIMENTAL (run vs mapping labelled):
E1. Repo-wide movement audit scanner — RUN. audit_all_movements.py
    scans 48 builders, 204 leg_upper keys: 17 keys would fail IF
    rendered with original lowers, across 12 files. Caveat, plain:
    this is a KEY audit, not a render audit — some flagged files
    already apply FootIn (dance correction builder) or are test /
    measure scripts, not shipped movements. Files that actually
    ship movements with inward keys and no FootIn in source:
    dance-improved build_dance, dance-arm-snap, pseudo-turn
    templates, size power, walk layer/elbow builders (walk is
    fixed here; the others are still owed, listed in
    repo_wide_audit.json, scanner exit 1 = FAIL by design).
E2. Rendered-frame foot-band measurement — RUN as a diagnostic,
    NOT as the gate. Measuring the old walk's foot band showed
    feet together (no gap) from f13-27 and separated before/after
    — which is what exposed the crossing/overlap problem in §2.
    It is not reliable enough to be the gate on its own (band
    includes shins), so the gate stays analytic (thigh sign +
    knee-x crossing), and this stays a diagnostic.
E3. Blender FK leg rig with foot roll / tibia rotation proxy —
    MAPPING only. No Blender figure rig was built for this walk;
    the walk is a PIL plate rig. The FK chain direction (hip ->
    knee -> foot) is the same, the Blender run is not claimed.
E4. Harmony/Animate bone foot peg — MAPPING only. Trials not
    confirmed; no Harmony foot peg was run for this walk.
E5. Motion-capture / MediaPipe gait foot-progression angle check
    — MAPPING only. No mocap data and no pose model were run for
    Cape; the foot-progression angle concept is reused as the
    gate's anatomical reason, not as a measured run.

## 5. Honest limit, plainly

In the overlapping passing frames (f14-16, f24-26) the feet sit
together at the centre, and the existing side-profile FootIn
pieces cannot make both toes read inward without their tips
crossing past the midline and reading as splayed again at close
inspection. Those frames pass the per-leg + crossing gate (their
leg pieces are the correct substitution by the rule), but their
eye read at large scale is still ambiguous because there is no
forward-facing (toe-down, toward camera) foot drawing in the rig.
A forward-facing foot piece is owed if Mars wants those passing
frames perfect — that is the exact unblocker, not a hidden gate
failure, and it is not hand-tooled here. The frames where the
switch unambiguously helps (f11-13, f27-29, feet separating) are
fixed; CONTACT-R (f20) is kept correct and unchanged.

## Files (all new, elbow-fixed walk untouched, no repo push)

- coming-forward-walk-KNEEFEET-FIXED-20261031.gif (44f @ 24fps)
- kneefeet-before-after-contact-20261031.png (foot crops: f11
  L-only, f13 first both-in, f20 CONTACT-R crossed = unchanged,
  f24 both-in after crossing)
- kneefeet-fullframe-contact-20261031.png (f13, f20 full frames)
- kneefeet_audit.csv (44 rows: thigh angles, knee directions,
  knee-x, crossed, footin, changed)
- kneefeet_measurements.json (gate proofs, changed/identical
  frames, feet, margins, arm angles)
- kneefeet_gate.py (universal gate + LegChain, CLI exit 0/1)
- kneefeet_figure.py (snap_figure.py + footin only; diff vs
  snap_figure.py is exactly the footin branch)
- build_kneefeet_fix.py (audit + gate + render + contacts)
- audit_all_movements.py + repo_wide_audit.json (48 builders,
  204 keys, 17 failing-if-original keys)
- frames-fixed/f000.jpg ... f043.jpg

## Status

- Elbow approval 1/1 stands for elbows only.
- Knee-feet fixed walk: approval 0/1.
- Universal knee-feet wiring: approval 0/1 separately.
- No repo push. No existing file overwritten.
