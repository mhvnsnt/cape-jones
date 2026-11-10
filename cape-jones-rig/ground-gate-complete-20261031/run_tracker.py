import sys, os, json
sys.path.insert(0, os.path.expanduser("~/pose-libs"))
import cv2, numpy as np
from PIL import Image
RIG=os.path.expanduser("~/workspace/cape-jones-rig"); OUT=os.path.join(RIG,"ground-gate-complete-20261031")
frames=["CJ-06-walk-street-contact-20261031.png","CJ-07-walk-town-passing-20261031.png","CJ-08-walk-alley-night-20261031.png","CJ-06-walk-street-contact-20261031.png"]
# use grey composites, downscale 2x for speed
imgs=[]
for f in frames:
    im=np.asarray(Image.open(os.path.join(OUT,"composites",f)).convert("L").resize((550,750)))
    imgs.append(im)
# initial foot point: from gate, walk feet ~997 in full res -> 498 in half res, centre-x ~550/2=275
pts=np.array([[[275.,498.]]], dtype=np.float32)
track=[(frames[0], float(pts[0,0,0]), float(pts[0,0,1]))]
for i in range(1,len(imgs)):
    nxt,st,err=cv2.calcOpticalFlowPyrLK(imgs[i-1],imgs[i],pts,None)
    pts=nxt; track.append((frames[i], float(pts[0,0,0]), float(pts[0,0,1])))
    print(frames[i], "tracked foot half-res", pts[0,0].tolist(), "status", st.tolist())
json.dump({"method":"OpenCV Lucas-Kanade (free tracker, AE/Premiere tracker equivalent — AE itself not run, see report)",
 "note":"AE/Premiere tracker itself: NOT run — Adobe trial not confirmed, Win/Mac only, no AE on this Linux VM. Free way around RUN here: OpenCV tracker on the walk composites, plus Blender Cycles ground-plane render above.",
 "track_half_res":track}, open(os.path.join(OUT,"tracker-20261031.json"),"w"), indent=2)
