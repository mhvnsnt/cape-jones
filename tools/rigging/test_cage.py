"""Test poses on CAGE only (lightweight, fast). Verifies rig deform."""
import bpy, os, math
print('START', flush=True)
TMP = os.path.expanduser('~/workspace/cj-rig-wt/.rig_tmp')
OUTDIR = os.path.expanduser('~/workspace/cj-rig-wt/3d-assets/cape-jones-rig/test-poses')
os.makedirs(OUTDIR, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=os.path.join(TMP, 'cj_clean.blend'))
print('LOADED', flush=True)
scn = bpy.context.scene
cage = bpy.data.objects['BlenRigMdefCage']
arm = bpy.data.objects['CapeJones_Rig']
# hide heavy meshes, show cage
for o in bpy.data.objects:
    if o.type == 'MESH' and o != cage:
        o.hide_render = True
        o.hide_viewport = True
    if o == cage:
        o.hide_render = False
        o.hide_viewport = False
print('VISIBILITY SET', flush=True)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.camera_add(location=(0, -2.2, 0.55))
cam = bpy.context.object
scn.camera = cam
# point camera at origin
from mathutils import Vector
dir = Vector((0, 0, 0.45)) - cam.location
cam.rotation_euler = dir.to_track_quat('-Z', 'Y').to_euler()
scn.render.engine = 'BLENDER_WORKBENCH'
scn.display.shading.light = 'MATCAP'
scn.render.resolution_x = 640
scn.render.resolution_y = 640
scn.render.resolution_percentage = 50
print('SCENE SET', flush=True)
# Note: arm.pose.bones accessible in OBJECT mode; no need for POSE mode ops
def reset_pose():
    for pb in arm.pose.bones:
        pb.rotation_mode = 'XYZ'
        pb.rotation_euler = (0, 0, 0)
        pb.location = (0, 0, 0)
    bpy.context.view_layer.update()
    print('RESET DONE', flush=True)
def render(name):
    scn.render.filepath = os.path.join(OUTDIR, 'cage_' + name + '.png')
    bpy.ops.render.render(write_still=True)
    print('RENDERED', name, flush=True)
D = math.radians
reset_pose(); render('01_tpose')
reset_pose()
arm.pose.bones['upperarm_fk_L'].rotation_euler = (D(80), 0, 0)
arm.pose.bones['upperarm_fk_R'].rotation_euler = (D(-80), 0, 0)
bpy.context.view_layer.update(); render('02_arms_raised')
reset_pose()
arm.pose.bones['forearm_fk_L'].rotation_euler = (0, 0, D(-100))
arm.pose.bones['forearm_fk_R'].rotation_euler = (0, 0, D(100))
bpy.context.view_layer.update(); render('03_elbow_100')
reset_pose()
arm.pose.bones['shin_fk_L'].rotation_euler = (D(100), 0, 0)
arm.pose.bones['shin_fk_R'].rotation_euler = (D(100), 0, 0)
bpy.context.view_layer.update(); render('04_knee_100')
reset_pose()
arm.pose.bones['head'].rotation_euler = (0, 0, D(45))
bpy.context.view_layer.update(); render('06_head_turn')
reset_pose()
for s in ('L', 'R'):
    arm.pose.bones[f'thigh_fk_{s}'].rotation_euler = (D(70), 0, 0)
    arm.pose.bones[f'shin_fk_{s}'].rotation_euler = (D(-90), 0, 0)
arm.pose.bones['root'].location = (0, 0, -0.25)
bpy.context.view_layer.update(); render('07_crouch')
print('ALL DONE', flush=True)
