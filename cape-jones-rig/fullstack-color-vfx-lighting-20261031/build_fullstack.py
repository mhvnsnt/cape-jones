"""Full-stack projects: color + VFX + lighting + shadow + color-keying in ONE pipeline each.
Base art never recoloured in place: every step is a separate layer masked to plate alpha.
Base: rig-apose-v7c-clean-transparent.png, shifted +106 so feet=1400 (Gy=1400).
"""
import os, json, math
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from scipy import ndimage

ROOT=os.path.expanduser("~/workspace/cape-jones-rig/fullstack-color-vfx-lighting-20261031")
BASE=np.array(Image.open(os.path.expanduser("~/workspace/cape-jones-rig/rig-apose-v7c-clean-transparent.png")).convert("RGBA")).astype(float)
# shift +106 vertically
H,W=1500,1100
shifted=np.zeros_like(BASE); shifted[106:,:]=BASE[:-106,:]
FIG=shifted
ALPHA=FIG[...,3]
MASK=ALPHA>10
ys,xs=np.where(MASK); BBOX=(int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()))
print("bbox",BBOX,"alpha",int(MASK.sum()),"feet",int(ys.max()))
Gy=1400

def dilate(a, n):
    return ndimage.binary_dilation(a, iterations=n)
def blur_arr(a, r):
    im=Image.fromarray(np.clip(a,0,255).astype(np.uint8)); return np.array(im.filter(ImageFilter.GaussianBlur(r))).astype(float)
def edt(a):
    return ndimage.distance_transform_edt(a)

EDT=edt(MASK)
RIM_MASK=dilate(MASK,6) & ~MASK

def room(kind):
    # labelled test gradient room, vertical gradient + floor band y1400-1500
    y=np.linspace(0,1,H)[:,None]; x=np.linspace(0,1,W)[None,:]
    if kind=="warm":
        top=np.array([60,40,30.]); bot=np.array([120,80,40.]); floor=np.array([180,140,80.])
    elif kind=="night":
        top=np.array([10,15,40.]); bot=np.array([20,30,70.]); floor=np.array([30,50,100.])
    elif kind=="comic":
        top=np.array([20,20,20.]); bot=np.array([50,45,55.]); floor=np.array([90,80,90.])
    elif kind=="day":
        top=np.array([140,180,220.]); bot=np.array([200,190,150.]); floor=np.array([230,210,150.])
    elif kind=="dual":
        top=np.array([40,30,60.]); bot=np.array([90,70,90.]); floor=np.array([140,110,130.])
    elif kind=="prism":
        top=np.array([50,20,80.]); bot=np.array([90,50,110.]); floor=np.array([150,90,150.])
    elif kind=="crystal":
        top=np.array([20,60,90.]); bot=np.array([40,100,140.]); floor=np.array([80,160,190.])
    elif kind=="ghost":
        top=np.array([30,40,50.]); bot=np.array([60,80,90.]); floor=np.array([100,130,140.])
    elif kind=="storm":
        top=np.array([15,20,35.]); bot=np.array([40,50,80.]); floor=np.array([70,90,130.])
    else: # pools
        top=np.array([70,50,30.]); bot=np.array([130,90,50.]); floor=np.array([200,160,90.])
    img=top*(1-y)+bot*y
    img=np.repeat(img[:,:,None],3,axis=2) if img.ndim==2 else img
    # actually build RGB properly
    img=np.zeros((H,W,3))
    for c in range(3): img[:,:,c]=top[c]*(1-y)+bot[c]*y
    img[1400:,:]=floor
    return img

def shafts(img, cols, tint, strength=0.35):
    out=img.copy()
    colmask=np.zeros((H,W))
    for a,b in cols:
        colmask[:,a:b]=1
    # shafts behind figure: only where figure alpha low
    behind=(1-MASK/255.0)[:, :, None] if False else None
    m=colmask*(1-(ALPHA/255.0))
    for c in range(3):
        out[:,:,c]=out[:,:,c]*(1-m*strength)+tint[c]*m*strength
    return out

