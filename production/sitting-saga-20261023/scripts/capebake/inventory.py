import bpy, json

print("=== SCENE INVENTORY ===")
print("objects:")
for o in bpy.data.objects:
    info = {"name": o.name, "type": o.type}
    if o.type == 'MESH':
        info["verts"] = len(o.data.vertices)
        info["polys"] = len(o.data.polygons)
        info["vgroups"] = [g.name for g in o.vertex_groups]
        info["materials"] = [m.name if m else None for m in o.data.materials]
    info["modifiers"] = [(m.name, m.type) for m in o.modifiers]
    info["parent"] = o.parent.name if o.parent else None
    print(json.dumps(info))

print("\n=== CAPE-RELATED OBJECT DETAIL ===")
for o in bpy.data.objects:
    if 'cape' in o.name.lower():
        print(f"--- {o.name} ---")
        for m in o.modifiers:
            print(f"  modifier: {m.name} type={m.type}")
            if m.type == 'CLOTH':
                cs = m.settings
                print(f"    quality={cs.quality} mass={cs.mass} vertex_group_mass={cs.vertex_group_mass!r}")
                print(f"    tension_stiffness={cs.tension_stiffness} compression_stiffness={cs.compression_stiffness} shear_stiffness={cs.shear_stiffness} bending_stiffness={cs.bending_stiffness}")
                print(f"    air_damping={cs.air_damping} use_pressure={cs.use_pressure} use_sewing_springs={cs.use_sewing_springs}")
                print(f"    pin_stiffness={cs.pin_stiffness}")
                col = m.collision_settings
                print(f"    collision: quality={col.collision_quality} use_collision={col.use_collision} distance_min={col.distance_min} use_self_collision={col.use_self_collision} self_distance_min={col.self_distance_min}")
                pc = m.point_cache
                print(f"    point_cache: frame_start={pc.frame_start} frame_end={pc.frame_end} is_baked={pc.is_baked} is_outdated={pc.is_outdated}")
            if m.type == 'COLLISION':
                cs = m.collision_settings
                print(f"    collision pad: thickness_outer={cs.thickness_outer} thickness_inner={cs.thickness_inner} damping={cs.damping} friction={cs.cloth_friction if hasattr(cs,'cloth_friction') else '?'}")

print("\n=== COLLISION OBJECTS ===")
for o in bpy.data.objects:
    for m in o.modifiers:
        if m.type == 'COLLISION':
            print(f"  {o.name} has COLLISION modifier")

print("\n=== FRAME RANGE / ACTIONS ===")
sc = bpy.context.scene
print(f"frame range: {sc.frame_start}-{sc.frame_end}")
for o in bpy.data.objects:
    if o.animation_data and o.animation_data.action:
        print(f"  {o.name}: action={o.animation_data.action.name}")
print("\n=== RIG BONES (cape-relevant) ===")
for o in bpy.data.objects:
    if o.type == 'ARMATURE':
        print(f"armature {o.name}: {len(o.data.bones)} bones")
        for b in o.data.bones:
            if 'cape' in b.name.lower() or 'root' in b.name.lower() or 'spine' in b.name.lower() or 'neck' in b.name.lower():
                print(f"   bone: {b.name} parent={b.parent.name if b.parent else None}")
print("=== DONE ===")
