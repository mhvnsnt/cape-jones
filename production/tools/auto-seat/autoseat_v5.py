"""AUTO-SEAT v5 — direct fcurve edit (no frame_set loop).
v4 hung on per-frame frame_set. v5: directly offset the pelvis.location fcurve
points. No scene updates needed until the final verify + render.
"""
import bpy, os, time
from mathutils import Vector

WORKTREE = "/home/hatch/workspace/wt-autoseat"
IN_BLEND = os.path.join(WORKTREE, "production/tools/auto-seat/proof_sitting.blend")
PROOF_DIR = os.path.join(WORKTREE, "production/tools/auto-seat/proofs")
os.makedirs(PROOF_DIR, exist_ok=True)
STAMP = time.strftime("%Y%m%d_%H%M%S")

scn = bpy.context.scene
rig = bpy.data.objects.get("CapeJones_Rig")
body = bpy.data.objects.get("CapeJones_Body")
pb = rig.pose.bones['pelvis']

SEAT_C = Vector((3.05, 2.067, 0.230))
BUTT_Z = 0.210

act = rig.animation_data.action
print(f"action: {act.name}", flush=True)

# Find pelvis location fcurves
loc_fcurves = [fc for fc in act.fcurves if fc.data_path == 'pose.bones["pelvis"].location']
print(f"pelvis location fcurves: {len(loc_fcurves)}", flush=True)
for fc in loc_fcurves:
    print(f"  index {fc.array_index}: {len(fc.keyframe_points)} keys", flush=True)

# Load pelvis vert indices from file (precomputed)
with open("/tmp/pelvis_idx.txt") as f:
    PELVIS_IDX = list(map(int, f.read().strip().split(",")))
print(f"pelvis idx count: {len(PELVIS_IDX)}", flush=True)

# Measure current butt at frame 41 (need ONE update)
scn.frame_set(41)
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
pm = body.evaluated_get(deps); mesh = pm.to_mesh(); mw = pm.matrix_world
pts = [mw@mesh.vertices[i].co for i in PELVIS_IDX]
pm.to_mesh_clear()
s = Vector((0,0,0))
for p in pts: s += p
mean_butt = s / len(pts)
min_z = min(p.z for p in pts)
print(f"current: mean=({mean_butt.x:.3f},{mean_butt.y:.3f},{mean_butt.z:.3f}) min_z={min_z:.4f}", flush=True)

MEAN_Z_TGT = BUTT_Z + (mean_butt.z - min_z)
target = Vector((SEAT_C.x, SEAT_C.y, MEAN_Z_TGT))
delta_world = target - mean_butt
R = (rig.matrix_world @ pb.matrix).to_3x3()
delta_local = R.inverted() @ delta_world
print(f"delta_local: ({delta_local.x:.4f},{delta_local.y:.4f},{delta_local.z:.4f})", flush=True)

# Offset all pelvis.location keyframes by delta_local (no frame_set!)
for fc in loc_fcurves:
    d = delta_local[fc.array_index]
    for kp in fc.keyframe_points:
        kp.co.y += d
        kp.handle_left.y += d
        kp.handle_right.y += d
    fc.update()
print("fcurves offset", flush=True)

# Verify (one update)
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
pm = body.evaluated_get(deps); mesh = pm.to_mesh(); mw = pm.matrix_world
pts = [mw@mesh.vertices[i].co for i in PELVIS_IDX]
pm.to_mesh_clear()
s = Vector((0,0,0))
for p in pts: s += p
mean2 = s / len(pts)
min2 = min(p.z for p in pts)
print(f"after: mean=({mean2.x:.3f},{mean2.y:.3f},{mean2.z:.3f}) min_z={min2:.4f} target={BUTT_Z:.4f}", flush=True)

bpy.ops.wm.save_as_mainfile(filepath=IN_BLEND)
print("SAVED", flush=True)

# Render
scn.render.engine='CYCLES'; scn.cycles.samples=24
scn.render.resolution_x=960; scn.render.resolution_y=540; scn.render.resolution_percentage=100
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