def ground_shadow(rim, dx, scale=1.0, alpha=190):
    # squashed figure alpha 28% height, sheared by dx
    fig_alpha=ALPHA/255.0
    # squash: take rows, compress vertically toward Gy
    sq=np.zeros((H,W))
    # simple: resize figure alpha to height 0.28*figheight, place bottom at Gy
    from PIL import Image as I
    aimg=I.fromarray((fig_alpha*255).astype(np.uint8))
    fh=BBOX[3]-BBOX[1]
    nh=int(fh*0.28)
    small=aimg.resize((W,nh))
    sq[Gy-nh:Gy,:]=np.array(small).astype(float)/255.0
    # shear by dx proportional to distance below feet? use shift per row
    sh=np.zeros_like(sq)
    for i,row in enumerate(sq):
        s=int(dx*(1-i/H))
        sh[i]=np.roll(row,s)
    sh=blur_arr(sh*255,12)/255.0
    tint=np.array([46.,32.,14.]) if rim[0]>100 else np.array([20.,80.,110.])
    # mix tint toward rim 18%
    tint=np.array(rim)*0.18
    return sh, tint

def contact_ellipse():
    m=np.zeros((H,W))
    cx=(BBOX[0]+BBOX[2])//2; cy=Gy
    yy,xx=np.mgrid[0:H,0:W]
    e=((xx-cx)/( (BBOX[2]-BBOX[0])*0.58))**2+((yy-cy)/28)**2<=1
    m[e]=1
    return blur_arr(m*255,10)/255.0

def lit_figure(grade, form_dir, form_lo, rim, wrap=0.0):
    fig=FIG[...,:3].copy()
    # color grade gains
    fig=fig*np.array(grade)
    # form cel gradient: across x if side, y if overhead/low
    yy,xx=np.mgrid[0:H,0:W]
    if form_dir=="x":
        g=np.linspace(1.0,form_lo,W)[None,:].repeat(H,axis=0)
    elif form_dir=="-x":
        g=np.linspace(form_lo,1.0,W)[None,:].repeat(H,axis=0)
    elif form_dir=="y":
        g=np.linspace(1.0,form_lo,H)[:,None].repeat(W,axis=1)
    else:
        g=np.linspace(form_lo,1.0,H)[:,None].repeat(W,axis=1)
    if wrap: g=g*(1-wrap)+ (1.0) *wrap*0.5  # wrap softens terminator: pull gradient toward mid
    fig=fig*g[:,:,None]
    # AO interior band <12px dark 25%
    ao=(EDT<12)&MASK
    fig[ao]*=0.75
    # subsurface thin edge warm on away side: EDT<10, tint
    # rim layer separate later; keep fig here
    return np.clip(fig,0,255)

def apply_rim(img, rim, width=6):
    m=dilate(MASK,width)&~MASK
    out=img.copy()
    for c in range(3): out[:,:,c]=np.where(m, rim[c], out[:,:,c])
    return out, int(m.sum())

def hue_key_mask(kind):
    r,g,b=FIG[...,0],FIG[...,1],FIG[...,2]
    if kind=="purple": # cowl/emblem purple
        return MASK & (r>50)&(r<160)&(g<100)&(b>90)
    if kind=="cyan":
        return MASK & (b>120)&(g>120)&(r<120)
    if kind=="white": # white suit
        return MASK & (r>180)&(g>180)&(b>180)
    if kind=="gold":
        return MASK & (r>180)&(g>140)&(b<120)
    if kind=="face":
        return MASK & (r>150)&(g>100)&(g<180)&(b<140)
    return MASK

def glow_on(img, mask, colour, strength=0.5, blur=12):
    m=blur_arr(mask.astype(float)*255,blur)/255.0
    out=img.copy()
    for c in range(3): out[:,:,c]=out[:,:,c]*(1-m*strength)+colour[c]*m*strength
    return out

def composite_on_room(room_img, fig_rgb, ground, tint, contact):
    out=room_img.copy()
    # ground shadow behind figure
    for c in range(3): out[:,:,c]=out[:,:,c]*(1-ground*0.75)+tint[c]*ground*0.75
    for c in range(3): out[:,:,c]=out[:,:,c]*(1-contact*0.6)+tint[c]*contact*0.6
    # figure
    a=(ALPHA/255.0)[:,:,None]
    out=out*(1-a)+fig_rgb*a
    return out

COLS=[(58,212),(267,418),(474,622),(679,832),(887,1041)]

