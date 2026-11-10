# Kaggle Kernel Fixes — Cape Jones (2026-10-17)

## Verified issues

### 1. dataset_sources empty (fixed in one-to-all, missing elsewhere)
`production/kaggle/one-to-all/KAGGLE-PUSH-FIX.md` documents the root cause:
kernels pushed with `"dataset_sources": []` fail with `FileNotFoundError` on
`/kaggle/input/...` because no datasets are attached.

**Fixed example** (`production/kaggle/one-to-all/kernel-metadata.json`):
```json
"dataset_sources": ["marsfmmg/cape-jones-viggle-inputs"]
```

**Still empty** (needs population):
- `production/kaggle/weight-seeding/seed-output-tooncrafter/kernel-metadata.json`
- `production/kaggle/weight-seeding/seed-output-viggle-*/kernel-metadata.json`

### 2. ToonCrafter notebook — known failure modes
File: `production/kaggle/tooncrafter/cape_jones_tooncrafter_kaggle.ipynb`

Common ERROR causes (from notebook comments + KAGGLE-PUSH-FIX):
- **PATCH ANCHOR NOT FOUND** — upstream `inference.py` changed; the FP16
  `model.half()` patch assert fails.
- **Missing dataset** — notebook looks for
  `/kaggle/input/tooncrafter-weights-fp16/model.ckpt`. If the dataset is not
  attached, it falls back to HuggingFace download (works only if Internet is ON
  and the session doesn't time out).
- **Quick Save** — does not capture `/kaggle/working/`. Must use Save & Run All
  or the bulletproof saver cell.
- **Python version** — Kaggle may be on 3.13; some deps (decord) were already
  removed for that reason. transformers pinned to 4.48.3.

### 3. one-to-all kernel in ERROR
From `KAGGLE-PUSH-FIX.md`:
> the raw-inference notebook is what put the kernel in ERROR state.
> Rebuild on the authors' official ComfyUI 1.3B T4 path.

## Recommended fixes

### A. Populate dataset_sources on all kernel-metadata.json
For ToonCrafter weights seeding, set:
```json
"dataset_sources": ["marsfmmg/tooncrafter-weights-fp16"]
```
(or whatever the actual dataset slug is after the FP16 seeding kernel succeeds).

### B. ToonCrafter notebook hardening
1. Make the FP16 patch non-fatal if the anchor is missing (log and continue).
2. Always prefer the dataset cache; fail fast with a clear message if both
   cache and internet are unavailable.
3. Keep the bulletproof saver cell; document that Quick Save is never enough.

### C. Re-push after metadata fix
```bash
cd production/kaggle/tooncrafter
# ensure kernel-metadata.json exists with dataset_sources populated
kaggle kernels push -p .
```

## Files to edit
- `production/kaggle/weight-seeding/seed-output-tooncrafter/kernel-metadata.json`
- `production/kaggle/tooncrafter/` — add a `kernel-metadata.json` if missing
- Notebook cells that assert on the FP16 patch anchor
