# Cape Jones — Rig / Rigging Asset Inventory + Verdict Draft (v5 rig-first lane)

- Repo: `mhvnsnt/cape-jones` (private), read via `gh api` against `main`
  (root tree SHA `832b342cedf1f2e7a157524b535e26e2a5a0b29e`), 2026-11-02.
- READ-ONLY pass: no pushes, no PRs, no repo edits. This file is a draft for the parent lane.
- Method note: gate-result / verify JSONs were read but **not trusted as deform proof**.
  A gate "PASS" in this repo checks structure (part mapping, parenting, Z-order, bbox,
  frame counts). Only rendered stills / clips count as visual evidence, and none of the
  gates anywhere in the repo render a posed shoulder→bicep→elbow deform close-up.

## Owner rulings applied throughout (not contradicted)

- The **sitting rig / sitting pose library is READ-ONLY canon**. Its bent legs are
  INTENTIONAL (he sits ~90% of the show) and are never logged below as a defect.
- The **named defect** is shoulders / biceps / upper-body stiffness — the
  shoulder→bicep→elbow chain — present in v4 (PR #274) and in the Grease Pencil
  refined rig line (`blender523-rig-refined-20261101/`).
- v4 (PR #274) was built from scratch on Rigify from the v3 scene's MPFB-wired model;
  the owner judged its deformations broken/stiff by eye. Its own measurements do not
  override that verdict.

---

## 1. Per-asset table

### A. The 3D rig family — `3d-assets/cape-jones-rig/`

| Path | What it is | Size | Rig system | Evidence shipped | Verdict |
|---|---|---|---|---|---|
| `3d-assets/cape-jones-rig/cape_jones_rigged.blend` | Original full-body 3D rig deliverable (0.925 m, scale locked) | 95,744,707 B (~95.7 MB) | Custom two-layer FK/IK deform armature `CapeJones_Rig`, **94 bones** (RIG-DOCS.md), driven as direct Armature deform; BlenRig 6 v4.0.1 MDEF muscle cage fitted and present in the blend but **staged, not active** in the final (RIG-DOCS says so plainly) | RIG-DOCS.md (full bone layout, FK/IK switches on `root`, 5-joint spine lane with measured twist distribution); `deform-proofs/` before/after PNGs | **Soundest 3D base in the repo — with a documented shoulder defect zone (see bakeoff).** See §2. |
| `3d-assets/cape-jones-rig/cape_jones_rigged_w5r.blend` | Same rig carrying the winning W5r weights | 92,125,095 B (~92.1 MB) | 85-bone W5r rig (per SITTING-POSE-LIBRARY.md) + Surface Heat Diffuse weights + Preserve Volume + Corrective Smooth (0.5, 3 iters) | WEIGHT-BAKEOFF-RESULT.md with a real 7-pose suite | **Sound technique, honestly scored:** P1 rest ✅, P3 elbow_90 ✅, P6 head_turn ✅; P2 arms_raised ⚠️; **P4 knee_deep ❌, P5 shoulder_raise ❌, P7 crouch ❌**. The P5 failure is the shoulder zone — the same chain the owner later named stiff. |
| `3d-assets/cape-jones-rig/cape_jones_rigged_w5r_clean.blend` | "Clean" W5r variant | 96,835,930 B (~96.8 MB) | W5r (as above) | No separate report found for what "clean" changed | **Suspect-by-omission:** largest of the standing variants, no doc states its delta from `w5r`. Do not adopt blind; diff inside Blender first. |
| `3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend` | W5r + idle action | 96,975,121 B (~97.0 MB) | W5r + `idle_heroic_breathe` action (preserved in the sitting library too) | `idle-test/` folder in same dir | Plausible working file; no standalone verdict doc. |
| `3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle_cape_STEP1.blend` | Idle + cape step-1 work | 96,903,454 B (~96.9 MB) | W5r + cape lane step 1 | Cape scripts alongside (`cape_build_sheet.py`, `cape_sim_bake.py`, etc.) | Intermediate lane file, not a deliverable rig. |
| `3d-assets/cape-jones-rig/sitting_pose_library.blend` | **Sitting pose library — READ-ONLY CANON** | 96,943,918 B (~96.9 MB) | 85-bone W5r rig, full-body FK; five Actions marked as Pose Assets: `sit_normal`, `sit_leg_folded`, `sit_lean_forward`, `sit_recline`, `sit_shrug` | SITTING-POSE-LIBRARY.md + `sitting-poses/*.png` — one Cycles proof render per pose, eye-verified (no chair/floor clipping, feet grounded exactly, ankle residual 0.064) | **CANON — DO NOT MODIFY, DO NOT "FIX" THE LEGS.** Bent legs are the design (seat height 0.37 vs 0.925 m character; thighs ~60° down, shins vertical — documented as correct in the library doc itself). Cape drape validation against these poses is still PENDING on the cape lane (their note, not a rig defect). |
| `3d-assets/cape-jones-rig/RIG-DOCS.md` | Rig documentation | 11,553 B | — | Self-describing; candid about the BlenRig 6 boundary: the full 2424-bone BlenRig control rig could **not** be re-proportioned headlessly to 0.925 m (constraint network explodes/diverges), so only its MDEF cage was used | **Sound doc** — unusually honest; its limits are stated, not hidden. |
| `3d-assets/cape-jones-rig/WEIGHT-BAKEOFF-RESULT.md` | Weight bake-off handoff (2026-10-17) | 4,878 B | W5r = Surface Heat Diffuse (in-repo MIT solver `shd`) | 7-pose suite scores + defect list | **Sound and self-incriminating in the right way.** Known defect zones it names itself: (1) **right shoulder pinches/collapses on forward raise (P5), kinks overhead (P2)** — solver asymmetry, Shoulder.R claims ~688k verts vs Shoulder.L ~300k, deltoid falloff needs hand repaint; (2) feet/ankle crumple on deep knee bend/crouch; (3) slab artifact under thigh on P4/P7; (4) cape goes rigid board on crouch. Losers documented (Blender Bone Heat total failure, Envelope candy-wrapper shoulders). |
| `3d-assets/cape-jones-rig/SITTING-POSE-LIBRARY.md` | Sitting library doc | 3,503 B | — | Measured chair/seat data taken from the blend files, pose-by-pose notes | **Sound doc** (canon reference). |
| `3d-assets/cape-jones-rig/deform-proofs/` | Before/after deform proof renders | 8 PNGs, ~483–592 KB each | — | `elbow_crease_before/after`, `elbow_topdown_before/after`, `head_turn_before/after`, `jaw_side_before/after` | **Partial evidence.** Real rendered deform proof — but only for elbow crease, head turn, jaw. **There is no shoulder-raise deform proof in this folder**, which is exactly the named defect chain. A claim of "shoulders fixed" anywhere would have no rendered support here. |
| `3d-assets/cape-jones-rig/sitting-canon/` | Sitting canon support: retarget/drop/fix scripts + `final_front.png`, `final_threeq.png` | scripts 1.5–10 KB; PNGs ~381–391 KB | W5r sitting line | Two final renders | Canon support material; read-only in spirit (sitting line). |
| `3d-assets/cape-jones-rig/` (other subdirs: `deform-scripts/`, `deform-wave2/`, `fingertip-fix/`, `idle-test/`, `mpfb_proofs/`, `proofs/`, `sitting-poses/`, `sitting-redo/`, `sitting-take3/`, `spine-lane/`, `test-poses/`, `tools/`, `cape-turntable/`, `.scratch/`) | Lane working folders around the 3D rig | — | Mixed | Varies | Working history, not separate rigs. `sitting-redo/` + `sitting-take3/` are earlier sitting attempts superseded by the canon library. |
| `mocap_retarget.py` (repo root) | Mocap retarget script: CMU 113_15 ("sit in chair and get up") onto the 94-bone rig, world-space delta math with butt→seat contact solving | 8,283 B | Targets `CapeJones_Rig` (asserts exactly 94 bones) | Script only; output `proof/sitting_mocap.blend` is written to a local worktree path (`/home/hatch/workspace/wt-mocapsit/...`), source FBX from `/home/hatch/workspace/mocap-sit/113_15.fbx` — neither is in this repo path | **Suspect as a reproducible asset:** math is documented and plausible, but it is hard-wired to local absolute paths and a sitting clip; it is not a standing/dance retarget solution as shipped. |

### B. The 2D puppet rig package — `cape-jones-rig/`

| Path | What it is | Size | Rig system | Evidence shipped | Verdict |
|---|---|---|---|---|---|
| `cape-jones-rig/CAPE-JONES-RIG.md` | Master doc for the 2D cutout puppet: 28 sliced transparent PNGs from the owner's uploaded sheets, layer stack, pivots, parenting, hand/mouth/eye swap symbols, JSFL build into Adobe Animate | 5,574 B | 2D cutout puppet (Animate/JSFL), **not a 3D rig** | `contact-sheet.png`, `assembly-preview.png` (T-pose reassembly), `sliced/MANIFEST.json` | **Sound for what it is, and honest about its core limit:** the sheet draws each arm as ONE piece and each leg as ONE piece — "elbow bend does NOT [work] without a cut", same for knee. This single-piece arm is the structural root of the shoulder→bicep→elbow stiffness the owner named in the Blender descendants of this package. |
| `cape-jones-rig/INDUSTRY-STANDARDS-PULL-20261031.md` | Standards mapping audit | 10,049 B | — | Self-audit table | **Mixed:** candid in places (ACES in a colour-managed tool 0/1, viewed Blender render 0/1, Harmony NOT installed "do not claim it is"), but several rows are "YES as mapping" — i.e. a paper mapping to the v7c rig, not a wired, rendered result. Treat "YES as mapping" as **unproven**. |
| `cape-jones-rig/FREE-STACKS-INDUSTRY-STANDARDS.md` | Free-stack wiring doc | 3,431 B | Names Blender 5.2.3 LTS Grease Pencil, OpenToonz/Synfig, LUT workflow | Doc only | Reference doc; no rig evidence of its own. |
| `cape-jones-rig/METHODS-PULLED-20261031.md` | Methods/research pull log | 2,267 B | — | Doc only | Reference doc. |
| `cape-jones-rig/KNEE-FEET-RULE.md` | Owner rule: knees direction == toes direction, per frame, both legs (universal form landed by PR #346, see §3) | 7,514 B | 2D rig rule | Rule text | Canon rule for posing/QC; not a rig. (Sitting-canon bent legs are a pose, not a knee/toe direction violation.) |
| `cape-jones-rig/ARM-FRONT-SNAP-RULE.md` | Owner rule: arm chain snaps in front of torso (whole chain, per arm, per frame) with Z-order values | 17,661 B (also a copy at repo root, 18,132 B) | 2D rig rule | Rule text; implemented as keyed drawing-Z in the blender523 line | Canon rule; the blender523 gate's `crossed_snap_z` check verifies this rule's numbers, not deformation. |
| `cape-jones-rig/joint_locked_rig*.py` + `locked-*.json` (v3–v8) | The actual 2D rig definition used downstream: joint coordinates, locked T-pose/A-pose defaults (`joint_locked_rig_v7c.py` is the coordinate source the Blender 5.2.3 builds cite) | ~5.4–8 KB each | 2D joint/pivot data (1100×1500 canvas) | `rig-apose-v6-transparent.png`, `rig-apose-v7c-clean-transparent.png`, assembly previews v2–v8 | **Sound as 2D ground truth** — the blender523 fixed/refined reports derive every anchor from v7c + `locked-default-rig.json` + PARTS-LABEL-AUDIT, and that derivation checks out against the docs. Still 2D: pivots, not bones-with-weights. |
| `cape-jones-rig/experimental-25-20261031/group-b-pose-motion/` | Pose/motion experiments: `GROUP-B.md` (20,230 B), `pose_angle_tool.py` (10,311 B), `pose-angles-20261031.json`, `mediapipe-attempt-log-20261031.txt`, `proofs/` | as listed | 2D pose-angle tooling + a MediaPipe pose-estimation attempt | GROUP-B.md + proofs folder | Experimental 2D tooling. The MediaPipe item is an *attempt log*, not a working mocap pipe. Not a dance-rig base. |
| `cape-jones-rig/` (remaining ~150 subfolders: `rig-34-*`, `cut-limbs-*`, `reposes-*`, `clips-*`, dance-*, gap-close-*, etc.) | The 2D production swarm: per-fix dated folders for the FLA/2D line | — | 2D | Per-folder sheets/renders | Out of v5-3D scope except as ancestry: the `rig-34-*` line is the 2D 3/4-view sitting rig family (see root `rig-34-...` below). Not inventoried folder-by-folder here. |

### C. The Blender 5.2.3 toon line (2D pieces in Blender) — root dated folders

**Critical framing for the whole section:** these are **image-plane cutout rigs inside
Blender** — flat drawings on planes parented to empty "pegs". There is no mesh, no skin
weights, and no deformation anywhere in this line. An arm is one whole drawing rotating
at the shoulder peg; the forearm peg exists but the drawing is never cut at the elbow
(both reports state cutting is banned / not done). That is precisely why the owner's
named stiffness (shoulder→bicep→elbow) is *structural* here, not a tuning miss.

| Path | What it is | Size | Rig system | Evidence shipped | Verdict |
|---|---|---|---|---|---|
| `blender523-rig-fixed-20261101/cape_jones_toon_blender523_FIXED.blend` | "Fixed" toon rig: corrects the earlier build's Arm1/Arm2 + Leg1/Leg2 swap, cape collar Z, cape placement, neck/head seating | 114,612 B | Blender **5.2.3 LTS**, EEVEE; 17 pegs, 11 drawings, 6 FK chains (spine/cape/arm1/arm2/leg1/leg2); 48-frame test clip (rest f1, crossed-chest snap f25, flex f37, shuffle f48) | Report (8,308 B) + 3 before/after stills (~962–974 KB each) + 3 renders + test clip MP4 + SFX clip + `gate-result.json` + `pose-table.json` + `blender523-fixed-verify.json` | **Sound as a 2D-in-Blender assembly fix; NOT deform evidence.** The renders are real and do show the placement corrections (collar as shoulder band not bib, cape at shoulder level, head seated with 0.31 overlap). But `gate-result.json` "PASS 12/12" checks only mapping/parents/Z-order/spread-angle — it cannot and does not test deformation. The report itself admits a true arms-up flex is **not claimed** (whole arm rotated up puts the fist upside-down) and the "flex" is a 120° wide-out spread. Approval: 0/1 (report's own status line in the refined successor). |
| `blender523-rig-refined-20261101/cape_jones_toon_blender523_REFINED.blend` | Refinement of the fixed build using a Grease Pencil overlay of the 2D A-pose as ground truth: rest arms −20°/+20°, rest legs −9°/+10°, leg planes +0.15 units | 118,221 B | Same peg/plane system, Blender 5.2.3 LTS + GP object `GP_Apose_Overlay` (4 strokes) | Report (4,768 B) + 5 renders incl. `pose-rest-GP-OVERLAY.png` + `gate-result-refined.json` (`PASS_WITH_KNOWN_LIMITS`) + `gp-silhouette.json` + verify JSON with per-row edge measurements | **The most honestly-labelled item in this line — and still the owner's named stiffness.** Mean silhouette edge deviation improved 34.7 px → 12.8 px vs the A-pose, which is a *rest-pose outline match*, not articulation quality. Its own known-limits list concedes: whole pieces cannot match cut-limb elbow/knee bends; rest legs are straight angled lines, knees sit too far out, shins slant where the A-pose shins are near-vertical; arms-up flex still not claimed. This is the "Grease Pencil refined rig line" the owner judged stiff in the shoulder→bicep→elbow chain — the GP work refined the *silhouette*, it did not add an elbow. See §4 for what the GP overlay actually encodes. |
| `blender523-rig-fixed-20261101/build_blender523_rig_fixed.py` / `blender523-rig-refined-20261101/build_blender523_rig_refined.py` | Build scripts for the above | 14,758 B / 19,039 B | — | Headers derive every anchor from PARTS-LABEL-AUDIT-20261031 lines 38/178, `joint_locked_rig_v7c.py`, `locked-default-rig.json`, CAPE-JONES-RIG.md pivots; transform X=(x2d−550)/200, Y=5.0−y2d/200 | **Sound provenance** — no invented pegs; the derivation chain is checkable and checks out. Invocation in-script is generic: `blender --background --python build_blender523_rig_fixed.py`, output dir default `~/workspace/cape-jones-rig/blender523-rig-fixed-20261101` (env `CJTOON_OUT`). No absolute Blender binary path is pinned in these scripts. |

### D. The side-rig line (2D profile rigs) — root dated folders

| Path | What it is | Size | Rig system | Evidence shipped | Verdict |
|---|---|---|---|---|---|
| `side-rig-auto-20261101/` | Automated side rig: single global scale derived from the model sheet, joint anchors detected at runtime (grey joint-ball circularity filter), no hand-typed per-piece coordinates. `side-rig-auto-20261101.blend` (436,066 B), spine JSON, grey + colour idle/bent renders | blend 436 KB; report 8,056 B; `build_auto.py` 19,174 B | PIL assembly + Blender **4.5.3 LTS** armature `SideRigArmature_Auto` | REPORT + before/after scaling sheet + 4 renders | **Method sound, superseded:** its own successor report (wrist-fix) says the auto rigs "were still hand-tooled PIL pastes" in effect for the hands. Two finished poses only. |
| `side-rig-fixed-20261101/` | Anatomy fix of the side rig: un-flips the bent arm/forearm/fist (flexion must go anterior/+x), bicep stays on the front side, cape moved to the back | no .blend — PNG assemblies + manifests with FK pivots; report 2,766 B | PIL/FK-pivot assembly (1400×1600), tools in `tools/` | before/after flip sheet, idle + bent renders (colour + grey), 5 gate tools all PASS incl. a negative test (flipped manifest FAILS, proving the checks catch the owner's exact complaint) | **Sound within its scope, honestly limited:** report states a full FK animation chain "is not built in this fix — these are two finished poses". The negative-test gate is the best QC practice found anywhere in this inventory. |
| `side-rig-wrist-fix-20261101/` | Wrist fix, bent pose only: hands bone-parented to forearm bones so the hand follows the wrist — no wrist cut, no separate hand placement | `side-rig-wrist-fix-20261101.blend` 1,015,573 B; report 6,384 B | Blender **4.5.3 LTS**, armature `SideRigArmature_WristFix`, 14 bones, 17 image planes, `parent_type=BONE` | One render (bent, grey) + `verify_wrist.py` plane-gate | **Sound narrow fix.** Honest gaps stated: the fused bent open-hand piece can't be a hand-bone child without cutting, so the open hand is NOT in this rig (fist only); only the bent pose built, no idle. One pose of evidence for a one-pose claim — proportionate. |
| `rig-34-locked-neck-v4-cape-fix-20261101/` (landed by PR #338) | 2D 3/4-view ("rig-34") locked sitting rig, neck v4 + cape fix | manifest JSON 3,650 B; `build_cape_fix_v4.py` 8,034 B | 2D rig-34 line (sitting) | 2 sitting pose stills + sit-idle MP4 + sit-lean MP4 (in `animation-lean/`) + chat-sized GIF/MP4 pairs | Sitting-line material — adjacent to the sitting canon family, **not** the 3D sitting library and not a standing rig. Evidence matches its modest claim (idle/lean clips exist and are playable-sized). Not deform-tested beyond the two clips. |
| `arm-snap-last3-fix-20261101/` (landed by PR #344) | Fix for the last-3-frames arm-snap in the A/C dance template placeholders: snapped-frames list + xsheet CSV, recut GIF/MP4s | report 5,428 B; sheets ~567–605 KB | 2D template timing fix (pose-dialect successor clip) | A/B/C last-3 sheets + fixed A and C GIF/MP4 + successor pose-dialects MP4 | **Sound as a timing/Z-order fix on placeholder templates.** It fixes *when/where* the arm snaps in a 2D template clip; it is not rig work and gives the stiff arm chain nothing new to bend with. Note the filenames' own honesty: `TEMPLATE-PLACEHOLDER-*`. |

### E. Dance / movement material

| Path | What it is | Size | Rig system | Evidence shipped | Verdict |
|---|---|---|---|---|---|
| `dance-test-20261101/` | Dance test composite: existing CJ dance material over canonical room / painted CJ23 / stage CJ09 / night-city CJ29 backgrounds | GIF 7.6 MB; silent MP4 1.8 MB + EN/JP excerpt MP4s; 12 check stills 1.0–2.8 MB | 2D composite test | `DANCE-TEST-REPORT-20261101.md` (7,983 B) + frame-check stills across all backgrounds + flash CSV/JSON | A compositing/background test, not a rig. Useful as proof the 2D clips sit in scenes; says nothing about 3D deformation. |
| `movement-library-clips-20261101/` | Donor movement library: 8 extracted template clips (Gumball dance/fight, Foster's pose-swap, Smiling Friends pose-swap, Scooby step, Nick baked-cache walk, Johnny Bravo flex-dance, Richard/Scooby gang-step), each GIF+MP4+WAV | clips 118 KB–3.4 MB | Donor-show timing/structure reference (per FREE-GAME use: craft/timing, not their characters/names) | `MOVEMENT-LIBRARY-20261101.md` (10,686 B), `CLIPS-20261101.json`, `GATE-RESULTS-20261101.md`, `TEMPLATE-CHARACTER-WORKFLOW-20261101.md` | **Sound as choreography source material** — this is the timing/structure library a v5 dance should be built *from*. It is not itself a CJ rig. |
| `movement-dance-presets-20261101/` | A/B/C structure presets: Cape-Jones-shaped placeholder characters animated on Smiling Friends (A, C) and Foster's (B) structures, clean + arm-snap-fixed versions | GIF/MP4 ~308–653 KB each + WAVs | 2D template placeholders | `CLEAN-REPORT-20261101.md`, `PRESET-INDEX-20261101.md` | **Placeholders by their own labelling.** They prove the donor structures transfer onto a CJ-shaped figure in 2D; they are not the 3D dance and must not be presented as one. |
| `anims/` | Show EP01 animation exports: `anims/show/cape-jones/*.glb` (idle, stance, strike light/heavy, hit, hit-launch, KO, portal flight, cape channel flip — 103–167 KB each), Pantera GLBs, EP01 proof PNGs/MP4, choreography + proof-index docs | GLBs ~62–167 KB | Low-poly GLB action exports (show pipeline) | `EP01-PROOF-INDEX.md`, proof stills incl. `stance-ik-frame30.png`, `upright-frame25.png` | Finished show exports, not master rigs — far too small to contain the 92–97 MB master blends' mesh/weights. Relevant as evidence the character has shipped *some* full-body motion in the show line; not a v5 base. |

### F. CloudRig — `production/tools/cloudrig/`

| Path | What it is | Size | Rig system | Evidence shipped | Verdict |
|---|---|---|---|---|---|
| `production/tools/cloudrig/` | Blender Studio's CloudRig rig-generation extension, vendored into the repo: `README.md` (4,273 B), `pyproject.toml`, `requirements*.txt`, `tests/` (full upstream test suite incl. `test_generate_metarigs.py`, `test_pose_consistency.py`), `docs/metarig_generate.mp4`, and the extension itself under `CloudRig/` (`__init__.py`, `properties.py` 37,767 B, `generation/`, `rig_components/`, `rig_component_features/`, `metarigs/`, `operators/`, `ui/`, `utils/`, `translations.py` 483,590 B, LICENSE) | full tree | CloudRig (Rigify-based generation, Blender Studio, for Blender ~4.1–5.0 per its README's example rigs) | Upstream tests + docs video in-tree | **VENDORED, NOT a submodule pointer — see §5.** No CJ-specific metarig, generated rig, or report anywhere in the repo shows CloudRig was ever actually run on Cape Jones. |

---

## 2. Which existing rig is the soundest STANDING base — and why

**Answer: the 3D W5r family in `3d-assets/cape-jones-rig/` — specifically the
`cape_jones_rigged.blend` armature (94-bone custom FK/IK, RIG-DOCS) carrying the W5r
weights (`cape_jones_rigged_w5r.blend`, 85-bone pose set) — is the only credible
standing base for v5. With one large, named caveat below.**

Why it wins by elimination and by evidence:

1. **It is the only true skinned 3D deform rig in the repo.** Everything in the
   blender523 / side-rig / rig-34 lines is flat image planes on pegs or bones — there
   is no mesh to deform, so "fixing stiffness" there means re-drawing and re-cutting
   artwork, not rigging. The sitting library is the same W5r family but is canon-locked
   to sitting and read-only. PR #274's Rigify rig is not on main at all (see §3).
2. **It is the only rig with a measured pose suite.** The bake-off ran 7 poses and
   published failures (P4/P5/P7) alongside passes — no other asset in the repo submits
   to that test. Its spine lane has measured twist distribution (45° → 9/18/27/36/45°
   across five joints, waist radius ≥96.9% preserved), and `deform-proofs/` contains
   real before/after deform renders (elbow, head, jaw).
3. **Its FK/IK design is dance-capable on paper:** per-limb IK/FK switches on `root`,
   elbow/knee pole targets, finger chains, 5-joint spine with FK + IK modes — the
   control set a standing dance needs, already built and documented.

**The caveat (this is the v5 work, not a reason to pick a different base):** the W5r
shoulder zone is *documented defective in the repo's own bake-off* — P5 shoulder_raise
❌, P2 arms_raised ⚠️, right-shoulder pinch/collapse with a measured solver asymmetry
(Shoulder.R ~688k verts vs Shoulder.L ~300k) and an explicit instruction to repaint
the deltoid falloff by hand. That is the same shoulder→bicep→elbow chain the owner
named stiff in v4 and in the GP refined line. So: **base = W5r; first v5 job = the
shoulder/deltoid weight repaint + a rendered shoulder-raise deform proof (the proof
`deform-proofs/` conspicuously lacks), before any mocap is solved onto it.**
Also resolve the undocumented `w5r_clean` delta before choosing between `w5r` and
`w5r_clean` as the literal starting file.

Runner-up, for a different job: if v5's deliverable were a *2D-in-Blender* standing
figure, `blender523-rig-refined` is the best-labelled starting point — but it cannot
bend an elbow (whole-piece arms by design), so it cannot answer the owner's stiffness
verdict and is **not** recommended as the v5 dance base.

---

## 3. PR evidence — #338, #344, #346, #351, #357 (merged) and #274 (open)

| PR | Title / merged | Claims (from body) | Evidence actually shipped | Gap check |
|---|---|---|---|---|
| **#338** | "Batch D1: side rig auto + wrist fix + FLA choose side/back + v4 cape fix + top5 fixed Blender render" — merged 2026-11-01T20:26Z, 42 files | Lands the side-rig-auto, side-rig-wrist-fix, rig-34 v4 cape fix folders + FLA choose sheets + top5 Blender render fix | Exactly the folders in §1D + `fla-choose-side-back-20261101/` (choose sheets, contact sheets, measurements.json) + `top5-software-20261101/` (render-fix doc, fixed PNG, fixed .blend). Body honestly notes: two large full GIFs (16 MB/32 MB) skipped, still on disc; "Approval of all landed content remains 0/1" | Claims match files. No deform claim made; none needed. |
| **#344** | "Batch D6: Blender 5.2.3 rig fixed + arm-snap last-3 fix + refined rig with Grease Pencil overlay" — merged 2026-11-01T20:50Z, 39 files | Lands §1C + §1D arm-snap folders | All files listed in §1C/§1D incl. both .blends, both gate JSONs, GP silhouette JSON, all renders | Claims match files. The *gate* claims inside are structural (see §1C) — the PR body itself only claims the folders landed, which is true. |
| **#346** | "Batch D8: Universal knee-feet rule update" — merged 2026-11-01T20:55Z, **1 file** | Updates ONLY `learning-remembering-gate-20261101/rules.json`: the 12:07 CST universal rule (knees direction == toes direction, both legs, per frame) supersedes the 11:30 leg1/leg2 exception (R04b), which was for one bundle/clip only | The single rules.json modification | **No rig asset in this PR at all** — it is a posing/QC rule correction. Correctly labelled as an update, not a silent overwrite. |
| **#351** | "Batch E4: side rig next steps, belt/palm trials" — merged 2026-11-01T23:10Z | Lands Batch B into **`batch-b-side-rig-next-20261101/`** (note: a new folder, not the root `side-rig-*` folders): standalone side open hand, neck-gap fix, FK chain frames + GIF/MP4, back rig v2 (.blend + standing render), 3/4-back trial (.blend), back-sitting trials, knee/shin pivot trials A/B/C, belt/palm trials | Trial sheets, contact sheets, measurements.json, 2 .blends, FK frames — all present in the file list | Body explicitly makes **no decisions**: back-sitting S-A/S-B/S-C, knee pivot A/B/C, palm and belt picks are "all Mars-only picks, still owed", approval 0/1. Evidence = trial options, not a finished rig. Anyone citing #351 as a completed side rig is overstating it. |
| **#357** | "Push-everything: elbow 90deg + native sole boot + angle sheets 2-4" — merged 2026-11-02T03:29Z | Lands `production-extensions-elbow-sole-20261101/` (elbow bend piece sets at 0/45/90° ±, PIL + Blender isolated elbow .blends with cap/nocap renders, sole boot builder) + `production-extensions-20261101-angle-sheets-234/` (bird's-eye / worm's-eye / diagonal-lunge derived assemblies + Z-pieces) | Piece PNGs, contact sheets, measurements, 2 isolated elbow .blends, reports, manifests | This is **piece production for the 2D line**, not a rig: elbow bends exist as *separate drawn pieces* (drawing substitution), which is a legitimate 2D answer to elbow bending — but nothing here wires them into a single animatable rig, and the PR body (unusually terse vs #338/#344) makes no verification claims beyond size+SHA-after-merge. |
| **#274** (OPEN) | "3D dance proof v4: Rigify auto-IK rig + CMU mocap loop (v3 stiffness fix)" — open, head `feature/cj-dance-proof-3d-v4-20261031`, base is the v3 branch (stacked on unmerged #272 ← #271) | Rigify metarig fitted to measured joints + 5-bone cape `limbs.spline_tentacle`; `rigify_generate()` → **741-bone** full IK rig; v3 skin weights transferred to DEF bones; CMU 15_04 mocap retargeted (world-space torso deltas + IK hand/foot targets, finger distribution, verlet cape); 96-frame loop; measured acceptance: elbows 57.7°/41.0° range, wrists ~164°/162°, spine 27.1°, knees 54.2°/58.3°, torso-band travel 11.7%, 96/96 distinct frames | **In the PR's file list: scripts only** (`build_v4.py`, `solve_v4.py`, `render_v4.py`, `measure_v4.py`, `bvh_analyze.py`, `bvh_facing_scan.py`, `make_sheet.py`), `measurements.json`, the CMU BVH (`3d-assets/animation/mocap-cmu/15_04.bvh`), research doc, README. **The .blend and the rendered MP4/sheet are NOT in the PR** — the body says the MP4 (75.79 s, 960×540) + sheet were "delivered with the lane report", i.e. outside the repo | **The central evidence gap of this inventory.** Every v4 quality claim rests on `measure_v4.py` numbers + a README; the actual rig and render never landed in the repo, the stack it sits on (#271/#272) is itself unmerged, and the owner has since judged v4's deformations broken/stiff by eye. The body's own shortfall list (exercise-style routine not salsa, feet mostly planted, exaggerated toe ratio, coupled ring/pinky) is honest — but nothing in-repo lets a v5 lane inspect, reuse, or even verify the 741-bone rig. **Do not build v5 on v4; at most, salvage its method (facing-scan clip selection, world-space delta retarget) from the scripts.** |

---

## 4. What the Grease Pencil overlay (refined rig) actually encodes

From `blender523-rig-refined-20261101/BLENDER-RIG-REFINED-REPORT-20261101.md`,
`blender523-refined-verify.json`, and `gp-silhouette.json` itself:

- The overlay is a Grease Pencil object `GP_Apose_Overlay` containing **4 strokes**,
  traced from the **alpha silhouette of the 2D A-pose**
  (`rig-apose-v7c-clean-transparent.png`): left edge, right edge, head top, foot bottom.
- `gp-silhouette.json` is exactly that: two polylines of 21 (x, y) points each for the
  left/right silhouette edges (y from 3.735 down to −1.265 in Blender units), a 2-point
  head-top segment, and a 2-point foot-bottom segment. **That is all it encodes** — a
  static rest-pose outline at one scale (200 px = 1 unit), placed at Z 0.25 in front of
  a reference image plane (5.5 × 7.5, Z 0.20). It stays in the .blend, hidden from the
  clean renders; `renders/pose-rest-GP-OVERLAY.png` is its proof render.
- Its function was **measurement, not animation**: per-row left/right edge comparison
  (10 rows, y=300..1200) between the Blender rest render and the 2D A-pose produced the
  headline improvement (mean edge deviation 34.7 px → 12.8 px) and drove the rest-pose
  adjustments (arms −20°/+20°, legs −9°/+10°, leg planes +0.15).
- It encodes **no** pose library, no timing, no joint limits, no weight/deform data,
  and nothing about the shoulder→bicep→elbow chain in motion. It made the *standing
  still* outline match the drawing more closely. Calling the refined rig "GP-driven"
  beyond silhouette-matching would be an overclaim; the report itself does not make
  that claim.

## 5. Is CloudRig usable as-is?

**Yes as a tool, no as a Cape Jones rig — and it is genuinely vendored, not a pointer.**

- The task brief asked whether `production/tools/cloudrig/` is "actually vendored or
  just a submodule pointer". Finding: **the code is in-tree.** `CloudRig/` contains the
  full extension (generation, rig components, metarigs, operators, UI, 483 KB of
  translations), and even its one declared submodule is present as real files:
  `.gitmodules` (181 B, *inside* `production/tools/cloudrig/`, not at repo root — the
  repo root has no `.gitmodules`, it 404s) declares only
  `CloudRig/bs_utils` → `blender_studio_utils` (HTTPS, pinned 88556987), and
  `CloudRig/bs_utils/` in the repo contains actual files (`hotkeys.py` 21 KB,
  `properties.py` 11.7 KB, `geonode_util.py`, LICENSE, etc.), not a gitlink stub.
  The upstream test suite is in-tree too.
- So a lane can install/load it in Blender (README: add the Cloud Human metarig via
  Add → Armature → CloudRig MetaRigs, then Generate) without fetching anything.
- **But:** there is no CJ metarig, no CloudRig-generated CJ .blend, and no report of a
  CloudRig run anywhere in the repo. "Usable as-is" means the *generator* is present
  and complete; fitting it to the 0.925 m CJ mesh + re-skinning would be new work —
  and note the cautionary precedent in RIG-DOCS: BlenRig 6's calibrated control rig
  could not be re-proportioned headlessly to this character. CloudRig generation is
  interactive/metarig-fit work; budget it as a build, not a switch-flip.
- Version fit: CloudRig's own README examples span Blender 4.1–5.0, compatible with
  both Blender versions the repo lanes use (below).

## 6. What Blender version / path the repo lanes use

There is **no single pinned binary** — three versions appear, by lane:

| Lane | Version | Path / invocation (as recorded in-repo) |
|---|---|---|
| Blender 5.2.3 toon line (§1C) | **5.2.3 LTS** (`blender523-*-verify.json`: `"blender": "5.2.3 LTS"`; FREE-STACKS doc: "Blender 5.2.3 LTS Grease Pencil") | Generic `blender --background --python build_*.py` — **no absolute binary path in the scripts**; whichever `blender` is on PATH must be 5.2.3. Output default `~/workspace/cape-jones-rig/blender523-*/`. Refined report notes headless EEVEE needed `Xvfb + LIBGL_ALWAYS_SOFTWARE=1` (plain background run failed on libEGL and was discarded). |
| Side-rig Blender builds (§1D) | **4.5.3 LTS** (stated in both side-rig-auto and side-rig-wrist-fix reports) | Run via their `build_auto.py` / `build_blender_rig.py` inside Blender 4.5.3. |
| 3D rig / weight bake-off era (§1A) | **4.0.2** | Explicit path in WEIGHT-BAKEOFF-RESULT.md: `~/workspace/tools/blender/blender-4.0.2-linux-x64/blender`, run as `xvfb-run -a env -u PYTHONPATH … -b --python …`. (Note for the parent lane: per the workspace TOOLS.md, `~/workspace/tools/` was archived to a GitHub release on 2026-10-31 and the local copy deleted — this binary is archive-only until pulled back.) |
| `mocap_retarget.py` | Unversioned | `blender -b 3d-assets/living_room.blend --python mocap_retarget.py` with hard-coded local input/output paths (see §1A). |

## 7. Claims that lack rendered deform evidence (flag list for the parent lane)

1. **PR #274 / v4** — all deformation-quality claims: numbers + README only; rig and
   render never landed in the repo; owner eye-verdict since: broken/stiff. (§3)
2. **blender523 fixed "PASS 12/12" and refined "PASS_WITH_KNOWN_LIMITS" gates** — the
   checks are mapping/parenting/Z-order/bbox assertions. The shipped stills do evidence
   *placement*, but no gate or render anywhere in this line evidences *deformation* —
   the rig has no deformable mesh. The refined report's own known-limits are the
   honest part; the PASS labels are not deform proof.
3. **INDUSTRY-STANDARDS-PULL rows marked "YES as mapping"** — paper mappings to the
   v7c rig (e.g. rigging-standards row), explicitly without a wired/rendered result.
4. **W5r shoulder zone** — inverse case: here the repo *does* have evidence, and it is
   negative (bake-off P5 ❌ + named repaint instruction). Any future "shoulders fixed"
   claim for the 3D line must ship a rendered shoulder-raise proof; `deform-proofs/`
   currently has none.
5. **PR #351 back-rig / knee-pivot / belt / palm items** — trial options awaiting
   owner picks (per its own body); not finished-rig evidence.
6. **`cape_jones_rigged_w5r_clean.blend`** — a 96.8 MB variant with no doc stating
   what was cleaned; unverifiable as shipped.

## 8. Bottom line for v5

- Base: **W5r 3D family** (§2), first job = shoulder/deltoid weight repaint + rendered
  shoulder proof, then mocap.
- Salvage methods, not rigs, from v4's scripts (facing scan, world-space delta
  retarget, IK-target solving) and choreography from `movement-library-clips-20261101/`.
- Do not build on: the blender523 plane rigs (no elbow exists to fix), the sitting
  library (canon, read-only, sitting-only), or v4's unlanded Rigify rig.
- CloudRig is present and complete if the lane wants a generated-rig experiment —
  as a fresh build with a metarig fit, not as an existing CJ asset.
