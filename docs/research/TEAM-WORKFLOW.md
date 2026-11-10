# Team Workflow — AI Agent Team on Cape Jones Video Pipeline

**Date:** 2026-10-16
**Team lead:** Coordinator subagent (this session)
**Members:** agy (Antigravity CLI), opencode, aider, main agent (browser/repo ops)

## Mission

Owner's direction: "Get the videos done. Pull in COMPLETE WORKING SYSTEMS, not
hand-tooled prototypes. Work autonomously as a team."

## What the Team Accomplished

### 1. ToonCrafter — FIXED (weights cached)

**Problem:** Every run re-downloaded 10.5GB model.ckpt from HuggingFace; download
failed at 99% on v3, killing the run.

**Fix (already in repo):**
- `marsfmmg/tooncrafter-weights` Kaggle dataset created with model.ckpt
  (10,502,492,136 bytes, verified via `kaggle datasets files`)
- `production/kaggle/tooncrafter/gen_notebook.py` has cache-first logic:
  checks `/kaggle/input/tooncrafter-weights/model.ckpt` → copies if present →
  downloads from HF only on cache miss
- Notebook regenerated, cache logic verified in cell 4

**Status:** Ready. Next run with the dataset attached will skip the download.

### 2. Viggle-Animate — DEAD END (documented honestly)

**Problem:** Never worked end-to-end on any attempt.

**Root causes found (verified, not guessed):**
1. **VRAM:** Viggle-Animate needs 73.5 GiB (62 GiB transformer + VAEs).
   Our T4 has 16 GiB. Physical impossibility — not a setup issue.
   Source: official HF Space README, verbatim.
2. **License:** MiniMax H3 Community License EXCLUDES the USA (plus EU, UK, Korea).
   Owner is in USA. Cannot legally use these weights.
   Source: HF LICENSE file, verbatim.

Full analysis: `docs/research/VIGGLE-ANIMATE-ASSESSMENT.md`

**Pivot:** One-to-All Animation 1.3B (CVPR 2026, Apache-2.0) — authors verify it
runs on Kaggle's free 16GB T4. Already in `production/tools/one-to-all-animation/`.

### 3. One-to-All Animation — Notebook Built

**Deliverable:** `production/kaggle/one-to-all/gen_notebook.py` + generated
`cape_jones_one_to_all_kaggle.ipynb` (9 cells, all compile-verified).

**What it does:**
- GPU check → deps install → checkpoint download (HF, cache-first) →
  input staging from `marsfmmg/cape-jones-viggle-inputs` dataset →
  author's `inference_1.3b.py` (not hand-tooled) →
  output to `/kaggle/working/` + bulletproof saver checkpoint

**Status:** Built, compile-verified. **Needs live T4 test** (first run will reveal
any CLI/input-format mismatches in the author's script).

### 4. Pipeline Integration

Both tools output to `/kaggle/working/` with bulletproof saver checkpoints.
Downstream (`finish.py` → grading → audio → delivery) is unchanged.

## How the Team Coordinated

**Branch-per-workstream:** All work on `team/body-replacement-pivot-20261016`.
No collisions because each deliverable was a separate file.

**Laws followed:**
- CHECK → RESEARCH → WIRE → DO (researched Viggle VRAM/license BEFORE pivoting)
- NO-HAND-TOOLING: One-to-All notebook calls the author's scripts directly;
  we wire inputs/outputs, we don't rewrite their inference
- VERIFY-BEFORE-CLAIMING: every claim tagged (verbatim / verified / single-source)
- ANTI-SYCOPHANCY: reported the Viggle dead-end honestly instead of claiming
  "we'll make it work"
- Branch → PR → merge (this doc is part of the PR)

**Agent roles:**
- Coordinator (this session): research, architecture decisions, generator code,
  docs, PR
- agy / opencode: installed and ready, but need browser OAuth/API keys to
  activate (parent handles via browser — documented in AI-AGENTS-SETUP.md)
- aider: binary broken in this environment (traceback on --version); needs reinstall
- Main agent: browser work (dataset attach, OAuth, Colab), PR merges, verification

## What Needs Browser Work (parent)

1. **Attach datasets** to new Kaggle kernels (API doesn't propagate dataset_sources):
   - `marsfmmg/tooncrafter-weights` → ToonCrafter kernel
   - `marsfmmg/cape-jones-viggle-inputs` → One-to-All kernel
2. **agy OAuth:** run `agy`, sign in with fmmg.mars@gmail.com
3. **API keys:** GEMINI_API_KEY from aistudio.google.com for opencode/aider
4. **Test One-to-All** on Kaggle T4 (first live run)

## Files Changed (this PR)

- `docs/research/VIGGLE-ANIMATE-ASSESSMENT.md` (new) — honest dead-end analysis
- `docs/research/TEAM-WORKFLOW.md` (new, this file) — team coordination
- `production/kaggle/one-to-all/gen_notebook.py` (new) — notebook generator
- `production/kaggle/one-to-all/cape_jones_one_to_all_kaggle.ipynb` (new) — generated
- `production/kaggle/tooncrafter/cape_jones_tooncrafter_kaggle.ipynb` (regenerated) — cache logic confirmed
