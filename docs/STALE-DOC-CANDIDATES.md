# Stale Doc Candidates — 2026-10-17

The original audit mentioned "a stale doc pointing to a folder that doesn't exist."
I could not find an exact match via code search, but these are the strongest candidates from the live repo:

## 1. RESEARCH-INDEX.md references
- `docs/research/RESEARCH-INDEX.md` lists paths such as:
  - `MP3s in cape-jones-build/` (SOUNDTRACKS.md row)
  - `opencode/ source in production/devtools/` (docs/cloud/OPENCODE.md row)
  - Various `~/workspace/tools/...` paths in EXPANSION-4.md that were later moved into the repo

## 2. EXPANSION-4.md local paths
- `docs/research/EXPANSION-4.md` still lists many tools under `~/workspace/tools/...`
  (layerinbetween, ltx-2, omnicolor, everanimate, open-toon, etc.).
  InstanceAnimator and LDF-VFI were moved into `production/tools/` via PR #33,
  but the doc still shows the old workspace paths.

## 3. Possible missing folders
- `production/devtools/` — referenced in RESEARCH-INDEX for OpenCode
- `cape-jones-build/` — referenced for soundtrack MP3s

## Recommended fix
Update `docs/research/EXPANSION-4.md` and `docs/research/RESEARCH-INDEX.md` so that:
- InstanceAnimator → `production/tools/InstanceAnimator/`
- LDF-VFI → `production/tools/LDF-VFI/`
- Any other tools that landed in the repo get their new paths
- Remove or mark as external any `~/workspace/tools/` paths that were never moved

## Wrappers updated
Both stubs now call the real entry points when the tools and weights are present:
- `instance_animator_wrapper.py` → `production/tools/InstanceAnimator/inference/predict_video_decouple.py`
- `ldf_vfi_wrapper.py` → `production/tools/LDF-VFI/generate.py` (mirrors quick_start/generate.sh)
