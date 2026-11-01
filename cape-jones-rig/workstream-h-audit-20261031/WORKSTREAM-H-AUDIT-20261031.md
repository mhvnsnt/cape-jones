# WORKSTREAM H — Audit, Mars 100% sweep 2026-10-31 (audit date 2026-10-31, evening CDT)

Scope: Gaussian / 8-bit / Invisible Presets / CapeGP, in `~/workspace/cape-jones-rig/` only.
No repo push. No deletions. No original file overwritten by this audit — only this new
dated folder was added. Nothing in this audit is approved or landed; approvals below are
0/1 unless a line says "saved by Mars order" (V1 default only).

## FOCUS CHANGE applied — TV PRODUCTION READINESS first (Mars, 2026-10-31 20:53 CDT)

This audit does NOT restart and does NOT expand preset variants. It re-sorts the same
scope into two buckets, per the focus change:

- **PRODUCTION — work that blocks shots:** a saved default look, a no-crop invisible
  power, invisibility/silhouette effects, and layer proofs that let a shot be checked.
  If it is missing, a shot cannot be delivered in that look.
- **ADDITIVES / EXTRAS — preset variants that do NOT block shots:** denser / pixel-grid /
  stepping variants, method proxies, and an extra coloured invisible state. Built, counted,
  and labelled separately — never at the expense of the production gaps.

Headline: apose proofs are largely built, but **shot production is not ready**, because
approvals are 0 and per-shot application is 0. Do not read "built" as "ready to air."

## Percentages — read the denominator, not just the number

### PRODUCTION bucket
| Item | Built | Approved | Per-shot / per-pose |
|---|---|---|---|
| 8-bit Preset V1, saved as DEFAULT | 1/1 = 100% | Saved by Mars order 2026-10-31 20:17 CDT (not a new-work approval) | Apose only; per-pose beyond apose 0/1 |
| Invisible Power V1, NO-CROP FIXED (fixed version; draft kept separately) | 1/1 = 100% | 0/1 | 0/30 shots |
| Silhouette Preset Pack Two effects (see below) | 8/8 = 100% | 0/1 (pack) | Per-shot / per-pose application still owed (apose plate only) |
| CapeGP layer proofs (6 presets, see below) | 6/6 = 100% | 0/1 (pack) | Per-shot CapeGP proofs 0/30 |
| **Production builds, apose level** | **16/16 = 100%** (1 + 1 + 8 + 6) | **New-work approvals 0/3 packs** (Invisible, Pack Two, CapeGP) | **Per-shot 0/30 where counted** |

Caveat on CapeGP in production: PIL/v7c is DEFAULT for clean plates and approved poses.
CapeGP is layer-proof / motion-test support only (outlines only, no fills). CapeGP therefore
does NOT block clean plates — its absence would block layer-proof checks, not the plate itself.
That distinction is production-relevant and is preserved, not flattened.

### ADDITIVES / EXTRAS bucket (labelled separately, do not expand further first)
| Item | Built |
|---|---|
| Gaussian upgrades V2 DENSE, V3 PIXEL-GRID, V4 STEP-TO-CAMERA | 3/3 = 100% (variants only; V1 remains default) |
| Gaussian methods, CPU core/proxy runs (I1–I5 industry + X1–X5 experimental) | 10/10 = 100% CPU; 0/10 = 0% vendor CUDA |
| Colored Invisible Line Work — 1 preset as a MODE, 6 source-pose variants | 1/1 preset, 6/6 variants, 12 variant files (transparent + on-black) |
| **Additives built** | **3 + 10 + 1 preset (6 variants) — all built, all unapproved as new work** |

### Overall new-work approvals (all packs in scope)
Gaussian upgrade 0/1 + Invisible Power fixed 0/1 + Pack Two 0/1 + Colored 0/1 + CapeGP 0/1
= **0/5 = 0% approved, 0 pushed, 0 landed.** V1 default saved is the only "saved" item, and
it is not counted as a new-work approval.

