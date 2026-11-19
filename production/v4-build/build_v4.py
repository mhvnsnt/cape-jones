"""Cape Jones dance proof 3D v4 - build + solve (stages A and B).

v4 answers the owner's stiffness verdict on v3 (hand-keyed FK, arms locked
in T-pose, only forearms moving). The fix is a pulled-in industry stack,
wired in this order:

  1. AUTO-RIG FIRST: Blender Rigify (the bundled industry-standard
     auto-rig generator) builds the full control rig from a human metarig
     fitted to Cape Jones's measured joint positions. IK/FK limbs, spine,
     neck/head, fingers - plus a Rigify spline-tentacle chain for the CAPE
     (its own IK chain: DEF-cape.001..005). No hand-built rigging.
  2. REAL MOTION SECOND: CMU Graphics Lab mocap 61_03 (salsa dance),
     frames 1010..1485 at 120 fps -> a 96-frame loop at 24 fps, retargeted
     onto the Rigify controls with the world-space delta method (the same
     math as this repo's mocap_retarget.py): IK end-effectors take the
     mocap joints' world positions, spine/neck/head take world-orientation
     deltas, fingers take the CMU index/thumb joint deltas (middle/ring/
     pinky follow the finger-base delta, Cascadeur AutoPosing-style
     master coupling). Root XZ travel is recentered + dampened x0.6
     (standard root-motion cleanup) so he dances in one spot.
  3. SECONDARY MOTION: the cape's spline-IK hook controls (mid + end) are
     driven by a verlet spring chain trailing the solved chest - the
     Cascadeur AutoPhysics secondary-motion method re-implemented in the
     open pipeline (local/global blending -> per-point stiffness falloff,
     damping, gravity).

Inputs : scene_v3.blend (v3 scene copy - READ ONLY, never overwritten),
         bvh/61_03.bvh (CMU mocap, una-dinosauria/cmu-mocap mirror)
Outputs: rig_v4.blend (auto-rigged, weights transferred, rest pose),
         scene_v4.blend (solved 96-frame loop in NLA x19 = 1824 frames),
         measurements.json (owner joint checklist, measured on DEF bones)

Run: xvfb-run -a env -u PYTHONPATH blender -b --python build_v4.py
"""
import bpy, math, os, sys, json, time
import numpy as np
from mathutils import Vector, Quaternion, Matrix

D = math.radians
WORK = "/home/hatch/workspace/_cj_v4_build"
SRC_SCENE = "/home/hatch/workspace/_cj-dance3d-v3/scene_v3.blend"
BVH_PATH = "/home/hatch/workspace/_cj_v4_assets/bvh/61_03.bvh"
SRC_START = 1010          # CMU 61_03 source frame (120 fps)
LOOP = 96                 # output frames at 24 fps (step 5)
STEP = 5
XFADE = 12                # seam crossfade frames
ROOT_DAMP = 0.6
TARGET_H = 0.925
os.makedirs(WORK, exist_ok=True)
t00 = time.time()
def log(*a):
    print("[v4]", *a, round(time.time() - t00, 1), "s", flush=True)

# ============================================================ load v3 scene
bpy.ops.wm.open_mainfile(filepath=SRC_SCENE)
sc = bpy.context.scene
old_rig = bpy.data.objects["CapeJones_Rig"]
body = bpy.data.objects["BodyR"]
sheet = bpy.data.objects["CapeSheet"]

# old skeleton joint map (rest, armature space)
J = {}
for b in old_rig.data.bones:
    J[b.name] = (Vector(b.head_local), Vector(b.tail_local))
log("old joints captured:", len(J))

def jn(name):  # joint head
    return J[name][0]
def jt(name):  # joint tail
    return J[name][1]

# ============================================================ STAGE A: Rigify
bpy.ops.preferences.addon_enable(module="rigify")
bpy.ops.object.armature_human_metarig_add()
meta = bpy.context.active_object
meta.name = "CJ_Metarig"
bpy.ops.object.mode_set(mode="EDIT")
eb = meta.data.edit_bones

def setb(name, head, tail):
    b = eb[name]
    b.head = Vector(head); b.tail = Vector(tail)
    return b

# spine chain from the measured old skeleton
setb("spine",     jn("pelvis"),  jt("pelvis"))
setb("spine.001", jn("spine_1"), jt("spine_1"))
setb("spine.002", jn("spine_2"), jt("spine_2"))
setb("spine.003", jn("chest"),   Vector((0.0, -0.01, 0.78)))
setb("spine.004", Vector((0.0, -0.01, 0.78)), Vector((0.0, -0.015, 0.83)))
setb("spine.005", Vector((0.0, -0.015, 0.83)), Vector((0.0, -0.02, 0.865)))
setb("spine.006", Vector((0.0, -0.02, 0.865)), jt("head"))
# face subtree: translate onto the (much lower) head
face_root = eb["face"]
delta = eb["spine.006"].head - face_root.head
face_bones = [face_root] + list(face_root.children_recursive)
for b in face_bones:
    b.head += delta; b.tail += delta
