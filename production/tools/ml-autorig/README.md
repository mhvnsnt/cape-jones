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
| **HumanRig** (Alibaba Amap, CVPR 2025) | **MIT ✅** | Humanoid-only; 2D-prior skeleton estimator + point-transformer skinning; strong on AI-generated meshes. | runbook below (not yet queued) |
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

## HumanRig runbook (Kaggle/Colab, MIT)

Repo: `https://github.com/c8241998/HumanRig` — follow its README; needs
CUDA GPU. Humanoid characters only (uniform skeleton topology).

## Results ledger

| Date | Tool | Proof | Verdict |
|---|---|---|---|
| 2026-10-17 | UniRig | queued (pending GPU) | — |
| 2026-10-17 | Pinocchio (CPU lane) | `../pinocchio/proof/` | see main research doc |
| 2026-10-17 | Puppeteer | pulled code-only (`puppeteer/`, wiring doc) | queued after UniRig — brings video-guided animation |
