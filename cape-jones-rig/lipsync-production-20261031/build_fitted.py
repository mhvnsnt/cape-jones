"""Fit 14-viseme chart to Cape clean head, single target centre, jaw-drop proxy.
Fitted widths = design table; jaw: chin shift below y=560, hinge-row fill masked to
shifted chin width; mouth centre follows jaw by drop/4 (same proxy as movement system)."""
from PIL import Image, ImageDraw
import numpy as np, os, json
RIG='/home/hatch/workspace/cape-jones-rig'; OUT=f'{OUT_DIR}' if False else f'{RIG}/lipsync-production-20261031'
BASE=Image.open(f'{RIG}/visemes-v2-20261031/clean-head-base-20261031.png').convert('RGBA')
TARGET=(231.5,504.5)
CHART=[
 # key, label, patch, fitted_w, jaw, method, sources, angle
 ('rest','REST / neutral (closed)','rest_mbp_copy.png',178,0,'reuse (same drawing as MBP)','09_RBN01_CAMS','FRONT'),
 ('ee','EE (smile)','ee_verbatim.png',180,2,'verbatim single-source','50_RBEXPRES04','FRONT'),
 ('eh','EH (open smile)','eh_verbatim.png',194,10,'verbatim single-source','53_RBEXPRES03','FRONT'),
 ('ah','AH SHOUT (teeth + tongue)','ah_shout_composite.png',198,16,'composite: EH cavity+tongue + GK upper teeth','53_RBEXPRES03 + 49_RBEXPRES05','FRONT (both)'),
 ('oh','OH (tall oval)','oh_composite.png',110,12,'composite-transform: EH cavity-only, sx0.55 sy0.95','53_RBEXPRES03 (cavity)','FRONT'),
 ('oo','OO (small round)','oo_composite.png',72,8,'composite-transform: EH cavity-only, sx0.36 sy0.62','53_RBEXPRES03 (cavity)','FRONT'),
 ('mbp','MBP (closed)','mbp_verbatim.png',178,0,'verbatim single-source, 288dpi','09_RBN01_CAMS','FRONT'),
 ('fv','FV (teeth on lip)','fv_composite.png',170,2,'composite: GK teeth row + MBP lip line','49_RBEXPRES05 + 09_RBN01_CAMS','FRONT (both)'),
 ('l','L (tongue up)','l_composite.png',130,6,'composite: narrowed cavity + tongue tip at top','53_RBEXPRES03','FRONT'),
 ('sz','SZ (closed teeth)','sz_composite.png',150,2,'composite-transform: GK teeth, sx0.75 sy0.70','49_RBEXPRES05','FRONT'),
 ('th','TH (tongue thru teeth)','th_composite.png',150,4,'composite: GK teeth + tongue protruding below','49_RBEXPRES05 + 53_RBEXPRES03','FRONT (both)'),
 ('r','R (small rounded)','r_composite.png',90,6,'composite-transform: EH cavity-only, sx0.48 sy0.68','53_RBEXPRES03 (cavity)','FRONT'),
 ('w','W (tight round)','w_composite.png',64,6,'composite-transform: EH cavity-only, sx0.33 sy0.52','53_RBEXPRES03 (cavity)','FRONT'),
 ('gk','GK (teeth grin)','gk_verbatim.png',190,8,'verbatim single-source, chin curve dropped, corner outlines retained','49_RBEXPRES05','FRONT'),
]
def alpha_bbox(im):
    a=np.array(im); ys,xs=np.where(a[:,:,3]>0)
    return (int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()),int(len(xs))) if len(xs) else None
def jaw_shift(head, drop):
    if drop==0: return head.copy()
    a=np.array(head); H=a.shape[0]
    out=np.zeros_like(a); out[:560]=a[:560]
    out[560+drop:]=a[560:H-drop]
    # gap fill: hinge row 559, masked to shifted chin width at row 560+drop
    shifted_mask=out[560+drop,:,3]>0
    for y in range(560,560+drop):
        row=a[559].copy(); row[~shifted_mask]=0; out[y]=row
    return Image.fromarray(out)
def fit(patch, fitted_w, jaw):
    bb=alpha_bbox(patch); w=bb[2]-bb[0]+1
    sc=fitted_w/w; nw=max(1,int(round(patch.width*sc))); nh=max(1,int(round(patch.height*sc)))
    rs=patch.resize((nw,nh), Image.LANCZOS); bb2=alpha_bbox(rs)
    cx=(bb2[0]+bb2[2])/2; cy=(bb2[1]+bb2[3])/2
    head=jaw_shift(BASE, jaw)
    tx=int(round(TARGET[0]-cx)); ty=int(round(TARGET[1]+jaw/4-cy))
    head.alpha_composite(rs,(tx,ty))
    return head, dict(scale=round(sc,4), fitted_size=[nw,nh], fitted_alpha_bbox=bb2, fitted_alpha_px=bb2[4], jaw_drop=jaw, mouth_centre=[round(TARGET[0],1), round(TARGET[1]+jaw/4,1)])
