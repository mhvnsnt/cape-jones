# Auto-rigging Tripo models — 2026 research + pull-in

**Researched:** 2026-10-17. **Method:** real 2026 sources only (GitHub repos,
papers, pricing pages, docs) — no training-data guesses. **Baseline:**
BlenRig 6 (`production/tools/blenrig6/`, pulled 2026-10-16).

**Scope:** what auto-rigs *unrigged Tripo-topology* characters (multi-shell,
~1M verts, chaotic AI topology) with minimal manual work. The acceptance test
is a clean auto-rig + skinning on `cape_jones_plain.glb` (0.925 m, NOT
rescaled).

**Correction to prior notes:** MagicArticulate is **not** Meta — it is
NTU + ByteDance Seed (CVPR 2025). There is no Meta 3D-articulation product in
this space; Meta's relevant work here is nil.

## Verdict table

| Tool | License (commercial?) | Runs | Verdict |
|---|---|---|---|
| **Pinocchio** (Baran & Popović 2007) | LGPL-2.1 lib / MIT demo ✅ | Local CPU, headless ✅ | ✅ **PULLED** (`production/tools/pinocchio/`) — proven on CJ below |
| **UniRig** (Tsinghua + Tripo, SIGGRAPH 2025) | MIT ✅ | GPU ≥8GB (Kaggle/Colab) | ✅ **WIRED** (`production/tools/ml-autorig/`) — Kaggle proof queued |
| **Puppeteer** (NTU + ByteDance, NeurIPS 2025 Spotlight) | Apache-2.0 ✅ | GPU (Kaggle/Colab) | ✅ **PULLED 2026-10-17** — license verified own-eyes on the repo page (Apache-2.0). Code-only, 4.7MB, 38/38 py compile at `production/tools/ml-autorig/puppeteer/` (upstream commit 1c0f9fc; weights stay off disk per law, HF Seed3D/Puppeteer on the GPU machine). Wiring: `production/tools/ml-autorig/puppeteer/CAPE-JONES-WIRING.md`. Only pulled rigger with VIDEO-GUIDED ANIMATION (differentiable-optimization anim from a guide video) + FBX export — second ML opinion vs TokenRig/UniRig in the weight bake-off; queue after UniRig |
| **MagicArticulate** (NTU + ByteDance Seed, CVPR 2025) | Apache-2.0 ✅ | GPU 4.6GB (Kaggle/Colab) | ✅ **PULLED 2026-10-17** — license verified own-eyes (Apache-2.0), 18/18 py_compile OK, code-only ~49MB at `production/tools/ml-autorig/magicarticulate/` (upstream commit at pull = 2026-10-17 depth-1; weights stay on HF Seed3D/MagicArticulate per law). Wiring: `production/tools/ml-autorig/magicarticulate/CAPE-JONES-WIRING.md`. Skeleton generation ONLY — the public release ships no skinning inference (verdict 2026-10-17: `docs/research/MAGICARTICULATE-WEIGHT-VERDICT-2026.md`); superseded by Puppeteer for weights — best role: fast skeleton-proposer for bake-off cross-check. |
| ~~**HumanRig**~~ (Alibaba Amap, CVPR 2025) | repo MIT, **no public code** | — | ❌ **NOT RUNNABLE — 2026-10-17 own-eyes re-check:** `c8241998/HumanRig` (7 commits, 92 stars) is a stub: LICENSE + README + assets only, README body is "TODO — release dataset on Hugging Face". No inference code, no weights. Paper + HF dataset (`jellyczd/HumanRig`) only. Earlier "runbook wired" claim was wrong — corrected here. Keep as paper reference. |
| **RigNet** (Xu et al., SIGGRAPH 2020) | GPL-3.0 ✅ | GPU | 📝 documented only — outclassed by UniRig/Puppeteer, orientation-restricted |
| **Make-It-Animatable** (Tencent, CVPR 2025 Highlight) | MIT ✅ | GPU (Kaggle/Colab) | ✅ **PULLED 2026-10-17** — license verified own-eyes (MIT, Copyright 2025 Zhiyang Guo). Code-only, 1.5MB, all .py compile at `production/tools/ml-autorig/make-it-animatable/` (upstream commit 8fb51382; weights stay off disk per law, HF jasongzy/Make-It-Animatable on the GPU machine). Wiring: `production/tools/ml-autorig/make-it-animatable/CAPE-JONES-WIRING.md`. Differentiators: <1s inference, ANY-pose input + rest-pose reset, fine-grained skeleton w/ extra body-structure bones, meshes AND Gaussian splats, built-in Blender armature builder (`app_blender.py`). MIA v2 branch: Hunyuan3D 2.1 backbone, `python app_v2.py`. |
| **Mixamo** (Adobe) | Adobe terms, royalty-free incl. commercial ✅ | Web only | 📝 documented workflow — needs Adobe ID (parent browser lane) |
| **AccuRIG 2.0** (Reallusion) | free, account required | Windows GUI only | 📝 documented only — no CLI/headless |
| **Tripo one-click rigging** (Tripo Studio) | Tripo terms, credits | Web only | 📝 documented only — browser lane |
| **Meshy rigging** (+ Rigging API) | CC BY 4.0 on free plan (attribution!) | Web/API | 📝 documented only — free plan license needs attribution; API is paid |
| **Cinevva Auto Rigger** | freemium (1st rig free, then paid; $29 Blender addon) | Web / paid addon | 📝 documented only — paid path violates no-paid rule |
| **Kinetiq Engine** (Thirdrez) | check terms | **100% in-browser, on-device** (no upload!) | ⚠️ **BROWSER-LANE TEST ATTEMPTED 2026-10-17 — BLOCKED AT SIGN-IN.** `thirdrez.com/kinetiq` loads; "Rig Your Mesh — Free" entry redirects to `app.thirdrez.com/login?next=/kinetiq` — account REQUIRED. Google sign-in as fmmg.mars@gmail.com reached the "Hi Mars" password challenge for the Thirdrez OAuth app; the credential service could not complete password entry (8 failed attempts, no lockout/CAPTCHA — it simply didn't fill, "the operation did not complete, and it changed nothing"). No paid plan or trial started. Auto-rig itself NOT yet tested. Marketing claims observed on the page (UNVERIFIED): 100% client-side (no upload, no GPU server), per-joint confidence scores, full Foot→Ball→Toe chains, live Influence Map heat per bone, finger detection; free plan = $0 (rig + preview free), animation export needs Starter+ ($4.99/mo). See "BROWSER-LANE TEST 2026-10-17" section below. Resume path: owner completes the Google sign-in (Secure Vault password entry or main-agent handoff), then the browser lane can upload `cape_jones_plain.glb` (54MB, granted in the browser task) and run the rig. Do NOT retry blind — every attempt stalls at the same password page. |
| **ai3dmodel.app** | check terms | Web, free | 📝 documented only — browser lane |
| **DeepMotion Animate 3D** | free tier 60s/mo, personal non-commercial | Web/API | 📝 documented only — mocap, not a mesh auto-rigger; free tier non-commercial |
| **Krikey AI** | freemium | Web | 📝 documented only |
| ~~**RigAnything**~~ (UCSD + Adobe, SIGGRAPH 2025) | ❌ **Adobe Research License — NONCOMMERCIAL ONLY** | GPU | ❌ **REJECTED** — license forbids commercial use |
| SkinTokens/TokenRig (Tripo/VAST-AI-Research) | **MIT** ✅ | GPU (≥14GB VRAM; Kaggle/Colab lane) | ✅ **PULLED 2026-10-17** — public code confirmed (was "announced, no public code"): unified single-pass skeleton + skinning weights via learned SkinTokens; 98–133% skinning accuracy gain over UniRig per authors. Lives at `production/tools/skintokens-autorig/` (code only, weights fetched on GPU machine via `download.py`). Wiring: `production/tools/skintokens-autorig/CAPE-JONES-WIRING.md`. |
| TARig / Drive | papers, no public code found | — | 📝 papers only, not runnable |

## PROOF: Pinocchio on Cape Jones (CPU lane, 2026-10-17) — VERIFIED

**Ran it.** `production/tools/pinocchio/rig` (headless C++ driver over the
Pinocchio LGPL library) on a voxel-remeshed single-shell CJ mesh:

- Input: `work/cj_vox.obj` — 111,010 verts / 222,016 tris (voxel remesh of
  the 991k-vert Tripo mesh; see "Tripo multi-shell" note below)
- **Result: 18-joint human skeleton embedded in 42s on CPU, mean
  skinning-weight row-sum = 1.0** (weights properly normalized)
- Joint sanity (own-eyes on `work/cj_pinocchio_skeleton.json`): height span
  0.877 m vs 0.925 m model, hips→shoulders→head chain correct, knees below
  thighs, elbows between shoulders and hands, left/right symmetric.
- Pose test in Blender (elbows −70°, knees +55°, shoulders ±25°, head 18°):
  `proof/pinocchio_pose_front.png`, `proof/pinocchio_pose_side.png`,
  `proof/pinocchio_rest_front.png` — rendered with the repo lighting canon,
  read with own eyes (see "Reading the proof" below).

**What the proof shows** (read with own eyes 2026-10-17):
- `proof/skeleton_placement.png` — all 18 bones land exactly on the mesh:
  head/spine/hips chain, symmetric arms (shoulder→elbow→hand tracking the
  T-pose), symmetric legs. Clean.
- `proof/lbs_pose_big.png` — numerical LBS pose test (lelbow 90°,
  rknee 60°, lshoulder 30°): forearm bends up smoothly at the elbow, shin
  flexes at the knee, arm raises at the shoulder. No explosions, no NaN,
  max vertex displacement 0.33 m for these angles. The skinning is clean
  and articulable.
- `proof/pinocchio_rest_front.png` / `pinocchio_pose_front.png` /
  `pinocchio_pose_side.png` — Blender Cycles renders of the same rig
  (repo lighting canon). The mesh + armature render correctly.

**Orientation sensitivity (important):** the first Pinocchio run was on a
mesh yawed 90° (an artifact of the OBJ round-trip). Pinocchio placed 17/18
joints correctly but **missed the left arm** — the lshoulder→lelbow→lhand
chain collapsed down the torso, and the −Z arm verts got diffuse mush
weights (top joint only 0.187). Re-running on the mesh yawed to face +Z
(`work/cj_vox_std.obj` → `work/cj_std_*`) gives a perfect 18/18 with
dominant weights (lelbow 0.919, relbow 0.826 on the arms). **Lesson: yaw
the character to face +Z before running Pinocchio.** This is documented in
`production/tools/pinocchio/README.md`.

**Blender gotchas hit during proof** (documented for the team):
- Blender 4.0.2's `wm.obj_import` does **no** Y-up→Z-up conversion (unlike
  the glTF importer). The mesh arrives Y-up; the proof bakes +90° X into
  the mesh data.
