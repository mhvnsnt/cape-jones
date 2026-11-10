# Auto-Rig + Mocap Research — the v4 dance fix (2026-10-31)

Owner verdict on 3D dance v3: stiff everywhere — shoulder→elbow locked in
T-pose, only forearms moved, wrist→fingers stiff, shoulders→torso stiff,
knee→shin→ankle stiff, knee→hip→pelvis stiff, spine stiff. Root cause on
record: v3 was hand-keyed FK, no IK, no motion data. Owner's order: pull
the top three industry-standard animation systems (free ones pulled in;
paid ones reverse-engineered for their METHODS — cracked installers stay
untouched, we take the craft, not the software), auto-rig the character
with a machine-built full-body IK rig (no hand-built rigging), then attach
a small repetitive loopable REAL mocap dance. IK must cover everything:
fingers to toes to cape tip to head, cape included as its own chain.

## The top 3 selected (and what each changed in the motion)

### 1. CMU Graphics Lab Motion Capture Database — the motion itself
- Source: mocap.cs.cmu.edu, BVH via the cgspeed conversion (same source as
  the repo's existing `3d-assets/animation/mocap-cmu/` starter pack).
- License (verbatim on the existing MANIFEST): data "may be copied,
  modified, or redistributed without permission"; free for research AND
  commercial use; NSF EIA-0196217 acknowledgment appreciated; may not
  resell the data itself.
- Pulled this lane: subjects 60/61 (salsa, 15 trials each), 05 (modern
  dance), 15 (everyday/dance moves) — 9 BVH files into the lane workspace.
- USED: **15_04, window starting at source frame 12625** (476 source
  frames @120fps → 96 frames @24fps), committed in this PR.
  Window chosen by a facing scan (`bvh_facing_scan.py`): front-facing
  fraction 1.00 (median yaw −7°), root spread 7.0 units (in one spot),
  seam distance 0.57 (near-seamless loop).
- REJECTED after measurement: 61_03 salsa @1010 (the first pick — biggest
  joint ranges) because the dancer faces ≈−90° (profile, partner work) for
  the entire window; all of subjects 60/61 failed the front-facing test.
  They remain pulled in the lane workspace, uncommitted, logged here.
  05_03/05_11 were too short for a 476-frame window.
- What it changed: ALL of the motion is now real captured human movement —
  elbows, knees, spine, head timing and weight come from a person, not
  from keyframes.

### 2. Blender Rigify — the auto-rigging path (machine builds the rig)
- Bundled with Blender 4.0.2, free/GPL. Rigify auto-generates a complete
  control rig from a fitted metarig: two-bone IK arms/legs with IK/FK
  sliders and pole targets, bendy spine chain, dedicated finger sub-rig
  (master curl controls + per-segment FK), neck/head super-head chain,
  shoulder/clavicle controls.
- This is the same CLASS of auto-rigger as Mixamo's and Auto-Rig Pro's
  auto-build (see paid methods below) and is the one reachable here
  without any sign-in. The metarig was fitted to Cape Jones's measured
  joints (taken from the v3 model's own skeleton), then
  `bpy.ops.pose.rigify_generate()` built the rig: 741 bones, 165 deform.
- Cape: a 5-bone chain (cape.001–005) parented to the spine was given
  Rigify's `limbs.spline_tentacle` type, so generation also produced a
  spline-IK cape chain with start/mid/end hook controls (cape.start01,
  cape.mid01, cape.end01, cape.end, cape.master) — the cape is rigged by
  the same auto-generation, not hand-built.
- What it changed: IK everywhere. Elbows and knees bend because IK targets
  say so; the spine is a chain, not a single pivot; fingers have real
  joints driven per segment.

### 3. Cascadeur secondary-motion + Rokoko/HumanIK retarget METHODS
(paid tools — methods reverse-engineered into the open pipeline, no
software taken)
- **Cascadeur** (paid) is known for AutoPhysics + Secondary Motion:
  physics-flavoured follow-through computed per controller with damping,
  gravity and inertia. Method implemented here as a verlet spring chain
  for the cape: 6 points in chest space, per-joint stiffness falloff
  [0, .38, .26, .17, .11, .07], damping 0.90, gravity step, 3 constraint
  iterations, warm-started across 3 loop passes so the loop wraps; drives
  the Rigify spline-IK cape hooks. The cape still renders as the same
  one-piece sheet mesh from v3 — the chain only moves it.
  Cascadeur's AutoPosing-for-fingers method (one master curl driving
  coupled finger joints) is mirrored in the finger solve: CMU's single
  finger-base/index/thumb channels are distributed across the full
  15-joint-per-hand finger rig with per-finger and per-segment falloff.
- **Rokoko / MotionBuilder HumanIK** (Rokoko's retarget plugin is free
  but requires a Rokoko account sign-in to run — not used; its METHOD is
  the industry standard and is what is implemented): world-space
  retargeting with per-limb reach normalization. Implemented in
  `solve_v4.py`: torso = world-space rotation deltas (premultiplied) on
  the Rigify torso/chest controls with the torso anchor following the
  hips translation; hands/feet = IK targets placed relative to the
  EVALUATED shoulder/hip anchors, scaled by the target/source limb-length
  ratio (arms 0.84–0.86, legs 0.72–0.75) and reach-clamped to 99% of limb
  length; poles placed from the source limb's own bend direction.
  Why this matters (found the hard way): plain position-delta retargeting
  from the T-pose overshoots when skeleton proportions differ — the right
  hand target sat 0.326 m from the shoulder of a 0.242 m arm, so the
  elbow locked at 180° for the whole loop. Anchor-relative targets fixed
  it (right elbow now ranges 48.5–89.5°... see README measurements).

## Paid standards researched, NOT pulled (honest gaps)
- **Mixamo** (Adobe): the canonical auto-rigger + motion library, free
  with an Adobe ID — requires the owner's sign-in. Per standing orders we
  never ask him for a login; skipped and logged. Its auto-rig class is
  covered by Rigify above.
- **Auto-Rig Pro** (~$40, Blender add-on): its Smart auto-build and Remap
  retargeting methods were read from its public docs (lucky3d.fr) — the
  Remap bone-list world-space method matches the retarget implemented
  here. Software not purchased, not cracked.
- **Rokoko Studio Live Blender plugin**: free on GitHub
  (Rokoko/rokoko-studio-live-blender) but unusable without a Rokoko
  account sign-in; method implemented natively instead (above).
- **MotionBuilder / HumanIK** (Autodesk, paid): the reference
  implementation for the anchor-relative IK retarget used here.

## Bugs found and fixed while wiring (for the next lane)
1. Source sampling must be fully cached BEFORE the target rig gets its
   action: `frame_set` during the solve re-evaluates the target at the
   wrong frame and corrupts parent matrices.
2. Rotation deltas compose as `delta_world @ rest_q` (premultiply) when
   assigning world matrices; the postmultiply order pretzels the body.
3. Rotation-only controls whose position is parent-driven (neck, head,
   shoulders) must NOT be assigned a fixed world position — pinning the
   neck control at its rest position stretched DEF-spine.003 from 0.11 m
   to 0.305 m (the "puffer torso" in the squat). Keep their evaluated
   position; override orientation only.
4. The torso control must follow the hips translation or the spine chain
   stretches to bridge the gap.
5. Quaternion "range" metrics on DEF bones are poisoned by IK-stretch
   scale in the matrices — measure direction-vector swing instead
   (`measure_v4.py` does).
6. Facing matters: score mocap windows for facing (toe−ankle yaw), not
   just joint range — partner-dance clips face sideways.
