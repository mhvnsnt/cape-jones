#!/usr/bin/env python3
"""Build Rig Jones 2 / Clean-Up Jones 1 — the PURPLE LOT V3 rig, v2.
Gumball level, 100% their method: slot swap, frame-addressed comps,
anatomical pivots, one-piece deforming cape.

This is the NEXT version of Rig Jones (Rig Jones 2 = Clean-Up Jones 1).
Standard: if it is not at Gumball level, it is not done.

v2 CORRECTIONS (owner, 2026-11-23 10:40-10:42 EST — the handswap
rejection, owned not defended):
1. NO CAPS, EVER. The sibling handswap lane generated a literal white
   disc (rig/parts/Cap_disc.png) and stuck it on every joint — that file
   is NOT in this build and never will be. This build's own fault was the
   same class of mistake in smaller form: the elbow/knee crops overlapped
   +-8px, so the ball was drawn in BOTH pieces and read as a separate
   joint disc during the raise. FIX: SOCKET CUT (prep_art.py v2). Each
   joint is cut along the ball's OWN outline circle (RANSAC+Kasa fit,
   RMS ~1.1px): the ball belongs entirely to the lower piece, the upper
   piece ends in a concave socket of the same circle. No pixel is in
   both pieces, none in neither (verified by pixel diff in prep). No
   added piece, no cover-up — the cut follows the art's own contour.
   GUMBALL VERIFIED FIRST-HAND (GB200 .fla, opened 2026-11-23): there is
   NO cap/disc/ball-joint anywhere in GB200. L_ARM/R_ARM are ONE ARM
   layer of 24/26 keyframes, every keyframe a single DOMShape — the whole
   arm+hand redrawn per pose, elbow bend DRAWN not jointed. The ONLY
   limb split is at the SHOULDER, front/back, sharing ONE
   transformationPoint. The old claim of a Gumball "overlap-cap" was
   WRONG and is struck from this build.
2. MEASURED PIVOTS. The old pivots (+-1.6 / +-0.9 straight down the
   limb) were approximations. Measured from the art: the elbow ball
   centre is NOT on the limb's centre line, and the wrist pinch is
   0.12-0.33 units off the old x. That is why the hands did not sit
   cleanly on the wrists. New pivots (art-geometry.json, fitted):
   elbow R (-1.767, 8.681) / L (1.889, 8.183), wrist R (-1.724, 6.905)
   / L (1.928, 6.905), knee R (-0.757, 5.109) / L (1.068, 5.127).
   Bones follow the art; planes are centred so the ball lands on the
   bone pivot.
3. INVISIBLE SWAP. The old swap used 7 separate planes per side, each
   sized from its own art — cuff centre x varied 37-64px between
   variants, so the hand TELEPORTED sideways up to 0.24 units at every
   swap (a literal scene cut). FIX: ONE plane per side, one common
   canvas (132x144), every variant re-centred in the ART (cuff centre
   x=66, cuff top row 0). Same plane, same pivot, same position — only
   the IMAGE on that plane changes. Mouths likewise on one common
   canvas (105x95). The hands themselves were GOOD (owner 10:42 EST) —
   the hand system is kept exactly, only the swap mechanism changed.
4. CAPE: kept. The one-piece skin-weighted mesh cape is CLEAN — no
   cover-up, no split, no disc. It hangs from the torso and trails the
   arm's motion (velocity lag + lean compensation). If it cannot be
   clean it reverts to the V2 cape; it is clean, so it stays.
5. EVERYTHING ADDED IS NAMED HERE. Nothing is hidden: the socket cut
   (no added piece), the single hand/mouth planes (image-swap), the
   re-centred hand/mouth art (common canvases), the measured pivots.
   No Cap_disc, no extra anatomy, no cover-up of any join.

What is unchanged from v1 (all still true):
- ONE HAND PER ARM (owner 08:50 EST). Forearm ends at the cuff, no
  drawn fist. Hand plane is the ONLY hand.
- PARENTING — prime suspect CLEARED (pivot_experiment.py). The V2
  parent_keep() tail form is correct and used verbatim. The real bug
  was the bone HEADS — now measured, not guessed.
- SLOT SWAP, Gumball way: one slot per part, swapping REPLACES the part
  in place. Now literally: the image on one plane changes.
- ONE-PIECE CAPE (owner 08:56 EST): mesh, skin-weighted, torso chain.

CN METHOD (study-only): method travels, CN/Gumball characters and
artwork NEVER go into show files. GB200 opened first-hand; see
GUMBALL-FIRSTHAND.md and CN-IN-OUR-LANGUAGE.md.

Run: blender-5.0.1-linux-x64/blender -b --python v3-swap-system/build_v3.py
Output: v3-swap-system/purple-lot-v3-rig.blend
"""
import bpy
import json
import math
import os
import struct
import sys

