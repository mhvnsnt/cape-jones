#!/usr/bin/env python3
"""
apply_furniture_position.py — set the living room TV/shelf layout.

Owner directive 2026-10-18 ~10:10 CDT. Two saved layouts (see
furniture_positions.json):
  position_1 = backs against the wall (DEFAULT)
  position_2 = TV and shelf facing the chair (walkthrough video layout)

RUN INSIDE BLENDER with the living room scene open:
    blender -b 3d-assets/living_room.blend \
        --python 3d-assets/living-room/apply_furniture_position.py \
        -- position_1

Or import and call apply_position("position_1") from another script.

The chair (loungeChairRelax) is NEVER touched — canon placement locked.
This script never saves the blend.
"""

import bpy
import json
import os
import sys
from mathutils import Vector

WALLBACK_FACE_Y = 2.925  # WallBack at y=3.0, 0.15 thick

def _positions_path():
    blend_path = bpy.data.filepath
    repo_assets = os.path.dirname(os.path.abspath(blend_path))
    return os.path.join(repo_assets, "living-room", "furniture_positions.json")

def _assembly_max_y(yaw_obj):
    """Max world Y over the yaw empty and all its children (meshes)."""
    deps = bpy.context.evaluated_depsgraph_get()
    max_y = float("-inf")
    stack = [yaw_obj]
    seen = set()
    while stack:
        o = stack.pop()
        if o.name in seen:
            continue
        seen.add(o.name)
        stack.extend(o.children)
        if o.type == "MESH" and len(o.data.vertices) > 0:
            ev = o.evaluated_get(deps)
            me = ev.to_mesh()
            try:
                for v in me.vertices:
                    w = ev.matrix_world @ v.co
                    if w.y > max_y:
                        max_y = w.y
            finally:
                ev.to_mesh_clear()
    return max_y

def apply_position(name):
    with open(_positions_path()) as f:
        data = json.load(f)
    if name not in data["positions"]:
        raise ValueError(f"unknown position '{name}'. valid: {list(data['positions'])}")
    pos = data["positions"][name]
    print(f"applying furniture {name}: {pos['name']}")

    # ---- TV console (the yaw empty parents the whole TV assembly)
    yaw = bpy.data.objects.get("TVConsole_Yaw")
    if yaw is None:
        raise RuntimeError("TVConsole_Yaw not found in scene")
    cfg = pos["TVConsole_Yaw"]
    yaw.rotation_euler = cfg["rotation_euler"]
    loc = list(cfg["location"])
    if loc[1] == "AUTO_BACK_TO_WALL":
        bpy.context.view_layer.update()
        max_y = _assembly_max_y(yaw)
        loc[1] = WALLBACK_FACE_Y - (max_y - yaw.location.y)
        print(f"  TVConsole_Yaw back-to-wall: assembly max_y={max_y:.3f} -> yaw y={loc[1]:.3f}")
    yaw.location = loc
    bpy.context.view_layer.update()

    # ---- bookcase / shelf
    shelf = bpy.data.objects.get("bookcaseClosed(Clone)")
    if shelf is None:
        raise RuntimeError("bookcaseClosed(Clone) not found in scene")
    cfg = pos["bookcaseClosed(Clone)"]
    shelf.rotation_euler = cfg["rotation_euler"]
    loc = list(cfg["location"])
    if loc[1] == "AUTO_BACK_TO_WALL":
        # bookcase is 0.25 deep in Y at rot 0; back (+Y side) flush to wall face
        loc[1] = WALLBACK_FACE_Y - 0.125
        print(f"  bookcase back-to-wall: y={loc[1]:.3f}")
    shelf.location = loc
    bpy.context.view_layer.update()

    print(f"furniture {name} applied "
          f"(TV yaw={tuple(round(v,3) for v in yaw.location)}, "
          f"shelf={tuple(round(v,3) for v in shelf.location)})")

if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    apply_position(argv[0] if argv else "position_1")
