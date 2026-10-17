# NOTE TO BUILD LANE (build/living-room-relayout-20261016)

## Status: PROP PENDING — pipeline proven, live GLB blocked

The `dvd-case-stack.glb` prop (stack of 5 DVD keep cases, TripoSR on Kaggle T4,
MIT-licensed, recolored to the locked palette) is **not yet generated**. The
kernel that generates it was cancelled by an external party mid-run
(2026-10-17 ~01:45 UTC — see `docs/pipeline/KAGGLE-GPU-SETUP.md` §9); re-push
is awaiting parent go-ahead. **Do not wait on this file** — everything else
in the re-layout proceeds without it.

## What IS proven and ready (verbatim from kernel logs)

- Kaggle T4 ×2 via API, headless: `nvidia-smi` → 2× Tesla T4 (15360 MiB).
- Pinned Blender 5.2.2 LTS installs headless in ~27–30 s, sha256-verified,
  all shared libs present.
- Cycles lists `OPTIX | Tesla T4` ×2 (`OPTIX_AVAILABLE: True`).
- Input dataset `marsfmmg/cj-living-room-setup` resolves correctly
  (`/kaggle/input/datasets/marsfmmg/cj-living-room-setup/…`).
- The full recipe (render 1 frame @64 samples → TripoSR image→3D →
  `canon_material()` recolor → exact-hex verification → GLB export) is
  documented end-to-end in `docs/pipeline/KAGGLE-GPU-SETUP.md` and push-ready.

## Planned prop (when the live test completes)

`3d-assets/living-room/props/dvd-case-stack.glb` — 5 DVD keep cases, materials
banded along the stack axis and machine-verified to the exact locked hexes:

| Band (bottom → top) | Canon hex | Name |
|---|---|---|
| case 1 | `#F15E57` | coral pink |
| case 2 | `#5B84DD` | blue |
| case 3 | `#FFE996` | amber |
| case 4 | `#F15E57` | coral pink |
| case 5 | `#5B84DD` | blue |

## Suggested placement (from the 2D reference, for when it lands)

On the **open-shelf TV console**, beside the VCR/DVD player — the 2D ref shows
the stand shelves holding the VCR/DVD player, boxes, and the monster toy; a DVD
case stack belongs on that same shelf. Approx footprint of one case:
135mm × 190mm; stack of 5 ≈ 70mm tall. Scale to sit flush on the shelf surface,
spines facing the camera (front).

## No duplication

The build lane's existing props are: CRT TV, console, VCR/DVD, boxes, monster
toy, side table, mug, doorway/window, posters, lamp. This DVD stack complements
the shelf — it duplicates nothing.
