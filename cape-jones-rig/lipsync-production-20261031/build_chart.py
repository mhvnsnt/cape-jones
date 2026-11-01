"""Lip-sync production chart 2026-10-31. Front sources ONLY (all FRONT by prior angle audit):
09_RBN01_CAMS (MBP model sheet), 53_RBEXPRES03 (EH open smile), 49_RBEXPRES05 (GK grit),
50_RBEXPRES04 (EE smile). 51 shout is 3/4 and contributes ZERO pixels to any front patch.
Method: Ghostscript 288dpi renders (vector source, render DPI disclosed), non-skin +
colour filters, connected-component mouth isolation. Composites use ONLY pixels from
those 4 front sources (crop/scale/translate/overlay transforms, no vector drawing,
no new colours, no skin/costume/jaw pixels)."""
from PIL import Image
import numpy as np, os, json
from scipy import ndimage
RIG='/home/hatch/workspace/cape-jones-rig'
OUT=f'{RIG}/lipsync-production-20261031'
EYE=f'{RIG}/robin-eyes-100-20261031'
GS=f'{EYE}/gsroot/root/usr/bin/gs'
import subprocess
env=dict(os.environ, LD_LIBRARY_PATH=f'{EYE}/gsroot/root/usr/lib/x86_64-linux-gnu')
ARGS=['-dBATCH','-dNOPAUSE','-sDEVICE=pngalpha','-r288',
      f'-I{EYE}/gsroot/share/ghostscript/10.02/lib',
      f'-I{EYE}/gsroot/share/ghostscript/10.02/Resource/Init',
      f'-sGenericResourceDir={EYE}/gsroot/share/ghostscript/10.02/Resource/']
SOURCES={'09':'09_RBN01_CAMS_DCTTAS.EPS','53':'53_RBEXPRES03_CA_DCTTAS.EPS',
         '49':'49_RBEXPRES05_CA_DCTTAS.EPS','50':'50_RBEXPRES04_CA_DCTTAS.EPS'}
os.makedirs(f'{OUT}/render', exist_ok=True)
for k,f in SOURCES.items():
    out=f'{OUT}/render/{f.rsplit(".",1)[0]}_288.png'
    if not os.path.exists(out):
        p=subprocess.run([GS]+ARGS+[f'-o{out}', f'{EYE}/raw/{f}'], capture_output=True, text=True, timeout=300, env=env)
        print('render', k, os.path.exists(out), flush=True)
    else:
        print('render cached', k, flush=True)

def is_skin(rgb):
    r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    return (r>190)&(g>165)&(b>130)&(r-g>15)&(r-g<115)&(g-b>5)&(g-b<105)
def is_costume(rgb):
    R,G,B=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    return ((R>200)&(G<80)&(B<80))|((R>200)&(G>170)&(B<120))|((G>130)&(R<120)&(B<120))
def comps(mask):
    lab,n=ndimage.label(mask)
    out=[]
    for i in range(1,n+1):
        ys,xs=np.where(lab==i)
        if len(ys)>=20:
            out.append(dict(id=i, px=int(len(ys)), bbox=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]))
    return lab, sorted(out, key=lambda d:-d['px'])
def report(name, mask, lab, kept_ids):
    _,cs=comps(mask)
    print(f'{name}: total kept-px={int(mask.sum())} components={cs} kept_ids={kept_ids}', flush=True)
    return cs

# ---- MBP verbatim: box 2x of (180,680,321,711) ----
src=Image.open(f'{OUT}/render/09_RBN01_CAMS_DCTTAS_288.png').convert('RGBA')
box=(360,1360,642,1422); a=np.array(src.crop(box))
dark=(a[:,:,3]>100)&(a[:,:,0]<100)&(a[:,:,1]<100)&(a[:,:,2]<100)
lab,cs=comps(dark)
# interior component = mouth (jaw pieces touch edges)
mouth=None
for c in cs:
    bb=c['bbox']
    if bb[0]>0 and bb[2]<a.shape[1]-1 and bb[1]>0 and bb[3]<a.shape[0]-1:
        mouth=c; break
assert mouth, 'no interior MBP component'
i=mouth['id']; ys,xs=np.where(lab==i)
mbp_arr=np.zeros((ys.max()-ys.min()+1, xs.max()-xs.min()+1, 4), dtype=np.uint8)
full=np.array(src.crop((xs.min()+box[0], ys.min()+box[1], xs.max()+box[0]+1, ys.max()+box[1]+1)))
m=(lab[ys.min():ys.max()+1, xs.min():xs.max()+1]==i)
mbp_arr[m]=full[m]
mbp=Image.fromarray(mbp_arr); mbp.save(f'{OUT}/mouths/mbp_verbatim_288.png')
# continuity: every column in bbox has >=1 dark px?
cols_with=np.where(m.any(axis=0))[0]
print(f"MBP verbatim: size={mbp.size} px={int(m.sum())} bbox_in_render=({xs.min()+box[0]},{ys.min()+box[1]},{xs.max()+box[0]},{ys.max()+box[1]}) cols_covered={len(cols_with)}/{m.shape[1]} missing_cols={sorted(set(range(m.shape[1]))-set(cols_with.tolist()))}", flush=True)
print(f"MBP all components in box: {cs}", flush=True)

