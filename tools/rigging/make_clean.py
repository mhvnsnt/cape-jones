"""Create clean deliverable blend: remove BlenRig rig, keep only needed objects."""
import bpy, os
TMP = os.path.expanduser('~/workspace/cj-rig-wt/.rig_tmp')
OUT = os.path.expanduser('~/workspace/cj-rig-wt/3d-assets/cape-jones-rig/cape_jones_rigged.blend')
bpy.ops.wm.open_mainfile(filepath=os.path.join(TMP, 'cj_cape_sep.blend'))
# remove BlenRig objects (keep for reference in a separate file, not deliverable)
to_remove = []
for o in bpy.data.objects:
    if 'biped_blenrig' in o.name or 'BlenRig' in o.name and 'MdefCage' not in o.name:
        # keep MdefCage, remove the rig
        if 'MdefCage' not in o.name:
            to_remove.append(o)
# also remove BlenRig-specific objects
for o in list(bpy.data.objects):
    if o.name.startswith('biped_blenrig') or 'blenrig' in o.name.lower():
        if 'MdefCage' not in o.name and 'CapeJones' not in o.name:
            if o not in to_remove:
                to_remove.append(o)
print('removing:', [o.name for o in to_remove][:10])
for o in to_remove:
    bpy.data.objects.remove(o, do_unlink=True)
# also remove BlenRig armatures
for arm in list(bpy.data.armatures):
    if 'blenrig' in arm.name.lower() or 'biped' in arm.name.lower():
        if 'CapeJones' not in arm.name:
            print('removing armature:', arm.name)
            bpy.data.armatures.remove(arm)
print('remaining objects:', [o.name for o in bpy.data.objects][:10])
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print('CLEAN BLEND SAVED to', OUT)
# also save a tmp copy for further work
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(TMP, 'cj_clean.blend'))
print('TMP CLEAN SAVED')
