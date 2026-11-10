# Idle Gate Correction — 2026-11-09 (v6-fix1)

## What was wrong, in plain language

The v6 idle gate measured **one thing only**: the angle of the evaluated
deform **upper-arm bone** (shoulder joint → elbow joint) against world-down.
Those numbers were *true* — standing 4.9° / 0.9°, the sits 8.3–23° — but they
were **blind**. The gate never measured **where the elbow actually sits**
relative to the torso.

The shoulder joint sits ~0.24–0.26 m lateral of the body axis, because the
clavicle runs at 72–84° from down (nearly horizontal). A perfectly vertical
upper arm hanging from a high, wide shoulder therefore still puts the elbow
well outside the body silhouette. On screen, the line the eye actually reads —
clavicle head → elbow — runs **47–57° from vertical**, and the elbows land
**outside the torso's pixel band in every pose the old gate passed**.

A vertical upper arm hanging from a high, wide shoulder **is** the scarecrow
read that was rejected. The gate measured the one segment that could not fail
and ignored elbow position entirely. The owner's own guess — "you must not
have the videos called arms" — was directionally right: the number never
described the visible arm.

Evidence: `diag/ground_truth.py` measurements of the evaluated deform rig +
evaluated mesh, projected through a true front camera
(`gt_stand.json`, `gt_sit.json`, `gt_w5r.json` in the fix lane's records).

## Numbers vs render — before (the divergence)

Per pose: upper-arm bone angle (3D / on-screen) vs clavicle-head→elbow
on-screen angle vs elbow distance outside the torso pixel band.
800×800 front-camera renders, ground-truth probe.

| Pose | Side | Bone 3D° | Bone screen° | Clav→elbow screen° | Elbow outside torso (px) |
|---|---|---|---|---|---|
| Standing idle (DanceV6Full f1) | L | 4.9 | 1.6 | 56.9 | 22 |
| Standing idle (DanceV6Full f1) | R | 0.9 | 0.2 | 48.3 | 32 |
| sit_normal | L | 8.3 | 7.4 | 54.5 | 39 |
| sit_normal | R | 8.3 | 7.2 | 54.7 | 36 |
| sit_leg_folded | L | 8.3 | 7.4 | 54.6 | 39 |
| sit_leg_folded | R | 8.3 | 4.2 | 51.9 | 24 |
| sit_lean_forward | L | 22.8 | 22.6 | 46.6 | 8 |
| sit_lean_forward | R | 22.8 | 22.9 | 46.8 | 3 |
| sit_recline | L | 9.2 | 9.0 | 55.2 | 44 |
| sit_recline | R | 9.2 | 8.8 | 55.4 | 41 |
| sit_shrug | L | 23.0 | 16.5 | 49.8 | 14 |
| sit_shrug | R | 23.0 | 17.6 | 49.6 | 11 |
| idle_heroic_breathe (sitting library, f12) | L | 17.6 | 2.0 | 52.7 | 34 |
| idle_heroic_breathe (sitting library, f12) | R | 17.6 | 2.0 | 52.7 | 34 |
| idle_heroic_breathe (w5r file, f1) | L | 12.7 | 2.5 | 52.7 | 34 |
| idle_heroic_breathe (w5r file, f1) | R | 12.7 | 2.5 | 52.7 | 34 |

Read: poses with bone angles under 10° — "passing" under the old gate — still
show elbows 22–44 px outside the torso. The bone angle and the visible arm
disagree because the clavicle offset dominates the silhouette.

## The new gate (replaces the old one)

All checks are made **on the rendered frame**, per pose, per side:

- **(a)** Shoulder→elbow bone **screen** angle ≤ ~12°.
- **(b)** Elbow **inside** the torso pixel band, or ≤ a few px outside it
  (exact px reported — this is the check the old gate never ran).
- **(c)** Clavicle-head→elbow screen angle reported honestly. Anatomy keeps
  this ~35–45° even in a correct hang; it is context, not a pass/fail at 12°.
- **(d)** The zoomed upper-body crop must *read* as arms hanging beside the
  body, elbows in. A human eye check, not a number.

`sit_shrug` note: the shrug is a gesture (raised shoulders, folded forearms).
It may keep its gesture, but its elbows must still satisfy (b); any exception
is documented with its crop, not silently passed.

## The fix

Pose-data correction only (no rig, mesh, seat, leg, or root changes): rotate
the clavicle down/in about the facing axis at its head and adduct the upper
arm at the shoulder until the *evaluated* elbow lands beside the torso
silhouette, with the forearm compensated so the hands keep their original
world direction. Sitting seat/legs/root data stays byte/value-identical to
`sitting_pose_library_armsdown.blend` — arms only.

## After numbers

_(Filled in by the fix lane once pixel verification on the rendered frames is
complete — rendered pixels only, never solver-internal numbers.)_