# ---- EH verbatim: box 2x of (270,1085,565,1182), colour filter + mouth-body component ----
src53=Image.open(f'{OUT}/render/53_RBEXPRES03_CA_DCTTAS_288.png').convert('RGBA')
box53=(540,2170,1130,2364); a53=np.array(src53.crop(box53)); rgb53=a53[:,:,:3].astype(int)
skin=is_skin(rgb53); costume=is_costume(rgb53)
grey=(rgb53.max(axis=2)-rgb53.min(axis=2)<35)&(rgb53.mean(axis=2)>100)&(rgb53.mean(axis=2)<210)
keep53=(a53[:,:,3]>100)&(~skin)&(~costume)&(~grey)
lab53,cs53=comps(keep53)
print(f'EH box components: {cs53}', flush=True)
# mouth body = largest component that contains the tongue (brown px). Find brown mask overlap per component.
R,G,B=rgb53[:,:,0],rgb53[:,:,1],rgb53[:,:,2]
brown=(R>120)&(R<210)&(G>50)&(G<140)&(B<110)&(R-G>40)
best=None
for c in cs53:
    sub=(lab53==c['id'])
    ov=int((sub&brown).sum())
    if ov>200 and (best is None or ov>best[0]): best=(ov,c)
print('EH brown-overlap best:', best, flush=True)
i=best[1]['id']; ys,xs=np.where(lab53==i)
eh_arr=np.zeros((ys.max()-ys.min()+1, xs.max()-xs.min()+1, 4), dtype=np.uint8)
full53=np.array(src53.crop((xs.min()+box53[0], ys.min()+box53[1], xs.max()+box53[0]+1, ys.max()+box53[1]+1)))
m53=(lab53[ys.min():ys.max()+1, xs.min():xs.max()+1]==i)
eh_arr[m53]=full53[m53]
eh=Image.fromarray(eh_arr); eh.save(f'{OUT}/mouths/eh_verbatim_288.png')
print(f'EH verbatim: size={eh.size} px={int(m53.sum())} bbox_in_render=({xs.min()+box53[0]},{ys.min()+box53[1]},{xs.max()+box53[0]},{ys.max()+box53[1]})', flush=True)
# EH black-cavity-only (for OH/OO/R/W): dark pixels within EH patch
eh_a=np.array(eh); dark_eh=(eh_a[:,:,3]>0)&(eh_a[:,:,0]<90)&(eh_a[:,:,1]<90)&(eh_a[:,:,2]<90)
cav=np.zeros_like(eh_a); cav[dark_eh]=eh_a[dark_eh]
cav_im=Image.fromarray(cav)
# crop cavity to its own bbox
ys,xs=np.where(dark_eh); cav_crop=cav_im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); cav_crop.save(f'{OUT}/mouths/_eh_cavity_only.png')
print(f'EH cavity-only: size={cav_crop.size} px={int(dark_eh.sum())}', flush=True)
# EH tongue-only (brown pixels within EH patch)
tong=(eh_a[:,:,3]>0)&(R[ys.min():ys.max()+1, xs.min():xs.max()+1] if False else False)
# recompute tongue on full eh patch coords: use eh patch rgb
rgb_eh=eh_a[:,:,:3].astype(int); Re,Ge,Be=rgb_eh[:,:,0],rgb_eh[:,:,1],rgb_eh[:,:,2]
brown_eh=(eh_a[:,:,3]>0)&(Re>120)&(Re<210)&(Ge>50)&(Ge<140)&(Be<110)&(Re-Ge>40)
tong_arr=np.zeros_like(eh_a); tong_arr[brown_eh]=eh_a[brown_eh]
tong_im=Image.fromarray(tong_arr); ys2,xs2=np.where(brown_eh)
tong_crop=tong_im.crop((xs2.min(),ys2.min(),xs2.max()+1,ys2.max()+1)); tong_crop.save(f'{OUT}/mouths/_eh_tongue_only.png')
print(f'EH tongue-only: size={tong_crop.size} px={int(brown_eh.sum())} bbox_in_patch=({xs2.min()},{ys2.min()},{xs2.max()},{ys2.max()})', flush=True)

