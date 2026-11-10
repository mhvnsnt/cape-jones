# Crop-window audit — Cape Jones rig builders, 2026-10-31

Scope: every builder in `~/workspace/cape-jones-rig/` that renders a
figure or a piece, searched for fixed-canvas rotation, fixed-size
transform, and edge-clipping paste. Search excluded `venv/` (library
code, not our builders). Counts below are grep counts of
`expand=False` in our builders: 50+ sites across ~35 files. The pattern
is everywhere because it was copied from builder to builder.

## The three crop-window mechanisms (all three are real, all three clip)

### M1. `layer.rotate(angle, center=joint, expand=False)` — limb rotation
The limb is pasted onto a full-canvas transparent layer (1100x1500,
or 2200x1500 in inbetweening), then rotated in place. `expand=False`
is Pillow's default: the output stays the layer's size, so anything
the rotation swings outside the layer is dropped silently.
- Files (primary, not exhaustive): `joint_locked_rig.py:61`,
  `joint_locked_rig_v4.py:45`, `v5.py:45`, `v6.py:45`, `v7.py:41`,
  `v7b.py:23`, `v7c.py:23`, `repose_tests_v2.py:27`,
  `dance-improved-20261031/build_dance.py:25`,
  `clean-100-20261031/flex-opposition/build_flex_opposition_20261031.py:69,139,161,171`,
  `clean-100-20261031/exposure-clips/rig-v7c-clean100.py:19`,
  `dual-light-variants-20261031/build_base.py:34`,
  `build_true_final_flex_v2.py:56,77,132`,
  `build_exaggerated_deep_squat.py:56,77,132`,
  `build_hip_lower.py:67,80,150`,
  `pose-dialects-20261031/build_poses.py:22`,
  `ginyu-force-poses-20261031/build_ginyu_force.py:27`,
  `face-cowl-snap-wire100-20261031/snap_figure.py:39`,
  `fight-and-sheets-20261031/build_fight.py:36`,
  `inbetween-20261031/build_inbetween.py:31`,
  `wrist-attach-fix-20261031/build_wrist_fixes.py:105`,
  `movements-interp-v2-20261031/build_interp_v2.py:39`, and more
  (dance-kneefeet, dance-arm-snap, gap-close-rig, joint-cleanup,
  pose-dialects-fix, ginyu-force-limits-broken, depth-25d cowl_gate_v2b).
- What it clips: a limb tip swung past the canvas edge. On the centred
  apose it usually does NOT clip (margins are large), which is why it
  survived so long — it clips on wide, off-centre, or leaning poses,
  exactly when Mars notices.
- Fix in this folder: `no_crop.limb_layer_nocrop()` — pad, rotate,
  return the expanded layer when the piece no longer fits, and
  composite with `paste_nocrop()`.

### M2. Whole-figure `rotate()` / `transform()` on a fixed (1100,1500) canvas
- `limits-broken-10x10-20261031/build_10x10.py` G5 section:
  `rot_arm()` = `im.rotate(deg, center=(550,750))` (expand defaults
  to False); `im.transform((1100,1500), Image.AFFINE, (1,k,0,0,1,0))`
  for lean shears; `im.rotate(15)` for fly tilt.
- `poses-as-movements-20261031/build_movements.py:23`:
  `im.rotate(rot, expand=False, center=(275,375))` on the downscaled
  550x750 video frame — same window, smaller.