### Production gaps still owed (the work that matters first now)
- Mars approval for each new pack: 0/5 (above).
- Per-shot application: Invisible Power V1 0/30; CapeGP per-shot proofs 0/30; Pack Two
  per-shot/per-pose application owed (apose only at present).
- Gaussian: true multi-view capture 0/1; CUDA run on a Mars-approved FREE GPU only 0/1
  (never paid); Blender Gaussian-shader render 0/1; per-pose splats beyond apose 0/1.
- CapeGP T5 new-character dry run 0/1 — owed before any multi-character claim or any
  other-repo staging. T1–T4 are the here-first tests in the CapeGP README; T5 is the
  remaining gate for that claim. CapeGP use in any other repo: 0, not staged, not claimed.
- Colored: saturated snap colours owed (Eevee renders muted — see below); GP fills,
  interior linework, line-weight-by-depth owed.
- **NOT owed, do not count as a gap:** a true back view from splats alone. Impossible
  from one front plate. The route is Mars's FLA back pieces.

## (1) Gaussian / 8-bit — honest label throughout

Tool name stays **Gaussian Splatting**. Builder for V1: `build_splats.py` in
`gaussian-splatting-20261031/`. Never renamed in this audit.

- **V1 — 8-bit Cape Jones Preset, SAVED as default** (`gaussian-splatting-20261031/
  8-BIT-CAPE-JONES-PRESET-20261031.md`): 5,846 Gaussians, stride 8, sigma 3.2,
  opacity 0.85, focal 900, plate alpha 373,846 px, front splat alpha 250,408 px,
  **IoU 0.647**. Turn GIF 9 frames, −40° to +40° and back (pseudo-turn, NOT a full turn,
  NOT a true back). Depth is a SYNTHETIC bulge proxy (max 81.9 px), NOT a true
  multi-view reconstruction, NOT a scanned back, NOT a measured depth map.
  **Honest label:** Mars calls it "8-bit", but the look is a Gaussian-splat point field,
  NOT a true pixel-grid sprite with a fixed palette. Call it "8-bit Cape Jones preset
  (Gaussian splat point look)" when accuracy matters. V1 is a splat-point proof, NOT a
  clean-plate replacement. No-crop: V1 files are the untouched originals.
- **V1 reproduction verified by this audit:** upgrade-folder V1 front and turn GIF are
  byte-identical to the originals (front md5 `6e39ef989609038715f7a478ca6a459c`,
  GIF md5 `a04ca47625cd7795054844cdb30c5238`). Original V1 folder unchanged.
- **V2 DENSE** (`gaussian-splatting-upgrade-20261031/8BIT-V2/`): stride 4, sigma 2.4,
  23,391 Gaussians (4.0× V1, PLY vertex count re-verified), IoU **0.9653** (+0.3181).
  Same −40°..+40° motion. Near-solid coverage; point-field look weakest here.
  ADDITIVE variant, not the default.
- **V3 PIXEL-GRID** (`8BIT-V3/`): stride 6, 6×6 box dots, 16-colour plate palette,
  10,389 Gaussians (PLY re-verified), IoU **0.8815** (+0.2343). Closest to a true 8-bit
  pixel look; V1/V2 remain soft-dot splats. Same −40°..+40° motion. ADDITIVE variant.
- **V4 STEP-TO-CAMERA** (`8BIT-V4/`): 5,846 Gaussians, front IoU 0.6472 (same as V1 at
  front). Motion explicitly differs: turn halved to −20°..+20°, scale 0.85→1.25→0.85,
  lower-body shift ±18 px alternating. **Stepping PROXY only, NOT a walk cycle, no walk
  keys, feet NOT planted** (peak bbox y 126–1484, height 1,359 px, 15 px margin).
  ADDITIVE variant. Never call V1 or V4 a walk cycle.
