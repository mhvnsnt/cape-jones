"""Test-pose renders v2: correct local axes."""
import bpy, os, math
from mathutils import Vector

TMP = os.path.expanduser('~/workspace/cj-rig-wt/.rig_tmp')
OUTDIR = os.path.expanduser('~/workspace/cj-rig-wt/3d-assets/cape-jones-rig/test-poses')
os.makedirs(OUTDIR, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=os.path.join(TMP, 'cj_direct.blend'))
scn = bpy.context.scene
char = bpy.data.objects['CapeJones_Body']
cape = bpy.data.objects['CapeJones_Cape']
arm = bpy.data.objects['CapeJones_Rig']

for o in bpy.data.objects:
    if 'Cage' in o.name or 'cage' in o.name:
        o.hide_render = True
        o.hide_viewport = True

# ensure active is visible before mode_set
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')
cam_data = bpy.data.cameras.new('TestCam')
cam = bpy.data.objects.new('TestCam', cam_data)
scn.collection.objects.link(cam)
cam.location = (0, -2.2, 0.55)
dir = Vector((0, 0, 0.45)) - cam.location
q = dir.to_track_quat('-Z', 'Y')
cam.rotation_euler = q.to_euler()
cam_data.lens = 50
scn.camera = cam

light_data = bpy.data.lights.new('TestLight', 'SUN')
light = bpy.data.objects.new('TestLight', light_data)
scn.collection.objects.link(light)
light.location = (1, -1, 2)
light_data.energy = 3.0
world = bpy.data.worlds.new('TestWorld')
world.use_nodes = True
world.node_tree.nodes['Background'].inputs[0].default_value = (0.7, 0.7, 0.7, 1)
world.node_tree.nodes['Background'].inputs[1].default_value = 1.0
scn.world = world

scn.render.engine = 'BLENDER_WORKBENCH'
scn.display.shading.light = 'MATCAP'
scn.render.resolution_x = 640
scn.render.resolution_y = 640
scn.render.resolution_percentage = 50

bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='POSE')

def reset_pose():
    for pb in arm.pose.bones:
        pb.rotation_mode = 'XYZ'
        pb.rotation_euler = (0, 0, 0)
        pb.location = (0, 0, 0)
    arm.pose.bones['root']['ik_arm_L'] = 0.0
    arm.pose.bones['root']['ik_arm_R'] = 0.0
    arm.pose.bones['root']['ik_leg_L'] = 0.0
    arm.pose.bones['root']['ik_leg_R'] = 0.0
    bpy.context.view_layer.update()

def render(name):
    scn.render.filepath = os.path.join(OUTDIR, name + '.png')
    bpy.ops.render.render(write_still=True)
    print('RENDERED', name)

D = math.radians
# 1. T-pose
reset_pose()
render('01_tpose')
# 2. Arms raised: upperarm_fk local X (+ for L, - for R to raise)
reset_pose()
arm.pose.bones['upperarm_fk_L'].rotation_euler = (D(80), 0, 0)
arm.pose.bones['upperarm_fk_R'].rotation_euler = (D(-80), 0, 0)
bpy.context.view_layer.update()
render('02_arms_raised')
# 3. Elbow 100deg: forearm_fk local Z (negative = forward for L)
reset_pose()
arm.pose.bones['forearm_fk_L'].rotation_euler = (0, 0, D(-100))
arm.pose.bones['forearm_fk_R'].rotation_euler = (0, 0, D(100))
bpy.context.view_layer.update()
render('03_elbow_100')
# 4. Knee 100deg: shin_fk local X positive (backward)
reset_pose()
arm.pose.bones['shin_fk_L'].rotation_euler = (D(100), 0, 0)
arm.pose.bones['shin_fk_R'].rotation_euler = (D(100), 0, 0)
bpy.context.view_layer.update()
render('04_knee_100')
# 5. Shoulder raise: clavicle local X (shrug up)
reset_pose()
arm.pose.bones['clavicle_L'].rotation_euler = (D(-20), 0, 0)
arm.pose.bones['clavicle_R'].rotation_euler = (D(20), 0, 0)
bpy.context.view_layer.update()
render('05_shoulder_raise')
# 6. Head turn: head local Z 45deg yaw
reset_pose()
arm.pose.bones['head'].rotation_euler = (0, 0, D(45))
bpy.context.view_layer.update()
render('06_head_turn')
# 7. Crouch
reset_pose()
for s in ('L', 'R'):
    arm.pose.bones[f'thigh_fk_{s}'].rotation_euler = (D(70), 0, 0)
    arm.pose.bones[f'shin_fk_{s}'].rotation_euler = (D(-90), 0, 0)
    arm.pose.bones[f'foot_fk_{s}'].rotation_euler = (D(20), 0, 0)
arm.pose.bones['root'].location = (0, 0, -0.25)
bpy.context.view_layer.update()
render('07_crouch')

print('ALL TEST POSES RENDERED')
