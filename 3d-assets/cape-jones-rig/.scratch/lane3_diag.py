"""Lane 3 definitive diagnostic on PRISTINE file: which space are pb.head in?"""
import bpy
import numpy as np

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
bpy.context.view_layer.update()
rig = bpy.data.objects["CapeJones_Rig"]
mesh = bpy.data.objects["CapeJones_Body"]
me = mesh.data
n = len(me.vertices)
print("current frame:", bpy.context.scene.frame_current)

bn = "finger_index_1_L"
db = rig.data.bones[bn]
pb = rig.pose.bones[bn]
print(f"{bn}:")
print("  data.bones.head (true rest):", np.round(np.array(db.head), 4))
print("  pose.bones.head           :", np.round(np.array(pb.head), 4))
print("  pose matrix translation   :", np.round(np.array((rig.matrix_world @ pb.matrix).translation), 4))

# depsgraph evaluated position of a vert known to be in the L index finger:
# find vert nearest to pose.bones.head in STORED coords
co = np.empty(n * 3, dtype=np.float64)
me.vertices.foreach_get("co", co)
P = co.reshape(n, 3)
h = np.array(pb.head)
d = np.linalg.norm(P - h, axis=1)
print("  nearest STORED vert to pose.bones.head: d =", round(d.min(), 4))

# and nearest stored vert to data.bones.head
h0 = np.array(db.head)
d0 = np.linalg.norm(P - h0, axis=1)
print("  nearest STORED vert to data.bones.head: d =", round(d0.min(), 4))

# finger weight census on pristine
vg_names = [v.name for v in mesh.vertex_groups]
finger_gids = {vg_names.index(b.name) for b in rig.pose.bones if b.name.startswith("finger_")}
cnt = 0
for v in me.vertices:
    for g in v.groups:
        if g.group in finger_gids and g.weight >= 0.005:
            cnt += 1
            break
print("pristine verts with finger w>=0.005:", cnt)

# how many stored verts within 8mm of pose-space finger segments?
def seg_dist(p, a, b):
    ab = b - a
    t = np.clip(((p - a) @ ab) / (ab @ ab), 0, 1)
    return np.linalg.norm(p - (a + t[:, None] * ab), axis=1)
dmin = np.full(n, 1e9)
for b in rig.pose.bones:
    if b.name.startswith("finger_"):
        a = np.array(b.head); t = np.array(b.tail)
        d = seg_dist(P, a, t)
        dmin = np.minimum(dmin, d)
print("pristine stored verts within 8mm of pose-space finger segs:", int((dmin <= 0.008).sum()))
print("within 20mm:", int((dmin <= 0.02).sum()))
