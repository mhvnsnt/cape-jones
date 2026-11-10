# COLAB — Google Colab GPU lane for the Cape Jones living room

**Notebook:** `notebooks/colab/cape_jones_scene_render.ipynb`
**Researched/written:** 2026-10-16. Blender version pinned from the live source
(blender.org/download/lts/), not from training data. Colab limits verified against 2026 sources
(see §4) — Google publishes no hard numbers, so every figure below is labeled.

This lane is the **interactive** GPU path: a human (or a browser lane) opens the notebook and
presses Run-all. For headless, agent-driven batch renders, use the **Kaggle** path instead —
`docs/research/FREE-3D-TOOLS.md` §1a (that doc owns the Kaggle recipe; this doc does not repeat it).

## 1. What the notebook does

Renders `3d-assets/living_room.blend` headless with Cycles on the Colab GPU:

| Cell | Does |
|---|---|
| 1 | `nvidia-smi` — proves a GPU is actually attached (fails fast with a clear message if not) |
| 2 | Installs **Blender 5.2.2 LTS** (pinned tarball `https://download.blender.org/release/Blender5.2/blender-5.2.2-linux-x64.tar.xz`, 383,295,504 bytes — byte-count asserted after download). Current LTS per blender.org, updated 2026-09-15 |
| 3 | Downloads `living_room.blend` from `origin/main` via raw GitHub URL; verifies `BLENDER` magic bytes + nonzero size |
| 4 | Parameters: `FRAME_START/FRAME_END` (default 1–1 smoke test; full shot = 1–360), `SAMPLES` (default 64; final 128–256), `RES_PCT` (default 50 → 480×270), `OUT_DIR` |
| 5 | Writes `render_scene.py` — the guarded render script |
| 6 | Runs headless Blender with the script; Blender's exit code is preserved; full log → `render.log` |
| 7 | Verifies PNGs exist and are nonzero, previews first/last frame inline, zips them, one-click download |

**Canon guard:** the render script sets render params + GPU device **only**. It never touches
materials, colors, lights, or geometry — the locked palette in
`3d-assets/living-room/SCENE-CANON.md` (coral pink `#F15E57`, warm oak `#E59964`, violet LED
`#731AE5`, …) is protected by construction. If a render looks off-canon, the `.blend` on `main`
changed — check `git log -- 3d-assets/living_room.blend`, not this notebook.

**GPU device selection:** tries OptiX → CUDA → CPU fallback. A Colab T4 is Turing (compute 7.5),
OptiX-supported, so the normal path is `GPU via OPTIX`. If Colab ever assigns a runtime without
a usable NVIDIA GPU, the script prints `CPU fallback` and still renders instead of crashing.

## 2. How to run it

1. Open the notebook in Colab. The repo is **private**, so either:
   - upload the `.ipynb` via Colab's **File → Upload notebook**, or
   - open `https://colab.research.google.com/github/mhvnsnt/cape-jones/blob/main/notebooks/colab/cape_jones_scene_render.ipynb`
     (Colab will prompt you to authorize GitHub access for the private repo).
2. **Runtime → Change runtime type → Hardware accelerator: GPU** (pick T4 if offered) → Save.
3. **Runtime → Run all.**
4. When Cell 3 prompts: paste a **fine-grained GitHub PAT** with **Contents: read-only** on
   `mhvnsnt/cape-jones`. (Why: the repo went private 2026-10-16, so the raw
   `raw.githubusercontent.com` URL returns 404 without auth. Cell 3 tries anonymous first, then
   falls back to the token. The token is used for one download and never written to disk by the
   notebook.)
5. Cell 7 shows the rendered frame(s) inline and downloads `renders.zip`.

> **Note for other notebooks:** the private-repo 404 applies to every Colab notebook that pulls
> from this repo (`production/colab/*.ipynb` included) — they need the same token treatment.

## 3. When to use Colab vs Kaggle

