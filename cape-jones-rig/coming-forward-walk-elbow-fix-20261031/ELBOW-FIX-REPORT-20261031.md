# Coming-forward walk — ELBOW FIX — 2026-10-31

Mars, 2026-10-31 22:12 CDT, replying to the layer-fixed walk GIF:
elbows are backwards, biceps should be at the opposite degree tilt,
forearms also tilt opposite, elbow in a slightly different position,
and: if you move/slide/rotate the bicep, does the elbow move with it?
Is there industry-standard rigging where moving one part makes the
other part follow, like real anatomy, wired 100%?

## Answer to his question, first: yes, in a parent-child rig
Shoulder -> upper arm (bicep) -> elbow joint -> forearm -> wrist/hand.
The elbow is a CHILD of the bicep: its position is computed from the
shoulder and the bicep angle, never hand-placed. The forearm is a
child of the elbow: it is pasted AT the computed elbow. So rotating
the bicep moves the elbow, and the elbow moves the forearm, and
sliding the shoulder moves the whole chain by the same amount.
That follow-through already existed implicitly in snap_figure.py;
here it is a named, tested module (`build_elbow_fix.py`, ArmChain)
with a pole gate, instead of an implicit formula. That gate is what
would have caught the backwards key.

## 1. Measured, old walk (plate coords, figure cx 550, before walk scaling)
Angle convention: 0 deg = straight down, positive = toward viewer's
right (east), negative = toward viewer's left (west). Same for upper
and lower. Shoulders: L (430,445), R (670,445). Elbow positions are
analytic (shoulder + rotated upper vector x 0.95), not eyeballed.
Wrist positions are APPROX (lower-piece fist-centroid offset rotated
by the lower angle; the fist cannot be segmented separately from the
cuff+fist lower piece, same limit as the layer-fix report).

| key | side | bicep deg | forearm deg | relative bend | elbow (x,y) | elbow dx | apex |
|---|---|---:|---:|---:|---|---|---|
| CONTACT-L OLD | L | +20 | -30 | -50 | (478.1, 621.6) | +48.1 | INWARD (BACKWARDS) |
| CONTACT-L OLD | R | -20 | +30 | +50 | (628.1, 623.9) | -41.9 | INWARD (BACKWARDS) |
| PASSING | L | 0 | -10 | -10 | (414.8, 627.4) | -15.2 | OUTWARD |
| PASSING | R | 0 | +10 | +10 | (691.9, 627.4) | +21.9 | OUTWARD |
| CONTACT-R | L | -20 | +30 | +50 | (353.3, 611.2) | -76.7 | OUTWARD |
| CONTACT-R | R | +20 | -30 | -50 | (752.9, 608.9) | +82.9 | OUTWARD |

Why the elbows read as backwards, plainly: in CONTACT-L both elbow
caps sit INBOARD, tucked against the waist/abs, and the forearms
angle OUTWARD to fists outside the hips. The elbow is the apex
pointing INTO the chest. A human elbow in front view points LATERAL
(outward, away from the torso), with the forearm coming back INWARD
toward the front of the body. CONTACT-R already does that (caps out
at the sides, forearms in, fists in front of the thighs); PASSING
does it small. So the walk alternated correct / backwards every
step, and the backwards key is the one the walk starts and holds on
(CONTACT-L hold, frames 40-43), which is why it dominated the GIF.

## 2. The correction, and what was NOT done, plainly
ONLY the backwards key was negated. Corrected CONTACT-L:
upper L -20 / R +20, lower L +30 / R -30, elbows L (353.3,611.2) /
R (752.9,608.9), both OUTWARD, pole gate PASS. Legs, scale, timing,
feet and ground are unchanged.
NOT done: negating the WHOLE walk. That would make CONTACT-R
backwards, which would be wrong. If Mars literally meant a global
negation, say so and it will be built as a separate variant, but it
is not what is in this corrected walk.
Forced change, plainly: inbetween frames on the two segments
touching CONTACT-L (frames 0-9 and 31-40) change because they
interpolate from the corrected key. No other key changes. Snap
table from the layer-fix walk is reused unchanged (chest rows
0,1,2,3,37,38,39,40,41,42,43); the corrected arms still come down
in front of the chest there.
Consequence to note: both contacts now share the same outward-elbow
arm pose, with PASSING as the straighter in-between (upper 0, bend
+/-10). Arm swing in this front-view walk is now bend amount, not
a sign flip that breaks the elbow. If Mars wants a different
left-step vs right-step arm swing (e.g. one arm more bent than the
other per step), that is a new key decision, not part of this fix.

## 3. Rig chain, wired 100%, with measured follow test (L arm, base CONTACT-R)
- Base: shoulder (430,445), upper -20, lower +30, bend +50,
  elbow (353.3,611.2), wrist approx (479.3,798.0), OUTWARD.
- Bicep rotated +20 (upper -20 -> 0), bend KEPT (lower 30 -> 50):
  elbow (414.8,627.4) = +61.5 east, +16.2 down; wrist approx
  (597.1,759.9). Elbow AND forearm followed the bicep.
- Bicep rotated +20, absolute forearm angle KEPT (lower stays 30):
  elbow (414.8,627.4), same elbow move; wrist approx (540.8,814.2),
  bend now +30. Position still follows; bend is the choice.
- Shoulder slid +30 east: shoulder (460,445), elbow (383.3,611.2)
  = exactly +30; wrist approx (509.3,798.0) = exactly +30.
- Shoulder slid -40 west, +10 down: shoulder (390,455),
  elbow (313.3,621.2) = exactly -40, +10; wrist (439.3,808.0).
Industry methods: FK chain RUN (this module + snap_figure.py);
elbow-pole constraint RUN (gate: L elbow x < shoulder x, R elbow x
> shoulder x, medial = FAIL); IK with elbow pole MAPPING only
(no IK solver in this 2D piece rig, pieces are fixed-angle
rotations, never claimed as a run); anatomy hinge ranges as the
reason for the outward pole, not a medical claim for this character.
Honest limit on the rig-test contact: the bicep-rotation panels are
real re-renders (upper angle changed in the figure); the shoulder-
slide panel's UNDERLYING figure is not re-rendered at a moved
shoulder (snap.figure has fixed shoulders), only the overlay chain
moves — the slide proof is the measured numbers above, not that
panel's art.

## 4. Corrected walk
44 frames @ 24fps, same keys/timing/scales as layer-fix walk except
CONTACT-L arms above, same 1600x1800 canvas, grey + ground band,
feet_y 1500 on all 44 frames, spread 0 px, no edge-touch, PASS.
Layer-fix walk untouched. No repo push.

## Files (all new, this folder)
- coming-forward-walk-ELBOW-FIXED-20261031.gif (44f @24fps)
- elbow-before-after-contact-20261031.png (f00, f20 unchanged, f40; red ring = elbow, red line = bicep, orange = forearm)
- rig-follow-test-contact-20261031.png (base / bicep +20 / shoulder +30, L arm)
- elbow-measurements-20261031.json (key table + rig tests + pole gates)
- corrected_walk_measurements.json (44f, feet, PASS)
- frames-fixed/f000.jpg ... f043.jpg
- build_elbow_fix.py (measurement + ArmChain + corrected builder + contacts)

## Status
Approval 0/1 for the corrected elbow walk, 0/1 for the rig chain
separately. Layer-fixed walk approval stands separately and is not
re-asked or claimed by this fix.
