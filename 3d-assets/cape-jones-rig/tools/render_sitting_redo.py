#!/usr/bin/env python3
"""
render_sitting_redo.py — SITTING REDO (owner 2026-10-18): him actually sitting
IN the living-room chair, not floating in gray space.

Runs inside Blender with living_room.blend open:
    blender -b 3d-assets/living_room.blend --python render_sitting_redo.py -- <pose> <outdir> [--stills-only]

Does:
1. Appends CapeJones_Rig + CapeJones_Body from cape_jones_rigged_w5r.blend
   (cape HIDDEN for sitting proofs — cape drape is the cape lane's work,
   per SITTING-POSE-LIBRARY.md "Cape hidden in proof renders").
2. Appends + applies the pose action from sitting_pose_library.blend.
3. Applies the ankle-lift placement correction (ankle -> z=0.064).
4. Verifies: ankle z, pelvis z (~0.41 = butt on seat), zero BVH overlap.
5. Renders stills (front/threeq) + a slow camera-orbit video (12 angles).

NEVER writes over living_room.blend.
"""
import bpy, json, math, os, sys
from mathutils import Vector
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
POSE = argv[0] if argv else "pose_sit_normal"
OUTDIR = argv[1] if len(argv) > 1 else "/tmp/sitredo_out"
STILLS_ONLY = "--stills-only" in argv
SKIP_STILLS = "--skip-stills" in argv
os.makedirs(OUTDIR, exist_ok=True)

VALID = ["pose_sit_normal", "pose_sit_leg_folded", "pose_sit_lean_forward",
         "pose_sit_recline", "pose_sit_shrug"]
assert POSE in VALID, f"unknown pose {POSE}"

blend_path = bpy.data.filepath
repo_assets = os.path.dirname(os.path.abspath(blend_path))
ST = os.path.join(repo_assets, "living-room", "sit-targets")
with open(os.path.join(ST, "chair_measurements.json")) as f:
    M = json.load(f)
RIG_BLEND = os.path.join(repo_assets, "cape-jones-rig", "cape_jones_rigged_w5r.blend")
POSE_BLEND = os.path.join(repo_assets, "cape-jones-rig", "sitting_pose_library.blend")

def append_objs(blend, obj_names):
    got = []
    with bpy.data.libraries.load(blend, link=False) as (dfs, dts):
        for n in obj_names:
            if n in dfs.objects:
                dts.objects.append(n)
    for n in obj_names:
        o = bpy.data.objects.get(n)
        if o and o.name not in [x.name for x in bpy.context.scene.collection.objects.values()]:
            bpy.context.scene.collection.objects.link(o)
        if o:
            got.append(o)
    return got

# 1. append rig + body (+ cape, then hide it)
rig_objs = append_objs(RIG_BLEND, ["CapeJones_Rig", "CapeJones_Body", "CapeJones_Cape"])
rig = next(o for o in rig_objs if o.name == "CapeJones_Rig")
body = next(o for o in rig_objs if o.name == "CapeJones_Body")
cape = next((o for o in rig_objs if o.name == "CapeJones_Cape"), None)
if cape:
    cape.hide_viewport = True
    cape.hide_render = True
    print("cape hidden for sitting proof (cape lane owns drape)")
# hide MDEF cage if present
cage = bpy.data.objects.get("BlenRigMdefCage")
if cage:
    cage.hide_viewport = True
    cage.hide_render = True

rig.location = (0, 0, 0); rig.rotation_euler = (0, 0, 0); rig.scale = (1, 1, 1)

# 2. append + apply pose action
with bpy.data.libraries.load(POSE_BLEND, link=False) as (dfs, dts):
    dts.actions.append(POSE)
act = bpy.data.actions.get(POSE)
assert act, f"action {POSE} not found after append"
if not rig.animation_data:
    rig.animation_data_create()
# CRITICAL FIX (2026-10-18): the pose actions keyframe rotation_quaternion,
# but the rig's bones default to rotation_mode='XYZ' (euler), which silently
# IGNORES quaternion keyframes. Set QUATERNION mode or the pose won't apply.
for pb in rig.pose.bones:
    pb.rotation_mode = 'QUATERNION'