| | **Colab** (this lane) | **Kaggle** (`docs/research/FREE-3D-TOOLS.md` §1a) |
|---|---|---|
| Driving | Interactive — a human/browser presses Run-all | Headless — agents drive it via the Kaggle API, no browser |
| GPU | T4 typical, dynamic (see §4) | 2× T4, 30 GPU-hours/week quota |
| Best for | Visual smoke tests, quick look-dev, owner-run renders | Batch/overnight renders, queued pipelines |
| Session cap | ~12 h, idle disconnect ~90 min | ~12 h per notebook session |
| Cost | $0, no card (free tier only — owner law: no spending) | $0, no card |

Use **both** in the same week for maximum free GPU time. Rule of thumb: iterating on the look →
Colab; rendering the thing once the look is locked → Kaggle queue.

## 4. Colab free-tier limits (verified Oct 2026)

Google's own FAQ is candid: free-tier resources are **dynamic and unpublished** — "GPU types vary
over time," limits "fluctuate," and Colab "does not publish these limits." What the 2026 sources
agree on in practice:

- **GPU:** T4 (16 GB VRAM) is the common free assignment, but it is **not guaranteed** — during
  high-demand windows you may get no GPU at all. Premium hardware is heavily restricted for
  non-paying users. (Google Colab FAQ; thundercompute.com Oct 2026 roundup; spheron.network 2026
  comparison; gpuperhour.com 2026 breakdown)
- **Max session:** ~12 hours, then the runtime is recycled regardless of activity.
- **Idle timeout:** ~90 minutes without interaction; free runtimes are interrupted when user
  interaction ceases. **Keep the tab active during long renders; render long shots in chunks.**
- **No background execution, no SSH** on the free tier (those need compute units / paid tiers).
- **Cost:** $0. No credit card is ever entered — paid tiers (Pro/Pro+) exist but are out of scope
  per the owner's no-spending law.

Practical consequences for this notebook: the default smoke test (1 frame @ 64 samples) finishes
in minutes — safe. A full 360-frame shot at 128+ samples should be chunked (e.g. 1–120, 121–240,
241–360 across runs) so an idle disconnect can't waste hours.

## 5. Troubleshooting

- **Cell 1: no GPU** — free-tier GPU assignment is dynamic; wait and retry, or Runtime → Factory
  reset runtime and re-run. Do not pay for a tier (owner law).
- **Cell 2: tarball size mismatch** — truncated download; re-run the cell (it re-downloads).
  If blender.org changes the LTS, update the pinned URL + byte count in Cell 2 (source of truth:
  https://www.blender.org/download/lts/).
- **Cell 3: 404 even with token** — token lacks Contents:read on `cape-jones`, or it expired;
  create a fresh fine-grained PAT.
- **Render falls back to CPU** — Colab assigned a runtime without NVIDIA compute; the render
  still completes (slowly). For a real GPU run, factory-reset the runtime and try again later.
- **`r.check_returncode()` raised in Cell 6** — read `render.log` (last 25 lines are printed
  above the error); the common cause is an OptiX/CUDA hiccup, which the script already falls
  back from — a hard failure means Blender itself crashed.

## 6. Honest status

- Notebook JSON: **valid** (`nbformat.validate`, 9 cells, cell ids present).
- Command chain: **proven locally on CPU** 2026-10-16 — Blender 4.0.2 opened
  `3d-assets/living_room.blend` (Cycles, 480×270, frames 1–360), rendered frame 1 to PNG in
  37.8 s; the PNG was viewed (living room, canon colorway — not a black frame). The notebook's
  own `render_scene.py` was executed locally with env params (frames 1–2, 1 sample): GPU
  detection fell back to CPU cleanly, both PNGs saved, exit 0.
- GPU cells (nvidia-smi, OptiX-on-T4 device selection): **verified by construction** against the
  Blender 5.2 Cycles API and T4/OptiX compatibility — **not yet executed on a live Colab GPU**.
- **Remaining manual step:** one **Runtime → Run all** on a Colab T4 GPU (owner, or a parent
  browser lane — subagents have no live-browser/Colab-execution API). After that run, append its
  result (GPU name, frame time, PNG check) to this section.
