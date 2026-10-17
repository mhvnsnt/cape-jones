# MagicArticulate vs W5r — weight bake-off verdict

**Date:** 2026-10-17 · **Lane:** builder (Aider + Copilot CLI) · **Task:** evaluate
MagicArticulate (PR #89, `production/tools/ml-autorig/magicarticulate/`) against the
W5r weight baseline on Cape Jones — run it on the model, score it on the same 7-pose
test, report honestly whether it beats W5r anywhere.

## Verdict: LOSES — structural, not marginal

MagicArticulate **cannot be scored on the 7-pose weight test**: its public code
release contains **no skinning-weight inference at all**. Its inference code is
skeleton-generation only. (Precision note: `data_utils/` does contain tooling that
reads, cleans, and stores *existing* skinning-weight annotations from datasets —
`clean_skin_in_npz.py`, `read_rig_mesh_from_glb.py`, `save_npz.py` — but nothing
that *predicts* weights for a new mesh.) The CVPR 2025 paper describes
functional-diffusion skinning, but the authors never released that code.

**Evidence (verified 2026-10-17, 4 independent checks):**
1. Local vendored tree (`production/tools/ml-autorig/magicarticulate/`, 18 `.py`
   files, py_compile OK): `demo.py` runs SkeletonGPT skeleton generation only
   (joints/bones → `skeleton.txt` in Rignet format, skeleton OBJ, preview renders).
   No skinning model, no weight-prediction script, no `skinning/` directory.
2. Upstream GitHub root listing (api.github.com): directories are `data_utils`,
   `examples`, `skeleton_models`, `utils` — no skinning directory.
3. Upstream recursive file tree (49 files via GitHub API): zero skinning-inference
   files. The only file with "skin" in the name is
   `data_utils/clean_skin_in_npz.py` — a dataset cleanup script, not inference.
   Zero infer/predict scripts of any kind.
4. Web search: the paper (arXiv 2502.12135) confirms functional-diffusion skinning
   is described but no public skinning code release exists. The HuggingFace hub
   `Seed3D/MagicArticulate` hosts only the two skeleton checkpoints
   (`skeleton_ckpt/checkpoint_trainonv2_hier.pth`,
   `skeleton_ckpt/checkpoint_trainonv2_spatial.pth`).

What MagicArticulate CAN produce (GPU, 1–2 s/mesh): joint positions + bone hierarchy,
`skeleton.txt` (Rignet format), skeleton OBJ, preview renders. **No per-vertex weights.**

## Consequence

- **No GPU job for a weight test.** Queuing one would burn the owner's finite Kaggle
  GPU hours on a run that cannot produce weights. Logged here instead, per the
  working-smart laws.
- **Puppeteer is this family's real weight contender.** Same team (ByteDance Seed),
  MagicArticulate's successor, and its vendored tree HAS `skinning/` +
  `skinning_models/`. It is already queued after UniRig in the GPU lane — the
  neural-rigger-vs-W5r question gets its honest answer from Puppeteer (and UniRig),
  not MagicArticulate.
- **MagicArticulate's complementary role stands: fast skeleton-proposer.** 1–2 s
  joint-layout proposals on GPU, cross-checked against UniRig/Puppeteer/CJ-TEST
  layouts before the skinning pick. The existing queue plan (skeleton proof job
  behind UniRig/Puppeteer) already covers this — no new GPU job added by this
  evaluation.

## If it complements (shoulders)

If a future MagicArticulate skeleton shows better shoulder joint placement than the
CJ-TEST skeleton, the path is: MA skeleton + W5r weights — re-run Surface Heat
Diffuse against the MA bone layout per
`3d-assets/cape-jones-rig/WEIGHT-BAKEOFF-RESULT.md` § "Applying the winning
TECHNIQUE", then score on the 7-pose suite via
`tools/weights/cj_bakeoff/bakeoff.py`. No new tooling needed — the harness already
takes any (mesh, rig) pair.
