#!/usr/bin/env python3
"""
render_sitting_preview.py — corrected sitting preview for the living room.

Owner directives 2026-10-18:
- Character SITTING IN the chair (not T-posed inside it), facing the TV/table
  direction (-X world), OUT of T-pose, BREATHING.
- Furniture: POSITION 1 (backs against the wall, DEFAULT).
- 480p is fine; no HD re-render.

RUN INSIDE BLENDER (never saves the blend):
    blender -b 3d-assets/living_room.blend \
        --python 3d-assets/living-room/render_sitting_preview.py \
        -- /path/to/out.mp4

WHAT IT DOES (memory-efficient: uses the rig + pose_sit_normal already in the
blend; no 90MB+ library appends)
1. Applies furniture POSITION 1 (apply_furniture_position.py).
2. Verifies the existing CapeJones_Rig has pose_sit_normal (850 fcurves) applied.
3. Creates a procedural 24-frame breathing loop (chest scale + spine/head
   micro-motion, sinusoidal, loopable) and layers it via NLA ADD over the
   sitting pose (NLA REPLACE, held 24f). Breathing touches chest/spine/head
   only — never the root, so the seat placement is untouched.
4. TV ON + LED preset 0 (canon violet), like the walkthrough.
5. Renders 24 frames (one breathing loop, 24fps) 480x270 Cycles CPU + OIDN,
   assembles to MP4.
"""

import bpy
import math
import os
import runpy
import subprocess
import sys
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT_MP4 = argv[0] if argv else "/tmp/sitting_preview.mp4"
FRAMES_DIR = os.path.join(os.path.dirname(OUT_MP4), "sitting_frames")
os.makedirs(FRAMES_DIR, exist_ok=True)

N_FRAMES = 24  # one full breath (breathing is 2 breaths per 48f; 24f = 1 breath)
FPS = 24

blend_path = bpy.data.filepath
repo_assets = os.path.dirname(os.path.abspath(blend_path))
LR = os.path.join(repo_assets, "living-room")

sc = bpy.context.scene
vl = bpy.context.view_layer

# ---------------------------------------------------------------- 1. furniture position 1
old_argv = sys.argv
sys.argv = ["blender", "--", "position_1"]
runpy.run_path(os.path.join(LR, "apply_furniture_position.py"), run_name="__main__")
sys.argv = old_argv

# ---------------------------------------------------------------- 2. verify sitting pose
rig = bpy.data.objects.get("CapeJones_Rig")
if rig is None:
    print("FATAL: CapeJones_Rig not found"); sys.exit(2)
ad = rig.animation_data
act = ad.action if ad else None
if act is None or act.name != "pose_sit_normal":
    print(f"FATAL: expected pose_sit_normal, got {act.name if act else None}"); sys.exit(2)
print(f"sitting pose verified: {act.name} ({len(act.fcurves)} fcurves)")
sc.frame_set(1); vl.update()
pelvis_z = (rig.matrix_world @ rig.pose.bones["pelvis"].head).z
print(f"pelvis z={pelvis_z:.3f} (seat top ~0.362, want ~0.41)")

# ---------------------------------------------------------------- 3. procedural breathing (48f loopable)
# Subtle chest rise/fall + spine/head micro-motion. Sinusoidal, so frame 48
# flows into frame 1 seamlessly.
br_act = bpy.data.actions.new("breathing_procedural")
br_act.use_fake_user = True
def add_fcurve(data_path, index, values):
    fc = br_act.fcurves.new(data_path=data_path, index=index)
    for i, v in enumerate(values):
        kp = fc.keyframe_points.insert(i + 1, v)
        kp.interpolation = "BEZIER"
    # make cyclic for a seamless loop
    mod = fc.modifiers.new(type="CYCLES")
    mod.mode_before = "REPEAT_OFFSET"
    mod.mode_after = "REPEAT_OFFSET"
    return fc

chest_pb = rig.pose.bones.get("chest")
if chest_pb is None:
    print("FATAL: chest bone not found"); sys.exit(2)
# chest scale: 1.0 -> 1.018 (inhale) -> 1.0 -> 0.982 (exhale), 1 breath per loop
for idx in (0, 1, 2):
    vals = [1.0 + 0.018 * math.sin(2 * math.pi * f / N_FRAMES)
            for f in range(N_FRAMES)]
    add_fcurve('pose.bones["chest"].scale', idx, vals)
