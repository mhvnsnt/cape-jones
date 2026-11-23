#!/usr/bin/env python3
"""Dump per-frame 2D transforms for the Rig Jones 2 (V3) rig, WITHOUT
rendering. Blender does all the bone math; PIL rasterises (pil_render_v3.py).
- Plane parts (P_* except P_Cape): centre in rig units, size, in-plane
  rotation (deg), z-order, hide flag, texture path — same schema as the
  V2 transforms.json.
- Cape (P_Cape): the deformed mesh grid. COLS x ROWS cells; for each frame
  the (x, y) rig-space position of every grid vertex (evaluated depsgraph,
  armature modifier applied). pil_render_v3.py warps the cape texture
  through those vertices — one continuous deforming piece.
- Slots: applied with the cj_swap_addon headless API (cj_set_slot), so
  the dump and the interactive add-on agree on what "swap" means.
  Image-swap slots (handR/handL/mouth) record the active image per
  frame as rec["tex"]; visibility slots (eyes/remote/forearms) record
  hide flags as before.
- Cameras per frame.
Usage: blender -b v3-swap-system/purple-lot-v3-rig.blend --python \
         v3-swap-system/dump_v3.py -- v3-swap-system/v3_keys.json \
         v3-swap-system/v3_transforms.json
"""
import bpy
import json
import math
import sys

sys.path.insert(0, "/home/hatch/workspace/_cape-jones-parking-lot-2d/v3-swap-system")
import cj_swap_addon

argv = sys.argv[sys.argv.index("--") + 1:]
keys_path, out_path = argv[0], argv[1]
spec = json.load(open(keys_path))

REST = {"pelvis": 90, "torso": 90, "neck": 90, "head": 90,
        "upperArmR": -90, "forearmR": -90, "handR": -90,
        "upperArmL": -90, "forearmL": -90, "handL": -90,
        "thighR": -90, "shinR": -90, "thighL": -90, "shinL": -90,
        "capeNeck": -90, "capeMid": -90, "capeTip": -90}

scene = bpy.context.scene
arm = bpy.data.objects["CJ_Rig_V3"]
cam = bpy.data.objects["Cam"]
cape = bpy.data.objects["P_Cape"]

SLOTS = json.loads(arm["cj_slots"])
HAND_NAMES = ["Fist", "FistBack", "Open", "Point", "Point2", "Relaxed", "Grip"]
MOUTH_NAMES = ["Closed", "Open", "Shout", "Smile", "Teeth"]
# Image-swap slots: ONE plane per slot; the per-frame record carries
# "tex" (the active image filename). Visibility slots carry no tex.
IMAGE_SLOTS = {s: spec_["object"] for s, spec_ in SLOTS.items()
               if spec_["variants"] and "image" in spec_["variants"][0]}


def slot_index(slot, variant):
    if slot in ("handR", "handL"):
        return HAND_NAMES.index(variant)
    if slot == "mouth":
        return MOUTH_NAMES.index(variant)
    if slot == "eyes":
        return 1 if variant == "Pupils" else 0
    return 0


def at(frame, field):
    val = spec["keys"][0][field]
    for k in spec["keys"]:
        if k["frame"] <= frame:
            val = k[field]
        else:
            break
    return val


# Insert keys.
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")
for rec in spec["keys"]:
    f = rec["frame"]
    for name, target in rec["bones"].items():
        pb = arm.pose.bones[name]
        pb.rotation_euler = (0, 0, math.radians(target - REST[name]))
        pb.keyframe_insert(data_path="rotation_euler", frame=f)
    pb = arm.pose.bones["pelvis"]
    pb.location = (rec["root"][0], rec["root"][1], 0)
    pb.keyframe_insert(data_path="location", frame=f)
bpy.ops.object.mode_set(mode="OBJECT")

for f in range(1, spec["frames"] + 1):
    c = at(f, "camera")
    cam.data.ortho_scale = c["ortho"]
    cam.location = (c["x"], c["y"], 20)
    cam.data.keyframe_insert(data_path="ortho_scale", frame=f)
    cam.keyframe_insert(data_path="location", frame=f)
    sl = at(f, "slots")
    for slot in SLOTS:
        if slot == "remote":
            idx = 0 if sl["remote"] else -1
            if idx >= 0:
                cj_swap_addon.cj_set_slot(arm, slot, idx, set_viewport=False)
            else:
                for v in SLOTS[slot]["variants"]:
                    for obname in v["objects"]:
                        ob = bpy.data.objects.get(obname)
                        if ob:
                            # hide_render ONLY: hide_viewport would exclude
                            # the object from the depsgraph and break the
                            # hide_render F-Curve evaluation on frame_set.
                            ob.hide_render = True
            arm[f"cj_active_{slot}"] = idx
        else:
            cj_swap_addon.cj_set_slot(arm, slot, slot_index(slot, sl[slot]),
                                      set_viewport=False)
    for slot in SLOTS:
        for v in SLOTS[slot]["variants"]:
            # Image-swap slots have NO objects (one plane, image changes)
            # — only keyframe hide_render for visibility-slot objects.
            for obname in v.get("objects", []):
                ob = bpy.data.objects.get(obname)
                if ob:
                    ob.keyframe_insert(data_path="hide_render", frame=f)

