# KAGGLE-SAVE-RESEARCH.md — Why Outputs Get Lost + How to Render Faster

**Date:** 2026-10-16
**Incident:** 4 Pantera render chunks (1000 frames, ~8 GPU-hours) lost because "Quick Save" was used instead of "Save & Run All". Quick Save does NOT preserve `/kaggle/working/` files.

---

## PROBLEM 1: Kaggle Output Preservation

### Why Quick Save doesn't capture outputs

This is **documented Kaggle behavior**, not a bug:

| Action | What it does | Captures /kaggle/working/? |
|--------|--------------|---------------------------|
| **Quick Save** | Saves notebook code "as it is on screen", no re-run | **NO** — code only, 0 output files |
| **Save & Run All** (commit) | Re-executes entire notebook in a fresh session, saves version | **YES** — up to 20GB of `/kaggle/working/` |

Sources:
- Kaggle's own notebook template: "You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using **'Save & Run All**'"
- TU Delft course guide: "Quick Save stores the notebook as it is on screen, **without re-running it**. Save & Run All re-executes everything from a clean session."
- Verified empirically 2026-10-16: versions #2, #3, #4 (Quick Saves) showed **0 files** in Output tab. Version #6 (Save & Run All) showed **500 files** including the chunk zip.

### Why this is confusing

The interactive session's right-panel Output listing **shows live session files**, making it look like outputs are "saved". They are not. `/kaggle/working/` is ephemeral — cleared when the session ends (~20 min idle timeout, 12h hard limit). The files only become durable when a **completed commit** captures them.

### Correct patterns for preserving large outputs

**Pattern A: Commit per checkpoint (simplest, bulletproof)**
- After each render chunk completes, click "Save & Run All"
- Downside: re-runs the entire notebook from scratch (~7 min setup each time)
- Mitigation: make the notebook **resumable** — check for existing outputs and skip completed chunks