WD = "/home/hatch/workspace/_cape-jones-parking-lot-2d"
V3 = f"{WD}/v3-swap-system"
ART = f"{V3}/art"
sys.path.insert(0, V3)

GEOM = json.load(open(f"{V3}/art-geometry.json"))

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 32
scene.cycles.use_denoising = False
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.film_transparent = True
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.frame_start = 1
scene.frame_end = 480
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
    return struct.unpack(">II", data[16:24])


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


def plane_size(fname, scale=0.95):
    pw, ph = png_size(os.path.join(ART, fname))
    return (pw * scale / 100.0, ph * scale / 100.0)


# ---- armature -----------------------------------------------------------
arm_data = bpy.data.armatures.new("CJ_Rig_V3")
arm_ob = bpy.data.objects.new("CJ_Rig_V3", arm_data)
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


# Y-up rig space. Limb bones point DOWN (head = proximal joint).
# Pivots measured from the art (art-geometry.json) — NOT the old
# +-1.6/+-0.9 straight-line guesses.
ELB_R = GEOM["balls"]["elbowR"]["rig"]
ELB_L = GEOM["balls"]["elbowL"]["rig"]
WRI_R = GEOM["wrists"]["R"]["rig"]
WRI_L = GEOM["wrists"]["L"]["rig"]
KNE_R = GEOM["balls"]["kneeR"]["rig"]
KNE_L = GEOM["balls"]["kneeL"]["rig"]
bone("pelvis", (0, 8.07), (0, 9.4))
bone("torso", (0, 7.97), (0, 10.9), "pelvis")
bone("neck", (0, 10.9), (0, 11.5), "torso")
bone("head", (0, 10.87), (0, 12.5), "neck")
# Arms: shoulder -> elbow (ball centre) -> wrist (pinch) -> fingertips.
bone("upperArmR", (-1.6, 10.8), ELB_R, "torso")
bone("forearmR", ELB_R, WRI_R, "upperArmR")
bone("handR", WRI_R, (WRI_R[0], 5.77), "forearmR")
bone("upperArmL", (1.6, 10.8), ELB_L, "torso")
bone("forearmL", ELB_L, WRI_L, "upperArmL")
bone("handL", WRI_L, (WRI_L[0], 5.77), "forearmL")
# Legs: hip -> knee (ball centre) -> ankle.
bone("thighR", (-0.9, 7.47), KNE_R, "pelvis")
bone("shinR", KNE_R, (KNE_R[0], 1.90), "thighR")
bone("thighL", (0.9, 7.47), KNE_L, "pelvis")
bone("shinL", KNE_L, (KNE_L[0], 1.90), "thighL")
# Cape chain: parented to TORSO only — never to the arm.
bone("capeNeck", (0, 10.9), (0, 8.0), "torso")
bone("capeMid", (0, 8.0), (0, 5.5), "capeNeck")
bone("capeTip", (0, 5.5), (0, 3.0), "capeMid")

bpy.ops.object.mode_set(mode="OBJECT")

# Parent planes to bones (keep world transform). VERIFIED by
# pivot_experiment.py: the tail-form inverse is the only formula that
# preserves the rest position AND rotates about the bone HEAD. Do not
# "fix" this into the canonical form — that displaces every part.
def parent_keep(ob, bone_name):
    ob.parent = arm_ob
    ob.parent_type = "BONE"
    ob.parent_bone = bone_name
    pb = arm_ob.pose.bones[bone_name]
    m = pb.matrix.copy()
    m.translation = pb.tail
    ob.matrix_parent_inverse = (arm_ob.matrix_world @ m).inverted()


for pb in arm_ob.pose.bones:
    pb.rotation_mode = "XYZ"

