# OpenToonz — Node-Based Compositing & Effects

**Pinned version:** 1.8.0 (latest stable, released 2026-06-19, verified 2026-10-19)
**License:** Modified BSD (open source, free incl. commercial)
**Upstream:** https://opentoonz.github.io/ · https://github.com/opentoonz/opentoonz

## What it is

The open-sourced Toonz — the software Studio Ghibli customized and used for decades.
Full production pipeline in one app: scanning, cleanup, raster+vector drawing, and
its killer feature vs simpler tools: a **node-based compositing schematic** (the
Schematic/Fx room). Effects, multiplane camera, particles, Python scripting.

Shares its engine with Tahoma2D — `.tnz` scenes move between the two.

## Why this tool (pipeline role)

**Compositing and effects stage.** Drawing happens in Tahoma2D (friendlier);
when a shot needs layered effects, glows, multiplane moves, or complex composites,
it comes here for the node schematic. This is the closest free equivalent to
Toon Boom Harmony's compositing.

Do NOT use for: primary drawing (Tahoma2D is friendlier), vector auto-tweening
(Synfig's job), final video assembly (Blender VSE / ffmpeg).

## Linux install

Upstream ships no Linux binary — use the community Flatpak (1.8.0, x86_64):

```bash
flatpak install flathub io.github.OpenToonz
flatpak run io.github.OpenToonz
```

Alternatives: Morevna AppImage (based on older 1.4.0 — avoid unless Flatpak fails),
or build from source at the v1.8.0 tag (`cmake ../sources -DWITH_TRANSLATION=OFF`
if the translation build fails on newer Qt).

Install ffmpeg separately — OpenToonz needs it for video export.

## Node-compositing workflow (Cape Jones)

1. **Import** — PNG sequences from Tahoma2D/Synfig/RIFE, or `.tnz` scenes directly.
2. **Schematic** — build the node graph: levels → effects (glow, blur, color)
   → composite → camera (multiplane/pan/zoom).
3. **Preview** — flipbook the schematic output; iterate on effect nodes.
4. **Render** — output PNG sequence or MOV; hand to Blender VSE / ffmpeg for
   final assembly with audio.

## Pipeline handoffs

- IN: Tahoma2D (`.tnz` / PNG seq), Synfig (PNG seq), RIFE (interpolated PNG seq)
- OUT: composited PNG seq / video → `production/pipeline/FLIPACLIP-POST-PIPELINE.md`
  (grades, bloom, audio master) → final MP4.

## License

Modified BSD. Repo integration is legal — document version pin on upgrade.
