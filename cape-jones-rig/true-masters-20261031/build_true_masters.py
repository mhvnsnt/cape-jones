"""True masters 2026-10-31. Sources stated in REPORT; base art never recoloured.
1-3: Mars B-model sheet crops, padded only (no scale, no recolour).
4: torso-twist composite: upper = 3/4-front-set2, lower = front-set2 (same set2 series)."""
from PIL import Image
import os, json
ROOT="/home/hatch/workspace/cape-jones-rig"
SRC=os.path.join(ROOT,"sliced-clean-20261031/B-model")
OUT=os.path.join(ROOT,"true-masters-20261031")
PAD=40; GREY=(128,128,128,255)
def load(p): return Image.open(p).convert("RGBA")
def pad(im,pad=PAD):
    c=Image.new("RGBA",(im.size[0]+2*pad,im.size[1]+2*pad),(0,0,0,0)); c.alpha_composite(im,(pad,pad)); return c
def on_grey(im):
    bg=Image.new("RGBA",im.size,GREY); bg.alpha_composite(im); return bg.convert("RGB")
def stats(im):
    import numpy as np; a=np.array(im)[:,:,3]; ys,xs=np.where(a>10)
    return {"size":list(im.size),"bbox":[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],"alpha_px":int((a>10).sum())}
def save_pair(im,name):
    p=pad(im); p.save(os.path.join(OUT,name)); on_grey(p).save(os.path.join(OUT,name.replace(".png","-on-grey.png")))
    return stats(p)
meas={}
# 1-3 direct masters
jobs=[
 ("model-sheet-3quarter-front-set2/Row1_1.png","01-true-master-3quarter-front-20261031.png"),
 ("model-sheet-side-set2/Row1_1.png","02-true-master-side-20261031.png"),
 ("model-sheet-back-set2/Row1_1.png","03-true-master-back-20261031.png"),
]
for src,name in jobs:
    meas[name]=save_pair(load(os.path.join(SRC,src)),name); print(name,meas[name])
# 4 torso-twist
front=load(os.path.join(SRC,"model-sheet-front-set2/Row1_1.png"))
q=load(os.path.join(SRC,"model-sheet-3quarter-front-set2/Row1_1.png"))
# scale 3/4 to front height, align waists
scale=front.size[1]/q.size[1]
qw=int(q.size[0]*scale); qh=int(q.size[1]*scale)
q2=q.resize((qw,qh),Image.LANCZOS)
FRONT_WAIST=478; Q_WAIST=492  # estimated belt centres, native coords; checked visually in v1
shift_y=int(FRONT_WAIST - Q_WAIST*scale)
# centre-align on figure centre: front centre x ~553, q centre ~261*scale
shift_x=int(553 - 261*scale)
comp=Image.new("RGBA",front.size,(0,0,0,0)); comp.alpha_composite(front,(0,0))
# build upper layer: keep all rows < FRONT_WAIST; below, keep only outer zones (arms/cape), drop central leg column
import numpy as np
layer=Image.new("RGBA",front.size,(0,0,0,0)); layer.alpha_composite(q2,(shift_x,shift_y))
la=np.array(layer); fa=np.array(front)
# central leg column in composited coords: q native x 100..420 scaled+shifted
x0=int(shift_x+100*scale); x1=int(shift_x+420*scale)
mask=np.zeros(la.shape[:2],bool); mask[FRONT_WAIST:,:]=True; mask[:,x0:x1]=False  # placeholder, refine below
# Actually: below waist, zero out central column only
arr=np.array(layer)
arr[FRONT_WAIST:, x0:x1, 3]=0
# also zero the alpha where it was only central-column? above line already handles (rows>=waist, cols x0:x1 -> alpha 0)
layer=Image.fromarray(arr)
# erase front upper body above waist (keep nothing above waist from front except nothing) -> rebuild: front lower only
base=np.array(front); base[:FRONT_WAIST,:,3]=0
comp=Image.fromarray(base); comp.alpha_composite(layer,(0,0))
# seam softening: none (no recolour, no blur of art) - belt discontinuity left visible for Mars ruling if present
meas["04-true-master-torso-twist-20261031.png"]=save_pair(comp,"04-true-master-torso-twist-20261031.png")
print("twist",meas["04-true-master-torso-twist-20261031.png"],"scale",scale,"shift",shift_x,shift_y,"legcol",x0,x1)
# contact sheet on grey
from PIL import ImageDraw
tiles=[]
for n in ["01-true-master-3quarter-front-20261031.png","02-true-master-side-20261031.png","03-true-master-back-20261031.png","04-true-master-torso-twist-20261031.png"]:
    t=on_grey(pad(load(os.path.join(OUT,n)),20)); t.thumbnail((520,520),Image.LANCZOS); tiles.append((n,t))
W=1080; H=sum(t.size[1]+44 for _,t in tiles)+20
sheet=Image.new("RGB",(W,H),(128,128,128)); d=ImageDraw.Draw(sheet); y=10
for n,t in tiles:
    d.text((10,y),n,fill=(255,255,255)); y+=22; sheet.paste(t,((W-t.size[0])//2,y)); y+=t.size[1]+22
sheet.save(os.path.join(OUT,"true-masters-contact-20261031.png")); print("contact",sheet.size)
json.dump({"masters":meas,"twist_params":{"scale":scale,"shift_x":shift_x,"shift_y":shift_y,"front_waist":FRONT_WAIST,"q_waist_native":Q_WAIST,"leg_col_composited":[x0,x1]}},open(os.path.join(OUT,"measurements-20261031.json"),"w"),indent=1)
