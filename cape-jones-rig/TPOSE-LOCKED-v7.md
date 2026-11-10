# T-pose LOCKED — v7, 2026-10-31 (supersedes v5 and v6, neither was repo-locked)
Mars, 2026-10-31 10:26 CDT: "lock that in and show that to me" (after
torso/pelvis clean-up). This v7 is the locked default T-pose.
File: assembly-preview-v7-20261031.png — do NOT overwrite it.
Builder that reproduces it exactly: assemble_tpose_default.py
Registry: locked-default-tpose.json (same numbers, machine-readable)

Locked positions (canvas 1100x1500, scale 0.95 unless noted):
Layer order bottom->top: Cape_Back_Main 550/410, Leg_Back? No — legs:
Leg_Front 450/720, Leg_Back_GRAFTED 650/720, Arm (left) 300/380,
Arm (right) 800/380, Pelvis 550/680, Cape_Collar 550/370,
Torso_Chest 550/400, Belt_Overlay 550/670, Neck 550/360 scale 1.05,
Head_Front 550/250.
Arms: both Arm_Front, VERTICAL flip (top-to-bottom, NOT horizontal):
left = flip-top-bottom + rot +90 + flip-top-bottom, right = rot +90 +
flip-top-bottom. Pads TOP, bicep BOTTOM, fists/fingers/thumbs BOTTOM.
Head: lowered 20px from v5 (230->250), jaw on neck.
Neck: scaled 1.05 (109x87), wider than v5 99x79, narrower than head 113.
Legs: 200 apart, thigh gap shows cape, right foot graft complete.
Waist v7: pelvis up 20px (700->680), belt up 10px (680->670),
torso-pelvis overlap 23px, belt covers junction, no side tab.
Pieces locked: sliced core 28 + Leg_Back_GRAFTED, Pack1-clean 25,
cut-limbs 8. Clean-cut rule: slice_clean.py first, rembg per-piece only.
Future pieces: add as new files, never overwrite a locked piece;
a new T-pose version gets a new dated filename, and this doc is
superseded in writing, never silently edited.
Repo status: LOCAL LOCK ONLY in this turn — repo PR for v7 is the
next step from the 2026-10-31 10:25 repo request, pending Mars seeing v7.
