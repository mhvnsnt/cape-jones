from PIL import Image, ImageDraw, ImageFilter
import numpy as np, os
R=os.path.expanduser("~/workspace/cape-jones-rig")
OUT=os.path.join(R,"blender-composite-wrap-v3-20261031/scratch")
W,H=640,360
# ---------- Upgraded background ----------
# vertical gradient: deep teal-navy top -> teal mid -> warm gold-green horizon
bg=np.zeros((H,W,3),dtype=np.float32)
for y in range(H):
    t=y/H
    if t<0.55:
        c=np.array([18,52,66])*(1-t/0.55)+np.array([38,110,105])*(t/0.55)
    else:
        u=(t-0.55)/0.45
        c=np.array([38,110,105])*(1-u)+np.array([150,150,95])*(u)
    bg[y,:,:]=c
im=Image.fromarray(bg.astype(np.uint8))
# gold glow centre behind character
glow=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(glow)
d.ellipse([180,-80,460,320],fill=(255,200,110,90))
glow=glow.filter(ImageFilter.GaussianBlur(60)); im=Image.alpha_composite(im.convert("RGBA"),glow)
# brighter cyan shafts from upper-left
shafts=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(shafts)
for x0,wd,a in [(60,26,110),(110,18,90),(170,34,70),(230,14,60)]:
    d.polygon([(x0,0),(x0+wd,0),(x0+wd+70,H),(x0+50,H)],fill=(0,210,255,a))
shafts=shafts.filter(ImageFilter.GaussianBlur(8)); im=Image.alpha_composite(im,shafts)
# ground glow + reflection pool under feet
pool=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(pool)
d.ellipse([230,300,410,340],fill=(0,220,255,70)); d.ellipse([250,310,390,332],fill=(255,190,90,50))
pool=pool.filter(ImageFilter.GaussianBlur(12)); im=Image.alpha_composite(im,pool)
# dust specks in shafts
import random; random.seed(7)
d=ImageDraw.Draw(im)
for _ in range(120):
    x=random.randint(40,300); y=random.randint(10,300); r=random.randint(1,2)
    d.ellipse([x,y,x+r,y+r],fill=(255,255,255,random.randint(60,160)))
# vignette
vig=Image.new("L",(W,H),0); d=ImageDraw.Draw(vig); d.rectangle([0,0,W,H],fill=0)
vig=Image.fromarray(np.clip(np.array(Image.new("L",(W,H),0)),0,255).astype(np.uint8))
# simple vignette via radial darkening
arr=np.array(im.convert("RGB")).astype(np.float32)
yy,xx=np.mgrid[0:H,0:W]; cx,cy=W/2,H/2
dist=np.sqrt(((xx-cx)/(W/2))**2+((yy-cy)/(H/2))**2)
arr*=np.clip(1.05-0.25*np.maximum(dist-0.7,0),0.75,1.05)[...,None]
Image.fromarray(arr.astype(np.uint8)).convert("RGBA").save(f"{OUT}/bg-upgraded-v3-20261031.png")
print("bg saved")

# ---------- Interior shading (2D relight approximation) ----------
from scipy import ndimage
def shade_plate(src, dst):
    im0=Image.open(src).convert("RGBA"); a=np.array(im0); alpha=a[:,:,3]
    rgb=a[:,:,:3].astype(np.float32)
    ys,xs=np.where(alpha>10)
    xmin,xmax,ymin,ymax=xs.min(),xs.max(),ys.min(),ys.max()
    # interior linework: dark pixels well inside the alpha (eroded mask)
    eroded=ndimage.binary_erosion(alpha>10, iterations=4)
    lum=rgb.mean(axis=2)
    lines=(lum<110)&eroded
    # relief: lit side offset toward light (-4,-3), shadow side away (+4,+3)
    # shift masks with slicing
    lit_shift=np.zeros_like(lines); lit_shift[:-3,:-4]=lines[3:,4:]
    shad_shift=np.zeros_like(lines); shad_shift[3:,4:]=lines[:-3,:-4]
    # directional gradient across bbox: cyan backlight upper-left, gold front key right
    xx=np.arange(rgb.shape[1])[None,:]; t=np.clip((xx-xmin)/max(xmax-xmin,1),0,1)
    cyan_s=(1-t)*0.20; gold_s=t*0.10
    # apply tint: white/light pixels tint most, dark pixels least (preserve shadow)
    light_w=np.clip((lum-80)/175,0,1)[...,None]
    out=rgb.copy()
    out+= (np.array([0,200,255])-out)*cyan_s[...,None]*light_w*0.9
    out+= (np.array([255,180,80])-out)*gold_s[...,None]*light_w*0.7
    # form shading: top brighter, bottom slightly darker/cool
    yy=np.arange(rgb.shape[0])[:,None]; yn=np.clip((yy-ymin)/max(ymax-ymin,1),0,1)
    out*= (1+0.08*(1-yn)-0.06*yn)[...,None]
    # relief around lines
    m=alpha>10
    out[lit_shift&m]=np.clip(out[lit_shift&m]*1.18+np.array([10,25,30]),0,255)
    out[shad_shift&m]=np.clip(out[shad_shift&m]*0.72+np.array([0,0,10]),0,255)
    # keep pure black outlines black (do not tint them)
    black=(rgb[:,:,0]<20)&(rgb[:,:,1]<20)&(rgb[:,:,2]<20)
    out[black]=rgb[black]
    res=np.dstack([np.clip(out,0,255).astype(np.uint8),alpha])
    Image.fromarray(res,"RGBA").save(dst); print("shaded",dst, "lines",int(lines.sum()))

shade_plate(f"{R}/rig-apose-v7c-clean-transparent.png", f"{OUT}/plate-apose-shaded-v3.png")
shade_plate(f"{R}/dual-light-variants-20261031/base-arms-up-transparent-20261031.png", f"{OUT}/plate-armsup-shaded-v3.png")
# fighting pose: opaque grey-128 background -> key it out
fp=Image.open(f"{R}/reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png").convert("RGBA")
arr=np.array(fp); grey=(np.abs(arr[:,:,0].astype(int)-128)<8)&(np.abs(arr[:,:,1].astype(int)-128)<8)&(np.abs(arr[:,:,2].astype(int)-128)<8)
arr[grey,3]=0
Image.fromarray(arr,"RGBA").save(f"{OUT}/plate-fighting-extracted.png")
shade_plate(f"{OUT}/plate-fighting-extracted.png", f"{OUT}/plate-fighting-shaded-v3.png")