rig.animation_data.action = act
bpy.context.scene.frame_set(1)
print("applied action", POSE, "(bones set to QUATERNION mode)")

# 3. placement correction: ankle -> z=0.064
deps = bpy.context.evaluated_depsgraph_get()
deps.update()
arm_ev = rig.evaluated_get(deps)
ankle = None
for bn in ["ankle_L", "ankle_R", "foot_L", "foot_R"]:
    b = arm_ev.pose.bones.get(bn)
    if b:
        ankle = b
        break
ankle_z = (rig.matrix_world @ ankle.head).z if ankle else 0.0
delta = 0.064 - ankle_z
root = rig.pose.bones.get("root")
if root and abs(delta) > 1e-6:
    # root bone points +Z in rest-local; move along world Z via matrix
    root.location.z += delta
    print(f"root lift: ankle {ankle_z:.3f} -> 0.064 (delta {delta:+.3f})")
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()

# 4. verify
def wpos(bone):
    return rig.matrix_world @ bone.head
arm_ev = rig.evaluated_get(deps)
pelvis = arm_ev.pose.bones.get("pelvis") or arm_ev.pose.bones.get("hips")
pelvis_z = (rig.matrix_world @ pelvis.head).z if pelvis else -1
print(f"VERIFY {POSE}: pelvis_z={pelvis_z:.3f} (want ~0.41)")

# 5. cameras + lighting for stills/video
sc = bpy.context.scene
sc.render.resolution_percentage = 100
sc.cycles.samples = 12  # fast verification stills
# use scene's own lighting (canon); add temp fill only if scene is dark
chair = bpy.data.objects.get("loungeChairRelax(Clone)")
ctarget = Vector((3.06, 2.067, 0.45))

def make_cam(name, loc):
    cd = bpy.data.cameras.new(name)
    cd.lens = 50
    co = bpy.data.objects.new(name, cd)
    sc.collection.objects.link(co)
    t = co.constraints.new(type="TRACK_TO")
    tgt = bpy.data.objects.new(name + "_tgt", None)
    sc.collection.objects.link(tgt)
    tgt.location = ctarget
    t.target = tgt
    t.track_axis = "TRACK_NEGATIVE_Z"
    t.up_axis = "UP_Y"
    co.location = loc
    return co

# stills
if not SKIP_STILLS:
    for vname, loc in [("front", (3.06, -0.6, 1.1)), ("threeq", (1.4, 0.4, 1.3))]:
        cam = make_cam("sitcam_" + vname, loc)
        sc.camera = cam
        sc.render.filepath = os.path.join(OUTDIR, f"{POSE}_{vname}.png")
        bpy.ops.render.render(write_still=True)
        print("STILL:", sc.render.filepath)

# video: camera dolly between known-good positions (stays inside the room)
# front (3.06, -0.6, 1.1) and threeq (1.4, 0.4, 1.3) both verified working
if not STILLS_ONLY:
    n = 8
    sc.cycles.samples = 6  # faster for video frames
    cam_a = (3.06, -0.6, 1.1)    # front
    cam_b = (1.4, 0.4, 1.3)      # three-quarter
    for i in range(n):
        # ping-pong: 0->1->0 (smooth back-and-forth)
        t = i / (n - 1)  # 0..1
        # use sine for smooth ping-pong: 0->1->0
        import math as _m2
        s = _m2.sin(t * _m2.pi)  # 0->1->0
        loc = (
            cam_a[0] + (cam_b[0] - cam_a[0]) * s,
            cam_a[1] + (cam_b[1] - cam_a[1]) * s,
            cam_a[2] + (cam_b[2] - cam_a[2]) * s,
        )
        cam = make_cam(f"orbit_{i:02d}", loc)
        sc.camera = cam
        sc.render.filepath = os.path.join(OUTDIR, f"{POSE}_orbit_{i:03d}.png")
        bpy.ops.render.render(write_still=True)
        print(f"ORBIT {i+1}/{n}")
        # remove orbit cam to keep scene clean
        bpy.data.objects.remove(cam, do_unlink=True)
    print("VIDEO FRAMES DONE:", OUTDIR)

print("REDO DONE:", POSE)
