"""Assemble sitting_pose_library.blend from per-pose stage blends.
Appends the 5 pose_* actions into a fresh copy of the rig blend, marks them
as pose assets, saves sitting_pose_library.blend (full-res mesh).
"""
import bpy, os

RIG_BLEND = "/home/hatch/workspace/cj-sitting-poses/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend"
STAGE_DIR = "/home/hatch/workspace/cj-sitting-poses/3d-assets/cape-jones-rig/pose_stage"
OUT_BLEND = "/home/hatch/workspace/cj-sitting-poses/3d-assets/cape-jones-rig/sitting_pose_library.blend"

KEYS = ["sit_normal", "sit_leg_folded", "sit_lean_forward", "sit_recline", "sit_arms_crossed"]

bpy.ops.wm.open_mainfile(filepath=RIG_BLEND)
rig = bpy.data.objects['CapeJones_Rig']
idle = bpy.data.actions.get('idle_heroic_breathe')
if idle:
    idle.use_fake_user = True

for key in KEYS:
    stage = os.path.join(STAGE_DIR, f"pose_{key}.blend")
    assert os.path.exists(stage), f"missing stage {stage}"
    with bpy.data.libraries.load(stage) as (df, dt):
        dt.actions = [f"pose_{key}"]
    act = dt.actions[0]
    act.use_fake_user = True
    if not act.asset_data:
        act.asset_mark()
    print(f"APPENDED {act.name}", flush=True)

print("ACTIONS:", [a.name for a in bpy.data.actions if a.name.startswith("pose_")], flush=True)
# hide the broken pre-rebuild cape in the library file too
cape = bpy.data.objects.get('CapeJones_Cape')
if cape:
    cape.hide_viewport = True
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print(f"SAVED {OUT_BLEND}", flush=True)
