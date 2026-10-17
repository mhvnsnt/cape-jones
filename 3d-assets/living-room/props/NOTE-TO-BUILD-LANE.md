# NOTE TO BUILD LANE (build/living-room-relayout-20261016)

## What this is

`dvd-case-stack.glb` — a stack of 5 DVD keep cases, AI-generated on a Kaggle T4
with TripoSR (MIT-licensed, self-hosted — clean for global distribution), then
recolored in Blender headless to the locked palette. Proof pipeline documented in
`docs/pipeline/KAGGLE-GPU-SETUP.md`.

## Palette verification (do not re-tint)

Every material base color on this prop was machine-verified inside Blender to be
**exactly** one of the locked canon hexes (tolerance 1e-3), then re-verified on
an independent re-import of the final GLB:

| Band (bottom → top) | Canon hex | Name |
|---|---|---|
| case 1 | `#F15E57` | coral pink |
| case 2 | `#5B84DD` | blue |
| case 3 | `#FFE996` | amber |
| case 4 | `#F15E57` | coral pink |
| case 5 | `#5B84DD` | blue |

Verification: `HEX_VERIFY: ALL_PASS` + `VERIFY_GLB: ALL_PASS` in the kernel log
(`setup_results.json` pulled with the kernel output). If you re-export it, keep
these exact values — "verify in the material panel, not by eye"
(SCENE-CANON.md law).

## Suggested placement (from the 2D reference)

On the **open-shelf TV console**, beside the VCR/DVD player — the 2D ref shows
the stand shelves holding the VCR/DVD player, boxes, and the monster toy; a DVD
case stack belongs on that same shelf. Approx footprint of one case:
135mm × 190mm; stack of 5 ≈ 70mm tall. Scale to sit flush on the shelf surface,
spines facing the camera (front).

## Provenance

- Reference: deterministic PIL-drawn 3/4 view (no watermark, reproducible —
  see recipe doc §9, failure #2 for why AI-generated refs were rejected).
- Generator: TripoSR `stabilityai/TripoSR` on Kaggle T4, MIT license.
- NOT from the build lane's manual modeling — no duplication: the build lane's
  props are CRT TV, console, VCR/DVD, boxes, monster toy, side table, mug,
  doorway/window, posters, lamp. This DVD stack complements the shelf.
