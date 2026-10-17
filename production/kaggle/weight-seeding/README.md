# Weight Seeding — Kaggle Kernel Generators

Generators that build CPU-only Kaggle kernels for downloading model weights
from HuggingFace and publishing them as Kaggle Datasets. Zero local disk.

## Generators

| Script | Kernel output | Dataset | Size |
|--------|---------------|---------|------|
| `gen_seed_tooncrafter.py` | `seed-output-tooncrafter/` | `marsfmmg/tooncrafter-weights` | 10.5 GB |
| `gen_seed_viggle.py` | `seed-output-viggle-small/` | `marsfmmg/viggle-animate-weights` (v1) | 4.2 GB |
| `gen_seed_viggle.py` | `seed-output-viggle-diffusion/` | `marsfmmg/viggle-animate-weights` (v2) | +21 GB |

## Usage

```bash
# 1. ToonCrafter (independent)
python3 gen_seed_tooncrafter.py
cd seed-output-tooncrafter && kaggle kernels push -p . && cd ..

# 2. Viggle small files (independent)
python3 gen_seed_viggle.py
cd seed-output-viggle-small && kaggle kernels push -p . && cd ..

# 3. Viggle diffusion (AFTER small completes — attaches v1)
cd seed-output-viggle-diffusion && kaggle kernels push -p . && cd ..
```

All kernels are CPU-only. They don't consume GPU quota.

## How seeding works

Each kernel:
1. Downloads weights from HuggingFace via `wget`/`curl`
2. Verifies exact byte size (sizes in `X-Linked-Size` header, verified 2026-10-16)
3. Writes `dataset-metadata.json` with the target dataset ID
4. Runs `kaggle datasets version -p /kaggle/working/seed -m "..."`
   (kernel is pre-authenticated as the notebook owner)

## The 21GB diffusion model

Exceeds the 20GB kernel disk. Downloaded in two ~10.5GB halves via HTTP
Range requests, reassembled with `cat`-equivalent Python, verified, then
published. See `dl_range()` in `gen_seed_viggle.py`.

## After seeding

Update the main notebook generators to check `/kaggle/input/<slug>/` first.
See:
- `production/kaggle/tooncrafter/gen_notebook.py` (ToonCrafter cache logic)
- `production/ai-body-replace/gen_notebook.py` (Viggle cache logic)

Full pattern documented in `docs/research/MODEL-WEIGHT-CACHING.md`.
