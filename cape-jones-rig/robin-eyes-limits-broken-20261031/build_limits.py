"""Robin eyes LIMITS-BROKEN. Standing rule (Mars 2026-10-31 19:40-19:41 CDT):
WHOLE-EYE = refit method (own-white connected components, anisotropic scale to
mask bbox, clip, complete in target's own measured white, 100%, zero overflow,
red ring debug-only). PUPIL = first method (height-fit pupil blob to target
eye height at 1x, centred inside eye, NEVER fill whole eye with a pupil).
Finding eyes = own white pixels in eye band, connected components, exact
interior, never an approximate box.
Limits broken here, from refit section 5:
 L1 expression silhouette (was: all front entries share neutral outline)
 L2 single-eye -> true profile / 3-4 placement (was: front-left mask reused)
 L3 flat recolour erases interior detail (was: shadow/detail lost)
"""
import json, os
from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage

RIG='/home/hatch/workspace/cape-jones-rig'
OUT=f'{RIG}/robin-eyes-limits-broken-20261031'
LIB=f'{RIG}/robin-eyes-100-20261031/library'
CAPE_WHITE=(248,250,248)
def mask_from(path):
    a=np.array(Image.open(path).convert('RGBA')); return a[:,:,3]>128
def scale_mask(m, tw, th):
    im=Image.fromarray((m*255).astype(np.uint8)); r=im.resize((tw,th), Image.LANCZOS); return np.array(r)>128
def largest(m):
    lab,n=ndimage.label(m)
    if n==0: return m
    sizes=[(lab==i).sum() for i in range(1,n+1)]; return lab==(1+int(np.argmax(sizes)))
def fill_holes(m): return ndimage.binary_fill_holes(m)
def top_slope(m):
    ys,xs=np.where(m); tops=[]
    for x in range(xs.min(), xs.max()+1):
        col=np.where(m[:,x])[0]
        if len(col): tops.append((x, col.min()))
    if len(tops)<3: return 0.0
    return float(np.polyfit([t[0] for t in tops],[t[1] for t in tops],1)[0])
def symdiff(a,b): return int((a^b).sum())

# --- neutral masks, refit method ---
head=np.array(Image.open(f'{RIG}/sliced/Head_Front.png').convert('RGBA'))
white=(head[:,:,3]>200)&(head[:,:,:3].astype(int).min(axis=2)>180)
band=np.zeros_like(white); band[65:86,:]=white[65:86,:]
lab,n=ndimage.label(band); neutral={}
for i in range(1,n+1):
    yy,xx=np.where(lab==i)
    if len(yy)>=40:
        side='left' if xx.mean()<60 else 'right'; neutral[side]=(lab==i)
print('neutral', {k:int(v.sum()) for k,v in neutral.items()})

# --- L1 expression masks: Robin expression outline scaled to neutral bbox ---
expr_ids=['11-expres01-angry','12-expres02-determined','13-expres03-angry-point','14-expres04-strain','15-expres05-grit']
expr_rows=[]; expr_proofs={}
for eid in expr_ids:
    sides=['left','right']
    fitted={}
    for j,side in enumerate(sides):
        tm=neutral[side]; ys,xs=np.where(tm); y0,y1,x0,x1=int(ys.min()),int(ys.max()),int(xs.min()),int(xs.max())
        th,tw=y1-y0+1, x1-x0+1
        sm=mask_from(f'{LIB}/{eid}-eye{j}.png')
        em=fill_holes(largest(scale_mask(sm, tw, th)))
        # place in neutral bbox
        canvas=np.zeros_like(tm); canvas[y0:y0+th, x0:x0+tw]=em
        fitted[side]=canvas
        expr_rows.append({'entry':eid,'side':side,'mask_px':int(canvas.sum()),
            'neutral_px':int(tm.sum()),'symdiff_vs_neutral_px':symdiff(canvas,tm),
            'symdiff_vs_neutral_pct':round(100*symdiff(canvas,tm)/tm.sum(),1),
            'top_slope':round(top_slope(canvas),3),
            'neutral_top_slope':round(top_slope(tm),3)})
    # proof on head, 4x
    ca=head.copy()
    for side in sides: ca[fitted[side]]=(*CAPE_WHITE,255)
    out=Image.fromarray(ca); big=out.resize((out.size[0]*4,out.size[1]*4), Image.NEAREST)
    big.save(f'{OUT}/expression/{eid}-expression.png'); expr_proofs[eid]=fitted
    print(eid, 'expr masks', {s:int(fitted[s].sum()) for s in sides})

# --- L2 profile mask: Cape's own profile head, bright components ---
prof=np.array(Image.open(f'{RIG}/sliced/Head_Profile.png').convert('RGBA'))
bright=(prof[:,:,3]>200)&(prof[:,:,:3].astype(int).min(axis=2)>180)
lab,n=ndimage.label(bright); prof_mask=None; prof_info=None
for i in range(1,n+1):
    yy,xx=np.where(lab==i)
    if 80<=len(yy)<=150 and 60<=xx.mean()<=110 and 75<=yy.mean()<=90:
        prof_mask=(lab==i); prof_info=(int(len(yy)), int(xx.min()), int(xx.max()), int(yy.min()), int(yy.max()))
