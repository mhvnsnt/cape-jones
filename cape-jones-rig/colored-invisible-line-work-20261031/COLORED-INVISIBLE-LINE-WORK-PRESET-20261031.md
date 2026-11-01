# COLORED INVISIBLE LINE WORK — CapeGP preset

**Exact name, use everywhere: COLORED INVISIBLE LINE WORK.**
Mars order, 2026-10-31 20:33 CDT, replying to `capegp-preset-contact-20261031.png`:
"that is awesome, really cool, that can be a preset for him for us to see
him like that" — call it colored invisible line work, because we already
have his invisible line work, so this is a different invisible state for him.
Approval of this built preset: **0/1** (Mars called the contact awesome/cool
and named it; the built preset itself is new work). No repo push made here;
landing is a separate step.

## What it is — and what it is not
- **COLORED INVISIBLE LINE WORK** = CapeGP coloured outline-only state.
  Coloured Grease Pencil strokes only, no fills, body invisible except for
  its coloured outlines, on a transparent background (composited onto black
  in the proof views, because coloured outlines on transparent are hard to
  read in a thumbnail — the transparent files are the real outputs).
- **Existing INVISIBLE LINE WORK** = Silhouette Preset Pack Two, TOP ROW:
  L1 faint 1px alpha 70, L2 medium 2px alpha 120, L3 visible 3px alpha 180,
  L-depth line-weight-by-depth, Sobel cross-check. Black-and-white lineart,
  part of his INVISIBILITY POWERS. Do NOT confuse the two: one is B/W
  lineart, the other is coloured GP outlines. Different invisible states,
  different presets, different files.
- **Also not this:** Coloured Shadow (dark purple 52,22,90, own-rig
  silhouette behind him, a separate mechanic), black-silhouette Pack Two
  second row, and any filled/coloured character render. This preset has
  no fills by construction — GP fills / interior linework / colour fills
  are 0/1, NOT run, and are not claimed here.

## The tool, stated plainly
The tool is **CapeGP — Cape Jones Grease Pencil Layer Rig**, Blender 5.2.3 LTS.
One Grease Pencil object named `CapeGP`, 10 layers front-to-back:
`FaceSnapArm > Head > CowlUpperArm > Neck > ChestSnapArm > Torso > Collar >
NormalArm > Legs > CapeBack`. Strokes are traced outlines (cv2 largest
external contour, approxPolyDP, max 140 points) of existing v7c pieces,
placed by the same joint/anchor/rotation math as `snap_figure.py`. No new
art is drawn in this preset. The coloured lines in the CapeGP contact are
GP stroke colours per layer/snap — a visualization, not a recolour of the
base art. Base art is untouched; every file here is new and dated.

## Colour per layer (material, as set in the .blend)
| Layer | Material RGBA 0-255 | Seen in |
|---|---|---|
| FaceSnapArm | (255, 102, 51) orange-red | FACE_SNAP only: whole R chain above Head, 3 strokes |
| Head | (140, 51, 179) purple | every variant, 1 stroke |
| CowlUpperArm | (255, 204, 51) gold | COWL_SNAP only: both uppers above Collar, 2 strokes — COWL IS UPPER-ONLY |
| Neck | (242, 179, 128) skin | every variant, 1 stroke |
| ChestSnapArm | (51, 204, 255) cyan | CHEST_SNAP only: both chains above Torso, 6 strokes |
| Torso | (230, 230, 242) near-white | every variant, 3 strokes |
| Collar | (26, 26, 38) near-black | every variant, 1 stroke |
| NormalArm | (217, 217, 230) pale | NORMAL/APOSE_FLEX/JOINT_SMOOTH 6, FACE_SNAP 3 (L chain), COWL_SNAP 4 (both lowers+caps) |
| Legs | (204, 217, 242) pale-blue | every variant, 6 strokes |
| CapeBack | (38, 31, 51) dark purple | every variant, 1 stroke |

**Honest colour caveat, not hidden:** in the Eevee renders the snap colours
come out MUTED, not saturated. Example, FACE_SNAP transparent render: the
largest warm bucket is (192,128,128), 1,956 px — a muted rose/brown, not
saturated (255,102,51) — and no pixel in that render is orange-ish by a
strict R>180, G 60-170, B<120 test. The snap strokes are still
distinguishable in the contact (warm FACE_SNAP, gold COWL_SNAP, cyan
CHEST_SNAP tints), and the layer/material identity in the .blend is exact
(counts above, verified from the frames JSON), but do NOT quote a saturated
screen colour as measured. Saturated screen colours would need a
compositor/material tweak — owed, not claimed here. This is the same
rendering behaviour as the original CapeGP preset renders, not a new defect
introduced by this preset.

