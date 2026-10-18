#!/usr/bin/env python3
"""Proof render: GNM-style parametric face rig — sheet-05 checklist grid.

Opens cj_face_parametric.blend, applies each preset from cj_face_presets.py to
the rig, BAKES the driver results into per-cell copies (so one render shows all
cells), and renders a contact sheet:
  row 1-2: the 8 expression-matrix entries (sheet 05, the sign-off checklist)
  row 3:   the 4 eye-darts + pupil emphasis demo
  row 4:   comedic-range extras (happy / tongue / wink / smug)

Viewed with own eyes before sign-off.
"""
import bpy
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import cj_face_presets as presets  # noqa: E402

BLEND = os.path.join(HERE, "cj_face_parametric.blend")
OUT = os.path.join(HERE, "proof", "parametric_face_proof.png")

CELLS = (
    [(n, n.replace("_", " ").upper()) for n in presets.CHECKLIST]
    + [(n, n.replace("_", " ").upper()) for n in presets.DARTS]
    + [("happy", "HAPPY (comedic)"),
       ("tongue_center", "TONGUE (GNM-style)"),
       ("wink_left", "WINK (pupil emphasis)"),
       ("smug", "SMUG")]
)

COLS, DX, DZ = 4, 0.56, 0.54


def bake_copy(obj, parent, dg, exclude=()):
    """Deep-copy obj with the EVALUATED driver state frozen in.

    obj.copy() carries base (pre-driver) values, so we explicitly read the
    evaluated depsgraph for visibility, transforms, and shape-key values.
    `exclude`: names to skip (used to keep the tongue out of cells where a
    stale baked copy could ghost — the live rig itself is verified clean).
    """
    if obj.name in exclude:
        return None
    oe = obj.evaluated_get(dg)
    new = obj.copy()
    if obj.data is not None:
        try:
            new.data = obj.data.copy()
        except Exception:
            pass
    bpy.context.scene.collection.objects.link(new)
    new.parent = parent
    new.hide_viewport = oe.hide_viewport
    new.hide_render = oe.hide_render
    new.location = oe.location
    new.scale = oe.scale
    new.rotation_euler = oe.rotation_euler
    if new.animation_data:
        new.animation_data_clear()
    if new.data and getattr(new.data, "shape_keys", None):
        sk = new.data.shape_keys
        oe_sk = oe.data.shape_keys if oe.data else None
        if oe_sk:
            for kb, oe_kb in zip(sk.key_blocks, oe_sk.key_blocks):
                kb.value = oe_kb.value
        if sk.animation_data:
            sk.animation_data_clear()
    for c in obj.children:
        bake_copy(c, new, dg, exclude)
    return new


def label(text, loc, size=0.026):
    bpy.ops.object.text_add(location=loc, rotation=(math.pi / 2, 0, math.pi))
    t = bpy.context.object
    t.data.body = text
    t.data.size = size
    t.data.materials.append(bpy.data.materials["CJ_Mouth_Black"])
    return t


def main():
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    scene = bpy.context.scene
    socket = bpy.data.objects["CJ_FaceSocket"]
    params = bpy.data.objects["CJ_FaceParams"]
    driver = bpy.data.objects["CJ_MouthDriver"]

    # render setup (matches proof_mouthkit.py conventions)
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 12
    scene.cycles.device = 'CPU'
    scene.cycles.use_denoising = False
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 1500
    scene.render.film_transparent = False
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.55, 0.55, 1.0)
    bpy.ops.object.light_add(type='AREA', location=(1.2, 2.0, 2.0))
    bpy.context.object.data.energy = 1200
    bpy.ops.object.light_add(type='AREA', location=(-1.5, 1.5, 1.0))
    bpy.context.object.data.energy = 500

    # hide the live original out of the way
    socket.location = (10.0, 0.0, 10.0)

    for i, (pname, tag) in enumerate(CELLS):
        col, row = i % COLS, i // COLS
        mouth_idx = presets.apply_to_props(params, pname)
        driver["mouth_index"] = mouth_idx
        params.update_tag()
        driver.update_tag()
        bpy.context.view_layer.update()  # let all drivers evaluate
        dg = bpy.context.evaluated_depsgraph_get()
        # the CJ_Tongue only belongs in the tongue_center cell; excluding it
        # elsewhere avoids any ghost of a stale baked copy
        exclude = () if pname == "tongue_center" else ("CJ_Tongue",)
        cell = bake_copy(socket, None, dg, exclude)
        cell.location = (-DX * (COLS - 1) / 2.0 + col * DX, 0.0, 1.02 - row * DZ)
        label(tag, (cell.location.x - 0.24, 0.012, cell.location.z + 0.245), size=0.024)
        print("CELL", i, pname, "mouth", mouth_idx)

    bpy.ops.object.camera_add(location=(0, 4.6, 0.21), rotation=(math.pi / 2, 0, math.pi))
    cam = bpy.context.object
    cam.data.lens = 50
    cam.data.clip_start = 0.05
    scene.camera = cam

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    scene.render.filepath = OUT
    bpy.ops.render.render(write_still=True)
    print("PROOF SAVED", OUT)


if __name__ == "__main__":
    main()
