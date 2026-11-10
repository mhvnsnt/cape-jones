# Cape Jones rig inventory + v4 diagnosis (v5 rig-first lane, 2026-11-02)

Owner's verdict on v4, which this lane answers: the dance would work if the
rig was completely fixed with industry-standard auto-rig/skinning tools;
the rig and movement still read broken and stiff. And his correction: the
dance chain used the sitting rig — the sitting position is canon, do not
change it; make a NEW standing rig. The named defect is the
shoulder→bicep→elbow chain (upper-body stiffness). The bent legs of the
sitting position are INTENTIONAL and are never treated as a defect here.

All findings below are from the files themselves (opened and measured in
Blender), the repo's own docs, and rendered evidence — not from gate files'
PASS labels.

## 1. What rigs the repo actually holds

### 1a. The 3D family — `3d-assets/cape-jones-rig/` (the only skinned 3D rigs)

- `cape_jones_rigged.blend` (95.7 MB) — custom two-layer FK/IK armature
  `CapeJones_Rig`, measured in Blender by this lane at **85 bones**.
  Deform chains + FK/IK layers blended by COPY_TRANSFORMS driven from
  `root` custom props (`ik_arm_L/R`, `ik_leg_L/R`, `ik_spine`), finger
  chains, BlenRig 6 MDEF cage present. Same body (910,374 verts,
  Preserve Volume TRUE, Corrective Smooth 0.5/3); its body additionally
  carries inert FK/IK-layer vertex groups.
- `cape_jones_rigged_w5r.blend` (92.1 MB) — **the 94-bone rig
  RIG-DOCS.md describes** (the doc's attribution to the file above is
  off; measured here from the hash-verified blob on main): full
  `spine_1..4` deform chain + `spine_fk_1..4` + `chest_fk` +
  `spine_twist`, complete finger chains, body vertex groups including
  all fingers and `spine_3`/`spine_4`. This is the bake-off-winning
  W5r-weighted flagship and the **v5 base**. (Cautionary note: a
  same-named copy in a stale local checkout on this machine is an
  85-bone variant — all v5 work uses the hash-verified blob from main,
  git sha `2a51a646…`, never the local copy.)
  Its weights are the bake-off-winning **W5r** solution: Surface Heat
  Diffuse (in-repo MIT solver `tools/weights/surface-heat-diffuse/`) +
  Preserve Volume + Corrective Smooth (0.5, 3). Body mesh
  `CapeJones_Body` = 910,374 verts. Measured in Blender by this lane:
  rig rest is near-straight-legged (knee bend 2.6°/4.2°, elbow 9.1°),
  pelvis head z = 0.409, no pose applied, armature modifier Preserve
  Volume = TRUE, Corrective Smooth 0.5/3 — matches the winning recipe
  exactly.
- `cape_jones_rigged_w5r_clean.blend` (96.8 MB) — "clean" variant; **no doc
  anywhere states what was cleaned** — flagged, not adopted blind.
- `cape_jones_rigged_w5r_idle.blend`, `..._idle_cape_STEP1.blend` — working
  variants (idle action / cape step 1), not separate rigs.
- `sitting_pose_library.blend` (96.9 MB) — **READ-ONLY CANON.** Five sitting
  pose actions (`sit_normal`, `sit_leg_folded`, `sit_lean_forward`,
  `sit_recline`, `sit_shrug`) on the 85-bone W5r rig, root bone carrying
  seat translation/yaw for the canon recliner. **This lane never writes to
  it; its blob hash is recorded before/after in the v5 PR and is unchanged.**
- The bake-off (`WEIGHT-BAKEOFF-RESULT.md`) scored W5r on 7 poses:
  rest ✅, elbow_90 ✅, head_turn ✅, arms_raised ⚠️, **knee_deep ❌,
  shoulder_raise ❌, crouch ❌** — and names its own defect zones:
  (1) right shoulder pinches/collapses on forward raise, solver asymmetry
  (Shoulder.R claims ~688k verts vs Shoulder.L ~300k) — deltoid falloff
  needs repaint; (2) feet/ankles crumple on deep knee bend and crouch;
  (3) slab artifact under thigh on deep bends; (4) cape goes rigid on
  crouch. Blender Bone Heat fails completely on this mesh (100% empty
  groups, even on a decimated proxy) — documented, measured.

### 1b. The Blender 5.2.3 toon line (PR #344) — NOT a deform rig

