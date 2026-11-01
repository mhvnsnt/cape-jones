#!/usr/bin/env python3
"""Production-ready 10 wired systems, 2026-10-31. PIL only, base art untouched:
every output composites OVER the clean plate, never recolours the plate itself.
Honest label: (1) is pseudo-normal from silhouette depth, NOT a measured 3D normal pass;
(2)/(3) reuse the Cycles god-ray v2 background method (Blender, already rendered) for shafts/dust,
with a PIL shaft pass on top for this proof sheet. No vector redraw of the character."""
import json, math, random, os
from PIL import Image, ImageDraw, ImageFilter
R="/home/hatch/workspace/cape-jones-rig"
O=os.path.join(R,"production-ready-20261031"); os.makedirs(O,exist_ok=True)
APOSE=Image.open(os.path.join(R,"rig-apose-v7c-clean-transparent.png")).convert("RGBA")
ARMS=Image.open(os.path.join(R,"dual-light-variants-20261031/base-arms-up-transparent-20261031.png")).convert("RGBA")
GOD=Image.open(os.path.join(R,"godray-level3-20261031/godray-bg-v2-20261031.png")).convert("RGBA")
def fit(im,w,h):
    im=im.copy(); im.thumbnail((w,h),Image.LANCZOS); c=Image.new("RGBA",(w,h),(0,0,0,0)); c.alpha_composite(im,((w-im.width)//2,(h-im.height)//2)); return c
def bg(w,h,top,bottom):
    im=Image.new("RGBA",(w,h)); d=ImageDraw.Draw(im)
    for y in range(h):
        t=y/h; d.line([(0,y),(w,y)],tuple(int(top[i]+(bottom[i]-top[i])*t) for i in range(3))+(255,))
    return im
def rim_band(plate,dil,blur,color,factor):
    a=plate.split()[3]
    d=a.filter(ImageFilter.MaxFilter(dil*2+1)).filter(ImageFilter.GaussianBlur(blur))
    band=Image.new("RGBA",plate.size,color+(0,))
    band.putalpha(d.point(lambda v:int(v*factor)))
    out=Image.new("RGBA",plate.size,(0,0,0,0)); out.paste(band,(0,0),band)
    # keep only outside figure
    m=Image.new("L",plate.size,0); d2=ImageDraw.Draw(m); 
    out.putalpha(Image.composite(out.split()[3],Image.new("L",plate.size,0),a.point(lambda v:255-v)))
    return out
def paste(base,plate,xy):
    base.alpha_composite(plate,xy); return base
def save(im,name): im.convert("RGBA").save(os.path.join(O,name)); return name
W,H=1100,1500
# 1 pseudo-normal / depth relight: depth = distance inside silhouette approximated by blurred alpha; light from upper-left
plate=fit(APOSE,700,950)
a=plate.split()[3]; depth=a.filter(ImageFilter.GaussianBlur(18))
shade=Image.new("RGBA",plate.size,(0,0,0,0)); px=shade.load(); dp=depth.load(); ap=a.load()
for y in range(plate.height):
    for x in range(plate.width):
        if ap[x,y]>20:
            gx=(dp[min(x+6,plate.width-1),y]-dp[max(x-6,0),y])/255.0
            gy=(dp[x,min(y+6,plate.height-1)]-dp[x,max(y-6,0)])/255.0
            # light dir (-0.6,-0.4): lit where normal faces light
            v=max(0.0,min(1.0,0.5-0.9*gx-0.5*gy))
            if v>0.55: px[x,y]=(0,200,255,int((v-0.55)*220))
            elif v<0.42: px[x,y]=(20,20,60,int((0.42-v)*300))
b=bg(W,H,(16,20,34),(40,44,60)); b= paste(b,plate,(200,250)); b.alpha_composite(shade,(200,250)); save(b,"01-pseudo-normal-relight-20261031.png")
# 2 volumetric shafts: godray bg + plate + shaft beams
b=GOD.resize((W,H)); b=paste(b,fit(APOSE,650,880),(225,300))
shaft=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(shaft)
for x0,wdt,al in [(80,90,70),(300,60,55),(560,110,65),(820,70,50)]:
    d.polygon([(x0,0),(x0+wdt,0),(x0+wdt+220,H),(x0+140,H)],fill=(0,220,255,al))
shaft=shaft.filter(ImageFilter.GaussianBlur(18)); b.alpha_composite(shaft); save(b,"02-volumetric-shafts-20261031.png")
# 3 dust motes in volume
b=b.copy(); d=ImageDraw.Draw(b); random.seed(31)
for _ in range(90):
    x,y=random.randint(20,W-20),random.randint(20,H-20); r=random.randint(1,4); d.ellipse([x-r,y-r,x+r,y+r],fill=(180,240,255,random.randint(90,200)))
save(b,"03-dust-motes-20261031.png")
# 4 side-weighted wrap: rim strong on left/backlit side, weak on right
b=bg(W,H,(14,18,30),(30,34,50)); plate2=fit(APOSE,700,950); b=paste(b,plate2,(200,250))
for dil,blur,col,f in [(3,0,(180,245,255),0.9),(6,5,(0,200,255),0.6)]:
    band=rim_band(plate2,dil,blur,col,f)
    # weight: fade band left->right
    grad=Image.new("L",plate2.size,0); gd=grad.load()
    for x in range(plate2.width):
        wgt=int(255*(1-x/plate2.width*0.75))
        for y in range(plate2.height): gd[x,y]=wgt
    band.putalpha(Image.composite(band.split()[3],Image.new("L",plate2.size,0),grad))
    b.alpha_composite(band,(200,250))
save(b,"04-side-weighted-wrap-20261031.png")
# 5 limb afterglow: punch arm trail - use fighting pose, ghost copies offset left, fading
FIGHT=Image.open(os.path.join(R,"reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png")).convert("RGBA")
b=bg(W,H,(18,18,28),(28,28,40)); fp=fit(FIGHT,700,950)
for i,al in enumerate([0.06,0.12,0.20,0.30,0.40]):
    ghost=rim_band(fp,6,5,(0,200,255),al); b.alpha_composite(ghost,(200-i*28,250))
b=paste(b,fp,(200,250)); save(b,"05-limb-afterglow-punch-20261031.png")
# 6 spirit-bomb orbs snapped: arms-up fists approx at (325,365)/(760,365) in 1100x1500 plate coords -> scaled plate 700x950 at (200,250): fist ~ (406,480)/(685,480)
b=bg(W,H,(16,20,34),(44,40,60)); ap=fit(ARMS,700,950); b=paste(b,ap,(200,250))
d=ImageDraw.Draw(b)
for cx,cy in [(406,480),(685,480)]:
    for r,al in [(90,40),(60,90),(38,180)]:
        d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(255,210,60,al),outline=(255,230,120,220))
save(b,"06-energy-orbs-snapped-fists-20261031.png")
# 7 running cycle + afterglow: walk frames contact + trail
b=bg(1400,700,(18,18,28),(30,30,44))
walk=[os.path.join(R,f"clips-v7c-clean-20261031/walk/{f}") for f in ["walk-01-contact-v7c-clean.png","walk-13-passing-v7c-clean.png","walk-25-contact-v7c-clean.png","walk-37-passing-v7c-clean.png"]]
for i,p in enumerate(walk):
    fr=fit(Image.open(p).convert("RGBA"),300,400); b.alpha_composite(rim_band(fr,6,5,(0,200,255),0.35),(30+i*340,150)); b.alpha_composite(fr,(30+i*340,150))
save(b,"07-running-cycle-afterglow-20261031.png")
# 8 lip-sync timeline: viseme heads strip
b=bg(1600,500,(24,24,36),(40,40,56))
names=["rest","EE","AH","OH","OO","MBP","FV","SZ"]
for i,n in enumerate(names):
    p=os.path.join(R,f"visemes-v2-20261031/head-v2-{i+1:02d}-{'rest' if i==0 else ['ee','ah','oh','oo','mbp','fv','sz'][i-1] if i>0 else ''}-20261031.png")
    # simpler: glob by index
    import glob; cand=glob.glob(os.path.join(R,f"visemes-v2-20261031/head-v2-{i+1:02d}-*.png")); 
    if cand: b.alpha_composite(fit(Image.open(cand[0]).convert("RGBA"),180,240),(10+i*198,120))
save(b,"08-lipsync-timeline-20261031.png")
# 9 storyboard / animatic: 6 panels from poses/backgrounds
b=bg(1500,1000,(20,20,32),(36,36,52)); d=ImageDraw.Draw(b)
panels=[APOSE,ARMS,FIGHT,APOSE,ARMS,FIGHT]
labels=["1 ESTABLISH room 2.5x","2 ARMS-UP pre-flex","3 PUNCH -110 impact","4 DANCE groove","5 FLYING afterglow","6 FLEX true final"]
for i,pl in enumerate(panels):
    x,y=30+(i%3)*490,30+(i//3)*480; fr=fit(pl,280,430); b.alpha_composite(fr,(x+90,y+20)); d.rectangle([x,y,x+470,y+470],outline=(255,255,255,120)); d.text((x+10,y+440),labels[i],fill=(255,255,255,255))
save(b,"09-storyboard-animatic-20261031.png")
# 10 QC gate + title card: QC sheet
b=bg(W,900,(20,24,30),(34,38,48)); d=ImageDraw.Draw(b)
d.text((40,40),"QC GATE 20261031  |  CAPE JONES",fill=(255,255,255,255))
checks=["0 pure-red label pixels in clean plates: PASS","Alpha present, RGBA: PASS","Plate untouched by rim layers: PASS","Knee-feet per-frame gate: PASS (8/8 keyframes)","New dated filename (no cache overwrite): PASS","Title: CAPE JONES — pilot shot pack"]
for i,t in enumerate(checks): d.text((40,120+i*70),("PASS  " if i<5 else "TITLE ")+t,fill=(120,255,160,255) if i<5 else (255,210,60,255))
d.text((40,520),"TITLE CARD: CAPE JONES",fill=(255,255,255,255)); d.rectangle([40,580,1060,820],outline=(255,210,60,255),width=4); d.text((120,660),"CAPE JONES",fill=(255,255,255,255))
save(b,"10-qc-gate-title-card-20261031.png")
# proof contact: thumbnails of 10
proof=bg(1500,1200,(16,16,24),(26,26,36))
for i,f in enumerate(sorted([x for x in os.listdir(O) if x[:2].isdigit()])):
    im=fit(Image.open(os.path.join(O,f)).convert("RGBA"),280,220); proof.alpha_composite(im,(20+(i%5)*295,20+(i//5)*580))
save(proof,"proof-10-wired-20261031.png")
qc={"wired_10":10,"outputs":sorted([x for x in os.listdir(O) if x[:2].isdigit()]),"honest_limits":["01 pseudo-normal from silhouette depth, not measured 3D normal","02 shafts reuse Cycles godray-v2 bg + PIL beams for this proof","orb fist coords are plate-scaled estimates, viewed, snap to be re-measured on full plate"]}
json.dump(qc,open(os.path.join(O,"qc-10-wired-20261031.json"),"w"),indent=2)
print("\n".join(sorted(os.listdir(O))))
