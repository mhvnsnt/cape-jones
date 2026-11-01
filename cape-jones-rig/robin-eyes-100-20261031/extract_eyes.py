import json, os
from PIL import Image
import numpy as np
from scipy import ndimage
W='/home/hatch/workspace/cape-jones-rig/robin-eyes-100-20261031'
OUT=f'{W}/eyes'; os.makedirs(OUT, exist_ok=True)
def white_comps(im, thr):
    a=np.array(im.convert('RGBA')); rgb=a[:,:,:3].astype(int); al=a[:,:,3]
    white=(rgb[:,:,0]>thr)&(rgb[:,:,1]>thr)&(rgb[:,:,2]>thr)&(al>200)
    lab,n=ndimage.label(white)
    ys,xs=np.where(al>10); fb=(int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max()))
    comps=[]
    for i in range(1,n+1):
        yy,xx=np.where(lab==i)
        if len(yy)>=60: comps.append(dict(n=len(yy), x0=int(xx.min()),x1=int(xx.max()),y0=int(yy.min()),y1=int(yy.max()), mask=(lab==i)))
    return fb, comps, a
def eye_line(fb, comps):
    fx0,fx1,fy0,fy1=fb; fh=fy1-fy0; fw=fx1-fx0
    cand=[c for c in comps if (c['y0']-fy0) < 0.62*fh and (c['x1']-c['x0']) < 0.35*fw and (c['y1']-c['y0']) < 0.25*fh and c['n'] > 0.0004*fw*fh]
    if not cand: return []
    cand.sort(key=lambda c:(c['y0']+c['y1'])/2)
    top=cand[0]; cy=(top['y0']+top['y1'])/2
    line=[c for c in cand if abs((c['y0']+c['y1'])/2-cy) <= max(30, 0.35*(top['y1']-top['y0']))]
    line.sort(key=lambda c:c['x0'])
    # drop comps that are much wider than the others (teeth-like) when 3+ in line
    if len(line)>2:
        ws=sorted((c['x1']-c['x0']) for c in line); med=ws[len(ws)//2]
        line=[c for c in line if (c['x1']-c['x0']) <= 1.6*med]
    return line[:2]
def save_pair(srcname, fb, line, im):
    if not line: return None
    a=np.array(im.convert('RGBA'))
    masks=[]
    for c in line:
        m=np.zeros_like(a); m[c['mask']]=a[c['mask']]
        crop=Image.fromarray(m[c['y0']:c['y1']+1, c['x0']:c['x1']+1])
        masks.append(crop)
    return dict(source=srcname, eyes=[dict(x0=c['x0'],x1=c['x1'],y0=c['y0'],y1=c['y1'],n=c['n']) for c in line], masks=masks)
results=[]
m=json.load(open(f'{W}/manifest.json'))
seen=set()
for x in m:
    if x['usize']==0 or x['sha256'] in seen: continue
    seen.add(x['sha256'])
    base=x['file'].rsplit('.',1)[0]
    if x['file'].lower().endswith(('.eps','.ai')):
        p=f"{W}/render/{base}.png"
        if not os.path.exists(p): print("NO RENDER", x['file']); continue
        fb,comps,arr=white_comps(Image.open(p), 235)
        line=eye_line(fb, comps)
        r=save_pair(x['file'], fb, line, Image.open(p))
        print(f"{x['file']}: line={[ (c['x0'],c['x1'],c['y0'],c['y1'],c['n']) for c in line ]}")
        if r: results.append(r)
# Day/Night close-ups (fixed head box from v4 coords, verified)
for fname, thr in [('02_ROBIN_Day.jpg',235), ('03_ROBIN_Night.jpg',150)]:
    im=Image.open(f'{W}/raw/{fname}').convert('RGBA')
    crop=im.crop((700,600,1100,800))
    fb,comps,arr=white_comps(crop, thr)
    # comps are in crop coords; eye_line on crop fb
    line=eye_line(fb, comps)
    print(f"{fname} closeup: line={[ (c['x0']+700,c['x1']+700,c['y0']+600,c['y1']+600,c['n']) for c in line ]}")
    if line:
        r=save_pair(fname, fb, line, crop)
        # shift coords back
        for e in r['eyes']: e['x0']+=700; e['x1']+=700; e['y0']+=600; e['y1']+=600
        results.append(r)
json.dump([{ 'source':r['source'], 'eyes':r['eyes']} for r in results], open(f'{W}/eyes/eye-lines.json','w'), indent=1)
# save masks
for i,r in enumerate(results):
    for j,mk in enumerate(r['masks']):
        mk.save(f"{W}/eyes/{i:02d}_{r['source'].replace(' ','_').replace('.','_')}_eye{j}.png")
print("pairs saved:", len(results))
