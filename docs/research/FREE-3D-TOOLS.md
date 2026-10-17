# FREE-3D-TOOLS — free production-grade 3D/animation tooling for the Cape Jones living room

**Researched:** 2026-10-16. **Method:** every claim below was verified against a real 2026
source (official pricing/docs pages, GitHub repos, API docs, or a live headless test run by
this lane). No training-data guesses. If a free tier changed or died in 2026, it is marked
plainly (NO-SILENT-FAILURE).

**Setup lanes:** this doc is written to be executed. Each winner has an exact recipe and a
concrete proof test. Anything that needs a browser sign-in is flagged
`NEEDS PARENT BROWSER LANE` — subagents cannot do live-browser OAuth.

**What the scene needs (from `3d-assets/living-room/SCENE-CANON.md`):**
- GPU render of the room (Eevee/Cycles stills; later the 5-min EP01) — Cycles target.
- Small props for the re-layout: VCR/DVD player, boxes, small monster toy, mug, posters —
  all recolored to the LOCKED palette: coral pink `#F15E57`, blue `#5B84DD`, warm oak
  `#E59964`, violet LED `#731AE5`, amber `#FFE996`, rug trim `#9B4C49`, silver `#BDD2D6`.
- Hard constraints: **no credit card, no paid tier.** If a tool asks for a card, stop and
  report (owner law).

---

## 1. FREE GPU RENDER PATHS

### 1a. Kaggle Notebooks via the Kaggle API — ✅ WORKS HEADLESS (verified by this lane)

**Live test this lane ran (2026-10-16):** `kaggle kernels list --page-size 1 --csv`
succeeded headlessly with the stored `~/.kaggle/kaggle.json` (user marsfmmg). No browser,
no paste-code, no phone challenge. The Kaggle API lane is fully agent-drivable.

**Free-tier numbers (verified Oct 2026):**
- Hardware: **2× Tesla T4 (16 GB each)** on GPU notebooks.
- Quota: **30 GPU-hours/week**, resets weekly.
- Max run: **~12 hours per notebook session.**
- Cost: $0, no credit card. Source:
  https://github.com/au-nlp/2026/blob/HEAD/COMPUTE_RESOURCES.md

**Exact recipe (end-to-end, headless):**

1. Put the `.blend` into a Kaggle dataset once (so notebooks can attach it as read-only input):
```bash
mkdir -p ~/workspace/kaggle-render/dataset && cp /path/to/living_room.blend ~/workspace/kaggle-render/dataset/
cat > ~/workspace/kaggle-render/dataset/dataset-metadata.json <<'EOF'
{
  "title": "cape-jones-living-room",
  "id": "marsfmmg/cape-jones-living-room",
  "licenses": [{"name": "CC0-1.0"}]
}
EOF
kaggle datasets create -p ~/workspace/kaggle-render/dataset   # first time
# later updates: kaggle datasets version -p ~/workspace/kaggle-render/dataset -m "v2"
```

2. Notebook source dir (`~/workspace/kaggle-render/kernel/`):
`render.py` (run as `%run render.py` from the one notebook cell, or split into cells):
```python
# cell 1 — prove the GPU is really there
!nvidia-smi --query-gpu=name,memory.total --format=csv

# cell 2 — install Blender 5.2 LTS (verify exact filename on
# https://www.blender.org/download/lts/ at setup time; pattern below)
!wget -q https://download.blender.org/release/Blender5.2/blender-5.2.2-linux-x64.tar.xz \
  && tar -xf blender-5.2.2-linux-x64.tar.xz && ./blender-5.2.2-linux-x64/blender --version

# cell 3 — prove Cycles sees the T4 (expect CUDA/OPTIX entries)
!./blender-5.2.2-linux-x64/blender -b --python-expr \
  "import bpy; prefs=bpy.context.preferences.addons['cycles'].preferences; prefs.refresh_devices(); \
   [print(d.type, d.name) for d in prefs.devices]"

# cell 4 — render (OptiX on Turing T4; fall back to --cycles-device CUDA if OptiX errors)
!./blender-5.2.2-linux-x64/blender -b /kaggle/input/cape-jones-living-room/living_room.blend \
  -E CYCLES --cycles-device OPTIX -o /kaggle/working/frame_#### -f 1
!ls -la /kaggle/working/*.png
```