- `Mesh.transform()` leaves custom split normals stale → clear them
  (`customdata_custom_splitnormals_clear`) or shading breaks.
- The 2m default Cube **swallows** the 0.9m character — delete default
  objects first (this caused every "blank" render in the lane).

### Tripo multi-shell finding (important for every tool)

The raw Tripo mesh is **322 disconnected shells** (largest 31,882 of 991,082
verts) — body, cape, accessories are separate. Pinocchio *requires* a single
connected component, so the lane voxel-remeshed to one watertight shell.
Consequences:
- The rig is computed on the *fused* mesh; the cape is fused to the body in
  the rigged version. For the hero rig the rig lane should re-run Pinocchio
  per logical part or use the fused mesh only for bone placement, then
  transfer weights to the original shells (`proof/transfer_weights_full.py`
  pattern).
- The ML riggers (UniRig/Puppeteer) train on multi-component Objaverse data
  and handle shells natively — this is their structural advantage over
  Pinocchio for Tripo meshes.

## Comparison vs BlenRig 6 (honest)

| | Pinocchio (pulled) | UniRig etc. (GPU lane) | BlenRig 6 (baseline) |
|---|---|---|---|
| Bone placement | automatic (template fit) | automatic (learned) | manual guide fitting |
| Skinning weights | automatic, smooth | automatic, learned | guided manual + mesh-deform |
| Face rig | none | none | **full facial rig** ✅ |
| Controls (IK/FK) | none — plain joints | none — plain joints | **full control rig** ✅ |
| Muscle/deform quality | decent LBS | best-in-class LBS | **mesh-deform + lattices** ✅ |
| Tripo multi-shell | needs remesh fusion | native ✅ | manual |
| Speed | ~1 min CPU | seconds GPU | hours of artist time |
| Cost | free | free (his GPU) | free |