parts = [ob for ob in bpy.data.objects
         if ob.type == "MESH" and ob.name.startswith("P_") and ob.name != "P_Cape"]
print("plane parts:", len(parts))

out = {"frames": spec["frames"], "keys": spec["keys"],
       "parts": [], "cameras": [], "cape": None}
for f in range(1, spec["frames"] + 1):
    c = at(f, "camera")
    out["cameras"].append({"frame": f, "ortho": c["ortho"], "x": c["x"], "y": c["y"]})

for ob in parts:
    w, h = ob.dimensions.x, ob.dimensions.y
    rec = {"name": ob.name, "z": round(ob.location.z, 4), "w": w, "h": h,
           "image": None, "frames": []}
    for m in ob.data.materials:
        for n in m.node_tree.nodes:
            if n.type == "TEX_IMAGE" and n.image:
                rec["image"] = n.image.filepath
    out["parts"].append(rec)

import mathutils
# Cape grid: assign (col, row) from REST vertex positions. NOTE: the mesh
# data is OBJECT-LOCAL (transform_apply ran with location=False): x in
# [-W/2, W/2], y in [-H/2, H/2], top edge y=+H/2. Row 0 = top.
CAPE_W, CAPE_H, CAPE_TOP = 4.655, 7.9135, 10.9
COLS, ROWS = 6, 12
rest_verts = [(v.co.x, v.co.y) for v in cape.data.vertices]
grid_index = {}
for i, (x, y) in enumerate(rest_verts):
    c = int(round((x + CAPE_W / 2) / CAPE_W * COLS))
    r = int(round((CAPE_H / 2 - y) / CAPE_H * ROWS))
    grid_index[i] = (c, r)
cape_rec = {"cols": COLS, "rows": ROWS, "w": CAPE_W, "h": CAPE_H,
            "top": CAPE_TOP, "image": "//art/Cape_Back_Main.png", "frames": []}
out["cape"] = cape_rec

for f in range(1, spec["frames"] + 1):
    scene.frame_set(f)
    # Active texture per image-swap plane this frame (from the slot
    # schedule — the same schedule cj_set_slot applied above).
    sl = at(f, "slots")
    tex_of = {}
    for slot, obname in IMAGE_SLOTS.items():
        idx = slot_index(slot, sl[slot])
        tex_of[obname] = SLOTS[slot]["variants"][idx]["image"]
    for ob, rec in zip(parts, out["parts"]):
        mw = ob.matrix_world
        loc = mw.translation
        x_axis = mw.to_quaternion() @ mathutils.Vector((1, 0, 0))
        ang = math.degrees(math.atan2(x_axis.y, x_axis.x))
        frec = {
            "f": f, "x": round(loc.x, 4), "y": round(loc.y, 4),
            "rot": round(ang, 3), "hide": bool(ob.hide_render),
        }
        if ob.name in tex_of:
            frec["tex"] = tex_of[ob.name]
        rec["frames"].append(frec)
    # Cape deformed vertices (evaluated depsgraph, armature applied).
    # to_mesh() vertices are OBJECT-LOCAL: transform by the cape object's
    # matrix_world to get rig coords.
    deps = bpy.context.evaluated_depsgraph_get()
    ev = cape.evaluated_get(deps)
    me = ev.to_mesh()
    mw = cape.matrix_world
    verts = {}
    for i, v in enumerate(me.vertices):
        c, r = grid_index[i]
        w = mw @ v.co
        verts[f"{c},{r}"] = [round(w.x, 4), round(w.y, 4)]
    ev.to_mesh_clear()
    cape_rec["frames"].append({"f": f, "verts": verts})

json.dump(out, open(out_path, "w"))
print("V3 TRANSFORMS DUMPED", len(out["parts"]), "parts + cape grid x",
      spec["frames"], "frames ->", out_path)
