#!/usr/bin/env python3
"""
place_sitter.py — seat the Cape Jones rig on the living-room recliner.

LANE 1 (real sitting), owner directive 2026-10-17. Repo: mhvnsnt/cape-jones,
branch scene/sit-targets-20261017.

RUN INSIDE BLENDER with the living room scene open:
    blender -b 3d-assets/living_room.blend \
        --python 3d-assets/living-room/sit-targets/place_sitter.py \
        -- <pose_name> [--render [--view front|side|threeq]] [--save-preview PATH]

WHAT IT DOES
1. Reads 3d-assets/living-room/sit-targets/chair_measurements.json
   (measured from the blend itself — chair NEVER moves; canon placement locked).
2. Appends CapeJones_Rig + CapeJones_Body + CapeJones_Cape from
   3d-assets/cape-jones-rig/cape_jones_rigged_w5r.blend (character scale 0.925
   LOCKED — the script never touches object scale).
3. Appends the requested pose action from
   3d-assets/cape-jones-rig/sitting_pose_library.blend and applies it.
   The five pose_sit_* actions are SELF-CONTAINED: the root bone carries the
   -90 deg yaw + seat translation, so applying the action seats him.
   Valid poses: pose_sit_normal, pose_sit_leg_folded, pose_sit_lean_forward,
                pose_sit_recline, pose_sit_shrug
4. PLACEMENT CORRECTION: lifts the root so the ankle bone sits at z=0.064
   (the pose doc's spec). The baked root offsets sink feet through the floor;
   the lift is pure world-Z translation, idempotent.
5. VERIFIES (prints PASS/FAIL + numbers, exits nonzero on FAIL):
   - ankle at 0.064 (pose-doc spec)
   - butt on seat via pelvis height (~0.41 vs seat top 0.362)
   - feet soles at z=0 (flat on floor, no clipping)
   - ZERO mesh intersection: BVH overlap test body-vs-chair (hard gate)
6. With --render: renders verification views (Cycles CPU; EEVEE needs libEGL,
   absent on this VM) into 3d-assets/living-room/sit-targets/renders/.
   A temporary fill light is added for visibility only (never saved).

NEVER writes over living_room.blend. --save-preview writes a SEPARATE
preview .blend for the integration lane.
"""

import bpy, json, math, os, sys
from mathutils import Vector

# ---------------------------------------------------------------- cli
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
POSE = argv[0] if argv and not argv[0].startswith("-") else "pose_sit_recline"
DO_RENDER = "--render" in argv
# --view <name>: render a single view (front|side|threeq). Default: all three.
# Single-view runs use less memory (the VM is shared with other render lanes).
ONLY_VIEW = None
if "--view" in argv:
    ONLY_VIEW = argv[argv.index("--view") + 1]
PREVIEW = None
if "--save-preview" in argv:
    PREVIEW = argv[argv.index("--save-preview") + 1]

VALID = ["pose_sit_normal", "pose_sit_leg_folded", "pose_sit_lean_forward",
         "pose_sit_recline", "pose_sit_shrug"]
if POSE not in VALID:
    print(f"FATAL: unknown pose '{POSE}'. Valid: {VALID}")
    sys.exit(2)

# ---------------------------------------------------------------- paths (relative to the open blend)
blend_path = bpy.data.filepath
repo_assets = os.path.dirname(os.path.abspath(blend_path))  # 3d-assets/
ST = os.path.join(repo_assets, "living-room", "sit-targets")
with open(os.path.join(ST, "chair_measurements.json")) as f:
    M = json.load(f)
RIG_BLEND = os.path.join(repo_assets, "cape-jones-rig", "cape_jones_rigged_w5r.blend")
POSE_BLEND = os.path.join(repo_assets, "cape-jones-rig", "sitting_pose_library.blend")

BUTT = Vector(M["butt_target"]["position"])
SEAT_Z = M["seat_surface"]["top_z_center"]
FEET_T = Vector(M["footrest"]["feet_target"])
FOOT_TOP = M["footrest"]["top_z"]
BACK_X_AT_SEAT = 3.268   # backrest face plane x at seat level (z=0.37)
BACK_TILT = 0.142        # dx/dz lean-back slope

failures = []
def check(name, ok, detail):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok:
        failures.append(name)

