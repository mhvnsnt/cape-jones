# TEAM-CONVERSATION.md — Cape Jones rig-perfection wave

Coordination log for the lanes working the rig perfection wave. Each lane posts what it
touched, what it needs from others, and what it deliberately did NOT touch.

---

## 2026-10-18 — rig-perfection / best-rigging-tech research lane (restart)

**Lane:** autonomy research + Wiggle 2 pull + wiring. Branch: `pull/wiggle2-20261017`.

**Touched (mine, committed in my PR):**
- `docs/research/BEST-RIGGING-TECH-2026.md` — full autonomy ranking (20 systems, grades A–D),
  updated with the 2026-10-18 restart addendum.
- `production/tools/wiggle2/` — vendored Wiggle 2 v2.2.4 (GPL-3.0, byte-identical to upstream),
  proof script + 3 proof renders, `CAPE-JONES-WIRING.md` (new: chain-build/bind/bake template).

**Verified, not relayed:** addon enables in headless Blender 4.0.2; proof renders own-eyes;
upstream hash match. Rig introspection: `CapeJones_Rig` = 94 bones, **zero cape bones** —
the cape chain gets built by the wiring, not found.

**Needed from other lanes:**
- **Spine lane:** run the Wiggle cape wiring only on your SETTLED rig file, never a WIP .blend.
  The wiring is additive (new armature + modifier), it never edits existing bones.
- **GPU lane:** Puppeteer vs TokenRig vs UniRig neural-skinning bake-off against W5r stays yours.
- **GNM head / MPFB lanes:** face and parametric body stay yours — no overlap.

