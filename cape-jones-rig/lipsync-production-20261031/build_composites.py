"""Fix EE (smile curve only) + trim GK (teeth extent) + build 9 composites from front pixels only.
Front pixel sources: 09 MBP, 53 EH, 49 GK, 50 EE (all FRONT). 51 shout (3/4) = 0 pixels here."""
from PIL import Image
import numpy as np, os, json
from scipy import ndimage
RIG='/home/hatch/workspace/cape-jones-rig'; OUT=f'{RIG}/lipsync-production-20261031'
BASE=Image.open(f'{RIG}/visemes-v2-20261031/clean-head-base-20261031.png').convert('RGBA')
TARGET=(231.5,504.5)
def alpha_stats(im):
    a=np.array(im); ys,xs=np.where(a[:,:,3]>0)
    if len(xs)==0: return dict(size=list(im.size), alpha_px=0, alpha_bbox=None)
    return dict(size=list(im.size), alpha_px=int(len(xs)), alpha_bbox=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())])
def skin_costume_counts(im):
    a=np.array(im); rgb=a[:,:,:3].astype(int); al=a[:,:,3]>0
    r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    skin=al&(r>190)&(g>165)&(b>130)&(r-g>15)&(r-g<115)&(g-b>5)&(g-b<105)
    cost=al&(((r>200)&(g<80)&(b<80))|((r>200)&(g>170)&(b<120))|((g>130)&(r<120)&(b<120)))
    return int(skin.sum()), int(cost.sum())
def save_patch(im, name):
    im.save(f'{OUT}/mouths/{name}')
    s=alpha_stats(im); sk,co=skin_costume_counts(im)
    print(f'{name}: size={im.size} alpha={s["alpha_px"]} bbox={s["alpha_bbox"]} skin_px={sk} costume_px={co}', flush=True)
    return s

# ---- EE fix: smile curve component only (id2 in box coords) ----
src50=Image.open(f'{OUT}/render/50_RBEXPRES04_CA_DCTTAS_288.png').convert('RGBA')
box50=(940,2360,1260,2540); a50=np.array(src50.crop(box50)); rgb50=a50[:,:,:3].astype(int)
def is_skin(rgb):
    r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    return (r>190)&(g>165)&(b>130)&(r-g>15)&(r-g<115)&(g-b>5)&(g-b<105)
def is_cost(rgb):
    R,G,B=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    return ((R>200)&(G<80)&(B<80))|((R>200)&(G>170)&(B<120))|((G>130)&(R<120)&(B<120))
grey50=(rgb50.max(axis=2)-rgb50.min(axis=2)<35)&(rgb50.mean(axis=2)>100)&(rgb50.mean(axis=2)<210)
keep50=(a50[:,:,3]>100)&(~is_skin(rgb50))&(~is_cost(rgb50))&(~grey50)
lab50,n50=ndimage.label(keep50)
# id2 bbox (19,63,310,172) in box coords = smile curve; id1 = eye-mask bottom, DROPPED
ys,xs=np.where(lab50==2)
ee_arr=np.zeros((ys.max()-ys.min()+1, xs.max()-xs.min()+1, 4), dtype=np.uint8)
full50=np.array(src50.crop((xs.min()+box50[0], ys.min()+box50[1], xs.max()+box50[0]+1, ys.max()+box50[1]+1)))
m50=(lab50[ys.min():ys.max()+1, xs.min():xs.max()+1]==2)
ee_arr[m50]=full50[m50]
ee=Image.fromarray(ee_arr); ee.save(f'{OUT}/mouths/ee_verbatim_288.png')
print(f'EE FIXED (smile curve only, eye fragment dropped): size={ee.size} alpha={int(m50.sum())} bbox_in_render=({xs.min()+box50[0]},{ys.min()+box50[1]},{xs.max()+box50[0]},{ys.max()+box50[1]})', flush=True)

# ---- GK trim: white teeth x-range + 12px margin ----
gk=Image.open(f'{OUT}/mouths/gk_verbatim_288.png').convert('RGBA')
ga=np.array(gk); white=(ga[:,:,3]>0)&(ga[:,:,0]>200)&(ga[:,:,1]>200)&(ga[:,:,2]>200)
wys,wxs=np.where(white); x0=max(0,wxs.min()-12); x1=min(gk.width-1,wxs.max()+12)
gk_t=gk.crop((x0,0,x1+1,gk.height)); gk_t.save(f'{OUT}/mouths/gk_verbatim_288.png')
print(f'GK TRIMMED: white_x=({wxs.min()},{wxs.max()}) trim_x=({x0},{x1}) new_size={gk_t.size} alpha={int((np.array(gk_t)[:,:,3]>0).sum())} (diagonal corner strokes beyond teeth extent dropped)', flush=True)