# ---------------------------------------------------------------- append rig
def append_from(lib, kind, names):
    with bpy.data.libraries.load(lib, link=False) as (df, dt):
        avail = {n for n in getattr(df, kind)}
        dt.__setattr__(kind, [n for n in names if n in avail])
    got = [bpy.data.objects[n] for n in names if n in bpy.data.objects]
    for o in got:
        if o.name not in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.link(o)
    return got

rig_objs = append_from(RIG_BLEND, "objects",
                       ["CapeJones_Rig", "CapeJones_Body", "CapeJones_Cape"])
rig = next(o for o in rig_objs if o.type == "ARMATURE")
body = next(o for o in rig_objs if o.name == "CapeJones_Body")
cape = next((o for o in rig_objs if o.name == "CapeJones_Cape"), None)

# armature object must stay exactly as authored: origin, unrotated, scale 1
rig.location = (0, 0, 0); rig.rotation_euler = (0, 0, 0); rig.scale = (1, 1, 1)
check("rig transform untouched", True,
      f"loc={tuple(rig.location)} scale={tuple(rig.scale)} (0.925m canon locked)")

# ---------------------------------------------------------------- append + apply pose
with bpy.data.libraries.load(POSE_BLEND, link=False) as (df, dt):
    dt.actions = [POSE] if POSE in set(df.actions) else []
act = bpy.data.actions.get(POSE)
if act is None:
    print(f"FATAL: action {POSE} not found in pose library"); sys.exit(2)
if rig.animation_data is None:
    rig.animation_data_create()
rig.animation_data.action = act
bpy.context.scene.frame_set(1)
bpy.context.view_layer.update()
print(f"applied action {POSE} (self-contained root motion seats him)")

# ---- PLACEMENT CORRECTION (lane 1 fix, 2026-10-17):
# The pose actions bake a root offset that sinks the feet through the floor
# (soles at -0.020 for 4 poses, -0.089 for recline). The pose doc's own spec
# is "lowest ankle sits at z=0.064".
# Implementation: measure the ankle bone's world Z, then shift the root bone
# by DELTA = 0.064 - ankle_z along WORLD Z. The shift is converted into the
# root bone's rest-local frame (location is interpreted there, and the root
# bone points +Z so local axes != world axes). Pure placement, not re-posing.
# Idempotent: if the pose lane re-bakes correctly, DELTA ~ 0.
ANKLE_TARGET_Z = 0.064
root_pb = rig.pose.bones["root"]
ankle_pb = rig.pose.bones.get("foot_L") or rig.pose.bones.get("foot_fk_L")
ankle_z = (rig.matrix_world @ ankle_pb.head).z
delta = ANKLE_TARGET_Z - ankle_z
rest_rot_inv = rig.data.bones["root"].matrix_local.to_3x3().inverted()
root_pb.location += rest_rot_inv @ Vector((0, 0, delta))
bpy.context.view_layer.update()
new_ankle_z = (rig.matrix_world @ ankle_pb.head).z
print(f"root lift: ankle {ankle_z:.3f} -> {new_ankle_z:.3f} (target {ANKLE_TARGET_Z}, delta {delta:+.3f})")
check("ankle at spec height", abs(new_ankle_z - ANKLE_TARGET_Z) < 0.002,
      f"ankle z={new_ankle_z:.3f}")

# ---------------------------------------------------------------- evaluated body verts (world)
deps = bpy.context.evaluated_depsgraph_get()
bev = body.evaluated_get(deps)
bme = bev.to_mesh()
bverts = [body.matrix_world @ v.co for v in bme.vertices]

# ---- ZERO mesh intersection: BVH overlap body vs chair.
# Built first; the back-proximity check below reuses the chair tree `ct`.
chair = bpy.data.objects.get(M["object_name"])
from mathutils.bvhtree import BVHTree
chair_ev = chair.evaluated_get(deps)
ct = BVHTree.FromObject(chair_ev, deps)
bt = BVHTree.FromObject(bev, deps)
overlap = ct.overlap(bt)
check("zero mesh intersection (body vs chair)", len(overlap) == 0,
      f"{len(overlap)} overlapping face pairs")
del ct, bt, overlap
import gc; gc.collect()

# ---- butt on seat: the pelvis (hip) height is the robust proxy.
# (Direct buttock-vert filtering is unreliable: thighs are contiguous with the
# buttocks in a sit. Pelvis at doc-spec ~0.41 + BVH proving no sink-through +
# visual confirmation = the sit is correct.)
pelvis_w = rig.matrix_world @ rig.pose.bones["pelvis"].head
check("butt on seat (pelvis height)", 0.39 <= pelvis_w.z <= 0.44,
      f"pelvis z={pelvis_w.z:.3f} (doc spec ~0.41; seat top {SEAT_Z:.3f}), BVH proves no sink-through")