**Pattern B: Dataset publishing from inside the notebook (fastest, no re-run)**
- Kaggle kernels run as the authenticated notebook owner — no API keys needed
- `!kaggle datasets version -p /kaggle/working/output -m "chunk 3 done"` publishes outputs to a dataset **immediately**, while the session is still alive
- Dataset versions survive session death. This is the **primary mechanism** in our bulletproof save system (`production/pipeline/save_outputs.py`, PR #37)
- Upload speed: ~500MB takes a few minutes on Kaggle's internal network

**Pattern C: External upload during run (for second copies)**
- Upload to TeraBox/GitHub releases from inside the notebook after each chunk
- Requires credentials in notebook source — **security concern**, not recommended for interactive notebooks
- Better: do this queue-side on the VM where creds live (our `kaggle_queue.py --terabox-dir` / `--gh-release-tag` pattern)

**Pattern D: `kaggle kernels output` from outside (recovery)**
- `kaggle kernels output <owner>/<notebook> -p ./out` downloads outputs from the latest completed version
- Only works for **completed commits**, not Quick Saves or dead sessions
- Useful for pulling finished chunks without the browser

### Recommended workflow (going forward)

1. **In-notebook:** `save_outputs.py` publishes a dataset version after EVERY chunk (Pattern B) — zero re-run cost, survives session death
2. **Queue-side:** `kaggle_queue.py` downloads completed outputs and pushes second copies to GitHub releases + TeraBox (Pattern C, safe creds)
3. **Browser lane:** Use "Save & Run All" (never Quick Save) when manual saves are needed (Pattern A)
4. **Never rely on:** Quick Save, the live Output panel, or "the session is still running"

---

## PROBLEM 2: Faster Re-rendering (Same Quality)

### Current state (v4 pipeline)

- Blender 4.5 LTS, 16spp + adaptive threshold 0.05, GPU OIDN, persistent data
- ~2.5s/frame on Kaggle T4 → ~20 min per 250-frame chunk
- 4 missing chunks = ~80 min of pure render time (~2 hours with setup overhead)

### Speedup options (no quality change)

**1. Parallel Kaggle kernels — 2x wall-clock (RECOMMENDED)**
- Kaggle allows **~2 concurrent GPU sessions** (documented in rlaplaza-lab/famex, Sep 2026: "Kaggle rejects a third batch GPU push")
- Run 2 chunks simultaneously on 2 separate notebook commits
- Our `kaggle_queue.py` already supports this: `--max-parallel 2`
- 4 chunks → 2 waves → ~40 min wall-clock instead of ~80 min
- **Zero quality impact** — same settings, just parallel

**2. Colab as second GPU lane — up to 4x wall-clock**
- Google Colab free tier provides T4 GPUs (separate quota from Kaggle)
- Run 2 more chunks on Colab while Kaggle handles 2
- 4 chunks in parallel → ~20 min wall-clock
- Caveat: Colab free-tier GPUs are not guaranteed; sessions can disconnect
- The Colab Blender notebook pattern is already in our repo (`production/colab/`)

**3. Blender 4.5 scene loading improvements — ~5-10% on animation**
- 4.5 loads large geometries 4-6x faster, mesh attributes up to 10x faster
- For animation (geometry reloads per frame), this reduces per-frame overhead
- Already in v4 (we use Blender 4.5 LTS)

**4. Additional Cycles micro-optimizations**
- **Scrambling distance: Automatic** — reduces GPU render time, recommended by Blender devs
- **Light path bounces:** reduce total bounces if the scene doesn't need them (each bounce = more computation)
- These are scene-dependent and need per-scene validation

### Speedup options (need validation before use)

**5. Half-res + SPAN 2x upscale — ~3x (v5 plan)**
- Render at 960x540, upscale to 1920x1080 with SPAN (SOTA efficient super-resolution)
- Research says "none" quality impact, but needs visual confirmation on Pantera
- **Blocked:** SPAN weights not yet downloaded (browser task pending)

**6. Half-fps + RIFE interpolation — ~2x**
- Render at 15fps, interpolate to 30fps with RIFE
- **NOT recommended for Pantera** — owner previously rejected RIFE for introducing ghosting artifacts on cartoon content. On 3D it may be fine, but needs his approval.

### Recommended re-render plan

For the 4 missing Pantera chunks (owner: same quality, get it done):

1. **Use 2 parallel Kaggle commits** (max-parallel 2) with the v4 notebook
2. **Each commit has `save_outputs.py`** publishing dataset versions per chunk — never lose work again
3. **Optional:** add Colab as a 3rd/4th parallel lane if a GPU is available
4. **Estimated wall-clock:** ~40 min (Kaggle x2) or ~20 min (Kaggle x2 + Colab x2)
5. **DO NOT use:** half-res upscale or RIFE without owner approval (quality constraint)

### GPU quota math

- Kaggle: 30 GPU-hours/week. 4 chunks × 20 min = 80 GPU-minutes (~1.3 hours). Well within quota.
- Parallel doesn't cost extra quota — same total GPU-minutes, just less wall-clock time.
- Colab: separate free quota, doesn't touch Kaggle hours.

---

## What Changed in This PR

1. **New:** `docs/research/KAGGLE-SAVE-RESEARCH.md` (this file)
2. **New:** `production/pipeline/kaggle_commit_guide.md` — quick-reference for browser operators: when to use Save & Run All vs Quick Save vs dataset publish
3. **Updated:** `production/pipeline/cycles_speed_config.py` — added `scrambling_distance='AUTOMATIC'` to the animation preset (free GPU speedup)

---

## Sources

- Kaggle notebook template (official): /kaggle/working/ preserved on "Save & Run All"
- TU Delft AE4353 course guide (2026): https://github.com/tudelft/ae4353-y26/blob/HEAD/kaggle.md
- Kaggle CLI reference: https://github.com/shepsci/kaggle-skill/blob/HEAD/skills/kaggle/modules/references/cli-reference.md
- Parallel GPU limit: https://github.com/rlaplaza-lab/famex/commit/416d3e04d9fc52571a1a0490a20bfec92f6d46b5
- Blender 4.5 Cycles: https://developer.blender.org/docs/release_notes/4.5/cycles/
- Free GPU comparison 2026: https://github.com/spinov001-art/free-gpu-machine-learning

---

## Appendix: Production Precedents & Additional Pitfalls (2026-10-16 deep research)

### Dataset Publishing From Inside the Notebook — Production Standard

Multiple 2026 production repos publish Kaggle datasets from inside running kernels as their primary output-preservation mechanism:

- **CodeWithOz/umud-challenge:** "Kaggle-native gen notebooks publish datasets via `kaggle datasets version/create` from inside the prep kernel"
- **alansencinas/lunarsite:** "Checkpoints dataset: trained model weights live in the private dataset. Update with `kaggle datasets version` to publish new versions"
- **basyirin-dev/sigma-model:** Publishes metrics as dataset versions from inside notebooks. When multiple notebooks upload concurrently, adds `time.sleep(random.uniform(5, 30))` before the version call to avoid version conflicts.

Our `production/pipeline/save_outputs.py` implements this exact pattern.

### Papermill IOPub Timeout

Kaggle uses papermill to execute notebooks. Papermill kills the kernel if no output is produced for ~4 seconds.

**Fix:** Ensure regular output during long operations with `flush=True`:
```python
for i, batch in enumerate(dataloader):
    train_step(batch)
    if i % 10 == 0:
        print(f"Step {i}/{len(dataloader)}", flush=True)
```

**Source:** 14790897/my-skills kaggle-kernel-runner SKILL.md

### Dataset Auto-Extraction Quirk

Kaggle automatically extracts `.zip`, `.tar.gz`, `.tar`, `.7z` when uploaded as datasets. If you publish a zip as a dataset version then attach it to another kernel, files arrive extracted — `glob('*.zip')` finds nothing.

**Fix:** When restoring, search by filename recursively and re-zip if needed. Our `save_outputs.py` `restore_from_input()` handles this.

### API-Triggered Runs Lose GPU Flags

`save_notebook` with `SaveAndRunAll` via the Kaggle API executes on **CPU** even when the notebook is configured for GPU. Only browser "Save Version → Save & Run All" provisions GPU.

**Source:** manojdadi56/kaggle AGENTS.md (re-confirmed 2026)

**Implication:** `kaggle kernels push` via CLI *does* trigger a run with saved settings (including GPU). But programmatic `save_notebook` API calls do not preserve GPU. For GPU work pushed via API, verify the run actually got GPU.

### Additional Sources

- https://github.com/codewithoz/umud-challenge/blob/HEAD/AGENTS.md
- https://github.com/alansencinas/lunarsite/blob/HEAD/CLAUDE.md
- https://github.com/basyirin-dev/sigma-model/blob/HEAD/archive/docs/research/kaggle-experiment-architecture.md
- https://github.com/14790897/my-skills/blob/HEAD/skills/kaggle-kernel-runner/SKILL.md
- https://github.com/manojdadi56/kaggle/blob/HEAD/AGENTS.md
- https://github.com/arnavlifelesscoder/ag-ar-gud-stuff/blob/HEAD/KAGGLE_RUNBOOK.md