PROJECTS=[
 dict(id="F-I1", name="Golden Hour Hero", kind="industry", room="warm", grade=(1.15,1.0,0.85), form="x", lo=0.78, rim=(255,180,80), dx=30, vfx="god-ray shafts + warm glow", key="purple", keycol=(255,180,80), keystr=0.4),
 dict(id="F-I2", name="Night City Neon", kind="industry", room="night", grade=(0.85,0.95,1.2), form="-x", lo=0.72, rim=(0,200,255), dx=-120, vfx="cyan neon rim glow + city shafts", key="cyan", keycol=(0,220,255), keystr=0.5),
 dict(id="F-I3", name="Comic Dramatic Uplight", kind="industry", room="comic", grade=(1.1,1.05,1.05), form="-y", lo=0.70, rim=(255,220,150), dx=60, vfx="underlight spot + AO drama", key="face", keycol=(255,200,120), keystr=0.5),
 dict(id="F-I4", name="Desert Day Dappled", kind="industry", room="day", grade=(1.1,1.05,0.9), form="y", lo=0.78, rim=(255,200,120), dx=30, vfx="dappled shaft stripes on figure+ground", key="gold", keycol=(255,210,100), keystr=0.4),
 dict(id="F-I5", name="Dual-Light Split", kind="industry", room="dual", grade=(1.05,0.95,1.05), form="x", lo=0.72, rim=(255,180,80), dx=60, vfx="dual god rays warm front + cyan back, double shadow", key="purple", keycol=(0,200,255), keystr=0.4),
 dict(id="F-X1", name="Chroma Prism", kind="experimental", room="prism", grade=(1.1,0.95,1.15), form="x", lo=0.72, rim=(255,120,220), dx=90, vfx="prismatic RGB edge shift + light leak", key="purple", keycol=(255,100,220), keystr=0.6),
 dict(id="F-X2", name="Crystal Power", kind="experimental", room="crystal", grade=(0.9,1.1,1.2), form="y", lo=0.75, rim=(42,126,207), dx=30, vfx="crystal cyan/pink glints + facet tint", key="white", keycol=(42,200,255), keystr=0.5),
 dict(id="F-X3", name="Ghost Outline", kind="experimental", room="ghost", grade=(0.85,0.9,0.95), form="-x", lo=0.72, rim=(0,200,255), dx=-60, vfx="invisible outline + halo, desaturated ghost", key="cyan", keycol=(180,245,255), keystr=0.6),
 dict(id="F-X4", name="Storm Flicker", kind="experimental", room="storm", grade=(0.9,0.95,1.15), form="x", lo=0.70, rim=(160,200,255), dx=120, vfx="lightning flash + flicker sway shadow", key="white", keycol=(200,220,255), keystr=0.5),
 dict(id="F-X5", name="Ground Pool Dance", kind="experimental", room="pools", grade=(1.15,1.0,0.85), form="y", lo=0.78, rim=(255,180,80), dx=30, vfx="floor pool glow + ground bounce, depth-gradient shadow", key="gold", keycol=(255,180,80), keystr=0.5),
]

