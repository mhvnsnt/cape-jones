import bpy
from mathutils import Vector, Matrix

print("=== STAGE C: unslide moving parts + stow fold + shaped coupling ===")
SRC = "/home/hatch/workspace/sitcanon-work/mech-scratch/repo/3d-assets/living-room/recliner/recliner_rigged.blend"
OUT = "/home/hatch/workspace/sitcanon-work/scene_recliner_mech.blend"
rig = bpy.data.objects.get("CapeJones_Rig")
rrig = bpy.data.objects.get("recliner_rig")
scene = bpy.context.scene

def eval_update():
    rrig.update_tag(refresh={'DATA'})
    rig.update_tag(refresh={'DATA'})
    bpy.context.view_layer.update()

# --- 1. restore pad + link mesh verts from source (undo the slide on moving parts) ---
with bpy.data.libraries.load(SRC, link=False) as (df, dt):
    dt.objects = ['recliner_footrest_pad', 'recliner_footrest_link']
for tobj in [o for o in dt.objects if o is not None]:
    target = bpy.data.objects[tobj.name.rsplit('.', 1)[0]] if tobj.name.rsplit('.', 1)[-1].isdigit() else bpy.data.objects[tobj.name]
    assert len(tobj.data.vertices) == len(target.data.vertices), f"vert count mismatch {target.name}"
    for i, v in enumerate(tobj.data.vertices):
        target.data.vertices[i].co = v.co
    target.data.update()
    print(f"restored {target.name} verts from source ({len(tobj.data.vertices)})")
    mesh = tobj.data
    bpy.data.objects.remove(tobj, do_unlink=True)
    if mesh.users == 0:
        bpy.data.meshes.remove(mesh)

# --- 2. scan stow angle with recliner drivers muted ---
drv_fcurves = list(rrig.animation_data.drivers)
for d in drv_fcurves:
    d.mute = True
pb_shank = rrig.pose.bones['footrest']
pb_pad = rrig.pose.bones['footrest_pad']
pad = bpy.data.objects['recliner_footrest_pad']

def pad_bbox():
    eval_update()
    ws = [pad.matrix_world @ v.co for v in pad.data.vertices]
    return (min(v.x for v in ws), max(v.x for v in ws), min(v.z for v in ws), max(v.z for v in ws))

best = None
for sign in (1, -1):
    for deg in range(20, 80, 5):
        import math
        phi = sign * math.radians(deg)
        pb_shank.rotation_euler.y = phi
        pb_pad.rotation_euler.y = 0.0
        x0, x1, z0, z1 = pad_bbox()
        ok = x0 >= 2.85 and z1 <= 0.26 and z0 >= 0.004
        print(f"  phi={phi:+.3f} rad: pad x {x0:.3f}..{x1:.3f} z {z0:.3f}..{z1:.3f} {'OK' if ok else ''}")
        if ok and best is None:
            best = phi
    if best is not None:
        break
pb_shank.rotation_euler.y = 0.0
pb_pad.rotation_euler.y = 0.0
for d in drv_fcurves:
    d.mute = False
assert best is not None, "no stow angle satisfied the criteria"
STOW = best
print(f"STOW angle chosen: {STOW:+.4f} rad")

# --- 3. shaped driver expressions on the recliner bones ---
def set_driver(bone, expr):
    for d in rrig.animation_data.drivers:
        if d.data_path == f'pose.bones["{bone}"].rotation_euler':
            d.driver.type = 'SCRIPTED'
            d.driver.expression = expr
            print(f"  {bone}: {expr}")
            return
    raise RuntimeError(f"driver not found for {bone}")

deploy = "min(max((recline - 0.35) / 0.65, 0.0), 1.0)"
stowf = f"(1.0 - min(max(recline / 0.35, 0.0), 1.0))"
set_driver('footrest', f"{STOW:.4f} * {stowf} - 0.873 * {deploy}")
set_driver('footrest_pad', f"0.873 * {deploy}")
# backrest keeps repo expression: -0.454 * recline

# --- 4. shaped coupling drivers (ik_leg + ReclinerFollow influence) ---
couple = "min(max((recline - 0.3) / 0.7, 0.0), 1.0)"
for side in ("L", "R"):
    dp = f'pose.bones["root"]["ik_leg_{side}"]'
    for d in rig.animation_data.drivers:
        if d.data_path == dp:
            d.driver.type = 'SCRIPTED'
            d.driver.expression = couple
            print(f"  ik_leg_{side}: {couple}")
# constraint influence drivers live on the rig object's animation data
for d in rig.animation_data.drivers:
    if 'ReclinerFollow' in d.data_path:
        d.driver.type = 'SCRIPTED'
        d.driver.expression = couple
        print(f"  {d.data_path}: {couple}")

# --- 5. re-place empties against the TRUE deployed pad (recline=1) ---
scene.frame_set(40)
rrig['recline'] = 1.0
eval_update()
padw = [pad.matrix_world @ v.co for v in pad.data.vertices]
zmax = max(v.z for v in padw)
top = [v for v in padw if v.z > zmax - 0.02]
tcx = sum(v.x for v in top) / len(top)
tcy = sum(v.y for v in top) / len(top)
print(f"deployed pad: x {min(v.x for v in padw):.3f}..{max(v.x for v in padw):.3f} z ..{zmax:.3f}  top centroid ({tcx:.3f}, {tcy:.3f})")
pelvis_w = rig.matrix_world @ rig.pose.bones["pelvis"].head
for side in ("L", "R"):
    foot_w = rig.matrix_world @ rig.pose.bones[f"foot_fk_{side}"].head
    off_y = max(-0.09, min(0.09, foot_w.y - pelvis_w.y))
    desired = Vector((tcx - 0.10, tcy + off_y, zmax + 0.03))
    e = bpy.data.objects[f"FootPadTarget_{side}"]
    e.matrix_world = Matrix.Translation(desired)
    eval_update()
    print(f"  FootPadTarget_{side}: desired {tuple(round(v,3) for v in desired)} got {tuple(round(v,3) for v in e.matrix_world.translation)}")

rrig['recline'] = 0.0
eval_update()
x0 = min((pad.matrix_world @ v.co).x for v in pad.data.vertices)
print(f"pad front edge at recline=0: {x0:.3f} (target ~2.858)")
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT)
print("=== STAGE C DONE ===")
