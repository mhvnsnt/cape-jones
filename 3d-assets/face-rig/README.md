# CJ Face Rig — Telltale-style mouth kit + eye-dart cards + GNM-style parametric layer

Spec: `characters/sheets/06-viseme-phoneme-mouth-matrix.jpg` (mouths),
`05-expression-eye-dart-matrix.jpg` (white eyes default, pupils sometimes-only for emphasis).

## Layer 1 — swap-set mouth kit (unchanged)

A **swap-set** mouth system in the Telltale tradition: 17 discrete mouth meshes, exactly one visible
at a time, driven by an int property — no blendshape interpolation, so every viseme stays pixel-true
to the sheet's hard-vector look.

- `cj_mouth_kit.blend` — built by `build_mouthkit.py` (procedural, Blender 4.0.2 headless).
  - `CJ_FaceSocket` — parent this to the head bone in the shot/rig file; position on the face.
    (Ships at a plausible default measured from the rig's jaw bone; the FACE lane owns final fitting —
    this kit never edits the rig file.)
  - `CJ_MouthDriver` — int `mouth_index` 0..16; visibility drivers show one mouth.
  - `CJ_EyeDriver` — legacy int `eye_index` (kept for back-compat; the parametric
    layer supersedes it — see Layer 2).
- `rhubarb_map.json` — Rhubarb A–H+X shapes → mouth indices (shape definitions verbatim from Rhubarb's
  own README; Hanna-Barbera 6-shape base + optional G/H/X) + Papagayo Preston-Blair names → indices.
- `rhubarb_to_blender.py` — keys `mouth_index` from Rhubarb TSV/JSON or Papagayo .dat with CONSTANT
  interpolation (hard cuts).
- `tools/rhubarb/` — Rhubarb Lip Sync 1.14.0 Linux binary (MIT, LICENSE-Rhubarb.md, SHA256.txt).
  Extract the zip next to the script; run `./rhubarb -o cues.tsv -d transcript.txt dialogue.wav`.

## Layer 2 — GNM-style parametric face (NEW)

`cj_parametric_face.py` builds `cj_face_parametric.blend` on top of the kit:
a **grouped expression parameter vector** (`CJ_FaceParams`, 20 float props) in the
same architecture as Google's GNM-Head (studied, not copied — see
`docs/research/GNM-HEAD.md` and `tools/pulled/GNM/`):

- **EYES** (GNM: 100/eye): blink_L/R, wide, squint_L/R, look_x/look_y (eye-darts)
- **BROW**: brow_L/R, brow_squeeze — mask-brow cards (sheet 05: "the mask's dynamic movement";
  GNM itself ships no brow basis, we added one)
- **LOWER FACE** (GNM: 150): jaw_open, smile, frown, grimace, smirk_L/R, mouth_shift_x —
  driven as *transforms* on the swap-set mouth holders (the mouths themselves stay hard-cut)
- **TONGUE** (GNM: 32): tongue_out, tongue_side — drives a shape-keyed tongue card
- **IRIS** (GNM: 1): pupil_toggle — 0 = white eyes (canon default), 1 = pupils (emphasis beats)

`cj_face_presets.py` is the semantic-sampler equivalent: 21 named presets
(the 8 expression-matrix entries = the sign-off checklist, the 4 eye-darts,
plus comedic-range extras) mapping to param vectors, with `blend_presets()`
mirroring GNM's `blend_expressions()`.

`cj_face_ui.py` — installable Blender add-on: N-panel "CJ Face" with grouped
sliders + preset buttons (our own code; the free "GNM Head Importer" add-on was
studied but not vendored — no stated license).

```bash
cd 3d-assets/face-rig
xvfb-run -a env -u PYTHONPATH ~/workspace/tools/blender/blender-4.0.2-linux-x64/blender \
  -b --python cj_parametric_face.py        # builds cj_face_parametric.blend
xvfb-run -a env -u PYTHONPATH ~/workspace/tools/blender/blender-4.0.2-linux-x64/blender \
  -b --python proof_parametric.py         # writes proof/parametric_face_proof.png
```

**Headless gotchas found while building (Blender 4.0.2):**
- Setting ID custom props via Python does NOT re-evaluate drivers — call
  `obj.update_tag()` on the driver-target objects, then `view_layer.update()`.
- `hide_render` on a parent does NOT hide children in renders — visibility
  drivers must be placed on every descendant, not just the holder.
- `obj.copy()` carries BASE (pre-driver) values — freeze bakes from
  `obj.evaluated_get(depsgraph)` (visibility, transforms, shape-key values),
  never from the raw copy.

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
