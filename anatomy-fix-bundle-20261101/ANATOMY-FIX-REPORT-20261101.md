# ANATOMY FIX BUNDLE — 2026-11-01, Mars 11:26–11:31 CST

NEW rig re-renders, Cape Jones pieces only. NOT show footage, NOT show rig/art/audio.
Label, honestly: timing descriptions from audit, Cape Jones pieces only, new files.
Originals untouched. Approval 0/1 each, Mars only.

## Research first (methods, not show material)
- Shoulder: ball-and-socket, abduction = arm away from body sideways, deltoid;
  elbow: hinge, flexion decreases angle, extension increases it (biceps flexes
  elbow, triceps extends). A flex that keeps both elbows close to the head
  centreline reads as an overexerted/acute squeeze, not a double bicep:
  a double bicep needs elbows OUT, upper arms near horizontal, forearms
  flexed up/in toward the head/shoulders.
- Knee: hinge, tibia tracks over the 2nd toe; internal tibial rotation =
  toes inward, external = toes outward. Valgus (knee-in/toe-out) and varus
  (knee-out/toe-in) are both misalignments — hence per-frame, bidirectional.
- Weight shift: a character cannot lift a leg until weight shifts onto the
  other leg; a side step is lift → move → plant → weight shift → other leg,
  not both feet sliding together.
- Cutout layering (Harmony/Godot/Animate, as in ARM-FRONT-SNAP-RULE.md):
  depth is keyable per frame; an arm across the chest is anterior to the
  pectoralis, so it must be drawn above the torso for that moment only.

## 1. FLEX — wider / obtuse
Old arms-up reference: upper -170/+170, elbows 413,263 / 680,262,
dx from centre -137/+130, inter-elbow 267px, fists 494/620 (inter-fist 126px),
angle from vertical-up 5°/3° — acute V above the head. That is the defect.
New wide-up key (replaces arms-up reference): upper -100/+100, lower 20/-20,
elbows 253,398 / 846,392, dx -297/+296, inter-elbow 593px,
angle from vertical-up 75°/73° — +70° per arm vs old arms-up.
Flex hold (unchanged upper, already wide): upper -85/+85, lower 145/-145,
elbows 247,446 / 854,439, dx -303/+304, inter-elbow 607px,
angle from vertical-up 90°/88° — +85° per arm vs old arms-up, inter-arm ~178°,
obtuse. Fists still roll toward head/shoulders: lower far point 375,203 /
710,207, above the elbow, toward the head — NOT outward away from the head.
Anticipation also widened: upper -40/+40 → -70/+70, elbows dx -249/+254 →
-297/+299, inter-elbow 503 → 595px.
Elbow audit flex: 0 lateral fails in 75 frames. Elbow = lateral/outward,
forearm flexes inward/up, never reversed.

## 2. ARMS ACROSS CHEST — automatic snap, wired into this builder
Sensor: forearm-vs-torso alpha overlap >1000px at 1100x1500, per arm, per
frame, from the rig angles BEFORE rendering (arm_front_snap_sensor.py logic,
ported into figure2() in build_anatomy_fix.py). Chest snap = WHOLE chain
(upper + forearm + fist + cap) after torso, before neck/head.
Face-top keys (original top keys) stay after head. Priority face > chest.
Snap counts (frames with at least one snapped arm):
- flex-wide: 39/75, max overlap 6,948px
- dance-shuffle: 24/133, max 7,021px
- punch-cross: 51/75, max 12,012px
- cross-down (corrected): 27/39, max 11,800/10,918px (L/R, key hold)
Torso NEVER eats a snapped arm in these renders: on snap frames the whole
chain is drawn after the torso. This figure2() + sensor is the portable
wire-into-every-builder module for these chains; frozen historical builders
(joint_locked_rig_v7c.py etc.) were NOT edited, per the frozen-builder rule
— the gate sits in front of them. Claiming every historical builder was
rewritten would be false, so it is not claimed here.