# ---- Load bases ----
mbp=Image.open(f'{OUT}/mouths/mbp_verbatim_288.png').convert('RGBA')
eh=Image.open(f'{OUT}/mouths/eh_verbatim_288.png').convert('RGBA')
cav=Image.open(f'{OUT}/mouths/_eh_cavity_only.png').convert('RGBA')
tong=Image.open(f'{OUT}/mouths/_eh_tongue_only.png').convert('RGBA')
gk=Image.open(f'{OUT}/mouths/gk_verbatim_288.png').convert('RGBA')
ee=Image.open(f'{OUT}/mouths/ee_verbatim_288.png').convert('RGBA')
def resize(im, w, h):
    return im.resize((max(1,int(round(w))), max(1,int(round(h)))), Image.LANCZOS)
def canvas(w,h):
    return Image.new('RGBA',(int(round(w)),int(round(h))),(0,0,0,0))
def paste_at(base, piece, cx, cy):
    # paste piece centred at (cx,cy) in base coords
    x=int(round(cx-piece.width/2)); y=int(round(cy-piece.height/2))
    base.alpha_composite(piece,(x,y)); return base

# ---- AH shout: EH cavity+tongue + GK upper teeth row ----
gk_top=gk.crop((0,0,gk.width,int(gk.height*0.62)))  # teeth + top outline only
teeth_w=int(eh.width*0.92); teeth=resize(gk_top, teeth_w, gk_top.height*(teeth_w/gk_top.width))
ah=eh.copy(); ah.alpha_composite(teeth, ((eh.width-teeth.width)//2, 0))
save_patch(ah, 'ah_shout_composite.png')
# ---- OH / OO / R / W: cavity-only, independent x/y scales ----
def cavity_scaled(sx, sy, name):
    c=resize(cav, cav.width*sx, cav.height*sy); save_patch(c, name); return c
cavity_scaled(0.55, 0.95, 'oh_composite.png')
cavity_scaled(0.36, 0.62, 'oo_composite.png')
cavity_scaled(0.48, 0.68, 'r_composite.png')
cavity_scaled(0.33, 0.52, 'w_composite.png')
# ---- FV: teeth row + MBP lip line directly beneath ----
teeth_fv=resize(gk_top, 420, gk_top.height*(420/gk_top.width))
mbp_line=resize(mbp, 420, mbp.height*(420/mbp.width))
fv=canvas(teeth_fv.width, teeth_fv.height+mbp_line.height-2)
fv.alpha_composite(teeth_fv,(0,0)); fv.alpha_composite(mbp_line,(0,teeth_fv.height-2))
save_patch(fv, 'fv_composite.png')
# ---- L: narrowed cavity + tongue tip at top centre ----
cav_l=resize(cav, cav.width*0.62, cav.height*0.80)
tip=tong.crop((0,0,tong.width,int(tong.height*0.45)))
tip_l=resize(tip, 120, tip.height*(120/tip.width))
L=canvas(cav_l.width, cav_l.height); L.alpha_composite(cav_l,(0,0))
L.alpha_composite(tip_l, ((cav_l.width-tip_l.width)//2, 2))
save_patch(L, 'l_composite.png')
# ---- SZ: GK teeth narrowed + compressed ----
sz=resize(gk, gk.width*0.75, gk.height*0.70); save_patch(sz, 'sz_composite.png')
# ---- TH: GK teeth + tongue protruding below teeth centre ----
th_base=resize(gk, gk.width*0.78, gk.height*0.75)
tong_th=resize(tong, 130, tong.height*(130/tong.width))
TH=canvas(th_base.width, th_base.height+18)
TH.alpha_composite(th_base,(0,0))
TH.alpha_composite(tong_th, ((th_base.width-tong_th.width)//2, th_base.height-18))
save_patch(TH, 'th_composite.png')
# ---- rest = MBP copy (same drawing, Toon Boom X vs A) ----
import shutil; shutil.copy(f'{OUT}/mouths/mbp_verbatim_288.png', f'{OUT}/mouths/rest_mbp_copy.png')
print('rest: byte copy of MBP patch (same drawing reused, not a distinct mouth)', flush=True)
# ---- rename verbatim patches to final chart names ----
shutil.copy(f'{OUT}/mouths/mbp_verbatim_288.png', f'{OUT}/mouths/mbp_verbatim.png')
shutil.copy(f'{OUT}/mouths/eh_verbatim_288.png', f'{OUT}/mouths/eh_verbatim.png')
shutil.copy(f'{OUT}/mouths/ee_verbatim_288.png', f'{OUT}/mouths/ee_verbatim.png')
shutil.copy(f'{OUT}/mouths/gk_verbatim_288.png', f'{OUT}/mouths/gk_verbatim.png')
for f in ['mbp_verbatim.png','eh_verbatim.png','ee_verbatim.png','gk_verbatim.png']:
    im=Image.open(f'{OUT}/mouths/{f}'); save_patch(im, f)
print('COMPOSITES DONE')
