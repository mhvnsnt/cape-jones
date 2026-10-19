# Natron 2.5.0 — headless compositing for the show pipeline (wiring doc)

**Upstream:** https://github.com/NatronGitHub/Natron (5.5k stars, active 2026)
**License:** GPL-2.0 — free, commercial USE as a tool is OK. We do not vendor or
redistribute Natron's source or binaries; only our own helper scripts live here.
**Why:** owner's standing order — "pull in a real compositing tool, not the
cheapest manual path" (the 45-second playback failure). Pipeline docs name Natron
as the comp step ("Krita → Natron → finish.py") — this run made that REAL:
Natron was previously *claimed* installed (EXPANSION-3.md line 49) but no binary
existed on this VM. As of 2026-10-19 it is genuinely installed and headless-render
verified.

## Install (this VM — persistent, NOT in the repo)

- Path: `~/workspace/tools/natron/Natron-2.5.0-Linux-x86_64-no-installer/`
  (official Linux no-installer tarball from NatronGitHub/Natron release v2.5.0)
- Wrapper: `~/workspace/tools/natron/natron-render.sh` — sets the bundled
  `LD_LIBRARY_PATH` and execs `NatronRenderer`. Usage: `natron-render.sh --help`
- The wrapper keeps two fetched-from-Ubuntu-noble libs local:
  `libGLU.so.1.3.1`, `libOpenGL.so.0.0.0` (apt is broken on this VM; fetched via
  curl + dpkg-deb, never committed). Nothing else system-wide was touched.

## Verified working (own-eyes, 2026-10-19)

- `NatronRenderer --version` → `Natron version 2.5 at commit 53ee17e... on branch tags/v2.5.0`
- Headless script execution: `NatronRenderer make_project.py` (Constant node →
  Write node → PNG) ran to "Rendering finished" and produced a byte-valid PNG.
- The output frame was viewed own-eyes: exactly the magenta color set in the
  script (1.0, 0.2, 0.8) — pipeline is real, not claimed.
- Gotchas found the hard way:
  - `NatronRenderer -t script.py` DROPS INTO AN INTERACTIVE INTERPRETER (hangs).
    Use positional script form instead: `NatronRenderer script.py < /dev/null`.
  - `ColorParam.set()` needs 4 args (RGBA): `set(1.0, 0.2, 0.8, 1.0)`.
  - First-run plugin scan takes ~40s; subsequent runs are fast.
  - OpenGL rendering is disabled headless (no display) — CPU path works fine.

## Headless lane runbook

1. Write a Python script that builds the node graph:
   ```python
   app = NatronEngine.natron.getInstance(0)
   reader = app.createNode("fr.inria.built-in.Read")
   reader.getParam("filename").set("/path/to/frames.%04d.png")
   write = app.createNode("fr.inria.built-in.Write")
   write.connectInput(0, reader)
   write.getParam("filename").set("/path/to/out.mp4")
   ```
2. Run it: `natron-render.sh /tmp/comp_script.py < /dev/null`
3. Or render a saved project: `natron-render.sh project.ntp [1,50]`
4. Smoke test first: `python3` this dir's `natron_smoke_test.py` (runs the
   verified magenta-frame test into /tmp; exits non-zero on any failure).

## Cape Jones uses

- **Comp the show pipeline:** Blender scene frames (walkthrough, EP01 shots) →
  Natron grade/light-wrap/glow → final mp4. Replaces the hand-rolled ffmpeg-only
  comp pass for anything needing real node-graph compositing.
- **The 45-second playback failure:** re-composite suspect segments through
  Natron's Write (ffmpeg-backed) to produce known-good encodes; Natron is the
  verification-grade renderer when ffmpeg CLI output is in doubt.
- Pairs with: `finish.py` grade presets, `soda` (Blender→Natron project
  generator, documented in EXPANSION-3.md), comp_glow.py presets.

## Limits

- Natron binary + libs stay on disk only (NO-LOCAL-CLUTTER: ~700MB extracted;
  the tar.xz is kept for reinstall). If a GPU/cloud lane needs it, the download
  URL + wrapper are documented here — fetch, don't re-upload.
- GUI mode works under `xvfb-run -a` but is not the lane path; headless only.
