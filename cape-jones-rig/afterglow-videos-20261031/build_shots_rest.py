import json, re, os
from PIL import Image, ImageFilter
import numpy as np
R=os.path.expanduser("~/workspace/cape-jones-rig"); OUT=f"{R}/afterglow-videos-20261031"
BG=(18,18,28,255); TRAIL=[0.50,0.40,0.30,0.20,0.12,0.06]; W,H=640,360
def soft_band(alpha):
    d=alpha.filter(ImageFilter.MaxFilter(13)).filter(ImageFilter.GaussianBlur(5))
    return Image.fromarray(np.clip(np.array(d,dtype=np.int16)-np.array(alpha,dtype=np.int16),0,255).astype(np.uint8),"L")
def parse_rim(s):
    if isinstance(s,list) and len(s)>=3: return tuple(int(x) for x in s[:3])
    if isinstance(s,str):
        m=re.findall(r"(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})",s)
        if m: return tuple(int(x) for x in m[0])
    return (0,200,255)
plate=Image.open(f"{R}/rig-apose-v7c-clean-transparent.png").convert("RGBA")
w,h=plate.size; plate=plate.resize((int(w*300/h),300),Image.LANCZOS)
pw2,ph2=plate.size; band=soft_band(plate.split()[3])
specs=json.load(open(f"{R}/clean-100-20261031/shots/shot-specs-30-20261031.json"))["shots"]
moving={"CJ-02","CJ-05","CJ-06","CJ-07","CJ-08","CJ-09","CJ-10","CJ-11","CJ-12","CJ-13","CJ-14","CJ-15","CJ-21","CJ-22","CJ-04"}
for s in specs:
    sid,slug=s["shot_id"],s["slug"]
    if sid in ("CJ-01","CJ-02","CJ-03","CJ-04","CJ-05","CJ-06","CJ-07","CJ-08","CJ-09","CJ-10","CJ-11","CJ-12","CJ-13"): continue
    color=parse_rim(s.get("rim_color"))
    xs=[60+i*24 for i in range(6)]+[204]*6 if sid in moving else [180]*12
    pos=[(x,30) for x in xs]; frames=[]
    for fi,(x,y) in enumerate(pos):
        decay=0.5**(fi-5) if fi>=6 else 1.0
        canvas=Image.new("RGBA",(W,H),BG)
        for lag,f in enumerate(TRAIL,1):
            if fi-lag<0: continue
            px,py=pos[fi-lag]
            glow=Image.new("RGBA",(pw2,ph2),(color[0],color[1],color[2],0))
            glow.putalpha(band.point(lambda v: int(v*f*decay)))
            canvas.alpha_composite(glow,(px,py))
        canvas.alpha_composite(plate,(x,y)); frames.append(canvas.convert("RGB"))
    d=f"{OUT}/frames_shots/{sid}"; os.makedirs(d,exist_ok=True)
    for fi,fr in enumerate(frames): fr.save(f"{d}/{sid}-frame-{fi:02d}.png")
    frames[0].save(f"{OUT}/{sid}-{slug}-afterglow-20261031.gif",save_all=True,append_images=frames[1:],duration=100,loop=0)
    print(sid,slug,color,"moving" if sid in moving else "hold",flush=True)
print("REST DONE")
