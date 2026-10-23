"""Lane 3 debug: where are rest verts relative to rest finger bones?"""
import bpy
import numpy as np

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
rig = bpy.data.objects["CapeJones_Rig"]
mesh = bpy.data.objects["CapeJones_Body"]
me = mesh.data
n = len(me.vertices)

co = np.empty(n * 3, dtype=np.float64)
me.vertices.foreach_get("co", co)
P = co.reshape(n, 3)
print("rest vert bbox: x", P[:,0].min(), P[:,0].max(), "y", P[:,1].min(), P[:,1].max(), "z", P[:,2].min(), P[:,2].max())

# finger bone REST positions (armature space)
for bn in ["finger_index_1_L", "finger_index_1_R", "hand_L", "hand_R"]:
    b = rig.data.bones[bn]
    h = np.array(b.head); t = np.array(b.tail)
    d = np.linalg.norm(P - h, axis=1)
    print(f"{bn}: rest head={np.round(h,3)} tail={np.round(t,3)} nearest_rest_vert_d={d.min():.4f}")

# are pose bones currently at rest?
for bn in ["finger_index_1_L", "hand_R"]:
    pb = rig.pose.bones[bn]
    m = np.array(pb.matrix)
    print(f"{bn} pose matrix == identity-ish: {np.allclose(m, np.eye(4), atol=1e-6)}")
    print("  matrix translation:", np.round(m[:3,3], 4))

# what is the CURRENT pose doing? check a few bones' rotation
for bn in ["upperarm_fk_R", "hand_R", "finger_index_1_R"]:
    pb = rig.pose.bones[bn]
    print(f"{bn} rotation_euler={tuple(round(v,3) for v in pb.rotation_euler)} loc={tuple(round(v,3) for v in pb.location)}")