log("face subtree translated", len(face_bones), "bones")

for side in ("L", "R"):
    s = f"_{side}"
    setb(f"shoulder{'.' + side}", jn(f"clavicle{s}"), jt(f"clavicle{s}"))
    setb(f"upper_arm.{side}", jn(f"upperarm{s}"), jt(f"upperarm{s}"))
    setb(f"forearm.{side}",   jn(f"forearm{s}"),  jt(f"forearm{s}"))
    hw = jn(f"hand{s}")
    setb(f"hand.{side}", hw, hw + Vector((0.0, -0.055, 0.0)))
    # fingers straight from the old rig's finger bones
    fmap = {"index": "f_index", "middle": "f_middle", "ring": "f_ring",
            "pinky": "f_pinky", "thumb": "thumb"}
    for old_f, new_f in fmap.items():
        for seg in (1, 2, 3):
            if old_f == "thumb" and seg == 3:
                # old rig has 2 thumb segments; extend the 2nd for the 3rd
                h2, t2 = jn(f"finger_thumb_2{s}"), jt(f"finger_thumb_2{s}")
                setb(f"thumb.03.{side}", h2 + (t2 - h2) * 0.55, t2 + (t2 - h2) * 0.35)
                continue
            setb(f"{new_f}.{seg:02d}.{side}", jn(f"finger_{old_f}_{seg}{s}"), jt(f"finger_{old_f}_{seg}{s}"))
    # palm bones: hand head -> each finger base (thumb palm shares palm.01)
    for pi, f in enumerate(("index", "middle", "ring", "pinky"), start=1):
        setb(f"palm.{pi:02d}.{side}", hw, jn(f"finger_{f}_1{s}"))
    # legs
    setb(f"thigh.{side}", jn(f"thigh{s}"), jt(f"thigh{s}"))
    setb(f"shin.{side}",  jn(f"shin{s}"),  jt(f"shin{s}"))
    setb(f"foot.{side}",  jn(f"foot{s}"),  jt(f"foot{s}"))
    setb(f"toe.{side}",   jn(f"toe{s}"),   jt(f"toe{s}"))
    ank = jn(f"foot{s}")
    setb(f"heel.02.{side}", ank, Vector((ank.x, 0.045, 0.0)))
    setb(f"pelvis.{side}", jn("pelvis"), jn(f"thigh{s}"))
    setb(f"breast.{side}", Vector((jn("chest").x + (0.055 if side == "L" else -0.055), -0.055, 0.70)),
                           Vector((jn("chest").x + (0.055 if side == "L" else -0.055), -0.10, 0.70)))

# cape: Rigify spline-tentacle chain off the chest (its own IK rig)
cape_pts = [(0.0, 0.098, 0.750), (0.0, 0.108, 0.620), (0.0, 0.114, 0.490),
            (0.0, 0.118, 0.360), (0.0, 0.118, 0.230), (0.0, 0.112, 0.100)]
prev = eb["spine.003"]
for i in range(5):
    b = eb.new(f"cape.{i + 1:03d}")
    b.head, b.tail = Vector(cape_pts[i]), Vector(cape_pts[i + 1])
    b.parent = prev
    b.use_connect = i > 0
    prev = b
bpy.ops.object.mode_set(mode="POSE")
meta.pose.bones["cape.001"].rigify_type = "limbs.spline_tentacle"
log("metarig fitted; generating Rigify rig...")
_before = set(bpy.data.objects)
res = bpy.ops.pose.rigify_generate()
log("rigify_generate:", res)
_new = [o for o in bpy.data.objects if o not in _before and o.type == "ARMATURE"]
rig = _new[0] if _new else bpy.data.objects.get("rig")
log("generated rig object:", rig.name if rig else None)
rig.name = "CapeJones_Rigify"
meta.hide_render = True; meta.hide_viewport = True
for o in bpy.data.objects:
    if o.name.startswith("WGT-"):
        o.hide_render = True; o.hide_viewport = True
defs = [b.name for b in rig.data.bones if b.use_deform]
log("generated rig bones:", len(rig.data.bones), "deform:", len(defs))
cape_ctrls = [b.name for b in rig.data.bones if "cape" in b.name and not b.name.startswith(("DEF-", "ORG-", "MCH-"))]
log("cape controls:", cape_ctrls)

