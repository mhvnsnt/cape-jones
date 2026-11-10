import json, os
from PIL import Image
import numpy as np
from scipy import ndimage
W='/home/hatch/workspace/cape-jones-rig/robin-eyes-100-20261031'
OUT=f'{W}/library'; os.makedirs(OUT, exist_ok=True)
def comp_mask(im, box):
    """Return mask image (RGBA, white shape only) for the white component whose bbox best matches box."""
    a=np.array(im.convert('RGBA')); rgb=a[:,:,:3].astype(int); al=a[:,:,3]
    white=(rgb[:,:,0]>235)&(rgb[:,:,1]>235)&(rgb[:,:,2]>235)&(al>200)
    lab,n=ndimage.label(white)
    x0,x1,y0,y1=box; best=None; bestscore=1e9
    for i in range(1,n+1):
        yy,xx=np.where(lab==i)
        if len(yy)<40: continue
        bx0,bx1,by0,by1=int(xx.min()),int(xx.max()),int(yy.min()),int(yy.max())
        score=abs(bx0-x0)+abs(bx1-x1)+abs(by0-y0)+abs(by1-y1)
        if score<bestscore: bestscore=score; best=(lab==i,bx0,bx1,by0,by1)
    assert best is not None and bestscore<60, (box, bestscore)
    m,ax0,ax1,ay0,ay1=best
    out=np.zeros_like(a); out[m]=a[m]
    return Image.fromarray(out[ay0:ay1+1, ax0:ax1+1]), (ax0,ax1,ay0,ay1)
# curated pairs: (id, label, source render, [boxL, boxR] or [box] for profile, kind)
PAIRS=[
 ("01-day-front-neutral","Day front neutral (v4 source)","02_ROBIN_Day.jpg",[(805,898,676,737),(935,998,685,733)],"jpg"),
 ("02-night-front-neutral","Night front neutral (shadow grey)","03_ROBIN_Night.jpg",[(799,895,682,743),(927,992,691,739)],"jpg"),
 ("03-rbn01-front-neutral","RBN01 front neutral (tall model)","09_RBN01_CAMS_DCTTAS.png",[(191,222,625,654),(238,287,623,655)],"render"),
 ("04-rbn02-side-profile","RBN02 side profile","10_RBN02_CAMS_DCTTAS.png",[(147,193,636,669)],"render"),
 ("05-ca01-action","CA01 action","23_RBN01_CA_DCTTAS.png",[(537,578,599,667),(601,687,628,681)],"render"),
 ("06-ca02-action","CA02 action","26_RBN02_CA_DCTTAS.png",[(503,570,698,759),(600,691,713,772)],"render"),
 ("07-ca03-action","CA03 action","24_RBN03_CA_DCTTAS.png",[(648,716,562,603),(745,776,526,582)],"render"),
 ("08-rb01-action","RB01 action (SG01)","37_RB01_CA_DCTTA.png",[(727,781,377,442)],"render"),
 ("09-rb02-action","RB02 action (SG01)","40_RB02_CA_DCTTA.png",[(673,734,822,912)],"render"),
 ("10-rb03-action","RB03 action (SG01)","39_RB03_CA_DCTTA.png",[(502,547,368,403)],"render"),
 ("11-expres01-angry","RBEXPRES01 angry shout","51_RBEXPRES01_CA_DCTTAS.png",[(256,349,658,739),(370,599,654,749)],"render"),
 ("12-expres02-determined","RBEXPRES02 determined","47_RBEXPRES02_CA_DCTTAS.png",[(222,374,1061,1207),(429,549,1144,1212)],"render"),
 ("13-expres03-angry-point","RBEXPRES03 angry point","53_RBEXPRES03_CA_DCTTAS.png",[(227,386,957,1069),(424,564,946,1069)],"render"),
 ("14-expres04-strain","RBEXPRES04 strain","50_RBEXPRES04_CA_DCTTAS.png",[(434,605,1065,1185),(622,710,1078,1180)],"render"),
 ("15-expres05-grit","RBEXPRES05 grit","49_RBEXPRES05_CA_DCTTAS.png",[(197,417,977,1045),(500,703,999,1052)],"render"),
 ("16-sg01-laugh-swirl","SG01 laughing swirl (comedic)","38_RBNEXPRES_CA_DCTTA.png",[(202,321,1028,1188),(353,413,1121,1188)],"render"),
 ("17-dc-robin1-action","DC ref Robin1 action","58_Robin1.png",[(574,634,539,629)],"render"),
 ("18-dc-robin2-action","DC ref Robin2 action","59_Robin2.png",[(873,927,273,338)],"render"),
 ("19-dc-robin3-action","DC ref Robin3 action","57_Robin3.png",[(550,596,234,270)],"render"),
 ("20-cc-front-neutral","CC front neutral","05_Robin_CC.png",[(605,635,362,382),(649,669,366,381)],"render"),
 ("21-robin1-neutral","Robin 1.ai neutral (small figure)","00_Robin_1.png",[(608,628,593,607),(639,652,596,606)],"render"),
 ("22-robin2-34","Robin 2.ai 3/4 close-up","01_Robin_2.png",[(180,260,150,212),(296,371,98,176)],"render"),
 ("23-headai-neutral","Robin Head.ai neutral","13_Robin_Head.png",[(604,623,800,813),(634,647,803,812)],"render"),
 ("24-rbn01bw-front-neutral","RBN01 B&W front neutral (same art as #03)","15_RBN01_CAMSb_DCTTAS.png",[(175,222,621,654),(238,287,623,655)],"render"),
]
# Night uses grey threshold: handle by thr param
def comp_mask_thr(im, box, thr):
    a=np.array(im.convert('RGBA')); rgb=a[:,:,:3].astype(int); al=a[:,:,3]
    white=(rgb[:,:,0]>thr)&(rgb[:,:,1]>thr)&(rgb[:,:,2]>thr)&(al>200)
    lab,n=ndimage.label(white)
    x0,x1,y0,y1=box; best=None; bestscore=1e9
    for i in range(1,n+1):
        yy,xx=np.where(lab==i)
        if len(yy)<40: continue
        bx0,bx1,by0,by1=int(xx.min()),int(xx.max()),int(yy.min()),int(yy.max())
        score=abs(bx0-x0)+abs(bx1-x1)+abs(by0-y0)+abs(by1-y1)
        if score<bestscore: bestscore=score; best=(lab==i,bx0,bx1,by0,by1)
    assert best is not None and bestscore<80, (box, bestscore)
    m,ax0,ax1,ay0,ay1=best
    out=np.zeros_like(a); out[m]=a[m]
    return Image.fromarray(out[ay0:ay1+1, ax0:ax1+1]), (ax0,ax1,ay0,ay1)