## 3. ELBOWS BACKWARDS — found and flipped
Reversed config found: cross-down upper (20,-20), lower (90,-90).
Elbows 478,622 / 628,624, dx from shoulder +48/-42 (INWARD), forearm far
points 750,587 / 357,608 (overshooting past the opposite side).
That is elbows inward/forward, opposite to a crossed-arms pose.
Corrected: upper (-20,+20), lower (90,-90). Elbows 353,611 / 753,609,
dx from shoulder -77/+83 (OUTWARD/backward), forearm far points
625,577 / 482,592 (crossing the centre, not overshooting).
Corrected cross-down: 0 elbow-lateral fails in 39 frames.
One borderline frame remains in dance-shuffle (frame 121, dance B →
finale transition, upper -171/+175.5, angle_from_up -4.2°/-2.3°):
elbow is almost directly ABOVE the shoulder, so a lateral test does not
apply — it is a vertical arms-up transition, not a reversed elbow.
Recorded here, not hidden, not counted as a pass by redefining the test.

## 4. LEGS — per-frame, Mars exception for THIS bundle only
Gate (standing correction gate): inward = leg_upper L > 0 AND R < 0.
Standing KNEE-FEET-RULE.md is NOT overwritten by this bundle exception.
- If gate ON: LEG2 RIGHT foot TURNS (mirror R lower piece, anchor remapped
  width − ball, as in the dance-kneefeet correction; measured on a test
  frame: R foot centroid moves from -49px to -118px relative to the knee,
  i.e. further in the knee direction). LEG1 LEFT foot does NOT turn
  (no mirror, original lower kept, Mars: "it is fine as-is").
- If gate OFF: no turn, feet follow knees (outward/straight).
Counts: flex-wide 0/75 turned (gate never on — legs -22/22, -20/20),
punch-cross 0/75, cross-down 0/39, dance-shuffle 11/133 turned R, 0 turned L.
Those 11 are the plant-R transition frames (leg_upper L > 0, R < 0).
Per-frame tables are in each *-xsheet-20261101.csv:
frame, arm_upper/lower, leg_upper/lower, snap px + snap Y/N, chest/face top,
knee gate, foot_turn_L/R, elbow angle_from_up + lateral ok.

## 5. SIDE-TO-SIDE SHUFFLE — alternating lift-plant
Replaced the old shimmy sway (whole-rig dx -30/+30, both feet sliding
together) with, in order: shimmy centre → step L (lift, dx -30, L leg
upper -15, lower 70 = knee bent, foot up, weight on R) → plant L (dx -30,
both planted) → step R (lift, dx 0, R leg upper 15, lower -70, weight on L)
→ plant R (dx 0) → step L (lift, dx -30) → plant L (dx -30) → shimmy centre.
Steps in the xsheet: step L frames 33–42, plant L 43–52, step R 53–62,
plant R 63–72, step L 2 73–82, plant L 2 83–92. Grounded except the lifted
foot moment (silhouette bottom stays on the ground line via the planted
foot, as in build_chains ground compensation).

## Outputs (new, originals untouched)
- anatomy-flex-wide-20261101.mp4 — 75f @24fps, 3.12s, 1100x750, aac, 208K
- anatomy-dance-shuffle-20261101.mp4 — 133f @24fps, 5.54s, 1100x750, aac, 389K
  (first mux was truncated to 93f by a 3.88s wav + -shortest; remuxed with a
  new 5.54s wav, lifts = blip, plants = thump — disclosed, not hidden)
- anatomy-punch-cross-20261101.mp4 — 75f @24fps, 3.12s, 1100x750, aac, 169K
- anatomy-cross-down-20261101.mp4 — 39f @24fps, 1.62s, 1100x750, aac, 96K
- Each with a .gif preview, a *-xsheet-20261101.csv per-frame table, and
  build_anatomy_fix.py (the sensor + figure2 builder).
- Sound: original clip WAVs reused for flex/punch/cross; shuffle uses the
  new 5.54s wav above. Peak -1dB as in the movement clips, NOT a final
  -14 LUFS mix.

## Gates
- Flicker, whole-frame proxy @6fps, mean-luminance jump >25.5 = flash:
  cross-down max 8.33, 0 flashes; shuffle max 12.49, 0; flex max 9.23, 0;
  punch max 8.67, 0. PASS, all 4.
- Elbow lateral: flex 0 fails, punch 0 fails, cross-down (corrected) 0 fails,
  shuffle 1 vertical-exempt frame (see §3).
- Snap: see §2 counts. A frame with forearm overlap >1000px and no snap
  would FAIL; none occurs in these 4 outputs.
- Wrist: no new hand placement, no wrist cut, no hand-draw in this bundle
  (rig pieces as built); wrist gate for new hand attachments is still owed
  separately, as before.
- Approval: 0/1 each. Landing: local only, no PR claimed, not verified on main.