**Reading:** Pinocchio/UniRig do not *replace* BlenRig 6 — they replace the
*first 80%* of it (bone placement + weight blocking). The winning pipeline is:
**auto-rigger places bones + weights → BlenRig-style controls built on top**
(BlenRig's guide can bind to an existing skeleton). BlenRig stays the hero-rig
system for face + controls; the auto-riggers kill the tedious blocking stage.

## Recommended standard path (for the team)

1. **Now (CPU):** `production/tools/pinocchio/` — `./rig mesh.obj out --skel
   human` → skeleton JSON + weights → Blender import script. Use for every
   Tripo character's first-pass rig today. No GPU, no account, no upload.
2. **Next (his Kaggle GPU):** `production/tools/ml-autorig/` —
   `kaggle_unirig_capejones.ipynb` is queued; UniRig (MIT) is the
   quality challenger on native multi-shell meshes. If its rig beats
   Pinocchio's on the proof renders, it becomes the first-pass standard.
3. **Hero rig:** BlenRig 6 controls + face on top of the auto-rig's
   skeleton (rig lane owns this).
4. **Quick'n'dirty / mocap:** Mixamo (browser lane, Adobe ID) for background
   characters; DeepMotion free tier is mocap-only, non-commercial — not for
   show assets.

## Needs parent browser action

- **Mixamo:** sign in with Google (blanket permission covers it) at
  mixamo.com → Upload Character → upload CJ as ZIP (OBJ+MTL+textures) →
  place chin/wrist/elbow/knee/groin markers → Download rigged FBX. Note:
  this uploads the model to Adobe's servers — fine for CJ (his character),
  documented in the workflow.
- **Tripo one-click rigging / Meshy / Cinevva / ai3dmodel.app:**
  all web lanes, each needs its own account/clicks — none attempted here.
- **Kinetiq Engine:** browser-lane test ATTEMPTED 2026-10-17 — see section below; blocked at sign-in, auto-rig itself untested.

## BROWSER-LANE TEST 2026-10-17 — Kinetiq Engine (Thirdrez) — blocked at sign-in

**What was attempted:** live browser task against `https://thirdrez.com/kinetiq`
with `cape_jones_plain.glb` (54MB, granted to the browser) as the test mesh —
the "worth a browser-lane test" entry in this doc's verdict table.

**Facts observed (browser task, `thirdrez.com`):**
- Marketing page loads; the "Rig Your Mesh — Free" Auto-Rig entry point
  redirects to `https://app.thirdrez.com/login?next=/kinetiq` — an account is
  required to use Kinetiq Auto-Rig.
- Page claims (UNVERIFIED — never got past login): Auto-Rig is "100% in your
  browser" / "No upload. No GPU server"; Kinetiq Vision detects every joint
  with a measured confidence score; clean canonical skeleton down to a full
  Foot → Ball → Toe chain; binds skin weights with "no bleed at the joints";
  live Influence Map (weight-color heat map per bone with per-joint reach
  slider that re-solves skin weights live); free rig + preview; animation
  export requires Starter or higher ($4.99/mo; free plan $0, no credit card).
- Sign-in flow: "Continue with Google" → Google account chooser (Mars FMMG /
  fmmg.mars@gmail.com selected) → Google password challenge page at
  `accounts.google.com/v3/signin/challenge/pwd` for the Thirdrez OAuth app.
  The credential service (login.advance) failed 8 times across two login-agent
  attempts ("The operation did not complete, and it changed nothing") — the
  password field stayed empty. No rejection, lockout, or CAPTCHA from Google.
- No paid plan or trial was started; nothing was uploaded; nothing was rigged.

**Verdict:** AUTO-RIG UNTESTED — blocked at sign-in, not rejected on merit.
Do NOT re-run blind: every attempt stalls at the same password page.

**Resume path (owner/main-agent):**
1. Owner completes the Thirdrez Google sign-in (he is phone-only, so either a
   Secure Vault password entry for fmmg.mars@gmail.com or a manual takeover
   in a live chat — NOT on a detached run).
2. Re-run the browser lane: upload `cape_jones_plain.glb`, run Auto-Rig,
   verify the 100%-client-side claim via devtools Network (does the mesh
   leave the machine?), record joint count/confidence scores, skeleton
   structure (Foot→Ball→Toe?), Influence Map quality, finger rigging, and
   which export formats (FBX/GLB) are actually free.

## Sources

- Puppeteer repo (Apache-2.0, NeurIPS'25 Spotlight): https://github.com/Seed3D/Puppeteer
- MagicArticulate repo (Apache-2.0, CVPR'25): https://github.com/Seed3D/MagicArticulate
- UniRig repo (MIT, SIGGRAPH'25): https://github.com/VAST-AI-Research/UniRig
- ~~HumanRig repo (MIT, code promised but never shipped)~~: https://github.com/c8241998/HumanRig — own-eyes 2026-10-17: stub (LICENSE + README + assets), no code. Dataset only: https://huggingface.co/jellyczd/HumanRig
- RigAnything HF (Adobe non-commercial license): https://huggingface.co/Isabellaliu/RigAnything
- RigNet repo (GPL-3.0): https://github.com/zhan-xu/RigNet
- Make-It-Animatable (CVPR'25): https://github.com/jasongzy/Make-It-Animatable
- AccuRIG 2.0: https://www.cgchannel.com/2025/07/rig-and-animate-3d-characters-for-free-with-accurig-2-0/
- Mixamo FAQ (free, royalty-free commercial use): https://helpx.adobe.com/sea/creative-cloud/faq/mixamo-faq.html
- DeepMotion pricing (free 60s/mo): https://www.saasworthy.com/product/deepmotion
- Cinevva rigger (free tier terms): https://app.cinevva.com/tools/rigger
- Meshy rigging API: https://docs.meshy.ai/en/api/rigging ; pricing comparison: https://sculptly3d.com/meshy-vs-tripo
- Kinetiq Engine (in-browser auto-rig): https://thirdrez.com/kinetiq
- Tripo auto-rigging features: https://www.tripo3d.ai/pt/features/ai-auto-rigging
