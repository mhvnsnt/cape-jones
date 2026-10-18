# BEST RIGGING TECH 2026 — Autonomous Systems Ranking

**Date:** 2026-10-17 · **Restart:** 2026-10-18 (worker died in daemon restart mid-PR; picked up fresh — verified the lane's work, finished the wiring, filed the PR) · **Lane:** rig-perfection-wave / best-in-class research
**Owner directive (verbatim):** "keep doing more research on things that could help us get this done — especially all of my complaints, and especially things that are really autonomous, that'll do it automatically... auto-rigging and auto-boning, auto-scanning things... same for getting the animations and getting the skin and the meshing and all that right — with the animations and stuff — without it being bullshitted and hand-tooled all the way."
**Earlier directive:** "research the top most high tech, high quality, best things you can use — open source, free, free APIs, brand-new 2026 things AND things that have been worked on for a long time with legacies, full industry-standard production-grade stuff. Pull in the winners."

**Method:** 2026 sources only (80.lv, CG Channel, StraySpark 2026 roundups, Blender Studio docs, project repos). No training-data guesses. License verdicts are the pull/skip decision. Nothing commercial was cracked or pirated — paid tools are documented honestly, never pulled.

**Scope note:** GNM head work and parametric-body/ML-deformation/muscle deep research belong to sibling lanes (body-equivalent lane, MPFB lane). This doc covers rigging, skinning, correctives, cloth/secondary, frameworks, retargeting, and free APIs — and references, not duplicates, the sibling lanes.

## Autonomy grading

| Grade | Meaning |
|---|---|
| **A** | Fully automatic: mesh in → result out, no artist touch |
| **B** | Auto + verify: one click, then eyeball/tweak |
| **C** | Guided: system does the heavy lifting, artist steers |
| **D** | Manual with good tools |

## THE AUTONOMY RANKING (money table)

Ranked by autonomy first, quality second. "In repo" = already vendored. "PULLED" = this lane.

| # | System | Category | Autonomy | License | Status | Why it wins |
|---|---|---|---|---|---|---|
| 1 | **Puppeteer** (ByteDance Seed, NeurIPS 2025 Spotlight) | auto-rig + auto-skin + video→anim | **A** | Apache-2.0 ✅ | In repo (`production/tools/ml-autorig/puppeteer/`) | Mesh → skeleton + neural weights + animation from video, one pipeline. First open production-ready system. The autonomy champion. |
| 2 | **TokenRig / SkinTokens** (VAST-AI-Research, Tripo team) | auto-rig + auto-skin | **A** | MIT ✅ | In repo (`production/tools/skintokens-autorig/`) | One command: mesh → full skeleton + dense weights. Same team as the Tripo mesh generator. |
| 3 | **Make-It-Animatable** (Tencent, CVPR 2025 Highlight) | auto-rig + auto-skin | **A** | MIT ✅ | In repo (`production/tools/ml-autorig/make-it-animatable/`) | <1s, works on **arbitrary-pose** input (not just T-pose) — directly attacks re-rig pain. |
| 4 | **afk-rig** (afk.ai) | auto-rig + anim library | **A** | MIT ✅ (anims CC0) | In repo (`production/tools/afk-rig/`) | Local, no account, CLI/MCP, 9 skeletons, **240+ CC0 animations**. Auto-fit joints ≈2.4% height accuracy. Caveat: limbs touching body need weight fixes. |
| 5 | **W5r** (in-repo recipe: Surface Heat Diffuse + Preserve Volume/DQ + Corrective Smooth) | auto-skin | **B** | MIT ✅ (solver vendored at `tools/weights/surface-heat-diffuse/`) | In repo, bake-off winner | Only pipeline producing usable full-mesh weights on the Tripo mesh (Blender Bone Heat fails 100%). Needs manual cleanup in 2 zones. |
| 6 | **UniRig** (VAST-AI-Research) | auto-rig + auto-skin | **B** | MIT ✅ | In repo (GPU notebook) | Two-stage predecessor of TokenRig; documented fallback. |
| 7 | **Wiggle 2** (shteeve3d) | auto secondary motion (cape/cloth/hair jiggle) | **B** | GPL-3.0 ✅ | **PULLED this lane** (`production/tools/wiggle2/`) | Spring physics on bone chains, bakeable to keyframes, wind + collision. Verified working on our Blender 4.0.2 headless. Directly attacks the stiff-cape complaint with a SYSTEM. |
| 8 | **Mixamo** (Adobe) | auto-rig + anim library | **B** | Free w/ Adobe ID; **terms check before commercial use** | Browser lane | Fastest free auto-rigger + huge mocap library. Rigs are basic, no face. |
| 9 | **Corrective Smooth modifier** (Blender built-in) | auto-corrective | **B** | Blender/GPL ✅ | In W5r stack | Automatic smoothing of deformation artifacts — a corrective with zero sculpting. |
| 10 | **Rokoko Studio + Blender plugin** | capture + auto-retarget | **B** | Free tiers; plugin free (account) | Documented | Video/webcam → mocap → auto bone-map → retarget in Blender. Free tier is genuinely usable. |
| 11 | **Meshroom (AliceVision) / COLMAP** | auto-scan (photo→mesh) | **B** | MPL-2.0 / BSD ✅ | Documented | Free photogrammetry → mesh → (Puppeteer/TokenRig/afk-rig) = 100% free scan-to-rigged pipeline. |
| 12 | **TripoSR** | image→3D | **B** | MIT ✅ | Documented | Local single-image-to-3D; feeds the auto-riggers. |
| 13 | **BlenRig 6** | rig framework + guided correctives | **C** | GPL-3.0 ✅ | In repo (`production/tools/blenrig6/`) | Best FREE full body+face system; MDEF muscle cage; guided (not automatic) corrective workflow. |
| 14 | **Cascadeur** (free tier) | mocap cleanup | **C** | Free tier, no time limit | Documented | AutoPhysics + AutoPosing repair mocap automatically. |
| 15 | **DeepMotion Animate 3D** (free tier) | video→anim | **C** | Free 60s/mo **non-commercial**; API is paid tier | Documented | Good free test drive; commercial needs paid. |
| 16 | **Rigify / CloudRig** | rig framework | **C** | Blender/GPL ✅ | Rigify bundled; CloudRig = **upgrade path (needs Blender 5.0+)** | Production standard (Blender Studio films). CloudRig 2.2.32 requires Blender 5.0 — we are on 4.0.2. |
| 17 | **Pose Shape Keys** (Blender Studio) | corrective authoring | **C** | Free ✅ | **Upgrade path (needs Blender 4.2+)** | Auto driver initialization; our `tools/rigging/corrective_builder.py` covers the workflow on 4.0.2. |
| 18 | **EasyWeight** (Blender Studio) | weight-paint QC | **C** | Free ✅ | **Upgrade path (extensions platform, 4.2+)** | Rogue Weight Hunter finds bad weights automatically — exactly what the 2 defect zones need. |
| 19 | **FreeMoCap** | multi-cam mocap | **C** | Open source ✅ | Documented | 100% free, but a full app with heavy deps — not vendored. |
| 20 | **MediaPipe / MMPose** | pose estimation (reference) | **C** | Apache-2.0 ✅ | Documented | Free on-device pose tracking for video→pose reference. |

### Paid wall — documented honestly, NEVER pulled
| Tool | What | Price | Why not |
|---|---|---|---|
| Adaptive Auto Skinning (Jessy Leite) | Best 2026 auto-skinner, 80.9% artist-match benchmark, GPU voxel | Paid (SuperHive) | Paid license; also needs Blender 4.2–5.2 |
| Voxel Heat Diffuse Skinning (meshonline) | Better auto-weights on messy geometry | $30 | Paid; the FREE Surface Heat Diffuse sibling is already our W5r core |
| Auto-Rig Pro (+ Remap) | One-click rig + best Blender retargeting | Paid | Paid; BlenRig 6 + Rokoko cover the free path |
| Simply Cloth Studio 2.0 | Best Blender cloth UX, adaptive wrinkles | Paid | Paid; Blender built-in + Wiggle 2 cover free |
| JiggleGen 2.0 | Cloth-proxy jiggle batch system | $10 | Paid; Wiggle 2 does the job free |
| X-Muscle System | Muscle/tissue sim | Paid | Paid; muscle deep research = body lane |
| Mush3D 3.0 Pose Trainer | **The** automatic example-based corrective system (train on sculpted poses → auto-apply across cache) | $980/yr rental | Paid — and **there is no open-source equivalent** (honest gap, see §5) |
| FaceIt | Best face rigging + ARKit | Paid | Paid; GNM head lane owns the face |

---

## 1. AUTO-RIGGING — skeleton generators, 2026 state of the art

**In-repo arsenal (already vendored, GPU lane owns the bake-offs):**
- **Puppeteer** (Apache-2.0, ByteDance Seed, NeurIPS 2025 Spotlight): skeleton prediction + neural skinning + video-guided animation, trained on Articulation-XL2.0 (59.4K rigged models). The single most autonomous system available open-source.
- **TokenRig/SkinTokens** (MIT, VAST-AI-Research = the Tripo team): `python demo.py --input model.glb --output rigged.glb --use_transfer` — one mesh → full skeleton + dense weights.
- **Make-It-Animatable** (MIT, Tencent/CVPR 2025 Highlight): <1s, handles arbitrary-pose input — unique among auto-riggers.
- **afk-rig** (MIT, CC0 anims): local CLI/MCP, 9 skeletons, 240+ CC0 clips, no account, no upload. Auto-fit ≈2.4% height joint error; caveat: limbs touching the body need weight fixes.
- **UniRig** (MIT): two-stage fallback. **MagicArticulate** (skeleton only — its paper claims skinning but no skinning code was ever released; verified 2026-10-17). **Pinocchio** (LGPL-2.1, 2007, Mixamo's ancestor) — legacy reference.
- **MPFB** (pulled by sibling lane): parametric human bodies with rigs — body-lane territory.

**Free outside the repo:** Mixamo (Adobe ID, browser auto-rig + huge mocap library — basic rigs, no face, check commercial terms); AccuRig 2.0 (free, Windows GUI, not scriptable); Tripo/Meshy one-click (free tiers, commercial-use blocked).

**Verdict:** The auto-rigging problem is SOLVED in-repo. The remaining work is GPU bake-offs (Puppeteer vs TokenRig vs UniRig on the actual Cape Jones mesh), owned by the GPU lane — not duplicated here.

## 2. AUTO-SKINNING — better than W5r?

**W5r remains the best open CPU option:** in-repo Surface Heat Diffuse solver (MIT, `tools/weights/surface-heat-diffuse/`) + Preserve Volume (dual quaternion) + Corrective Smooth. It is the only pipeline that produced usable full-mesh weights on the Tripo mesh where Blender's Bone Heat fails 100%.

**Challengers (autonomy grade A, GPU lane):** Puppeteer / TokenRig / UniRig / Make-It-Animatable neural skinning — the honest bake-off against W5r is queued on the GPU lane. MagicArticulate is OUT (no skinning code exists).

**Paid wall:** Adaptive Auto Skinning (Sept 2026, 80.9% artist-match on 202 chars, GPU voxel, needs Blender 4.2–5.2) and Voxel Heat Diffuse Skinning ($30). Both documented, neither pulled.

**Verdict:** No new open CPU skinning beats W5r in 2026. The ML challengers are already in-repo. No pull needed here.

## 3. AUTO-RETARGETING — animation that just works across skeletons

- **Mixamo** (free, Adobe ID): auto-rig + thousands of mocap clips as FBX. The fastest path from "I need a walk cycle" to keyframes. Browser lane.
- **Rokoko Studio + Rokoko Blender plugin** (free tiers): Rokoko Video (webcam/video → mocap, free tier) → Studio (foot lock, drift fix) → Blender plugin auto-builds the bone map and retargets. Genuinely usable free.
- **Rokoko Video / Plask / DeepMotion / QuickMagic / Cascadeur**: free tiers for video→motion; Cascadeur's free tier (no time limit) adds AutoPhysics + AutoPosing — automatic mocap cleanup, the closest thing to autonomous animation repair.
- **Auto-Rig Pro Remap**: the best Blender-native retargeter — paid, documented only.
- **MakeWalk / RetargetBVH** (MakeHuman community, open): legacy BVH retargeters from the Blender 2.79 era — documented as history, not pulled (API-dead).
- **Blender 5.x**: retargeting/animation workflow improvements (slotted actions, pose library) — upgrade path.

**Verdict:** Free retargeting is well covered by Mixamo + Rokoko (account-required, GUI/browser — a browser-lane task, not a code pull). No code pull warranted.

## 4. AUTO-SCANNING — scan → rigged model, free

The 100%-free scan-to-rigged pipeline, all open:
1. **Capture:** phone photos → **Meshroom** (AliceVision, MPL-2.0) or **COLMAP** (BSD). Free phone apps with free tiers: Polycam, KIRI Engine, Luma AI.
2. **Generate (alternative):** **TripoSR** (MIT, local single-image→3D); TRELLIS.2 / InstantMesh keyless providers already in-repo.
3. **Rig:** feed the mesh to Puppeteer / TokenRig / afk-rig (all in-repo) → rigged + skinned.
4. **Animate:** Puppeteer video→animation, afk-rig's 240 CC0 clips, or Mixamo.

**Verdict:** Documented as a pipeline recipe; no new pull (all components already in-repo or open tools).

## 5. AUTO-CORRECTIVES — the owner's webbing complaint, attacked by systems

This is the highest-value gap: everything that fixes elbows/jaw/face/neck deformation WITHOUT hand-sculpting.

**What exists free/open, ranked by autonomy:**
1. **Corrective Smooth modifier** (Blender built-in, in the W5r stack): fully automatic smoothing of pinching artifacts. Already deployed.
2. **Wiggle 2 — PULLED THIS LANE** (`production/tools/wiggle2/`): automatic spring-physics secondary motion on bone chains with bake-to-keyframes, wind, collision. It doesn't fix webbing directly — it makes the cape (and any chain) move like a SYSTEM instead of hand-keyed shapes. Verified working on Blender 4.0.2 headless (own-eyes test, §7).
3. **BlenRig 6 guided correctives** (in-repo): corrective-shape workflow with guides — semi-automatic (C grade).
4. **Pose Shape Keys** (Blender Studio, free): auto driver initialization from poses — 4.2+ only, upgrade path. Our `tools/rigging/corrective_builder.py` covers the 4.0.2 path.
5. **Dual-quaternion (Preserve Volume) + bendy bones** (in-repo): automatic volume preservation — already in the stack.

**The honest gap:** **Mush3D 3.0's Pose Trainer** (June 2026) is the commercial state of the art — train on a few sculpted poses, auto-apply corrections across an entire animation cache, <1s training. It is **$980/year rental-only**. There is **no open-source equivalent** for Blender. Delta Mush itself only ever existed as a 2015 Gooseberry-branch experiment, never merged. This is a real hole in the open ecosystem — flagged for the research backlog, not solvable by pulling today.

**Verdict:** Wiggle 2 pulled (secondary motion). The example-based auto-corrective hole is documented honestly; Corrective Smooth + DQ + driven correctives remain the free stack.

## 6. MESH + ANIMATIONS → CLEAN RIGGED CHARACTER (minimal human touch)

The autonomy champions, end to end:
1. **Puppeteer**: mesh + video → rigged + skinned + animated FBX. One system.
2. **afk-rig**: `npx afk-rig auto model.glb --skeleton human` → rigged GLB + 240 CC0 animations, local, no account.
3. **Mixamo**: upload → rigged + animation library (browser lane).
4. **Scan path**: phone → Meshroom → Puppeteer/TokenRig → animated (100% free).

## 7. PULLED THIS LANE — Wiggle 2

**What:** Wiggle 2 v2.2.4 by Steve Miller (shteeve3d) — spring-physics simulation on bone transforms: stiffness, damping, gravity, wind, collision (mesh/collection), pinning, bake-to-keyframes with preroll and NLA push.
**Source:** https://github.com/shteeve3d/blender-wiggle-2
**License:** GPL-3.0 (LICENSE vendored, own-eyes verified) — free, commercial use allowed.
**Where:** `production/tools/wiggle2/` — `wiggle_2.py` (single file), `LICENSE`, `CAPE-JONES-WIRING.md`, proof renders in `proof/`.
**Why:** The cape is currently 48 baked shape keys — hand-built motion. Wiggle 2 puts procedural, art-directable physics on the cape bone chain and bakes it to keyframes: a SYSTEM replacing hand-keyed secondary motion. Same mechanism serves hair, belts, accessories.
**Verification (own-eyes, headless Blender 4.0.2):**
- Addon installs and enables cleanly (`WIGGLE2 ENABLE: OK`).
- All physics properties register on scene (`wiggle`, `wiggle_enable`) and bones (stiffness/damping/gravity/wind/collision/pin).
- Proof scene: 8-bone chain + proxy cape mesh, base swung ±25°, Wiggle 2 baked → child bones lag and overshoot vs the rigid chain (renders in `proof/`).

## 8. LEGACY INDUSTRY-STANDARD — honest open-vs-commercial map

| System | Status | License | Note |
|---|---|---|---|
| Autodesk Maya (skin, Delta Mush, Muscle) | Commercial | Paid | The production standard; Delta Mush + Pose Editor/PSD are the reference correctives |
| MotionBuilder | Commercial | Paid | Retargeting/story standard |
| Houdini (Vellum cloth) | Commercial | Paid | Best cloth sim in production |
| 3ds Max (CAT, Biped) | Commercial | Paid | Game-rig legacy |
| Ziva Dynamics / Faceware | Commercial | Paid | Muscle + face capture standard |
| Softimage XSI / Face Robot / Endorphin | **Dead** | — | Historical reference only |
| mGear 5.4 (Maya) | **Open** | MIT ✅ | Best open rigging framework — but Maya-only; documented, not pullable into a Blender repo |
| MakeHuman → MPFB | **Open** | AGPL/GPL ✅ | MPFB pulled by sibling lane |
| Pinocchio (2007) | **Open** | LGPL-2.1 ✅ | Mixamo's ancestor; in-repo |
| Mixamo | Free service | Adobe terms | The free auto-rig that defined the category |
| Blender itself (30 yrs) | **Open** | GPL ✅ | The free production standard everything here runs on |

## 9. What was NOT pulled (and why)

- **Adaptive Auto Skinning / Voxel Heat Diffuse / Simply Cloth / JiggleGen / Auto-Rig Pro / FaceIt / X-Muscle / Mush3D Pose Trainer / Cascade Plus** — paid. Standing policy: documented, never pulled, never cracked.
- **CloudRig** — free/GPL but requires Blender 5.0+ (2.2.32 manifest verified); we are on 4.0.2. Upgrade-path documented.
- **Pose Shape Keys / EasyWeight** — free but 4.2+ extensions-platform. Upgrade-path documented.
- **MakeWalk/RetargetBVH** — open but Blender 2.79-era, API-dead.
- **FreeMoCap / MediaPipe / MMPose** — open, but full apps/libs; documented as wiring references, not vendored.
- **mGear** — MIT but Maya-only; documented.

## 10. Sources

- https://80.lv/articles/try-this-one-click-automatic-skinning-add-on-for-blender (Adaptive Auto Skinning, 2026-09-23)
- https://www.strayspark.studio/blog/best-blender-animation-addons-2026 and /best-blender-rigging-addons-2026 (2026 roundups)
- https://80.lv/articles/this-blender-add-on-lets-you-add-jiggle-physics-to-bodies-clothes-and-hair (JiggleGen 2.0, 2026-09-11)
- https://www.cgchannel.com/2026/06/luiz-elias-releases-mush3d-3-0/ (Mush3D Pose Trainer)
- https://www.cgchannel.com/2026/10/get-free-maya-character-rigging-toolset-mgear-5-4/ (mGear 5.4, MIT)
- https://studio.blender.org/tools/addons/cloudrig/introduction, /pose_shape_keys, /easy_weight (Blender Studio)
- https://extensions.blender.org/add-ons/wiggle-bones/ (Wiggle lineage, GPL-3.0)
- https://afk.ai/developers (afk-rig: MIT, CC0 anims)
- https://www.meshy.ai/tutorials/character-auto-rigging-workflow ; https://www.tripo3d.ai/content/en/guide/the-best-auto-rigger-tools-for-unity
- https://aimocapfree.com/ ; https://filmthreat.com/features/10-best-ai-tools-for-turning-video-into-3d-character-motion/ (free mocap tiers)
- https://www.3dblendered.com/blender-add-ons/how-to-do-motion-capture-in-blender-with-rokoko-tools/ (Rokoko retargeting)
- In-repo: `3d-assets/cape-jones-rig/WEIGHT-BAKEOFF-RESULT.md`, `docs/research/RIGGING-STACK-2026.md`, `docs/research/AUTO-RIGGING-TOOLS-2026.md`, `docs/research/MAGICARTICULATE-WEIGHT-VERDICT-2026.md`
- https://dev.to/milkc0de/i-built-chibirigkit-turning-a-single-character-image-into-an-animated-2d-rig-2j36 (ChibiRigKit, 2D — not relevant, documented as skip)
- http://mesh2motion.org/ (Mesh2Motion — open, CC0)
- https://www.patreon.com/cebstudios/posts/ceb-sam-3d-body-172610949 (CEB SAM 3D Body Loader now free)
- https://blenderartists.org/t/auto-pose-in-blender/1651968 (Blaze AutoPose)

## 11. 2026-10-18 RESTART ADDENDUM (this lane, picked up fresh)

The previous worker died in a daemon restart before filing the PR. Restart work:

**Verification done (own eyes, not relayed):**
- `production/tools/wiggle2/wiggle_2.py` is **byte-identical to upstream** `shteeve3d/blender-wiggle-2` main
  (SHA256 `7333687ae3b6fd20feae8afda649faed1d99bc7b98e92622a8993c09061deac1`, v2.2.4).
- License vendored: GPL-3.0 (`LICENSE`).
- Proof renders `proof/wiggle_cape_f{10,20,30}.png` viewed: 8-bone chain + proxy cape mesh,
  frames show the cape curled (f10) → mid-swing (f20) → extended (f30) — real secondary motion.
- Re-ran the addon install+enable in headless Blender 4.0.2 under xvfb: `WIGGLE2 ENABLE: OK`,
  scene props `wiggle`/`wiggle_enable` registered.
- **Wrote the missing wiring doc** `production/tools/wiggle2/CAPE-JONES-WIRING.md`: chain-build +
  bind + physics-tune + bake + proof steps and a headless template script for the real cape.
- **Key rig fact (checked by introspection, not guessed):** `cape_jones_rigged_w5r.blend`'s
  `CapeJones_Rig` has 94 bones and **zero cape bones** — the wiring builds the chain, it is not
  found. The 48 baked shape keys stay until a Wiggle bake renders a clean swing-and-settle loop.

**New finds since 2026-10-17 (documented, NOT pulled yet — honest status):**
- **Mesh2Motion** (http://mesh2motion.org/) — free & open source, runs in the browser:
  upload GLB/GLTF/DAE/FBX → auto-rig → **170+ animations, all CC0**, Blender source files on
  GitHub. New open competitor to afk-rig/Mixamo for rig + anim library. Candidate for the
  browser lane (verify the GitHub repo + license before any pull).
- **CEB SAM 3D Body Loader** — went **100% FREE for everyone** (2026-10-17, per cebstudios
  Patreon): end-to-end AI mocap studio inside Blender (video→3D mocap via GEM-X, single-photo
  pose, multi-person tracking, pre-rigged MHR/SOMA characters, bi-directional Auto-Rig Pro
  retargeting, foot-sliding killer). Compatible with Blender 4.0–5.2 (fits our 4.0.2).
  Status: **free download, license terms not yet verified** — documented, not pulled until
  the license is confirmed open/commercial-OK.
- **Blaze AutoPose** (Blender Artists, 2026) — Cascadeur-style AutoPosing inside Blender
  (few constraints → FK pose). Paid add-on; documented only, per the no-paid-pull rule.

**Lane separation honored:** GNM head lane files (`docs/research/GNM-HEAD.md`,
`tools/pulled/GNM/`, GNM section of `tools/pulled/README.md`), the MPFB lane
(`production/tools/mpfb2/`), and the spine/face lanes' work (`spine-lane/`,
`cape_jones_rigged_w5r.blend` edits, `face-rig/` edits) were all left untouched —
none staged, none committed by this lane.
