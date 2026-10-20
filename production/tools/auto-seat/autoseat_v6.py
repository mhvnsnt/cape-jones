"""AUTO-SEAT v6 — direct pelvis placement (no fcurves, no loops).
Set pb.location directly, keyframe all frames via fcurve duplication (fast)."""
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

with open("/tmp/pelvis_idx.txt") as f:
    PELVIS_IDX = list(map(int, f.read().strip().split(",")))

def measure():
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    pm = body.evaluated_get(deps); mesh = pm.to_mesh(); mw = pm.matrix_world
    pts = [mw@mesh.vertices[i].co for i in PELVIS_IDX]
    pm.to_mesh_clear()
    s = Vector((0,0,0))
    for p in pts: s += p
    return s/len(pts), min(p.z for p in pts)

scn.frame_set(41)
mean_butt, min_z = measure()
print(f"current: mean=({mean_butt.x:.3f},{mean_butt.y:.3f},{mean_butt.z:.3f}) min_z={min_z:.4f}", flush=True)

MEAN_Z_TGT = BUTT_Z + (mean_butt.z - min_z)
target = Vector((SEAT_C.x, SEAT_C.y, MEAN_Z_TGT))
delta_world = target - mean_butt
# pelvis.location is in PARENT (root) space: world_delta = (M_world @ parent.matrix).rot @ local
par = pb.parent
Rpar = (rig.matrix_world @ par.matrix).to_3x3() if par else rig.matrix_world.to_3x3()
delta_local = Rpar.inverted() @ delta_world
print(f"delta_local: ({delta_local.x:.4f},{delta_local.y:.4f},{delta_local.z:.4f})", flush=True)

# Apply directly to pose (current frame)
pb.location += delta_local
bpy.context.view_layer.update()
mean2, min2 = measure()
print(f"after direct: mean=({mean2.x:.3f},{mean2.y:.3f},{mean2.z:.3f}) min_z={min2:.4f}", flush=True)

# If it worked, keyframe it for all frames by copying the fcurve
if abs(min2 - BUTT_Z) < 0.05:
    # Get current pelvis.location (after delta)
    new_loc = pb.location.copy()
    print(f"new pelvis.location: ({new_loc.x:.4f},{new_loc.y:.4f},{new_loc.z:.4f})", flush=True)
    # Set on all frames via direct fcurve point manipulation (fast, no frame_set)
    act = rig.animation_data.action
    for fc in act.fcurves:
        if fc.data_path == 'pose.bones["pelvis"].location':
            v = new_loc[fc.array_index]
            for kp in fc.keyframe_points:
                kp.co.y = v
                kp.handle_left.y = v
                kp.handle_right.y = v
            fc.update()
    print("keyframed all", flush=True)
    bpy.ops.wm.save_as_mainfile(filepath=IN_BLEND)
    print("SAVED", flush=True)
else:
    print("DIRECT FAILED - not saving", flush=True)

print("DONE", flush=True)