- **Methods 10/10 CPU, 0/10 CUDA:** I1 3DGS core IoU 0.6472; I2 voxel 8 px 0.8778;
  I3 palette-16 0.6472; I4 Floyd–Steinberg 0.6433; I5 Mip filter proxy 0.7671;
  X1 2DGS flatten proxy 0.4137; X2 Scaffold anchors 1,949/5,846, 0.3504;
  X3 4DGS breathing (t=0.25) 0.6089; X4 jitter 0.5498; X5 depth-sigma proxy 0.8979.
  Vendor CUDA (gsplat, splatfacto, Nerfstudio viewer, Blender Gaussian-shader render)
  are MAPPINGS, not runs: no torch / no CUDA GPU on this VM (verified: torch import
  fails). No paid GPU run made. PLY exports for V2/V3/V4 are real files.
- **Viewed by this audit:** `upgrade-contact-fronts-20261031.png` — V1 dotted,
  V2 near-solid, V3 chunky square dots, V4 dotted at front. Matches the numbers above.
  All four turn GIFs re-checked: 9 frames each.
- **Generated vs vector/code-drawn:** all splats are CODE-DRAWN (PIL + numpy + scipy,
  CPU) from the existing apose plate. No generated/AI image is claimed for any splat.
  Base art untouched.

## (2) Invisible presets — kept distinct, do NOT merge

### (a) Invisible Power V1 — animated going-invisible, 17 logical frames
Folder: `invisible-power-v1-nocrop-fix-20261031/` — **audit/report only here; the fixed
version was already built by a separate agent run and is NOT duplicated by this audit.**
- DRAFT vs FIXED split, both preserved: `draft/` holds the old 17-frame version
  (GIF, MP4, contact, 17 draft masters); `frames/f00–f16` hold the FIXED transparent
  masters (704×1296). Motion unchanged (body width 1.0→0.02 f00–f07, outline-only hold
  f08–f11, return f12–f16, 12 fps, hard ring (180,245,255) + soft halo (0,200,255)).
- Fix: 80 px pad BEFORE the outline pass + 40 px margin, so the halo is no longer sliced
  at the trimmed-figure bbox. Fixed hold alpha 131,199 px (was 104,787), halo 27 px above
  head, gate PASS (edge alpha 0 on all 17 masters, min margin 91 px, f00/f16 alpha 337,389).
- **Audit finding (new, not hidden):** the FIXED GIF as stored has **14 frames**, not 17,
  while the FIXED MP4 has **17 frames** (ffprobe) and the masters are 17. The GIF's
  identical hold frames were merged into one 330 ms frame (other frames 80 ms) — a GIF
  optimisation, not a missing motion frame. Quote "17f" for the masters/MP4; quote the
  GIF as "14 stored frames representing 17 logical frames" when the GIF itself is cited.
  Draft GIF, by contrast, stores 17 frames.
- Approval: 0/1 for the FIXED V1. Draft approval (if any) is NOT the fixed approval.
  Per-shot application: 0/30.
- Viewed by this audit: before/after contact — draft f08 shows the flat top cut, fixed
  f08 shows halo above the head. No-crop rule holds on the fixed masters.

### (b) Invisible Line Work — B/W lineart, Silhouette Pack Two TOP ROW
Folder: `drawing-masters-upgrade-20261031/effects/` — 5/5 files, all code-drawn
(OpenCV Canny/Sobel), body fill zero, outline only:
L1 faint 1 px alpha 70 (47,514 line px, 12.71% of silhouette); L2 medium 2 px alpha 120
(125,004 px, 33.44%); L3 visible 3 px alpha 180 (167,388 px, 44.77%);
L-depth line-weight-by-depth 3/2/1 px alpha 140 (118,906 px, 31.81%);
Sobel cross-check alpha 120 (32,952 px, 8.81%; Canny is the keeper, Sobel the check).
Use: INVISIBILITY POWERS — when he goes invisible, use these lineart pieces.
**Audit note on layout:** the source doc maps these as "top row" (5) and silhouettes as
"second row" (3), but the contact sheet itself lays the 8 effects out 4 + 4
(Sobel sits first in row 2 of the sheet). Content is identical (8 files); only the
sheet arrangement differs from the doc's row wording. Do not claim the sheet is 5 + 3.

