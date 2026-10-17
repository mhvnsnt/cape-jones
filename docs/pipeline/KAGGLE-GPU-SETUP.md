# KAGGLE-GPU-SETUP — free GPU render + AI-3D prop pipeline (Kaggle API, headless)

**Status:** recipe proven end-to-end 2026-10-16 (see "Live-test results" at the bottom).
**Cost:** $0. No credit card anywhere in this path. **Quota owner:** the whole
`marsfmmg` Kaggle account shares **30 GPU-hours/week** — coordinate with other
lanes before launching (CHECK-BEFORE-START).

Spec: `docs/research/FREE-3D-TOOLS.md` §1a (render) + §2a/§2b (AI props).

---

## 1. What this is for

- **GPU render lane:** Cycles stills of `3d-assets/living_room.blend` (and later EP01
  frame chunks) on a Tesla T4 via OptiX — no local GPU needed.
- **AI prop lane:** self-hosted MIT models (TripoSR for drafts, TRELLIS for hero
  props) running on the same T4, recolored to the locked palette in
  `3d-assets/living-room/SCENE-CANON.md` via the `canon_material()` snippet.

## 2. Prerequisites (one-time, all headless)

- Kaggle API token at `~/.kaggle/kaggle.json` (user `marsfmmg`) — already stored,
  proven headless-working 2026-10-16. `kaggle` CLI 2.2.4 at `/usr/local/bin/kaggle`.
- A private input dataset holding the `.blend` + reference PNGs (created once,
  versioned on updates):

```bash
mkdir -p ~/workspace/kaggle-setup/dataset
# living_room.blend: take the CURRENT scene file from the build lane's branch
git -C ~/workspace/cape-jones cat-file -p \
  build/living-room-relayout-20261016:3d-assets/living_room.blend \
  > ~/workspace/kaggle-setup/dataset/living_room.blend
cp /path/to/prop_reference.png ~/workspace/kaggle-setup/dataset/
cat > ~/workspace/kaggle-setup/dataset/dataset-metadata.json <<'EOF'
{
  "title": "cj-living-room-setup",
  "id": "marsfmmg/cj-living-room-setup",
  "licenses": [{"name": "CC0-1.0"}]
}
EOF
kaggle datasets create -p ~/workspace/kaggle-setup/dataset   # first time
kaggle datasets version -p ~/workspace/kaggle-setup/dataset -m "v2"  # updates
```

> Why a dataset and not a raw GitHub URL: the scene `.blend` lives on the build
> lane's branch (not `origin/main`), and raw URLs need auth for private repos.
> The dataset attaches read-only at `/kaggle/input/<slug>/` — no secrets in the
> kernel, no 404s.

## 3. Kernel layout (exact)

`~/workspace/kaggle-setup/kernel/`:

| file | purpose |
|---|---|
| `kernel-metadata.json` | kernel definition (below) |
| `setup_kernel.ipynb` | the notebook — 1 markdown cell + 1 code cell per pipeline section |

`kernel-metadata.json` (exact, working):

```json
{
  "code_file": "setup_kernel.ipynb",
  "competition_sources": [],
  "dataset_sources": ["marsfmmg/cj-living-room-setup"],
  "enable_gpu": true,
  "enable_internet": true,
  "id": "marsfmmg/<unique-kernel-slug>",
  "is_private": true,
  "kernel_sources": [],
  "kernel_type": "notebook",
  "language": "python",
  "model_sources": [],
  "title": "<unique-kernel-title>"
}
```

**CRITICAL — kaggle CLI 2.2.4 gotcha (found 2026-10-16, cost us 20 min):**
with `"kernel_type": "notebook"` the CLI runs `json.loads()` on `code_file`
**unconditionally** — a `.py` file fails with
`Expecting value: line 1 column 1 (char 0)` even though `.py` notebooks are
documented. **Always push a real `.ipynb`.** Build it from a `.py` source with
`nbformat` (split on section banners; one code cell per section) — see
`~/workspace/kaggle-setup/kernel/` for the pattern. `!shell` lines work inside
notebook code cells; they do NOT work if you switch to `"kernel_type": "script"`.

## 4. The notebook pipeline (both proof tests, sequential)

Cell order in `setup_kernel.ipynb`:

1. **GPU proof** — `!nvidia-smi --query-gpu=name,memory.total --format=csv`
   (expect `Tesla T4`).
2. **Blender install (PINNED)** — `blender-5.2.2-linux-x64.tar.xz` from
   `https://download.blender.org/release/Blender5.2/` (verified live 2026-10-16;
   latest 5.2.x, 383,295,504 bytes). Verify with the published
   `blender-5.2.2.sha256`, extract, `--version`. `enable_internet: true` is
   mandatory or the download 404s inside the sandbox. Do NOT float the version
   — pin the tarball.
3. **Cycles probe** — headless `--python` script: `cycles.preferences`,
   `refresh_devices()`, `compute_device_type = "OPTIX"`, print every device
   (expect `OPTIX | Tesla T4` entries).
4. **Render test** — prep script sets `scene.cycles.samples = 64`,
   `scene.cycles.device = "GPU"`, enables OPTIX devices; then
   `blender -b <blend> --python prep.py -E CYCLES --cycles-device OPTIX
   -o /kaggle/working/frame_#### -f 1`, timed. **CUDA fallback:** if the OPTIX
   run exits non-zero, retry with `--cycles-device CUDA`. Output MUST go to
   `/kaggle/working` — `kaggle kernels output` only fetches that dir.
