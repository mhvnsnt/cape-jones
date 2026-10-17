"""Lane 3: merge snap + LED actions and remote prop into main blend."""
import bpy

MAIN = "/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend"
bpy.ops.wm.open_mainfile(filepath=MAIN)
rig = bpy.data.objects["CapeJones_Rig"]

# append snap action
with bpy.data.libraries.load("/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/.scratch/snap_test.blend") as (di, do):
    do.actions = ["snap_test_R"]
print("snap actions:", [a.name for a in bpy.data.actions if "snap" in a.name], flush=True)

# append LED action + remote prop
with bpy.data.libraries.load("/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/.scratch/led_test.blend") as (di, do):
    do.actions = ["led_press_R"]
    do.objects = ["LED_Remote", "LED_Button"]
print("led actions:", [a.name for a in bpy.data.actions if "led" in a.name], flush=True)

# link remote objects to scene
for oname in ("LED_Remote", "LED_Button"):
    o = bpy.data.objects.get(oname)
    if o and o.name not in bpy.context.scene.collection.objects:
        bpy.context.scene.collection.objects.link(o)
        print("linked", oname, flush=True)

# ensure idle action is active (don't disturb default state)
if "idle_heroic_breathe" in bpy.data.actions:
    rig.animation_data.action = bpy.data.actions["idle_heroic_breathe"]
    print("active action reset to idle_heroic_breathe", flush=True)

bpy.ops.wm.save_mainfile(filepath=MAIN)
print("SAVED main blend with animations", flush=True)
