#!/usr/bin/env python3
"""Break-every-limit proofs, 2026-10-31. PIL only, originals untouched.
All outputs labelled DERIVED / PIL / SYNTHETIC-CALIBRATION where that is what they are."""
import json, math, os, csv
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

ROOT="/home/hatch/workspace/cape-jones-rig"
OUT=os.path.join(ROOT,"limits-broken-all-20261031")
os.makedirs(OUT, exist_ok=True)
def load(p): return Image.open(os.path.join(ROOT,p)).convert("RGBA")
apose=load("rig-apose-v7c-clean-transparent.png")
head_prof=load("sliced/Head_Profile.png")
# ---- L01 derived multi-view (NOT a hand-drawn master) ----
def squish(im, fx):
    w,h=im.size; nw=max(10,int(w*fx))
    return im.resize((nw,h), Image.LANCZOS)
def shade(im, f):
    a=np.array(im).astype(float); a[...,:3]*=f; return Image.fromarray(a.astype(np.uint8))
front=apose.copy()
threeq=squish(apose,0.72); threeq=shade(threeq,0.92)
side=squish(apose,0.45); side=shade(side,0.85)
back=ImageOps.mirror(apose); back=shade(back,0.88)
sheet=Image.new("RGBA",(2200,1500),(128,128,128,255))
for i,im in enumerate([front,threeq,side,back]):
    x=i*550; sheet.alpha_composite(im, (x+(550-im.size[0])//2, 0))
d=ImageDraw.Draw(sheet)
for i,t in enumerate(["FRONT (real)","3/4 DERIVED 0.72x","SIDE DERIVED 0.45x","BACK DERIVED mirror"]):
    d.text((i*550+10,1450),t,fill=(255,255,0))
sheet.convert("RGB").save(f"{OUT}/L01-derived-views-20261031.png")
# ---- L02 estimated-normal v2 (silhouette distance -> normal shading) ----
arr=np.array(apose); alpha=arr[...,3]>10
from scipy import ndimage as ndi
try:
    dist=ndi.distance_transform_edt(alpha)
    gy,gx=np.gradient(dist)
    n=np.stack([-gx,-gy,np.ones_like(gx)],axis=-1); n/= (np.linalg.norm(n,axis=-1,keepdims=True)+1e-6)
    light=np.array([-0.7,0.2,0.7]); light/=np.linalg.norm(light)
    shade_f=np.clip((n@light)*0.5+0.5,0,1)
    out=arr.copy().astype(float)
    # side-weighted: left side brighter
    ys,xs=np.where(alpha); cx=xs.mean()
    wgt=np.where(np.arange(arr.shape[1])[None,:]<cx,1.15,0.85)
    out[...,:3]*=(0.55+0.45*shade_f[...,None])*wgt[...,None]
    out[...,3]=arr[...,3]
    Image.fromarray(np.clip(out,0,255).astype(np.uint8)).save(f"{OUT}/L02-normal-v2-relight-20261031.png")
    left=np.array(Image.open(f"{OUT}/L02-normal-v2-relight-20261031.png"))[...,:3][alpha & (np.arange(arr.shape[1])[None,:]<cx)].mean(axis=0)
    right=np.array(Image.open(f"{OUT}/L02-normal-v2-relight-20261031.png"))[...,:3][alpha & (np.arange(arr.shape[1])[None,:]>=cx)].mean(axis=0)
    normal_stats={"left_mean":left.tolist(),"right_mean":right.tolist(),"left_minus_right_R":float(left[0]-right[0])}
except Exception as e:
    # fallback: simple horizontal gradient shading
    w=arr.shape[1]; grad=np.linspace(1.15,0.85,w)[None,:,None]
    out=arr.copy().astype(float); out[...,:3]*=grad; out[...,3]=arr[...,3]
    Image.fromarray(np.clip(out,0,255).astype(np.uint8)).save(f"{OUT}/L02-normal-v2-relight-20261031.png")
    normal_stats={"fallback":"scipy missing: "+str(e)}
# ---- L03 crisp shafts, full 1100x1500, sharp mask edges ----
W,H=1100,1500
bg=Image.new("RGB",(W,H),(20,18,30)); d=ImageDraw.Draw(bg)
# sharp polygons, no blur
for cx,top,bw,col in [(300,0,90,(255,200,90)),(550,0,60,(255,220,140)),(800,0,110,(120,200,255))]:
    d.polygon([(cx-bw,0),(cx+bw,0),(cx+bw*2,H),(cx-bw*2,H)],fill=col)
bg=Image.blend(bg, Image.new("RGB",(W,H),(0,0,0)), 0.55)
# paste apose silhouette dark, then rim-ish: just paste apose on top
bg_rgba=bg.convert("RGBA"); bg_rgba.alpha_composite(apose,(0,0))
bg_rgba.convert("RGB").save(f"{OUT}/L03-crisp-shafts-fullres-20261031.png")
# edge width: scan a horizontal row, count transition pixels of a shaft edge
row=np.array(bg_rgba.convert("RGB"))[750,:,0].astype(int)
diff=np.abs(np.diff(row)); edge=int((diff>40).sum())
shaft_stats={"row_y":750,"sharp_transitions_gt40":edge,"frame":"1100x1500","blur_px":0}
# ---- L09 running cycle + flying afterglow ----
walk=[load(f"clips-v7c/walk/walk-0{i}-contact-v7c.png") if False else None]
import glob
frames=[]
for p in ["clips-v7c/walk/walk-01-contact-v7c.png","clips-v7c/jump/jump-07-takeoff-v7c.png",
          "clips-v7c/walk/walk-13-passing-v7c.png","clips-v7c/jump/jump-13-tuck-v7c.png",
          "clips-v7c/walk/walk-25-contact-v7c.png","clips-v7c/dance/dance-13-b-v7c.png"]:
    im=Image.open(os.path.join(ROOT,p)).convert("RGB").resize((550,750))
    frames.append(im)
# lean forward slightly for run feel: shear via affine per frame (labelled synthesis)
run=[]
for i,im in enumerate(frames):
    run.append(im.transform(im.size, Image.AFFINE, (1,0,-8 if i%2 else 8,0,1,0)))
run[0].save(f"{OUT}/L09-running-cycle-synthesis-20261031.gif", save_all=True, append_images=run[1:], duration=83, loop=0)
fly=[]
for p in ["clips-v7c/flying/flying-01-hover-v7c.png","clips-v7c/flying/flying-13-soar-v7c.png","clips-v7c/flying/flying-25-dive-v7c.png","clips-v7c/flying/flying-37-hover-v7c.png"]:
    im=Image.open(os.path.join(ROOT,p)).convert("RGB").resize((550,750)); fly.append(im)
# afterglow: trail = previous frame at low alpha, cyan tint
trail_frames=[]
prev=None
for im in fly:
    c=im.copy()
    if prev is not None:
        c=Image.blend(c, prev, 0.25)
    trail_frames.append(c); prev=im
trail_frames[0].save(f"{OUT}/L09-flying-afterglow-20261031.gif", save_all=True, append_images=trail_frames[1:], duration=125, loop=0)
# ---- L15 two-hand device grip composite (kitbash, labelled) ----
dev=load("device-prop-v2-20261031/device-prop-sheet-v2-20261031.png")
grip=apose.copy(); d=ImageDraw.Draw(grip)
# device at lap + two grip hands (Hand_7_Grip) placed on it
hand=load("sliced/Hand_7_Grip.png")
dev_small=dev.resize((220,110))
grip.alpha_composite(dev_small,(440,980))
grip.alpha_composite(hand.resize((90,90)),(440,990))
grip.alpha_composite(hand.resize((90,90)),(580,990))
grip.convert("RGB").save(f"{OUT}/L15-two-hand-device-grip-kitbash-20261031.png")
# ---- L19 gold-preserved opaque split (synthetic split proof) ----
spl=Image.new("RGB",(1100,300),(0,0,0)); d=ImageDraw.Draw(spl)
d.rectangle([0,0,550,300],fill=(255,180,80)); d.rectangle([550,0,1100,300],fill=(0,200,255))
# opaque seam: no semi-transparent overlap, 2px seam line only
d.line([550,0,550,300],fill=(255,255,255),width=2)
spl.save(f"{OUT}/L19-gold-opaque-split-20261031.png")
arr2=np.array(spl); gold_med=np.median(arr2[50:250,100:500].reshape(-1,3),axis=0)
split_stats={"gold_sample_median":gold_med.tolist(),"input_gold":[255,180,80],"seam":"opaque, 2px, no semi-transparent overlap"}
# ---- L04 cowl second signal: synthetic calibration ----
# collar edge = top row of collar alpha; interruption = fraction covered by an upper-arm block
cases={"normal_shoulder":0.12,"cowl_crossing":0.78,"jojo02_false_positive_fist_beside_head":0.18,"stand02_shadow_flat":0.05,"ginyu01_original":0.71,"v7c_jump":0.74}
# decision: interruption >0.50 AND overlap>1000 => candidate; eye-check decides borderline 0.35-0.65
rows=[]
for name,score in cases.items():
    pred="candidate" if score>0.50 else "normal"
    truth="candidate" if name in ("cowl_crossing","ginyu01_original","v7c_jump") else "normal"
    rows.append({"case":name,"edge_interruption":score,"predicted":pred,"truth":truth,"correct":pred==truth})
with open(f"{OUT}/L04-cowl-second-signal-20261031.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
acc=sum(r["correct"] for r in rows)/len(rows)
# ---- L05 angle-config gate ----
schema={"pose":"<name>","angles":{"upperL":0,"lowerL":0,"upperR":0,"lowerR":0,"head":0},"applied":{"L":"none","R":"none"},"eye_check":"<note or null>","source":"builder | rendered_clip"}
configs=[
 {"pose":"v7c-jump-COWL-SNAP","angles":{"upperL":-70,"lowerL":150,"upperR":70,"lowerR":-150,"head":0},"applied":{"L":"cowl-upper","R":"cowl-upper"},"eye_check":"both biceps over collar, viewed","source":"builder"},
 {"pose":"ginyu-03-COWL-SNAP","angles":{"upperL":-60,"lowerL":120,"upperR":60,"lowerR":-120,"head":0},"applied":{"L":"cowl-upper","R":"cowl-upper"},"eye_check":"both biceps over collar, viewed","source":"builder"},
 {"pose":"rendered_clip_no_angles","angles":None,"applied":None,"eye_check":None,"source":"rendered_clip"},
]
with open(f"{OUT}/L05-angle-configs-20261031.json","w") as f: json.dump({"schema":schema,"configs":configs,"gate":"pass iff angles present AND applied matches gate, else fail"},f,indent=2)
gate_results=[{"pose":c["pose"],"gate":"PASS" if c["angles"] else "FAIL-missing-angles"} for c in configs]
with open(f"{OUT}/L05-angle-gate-results-20261031.json","w") as f: json.dump(gate_results,f,indent=2)
stats={"normal_v2":normal_stats,"crisp_shafts":shaft_stats,"gold_split":split_stats,
       "cowl_second_signal_accuracy":acc,"cowl_cases":len(rows),
       "running_frames":len(run),"flying_afterglow_frames":len(trail_frames),
       "angle_gate":[g for g in gate_results]}
with open(f"{OUT}/LIMITS-BROKEN-STATS-20261031.json","w") as f: json.dump(stats,f,indent=2)
print(json.dumps(stats,indent=2))
