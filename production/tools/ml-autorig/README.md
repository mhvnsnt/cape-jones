# ML auto-riggers — GPU lane (Kaggle / Colab)

Template-free neural riggers that handle arbitrary Tripo topology with no
skeleton template. All need a CUDA GPU (≥8GB VRAM) — **they cannot run on
the local VM**, so they run on the owner's Kaggle GPU via the repo's
`production/pipeline/kaggle_queue.py` batch queue (or Colab).

## The lineup (verified 2026-10-17 against real repos/papers)

| Tool | License (commercial?) | What it does | Run path |
|---|---|---|---|
| **UniRig** (Tsinghua + Tripo, SIGGRAPH 2025) | **MIT ✅** | Autoregressive skeleton + bone-point cross-attention skinning. Handles humans, animals, objects. | `kaggle_unirig_capejones.ipynb` (queued) |
| **Puppeteer** (NTU + ByteDance Seed, NeurIPS 2025 Spotlight) | **Apache-2.0 ✅** | Auto-rig + video-guided animation; FBX export. Successor of MagicArticulate. | ✅ **PULLED 2026-10-17** — `puppeteer/` code-only vendored; wiring doc: `puppeteer/CAPE-JONES-WIRING.md`. Runbook below (queue after UniRig) |
| **MagicArticulate** (NTU + ByteDance Seed, CVPR 2025) | **Apache-2.0 ✅** | Skeleton generation + functional-diffusion skinning; 1–2s inference, 4.6GB VRAM. NOTE: **not Meta** — earlier notes saying "Meta's MagicArticulate" are wrong. | runbook below (not yet queued) |
| ~~**HumanRig**~~ (Alibaba Amap, CVPR 2025) | repo MIT but **no public code** ❌ | Humanoid-only paper + HF dataset; repo is a stub (no inference code). Paper reference only, NOT runnable. |
| **Make-It-Animatable** (Tencent, CVPR 2025 Highlight) | **MIT ✅** | Any-pose → rest-pose reset, <1s inference, fine-grained skeleton + extra bones, meshes AND Gaussian splats, Blender armature builder. | ✅ **PULLED 2026-10-17** — `make-it-animatable/` code-only; wiring doc: `make-it-animatable/CAPE-JONES-WIRING.md`. Queue after UniRig; try MIA v2 (`app_v2.py`) too. |
| ~~RigAnything~~ (UCSD + Adobe, SIGGRAPH 2025) | ❌ **Adobe Research License — non-commercial only** | Template-free, ~2s on A100, exports rigged GLB via bpy. | **REJECTED for repo use** (license). Researchers may still run it privately; not wired in. |
| SkinTokens (Tripo/VAST, UniRig successor) | ? | Announced in UniRig README (98–133% better skinning claimed); **no public repo yet** as of 2026-10-17. | Watch; re-evaluate when code drops. |

## Why UniRig first

- MIT license = cleanest commercial terms of the ML bunch.
- Purpose-built for diverse skeletons (not human-only).
- Ships working `launch/inference/*.sh` scripts: skeleton → skin → merge to
  rigged GLB/FBX — closest to a headless pipeline of the group.
- Puppeteer is the quality challenger (newer, Spotlight); queue it second if
  UniRig's install fights back.

## Kaggle proof job (UniRig on Cape Jones)

Notebook: `kaggle_unirig_capejones.ipynb`
Enqueue (GPU frees up automatically; never hand-run):
```bash
python3 production/pipeline/kaggle_queue.py add \
  --notebook production/tools/ml-autorig/kaggle_unirig_capejones.ipynb \
  --title "UniRig auto-rig: Cape Jones proof" \
  --outputs "cj_unirig_rigged.glb,cj_unirig_skeleton.json,cj_unirig_report.json,cj_unirig_pose.png" \
  --output-dir production/tools/ml-autorig/proof/
```
The notebook:
1. Checks GPU, clones `VAST-AI-Research/UniRig`, installs deps.
2. Pulls `cape_jones_plain.glb` from Tripo's public API (no auth).
3. Runs skeleton → skinning → merge on the model.
4. Writes a numeric sanity report (joint count, weight row-sums, per-bone
   max influence) + a before/after LBS pose render.
