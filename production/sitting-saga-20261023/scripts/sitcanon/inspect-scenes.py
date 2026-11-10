import bpy

def inventory(tag):
    print(f"===== {tag} =====")
    sc = bpy.context.scene
    print("render:", sc.render.engine, "samples:", getattr(sc.cycles, 'samples', None),
          "res:", sc.render.resolution_x, sc.render.resolution_y, "@", sc.render.resolution_percentage,
          "camera:", sc.camera.name if sc.camera else None)
    print("frame range:", sc.frame_start, sc.frame_end)
    for ob in bpy.data.objects:
        mods = []
        for m in ob.modifiers:
            extra = ""
            if m.type == 'CLOTH':
                pc = m.point_cache
                extra = f" point_cache baked={pc.is_baked} frames={pc.frame_start}-{pc.frame_end}"
            mods.append(m.type + extra)
        print(f"OBJ {ob.name!r} type={ob.type} parent={ob.parent.name if ob.parent else None} "
              f"verts={len(ob.data.vertices) if ob.type=='MESH' else '-'} mods={mods}")
        if ob.type == 'ARMATURE':
            ad = ob.animation_data
            print(f"    action: {ad.action.name if ad and ad.action else None}")
        for k in ob.keys():
            print(f"    custom prop {k!r} = {ob[k]!r}")
    for cam in [o for o in bpy.data.objects if o.type == 'CAMERA']:
        print("CAMERA", cam.name, "loc", tuple(round(c, 3) for c in cam.location), "lens", cam.data.lens)

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/sitcanon-work/scene_recliner_mech.blend")
inventory("RECLINER_MECH")
bpy.context.scene.frame_set(40)
bpy.context.view_layer.update()
for ob in bpy.data.objects:
    if 'cape' in ob.name.lower() and ob.type == 'MESH':
        dg = bpy.context.evaluated_depsgraph_get()
        ev = ob.evaluated_get(dg)
        me = ev.to_mesh()
        import numpy as np
        arr = np.empty(len(me.vertices) * 3)
        me.vertices.foreach_get("co", arr)
        arr = arr.reshape(-1, 3)
        w = np.array([ev.matrix_world[i][3] for i in range(3)])
        print("MECH cape eval bbox local: min", arr.min(axis=0).round(3), "max", arr.max(axis=0).round(3))
        ev.to_mesh_clear()

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/sitcanon-work/scene_capebaked.blend")
inventory("CAPEBAKED")
bpy.context.scene.frame_set(40)
bpy.context.view_layer.update()
for ob in bpy.data.objects:
    if 'cape' in ob.name.lower() and ob.type == 'MESH':
        dg = bpy.context.evaluated_depsgraph_get()
        ev = ob.evaluated_get(dg)
        me = ev.to_mesh()
        import numpy as np
        arr = np.empty(len(me.vertices) * 3)
        me.vertices.foreach_get("co", arr)
        arr = arr.reshape(-1, 3)
        print("BAKED cape eval bbox local: min", arr.min(axis=0).round(3), "max", arr.max(axis=0).round(3))
        ev.to_mesh_clear()
print("INSPECT DONE")
