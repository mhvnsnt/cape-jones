# Cape Jones rig — default T-pose (locked v7)

Cape Jones is Mars's original character. These pieces are cut from
Mars's own exploded sheets, not from Pokemon, Sonic, or any other
franchise. No proprietary franchise material is in this folder.

## The locked default — v7, 2026-10-31

`previews/assembly-preview-v7-20261031.png` is the locked default
T-pose. Do not overwrite it. A new version gets a new dated filename,
and `TPOSE-LOCKED-v7.md` is superseded in writing, never silently edited.

Rebuild it exactly:

```
python3 assemble_tpose_default.py
```

That script is tested byte-identical to the locked preview
(420,161 bytes). The machine-readable positions are in
`locked-default-tpose.json`. In short, canvas 1100x1500, scale 0.95
unless noted, layer order bottom to top:

Cape_Back_Main 550/410, Leg_Front 450/720,
Leg_Back_GRAFTED 650/720, Arm_Front (left) 300/380,
Arm_Front (right) 800/380, Pelvis 550/680, Cape_Collar 550/370,
Torso_Chest 550/400, Belt_Overlay 550/670, Neck 550/360 scale 1.05,
Head_Front 550/250.

Arm flip terminology, per Mars: VERTICAL flip = top-to-bottom,
NOT horizontal (left-right) flip. V7 arms: pads TOP, bicep BOTTOM,
fists/fingers/thumbs BOTTOM, both sides.

## What is in here

- `pieces/` — 29 PNGs: the original 28 sliced pieces, plus
  `Leg_Back_GRAFTED.png`, the locked screen-right leg with the full
  toe restored (the original zone cut it at sheet x=1935; the real
  foot runs to x=1979). The original `Leg_Back.png` is kept, not
  deleted, so the graft is auditable.
- `pack1/` — 25 PNGs: Pack 1 clean arms, gauntlets, and hands
  (6 UpperArm, 6 Gauntlet, 13 Hand pieces = 14 hands).
- `cut-limbs/` — 8 PNGs: arms and legs cut at the elbow/knee circles,
  with overlap so the joint circle is kept on both halves.
- `previews/` — v1 through v7 assembly previews, in order.
- `docs/` — the dated correction notes for each version.
- `slice_clean.py` — the clean-cut tool. `CLEAN-CUT-NOTES.md` is the rule.

## Clean-cut rule — no square crops

Full sheets always go through `slice_clean.py` first: background
colour from the sheet corners, mask by distance from background,
morphological closing + hole fill, connected components found by
the sheet itself (no hand rectangles), 1px feather + fringe
decontamination, trim to silhouette only. rembg (u2netp) is only a
per-piece check, especially black-on-black cape, never a full-sheet
tool — it ghosts multi-island sheets. If a slice looks square-cropped
or a toe/finger is cut, the slice is wrong, not the character:
re-slice by component and graft the missing part, as was done for
the right leg in v7.

## Adding more pieces (Packs 2, 3, 4, 5, …)

1. Bring the new sheet in, clean-cut slice it with `slice_clean.py`.
2. Save each new piece as its own file, dated, never overwriting a
   locked piece. Add it to this folder in a new PR, additions only.
3. Show Mars the new assembly first. Only after approval does a new
   version become the locked default, with a new `TPOSE-LOCKED-*.md`,
   a new `locked-default-tpose.json`, and a builder that reproduces
   it byte-for-byte.
4. Future shots reuse this default setup: same pieces, same positions,
   same flips, unless a new locked version says otherwise.

## Animate

`build-cape-jones-rig.jsfl` / `-v2.jsfl` / `-v7.jsfl` build the
`.fla` inside Adobe Animate (no `.fla` is exported from chat).
v7 is the current one for the locked T-pose; see its header for the
v7 layer and position notes.
