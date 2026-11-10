"""Deterministic Blender layout applier.

Layout coords: x in [0, room.width_m], z in [0, room.depth_m]; z=0 is the
front (camera) wall, z=depth_m is the back wall. Blender mapping:
    obj.location.x = item["x"] - width_m / 2
    obj.location.y = item["z"] - depth_m / 2

Moves ONLY the named furniture objects to the validated JSON layout transforms.
Touches nothing else: no material/color edits, no geometry changes, no scene
settings. Safe to re-run: idempotent for the same layout JSON.

Usage (headless):
    xvfb-run -a env -u PYTHONPATH <blender> -b 3d-assets/living_room.blend \
        --python tools/layout-rules/apply_layout_blend.py -- <layout.json> [--preview-out /tmp/previews/]

Object matching: layout item "name" matches the START of the Blender object
name (so "loveseat" matches "loungeChairRelax(Clone)"). Match by exact name
first, then prefix. Unmatched items are reported, never guessed.
"""
import bpy
import json
import math
import os
import sys

argv = sys.argv[sys.argv.index("--") + 1:]
layout_path = argv[0]
preview_out = argv[1] if len(argv) > 1 and argv[1] == "--preview-out" \
    else None
preview_dir = argv[argv.index("--preview-out") + 1] if "--preview-out" in argv else None

layout = json.load(open(layout_path))
room = layout.get("room", {"width_m": 7.0, "depth_m": 6.0})
W, D = room["width_m"], room["depth_m"]


def find_object(name):
    if name in bpy.data.objects:
        return bpy.data.objects[name]
    cands = [o for o in bpy.data.objects if o.name.startswith(name)]
    return cands[0] if cands else None


moved, missing = [], []
for item in layout["items"]:
    obj = find_object(item["name"])
    if obj is None:
        missing.append(item["name"])
        continue
    obj.location.x = item["x"] - W / 2.0
    # Blender Y is depth: layout z=0 (front wall) -> y=-D/2, z=D (back wall) -> y=+D/2
    obj.location.y = item["z"] - D / 2.0
    obj.rotation_euler[2] = math.radians(item.get("rot_deg", 0))
    moved.append(obj.name)

print(f"MOVED {len(moved)}: {moved}")
if missing:
    print(f"MISSING {len(missing)} (left untouched): {missing}")

if preview_dir:
    os.makedirs(preview_dir, exist_ok=True)
    sc = bpy.context.scene
    sc.render.resolution_percentage = 40
    cams = [o for o in bpy.data.objects if o.type == "CAMERA"]
    for i, cam in enumerate(cams[:3]):
        sc.camera = cam
        sc.render.filepath = os.path.join(preview_dir, f"preview_cam{i}.png")
        bpy.ops.render.render(write_still=True)
        print("rendered", sc.render.filepath)
