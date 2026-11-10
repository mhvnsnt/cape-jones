# Glaxnimate — CAPE JONES WIRING

**Pulled:** 2026-10-23 (overnight-idle-pipeline) · upstream `invent.kde.org/graphics/glaxnimate`, master @ ef01e17a
**License:** GPL-3.0-or-later ✅ (own-eyes: COPYING in pulled tree = GNU GPL v3, "or any later version") — free + commercial OK.
**Size:** 19MB code-only. Upstream CI (`.gitlab-ci.yml`, `.github/workflows`) stripped per repo convention. 0 binaries >50MB. 7/7 Python plugins py_compile clean.

## What it is
Free, open-source, cross-platform 2D **vector animation / motion-design** desktop app (KDE project since 2026; 0.6.0 stable released 2026-03-03). The After-Effects-for-simple-things slot of the pipeline: tweening, precompositions, path animation, gradients/Bézier/image tracing/masking/text, Python scripting API.

## Slot map (2D ladder — now complete)
| Tool | Slot |
|------|------|
| Krita (AppImage) | frame-by-frame raster drawing |
| Tahoma2D / OpenToonz / Synfig / Pencil2D | character / cutout / tweened 2D animation |
| coa_tools2 / smart2d / tiny-2d-rig / guided-tweening | Blender 2D rigging addons |
| AnimeInbet / ToonCrafter / RIFE | cartoon inbetweening + interpolation |
| **Glaxnimate** | **vector motion graphics: titles, lower-thirds, end-cards, Lottie/animated SVG for web + shorts** |

## Setup
- **Use:** download the AppImage from glaxnimate.org (GNU/Linux) — no build needed for production use.
- **Source build (dev):** `mkdir build && cd build && cmake .. && make` (Qt6/KDE stack; see `docs/` in-tree).
- **Headless / pipeline scripting:** `pip install glaxnimate` (PyPI) exposes the document model — create, keyframe, and export animations from Python without the GUI.

## Usage
```bash
# GUI
./Glaxnimate-*.AppImage
# Programmatic (PyPI package): build a title card, export animated SVG
python3 - <<'EOF'
import glaxnimate
with glaxnimate.environment.Headless():
    doc = glaxnimate.model.Document("")
    layer = doc.main.add_shape("Layer")
    text = layer.add_shape("Text")
    text.text.value = "WIZARD GANG"
    text.position.set_keyframe(0, glaxnimate.utils.Point(100, 100))
    text.position.set_keyframe(90, glaxnimate.utils.Point(400, 100))
    with open("title.svg", "wb") as f:
        f.write(glaxnimate.io.registry.from_extension("svg").save(doc))
EOF
```

## Show-pipeline uses
1. **Episode title cards / lower-thirds** — vector titles stay crisp at any zoom, tiny file sizes vs rendered video.
2. **Web/shorts motion graphics** — export Lottie (top-500-app standard), animated SVG, GIF/WebP for socials (Facebook/YouTube/TikTok end-cards).
3. **Integration** — Glaxnimate is the animation engine behind Shotcut and Kdenlive vector tracks; pairs with our Natron/Kdenlive composite step.
4. **Batch generation** — PyPI API scripts living titles/lower-thirds for whole episode runs.

## Notes
- Not a character-animation tool — Tahoma2D/Synfig/coa_tools2 own that lane. Glaxnimate owns motion graphics.
- `external/` + `lib-example/` vendored deps kept (they're build inputs, not binaries).
- Weights/binaries: none (native app, no ML weights).
