# Joint-locked rig v4 — corrections, 2026-10-31
Mars, 2026-10-31 11:52 CDT, on the v3 presentation:
1. Hips: screen-right hip (character's left) was off to the right.
   Fix: HR hip 605 -> 585 (20px left), and screen-right leg uses
   Leg_Back pieces, screen-left leg uses Leg_Front pieces.
   Front-for-both was putting the back leg in the wrong socket.
2. Jump legs: bend TOWARD each other, not out into a split.
   Was lower -90/+90. Now lower +45/-45, shins down-in, feet
   together under the body. Tuck, not split.
3. Arms raised: do NOT bend forearm alone. Raise the WHOLE arm
   as one unit from the shoulder, forearm follows upper.
   Jump/arms-up now use the whole Arm_Front piece pinned at the
   shoulder joint and rotated around it. Cut-limb elbow bends
   stay only for true flex/bend poses, where the bend is the point.
All other v3 joints unchanged. Shoulders (430,445)/(670,445),
hips (495,760)/(585,760). Builder: joint_locked_rig_v4.py.
Poses: joint-apose/flex/punch/dance/seated/jump-v4, plus a
jump clip (clips/jump-clip.json + 4 keyframe frames: crouch,
takeoff, tuck-in, land). Spine rig: cape-jones-rig-spine.json.
