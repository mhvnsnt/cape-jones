# Cape Jones 3D Dance Proof — V6

Same dance as V5 — same mocap window (CMU 15_04 squat-bounce groove),
same set, same world cycle (day → LED colors → night → day), same
one-piece cape, full song length at 960×540 / 24fps. The Japanese v2
mix this time (the mixes rotate; V5 used English).

V6 fixes exactly the three things the owner called out on V5, plus a
permanent, everywhere fix for the first one.

## Fix 1 — the "H pose" at idle is dead, everywhere, permanently

**What the H pose actually was — three stacked causes, all measured:**

1. **The rig's rest pose IS an arms-out pose.** Upper arms sit at
   80.1° / 80.8° from hanging-straight-down in the rest pose, and the
   mesh is bound in that pose. Any moment no live animation channel is
   driving the arm bones, the arms return to out. The rest pose is the
   bind, so it stays — what kills the H is making sure a live
   arms-down pose always drives the arms.
2. **The rig's only idle animation was dead.** `idle_heroic_breathe`
   keys `rotation_euler`, but in the sitting pose library every one of
   the 85 pose bones is in QUATERNION rotation mode — Blender ignores
   euler channels on quaternion bones, so the idle never played a
   single frame of its intended arms-down pose. Layered anywhere, it
   showed the rest-pose H. In the older w5r idle file the same action
   is live (euler-mode bones) but its mirrored arm keys
   (left −1.25 rad / right +1.25 rad) flip the RIGHT arm up to 152° on
   the current rig — those keys predate a rig revision.
3. **The V5 video's own render diverged from its data.** The V5 dance
   action actually opens with the arms down (measured 10.2° / 5.7° at
   frame 1 — the mocap window itself starts arms-down). But V5 was
   solved in Blender 5.2.3 and rendered in Blender 4.0.2, and in the
   delivered frames the arms sit held out at ~55°. The arm bones are
   steered by driver-controlled FK/IK constraint blending tied to the
   rig root, and the evidence points to those drivers not holding in
   the 4.0.2 render path, letting the arms fall back toward the
   arms-out rest. That Blender build was later removed from the
   machine, so this last link cannot be re-run — it is stated as
   evidence-bounded, not proven. V6 removes the whole class of
   failure: ONE build (5.2.3) for solve, assembly and render, and the
   gate measures the RENDERED frames, not just the data.

V5 also had no idle at all — frame 1 was a raw cut into the loop. V6
adds a true arms-down idle: a 24-frame lead-in solved from the mocap
frames just before the loop, a matching 24-frame return at the end,
and a solve-layer stance relaxation on the lead/return only (the
mocap's natural hang splays the forearms ~25° on this bulky sculpt;
upper arm +5°, forearm +14° toward straight-down, smoothstep-ramped —
the dance loop itself is untouched data).

**Idle gate (measured three independent ways):**
- FK bones at idle frame 1: 4.9° / 0.9° from vertical (target ≤ ~15°)
- Deform bones: ≤ 8.2°
- Screen-projected on the rendered start frame: upper arms 1.0° / 0.0°
  from vertical, forearms 10.5° / 6.3° — hands relaxed at the thighs

### The permanent rule (owner, 2026-11-07)

> **Natural idle = arms down, sitting and standing. The H pose
> (biceps up, arms pointed out, hands straight) may appear ONLY when
> the owner explicitly directs it (the robot, King Tut, a deliberate
> gag). Never naturally, in any idle, ever.**

### Idle audit — every natural idle asset, measured

| Asset | Upper-arm angle | Verdict |
|---|---|---|
| Standing dance idle (new in V6) | 4.9° / 0.9° | PASS |
| pose_sit_normal | 8.3° / 8.3° | already arms-down |
| pose_sit_leg_folded | 8.3° / 8.3° | already arms-down |
| pose_sit_recline | 9.2° / 9.2° | already arms-down |
| pose_sit_lean_forward | 22.8° / 22.8° | arms-down class — leaning forward onto the knees is the pose |
| pose_sit_shrug | 23.0° / 23.0°, forearms 158.8° | the shrug gesture itself — deliberate expression, kept and documented |
| idle_heroic_breathe (library) | was INERT (showed rest-pose H, 80°) | FIXED — live now, arms 9.5–17.6° across the breath |
| idle_heroic_breathe (w5r file) | was live but right arm flipped to 152° | FIXED — arms 9.5–17.6°, spine keys untouched |

The five sitting poses never had the H — the H lived in the rest pose
and in the dead/flipped idle. Corrected files (NEW files; the
originals are untouched, byte-for-byte, and the original sitting
library blob on main is unchanged):

- `sitting_pose_library_armsdown.blend` — breathe converted to live
  channels with an arms-down hang; all five `pose_sit_*` actions
  verified fcurve-identical to the original (seat translations, bent
  legs, recliner yaw exactly as saved — only the idle changed). This
  is the going-forward default sitting library.
- `cape_jones_rigged_w5r_idle_armsdown.blend` — only the 12 arm
  curves of the breathe changed; the spine/head breathing keys and
  the `led_press_R` / `snap_test_R` / `KeyAction` actions verified
  identical.

Note: in the library file CapeJones_Cape carries no Armature modifier
(pre-existing) — flagged here, out of scope for this fix.

