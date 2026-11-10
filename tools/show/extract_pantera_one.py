"""Extract ONE Pantera action (clean scene per clip, avoids multi-action export)."""
import bpy, os, sys
a = sys.argv[sys.argv.index("--")+1:]
SRC, DST, OUTDIR = a[0], a[1], a[2]
os.makedirs(OUTDIR, exist_ok=True)
bpy.context.scene.render.fps = 30
bpy.ops.import_scene.gltf(filepath="/home/hatch/workspace/rig-audit-2026-10-23/main/pantera-leopard-king.glb")
arm = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
for x in list(bpy.data.actions):
    if x.name != SRC: bpy.data.actions.remove(x)
act = bpy.data.actions[SRC]
act.name = DST  # show-convention action name, like idle.glb's show_idle
if not arm.animation_data: arm.animation_data_create()
arm.animation_data.action = act
bpy.ops.object.select_all(action='DESELECT')
arm.select_set(True); bpy.context.view_layer.objects.active = arm
out = os.path.join(OUTDIR, DST + ".glb")
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', use_selection=True,
    export_animations=True, export_frame_range=True, export_anim_single_armature=True,
    export_skins=True, export_morph=False, export_cameras=False, export_lights=False)
print("EXPORTED", out, os.path.getsize(out), "bytes; frames:", act.frame_range)
