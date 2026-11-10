"""List NOREP vs REPROP bone overlap."""
import bpy
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_raw.blend')
arm = bpy.data.objects['biped_blenrig']
reprop_bones = set()
norep_bones = set()
for pb in arm.pose.bones:
    for c in pb.constraints:
        if 'REPROP' in c.name and 'NOREP' not in c.name:
            reprop_bones.add(pb.name)
        elif 'NOREP' in c.name:
            norep_bones.add(pb.name)
print('REPROP bones:', len(reprop_bones), 'NOREP bones:', len(norep_bones))
overlap = reprop_bones & norep_bones
print('OVERLAP:', len(overlap))
for n in sorted(overlap)[:20]:
    print('  ', n)
print('--- sample NOREP-only bones ---')
for n in sorted(norep_bones - reprop_bones)[:15]:
    print('  ', n)
