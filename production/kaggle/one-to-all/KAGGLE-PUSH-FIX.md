# Kaggle Push Fix — dataset_sources (2026-10-16)

## The problem (verified)
Kernels pushed via `kaggle kernels push` were hitting `FileNotFoundError` on
`/kaggle/input/...` because **no datasets were attached**. This was reported as
"the Kaggle API doesn't attach datasets to kernels."

It does. The push metadata just had `"dataset_sources": []`.

## The fix
`kernel-metadata.json` (in this directory) now sets:

```json
"dataset_sources": ["marsfmmg/cape-jones-viggle-inputs"]
```

The dataset was verified to exist via `kaggle datasets list --mine`
(`marsfmmg/cape-jones-viggle-inputs`, 6.4MB, updated 2026-10-16).

## How to push with datasets attached
```bash
cd production/kaggle/one-to-all
kaggle kernels push -p .
```
The Kaggle API reads `dataset_sources` from `kernel-metadata.json` and attaches
them — no manual "Attach dataset" step in the web UI needed.

## Related
- The weight-seeding scripts (`production/kaggle/weight-seeding/gen_*.py`)
  already emit the `dataset_sources` field (empty). The mechanism was known;
  it just wasn't populated for the one-to-all / tooncrafter pushes.
- The one-to-all notebook itself should ALSO be rebuilt on the authors'
  official ComfyUI 1.3B T4 path (see `docs/research/BETTER-ALTERNATIVES-2026.md`)
  — the raw-inference notebook is what put the kernel in ERROR state.
