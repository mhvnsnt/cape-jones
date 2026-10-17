# Weight Bake-Off 2026 — Cape Jones model

**Lane:** `rig/weight-bakeoff-20261017` · **Date:** 2026-10-17 · **Owner directive:** run the
Cape Jones model through EVERY weight-painting/skinning pipeline we've built across the
repos, plus open-source ones if ours aren't enough. Compare on test poses, keep the best,
wire the winner into the repo.

**Test model:** `~/workspace/cj-rev2-scratch/cape_jones_plain.glb` — 54 MB, valid glTF,
991,082 verts / 1,915,208 tris, native **0.925 m** (DO NOT RESCALE — owner scale lock).
Unrigged Tripo bake: T-pose, arms along ±Y, faces +X, cape fused behind (−X).
No skeleton, no weights, no vertex groups on import (verified headless, Blender 4.0.2).

**Common test rig (CJ-TEST skeleton):** 20 bones, built by
`tools/weights/cj_bakeoff/bakeoff.py::BONES` from measured mesh landmarks
(arm centerline z≈0.26, elbow |y|≈0.27, wrist |y|≈0.40, knee z≈−0.185, ankle z≈−0.37 —
see `docs/research/WEIGHT-BAKEOFF-2026.md` method notes). Bone placement verified:
every bone midpoint inside the mesh (KDTree nearest-surface check, worst case
Chest 0.064 m vs 0.16 m limit). The SAME skeleton is used for every entry, so the
comparison is apples-to-apples. Weights are skeleton-bound — see the handoff note
for how to carry the winning technique to the BlenRig 6 rig.

**Test poses (7):** P1 rest · P2 arms_raised · P3 elbow_90+ · P4 knee_deep ·
P5 shoulder_raise · P6 head_turn · P7 crouch.
**Acceptance:** no candy-wrapper elbows, no collapsing shoulders/hips.
**Render setup:** Cycles CPU, 480×270, 6 samples, clay material, 3/4 front view —
every proof render below was read with own eyes.

## 1. Inventory of OUR weight pipelines

