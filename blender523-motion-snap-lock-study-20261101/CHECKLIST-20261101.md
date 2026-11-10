# Next Blender motion build — start-here checklist

Copy this file into the new build folder and tick it with evidence,
not from memory. A tick without a file, frame, or gate line is not a tick.

- [ ] Source blend copied to a NEW dated folder; locked snap-early blend NOT opened as the working file.
- [ ] Crossing window written down first: snap-on / cross start / cross end / snap-off, with the snap-off pose proving arms are clear.
- [ ] Snap defaults applied: snap Z 0.11, torso 0.08, head 0.12, chest stack torso < arm < head; face cross uses torso < head < arm.
- [ ] Template run headless; gate JSON saved in the build folder; overall PASS before any render is claimed.
- [ ] Per-frame pose table supplied (POSE_JSON) if legs are in the move; otherwise knee-feet and grounded are reported NOT_CHECKED, never PASS.
- [ ] Eye-checks: first crossing frame (arms already on top), crossed peak (continuous chain, biceps on top), snap-off frame (arms clear, no pop), one frame either side of each.
- [ ] Feet checked: planted unless labelled airborne; planted foot within 5 px of ground line.
- [ ] Wrist checked: hands with wrists, no cut wrist, no fist left behind.
- [ ] Cape checked: collar moves with torso, bottom pinned when seated, cape lags body 1-2 frames on follow-through.
- [ ] Knee-feet checked per frame: knee direction == toe direction, both legs, exception only if Mars named that specific pose.
- [ ] Elbows checked: point back/out, never forward/in reversed.
- [ ] Flex checked if present: spread 100-160 deg, obtuse, not acute pinch.
- [ ] Guides hidden: GP_/LBL_ overlay off for clean renders; no debug orbs or labels in any final.
- [ ] No finished image erased, cropped, or inpainted; any removed piece was removed by layer in the source builder and re-rendered.
- [ ] New dated files only; no Mars-seen version overwritten.
- [ ] Shown to Mars; perfect only when Mars says so after seeing it.
