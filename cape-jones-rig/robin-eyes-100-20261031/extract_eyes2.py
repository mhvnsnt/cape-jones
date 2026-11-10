import json, os
from PIL import Image
import numpy as np
from scipy import ndimage
W='/home/hatch/workspace/cape-jones-rig/robin-eyes-100-20261031'
def comps_of(im, thr):
    a=np.array(im.convert('RGBA')); rgb=a[:,:,:3].astype(int); al=a[:,:,3]
    white=(rgb[:,:,0]>thr)&(rgb[:,:,1]>thr)&(rgb[:,:,2]>thr)&(al>200)
    lab,n=ndimage.label(white); out=[]
    for i in range(1,n+1):
        yy,xx=np.where(lab==i)
        if len(yy)>=40: out.append(dict(n=len(yy), x0=int(xx.min()),x1=int(xx.max()),y0=int(yy.min()),y1=int(yy.max()), mask=(lab==i)))
    return a, out
def eye_like(c):
    w=c['x1']-c['x0']+1; h=c['y1']-c['y0']+1
    return 8<=w<=160 and 6<=h<=110 and 40<=c['n']<=12000 and 0.25<=w/h<=6.0
def pairs(comps):
    cs=[c for c in comps if eye_like(c)]
    cs.sort(key=lambda c:(c['y0']+c['y1'])/2)
    used=set(); out=[]
    for i,c in enumerate(cs):
        if i in used: continue
        cy=(c['y0']+c['y1'])/2
        best=None
        for j,d in enumerate(cs):
            if j==i or j in used: continue
            if abs((d['y0']+d['y1'])/2-cy) <= max(25, 0.4*(c['y1']-c['y0'])) and 0 < (d['x0']-c['x1']) <= 220:
                best=j; break
        if best is not None:
            out.append([c, cs[best]]); used.add(i); used.add(best)
        else:
            out.append([c]); used.add(i)
    return out
m=json.load(open(f'{W}/manifest.json')); seen=set(); report={}
for x in m:
    if x['usize']==0 or x['sha256'] in seen: continue
    seen.add(x['sha256']); base=x['file'].rsplit('.',1)[0]
    if x['file'].lower().endswith(('.eps','.ai')):
        p=f"{W}/render/{base}.png"
        if not os.path.exists(p): continue
        a,cs=comps_of(Image.open(p), 235)
        pr=pairs(cs)
        report[x['file']]=[[(c['x0'],c['x1'],c['y0'],c['y1'],c['n']) for c in pair] for pair in pr]
        print(x['file'], '->', report[x['file']])
json.dump(report, open(f'{W}/eyes/eye-candidates2.json','w'), indent=1)
