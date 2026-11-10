# RIFE Interpolation on Kaggle GPU — Cape Jones

**Status:** Notebook built and tested. Replaces `ffmpeg minterpolate` for all episode
interpolation work. GPU minutes vs CPU hours.

## What it is

[RIFE](https://github.com/megvii-research/ECCV2022-RIFE) (Real-Time Intermediate Flow
Estimation, MIT licensed) — AI frame interpolation. Takes choppy low-fps footage
(Viggle AI outputs, expression montages, any 12fps source) and generates smooth
in-between frames on GPU.

- Notebook: `../cape_jones_rife_kaggle.ipynb` (7 cells, self-contained)
- Model/code: `model/` + `train_log/flownet.pkl` in this directory (RIFE v4)
- Test input: `input-12fps.mp4` (217 frames @ 12fps, 1080x1920, SHA-256 verified in-notebook)

The notebook downloads the RIFE package + input from this repo's `kaggle-rife` branch,
extracts frames, runs inference on CUDA (`exp=1`: one middle frame per pair, 12fps → 24fps),
and assembles the output MP4.

## How to run

1. **Push the notebook** to Kaggle:
   ```
   kaggle kernels push -p <notebook-dir>
   ```
2. **Attach datasets via the BROWSER — do NOT rely on `kaggle kernels push`.**
   `kaggle kernels push` does NOT propagate `dataset_sources`. This is a known,
   repeatedly-hit bug. After pushing, open the notebook on kaggle.com, go to the
   **Input** tab (right sidebar), click **Add Input**, and attach any needed datasets
   manually. Verify they appear under Input before running.
3. **Save & Run All** (never Quick Save — Quick Save captures 0 output files).
4. Download outputs from the Output tab.

## Known bug: dataset_sources not propagated (2026-10-16)

`kaggle kernels push` silently drops `dataset_sources` from kernel metadata.
Workaround is browser-attach + verify via Input tab, every time. Do not "fix" this
by re-pushing — it will not work. Documented here so nobody burns GPU hours on it again.

## When to use vs ffmpeg minterpolate

| | RIFE (this notebook) | ffmpeg minterpolate |
|---|---|---|
| Quality | Best free option, handles fast motion | Weakest on fast motion, smears |
| Speed | Minutes on T4 GPU | Hours on CPU for a full episode |
| Use when | Episode footage, Viggle clips, expressions | Quick preview only, or no GPU available |

**Rule: episode interpolation goes through RIFE. `minterpolate` is fallback only.**

## Wiring into the episode pipeline

1. Export the choppy section (e.g. expressions montage) as MP4.
2. Upload as Kaggle dataset `marsfmmg/<name>` (or attach via browser per above).
3. Run this notebook with the input swapped in cell 3.
4. Pull the interpolated MP4 back down, continue in the post pipeline
   (`production/pipeline/FLIPACLIP-POST-PIPELINE.md`).

## License

RIFE: MIT (megvii-research). Notebook + docs: same as repo.
