# Backgrounds + Blender / ACES log — 2026-10-31 (workstream report)

## 1. Final painted backgrounds — 4/4 built and viewed (with quality caveat)
New variants, 1168x784, in ~/workspace/cape-jones-rig/showcase/backgrounds-new-20261031/:
- bg-flying-new-20261031.jpg — sky, sun, cloud blobs, distant peaks, bird silhouettes. Viewed. Simple sky plate, usable.
- bg-rooftop-new-20261031.jpg — dusk skyline, lit windows, water tower, antenna, rooftop ledge foreground. Viewed. Strongest of the four.
- bg-alley-new-20261031.jpg (v2) — night alley, lit windows, pipes, bins, puddles, mist. Viewed. Readable, flat vector-style.
- bg-desk-new-20261031.jpg (v2) — room with desk foreground, window view (hills/sea), lamp glow, shelf books, papers, mug. Viewed. Readable, flat vector-style.
Original art only: no show character art, names, dialogue, or logos. Existing batch-*.jpg backgrounds in cape-jones-flying were NOT modified (read-only source).
CAVEAT (honest): these are procedurally painted PIL variants, not hand-painted masters at the detail level of the existing batch backgrounds (e.g. batch-KKGuh room, batch-RjoBx forest). They are layout/background plates for review. Still owed if Mars wants that level: a hand-painted-detail pass (artist / Blender / GPU run — GPU needs Mars's approval for a specific run).

## 2. Blender volumetric god-ray test — PENDING render (see below)
Blender 5.2.3 LTS (NOT 4.5.3), CPU only (local VM has no GPU).
Dual-light spec from RIM-COLOR-RULE.md / UNIVERSE-COLOR-LANGUAGE.md: warm gold key front (255,180,80) + cyan back god rays (0,200,255).
Scene: clean plate rig-apose-v7c-clean-transparent.png on a plane, backdrop plane, volume cube (Principled Volume, density 0.045, anisotropy 0.3), warm gold spot front, cyan spot behind, dim cool fill. Blend file + render in showcase/ (names below, filled in once render lands).

## 3. ACES — PENDING render result (see below)
Blender 5.2.3 view_transform enum verified by direct set: 'ACES 1.3' and 'ACES 2.0' are valid (plain 'ACES' is NOT — enum error). Test render uses view_transform 'ACES 1.3' in Blender's OCIO colour management, not flat PIL. Result logged once the frame is viewed.

## 2. (final) Blender volumetric god-ray test — VIEWED, partial pass
- Render 1 (20:36 UTC): character tiny + dark, spots mis-aimed (manual rotations, no tracking). REJECTED on viewing, not shipped.
- Render 2 (20:42 UTC): tracked spots, stronger lights, density 0.02. Character full/centred/lit; cyan volumetric cone visible top-left. Warm front beam not distinct. Viewed.
- Render 3 (20:50 UTC, FINAL FILE): warm spot moved to side-front (6,4,3), cyan back (-2,4,-4), both tracked to character. Viewed: cyan beam still visible top-left; character lit; warm tint on right side, but NO distinct warm-gold beam cone. Cause: warm light sits outside the 10-unit volume cube (x=6 > 5) and its angle is wide, so its beam is diffuse, not a cone.
- FINAL FILE: showcase/blender-godray-aces-test-20261031.png, 1168x784, sha256 e722007352740bc46c83efa41634d47bc6e3d220e0afcd064cfc8c0384877121 (render 3). Blend: blender-godray-aces-test-20261031.blend. Script: /tmp/blender_godray3.py (session scratch, not persisted — blend file is the reproducible scene).
- VERDICT: Blender render viewed = 1/1. Volumetric cyan back god-ray = proven. Full dual-light ray setup = NOT proven: warm front beam as a distinct cone is still owed (needs a dedicated warm beam pass — light inside the volume, narrower angle — on a real shot).

## 3. (final) ACES — 1/1 tested in Blender/OCIO
- Blender 5.2.3 view_transform enum, verified by direct set: 'ACES 1.3' SET OK, 'ACES 2.0' SET OK, plain 'ACES' FAILS (enum error, not a valid value). Blender's bundled OCIO config contains ACES 1.3 / ACES 2.0 views.
- Test render above was rendered with view_transform 'ACES 1.3' (logged in render output: VIEW_TRANSFORM: ACES 1.3), in Blender's OCIO colour management — not flat PIL. ACES = 1/1 for the test.
- Still owed: an AgX-vs-ACES side-by-side on the same shot, and ACES on a real production shot (not a test plate).
