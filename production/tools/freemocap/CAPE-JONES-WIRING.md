# FreeMoCap — markerless motion capture from ordinary cameras (wiring doc)

**Upstream:** https://github.com/freemocap/freemocap (2.0.0-alpha.25, active 2026)
**License:** AGPL-3.0 — free, commercial USE as a tool is OK. We vendor only the
core `freemocap` Python package (code). AGPL copyleft applies if we distribute a
*modified* version of FreeMoCap itself (e.g. over a network) — using it as a
tool to produce animation data does not infect our assets. Honest disclosure
per the license-check law.
**Why:** the owner's 3D animation automation directive — "full-stack
industry-standard production-grade stuff, real human motion" (sitting work kept
coming back robotic from hand-posing). FreeMoCap captures real human movement
with 2+ ordinary webcams/phones — no suit, no markers, no studio. Phone-first,
matches his philosophy. Export path goes straight into Blender
(`freemocap/core/blender/export_to_blender.py`).
**Vendored:** `freemocap/` package + `README.md` + `LICENSE` + `CITATION.cff` +
`pyproject.toml` (sparse pull of the essentials; the `freemocap-ui` frontend,
`freemocap-docs` site, and sample data were NOT pulled). No model weights on
disk — pose-estimation models download at runtime via the app's own pipeline
(Kaggle-side download for GPU lanes).

## Install (runtime, NOT vendored)

```bash
pip install freemocap        # PyPI, python 3.9–3.11 (3.11 recommended)
freemocap                    # launches the capture GUI
```

GPU (NVIDIA + CUDA) strongly recommended for the pose-estimation backend; CPU
works but is slow. Needs 2+ synchronized cameras (webcams/phones) and a printed
Charuco calibration board (pattern ships with the app).

## Capture → Blender runbook

1. Calibrate: print the Charuco board, record it from all cameras, run the
   app's calibration step.
2. Record: capture the performance (sitting, walk cycles, gag acting) from all
   cameras simultaneously.
3. Process: the app triangulates 2D pose detections into 3D skeletons
   (full body + hands + face).
4. Export to Blender: `freemocap/core/blender/export_to_blender.py` drives the
   AJC (animate-joints-correctly) Blender addon path — an armature animated by
   the capture appears in Blender, ready to retarget onto the show rigs via the
   existing `production/tools/mocap-sit/` retarget pipeline
   (`production/tools/mocap-retarget/`).
5. Retarget: run the repo's mocap-retarget world-space rotation transfer
   (M_REL, not M_LOCAL — the hard-won fix) onto the 94-bone rig, then the
   contact solver (butt-to-seat, feet-to-floor).

## Cape Jones uses

- **Real sitting motion:** capture actual sit-down/sit-idle/stand-up takes
  instead of hand-posing — the direct answer to "moving like a robot."
- **Gag acting:** record his own acting for Cape Jones bits, retarget to the
  toon rig.
- **Background crowds / fight reference:** multi-person captures for Western
  Heart move reference (study the motion, rebuild clean — steal-like-an-artist).
- Pairs with: `production/tools/mocap-sit/` (retarget pipeline),
  `production/tools/natron/` (comp), `production/tools/rhubarb-lip-sync/`
  (dialogue sync on captured acting).

## Limits

- Alpha software — the README says "It might break! Work in Progress lol."
  Expect jank on occluded limbs; foot placement is reportedly solid.
- Heavy dependency tree (pose estimation, triangulation); install in a venv,
  not system Python. Kaggle GPU lanes should install at session start.
- Accuracy depends on camera count, placement, and lighting — 3+ cameras,
  even lighting, plain background.
