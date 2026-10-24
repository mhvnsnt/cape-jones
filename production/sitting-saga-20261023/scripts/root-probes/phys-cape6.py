import bpy

print("=== APPEND CAPE AND SETUP CLOTH ===")

# Append cape from /tmp/cape_only.blend
with bpy.data.libraries.load("/tmp/cape_only.blend", link=False) as (data_from, data_to):
    data_to.objects = ["CapeJones_Cape"]

for ob in data_to.objects:
    if ob:
        bpy.context.scene.collection.objects.link(ob)
        print(f"Appended {ob.name}, verts={len(ob.data.vertices)}")

cape = bpy.data.objects.get("CapeJones_Cape")
if cape:
    # Add cloth modifier
    bpy.context.view_layer.objects.active = cape
    bpy.ops.object.select_all(action='DESELECT')
    cape.select_set(True)
    
    cloth_mod = cape.modifiers.new(name="Cloth", type='CLOTH')
    print("Cloth modifier added")
    
    # Cloth settings
    cloth = cloth_mod.settings
    cloth.pin_stiffness = 1.0
    # Set pin group
    cloth.vertex_group_mass = "cape_pin"
    
    # Collision settings (on modifier, not settings, in Blender 4.0)
    cloth_mod.collision_settings.collision_quality = 4
    cloth_mod.collision_settings.distance_min = 0.015
    
    # Material: silk preset-ish
    cloth.tension_stiffness = 15
    cloth.compression_stiffness = 15
    cloth.shear_stiffness = 5
    cloth.bending_stiffness = 0.5
    cloth.tension_damping = 5
    cloth.compression_damping = 5
    cloth.shear_damping = 5
    cloth.bending_damping = 0.5
    
    print("Cloth settings configured")

bpy.ops.wm.save_as_mainfile(filepath="/home/hatch/workspace/sitcanon-work/scene_sit_phys.blend")
print("SAVED")
