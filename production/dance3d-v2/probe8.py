import bpy, json

D = 0.017453292519943295
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
sc.frame_set(1)

def zero_all():
    for pb in rig.pose.bones:
        pb.location = (0, 0, 0)
        pb.rotation_euler = (0, 0, 0)
        pb.scale = (1, 1, 1)

def meas():
    dg = bpy.context.evaluated_depsgraph_get()
    ev = rig.evaluated_get(dg)
    P = ev.pose.bones
    MW = ev.matrix_world
    return {
        "hand_R": [round(float(v), 3) for v in (MW @ P["hand_fk_R"].head)],
        "foot_R": [round(float(v), 3) for v in (MW @ P["foot_fk_R"].head)],
        "hand_L": [round(float(v), 3) for v in (MW @ P["hand_fk_L"].head)],
    }

out = {}
zero_all(); out["zero"] = meas()
for bone, ax, val in (("upperarm_fk_R", "x", 30), ("upperarm_fk_R", "z", 30),
                      ("thigh_fk_R", "z", -30), ("thigh_fk_R", "z", 30),
                      ("chest", "y", 20)):
    zero_all()
    pb = rig.pose.bones[bone]
    pb.rotation_mode = "XYZ"
    e = [0, 0, 0]; e["xyz".index(ax)] = val * D
    pb.rotation_euler = tuple(e)
    out[f"{bone}_{ax}{val}"] = meas()
print("PROBE8_BEGIN")
print(json.dumps(out, indent=1))
print("PROBE8_END")
