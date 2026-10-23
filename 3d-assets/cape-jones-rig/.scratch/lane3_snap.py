"""Lane 3: FINGER SNAP animation test (R hand). Cartoony timing.
Creates 'snap_test' action (does not touch idle action). Renders key frames.
Snap: thumb+middle press (anticipation), middle flicks off (snap!), settle.
"""
import bpy, sys
from mathutils import Vector

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
sc = bpy.context.scene
rig = bpy.data.objects["CapeJones_Rig"]
bpy.context.view_layer.update()
sc.render.fps = 24

# new action for snap (keep idle action intact)
act = bpy.data.actions.new("snap_test_R")
rig.animation_data_create()
rig.animation_data.action = act
sc.frame_start = 1
sc.frame_end = 30

def set_finger(finger, side, x_angle, frame):
    """Set X rotation on all segments of a finger, keyframe it."""
    for pb in rig.pose.bones:
        if pb.name.startswith(f"finger_{finger}_") and pb.name.endswith("_" + side):
            pb.rotation_mode = 'XYZ'
            pb.rotation_euler = (x_angle, 0, 0)
            pb.keyframe_insert(data_path="rotation_euler", frame=frame)

def set_all(side, x_angle, frame, exclude=()):
    for pb in rig.pose.bones:
        if pb.name.startswith("finger_") and pb.name.endswith("_" + side):
            fname = pb.name.split("_")[1]
            if fname in exclude:
                continue
            pb.rotation_mode = 'XYZ'
            pb.rotation_euler = (x_angle, 0, 0)
            pb.keyframe_insert(data_path="rotation_euler", frame=frame)

# --- f1: open hand (rest) ---
set_all("R", 0.0, 1)

# --- f8: anticipation - fingers spread slightly, thumb+middle start coming together ---
# (slight extend for snap fingers, others start curling)
set_finger("thumb", "R", -0.3, 8)
set_finger("middle", "R", -0.4, 8)
set_finger("index", "R", -0.2, 8)
set_finger("ring", "R", -0.8, 8)
set_finger("pinky", "R", -0.8, 8)

# --- f14: PRESS - thumb+middle pressed together, others curled tight ---
set_finger("thumb", "R", -0.9, 14)
set_finger("middle", "R", -1.1, 14)  # middle curled to press thumb
set_finger("index", "R", -1.2, 14)
set_finger("ring", "R", -1.2, 14)
set_finger("pinky", "R", -1.2, 14)

# --- f16: SNAP! middle finger flicks out fast (2-frame snap) ---
set_finger("middle", "R", 0.8, 16)  # flicks to hyperextended (dramatic snap)
# thumb stays, others stay curled

# --- f22: follow-through, hand relaxes open ---
set_all("R", -0.1, 22)

# --- f30: settle to rest ---
set_all("R", 0.0, 30)

# set interpolation: snap needs SNAPPY (constant or fast bezier)
for fc in act.fcurves:
    for kp in fc.keyframe_points:
        # make the snap (f14->f16) sharp
        if kp.co.x in (14, 16):
            kp.interpolation = 'CONSTANT'
        else:
            kp.interpolation = 'BEZIER'

bpy.context.view_layer.update()
print("SNAP ACTION CREATED", flush=True)

# save to a test blend (don't overwrite the working file yet)
bpy.ops.wm.save_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/.scratch/snap_test.blend")
print("SAVED snap_test.blend", flush=True)
