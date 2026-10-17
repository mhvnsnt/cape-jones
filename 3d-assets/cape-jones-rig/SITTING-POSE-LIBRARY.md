# Sitting Pose Library — Cape Jones

Owner directive 2026-10-17: "the pose library thing we gotta get that together, the sitting and all of that."
Lane: `lane/sitting-pose-library-v2-20261017` (RESTART — previous lane died in a daemon restart with nothing pushed).

He sits ~90% of the time. Five core sitting poses, all full-body FK on the 85-bone
W5r rig (`cape_jones_rigged_w5r_idle.blend`), feet grounded exactly, seated on the
canon recliner (`loungeChairRelax(Clone)` @ (3.14, 1.5, 0), 225° yaw, right window wall).

## Poses
1. `sit_normal` — main upright relaxed sit, feet flat, hands on thighs.
2. `sit_leg_folded` — one leg folded up (his reference pose).
3. `sit_lean_forward` — pensive/focused, elbows on knees, hands clasped.
4. `sit_recline` — leaned back, sprawled, arms behind head (Space Ghost desk energy).
5. `sit_arms_crossed` — arms crossed, leaning back (comedic annoyed energy).

## File
- `3d-assets/cape-jones-rig/sitting_pose_library.blend` — each pose stored as an
  Action marked as a Pose Asset, frame 1, all FK control bones keyed.
- Proofs: `3d-assets/cape-jones-rig/sitting-poses/*.png` — one render per pose, verified by eye.

## Cape drape validation: PENDING
The cape rebuild lane is producing a single-sheet cloth cape. Poses were built now
per directive (don't wait). Cape drape/clipping validation against these poses is
PENDING on the cape lane's delivery.

## Canon
Palette locked: suit #FFFFFF, cowl #3E1473, cape #000000. Scale 0.925m locked.
Feet grounded EXACTLY per pose — no sinking, no floating, no chair/floor clipping.
