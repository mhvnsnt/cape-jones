"""PAH GO v2: mouth-only clean clip. Lips/teeth/tongue/opening ONLY.
Leak = (A) non-mouth-material pixels, (B) thin face-line pixels removed by
morphological opening (5x5) + 2px dilation mask, (C) disconnected fragments
<100px, or MBP's 26px slanted jaw segment. Thin-line mouths (MBP, 02) use
component rule only, NOT opening (opening would erase the line itself).
Resize halo fix: after LANCZOS resize, alpha is thresholded >=128; pixels
with alpha 1-127 are dropped and counted as fringe, never composited.
Placement: single target (231.5,504.5), alpha-bbox centre anchor,
scale = old fitted scale x 0.75, same for every mouth, no jumps."""
from PIL import Image
import numpy as np, os, json
from scipy import ndimage
R='/home/hatch/workspace/cape-jones-rig'
OUT=f'{R}/pahgo-mouth-cleanup-v2-20261031'
OLD=f'{R}/superhero-mouths-20261031/mouths'
TIGHT=f'{R}/pahgo-mouth-fix-20261031/mouths-tight'
BASE=Image.open(f'{R}/visemes-v2-20261031/clean-head-base-20261031.png').convert('RGBA')
TARGET=(231.5,504.5); SF=0.75
def is_mouth(rgb):
    r,g,b=rgb[...,0].astype(int),rgb[...,1].astype(int),rgb[...,2].astype(int)
    black=(r<80)&(g<80)&(b<80)
    white=(r>200)&(g>200)&(b>200)
    tongue=(r>100)&(g<135)&(b<95)&(r>g+25)
    return black|white|tongue
def clean(src_path, thin_line=False, extra_bbox_drop=None):
    im=np.array(Image.open(src_path).convert('RGBA'))
    alpha=im[:,:,3]>0
    mouth=is_mouth(im)&alpha
    leakA=int((alpha&~mouth).sum())
    work=mouth.copy()
    leakB=0
    if not thin_line:
        opened=ndimage.binary_opening(work, structure=np.ones((5,5)))
        mask=ndimage.binary_dilation(opened, structure=np.ones((5,5)))  # 2px approx via 2 dilations below
        mask=ndimage.binary_dilation(mask, structure=np.ones((3,3)))
        leakB=int((work&~mask).sum()); work=work&mask
    if extra_bbox_drop is not None:
        # drop mouth-material pixels outside teeth/tongue bbox expanded by extra_bbox_drop px
        ys,xs=np.where(mouth & (np.array(Image.open(src_path).convert('RGBA'))[:,:,0]>100))
        # simpler: caller passes a bbox
        x0,y0,x1,y1=extra_bbox_drop
        keep=np.zeros_like(work); keep[y0:y1+1,x0:x1+1]=True
        leakB+=int((work&~keep).sum()); work=work&keep
    lab,n=ndimage.label(work)
    sizes=ndimage.sum(work,lab,range(1,n+1)) if n else []
    leakC=0
    if n:
        if thin_line and src_path.endswith('mbp-front-09_tight_patch.png'):
            # keep largest component only (main line 67px); drop 26px slanted jaw segment
            keep_id=int(np.argmax(sizes))+1
            leakC=int(work.sum()-sizes[keep_id-1]); work=(lab==keep_id)
        else:
            keep=np.zeros_like(work)
            for i,s in enumerate(sizes,1):
                if s>=100: keep|=(lab==i)
                else: leakC+=int(s)
            work=keep
    out=np.zeros_like(im); out[work]=im[work]
    return Image.fromarray(out), dict(orig_alpha=int(alpha.sum()), leak_nonmouth=int(leakA),
        leak_thin_or_bbox=int(leakB), leak_fragments=int(leakC),
        clean_alpha=int(work.sum()), removed=int(leakA+leakB+leakC))
def alpha_bbox(im):
    a=np.array(im.convert('RGBA'))[:,:,3]>0; ys,xs=np.where(a)
    return None if not len(xs) else (int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()),int(len(xs)))
def place(patch, old_scale, key):
    if old_scale is None: sc=210.8/patch.width
    else: sc=old_scale*SF
    nw=max(1,int(round(patch.width*sc))); nh=max(1,int(round(patch.height*sc)))
    rz=patch.resize((nw,nh), Image.LANCZOS)
    arr=np.array(rz); fringe=int(((arr[:,:,3]>0)&(arr[:,:,3]<128)).sum())
    arr[:,:,3]=(arr[:,:,3]>=128)*255; rz=Image.fromarray(arr)
    bb=alpha_bbox(rz); head=BASE.copy()
    if bb:
        cx=(bb[0]+bb[2])/2; cy=(bb[1]+bb[3])/2
        head.alpha_composite(rz,(int(round(TARGET[0]-cx)),int(round(TARGET[1]-cy))))
    return head, dict(scale=round(sc,4), resized=[nw,nh], alpha_bbox=bb,
        alpha_px=bb[4] if bb else 0, fringe_dropped=fringe, target=list(TARGET))
# sources: (key, source file, old fitted scale, angle, thin_line)
ITEMS=[
 ('mbp-v2', f'{TIGHT}/mbp-front-09_tight_patch.png', None, 'front', True),
 ('ah-v2', f'{TIGHT}/ah-front-03_tight_patch.png', 0.949, 'front', False),
 ('gk-v2', f'{TIGHT}/gk-front-05_tight_patch.png', 0.529, 'front', False),
 ('ee-v2', f'{OLD}/04_smile-ee_patch.png', None, 'front', True),  # scale set below from library
 ('ah34-v2', f'{OLD}/01_shout-ah_patch.png', 0.701, '3/4-source', False),
 ('mbp34-v2', f'{OLD}/02_closed-mbp_patch.png', 1.861, '3/4-source', True),
 ('smile34-v2', f'{OLD}/06_rbn01-open-smile_patch.png', None, '3/4-source', False),
]
# library fitted scales for ee and 06 from old json
lib=json.load(open(f'{R}/superhero-mouths-20261031/mouth-library-20261031.json'))
scales={e['id']:e.get('fitted_scale') for e in lib}
print('library scales', scales)
ITEMS[3]=('ee-v2', ITEMS[3][1], scales.get('04'), 'front', True)
ITEMS[6]=('smile34-v2', ITEMS[6][1], scales.get('06'), '3/4-source', False)
results=[]
for key,src,scale,angle,thin in ITEMS:
    patch,meas=clean(src, thin_line=thin)
    patch.save(f'{OUT}/mouths-v2/{key}_clean_patch.png')
    head,pm=place(patch, scale, key)
    head.save(f'{OUT}/fitted-v2/{key}_on_cape_head.png')
    results.append(dict(key=key, source=os.path.basename(src), angle=angle, thin_line_rule=thin, **meas, **pm))
    print(key, meas, pm, flush=True)
# PAH GO v2 GIF: MBP, AH, GK only (front), 24f @24fps 6 per viseme
order=['mbp-v2','ah-v2','gk-v2']
frames=[]
for k in order:
    frames.append(Image.open(f'{OUT}/fitted-v2/{k}_on_cape_head.png'))
gif=[]
for f in frames: gif.extend([f]*6)
gif[0].save(f'{OUT}/pahgo-v2-20261031.gif', save_all=True, append_images=gif[1:], duration=42, loop=0)
for i,f in enumerate(gif): f.save(f'{OUT}/frames-v2/pahgo-v2-f{i:02d}-20261031.png')
json.dump(results, open(f'{OUT}/measurements-v2-20261031.json','w'), indent=1)
print('DONE', len(results))