# spine_2: tiny rotation_x sway (breathing rocks the torso)
spine2 = rig.pose.bones.get("spine_2")
if spine2:
    vals = [0.012 * math.sin(2 * math.pi * f / N_FRAMES) for f in range(N_FRAMES)]
    add_fcurve('pose.bones["spine_2"].rotation_euler', 0, vals)
# head: almost imperceptible nod
head = rig.pose.bones.get("head")
if head:
    vals = [0.008 * math.sin(2 * math.pi * f / N_FRAMES + 0.5) for f in range(N_FRAMES)]
    add_fcurve('pose.bones["head"].rotation_euler', 0, vals)
print(f"breathing action: {br_act.name} ({len(br_act.fcurves)} fcurves, {N_FRAMES}f loop)")

# NLA: sitting (REPLACE, held) + breathing (ADD)
# Move the existing action into an NLA strip, then layer breathing on top.
ad.action = None
nla = ad.nla_tracks
t1 = nla.new(); t1.name = "Sitting"
s1 = t1.strips.new(act.name, 1, act)
s1.frame_end = N_FRAMES
s1.blend_type = "REPLACE"
t2 = nla.new(); t2.name = "Breathing"
s2 = t2.strips.new(br_act.name, 1, br_act)
s2.frame_end = N_FRAMES
s2.blend_type = "ADD"
print(f"NLA: {[t.name for t in nla]}")
sc.frame_set(1); vl.update()
# verify breathing moves the chest
sc.frame_set(12); vl.update()
chest_s = tuple(round(v, 4) for v in rig.pose.bones["chest"].scale)
sc.frame_set(1); vl.update()
chest_s0 = tuple(round(v, 4) for v in rig.pose.bones["chest"].scale)
print(f"breathing check: chest scale f1={chest_s0} f12={chest_s} (should differ)")

# ---------------------------------------------------------------- 4. TV ON + LED preset 0
sys.argv = ["blender", "--"]
runpy.run_path(os.path.join(LR, "tv", "tv_setup.py"), run_name="__main__")
sys.argv = old_argv
tv = bpy.data.objects.get("crt_tv")
if tv:
    tv["tv_power"] = 1.0
    tv.update_tag()
sys.argv = ["blender", "--", "0"]
runpy.run_path(os.path.join(LR, "lighting", "set_led_preset.py"), run_name="__main__")
sys.argv = old_argv
sc.frame_set(1); vl.update()
print("TV ON, LED preset 0")

# ---------------------------------------------------------------- 5. render 48f 480x270
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = 12
sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 480, 270
sc.render.resolution_percentage = 100
sc.render.film_transparent = False
sc.render.image_settings.file_format = "PNG"

cam_data = bpy.data.cameras.new("SitFixCam")
cam_data.lens = 32.0
cam = bpy.data.objects.new("SitFixCam", cam_data)
sc.collection.objects.link(cam)
sc.camera = cam
cam.location = (1.15, 0.75, 1.30)
tgt = Vector((2.95, 2.067, 0.55))
d = tgt - cam.location
cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
# gentle push-in over the 48 frames (2 keyframes; Blender interpolates)
cam0 = Vector(cam.location)
cam1 = cam0 + Vector((0.25, 0.15, -0.05))
sc.frame_set(1)
cam.location = cam0
cam.keyframe_insert(data_path="location", frame=1)
sc.frame_set(N_FRAMES)
cam.location = cam1
cam.keyframe_insert(data_path="location", frame=N_FRAMES)
sc.frame_set(1); vl.update()

fill_data = bpy.data.lights.new("sitfix_fill", "AREA")
fill_data.energy = 150
fill_data.size = 1.5
fill_data.color = (1.0, 0.96, 0.92)
fill = bpy.data.objects.new("sitfix_fill", fill_data)
sc.collection.objects.link(fill)
fill.location = (1.4, 1.2, 1.6)
d = tgt - fill.location
fill.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()

for f in range(1, N_FRAMES + 1):
    out = os.path.join(FRAMES_DIR, "sitfix_%03d.png" % f)
    if os.path.exists(out) and os.path.getsize(out) > 10000:
        continue
    sc.frame_set(f)
    vl.update()
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)
    print(f"rendered {f}/{N_FRAMES}", flush=True)

subprocess.run([
    "ffmpeg", "-y", "-v", "error",
    "-framerate", str(FPS), "-i", os.path.join(FRAMES_DIR, "sitfix_%03d.png"),
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
    OUT_MP4,
], check=True)
print(f"PREVIEW: {OUT_MP4}")
