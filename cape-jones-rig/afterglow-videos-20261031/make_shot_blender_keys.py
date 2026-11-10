"""One Blender key frame per shot: frame 5 (last moving frame for moving
shots; rest frame for hold shots). Trail layer = soft bands of previous
positions only (never at current position); plate layer = apose plate.
Shot rim colour from shot-specs JSON."""
import json, re, os
from PIL import Image, ImageFilter
import numpy as np
R=os.path.expanduser("~/workspace/cape-jones-rig"); OUT=f"{R}/afterglow-videos-20261031/blender_keys_shots"
os.makedirs(OUT,exist_ok=True)
TRAIL=[0.50,0.40,0.30,0.20,0.12,0.06]; W,H=640,360
def parse_rim(s):
    if isinstance(s,list) and len(s)>=3: return tuple(int(x) for x in s[:3])
    if isinstance(s,str):
        m=re.findall(r"(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})",s)
        if m: return tuple(int(x) for x in m[0])
    return (0,200,255)
plate=Image.open(f"{R}/rig-apose-v7c-clean-transparent.png").convert("RGBA")
w,h=plate.size; plate=plate.resize((int(w*300/h),300),Image.LANCZOS)
d=plate.split()[3].filter(ImageFilter.MaxFilter(13)).filter(ImageFilter.GaussianBlur(5))
band=Image.fromarray(np.clip(np.array(d,dtype=np.int16)-np.array(plate.split()[3],dtype=np.int16),0,255).astype(np.uint8),"L")
specs=json.load(open(f"{R}/clean-100-20261031/shots/shot-specs-30-20261031.json"))["shots"]
moving={"CJ-02","CJ-05","CJ-06","CJ-07","CJ-08","CJ-09","CJ-10","CJ-11","CJ-12","CJ-13","CJ-14","CJ-15","CJ-21","CJ-22","CJ-04"}
for s in specs:
    sid=s["shot_id"]; color=parse_rim(s.get("rim_color"))
    xs=[60+i*24 for i in range(6)]+[204]*6 if sid in moving else [180]*12
    fi=5; x,y=xs[fi],30
    trail=Image.new("RGBA",(W,H),(0,0,0,0))
    for lag,f in enumerate(TRAIL,1):
        px,py=xs[fi-lag],30
        if px==x: continue
        glow=Image.new("RGBA",plate.size,(color[0],color[1],color[2],0))
        glow.putalpha(band.point(lambda v: int(v*f)))
        trail.alpha_composite(glow,(px,py))
    trail.save(f"{OUT}/{sid}-trail.png")
    pl=Image.new("RGBA",(W,H),(0,0,0,0)); pl.alpha_composite(plate,(x,y))
    pl.save(f"{OUT}/{sid}-plate.png")
    print(sid, color, "moving" if sid in moving else "hold-zero", flush=True)
print("KEY LAYERS DONE")
