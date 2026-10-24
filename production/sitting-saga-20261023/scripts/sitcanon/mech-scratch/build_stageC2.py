import bpy
from mathutils import Vector, Matrix

print("=== STAGE C2: shaped coupling + target placement on deployed pad ===", flush=True)
OUT = "/home/hatch/workspace/sitcanon-work/scene_recliner_mech.blend"
rig = bpy.data.objects.get("CapeJones_Rig")
rrig = bpy.data.objects.get("recliner_rig")
scene = bpy.context.scene
pad = bpy.data.objects['recliner_footrest_pad']

def eval_update():
    rrig.update_tag(refresh={'DATA'})
    rig.update_tag(refresh={'DATA'})
    bpy.context.view_layer.update()

# --- 1. shaped coupling drivers: couple = clamp((recline-0.2)/0.6) ---
couple = "min(max((recline - 0.2) / 0.6, 0.0), 1.0)"
n = 0
for d in rig.animation_data.drivers:
    if 'ik_leg_' in d.data_path or 'ReclinerFollow' in d.data_path:
        d.driver.type = 'SCRIPTED'
        d.driver.expression = couple
        print(f"  {d.data_path} -> {couple}", flush=True)
        n += 1
print(f"coupling drivers shaped: {n} (expect 4)", flush=True)

# --- 2. place empties against the deployed pad at recline=1 ---
scene.frame_set(40)
rrig['recline'] = 1.0
eval_update()
padw = [pad.matrix_world @ v.co for v in pad.data.vertices]
zmax = max(v.z for v in padw)
top = [v for v in padw if v.z > zmax - 0.02]
front_x = min(v.x for v in top)
tcy = sum(v.y for v in top) / len(top)
print(f"deployed pad: x {min(v.x for v in padw):.3f}..{max(v.x for v in padw):.3f} zmax {zmax:.3f} top-front x {front_x:.3f} top cy {tcy:.3f}", flush=True)

pelvis_w = rig.matrix_world @ rig.pose.bones["pelvis"].head
for side in ("L", "R"):
    foot_w = rig.matrix_world @ rig.pose.bones[f"foot_fk_{side}"].head
    off_y = max(-0.09, min(0.09, foot_w.y - pelvis_w.y))
    desired = Vector((front_x - 0.02, tcy + off_y, zmax + 0.03))
    e = bpy.data.objects[f"FootPadTarget_{side}"]
    e.matrix_world = Matrix.Translation(desired)
    eval_update()
    print(f"  FootPadTarget_{side}: desired {tuple(round(v,3) for v in desired)} got {tuple(round(v,3) for v in e.matrix_world.translation)}", flush=True)

# --- 3. self-check: tracking + lift at recline=1, then back to 0 ---
def check(rec):
    rrig['recline'] = rec
    eval_update()
    res = {}
    for side in ("L", "R"):
        e = bpy.data.objects[f"FootPadTarget_{side}"].matrix_world.translation
        fik = rig.matrix_world @ rig.pose.bones[f"foot_ik_{side}"].head
        fdf = rig.matrix_world @ rig.pose.bones[f"foot_{side}"].head
        res[side] = (e, fik, fdf)
    return res

m1 = check(1.0)
m0 = check(0.0)
for side in ("L", "R"):
    e, fik, fdf = m1[side]
    print(f"recline=1 {side}: track_err={(e - fik).length*1000:.1f}mm deform_foot {tuple(round(v,3) for v in fdf)} lift dz={(fdf.z - m0[side][2].z)*1000:.1f}mm", flush=True)
rrig['recline'] = 0.0
eval_update()
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT, flush=True)
print("=== STAGE C2 DONE ===", flush=True)
