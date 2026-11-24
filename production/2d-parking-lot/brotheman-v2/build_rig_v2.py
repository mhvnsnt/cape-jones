#!/usr/bin/env python3
"""Build BROTHERMAN Rig Jones 2 in Blender 5.0.1 (headless bpy).

Rig Jones 2 (owner 2026-11-23 19:42 EST): Rig Jones 1 is saved as DRAFT;
this rig is drawn from the APPROVED v3 concept art — bigger head, detailed
horseshoe, spiral tie-dye, championship belt, socket-cut joints (no caps).

The bar (owner, 2026-11-23 07:19 EST): BEAT Cape's V2 rig, don't match it.
Gumball rig method, repo-documented (no .fla on this VM — see report):
layered puppet with a fixed z-stack, swappable part libraries, REAL
elbow + knee joints with overlap caps, articulating fingers + thumbs,
squash & stretch, secondary-motion follow-through on the long hair and
bandana tails. Cleaned up from the start so it reads at Draw Jones /
Video Jones level. This rig is the EXAMPLE for the Cape Jones Clean-Up
Jones plan (see BROTHERMAN-REPORT.md).

Bones (26): pelvis, torso, neck, head, hair, bandanaTail,
upperArmR/L, forearmR/L, handR/L, fingerR1-4, fingerL1-4,
thumbR/L, thighR/L, shinR/L.
Cape V2 has 12 bones, one-piece arms/legs, no finger/thumb bones,
no hair/bandana follow-through, no squash & stretch.

Base pipeline reused from the Cape V2 rig (rig/build_rig.py): native
Blender armature + emission/shadeless image planes, transparent film,
ortho camera. NEW .blend — no Cape rig file is edited.
Parts: brotheman/parts/*.png (original PIL-drawn art, transparent alpha).

Run: <tools>/blender-5.0.1-linux-x64/blender -b --python brotheman/build_rig.py
Output: brotheman/brotheman-rig.blend
"""
import bpy
import os
import struct

WD = os.path.dirname(os.path.abspath(__file__))  # repo: production/2d-parking-lot/brotheman-v2/
PARTS = f"{WD}/parts"

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 16
scene.cycles.use_denoising = False
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.film_transparent = True
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.frame_start = 1
scene.frame_end = 96
scene.render.fps = 24

world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.0


def png_size(path):
    with open(path, "rb") as f:
        data = f.read(33)
    assert data[:8] == b"\x89PNG\r\n\x1a\n", path
    w, h = struct.unpack(">II", data[16:24])
    return (w, h)


