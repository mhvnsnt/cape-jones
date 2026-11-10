# MLT Multimedia Framework — CAPE JONES WIRING

**Pulled:** 2026-10-23 (overnight-idle-pipeline) · upstream `github.com/mltframework/mlt`, master (pushed 2026-10-22, ~1.9k★)
**License:** LGPL-2.1 ✅ (own-eyes: COPYING in pulled tree = GNU Lesser General Public License v2.1) — free + commercial OK.
**Size:** 14MB code-only. Upstream CI (`.github/`) stripped per repo convention. 0 binaries >50MB.

## What it is
The open-source **multimedia authoring/rendering engine** behind Shotcut, Kdenlive, and Flowblade. The critical piece for us is **`melt`** — a headless CLI that renders MLT XML timelines (EDLs) to video. That means episode assembly becomes *code*: a lane writes an XML timeline (clips, cuts, transitions, titles, audio mix) and `melt` renders it with zero GUI.

## Slot map (video pipeline)
| Tool | Slot |
|------|------|
| ffmpeg | single-clip encode/transcode |
| **MLT / melt** | **multi-track timeline assembly + headless render** |
| Flowblade | interactive NLE editing (writes MLT XML melt can render) |
| Glaxnimate | vector motion graphics (titles/lower-thirds) |

## Setup
- **Use (binary):** `apt install melt` / distro package — no build needed for production use. `melt` renders the XML timelines lanes generate.
- **Source build (dev):** `cmake --preset cc-debug && cmake --build build/cc-debug` then `source setenv` (per upstream AGENTS.md in-tree; default install prefix `$HOME/opt`).
- **Python binding:** `swig/python` in-tree — drive timelines from Python instead of hand-writing XML.

## Usage
```bash
# Render a timeline (MLT XML) to a finished episode file
melt episode01.mlt -consumer avformat:episode01_final.mp4 vcodec=libx264 acodec=aac

# Quick assembly: 3 clips with a dissolve, no GUI
melt clip1.mp4 clip2.mp4 clip3.mp4 -mix 25 -mixer luma -consumer avformat:out.mp4

# Titles: burn a PNG lower-third over 5 seconds at 24fps
melt main.mp4 -track lowerthird.png ttl=120 -mix 120 -mixer luma -consumer avformat:out.mp4
```

## Show-pipeline uses
1. **Headless episode assembly** — lanes that cut episodes (Wizard Gang, Cape Jones) emit MLT XML instead of driving a GUI; `melt` renders on any box (VM today, Kaggle tomorrow).
2. **Flowblade round-trip** — Flowblade edits save as MLT XML; a human can rough-cut in Flowblade and a lane can re-render/re-version it headlessly via melt.
3. **Batch socials** — one timeline template → melt renders per-episode/per-platform variants (16:9, 9:16, 1:1) by swapping the consumer profile.
4. **QC renders** — deterministic, scriptable renders for the proof pipeline (no "export settings were different" drift).

## Notes
- Native C/C++ engine — no ML weights, no binaries in-tree.
- `demo/`, `docs/` kept; they are the fastest way to learn the XML schema.
- Do NOT vendor a built `melt` binary into the repo — install from distro or build on the target box.
