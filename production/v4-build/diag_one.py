import bpy, math
from mathutils import Vector, Quaternion, Matrix
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/_cj_v4_build/rig_v4.blend")
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rigify"]
RPB = rig.pose.bones
bpy.ops.import_anim.bvh(filepath="/home/hatch/workspace/_cj_v4_assets/bvh/61_03.bvh", target="ARMATURE", global_scale=1.0, frame_start=0, use_fps_scale=False, update_scene_fps=False, update_scene_duration=False)
src = next(o for o in bpy.data.objects if o.type == "ARMATURE" and o != rig)
SPB = src.pose.bones
def sw(name, f):
    sc.frame_set(f); bpy.context.view_layer.update()
    m = src.matrix_world @ SPB[name].matrix
    return m.to_translation().copy(), m.to_quaternion()
SRC_START, STEP = 1010, 5
# rest + stats (same math as solve_v4)
rp0, rq0 = sw("Hips", 0)
hips_pts, floor_min = [], 1e9
for k in range(-12, 96):
    sf = SRC_START + STEP * k
    hp, _ = sw("Hips", sf); hips_pts.append(hp)
    for n in ("LeftFoot", "RightFoot", "LeftToeBase", "RightToeBase"):
        floor_min = min(floor_min, sw(n, sf)[0].z)
hips_mean = sum(hips_pts, Vector()) / len(hips_pts)
# scale from height
zs = []
for n, pb in SPB.items():
    sc.frame_set(0); bpy.context.view_layer.update()
    zs.append((src.matrix_world @ pb.matrix).to_translation().z)
    zs.append((src.matrix_world @ pb.matrix @ Vector((0, pb.length, 0))).z)
SCALE = 0.925 / (max(zs) - min(zs))
def map_pos(p):
    v = Vector((p.x - hips_mean.x, p.y - hips_mean.y, p.z - floor_min))
    return Vector((v.x * SCALE * 0.6, v.y * SCALE * 0.6, v.z * SCALE))
print("hips_mean", tuple(round(x,2) for x in hips_mean), "floor", round(floor_min,2), "SCALE", round(SCALE,5))
K = 24; SF = SRC_START + STEP * K
for joint, ctrl in (("LeftHand", "hand_ik.L"), ("RightHand", "hand_ik.R"), ("Hips", "hips")):
    p, q = sw(joint, SF)
    rp, rq = sw(joint, 0)
    mapped = map_pos(p); rest_mapped = map_pos(rp)
    pb = RPB[ctrl]
    rest_p = pb.head.copy()
    des_p = mapped + (rest_p - rest_mapped)
    print(joint, "src@", SF, tuple(round(x,2) for x in p), "| mapped", tuple(round(x,3) for x in mapped),
          "| rest_mapped", tuple(round(x,3) for x in rest_mapped), "| ctrl rest head", tuple(round(x,3) for x in rest_p),
          "| DES_P", tuple(round(x,3) for x in des_p))