def make_material(name, path):
    img = bpy.data.images.load(path)
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.blend_method = "BLEND"
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    emit = nt.nodes.new("ShaderNodeEmission")
    transp = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    nt.links.new(tex.outputs["Color"], emit.inputs["Color"])
    nt.links.new(tex.outputs["Alpha"], mix.inputs[0])
    nt.links.new(transp.outputs[0], mix.inputs[1])
    nt.links.new(emit.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    return mat


def make_plane(name, path, center, size, z):
    w, h = size
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(center[0], center[1], z))
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = (w, h, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mat = make_material("M_" + name, path)
    ob.data.materials.append(mat)
    return ob


def ps(name):
    w, h = png_size(os.path.join(PARTS, name))
    return (w / 200.0, h / 200.0)


# ---- planes: (name, file, center, bone, z, visible) -----------------------
# Gumball layering: fixed z-stack, back to front.
# Head image is 4.6 wide with the face centred at x=2.3, so the plane
# centre sits at x=0. Socket-cut joints: the elbow/knee ball lives on the
# lower piece, the concave socket on the upper piece — NO caps/discs.
PLANES = [
    ("Shadow", "Shadow.png", (0.0, 0.55), "pelvis", -0.05, True),
    ("Hair_Back", "Hair_Back.png", (0.0, 14.60), "hair", 0.085, True),
    ("Thigh_R", "Thigh_R.png", (-1.15, 6.15), "thighR", 0.02, True),
    ("Thigh_L", "Thigh_L.png", (1.15, 6.15), "thighL", 0.03, True),
    ("Shin_R", "Shin_R.png", (-1.15, 2.35), "shinR", 0.025, True),
    ("Shin_L", "Shin_L.png", (1.15, 2.35), "shinL", 0.035, True),
    ("Pelvis", "Pelvis.png", (0.0, 8.80), "pelvis", 0.06, True),
    ("Torso", "Torso.png", (0.0, 11.60), "torso", 0.08, True),
    ("UpperArm_R", "UpperArm_R.png", (-2.85, 12.10), "upperArmR", 0.04, True),
    ("UpperArm_L", "UpperArm_L.png", (2.85, 12.10), "upperArmL", 0.045, True),
    ("Forearm_R", "Forearm_R.png", (-2.85, 9.75), "forearmR", 0.042, True),
    ("Forearm_L", "Forearm_L.png", (2.85, 9.75), "forearmL", 0.047, True),
    ("Neck", "Neck.png", (0.0, 13.55), "neck", 0.10, True),
    ("Head", "Head_Front.png", (0.0, 15.05), "head", 0.11, True),
    ("Bandana_Pink", "Bandana_Pink.png", (0.0, 16.00), "head", 0.13, True),
    ("Bandana_Blue", "Bandana_Blue.png", (0.0, 16.00), "head", 0.13, False),
    ("BandanaTails_Pink", "BandanaTails_Pink.png", (1.50, 15.10), "bandanaTail", 0.12, True),
    ("BandanaTails_Blue", "BandanaTails_Blue.png", (1.50, 15.10), "bandanaTail", 0.12, False),
    ("Eye_Open_L", "Eye_Open.png", (-0.75, 15.18), "head", 0.14, True),
    ("Eye_Open_R", "Eye_Open.png", (0.75, 15.18), "head", 0.14, True),
    ("Eye_Happy_L", "Eye_Happy.png", (-0.75, 15.18), "head", 0.14, False),
    ("Eye_Happy_R", "Eye_Happy.png", (0.75, 15.18), "head", 0.14, False),
]
planes = {}
for name, f, center, bone, z, vis in PLANES:
    ob = make_plane("P_" + name, os.path.join(PARTS, f), center, ps(f), z * 0.1)
    ob.hide_render = not vis
    planes[name] = (ob, bone)

# Mouths: 6-shape library, Closed visible by default.
MOUTHS = ["Mouth_Closed", "Mouth_Smile", "Mouth_Grin", "Mouth_Open", "Mouth_Shout", "Mouth_Frown"]
mouth_planes = {}
for m in MOUTHS:
    ob = make_plane("P_" + m, os.path.join(PARTS, m + ".png"),
                    (0.0, 14.08), ps(m + ".png"), 0.145)
    ob.hide_render = (m != "Mouth_Closed")
    mouth_planes[m] = ob

# Hands: swap planes per side. Image top sits 0.35 above the wrist (8.3)
# so the wrist/cuff overlaps the forearm's wristband — wrist-to-wrist.
# Owner hand log 2026-11-23 07:06: swaps with CORRECT orientation only.
HANDS = {"Fist": ("Hand_Fist", 1.5), "Open": ("Hand_Open", 1.1),
         "Point": ("Hand_Point", 1.9)}
hand_planes = {}
for side, sx in (("R", -2.85), ("L", 2.85)):
    for kind, (stem, h) in HANDS.items():
        f = f"{stem}_{side}.png"
        ob = make_plane(f"P_Hand{side}_{kind}", os.path.join(PARTS, f),
                        (sx, 8.65 - h / 2.0), ps(f), 0.12)
        ob.hide_render = (kind != "Fist")
        hand_planes[(side, kind)] = ob

# Fingers + thumbs: articulate on their own bones, shown with Open hand.
FING_OFF = (-0.45, -0.15, 0.15, 0.45)
finger_planes = {}
for side, sx in (("R", -2.85), ("L", 2.85)):
    for i, off in enumerate(FING_OFF, 1):
        ob = make_plane(f"P_Finger{side}{i}", os.path.join(PARTS, "Finger.png"),
                        (sx + off, 7.10), ps("Finger.png"), 0.125)
        ob.hide_render = True
        finger_planes[(side, i)] = ob
thumb_planes = {}
for side, sx, sgn in (("R", -2.85, 1), ("L", 2.85, -1)):
    ob = make_plane(f"P_Thumb{side}", os.path.join(PARTS, "Thumb.png"),
                    (sx + sgn * 0.62, 7.55), ps("Thumb.png"), 0.125)
    ob.hide_render = True
    thumb_planes[side] = ob

# ---- armature ------------------------------------------------------------
arm_data = bpy.data.armatures.new("BM_Rig")
arm_ob = bpy.data.objects.new("BM_Rig", arm_data)
bpy.context.collection.objects.link(arm_ob)
bpy.context.view_layer.objects.active = arm_ob
bpy.ops.object.mode_set(mode="EDIT")


def bone(name, head, tail, parent=None):
    b = arm_data.edit_bones.new(name)
    b.head = (head[0], head[1], 0)
    b.tail = (tail[0], tail[1], 0)
    if parent:
        b.parent = arm_data.edit_bones[parent]
    return b


bone("pelvis", (0, 8.2), (0, 9.6))
bone("torso", (0, 9.4), (0, 13.6), "pelvis")
bone("neck", (0, 13.6), (0, 14.2), "torso")
bone("head", (0, 14.0), (0, 16.2), "neck")
bone("hair", (0, 15.6), (0, 13.0), "head")
bone("bandanaTail", (1.5, 16.3), (1.5, 14.3), "head")
bone("upperArmR", (-2.85, 13.3), (-2.85, 10.8), "torso")
bone("forearmR", (-2.85, 10.8), (-2.85, 8.3), "upperArmR")
bone("upperArmL", (2.85, 13.3), (2.85, 10.8), "torso")
bone("forearmL", (2.85, 10.8), (2.85, 8.3), "upperArmL")
bone("thighR", (-1.15, 7.6), (-1.15, 4.3), "pelvis")
bone("shinR", (-1.15, 4.3), (-1.15, 0.2), "thighR")
bone("thighL", (1.15, 7.6), (1.15, 4.3), "pelvis")
bone("shinL", (1.15, 4.3), (1.15, 0.2), "thighL")
bone("handR", (-2.85, 8.3), (-2.85, 7.0), "forearmR")
bone("handL", (2.85, 8.3), (2.85, 7.0), "forearmL")
for side, sx in (("R", -2.85), ("L", 2.85)):
    for i, off in enumerate(FING_OFF, 1):
        bone(f"finger{side}{i}", (sx + off, 7.6), (sx + off, 6.6), "hand" + side)
    sgn = 1 if side == "R" else -1
    bone(f"thumb{side}", (sx + sgn * 0.55, 7.85), (sx + sgn * 0.85, 7.15), "hand" + side)

bpy.ops.object.mode_set(mode="OBJECT")


def parent_keep(ob, bone_name):
    ob.parent = arm_ob
    ob.parent_type = "BONE"
    ob.parent_bone = bone_name
    # Same proven form as the Cape V2 rig: bone-parent evaluation origin
    # is the bone TAIL — build the inverse from tail translation.
    pb = arm_ob.pose.bones[bone_name]
    m = pb.matrix.copy()
    m.translation = pb.tail
    ob.matrix_parent_inverse = (arm_ob.matrix_world @ m).inverted()


for name, (ob, bone_name) in planes.items():
    parent_keep(ob, bone_name)
for ob in mouth_planes.values():
    parent_keep(ob, "head")
for (side, kind), ob in hand_planes.items():
    parent_keep(ob, "hand" + side)
for (side, i), ob in finger_planes.items():
    parent_keep(ob, f"finger{side}{i}")
for side, ob in thumb_planes.items():
    parent_keep(ob, f"thumb{side}")

for pb in arm_ob.pose.bones:
    pb.rotation_mode = "XYZ"

# ---- camera --------------------------------------------------------------
cam_data = bpy.data.cameras.new("Cam")
cam_data.type = "ORTHO"
cam_data.ortho_scale = 34.0
cam_ob = bpy.data.objects.new("Cam", cam_data)
bpy.context.collection.objects.link(cam_ob)
cam_ob.location = (0, 8.4, 20)
scene.camera = cam_ob

bpy.ops.wm.save_as_mainfile(filepath=f"{WD}/brotheman-rig-v2.blend")
print("RIG V2 SAVED", f"{WD}/brotheman-rig-v2.blend")
print("bones:", [b.name for b in arm_data.bones])
print("planes:", len(planes) + len(mouth_planes) + len(hand_planes) + len(finger_planes) + len(thumb_planes))