- What it clips, MEASURED on the apose (base alpha 373,846 px,
  bbox x248-876 y253-1295):
  - Rotations -10 / -18 / +10 / 15 deg: 11-59 px difference vs
    padded-truth, edge touch 0. That is RESAMPLING NOISE (<0.02%),
    not clipping — reported honestly, not inflated. The window is
    still wrong structurally: it only needs a nearer-edge pose to clip.
  - Lean shear 0.15: 0 px lost, but bbox shifts to x113 — 113 px from
    the edge, one more lean step from clipping.
  - Lean shear 0.30 (G5 I05, the "run lean"): **3,994 px lost
    (1.07%), left-edge touch 177 px, bbox hits x=0** — the foot/leg
    at the bottom of the figure is sheared off the left edge. This
    is Mars's lean complaint, measured.
  - Shear -0.20: 0 px lost, bbox reaches x1084 (16 px margin).
  - Lean test shear 0.40: **39,134 px lost (10.47%), left-edge
    touch 402 px** — a whole foot/leg chunk.
  - Compound lean (rotate -20 then shear 0.35): **34,830 px lost
    (9.3%), left-edge touch 339 px**.
- Fix in this folder: `no_crop.rotate_nocrop()` and
  `no_crop.shear_nocrop()` — pad, transform, trim to alpha bbox + 40px.

### M3. `paste_at()` / `paste()` / `alpha_composite()` at a partly off-canvas position
Every builder defines `paste_at(c, im, cx, top)` as
`c.paste(im, (cx - w/2, top), im)` (or alpha_composite with the same
coordinates). Pillow pastes clip silently at the canvas edge — no
error, no warning, pixels just vanish.
- Measured piece test (L3): leg lower piece, 23,687 alpha px, pasted
  at (-50,1400) on an 1100x1500 canvas: **15,691 px lost (66%)**,
  bottom-edge touch 91 px, left-edge touch 46 px. That is the
  piece-level crop window.
- Fix in this folder: `no_crop.paste_nocrop()` — canvas auto-expands
  transparent to hold the whole piece, shift returned so coordinates
  stay trackable. New L3: 0 px lost, edge touch 0.

## What is NOT a crop window (do not "fix" these by mistake)
- A piece's own bbox (e.g. `sliced/` pieces, `cut-limbs-v7c/` pieces):
  the piece file IS the art; its bbox is its extent, not a window.
  Clipping happens only when that piece is pasted/rotated onto a
  smaller window than it needs.
- Contact-sheet tiling (`build_10x10.contact()`, movement sheets):
  tiles are resized keeping aspect (275 wide, height from 1100:1500),
  so no figure pixels are cut by tiling. BUT the old sheets baked a
  grey background into the display tiles, which made the tile look
  like a window around a figure that has no background. New sheets
  use a checker display background, labelled DISPLAY ONLY, and the
  figure files themselves stay transparent RGBA.
- Resize-to-smaller, mirror, blur: these change alpha counts by
  scaling / spreading, not by clipping (measured: resize variants
  0 px lost vs their own resized truth; blur spreads alpha by
  +33,573 px). Do not quote those count changes as clipping.

## Builders updated vs still needing the same fix
- UPDATED in this folder (new path, gate-passed re-renders):
  the G5 whole-figure path (rotate/shear/mirror/resize/blur/double
  exposure) via `no_crop.py`, and the generic limb/paste path via
  `limb_layer_nocrop()` / `paste_nocrop()`. Proof: `frames-new/`,
  gate output `gate-new-20261031.json` (23/23 PASS).
- NOT YET EDITED (frozen builders, per standing rule — gate sits in
  front, builders are not rewritten here): `joint_locked_rig_v7c.py`,
  `snap_figure.py`, `build_poses.py`, `build_movements.py`,
  `build_inbetween.py`, and the ~35 files listed under M1. They are
  NOT claimed fixed. The fix for them is: replace their `limb()` /
  `paste_at()` internals with `no_crop.limb_layer_nocrop()` /
  `paste_nocrop()`, then re-run `check_no_clip.py` on their output
  and only claim fixed when it passes. That migration is still owed,
  file by file, and must not be claimed done from this folder alone.
- A delivery crop at export (e.g. a 1920x1080 / 1080x1920 delivery
  frame) is a SEPARATE step, governed by the dual-orientation
  protected-square spec, and is only allowed after the no-clip gate
  passes on the full figure. It is not part of building.
