# Flowblade — CAPE JONES WIRING

**Pulled:** 2026-10-23 (overnight-idle-pipeline) · upstream `github.com/jliljebl/flowblade`, master (pushed 2026-10-20, ~3.1k★)
**License:** GPL-3.0 ✅ (own-eyes: LICENSE in pulled tree = GNU General Public License v3) — free + commercial OK.
**Size:** 50MB pure-Python source. No upstream CI to strip. 0 binaries >50MB. Python files py_compile clean (sampled).

## What it is
A full **non-linear video editor** for Linux — multitrack timeline, compositors, keyframed filters, titling, audio mixing, proxy editing, batch render queue. Pure Python + GTK3 on top of the MLT engine (pulled alongside at `production/tools/mlt/`). The interactive counterpart to headless `melt`: cut in Flowblade, render anywhere.

## Slot map (video pipeline)
| Tool | Slot |
|------|------|
| ffmpeg | single-clip encode/transcode |
| **Flowblade** | **interactive NLE: rough cuts, fine edits, effects, audio** |
| MLT / melt | headless render of Flowblade's MLT-XML timelines |
| Glaxnimate | vector motion graphics (titles/lower-thirds imported as clips) |

## Setup
- **Use (binary):** distro package or upstream release tarball — no build needed for production use.
- **Source run (dev):** `cd flowblade-trunk && ./flowblade` (needs Python3, GTK3, MLT with python bindings; see README.md in-tree).
- **Round-trip:** Flowblade saves projects as MLT XML → hand the `.mlt` to `melt` for headless/farm renders.

## Usage
```bash
# Interactive edit
cd production/tools/flowblade/flowblade-trunk && ./flowblade

# Headless render of a Flowblade project (uses the MLT slot)
melt /path/to/project.mlt -consumer avformat:final.mp4 vcodec=libx264 acodec=aac
```

## Show-pipeline uses
1. **Episode rough cuts** — the human (or a lane driving the project XML) assembles Wizard Gang / Cape Jones episodes on a real multitrack timeline instead of ffmpeg concat chains.
2. **Flowblade → melt farm** — edit once on a workstation, render headlessly on the VM/Kaggle via melt with identical output.
3. **Batch queue** — Flowblade's render queue + melt covers the whole episode run without babysitting exports.
4. **Titles integration** — Glaxnimate exports (animated SVG/Lottie/PNG sequences) drop onto Flowblade tracks as clips.

## Notes
- Linux-only GUI (GTK3) — the VM value is the project-XML format + headless melt renders; interactive editing happens on a Linux workstation.
- Pure Python: lanes can read/generate Flowblade project files programmatically (they're MLT XML).
- Weights/binaries: none (native app, no ML weights).
