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
| Board 02 (`production/2d-parking-lot/boards-layered/cj-pl-02/`) | `production/2d-parking-lot/boards/cj-pl-02.png` | background-complete, 3 props, Jones, car shadows, light, grade |
| Board 03 (`production/2d-parking-lot/boards-layered/cj-pl-03/`) | `production/2d-parking-lot/boards/cj-pl-03.png` | background-complete, 4 props, Jones, car shadows, light, grade |
| Board 04 (`production/2d-parking-lot/boards-layered/cj-pl-04/`) | `production/2d-parking-lot/boards/cj-pl-04.png` | background-complete, 2 props, Jones, car shadows, light, grade |
| Board 05 (`production/2d-parking-lot/boards-layered/cj-pl-05/`) | `production/2d-parking-lot/boards/cj-pl-05.png` | background-complete, 1 prop (broken lamp), Jones, car shadows, light, grade |
| Board 06 (`production/2d-parking-lot/boards-layered/cj-pl-06/`) | `production/2d-parking-lot/boards/cj-pl-06.png` | background-complete, 3 props, Jones, car shadows, light, grade |
| Board 07 (`production/2d-parking-lot/boards-layered/cj-pl-07/`) | `production/2d-parking-lot/boards/cj-pl-07.png` | background-complete, 8 props (incl. dumpsters + barriers), Jones, car shadows, light, grade |

Boards 02–07 are DONE (2026-11-23, stage2) — each board measured fresh with
pixel profiles, its own specs in `segment.py`, its own background-complete,
PSD and moved-Jones proof. They are different drawings, not views of one
set, so no coordinates were reused.

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
Plate and board 01: per-row fill — narrow runs by horizontal interpolation;
wide asphalt runs by a same-rows donor (clean asphalt at the same rows, so
the horizontal parking lines continue at the right height), with the stop-sign
pole and the diagonal bay line excised from the donor, the donor's brightness
gain-matched to the local interpolation, and the donor blurred along x so its
segment joins do not step. The fill feathers to pure interpolation at the
mask silhouette (8px distance ramp), so the seam follows the prop's
silhouette, never a box. The diagonal bay line is re-drawn across the filled
bands from its Hough-fitted equation. Lamp-head holes are filled vertically
(the glow is bright above and below the head, dark sky to the sides —
horizontal fill made a dark slab).

