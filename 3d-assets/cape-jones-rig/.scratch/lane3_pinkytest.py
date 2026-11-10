"""Lane 3: does rotating pinky_1_R move its weighted verts? Numerical test."""
import bpy
import numpy as np

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
bpy.context.view_layer.update()
rig = bpy.data.objects["CapeJones_Rig"]
mesh = bpy.data.objects["CapeJones_Body"]
me = mesh.data
vg_names = [v.name for v in mesh.vertex_groups]

def eval_pos():
    deps = bpy.context.evaluated_depsgraph_get()
    ev = deps.objects.get(mesh.name).data
    co = np.empty(len(ev.vertices) * 3, dtype=np.float64)
    ev.vertices.foreach_get("co", co)
    return co.reshape(len(ev.vertices), 3)

# verts with pinky_1_R weight
gid = vg_names.index("finger_pinky_1_R")
idx = []
for v in me.vertices:
    for g in v.groups:
        if g.group == gid and g.weight >= 0.5:
            idx.append(v.index)
            break
idx = np.array(idx)
print(f"verts w>=0.5 to finger_pinky_1_R: {len(idx)}")

# check drivers/constraints on the bone
pb = rig.pose.bones["finger_pinky_1_R"]
print("constraints:", [c.type for c in pb.constraints])
print("rotation_mode before:", pb.rotation_mode)

P0 = eval_pos()
pb.rotation_mode = 'XYZ'
pb.rotation_euler = (-1.0, 0, 0)
bpy.context.view_layer.update()
print("rotation_euler after set:", tuple(pb.rotation_euler))
print("pose matrix translation:", np.round(np.array((rig.matrix_world @ pb.matrix).translation), 4))
P1 = eval_pos()
if len(idx) > 0:
    move = np.linalg.norm(P1[idx] - P0[idx], axis=1)
    print(f"mean vert movement: {move.mean():.6f}, max: {move.max():.6f}")
else:
    print("NO VERTS to test")
