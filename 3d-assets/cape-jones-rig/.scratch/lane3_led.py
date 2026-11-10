"""Lane 3: THUMB LED BUTTON test. Creates remote prop, animates thumb press.
Creates 'led_press_R' action. Renders key frames."""
import bpy, numpy as np
from mathutils import Vector

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
bpy.context.view_layer.update()
sc.render.fps = 24

# --- create LED remote prop ---
# simple box remote with a button, positioned at R thumb
thumb_head = np.array(rig.pose.bones["finger_thumb_1_R"].head)
thumb_tail = np.array(rig.pose.bones["finger_thumb_2_R"].tail)
# remote body: box under the thumb (static in world space, hand doesn't move)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=Vector(thumb_head + np.array([0.015, 0.01, -0.040])))
remote = bpy.context.active_object
remote.name = "LED_Remote"
remote.scale = (0.045, 0.030, 0.015)
bpy.context.view_layer.update()
# button: small cylinder on top, bigger and clearly visible
bpy.ops.mesh.primitive_cylinder_add(radius=0.010, depth=0.008,
    location=Vector(thumb_head + np.array([0.015, 0.01, -0.028])))
btn = bpy.context.active_object
btn.name = "LED_Button"
print("REMOTE CREATED", flush=True)

# --- LED press action ---
act = bpy.data.actions.new("led_press_R")
rig.animation_data_create()
rig.animation_data.action = act
sc.frame_start = 1
sc.frame_end = 24

def set_thumb(x1, x2, frame):
    for bn, x in (("finger_thumb_1_R", x1), ("finger_thumb_2_R", x2)):
        pb = rig.pose.bones[bn]
        pb.rotation_mode = 'XYZ'
        pb.rotation_euler = (x, 0, 0)
        pb.keyframe_insert(data_path="rotation_euler", frame=frame)

# f1: thumb hovering above button
set_thumb(-0.2, -0.1, 1)
# f8: anticipation (thumb lifts slightly)
set_thumb(-0.05, 0.0, 8)
# f12: PRESS (thumb curls down onto button)
set_thumb(-0.9, -0.7, 12)
# f16: hold press
set_thumb(-0.9, -0.7, 16)
# f24: release back to hover
set_thumb(-0.2, -0.1, 24)

for fc in act.fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = 'BEZIER'

bpy.context.view_layer.update()
print("LED ACTION CREATED", flush=True)
bpy.ops.wm.save_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/.scratch/led_test.blend")
print("SAVED led_test.blend", flush=True)
