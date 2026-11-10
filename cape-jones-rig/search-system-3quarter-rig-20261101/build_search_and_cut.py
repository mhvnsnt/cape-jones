#!/usr/bin/env python3
"""Search system (5 industry methods) + cut Mars 3/4 sitting sheet + 3/4 rig.
Methods:
 I1 full-tree file index (name/path/size/blob/md5-if-local)
 I2 faceted metadata catalogue (angle/pose/part/group/source)
 I3 exact + perceptual hash duplicate detection (md5 + dhash)
 I4 visual thumbnail contact index
 I5 keyword+synonym search CLI (search_sheets.py)
Front rig RIG-00 is NEVER written here. All outputs go to OUT only.
"""
import os, json, csv, hashlib, subprocess, sys
from PIL import Image
import numpy as np
from scipy import ndimage

HOME=os.path.expanduser('~')
RIG=f'{HOME}/workspace/cape-jones-rig'
OUT=f'{RIG}/search-system-3quarter-rig-20261101'
FLY=f'{HOME}/workspace/cape-jones-flying'
UP=f'{HOME}/workspace/user/files/1000179383_25_yh27.jpg'
os.makedirs(f'{OUT}/pieces', exist_ok=True)
os.makedirs(f'{OUT}/contacts', exist_ok=True)

# ---------- I1+I2+I3: index ----------
paths=subprocess.check_output(['git','-C',FLY,'ls-tree','-r','--name-only','HEAD','--','characters/sheets'],text=True).splitlines()
paths=[p for p in paths if p.lower().endswith(('.jpg','.jpeg','.png','.webp'))]
print('sheets in tree:',len(paths))
# blob sizes via batch-check (only sheets)
proc=subprocess.run(['git','-C',FLY,'cat-file','--batch-check=%(objectname) %(objectsize)'],input='\n'.join(f'HEAD:{p}' for p in paths),text=True,capture_output=True)
sizes={}
for line,p in zip(proc.stdout.splitlines(),paths):
    parts=line.split()
    if len(parts)==2: sizes[p]=int(parts[1])

SYN={'three':['3quarter','threequarter'],'quarter':['3quarter'],'3quarter':['three','quarter','threequarter'],
'sitting':['sit','seated','lounge','chair'],'sit':['sitting','seated','lounge'],'seated':['sit','sitting','lounge'],
'lounge':['sit','sitting','seated','chair'],'chair':['sit','sitting','lounge'],
'front':['forward'],'back':['rear'],'side':['profile'],'profile':['side']}
def tags_for(p):
    low=p.lower(); t=set()
    for k in ['3quarter','front','back','side','profile','sit','sitting','seated','lounge','chair','standing','turnaround','expression','viseme','cape','hand','leg','arm','head','torso']:
        if k in low: t.add(k)
    if '3quarter' in t: t.update(['three','quarter'])
    if t & {'sit','sitting','seated','lounge'}: t.update(['sit','sitting','seated','lounge'])
    return sorted(t)
def dhash(im):
    g=im.convert('L').resize((9,8),Image.LANCZOS); a=np.array(g)
    return ''.join('1' if a[:,i]>a[:,i+1] else '0' for i in range(8) for _ in [0]) if False else ''.join('1' if a[y,x]>a[y,x+1] else '0' for y in range(8) for x in range(8))

records=[]
for p in paths:
    local=os.path.join(FLY,p)
    present=os.path.exists(local)
    md5=None; dh=None; dims=None
    if present:
        try:
            md5=hashlib.md5(open(local,'rb').read()).hexdigest()
            im=Image.open(local); dims=f"{im.width}x{im.height}"; dh=dhash(im)
        except Exception as e:
            print('skip img',p,e)
    records.append({'repo_path':p,'group':p.split('/')[2] if len(p.split('/'))>2 else '',
        'filename':os.path.basename(p),'size_bytes':sizes.get(p),'present_locally':present,
        'md5_local':md5,'dhash':dh,'dimensions':dims,'tags':tags_for(p)})
