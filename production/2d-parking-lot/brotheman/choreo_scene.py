#!/usr/bin/env python3
"""BROTHERMAN test video choreo (scene), 120f / 5s / 24fps, SILENT.
  f1-24   idle, blink f12, Closed, fists
  f25-48  wave: arm up, Open hand, fingers + thumb wiggle, hair and
          bandana tails follow-through, Smile, Happy eyes
  f49-96  POINT LEFT at Cape Jones + the line: Point hand, mouth
          Open/Shout on the line, head lean, squash hit on the point
  f97-120 arm lowers, Smile, wink f100, Closed f113, blink f108
The line ("You just gotta motherfucking keep up with the Joneses,
brother.") is SILENT — voice is owner-gated. It is shown as an on-screen
speech card in the composite (ffmpeg), not in this render.
"""
import bpy

WD = "/home/hatch/workspace/_cape-jones-parking-lot-2d/brotheman"
bpy.ops.wm.open_mainfile(filepath=f"{WD}/brotheman-rig.blend")
scene = bpy.context.scene
arm = bpy.data.objects["BM_Rig"]
pb = arm.pose.bones


def rot(bone, frame, z):
    b = pb[bone]
    b.rotation_euler = (0, 0, z)
    b.keyframe_insert(data_path="rotation_euler", frame=frame)


def scl(bone, frame, sx, sy):
    b = pb[bone]
    b.scale = (sx, sy, 1.0)
    b.keyframe_insert(data_path="scale", frame=frame)


def hide(ob_name, frame, value):
    ob = bpy.data.objects[ob_name]
    ob.hide_render = value
    ob.keyframe_insert(data_path="hide_render", frame=frame)


def eye_scale(frame, sy):
    for n in ("P_Eye_Open_L", "P_Eye_Open_R"):
        ob = bpy.data.objects[n]
        ob.scale = (1.0, sy, 1.0)
        ob.keyframe_insert(data_path="scale", frame=frame)


MOUTHS = ["Mouth_Closed", "Mouth_Smile", "Mouth_Grin", "Mouth_Open", "Mouth_Shout", "Mouth_Frown"]


def mouth(frame, active):
    for m in MOUTHS:
        hide(f"P_{m}", frame, m != active)


def eyes(frame, state):
    hide("P_Eye_Open_L", frame, state in ("happy", "wink"))
    hide("P_Eye_Open_R", frame, state == "happy")
    hide("P_Eye_Happy_L", frame, state == "open")
    hide("P_Eye_Happy_R", frame, state in ("open", "wink"))


# ---- blinks ------------------------------------------------------------------
for f0 in (12, 108):
    eye_scale(f0 - 1, 1.0)
    eye_scale(f0, 0.1)
    eye_scale(f0 + 2, 1.0)

# ---- wave --------------------------------------------------------------------
for f, z in [(1, 0.0), (25, 0.0), (36, -1.95), (44, -2.05), (48, -1.95)]:
    rot("upperArmR", f, z)
for f, z in [(1, 0.0), (36, -0.30), (48, -0.30)]:
    rot("forearmR", f, z)
for f, z in [(36, 0.0), (40, 0.35), (44, -0.30), (48, 0.0)]:
    rot("handR", f, z)
for i in (1, 2, 3, 4):
    for f, z in [(36, 0.0), (40, 0.25 if i % 2 else -0.20),
                 (44, -0.20 if i % 2 else 0.25), (48, 0.0)]:
        rot(f"fingerR{i}", f, z)
for f, z in [(36, 0.0), (42, 0.30), (48, 0.0)]:
    rot("thumbR", f, z)
for f, z in [(25, 0.0), (38, -0.18), (46, 0.15), (52, 0.0)]:
    rot("hair", f, z)
for f, z in [(25, 0.0), (40, -0.30), (48, 0.25), (54, 0.0)]:
    rot("bandanaTail", f, z)
eyes(1, "open")
eyes(36, "happy")
eyes(49, "open")
mouth(1, "Mouth_Closed")
mouth(25, "Mouth_Smile")

# ---- point + line --------------------------------------------------------------
for f, z in [(48, -1.95), (55, -1.22), (96, -1.22), (104, -0.40), (112, 0.0)]:
    rot("upperArmR", f, z)
for f, z in [(48, -0.30), (55, -0.05), (96, -0.05), (112, 0.0)]:
    rot("forearmR", f, z)
for f, z in [(55, 0.0), (60, 0.12), (96, 0.12), (112, 0.0)]:
    rot("handR", f, z)
for f, z in [(48, 0.0), (60, -0.10), (96, -0.10), (112, 0.0)]:
    rot("head", f, z)
for f, z in [(48, 0.0), (60, -0.04), (96, -0.04), (112, 0.0)]:
    rot("torso", f, z)
# squash hit on the point, recover
for f, sx, sy in [(48, 1.0, 1.0), (55, 1.06, 0.94), (62, 1.0, 1.0)]:
    scl("torso", f, sx, sy)
# hair/tails swing on the point
for f, z in [(55, 0.0), (62, 0.20), (72, -0.12), (84, 0.06), (96, 0.0)]:
    rot("hair", f, z)
for f, z in [(55, 0.0), (64, 0.35), (74, -0.18), (86, 0.08), (96, 0.0)]:
    rot("bandanaTail", f, z)
# talking mouths on the line
mouth(49, "Mouth_Open")
mouth(55, "Mouth_Shout")
mouth(61, "Mouth_Open")
mouth(67, "Mouth_Shout")
mouth(73, "Mouth_Open")
mouth(79, "Mouth_Shout")
mouth(85, "Mouth_Open")
mouth(91, "Mouth_Grin")
mouth(97, "Mouth_Smile")
mouth(113, "Mouth_Closed")
eyes(100, "wink")
eyes(108, "open")

# ---- hand swaps ----------------------------------------------------------------
for kind in ("Fist", "Open", "Point"):
    hide(f"P_HandR_{kind}", 1, kind != "Fist")
hide("P_HandR_Fist", 25, True)
hide("P_HandR_Open", 25, False)
for i in (1, 2, 3, 4):
    hide(f"P_FingerR{i}", 1, True)
    hide(f"P_FingerR{i}", 25, False)
hide("P_ThumbR", 1, True)
hide("P_ThumbR", 25, False)
hide("P_HandR_Open", 49, True)
hide("P_HandR_Point", 49, False)
for i in (1, 2, 3, 4):
    hide(f"P_FingerR{i}", 49, True)
hide("P_ThumbR", 49, True)
hide("P_HandR_Point", 97, True)
hide("P_HandR_Fist", 97, False)

scene.render.filepath = f"{WD}/frames/f"
scene.frame_start = 1
scene.frame_end = 120
bpy.ops.wm.save_as_mainfile(filepath=f"{WD}/brotheman-rig-animated.blend")
print("ANIMATED RIG SAVED")
