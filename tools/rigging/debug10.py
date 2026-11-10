"""Map all REPROP constraints: which bones they drive and from which guides."""
import bpy
bpy.ops.wm.open_mainfile(filepath='/home/hatch/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_raw.blend')
arm = bpy.data.objects['biped_blenrig']
reproprop_entries = []
for pb in arm.pose.bones:
    for c in pb.constraints:
        if 'REPROP' in c.name:
            tgt = getattr(c, 'subtarget', '')
            reproprop_entry = (pb.name, c.type, tgt)
            reproprop_entries.append(reproprop_entry)
print('total REPROP constraints:', len(reproprop_entries))
from collections import Counter
targets = Counter(t for _, _, t in reproprop_entries)
print('--- top guide targets ---')
for t, n in targets.most_common(20):
    print(f'  {t}: {n}')
print('--- sample driven bones ---')
for b, t, tgt in reproprop_entries[:15]:
    print(f'  {b} <- {tgt} ({t})')