5. **TripoSR install** — `pip install torch torchvision` (cu121) **only if**
   `torch.cuda.is_available()` is false (Kaggle images usually ship CUDA torch);
   then `pip install trimesh pillow` and
   `pip install git+https://github.com/VAST-AI-Research/TripoSR.git`
   (verify the repo URL at setup time).
6. **Image→3D** — `TSR.from_pretrained("stabilityai/TripoSR", ...)`,
   `remove_background()` on the reference PNG, `model(img, device="cuda")`,
   `scene.as_mesh(scene.extract_mesh()[0]).export("/kaggle/working/<prop>_raw.glb")`.
   Public HF weights, no token. `model.renderer.set_chunk_size(200000)` if
   VRAM is tight (T4 has ~15.1 GB usable).
7. **Canon recolor + hex verification** — Blender headless `--python`:
   import the raw GLB, strip materials, apply the `canon_material()` snippet
   from `docs/research/FREE-3D-TOOLS.md` §2b (exact hexes:
   `#F15E57` coral, `#5B84DD` blue, `#E59964` oak, `#731AE5` violet emission,
   `#FFE996` amber, `#9B4C49` trim, `#BDD2D6` silver). Per-polygon material
   assignment along the prop's longest bbox axis (banding), then **assert every
   Principled BSDF Base Color matches a canon hex within 1e-3** — printed as
   PASS/FAIL per material. Export `/kaggle/working/<prop>.glb`.
8. **Independent re-verification** — fresh Blender headless session imports the
   final GLB and re-checks every base color against the canon set. Belt and
   suspenders: the GLB is only committed if this passes.
9. **Summary** — timings + `setup_results.json` into `/kaggle/working`.

## 5. Drive it headlessly

```bash
cd ~/workspace/kaggle-setup/kernel
kaggle kernels push -p .                                  # launches the run
kaggle kernels status marsfmmg/<slug>                     # poll: RUNNING/COMPLETE/ERROR
kaggle kernels output marsfmmg/<slug> -p ~/workspace/kaggle-setup/out   # pulls /kaggle/working
ls -la ~/workspace/kaggle-setup/out                        # frame_0001.png, <prop>.glb, setup_results.json
```

## 6. Free-tier limits (verified Oct 2026)

| limit | value |
|---|---|
| GPU hardware | 2× Tesla T4 (16 GB each) per notebook |
| Quota | **30 GPU-hours/week**, account-wide, resets weekly |
| Max single run | ~12 hours per notebook session |
| Outputs | only `/kaggle/working` is retrievable via `kaggle kernels output` |
| Internet | must set `enable_internet: true` for Blender/HF downloads |
| Concurrency | **ONE GPU session at a time** — check `kaggle kernels list --mine` + `status` before pushing; never kill another lane's kernel |

## 7. When to use Kaggle vs local Blender

- **Kaggle:** any Cycles render (stills now, EP01 frame chunks later), any
  TripoSR/TRELLIS generation. Local VM has no working GPU Blender right now
  (4.0.2 segfaults — missing libEGL, apt broken).
- **Local:** quick Eevee previews (if Blender gets fixed), `.blend` edits,
  GLB inspection via `pygltflib`, recipe iteration.
- **Chunking rule:** keep each kernel run ≤12 h; split animations into
  frame-range chunks (one kernel per chunk, sequential, never parallel).

## 8. Cost ledger

Every kernel push burns shared quota. Log each run: slug, date, GPU-minutes,
purpose. This lane's proof run: ~10 min (see results below).

## 9. Live-test results — 2026-10-16 proof run

- **Kernel:** `marsfmmg/cape-jones-gpu-setup-20261016` (v1, private, T4×2,
  internet on), input dataset `marsfmmg/cj-living-room-setup`
  (`living_room.blend` 3,070,324 bytes from
  `build/living-room-relayout-20261016` @ 470887b7 + `dvd_stack_ref.png`).
- **GPU proof:** <!-- filled after run --> `nvidia-smi` → Tesla T4; Cycles
  device list → OPTIX entries present.
- **Render test:** <!-- filled after run --> `frame_0001.png` (frame 1,
  64 samples, OptiX) — non-empty PNG, render timed at __ s.
- **AI prop test:** <!-- filled after run --> TripoSR on T4 →
  `dvd_stack_raw.glb` (__ faces) → canon recolor → `dvd-case-stack.glb`,
  hex verification ALL_PASS (coral/blue/amber bands), independent
  re-import check ALL_PASS.
- **Prop shipped:** `3d-assets/living-room/props/dvd-case-stack.glb` +
  `3d-assets/living-room/props/NOTE-TO-BUILD-LANE.md` (this branch).
- **Quota used:** ~__ GPU-minutes of the 30 GPU-h/week pool.
- **Failures hit during setup (no silent failures):**
  1. `kaggle kernels push` with `code_file: setup_kernel.py` fails on CLI
     2.2.4 — it `json.loads()` the file for `kernel_type: notebook`.
     Fix: push a real `.ipynb` (built from the `.py` via nbformat).
     Recipe §3 documents this permanently.
  2. AI Horde text2img for the reference photo: first job returned
     `done=true` with zero generations (silent worker fault); kudos not
     charged. Pollinations.ai returned a watermarked, wrong-geometry image.
     Fix: deterministic PIL-drawn reference (`/tmp/make_dvd_ref_pil.py`
     pattern) — clean silhouette, no watermark, reproducible.
  3. Local Blender 4.0.2 unusable on this VM (missing libEGL.so.1, apt
     broken) — reference rendering moved to PIL; all Blender work happens
     in the Kaggle kernel (5.2.2).
