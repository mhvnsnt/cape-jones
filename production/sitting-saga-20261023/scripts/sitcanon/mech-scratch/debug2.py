import bpy

def pad_state(tag, rrig, pad):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = pad.evaluated_get(dg)
    ws = [ev.matrix_world @ v.co for v in ev.data.vertices]
    evr = rrig.evaluated_get(dg)
    eul = evr.pose.bones['footrest'].rotation_euler
    print(f"  {tag}: footrest_euler=({eul.x:.3f},{eul.y:.3f},{eul.z:.3f}) pad x {min(v.x for v in ws):.3f}..{max(v.x for v in ws):.3f} z {min(v.z for v in ws):.3f}..{max(v.z for v in ws):.3f}")

print("=== A) STANDALONE RECLINER FILE ===")
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/sitcanon-work/mech-scratch/repo/3d-assets/living-room/recliner/recliner_rigged.blend")
rrig = bpy.data.objects['recliner_rig']
pad = bpy.data.objects['recliner_footrest_pad']
rrig['recline'] = 1.0
bpy.context.scene.frame_set(1)
pad_state("standalone recline=1", rrig, pad)

print("\n=== B) MY SCENE: manual pose test ===")
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/sitcanon-work/scene_recliner_mech.blend")
rrig = bpy.data.objects['recliner_rig']
pad = bpy.data.objects['recliner_footrest_pad']
scene = bpy.context.scene
scene.frame_set(40)
# is ReclinerMech in the view layer?
def find_lc(lc, name, depth=0):
    print("   " * depth + f"layercol {lc.name} exclude={lc.exclude} hide={lc.hide_viewport}")
    for ch in lc.children:
        find_lc(ch, name, depth + 1)
print("view layer collections:")
find_lc(bpy.context.view_layer.layer_collection, "ReclinerMech")
print("recliner_rig in view layer objects:", rrig.name in [o.name for o in bpy.context.view_layer.objects])
print("pad hide_viewport:", pad.hide_viewport, "rig hide_viewport:", rrig.hide_viewport)

rrig.pose.bones['footrest'].rotation_euler.y = -0.873
rrig.pose.bones['footrest_pad'].rotation_euler.y = 0.873
bpy.context.view_layer.update()
pad_state("manual pose", rrig, pad)
rrig.pose.bones['footrest'].rotation_euler.y = 0.0
rrig.pose.bones['footrest_pad'].rotation_euler.y = 0.0
bpy.context.view_layer.update()

print("\n=== C) driver re-set test: set recline then frame_set twice ===")
rrig['recline'] = 1.0
scene.frame_set(41)
scene.frame_set(40)
pad_state("recline=1 after frame_set", rrig, pad)
print("driver fcurve mute flags:", [(d.data_path, d.mute) for d in rrig.animation_data.drivers])
print("=== DEBUG2 DONE ===")
