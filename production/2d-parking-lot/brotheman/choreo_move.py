#!/usr/bin/env python3
"""BROTHERMAN Rig Jones 1 — MOVEMENT TEST (prove the rig first), 96f / 4s.
Cape dance-test equivalent: the rig must prove itself in a whole video
before the scene test. Beats:
  f1-12   idle, blink f6
  f13-36  ELBOW demo: forearm curls the fist to the shoulder and back
          (V2 Cape rig cannot bend the elbow at all)
  f37-60  KNEE demo / squat: thighs + shins bend, torso squash & stretch,
          spring back with overshoot
  f61-84  WAVE: arm up, Open hand, fingers + thumb wiggle, hair and
          bandana tails swing with lag/overshoot, Happy eyes
  f85-96  settle to idle, blink f90
Rotation sign: limb bones point down (-Y); negative Z swings toward -X
(viewer's left). Squash = pose-bone scale keys on the torso.
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


def loc(bone, frame, x, y):
    b = pb[bone]
    b.location = (x, y, 0.0)
    b.keyframe_insert(data_path="location", frame=frame)


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
    # state: "open" | "happy" | "wink" (L happy, R open)
    hide("P_Eye_Open_L", frame, state in ("happy", "wink"))
    hide("P_Eye_Open_R", frame, state == "happy")
    hide("P_Eye_Happy_L", frame, state == "open")
    hide("P_Eye_Happy_R", frame, state in ("open", "wink"))


# ---- blinks ----------------------------------------------------------------
for f0 in (6, 90):
    eye_scale(f0 - 1, 1.0)
    eye_scale(f0, 0.1)
    eye_scale(f0 + 2, 1.0)

# ---- elbow demo: forearm curl ----------------------------------------------
for f, z in [(1, 0.0), (13, 0.0), (24, -2.05), (30, -2.05), (36, 0.0)]:
    rot("forearmR", f, z)
for f, z in [(1, 0.0), (13, 0.0), (24, -0.35), (36, 0.0)]:
    rot("upperArmR", f, z)
for f, z in [(24, 0.0), (28, 0.30), (32, -0.25), (36, 0.0)]:
    rot("handR", f, z)
mouth(1, "Mouth_Closed")
mouth(20, "Mouth_Smile")
mouth(36, "Mouth_Closed")

# ---- knee demo / squat with squash & stretch --------------------------------
for f, z in [(37, 0.0), (48, -0.15), (54, -0.15), (60, 0.0)]:
    rot("thighR", f, z)
    rot("thighL", f, -z)
for f, z in [(37, 0.0), (48, 0.30), (54, 0.30), (60, 0.0)]:
    rot("shinR", f, z)
    rot("shinL", f, -z)
for f, y in [(37, 0.0), (48, -0.45), (54, -0.45), (60, 0.0)]:
    loc("pelvis", f, 0.0, y)
for f, sx, sy in [(37, 1.0, 1.0), (48, 1.07, 0.92), (54, 1.07, 0.92),
                  (58, 0.97, 1.04), (62, 1.0, 1.0)]:
    scl("torso", f, sx, sy)
mouth(44, "Mouth_Open")
mouth(60, "Mouth_Closed")

# ---- wave: arm up, open hand, fingers + thumb, hair/tails follow-through ----
for f, z in [(61, 0.0), (66, -1.95), (78, -2.05), (84, -1.95)]:
    rot("upperArmR", f, z)
for f, z in [(61, 0.0), (66, -0.30), (84, -0.30)]:
    rot("forearmR", f, z)
for f, z in [(66, 0.0), (70, 0.35), (74, -0.30), (78, 0.35), (82, 0.0)]:
    rot("handR", f, z)
for i in (1, 2, 3, 4):
    for f, z in [(66, 0.0), (70, 0.25 if i % 2 else -0.20),
                 (74, -0.20 if i % 2 else 0.25), (78, 0.25 if i % 2 else -0.20),
                 (82, 0.0)]:
        rot(f"fingerR{i}", f, z)
for f, z in [(66, 0.0), (72, 0.30), (78, -0.25), (82, 0.0)]:
    rot("thumbR", f, z)
# hair + bandana tails lag 2-4f behind the arm, overshoot on the settle
for f, z in [(61, 0.0), (68, -0.18), (76, 0.15), (84, -0.10), (90, 0.0)]:
    rot("hair", f, z)
for f, z in [(61, 0.0), (70, -0.30), (78, 0.25), (86, -0.12), (92, 0.0)]:
    rot("bandanaTail", f, z)
# head tilt + happy eyes during the wave
for f, z in [(61, 0.0), (70, 0.08), (84, 0.08), (96, 0.0)]:
    rot("head", f, z)
eyes(1, "open")
eyes(66, "happy")
eyes(84, "open")
mouth(61, "Mouth_Smile")
mouth(84, "Mouth_Smile")

# ---- hand swaps: Fist -> Open at f61 (fingers + thumb on) -------------------
for kind in ("Fist", "Open", "Point"):
    hide(f"P_HandR_{kind}", 1, kind != "Fist")
hide("P_HandR_Fist", 61, True)
hide("P_HandR_Open", 61, False)
for i in (1, 2, 3, 4):
    hide(f"P_FingerR{i}", 1, True)
    hide(f"P_FingerR{i}", 61, False)
hide("P_ThumbR", 1, True)
hide("P_ThumbR", 61, False)
# back to Fist at f85
hide("P_HandR_Open", 85, True)
hide("P_HandR_Fist", 85, False)
for i in (1, 2, 3, 4):
    hide(f"P_FingerR{i}", 85, True)
hide("P_ThumbR", 85, True)
mouth(85, "Mouth_Closed")

# ---- settle ------------------------------------------------------------------
for f, z in [(84, -1.95), (90, -0.60), (96, 0.0)]:
    rot("upperArmR", f, z)
for f, z in [(84, -0.30), (96, 0.0)]:
    rot("forearmR", f, z)

scene.render.filepath = f"{WD}/frames_move/f"
scene.frame_start = 1
scene.frame_end = 96
bpy.ops.wm.save_as_mainfile(filepath=f"{WD}/brotheman-rig-move.blend")
print("MOVE RIG SAVED")
