# Compute — free GPU + render queue for Cape Jones

**Problem we solve:** Kaggle cancels kernels, Colab browser automation failed, our VM has no GPU, daemon restarts kill long renders.

**Answer:** every render goes through `cj-render.py` (resume-safe, per-frame checkpointing) targeting local CPU, Flamenco queue, or Kaggle — plus two new free GPU wires (Lightning AI, SheepIt) once the owner completes the two open signups.

## Files

| File | What |
|------|------|
| `cj-render.py` | Resume-safe render CLI. `--target local\|flamenco\|kaggle`. Re-run the same command after any kill — it skips done frames. |
| `kaggle-ops.md` | Kaggle cancellation mitigations + push discipline. Read before every Kaggle push. |
| `lightning-ai-setup.md` | Lightning AI Studio signup + render bootstrap. **Needs owner: sign up + phone verify.** |
| `sheepit-setup.md` | SheepIt signup + headless client + job packaging. **Needs owner: create account.** |
| `flamenco-setup.md` | Blender's own OSS render manager: pull, configure, run manager + workers. |
| `../../docs/research/FREE-COMPUTE-2026.md` | Full 2026 research: rankings, dead ends, the Kaggle mystery. |

## Quick start

```bash
# Stills / tests on the VM (CPU)
python3 production/pipeline/compute/cj-render.py \
  --blend 3d-assets/living-room/scene.blend --frames 1-1 \
  --out renders/stills --target local

# A 1320-frame walkthrough, chunked through Flamenco (survives restarts)
python3 production/pipeline/compute/cj-render.py \
  --blend 3d-assets/living-room/scene.blend --frames 1-1320 \
  --out renders/walkthrough --target flamenco --chunk 60

# Generate a Kaggle kernel payload (then: kaggle kernels push)
python3 production/pipeline/compute/cj-render.py \
  --blend 3d-assets/living-room/scene.blend --frames 1-1320 \
  --out renders/walkthrough --target kaggle --payload /tmp/kg-payload
```

## The law

1. `--out` is **never /tmp**. Persistent dirs only.
2. Every render keeps `frames_done.json`. Every script skips done frames.
3. Long jobs go through `cj-render.py`, never bare `blender -b` in a 3-hour exec.
4. Kaggle pushes follow `kaggle-ops.md` (≥30min apart, one active kernel).