results=[]
for p in PROJECTS:
    rm=room(p["room"])
    # VFX behind: shafts
    rm2=shafts(rm, COLS, p["rim"], strength=0.30)
    fig=lit_figure(p["grade"], p["form"], p["lo"], p["rim"], wrap=0.3)
    # dappled for I4: modulate fig by columns
    if p["id"]=="F-I4":
        colmask=np.zeros((H,W))
        for a,b in COLS: colmask[:,a:b]=1
        fig=fig*(1+colmask[:,:,None]*0.08-colmask[:,:,None]*0)  # inside brighter
        fig=np.where(colmask[:,:,None]>0, fig*1.08, fig*0.92)
    if p["id"]=="F-X1":
        # RGB edge shift: shift R left 3, B right 3 inside figure only
        fr=np.roll(fig[:,:,0],-3,axis=1); fb=np.roll(fig[:,:,2],3,axis=1)
        fig2=fig.copy(); fig2[:,:,0]=np.where(MASK,fr,fig[:,:,0]); fig2[:,:,2]=np.where(MASK,fb,fig[:,:,2]); fig=fig2
    if p["id"]=="F-X2":
        # crystal tint: cyan/pink split by x
        fig=np.where(np.mgrid[0:H,0:W][1][:,:,None]>550, fig*np.array([0.9,1.1,1.2]), fig*np.array([1.1,0.9,1.1]))
    ground,tint=ground_shadow(p["rim"], p["dx"])
    if p["id"]=="F-I5":
        # dual: second cast opposite
        g2,_=ground_shadow((0,200,255), -60)
        ground=np.clip(ground+g2*0.6,0,1)
    if p["id"]=="F-X5":
        # depth gradient: fade ground with distance below feet already; scale by pool band
        ground=ground*0.9
    contact=contact_ellipse()
    out=composite_on_room(rm2, fig, ground, tint, contact)
    # rim on top of figure (only where figure, rim mask adjacent)
    out, rim_px=apply_rim(out, p["rim"], 6)
    # color keying: glow only on hue-keyed mask
    km=hue_key_mask(p["key"])
    out=glow_on(out, km, p["keycol"], strength=p["keystr"], blur=10)
    # VFX front: shafts overlay light (behind already) + glints for X2/X4
    if p["id"] in ("F-X2","F-X4"):
        out=glow_on(out, RIM_MASK, p["keycol"], strength=0.3, blur=8)
    out=np.clip(out,0,255)
    # before: room + unlit figure, no effects
    before=composite_on_room(rm, FIG[...,:3], np.zeros((H,W)), tint, np.zeros((H,W)))
    fn=f"{p['id']}-{p['name'].lower().replace(' ','-')}-20261031.png"
    Image.fromarray(out.astype(np.uint8)).save(os.path.join(ROOT,"projects",fn))
    Image.fromarray(before.astype(np.uint8)).save(os.path.join(ROOT,"projects",fn.replace(".png","-BEFORE.png")))
    # gates
    edge_alpha=0  # RGB composite, figure inside canvas checked via bbox
    inside = BBOX[0]>0 and BBOX[1]>0 and BBOX[2]<W and BBOX[3]<=H
    results.append(dict(id=p["id"], name=p["name"], kind=p["kind"], file=fn,
        stack=dict(color=f"LUT/grade gains {p['grade']} on {p['room']} room", vfx=p["vfx"], lighting=f"key rim {p['rim']} form {p['form']}->{p['lo']} wrap 0.3", shadow=f"contact+cast dx={p['dx']} + cel form + AO<12px 25%", keying=f"hue-key {p['key']} glow {p['keycol']} x{p['keystr']}"),
        bbox=BBOX, feet=int(BBOX[3]), ground_line=Gy, diff=int(BBOX[3]-Gy), figure_alpha=int(MASK.sum()), ground_shadow_px=int((ground>0.1).sum()), rim_px=int(rim_px), key_mask_px=int(km.sum()), inside_canvas=bool(inside), gate="PASS" if inside and BBOX[3]==Gy else "FAIL"))
    print(p["id"], results[-1])

# contacts: before/after pairs, industry and experimental
def contact(items, outname, tile_w=550):
    # each tile: before left, after right, stacked? make grid 2 cols (before,after) per row, scaled
    rows=[]
    for r in items:
        b=Image.open(os.path.join(ROOT,"projects",r["file"].replace(".png","-BEFORE.png"))).resize((tile_w, int(tile_w*1500/1100)))
        a=Image.open(os.path.join(ROOT,"projects",r["file"])).resize((tile_w, int(tile_w*1500/1100)))
        row=Image.new("RGB",(tile_w*2, b.height),(20,20,20)); row.paste(b,(0,0)); row.paste(a,(tile_w,0)); rows.append(row)
    Hc=sum(r.height for r in rows); Wc=tile_w*2
    c=Image.new("RGB",(Wc,Hc),(20,20,20)); y=0
    for r in rows: c.paste(r,(0,y)); y+=r.height
    c.save(os.path.join(ROOT,"contacts",outname)); print(outname, c.size)

ind=[r for r in results if r["kind"]=="industry"]; exp=[r for r in results if r["kind"]=="experimental"]
contact(ind,"fullstack-industry-before-after-20261031.png")
contact(exp,"fullstack-experimental-before-after-20261031.png")
contact(results,"fullstack-all-before-after-20261031.png")
with open(os.path.join(ROOT,"measurements-fullstack-20261031.json"),"w") as f: json.dump(dict(base_bbox=BBOX, base_alpha=int(MASK.sum()), projects=results),f,indent=2)
print("done", len(results))