| # | Pipeline | Location | What it does | How to run |
|---|---|---|---|---|
| W1 | Blender Bone Heat (`ARMATURE_AUTO`) | built into Blender 4.0.2 (GPL) | diffusion-based automatic weights | `bpy.ops.object.parent_set(type='ARMATURE_AUTO')` |
| W2 | Blender Envelope weights | built into Blender 4.0.2 (GPL) | bone-envelope distance falloff | `bpy.ops.object.parent_set(type='ARMATURE_ENVELOPE')` |
| W4 | BrutalFist `auto_rig_humanoid.py` | `brutalfist-fix/tools/animation/auto_rig_humanoid.py` | end-to-end: builds its own bounding-box landmark skeleton, then Bone Heat; exports rigged GLB | `blender -b --python tools/animation/auto_rig_humanoid.py -- in.glb out.glb` |
| W5 | bannon-video-pipe stack | `bannon-video-pipe/docs/AI_RIGGING_RESEARCH.md` §1 | Bone Heat + Armature-modifier **Preserve Volume** (true dual-quaternion skinning) + **Corrective Smooth** modifier | 3 lines of bpy (see doc) |
| W6 | bannon-video-pipe twist bones | same doc §4 | split limbs into twist segments; Copy Rotation (twist axis only, 0.5→1.0 down chain); redistribute weights with gradient falloff | scriptable headless; bakes cleanly to GLB |
| W7 | BlenRig 6 mesh-deform cage | `production/tools/blenrig6` (`blenrig.bind_mdef_modifiers`) | cage deformed by armature → Mesh Deform bind on the body (BlenRig's core skinning method; full guide-fitted bind belongs to the rig lane) | convex-hull cage → decimate → `ARMATURE_AUTO` on cage → `meshdeform_bind` |
| — | Corrective shape keys (driver-driven) | bannon-video-pipe doc §3 | sculpt corrective at problem pose, drive via bone rotation; exports to glTF as morph targets | Pose Shape Keys addon (Blender Studio, OSS) — render/game portable, listed for the rig lane |
| — | Blender weight cleanup tools | built-in | Normalize All, Mirror, Data Transfer (`VGROUP_WEIGHTS`), smooth brushes — scripted cleanup after any auto pass | `bpy` / Weight Paint mode |

**Searched, not applicable:** `wmxix-mesh-decode`/yukes-extractors (no repo in workspace —
only the lead name from the task; nothing found), `western-heart/tools` (no weight/skin
scripts — searched `*weight*`/`*skin*`), cape-jones `tools/` + `production/pipeline`
(no skinning scripts; `coa_tools2/operators/edit_weights.py` is 2D cutout-animation,
not 3D skinning), `brutalfist-fix/tools/weight-paint-pwa` (three.js weight-*painting*
PWA viewer — manual painting UI, not an auto-weight pipeline; noted for the manual lane).

## 2. Open-source pulls (2026 research, verified licenses)

| Tool | License | Verdict |
|---|---|---|
| **Surface Heat Diffuse Skinning** v3.4.2 (meshonline) — "never fails" Bone Heat alternative | MIT | ✅ PULLED → `tools/weights/surface-heat-diffuse/` (Linux solver compiled from `src/` via `build_linux.sh`; headless flow documented in `HEADLESS.md`; binary gitignored as build artifact) |
| DV Skin Tools (weight-painting workflow tools) | GPL-3.0 | documented only — requires Blender 4.2+ (we run 4.0.2); not auto-skinning |
| Easy Weight (Blender Studio) | Blender/OSS | documented only — paint-mode QoL, not a weight generator |
| Voxel Heat Diffuse Skinning (meshonline) | **paid** | ❌ skipped — no-paid law |
| Adaptive Auto Skinning (Jessy Leite, 80.9% artist-match on 202-char benchmark, Sept 2026) | **paid** (Superhive) | ❌ skipped — no-paid law; revisit if a free tier appears |

## 3. Results

Scoring per pose: ✅ clean · ⚠️ minor artifact · ❌ fails acceptance.
"n/a" = entry produced no usable weights, poses not judgeable.

### W1 — Blender Bone Heat (built-in)

> `Warning: Bone Heat Weighting: failed to find solution for one or more bones`
> (verbatim, 307 s on the full mesh) → **20 empty vertex groups, 991,082/991,082 verts
> (100.0%) with NO weights.** All 7 pose renders identical to rest pose.

| P1 | P2 | P3 | P4 | P5 | P6 | P7 |
|---|---|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a | n/a | n/a |

**Verdict: FAIL.** Blender's heat solver cannot handle this 991k-vert Tripo mesh
(non-manifold bake, dense). This is the failure the open-source pull (W3) exists to fix.

### W1p — Bone Heat on decimated proxy (105k verts), Data-Transfer to full mesh

> `Warning: Bone Heat Weighting: failed to find solution for one or more bones`
> (verbatim) → **0/105,415 proxy verts weighted (9 s), 0/991,082 full-mesh verts.**
> Rescue variant fails too — the problem is the Tripo mesh topology (non-manifold,
> internal faces), not just density.

**Verdict: FAIL.**

### W3 — Surface Heat Diffuse Skinning (meshonline, MIT) ✅ best raw weights

Solver: `shd` compiled from `src/` (g++), run headless with addon defaults
(res=128, loops=5, samples=64, influence=8, falloff=0.2, sharpness=3).
**991,082/991,082 verts weighted (0.00% unweighted)** — the "never fails" claim holds.
Torso weight audit: mean Foot weight on torso 0.0000; dominant torso bones are
Spine/Chest/root/Shoulders/Hips — sensible. Renders read:

| Pose | Result |
|---|---|
| P1 rest | ✅ |
| P2 arms_raised | ⚠️ arms reach overhead, but L/R asymmetric — one shoulder kinks (weight counts: Shoulder.R 688k vs Shoulder.L 300k verts — solver has directional bias) |
| P3 elbow_90 | ⚠️ both forearms bend forward 90°, minor inner-elbow crease, **no candy-wrapper, no collapse** |
| P4 knee_deep | ❌ thighs swing forward but feet crumple on one side; flat slab artifact under thigh (mis-weighted cape/thigh verts left behind) |
| P5 shoulder_raise | ❌ one shoulder pinches/collapses at the deltoid (asymmetric — the other side is clean) |
| P6 head_turn | ✅ clean yaw, no neck tearing |
| P7 crouch | ❌ body crouches well but one foot crumples into a blob; slab artifact persists |

**Verdict: MIXED — best automatic weights of the bake-off (only entry that weights
the full mesh at all), but asymmetric with real failures at shoulders (P5) and
feet (P4/P7).** Needs the W5/W6 modifier stack and/or manual cleanup at shoulders.

*Pose-euler corrections made during this entry (verified via bone world-direction
measurements, now in the shared `POSES` dict): mirrored bones need the SAME
z-euler sign (not mirrored); thigh-forward = `(0,0,-1.9)`; head yaw = `(0,1.0,0)`;
spine-forward = `(0,0,-0.35)`. The first W3 render pass used wrong eulers for
P3/P4/P5/P6/P7 — those renders are superseded; only the re-rendered set counts.*

### W2 — Blender Envelope weights

| P1 | P2 | P3 | P4 | P5 | P6 | P7 |
|---|---|---|---|---|---|---|
| ✅ | ❌ | ❌ | ❌ | ⚠️ | ✅ | ⚠️ |

P2: severe candy-wrapper/pinch at the raised shoulder (upper arm twisted into a
rope). P3: volume loss/pinch at both elbows. P4: cape+thigh verts smeared into a
flat sheet under the legs. P5: armpit webbing/crease. P7: body crouches OK but the
cape becomes a rigid surfboard (cape needs its own bones/cloth — separate lane).

**Verdict: FAIL** — 3/7 fail, envelope capsules can't handle this mesh.

### W4 — BrutalFist auto_rig_humanoid.py (our pipeline, as-is)

**Verdict: FAIL, two independent causes (verbatim evidence):**
1. `Warning: Bone Heat Weighting: failed to find solution for one or more bones` —
   its `bind_automatic_weights()` (plain `ARMATURE_AUTO`) fails on this mesh exactly
   like W1.
2. **Y-up assumption broken:** `build_humanoid()` derives height from `hi.y - lo.y`;
   a Blender-imported glTF is Z-up, so the landmark skeleton is built sideways —
   measured: `Hips head=(+0.00,-0.02,-0.00) tail=(+0.00,+0.03,-0.00)`,
   `Head tail=(+0.00,+0.43,-0.00)` — the whole Hips→Head chain runs along +Y
   (through the arm axis) at z≈0 instead of vertically. Any GLB imported to Blender
   (Z-up) gets a sideways rig from this script.
3. Bonus: the script has no `root` bone (its variable named `root` creates a bone
   named `Hips`), so `root:loc` poses KeyError — the run died at P4
   (`KeyError: 'bpy_prop_collection[key]: key "root" not found'`).

*Flagged for the brutalfist lane: fix the axis assumption (use Z-up / detect up-axis)
— the bake-off ran it unmodified per "run it don't just document it."*

### W7 — BlenRig-6-style mesh-deform cage (convex hull, decimate 0.002)

Mechanically works (`meshdeform_bind`, bound=True, 40 s), but the auto-cage came out
at **11 verts** — giant tetrahedra turn the arms into flat paddles on every pose.

**Verdict: FAIL as implemented** — the technique needs a fitted cage (that's the
rig lane's BlenRig guide work); a naive convex-hull auto-cage can't carry it.
W7b (denser relaxed cage) re-tests with a saner cage.

### W7b — mesh-deform cage, denser (decimate 0.15 + light smooth + 1.06 scale)

**Run completed 2026-10-17 (overnight-idle-pipeline):** bind + weighting succeeded —
`CJ_Cage` 731 verts, `meshdeform_bind` bound=True, bone-heat weights on the cage
sensible (Head 260 / Foot.L 218 / Foot.R 211 / Shin.L 194 / UpperArm.L 155 verts…).
Full-mesh Cycles pose renders **OOM-blocked on this 8 GB VM**: 2 attempts, both
`Killed` (exit 137) at ~5.47 GB Blender peak during depsgraph sync of the
991,082-vert mesh. A/B test with the MESH_DEFORM modifier disabled renders fine,
and W7's 11-vert-cage blend renders fine — the 731-vert deform evaluation itself
is what blows the RAM budget. Verdict therefore from cage-level evidence
(`tools/weights/cj_bakeoff/render_w7b_cage.py`, proofs `W7b_cagefront_*.png`):

- The cage **does** track the armature (P2: arm sections rise overhead; P5:
  shoulder sections lift) — the mechanism works.
- But the denser cage **does not fix W7's paddle problem**: decimate 0.15 +
  smooth×3 melts the thin arm protrusions into the torso — only 71/731 verts
  (9.7%) sit in the arm regions (|y|>0.35) while 206 verts (28%) bunch on the
  head cap; leg tessellation is asymmetric (legL 69 vs legR 189). Bone-heat on
  the cage also bleeds across center (UpperArm.L weights span y ∈ [-0.08, 0.46]
  — the W3 directional-bias problem again, one level down).
- Conclusion: a naive convex-hull auto-cage can't carry the limbs no matter the
  density — the technique needs a **fitted** cage (rig lane's BlenRig guide
  work), exactly as the W7 verdict said. Full-mesh pose proof deferred to a
  bigger machine; the winner stays **W5r**.

**Verdict: FAIL (structural, not just RAM)** — denser auto-cage confirmed
insufficient. Do not pursue W7c+ with denser hulls; the next step for this
technique is a fitted cage, owned by the rig lane.

### W8 — Pinocchio auto-rig (auto-rig lane's winner, Baran & Popović, LGPL-2.1/MIT)

Full-pipeline entry like W4: the auto-rig lane's committed artifacts
(`production/tools/pinocchio/` on origin/main) run through this lane's pose suite.
**Critical finding first:** the artifacts committed on main are from the lane's
BROKEN first run, not the fixed re-run their doc describes:
- `work/cj_pinocchio_skeleton.json`: left-arm chain collapsed down the torso —
  verified numerically: `lshoulder=[-0.027,0.270,0.035] → lelbow=[0.044,0.094,0.025]
  → lhand=[0.025,-0.057,0.047]` (elbow 4 cm off-center, 18 cm below the shoulder —
  inside the torso, not at the arm). I reproduced this exactly by running their
  committed `rig` binary on `work/cj_vox.obj` as-is (identical joint positions).
- The fixed run's files (`cj_vox_std.obj`, `cj_std_*`) were **never committed** —
  not in the `work/` tree on main.
- Their committed Blender pose proof `proof/pinocchio_pose_front.png` renders as a
  **mangled blob** (read with own eyes) — consistent with posing the broken weights,
  contradicting the doc's "no explosions" claim. The rest proof is clean (weights
  don't matter at rest), and `proof/skeleton_placement.png` shows correct 18/18
  placement (from the fixed run's data, not the committed JSON).

Per "run it don't just document it," I reproduced the fixed run: yawed
`cj_vox.obj` so the character faces +Z (Pinocchio's requirement — verified: arms
along ±Z and nose at +X in the raw OBJ, so `R_y(-90°): (x,y,z)→(-z,y,x)`), ran the
committed `rig` binary → **perfect 18/18**: `lshoulder=[-0.085,0.273] →
lelbow=[-0.262,0.269] → lhand=[-0.429,0.242]`, symmetric. Imported the yawed mesh
(111,010 verts) + fixed skeleton + fixed weights into Blender, built the armature,
measured bone world directions, and posed with verified eulers
(shoulder-raise = local X; elbow = local Z; thigh-forward = X −1.9; knee-flex = X +).

| Pose | Result |
|---|---|
| P1 rest | ✅ clean T-pose (voxel-remeshed mesh, smooth) |
| P2 arms_raised | ❌ **severe webbing** — arms reach overhead but the whole shoulder/chest/cape mass drags up into a giant tent-like sheet between the arms |
| P3 elbow_90 | ⚠️ elbows bend ~90° but with pinching and a fin-like protrusion artifact at the joint |
| P4 knee_deep | ⚠️ moderate bend looked clean; deep-bend eulers under-applied in this pass (inconclusive at full depth) |
| P5 shoulder_raise | ❌ shoulder collapse/webbing at the deltoid |
| P6 head_turn | — not run for this entry |
| P7 crouch | ⚠️ moderate crouch OK; deep crouch inconclusive (same under-application as P4) |

**Verdict: MIXED-FAIL — does not beat W5r.** Pinocchio's weights are very
smooth/diffuse (PDE-based, like heat weights but smoother), which is kind to
organic bends but drags the FUSED cape + shoulder mass on big motions (P2/P5).
Contributing factor: this entry runs on the voxel-remeshed proxy where the cape
is fused to the body — cape drag is partly a mesh artifact, not purely weights.
The auto-rig lane's real win stands: **the skeleton placement is excellent
(verified 18/18 symmetric)** — worth pulling for skeleton generation; the weights
need the W5-style treatment or manual cleanup before they beat surface-heat-diffuse
on this character.

*Recommendation to the auto-rig lane: commit the fixed run's `cj_vox_std.obj` +
`skeleton.json` + `weights.bin` (replacing the broken first-run artifacts) and
re-render the Blender pose proof — the current committed proof image is a mangled
blob and the current committed weights pair with a collapsed left arm.*

## 4. Comparison matrix & winner

Score key: ✅ clean · ⚠️ minor artifacts, usable · ❌ fails acceptance · — not run

| Entry | P1 rest | P2 arms↑ | P3 elbow90 | P4 knee | P5 sh.raise | P6 head | P7 crouch | Verdict |
|---|---|---|---|---|---|---|---|---|
| W1 Bone Heat | ✅* | — | — | — | — | — | — | **FAIL** — 0/991k verts weighted, all renders = rest (*P1 only "passes" trivially) |
| W1p proxy+transfer | ✅* | — | — | — | — | — | — | **FAIL** — same heat failure on proxy |
| W2 Envelope | ✅ | ❌ | ❌ | ❌ | ⚠️ | ✅ | ⚠️ | **FAIL** — candy-wrapper shoulders, elbow pinch, cape sheet |
| W3 Surf.Heat Diffuse | ✅ | ⚠️ | ⚠️ | ❌ | ❌ | ✅ | ❌ | **MIXED** — best raw auto weights; asymmetric, shoulder/foot failures |
| W4 BrutalFist | — | — | — | — | — | — | — | **FAIL** — bone-heat failure + Y-up bug + no root bone |
| W5r W3+DQ+CorrSmooth | ✅ | ⚠️ | ✅ | ❌ | ❌ | ✅ | ❌ | **WINNER** — best on the suite; smoothing doesn't rescue P4/P5/P7 |
| W6r W3+twist bones | =W3 | =W3 | =W3 | =W3 | =W3 | =W3 | =W3 | no measurable gain on hinge suite (twist not exercised) |
| W7 mesh-deform cage | ✅* | — | — | — | — | — | — | **FAIL** — 11-vert cage → paddle limbs |
| W7b dense cage | — (cage tracks ✅) | — | — | — | — | — | — | **FAIL** — 731-vert cage: arms melted (9.7% arm verts), full-mesh eval OOMs 8GB VM; fitted cage needed |
| W8 Pinocchio | ✅ | ❌ | ⚠️ | ⚠️ | ❌ | — | ⚠️ | **MIXED-FAIL** — great skeleton (18/18), weights web on big motions |

**Winner: W5r (Surface Heat Diffuse + Preserve Volume/Dual-Quaternion + Corrective
Smooth).** It is the only entry that weights the full 991k-vert mesh at all AND
survives the hinge poses without candy-wrapping or collapse (P3 ✅, P6 ✅, P1 ✅;
P2 ⚠️ asymmetric but intact). Nothing else in the bake-off beats it: Pinocchio's
W8 has the better skeleton generator but worse deformation on this fused-cape mesh;
every Blender-native auto method fails outright on the topology.

Known defect zones to fix with manual cleanup (documented for the rig lane):
asymmetric shoulders (Shoulder.R 688k vs Shoulder.L 300k verts — solver bias),
foot crumple on deep knee/crouch (P4/P7), right-shoulder pinch on raise (P5),
flat slab artifact under thigh (mis-weighted cape verts). The handoff note
`3d-assets/cape-jones-rig/WEIGHT-BAKEOFF-RESULT.md` carries the exact recipe.

## 5. AI-tooling status

| Tool | Status | Detail |
|---|---|---|
| GitHub Copilot CLI v1.0.98 | ✅ LIVE | PAT-authenticated 2026-10-17 ~00:08 (fine-grained "Copilot CLI" token, `COPILOT_GITHUB_TOKEN` in `~/.bashrc`). Used for repo research/iteration in this lane. `.github/copilot-instructions.md` landed with repo conventions (scale lock, colorway `#731AE5`, branch→PR→merge, `xvfb-run -a` + `env -u PYTHONPATH`, verify-before-claiming). |
| Aider (`~/workspace/tools/aider`) | ❌ key-blocked | Needs `GEMINI_API_KEY` — env var confirmed EMPTY (read-only check). Ready-to-run task once the key lands (below). |
| Cline CLI | ❌ not installed + key-blocked | `cline` not on PATH (npm globals show only `@github/copilot`). Needs install + `GEMINI_API_KEY`. Ready-to-run task below. |
| Colab (`notebooks/colab/` pattern) | ➖ not needed | Weight computation is CPU-bound bpy/shd work that runs fine headless on the VM; no GPU step justified — extending the notebook pattern would be show, not substance. |
| Browser/OAuth flows | ➖ NEEDS-PARENT-BROWSER | Per lane rules, no live-browser OAuth attempted (Mixamo/Cinevva/Tripo web riggers stay documented-only). |

**Aider ready-to-run (the moment `GEMINI_API_KEY` lands):**
```bash
export GEMINI_API_KEY="$GEMINI_API_KEY"   # from secure storage, never chat/files
cd ~/workspace/cape-jones-bakeoff
aider --model gemini-2.5-pro \
  --message "In tools/weights/cj_bakeoff/bakeoff.py, add a W8 entry: Laplacian-smoothed
  distance-falloff weights (closest-bone distance, smoothstep falloff, 20 Laplacian
  smooth iterations, normalize). Reuse build_skeleton/POSES/apply_pose. Keep headless
  (blender -b) compatible, no new dependencies."
```

**Cline ready-to-run (once `cline` CLI is installed and keyed):**
```bash
cline "In the cape-jones repo on branch rig/weight-bakeoff-20261017, read
docs/research/WEIGHT-BAKEOFF-2026.md section 3, then implement the documented
follow-up with the lowest effort-to-gain ratio as a new commit on this branch.
Do not touch other lanes' branches."
```

## 6. Method notes (reproducibility)

- Blender 4.0.2 headless: `xvfb-run -a env -u PYTHONPATH <blender> -b --python ...`
  (bare `-b` segfaults — libEGL; system numpy breaks Blender's Python).
- glTF import ≈ 69 s; Cycles CPU 480×270 @ 6 samples ≈ 35 s/frame on 1.9M tris.
- Workbench/matcap rendering segfaults under xvfb here — Cycles used instead.
- 7 GB VM RAM: one Blender at a time; BVH on the full mesh OOMs (RC=137) —
  KDTree used for the bone-inside-mesh check instead.
- Scratch (blends, full-res renders): `~/workspace/weight-bakeoff-scratch/` (NOT /tmp —
  512M tmpfs). Proof renders referenced below are copied to `docs/research/bakeoff-proofs/`.

## 7. Proof renders

*Copied here as entries complete. Every image below was read with own eyes in this lane.*

W8 (Pinocchio fixed-run): `W8_P1_rest.png` (clean T-pose, front),
`W8_P2_arms_raised.png` (severe shoulder/chest/cape webbing — ❌),
`W8_P3_elbow_90.png` (bends with pinching — ⚠️),
`W8_P4_knee_deep.png`, `W8_P5_shoulder_raise.png` (deltoid collapse — ❌),
`W8_P7_crouch.png`. W8_P6 not run.
