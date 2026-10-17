# Seeding the `marsfmmg/tooncrafter-weights-fp16` Kaggle Dataset

**Why:** The v4 ToonCrafter notebook (`production/kaggle/tooncrafter/`) uses a
cache-first strategy for model weights: it checks
`/kaggle/input/tooncrafter-weights-fp16/model.ckpt` before downloading from
HuggingFace. That dataset must exist and contain the converted FP16 `.ckpt`,
or every run falls back to the 3.2GB HF download.

**Verified facts (2026-10-16, measured — supersede any 2.5GB estimates):**
- Source file: `tooncrafter_512_interp-pruned-fp16.safetensors`
- Source URL: `https://huggingface.co/Kijai/DynamiCrafter_pruned/resolve/main/tooncrafter_512_interp-pruned-fp16.safetensors`
- Source size: **3,175,466,358 bytes (3.18 GB)**
- Converted `.ckpt` must satisfy the notebook's guard: **2.8–3.8 GB**
- The official ToonCrafter README links `tooncrafter_512_interp-fp16.safetensors`
  (underscore) — **that link is stale and 404s**. Use the hyphenated name above.
- Kaggle mount path: `/kaggle/input/tooncrafter-weights-fp16/model.ckpt`
  (file must be named exactly `model.ckpt` at the dataset root)

## Method A — kaggle CLI (what seeded it on 2026-10-16)

```bash
# 1. Download (3.18 GB) — verify byte count
wget https://huggingface.co/Kijai/DynamiCrafter_pruned/resolve/main/tooncrafter_512_interp-pruned-fp16.safetensors \
  -O tooncrafter_512_interp-pruned-fp16.safetensors
[ $(stat -c%s tooncrafter_512_interp-pruned-fp16.safetensors) -eq 3175466358 ] \
  && echo "SIZE OK" || echo "SIZE MISMATCH"

# 2. Convert safetensors -> .ckpt (needs torch + safetensors)
python3 production/kaggle/tooncrafter/convert_safetensors_to_ckpt.py \
  --input tooncrafter_512_interp-pruned-fp16.safetensors \
  --output model.ckpt
# sanity: 2.8GB < model.ckpt < 3.8GB

# 3. Stage for upload (model.ckpt at dataset root)
mkdir -p /tmp/tc-fp16-seed && mv model.ckpt /tmp/tc-fp16-seed/
cp production/kaggle/tooncrafter/fp16-dataset-metadata.json \
   /tmp/tc-fp16-seed/dataset-metadata.json

# 4. Create the dataset (private; attachable to the owner's kernels)
kaggle datasets create -p /tmp/tc-fp16-seed

# 5. Verify
kaggle datasets list --user marsfmmg | grep tooncrafter-weights-fp16
```

The `id` field in `fp16-dataset-metadata.json` must read
`marsfmmg/tooncrafter-weights-fp16`.

## Method B — Kaggle CPU kernel (no local disk needed)

If local disk is tight, do the whole thing inside a Kaggle notebook
(CPU-only kernel is fine — conversion is just a format rewrite):

1. New notebook, **Accelerator: None**, Internet ON.
2. Run:
   ```python
   !wget -q --show-progress https://huggingface.co/Kijai/DynamiCrafter_pruned/resolve/main/tooncrafter_512_interp-pruned-fp16.safetensors
   !pip install -q safetensors  # torch is preinstalled on Kaggle
   from safetensors.torch import load_file
   import torch, os
   sd = load_file("tooncrafter_512_interp-pruned-fp16.safetensors", device="cpu")
   torch.save({"state_dict": sd}, "/kaggle/working/model.ckpt")
   sz = os.path.getsize("/kaggle/working/model.ckpt")
   print(f"{sz/1e9:.2f} GB")
   assert 2_800_000_000 < sz < 3_800_000_000, "size out of range"
   ```
3. Publish `/kaggle/working/model.ckpt` as a new dataset named
   `tooncrafter-weights-fp16` (Add data → New Dataset from the output file,
   or the bulletproof `save_outputs.py` checkpoint flow).

## Re-seeding

If the dataset ever needs re-seeding (corrupt file, new pruned release),
repeat either method — `kaggle datasets version -p` (CLI) or a new dataset
version (kernel) replaces the file. The notebook's `_ok()` guard rejects
anything outside 2.8–3.8 GB, so a bad upload fails loudly at runtime instead
of silently OOMing.
