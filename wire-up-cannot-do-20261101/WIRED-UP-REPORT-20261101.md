# WIRE UP THE 'CANNOT DO' LIST — 2026-11-01
Mars 2026-11-01 12:53 CST: stop listing limits, make them work.
Standing rule applied: work properly first time, check before showing, no
cannot-do list as a deliverable, only an external blocker plainly with the
path ready. Approval 0/1 each. Repo landing local only, no PR claimed.

## 1. 48-frame animation in reasonable time — WIRED, via the 2D rig path
Delivered full 48-frame clip, not 3 stills:
- cjtoon-48f-final-20261101.mp4 — 550x750, 24fps, 48 frames, 2.000s,
  h264 + AAC (synthesised blips at 0.0 / 0.85 / 1.33s, test audio only,
  not a final mix, not show audio)
- Frames: renders/pil48/frame_001.png … frame_048.png, 1100x1500 source
- Pose table: renders/pil48/pose-table.json (48 frames, snap flag per frame)
- Builder: build_fast_clip.py (own code, Cape Jones pieces only)

Timeline: f1-8 rest, f9-20 arms out, f21-32 arms crossed-down (snap ON,
whole arm chain above torso, below head), f33-48 arms-up flex.
Render time, measured: 92.19s total for 48 frames, 1.92s/frame on this run;
an earlier optimised run was 75.79s, 1.58s/frame. The first unoptimised run
was 223.69s, 4.66s/frame — the optimisation was caching piece loads and
rotating a small joint layer instead of a full 1100x1500 canvas per limb.
Blender EEVEE, measured for comparison, is NOT the fast path on this VM:
1-sample EEVEE, 550x375, software GL, rendered frames 1-23 only, then the
run stopped, at ~27s/frame (frame 1 at 00:47, frame 23 at 10:50 in the log).
Extrapolated 48 frames ≈ 21 minutes. That is why the delivered 48-frame
clip is the 2D rig render, not an EEVEE render — the EEVEE numbers are
reported, not hidden, and the EEVEE frames that did render are in
renders/blender_fast/frame_0001.png … frame_0023.png (23/48, incomplete,
not a deliverable clip). No paid GPU run was used; no Kaggle/Colab run was
needed because the 2D rig path already renders 48 frames in ~90 seconds.

## 2. True arms-up flex with whole pieces — WIRED, via the joint cut
Method: NOT a square crop, NOT a wrist cut, NOT a separate hand placed
on top. The original rig's own standard joint cut (cut-limbs-v7):
upper and lower arm pieces split at the elbow ball centre
(Arm_Back (99,222) R30, Arm_Front (60,222) R30, measured from the art),
lower piece pivots on the ball, circle-masked elbow cap covers the seam.
That is the same cut the v7 rig already used — it is not a new cut
invented for this task, and the wrist is never cut: the lower piece is
forearm + gauntlet + fist as one piece, following the forearm peg.
Final flex (renders/arms-up-flex-final-20261101.png, also frame_048):
- Upper L -120, R +120 → spread 120deg, inside the 100-160deg obtuse gate
- Lower L -160, R +160 → forearm up-out, fist above the elbow
- Elbows: L (272,354), R (828,354); fists at the top corners, fingers up,
  fist orientation follows the lower piece rotation, no separate hand,
  no flip, no upside-down broken fist
- Flex test variants A-E are also in renders/ for comparison; B
  (upper120/lower160) is the final, A/C/D/E are superseded tests, not finals.
Crossed frame check (frame_032, eye-checked): upper at sides, forearms
horizontal across the torso, above the torso, not eaten by it. Two earlier
crossed attempts were wrong and are not hidden: (a) upper arms crossing
diagonally gave a tangled X with elbows at the centre; (b) lower signs
reversed sent the forearms off-canvas outward. The final signs were
verified by frame check: L lower +90 = east, R lower -90 = west in PIL.

## 3. .tpl / .plt export — OWN PROTOTYPE BUILT, Harmony import UNVERIFIED
Research, public docs only, no Toon Boom code copied:
- docs.toonboom.com, Harmony 24 Advanced, 'About the File Structure':
  a template is a mini-scene folder; drawings and palettes are separate
  linked files, not embedded; scene folders contain elements/,
  palette-library/, frames/, timings/, etc.
- Harmony 21 Advanced, Palette Operations: palettes are individual *.plt
  files stored in palette-library.
