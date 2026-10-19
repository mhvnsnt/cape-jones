import bpy
from mathutils import Vector, Matrix
rig = bpy.data.objects['CapeJones_Rig']
root = rig.pose.bones['root']
pb = rig.pose.bones['pelvis']
scn = bpy.context.scene
scn.frame_set(40); bpy.context.view_layer.update()

def root_world():
    bpy.context.view_layer.update()
    return (rig.matrix_world @ root.matrix).to_translation().copy()
def pelvis_world():
    bpy.context.view_layer.update()
    return (rig.matrix_world @ pb.head).copy()

# calibrate root
root.location = Vector((0,0,0)); r0 = root_world()
Acols = []
for i in range(3):
    e = Vector((0,0,0)); e[i] = 1.0
    root.location = e; Acols.append(root_world() - r0)
Aroot = Matrix((Acols[0], Acols[1], Acols[2])).transposed()
print("Aroot det:", round(Aroot.determinant(),3))
target_root = Vector((3.120, 2.067, 0.0))
root.location = Aroot.inverted() @ (target_root - r0)
print("root.loc set to:", tuple(round(v,3) for v in root.location))
print("root world now:", tuple(round(v,3) for v in root_world()))

# calibrate pelvis (root fixed)
pb.location = Vector((0,0,0)); p0 = pelvis_world()
Bcols = []
for i in range(3):
    e = Vector((0,0,0)); e[i] = 1.0
    pb.location = e; Bcols.append(pelvis_world() - p0)
Bpel = Matrix((Bcols[0], Bcols[1], Bcols[2])).transposed()
print("Bpel det:", round(Bpel.determinant(),3))
target_pel = Vector((3.120, 2.067, 0.389))
pb.location = Bpel.inverted() @ (target_pel - p0)
print("pelvis.loc set to:", tuple(round(v,3) for v in pb.location))
print("pelvis world now:", tuple(round(v,3) for v in pelvis_world()))

# bake to all frames
act = rig.animation_data.action
f0, f1 = int(act.frame_range[0]), int(act.frame_range[1])
rl, pl = root.location.copy(), pb.location.copy()
for f in range(f0, f1+1):
    root.location = rl; root.keyframe_insert(data_path="location", frame=f)
    pb.location = pl; pb.keyframe_insert(data_path="location", frame=f)
bpy.ops.wm.save_as_mainfile(filepath="/home/hatch/workspace/wt-mocapsit/proof/sitting_mocap.blend")
print("SAVED")