5. Leaves the rigged GLB + report in `/kaggle/working` for the queue's
   output collector.

After outputs land in `proof/`, render the real verification image in
Blender on the VM (see `proof/render_unirig_proof.py`) and READ it.

## Puppeteer runbook (Kaggle/Colab, Apache-2.0)

```bash
git clone https://github.com/Seed3D/Puppeteer.git --recursive && cd Puppeteer
pip install torch==2.1.1 torchvision==0.16.1 --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
pip install flash-attn==2.6.3 --no-build-isolation   # may fail; retry per repo guide
# download skeleton + skinning checkpoints (see skeleton/, skinning/ READMEs)
bash demo_rigging.sh                                 # rig files -> results/final_rigging
python export.py --mesh cape_jones.glb --rig results/final_rigging/cape_jones.txt \
    --output cape_jones_puppeteer.fbx                # needs bpy==4.2.0
```

## MagicArticulate runbook (Kaggle/Colab, Apache-2.0)

```bash
git clone https://github.com/Seed3D/MagicArticulate.git --recursive && cd MagicArticulate
pip install torch==2.1.1 torchvision==0.16.1 --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
python download.py        # skeleton-generation weights (HF)
bash demo.sh              # set input_dir to your model dir first
```

## HumanRig — NOT runnable (corrected 2026-10-17)

The earlier runbook claim was wrong. Own-eyes check (2026-10-17):
`https://github.com/c8241998/HumanRig` (7 commits) contains only LICENSE,
README, and assets — the README body is literally "TODO — release dataset on
Hugging Face". There is no inference code and no public weights. The paper
remains a useful reference (11k humanoid meshes, 2D-prior skeleton estimator +
point-transformer skinning; strong results on AI-generated meshes), and the
dataset is on HF (`jellyczd/HumanRig`), but nothing here can run. Do not
queue; do not wait for it.

## Make-It-Animatable runbook (Kaggle/Colab, MIT)

**Repo (pulled 2026-10-17, upstream 8fb51382):**
`https://github.com/jasongzy/Make-It-Animatable` — MIT, official
implementation, CVPR 2025 Highlight.

```bash
git clone https://github.com/jasongzy/Make-It-Animatable --recursive --single-branch
cd Make-It-Animatable
pip install -r requirements.txt   # torch 2.1.2 cu121, pytorch3d 0.7.7, bpy 4.3.0
# weights — GPU machine only, never commit:
hf download jasongzy/Make-It-Animatable --include 'output/best/new/**' --local-dir .
# demo:
python app.py                       # gradio UI
# scripted:
python test.py                      # joints + joints_tail + blend weights -> post-process
# build the Blender armature from a prediction dict:
python app_blender.py --input_path <npy>
```

For the hero-rig run, try **MIA v2** as well: `git checkout v2`, `python app_v2.py`
(Hunyuan3D 2.1 ShapeVAE backbone, retrained models, better post-processing,
mesh inputs only).

Cape Jones specifics: keep native 0.925 m (do NOT rescale); run on the body
without the cape or repair cape-bleed with afk-rig `weights` rules; MIA's
`mixamorig:` naming + finger cleanup is in `app_blender.py`. Full lane notes:
`make-it-animatable/CAPE-JONES-WIRING.md`.

## Results ledger

| Date | Tool | Proof | Verdict |
|---|---|---|---|
| 2026-10-17 | UniRig | queued (pending GPU) | — |
| 2026-10-17 | Pinocchio (CPU lane) | `../pinocchio/proof/` | see main research doc |
| 2026-10-17 | Puppeteer | pulled code-only (`puppeteer/`, wiring doc) | queued after UniRig — brings video-guided animation |
| 2026-10-17 | Make-It-Animatable | pulled code-only (`make-it-animatable/`, wiring doc) | queue after UniRig — brings <1s any-pose→rest-pose inference + Blender armature builder; try v2 |
| 2026-10-17 | HumanRig | own-eyes check: repo is a stub, no public code | NOT runnable — paper + HF dataset reference only |
