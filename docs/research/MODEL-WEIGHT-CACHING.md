# Model Weight Caching — Kaggle Datasets as Weight Stores

**Problem:** Every ToonCrafter run re-downloaded 10.5GB from HuggingFace. Every
Viggle run re-downloaded 25GB. Wasted time on every single run.

**Solution:** Kaggle Datasets as persistent weight caches. Download once via a
seeding kernel, attach the dataset to all future kernels. Zero local disk.

## Datasets

| Dataset | Contents | Size | Source |
|---------|----------|------|--------|
| `marsfmmg/tooncrafter-weights` | `model.ckpt` | 10.5 GB | `Doubiiu/ToonCrafter` on HF |
| `marsfmmg/viggle-animate-weights` | `diffusion_models/`, `loras/`, `text_cond/`, `vae/` | 25.2 GB | `drbaph/Viggle-Animate-ComfyUI` + `Kijai/MiniMax-H3-experimental` on HF |

All private. All versioned. Mount at `/kaggle/input/<slug>/` in any kernel
that lists them in `dataset_sources`.

## How it works

```
┌─────────────┐     ┌──────────────┐     ┌──────────────────┐
│ HuggingFace │────▶│ Seeding      │────▶│ Kaggle Dataset   │
│ (source)    │     │ Kernel (CPU) │     │ (persistent)     │
└─────────────┘     └──────────────┘     └────────┬─────────┘
                                                 │ attach
                                        ┌────────▼─────────┐
                                        │ Future kernels   │
                                        │ (no re-download) │
                                        └──────────────────┘
```

**Notebook logic (all generators):** check `/kaggle/input/<dataset>/` first →
copy if present and size matches → fall back to HuggingFace download.

## Seeding

Generators in `production/kaggle/weight-seeding/`:

| Generator | Output | What it does |
|-----------|--------|--------------|
| `gen_seed_tooncrafter.py` | `seed-output-tooncrafter/` | Downloads model.ckpt (10.5GB), publishes to dataset |
| `gen_seed_viggle.py` | `seed-output-viggle-small/` | Downloads LoRA+text_cond+VAE (4.2GB), publishes v1 |
| `gen_seed_viggle.py` | `seed-output-viggle-diffusion/` | Downloads diffusion model (21GB) via HTTP Range halves, publishes v2 |

**Run order:** tooncrafter → viggle-small → viggle-diffusion (diffusion
attaches v1 and publishes the combined v2).

```bash
cd production/kaggle/weight-seeding
python3 gen_seed_tooncrafter.py && cd seed-output-tooncrafter && kaggle kernels push -p .
# ... wait for completion, then:
cd ../seed-output-viggle-small && kaggle kernels push -p .
# ... wait for completion, then:
cd ../seed-output-viggle-diffusion && kaggle kernels push -p .
```

All seeding kernels are CPU-only (`enable_gpu: false`) — they don't consume
GPU quota.

## The 21GB problem

Kaggle kernels have 20GB disk in `/kaggle/working`. The Viggle diffusion
model is 21GB — it doesn't fit. Solution: HTTP Range requests download it in
two ~10.5GB halves, which are reassembled inside the kernel before publishing.
See `gen_seed_viggle.py` (`dl_range` function).

## Adding a new model

1. Get the exact byte size: `curl -s -H "Range: bytes=0-0" <url> -D - -o /dev/null | grep -i x-linked-size`
2. If total < 18GB: single seeding kernel (download → verify size → publish)
3. If total > 18GB: split via Range requests (see diffusion example)
4. Add the dataset slug to the notebook generator's `dataset_sources`
5. Add cache-first logic to the download cell (copy from existing generators)
6. Document here: dataset slug, contents, size, source

## Size limits (verified 2026-10-16)

- **Per dataset:** 100GB (public), ~100GB private quota per account
- **Per file via API:** ~2GB (use `kagglehub`, not raw `kaggle` CLI — the CLI has a `NoneType` join bug in v2.2.4)
- **Kernel disk:** 20GB (`/kaggle/working`)
- **Our usage:** 10.5GB + 25.2GB = 35.7GB of ~100GB private quota

## Versioning

When upstream weights change:
1. Update the expected size in the generator
2. Re-run the seeding kernel → new dataset version
3. Notebooks automatically get the new version (Kaggle mounts latest by default)
4. Old versions remain available for rollback

## License notes

- ToonCrafter weights: Apache-2.0 (matches upstream)
- Viggle-Animate weights: Apache-2.0 (upstream is open-source; MiniMax-H3 base)
- Datasets are private to `marsfmmg` — no redistribution concerns
