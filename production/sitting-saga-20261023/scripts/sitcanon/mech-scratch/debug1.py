import bpy

rrig = bpy.data.objects.get("recliner_rig")
rig = bpy.data.objects.get("CapeJones_Rig")
print("recline now:", rrig.get('recline'))
print("\n=== recliner_rig drivers ===")
ad = rrig.animation_data
if ad:
    for d in ad.drivers:
        print(f"  path={d.data_path} idx={d.array_index} expr='{d.driver.expression}' valid={d.driver.is_valid}")
        for v in d.driver.variables:
            for t in v.targets:
                print(f"    var {v.name} type={v.type} id={t.id.name if t.id else None} path='{t.data_path}'")
print("\n=== pose bone rotation modes ===")
for bname in ("root", "backrest", "footrest", "footrest_pad"):
    pb = rrig.pose.bones[bname]
    print(f"  {bname}: mode={pb.rotation_mode} euler={tuple(round(v,3) for v in pb.rotation_euler)}")

print("\n=== CapeJones_Rig new drivers ===")
if rig.animation_data:
    for d in rig.animation_data.drivers:
        if 'ik_leg' in d.data_path:
            print(f"  path={d.data_path} expr='{d.driver.expression}' valid={d.driver.is_valid}")
            for v in d.driver.variables:
                for t in v.targets:
                    print(f"    var {v.name} id={t.id.name if t.id else None} path='{t.data_path}'")
print("\n=== ReclinerFollow constraints ===")
for side in ("L", "R"):
    pb = rig.pose.bones[f"foot_ik_{side}"]
    for c in pb.constraints:
        print(f"  foot_ik_{side}: {c.name} [{c.type}] influence={c.influence:.3f} target={c.target.name if c.target else None}")

def pad_bbox(tag):
    dg = bpy.context.evaluated_depsgraph_get()
    pad = bpy.data.objects['recliner_footrest_pad']
    ev = pad.evaluated_get(dg)
    ws = [ev.matrix_world @ v.co for v in ev.data.vertices]
    print(f"  {tag}: pad world bbox x {min(v.x for v in ws):.3f}..{max(v.x for v in ws):.3f} z {min(v.z for v in ws):.3f}..{max(v.z for v in ws):.3f}")
    pb = rrig.pose.bones['footrest']
    evr = rrig.evaluated_get(dg)
    epb = evr.pose.bones['footrest']
    print(f"  {tag}: footrest bone euler (evaluated)={tuple(round(v,3) for v in epb.rotation_euler)} matrix translation={tuple(round(v,3) for v in epb.matrix.translation)}")

scene = bpy.context.scene
scene.frame_set(40)
print("\n--- set recline=0 ---")
rrig['recline'] = 0.0
bpy.context.view_layer.update()
pad_bbox("recline=0")
print("--- set recline=1 ---")
rrig['recline'] = 1.0
bpy.context.view_layer.update()
pad_bbox("recline=1 (view_layer.update)")
scene.frame_set(40)
pad_bbox("recline=1 (frame_set)")
print("raw pose bone euler now:", tuple(round(v, 3) for v in rrig.pose.bones['footrest'].rotation_euler))
print("=== DEBUG DONE ===")
