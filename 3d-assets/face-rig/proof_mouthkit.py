#!/usr/bin/env python3
"""Proof render: grid of all 17 mouths + eye cards. Viewed with own eyes."""
import bpy
import math

KIT = "./cj_mouth_kit.blend"
OUT = "./proof/mouthkit_proof.png"

bpy.ops.wm.open_mainfile(filepath=KIT)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 24
scene.cycles.device = 'CPU'
scene.render.resolution_x = 1600
scene.render.resolution_y = 1100
scene.render.film_transparent = False
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.55, 0.55, 1.0)

# lights
bpy.ops.object.light_add(type='AREA', location=(0.6, 1.0, 1.2))
bpy.context.object.data.energy = 800
bpy.ops.object.light_add(type='AREA', location=(-0.8, 0.7, 0.6))
bpy.context.object.data.energy = 300


def dup_hierarchy(empty):
    new_e = empty.copy()
    scene.collection.objects.link(new_e)
    if new_e.animation_data:
        new_e.animation_data_clear()
    new_e.hide_viewport = False
    new_e.hide_render = False
    for c in list(empty.children):
        nc = c.copy()
        if c.data is not None:
            try:
                nc.data = c.data.copy()
            except Exception:
                pass
        scene.collection.objects.link(nc)
        nc.parent = new_e
        if nc.animation_data:
            nc.animation_data_clear()
        nc.hide_viewport = False
        nc.hide_render = False
        for g in list(c.children):  # eye sub-groups
            ng = g.copy()
            if g.data is not None:
                try:
                    ng.data = g.data.copy()
                except Exception:
                    pass
            scene.collection.objects.link(ng)
            ng.parent = nc
            if ng.animation_data:
                ng.animation_data_clear()
            ng.hide_viewport = False
            ng.hide_render = False
    return new_e


def label(text, loc, size=0.022):
    bpy.ops.object.text_add(location=loc, rotation=(-math.pi / 2, 0, 0))
    t = bpy.context.object
    t.data.body = text
    t.data.size = size
    t.data.materials.append(bpy.data.materials["CJ_Mouth_Black"])
    return t


mouths = sorted([o for o in bpy.data.objects if o.name.startswith("CJ_Mouth_0") or
                 o.name.startswith("CJ_Mouth_1")],
                key=lambda o: o.name)
print("MOUTHS FOUND:", len(mouths), [o.name for o in mouths])

COLS, DX, DZ = 6, 0.22, 0.26
X0 = -DX * (COLS - 1) / 2.0
for i, m in enumerate(mouths):
    col, row = i % COLS, i // COLS
    d = dup_hierarchy(m)
    d.location = (X0 + col * DX, 0, 0.40 - row * DZ)
    short = m.name.replace("CJ_Mouth_", "")
    label(short, (X0 + col * DX - 0.085, 0.012, 0.40 - row * DZ - 0.105), size=0.018)

# eye row: white-only, white+pupil, closed
eyes = bpy.data.objects.get("CJ_Eyes")
if eyes:
    for k, (tag, eidx) in enumerate([("white", 0), ("pupil", 1), ("closed", 2)]):
        d = dup_hierarchy(eyes)
        d.location = (-0.45 + k * 0.45, 0, -0.42)
        # set visibility manually on the copy
        for child in list(d.children):
            if child.name == "CJ_Eye_Closed":
                hide = (eidx != 2)
            else:
                hide = (eidx == 2)
            child.hide_viewport = hide
            child.hide_render = hide
            for g in list(child.children):
                if "pupil" in g.name:
                    gh = (eidx != 1)
                    g.hide_viewport = gh
                    g.hide_render = gh
        label("eye_" + tag, (-0.45 + k * 0.45 - 0.09, 0.012, -0.52), size=0.020)

# camera: frontal at +Y looking -Y (mouths face +Y)
bpy.ops.object.camera_add(location=(0, 1.55, 0.02), rotation=(-math.pi / 2, 0, 0))
cam = bpy.context.object
cam.data.lens = 55
cam.data.clip_start = 0.05
scene.camera = cam

scene.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("PROOF SAVED", OUT)