# ---- body planes (always visible) ---------------------------------------
# (name, file, centre, z, bone). Limb centres/sizes come from
# art-geometry.json (the socket-cut crops); torso/head/etc. from the V2
# REST table as before. Do not hand-guess these — a wrong centre is a
# floating part.
def add_body(name, fname, center, z, bone_name, scale=0.95):
    ob = make_plane("P_" + name, os.path.join(ART, fname),
                    center, plane_size(fname, scale), z * 0.1)
    parent_keep(ob, bone_name)
    return ob


def add_body_geom(name, fname, z, bone_name):
    g = GEOM["planes"][name]
    ob = make_plane("P_" + name, os.path.join(ART, fname),
                    g["center"], g["size"], z * 0.1)
    parent_keep(ob, bone_name)
    return ob


def xy(cx, y):
    return ((cx - 550.0) / 100.0, (1500.0 - y) / 100.0)


def rest_center(fname, cx, top, scale=0.95):
    w, h = plane_size(fname, scale)
    cxu, topu = xy(cx, top)
    return (cxu, topu - h / 2.0)


add_body("Torso_Chest", "Torso_Chest.png", rest_center("Torso_Chest.png", 550, 400), 0.08, "torso")
add_body("Pelvis", "Pelvis.png", rest_center("Pelvis.png", 550, 680), 0.06, "pelvis")
add_body("Belt_Overlay", "Belt_Overlay.png", rest_center("Belt_Overlay.png", 550, 670), 0.09, "torso")
add_body("Neck", "Neck.png", rest_center("Neck.png", 550, 360, scale=1.05), 0.10, "neck", scale=1.05)
add_body("Head_Front", "Head_Front.png", rest_center("Head_Front.png", 550, 250), 0.11, "head")
add_body("Cape_Collar", "Cape_Collar.png", rest_center("Cape_Collar.png", 550, 370), 0.07, "torso")
# Limbs: socket-cut crops, centres from the geometry file.
add_body_geom("UpperArmR", "upperArm_R.png", 0.05, "upperArmR")
add_body_geom("UpperArmL", "upperArm_L.png", 0.04, "upperArmL")
add_body_geom("ForearmR", "forearm_R.png", 0.05, "forearmR")
add_body_geom("ForearmL", "forearm_L.png", 0.04, "forearmL")
add_body_geom("ThighR", "thigh_R.png", 0.03, "thighR")
add_body_geom("ThighL", "thigh_L.png", 0.02, "thighL")
add_body_geom("ShinR", "shin_R.png", 0.03, "shinR")
add_body_geom("ShinL", "shin_L.png", 0.02, "shinL")
# Ground shadow.
shadow_ob = make_plane("P_Shadow", os.path.join(ART, "Shadow.png"),
                       (0.0, 1.35), (4.6, 1.4), -0.05)
parent_keep(shadow_ob, "pelvis")

# ---- slots --------------------------------------------------------------
# Two kinds of slot (both "replace in place", Gumball way):
#  - IMAGE slots (handR, handL, mouth): ONE plane per slot; swapping
#    changes ONLY the image on that plane. Same plane, same pivot, same
#    position — the swap is invisible. Variants carry "image".
#  - VISIBILITY slots (eyes, remote, forearms): variants own objects,
#    exactly one variant's objects visible (the v1 system, kept — it
#    passed own-eyes; eyes share objects across variants).
HAND_NAMES = ["Fist", "FistBack", "Open", "Point", "Point2", "Relaxed", "Grip"]
MOUTH_NAMES = ["Closed", "Open", "Shout", "Smile", "Teeth"]
HAND_CANVAS = GEOM["hands"]["canvas"]  # [132, 144]
HAND_SIZE = (HAND_CANVAS[0] * 0.0095, HAND_CANVAS[1] * 0.0095)


def add_image_slot_plane(name, fname, center, z, bone_name, size):
    ob = make_plane(name, os.path.join(ART, fname), center, size, z)
    parent_keep(ob, bone_name)
    return ob