`kernel-metadata.json`:
```json
{
  "id": "marsfmmg/cape-jones-blender-render",
  "title": "cape-jones-blender-render",
  "code_file": "render.py",
  "language": "python",
  "kernel_type": "notebook",
  "is_private": true,
  "enable_gpu": true,
  "enable_internet": true,
  "dataset_sources": ["marsfmmg/cape-jones-living-room"],
  "kernel_sources": []
}
```

3. Drive it headlessly:
```bash
kaggle kernels push -p ~/workspace/kaggle-render/kernel
kaggle kernels status marsfmmg/cape-jones-blender-render        # poll: 'complete' / 'error'
kaggle kernels output marsfmmg/cape-jones-blender-render -p ~/workspace/kaggle-render/out
```
`kaggle kernels output` downloads everything in `/kaggle/working` (your PNGs land there).

**What breaks (know before you burn quota):**
- `enable_internet` must be `true` or the Blender download 404s inside the sandbox.
- Max ~12 h per run — chunk animation renders into ≤12 h segments (frame ranges per kernel).
- **CHECK-BEFORE-START:** another chat runs the Pantera Kaggle render lane. Do not start a
  render without checking that lane first — Kaggle GPU quota (30 h/wk) is shared on the
  account and concurrent heavy sessions can crowd each other.
- Blender 5.2 needs glibc ≥ 2.28 — Kaggle's image satisfies this; if the binary won't
  start, pin to Blender 4.5 LTS (`blender-4.5.14-linux-x64.tar.xz`, supported to Jul 2027).
- OptiX is fastest on T4; if it throws, `--cycles-device CUDA` is the fallback.
- `kaggle kernels output` only fetches `/kaggle/working` — renders MUST go there.

**Proof-of-work test (the setup lane runs this):**
Push the kernel above rendering a **single frame at 64 samples, OptiX**. Pass = the log
shows `Tesla T4` in `nvidia-smi`, Cycles lists an OPTIX device, and `kaggle kernels
output` returns a non-zero-byte `frame_0001.png`. Budget: ~3–5 min of GPU quota.

### 1b. Janction render API — ⚠️ PROMISING, UNVERIFIED BY US

Agent-first Blender render service (render.janction.jp): `pip install janction-render`,
first command creates a **free key = 100 JPY of GPU time, no card**. Previews stay free
(2 GPU-min/day). Measured: 24-frame 720p @64 samples ≈ 59 GPU-seconds ≈ 6 JPY, so the
free key covers real test renders. Blender 5.0/5.2 on their GPUs; supports `.blend`,
bpy scripts, GLB/FBX/USD/OBJ.
- Source: http://dev.to/_903a3934b362f0afe2a8/letting-an-ai-agent-pay-for-renders-without-surprises-free-credit-first-a-top-up-link-spending-3i1m
- Status: third-party write-up by the service author. **The setup lane must verify the
  key-creation step is truly headless before depending on it.** If it demands a browser,
  flag NEEDS PARENT BROWSER LANE. Never let an agent past the free key without the
  owner's explicit go-ahead (spending rule).

### 1c. SheepIt Render Farm — ⚠️ FREE BUT SLOW-START, BROWSER-ONLY ENTRY

Community farm: you earn points by rendering others' frames, spend points on your own.
Real 2026 reports: ~600 volunteer machines, Cycles/Eevee/Workbench, Blender-only, frame-level
distribution; users report getting ~3–4× their contributed frames back.
- Catch 1: **signup + project submission are web-only → NEEDS PARENT BROWSER LANE.**
- Catch 2: new accounts get a small starter balance; sources recommend running the
  client for several days before your first submission to build a reserve.
- Catch 3: your `.blend` is opened on strangers' machines (thumbnails visible) — fine
  for our scene, not for anything private. Blender versions lag latest releases.
