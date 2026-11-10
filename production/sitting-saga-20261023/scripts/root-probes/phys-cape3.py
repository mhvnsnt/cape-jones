import bpy
from mathutils import Vector

print("=== STAGE 2B: CREATE CLOTH CAPE FROM SCRATCH ===")

# Remove the bad extraction
bad_cape = bpy.data.objects.get("CapeJones_Cape_Cloth")
if bad_cape:
    bpy.data.objects.remove(bad_cape, do_unlink=True)
    print("Removed bad cape extraction")

# Get posed bone positions for cape placement
rig = bpy.data.objects.get("CapeJones_Rig")
if not rig:
    print("ERROR: rig not found")
else:
    bpy.context.view_layer.update()
    # Get neck and shoulder positions (world space, posed)
    neck_bone = rig.pose.bones.get("neck_1") or rig.pose.bones.get("neck")
    clav_L = rig.pose.bones.get("clavicle_L")
    clav_R = rig.pose.bones.get("clavicle_R")
    
    if neck_bone:
        neck_pos = rig.matrix_world @ neck_bone.head
        print(f"Neck world pos: {tuple(round(v,3) for v in neck_pos)}")
    if clav_L and clav_R:
        clavL_pos = rig.matrix_world @ clav_L.head
        clavR_pos = rig.matrix_world @ clav_R.head
        print(f"Clavicle L: {tuple(round(v,3) for v in clavL_pos)}")
        print(f"Clavicle R: {tuple(round(v,3) for v in clavR_pos)}")
        shoulder_width = (clavL_pos - clavR_pos).length
        print(f"Shoulder width: {shoulder_width:.3f}")