slots = {}
# Hands: ONE plane per side. Cuff top (canvas row 0) at the wrist;
# centre = wrist - H/2. Cuff centre x = plane centre x (canvas cuff
# x=66 is the canvas centre, 132/2).
for side, wri in (("R", WRI_R), ("L", WRI_L)):
    ob = add_image_slot_plane(
        f"P_hand{side}", f"Hand_{side}_6.png",
        (wri[0], wri[1] - HAND_SIZE[1] / 2), 0.12, f"hand{side}", HAND_SIZE)
    slots[f"hand{side}"] = {
        "bone": f"hand{side}", "object": ob.name, "art_dir": ART,
        "variants": [{"name": hn, "image": f"Hand_{side}_{i}.png"}
                     for i, hn in enumerate(HAND_NAMES, start=1)]}
# Mouth: ONE plane, anchor (0, 11.31), common canvas 105x95.
MOUTH_SIZE = (GEOM["mouth_canvas"][0] * 0.0095, GEOM["mouth_canvas"][1] * 0.0095)
mob = add_image_slot_plane(
    "P_mouth", "Mouth_Closed.png", (0.0, 11.31), 0.14, "head", MOUTH_SIZE)
slots["mouth"] = {
    "bone": "head", "object": mob.name, "art_dir": ART,
    "variants": [{"name": mn, "image": f"Mouth_{mn}.png"}
                 for mn in MOUTH_NAMES]}


def add_slot_plane(name, fname, center, z, bone_name, size_scale=1.0):
    w, h = plane_size(fname)
    ob = make_plane(name, os.path.join(ART, fname),
                    center, (w * size_scale, h * size_scale), z)
    ob.hide_render = True
    parent_keep(ob, bone_name)
    return ob


# Eyes: one comp. Normal = both white eyes; Pupils = white eyes + pupils.
# Eye whites at 0.32 scale (the 0.56-unit first try was caught own-eyes);
# pupils at V2's proven 0.34 (f440 gag look).
eyeL = add_slot_plane("P_eyes_Eye_L", "Eye_L.png", (-0.24, 11.78), 0.14,
                      "head", size_scale=0.32)
eyeR = add_slot_plane("P_eyes_Eye_R", "Eye_R.png", (0.22, 11.78), 0.14,
                      "head", size_scale=0.32)
pupils = []
for i, dx in enumerate((-0.19, 0.16)):
    ob = add_slot_plane(f"P_eyes_Pupil_{i}", "Pupil.png",
                        (dx, 11.62), 0.15, "head", size_scale=0.6)
    pupils.append(ob.name)
slots["eyes"] = {"bone": "head", "variants": [
    {"name": "Normal", "objects": [eyeL.name, eyeR.name]},
    {"name": "Pupils", "objects": [eyeL.name, eyeR.name] + pupils},
]}
# Forearms: single-variant slots (the slot exists so the forearm plate can
# be swapped like any other part; the art has one variant per side).
slots["forearmR"] = {"bone": "forearmR", "variants": [
    {"name": "Standard", "objects": ["P_ForearmR"]}]}
slots["forearmL"] = {"bone": "forearmL", "variants": [
    {"name": "Standard", "objects": ["P_ForearmL"]}]}
# Remote: device ONLY (no hand in the crop). Centre shifted by the wrist
# delta from v1 (wrist R moved (-0.124, +0.005)): the grip point must
# land on the Grip hand's finger centre (measured on the common canvas).
# finger centre (rig, rest) = hand centre + local offset of the Grip
# finger centroid: canvas (75.4, 100.7), canvas centre (66, 72).
_fx, _fy = GEOM["hands"]["Grip_R_finger_canvas"]
_finger_local = ((_fx - 66) * 0.0095, (72 - _fy) * 0.0095)
_hand_c = (WRI_R[0], WRI_R[1] - HAND_SIZE[1] / 2)
_finger_rig = (_hand_c[0] + _finger_local[0], _hand_c[1] + _finger_local[1])
# Remote grip point offset from the remote plane centre: (+0.18, +0.0855).
_remote_c = (_finger_rig[0] - 0.18, _finger_rig[1] - 0.0855)
remote = add_slot_plane("P_remote_Remote_Device", "Remote_Device.png",
                        _remote_c, 0.13, "handR")
slots["remote"] = {"bone": "handR", "variants": [
    {"name": "Device", "objects": [remote.name]}]}
# Default visible variants (rest pose): Relaxed hands, Closed mouth,
# Normal eyes, no remote.
DEFAULTS = {"handR": 5, "handL": 5, "mouth": 0, "eyes": 0,
            "forearmR": 0, "forearmL": 0, "remote": -1}
