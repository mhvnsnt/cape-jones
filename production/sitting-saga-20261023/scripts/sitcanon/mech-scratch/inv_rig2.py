import bpy
from collections import Counter

rig = bpy.data.objects.get('CapeJones_Rig')
print("=== RIG CUSTOM PROPS ===")
print(" object keys:", list(rig.keys()))
for k in rig.keys():
    if k != '_RNA_UI':
        print(f"   {k} = {rig[k]}")
print(" armature keys:", list(rig.data.keys()))

print("\n=== DRIVER VARIABLES (leg + arm samples) ===")
ad = rig.animation_data
for d in ad.drivers:
    if 'thigh_L' in d.data_path or 'upperarm_L' in d.data_path:
        print(f" {d.data_path} expr='{d.driver.expression}'")
        for v in d.driver.variables:
            print(f"    var '{v.name}' type={v.type}")
            for t in v.targets:
                print(f"      target id={t.id} data_path='{t.data_path}'")

print("\n=== ACTION FCURVE TARGETS ===")
act = rig.animation_data.action
paths = Counter()
for fc in act.fcurves:
    dp = fc.data_path
    if 'pose.bones' in dp:
        bone = dp.split('"')[1] if '"' in dp else dp
        paths[bone] += 1
    else:
        paths[dp] += 1
for bone, cnt in sorted(paths.items()):
    print(f"   {bone}: {cnt} fcurves")

print("\n=== IK CONSTRAINT DETAILS ===")
for bname in ('shin_ik_L', 'shin_ik_R', 'forearm_ik_L', 'chest_fk'):
    pb = rig.pose.bones.get(bname)
    if not pb:
        continue
    for c in pb.constraints:
        if c.type == 'IK':
            print(f" {bname}: chain_count={c.chain_count} target={c.target.name if c.target else None} subtarget={c.subtarget}")
            print(f"    pole_target={c.pole_target.name if c.pole_target else None} pole_subtarget={c.pole_subtarget} pole_angle={c.pole_angle:.3f}")
            print(f"    use_rotation={c.use_rotation} iterations={c.iterations}")

print("\n=== IK BONE REST POSITIONS (armature space) ===")
for name in ('foot_ik_L','foot_L','toe_ik_L','knee_pole_L','foot_ik_R','foot_R','toe_ik_R','knee_pole_R','thigh_ik_L','shin_ik_L','thigh_fk_L','shin_fk_L'):
    b = rig.data.bones.get(name)
    if b:
        print(f"  {name}: head={tuple(round(v,3) for v in b.head_local)} tail={tuple(round(v,3) for v in b.tail_local)} parent={b.parent.name if b.parent else None} use_deform={b.use_deform}")

print("\n=== POSED POSITIONS AT FRAME 40 ===")
bpy.context.scene.frame_set(40)
bpy.context.view_layer.update()
for name in ('foot_L','foot_ik_L','shin_L','thigh_L','pelvis'):
    pb = rig.pose.bones.get(name)
    if pb:
        head = rig.matrix_world @ pb.head
        print(f"  {name}: world head={tuple(round(v,3) for v in head)}")
print("\n=== DONE ===")
