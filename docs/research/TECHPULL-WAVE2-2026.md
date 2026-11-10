# TECH PULL WAVE 2 — 2026 3D/Animation Research + Pull-ins

**Date:** 2026-10-18 · **Lane:** `lane/techpull-wave2-20261018`
**Owner directive:** research the best FREE 2026 systems (new + legacy),
pull them in, hook them up. Autonomous systems first. Open source first,
commercial-safe licenses only, documented honestly.

**Already in-repo (NOT re-pulled):** BlenRig 6, MPFB2, GNM face-rig,
Wiggle 2, Puppeteer, TokenRig/SkinTokens, Make-It-Animatable, afk-rig
(240 CC0 anims), Surface Heat Diffuse (W5r), Rhubarb lip-sync, Pinocchio,
UniRig. SMPL-X/FLAME/STAR are HARD NO-GOs (non-commercial research-only).

## PULLED THIS WAVE

| # | System | Gap | License | Repo path | One-line function |
|---|---|---|---|---|---|
| 1 | **ZOZO ppf-contact-solver** v1.0.16 | cloth sim | Apache-2.0 ✅ | `production/tools/ppf-contact-solver/` | Guaranteed non-penetrating FEM cloth/soft-body/rope solver (SIGGRAPH Asia 2024); Blender 5.0+ add-on — **upgrade path** from our 4.0.2 |
| 2 | **Mesh2Motion GLB library** | animation library | **CC0** ✅ | `production/tools/mesh2motion/` | 170+ open animations as import-ready GLB; 87 human actions smoke-tested in our Blender 4.0.2 |
| 3 | **CJ Toon shader system** | toon/cel look | n/a (own recipe) | `production/tools/toon-shader/` | Hard-shadow Shader-to-RGB node-group spec + outline + lighting rules; no clean open code exists to vendor |

Wiring docs: `CAPE-JONES-WIRING.md` in each tool dir (what / license /
how to run against the Cape Jones rig / honest caveats).

---

## 1. AUTOMATIC WEIGHT PAINTING / SKINNING

**Verdict: our W5r stack still stands; no new open CPU skinning beats it.**

- **W5r** (in-repo: Surface Heat Diffuse MIT solver + Preserve Volume/DQ +
  Corrective Smooth) remains the only pipeline that weights the full 991k-vert
  Tripo mesh where Blender Bone Heat fails 100%. Bake-off: `WEIGHT-BAKEOFF-2026.md`.
- **ML challengers** (Puppeteer / TokenRig / Make-It-Animatable neural skinning)
  are already in-repo; GPU bake-off vs W5r belongs to the GPU lane.
