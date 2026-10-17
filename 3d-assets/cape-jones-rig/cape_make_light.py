"""LANE 1 — make a LIGHT sim file: keep rig + cape + shell + floor,
DELETE the 910k body, MDEF cage, old fragments. The sim doesn't need them.
Saves cape_sim_light.blend (small, fast to bake)."""
import bpy, os

LIGHT = os.path.join(os.getcwd(), 'cape_sim_light.blend')

# objects to keep
keep = {'CapeJones_Rig', 'CapeJones_Cape', 'BackShell_Collider', 'Floor_Collision'}
for ob in list(bpy.data.objects):
    if ob.name not in keep and ob.type != 'CAMERA':
        # remove object and its data
        bpy.data.objects.remove(ob, do_unlink=True)

# purge orphan data
for _ in range(3):
    bpy.ops.outliner.orphans_purge(do_recursive=True)

print(f"objects kept: {[o.name for o in bpy.data.objects]}", flush=True)
bpy.ops.wm.save_as_mainfile(filepath=LIGHT)
print(f"SAVED {LIGHT}", flush=True)
import os as _os
print(f"size: {_os.path.getsize(LIGHT)}", flush=True)
