#!/usr/bin/env python3
"""
pose_take3.py — SITTING REDO TAKE 3 (owner 2026-10-18 ~22:21 CDT).

Owner's spec (verbatim): "his elbows are bending but not his shoulders not his
fingers not his wrists he's doing like a robot stance like a H type of stance
it's bad his shoulders aren't bending he's not bending at the waist or hips
his knees are not bending enough his pelvis is not lowering enough his body
is not lowering into a sitting position and neither are his shoulders and arms"

Visual target: owner's Tripo sitting model — leaning BACK into the chair,
pelvis SUNK into the seat, knees ~90°, feet forward, one arm CROSSED over
torso, shoulders relaxed. v5 was bolt-upright H-stance: exactly what NOT to do.

Usage (inside Blender, living_room.blend open):
    blender -b 3d-assets/living_room.blend --python pose_take3.py -- <pose> <outdir> [views]

Poses: lounge (hero, Tripo match), leg_folded, lean_forward, shrug
views: comma list of front,threeq (default both)
NEVER writes over living_room.blend.
"""
import bpy, math, os, sys
from mathutils import Vector, Quaternion, Euler

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
POSE = argv[0] if argv else "lounge"
OUTDIR = argv[1] if len(argv) > 1 else "/home/hatch/workspace/sittake3-work/out"
VIEWS = argv[2].split(",") if len(argv) > 2 else ["front", "threeq"]
os.makedirs(OUTDIR, exist_ok=True)

# ---- helpers ----
def q(axis, deg):
    """quaternion for rotation of deg about bone-local axis x/y/z"""
    ax = {"x": (1,0,0), "y": (0,1,0), "z": (0,0,1)}[axis]
    return Quaternion(ax, math.radians(deg))

def q2(a1, d1, a2, d2):
    return q(a1, d1) @ q(a2, d2)

def q3(a1, d1, a2, d2, a3, d3):
    return q(a1, d1) @ q(a2, d2) @ q(a3, d3)

I = Quaternion((1,0,0,0))

def fingers(curl):
    """natural relaxed curl on all finger joints; curl in degrees"""
    d = {}
    for side in ("L", "R"):
        for f in ("index", "middle", "ring", "pinky"):
            d[f"finger_{f}_1_{side}"] = q("x", curl)
            d[f"finger_{f}_2_{side}"] = q("x", curl + 8)
            d[f"finger_{f}_3_{side}"] = q("x", curl + 4)
        d[f"finger_thumb_1_{side}"] = q3("x", curl*0.6, "z", 12 if side=="L" else -12, "y", 0)
        d[f"finger_thumb_2_{side}"] = q("x", curl*0.7)
    return d

# ---- pose definitions (bone-local quaternions; x = pitch) ----
POSES = {}

# HERO: leaning back, sunk in, right arm crossed over torso, knees ~90.
# NOTE (probe-verified): the FK spine controls (spine_fk_1..4, chest_fk) drive
# the torso — the deform bones (spine_1..4, chest) do NOT. -X = recline.
POSES["lounge"] = dict({
    "pelvis": q("x", -12),
    "spine_fk_1": q("x", -6), "spine_fk_2": q("x", -6),
    "spine_fk_3": q("x", -6), "spine_fk_4": q("x", -6),
    "chest_fk": q("x", -7),
    "neck_1": q("x", 8), "neck_2": q("x", 12), "head": q("x", 10),
    "clavicle_L": q("x", -6), "clavicle_R": q("x", -6),
    # RIGHT arm crossed over torso (probe: ux=-115 uz=25 fx=-55 puts hand
    # across lower chest/upper stomach, forward)
    "upperarm_fk_R": q2("x", -115, "z", 25),
    "forearm_fk_R": q("x", -55),
    "hand_fk_R": q("x", -15),
    # LEFT arm resting on thigh, elbow bent, wrist loose
    "upperarm_fk_L": q2("x", -80, "z", -10),
    "forearm_fk_L": q("x", -40),
    "hand_fk_L": q("x", -18),
    "thigh_fk_L": q2("x", -75, "z", 6),
    "thigh_fk_R": q2("x", -75, "z", -6),
    "shin_fk_L": q2("x", 70, "z", 3),
    "shin_fk_R": q2("x", 70, "z", -3),
    "foot_fk_L": q("x", -4), "foot_fk_R": q("x", -4),
}, **fingers(22))

