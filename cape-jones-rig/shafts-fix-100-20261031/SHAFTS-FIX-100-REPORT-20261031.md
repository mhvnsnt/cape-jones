# Shafts — ALL still-not-fixed items fixed, 20261031

Mars ordered 2026-10-31 22:14 CDT: fix everything listed as still not fixed
in the shafts improved preset message, wire 5 industry + 5 experimental
100%, use free GPU routes (Kaggle, Colab, etc.), present it, then land/push/merge.
Landing is NOT done by this task (no repo push by the builder) — the folder
below is push-ready for the parent landing agent, PR-only, 0 deletions,
merge gate, verify size+SHA on main after merge. Do NOT claim landed until
PR + merge SHA + verification arrive. Approval for the fixed set: 0/1
until Mars sees it.

## Folder (new, no existing file overwritten, base art never recoloured)
`~/workspace/cape-jones-rig/shafts-fix-100-20261031/`

## What was still not fixed — and what fixed it

### 1. 5-column separation — FIXED, measured
- Old: v2 3 runs, v3 3 runs centre merged, v3b 3 runs outer shoulders only.
- New design (NOT another spot-energy tweak): 5 SEPARATE volume boxes,
  one per column, gaps between them are empty air, 1 spot per column,
  no shared volume, no sun, no large ceiling slats.
- Cycles on this design still failed honestly: v4 and v4b peaked at only
  2 columns (x~440/650, centre-volume edges) and v4b's sun flooded the
  floor (uniform ~109). Both Cycles renders are preserved in this folder
  as evidence, NOT claimed as the master.
- Eevee on the SAME separate-volume scene succeeded: full-res 1100x1500,
  `shafts-eevee-v4-fullres-20261031.png`, mid-height rows 500-700,
  percentile gate (p90 peak 104.5, p10 valley 25.1, threshold 64.8):
  **5 runs: [58,212], [267,418], [474,622], [679,832], [887,1041]**,
  widths ~154-165px, gaps ~45-55px. Main gate `gate-main-20261031.json`
  exit 0 PASS.
- The 5 runs survive the method passes: I5 denoise, X1 gradient, X5
  edge-softened all still measure 5 runs (see methods-measurements).

### 2. Ceiling slats dominating the top — FIXED by removal
- v3/v3b had large black slat blocks at the top. The v4 design has NO
  large slats at all (only a thin trim in the Cycles attempts; the Eevee
  master has no slat blocks). Gate: top-300 max single-row near-black
  fraction = **0.0** — no row is a black block. Dark gaps between columns
  remain, which is correct for shafts, not slat blocks.

### 3. Eevee render 0 files — FIXED, file exists
- Previous attempts (shared volume, full-res, tile 2) timed out at
  180s/280s under xvfb. The v4 Eevee scene (separate volumes, tile 8,
  TAA samples 1) rendered LOCALLY under xvfb in ~10 seconds, half-res
  AND full-res. No Kaggle/Colab sign-in was needed for this master.
- Free-GPU wiring is still delivered: `shafts-eevee-free-gpu.ipynb`
  (Kaggle first, Mars FMMG fmmg.mars@gmail.com ONLY — if Kaggle rejects
  that login, STOP and report, do NOT try another account; Colab free
  GPU second; free only, no paid run). Cloudflare and Backblaze are
  storage/CDN, NOT GPU compute — stated plainly, NOT used as GPU here.
- If a future GPU sequence needs a Mars sign-in, the exact step is:
  open that notebook in Kaggle/Colab and sign in as fmmg.mars@gmail.com.
  That step was NOT needed for this master and was NOT invented.

### 4. True in-scene ground pools — FIXED, in the render
- The v4 scene has a real Blender floor plane at z=-1.5 receiving the
  5 spots. In the Eevee master the pools are the bright floor band at
  y1400-1500 (mean >110, column centres 111-115) with 5 overlapping
  spot ellipses — rendered by Blender, not drawn ellipses.
- Framing note, not hidden: pools sit at the MASTER floor (canvas
  bottom). Per-shot composites carry that master floor at canvas
  bottom; figure feet are NOT on that floor line in per-shot composites
  (figure plate feet sit mid-canvas). Ground-matching pools to each
  figure's feet is a separate framing step, not claimed here.

