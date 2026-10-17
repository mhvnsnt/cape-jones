# Make-It-Animatable — Cape Jones wiring

**What:** Make-It-Animatable (jasongzy/Make-It-Animatable) — official implementation
of the CVPR 2025 Highlight paper "Make-It-Animatable: An Efficient Framework for
Authoring Animation-Ready 3D Characters" (Zhiyang Guo et al.; work done during a
Tencent PCG internship). Unified particle-autoencoder framework that outputs
**blend weights + bones + pose transformations** for ANY humanoid 3D model
(meshes AND 3D Gaussian splats) in **< 1 second** — regardless of the input
pose.

**License:** MIT (LICENSE on disk, own-eyes verified) — commercial use allowed.

**Where:** `production/tools/ml-autorig/make-it-animatable/` — code only (1.5 MB,
largest file `assets/teaser.jpg` 1.1 MB). Submodules intentionally excluded
(`util/auto_rig_pro`, `util/3dgs-render-blender-addon`) — fetch on the GPU
machine with `git submodule update --init` if needed.

## Why it matters for Cape Jones (lane differentiators)

1. **Arbitrary-pose input.** Unlike most riggers that need a clean T-pose,
   MIA accepts a model in any pose and **resets it to a rest pose** as part of
   the pipeline (`pose` prediction head). If a Tripo variant comes back in a
   non-T pose, MIA still works.
2. **Sub-second inference.** Fastest of the pulled ML riggers — good for
   iterating on variants.
3. **Fine-grained skeleton + optional extra body-structure bones.** Can emit
   richer skeletons than Mixamo-standard (extra bones for unusual structures) —
   useful for CJ's wrist blasters / cape bones.
4. **Blender integration built in** (`app_blender.py`): consumes the predicted
   joints/weights dict and builds the armature directly in Blender (bpy). That
   is the CJ path: predict on GPU machine → `app_blender.py` → armature lands
   in the scene at native scale.
5. **MIA v2 exists** (separate `v2` branch): upgraded to the Hunyuan3D 2.1
   ShapeVAE backbone, retrained models, better skinning post-processing and
   Blender integration. Mesh inputs only; run with `python app_v2.py`.

## GPU machine setup (Kaggle / Colab — NOT the VM)

```bash
git clone https://github.com/jasongzy/Make-It-Animatable --recursive --single-branch
cd Make-It-Animatable
pip install -r requirements.txt   # torch 2.1.2 cu121, pytorch3d 0.7.7, bpy 4.3.0

# Pretrained weights — DOWNLOAD ON THE GPU MACHINE, NEVER COMMIT:
hf download jasongzy/Make-It-Animatable --include 'output/best/new/**' --local-dir .
# MIA v2 weights live on the v2 branch / the same HF repo.

# Example data (optional):
hf download jasongzy/Make-It-Animatable --include 'data/**' --local-dir .
```

## Inference paths

| Path | Command | Output |
|---|---|---|
| Gradio demo | `python app.py` | interactive rig in the browser |
| Batch / scripted | `python test.py` pattern (see `test.py`: `PCAE` model → joints + joints_tail + blend weights → post-process) | joints/bw dict |
| Blender armature | `python app_blender.py --input_path <npy from test/app>` | Blender armature + skinned mesh |

The v1 pipeline predicts in three heads (weights, joints, joints+tails) that are
trained separately; `test.py` shows the canonical composition. For the hero
rig, consider **v2** (`python app_v2.py`) — better post-processing and
Hunyuan3D 2.1 backbone.

## Cape Jones run notes

- **Scale:** keep native 0.925 m — do NOT rescale the model. MIA's pose-reset
  head preserves scale; verify the armature spans ~0.925 m before export.
- **Cape:** MIA's skinning sees the cape as part of the body shell. For the
  hero rig, either (a) separate the cape before running and rig it with the
  cloth-sim lane, or (b) run once on the full mesh and use afk-rig's `weights`
  rules to repair cape-bleed zones.
- **Multi-shell:** MIA handles AI topology via the particle encoder; no voxel
  remesh required (unlike Pinocchio).
- **Mixamo skeleton:** MIA's default bones follow Mixamo naming
  (`mixamorig:`) — the Blender script applies finger cleanup
  (`remove_fingers_from_data`) when merging fingers into hands; CJ finger
  handling per the W5r bake-off defect zones.

## Comparison vs the other pulled riggers

| | MIA | UniRig | Puppeteer | SkinTokens/TokenRig | afk-rig (local) |
|---|---|---|---|---|---|
| Input pose | **any pose** | T-pose-ish | any | any | T/A-pose |
| Inference | <1s | seconds | 1–2s | single pass | instant CPU |
| Skeleton detail | fine-grained + extras | diverse templates | fixed | learned | 66-bone human |
| Gaussian splats | ✅ | ❌ | ❌ | ❌ | ❌ |
| Blender build | ✅ `app_blender.py` | notebook | export.py | manual | export |

**Upstream:** https://github.com/jasongzy/Make-It-Animatable (pulled 2026-10-17,
upstream commit 8fb51382ff6da556cdb95cc03a48200603f3a493).
Weights: https://huggingface.co/jasongzy/Make-It-Animatable (fetch on GPU machine).
Paper: https://arxiv.org/abs/2411.18197. Project: https://jasongzy.github.io/Make-It-Animatable/.
