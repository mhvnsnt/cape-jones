import bpy

print("=== STAGE D: steepen coupling curve ===", flush=True)
OUT = "/home/hatch/workspace/sitcanon-work/scene_recliner_mech.blend"
rig = bpy.data.objects.get("CapeJones_Rig")
couple = "min(max((recline - 0.1) / 0.55, 0.0), 1.0)"
n = 0
for d in rig.animation_data.drivers:
    if 'ik_leg_' in d.data_path or 'ReclinerFollow' in d.data_path:
        d.driver.type = 'SCRIPTED'
        d.driver.expression = couple
        n += 1
        print(f"  {d.data_path} -> {couple}", flush=True)
print(f"updated {n} drivers", flush=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT, flush=True)