### 5. Per-shot shafts 0/30 — FIXED, 30/30
- `per-shot/` + `per-shot-table-20261031.json`: 30/30 built, gate-pass
  30/30. Each shot uses its own transparent plate + the v4 Eevee master,
  shafts tinted toward the shot's rim colour at 25% mix (shafts only,
  figure NEVER recoloured), intensity L3=1.0 / L2=0.85, shafts masked by
  (1-plate_alpha), plate pasted on top. Occlusion diff at alpha==255:
  0.0 on all 30; figure inside canvas 30/30; shaft runs 5/5 each.
  Earlier 2.3-3.5 diffs were anti-aliased edge pixels (alpha 251-254
  counted as opaque); the gate was corrected to alpha==255 exactly.
- Honest label: the Blender master is ONE v4 render; per-shot work is a
  measured composite application per shot, not 30 separate Blender
  volumetric renders.

### 6. Fresh numeric no-crop/occlusion gate on every new composite — RUN
- `gate_shafts.py` run on the main composite: exit 0 PASS (see §1, §2,
  §4, occlusion 0.0). Per-shot gate 30/30 (see §5). Main composites are
  filled-background, so the transparent-plate edge-alpha-0 test does
  NOT apply to them; the no-clip test for them is figure bbox inside
  canvas + occlusion 0.0, both measured. No gate PASS is quoted that
  was not run.

### 7. 5 industry + 5 experimental — ALL RUN, in methods/
- I1 Cycles separate-volume render — RUN (v4/v4b, preserved, honest
  outcome above; Eevee is the master, Cycles is evidence, not hidden).
- I2 Eevee volumetric render — RUN, full-res file exists (see §3),
  plus free-GPU notebook wired.
- I3 True in-scene ground pools — RUN, floor plane in the v4 scene
  (see §4).
- I4 Blender Glare Fog Glow — RUN, 5.2 API method (inputs dict, not
  attributes; File Output gives EXR, converted via save_render):
  `methods/I4-glare-v4.exr` (26 MB) + `methods/I4-glare-v4.png` (3.6 MB),
  Fog Glow, Quality High, Threshold 0.6, Strength 0.5, Size 6. Glare
  tile in final-contact is the Glare layer alone, not a figure composite.
- I5 Faster/cleaner — RUN, Cycles denoising ON in v4/v4b + timed logs
  (v4 ~16 min, v4b ~9.5 min, Eevee ~10 s) + PIL sigma-1 denoise proxy,
  5 runs unchanged.
- X1 Depth gradient, X2 Flicker sweep (one frame, NOT a sequence),
  X3 Dust streaks (120, seed 7), X4 Caustic pools overlay (noise dapple
  ON TOP of the in-scene pools, labelled as the overlay part),
  X5 Edge softened — all RUN as PIL composites on the Eevee master,
  in `methods/`, contact `methods-contact-20261031.png`.
- No method is left mapping-only without a blocker: AE CC Light Rays
  and Natron Sun Beams from the old upgrade remain PROXY/mapping in
  the old folder and are NOT re-claimed here; the 10 methods above are
  all run files in this folder.

### 8. Improved preset approval 0/1 — presented, still 0/1
- This fixed set is presented for Mars's approval. Nothing here is
  claimed approved until he sees it. The old Environmental preset
  approval (1/1 as preset, not production-ready) stands separately.

## Viewed before reporting
- Eevee half-res and full-res shafts, main composite (figure in front,
  5 columns, pools at floor), final contact, per-shot contact grid.
- Final contact tiles: V4 Eevee shafts only, V4 Eevee + figure, V4
  Glare layer, CJ-01..CJ-04 shafts samples. Per-shot contact: all 30.

## Files
- `shafts-eevee-v4-fullres-20261031.png` (master, 1.6 MB)
- `shafts-eevee-v4-20261031.png` (half-res)
- `shafts-only-cycles-v4-separate-20261031.png`, `shafts-only-cycles-v4b-separate-20261031.png` (evidence, not master)
- `composite-shafts-v4-figure-20261031.png` (main composite)
- `final-contact-20261031.png`, `per-shot-contact-20261031.png`, `methods-contact-20261031.png`
- `per-shot/` (30 PNGs), `per-shot-table-20261031.json`
- `methods/` (I4 Glare EXR+PNG, I5, X1-X5), `methods-measurements-20261031.json`
- `gate_shafts.py`, `gate-main-20261031.json`, `build_cycles_v4_separate.py`,
  `build_cycles_v4b_separate.py`, `build_eevee_v4.py`, `build_eevee_v4_fullres.py`,
  `build_glare_v4.py`, `build_methods.py`, `build_per_shot.py`, `build_contacts.py`,
  `shafts-eevee-free-gpu.ipynb`, `SHAFTS-FIX-100-PRESET-20261031.json`
- No existing file overwritten, no base art recoloured, shafts always
  behind figure (masked by 1-figure_alpha, figure pasted on top).
