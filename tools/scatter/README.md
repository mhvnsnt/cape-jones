# scatter — GScatter (free, GPL), wired

**What:** GScatter — Graswald's free geometry-nodes scattering add-on. Scatter any
object on a surface with density/scale/rotation control, effect layers, wind.
Ships with free downloadable assets (12 free assets incl. 1 environment) and
three built-in system presets.

**Why for us:** quick natural detail (rug fibers, shelf clutter, scattered papers)
and any "many small things on a surface" task in the living room — without
hand-placing.

**Verified 2026-10-17 by this lane (real run, Blender 4.5.12 LTS):**
- Source: community fork `romainguerif/gscatter-blender5-fix` — GScatter 0.12.0
  patched for Blender 4.2+/5.x (Python 3.13: cp313 Pillow wheels, attrs 26.1.0
  bump, Random-Value node socket fix). **License: GPL-3.0-or-later** (LICENSE in
  repo, © 2024 Graswald GmbH).
- Registered headless; `bpy.ops.gscatter.scatter(preset='system.default')`
  on a plane + cube → **FINISHED**, created `Pebble : System` with a
  `GScatterGeometryNodes` modifier and the full node network
  (Distribute On Faces, Instance Collection, Camera Culling…) plus the
  GScatter / Sources / Systems collections.
- Deps needed on Blender's python: `jsonschema`, `attrs`, `t3dn_bip`
  (bundled as wheels in the fork; `pip install` into Blender's python works).

## Install

```bash
# 1. get the fork
git clone https://github.com/romainguerif/gscatter-blender5-fix
cd gscatter-blender5-fix
# 2. zip the folder (do NOT unzip before installing) and install:
#    GUI: Edit → Preferences → Add-ons → Install from Disk → gscatter.zip
# 3. headless (see install_gscatter.py): copy to
#    ~/.config/blender/4.5/scripts/addons/gscatter, pip-install the 3 deps
#    into Blender's python, then bpy.ops.preferences.addon_enable(module='gscatter')
```

Needs **Preferences → System → Allow Online Access** for the free-asset list.
The paid Graswald plant library is NOT needed — free assets + our own objects
are the workflow.

## Headless scatter (verified pattern)

```python
bpy.ops.preferences.addon_enable(module='gscatter')
bpy.context.scene.gscatter.scatter_surface = surface_obj
bpy.ops.object.select_all(action='DESELECT')
scattered_obj.select_set(True)
bpy.context.view_layer.objects.active = surface_obj
bpy.ops.gscatter.scatter(preset='system.default')
```