meas=[]
for key,label,patchf,fw,jaw,method,src,ang in CHART:
    p=Image.open(f'{OUT}/mouths/{patchf}').convert('RGBA')
    ps=alpha_bbox(p); sk_co=None
    h,m=fit(p,fw,jaw); h.save(f'{OUT}/fitted/{key}-on-cape-head.png')
    a=np.array(p); rgb=a[:,:,:3].astype(int); al=a[:,:,3]>0
    r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    skin=int((al&(r>190)&(g>165)&(b>130)&(r-g>15)&(r-g<115)&(g-b>5)&(g-b<105)).sum())
    cost=int((al&(((r>200)&(g<80)&(b<80))|((r>200)&(g>170)&(b<120))|((g>130)&(r<120)&(b<120)))).sum())
    meas.append(dict(key=key,label=label,patch=patchf,patch_size=list(p.size),patch_alpha_px=ps[4],patch_alpha_bbox=ps[:4],
                     fitted_width=fw, method=method, sources=src, angle=ang, skin_test_px=skin, costume_test_px=cost, **m))
    print(key, label, 'patch', p.size, ps[4], '-> fitted', m['fitted_size'], 'alpha', m['fitted_alpha_px'], 'jaw', jaw, flush=True)
json.dump(meas, open(f'{OUT}/chart-measurements-20261031.json','w'), indent=1)
# contacts
def contact(img_paths, labels, path, thumb=(476,688), scale=0.42):
    tw,th=int(thumb[0]*scale),int(thumb[1]*scale); cols=4; rows=(len(img_paths)+cols-1)//cols
    sheet=Image.new('RGB',(cols*tw, rows*(th+26)),'white'); d=ImageDraw.Draw(sheet)
    for i,(p,lab) in enumerate(zip(img_paths,labels)):
        im=Image.open(p).convert('RGBA'); im.thumbnail((tw,th))
        bg=Image.new('RGBA',(tw,th),(255,255,255,255)); bg.alpha_composite(im,((tw-im.width)//2,(th-im.height)//2))
        x=(i%cols)*tw; y=(i//cols)*(th+26); sheet.paste(bg.convert('RGB'),(x,y)); d.text((x+4,y+th+4),lab,fill=(0,0,0))
    sheet.save(path); print('contact', path, sheet.size, flush=True)
keys=[c[0] for c in CHART]
contact([f'{OUT}/fitted/{k}-on-cape-head.png' for k in keys], [f'{c[0].upper()} {c[1]}' for c in CHART], f'{OUT}/chart-contact-20261031.png')
# patch contact on grey
def patch_contact(path):
    items=[(c[0],c[2]) for c in CHART]
    tw,th=360,240; cols=4; rows=(len(items)+cols-1)//cols
    sheet=Image.new('RGB',(cols*tw, rows*(th+26)),(128,128,128)); d=ImageDraw.Draw(sheet)
    for i,(k,pf) in enumerate(items):
        im=Image.open(f'{OUT}/mouths/{pf}').convert('RGBA'); im.thumbnail((tw-16,th-16))
        bg=Image.new('RGBA',(tw,th),(128,128,128,255)); bg.alpha_composite(im,((tw-im.width)//2,(th-im.height)//2))
        x=(i%cols)*tw; y=(i//cols)*(th+26); sheet.paste(bg.convert('RGB'),(x,y)); d.text((x+4,y+th+4),k.upper(),fill=(255,255,255))
    sheet.save(path); print('patch contact', path, sheet.size, flush=True)
patch_contact(f'{OUT}/chart-patches-contact-20261031.png')
# AH before/after + MBP old vs new contacts (fitted heads, mouth zooms)
def zoom_contact(paths, labels, path):
    # crop mouth zone from fitted heads (x 110-360, y 420-590) enlarged 2x
    tw,th=500,340; cols=len(paths)
    sheet=Image.new('RGB',(cols*tw, th+26),'white'); d=ImageDraw.Draw(sheet)
    for i,(p,lab) in enumerate(zip(paths,labels)):
        im=Image.open(p).convert('RGBA').crop((110,420,360,590)); im=im.resize((500,340), Image.LANCZOS)
        sheet.paste(im.convert('RGB'),(i*tw,0)); d.text((i*tw+4,th+4),lab,fill=(0,0,0))
    sheet.save(path); print('zoom contact', path, sheet.size, flush=True)
zoom_contact([f'{OUT}/fitted/eh-on-cape-head.png', f'{OUT}/fitted/ah-on-cape-head.png'], ['OLD AH-front = EH smile, NO teeth','NEW AH shout = teeth + tongue, FRONT'], f'{OUT}/ah-before-after-contact-20261031.png')
old_mbp=f'{RIG}/pahgo-mouth-fix-20261031/fitted-tight/mbp-front-09_on_cape_head.png'
zoom_contact([old_mbp, f'{OUT}/fitted/mbp-on-cape-head.png'], ['OLD MBP tight 86px, jaw fragment, 2.45x','NEW MBP verbatim 288dpi 68px, 1 comp, 2.62x'], f'{OUT}/mbp-old-vs-new-contact-20261031.png')
zoom_contact([f'{OUT}/fitted/oh-on-cape-head.png', f'{OUT}/fitted/oo-on-cape-head.png', f'{OUT}/fitted/r-on-cape-head.png', f'{OUT}/fitted/w-on-cape-head.png'], ['OH tall oval','OO small round','R small rounded','W tight round'], f'{OUT}/round-visemes-contact-20261031.png')
print('FITTED DONE')
