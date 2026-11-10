"""Minimal render test."""
import bpy, os
print('START', flush=True)
TMP = os.path.expanduser('~/workspace/cj-rig-wt/.rig_tmp')
OUTDIR = os.path.expanduser('~/workspace/cj-rig-wt/3d-assets/cape-jones-rig/test-poses')
bpy.ops.wm.open_mainfile(filepath=os.path.join(TMP, 'cj_cape_sep.blend'))
print('LOADED', flush=True)
scn = bpy.context.scene
arm = bpy.data.objects['CapeJones_Rig']
# hide cage
for o in bpy.data.objects:
    if 'Cage' in o.name:
        o.hide_render = True
print('CAGE HIDDEN', flush=True)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='OBJECT')
print('OBJECT MODE', flush=True)
# simple camera
bpy.ops.object.camera_add(location=(0, -2.2, 0.55))
cam = bpy.context.object
scn.camera = cam
print('CAMERA', flush=True)
# workbench (minimal memory for pose verification)
scn.render.engine = 'BLENDER_WORKBENCH'
scn.display.shading.light = 'MATCAP'
scn.render.resolution_percentage = 25
scn.render.filepath = os.path.join(OUTDIR, 'test_min.png')
print('RENDERING', flush=True)
bpy.ops.render.render(write_still=True)
print('DONE', flush=True)