**Deliberately NOT touched (other lanes' work, left in the tree):**
- `3d-assets/cape-jones-rig/spine-lane/`, the `cape_jones_rigged_w5r.blend` edit
- `3d-assets/face-rig/` (scratch files, `cj_face_*`, `face-rig/README.md` edit)
- `docs/research/GNM-HEAD.md`, `tools/pulled/GNM/`, GNM section of `tools/pulled/README.md`
- `production/tools/mpfb2/`

## 2026-10-18 ~04:30 — shared-checkout collision (resolved)

The `~/workspace/cape-jones` checkout is shared between lanes. Mid-lane, another agent switched
the checkout to `render/cape-turntable-20261018` and committed `e4637038` (cape cloth turntable)
while this lane's commit was being made — this lane's commit `cc6d6a6b` landed on TOP of their
branch. Fixed without touching their work: cherry-picked `cc6d6a6b` → `2feb0274` onto
`pull/wiggle2-20261017` (clean base on `origin/main`, only this lane's 10 files), pushed,
then mixed-reset their branch back to `e4637038` (their uncommitted changes intact, verified
28 uncommitted entries preserved). **Lesson for the coordinator: give each lane its own
worktree** (`git worktree add`) — sharing one checkout across lanes that commit is how
cross-lane commits happen.

---

## 2026-10-17 ~21:45 CDT — parametric-body / MPFB lane (subagent)

**Owner directive:** "pull it [MPFB] in completely, wire it up completely into the repo."
Branch: `pull/parametric-body-20261017`.

**Done (verified — own eyes on renders, files hashed):**
- MPFB2 v2.0.18 pulled COMPLETELY into `production/tools/mpfb2/` (106 MB, upstream
  commit 3af0cd5; code GPL-3.0, assets CC0-1.0). Blender 4.5.3 LTS installed at
  `~/workspace/tools/blender-4.5/` (MPFB2 requires Blender 4.2+; repo's 4.0.2 can't run it).
- Headless MPFB2 proven: create human (19,158 verts), semantic morph targets,
  163-bone default rig, render — `production/tools/mpfb2/mpfb_proof.py`.
- **WIRED:** `3d-assets/cape-jones-rig/cape_jones_mpfb_wired.blend` (147 MB, built
  from `cape_jones_rigged_w5r_clean.blend`, source untouched) — 5 semantic morphs
  as DRIVEN shape keys on the real 910,374-vert CJ mesh (`MPFB_bulk/height/
  shoulders/belly/limbs` ← custom props `mpfb_*` via SINGLE_PROP drivers),
  transferred via KD-tree from scripted T-posed MPFB humans. Plus
  `MPFB_FullSkeleton` (163 bones: spine01–05, neck01–03, segmented twist limbs,
  full fingers/toes) scaled to CJ's 0.925 m in-scene.
- **Animation proven:** scripted extreme poses on the MPFB rig — deep knee bend,
  elbow 90°, spine twist+bend — with programmatic sign-checks, zero hand-tooling
  (`mpfb_anim_proof.py`). Mixamo-topology rig (52 bones) generates headless;
  `mapmixamo` operator confirmed in-tree. Real Mixamo FBX files need an Adobe
  account (browser lane).
- Docs: `docs/research/PARAMETRIC-BODY.md` (full landscape ranking + concrete
  porting plan §5), `production/tools/mpfb2/WIRING.md`. Proofs rendering to
  `3d-assets/cape-jones-rig/mpfb_proofs/`.
- ANNY (CC0) proven loading locally via body-models numpy backend. MHR
  (Apache-2.0, ATLAS integrated) verified via published sources; local pull
  deferred (disk was 100%, cleared my own failed partials only).
- **Correction, stated plainly:** the 2026-10-13 claim of a Forge3D GNM-pipeline
  proof (commit `43ca3db`) is CONTRADICTED — that commit exists neither in the
  local Forge3D clone nor on GitHub (checked `gh api`). Do not cite it. The
  wiring in this repo is the first verified implementation.

**Needed from other lanes:**
- **Spine lane:** `MPFB_FullSkeleton` in the wired blend is your measured
  reference — `spine01–05` + `neck01–03` joint positions at CJ scale. Take them.
- **Deformation lane:** porting plan is `docs/research/PARAMETRIC-BODY.md` §5.
  `production/tools/mpfb2/src/mpfb/data/rigs/standard/weights.default.json` is
  the free twist-bone weight-ramp reference. MPFB muscle targets
  (`l-upperarm-muscle-*`, `torso-muscle-*`) are the corrective shape library.
- **GNM-head lane:** MPFB2 2.0.16's expression toolset (ARKit `faceunits01`) is
  in-tree if you need shape-key expression infra — no overlap taken.

**Deliberately NOT touched:** `cape_jones_rigged_w5r_clean.blend` (read-only
source), `3d-assets/face-rig/`, `tools/pulled/GNM/`, spine-lane dir, any WIP blends.

**Open:** belly/shoulders morphs subtle (7–8 mm) vs bulk (50 mm) — strengthen pass
with stronger targets queued before PR; MHR local pull (disk); real Mixamo FBX
retarget (Adobe account); Adaptive Auto Skinning license check + bakeoff.

---

## 2026-10-18 — GNM-head lane (Rig Perfection Wave)

**Lane:** Google GNM-Head study + CJ parametric face rig. Branch: `pull/gnm-head-20261017`.

**Pulled (licenses verified):**
- `tools/pulled/GNM/` — google/GNM @ 5cf11d78, **Apache-2.0** (commercial OK), code only
  (788K, 73 files; weights/.h5/textures/gifs stripped per repo convention; model weights
  download on first use via the loader and were NOT pulled). PROVENANCE.md documents
  commit, license, and what was stripped.
- NOT pulled: Nathan Dickson's "GNM Head Importer" Blender add-on (free Gumroad download,
  no stated license — documented in PROVENANCE.md, not vendored). Built our own UI instead.

**Studied:** GNM = template + linear identity(253)/expression(383) blendshape bases + 4-joint
LBS; 383 = 100/eye + 150 lower face + 32 tongue + 1 iris; semantic sampler maps 20 named
expressions → param vectors + blend_expressions(). Full study: `docs/research/GNM-HEAD.md`.

**Built (all original code, steal-like-an-artist — GNM's architecture, OUR cartoon face):**
- `3d-assets/face-rig/cj_parametric_face.py` → builds `cj_face_parametric.blend` on the
  existing mouth kit: `CJ_FaceParams` 20-float expression vector in GNM's 4 groups
  (EYES / BROW / LOWER / TONGUE / IRIS=pupil_toggle). Canon locked: white eyes default,
  pupils on emphasis only; 17 mouths stay hard-cut swap-set (parametric layer drives
  jaw/smile/frown TRANSFORMS on holders, never blends mouth geo). ADDED mask-brow cards
  (sheet 05: "the mask's dynamic movement" — GNM has no brow basis) + shape-keyed tongue.
- `3d-assets/face-rig/cj_face_presets.py` — 21 presets (8 expression-matrix entries +
  4 eye-darts + comedic extras) + `blend_presets()`, mirroring GNM's semantic sampler.
- `3d-assets/face-rig/cj_face_ui.py` — installable N-panel add-on: grouped sliders +
  preset buttons (Dickson-style UI, our code).
- `proof/parametric_face_proof.png` — 16-cell contact sheet, own-eyes verified against
  sheet 05 checklist (8 expressions + 4 darts + happy/tongue/wink/smug).

**Headless gotchas documented in `3d-assets/face-rig/README.md`:** ID-prop sets don't
re-evaluate drivers without `update_tag()`; `hide_render` doesn't propagate parent→child
in renders (visibility drivers on every descendant); `obj.copy()` carries base values —
freeze bakes from `evaluated_get(depsgraph)`.

**Deliberately NOT touched:** `cj_mouth_kit.blend` + `build_mouthkit.py` (face lane owns),
spine-lane dir, mpfb/wiggle2 dirs, `cape_jones_rigged_w5r*.blend`, any WIP blends.
