import bpy

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/sitcanon-work/scene_recliner_mech.blend")
scene = bpy.context.scene
rrig = bpy.data.objects['recliner_rig']
pad = bpy.data.objects['recliner_footrest_pad']
scene.frame_set(40)

def pad_bbox(tag):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = pad.evaluated_get(dg)
    ws = [ev.matrix_world @ v.co for v in ev.data.vertices]
    print(f"  {tag}: pad x {min(v.x for v in ws):.3f}..{max(v.x for v in ws):.3f} z {min(v.z for v in ws):.3f}..{max(v.z for v in ws):.3f}")

rrig['recline'] = 1.0
bpy.context.view_layer.update()
pad_bbox("1) set + view_layer.update")
dg = bpy.context.evaluated_depsgraph_get()
dg.update()
pad_bbox("2) + dg.update()")
rrig.update_tag(refresh={'DATA'})
bpy.context.view_layer.update()
pad_bbox("3) + update_tag(DATA)")
scene.frame_set(39)
scene.frame_set(40)
pad_bbox("4) + frame_set 39->40")

print("\n=== tiny render at recline=1 ===")
scene.render.engine = 'CYCLES'
scene.cycles.samples = 1
scene.render.resolution_x = 64
scene.render.resolution_y = 64
scene.render.resolution_percentage = 100
cam = bpy.data.objects.get('MainCam')
scene.camera = cam
scene.render.filepath = "/home/hatch/workspace/sitcanon-work/mech-scratch/driver_test.png"
bpy.ops.render.render(write_still=True)
pad_bbox("5) after render")
print("raw footrest euler:", tuple(round(v, 3) for v in rrig.pose.bones['footrest'].rotation_euler))
print("=== DEBUG5 DONE ===")