# ============================================================ weight transfer
SEG2 = {  # old bone -> (DEF proximal, DEF distal) split by projection
    "upperarm_L": ("DEF-upper_arm.L", "DEF-upper_arm.L.001"),
    "upperarm_R": ("DEF-upper_arm.R", "DEF-upper_arm.R.001"),
    "forearm_L": ("DEF-forearm.L", "DEF-forearm.L.001"),
    "forearm_R": ("DEF-forearm.R", "DEF-forearm.R.001"),
    "thigh_L": ("DEF-thigh.L", "DEF-thigh.L.001"),
    "thigh_R": ("DEF-thigh.R", "DEF-thigh.R.001"),
    "shin_L": ("DEF-shin.L", "DEF-shin.L.001"),
    "shin_R": ("DEF-shin.R", "DEF-shin.R.001"),
}
SIMPLE = {
    "spine_1": "DEF-spine.001", "spine_2": "DEF-spine.002", "chest": "DEF-spine.003",
    "neck_1": "DEF-spine.004", "neck_2": "DEF-spine.005", "head": "DEF-spine.006",
    "jaw": "DEF-jaw",
    "clavicle_L": "DEF-shoulder.L", "clavicle_R": "DEF-shoulder.R",
    "hand_L": "DEF-hand.L", "hand_R": "DEF-hand.R",
    "foot_L": "DEF-foot.L", "foot_R": "DEF-foot.R",
    "toe_L": "DEF-toe.L", "toe_R": "DEF-toe.R",
}
for side in ("L", "R"):
    for old_f, new_f in (("index", "f_index"), ("middle", "f_middle"), ("ring", "f_ring"), ("pinky", "f_pinky")):
        for seg in (1, 2, 3):
            SIMPLE[f"finger_{old_f}_{seg}_{side}"] = f"DEF-{new_f}.{seg:02d}.{side}"
    SIMPLE[f"finger_thumb_1_{side}"] = f"DEF-thumb.01.{side}"
    SIMPLE[f"finger_thumb_2_{side}"] = f"DEF-thumb.02.{side}"
CAPE_CENTERS = {"cape_1": 0.17, "cape_2": 0.5, "cape_3": 0.83}
CAPE_DEFS = [f"DEF-cape.{i:03d}" for i in range(1, 6)]
CAPE_T = [0.1, 0.3, 0.5, 0.7, 0.9]

def transfer(obj):
    me = obj.data
    old_groups = {g.name: g.index for g in obj.vertex_groups}
    per_vert = []
    for v in me.vertices:
        acc = {}
        cape_w = 0.0; cape_t = 0.0
        for g in v.groups:
            name = obj.vertex_groups[g.group].name
            w = g.weight
            if w <= 0.001:
                continue
            if name in CAPE_CENTERS:
                cape_w += w; cape_t += w * CAPE_CENTERS[name]
            elif name == "pelvis":
                acc["DEF-spine"] = acc.get("DEF-spine", 0) + w * 0.5
                tgt = "DEF-pelvis.L" if v.co.x >= 0 else "DEF-pelvis.R"
                acc[tgt] = acc.get(tgt, 0) + w * 0.5
            elif name in SEG2:
                h, t = J[name]
                axis = t - h
                tt = (v.co - h).dot(axis) / max(axis.length_squared, 1e-9)
                tt = min(max(tt, 0.0), 1.0)
                a, b = SEG2[name]
                acc[a] = acc.get(a, 0) + w * (1 - tt)
                acc[b] = acc.get(b, 0) + w * tt
            elif name in SIMPLE:
                acc[SIMPLE[name]] = acc.get(SIMPLE[name], 0) + w
        if cape_w > 0.001:
            ct = cape_t / cape_w
            for dn, c in zip(CAPE_DEFS, CAPE_T):
                share = max(0.0, 1.0 - abs(ct - c) / 0.22)
                if share > 0.01:
                    acc[dn] = acc.get(dn, 0) + cape_w * share
        per_vert.append(acc)
    # clear old groups, write new
    obj.vertex_groups.clear()
    buckets = {}
    for i, acc in enumerate(per_vert):
        for name, w in acc.items():
            if w <= 0.01:
                continue
            q = round(w / 0.02) * 0.02
            buckets.setdefault((name, q), []).append(i)
    for (name, q), idxs in buckets.items():
        vg = obj.vertex_groups.get(name) or obj.vertex_groups.new(name=name)
        vg.add(idxs, float(q), "REPLACE")
    # repoint armature modifier
    for md in obj.modifiers:
        if md.type == "ARMATURE":
            md.object = rig
    log("weights transferred:", obj.name, "groups:", len(obj.vertex_groups))

transfer(body)
transfer(sheet)

# drop the old rig + its cage (v3 scene file itself is never written)
for nm in ("BlenRigMdefCage",):
    ob = bpy.data.objects.get(nm)
    if ob:
        bpy.data.objects.remove(ob, do_unlink=True)
if old_rig.animation_data:
    old_rig.animation_data_clear()
bpy.data.objects.remove(old_rig, do_unlink=True)
if "DanceV3" in bpy.data.actions:
    bpy.data.actions.remove(bpy.data.actions["DanceV3"])
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(WORK, "rig_v4.blend"))
log("saved rig_v4.blend")
print("STAGE_A_DONE")
