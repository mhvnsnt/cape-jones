# Cape Jones dance proof 3D v4 — auto-rig + real mocap

Answers the owner's stiffness verdict on v3 (PR #272): T-pose arms, only
forearms moving, stiff fingers/spine/knees/hips. v3 was hand-keyed FK.
**v4 has zero hand-keyed dance motion**: a machine-generated Rigify
IK rig driven by a real CMU motion-capture dance loop. Research and
method mapping: `docs/production/AUTO-RIG-MOCAP-RESEARCH.md`.
**v3 is untouched** — this is a new build alongside it ("3D v3" stays the
version of record for v3).

## Pipeline (three stages, all headless Blender 4.0.2)

1. `build_v4.py` — STAGE A. Opens the v3 scene read-only (BodyR mesh,
   one-piece cape sheet, set, camera), fits a Rigify human metarig to the
   model's measured joints, adds a 5-bone cape chain
   (`limbs.spline_tentacle`), and lets `rigify_generate()` build the full
   IK rig (741 bones, 165 deform — IK arms/legs with poles and IK/FK
   sliders, spine chain, finger sub-rig, neck/head, spline-IK cape).
   Transfers the v3 skin weights onto the DEF bones (limb weights split
   across the .001 segment bones by projection; pelvis split
   DEF-spine/DEF-pelvis; cape weights redistributed across
   DEF-cape.001–005). Saves `rig_v4.blend`.
2. `solve_v4.py` — STAGE B. Imports CMU **15_04** (window @12625,
   front-facing per the facing scan in the research doc), retargets:
   world-space rotation deltas for the torso chain (torso anchor follows
   hips translation; neck/head/shoulder controls keep their evaluated
   positions — rotation only), anchor-relative reach-normalized IK
   targets for hands/feet/toes with poles from the source bend direction,
   finger curls distributed from CMU's finger channels with per-finger
   falloff (Cascadeur AutoPosing method), and a verlet secondary-motion
   pass (Cascadeur AutoPhysics method) driving the cape's spline-IK
   hooks. 96-frame loop, quaternion-continuous keys, 12-frame seam
   crossfade, tiled ×19 via NLA to the full 1,824 frames. Vertical root
   motion damped ×0.7, XZ ×0.6 (documented staging choices; rotations
   untouched). Saves `scene_v4.blend`.
3. `render_v4.py` — STAGE C (via the EGL-surfaceless launcher from the v3
   lane). Modes: `check` / `stills` / `loop` / `frames FS FE`, every saved
   frame byte-verified (size + JPEG EOI) with a retry ladder.
   `measure_v4.py` — joint-checklist measurements on the solved loop.
   `bvh_facing_scan.py`, `bvh_analyze.py` — mocap window selection tools.

Assembly: five world sections (day → LED magenta hflip → LED cyan →
night hflip → day, same as v3) from the 1,824 frames, muxed with the
**JP v2 mix** (v3 used EN; the two approved mixes rotate interchangeably)
→ `cj-dance-proof-3d-v4.mp4`, 75.79 s, 960×540, 24 fps.

## Measured acceptance (own-eyes verified)

Owner's joint checklist, measured on DEF bones across the 96-frame loop
(`measure_v4.py`, direction/position based — see research doc note 5):

| Joint group | v3 (hand-keyed FK) | v4 (mocap + IK) |
|---|---|---|
| Elbow L / R range | forearms only, small | **57.7° / 41.0°** (30–88° / 49–90°) |
| Upper arm vs T-pose | locked at horizontal | L −77…−39°, R −69…+31°; below −15° in **100% / 73%** of frames |
| Wrist direction swing | — | **164.6° / 161.6°** |
| Finger (middle chain) bend range | stiff | **57.1°** |
| Spine direction swing | stiff | **27.1°**, chest **31.3°** |
| Neck / head swing | stiff | **28.9° / 36.5°** |
| Knee L / R range | stiff | **54.2° / 58.3°** (deep squat phases to ~33–37°) |
| Ankle L / R range | stiff | **76.0° / 29.2°** |
| Pelvis | — | x-travel 0.085 m (in one spot), bounce 0.193 m |
| Cape tip travel | — | 0.46 / 0.41 / 0.42 m (x/y/z) — the cape dances too |

PR #269 §5 yardstick on the rendered loop (480×270, median-frame mask):
**torso-band travel 11.7%** of body width (spec ≥ ~10%), **foot-band
travel 17.2%**, **foot/torso ratio 1.48** (spec ≥ 0.5), **96/96 distinct
frames**, min frame step 0.74 (no frozen frames).

Cape §15 check (zoomed stills, front + back + hem): the cape is the same
one-piece sheet as v3, driven by the spline-IK chain — one solid piece in
every checked frame: no through-holes, slits, shards, or gap between
halves.

## Honest shortfalls
- The dance is an exercise-style front-facing routine from CMU subject 15
  (the only front-facing, in-one-spot, cleanly-looping window in the
  pulled set — the salsa subjects face sideways, partner work). It reads
  as a proper full-body dance loop; it is not a salsa.
- Feet mostly stay planted (foot x-travel 0.04/0.07 m) — the stepping is
  knee-bend/bounce weight shift rather than travelling steps; the §5
  foot-band test still passes via leg spread.
- Toe targets use an exaggerated length ratio (2.0–2.2× — CMU's toe joint
  sits close to the ankle); toe motion is bounded by reach clamp but is
  the least faithful chain.
- Fingers: CMU gives index + thumb + one shared finger-base channel per
  hand; middle/ring/pinky are coupled distributions of that channel, not
  independent captures.
