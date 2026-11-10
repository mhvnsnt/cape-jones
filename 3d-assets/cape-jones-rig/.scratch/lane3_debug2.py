"""Lane 3 debug2: compare data.bones head vs pose.bones head vs pose matrix."""
import bpy
import numpy as np

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
rig = bpy.data.objects["CapeJones_Rig"]
for bn in ["finger_index_1_L", "hand_L", "upperarm_fk_R"]:
    db = rig.data.bones[bn]
    pb = rig.pose.bones[bn]
    print(f"{bn}:")
    print(f"  data.bones.head = {np.round(np.array(db.head),4)}")
    print(f"  pose.bones.head = {np.round(np.array(pb.head),4)}")
    print(f"  pose matrix translation = {np.round(np.array((rig.matrix_world @ pb.matrix).translation),4)}")
    print(f"  bone.length = {db.length:.4f}")
print("armature pose_position:", rig.data.pose_position)
