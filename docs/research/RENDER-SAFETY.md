# RENDER-SAFETY.md — Bulletproof Output Saving for Kaggle GPU Renders

**Why this exists:** On 2026-10-16 we lost a 250-frame render zip — 12+ hours of
GPU work — because the Kaggle interactive session died before Quick Save went
through. The owner's words: *"How did we lose a whole zip of stuff we spent a
whole day working on?"* This system makes that impossible. Ever again.

## The core insight

**Quick Save is fragile. Kaggle dataset versions are not.**

- Quick Save requires the session to be alive, the browser to be watching, and
  a human (or agent) to click at the right moment. Any failure in that chain
  loses everything.
- `kaggle datasets version`, run **from inside the kernel**, publishes outputs
  to Kaggle's storage immediately — independent of the session, the browser, or
  Quick Save. Kaggle kernels are **pre-authenticated as the notebook owner**
  (no API keys, no credential cells). This is the production pattern used by
  real 2026 teams (verified: CodeWithOz/birdclef_2026 and umud-challenge
  AGENTS.md — *"Publish from the notebook ... with fallback to datasets
  create"*).
- Dataset versions survive session death. Quick Save doesn't.

**Rule: checkpoint after EVERY unit of work. Never only at the end.**

## Architecture

```
┌─ IN-KERNEL (no secrets, pre-authenticated) ─────────────┐
│ save_outputs.py::RenderSaver                            │
│   checkpoint(name, paths)                               │
│     1. stage files → .save_stage/ (+ manifest.json)     │
│     2. kaggle datasets version (fallback: create)       │
│     3. verify rc==0 + parse version number              │
│     4. record in .save_state.json                       │
│   watchdog thread: heartbeat every 120s                 │
│   atexit/SIGTERM: final emergency version (if dirty)    │
│   restore_from_input(): resume from attached dataset    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─ QUEUE-SIDE on VM (real creds live here, never in kernel) ┐
│ kaggle_queue.py                                          │
│   --save-dataset: pre-creates dataset, attaches as input,│
│                   injects KAGGLE_SAVE_DATASET            │
│   on job error: ONE auto-retry (notebook resumes from   │
│                 save dataset — never starts from zero)   │
│   on job done: publish_second_copies()                  │
│     --gh-release-tag + --gh-repo → gh release upload    │
│     --terabox-dir → tbupload.py upload                  │
└─────────────────────────────────────────────────────────┘
```

### Why GitHub/TeraBox are queue-side, not in-kernel

In-kernel uploads would need secrets inside the notebook source. Even in a
private kernel, that's worse than keeping them on the VM. The dataset version
is the primary bulletproof copy (zero secrets); GitHub releases and TeraBox
are second copies made from the VM after outputs land. The task spec allowed
AND/OR — this is the most secure correct design.

### The zip-extraction quirk

Kaggle **automatically extracts zip files on the dataset input mount**
(`/kaggle/input/...` shows extracted files, not zips). `kaggle datasets
download` returns the original files. So:

- `restore_from_input()` searches for the exact filename via rglob, and falls
  back to **re-zipping** an extracted frame directory into the expected zip
  name. Resume works regardless of layout.
- Queue-side verification uses `kaggle datasets download` (originals) and
  checks sha256 against `manifest.json`.

## Files

| File | Repo location | Purpose |
|------|---------------|---------|
| `save_outputs.py` | `mhvnsnt/cape-jones` `production/pipeline/` | In-kernel saver module (stdlib only). Also embedded into notebooks. |
| `kaggle_queue.py` | `mhvnsnt/cape-jones` `production/pipeline/` | `--save-dataset`, `--gh-repo/tag`, `--terabox-dir`, `ensure_save_dataset()`, `publish_second_copies()`, auto-retry-once |
| `gen_notebook_v4.py` | `mhvnsnt/western-heart` `promo/pantera-entrance-v1/kaggle/` | Embeds saver; segmented render (SAVE_SEGMENTS=3) with per-segment checkpoints; restore cell |
| `pantera_kaggle_render_v4.ipynb` | same as above | Generated notebook (8 cells) |
| `render_parallel.py` | same as above | `--save-dataset-base` → per-split datasets (`-s0`, `-s1`...), `SAVE_SEGMENTS=1` per split |

## Usage

```bash
# Single render, bulletproof:
python3 ~/workspace/tools/kaggle-queue/kaggle_queue.py add \
  --notebook ~/workspace/kaggle-pantera-render/pantera_kaggle_render_v4.ipynb \
  --title "pantera v4" \
  --save-dataset marsfmmg/pantera-v4-outputs \
  --gh-repo mhvnsnt/western-heart --gh-release-tag pantera-v4-outputs \
  --terabox-dir /renders/pantera

# Parallel render, bulletproof:
python3 ~/workspace/kaggle-pantera-render/render_parallel.py \
  --frames 0-1499 --splits 3 --title "pantera v4" \
  --save-dataset-base marsfmmg/pantera-v4-outputs
```

The queue's `tick` handles the rest: per-checkpoint dataset versions happen
in-kernel; on kernel death the job auto-retries once and resumes from the save
dataset; on completion, second copies go to GitHub/TeraBox.

## Failure matrix — what kills what, and what survives

| Failure | Old system | New system |
|---------|-----------|------------|
| Session dies mid-render | everything lost | all completed segments safe as dataset versions; retry resumes |
| Session dies before Quick Save | everything lost | irrelevant — nothing waits for Quick Save |
| Browser agent stalls | render unmonitored | in-kernel watchdog + heartbeats; queue notifies on failure |
| `kaggle datasets version` fails | n/a | logged loudly, render continues, retried at next checkpoint; local zip remains fallback |
| Kernel errors out | manual restart from zero | **one automatic resume-retry** from save dataset |
| Dataset API down | n/a | checkpoint returns False, loudly logged; never blocks render |

## What was tested (mock, no network)

`save_outputs.py` was exercised against a mock `kaggle` CLI:

- checkpoint → `version` on missing dataset → falls back to `create` → v1 ✓
- subsequent checkpoints → v2, v3... with version numbers parsed ✓
- `manifest.json` records every checkpoint + dataset version ✓
- heartbeat file written ✓
- atexit emergency save fires; skips when nothing changed ✓
- `restore_from_input` with Kaggle's extracted-on-mount layout → re-zips to
  expected filename, content round-trips byte-identical ✓
- save failure (rc!=0) → returns False, logs loudly, render continues ✓

The embedded-in-notebook path (config cell → saver cell → checkpoint) was
also dry-run against the mock. Live-Kaggle validation is still owed before
trusting it for a production run — the first v4 bulletproof run should be
watched.

## For interactive sessions (the original incident)

The incident was an interactive session. Going forward:

1. **Prefer batch kernels via the queue** — outputs in `/kaggle/working` are
   auto-captured on clean completion AND dataset versions protect against
   mid-run death. No browser needed, no Quick Save roulette.
2. If an interactive session is unavoidable, the notebook's saver still
   checkpoints per segment — the browser agent's only job is to keep the
   session alive, not to save.
3. Never rely on Quick Save as the sole persistence mechanism. Ever.

## Open items

- Live-Kaggle validation of the first bulletproof v4 run (watch it).
- ToonCrafter/Viggle notebooks: same saver pattern applies; integrate when
  those notebooks are next regenerated.
- `kaggle datasets version` upload speed for ~500MB segments: measured on
  first live run; if slow, reduce segment size or parallelize.