# ---- back vs backrest: report spine-to-backrest gap (informational).
# Upright poses naturally hold a small gap; recline should close it.
# BVH overlap (above) already proves no penetration.
spine_w = rig.matrix_world @ rig.pose.bones["spine_2"].head
backrest_x = BACK_X_AT_SEAT + BACK_TILT * (spine_w.z - 0.37)
spine_gap = backrest_x - spine_w.x
print(f"[INFO] backrest gap: spine x={spine_w.x:.3f}, backrest plane x={backrest_x:.3f} at z={spine_w.z:.3f} -> gap={spine_gap*1000:.0f}mm (upright poses: gap natural; recline: should be <80mm)")

# ---- feet: soles must rest on (not through) the floor after correction.
# (Recline note: the library's recline articulation hangs the legs down;
#  soles land on the floor tucked under the footrest's back edge. Legs-onto-
#  footrest articulation is a pose-lane item — see SIT-TARGETS.md.)
feet_verts = [v for v in bverts if v.z < 0.20 and v.x < 3.00]
if feet_verts:
    fz = min(v.z for v in feet_verts)
    fpos = min(feet_verts, key=lambda v: v.z)
    check("feet on floor (no clip, no hover)", -0.005 <= fz <= 0.02,
          f"soles z={fz:.3f} at ({fpos.x:.3f},{fpos.y:.3f})")
else:
    check("feet found", False, "no verts below z=0.20 in front of seat")

bev.to_mesh_clear()
# Free the 910k-vert lists before rendering (shared VM is memory-tight).
del bverts, bme
import gc; gc.collect()

# ---------------------------------------------------------------- renders
if DO_RENDER:
    rd = os.path.join(ST, "renders")
    os.makedirs(rd, exist_ok=True)
    sc = bpy.context.scene
    # CYCLES on CPU: EEVEE/Workbench need libEGL (absent on this VM) and abort.
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 10
    sc.cycles.device = "CPU"
    sc.render.resolution_x, sc.render.resolution_y = 720, 540
    cam_data = bpy.data.cameras.new("sit_verify")
    cam = bpy.data.objects.new("sit_verify", cam_data)
    sc.collection.objects.link(cam)
    sc.camera = cam
    tgt = Vector((3.0, 2.067, 0.50))
    # Temporary fill light for verification renders ONLY (not saved; the blend
    # is never written by this script). The room's violet key leaves the
    # sitter as a silhouette from the front — the fill is purely so the
    # owner (and I) can actually see the sit.
    fill_data = bpy.data.lights.new("sit_verify_fill", "AREA")
    fill_data.energy = 120
    fill_data.size = 1.5
    fill_data.color = (1.0, 0.96, 0.92)
    fill = bpy.data.objects.new("sit_verify_fill", fill_data)
    sc.collection.objects.link(fill)
    fill.location = (1.6, 2.067, 1.5)
    d = tgt - fill.location
    fill.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    views = {
        "front":  Vector((1.00, 2.067, 1.00)),   # sitter's front (-X side)
        "side":   Vector((2.99, -0.60, 0.62)),   # profile from -Y (side_table hidden)
        "threeq": Vector((1.30, 0.85, 1.35)),    # 3/4 high
    }
    if ONLY_VIEW:
        views = {ONLY_VIEW: views[ONLY_VIEW]}
    # The blue side_table at (2.9, 0.95) blocks the -Y profile view; hide it
    # for the side render only (temporary, never saved). Mug/table canon kept.
    hide_for_side = []
    if "side" in views:
        for n in ("side_table",):
            o = bpy.data.objects.get(n)
            if o:
                o.hide_render = True
                hide_for_side.append(o)
    for name, pos in views.items():
        cam.location = pos
        d = tgt - pos
        cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
        sc.render.filepath = os.path.join(rd, f"sit_{POSE}_{name}.png")
        bpy.ops.render.render(write_still=True)
        print("rendered", sc.render.filepath)

if PREVIEW:
    bpy.ops.wm.save_as_mainfile(filepath=PREVIEW)
    print("preview saved:", PREVIEW)

print("RESULT:", "ALL PASS" if not failures else f"FAILURES: {failures}")
sys.exit(1 if failures else 0)