- .xstage is an XML scene file (FileInfo / Toon Boom Help Centre).
What the prototype exports today (exporter/export_cjtoon_tpl_plt.py):
- CapeJonesToon.tpl, 447,577 bytes, zip of a mini-scene folder
- CapeJonesToon.xstage (XML: 1100x1500, 24fps, 48 frames, 17 pegs, 10 elements)
- elements/<layer>/drawing-1.png for 10 layers (CapeBack, LegBack, LegFront,
  ArmBack, Pelvis, Torso, CapeCollar, Neck, Head, ArmFront)
- palette-library/CapeJones.plt (12 colours, sampled from the actual PNGs)
  + CapeJones.plt.json (same 12 colours, machine-readable)
- PALETTE_LIST, scene.elementTable, README-PROTOTYPE.txt
Validator (exporter/validate_tpl.py): exit 0, self-consistent true,
16 files, 0 missing drawings, 48 timing frames, 12 palette lines = 12 JSON.
What it does NOT do, plainly, and what needs a real Harmony binary:
- It does NOT write .tvg vector drawings. Drawings are bitmap PNGs
  (Harmony's bitmap import path). Vector .tvg export is not claimed.
- The .plt file is a plain-text prototype format (header
  # CJTOON-PLT-PROTOTYPE-1). Toon Boom does not publish a .plt binary
  spec in its public docs, so Harmony reading this exact .plt file is
  UNVERIFIED. A first palette version mislabelled colours by order
  (white labelled purple); that was fixed by using generic Colour01-12
  names with the real RGB values, not by inventing semantic names.
- Harmony opening, rendering, or importing this .tpl is UNVERIFIED until
  a real Harmony binary opens it. That test is the first thing to run
  when the trial licence lands. No licence was bypassed, no binary was
  used, no Toon Boom code was copied.

## 4. In-Harmony rendering / activation — PATH READY, BLOCKER IS EXTERNAL
No bypass, no crack, no pirated binary, no card entry, no purchase.
Ready, syntax-checked (bash -n, all pass):
- ~/workspace/toon-boom-linux-20261101/install-harmony-rocky-chroot.sh
- ~/workspace/toon-boom-linux-20261101/install-harmony-rocky-chroot-v2.sh
- ~/workspace/toon-boom-linux-20261101/watch-for-harmony.sh
  (watches for a Linux .tgz, verifies gzip + >100MB, logs sha256, runs
  the v2 installer; it never downloads from third-party/crack sites)
Launch steps, minute a licence shows (see LAUNCH-READY-20261101.md):
1. Trial licence appears on shop.toonboom.com (fmmg.mars@gmail.com only)
2. Download Linux .tgz only (HAR27-PRM-lnx-25340.tgz), verify on disc
3. Run install-harmony-rocky-chroot-v2.sh <tgz> → tar -xvzf → ./install
   → choose STANDALONE (not Server/Client)
4. License Wizard: /usr/local/ToonBoomAnimation/harmony[Edition]_27/lnx86_64/bin/LicenseWizard
   as fmmg.mars@gmail.com, then launch in Rocky 9 chroot via host Xvfb
Blocker, plainly: NO Linux .tgz is on disc today (find for *lnx* / *harmony*.tgz
returned nothing, 2026-11-01), and the last parent browser check
(2026-11-01 11:57 CST) showed no subscription, no licence, no order for
fmmg, about 18 minutes after the 11:39 trial submission. As a subagent I
cannot operate the live browser, so I cannot recheck the shop myself —
the parent must recheck, and the scripts above run the minute a licence
shows. Harmony is NOT claimed to work until a Harmony binary launches.
Knee-feet rule used in this build: universal, Mars 2026-11-01 12:07 CST —
knees direction == toes direction, per frame, both legs, anatomy first.
The old 11:30 bundle leg1-only note does not carry forward as a default.
Legs in this clip are straight, toes as drawn, no turn claimed.

## Files
- WIRED-UP-REPORT-20261101.md (this file)
- LAUNCH-READY-20261101.md
- renders/cjtoon-48f-final-20261101.mp4
- renders/arms-up-flex-final-20261101.png
- renders/pil48/ (48 frames + pose-table.json)
- renders/blender_fast/ (23 EEVEE frames, incomplete, measurement only)
- build_fast_clip.py, flex_test.py, build_blender_fast.py
- exporter/export_cjtoon_tpl_plt.py, exporter/validate_tpl.py,
  exporter/CapeJonesToon.tpl, exporter/CapeJonesToon-scene/
Still owed: Mars approval 0/1 each (clip, flex, exporter, Harmony path);
Harmony import test (needs real binary); repo landing (local only, no PR).