# leg folded under (slight recline via FK spine)
POSES["leg_folded"] = dict({
    "pelvis": q("x", -8),
    "spine_fk_1": q("x", -4), "spine_fk_2": q("x", -4),
    "spine_fk_3": q("x", -4), "spine_fk_4": q("x", -4),
    "chest_fk": q("x", -5),
    "neck_1": q("x", 5), "neck_2": q("x", 7), "head": q("x", 6),
    "clavicle_L": q("x", -5), "clavicle_R": q("x", -5),
    "thigh_fk_R": q3("x", -70, "z", -30, "y", 0),
    "shin_fk_R": q("x", 110),
    "foot_fk_R": q("x", 15),
    "thigh_fk_L": q2("x", -78, "z", 8),
    "shin_fk_L": q("x", 72),
    "foot_fk_L": q("x", -4),
    "upperarm_fk_L": q2("x", -84, "z", -10),
    "forearm_fk_L": q("x", -42),
    "hand_fk_L": q("x", -18),
    "upperarm_fk_R": q2("x", -84, "z", 10),
    "forearm_fk_R": q("x", -42),
    "hand_fk_R": q("x", -18),
}, **fingers(26))

# lean forward pensive: deep forward bend via FK spine, elbows on knees
POSES["lean_forward"] = dict({
    "pelvis": q("x", 6),
    "spine_fk_1": q("x", 8), "spine_fk_2": q("x", 8),
    "spine_fk_3": q("x", 8), "spine_fk_4": q("x", 8),
    "chest_fk": q("x", 10),
    "neck_1": q("x", 12), "neck_2": q("x", 14), "head": q("x", 10),
    "clavicle_L": q("x", 8), "clavicle_R": q("x", 8),
    "thigh_fk_L": q2("x", -80, "z", 7),
    "thigh_fk_R": q2("x", -80, "z", -7),
    "shin_fk_L": q2("x", 68, "z", 3),
    "shin_fk_R": q2("x", 68, "z", -3),
    "foot_fk_L": q("x", -6), "foot_fk_R": q("x", -6),
    "upperarm_fk_L": q2("x", -110, "z", -6),
    "forearm_fk_L": q("x", -55),
    "hand_fk_L": q("x", -22),
    "upperarm_fk_R": q2("x", -110, "z", 6),
    "forearm_fk_R": q("x", -55),
    "hand_fk_R": q("x", -22),
}, **fingers(30))

# shrug: slight recline, arms up/out, palms up
POSES["shrug"] = dict({
    "pelvis": q("x", -8),
    "spine_fk_1": q("x", -3), "spine_fk_2": q("x", -3),
    "spine_fk_3": q("x", -3), "spine_fk_4": q("x", -3),
    "chest_fk": q("x", -4),
    "neck_1": q("x", 4), "neck_2": q("x", 6), "head": q2("x", 4, "z", 6),
    "clavicle_L": q2("x", -14, "z", -10),
    "clavicle_R": q2("x", -14, "z", 10),
    "thigh_fk_L": q2("x", -76, "z", 9),
    "thigh_fk_R": q2("x", -76, "z", -9),
    "shin_fk_L": q("x", 70), "shin_fk_R": q("x", 70),
    "foot_fk_L": q("x", -4), "foot_fk_R": q("x", -4),
    "upperarm_fk_L": q3("x", -95, "z", -28, "y", 0),
    "forearm_fk_L": q("x", -50),
    "hand_fk_L": q2("x", -10, "y", 25),
    "upperarm_fk_R": q3("x", -95, "z", 28, "y", 0),
    "forearm_fk_R": q("x", -50),
    "hand_fk_R": q2("x", -10, "y", -25),
}, **fingers(14))

assert POSE in POSES, f"unknown pose {POSE}"

