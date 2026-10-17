# tools/weights — weight-painting / skinning pipelines (bake-off home)

Everything the weight bake-off lane (2026-10-17) tested, pulled in, and wired up.
Full report: `docs/research/WEIGHT-BAKEOFF-2026.md`.

## Contents

| Path | What | License | Status |
|---|---|---|---|
| `cj_bakeoff/bakeoff.py` | Bake-off driver: canonical CJ-TEST skeleton, 7 weight entries (W1–W7), 7-pose test suite, Cycles proof renders | GPL-3.0 (repo) | Ran 2026-10-17 — see research doc for scores |
| `surface-heat-diffuse/` | Surface Heat Diffuse Skinning v3.4.2 — open-source "never fails" alternative to Blender Bone Heat | MIT | Pulled 2026-10-17; Linux solver compiled from `src/` via `build_linux.sh` |

## Entries tested (all on the same CJ-TEST skeleton, same 7 poses)

- **W1** Blender Bone Heat (`ARMATURE_AUTO`) — built-in baseline
- **W2** Blender Envelope weights (`ARMATURE_ENVELOPE`) — built-in baseline
- **W3** Surface Heat Diffuse Skinning (meshonline, MIT) — open-source pull
- **W4** `brutalfist-fix/tools/animation/auto_rig_humanoid.py` end-to-end — our pipeline
- **W5** W1 + Preserve Volume (dual-quaternion) + Corrective Smooth — bannon-video-pipe stack
- **W6** W1 + twist bones (Copy Rotation Y @ 0.5, weights redistributed) — bannon-video-pipe technique
- **W7** BlenRig-6-style mesh-deform cage skinning — technique entry (full guide-fitted
  BlenRig bind belongs to the rig lane; this is its core skinning method)

## Running the bake-off

```bash
# headless, Blender 4.0.2 (xvfb required — see repo AGENTS.md / TOOLS.md notes)
xvfb-run -a env -u PYTHONPATH ~/workspace/tools/blender/blender-4.0.2-linux-x64/blender \
  -b --python tools/weights/cj_bakeoff/bakeoff.py -- --entry W1 --poses all

# poses only, from an existing weight blend (no recompute):
xvfb-run -a env -u PYTHONPATH .../blender -b --python tools/weights/cj_bakeoff/bakeoff.py \
  -- --entry W5 --poses P3,P4 --from-blend ~/workspace/weight-bakeoff-scratch/blends/W1.blend
```

Weights are skeleton-bound: every set here pairs with the **CJ-TEST skeleton**
(`cj_bakeoff/bakeoff.py::BONES`, 20 bones, character faces +X, native 0.925 m —
DO NOT RESCALE). To apply the winning *technique* to the BlenRig 6 rig, see
`3d-assets/cape-jones-rig/WEIGHT-BAKEOFF-RESULT.md` (handoff note for the rig lane).

## Evaluated, not pulled (license / platform reasons)

- **Voxel Heat Diffuse Skinning** (meshonline) — paid, Blender Market. Skipped per no-paid law.
  Its free sibling Surface Heat Diffuse (above) is pulled instead.
- **Adaptive Auto Skinning** (Jessy Leite, 80.9% artist-match benchmark, Sept 2026) —
  paid (Superhive). Skipped per no-paid law. Revisit if a free tier appears.
- **DV Skin Tools** (GPL-3.0, free) — weight-*painting* workflow tools, not auto-skinning;
  requires Blender 4.2+ (we run 4.0.2). Documented for the manual-cleanup lane.
- **Easy Weight** (Blender Studio, extensions platform) — weight-paint QoL, not a weight
  generator. Documented for the manual-cleanup lane.
