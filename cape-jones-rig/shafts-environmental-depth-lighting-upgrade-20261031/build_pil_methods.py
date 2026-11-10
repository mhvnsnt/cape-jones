"""PIL improvement variants for Environmental Depth and Lighting preset.
Base: v2 shafts (preset base) + v3 Cycles (I1) + figure plate.
All variants: shafts masked by (1-figure_alpha), figure pasted on top, no recolour of base.
Column centres in composite space (from v2 measurement, mapped): use v2 mid columns
282-379, 494-604, 721-816 plus outer columns estimated at ~110 and ~980 (v3 check below).
Pools: ellipses centred under each column at feet y ~1282, stretched, blurred, warm.
"""
import json, math, random
from PIL import Image, ImageFilter, ImageDraw
import numpy as np
from scipy.ndimage import gaussian_filter

ROOT='/home/hatch/workspace/cape-jones-rig/shafts-environmental-depth-lighting-upgrade-20261031/'
SRC='/home/hatch/workspace/cape-jones-rig/shafts-volumetric-upgrade-20261031/'
shafts_v2=np.array(Image.open(SRC+'shafts-only-cycles-v2-20261031.png').convert('RGB')).astype(float)
fig=Image.open(SRC+'figure-only-plate-20261031.png').convert('RGBA')
fig_a=np.array(fig)[:,:,3].astype(float)/255.0
H,W=shafts_v2.shape[:2]
print("canvas", W, H, "fig bbox", )
# figure bbox
ys,xs=np.where(np.array(fig)[:,:,3]>10)
print("fig bbox", xs.min(), ys.min(), xs.max(), ys.max())

def composite(shaft_rgb, outname, pools=False, pool_alpha=90):
    s=np.clip(shaft_rgb,0,255).astype(float)
    # mask shafts under figure
    s=s*(1-fig_a[:,:,None])
    base=Image.fromarray(s.astype(np.uint8)).convert('RGBA')
    if pools:
        # pools layer: warm ellipses at feet, behind figure (figure pasted after)
        pool=Image.new('RGBA',(W,H),(0,0,0,0))
        d=ImageDraw.Draw(pool)
        centres=[165,330,550,770,935]  # 5 columns incl outer, in composite x
        feet_y=1282
        for cx in centres:
            for r, a in [(150,pool_alpha),(110,pool_alpha+30),(70,pool_alpha+50)]:
                d.ellipse([cx-r, feet_y-18, cx+r, feet_y+55], fill=(255,190,90,a))
        pool=pool.filter(ImageFilter.GaussianBlur(18))
        base=Image.alpha_composite(base, pool)
    out=Image.alpha_composite(base, fig)
    out.save(ROOT+outname)
    return out

def measure_columns(shaft_rgb, name):
    # same method as v2: rows 500-700, grey profile, midpoint threshold
    grey=shaft_rgb.mean(axis=2)
    prof=grey[500:700,:].mean(axis=0)
    thr=(prof.max()+prof.min())/2
    above=prof>thr
    runs=[]; i=0
    while i < len(above):
        if above[i]:
            j=i
            while j < len(above) and above[j]: j+=1
            if j-i>=20: runs.append([int(i),int(j-1)])
            i=j
        else: i+=1
    peaks=[]; valleys=[]
    print(name, "runs", runs, "prof max", float(prof.max()), "min", float(prof.min()))
    return {"runs":runs, "peak":float(prof.max()), "min":float(prof.min())}