# ---- scene setup ----
# The living room already contains the 94-bone rig + body + cape (scene wave).
# Use the existing ones — do NOT append (avoids .001 duplicates).
# CRITICAL: the scene rig has action pose_sit_normal applied. An applied action
# OVERWRITES direct bone rotation sets on evaluation. Clear it first, or the
# old stiff pose wins and the new pose never shows.
sc = bpy.context.scene
rig = bpy.data.objects.get("CapeJones_Rig")
assert rig, "CapeJones_Rig not in scene"
body = bpy.data.objects.get("CapeJones_Body")
cape = bpy.data.objects.get("CapeJones_Cape")
if cape:
    cape.hide_viewport = True; cape.hide_render = True
    print("cape hidden for sitting proof")
cage = bpy.data.objects.get("BlenRigMdefCage")
if cage:
    cage.hide_viewport = True; cage.hide_render = True
if rig.animation_data and rig.animation_data.action:
    print("clearing action:", rig.animation_data.action.name)
    rig.animation_data.action = None
# reset all bones to rest
for pb in rig.pose.bones:
    pb.rotation_mode = "QUATERNION"
    pb.rotation_quaternion = Quaternion((1,0,0,0))
    pb.location = (0,0,0)
    pb.scale = (1,1,1)
rig.location = (0, 0, 0); rig.rotation_euler = (0, 0, 0); rig.scale = (1, 1, 1)

# root placement (v5-proven: puts him in the chair)
root = rig.pose.bones.get("root")
root.location = (3.0600106716156006, -0.020069314166903496, -2.067213296890259)
root.rotation_quaternion = Quaternion((0.707, 0.0, -0.707, 0.0))

for bn, quat in POSES[POSE].items():
    pb = rig.pose.bones.get(bn)
    if pb is None:
        print("MISSING BONE:", bn); continue
    pb.rotation_quaternion = quat

bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get(); deps.update()

# placement correction: ankle -> z=0.064
arm_ev = rig.evaluated_get(deps)
ankle = None
for bn in ["ankle_L", "ankle_R", "foot_L", "foot_R"]:
    b = arm_ev.pose.bones.get(bn)
    if b: ankle = b; break
ankle_z = (rig.matrix_world @ ankle.head).z if ankle else 0.0
delta = 0.064 - ankle_z
if abs(delta) > 1e-6:
    root.location.z += delta
    print(f"root lift: ankle {ankle_z:.3f} -> 0.064 (delta {delta:+.3f})")
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()

arm_ev = rig.evaluated_get(deps)
pelvis = arm_ev.pose.bones.get("pelvis")
pelvis_z = (rig.matrix_world @ pelvis.head).z if pelvis else -1
print(f"VERIFY {POSE}: pelvis_z={pelvis_z:.3f} (seat ~0.36; lower = more sunk)")

# ---- cameras + stills ----
sc = bpy.context.scene
sc.render.resolution_x = 480
sc.render.resolution_y = 270
sc.render.resolution_percentage = 100
sc.cycles.samples = 4
vol = bpy.data.objects.get("VolumeBox_Room")
if vol:
    vol.hide_render = True
    print("volumetrics hidden for iteration (memory)")
ctarget = Vector((3.06, 2.067, 0.45))

def make_cam(name, loc):
    cd = bpy.data.cameras.new(name); cd.lens = 50
    co = bpy.data.objects.new(name, cd); sc.collection.objects.link(co)
    t = co.constraints.new(type="TRACK_TO")
    tgt = bpy.data.objects.new(name + "_tgt", None); sc.collection.objects.link(tgt)
    tgt.location = ctarget
    t.target = tgt; t.track_axis = "TRACK_NEGATIVE_Z"; t.up_axis = "UP_Y"
    co.location = loc
    return co

ALL_VIEWS = {"front": (3.06, -0.6, 1.1), "threeq": (1.4, 0.4, 1.3)}
for vname in VIEWS:
    loc = ALL_VIEWS[vname]
    cam = make_cam("sitcam_" + vname, loc)
    sc.camera = cam
    sc.render.filepath = os.path.join(OUTDIR, f"{POSE}_{vname}.png")
    bpy.ops.render.render(write_still=True)
    print("STILL:", sc.render.filepath)

print("TAKE3 DONE:", POSE)