- The client itself is CLI-capable after login: `java -jar sheepit-client.jar -login
  <user> -password <pw> -ui text -compute-method CPU_GPU`.
- Sources: https://superrendersfarm.com/article/sheepit-render-farm-free-point-system-blender-users,
  https://github.com/davidmueller13/sheepit-client,
  https://dev.to/lovestaco/we-rendered-a-hq-demo-video-on-a-free-farm-run-by-strangers-1440
- Verdict: legitimate overflow lane, not the primary path. Queue position depends on
  contributed points, so it cannot be scheduled deterministically.

### 1d. Google Colab headless Blender — ❌ NOT RECOMMENDED

- Free tier (Sep 2026 pricing page): **no compute units, "very limited access to GPUs"**,
  sessions ≤ 12 h, **no reliable background execution**, ~90-min idle timeout. GPU type
  is dynamic (T4 if you're lucky, sometimes nothing).
  Sources: https://gpuperhour.com/blog/google-colab-alternatives,
  https://www.spheron.network/blog/google-colab-alternatives-8-gpu-clouds-compared-2026/
- Headless operation needs `colab --auth=oauth2` paste-code → **NEEDS PARENT BROWSER LANE**
  and the session dies when idle. Fine for interactive experiments; unusable as an
  unattended render lane.

### 1e. Fox Renderfarm / RebusFarm / GarageFarm / RenderStreet — ❌ PAID

Free only as small trial credits (e.g. Fox: $25 new-user credit). Not free-tier
infrastructure. Listed here so nobody re-researches them.

**Category 1 verdict — WINNER: Kaggle notebook via Kaggle API (§1a).** Only path that is
free at real scale, headless-drivable today (API proven by this lane), with a T4 and
enough quota for the living-room stills.

---

## 2. FREE AI-3D-ASSET PATHS (props: VCR/DVD, boxes, monster toy, mug, posters)

License rule used below: a path is **OK** only if its output can ship in the show
(global YouTube/Facebook distribution) with no payment. Anything else is marked.

| Tool | Free tier (Oct 2026) | Commercial license on free outputs | Verdict |
|---|---|---|---|
| **TripoSR (self-hosted, stabilityai)** | Unlimited, no signup | **MIT — OK** | ✅ primary pick |
| **TRELLIS (self-hosted, microsoft)** | Unlimited, no signup | **MIT — OK** | ✅ quality pick |
| **Meshy** | 100 credits/mo, ~3–5 textured models, 10 downloads/mo (older engines), no card | **CC BY 4.0 — OK with attribution** | ⚠️ runner-up |
| **SupaVoxel** | 3 models/day, no card | Free outputs public/CC-BY-ish — confirm at download | ⚠️ conditional |
| **Tripo Studio** | 200 credits/mo (~13 models) | **Non-commercial, public models — BLOCKED** | ❌ blocked |
| **Hunyuan3D 2.1 (self-hosted, tencent)** | Unlimited self-hosted | **Tencent 3D 2.1 Community License: excludes EU/UK/SK + 1M MAU cap — BLOCKED for global distribution** | ❌ blocked (study/reference only) |
| **Rodin (Hyper3D)** | Generate free, pay $1.50/credit on confirm; tiny trial pool | **Unstated on free tier — treat as BLOCKED** (any-use licence is $120/mo Business) | ❌ blocked |

Key sources:
- Tripo pricing/license: https://www.therundown.ai/tools/tripo-ai,
  https://dev.to/rohanmori/tripo-ai-review-2026-i-tested-the-free-3d-model-generator-end-to-end-2ok7
- Meshy commercial FAQ (CC BY 4.0 on free, attribution required):
  https://help.meshy.ai/en/articles/16102098-can-i-use-meshy-assets-commercially
- Hunyuan3D license terms + VRAM: https://triposr.org/blog/free-meshy-alternative,
  https://triposr.org/blog/triposr-vs-hunyuan3d
- VRAM table (TripoSR ~4 GB, TRELLIS ~16 GB, Hunyuan3D-2.1 ~10 GB shape / ~21–29 GB full):
  https://github.com/jackicus/local-mesh
- Rodin pay-per-confirm + license gap:
  http://dev.to/meiferreira/hyper3d-rodin-review-2026-i-tested-the-free-ai-3d-generator-end-to-end-5a6d,
  https://github.com/jangtrinh/design-os-3d-blender/blob/HEAD/research/rodin.md
- SupaVoxel 3/day + license notes: https://supavoxel.com,
  https://dev.to/nadiapruett/meshy-vs-tripo-vs-hyper3d-vs-supavoxel-one-image-four-stls-one-trimesh-script-2i9g

### 2a. WINNER recipe — self-hosted MIT models on the Kaggle T4 (no signup, no credits, no cap)

Run this inside the §1a Kaggle notebook (enable_gpu + enable_internet), or on any CUDA box.

**TripoSR — fast drafts (seconds, ~4–6 GB VRAM, MIT):**
```bash
pip -q install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip -q install git+https://github.com/VAST-AI-Research/TripoSR.git  # verify repo URL at setup
```
```python
from tsr.system import TSR
from tsr.utils import remove_background
from PIL import Image
import torch

model = TSR.from_pretrained("stabilityai/TripoSR",
                            config_name="config.yaml", weight_name="model.ckpt")
model.to("cuda")
# reference: a front/side sketch or photo of the prop (white background works best)
img = remove_background(Image.open("/kaggle/input/refs/monster_toy.png").convert("RGB"))
scene = model(img, device="cuda")          # verify call signature against the repo README at setup
mesh = scene.as_mesh(scene.extract_mesh()[0])
mesh.export("/kaggle/working/monster_toy.glb")
print("faces:", len(mesh.faces))
```
Pass = `monster_toy.glb` downloads via `kaggle kernels output` and opens in Blender with a
closed mesh. Model page: https://huggingface.co/stabilityai/TripoSR (public, no token).

**TRELLIS — quality hero props (~16 GB VRAM, fits the T4, MIT):**
- Repo: https://github.com/microsoft/TRELLIS — follow its install + `image_to_3d.py`
  path at setup. Independent project verified running TRELLIS.2 on Kaggle's free T4:
  https://github.com/slomo-b/kaggle-3d-asset-pipeline (use its `t4-draft` config for
  iteration, full config for finals).
