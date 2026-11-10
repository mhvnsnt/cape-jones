# Updated wiring notes — 2026-10-17

## Concrete stubs added
- `production/pipeline/instance_animator_wrapper.py` — placeholder for InstanceAnimator
- `production/pipeline/ldf_vfi_wrapper.py` — placeholder for LDF-VFI (stage-3 alternative)

## Kaggle status (from repo)
- ToonCrafter notebook: `production/kaggle/tooncrafter/cape_jones_tooncrafter_kaggle.ipynb`
  - FP16 patch can fail if upstream inference.py changes (assert on anchor)
  - Relies on dataset cache `/kaggle/input/tooncrafter-weights-fp16/` or HF download
  - Bulletproof saver cell exists; Quick Save is insufficient
- one-to-all: `dataset_sources` now set to `marsfmmg/cape-jones-viggle-inputs`
  - Raw-inference path still the ERROR cause; needs ComfyUI 1.3B rebuild
- Weight-seeding kernels still have empty `dataset_sources`

See `docs/KAGGLE-FIXES.md` for the exact edits.

## Palette + pupil
- Palette enforcement already in `palette-enforce.py`; ingest queue now accepts `--palette`
- Pupil gag automation in `pupil_gag.py` (shock dots + directional looks)

## Next verified steps
1. Populate `dataset_sources` on the remaining kernel-metadata.json files
2. Make the ToonCrafter FP16 patch non-fatal
3. Re-push the kernels
4. Replace the two wrapper stubs with real calls once the tools are fully pulled