`blender523-rig-fixed-20261101/` and `blender523-rig-refined-20261101/`.
This lane downloaded both blends (hash-verified) and opened the refined
one in Blender 5.2.3: **17 EMPTY pegs + 11 flat drawing planes + the
Grease Pencil overlay + a reference plane. Zero armatures, zero skin
weights, zero deformable mesh.** Each arm is ONE drawing hinged at pegs;
the reports themselves state the elbow cut was not done. Its gates check
mapping/parenting/Z-order/bbox — placement, not deformation. This line
structurally cannot answer a shoulder→bicep→elbow deformation complaint:
there is no elbow in the arm and nothing deforms.
The Grease Pencil overlay (`GP_Apose_Overlay`, 4 strokes) encodes **only**
the 2D A-pose silhouette: two 21-point edge polylines + head-top +
foot-bottom (see `gp-silhouette.json`, read firsthand). It was a
rest-pose measuring tool (mean edge deviation 34.7 px → 12.8 px). It
encodes no poses, no joint limits, no weights, no motion.

### 1c. The 2D package — `cape-jones-rig/`

The 2D cutout puppet (Animate/JSFL): 28 sliced drawings, each arm and leg
ONE piece. Its own master doc states elbow/knee bends do not work without
a cut. This single-piece arm is the structural ancestor of the stiffness
the owner named; the blender523 line inherits it. Valuable canon in that
folder: KNEE-FEET-RULE (knees follow toes), ARM-FRONT-SNAP-RULE, the
joint-locked v7c coordinates the toon builds derive from. Not a 3D base.

### 1d. Side-rig line, rig-34, PRs #338/#346/#351/#357

Side-profile 2D rigs (auto/fixed/wrist-fix — narrow, honestly-scoped pose
fixes), the rig-34 sitting 3/4 line, knee-feet rule update (#346, a rule
file, no rig), belt/palm/knee-pivot trials (#351, explicitly undecided),
elbow piece-sets + angle sheets (#357, drawing substitution for the 2D
line). Choreography source worth reusing: `movement-library-clips-20261101/`
(donor timing/structure). None of these is a standing 3D rig.

### 1e. CloudRig — `production/tools/cloudrig/`

Blender Studio's CloudRig generation framework, **fully vendored in-tree**
(code, tests, docs; its `bs_utils` submodule content present as files) —
not a pointer. But no Cape Jones metarig or CloudRig-generated CJ rig
exists anywhere in the repo: it has never been run on this character.
Usable as a tool; using it = a fresh metarig fit + re-skin, the same class
of work that already failed headlessly for BlenRig 6's calibrated rig
(RIG-DOCS boundary). Not chosen as the v5 base; kept as a benchmark.

### 1f. PR #274 (v4) itself

Open, stacked on unmerged #272/#271. Its PR contains scripts +
measurements + the CMU BVH — **the rig .blend and the renders never
landed in the repo.** Every v4 quality claim rests on `measure_v4.py`
joint-angle numbers. The owner has since judged the actual deformations
broken/stiff by eye. This lane salvages v4's *methods* (facing scan,
world-space delta retarget, normalized-reach limb placement) — not its rig.

## 2. Did the v4 chain use the sitting rig? — the exact file chain

Owner's words: "You used the wrong rig — you used the sitting rig."

What the files show, precisely:

- `build_v4.py` opens **`/home/hatch/workspace/_cj-dance3d-v3/scene_v3.blend`**
  (v3's scene) — not `sitting_pose_library.blend` by name.
- That scene's character is `CapeJones_Rig` at **88 bones** + `BodyR`. This
  lane measured it: those 88 bones are the repo rig family's **85-bone
  variant** plus `cape_1/2/3` added by the v3 lane. Its rest joint angles
  and pelvis height match the family core (knee 2.6°/4.2°, elbow 9.1°,
  pelvis z 0.409 — the same numbers measured on the 94-bone file, whose
  FK layer is identical). The sitting library's five actions live on
  that same 85-bone variant. The repo's fuller 94-bone rig (§1a) was
  never used by any dance build.
- So in substance the owner is right: **the dance chain and the sitting
  library share one rig** — the 85-bone sitting-family variant — and
  that rig's weights were built and validated (bake-off pose suite +
  sitting library) around the sitting-first production, never around
  standing dance. Its documented failures (shoulder_raise ❌, knee_deep
  ❌, crouch ❌) are exactly the zones that read wrong in the dance.
- Measured nuance, stated honestly: the w5r file's REST pose is itself
  near-straight-legged — the file does not bake a sitting rest pose. The
  wrong-looking legs in the dance come from standing/dance motion solved
  onto leg weights that fail deep-bend tests and feet that crumple —
  not from a sitting pose frozen into the mesh. Either way, the fix the
  owner ordered is the fix this lane executes: sitting rig untouched,
  a NEW standing rig built and pose-gated for standing work.

## 3. Why v4 deformed broken/stiff — concrete causes, evidenced

1. **Weights were never re-solved for the new rig.** `build_v4.py`
   transfers the old groups onto Rigify DEF bones by name mapping,
   splits long bones by projection, **quantizes weights to 0.02 steps
   and prunes everything ≤ 0.01**. Whatever the old weights got wrong
   (see cause 5) was baked straight into v4, coarser.
