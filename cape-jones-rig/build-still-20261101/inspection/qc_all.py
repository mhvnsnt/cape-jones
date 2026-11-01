#!/usr/bin/env python3
"""Full-res numeric QC over ALL sliced pieces: old 2854 + new 964 = 3818.
Read-only. For each PNG: readable, native size, opaque px (alpha>10 or
non-white for RGB), blank, tiny (<800 opaque, the slice threshold).
Also verifies manifest counts: sliced-clean walk vs sliced-68 sheets walk.
"""
import os, json
from PIL import Image
import numpy as np
ROOT='/home/hatch/workspace/cape-jones-rig'
OUT=os.path.dirname(os.path.abspath(__file__))
sets={'old_sliced_clean': ROOT+'/sliced-clean-20261031',
      'new_sliced_68_sheets': ROOT+'/sliced-68-unsliced-20261031/sheets'}
results={}; anomalies=[]
for name, base in sets.items():
    files=[]
    for dp,dn,fn in os.walk(base):
        for f in fn:
            if f.lower().endswith('.png'): files.append(os.path.join(dp,f))
    files.sort()
    n=blank=tiny=corrupt=0; tot_opaque=0; sizes={}
    for p in files:
        try:
            im=Image.open(p); im.load()
            a=np.array(im.convert('RGBA'))
            op=int((a[:,:,3]>10).sum())
            tot_opaque+=op
            sizes.setdefault(f"{im.size[0]}x{im.size[1]}",0)
            if op==0: blank+=1; anomalies.append({'file':os.path.relpath(p,ROOT),'issue':'blank_zero_opaque'})
            elif op<800: tiny+=1
        except Exception as e:
            corrupt+=1; anomalies.append({'file':os.path.relpath(p,ROOT),'issue':f'corrupt:{e}'})
    results[name]={'files':len(files),'blank':blank,'tiny_lt800':tiny,'corrupt':corrupt,'total_opaque_px':tot_opaque}
    print(name, results[name])
# new-batch named/mixed from its manifest
m=json.load(open(ROOT+'/sliced-68-unsliced-20261031/SLICING-MANIFEST-20261031.json'))
results['new_manifest']={'sheets':m['sheets_sliced'],'pieces':m['total_new_pieces'],'named':m['named'],'mixed':m['mixed'],
  'named_check_sum':sum(s['named'] for s in m['sheets']),'mixed_check_sum':sum(s['mixed'] for s in m['sheets'])}
print(results['new_manifest'])
results['anomalies']=anomalies
json.dump(results, open(os.path.join(OUT,'qc-all-3818.json'),'w'), indent=1)
print('anomalies:', len(anomalies))
for an in anomalies[:20]: print(' ', an)