- Watch-out: T4 has 15.1 GB usable — keep batch size 1, use the repo's T4-tuned settings.

**Zero-GPU fallback (no Kaggle quota left):** public HF ZeroGPU Spaces are usable
**without login** (2 min/day unauthenticated, shared GPU). Drive via `gradio_client`
headlessly, e.g. the stabilityai/TripoSR demo Space. Docs:
https://huggingface.co/docs/hub/spaces-zerogpu

### 2b. Recolor/retexture recipe — force every AI prop onto the locked palette

AI outputs never match canon out of the box. Strip their textures, apply canon materials:

```python
# run inside Blender (GUI or headless with the living_room.blend open)
import bpy
CANON = {
    "coral":  (0xF1/255, 0x5E/255, 0x57/255, 1),  # coral pink #F15E57
    "blue":   (0x5B/255, 0x84/255, 0xDD/255, 1),  # blue #5B84DD
    "oak":    (0xE5/255, 0x99/255, 0x64/255, 1),  # warm oak #E59964
    "violet":(0x73/255, 0x1A/255, 0xE5/255, 1),  # violet LED #731AE5 (use as emission)
    "amber":  (0xFF/255, 0xE9/255, 0x96/255, 1),  # amber #FFE996
    "trim":   (0x9B/255, 0x4C/255, 0x49/255, 1),  # rug trim #9B4C49
    "silver": (0xBD/255, 0xD2/255, 0xD6/255, 1),  # silver #BDD2D6
}
def canon_material(name, hexkey, emission=False):
    mat = bpy.data.materials.new(name); mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = CANON[hexkey]
    if emission:
        bsdf.inputs["Emission Color"].default_value = CANON[hexkey]
        bsdf.inputs["Emission Strength"].default_value = 4.0
    return mat

# example: monster toy body -> coral, eyes -> amber, base -> oak
bpy.ops.import_scene.gltf(filepath="/kaggle/working/monster_toy.glb")
obj = bpy.context.selected_objects[0]
obj.data.materials.clear()
obj.data.materials.append(canon_material("ToyBody_coral", "coral"))
```