2. **Weight groups were LOST in the transfer.** Measured on
   `rig_v4.blend`: BodyR carries only 54 DEF groups. There are **no
   DEF-toe groups at all**, and finger-segment coverage is partial
   (e.g. thumb has only segment .01 on both sides; several ring/pinky
   segments missing). Verts in those zones lost their skinning — dead,
   stiff parts by construction.
3. **Preserve Volume was OFF.** Measured: BodyR's armature modifier in
   the v3 scene has `use_deform_preserve_volume = false`, and v4 kept
   the same modifier (repointed). The bake-off's winning recipe — the
   repo's own measured standard — requires it ON. With it off, every
   bend loses volume: pinched shoulders, collapsed elbows/knees — the
   "broken" look, on every joint, all the time.
4. **The metarig was fitted by writing bone head/tail positions only.**
   Bone rolls were never recalculated, so bend axes/pole behaviour are
   approximate; and the spine was NOT fully measured — `spine.003`–
   `spine.006` head/tail positions are hardcoded numbers in the script
   (z = 0.78 / 0.83 / 0.865) that override the measured skeleton, so the
   generated torso chain's proportions differ from the body the weights
   were painted for.
5. **The inherited shoulder weights were already documented defective.**
   The bake-off's P5 shoulder_raise FAILED on this mesh (right-shoulder
   pinch/collapse, solver claiming ~688k verts on R vs ~300k on L).
   v3 then decimated the body 910k → 107,476 verts; measured on the v3
   scene, BodyR has **48,080 non-manifold edges out of 273,574 (17.6%)** —
   the decimation wrecked the topology under those weights. v4 inherited
   the result. Shoulders/biceps — the owner's named defect — were never
   repaired in any version.
6. **The rig's own muscle system was deleted in v4's working copy.**
   `build_v4.py` removes the BlenRig MDEF cage and the old rig (with its
   tuned FK/IK layers and 5-joint spine behaviour) and drives the mesh
   from the generated Rigify armature alone.
7. **The source motion itself reads stiff.** CMU 15_04's chosen window
   is an exercise-style bounce (v4's own honest shortfall): feet mostly
   planted, stepping = weight shift, and the solve damped vertical root
   motion ×0.7. Even a perfect rig would have read small on this loop;
   on this rig it read broken.
8. **The base rig's extremities were never skinned at all.** Measured on
   `cape_jones_rigged_w5r.blend` by this lane (full per-group weight
   census in the v5 build report): `hand_L` total weight = 111 verts'
   worth, `hand_R` = 189; most finger groups are **exactly 0.0**
   (index_1_L, index_2_L, index_3_L, thumb_2 both sides, most of the
   right pinky/ring chain); **`toe_L` and `toe_R` are exactly 0.0** —
   the toes have no skin whatsoever. The hands/fingers ride the forearm
   as one rigid block in every version built on this rig (that is part
   of why v3's hands read as black blocks and why v4's transfer found
   almost nothing to transfer). The bake-off's SHD run was scored on a
   20-bone test skeleton with no fingers; on the production rig the
   extremity pass was simply never done. v5 completes it (§4).

## 4. What v5 does instead (summary; detail in the v5 README)

- **Base:** the repo's own 3D family — `cape_jones_rigged_w5r.blend`
  (85-bone armature + W5r weights, the bake-off-validated file) — copied
  OUT into a new file, `cape_jones_standing_v5.blend`. Sitting files
  untouched (hashes in PR).
- **Extremity completion:** hands/fingers/toes skinned by a
  distance-falloff pass over their bone segments (pool-conserving), so
  fingers can curl and toes can bend for the first time on this rig.
- **Cape panel unification:** the sculpt's cape panels are welded into
  the body mesh, and SHD painted their verts with alternating
  pelvis/thigh allegiance down each sheet — under any leg bend the
  rows pull apart into fringe (visible in this lane's first gate run;
  the same failure family as the bake-off's crouch ❌). All leg-bone
  weight inside the back-side panel slab is moved to the pelvis, so
  the panels hang from the torso as one sheet.
- **Systems, not hand-work:** the weights stay the bake-off-winning
  Surface Heat Diffuse solution (in-repo MIT solver); Preserve Volume
  restored ON; Corrective Smooth at the winning 0.5/3; twist bones added
  by the bake-off's own `add_twist_bones()` construction; the shoulder/
  deltoid zone re-blended by a symmetric distance-falloff across the
  shoulder joint (the bake-off's named repaint, done as a construction
  that cannot be asymmetric); ankle transition tightened the same way;
  influences capped at 4 + renormalized per repo standard.
- **Hard pose gate before any dance:** scripted extreme bends at every
  joint the owner named, with zoomed deform renders (shoulders, elbows,
  hips, knees, cape hem, between legs) and cross-section volume numbers.
  The dance is attached only after the gate passes.
- **Dance:** CMU 15_04 loop retargeted onto the standing rig's own FK
  layer (world-space delta method, the repo's method), full song, EN v2
  mix (rotation: v4 used JP), same world cycle as v3/v4.
