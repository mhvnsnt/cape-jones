"""Stage export: living room -> stages/cape-house/living-room.glb (additive).

Exports the room WITHOUT the character (CapeJones_Rig/Body/Cape stay in the
show .blend; the stage is the empty room). Lights + emission materials included.
Never saves the .blend.

Usage: blender -b <living_room.blend> --python export_stage.py -- <out.glb>
"""
import bpy, sys

out = sys.argv[sys.argv.index("--") + 1:][0]

EXCLUDE = {"CapeJones_Rig", "CapeJones_Body", "CapeJones_Cape",
           "140_06", "showProofCam", "qa_cam_front", "qa_cam_side"}

# clear any animation (stage is static)
for o in bpy.data.objects:
    if o.type == 'ARMATURE' and o.animation_data:
        o.animation_data.action = None

sel = [o for o in bpy.data.objects
       if o.name not in EXCLUDE and not o.name.startswith("140_06")]
print(f"exporting {len(sel)} objects, excluded: "
      f"{sorted(o.name for o in bpy.data.objects if o.name in EXCLUDE)}")

bpy.ops.object.select_all(action='DESELECT')
for o in sel:
    o.select_set(True)
bpy.context.view_layer.objects.active = sel[0]

bpy.ops.export_scene.gltf(
    filepath=out, export_format='GLB', use_selection=True,
    export_animations=False, export_skins=False, export_morph=False,
    export_cameras=False, export_lights=True,
    export_image_format='AUTO')
print("STAGE_GLB:", out)