# ---- GK verbatim: box 2x of (135,1110,665,1190), colour filter, teeth band ----
src49=Image.open(f'{OUT}/render/49_RBEXPRES05_CA_DCTTAS_288.png').convert('RGBA')
box49=(270,2220,1330,2380); a49=np.array(src49.crop(box49)); rgb49=a49[:,:,:3].astype(int)
skin49=is_skin(rgb49); cost49=is_costume(rgb49)
grey49=(rgb49.max(axis=2)-rgb49.min(axis=2)<35)&(rgb49.mean(axis=2)>100)&(rgb49.mean(axis=2)<210)
keep49=(a49[:,:,3]>100)&(~skin49)&(~cost49)&(~grey49)
lab49,cs49=comps(keep49)
print(f'GK box components: {cs49}', flush=True)
# teeth band = component containing white px, rows above chin curve: take largest white-overlap component, then drop rows below white extent+6
white49=(rgb49[:,:,0]>200)&(rgb49[:,:,1]>200)&(rgb49[:,:,2]>200)
best=None
for c in cs49:
    sub=(lab49==c['id']); ov=int((sub&white49).sum())
    if best is None or ov>best[0]: best=(ov,c)
print('GK white-overlap best:', best, flush=True)
i=best[1]['id']; ys,xs=np.where(lab49==i)
sub_a=np.array(src49.crop((xs.min()+box49[0], ys.min()+box49[1], xs.max()+box49[0]+1, ys.max()+box49[1]+1)))
sub_m=(lab49[ys.min():ys.max()+1, xs.min():xs.max()+1]==i)
sub_rgb=sub_a[:,:,:3].astype(int)
white_rows=np.where((sub_m)&(sub_rgb[:,:,0]>200)&(sub_rgb[:,:,1]>200)&(sub_rgb[:,:,2]>200))[0]
wmax=int(white_rows.max()) if len(white_rows) else sub_a.shape[0]-1
cut=wmax+8  # keep a few rows of outline below teeth, drop chin curve below
gk_arr=np.zeros((cut+1, sub_a.shape[1], 4), dtype=np.uint8); gk_arr[:]=sub_a[:cut+1]; gk_arr[~sub_m[:cut+1]]=0
gk=Image.fromarray(gk_arr); gk.save(f'{OUT}/mouths/gk_verbatim_288.png')
print(f'GK verbatim: size={gk.size} px={int((gk_arr[:,:,3]>0).sum())} white_row_max={wmax} cut={cut} bbox_in_render=({xs.min()+box49[0]},{ys.min()+box49[1]},{xs.max()+box49[0]},{ys.max()+box49[1]})', flush=True)
# GK teeth-only strip (white + outline rows 0..cut, cropped to white bbox x-range)
gk_a=np.array(gk); print(f'GK teeth strip alpha px={int((gk_a[:,:,3]>0).sum())}', flush=True)

# ---- EE verbatim: box 2x of (470,1180,630,1270), non-skin filter ----
src50=Image.open(f'{OUT}/render/50_RBEXPRES04_CA_DCTTAS_288.png').convert('RGBA')
box50=(940,2360,1260,2540); a50=np.array(src50.crop(box50)); rgb50=a50[:,:,:3].astype(int)
skin50=is_skin(rgb50); cost50=is_costume(rgb50)
grey50=(rgb50.max(axis=2)-rgb50.min(axis=2)<35)&(rgb50.mean(axis=2)>100)&(rgb50.mean(axis=2)<210)
keep50=(a50[:,:,3]>100)&(~skin50)&(~cost50)&(~grey50)
lab50,cs50=comps(keep50)
print(f'EE box components: {cs50}', flush=True)
# keep components: main smile curve = largest; upper mark = smaller component ABOVE main curve -> drop if separate and y-max < main y-min+10
cs50_sorted=sorted(cs50, key=lambda d:-d['px'])
main=cs50_sorted[0]
keep_ids=[main['id']]
for c in cs50_sorted[1:]:
    if c['bbox'][3] < main['bbox'][1]+10:
        print(f"EE dropping upper-mark component {c} (above main curve)", flush=True)
    else:
        keep_ids.append(c['id']); print(f"EE keeping extra component {c}", flush=True)
mask50=np.isin(lab50, keep_ids)
ys,xs=np.where(mask50)
ee_arr=np.zeros((ys.max()-ys.min()+1, xs.max()-xs.min()+1, 4), dtype=np.uint8)
full50=np.array(src50.crop((xs.min()+box50[0], ys.min()+box50[1], xs.max()+box50[0]+1, ys.max()+box50[1]+1)))
m50=mask50[ys.min():ys.max()+1, xs.min():xs.max()+1]
ee_arr[m50]=full50[m50]
ee=Image.fromarray(ee_arr); ee.save(f'{OUT}/mouths/ee_verbatim_288.png')
print(f'EE verbatim: size={ee.size} px={int(m50.sum())} kept_ids={keep_ids} bbox_in_render=({xs.min()+box50[0]},{ys.min()+box50[1]},{xs.max()+box50[0]},{ys.max()+box50[1]})', flush=True)
print('EXTRACTION DONE')
