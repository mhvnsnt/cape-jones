# Tahoma2D — Primary 2D Drawing & Timeline Tool

**Pinned version:** 1.6 (latest, verified 2026-10-19 via tahoma2d.readthedocs.io)
**License:** Open source (free, commercial use allowed)
**Upstream:** https://tahoma2d.org/ · https://github.com/tahoma2d/tahoma2d

## What it is

Tahoma2D is an OpenToonz fork repackaged for humans — same Toonz engine that Studio
Ghibli used for decades, with a streamlined UI, more stable drawing tools, and
implicit holds (frames auto-persist, less fiddly timeline work). Raster, smart-raster,
and vector drawing; onion skinning; Fx schematic for effects; stop-motion support.

1.6 highlights relevant to us: brush tips, stylus settings popup, column alpha lock,
loop frames, inbetween-from-timeline, vector inspector.

## Why this tool (pipeline role)

**Primary 2D workhorse for hand-drawn frame-by-frame.** The owner's workflow is
hand-drawing on his phone in FlipaClip — Tahoma2D is the easiest professional-grade
landing spot for that style on desktop. Drawing + timeline live here; heavier node
compositing goes to OpenToonz; vector auto-tweening goes to Synfig.

## Linux install

Download the Linux build from the releases page:
https://github.com/tahoma2d/tahoma2d/releases (pin: v1.6)

```bash
# AppImage (recommended — no install, no root)
chmod +x Tahoma2D-*-Linux.AppImage
./Tahoma2D-*-Linux.AppImage
```

## Pipeline wiring (Cape Jones)

1. **Draw** — keys and breakdowns in Tahoma2D (raster or vector levels).
2. **Time** — Xsheet/timeline with implicit holds; export image sequences (PNG).
3. **Hand off** —
   - Image sequences → RIFE notebook (`production/kaggle/rife/`) for AI inbetweening, OR
   - `.tnz` scenes → OpenToonz for node-based compositing/effects.
4. **Cards/titles** — draw in Tahoma2D, composite in OpenToonz or Blender VSE.

## Notes

- Bundles its own ffmpeg + rhubarb (lip-sync) binaries — matches our existing
  `production/tools/rhubarb-lip-sync/` lane; keep the two in sync on versions.
- Do NOT use as a compositor for heavy multi-pass effects — that's OpenToonz's job.
- Scene files (`.tnz`) are the interchange format with OpenToonz (shared engine).

## License

Open source. Repo integration is legal — document version pin on upgrade.
