# TRUE PROP SEPARATION — PURPLE LOT layered rebuild (v2)

**Owner rule (2026-11-23, permanent):** ALWAYS clean alphas with no rectangular
edges. Every cut, slice, prop, hand, remote, part — cut along the art's own
edges with clean alpha, never a square/box crop, never a rectangular edge
showing, never baked background inside a cutout. True prop separation,
re-sliced cleanly from the source art. If a prop cannot be separated cleanly,
say which one and why and re-slice from the source art instead of faking it.

## What this replaces

The v1 layered PSD (`torbox-pulls/free-proof/purple-lot-layered.psd`, PR #443)
split the flat plate by REGION — bands for sky/skyline/asphalt and box crops
for the cars, lamps and stop sign. A car moved far from its spot would carry a
visible rectangle of the old background. That version is **superseded**. Do not
ship it as the final method. The v2 rebuild below is the method.

## What was rebuilt (v2, this PR)

| Set | Source | Layers |
|---|---|---|
| Plate (`production/2d-parking-lot/purple-lot-layered-v2/`) | `rig/plate-sodium.png` (2048×1152) | background-complete, 6 props, car shadows, light, grade |
| Board 01 (`production/2d-parking-lot/boards-layered/cj-pl-01/`) | `production/2d-parking-lot/boards/cj-pl-01.png` | background-complete, 6 props, Jones, car shadows, light, grade |

Boards 02–07 are NOT in this PR — the pipeline below is proven on the plate
and board 01, and each remaining board needs its own measured specs (see
"Extending to boards 02–07"). They are different drawings, not views of one
set, so no coordinates are reused.

## Method

**Props — cut along the art's own edges, never a box.**
- Cars and Jones: hand-measured polygon ~5px outside the true edge, grabCut on
  the polygon's bbox crop only, sure-FG/BG seeds, result clamped to the polygon
  dilated 3px so it can never leak into the background. Alpha follows the
  silhouette (roofline, tires, cape edge, boots).
- Lamps and stop sign: traced outlines (pole rect, head ellipse, sign
  octagon), 1px feather. No grabCut, no glow — the glow is a light layer.
- Overlapping car rows cannot be split car-by-car: the cars occlude each
  other and the shared edges do not exist in the drawing. Each row is ONE
  cluster layer whose outer silhouette follows the cars' real edges.
  (`rig/true-prop-separation/segment.py`, specs per board; `masks.json` and
  `mask-qa.png` per set.)

**Background-complete — the lot with the props removed, rebuilt from the art.**
Per-row fill: narrow runs by horizontal interpolation; wide asphalt runs by a
same-rows donor (clean asphalt at the same rows, so the horizontal parking
lines continue at the right height), with the stop-sign pole and the diagonal
bay line excised from the donor, the donor's brightness gain-matched to the
local interpolation, and the donor blurred along x so its segment joins do not
step. The fill feathers to pure interpolation at the mask silhouette (8px
distance ramp), so the seam follows the prop's silhouette, never a box. The
diagonal bay line is re-drawn across the filled bands from its Hough-fitted
equation. Lamp-head holes are filled vertically (the glow is bright above and
below the head, dark sky to the sides — horizontal fill made a dark slab).
(`rig/true-prop-separation/complete_bg.py`)

**Shadows — extracted, not painted.** The contact shadows are the luminance
difference between the original and the background-complete, clipped to the
ground strips under the props, as a MULTIPLY layer (`layers/car_shadows.png`).
A moved prop carries no shadow at its new spot until one is added — that is
the honest behaviour, and the moved-car proof adds a soft ellipse and labels
it as added.

**Light / grade — reused from v1 (synthetic, full-frame, no box cuts).**
Lamp glow and light pools are radial SCREEN layers, the sodium/purple shift is
a COLOR solid toggle, plus dusty air, vignette and grain. Sodium visible,
purple hidden by default; flip the three pairs for the purple state. The glow
is baked into the plate's sky and cannot be cleanly extracted as a prop, so
the synthetic radial is the honest treatment. Stored once in
`purple-lot-layered-v2/light/` and shared by every set.

## Proof

**Rest match (light/grade OFF):** background + props (+ Jones) + shadows vs
the original — plate **0.490** mean abs diff, board 01 **0.159**. The layered
split reproduces the originals essentially exactly at rest.

**Full PSD sodium composite:** plate 8.53, board 01 8.30 mean abs diff vs the
original — that is the v1 light/grade layers' contribution on top of the baked
plate (v1 was 8.26). The light layers are the toggle, not a redraw; the
separation itself matches at 0.49 / 0.16.

**Moved-car proof** (`purple-lot-layered-v2/proof-moved-car.png`): the blue
car moved from its spot (bbox x437–667, y542–617) to the open sunlit asphalt
at centre (1415, 887), scaled 1.5× for the foreground depth, with a soft
contact shadow ellipse added under it (labelled as added). Own-eyes: the car
sits on the open lot with NO rectangular edge — the asphalt and parking lines
continue uninterrupted around its silhouette — and the vacated spot reads as
clean asphalt with the light pool continuing across it. No box, no ghost.

## The PSDs

`purple-lot-layered-v2.psd` (49,990,218 B, sha256
`03c88f59…`) and `cj-pl-01-layered-v2.psd` (54,122,334 B, sha256 `5b89ba82…`)
are ~50 MB each — over the 25 MB web-upload limit and the connector's 16 MiB
push limit. They are NOT in the repo tree. They ship via a GitHub Release
(slices/Releases method this project uses for big files). Layer PNGs and
composites ARE in the tree; the PSD can be rebuilt from them at any time with
`rig/true-prop-separation/build_psd.py`.

## Honest limits

- Car rows are cluster layers, not per-car (occluded edges do not exist).
- The lamp glow and light pools are synthetic radials, not extracted.
- The purple boards' sodium light state is a re-light, not a drawn state.
- A moved prop has no contact shadow at its new spot unless one is added.
- The lamp-head hole's glow peak is interpolated (horizontal interp gives
  mid-orange; the vertical fill restores the bright core). At 3× zoom the
  head-hole patch shows a faint rectangular edge; at shot scale it reads as
  the glow's peak.
- The far lamp's pole disappears behind the car row (~y540) — the traced
  polygon ends where the pole meets the car roof; that is the visible edge,
  not a guess.
- The background-complete's filled asphalt is smoother than the drawn asphalt
  (the donor is blurred and gain-matched); at shot scale it reads as the
  lot's light falloff, not as a patch.

## Extending to boards 02–07

1. View the board own-eyes; list its props (cars, lamps, signs, Jones, and
   for 05 the broken lamp + fence; for 04 the blurred background; for 07 the
   dumpsters and barriers).
2. Measure each prop's polygon with pixel profiles (row/column scans — do not
   trust downscaled previews for coordinates) and add a spec to
   `rig/true-prop-separation/segment.py`.
3. Run `segment.py`, view `mask-qa.png` (magenta on checkerboard), fix leaks.
4. Run `complete_bg.py`, view `background-complete.png` own-eyes (ghost car,
   triangle, pole remnant, red speck are the known failure modes — the donor
   and gain fixes in this PR address them; a new board may need its own donor
   segments in `donor_segments()`).
5. Run `build_psd.py`, check the rest composite, and build a moved-prop proof.
6. Stage with `stage_tree.py` and land the same way as this PR.
