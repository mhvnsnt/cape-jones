# Blender render fix + MediaPipe pose check — 2026-11-01

## Task 1 — Blender render: FIXED, non-blank, verified by opening the PNG
- Original (unchanged): side-rig-blender-20261101.blend, camera (0, 2.8, 8), ORTHO, ortho_scale 8.0, rotation (0,0,0)
- Original render: blender-side-rig-render-20261101.png, 1400x1600, uniform (58,59,59), 0 coloured pixels — blank grey.
- Root cause (measured, not guessed): bone-parented planes landed OUT of the camera frustum.
  - Plane_side_torso_belt: parent SideRigArmature, parent_type BONE, bone chest, local loc (0, 3.9, 0.01) -> world bbox x -1..1, y 7.5..9.5
  - Plane_side_head_profile: parent SideRigArmature, parent_type BONE, bone head, local loc (0.2, 5.4, 0.01) -> world bbox x -0.4..0.8, y 10.6..11.8
  - Camera centred at y 2.8 covered roughly y -1.8..7.4, so both planes were above the frame.
  - Materials/EEVEE were NOT the fault: Mat_side_head_profile.png / Mat_side_torso_belt.png, HASHED blend, image textures linked, images have data (173x193 / 256x365), and a camera-only move already showed both planes.
- Proof step 1 (camera-only): camera (0, 9.65, 8), ortho_scale 6.0 -> side-rig-blender-camera-fix-test-20261101.png, head + torso visible but floating apart (gap = bone-parent offset).
- Fix (final, saved as a NEW file, original untouched):
  - Unparented both planes (parent=None, parent_type OBJECT).
  - Plane_side_torso_belt -> world (0.0, 3.3, 0.01), size 2.0x2.0 (spans y 2.3..4.3: pelvis/chest zone)
  - Plane_side_head_profile -> world (0.2, 5.4, 0.01), size 1.2x1.2 (spans y 4.8..6.0: head zone; note 5.4 is the same number as before, but now world coords, not bone-local)
  - Camera -> (0.0, 4.15, 8.0), ORTHO, ortho_scale 5.0, rotation (0,0,0) (looks -Z, sees the XY rig plane)
  - Bones untouched: SideRigArmature forearm head (0.1, 3.4, 0) -> tail (0.9, 3.4, 0), delta +0.8 +X.
- Final render: side-rig-blender-fixed-20261101.png, 1400x1600 RGBA, opened and inspected visually: head (purple, facing right) above torso (grey, belt at bottom), facing right, neck-sized gap between them (0.5 unit: y 4.3..4.8 — no neck plane exists in this .blend, only torso+head planes, so a full body is NOT shown here).
  - Opaque pixels (alpha>10): 2,240,000 / 2,240,000 (film_transparent=False, so alpha is not the discriminator)
  - Content pixels (differ >12 from modal background (59,59,59)): 376,026
  - Content bbox: (380, 208, 1019, 1391)
- Fixed blend: side-rig-blender-FIXED-20261101.blend — re-opened and verified: both planes parent=None at the coords above, camera (0, 4.15, 8), ortho_scale 5.0, forearm delta +0.8 +X.
- Blender: 4.5.3 LTS, headless EEVEE_NEXT. (EGL BAD_MATCH warnings on stderr are non-fatal; render completed.)

## Task 2 — MediaPipe pose check: RUN, on home-disk venv (no /tmp)
- Venv: cape-jones-rig/mediapipe-venv-20261101/ (home disk, not /tmp). System pip PEP 668 avoided via venv.
- mediapipe 1.2.0 installed. NOTE: 1.2.0 has NO legacy `solutions` API (import fails); used the Tasks API PoseLandmarker with official model pose_landmarker_heavy.task (30,664,242 bytes, downloaded to mediapipe-venv-20261101/models/).
- Extra fix needed: libGLESv2.so.2 was missing -> apt installed libgles2 1.7.0-1build1; then PoseLandmarker loaded.
- Full landmark dump: mediapipe-pose-check-20261101.log; script: mediapipe_pose_check.py.
- side-bent-correct-grey-20261101.png (and colour twin, same result): 1 pose, 33 landmarks. USABLE side (high visibility):
  - Facing: nose x 0.5681 > ear x 0.5492/0.5080 -> face toward +X (right).
  - Visible arm (R labels, visibility 0.99): shoulder (0.4726, 0.2890) -> elbow (0.5629, 0.3856) -> wrist (0.7127, 0.3724).
  - Elbow_x - shoulder_x = +0.0902, wrist_x - elbow_x = +0.1498, elbow angle 128.0 deg.
  - Conclusion: forearm points +X, same direction as facing = FLEXION (forward), not extension (-X, behind back). Agrees with bone data (+0.8 +X forearm) and with the visible image (open hand extended right).
  - Hidden arm (L labels) visibility 0.04-0.17 — expected in a side view, not used.
- side-idle-arms-down-fixed-20261101.png: 1 pose returned BUT NOT TRUSTED, stated plainly:
  - Elbow/wrist visibility 0.02-0.10 (essentially undetected), shoulder y 0.19 vs hip y 0.22 (implausibly compressed for a 120..1450px figure), elbow angles 97.8 / 42.9 deg on near-invisible joints.
  - Do NOT use the idle MediaPipe numbers as a pose verdict; the idle verdict rests on the fixed-rig anatomy/flip checks, not on this detection.
- No landmarks were faked. Where MediaPipe failed to see a joint (idle arms), that is reported as failure, not filled in.

## No landing, no Mars questions, no purchase — per task.
