# CJ Face Rig — Telltale-style mouth kit + eye-dart cards

Spec: `characters/sheets/06-viseme-phoneme-mouth-matrix.jpg` (mouths),
`05-expression-eye-dart-matrix.jpg` (white eyes default, pupils sometimes-only for emphasis).

## What this is

A **swap-set** mouth system in the Telltale tradition: 17 discrete mouth meshes, exactly one visible
at a time, driven by an int property — no blendshape interpolation, so every viseme stays pixel-true
to the sheet's hard-vector look.

- `cj_mouth_kit.blend` — built by `build_mouthkit.py` (procedural, Blender 4.0.2 headless).
  - `CJ_FaceSocket` — parent this to the head bone in the shot/rig file; position on the face.
    (Ships at a plausible default measured from the rig's jaw bone; the FACE lane owns final fitting —
    this kit never edits the rig file.)
  - `CJ_MouthDriver` — int `mouth_index` 0..16; visibility drivers show one mouth.
  - `CJ_EyeDriver` — int `eye_index`: 0 = white only (default), 1 = white + pupils (emphasis beats),
    2 = closed lids.
- `rhubarb_map.json` — Rhubarb A–H+X shapes → mouth indices (shape definitions verbatim from Rhubarb's
  own README; Hanna-Barbera 6-shape base + optional G/H/X) + Papagayo Preston-Blair names → indices.
- `rhubarb_to_blender.py` — keys `mouth_index` from Rhubarb TSV/JSON or Papagayo .dat with CONSTANT
  interpolation (hard cuts).
- `tools/rhubarb/` — Rhubarb Lip Sync 1.14.0 Linux binary (MIT, LICENSE-Rhubarb.md, SHA256.txt).
  Extract the zip next to the script; run `./rhubarb -o cues.tsv -d transcript.txt dialogue.wav`.

## Rebuild

```bash
cd 3d-assets/face-rig
xvfb-run -a env -u PYTHONPATH ~/workspace/tools/blender/blender-4.0.2-linux-x64/blender \
  -b --python build_mouthkit.py -- ./cj_mouth_kit.blend
# proof grid only:
xvfb-run -a env -u PYTHONPATH ~/workspace/tools/blender/blender-4.0.2-linux-x64/blender \
  -b --python proof_mouthkit.py   # writes proof/mouthkit_proof.png
```

## Mouth index table

| idx | mouth | covers |
|---|---|---|
| 0 | resting | X (idle), silence |
| 1 | A_AH | D (wide open AA) |
| 2 | E_I | C (open EH/AE) |
| 3 | O_OO | E (slightly rounded AO/ER) |
| 4 | U | small rounded |
| 5 | U_wide | big open |
| 6 | M_B_P | A (closed P/B/M) |
| 7 | E_I_smile | big grin |
| 8 | E_O | E/O |
| 9 | F | G (upper teeth on lower lip, F/V) |
| 10 | C_D_G_K_N_R_S_T_Y | near-closed consonants |
| 11 | teeth_clench | B (clenched-teeth consonants, EE) |
| 12 | L_Th | H (long L, tongue) |
| 13 | W_Q | F (puckered UW/OW/W) |
| 14 | Sh_Ch | Sh/Ch |
| 15 | intense | clenched grimace |
| 16 | gasp | surprise |

## Licenses

- Mouth/eye geometry: ours (built from our sheets). No third-party art.
- Rhubarb Lip Sync 1.14.0: **MIT** (Daniel S. Wolf) — vendored with license text.
- Papagayo-NG: **GPL** — external manual tool only, never vendored or linked.