## What the preset is — a MODE, not a new pose
`COLORED_INVISIBLE_LINE_WORK` is a mode applied to a pose, not a pose itself.
Default source pose = NORMAL (apose). The same mode is built for all six
existing CapeGP poses, so it can be used for anything in this repo that
already has a CapeGP pose frame:

| Source pose | Strokes | Transparent alpha px | Alpha bbox (550x750) | Edge touch |
|---|---|---|---|---|
| NORMAL (default) | 19 | 33,919 | (165,140)-(384,638) | 0 |
| APOSE_FLEX | 19 | 34,947 | (116,132)-(448,649) | 0 |
| FACE_SNAP | 19 | 33,010 | (146,136)-(384,638) | 0 |
| COWL_SNAP | 19 | 34,944 | (116,132)-(448,649) | 0 |
| CHEST_SNAP | 19 | 34,933 | (136,140)-(430,638) | 0 |
| JOINT_SMOOTH | 19 | 34,384 | (117,133)-(447,648) | 0 |

No variant touches a canvas edge (edge-touch 0/6). No-crop rule holds:
canvas fits the figure, never the figure fits the window.

## How to call it
```
cd colored-invisible-line-work-20261031/
python3 build_colored_invisible_line_work.py                 # all 6 variants
python3 build_colored_invisible_line_work.py --source-preset FACE_SNAP
```
Outputs per variant: `blends/colored-invisible-<POSE>.blend` (single-preset
blend, no multi-frame holdover — see the CapeGP README: a layer with no
keyframe at a frame HOLDS its previous frame in a multi-frame GP object,
so proof renders must come from single-preset blends),
`variants/colored-invisible-<POSE>-transparent.png` (real output),
`variants/colored-invisible-<POSE>-on-black.png` (viewing composite).
Default proof: `colored-invisible-line-work-default-proof-20261031.png`
(NORMAL on black). Frames file:
`colored_invisible_line_work_frames.json` (source frames +
`COLORED_INVISIBLE_LINE_WORK` alias of NORMAL, plus a `_MODE` note).
To use it for anything new: add that pose's frame to a CapeGP frames JSON
in the same shape (same 10 layer names, same order), then run the builder
with `--source-preset YOUR_POSE` — same layer tree, same colours, same gate.

## What CapeGP is used for — and what it is NOT for
**Used for:** (a) layer-order proofs — a snap decision seen as a layer
stack, not just a flat render; (b) motion tests where a pose needs to live
inside Blender (compositor, camera, 2.5D depth); (c) any pose where the
layer tree itself is the deliverable; (d) now also: the COLORED INVISIBLE
LINE WORK state — seeing him as coloured outlines only, a different
invisible state from B/W invisible linework.
**NOT used for:** final clean plates (outlines only), coloured/filled
character art, or any approved pose replacement. **PIL/v7c
(`snap_figure.py` / `joint_locked_rig_v7c.py`) remains DEFAULT** for approved
poses, clean plates, and anything that must match an already-approved file
pixel-for-pixel. It is the production path; CapeGP is not a replacement.

## Staging — HERE FIRST (Mars's order, standing)
CapeGP is staged, prototyped, and tested HERE first, in this repo only.
It is NOT in any other repo yet, and it is NOT claimed as used in other
repos. Test plan T1 layer order, T2 proofs viewed, T3 no-crop, T4 pipeline
rule all pass for this preset (layer counts above, contact + default proof
viewed by the builder, edge-touch 0/6, PIL/v7c files untouched — this task
wrote only inside its own folder). **T5 new-character dry run is still
owed** — one other character's pieces traced through the same builder with
the same layer tree, proof viewed — before CapeGP may be staged into
another 2D-animation repo, and before it may be called a multi-character
tool. Only after T1–T4 pass (and T5 for multi-character claims) may CapeGP
be staged into another 2D-animation repo, with its README carried over
unchanged, name unchanged. "Put it in the repo so we can use it for
anything" is therefore satisfied as: cape-jones repo only, for anything in
this repo, not other repos yet.

## Still owed (not claimed here)
- Preset approval: 0/1.
- GP colour fills, interior linework, line-weight-by-depth (next GP passes).
- Saturated screen snap colours (compositor/material tweak, see caveat).
- T5 new-character dry run (above).
- CapeGP use in any other repo (after testing here first).
- Per-shot COLORED INVISIBLE LINE WORK proofs: 0/30.
- No repo push made here; landing is a separate step.
