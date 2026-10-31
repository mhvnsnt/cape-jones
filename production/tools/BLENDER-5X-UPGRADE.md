# Blender 5.2.3 LTS — Production Default (Wired 2026-10-31)

**Status:** Wired into the pipeline as the production Blender.
**Previous:** 4.0.2 (kept as fallback at `~/workspace/tools/blender/blender-4.0.2-linux-x64/`)
**Current:** **Blender 5.2.3 LTS** (released 2026-10-22, supported until July 2028)
**License:** GNU GPL (open source, free — no reverse engineering needed)
**Download:** Official portable Linux archive from https://download.blender.org/release/Blender5.2/blender-5.2.3-linux-x64.tar.xz (~367 MB)

## Why this is the 100% version

- Latest LTS with 2 years of support.
- Full Grease Pencil overhaul (fills, SVG, Geometry Nodes driven 2D).
- Faster compositor, animation playback, and shape-key evaluation.
- CloudRig and modern add-ons work cleanly.
- No paid tier, no account, no watermark.

## Install (portable, no root)

```bash
# On the machine that runs the pipeline
mkdir -p ~/workspace/tools/blender
cd ~/workspace/tools/blender
curl -L -o blender-5.2.3-linux-x64.tar.xz \
  https://download.blender.org/release/Blender5.2/blender-5.2.3-linux-x64.tar.xz
tar -xJf blender-5.2.3-linux-x64.tar.xz
# Resulting binary:
# ~/workspace/tools/blender/blender-5.2.3-linux-x64/blender
```

## Headless recipe (re-proven for 5.x)

```bash
xvfb-run -a env -u PYTHONPATH \
  ~/workspace/tools/blender/blender-5.2.3-linux-x64/blender \
  -b --python-expr "import bpy; print(bpy.app.version_string)"
```

## Pipeline role

Blender 5.2.3 LTS is now the default for:
- Grease Pencil 2D/3D hybrid shots
- Node compositor (bloom/glow passes)
- VSE final assembly
- Geometry Nodes procedural 2D
- All existing CloudRig / BlenRig / Wiggle 2 / ML autorig workflows

4.0.2 remains available as fallback until the owner signs off on full switch.

## Verification

- Download confirmed working (official blender.org release).
- License: pure GPL, no reverse engineering required.
- Docs and pipeline references updated to 5.2.3 LTS.
