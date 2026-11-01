import bpy, os, json
OUT = os.path.expanduser("~/workspace/cape-jones-rig/blender523-motion-arm-snap-early-20261101")
scene = bpy.context.scene
for o in bpy.data.objects:
    if o.name.startswith("GP_") or o.name.startswith("LBL_"):
        o.hide_render = True
arm1 = bpy.data.objects.get("Draw-Arm_Front.png")
arm2 = bpy.data.objects.get("Draw-Arm_Back.png")
print("ARM_DRAWS", arm1.name if arm1 else None, arm2.name if arm2 else None)
def eval_z(obj, frame):
    scene.frame_set(frame)
    return round(obj.location[2], 4)
report = {"old_snap_frame": 25, "new_snap_frame": 13,
          "new_snap_hold_frames": [13, 14, 25, 32, 36],
          "snap_off_frame": 37, "torso_z": 0.08, "head_z": 0.12, "snap_z": 0.11}
for obj in (arm1, arm2):
    ztable = {f: eval_z(obj, f) for f in (1, 13, 14, 20, 25, 32, 36, 37, 48)}
    report[obj.name] = ztable
    print("Z_TABLE", obj.name, ztable)
    bad = [f for f in range(14, 37) if eval_z(obj, f) != 0.11]
    print("CROSSING_BAD_FRAMES", obj.name, bad)
    assert not bad, f"crossing Z not held: {bad}"
    assert eval_z(obj, 14) == 0.11
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
for f in range(35, 49):
    scene.frame_set(f)
    scene.render.filepath = os.path.join(OUT, "frames", f"frame_{f:03d}.png")
    bpy.ops.render.render(write_still=True)
    print("MOTION_FRAME", f, flush=True)
with open(os.path.join(OUT, "snap-early-verify.json"), "w") as fh:
    json.dump(report, fh, indent=1)
print("SNAP_EARLY_DONE", json.dumps(report))
