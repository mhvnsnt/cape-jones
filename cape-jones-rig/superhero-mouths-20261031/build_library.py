"""Pulled superhero mouth library, Robin only (Batman 0, Superman 0 in archive).
Method: verbatim crop from Ghostscript render / JPG, then mouth-only cutout =
non-skin connected components in the measured box, pixels unchanged.
No redraw, no PIL vector mouth."""
from PIL import Image
import numpy as np, os, json
from scipy import ndimage
EYE='/home/hatch/workspace/cape-jones-rig/robin-eyes-100-20261031'
OUT='/home/hatch/workspace/cape-jones-rig/superhero-mouths-20261031'
os.makedirs(f'{OUT}/mouths', exist_ok=True)
os.makedirs(f'{OUT}/raw', exist_ok=True)
os.makedirs(f'{OUT}/fitted', exist_ok=True)
ENTRIES=[
 dict(id='01', key='shout-ah', label='SHOUT / AH - wide open, teeth top, tongue', source='51_RBEXPRES01_CA_DCTTAS.EPS', render='51_RBEXPRES01_CA_DCTTAS.png', box=(200,755,600,945), viseme='AH'),
 dict(id='02', key='closed-mbp', label='CLOSED / MBP - thin closed line', source='47_RBEXPRES02_CA_DCTTAS.EPS', render='47_RBEXPRES02_CA_DCTTAS.png', box=(330,1225,480,1250), viseme='MBP'),
 dict(id='03', key='open-smile-eh', label='OPEN SMILE / EH - wide open, tongue, no teeth', source='53_RBEXPRES03_CA_DCTTAS.EPS', render='53_RBEXPRES03_CA_DCTTAS.png', box=(270,1085,565,1182), viseme='EH', drop_costume=True),
 dict(id='04', key='smile-ee', label='SMILE / EE - closed curved smile line', source='50_RBEXPRES04_CA_DCTTAS.EPS', render='50_RBEXPRES04_CA_DCTTAS.png', box=(470,1180,630,1270), viseme='EE'),
 dict(id='05', key='grit-teeth', label='GRIT / teeth grin, wide', source='49_RBEXPRES05_CA_DCTTAS.EPS', render='49_RBEXPRES05_CA_DCTTAS.png', box=(135,1110,665,1190), viseme='GK'),
 dict(id='06', key='rbn01-open-smile', label='OPEN SMILE (model) - teeth top, tongue', source='23_RBN01_CA_DCTTAS.EPS', render='23_RBN01_CA_DCTTAS.png', box=(525,695,660,780), viseme='AH-alt', drop_costume=True),
 dict(id='07', key='day-neutral-closed', label='NEUTRAL CLOSED - straight line (Day head close-up)', source='02_ROBIN_Day.jpg', render=None, box=(890,765,940,775), viseme='rest', black_only=True),
]
def is_skin(rgb):
    r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    return (r>190)&(g>165)&(b>130)&(r-g>15)&(r-g<115)&(g-b>5)&(g-b<105)
results=[]
for e in ENTRIES:
    src = f"{EYE}/render/{e['render']}" if e['render'] else f"{EYE}/raw/{e['source']}"
    im=Image.open(src).convert('RGBA')
    x0,y0,x1,y1=e['box']
    crop=im.crop((x0,y0,x1+1,y1+1))
    crop.save(f"{OUT}/raw/{e['id']}_{e['key']}_raw.png")
    a=np.array(crop); rgb=a[:,:,:3].astype(int); al=a[:,:,3]
    skin=is_skin(rgb)
    # white background (Day JPG) counts as background, not mouth
    white=(rgb[:,:,0]>235)&(rgb[:,:,1]>235)&(rgb[:,:,2]>235) if e['render'] is None else np.zeros(rgb.shape[:2], bool)
    grey=(rgb.max(axis=2)-rgb.min(axis=2)<35)&(rgb.mean(axis=2)>100)&(rgb.mean(axis=2)<210)
    if e.get('black_only'):
        keep=(al>100)&(rgb[:,:,0]<190)&(rgb[:,:,1]<190)&(rgb[:,:,2]<190)
    else:
        keep=(al>100)&(~skin)&(~white)&(~grey)
    lab,n=ndimage.label(keep)
    # keep components area>=25, drop tiny specks; keep all larger ones (mouth shape is connected via outline)
    mask=np.zeros(keep.shape, bool)
    kept=[]
    for i in range(1,n+1):
        yy,xx=np.where(lab==i)
        if len(yy)>=25:
            mask[lab==i]=True; kept.append(int(len(yy)))
    if e.get('drop_costume'):
        R,G,B=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
        costume=((R>200)&(G<80)&(B<80))|((R>200)&(G>170)&(B<120))|((G>130)&(R<120)&(B<120))
        mask=mask&(~costume)
    out=np.zeros_like(a); out[mask]=a[mask]
    Image.fromarray(out).save(f"{OUT}/mouths/{e['id']}_{e['key']}_patch.png")
    ys,xs=np.where(mask)
    bbox=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())] if len(xs) else None
    print(e['id'], e['key'], 'raw', crop.size, 'patch px', int(mask.sum()), 'kept comps', sorted(kept, reverse=True)[:6], 'bbox-in-crop', bbox, flush=True)
    rec=dict(e, patch=f"mouths/{e['id']}_{e['key']}_patch.png", raw=f"raw/{e['id']}_{e['key']}_raw.png", patch_px=int(mask.sum()), patch_bbox=bbox, components=sorted(kept, reverse=True)[:6])
    rec['status']='rejected-not-cleanly-extractable' if e['id']=='07' else 'usable'
    if e['id']=='07': rec['reject_reason']='Day JPG neutral line is faint/compressed and mixed with nose shading; fitted proof shows smudge + angular fragment, not a clean line. EXPRES02 closed line is used for rest/MBP instead.'
    results.append(rec)
# fitted heads: Cape clean-head-base 4x, mouth zone box [111,409,392,560]
base=Image.open('/home/hatch/workspace/cape-jones-rig/visemes-v2-20261031/clean-head-base-20261031.png').convert('RGBA')
zx0,zy0,zx1,zy1=111,409,392,560; zw,zh=zx1-zx0, zy1-zy0
for r in results:
    p=Image.open(f"{OUT}/{r['patch']}")
    # scale by width to zone width, centre in zone
    sc=zw/p.width
    nw,nh=int(round(p.width*sc)), int(round(p.height*sc))
    if nh>zh:  # very tall mouth: scale by height instead
        sc=zh/p.height; nw,nh=int(round(p.width*sc)), int(round(p.height*sc))
    patch=p.resize((nw,nh), Image.LANCZOS)
    head=base.copy()
    head.alpha_composite(patch, (zx0+(zw-nw)//2, zy0+(zh-nh)//2))
    head.save(f"{OUT}/fitted/{r['id']}_{r['key']}_on_cape_head.png")
    r['fitted']=f"fitted/{r['id']}_{r['key']}_on_cape_head.png"; r['fitted_scale']=round(sc,3); r['fitted_size']=[nw,nh]
    print('fitted', r['id'], r['key'], 'scale', round(sc,3), 'size', nw, nh, flush=True)
json.dump(results, open(f'{OUT}/mouth-library-20261031.json','w'), indent=1)
print('DONE', len(results))
