import json, re, os
from PIL import Image, ImageFilter
import numpy as np
R=os.path.expanduser("~/workspace/cape-jones-rig"); OUT=f"{R}/afterglow-videos-20261031"
BG=(18,18,28,255); TRAIL=[0.50,0.40,0.30,0.20,0.12,0.06]; W,H=640,360
def band_of(alpha):
    d=alpha.filter(ImageFilter.MaxFilter(13)).filter(ImageFilter.GaussianBlur(5))
    return Image.fromarray(np.clip(np.array(d,dtype=np.int16)-np.array(alpha,dtype=np.int16),0,255).astype(np.uint8),"L")
def parse_rim(s):
    if isinstance(s,list) and len(s)>=3: return tuple(int(x) for x in s[:3])
    if isinstance(s,str):
        m=re.findall(r"(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})",s)
        if m: return tuple(int(x) for x in m[0])
    return (0,200,255)
def render(piece, positions, color, decay_hold=None):
    band=band_of(piece.split()[3]); frames=[]
    for fi,(x,y) in enumerate(positions):
        decay=1.0
        if decay_hold is not None and fi>=decay_hold: decay=0.5**(fi-decay_hold+1)
        canvas=Image.new("RGBA",(W,H),BG)
        for lag,f in enumerate(TRAIL,1):
            if fi-lag<0: continue
            px,py=positions[fi-lag]
            if (px,py)==(x,y): continue
            glow=Image.new("RGBA",piece.size,(color[0],color[1],color[2],0))
            glow.putalpha(band.point(lambda v: int(v*f*decay)))
            canvas.alpha_composite(glow,(px,py))
        canvas.alpha_composite(piece,(x,y)); frames.append(canvas.convert("RGB"))
    return frames
fore=Image.open(f"{R}/forearm-fist-v5-correction-20261031/forearm-v5-arm2-forward-punch-flipped-20261031.png").convert("RGBA")
fw,fh=fore.size; fore=fore.resize((200,int(fh*200/fw)),Image.LANCZOS)
punch_pos=[(400,150)]*3+[(350,125),(300,100),(250,75),(210,60)]+[(210,60)]*4+[(260,85),(320,115),(380,140)]+[(380,140)]*4
pf=render(fore,punch_pos,(0,200,255))
for i,fr in enumerate(pf): fr.save(f"{OUT}/frames_punch/punch-frame-{i:02d}.png")
pf[0].save(f"{OUT}/punch-limb-afterglow-20261031.gif",save_all=True,append_images=pf[1:],duration=100,loop=0)
sheet=Image.new("RGB",(640*4+30,360+40),(255,255,255))
for i,idx in enumerate([2,5,7,17]): sheet.paste(pf[idx],(i*650,20))
sheet.save(f"{OUT}/punch-limb-afterglow-contact-20261031.png")
print("punch ok",flush=True)
plate=Image.open(f"{R}/rig-apose-v7c-clean-transparent.png").convert("RGBA")
w,h=plate.size; plate=plate.resize((int(w*300/h),300),Image.LANCZOS)
specs=json.load(open(f"{R}/clean-100-20261031/shots/shot-specs-30-20261031.json"))["shots"]
moving={"CJ-02","CJ-05","CJ-06","CJ-07","CJ-08","CJ-09","CJ-10","CJ-11","CJ-12","CJ-13","CJ-14","CJ-15","CJ-21","CJ-22","CJ-04"}
res=[]
for s in specs:
    sid,slug=s["shot_id"],s["slug"]; color=parse_rim(s.get("rim_color"))
    xs=[60+i*24 for i in range(6)]+[204]*6 if sid in moving else [180]*12
    frames=render(plate,[(x,30) for x in xs],color,decay_hold=6)
    d=f"{OUT}/frames_shots/{sid}"; os.makedirs(d,exist_ok=True)
    for fi,fr in enumerate(frames): fr.save(f"{d}/{sid}-frame-{fi:02d}.png")
    frames[0].save(f"{OUT}/{sid}-{slug}-afterglow-20261031.gif",save_all=True,append_images=frames[1:],duration=100,loop=0)
    res.append({"shot_id":sid,"slug":slug,"rim_input_rgb":list(color),"moving":sid in moving,"frames":len(frames),"lighting_level":s["lighting_level"],"god_ray_decision":s["god_ray_decision"]})
    print(sid,slug,color,"moving" if sid in moving else "hold-zero",flush=True)
json.dump(res,open(f"{OUT}/shot-afterglow-index-20261031.json","w"),indent=1)
print("ALL DONE",len(res))
