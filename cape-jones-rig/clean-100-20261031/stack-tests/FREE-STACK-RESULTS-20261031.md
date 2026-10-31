# Free-stack tests — Workstream G, 2026-10-31

Rule applied: a tool counts as tested ONLY when a real operation ran and an output
file exists in this folder. A version string alone is not a test. Web-only tools
are pending-browser, never claimed as tested. No push, no delete, no commit in
this batch. All inputs are our own v7c clean rig pieces (no proprietary
character/logo/asset copied).

## Count

- Tools in scope: 9 (Blender, FFmpeg, PIL/Python, Tahoma2D/OpenToonz family,
  Krita, Pencil2D, Synfig, Wick Editor, Cavalry, Brinimate — see note below).
  Counted as full import+operation+export tests: **5/9**
  (Blender, FFmpeg, PIL, Krita, Synfig).
- Partial (real run, export owed): **2/9** (Tahoma2D, Pencil2D).
- Pending-browser (web-only, out of subagent scope): **2/9** (Wick Editor, Brinimate).
- Not installed / no local route: Cavalry (see below). OpenToonz itself is not
  installed separately; Tahoma2D is its fork and is the tested representative.
  So the honest roll-up is: full 5, partial 2, pending-browser 2, missing 1
  (Cavalry) — against the 9 named tools in the task (OpenToonz/Tahoma2D counted
  as one family slot, Blender/FFmpeg/PIL counted inside the free stack).

## Versions (verified this batch)

- Blender 5.2.3 LTS (build 2026-10-22), `~/workspace/tools-industry/blender-5.2.3-linux-x64/blender`
- FFmpeg 8.1.2
- Python PIL 10.2.0
- Krita 1:5.2.2+dfsg-2build8 (dpkg ii, `/usr/bin/krita`)
- Pencil2D 0.6.6 (dpkg ii, `/usr/bin/pencil2d`)
- Synfig 1.5.1 (`synfig` CLI; `synfigstudio` also installed)
- Tahoma2D v1.6.3 (tarball `~/workspace/tools-industry/Tahoma2D-linux-clang-1.6.3.tar.gz`,
  extracted to `~/workspace/tools-industry/tahoma2d-1.6.3/`; direct AppImage run
  FAILS: no fusermount / no FUSE device — `--appimage-extract` workaround used)
- Cavalry: NOT installed — no binary, no apt package; download route is a
  browser/GUI task, pending for parent.
- OpenToonz: NOT installed separately.

## Full tests (output file in this folder, operation named)

1. Blender 5.2.3 — import rig-apose-v7c-clean-transparent.png, compositor
   Image node -> group output, headless render.
   Output: blender-compositor-apose-20261031.png, 887,145 bytes, 1100x1100 RGBA,
   VIEWED (character intact). Caveats, honestly: scene resolution was 1100x1100
   vs source plate 1100x1500, so the render is a square compositor render, not
   a full-height plate; Blender 5.2 API differs from older scripts —
   `scene.compositing_node_group` (not `scene.node_tree`), and
   `CompositorNodeComposite` is UNDEFINED in 5.2 (group-output pattern used,
   same as blender-compositor-stack.py). Script: blender_stack_test.py.
2. FFmpeg 8.1.2 — (a) `lut3d` with showcase/lut-neutral.cube on the clean apose.
   Output: ffmpeg-lut-neutral-apose-20261031.png, 495,895 bytes, VIEWED.
   (b) 24-frame beat encode from showcase/free-stack-tests/frames-24.
   Output: ffmpeg-24f-beat-20261031.mp4, 24 frames @ 24/1 fps verified by ffprobe
   (`nb_read_frames=24`).
3. PIL 10.2.0 — original Arm_Front_Lower vs OutFixed side-by-side composite.
   Output: pil-outfixed-vs-original-20261031.png, 47,543 bytes.
   Per-row alpha-span check: 289/289 rows identical — the OutFixed rule holds.
   Gauntlet regression check_gauntlet_flip.py re-run: 5/5 PASS.
4. Krita 5.2.2 — open rig-apose-v7c-clean-transparent.png under Xvfb, export.
   Output: krita-apose-export-20261031.png, 515,000+ bytes, exists.
   (Import + export round-trip; no paint stroke was applied — a paint operation
   in Krita is still owed if a stroke-level test is required.)
5. Synfig 1.5.1 — render prior .sif tween
   (showcase/free-stack-tests/synfig-cape-jones-tween-20261031.sif) at frame 12.
   Output: synfig-tween-frame12-20261031.png, 3,300+ bytes, `DONE` from synfig CLI.
   Note: this renders the prior .sif (a circle tween over grey-128), NOT a Cape
   Jones character tween — a character-piece Synfig rig is still owed.

## Partial tests (run, export owed — NOT counted as full)

6. Tahoma2D 1.6.3 — `-version` prints "Tahoma2D v1.6.3", `-help` usage prints,
   process alive under Xvfb, BUT the GUI screenshot is 295 bytes black/blank —
   window did NOT paint in 15s, so GUI is NOT counted as viewed.
   Project folder built here: tahoma-cape-jones-24f/inputs/ (24 frames copied)
   + xsheet-beat-grid-20261031.json (24 cells, beat markers 1,7,13,19).
   Owed: open the level in the Tahoma GUI and render — needs a GUI session.
7. Pencil2D 0.6.6 — GUI launches under Xvfb and the screenshot IS viewed:
   pencil2d-gui-launch-20261031.png shows the full UI (Bitmap/Vector/Camera
   layers, timeline). BUT no Cape Jones .pclx import/export was achieved: no
   sample project on disk, and a hand-crafted .pclx format was not verified in
   this batch. Owed: a real .pclx built in the GUI, then `pencil2d -o` export.
   Script: gui_launch_probe.sh.

## Pending-browser (report to parent, do not claim)

- Wick Editor: web-only, no local install. Needs a live-browser task.
- Brinimate: web-only, no local install. Needs a live-browser task.

## Correction to an earlier assumption in this batch

An early glob (`/usr/bin/*krita*` etc.) appeared to show Krita/Pencil2D/Synfig
absent; `dpkg -l` proves they are installed (ii) and their binaries exist.
They were tested above, not reported missing.

## Files in this folder

run_free_stack_tests.py, blender_stack_test.py, gui_launch_probe.sh,
free-stack-results.json (machine log), plus the output PNG/MP4 files above,
tahoma-cape-jones-24f/, verify_repo_readonly.py, repo-verification.json,
repo-main-tree.json, COMPARISON-RESULTS-20261031.md, REPO-MANIFEST-20261031.md.
