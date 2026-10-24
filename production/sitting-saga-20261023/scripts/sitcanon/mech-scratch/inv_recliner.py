import bpy

print("=== FILE ===", bpy.data.filepath)
print("\n=== COLLECTIONS ===")
for col in bpy.data.collections:
    print(f"  {col.name} objects={[o.name for o in col.objects]} children={[c.name for c in col.children]}")
print(" scene collection children:", [c.name for c in bpy.context.scene.collection.children])

print("\n=== OBJECTS ===")
for ob in bpy.data.objects:
    mw = ob.matrix_world
    loc = tuple(round(v, 3) for v in mw.translation)
    rot = tuple(round(v, 3) for v in ob.rotation_euler)
    print(f"  {ob.name} [{ob.type}] parent={ob.parent.name if ob.parent else None} ptype={ob.parent_type} pbone={ob.parent_bone} loc={loc} rot_euler={rot}")
    if ob.type == 'MESH':
        ws = [mw @ v.co for v in ob.data.vertices]
        print(f"      verts={len(ws)} world bbox x {min(v.x for v in ws):.3f}..{max(v.x for v in ws):.3f} y {min(v.y for v in ws):.3f}..{max(v.y for v in ws):.3f} z {min(v.z for v in ws):.3f}..{max(v.z for v in ws):.3f}")
        print(f"      mats={[m.name if m else None for m in ob.data.materials]}")

arm = bpy.data.objects.get('recliner_rig')
if arm:
    print("\n=== RECLINER RIG ===")
    print("  custom props:", {k: arm[k] for k in arm.keys() if k != '_RNA_UI'})
    print("  animation:", arm.animation_data.action.name if arm.animation_data and arm.animation_data.action else None)
    for b in arm.data.bones:
        print(f"  bone {b.name}: parent={b.parent.name if b.parent else None} head={tuple(round(v,3) for v in b.head_local)} tail={tuple(round(v,3) for v in b.tail_local)}")
    print("  pose bone constraints:")
    for pb in arm.pose.bones:
        for c in pb.constraints:
            print(f"    {pb.name}: {c.name} [{c.type}]")
    print("  drivers:")
    if arm.animation_data:
        for d in arm.animation_data.drivers:
            vars_ = [(v.name, [(t.id.name if t.id else None, t.data_path) for t in v.targets]) for v in d.driver.variables]
            print(f"    {d.data_path} expr='{d.driver.expression}' vars={vars_}")
        act = arm.animation_data.action
        if act:
            print("  action fcurves:")
            for fc in act.fcurves:
                print(f"    {fc.data_path} range={tuple(round(v,1) for v in fc.frame_range)} keys={[(round(k.co.x,1), round(k.co.y,3)) for k in fc.keyframe_points]}")
print("\n=== DONE ===")
