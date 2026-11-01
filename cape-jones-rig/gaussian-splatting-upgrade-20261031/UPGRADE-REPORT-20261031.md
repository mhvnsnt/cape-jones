# Gaussian Splatting upgrade report — 2026-10-31

Folder: `gaussian-splatting-upgrade-20261031/` — approval 0/1 for all new work.
No repo push. No original builder or file Mars saw overwritten. V1 preset file
in `gaussian-splatting-20261031/` is UNCHANGED.

## 1. Preset V1 confirmation (unchanged)
V1 = splat turn sequence, 9 frames -40 to +40 and back, 5,846 Gaussians, stride 8,
sigma 3.2, opacity 0.85, focal 900, synthetic bulge depth sampled max 81.9px,
plate alpha 373,846px, front splat alpha 250,408px, IoU 0.6472.
Reproduced in this folder byte-identically (front md5
6e39ef989609038715f7a478ca6a459c, GIF md5 a04ca47625cd7795054844cdb30c5238).
It is a Gaussian-splat point look, NOT a true 8-bit sprite / pixel-grid palette
conversion — V3 below is the pixel-grid step toward that look.

## 2. Ten methods — 10/10 CPU runs, 0/10 vendor-CUDA runs
Each method is a CPU implementation/proxy of the method's core, run on the apose
plate and viewed in `methods/methods-contact-20261031.png`. The full vendor
CUDA versions are mappings, not runs, because this VM has no torch, no gsplat
module, and no GPU — that is the exact reason, and no paid GPU run was made.
Counts: industry 5/5 ran, experimental 5/5 ran, total 10/10 = 100% ran as CPU
core/proxy, 0% ran as vendor CUDA.

### Industry-standard 5
- I1 3DGS core (Kerbl et al., SIGGRAPH 2023): projection + depth sort + alpha
  blend. RAN. Front IoU 0.6472, 250,408px. This is V1 itself.
- I2 Voxel grid 8px (voxel / point-cloud rendering, Minecraft-style cubes):
  box dots 8x8 on the stride-8 grid. RAN. IoU 0.8778, 346,460px.
- I3 Palette quantize 16 (median-cut indexed colour, classic pixel art):
  Gaussian colours snapped to a 16-colour palette from the plate itself. RAN.
  IoU 0.6472, 250,408px (same coverage as I1, colours changed only).
- I4 Floyd–Steinberg dither 16 (halftone error diffusion): V1 front dithered
  to 16 colours. RAN. IoU 0.6433, 248,826px.
- I5 Mip-Splatting filter (Yu et al. 2024): sigma x1.6 at -20deg. RAN as a
  filter proxy; the paper's exact 3D+2D filter pair is a mapping on top.
  IoU 0.7671, 344,823px.

### Experimental 5
- X1 2DGS surfels (Huang et al. 2024): flattened disks, sigma x1.6 / y0.55.
  RAN as a flattening proxy. IoU 0.4137, 160,218px — thinnest coverage, as
  expected from flattening.
- X2 Scaffold-GS anchors (Lu et al., CVPR 2024): every 3rd Gaussian as an
  anchor, sigma x1.5. RAN as an anchor-count proxy (1,949 anchors of 5,846);
  the anchor-prediction network itself is a mapping. IoU 0.3504, 136,006px.
- X3 4DGS breathing (dynamic Gaussian time parameter): y-scale pulse at
  t=0.25 (peak pulse; an earlier t=0.5 draft was a zero crossing and identical
  to V1, and was replaced). RAN as a time-parameter proxy. IoU 0.6089, 244,145px.
- X4 Jittered / blue-noise sampling: stride-8 grid jittered +/-3px, seed 7.
  RAN. IoU 0.5498, 214,553px.
- X5 Depth-scaled sigma: two-sigma composite proxy (0.7x + 1.4x), labelled
  proxy, not a paper method. RAN. IoU 0.8979, 354,853px — highest method IoU.

### Extra mappings (NOT counted in the 10)
gsplat CUDA rasterizer, Nerfstudio splatfacto, web splat viewers (PLY export
did run for V2/V3/V4 — see below), Blender Gaussian-shader render. PLY files
are real exports: V2 23,391 vertices, V3 10,389, V4 5,846, in each version folder.

## 3. Upgrades — measured differences vs V1
All upgrades have a new front PNG and a new 9-frame turn GIF, viewed by me.
- V2 DENSE: 23,391 Gaussians (4.0x), stride 4, sigma 2.4, IoU 0.9653
  (+0.3181 vs V1, +49% relative). Dots merge into near-solid coverage; the
  point-field look is weakest here, detail is strongest. Motion: V1's
  -40..+40 out-and-back, preserved.
- V3 PIXEL-GRID: 10,389 Gaussians (1.78x), stride 6, 6x6 box dots, 16-colour
  plate palette, IoU 0.8815 (+0.2343 vs V1). Chunky square dots, true pixel
  read, face/cowl colours snapped to palette (some purple/grey shift is
  palette snap, not a recolour of the base plate). Motion: V1's -40..+40
  out-and-back, preserved.
- V4 STEP-TO-CAMERA: 5,846 Gaussians (same as V1), front IoU 0.6472 (same as
  V1 at front). Motion EXPLICITLY differs: turn -20..+20 (halved), scale
  0.85 -> 1.25 -> 0.85, lower-body shift +/-18px alternating. Frame widths
  508px (scale 0.85) -> 755px (scale 1.25); heights 922px -> 1,359px; peak
  bbox y 126-1484 (15px margin, off the edge). NOT a walk cycle: no walk keys,
  no rig pose, feet not planted, scale growth moves feet with the figure.

## 4. Corrections made during this build (not hidden)
- First methods contact pasted full-size tiles and overflowed the sheet;
  rebuilt resized to 440x600 tiles, method files unchanged.
- First V4 peak scale 1.45 touched y=1499 (canvas edge); capped at 1.25,
  peak now y=1484, 15px margin.
- First X3 4D frame at t=0.5 was a zero crossing, identical to V1; moved to
  t=0.25 (peak pulse), IoU now 0.6089, visibly different.
- First I2 voxel dots were 6px (box half 3) while labelled 8px; fixed to
  box half 4 (8x8), IoU now 0.8778.
- Depth max first reported as full-image 84.8px; corrected to sampled max
  (V1 81.9px, matching the original report) — the stride grid differs per
  version, so V2/V3 sampled maxima differ (84.5 / 83.2).

## 5. Still owed
- Approval for all new work: 0/1 (V1 preset approval stands separately).
- True multi-view Cape capture (front + side + back from Mars's FLA pieces,
  or a Mars-approved free GPU training run): 0/1.
- Real gsplat / splatfacto CUDA training run: 0/1 (needs a Mars-approved free
  GPU run, never paid).
- True Blender Gaussian-shader render (splat ellipses, not points): 0/1.
- Per-pose splat application beyond apose: 0/1.
- A true back view from splats alone is NOT owed as a claim — impossible from
  one front plate; FLA back pieces are the route.
- No repo push made in this task; landing is a separate step.