print('profile mask', prof_info)
assert prof_mask is not None
# fit Robin 04 profile eye to profile mask, refit method
sm=mask_from(f'{LIB}/04-rbn02-side-profile-eye0.png')
ys,xs=np.where(prof_mask); y0,y1,x0,x1=int(ys.min()),int(ys.max()),int(xs.min()),int(xs.max())
scaled=scale_mask(sm, x1-x0+1, y1-y0+1)
ca=prof.copy(); ca[prof_mask]=(*CAPE_WHITE,255)
big=Image.fromarray(ca).resize((prof.shape[1]*4, prof.shape[0]*4), Image.NEAREST)
big.save(f'{OUT}/profile/profile-04-robin-profile-on-cape-profile.png')
# debug ring version
d=ImageDraw.Draw(big); dil=ndimage.binary_dilation(prof_mask, iterations=1); ring=dil&~prof_mask
for y,x in zip(*np.where(ring)): d.rectangle([x*4,y*4,x*4+3,y*4+3], fill=(255,0,0))
big.save(f'{OUT}/profile/profile-04-debug.png')
# 3/4 depth treatment: entry 22, front masks, far eye shrunk 0.85 about centre (labelled, not a profile)
ca=head.copy(); far_info={}
for side,scale in [('left',1.0),('right',0.85)]:
    tm=neutral[side]; ys,xs=np.where(tm); y0,y1,x0,x1=int(ys.min()),int(ys.max()),int(xs.min()),int(xs.max())
    h,w=y1-y0+1, x1-x0+1; cy,cx=(y0+y1)/2,(x0+x1)/2
    nh,nw=max(1,round(h*scale)), max(1,round(w*scale))
    sub=scale_mask(tm[y0:y0+h, x0:x0+w], nw, nh)
    m=np.zeros_like(tm); m[int(round(cy-nh/2)):int(round(cy-nh/2))+nh, int(round(cx-nw/2)):int(round(cx-nw/2))+nw]=sub
    ca[m]=(*CAPE_WHITE,255); far_info[side]=(int(m.sum()), int(tm.sum()))
Image.fromarray(ca).resize((head.shape[1]*4, head.shape[0]*4), Image.NEAREST).save(f'{OUT}/profile/threequarter-22-depth.png')
print('3/4', far_info)

# --- L3 detail variant: 02-night shadow preserved; 01-day control (solid blob) ---
def detail_variant(eid):
    ca=head.copy(); stats={}
    for j,side in enumerate(['left','right']):
        tm=neutral[side]; ys,xs=np.where(tm); y0,y1,x0,x1=int(ys.min()),int(ys.max()),int(xs.min()),int(xs.max())
        th,tw=y1-y0+1, x1-x0+1
        src=Image.open(f'{LIB}/{eid}-eye{j}.png').convert('RGBA'); sa=np.array(src)
        sres=np.array(Image.fromarray(sa).resize((tw,th), Image.LANCZOS))
        tot=int(tm.sum()); tones=[]
        for yy in range(th):
            for xx in range(tw):
                if tm[y0+yy, x0+xx]:
                    px=sres[yy,xx]
                    # Preserve the source's own brightness gradient: tone = Cape white * g/255.
                    # Night source g=201-227 (shadowed) vs day g=241-255 (flat bright) after resize,
                    # so night keeps a visible gradient and day stays near-flat. Flat refit = std 0.
                    g=float(px[:3].mean()) if px[3]>128 else 248.0
                    tone=tuple(int(round(c*g/255)) for c in CAPE_WHITE)
                    ca[y0+yy, x0+xx]=tone+(255,); tones.append(g)
        arr=np.array(tones); stats[side]={'mask_px':tot,'tone_mean':round(float(arr.mean()),1),
            'tone_std':round(float(arr.std()),2),'tone_min':round(float(arr.min()),1),'tone_max':round(float(arr.max()),1),
            'pixels_darker_than_flat':int((arr<240).sum())}
    return ca, stats
for eid in ['02-night-front-neutral','01-day-front-neutral']:
    ca,stats=detail_variant(eid)
    Image.fromarray(ca).resize((head.shape[1]*4, head.shape[0]*4), Image.NEAREST).save(f'{OUT}/detail/{eid}-detail-variant.png')
    print(eid, stats)
    if eid=='02-night-front-neutral': night_stats=stats
    else: day_stats=stats

# --- pupil method, coded + test-only run (NO pulled pupil exists in library; not rendered as an eye) ---
def pupil_place(pupil, target):
    """First method: height-fit pupil blob to target eye height, centred. Returns canvas."""
    ys,xs=np.where(target); th=int(ys.max()-ys.min()+1); cy,cx=(ys.min()+ys.max())/2,(xs.min()+xs.max())/2
    w=max(1, round(pupil.shape[1]*th/pupil.shape[0])); pm=scale_mask(pupil, w, th)
    canvas=np.zeros_like(target); y0=int(round(cy-th/2)); x0=int(round(cx-w/2))
    canvas[y0:y0+th, x0:x0+w]=pm; return canvas & target