results={}
# I3 pools on v2
composite(shafts_v2, 'methods/I3-ground-pools-composite-20261031.png', pools=True)
results['I3_pools']='ellipses at feet_y 1282, centres 165/330/550/770/935, blur 18'
# I5 denoised v2: gaussian + median-like via scipy uniform? use gaussian_filter sigma 1
den=np.stack([gaussian_filter(shafts_v2[:,:,c],1.0) for c in range(3)],axis=2)
composite(den, 'methods/I5-denoised-faster-composite-20261031.png')
results['I5_denoise']='gaussian sigma 1.0 on v2 shafts (proxy for Cycles denoiser; v3 itself used Cycles denoising)'
# X1 depth gradient: warm top -> cooler/dimmer bottom, plus fade
grad=np.linspace(1.0,0.55,H)[:,None,None]
cool=np.array([0.85,0.95,1.15])
x1=shafts_v2*grad*cool[None,None,:]
composite(x1, 'methods/X1-depth-gradient-composite-20261031.png')
# X2 flicker frame (mid flicker): outer columns boosted, centre dimmed slightly (one frame of a sweep)
flick=shafts_v2.copy()
for (x0,x1c,fac) in [(0,220,1.35),(220,440,1.0),(440,660,0.85),(660,880,1.0),(880,1100,1.35)]:
    flick[:,x0:x1c,:]*=fac
composite(flick, 'methods/X2-flicker-sweep-composite-20261031.png')
# X3 dust streaks: add vertical streaks inside columns
random.seed(7)
streak=np.zeros((H,W,3))
for _ in range(120):
    cx=random.choice([165,330,550,770,935])+random.uniform(-40,40)
    y0=random.uniform(240,900); ln=random.uniform(80,260)
    x0=int(cx)
    streak[int(y0):int(y0+ln), max(0,x0-1):x0+2,:]+=np.array([255,220,150])*0.5
streak=gaussian_filter(streak, sigma=(2,1,0))
composite(shafts_v2+streak, 'methods/X3-dust-streaks-composite-20261031.png')
# X4 caustic pools: pools with noise dapple
pool_img=np.zeros((H,W,4),dtype=np.uint8)
noise=np.random.default_rng(11).normal(0,1,(H,W))
noise=gaussian_filter(noise,4)
feet_y=1282
for cx in [165,330,550,770,935]:
    yy,xx=np.mgrid[0:H,0:W]
    mask=((xx-cx)/150)**2+((yy-feet_y)/45)**2<1
    a=np.clip(90+50*noise,0,180)
    pool_img[:,:,0]=np.where(mask,255,pool_img[:,:,0]); pool_img[:,:,1]=np.where(mask,190,pool_img[:,:,1]); pool_img[:,:,2]=np.where(mask,90,pool_img[:,:,2]); pool_img[:,:,3]=np.where(mask,a.astype(np.uint8),pool_img[:,:,3])
base=Image.fromarray((shafts_v2*(1-fig_a[:,:,None])).astype(np.uint8)).convert('RGBA')
base=Image.alpha_composite(base, Image.fromarray(pool_img).filter(ImageFilter.GaussianBlur(6)))
out=Image.alpha_composite(base, fig); out.save(ROOT+'methods/X4-caustic-pools-composite-20261031.png')
# X5 edge-softened shafts: blur shafts then re-mask (softer column edges, less hard separation)
soft=gaussian_filter(shafts_v2, sigma=(3,3,0))
composite(soft, 'methods/X5-edge-softened-composite-20261031.png')
# measure v3 if present
import os
meas={}
for name, arr in [('v2',shafts_v2),('v2_denoised',den),('v2_soft',soft)]:
    meas[name]=measure_columns(arr,name)
if os.path.exists(ROOT+'shafts-only-cycles-v3-20261031.png'):
    v3=np.array(Image.open(ROOT+'shafts-only-cycles-v3-20261031.png').convert('RGB')).astype(float)
    meas['v3']=measure_columns(v3,'v3')
    composite(v3, 'methods/I1-cycles-v3-composite-20261031.png', pools=False)
    # v3 + pools = improved final composite candidate
    composite(v3, 'composite-environmental-depth-lighting-v3-pools-20261031.png', pools=True)
json.dump({"results":results,"measures":meas}, open(ROOT+'measurements-methods-20261031.json','w'), indent=2)
print(json.dumps(meas,indent=2))
print("PIL_DONE")
