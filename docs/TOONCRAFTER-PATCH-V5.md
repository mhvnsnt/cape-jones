# ToonCrafter FP16 Patch — Non-Fatal Version (v5)

## Problem
The current notebook cell asserts hard if the upstream anchor string is missing:

```python
assert old in src, "PATCH ANCHOR NOT FOUND — upstream inference.py changed, fix me"
```

Any upstream change to `scripts/evaluation/inference.py` turns the whole kernel into ERROR.

## Fix
Replace the assert with a soft check. The cell now:

1. Skips if the file is missing.
2. Skips if the patch is already applied.
3. Applies the patch if the anchor matches.
4. Logs a warning and continues if the anchor is missing.

## How to apply
1. Open `production/kaggle/tooncrafter/cape_jones_tooncrafter_kaggle.ipynb`.
2. Find the cell titled “Patch ToonCrafter for FP16 execution”.
3. Replace its source with the contents of `fp16_patch_cell_v5.py`.
4. Or regenerate the notebook from an updated `gen_notebook.py` that uses the v5 cell.

## Also added
- `kernel-metadata.json` for the ToonCrafter notebook with
  `dataset_sources: ["marsfmmg/tooncrafter-weights-fp16"]`
  (adjust the slug if your actual dataset name differs).

After editing, re-push:

```bash
cd production/kaggle/tooncrafter
kaggle kernels push -p .
```