- **NEW 2026-10-18 — Armature by FabricatorStudio** (Adrian Melian, ex-Sledgehammer
  lead TA): free AI-assisted standalone rigger/skinner, imports
  USD/OBJ/FBX/glTF, exports USD for Blender/Maya/Unreal, two local skinning
  engines. **Free to indie artists; pipeline toolset free under $2M/yr revenue.**
  NOT open source — proprietary download from https://fabricator.studio/
  (CG Channel 2026-08-06). **Documented as a wiring recipe, not vendored**
  (no code to pull; needs a download + it's a standalone app).
- **Adaptive Auto Skinning** (Jessy Leite, Sept 2026, 80.9% artist-match,
  GPU voxel, one-click): still **paid** (SuperHive) — documented only.
- **Audio Lip Sync Pro** (launched 2026-10-14, Product Hunt): buy-once, local,
  no account — but **paid**. Documented only.

No pull in this category: nothing open beats the in-repo stack.

## 2. CORRECTIVE-SHAPE-KEY AUTO-GENERATION

**Verdict: the honest gap stands — no open Mush3D equivalent exists.**

- **Mush3D 3.0 Pose Trainer** ($980/yr rental): the commercial state of the art
  (train on sculpted poses → auto-apply across a cache). No open-source
  equivalent for Blender — re-verified 2026-10-18, still true.
- Free stack remains: Corrective Smooth modifier (in W5r) + dual-quaternion
  Preserve Volume + bendy bones + BlenRig 6 guided correctives + Pose Shape
  Keys addon (Blender Studio, free, 4.2+ upgrade path).
- **Second Nature** (Blender Artists, July 2026): automates mesh-penetration
  correction + secondary motion via F-Curves (register 4 poses → auto drivers).
  **$19.99 on SuperHive — paid**, documented only.

No pull: nothing open fills the example-based auto-corrective hole.

## 3. CLOTH SIM

**Verdict: PULLED ZOZO ppf-contact-solver (upgrade path); Wiggle 2 stays for
secondary motion.**

- ✅ **ppf-contact-solver** (`st-tech`, Apache-2.0): FEM solver, guaranteed
  no-intersection + strict strain limits, SIGGRAPH Asia 2024, 180M contact
  points/GPU, MCP-server exposed (LLM-drivable), cloud-GPU offload (~$0.10/drape).
  **Caveat:** Blender add-on needs **5.0+** (we're 4.0.2) → vendored as
  upgrade-path; solver core is a standalone Rust server.
- Wiggle 2 (in-repo): spring-physics secondary motion — different problem
  (procedural jiggle), complementary, not replaced.
- Blender 5.2 Geometry Nodes XPBD cloth: built-in upgrade path, documented.
- Paid wall (documented only): Simply Cloth Studio 2.0, JiggleGen 2.0 ($10),
  Cascade Plus (baked sim library).

## 4. AUTO-RIGGING

**Verdict: solved in-repo; one new free-indie tool documented.**

- In-repo arsenal unchanged and best-in-class: Puppeteer (Apache-2.0),
  TokenRig (MIT), Make-It-Animatable (MIT, arbitrary-pose input), afk-rig
  (MIT + 240 CC0 anims), UniRig fallback, Pinocchio skeleton placement.
- **NEW:** Armature (FabricatorStudio) — free for indie, documented as recipe.
- Mixamo: still the fastest free browser auto-rigger (Adobe ID; check
  commercial terms); browser-lane task, not a code pull.

No pull: the problem is solved in-repo; remaining work is GPU bake-offs.

## 5. AUTO-RETARGETING

**Verdict: covered by free services; open code options are legacy.**

- Mixamo (free, Adobe ID) + Rokoko Studio/Blender plugin (free tiers,
  auto bone-map) remain the free retargeting path — account/GUI work for the
  browser lane, not code pulls.
- **Directly relevant:** the sitting lane's 2026-10-18 directive — "Scan tech
  (auto bone-fitting/retargeting of the Tripo pose onto the canon rig) is the
  path" — is served by this stack: fit source skeleton → bone-map → bake.
  The Mesh2Motion retarget recipe (§7 wiring doc) is the worked example.
- MakeWalk/RetargetBVH (MakeHuman): open but Blender 2.79-era, API-dead.
- Auto-Rig Pro Remap: best Blender-native retargeter — paid, documented only.
- mimem.ai Mocap Blender add-on: paid, documented only.

No pull: no open, current, vendored-able retargeter beats the service path.

## 6. MOCAP / ANIMATION SOURCES

**Verdict: Mesh2Motion GLB pulled; several free sources documented.**

- ✅ **Mesh2Motion** (CC0): 170+ animations, Blender-source + GLB. Pulled the
  complete human set as GLB (13 MB).
- **Xsens free mocap assets** (https://www.xsens.com/entertainment/free-xsens-motion-capture-animation-assets):
  5 walk/run + 10 sports + 7 dance, FBX, "HD reprocessed, ready for
  retargeting" — free download, license terms to verify before commercial use.
  Documented; browser lane can fetch.
- **RancidMilk CMU library** (itch.io): CMU mocap → FBX/glTF, free to
  use/modify/redistribute (not for resale as animations). Documented.
- **Bandai Namco 3,077 moves** (BVH): **research/personal use only — NOT
  commercial-safe.** Documented with the warning.
- **Anderson Rohr Halloween pack** (80.lv, Oct 2026): 19 mocap clips, free for
  personal + commercial. Documented.
- Krikey AI: free mocap library + video-to-anim, browser, account-gated —
  browser lane.

## 7. ANIMATION LIBRARIES → see §6 + the Mesh2Motion pull.

Curated in-repo: afk-rig 240 CC0 clips (in-repo) + Mesh2Motion 170+ CC0
(pulled this wave). Mixamo's thousands of clips remain the browser-lane
backstop (terms check before commercial use).

## 8. LIP-SYNC / VISEME AUTO-GENERATION

**Verdict: Rhubarb remains the open standard (already in-repo); new AI
options are paid.**

- **Rhubarb Lip Sync** (in-repo `production/tools/rhubarb-lip-sync/`): still
  the free/open audio→phoneme-timing standard (Preston Blair visemes).
  Nothing open has dethroned it in 2026.
- **Blender's built-in Lip Sync add-on**: free, ships with Blender — bake
  audio → drive shape keys. Documented as the zero-dependency path.
- **Audio Lip Sync Pro** (Oct 2026): ARKit-blendshape AI lip-sync, local,
  buy-once — **paid**. Documented only.
- Papagayo-NG: open timeline-based phoneme editor — documented alternative.

No pull: Rhubarb + built-in cover the free path; the viseme mouth matrix in
the character sheets remains the spec Rhubarb output maps onto.

## 9. TOON / CEL SHADER TOOLING

**Verdict: recipe pulled (no vendored-able open code exists); paid + fork
options documented honestly.**

- ✅ `production/tools/toon-shader/CAPE-JONES-TOON-WIRING.md`: the CJ_Toon
  node-group spec (Shader-to-RGB → Constant ColorRamp = hard shadow edge, no
  gradient), inverted-hull outlines, Cycles Toon-BSDF fallback, lighting
  rules, and the `apply_cj_toon.py` script contract for the shading lane.
- **Goo Engine** (open Blender NPR fork, GPL): the serious open answer for
  renderer-level anime features — a full fork, so it's a pipeline decision,
  not a casual pull. Documented.
- **Style Engine** ($24.99, GPL-3.0, Blender 4.2+): best-priced dedicated
  add-on. **Paid** — documented only.
- Community itch.io node groups: licenses unverifiable — never vendored.

## SIGNUP-NEEDED (for the parent's browser lane)

| Service | URL | What the account unlocks |
|---|---|---|
| Mixamo | https://www.mixamo.com/ | Free auto-rig + thousands of mocap clips (Adobe ID). Verify commercial terms before use. |
| Rokoko Studio | https://www.rokoko.com/ | Free tier: video/webcam mocap → Studio cleanup → Blender auto-retarget plugin. |
| Armature | https://fabricator.studio/ | Free-for-indie AI rigger/skinner download (standalone app). |
| Xsens free assets | https://www.xsens.com/entertainment/free-xsens-motion-capture-animation-assets | 22 free FBX mocap clips (verify license). |
| Krikey AI | https://www.krikey.ai/create/free-mocap-animations | Free mocap library + video-to-animation (browser). |

## SOURCES

- https://80.lv/articles/try-this-one-click-automatic-skinning-add-on-for-blender (Adaptive Auto Skinning, 2026-09-23)
- https://www.cgchannel.com/2026/08/armature-is-a-free-ai-assisted-standalone-character-rigging-tool/
- https://toknow.ai/posts/zozo-ppf-contact-solver-blender-cloth-physics-open-source/ · https://80.lv/articles/new-open-source-physics-engine-for-blender-released · https://github.com/st-tech/ppf-contact-solver (Apache-2.0, verified)
- https://www.strayspark.studio/blog/best-blender-toon-shader-addons-2026
- https://github.com/Mesh2Motion/mesh2motion-app (MIT) · https://github.com/Mesh2Motion/mesh2motion-assets (CC0)
- https://www.producthunt.com/products/audio-lip-sync-pro-for-blender (paid)
- https://blenderartists.org/t/second-nature-automates-mesh-penetration-correction-and-secondary-motion/1649113 (paid $19.99)
- https://app.cinevva.com/guides/free-rigged-3d-character-models (CC0 sources roundup)
- https://www.cgchannel.com/2022/05/download-3000-free-mocap-moves-from-bandai-namco-research/ (research/personal only)
- https://80.lv/articles/get-ready-for-halloween-with-these-19-free-mocap-animations
- https://code.blender.org/2026/07/geometry-nodes-physics/ (Blender 5.2 cloth)
- Sibling docs: `BEST-RIGGING-TECH-2026.md`, `WEIGHT-BAKEOFF-2026.md`,
  `RIGGING-STACK-2026.md`, `AUTO-RIGGING-TOOLS-2026.md`
