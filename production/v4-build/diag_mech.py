import bpy, math
from mathutils import Euler
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/_cj_v4_build/rig_v4.blend")
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rigify"]
RPB = rig.pose.bones
def show(tag):
    bpy.context.view_layer.update()
    print(tag, {n: tuple(round(x,3) for x in (rig.matrix_world @ RPB[n].head)) for n in ("DEF-spine.003","DEF-spine.004","DEF-spine.006","DEF-upper_arm.L")})
sc.frame_set(1)
show("REST      ")
pb = RPB["chest"]; pb.rotation_mode = "QUATERNION"
pb.rotation_quaternion = Euler((math.radians(35), 0, 0)).to_quaternion()
show("CHEST+35X ")
pb.rotation_quaternion = Euler((0, 0, 0)).to_quaternion()
pb = RPB["hips"]; pb.location = (0.15, 0, 0)
show("HIPS+0.15X")
pb.location = (0, 0, 0)
pb = RPB["neck"]; pb.rotation_mode = "QUATERNION"
pb.rotation_quaternion = Euler((math.radians(30), 0, 0)).to_quaternion()
show("NECK+30X  ")
# who drives DEF-spine.004?
for pb2 in RPB:
    if pb2.name in ("DEF-spine.004", "DEF-spine.005", "DEF-spine.006"):
        print(pb2.name, "parent:", pb2.parent.name if pb2.parent else None,
              "constraints:", [(c.type, getattr(getattr(c, 'target', None), 'name', ''), getattr(c, 'subtarget', '')) for c in pb2.constraints])