### (c) Colored Invisible Line Work — a DIFFERENT invisible state, CapeGP mode
Folder: `colored-invisible-line-work-20261031/` — built, approval **0/1**, tool CapeGP
(Blender 5.2.3), NOT any other repo. NOT the B/W linework above, NOT Coloured Shadow,
NOT a black silhouette, NOT a filled render.
- 1 preset as a MODE (default source pose NORMAL/apose), applied to all 6 CapeGP poses:
  6 single-preset blends, 12 variant files (6 transparent + 6 on-black), 19 strokes each.
  Alpha: NORMAL 33,919 px, APOSE_FLEX 34,947, FACE_SNAP 33,010, COWL_SNAP 34,944,
  CHEST_SNAP 34,933, JOINT_SMOOTH 34,384; edge-touch 0/6. No-crop holds.
- Honest colour caveat (from the source report, re-confirmed on viewing): Eevee snap
  colours render MUTED, not saturated — e.g. FACE_SNAP largest warm bucket (192,128,128),
  1,956 px, no strict orange-ish pixel. Layer/material identity in the .blend is exact;
  saturated screen colours are OWED, not claimed. Contact-sheet title overlap noted in
  the source report is a sheet annotation flaw, not a preset flaw.
- Still owed: approval 0/1; T5 new-character dry run (before any other-repo staging);
  GP fills / interior / line-weight; per-shot proofs; landing (separate step).
- Bucket: ADDITIVE extra invisible state. It does not replace the core Invisible Power
  V1 or the B/W linework, and expanding it further is NOT production priority.

## (3) CapeGP presets — layer proofs only, PIL/v7c stays default

Folder: `capegp-presets-20261031/` — approval **0/1**, no repo push, no other-repo staging.
Formal name **CapeGP** everywhere. Blender 5.2.3 LTS, one GP object `CapeGP`, 10 layers
front-to-back: FaceSnapArm > Head > CowlUpperArm > Neck > ChestSnapArm > Torso > Collar >
NormalArm > Legs > CapeBack. Strokes are traced outlines (cv2 largest external contour,
max 140 points) of existing v7c pieces — code-traced, NOT newly drawn art, NOT generated.

| # | Preset | Strokes (re-verified) | Key layer fact |
|---|---|---|---|
| 1 | NORMAL | 19 | NormalArm 6, Legs 6 |
| 2 | APOSE_FLEX | 19 | TRUE_FINAL flex, dip 28 px |
| 3 | FACE_SNAP | 19 | FaceSnapArm 3 (R chain above Head), NormalArm 3 (L) |
| 4 | COWL_SNAP | 19 | **COWL IS UPPER-ONLY:** CowlUpperArm 2 (both uppers), NormalArm 4 (lowers + caps) |
| 5 | CHEST_SNAP | 19 | ChestSnapArm 6 (both chains above Torso) |
| 6 | JOINT_SMOOTH | 19 | Chaikin ×2 on every stroke, same layers as APOSE_FLEX |
| **Total** | **6/6 presets** | **114 strokes** | 6 single-preset blends + 6 proof renders (proofs from single blends, NOT the multi-frame all-presets file, which has GP holdover) |

- Pipeline rule (every CapeGP doc): **PIL/v7c = DEFAULT for clean plates and approved
  poses.** GP = layer proofs only (snap decision seen as a layer stack), Blender-internal
  motion tests, and layer-tree deliverables. No CapeGP render is an approved clean plate.
