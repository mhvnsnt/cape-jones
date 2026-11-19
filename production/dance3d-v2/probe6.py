import bpy, json
from mathutils import Vector

sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
body = bpy.data.objects["BodyR"]
pat = bpy.data.objects.get("CapePatches")
base_co = [tuple(v.co) for v in body.data.vertices]
cape_idx = [i for i, c in enumerate(base_co) if c[1] > 0.05 and c[2] < 0.66]
out = {}

def snap(tag):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    me = bpy.data.meshes.new_from_object(ev)
    zs = [me.vertices[i].co.z for i in cape_idx]
    xs = [me.vertices[i].co.x for i in cape_idx]
    info = {"cape_min_z": round(min(zs), 3), "cape_max_z": round(max(zs), 3),
            "cape_x_range": [round(min(xs), 3), round(max(xs), 3)],
            "hand_L": [round(v, 3) for v in (rig.matrix_world @ rig.pose.bones["hand_fk_L"].head)],
            "foot_L": [round(v, 3) for v in (rig.matrix_world @ rig.pose.bones["foot_fk_L"].head)],
            "pelvis_loc": [round(v, 3) for v in rig.pose.bones["pelvis"].location]}
    if pat is not None:
        pev = pat.evaluated_get(dg)
        pme = bpy.data.meshes.new_from_object(pev)
        if len(pme.vertices):
            pz = [v.co.z for v in pme.vertices]
            info["patch_z_range"] = [round(min(pz), 3), round(max(pz), 3)]
        bpy.data.meshes.remove(pme)
    bpy.data.meshes.remove(me)
    out[tag] = info

for f in (1, 5, 39):
    sc.frame_set(f)
    snap(f"frame{f}")
# isolate: zero the cape bones at frame 39
sc.frame_set(39)
for bn in ("cape_1", "cape_2", "cape_3"):
    rig.pose.bones[bn].rotation_euler = (0, 0, 0)
snap("f39_cape_zeroed")
# isolate: zero everything (rest pose) at frame 39
for pb in rig.pose.bones:
    pb.location = (0, 0, 0)
    pb.rotation_euler = (0, 0, 0)
    pb.scale = (1, 1, 1)
snap("f39_all_zeroed")
print("PROBE6_JSON_BEGIN")
print(json.dumps(out, indent=1))
print("PROBE6_JSON_END")