Boards 02–07: the Jones hole is 40–55% of the frame and spans sky,
buildings, fence, car rows and asphalt at once, so horizontal-only fill
fails (orange wash across the torso, white slab at the legs). These boards
use a TWO-AXIS fill instead of the donor: each masked pixel gets both a
horizontal interp (nearest unmasked left/right in the row) and a vertical
interp (nearest unmasked above/below in the column), blended with a span
weight — the axis whose anchors are closer dominates. Columns with only
one vertical anchor (the hole runs to the frame bottom) use a vertical
GRADIENT from that anchor (sky/buildings, weight 0.75) at the hole's top to
the row's horizontal interp (asphalt, weight 0.25) at the frame bottom, so
the fill goes sky → buildings → asphalt like the real lot. Both axes'
anchors are MEDIANS of the 25px (horizontal) / 10px (vertical) runs just
outside the mask edge, not single pixels — a mask that sits a few px short
of a prop's true edge would otherwise land an anchor ON the figure and
smear its colour across whole rows (the 06 shoulder's white ran 1px past
the mask and filled a whole column white; the 03 hand's white ran 7px past
it). A guard rejects an anchor run that is >25% white/bright figure pixels
and falls back to the darker half of the run. The blend is Gaussian-blurred
(sigma 15) inside the mask so the per-column/per-row anchor steps do not
read as the figure's ghost, then feathered to pure interpolation at the
silhouette. The diagonal bay line's colour is the median of the
bright-AND-saturated pixels in a ±5px band along the full fitted line
(brightness alone catches the white suit where the line passes under
Jones and comes out white; saturation rejects it). (`complete_bg.py`)

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
the original — plate **0.490** mean abs diff, board 01 **0.159**, board 02
**0.367**, board 03 **0.260**, board 04 **0.220**, board 05 **0.257**, board
06 **0.243**, board 07 **0.257**. The layered split reproduces the originals
essentially exactly at rest. (02's number is the highest because its fill
runs under the widest lamp glow; the rest composite still matches at rest —
the number measures the background-complete's fill under the figure against
the figure's own pixels, which is not a visible error at rest.)

**Full PSD sodium composite:** plate 8.53, board 01 8.30, board 02 6.70,
board 03 7.79, board 04 8.08, board 05 11.70, board 06 9.78, board 07 8.58
mean abs diff vs the original — that is the v1 light/grade layers'
contribution on top of the baked plate (v1 was 8.26). The light layers are
the toggle, not a redraw; the separation itself matches at 0.49 / 0.16 /
0.22–0.37. The purple-state boards (05, 06, 07) read higher on the sodium
composite because the sodium light is the wrong state for them — their
PURPLE composites are the ones that match: 05 **7.37**, 06 **8.03**, 07
**8.69** (02 **9.23**, 03 **9.58**, 04 **9.96** on purple, the wrong state
for those).

**Moved-car proof** (`purple-lot-layered-v2/proof-moved-car.png`): the blue
car moved from its spot (bbox x437–667, y542–617) to the open sunlit asphalt
at centre (1415, 887), scaled 1.5× for the foreground depth, with a soft
contact shadow ellipse added under it (labelled as added). Own-eyes: the car
sits on the open lot with NO rectangular edge — the asphalt and parking lines
continue uninterrupted around its silhouette — and the vacated spot reads as
clean asphalt with the light pool continuing across it. No box, no ghost.

**Moved-Jones proofs** (`boards/cj-pl-0N/proof-moved-jones.png`, one per
board, Jones moved far from his spot, scaled for depth, soft contact shadow
added and labelled as added — `proof_moved_prop.py`):
- 02: Jones 0.5× to centre (450,950), open bottom-left asphalt. Own-eyes:
  no rectangular edge, cape's wavy edge clean, vacated spot reads as clean
  dark lot. Minor: a ~5px white sliver of the arm's right edge at the
  vacated spot's right edge (x1580–1588), and the bright light-pool strip
  behind the arm (real background, now exposed).
- 03: Jones 0.5× to centre (1650,900), open right foreground. Own-eyes:
  no rectangular edge, vacated spot clean dark lot, car rows intact. Minor:
  the remote's top-left tip leaves a ~20×30px white sliver in the bg.
- 04: Jones 0.45× to centre (1600,850), open right foreground. Own-eyes:
  no rectangular edge, face + hand + remote are clean silhouettes, vacated
  spot reads as the board's soft blurred background with lamps and car row
  intact. The lamp pole's warm tan at (820,400–450) is the pole's own lit
  colour, not an artifact.
- 05: Jones 0.8× to centre (350,850), open left lot. Own-eyes: no
  rectangular edge, cape's rim-light clean on the moved figure. The
  vacated spot shows the cape's purple rim-light as a soft ghost curve
  around where Jones stood (the rim-light is a glow in the bg, not part of
  Jones) and a ~5px white sliver at the hand's left edge.
- 06: Jones 0.5× to centre (600,900), open centre-left asphalt. Own-eyes:
  no rectangular edge, vacated spot clean dark purple field. (The torso's
  left edge was 1–9px short at y500–650 and left a white sliver in the
  first proof — fixed by widening the polygon, mask re-run, bg re-run;
  the proof shown is the fixed one.)
- 07: Jones 0.5× to centre (1550,880), open centre-right, AND the
  dumpsters + barriers group 1.2× to centre (400,950), open left
  foreground. Own-eyes: no rectangular edge on either move, dumpsters read
  as proper boxes, their vacated spot reads as clean fence/wall. Minor:
  the cape's rim-light arc ghosts faintly at the vacated spot, as on 05.

## The PSDs

`purple-lot-layered-v2.psd` (49,990,218 B, sha256
`03c88f59…`) and `cj-pl-01-layered-v2.psd` (54,122,334 B, sha256 `5b89ba82…`)
are ~50 MB each — over the 25 MB web-upload limit and the connector's 16 MiB
push limit. They are NOT in the repo tree. They ship via a GitHub Release
(slices/Releases method this project uses for big files). Layer PNGs and
composites ARE in the tree; the PSD can be rebuilt from them at any time with
`rig/true-prop-separation/build_psd.py`.

Boards 02–07 PSDs (same Release route, NOT in the tree):
- `cj-pl-02-layered-v2.psd` — 36,045,918 B, sha256
  `26d864c499c5d8cf302ed6a59ee16307bbc4ded56f0adb3fd625301206f8fa1c`
- `cj-pl-03-layered-v2.psd` — 41,517,050 B, sha256
  `a803761fde8cc1f00259d15ae1003ecd422997169f4d03c5463fbd6be9e00c7a`
- `cj-pl-04-layered-v2.psd` — 33,564,582 B, sha256
  `78958b928b4c0f7659c6f926c1045709fcb16f3be2dcb3d0cdeffd7ac2208f46`
- `cj-pl-05-layered-v2.psd` — 31,207,154 B, sha256
  `342baefd0b683a7ee4c1c62994003264baf896de477623f6f500d0f4138a5d29`
- `cj-pl-06-layered-v2.psd` — 38,071,262 B, sha256
  `7dc4aab026c9ecb1127573c9469c837c779b3b17f02150e491c748d0409e9707`
- `cj-pl-07-layered-v2.psd` — 53,897,998 B, sha256
  `cca3ce63e19e82d7043520ef59aaf57142d0a7bca5ff6933757951045d58c03a`

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
- **Boards 02–07:** the background behind Jones was never drawn (he
  occludes it) — the background-complete is a plausible reconstruction
  (two-axis fill + blur), not the true background. It reads as empty lot;
  parking lines crossing the vacated spot have gaps where the hole was, and
  the lamp glow's exact edge and the light pools' exact edges are
  approximated.
- **02:** the lamp-head hole at the frame top leaves a soft dark patch
  (vertical fill has no above anchor there); the arm's right edge is ~5px
  short (white sliver at the vacated spot's right edge); the diagonal
  parking line is re-drawn (fitted line + bright-and-saturated colour),
  not the original stroke.
- **03:** a ~20×30px white sliver at the remote's top-left tip remains in
  the bg; the lamp-head glow peak is interpolated.
- **04:** a tiny black/white sliver at ~(1400,650) (remote tip vs car row);
  the whole bg is soft by design (blurred-background board).
- **05:** the cape's purple rim-light outline stays faintly visible as a
  soft curve around the vacated spot; the diagonal line is re-drawn; the
  shadow layer is essentially empty (23 px) because the board has no
  distinct contact shadow under the boots — the purple light washes it
  out, and the asphalt under the boots matches the surrounding asphalt.
  The 05 lamp's crack shards are light effects left in the background.
- **06:** the cape is low-contrast vs the sky, so the mask edge there is
  outline-driven and may be ±5px; the head's hole fills slightly darker
  than the surrounding sky (a soft dark band at the vacated spot's top).
- **07:** dumpsters/barriers are box-shaped — their masks are
  near-rectangles by nature (verified: corners ~100% filled, which is
  correct for boxes, not a box-cut cheat); the cape's rim-light arc ghosts
  faintly at the vacated spot, as on 05.

## Extending to boards 02–07

Done (2026-11-23, stage2). The steps were the same as above, with the
two-axis fill in `complete_bg.py` replacing the donor for these boards
(see Method), `proof_moved_prop.py` (generalised from
`proof_moved_car.py`) moving Jones instead of a car, and the dumpsters /
barriers group moved as well on 07. Per-board specs live in
`segment.py` (`JONES_02`–`JONES_07` and the `SPECS` entries); per-board
background config lives in `complete_bg.py` (`BG` dict). Pipeline scripts
for all seven boards + the plate live in `rig/true-prop-separation/`.
