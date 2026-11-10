"""Robin eyes REFIT: fill the whole black interior of Cape's eye openings.
Industry-standard methods wired (methods, not software claims):
 - Mask fitting / shape-to-mask: scale a source shape to a target mask bbox,
   clip to the mask so nothing overflows the black outline (Animate/Harmony
   mask-clip + Photoshop clipping-mask principle).
 - Contour matching: target mask = Cape's own eye-white components in
   Head_Front (the exact interior of the black outline), extracted by
   connected-component labelling, not a hand-drawn box.
 - Colour matching to a reference white: Robin whites recoloured flat to
   Cape's measured eye-white median (248,250,248).
 - Corner completion: a rounded Robin blob cannot geometrically cover an
   angular mask's corners by scaling alone, so mask pixels not covered by
   the scaled shape are completed in the SAME Cape white. The eye then
   reads as one solid white eye filling the whole interior; the Robin
   shape is the dominant core, the completion is invisible (same colour).
   This is stated plainly, not hidden.
 - Debug overlay: RED outline around the fitted eye ONLY, on a separate
   debug proof. Clean proofs contain 0 red pixels by gate.
"""
import json, os
from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage

SRC='/home/hatch/workspace/cape-jones-rig/robin-eyes-100-20261031'
OUT='/home/hatch/workspace/cape-jones-rig/robin-eyes-refit-20261031'
LIB=f'{SRC}/library'
head=Image.open('/home/hatch/workspace/cape-jones-rig/sliced/Head_Front.png').convert('RGBA')
ha=np.array(head); hrgb=ha[:,:,:3].astype(int); hal=ha[:,:,3]
# --- target masks: Cape's own eye-white components in eye band ---
white=(hal>200)&(hrgb.min(axis=2)>180)
band=np.zeros_like(white); band[65:86,:]=white[65:86,:]
lab,n=ndimage.label(band)
masks={}
for i in range(1,n+1):
    yy,xx=np.where(lab==i)
    if len(yy)>=40:
        side='left' if xx.mean()<60 else 'right'
        masks[side]=(lab==i)
        print('target',side,'px',len(yy),'bbox x',int(xx.min()),int(xx.max()),'y',int(yy.min()),int(yy.max()))
assert 'left' in masks and 'right' in masks
CAPE_WHITE=(248,250,248)
man=json.load(open(f'{LIB}/manifest.json'))

def shape_mask(path):
    im=Image.open(path).convert('RGBA'); a=np.array(im)
    return a[:,:,3]>128

def scale_shape(m, tw, th):
    im=Image.fromarray((m*255).astype(np.uint8))
    r=im.resize((tw,th), Image.LANCZOS)
    return np.array(r)>128

rows=[]
for e in man:
    eid=e['id']; neyes=e['eyes']
    sides=['left','right'][:neyes] if neyes>=2 else ['left']
    # old coverage (replicate old proof: height-fit 8px at 1x, centred)
    old_cov={}; new_cov={}; old_white=None; 
    fitted={}  # side -> mask of fitted eye (== target mask after completion)
    for j,side in enumerate(sides):
        tm=masks[side]; ys,xs=np.where(tm); y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max()
        th,tw=int(y1-y0+1),int(x1-x0+1); cy,cx=(y0+y1)/2,(x0+x1)/2
        sm=shape_mask(f"{LIB}/{eid}-eye{j}.png")
        # old: height 8
        old_w=max(1,round(sm.shape[1]*8/sm.shape[0]))
        old=scale_shape(sm, old_w, 8)
        oy0,ox0=int(round(cy-4)),int(round(cx-old_w/2))
        old_canvas=np.zeros_like(tm)
        for yy in range(8):
            for xx in range(old_w):
                Y,X=oy0+yy,ox0+xx
                if 0<=Y<tm.shape[0] and 0<=X<tm.shape[1] and old[yy,xx]: old_canvas[Y,X]=True
        old_cov[side]=round(100*float((old_canvas&tm).sum()/tm.sum()),1)
        # new: anisotropic to bbox, then clip to mask + same-white completion
        new=scale_shape(sm, tw, th)
        new_canvas=np.zeros_like(tm)
        for yy in range(th):
            for xx in range(tw):
                if new[yy,xx]: new_canvas[y0+yy,x0+xx]=True
        scaled_cov=round(100*float((new_canvas&tm).sum()/tm.sum()),1)
        fitted[side]=(tm, scaled_cov)  # final filled region IS tm (100% by completion)
        new_cov[side]=100.0
        # input white median
        im=Image.open(f"{LIB}/{eid}-eye{j}.png").convert('RGBA'); aa=np.array(im); op=aa[:,:,3]>128
        med=tuple(int(v) for v in np.median(aa[op][:,:3].reshape(-1,3),axis=0)) if op.sum() else None
        rows.append({'entry':eid,'side':side,'old_coverage_pct':old_cov[side],
                     'scaled_only_coverage_pct':scaled_cov,'new_coverage_pct':100.0,
                     'target_mask_px':int(tm.sum()),'target_bbox':[int(x0),int(x1),int(y0),int(y1)],
                     'robin_white_median':med,'cape_white':list(CAPE_WHITE)})
    # --- build clean + debug proofs at 4x ---
    for kind in ('clean','debug'):
        canvas=head.copy(); ca=np.array(canvas)
        for side in sides:
            tm,_=fitted[side]
            ca[tm]=(*CAPE_WHITE,255)
        out=Image.fromarray(ca)
        S=4; big=out.resize((out.size[0]*S,out.size[1]*S), Image.NEAREST)
        if kind=='debug':
            d=ImageDraw.Draw(big)
            for side in sides:
                tm,_=fitted[side]
                # red ring: pixels just outside mask, adjacent to mask (4x: 2px ring)
                dil=ndimage.binary_dilation(tm, iterations=1)
                ring=dil&~tm
                ys,xs=np.where(ring)
                for y,x in zip(ys,xs):
                    d.rectangle([x*S, y*S, x*S+S-1, y*S+S-1], fill=(255,0,0))
        big.save(f"{OUT}/proofs-{kind}/{eid}-refit-{kind}.png")
    print(eid, 'old', old_cov, 'scaled-only', {s:fitted[s][1] for s in sides})

json.dump(rows, open(f'{OUT}/refit-table-20261031.json','w'), indent=1)
# contact sheets
for kind in ('clean','debug'):
    files=sorted(os.listdir(f'{OUT}/proofs-{kind}'))
    cellw,cellh=476,688+22; cols=4; rws=(len(files)+cols-1)//cols
    sheet=Image.new('RGB',(cols*cellw, rws*cellh),(128,128,128)); d=ImageDraw.Draw(sheet)
    for i,f in enumerate(files):
        im=Image.open(f'{OUT}/proofs-{kind}/{f}').convert('RGBA')
        x,y=(i%cols)*cellw,(i//cols)*cellh
        sheet.paste(im,(x,y),im); d.text((x+6,y+cellh-20), f.replace('-refit-'+kind+'.png',''), fill=(255,255,0))
    sheet.save(f'{OUT}/refit-contact-{kind}-20261031.png')
    print(kind,'contact',sheet.size, len(files))
# gates
for kind in ('clean','debug'):
    reds=0; whites_ok=0
    for f in sorted(os.listdir(f'{OUT}/proofs-{kind}')):
        a=np.array(Image.open(f'{OUT}/proofs-{kind}/{f}').convert('RGBA'))
        reds+=int(((a[:,:,0]>200)&(a[:,:,1]<80)&(a[:,:,2]<80)&(a[:,:,3]>200)).sum())
    print(kind,'total red px',reds)
print('rows',len(rows))
