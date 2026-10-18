# render-manager — Render Manager (free, GPL), wired

**What:** Render Manager v3.0.11 by Robert Rioux — manages Blender render layers
and render passes the way real VFX studios do (Rioux built it after the
in-house tools at Real by Fake, where he was CG Supervisor). Create/delete/
reorder render layers, control which collections and passes feed each layer,
copy/paste pass sets between layers, then export per-layer 16-bit color +
32-bit data passes (incl. Cryptomatte) plus an overall precomp — ready for
Nuke/DaVinci Resolve. Also converts Z-up to Y-up for Nuke.

**Why for us:** the living room is heading for compositing (god-ray glare pass,
TV-screen pass, LED glow pass, Cryptomatte for the remote/buttons). This is the
industry-standard layer/pass workflow, GPL free. Use it instead of hand-rolled
file-output nodes.

**Verified 2026-10-17 by this lane (real run, Blender 4.5.3 LTS):**
- Clone `riouxr/Render-Manager` @ `e827295` (v3.0.11), vendored to
  `tools/pulled/Render-Manager/` (.git stripped, license kept).
- SPDX: GPL-3.0 (`LICENSE`).
- Installed headless via `bpy.ops.extensions.package_install_files`
  (repo=`user_default`), registered by path — `render_manager.register()` OK.

**Install:**
```bash
# GUI: Blender 4.2+ -> Edit -> Preferences -> Add-ons -> Install from Disk ->
#        tools/pulled/Render-Manager/ -> enable "Render: Render Manager"
# Headless (agents):
BLENDER=<blender-4.5.x> xvfb-run -a env -u PYTHONPATH \
  $BLENDER -b --python tools/render-manager/install_render_manager.py
```

**Location in scene:** Properties > Render > Render Manager panel.