manifest=[]
for pid,label,src,boxes,kind in PAIRS:
    if kind=="jpg":
        im=Image.open(f'{W}/raw/{src}').convert('RGBA')
        thr=150 if 'Night' in src else 235
        masks=[comp_mask_thr(im,b,thr)[0] for b in boxes]
    else:
        im=Image.open(f'{W}/render/{src}').convert('RGBA')
        masks=[comp_mask(im,b)[0] for b in boxes]
    # strip 480x128: eyes side by side, dark cowl segment image-left (v4 convention, (52,22,66))
    strip=Image.new('RGBA',(480,128),(0,0,0,0))
    # dark end segment x38-79 full strip height band? v4: dark left segment in strip; use a vertical band y34-94
    from PIL import ImageDraw
    d=ImageDraw.Draw(strip); d.rectangle([38,34,79,94], fill=(52,22,66,255))
    # place eyes: scale each to height 60, centered vertically, pair centered
    scaled=[]
    for mk in masks:
        s=60/mk.size[1]; scaled.append(mk.resize((max(1,int(mk.size[0]*s)),60), Image.LANCZOS))
    total=sum(s.size[0] for s in scaled)+ (20 if len(scaled)>1 else 0)
    x=(480-total)//2
    for s in scaled:
        strip.paste(s,(x,34),s); x+=s.size[0]+20
    strip.save(f'{OUT}/{pid}-strip.png')
    for j,mk in enumerate(masks): mk.save(f'{OUT}/{pid}-eye{j}.png')
    manifest.append(dict(id=pid,label=label,source=src,eyes=len(masks),
                         eye_sizes=[list(mk.size) for mk in masks]))
    print(pid, [mk.size for mk in masks])
json.dump(manifest, open(f'{OUT}/manifest.json','w'), indent=1)
print("LIBRARY DONE", len(manifest))
