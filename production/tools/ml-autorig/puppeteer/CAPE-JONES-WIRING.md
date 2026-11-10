# Puppeteer — Cape Jones wiring

**What:** Puppeteer (Seed3D / NTU + ByteDance Seed, NeurIPS 2025 Spotlight).
Automatic rigging AND animation of arbitrary 3D objects: auto-regressive
transformer predicts the skeleton, topology-aware joint-attention predicts
skinning weights, then a differentiable-optimization pipeline animates the
rigged model guided by a video. Ships FBX export (bpy). Successor of the
team's MagicArticulate (CVPR 2025).
Upstream: https://github.com/Seed3D/Puppeteer (commit 1c0f9fc, pulled 2026-10-17).
Paper: https://arxiv.org/pdf/2508.10898

**Why here:** the standing task is "auto-rig Tripo models perfectly" PLUS
"rig AND ANIMATE the Cape Jones model" (owner 2026-10-16). Puppeteer is the
only pulled tool that does BOTH halves of that sentence in one framework:
skeleton+skin in seconds on GPU, then **video-guided animation** — the
Cape Jones model could be animated from reference video (a walk cycle, a
punch) with no hand keyframes. It complements TokenRig (best single-pass
skin quality), UniRig (MIT baseline), afk-rig (local CPU pass + CC0 anim
library), and BlenRig 6 (artist control rig + full face).

**Verified this lane (2026-10-17, own-eyes):**
- All 38 `.py` files pass `python3 -m py_compile`.
- `LICENSE` is **Apache-2.0** — read on the GitHub repo page this run — license gate PASSED.
- Code + scripts only, 4.7MB (largest file 1.6MB demo texture); model weights were
  NOT pulled (they stay off local disk per law — see below).
- Demo media pruned: kept `examples/deer.obj` (262KB) as a CPU smoke-test mesh;
  dropped 12MB textures + input.mp4 videos (GPU machine downloads the full upstream
  repo or re-downloads demo inputs as needed).
- `__pycache__` removed post-compile so it never lands in the commit.

## Requirements (GPU machine — Kaggle / Colab, NOT the local VM)

- Python 3.10, NVIDIA GPU (skeleton inference ≈ 4.6 GB VRAM, 1–2 s/mesh).
- `pip install torch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 --index-url https://download.pytorch.org/whl/cu118`
- `pip install -r requirements.txt`
- `pip install flash-attn==2.6.3 --no-build-isolation` (may need retry; per upstream guide)
- `pip install torch-scatter -f https://data.pyg.org/whl/torch-2.1.1+cu118.html`
- `pip install --no-index --no-cache-dir pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py310_cu118_pyt211/download.html`
- FBX export only: `pip install bpy==4.2.0`
- **Submodules:** the animation pipeline needs `animation/third_partys/`
  (Video_Depth_Anything, co_tracker, ptlflow) and `skinning/third_partys/PartField`
  and `skeleton/third_partys/Michelangelo` — clone upstream `--recursive` on the
  GPU machine (`.gitmodules` lists them; not vendored here).

## Model weights (download on the GPU machine — NOT committed here)

Each folder has its own `download.py` / README with HF links:
- `skeleton/`: `skeleton_ckpts/puppeteer_skeleton_w_diverse_pose.pth`
  (+ bone-token variant `..._bone_token.pth` if joint results disappoint) —
  plus Michelangelo `aligned_shape_latents` (https://huggingface.co/Maikou/Michelangelo)
- `skinning/`: `skinning_ckpts/puppeteer_skin_w_diverse_pose_depth1.pth` —
  plus PartField ckpt (https://huggingface.co/mikaelaangel/partfield-ckpt)
- `animation/`: CoTracker3 (https://huggingface.co/facebook/cotracker3) +
  Video-Depth-Anything-Large (https://huggingface.co/depth-anything/Video-Depth-Anything-Large)
- All released weights: https://huggingface.co/Seed3D/Puppeteer

## Usage (Cape Jones model)

Full auto-rig (GPU machine), from the repo root:

```bash
bash demo_rigging.sh     # reads examples/, writes results/final_rigging/*.txt
```

For Cape Jones, drop the model (OBJ) into `examples/` first. Tripo multi-shell
note: the demo passes `--apply_marching_cubes`, which fuses shells — the same
remesh-fusion the Tripo multi-shell finding requires (matches afk-rig/Pinocchio handling).

FBX export (for import into Blender 4.0.2 on the VM):

```bash
python export.py --mesh <cape-jones>.glb --rig results/final_rigging/<cape-jones>.txt \
    --output cape_jones_puppeteer.fbx
```

Video-guided animation (the new capability vs every other pulled rigger):

```bash
# put a guide video at examples/<seq>/input.mp4 + mesh at examples/<seq>.obj,
# rig .txt from demo_rigging.sh, then:
bash demo_animation.sh   # -> results/animation (multi-view render sequence)
```

Ideas for the EP01 work: drive a cape-jones idle/walk from a phone-recorded
reference video; use Puppeteer's rig as the SECOND ML opinion in the weight
bake-off against TokenRig/UniRig/Pinocchio on the shoulder/feet defect zones
(keep the W5r bake-off winner as primary — this is a challenger, not a replacement).

## Lane position (vs the other riggers)

| Lane | Type | Face | Control rig | Video-guided anim | License |
|---|---|---|---|---|---|
| Puppeteer (here) | ML, GPU | — | — | **yes** | Apache-2.0 ✅ |
| TokenRig/SkinTokens | ML, GPU | — | — | — | MIT ✅ |
| UniRig | ML, GPU | — | — | — | MIT ✅ |
| afk-rig | CPU/agent loop + 178 CC0 anims | — | — | no (but has anim lib) | MIT/CC0 ✅ |
| BlenRig 6 | artist-driven | **full** | **full IK/FK** | — | GPL-3.0 ✅ |
| Pinocchio | CPU, template fit | — | — | — | LGPL/MIT ✅ |

Suggested path: Puppeteer one-shot rig+skin → bake-off compare vs TokenRig →
BlenRig 6 for the final control rig + face → afk-rig's CC0 clips as EP01
blocking anims.
