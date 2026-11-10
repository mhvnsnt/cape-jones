"""DROP HIM INTO THE CHAIR. Butt 0.370 -> 0.335 (3.5cm cushion compression).

Owner 2026-10-19: "you have him standing on his seat... just sit him down in
the chair with his back against the chair and his ass sitting on the fucking
cushion seat of the chair, that's literally it."

Method: shift pelvis location keyframes ONLY (pelvis is relative to root;
shifting root too would double the drop). Calibrate pelvis local axes ->
world numerically, convert the world-Z delta, apply to all 81 frames.
"""
import bpy
from mathutils import Matrix, Vector

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/sitcanon-work/scene_sit.blend")
scn = bpy.context.scene
rig = bpy.data.objects.get("CapeJones_Rig")
body = bpy.data.objects.get("CapeJones_Body")
pb = rig.pose.bones['pelvis']

TARGET_BUTT_Z = 0.335  # 3.5cm below seat top (0.370) = cushion compression
MID = 40
scn.frame_set(MID)
bpy.context.view_layer.update()

def butt_min_z():
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    bm = body.evaluated_get(deps)
    mesh = bm.to_mesh()
    gP = body.vertex_groups.get('pelvis').index
    gT = {body.vertex_groups.get(x).index for x in ('thigh_L', 'thigh_R') if body.vertex_groups.get(x)}
    zs = []
    for v in mesh.vertices:
        gs = {g.group for g in v.groups}
        if gP in gs or gs & gT:
            w = bm.matrix_world @ v.co
            if w.z < 0.6:
                zs.append(w.z)
    bm.to_mesh_clear()
    return min(zs) if zs else None

# MEASURE FIRST at posed state (do not touch bones before measuring)
cur_bz = butt_min_z()
print(f"CURRENT butt_min_z={cur_bz:.4f} target={TARGET_BUTT_Z}", flush=True)

# calibrate pelvis location axes -> world
def pelvis_head_world():
    bpy.context.view_layer.update()
    return (rig.matrix_world @ pb.head).copy()
pb.location = Vector((0, 0, 0))
bpy.context.view_layer.update()
p0 = pelvis_head_world()
Bcols = []
for i in range(3):
    e = Vector((0, 0, 0)); e[i] = 1.0
    pb.location = e
    bpy.context.view_layer.update()
    Bcols.append(pelvis_head_world() - p0)
Bpel = Matrix((Bcols[0], Bcols[1], Bcols[2])).transposed()
Binv = Bpel.inverted()

dz = TARGET_BUTT_Z - cur_bz
local_delta = Binv @ Vector((0, 0, dz))
print(f"dz={dz:.4f} local_delta={tuple(round(v, 4) for v in local_delta)}", flush=True)

# shift pelvis location keyframes ONLY
act = rig.animation_data.action
moved = 0
for fc in act.fcurves:
    if fc.data_path == 'pose.bones["pelvis"].location':
        for kp in fc.keyframe_points:
            kp.co.y += local_delta[fc.array_index]
            kp.handle_left.y += local_delta[fc.array_index]
            kp.handle_right.y += local_delta[fc.array_index]
            moved += 1
print(f"shifted {moved} pelvis keyframes", flush=True)

scn.frame_set(MID)
bpy.context.view_layer.update()
print(f"NEW butt_min_z={butt_min_z():.4f}", flush=True)
bpy.ops.wm.save_as_mainfile(filepath="/home/hatch/workspace/sitcanon-work/scene_sit_dropped.blend")
print("SAVED scene_sit_dropped.blend", flush=True)
