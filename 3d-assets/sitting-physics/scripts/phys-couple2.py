import bpy
from mathutils import Vector, Matrix

print("=== BUILD RECLINER COUPLING ===")

rig = bpy.data.objects.get("CapeJones_Rig")
recliner_rig = bpy.data.objects.get("recliner_rig")

if not rig or not recliner_rig:
    print("ERROR: rigs not found")
else:
    bpy.context.view_layer.update()
    
    # STEP 1: Snap foot_ik to FK foot positions (no pop at recline=0)
    for side in ["L", "R"]:
        fik = rig.pose.bones.get(f"foot_ik_{side}")
        ffk = rig.pose.bones.get(f"foot_fk_{side}")
        if fik and ffk:
            # Get FK foot world matrix
            fk_world = rig.matrix_world @ ffk.matrix
            # Set IK to same (in rig space)
            fik.matrix = rig.matrix_world.inverted() @ fk_world
            print(f"Snapped foot_ik_{side} to FK position")
    
    bpy.context.view_layer.update()
    
    # STEP 2: Create target empties parented to pad bone
    pad_bone = recliner_rig.pose.bones.get("footrest_pad")
    for side, x_offset in [("L", -0.08), ("R", 0.08)]:
        ename = f"FootPadTarget_{side}"
        empty = bpy.data.objects.get(ename)
        if not empty:
            empty = bpy.data.objects.new(ename, None)
            bpy.context.scene.collection.objects.link(empty)
        
        # Parent to pad bone (Bone parenting)
        empty.parent = recliner_rig
        empty.parent_type = 'BONE'
        empty.parent_bone = "footrest_pad"
        
        # Offset: on top of pad, left/right for each foot
        # Pad is ~0.3 wide, feet should be ~0.16 apart
        empty.location = (x_offset, 0, 0.05)  # 5cm above pad center, offset sideways
        print(f"Created {ename} on pad bone")
    
    bpy.context.view_layer.update()
    
    # STEP 3: Add Copy Location to foot_ik from empties, driven by recline
    for side in ["L", "R"]:
        fik = rig.pose.bones.get(f"foot_ik_{side}")
        ename = f"FootPadTarget_{side}"
        if fik:
            # Remove existing if present
            for c in [c for c in fik.constraints if c.name == "ReclinerFollow"]:
                fik.constraints.remove(c)
            
            c = fik.constraints.new(type='COPY_LOCATION')
            c.name = "ReclinerFollow"
            c.target = bpy.data.objects.get(ename)
            c.influence = 0.0  # driven by recline
            
            # Add driver: influence = recline
            drv = c.driver_add("influence").driver
            drv.type = 'AVERAGE'
            var = drv.variables.new()
            var.name = "recline"
            var.type = 'SINGLE_PROP'
            var.targets[0].id = recliner_rig
            var.targets[0].data_path = '["recline"]'
            print(f"Added ReclinerFollow to foot_ik_{side}, driven by recline")
    
    # STEP 4: Drive ik_leg_L/R from recline
    for side in ["L", "R"]:
        root_bone = rig.pose.bones.get("root")
        if root_bone and f"ik_leg_{side}" in root_bone:
            # Add driver to ik_leg property
            # First, check if driver exists
            dp = f'pose.bones["root"]["ik_leg_{side}"]'
            # Remove existing driver if any
            if rig.animation_data:
                for d in list(rig.animation_data.drivers):
                    if d.data_path == dp:
                        rig.animation_data.drivers.remove(d)
            
            drv = rig.driver_add(dp).driver
            drv.type = 'AVERAGE'
            var = drv.variables.new()
            var.name = "recline"
            var.type = 'SINGLE_PROP'
            var.targets[0].id = recliner_rig
            var.targets[0].data_path = '["recline"]'
            print(f"ik_leg_{side} driven by recline")
    
    bpy.context.view_layer.update()
    print("=== COUPLING BUILT ===")

bpy.ops.wm.save_as_mainfile(filepath="/home/hatch/workspace/sitcanon-work/scene_sit_phys.blend")
print("SAVED")