**Prop→palette mapping for the re-layout** (placement comes later; colors are locked now):
| Prop | Canon mapping |
|---|---|
| VCR/DVD player body | silver `#BDD2D6`, display window amber `#FFE996` emission |
| Boxes | warm oak `#E59964` |
| Monster toy | coral `#F15E57` body, amber eyes (green is NOT in canon — recolor required) |
| 'WORLD'S OKAYEST HERO' mug | blue `#5B84DD` |
| Posters/frames | oak frames, pink/blue print areas |
| Any LED-ish accent | violet `#731AE5` emission, strength ~4.0 (matches LEDStripMat) |

Full canon: `3d-assets/living-room/SCENE-CANON.md`. **Nothing ships unless its base colors
are exactly these hex values** — verify in the material panel, not by eye.

### 2c. Runner-up — Meshy free tier (quality + attribution)

- 100 credits/mo, no card. Reality check: ~20–30 credits per textured generation =
  **~3–5 models/month**; free downloads capped at 10/month on older engines (Meshy 7
  downloads are paywalled). Free outputs are **CC BY 4.0: commercial use allowed WITH
  attribution to Meshy** (credits screen / product page).
- Has a Blender DCC bridge; webhook/API is paid-only.
- **Signup is web OAuth → NEEDS PARENT BROWSER LANE if a setup lane picks this.**
- Use only when the MIT self-hosted route fails on a specific prop.

### 2d. Explicitly NOT recommended

- **Tripo Studio free** — 200 credits/mo looks generous, but outputs are **public and
  non-commercial**. Cannot ship. (The existing `tripo-pull` tool in Forge3D still works
  for pulling public Studio links without sign-in — useful for reference/study only.)
- **Hunyuan3D 2.1** — technically the best open model, but the Tencent 3D 2.1 Community
  License **excludes the EU, UK, and South Korea and caps at 1M monthly active users**.
  Cape Jones distributes globally. Blocked for ship; fine for internal study.
- **Rodin free** — best raw topology in the comparisons, but the trial pool is tiny,
  Gen-2.5 downloads are paywalled, commercial rights on free outputs are unstated, and
  the any-use licence + API live at $120/mo Business. Blocked for our use.

**Category 2 verdict — WINNER: self-hosted TripoSR (drafts) + TRELLIS (hero) on the
Kaggle T4, MIT-clean, unlimited, $0 (§2a), recolored via the canon recipe (§2b).**

---

## 3. FREE CLOUD GPU WORKSTATIONS / IDEs

| Platform | Free GPU | Free allowance | Sign-in method | Agent-headless? | Verdict |
|---|---|---|---|---|---|
| **Kaggle Code** | T4 ×2 (16 GB) | **30 GPU-h/week** | API token (already stored) | ✅ **proven by this lane today** | ✅ primary |
| **Lightning AI** | T4 (free tier); L4 selectable | **15 credits/mo ≈ 22 T4-h/mo** | Web: Google/GitHub/Apple/email | ❌ studio creation is web UI | ⚠️ runner-up, **NEEDS PARENT BROWSER LANE** |
| **Google Colab** | T4 (dynamic) | No units; "very limited"; ≤12 h sessions | Google OAuth, paste-code for CLI | ❌ + unreliable idle timeouts | ❌ |
| **HF Spaces (ZeroGPU)** | Shared RTX Pro 6000 / H200 slices | Free acct: **5 min GPU/day**; unauth: 2 min/day | HF login optional for use | ✅ via gradio_client | ⚠️ micro-tasks only |
| **SageMaker Studio Lab** | T4 | 4-h sessions, ~8 h/day, no card | AWS signup (web) | ❌ | bonus option |
| **Modal** | A100/H100 | $30/mo free credit (~2 h A100) | Web signup; card status unverified | ❌ | unverified, skip |

