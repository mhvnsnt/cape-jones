from PIL import Image
import numpy as np, json, os
B='~/workspace/cape-jones-rig/'
B=os.path.expanduser(B)
def load(p):
    im=Image.open(p).convert('RGBA'); return np.array(im)
def place(canvas, im, cx, cy, s):
    # scale im by s, paste centred at (cx,cy) onto canvas alpha array (max alpha)
    h,w=im.shape[:2]
    nw,nh=max(1,round(w*s)),max(1,round(h*s))
    rs=Image.fromarray(im).resize((nw,nh), Image.LANCZOS)
    a=np.array(rs)
    x0,y0=int(round(cx-nw/2)),int(round(cy-nh/2))
    H,W=canvas.shape
    x1,y1=x0+nw,y0+nh
    cx0,cy0=max(0,x0),max(0,y0); cx1,cy1=min(W,x1),min(H,y1)
    if cx1<=cx0 or cy1<=cy0: return
    sub=a[cy0-y0:cy1-y0, cx0-x0:cx1-x0]
    reg=canvas[cy0:cy1, cx0:cx1]
    canvas[cy0:cy1, cx0:cx1]=np.maximum(reg, sub[:,:,3])
    return (x0,y0,nw,nh)
def col_top_bottom(alpha, x):
    col=alpha[:,x]
    ys=np.where(col>10)[0]
    return (int(ys[0]),int(ys[-1])) if len(ys) else (None,None)
# --- NECK GAP, wrist-fix layout, S=0.9557, canvas 1400x1600
S=0.9557
head=load(B+'side-pack-new-20261101/side_head_profile.png')
neck=load(B+'side-pack-new-20261101/side_cowl_neck.png')
H=W=0
ch=np.zeros((1600,1400),dtype=np.uint8); cn=np.zeros((1600,1400),dtype=np.uint8)
place(ch,head,662,200,S); place(cn,neck,663,367,S)
rows=[]
for x in range(560,760):
    ht,hb=col_top_bottom(ch,x); nt,nb=col_top_bottom(cn,x)
    if hb is not None and nt is not None:
        rows.append((x,hb,nt,nt-hb))
xs=[r[0] for r in rows]; gaps=[r[3] for r in rows]
print('NECK head-bottom/neck-top per column (x,hb,nt,gap):')
for r in rows[::10]: print('  ',r)
print('NECK overlap x range', min(xs), max(xs), 'gap min/max/mean', min(gaps), max(gaps), round(sum(gaps)/len(gaps),1))
face=[r for r in rows if r[0]>=700]; back=[r for r in rows if r[0]<660]
print('NECK face-side x>=700: n',len(face),'gap min/max/mean',min(r[3] for r in face),max(r[3] for r in face),round(sum(r[3] for r in face)/len(face),1))
print('NECK back-side x<660: n',len(back),'gap min/max/mean',min(r[3] for r in back),max(r[3] for r in back),round(sum(r[3] for r in back)/len(back),1))
# try neck shifts: dy up (negative cy shift) and dx, rotation approx ignored; report face-side mean gap + centre overlap
for dy in [0,-10,-20,-30,-43]:
    cn2=np.zeros((1600,1400),dtype=np.uint8); place(cn2,neck,663,367+dy,S)
    fg=[]; cg=[]
    for x in range(560,760):
        ht,hb=col_top_bottom(ch,x); nt,nb=col_top_bottom(cn2,x)
        if hb is not None and nt is not None:
            if x>=700: fg.append(nt-hb)
            if 640<=x<680: cg.append(nt-hb)
    print(f'NECK dy={dy}: face-side mean gap {round(sum(fg)/len(fg),1)} (n={len(fg)}), centre mean {round(sum(cg)/len(cg),1)}')
# neck top edge slant: top opaque y per column of neck alone
print('NECK piece top edge per column (native px):')
nt_im=neck[:,:,3]
for x in range(0,145,15):
    col=nt_im[:,x]; ys=np.where(col>10)[0]
    print('   x',x,'top',int(ys[0]) if len(ys) else None,'bottom',int(ys[-1]) if len(ys) else None)
print('HEAD piece bottom edge per column (native px):')
hd_im=head[:,:,3]
for x in range(0,173,15):
    col=hd_im[:,x]; ys=np.where(col>10)[0]
    print('   x',x,'top',int(ys[0]) if len(ys) else None,'bottom',int(ys[-1]) if len(ys) else None)
# --- BELT split profile
belt=load(B+'back-pack-base-20261101/back_belt_pelvis.png')
a=belt[:,:,3]
print('BELT rows: y, alpha-count, dark-count (rgb<60 & a>10)')
for y in range(0,160,5):
    row=a[y]; cnt=int((row>10).sum())
    dark=int(((belt[y,:,:3].max(axis=1)<60)&(row>10)).sum())
    print(f'   y={y} alpha={cnt} dark={dark}')
print('BELT col x-range per band of rows:')
for (y0,y1) in [(0,40),(40,60),(60,160)]:
    sub=a[y0:y1]; xs=np.where((sub>10).any(axis=0))[0]
    print(f'   rows {y0}-{y1}: x {xs[0]}-{xs[-1]}')
# --- PALM split profile
palm=load(B+'back-pack-base-20261101/back_forearm_gauntlet_hand_left.png')
pa=palm[:,:,3]
print('PALM rows: y, alpha-count, x-range')
for y in range(0,273,10):
    row=pa[y]; xs=np.where(row>10)[0]
    print(f'   y={y} alpha={int((row>10).sum())} x {int(xs[0]) if len(xs) else None}-{int(xs[-1]) if len(xs) else None}')
# wrist pinch: min alpha-count rows in 150-230
counts=[(y,int((pa[y]>10).sum())) for y in range(140,240)]
print('PALM narrowest rows 140-240:', sorted(counts,key=lambda t:t[1])[:8])
# --- side torso waist + Row7_10 fit numbers
torso=load(B+'side-pack-new-20261101/side_torso_belt.png')
ta=torso[:,:,3]
print('TORSO native', torso.shape[1], torso.shape[0])
for y in [200,250,300,330,360]:
    xs=np.where(ta[y]>10)[0]; print(f'   torso row y={y}: x {xs[0]}-{xs[-1]} w={xs[-1]-xs[0]+1}')
r7=load(B+'sliced-clean-20261031/A-root/08-body-parts-limbs-capes/Row7_10.png')
print('ROW7_10', r7.shape[1], r7.shape[0], 'opaque', int((r7[:,:,3]>10).sum()))
r5=load(B+'sliced-clean-20261031/A-root/08-body-parts-limbs-capes/Row5_15.png')
print('ROW5_15', r5.shape[1], r5.shape[0], 'opaque', int((r5[:,:,3]>10).sum()))
h10=load(B+'pack1/Hand_10.png')
print('HAND_10', h10.shape[1], h10.shape[0], 'opaque', int((h10[:,:,3]>10).sum()))
# fused palm bbox within forearm piece (rows below wrist ~190)
sub=pa[190:]; ys,xs=np.where(sub>10)
print('FUSED palm region rows>=190: x', xs.min(), xs.max(), 'w', xs.max()-xs.min()+1, 'y', 190+ys.min(), 190+ys.max(), 'h', 190+ys.max()-(190+ys.min())+1, 'opaque', int((sub>10).sum()))