- No-crop gate: all 6 presets fit the ortho frame with margin; rendered proofs touch no
  canvas edge (per source README; stroke bboxes re-checked via frames JSON structure).
- Still owed: **T5 new-character dry run 0/1 before any other-repo staging or any
  multi-character claim**; GP fills / interior linework / line-weight-by-depth; per-shot
  CapeGP proofs 0/30; long GP sequences (free GPU route).
- Viewed by this audit: `capegp-preset-contact-20261031.png` — outlines only in all six,
  gold uppers in COWL_SNAP, cyan chains in CHEST_SNAP, warm R chain in FACE_SNAP, all
  muted as in the coloured preset (same Eevee behaviour, not a new defect).

## (4) Silhouette Preset Pack Two — second row

Folder: `drawing-masters-upgrade-20261031/` — pack approval **0/1**, named PACK TWO
(not Pack One, per Mars order 2026-10-31 19:55 CDT; it does not overwrite or claim Pack One).
- **Second row = silhouette appearances / silhouette reveal (3/3):** S1 pure black
  (373,846 px = full silhouette); S2 black + cyan rim (180,245,255), 23,907 rim px;
  S3 black + light-grey (200,200,200) interior lineart, 47,514 line px.
- **Top row (for reference in this pack, counted in §2b):** L1/L2/L3/L-depth/Sobel (5/5).
  Pack total: **8/8 effects**.
- Rules preserved: base art untouched; lineart/silhouette are effects, never a recolour
  of the base; Coloured Shadow (dark purple 52,22,90, own-rig silhouette behind him) is a
  SEPARATE mechanic, not this pack. Apose plate only; per-shot/per-pose application owed.
- Viewed by this audit: `effects-lineart-silhouette-contact-20261031.png` — faint→visible
  lineart progression, then pure black, cyan-rimmed black, and lineart-on-black silhouettes.
  All read as the caped figure; no figure is cropped by the sheet.
- Gate in source measurements: 26/26 individual + effect files checked, 0 edge-touch
  failures (auto-fit canvas = alpha bbox + 40 px pad).

## What this audit did NOT do (per task rules)
- Did not duplicate the Invisible Power V1 fixed build (audit/report only).
- Did not build any new preset variant, did not expand V2/V3/V4, Colored, or CapeGP.
- Did not claim any approval, landing, repo push, generated image, clean-plate status,
  walk cycle, true back, true multi-view capture, CUDA run, or Blender shader render.
- Did not touch, move, or delete any pre-existing file. Only this folder is new.

## Verification (this audit, recomputed from disk)
- `verify_workstream_h.py` + `counts-20261031.json` in this folder.
- PLY vertices: V1 5,846; V2 23,391; V3 10,389; V4 5,846 — all match their reports.
- CapeGP strokes: 19 × 6 = 114 — matches.
- Turn GIFs: 9 frames each (V1–V4). Invisible fixed masters 17, draft masters 17,
  fixed GIF 14 stored frames (see §2a finding), fixed MP4 17 frames.
- Pack Two effects: 8 files listed in counts JSON. Colored: 6 blends, 12 variant files.
  CapeGP: 6 single blends, 6 proof renders. Methods: 10 front files.
- V1 byte-identity: front and GIF md5s match the upgrade reproduction exactly (above).

## Blocked / needs Mars (in production-priority order)
1. Approvals for new work: 0/5 packs — nothing here should be presented as approved.
2. Per-shot work (0/30): this is the production gap; apose proofs alone do not make shots.
3. Gaussian production gaps: multi-view capture, Mars-approved FREE GPU CUDA run only,
   Blender Gaussian-shader render, per-pose splats — each 0/1, each needs Mars's call
   (especially the free-GPU route; never a paid run on this audit's say-so).
4. T5 new-character dry run before CapeGP leaves this repo or is called multi-character.
5. Saturated coloured-snap colours (compositor/material tweak) before Colored is quoted
   with saturated screen colours.
