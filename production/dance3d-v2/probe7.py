import bpy, json
import numpy as np

D = 0.017453292519943295
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
body = bpy.data.objects["BodyR"]
sc.frame_set(1)
base_co = np.array([tuple(v.co) for v in body.data.vertices])
hem_idx = [i for i, c in enumerate(base_co) if c[1] > 0.05 and c[2] < 0.22]

def zero_all():
    for pb in rig.pose.bones:
        pb.location = (0, 0, 0)
        pb.rotation_euler = (0, 0, 0)
        pb.scale = (1, 1, 1)

def measure():
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    me = bpy.data.meshes.new_from_object(ev)
    hem = np.array([tuple(me.vertices[i].co) for i in hem_idx])
    bpy.data.meshes.remove(me)
    P = rig.pose.bones
    return {
        "hand_L": [round(float(v), 3) for v in (rig.matrix_world @ P["hand_fk_L"].head)],
        "foot_L": [round(float(v), 3) for v in (rig.matrix_world @ P["foot_fk_L"].head)],
        "head_tail": [round(float(v), 3) for v in (rig.matrix_world @ P["head"].tail)],
        "hem_cent": [round(float(v), 3) for v in hem.mean(axis=0)],
    }

out = {}
zero_all(); out["zero"] = measure()
for bone, tgt in (("upperarm_fk_L", "hand_L"), ("thigh_fk_L", "foot_L"), ("head", "head_tail")):
    for ax, val in (("x", 30), ("y", 30), ("z", 30)):
        zero_all()
        pb = rig.pose.bones[bone]
        pb.rotation_mode = "XYZ"
        e = [0, 0, 0]; e["xyz".index(ax)] = val * D
        pb.rotation_euler = tuple(e)
        out[f"{bone}_{ax}"] = measure()
for ax, val in (("x", 25), ("z", 25)):
    zero_all()
    pb = rig.pose.bones["cape_3"]
    pb.rotation_mode = "XYZ"
    e = [0, 0, 0]; e["xyz".index(ax)] = val * D
    pb.rotation_euler = tuple(e)
    out[f"cape_3_{ax}"] = measure()
print("PROBE7_BEGIN")
print(json.dumps(out, indent=1))
print("PROBE7_END")
