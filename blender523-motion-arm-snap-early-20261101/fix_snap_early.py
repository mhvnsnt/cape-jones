"""Arm-front-snap EARLIER in Blender motion, Mars 2026-11-01 15:58 CST.
Old: arm draw Z keyed to 0.11 only at f25 (crossed peak). Arms moving
toward torso from f14 were still at/below torso Z, so torso ate them.
New: Z 0.11 keyed at f13 (arms-out, before any crossing), held through
f14, f25, f32, f36, then back to rest Z only at f37 (wide flex, clear).
Poses, angles, timing, legs, head, cape, camera unchanged - only arm
draw location-Z keys.
"""
import bpy, os, json, math
OUT = os.path.expanduser("~/workspace/cape-jones-rig/blender523-motion-arm-snap-early-20261101")
scene = bpy.context.scene
# Hide overlay guide for clean motion
for o in bpy.data.objects:
    if o.name.startswith("GP_") or o.name.startswith("LBL_"):
        o.hide_render = True

arm1 = bpy.data.objects.get("Draw-Arm_Front.png")
arm2 = bpy.data.objects.get("Draw-Arm_Back.png")
assert arm1 and arm2, f"arm draws missing: {arm1} {arm2}"
print("ARM_DRAWS", arm1.name, arm2.name)

def set_z(obj, frame, z):
    scene.frame_set(frame)
    obj.location[2] = z
    obj.keyframe_insert(data_path="location", frame=frame)

# Rest Z values from legs-fixed build
rest = {arm1.name: 0.03, arm2.name: 0.035}
for obj in (arm1, arm2):
    r = rest[obj.name]
    # Explicit rest at f1 (already keyed in source, re-assert)
    set_z(obj, 1, r)
    # Snap ON early: f13 arms-out, before f14 crossing movement starts
    set_z(obj, 13, 0.11)
    set_z(obj, 14, 0.11)
    set_z(obj, 25, 0.11)
    set_z(obj, 32, 0.11)
    set_z(obj, 36, 0.11)
    # Snap OFF only at f37 wide flex, arms clear of torso
    set_z(obj, 37, r)
    set_z(obj, 48, r)
    # Interpolation: hold keys are at f13, f14, f25, f32, f36 with the
    # same value, so the curve stays flat through the crossing even
    # with default Bezier handles. The f36->f37 drop is 1 frame, arms
    # are in wide flex and clear of the torso there. Blender 5.2
    # layered-action API differs from the old fcurves API, so do not
    # force interpolation here; the close-spaced hold keys are the
    # guarantee, verified by the per-frame evaluation below.

# Verify: evaluate Z at every frame via fcurve evaluation
def eval_z(obj, frame):
    # Use scene frame_set + matrix_world? Draw location is local to peg (Z 0 parent chain),
    # so local Z is the effective layer offset. Report local Z.
    scene.frame_set(frame)
    return round(obj.location[2], 4)

report = {"old_snap_frame": 25, "new_snap_frame": 13,
          "new_snap_hold_frames": [13, 14, 25, 32, 36],
          "snap_off_frame": 37,
          "torso_z": 0.08, "head_z": 0.12, "snap_z": 0.11}
for obj in (arm1, arm2):
    ztable = {f: eval_z(obj, f) for f in (1, 13, 14, 20, 25, 32, 36, 37, 48)}
    report[obj.name] = ztable
    print("Z_TABLE", obj.name, ztable)
    # Crossing window f14-f36 must all be 0.11
    bad = [f for f in range(14, 37) if eval_z(obj, f) != 0.11]
    print("CROSSING_BAD_FRAMES", obj.name, bad)
    assert not bad, f"crossing Z not held: {bad}"
    # First frame moving toward torso (f14) already above torso
    assert eval_z(obj, 14) == 0.11 and 0.11 > 0.08

# Save new blend
blend_path = os.path.join(OUT, "cape_jones_toon_blender523_SNAP_EARLY.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("SNAP_EARLY_BLEND", blend_path)

# Render frames 1-48, EEVEE, ortho 8.5 (motion framing, flex fists never crop)
scene.render.engine = 'BLENDER_EEVEE'
try: scene.eevee.taa_render_samples = 4
except Exception: pass
scene.render.resolution_x = 700
scene.render.resolution_y = 950
scene.render.image_settings.file_format = 'PNG'
cam = scene.camera
cam.data.ortho_scale = 8.5
cam.data.sensor_fit = 'VERTICAL'
scene.frame_start = 1; scene.frame_end = 48
for f in range(1, 49):
    scene.frame_set(f)
    scene.render.filepath = os.path.join(OUT, "frames", f"frame_{f:03d}.png")
    bpy.ops.render.render(write_still=True)
    print("MOTION_FRAME", f, flush=True)
with open(os.path.join(OUT, "snap-early-verify.json"), "w") as fh:
    json.dump(report, fh, indent=1)
print("SNAP_EARLY_DONE", json.dumps(report))
