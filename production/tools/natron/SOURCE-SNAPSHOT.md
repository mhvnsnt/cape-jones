> Landed 2026-10-24 with the vendored Natron source snapshot (land/natron-20261023, from pull/natron-20261023). This was the pull lane's wiring doc for the in-repo source tree. The live headless-runbook wiring doc remains CAPE-JONES-WIRING.md (kept from main).

# Natron — CAPE JONES WIRING

**Pulled:** 2026-10-23 (overnight-idle-pipeline) · upstream `github.com/NatronGitHub/Natron`, branch RB-2.6 @ 3763d805d7d2 (pushed 2026-07-24, ~5.6k★)
**License:** GPL-2.0 ✅ (own-eyes: LICENSE.txt in pulled tree = GNU General Public License Version 2, June 1991; gh API license field = gpl-2.0) — free + commercial OK as a tool.
**Size:** 78MB code-only (4822 files, depth-1 snapshot; upstream `.github/` CI stripped per convention). 0 binaries >50MB. No prebuilt .so/.dll.

## What it is
A free, open-source (GPLv2) **node-based video compositor** — in upstream's own words, "similar in functionality to Adobe After Effects, Foundry's Nuke, or Blackmagic Fusion." Cross-platform (GNU/Linux, macOS, Windows), Qt-based GUI, Python scripting API, and a headless renderer (`NatronRenderer`) for batch/compose-farm renders.

## Slot map (video pipeline)
| Tool | Slot |
|------|------|
| ffmpeg | single-clip encode/transcode |
| Flowblade + MLT/melt | interactive NLE + headless timeline renders |
| Glaxnimate | vector motion graphics (titles/lower-thirds as clips) |
| **Natron** | **compositing: keying, rotoscoping, tracking, color, FX, title compositing** |

Natron is the compositing layer UNDER/OVER the NLE chain: episode scenes that need more than a timeline — greenscreen/keying, motion tracking, plate cleanup, multi-layer FX, AI-matte compositing — get a Natron project (`.ntp`), rendered headless with `NatronRenderer`, and the rendered composite goes back onto the Flowblade timeline as a clip.

## Setup
- **Use (binary):** distro package or upstream release tarball — no build needed for production use. A no-installer Natron 2.5.0 Linux binary lives at `~/workspace/tools/natron/` (includes `NatronRenderer` for headless renders). Headless render verified working on this VM 2026-10-23 (own-eyes: `--help` reports the three background execution modes — `.ntp` projects, Python scripts, interpreter); needs the bundled GL libs on the loader path:
  ```bash
  cd ~/workspace/tools/natron
  LD_LIBRARY_PATH=$PWD:$PWD/Natron-2.5.0-Linux-x86_64-no-installer/lib \
    ./Natron-2.5.0-Linux-x86_64-no-installer/bin/NatronRenderer shot.ntp -f 1 100
  ```
  (alternatively `~/workspace/tools/natron/natron-render.sh`, which wraps the same call).
- **Source build (dev):** needs submodules initialized first:
  ```bash
  git clone https://github.com/NatronGitHub/Natron.git && cd Natron
  git submodule update --init --recursive   # libs/OpenFX, libs/SequenceParsing, libs/google-breakpad, Tests/gtest
  # CMake build; Qt4/Qt5 (not yet Qt6), C++98 base moving to C++11/14
  ```
  Depth-1 snapshot in this repo does NOT include submodule contents — re-clone upstream for a build tree.

## Usage
```bash
# Interactive compositing session
/path/to/Natron

# Headless render of a compositing project (the farm path)
NatronRenderer /path/to/shot.ntp -f 1 100 -w Writer1
```

## Show-pipeline uses
1. **Title/composite shots** — lower-thirds and motion-graphic plates from Glaxnimate get keyed/tracked/composited in Natron rather than baked in the NLE.
2. **AI-matte compositing** — roto/AI matting passes (per NO-CHROMA-KEY-ON-ANIMATION: AI matting or rotoscoping only) composite onto plates here, not in-editor.
3. **Keying & plate cleanup** — greenscreen/keying, wire/object removal, set-extension composites for Wizard Gang / Cape Jones episode VFX shots.
4. **Natron → melt chain** — `NatronRenderer` headless renders feed composited shots into the Flowblade/melt episode assembly as final-quality clips.

## Notes
- GUI is Qt-based (Qt4/Qt5); the VM value is `NatronRenderer` headless renders + Python scripting (projects are scriptable `.ntp` node graphs).
- Upstream is looking for maintainers (per README "Help wanted") — flag for watch, not a blocker.
- Weights/binaries: none (native app, no ML weights).
- Upstream CI (`.github/`, 52K) stripped from this snapshot per pull convention; documentation GIFs kept (36MB, part of user docs).
