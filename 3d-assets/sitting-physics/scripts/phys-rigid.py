import bpy

print("=== RIGID BODY WORLD SETUP ===")

scene = bpy.context.scene

# Create rigid body world if not exists
if not scene.rigidbody_world:
    bpy.ops.rigidbody.world_add()
    print("Rigid body world created")
else:
    print("Rigid body world exists")

rbw = scene.rigidbody_world
rbw.point_cache.frame_start = 1
rbw.point_cache.frame_end = 250

# PASSIVE colliders: floor, tables, chair base
passive_names = ["Floor", "tableCoffee(Clone)", "side_table", "recliner_base"]
for oname in passive_names:
    ob = bpy.data.objects.get(oname)
    if ob:
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.select_all(action='DESELECT')
        ob.select_set(True)
        if ob.rigid_body:
            bpy.ops.rigidbody.object_remove()
        bpy.ops.rigidbody.object_add(type='PASSIVE')
        # Use mesh shape for accurate collisions
        ob.rigid_body.collision_shape = 'MESH'
        ob.rigid_body.collision_margin = 0.01
        print(f"PASSIVE: {oname}")

# ACTIVE: mug (can be knocked off table)
mug_parts = ["okayest_hero_mug", "mug_handle"]
# Join mug parts for a single rigid body (or keep separate?)
# For simplicity, make the main mug active, handle follows via parent
mug = bpy.data.objects.get("okayest_hero_mug")
if mug:
    bpy.context.view_layer.objects.active = mug
    bpy.ops.object.select_all(action='DESELECT')
    mug.select_set(True)
    if mug.rigid_body:
        bpy.ops.rigidbody.object_remove()
    bpy.ops.rigidbody.object_add(type='ACTIVE')
    mug.rigid_body.collision_shape = 'CONVEX_HULL'
    mug.rigid_body.mass = 0.3  # 300g mug
    mug.rigid_body.friction = 0.5
    mug.rigid_body.restitution = 0.1
    # Start sleeping so it's stable until hit
    mug.rigid_body.start_deactivated = True
    print(f"ACTIVE: {mug.name} (sleeping)")

# Parent handle to mug so they move together
handle = bpy.data.objects.get("mug_handle")
if handle and mug:
    handle.parent = mug
    handle.matrix_parent_inverse = mug.matrix_world.inverted() @ handle.matrix_world
    print("Handle parented to mug")

# Mug text also parented
mug_text = bpy.data.objects.get("mug_text")
if mug_text and mug:
    mug_text.parent = mug
    mug_text.matrix_parent_inverse = mug.matrix_world.inverted() @ mug_text.matrix_world
    print("Mug text parented")

bpy.ops.wm.save_as_mainfile(filepath="/home/hatch/workspace/sitcanon-work/scene_sit_phys.blend")
print("SAVED")
