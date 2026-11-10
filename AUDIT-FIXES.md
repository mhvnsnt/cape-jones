# Cape Jones Audit Fixes — 2026-10-17 (both tracks)

## Docs patched
- `docs/research/EXPANSION-4.md` — paths updated. InstanceAnimator and LDF-VFI now point at `production/tools/...`. Wrappers listed. External tools marked as such. FFmpeg filters path corrected to `production/pipeline/`.
- `docs/RESEARCH-INDEX-PATCH-NOTES.md` — exact replacements for the two stale references in RESEARCH-INDEX.md (`cape-jones-build/`, `production/devtools/`).

## Kaggle re-push side
- `production/kaggle/tooncrafter/re_push_tooncrafter.sh` — checklist script for the re-push.
- Still ready: non-fatal FP16 cell (`fp16_patch_cell_v5.py`) and `kernel-metadata.json` with dataset_sources.

## Wrappers (from prior round)
- `instance_animator_wrapper.py` and `ldf_vfi_wrapper.py` call the real entry points.

## Apply
```bash
cp -r /workspace/artifacts/cape-jones-fixes/* /path/to/cape-jones/
# then commit the doc updates and run the re-push checklist
```
