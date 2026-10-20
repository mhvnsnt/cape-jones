import bpy

print("=== MUG RIGID BODY ===")

mug = bpy.data.objects.get("okayest_hero_mug")
if mug:
    bpy.context.view_layer.objects.active = mug
    bpy.ops.object.select_all(action='DESELECT')
    mug.select_set(True)
    if mug.rigid_body:
        bpy.ops.rigidbody.object_remove()
    bpy.ops.rigidbody.object_add(type='ACTIVE')
    mug.rigid_body.collision_shape = 'CONVEX_HULL'
    mug.rigid_body.mass = 0.3
    mug.rigid_body.friction = 0.5
    mug.rigid_body.restitution = 0.1
    mug.rigid_body.use_start_deactivated = True
    print(f"ACTIVE: {mug.name} (sleeping)")

    # Parent handle and text
    for pname in ["mug_handle", "mug_text"]:
        p = bpy.data.objects.get(pname)
        if p:
            p.parent = mug
            p.matrix_parent_inverse = mug.matrix_world.inverted() @ p.matrix_world
            print(f"Parented {pname}")

bpy.ops.wm.save_as_mainfile(filepath="/home/hatch/workspace/sitcanon-work/scene_sit_phys.blend")
print("SAVED")