## Fix 2 — feet grounded, gravity works

**What the floating feet actually was — measured, two compounding
bugs in the V5 solver (the mocap data is innocent):**

1. **A scrambled root axis.** The rig's root bone takes LOCAL
   location, and its local axes are rotated −90° about X — its local
   Y is world UP. The V5 solver wrote the mocap's WORLD hips vector
   straight into that local channel, so the data's vertical bounce
   played as forward/back sway and the body's height never followed
   the data at all. (Proof: setting root.location to (0, 0, 0.3)
   moved the head to world (0, −0.3, 0) — pure sideways.)
2. **No floor constraint anywhere.** The legs were solved by
   rebuilding joint directions (FK): the ankle was placed wherever
   the directions and bone lengths landed, never checked against the
   ground. Body and legs rode up together — in the delivered V5 loop
   the toes float up to **+18.8 cm** above their contact height
   (loop frames 48–50) while the pelvis travels only 8.3 cm total.
   The source clip's toes, in the same window, NEVER leave the floor
   (max liftoff ~1.5 cm, zero airborne frames).

**The V6 fix, at the solve layer:**
- Root axis conversion (world → root-local) so height data drives
  height again.
- Contact-aware leg solve: on frames where the source toe is in
  contact (≤ 2.5 cm — that is 100% of this window), the ankle target
  is pinned to flat-foot height and the sole is flattened.
- A per-frame ground snap after the full solve: the lowest toe is set
  exactly to the rig's rest contact height by trimming the root
  (applied on all 96 loop frames; max trim 5.9 cm; zero skips).

**Feet gate (measured):**
- Toe trace over the full 1,824-frame action, 498 samples: the toes
  NEVER rise above contact — max 0.000 m; deepest point is a 5 mm toe
  press. Contact frames sit at exactly 0.
- Pelvis drop at the deepest squat: **16.2 cm** (V5: 8.3 cm) — the
  squat is absorbed by knees + pelvis, the way gravity reads.
- Rendered deepest-squat frame: soles flat on the ground with
  contact shadows (see the proof sheet).

## Fix 3 — what worked is kept, and the arms stay ALIVE

Same groove, same world cycle, same one-piece cape (zoom-verified on
the sheet). And arms-down does NOT mean arms-frozen: the dance loop
is pure mocap, no damping anywhere. Shoulder swing range across a
loop tile, V6 vs V5: left 2.6–53.3° vs 2.6–54.2°, right 1.7–130.3°
vs 1.7–134.3° — the full swing of the data, preserved.

## Honest shortfalls

- The V5-render driver divergence (cause 3 of the H) cannot be
  re-run: the Blender 4.0.2 build was deleted from the machine by
  another lane. The diagnosis is evidence-bounded; the single-build
  pipeline + rendered-frame gate make the failure class impossible
  to ship silently again.
- The lead-in/return stance relaxation is a solve-layer correction,
  disclosed above — needed because data-true hang splays the
  forearms ~25° on this sculpt. The loop is untouched.
- sit_shrug's folded forearms (158.8°) are the gesture itself, kept.
- Render is EEVEE at 8 TAA samples, same as V5 (software rendering
  on this machine, ~1 min/frame under a resume-safe driver).

## Files in this PR

- `production/dance-proof-3d-v6/README.md` — this document
- `production/dance-proof-3d-v6/solve_v6.py` — the V6 solver
  (root-axis fix, grounded leg solve, ground snap, idle lead-in)
- `production/dance-proof-3d-v6/assemble_v6.py` — full-song action
  assembly (idle + loop tiles + return, world cycle)
- `production/dance-proof-3d-v6/render_v6_eevee.py`,
  `run_render_v6.sh`, `watchdog_v6.sh` — resume-safe render chain
- `production/dance-proof-3d-v6/fix_breathe.py` — the mode-aware
  idle/breathe repair used for both corrected rig files
- `production/dance-proof-3d-v6/trace_v6.json` — the full-action
  gate trace (arm angles, toe heights, pelvis)
- `production/dance-proof-3d-v6/cj-dance-proof-3d-v6-sheet.png` —
  proof sheet (arms-down start, deepest-squat feet zoom, shoulder
  zoom, cape zoom, world cycle)
- `production/dance-proof-3d-v6/cj-idle-proofs-v6.png` — zoomed idle
  proofs: corrected standing idle + all five corrected sitting poses
- `3d-assets/cape-jones-rig/sitting_pose_library_armsdown.blend` —
  corrected sitting library (new file; original untouched)
- `3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle_armsdown.blend`
  — corrected w5r idle file (new file; original untouched)
- `3d-assets/cape-jones-rig/SITTING-POSE-LIBRARY.md` — updated: the
  corrected library is the going-forward default; the permanent
  no-H-pose rule is written in
- `3d-assets/cape-jones-rig/RIG-DOCS.md` — the permanent rule +
  pointers to the corrected files

The V6 standing rig (`cape_jones_standing_v6.blend`) and the video
(`cj-dance-proof-3d-v6.mp4`, Japanese v2 mix) are delivered with the
dance-proof files alongside the V3–V5 proofs; the rig also sits next
to this folder's scripts in the working archive. Nothing in this PR
deletes or modifies an existing file other than the two doc updates
named above, which the owner's expansion explicitly ordered.