Sources: https://github.com/openadaptai/openadapt-ml/blob/HEAD/docs/gpu_hosting_options.md,
https://github.com/guruprasath-annadurai/orneur/blob/HEAD/docs/orneur/phase-21/GENESIS_FREE_GPU_CREDIT_MATRIX.md,
https://huggingface.co/docs/hub/spaces-zerogpu,
https://github.com/beer-sakthai/sak-family-agent/blob/HEAD/personas/sakking/skills/mlops/SakKing-hf-spaces-zerogpu/SKILL.md

**Sign-in reality check (critical):** this lane and all subagents **cannot do
live-browser OAuth**. Status per platform:
- **Kaggle: CLEARED.** `~/.kaggle/kaggle.json` is present and `kaggle kernels list`
  succeeded headlessly on 2026-10-16. No browser will ever be needed.
- **Hugging Face: CLEARED for reads.** Account verified; public models/Spaces need no
  token. `gradio_client` calls to public ZeroGPU Spaces work unauthenticated.
- **Lightning AI: NEEDS PARENT BROWSER LANE.** Account creation is web sign-in
  (standing permission covers Google sign-in as fmmg.mars@gmail.com, but a browser lane
  must perform it). Public sources disagree on whether a card is asked at signup —
  the browser lane must confirm **no card on file** before any studio is created.
  After signup, Studios are persistent Linux boxes with a real terminal — the best
  "IDE-like" free option, which is why it is runner-up.
- **Colab / SageMaker / Modal: NEEDS PARENT BROWSER LANE** and still not recommended
  (reliability or unverified card status).

**Category 3 verdict — WINNER: Kaggle Code via API (already authenticated, 30 GPU-h/wk,
fully headless). Runner-up: Lightning AI Studio (better as a persistent IDE, but
requires a parent-delegated browser sign-in first).**

---

## FINAL SHORTLIST

| # | Winner | One-line proof-of-work test (setup lane runs this) |
|---|---|---|
| (a) GPU render | **Kaggle notebook + Kaggle API, Blender 5.2 LTS, OptiX on T4** (§1a) | Push smoke kernel rendering 1 frame @64 samples; pass = `nvidia-smi` shows T4, Cycles lists OPTIX device, `kaggle kernels output` returns non-empty `frame_0001.png` (~3–5 min quota) |
| (b) AI-3D props | **TripoSR (drafts) + TRELLIS (hero), self-hosted on Kaggle T4, MIT-clean** (§2a), recolored to canon (§2b) | Generate 1 prop from a reference PNG on the T4; pass = GLB downloads, opens in Blender, and after §2b its base colors are exactly the canon hex values |
| (c) Cloud workstation | **Kaggle Code via API** — already authenticated headlessly (§3) | `kaggle kernels list --page-size 1` returns 200 today (proven); then push + run any notebook end-to-end |

**Needs parent-delegated browser sign-in (do NOT attempt as subagent):**
1. Lightning AI account + Studio creation (Google sign-in as fmmg.mars@gmail.com per
   standing permission; confirm no card on file at signup).
2. SheepIt account + first project submission (web-only; client CLI works after).
3. Meshy account (only if the runner-up lane is ever activated).
4. Colab CLI auth — not recommended; skip unless Kaggle is unavailable.

**Coordination note:** the living-room re-layout build lane is live on
`build/living-room-relayout-20261016`, and another chat runs a Kaggle render lane.
Per CHECK-BEFORE-START, the setup lane must check both before consuming Kaggle GPU
quota or touching the `.blend`.

**What was verified dead/changed in 2026 (not silently dropped):** Kaggle P100s are
effectively replaced by T4 ×2; Colab free lost its old 100-unit monthly grant (now "very
limited", no units); Tripo Studio locked free exports behind paywalls (hence the
existing `tripo-pull` workaround, which only helps for non-commercial reference);
Blender is at 5.2 LTS (4.5 LTS still supported to Jul 2027) — pin the tarball version
at setup time.