# The slots JSON must be on the armature BEFORE cj_set_slot is called
# (it reads arm["cj_slots"]).
arm_ob["cj_slots"] = json.dumps(slots)
arm_ob["cj_defaults"] = json.dumps(DEFAULTS)
import cj_swap_addon
for slot, idx in DEFAULTS.items():
    if idx < 0:
        # remote: hidden.
        for obname in slots[slot]["variants"][0]["objects"]:
            bpy.data.objects[obname].hide_render = True
        continue
    if "image" in slots[slot]["variants"][0]:
        cj_swap_addon.cj_set_slot(arm_ob, slot, idx, set_viewport=False)
    else:
        for obname in slots[slot]["variants"][idx]["objects"]:
            bpy.data.objects[obname].hide_render = False
print("remote centre:", _remote_c, "finger rig:", _finger_rig)

# ---- cape: ONE continuous mesh, skin-weighted (UNCHANGED — clean) --------
# Cape_Back_Main 490x833 -> 4.655 x 7.9135 units, top (collar) 10.9.
CAPE_W, CAPE_H = plane_size("Cape_Back_Main.png")
CAPE_TOP = 10.9
COLS, ROWS = 6, 12
bpy.ops.mesh.primitive_grid_add(x_subdivisions=COLS, y_subdivisions=ROWS,
                                size=1.0, location=(0, CAPE_TOP - CAPE_H / 2, 0.001))
cape = bpy.context.active_object
cape.name = "P_Cape"
cape.scale = (CAPE_W, CAPE_H, 1.0)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
mesh = cape.data
for loop in mesh.loops:
    v = mesh.vertices[loop.vertex_index]
    u = (v.co.x + CAPE_W / 2) / CAPE_W
    vv = (v.co.y + CAPE_H / 2) / CAPE_H
    mesh.uv_layers.active.data[loop.index].uv = (u, vv)
mat = make_material("M_P_Cape", os.path.join(ART, "Cape_Back_Main.png"))
mesh.materials.append(mat)
groups = {}
for bn in ("torso", "capeNeck", "capeMid", "capeTip"):
    groups[bn] = cape.vertex_groups.new(name=bn)
bone_y = {"torso": 10.9, "capeNeck": 9.45, "capeMid": 6.75, "capeTip": 4.25}
for v in mesh.vertices:
    y = v.co.y + (CAPE_TOP - CAPE_H / 2)
    ws = {}
    for bn, ay in bone_y.items():
        d = abs(y - ay)
        ws[bn] = max(0.0, 1.0 - d / 2.6)
    tot = sum(ws.values()) or 1.0
    for bn, w in ws.items():
        if w > 0:
            groups[bn].add([v.index], w / tot, "REPLACE")
mod = cape.modifiers.new("Armature", "ARMATURE")
mod.object = arm_ob
cape.parent = arm_ob
cape.parent_type = "ARMATURE"
cape.hide_render = False

# ---- camera -------------------------------------------------------------
cam_data = bpy.data.cameras.new("Cam")
cam_data.type = "ORTHO"
cam_data.ortho_scale = 28.0
cam_ob = bpy.data.objects.new("Cam", cam_data)
bpy.context.collection.objects.link(cam_ob)
cam_ob.location = (0, 7.0, 20)
scene.camera = cam_ob

# Rest pose.
bpy.context.view_layer.objects.active = arm_ob
bpy.ops.object.mode_set(mode="POSE")
for pb in arm_ob.pose.bones:
    pb.rotation_euler = (0, 0, 0)
bpy.ops.object.mode_set(mode="OBJECT")

# Embed the swap add-on source as a text block so the .blend carries it.
addon_path = os.path.join(V3, "cj_swap_addon.py")
if os.path.exists(addon_path):
    txt = bpy.data.texts.new("cj_swap_addon.py")
    txt.from_string(open(addon_path).read())

bpy.ops.wm.save_as_mainfile(filepath=f"{V3}/purple-lot-v3-rig.blend")
print("RIG JONES 2 v2 SAVED", f"{V3}/purple-lot-v3-rig.blend")
print("bones:", [b.name for b in arm_data.bones])
print("slots:", list(slots.keys()))
