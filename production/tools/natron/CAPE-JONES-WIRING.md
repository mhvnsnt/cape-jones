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

## Finishing comp template: `natron_comp_finish.py` (2026-10-19)

The first real comp built on the headless Natron install — the "Krita -> Natron ->
finish.py" pipeline step is now an actual runnable script, not just a doc line.

**Graph:** `Read(beauty) -> Grade -> Saturation -> DenoiseSharpen(sharpen only)
-> Merge(over, bg) -> Write`

**Usage:**
```bash
NATRON_BEAUTY=/path/beauty.png NATRON_BG=/path/bg.png NATRON_OUT=/path/final.png \
    ~/workspace/tools/natron/natron-render.sh production/tools/natron/natron_comp_finish.py < /dev/null
```
Env knobs: `NATRON_BEAUTY` (required), `NATRON_BG` (optional; skipped = comp on
black), `NATRON_OUT` (required), `NATRON_MULTIPLY` (grade gain, linear),
`NATRON_GAMMA`, `NATRON_SATURATION`, `NATRON_SHARPEN` (all optional, sane
defaults). Self-test: `python3 natron_comp_finish.py --selftest` (needs PIL,
runs the full headless comp on synthetic plates, pixel-verified, exit 0/1).

**Hard-won facts (verified by render, not docs):**
- Natron Merge: **input 0 = B (background), input 1 = A (foreground)**. Swapping
  silently drops the foreground (verified by two rendered probes).
- `createNode` returns `None` on bad plugin IDs (no exception) — always assert.
- Choice params take **script names** (`"project"`, `"over"`), not display labels
  (`"To Project Format"` silently breaks the node).
- Still PNGs report frame range 0-0: normalize each Read to 1-1 AND pin the
  project `frameRange` to (1,1), or NatronRenderer renders 0-250 onto one file.
- Reformat's "project" mode misbehaves headless (black output) — dropped from
  the chain; inputs must share the project format (true for render passes) and
  Write conforms the output to it.
- Misc bundle has no standalone Sharpen node: `net.sf.openfx.DenoiseSharpen`
  with `denoiseAmount=0` sharpens only.
- CLI args do NOT reach Natron scripts (`NatronRenderer script.py arg` fails);
  params travel via env vars, and the script detects the Natron interpreter via
  `import NatronEngine` so the same file runs as driver + build script.

**Verified (own-eyes, 2026-10-19):** synthetic red-disc-over-blue comp rendered
correct over, pixel math checked (red disc / blue bg / black surround), no-BG
path renders, 0.5 grade gain maps to correct linear->sRGB (188). Output frame
viewed and confirmed.