with open(f'{OUT}/sheet-index-20261101.json','w') as f: json.dump(records,f,indent=1)
with open(f'{OUT}/sheet-index-20261101.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['repo_path','group','filename','size_bytes','present_locally','md5_local','dhash','dimensions','tags'])
    w.writeheader()
    for r in records: w.writerow({**r,'tags':','.join(r['tags'])})
# duplicates among present files: exact md5 groups + dhash groups
from collections import defaultdict
md5g=defaultdict(list); dhg=defaultdict(list)
for r in records:
    if r['md5_local']: md5g[r['md5_local']].append(r['repo_path'])
    if r['dhash']: dhg[r['dhash']].append(r['repo_path'])
dup={'exact_md5_groups':{k:v for k,v in md5g.items() if len(v)>1},
     'dhash_groups':{k:v for k,v in dhg.items() if len(v)>1}}
with open(f'{OUT}/duplicates-20261101.json','w') as f: json.dump(dup,f,indent=1)
print('present locally:',sum(r['present_locally'] for r in records),'exact dup groups:',len(dup['exact_md5_groups']),'dhash groups:',len(dup['dhash_groups']))

# ---------- I5 search function (shared logic, CLI file written separately) ----------
def search(q):
    terms=set()
    for t in q.lower().replace('-',' ').replace('/',' ').split():
        terms.add(t); terms.update(SYN.get(t,[]))
    scored=[]
    for r in records:
        hay=(r['repo_path']+' '+' '.join(r['tags'])).lower()
        score=sum(1 for t in terms if t in hay)
        # bonus: all core terms present
        if score: scored.append((score,r))
    scored.sort(key=lambda x:(-x[0],x[1]['repo_path']))
    return terms,scored
tests={}
for q in ['three quarter sitting','3quarter sitting','lounge','sitting','chair','front facing','side']:
    terms,scored=search(q)
    tests[q]={'expanded_terms':sorted(terms),'matches':len(scored),'top':[r['repo_path'] for _,r in scored[:10]]}
    print(q,'->',len(scored),tests[q]['top'][:3])
with open(f'{OUT}/search-tests-20261101.json','w') as f: json.dump(tests,f,indent=1)

# ---------- I4 contacts: matched sheets present locally ----------
matched=[r for _,r in search('three quarter sitting')[1] if r['present_locally']]
# ensure lounge-3quarter 11 are in (they match lounge/sit tags via path? check: they contain lounge)
print('matched present:',len(matched))
tiles=[]
for r in matched:
    try:
        im=Image.open(os.path.join(FLY,r['repo_path'])).convert('RGB'); im.thumbnail((360,360)); tiles.append((r['filename'],im))
    except Exception as e: print('tile skip',e)
if tiles:
    cols=4; rows=(len(tiles)+cols-1)//cols
    sheet=Image.new('RGB',(cols*360,rows*380),(255,255,255))
    from PIL import ImageDraw
    d=ImageDraw.Draw(sheet)
    for i,(name,im) in enumerate(tiles):
        x=(i%cols)*360; y=(i//cols)*380; sheet.paste(im,(x,y+20)); d.text((x+5,y+2),name[:42],fill=(0,0,0))
    sheet.save(f'{OUT}/contacts/sheet-contact-3quarter-sitting-20261101.png')
    print('contact tiles:',len(tiles))

# ---------- Cut Mars upload ----------
im=Image.open(UP).convert('RGB'); arr=np.array(im).astype(int)
bg=np.array([126,126,126])
dist=np.sqrt(((arr-bg)**2).sum(axis=2))
mask=dist>45  # non-grey foreground (white/black/purple pieces; grey shading lines inside pieces are close to bg but pieces are solid enough that components still connect via outlines? use closing)
mask=ndimage.binary_closing(mask,iterations=2)
mask=ndimage.binary_fill_holes(mask)
lab,n=ndimage.label(mask)
objs=ndimage.find_objects(lab)
print('components:',n)
pieces=[]
for i,sl in enumerate(objs,1):
    h=sl[0].stop-sl[0].start; w=sl[1].stop-sl[1].start; area=int((lab[sl]==i).sum())
    if area<800: continue
    pieces.append({'id':i,'bbox':[int(sl[1].start),int(sl[0].start),int(sl[1].stop),int(sl[0].stop)],'w':int(w),'h':int(h),'area':area})
pieces.sort(key=lambda p:(p['bbox'][1],p['bbox'][0]))
for p in pieces: print(p)
with open(f'{OUT}/upload-pieces-20261101.json','w') as f: json.dump(pieces,f,indent=1)
# save each component as transparent PNG (crop, alpha = component mask)
for p in pieces:
    x0,y0,x1,y1=p['bbox']; comp=(lab[y0:y1,x0:x1]==p['id'])
    crop=np.array(im)[y0:y1,x0:x1]
    out=np.zeros((y1-y0,x1-x0,4),dtype=np.uint8); out[:,:,:3]=crop; out[:,:,3]=np.where(comp,255,0)
    Image.fromarray(out).save(f"{OUT}/pieces/piece-{p['id']:02d}-{x0}x{y0}.png")
print('saved pieces:',len(pieces))
