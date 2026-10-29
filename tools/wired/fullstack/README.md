# Full-stack wiring — USD, Alembic, OpenTimelineIO, MaterialX, OpenColorIO/ACES
Wired 2026-10-28 (user: "Do all that 100%"). All tests ran on COPIES, never on the locked sit/guard files. Locked files verified untouched (sit 2026-10-28 21:18:51, guard 2026-10-28 21:21:11).

## 1. USD (Pixar, Apache) — Blender native
- Wiring: Blender 4.2 `wm.usd_export` with `export_animation=True`, scene frame range drives the export (no start/end params in 4.2 — first attempt failed on that, fixed by setting scene frames).
- Proof: `guard_test.usda` (94 KB, ASCII) from a guard-rig copy, frames 30-32, contains CapeJones_Rig prim.
- Use: export sit/guard/room as separate USD layers so changing one cannot change another. USD layers are the format-level fix for "guard changes sit".

## 2. Alembic (BSD) — Blender native
- Wiring: Blender 4.2 `wm.alembic_export` with `start`/`end` and `selected=False` (first attempt failed on `selected_objects_only`, which Alembic does not accept — fixed).
- Proof: `guard_test.abc` (9.4 KB), round-trip import into a clean session returns CapeJones_Rig + meshes.
- Honest limit: Alembic is a baked MESH cache, not a rig transfer. For sit/guard, Alembic caches the deformed body mesh (large for 910k verts) — the rig-only test proves the exporter + round-trip, a full body-cache test is still owed before Alembic replaces rig renders.

## 3. OpenTimelineIO (Pixar/Netflix, Apache)
- Wiring: venv at `fullstack/.venv` (pip install opentimelineio; system pip is PEP 668-blocked, venv is the clean path — do NOT commit `.venv`).
- File: `ep01_immortal_qombat.otio` (24 fps) — Scene 1 (45s), Scene 2 (45s), Scene 3 (20s), Scene 4 (50s), Scene 5 (40s), Scene 6 (160s), Tag (10s), read back exactly.
- Honest limit: Scene 6 end and Tag length are ESTIMATES (script says Scene 6 "3:20-end" and runtime ≥6 min; 200-360s + 10s tag = 6:10 total). Flagged TBD in the script — update the .otio when the final runtime locks.

## 4. MaterialX (Lucasfilm/Academy, Apache)
- Wiring: same venv (pip install MaterialX).
- File: `cape_jones_materials.mtlx` — standard_surface materials: cape_suit_white (0.92,0.92,0.92), cape_black (0.05,0.05,0.06), cape_cowl_violet (0.45,0.11,0.90), read back exactly.
- Honest limit: cowl violet is a STARTING value from the proof image, not a canon hex claim. Owner tunes it.

## 5. OpenColorIO / ACES (Academy, BSD)
- Wiring: `aces/cg-config-v2.1.0_aces-v1.3_ocio-v2.1.ocio` (ACES 1.3, OCIO 2.1, AcademySoftwareFoundation release) + venv pip install OpenColorIO + numpy.
- Proof: config loads (colour spaces include ACEScg, ACEScc, ACEScct, ACES2065-1); processor ACEScg → sRGB-Display converts [0.5,0.2,0.1] → [0.865,0.4392,0.3085]; Blender started with `OCIO=<config>` switches view_transform to "ACES 1.0 - SDR Video".
- Honest limit: the Scene 1 preview already rendering used Blender's DEFAULT colour (it started before ACES wiring). ACES applies to the NEXT renders, not retroactively to the running Scene 1 — re-rendering Scene 1 in ACES is a separate owner decision, not done silently.

## Sit-scene counterparts (2026-10-29) — the guard proofs above, run on the sit scene

Source for both tests: `scene_anim_placed3.blend` (release `sitcanon-anim-placed-20261020`, sha256 `21e1c67a…`). All tests ran on a copy; the locked files were not touched.

- **USD:** `sit_test.usda` (3,416,003 bytes, ASCII) — rig + cape + set, 118 objects, frames 30–32 (`startTimeCode` 30 / `endTimeCode` 32), contains the `CapeJones_Rig` prim. The 910k-vert body mesh is excluded — same rig-level scope as `guard_test.usda`. The world texture rides along at `textures/color_121212.hdr` (the `.usda` references `./textures/…`).
- **Alembic full body-cache test (the owed item from §2):** exported the FULL scene, body included, frames 30–32 → `sit_body_test.abc`, **291,199,101 bytes** — too big for git, stored on release `fullstack-sit-tests-20261029`. Round-trip into a clean session returns `CapeJones_Body` at exactly **910,374 verts**, bbox x[2.623, 3.210] y[1.712, 2.495] z[0.009, 0.759] — the seated figure, matching the source. Verdict: exporter + round-trip are now PROVEN for the full body. But at ~97 MB per frame the cache is an interchange format, not a storage path (the full 81-frame sit would run ~7.9 GB). USD layers remain the working split; Alembic is the per-shot bake-out when something needs it.
