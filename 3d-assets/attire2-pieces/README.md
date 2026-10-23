# Attire-2 Pieces (STAGED — not built into an attire)

Canon (owner 2026-10-17 ~14:47 CDT): Cyborg X = Cape Jones. Future Attire 2 =
female-universe reskin of Cyborg X (Alisa's Tekken model): Space Ghost style
WITHOUT head ears, WHITE eyes, Batgirl-style pieces — from OUR pieces, NOT any
actual 3D Cape Ghost model.

## Contents

- `cj_attire2_pieces.blend` — 15 staged piece objects in collection
  `CJ_Attire2_Pieces` (built by `build_attire2_pieces.py`, Blender 4.0.2 headless)
- `proof/attire2_pieces_proof.png` — turnaround, viewed with own eyes
- `PULL-LOG.md` — every source checked, what was taken vs excluded and why

## Rebuild

```bash
cd 3d-assets/attire2-pieces
xvfb-run -a env -u PYTHONPATH ~/workspace/tools/blender/blender-4.0.2-linux-x64/blender \
  -b --python build_attire2_pieces.py -- ./cj_attire2_pieces.blend
```

## Notes for the attire lane

Pieces are unfitted blanks at approximate CJ head scale. Fit, scale, and paint
onto Alisa's model; white eyes from `3d-assets/face-rig/` sit behind the domino
mask. Colors are placeholders — paint per the future Attire-2 sheet.
