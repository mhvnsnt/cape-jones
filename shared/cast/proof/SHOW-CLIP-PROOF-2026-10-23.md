# Moving show-clip proof — cyborgx (Cape Jones rig) waving in Cape's living room (2026-10-23 CT)

Handoff step 1 ("render a moving proof clip in cape-jones and view it").

- Video: `cyborgx_wave_in_cape_room_v1.mp4` — 640x360, h264, 24 frames @ 7.5 fps = 3.20 s (source 30 fps, frame_step 4, so real-time speed). SHA-256 `3914bc2d65cda9428149095475e9d590ba3d7201b3b6961b76767dbb409d4766`. Full ffmpeg decode: no errors.
- Check frames: `cyborgx_wave_in_cape_room_v1_checkframes.png` (t = 0.25 / 1.1 / 2.0 / 2.9 s). Viewed by Grok Bot: the fighter stands on the living-room floor by the rug and raises both arms in a wave; the pose changes frame to frame (no T-pose), feet stay on the floor, nothing off-frame.
- Model: western-heart `game/assets/models/cyborg-x.glb` (160 joints, T7 Alisa SFM port = cyborgx rig). **STAND-IN look:** Alisa-port mesh, not the owner's Cape Jones model.
- Clip: western-heart PR #849 `anims/show/cape-jones/wave.glb` (CMU take 13_26, retargeted with `tools/anim-retarget/retarget_rot.py`). Binding gate: 1600/1600 fcurves bound.
- Render: `blender -b 3d-assets/living_room.blend -P shared/cast/render_show_clip_in_room.py -- cyborg-x.glb wave.glb <rot> out '[1.2,0.9,0]' 24 CYCLES 4` (Blender 4.2.3, Cycles CPU, 12 spp, denoise). The .blend is never saved; room lighting/colours untouched.
- Known: the scene's own Cape Jones figure is visible in the background in its stored rest pose (part of `living_room.blend`). Show clips are SHOW-context only (ANIM-GATE); never in FIGHT.
- License: CMU Graphics Lab Motion Capture Database, free incl. commercial. "The data used in this project was obtained from mocap.cs.cmu.edu. The database was created with funding from NSF EIA-0196217."

Next: same render for walk / talk_gesture / idle; owner's Cape Jones mesh on the 52-bone rig once its binding lands.
