#!/usr/bin/env python3
"""render_looks.py — apply a Cape Jones render look (show lighting preset).

The show's look list lives in docs/lighting/RENDER-LOOKS.md. A look is the
"film" a scene is shot on: it sets Blender's view transform and nothing
else — scene lights, materials and grades are separate layers.

Usage (inside Blender):
  blender -b scene.blend --python production/pipeline/render_looks.py -- list
  blender -b scene.blend --python production/pipeline/render_looks.py -- pale-wash
  OCIO=<repo>/tools/wired/fullstack/aces/cg-config-v2.1.0_aces-v1.3_ocio-v2.1.ocio \
    blender -b scene.blend --python production/pipeline/render_looks.py -- deep-saturation

Exit codes: 0 = look applied (or listed), 2 = look needs a relaunch with
the ACES OCIO config (the exact line is printed), 3 = unknown look name.
The applied look name is stored on the scene as scene["render_look"].
"""

import sys
from pathlib import Path

import bpy

ACES_CONFIG = (
    Path(__file__).resolve().parents[2]
    / "tools/wired/fullstack/aces/cg-config-v2.1.0_aces-v1.3_ocio-v2.1.ocio"
)

LOOKS = {
    "pale-wash": {
        "label": "LOOK 1 - PALE WASH (default)",
        "view_transform": "AgX",
        "needs_aces_config": False,
    },
    "deep-saturation": {
        "label": "LOOK 2 - DEEP SATURATION",
        "view_transform": "ACES 1.0 - SDR Video",
        "needs_aces_config": True,
    },
}


def available_transforms(scene):
    prop = scene.view_settings.bl_rna.properties.get("view_transform")
    if prop and prop.enum_items:
        return [item.name for item in prop.enum_items]
    return []


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    name = argv[0] if argv else "list"
    scene = bpy.context.scene

    if name == "list":
        for key, look in LOOKS.items():
            print(f"[looks] {key}: {look['label']} -> {look['view_transform']}")
        print(f"[looks] current view_transform = {scene.view_settings.view_transform}")
        return 0

    look = LOOKS.get(name)
    if look is None:
        print(f"[looks] unknown look '{name}'. Known: {', '.join(LOOKS)}")
        return 3

    target = look["view_transform"]
    try:
        scene.view_settings.view_transform = target
    except TypeError:
        # The transform is not in this session's OCIO config.
        if look["needs_aces_config"]:
            print(f"[looks] '{target}' is not available in this Blender session.")
            print("[looks] Deep Saturation needs Blender launched with the ACES config:")
            print(
                f"[looks]   OCIO={ACES_CONFIG} blender -b <scene.blend> "
                f"--python production/pipeline/render_looks.py -- {name}"
            )
            return 2
        print(f"[looks] could not set view transform to '{target}' in this session.")
        return 2

    scene["render_look"] = name
    print(f"[looks] applied {look['label']}: view_transform = {scene.view_settings.view_transform}")
    print(f"[looks] scene['render_look'] = '{name}'")
    return 0


sys.exit(main())
