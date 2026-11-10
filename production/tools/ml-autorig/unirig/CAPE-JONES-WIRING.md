# UniRig — Cape Jones wiring

**What:** UniRig (Tsinghua + Tripo / VAST-AI-Research, SIGGRAPH 2025).
Two-stage template-free ML auto-rigger: GPT-like transformer predicts a
topologically valid skeleton (Skeleton Tree Tokenization), then a
Bone-Point Cross-Attention stage predicts per-vertex skinning weights and
bone attributes (e.g. stiffness for physics secondary motion) on top of it.
Handles humans, animals, AND objects — the same stack behind Tripo's own
auto-rigging.
Upstream: https://github.com/VAST-AI-Research/UniRig (commit 6793c66,
pulled 2026-10-18).
Paper: https://arxiv.org/abs/2503.19816 (SIGGRAPH 2025)

**Why here:** this is the repo's DOCUMENTED FALLBACK (see
`docs/research/AUTO-RIGGING-TOOLS-2026.md`): if SkinTokens/TokenRig's
single pass bleeds weights on the cape/edge zones of the Cape Jones mesh,
fall back to UniRig's two-stage pipeline (skeleton first, inspect, then
skin). MIT license = cleanest commercial terms of the ML bunch, and it
ships working `launch/inference/*.sh` scripts — the closest thing to a
headless rig pipeline of the GPU set. It complements TokenRig (best
single-pass skin quality), Puppeteer (rig + video-guided animation),
MagicArticulate (fast skeleton-proposer), Make-It-Animatable (any-pose →
rest-pose reset), afk-rig (local CPU pass + CC0 anim library), and BlenRig 6
(artist control rig + full face).

**Verified this lane (2026-10-18, own-eyes):**
- All 89 `.py` files pass `python3 -m py_compile`.
- `LICENSE` is **MIT** — read raw from upstream this run — license gate PASSED.
- Code + launch scripts + example test meshes only, 6.9MB (largest file
  1.8MB `examples/tripo_carrot.glb`); model weights were NOT pulled
  (they stay off local disk per law — see below).
- Demo media pruned: dropped `assets/doc/*.{png,gif}` (~17MB teaser/marketing
  renders, per repo convention); kept the `examples/*.glb` + `examples/skeleton/`
  test meshes the `launch/inference/*.sh` scripts reference.
- `.git` stripped (not a submodule); upstream has no `.gitea`/`.vscode` in-tree.
- `__pycache__` removed post-compile so it never lands in the commit.

**GPU run path (Kaggle / Colab — NOT the VM):**

1. `python3.11` + `pip install torch>=2.3.1 torchvision`
2. `pip install -r requirements.txt`
3. `pip install spconv-<your-cuda-version>` (from https://github.com/traveller59/spconv)
4. `pip install torch_scatter torch_cluster -f https://data.pyg.org/whl/torch-<ver>+<cuda>.html --no-cache-dir`
5. `pip install numpy==1.26.4` (flash_attn: follow the flash-attention repo if it errors)
6. Weights: skeleton + skinning checkpoints trained on Articulation-XL2.0
   download automatically via the HF hub on first script run (never committed).

**Three-step inference (headless-friendly):**

```bash
# 1. skeleton
bash launch/inference/generate_skeleton.sh --input cape_jones.glb --output results/cj_skeleton.fbx
# 2. skinning (REFINE the skeleton first — garbage bones here degrade weights a lot)
bash launch/inference/generate_skin.sh --input results/cj_skeleton.fbx --output results/cj_skin.fbx
# 3. merge into a fully rigged GLB
bash launch/inference/merge.sh --source results/cj_skin.fbx --target cape_jones.glb --output results/cj_rigged.glb
```

**Cape Jones bake-off role:** TokenRig runs first; UniRig runs as the
two-stage fallback on the same input mesh. Score it on: joint count /
placement vs. the T-pose bake-off reference, weight row-sums ≈ 1.0,
per-bone max influence, and zero cape bleed (cape excluded from fitting or
weights cleaned post-hoc). Its Bone Attribute Prediction (stiffness,
planned for a later release) maps to the cape physics work.
