"""AUTO-SEAT v4 — lightweight fix on v2 blend.
v2 has FK rotations baked (deform follows via constraints). Only the TRANSLATION
was wrong (root.location doesn't deform). Fix: animate pelvis.location (deform=True)
to place the butt at the measured seat. No FBX reimport, no proxy.
"""
import bpy, math, os, time
from mathutils import Vector, Quaternion

WORKTREE = "/home/hatch/workspace/wt-autoseat"
IN_BLEND = os.path.join(WORKTREE, "production/tools/auto-seat/proof_sitting.blend")
OUT_BLEND = os.path.join(WORKTREE, "production/tools/auto-seat/proof_sitting.blend")
PROOF_DIR = os.path.join(WORKTREE, "production/tools/auto-seat/proofs")
os.makedirs(PROOF_DIR, exist_ok=True)
STAMP = time.strftime("%Y%m%d_%H%M%S")

scn = bpy.context.scene
rig = bpy.data.objects.get("CapeJones_Rig")
body = bpy.data.objects.get("CapeJones_Body")
pb = rig.pose.bones['pelvis']

# measured constants (from v3 runs)
SEAT_C = Vector((3.05, 2.067, 0.230))
BUTT_Z = 0.210  # seat - compression
FLOOR_Z = 0.0

# Find the action (v2 baked)
act = rig.animation_data.action
print(f"action: {act.name if act else None}", flush=True)

# Measure current butt position at middle frame (frame 41)
scn.frame_set(41)
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
pm = body.evaluated_get(deps); mesh = pm.to_mesh(); mw = pm.matrix_world
gi = body.vertex_groups["pelvis"].index
pts = []
for v in mesh.vertices:
    for g in v.groups:
        if g.group == gi and g.weight > 0.6 and v.co.z < 0.5:
            pts.append(mw @ v.co)
            break
pm.to_mesh_clear()
s = Vector((0,0,0))
for p in pts: s += p
mean_butt = s / len(pts)
min_z = min(p.z for p in pts)
print(f"current: mean=({mean_butt.x:.3f},{mean_butt.y:.3f},{mean_butt.z:.3f}) min_z={min_z:.4f}", flush=True)

# Compute pelvis translation needed (in pelvis bone-local space)
# Target: mean at (SEAT_C.x, SEAT_C.y, BUTT_Z + (mean_z - min_z))
MEAN_Z_TGT = BUTT_Z + (mean_butt.z - min_z)
target = Vector((SEAT_C.x, SEAT_C.y, MEAN_Z_TGT))
delta_world = target - mean_butt
print(f"delta_world: ({delta_world.x:.3f},{delta_world.y:.3f},{delta_world.z:.3f})", flush=True)

# pelvis world rotation -> bone-local delta
R = (rig.matrix_world @ pb.matrix).to_3x3()
delta_local = R.inverted() @ delta_world
print(f"delta_local: ({delta_local.x:.3f},{delta_local.y:.3f},{delta_local.z:.3f})", flush=True)

# Apply to all frames (constant offset — the v2 animation has the motion)
# We need to ADD this delta to the existing pelvis.location keyframes
# For simplicity: set pelvis.location = delta_local on all frames (v2 had it at 0)
for f in range(1, 82):
    scn.frame_set(f)
    # pelvis.location might have v2 keyframes at 0; override
    pb.location = delta_local
    pb.keyframe_insert(data_path="location", frame=f)

# Verify at frame 41
scn.frame_set(41)
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
pm = body.evaluated_get(deps); mesh = pm.to_mesh(); mw = pm.matrix_world
pts = []
for v in mesh.vertices:
    for g in v.groups:
        if g.group == gi and g.weight > 0.6 and v.co.z < 0.6:
            pts.append(mw @ v.co)
            break
pm.to_mesh_clear()
s = Vector((0,0,0))
for p in pts: s += p
mean2 = s / len(pts)
min2 = min(p.z for p in pts)
print(f"after: mean=({mean2.x:.3f},{mean2.y:.3f},{mean2.z:.3f}) min_z={min2:.4f} target={BUTT_Z:.4f}", flush=True)

bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print("SAVED", flush=True)

# Render proofs
scn.render.engine='CYCLES'; scn.cycles.samples=24
scn.render.resolution_x=960; scn.render.resolution_y=540; scn.render.resolution_percentage=100
scn.frame_set(41); bpy.context.view_layer.update()
cam=scn.camera
def look_at(eye,target):
    d=Vector(target)-Vector(eye); cam.location=eye
    cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
    bpy.context.view_layer.update()
look_at((1.35,2.067,0.85),(3.05,2.067,0.45))
scn.render.filepath=os.path.join(PROOF_DIR,f"autoseat_front_{STAMP}.png")
bpy.ops.render.render(write_still=True); print("front rendered",flush=True)
look_at((1.75,1.15,1.15),(3.05,2.067,0.45))
scn.render.filepath=os.path.join(PROOF_DIR,f"autoseat_threeq_{STAMP}.png")
bpy.ops.render.render(write_still=True); print("threeq rendered",flush=True)
print("DONE",flush=True)
