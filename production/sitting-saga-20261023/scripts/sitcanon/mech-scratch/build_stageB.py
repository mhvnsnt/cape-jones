import bpy
from mathutils import Vector, Matrix

print("=== STAGE B: PR #166 leg coupling ===")
OUT = "/home/hatch/workspace/sitcanon-work/scene_recliner_mech.blend"

rig = bpy.data.objects.get("CapeJones_Rig")
rrig = bpy.data.objects.get("recliner_rig")
assert rig and rrig, "rigs missing"
scene = bpy.context.scene
scene.frame_set(40)
bpy.context.view_layer.update()

# --- 1. snap foot_ik pose to FK foot pose at frame 40 (PR166 step 1) ---
for side in ("L", "R"):
    fik = rig.pose.bones[f"foot_ik_{side}"]
    ffk = rig.pose.bones[f"foot_fk_{side}"]
    fk_world = rig.matrix_world @ ffk.matrix
    fik.matrix = rig.matrix_world.inverted() @ fk_world
    print(f"snapped foot_ik_{side}")
bpy.context.view_layer.update()

# foot/pelvis world anchors at frame 40 (for L/R split of targets)
pelvis_w = rig.matrix_world @ rig.pose.bones["pelvis"].head
foot_w = {s: rig.matrix_world @ rig.pose.bones[f"foot_{s}"].head for s in ("L", "R")}
print("pelvis world:", tuple(round(v, 3) for v in pelvis_w))
for s in ("L", "R"):
    print(f"foot_{s} world:", tuple(round(v, 3) for v in foot_w[s]))

# --- 2. measure pad top at recline=1, place empties by desired world position ---
rrig['recline'] = 1.0
bpy.context.view_layer.update()
pad = bpy.data.objects['recliner_footrest_pad']
padw = [pad.matrix_world @ v.co for v in pad.data.vertices]
zmax = max(v.z for v in padw)
top = [v for v in padw if v.z > zmax - 0.02]
tcx = sum(v.x for v in top) / len(top)
tcy = sum(v.y for v in top) / len(top)
print(f"pad at recline=1: bbox x {min(v.x for v in padw):.3f}..{max(v.x for v in padw):.3f} "
      f"y {min(v.y for v in padw):.3f}..{max(v.y for v in padw):.3f} z {min(v.z for v in padw):.3f}..{zmax:.3f}")
print(f"pad top center: ({tcx:.3f}, {tcy:.3f}, {zmax:.3f})")

ANKLE_H = 0.065  # ankle joint height above support surface (measured from frame-40 stance)
for side in ("L", "R"):
    ename = f"FootPadTarget_{side}"
    empty = bpy.data.objects.get(ename)
    if not empty:
        empty = bpy.data.objects.new(ename, None)
        scene.collection.objects.link(empty)
    # move it into the ReclinerMech collection for tidiness
    mech = bpy.data.collections.get("ReclinerMech")
    if mech and ename not in mech.objects:
        for c in list(empty.users_collection):
            c.objects.unlink(empty)
        mech.objects.link(empty)
    off_y = foot_w[side].y - pelvis_w.y
    off_y = max(-0.09, min(0.09, off_y))
    desired = Vector((tcx, tcy + off_y, zmax + ANKLE_H))
    empty.parent = rrig
    empty.parent_type = 'BONE'
    empty.parent_bone = "footrest_pad"
    empty.matrix_parent_inverse = Matrix.Identity(4)
    empty.matrix_world = Matrix.Translation(desired)
    bpy.context.view_layer.update()
    got = empty.matrix_world.translation
    print(f"{ename}: desired {tuple(round(v,3) for v in desired)} got {tuple(round(v,3) for v in got)}")

rrig['recline'] = 0.0
bpy.context.view_layer.update()
for side in ("L", "R"):
    e = bpy.data.objects[f"FootPadTarget_{side}"]
    print(f"FootPadTarget_{side} at recline=0: {tuple(round(v,3) for v in e.matrix_world.translation)}")

# --- 3. ReclinerFollow Copy Location on foot_ik, influence <- recline (PR166 step 3) ---
for side in ("L", "R"):
    fik = rig.pose.bones[f"foot_ik_{side}"]
    for c in [c for c in fik.constraints if c.name == "ReclinerFollow"]:
        fik.constraints.remove(c)
    c = fik.constraints.new(type='COPY_LOCATION')
    c.name = "ReclinerFollow"
    c.target = bpy.data.objects[f"FootPadTarget_{side}"]
    c.influence = 0.0
    drv = c.driver_add("influence").driver
    drv.type = 'AVERAGE'
    var = drv.variables.new()
    var.name = "recline"
    var.type = 'SINGLE_PROP'
    var.targets[0].id = rrig
    var.targets[0].data_path = '["recline"]'
    print(f"ReclinerFollow on foot_ik_{side}")

# --- 4. ik_leg_L/R driven by recline (PR166 step 4) ---
for side in ("L", "R"):
    dp = f'pose.bones["root"]["ik_leg_{side}"]'
    if rig.animation_data:
        for d in list(rig.animation_data.drivers):
            if d.data_path == dp:
                rig.animation_data.drivers.remove(d)
    drv = rig.driver_add(dp).driver
    drv.type = 'AVERAGE'
    var = drv.variables.new()
    var.name = "recline"
    var.type = 'SINGLE_PROP'
    var.targets[0].id = rrig
    var.targets[0].data_path = '["recline"]'
    print(f"ik_leg_{side} driven by recline")

bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT)

# --- 5. self-check: foot_ik tracking + deform foot lift at recline 1 vs 0, frame 40 ---
def measure(rec):
    rrig['recline'] = rec
    bpy.context.view_layer.update()
    out = {}
    for side in ("L", "R"):
        e = bpy.data.objects[f"FootPadTarget_{side}"].matrix_world.translation
        fik = rig.matrix_world @ rig.pose.bones[f"foot_ik_{side}"].head
        fdf = rig.matrix_world @ rig.pose.bones[f"foot_{side}"].head
        out[side] = (e, fik, fdf)
    return out

m0 = measure(0.0)
m1 = measure(1.0)
for side in ("L", "R"):
    e, fik, fdf = m1[side]
    print(f"recline=1 {side}: empty {tuple(round(v,3) for v in e)} foot_ik {tuple(round(v,3) for v in fik)} "
          f"track_err={((e - fik).length)*1000:.1f}mm deform_foot {tuple(round(v,3) for v in fdf)}")
    e0, fik0, fdf0 = m0[side]
    print(f"recline=0 {side}: deform_foot {tuple(round(v,3) for v in fdf0)}  lift dz={(fdf.z - fdf0.z)*1000:.1f}mm")
rrig['recline'] = 0.0
bpy.context.view_layer.update()
print("=== STAGE B DONE ===")