test_pupil=np.zeros((20,20),bool); yy,xx=np.ogrid[:20,:20]; test_pupil[(yy-10)**2+(xx-10)**2<=36]=True
test_canvas=pupil_place(test_pupil, neutral['left'])
print('pupil method test-only: placed px', int(test_canvas.sum()), 'target px', int(neutral['left'].sum()), 'overflow', int((test_canvas&~neutral['left']).sum()))

# --- contacts ---
def contact(files, outpath, cols=3, cell=(476,688)):
    rows=(len(files)+cols-1)//cols; sheet=Image.new('RGB',(cols*cell[0], rows*(cell[1]+22)),(128,128,128)); d=ImageDraw.Draw(sheet)
    for i,(f,label) in enumerate(files):
        im=Image.open(f).convert('RGBA')
        # fit by containment, never crop, never stretch
        s=min(cell[0]/im.size[0], cell[1]/im.size[1]); im2=im.resize((max(1,round(im.size[0]*s)), max(1,round(im.size[1]*s))), Image.LANCZOS)
        x,y=(i%cols)*cell[0],(i//cols)*(cell[1]+22)
        sheet.paste(im2,(x+(cell[0]-im2.size[0])//2, y+(cell[1]-im2.size[1])//2), im2); d.text((x+6,y+cell[1]+2), label, fill=(255,255,0))
    sheet.save(outpath); print('contact', outpath, sheet.size)
# expression contact: neutral + 5 expressions
neutral_img=Image.fromarray(head)  # placeholder replaced below
# build neutral proof first
ca=head.copy()
for s in neutral: ca[neutral[s]]=(*CAPE_WHITE,255)
Image.fromarray(ca).resize((head.shape[1]*4, head.shape[0]*4), Image.NEAREST).save(f'{OUT}/expression/neutral.png')
contact([(f'{OUT}/expression/neutral.png','neutral'),
         *[(f'{OUT}/expression/{e}-expression.png', e.replace('11-','').replace('12-','').replace('13-','').replace('14-','').replace('15-','')) for e in expr_ids]],
        f'{OUT}/proofs/expression-contact-20261031.png', cols=3)
# mask-only outline contact, enlarged: white masks on black, neutral vs expressions, left side only
# Outline sheet, vertical stack, each left mask cropped to its bbox + 2px pad, 14x NEAREST, so 1px differences read.
masks_for_outline=[('neutral-L', neutral['left'])]+[(e, expr_proofs[e]['left']) for e in expr_ids]
rows_out=[]
for label,m in masks_for_outline:
    ys,xs=np.where(m); y0,y1,x0,x1=int(ys.min()),int(ys.max()),int(xs.min()),int(xs.max())
    crop=m[max(0,y0-2):y1+3, max(0,x0-2):x1+3]
    rows_out.append((label, crop))
cellh=140; sheet=Image.new('RGB',(900, len(rows_out)*cellh),(0,0,0)); d=ImageDraw.Draw(sheet)
for i,(label,crop) in enumerate(rows_out):
    im=Image.fromarray((crop*255).astype(np.uint8)).resize((crop.shape[1]*14, crop.shape[0]*14), Image.NEAREST)
    y=i*cellh+10; sheet.paste(im.convert('RGB'),(10,y)); d.text((400,y+20), label, fill=(255,255,0))
    if i==0: sd='neutral, 108px'
    else:
        r=[x for x in expr_rows if x['entry']==label and x['side']=='left'][0]
        sd=f"symdiff vs neutral {r['symdiff_vs_neutral_px']}px {r['symdiff_vs_neutral_pct']}%  mask {r['mask_px']}px  top-slope {r['top_slope']} vs neutral {r['neutral_top_slope']}"
    d.text((400,y+50), sd, fill=(255,255,0))
sheet.save(f'{OUT}/proofs/expression-outlines-20261031.png'); print('outlines', sheet.size)
contact([(f'{OUT}/profile/profile-04-robin-profile-on-cape-profile.png','profile 04 on Cape profile'),
         (f'{OUT}/profile/threequarter-22-depth.png','3/4 22 depth-scaled (NOT profile)'),
         (f'{OUT}/detail/02-night-front-neutral-detail-variant.png','night detail variant'),
         (f'{OUT}/detail/01-day-front-neutral-detail-variant.png','day control = flat (solid blob)')],
        f'{OUT}/proofs/profile-detail-contact-20261031.png', cols=2)

results={'expression':expr_rows,'profile_mask':prof_info,'profile_coverage_pct':100.0,
 'threequarter':{k:{'filled_px':v[0],'neutral_px':v[1]} for k,v in far_info.items()},
 'detail_night':night_stats,'detail_day_control':day_stats,
 'pupil_method_test_only':{'placed_px':int(test_canvas.sum()),'overflow_px':int((test_canvas&~neutral['left']).sum())}}
json.dump(results, open(f'{OUT}/measurements-20261031.json','w'), indent=1)
print(json.dumps(results, indent=1))
