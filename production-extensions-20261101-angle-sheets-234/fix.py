import os, json
from PIL import Image
OUT="/tmp/angle-sheets-234"; SRC=os.path.expanduser("~/workspace/cape-jones-rig/production-extensions-20261101/slices")
P=os.path.join(OUT,"pieces"); A=os.path.join(OUT,"assemblies")
def load(p): return Image.open(p).convert("RGBA")
def scale(im,sx,sy=None):
    sy=sx if sy is None else sy
    return im.resize((max(1,round(im.width*sx)),max(1,round(im.height*sy))),Image.LANCZOS)
def trap(im,top,bot,ys):
    w,h=im.size; nh=max(1,round(h*ys))
    out=Image.new("RGBA",(max(1,round(w*max(top,bot)))+4,nh),(0,0,0,0))
    for y in range(h):
        oy=round(y*ys)
        if oy>=nh: break
        f=top+(bot-top)*(y/max(1,h-1)); row=im.crop((0,y,w,y+1)); nw=max(1,round(w*f))
        out.alpha_composite(row.resize((nw,1),Image.LANCZOS),((out.width-nw)//2,oy))
    bb=out.getchannel("A").getbbox(); return out.crop(bb) if bb else out
def paste(b,im,cx,cy): b.alpha_composite(im,(round(cx-im.width/2),round(cy-im.height/2)))
from PIL import ImageDraw
def shadow(b,cx,cy,rx,ry):
    l=Image.new("RGBA",b.size,(0,0,0,0)); ImageDraw.Draw(l).ellipse([cx-rx,cy-ry,cx+rx,cy+ry],fill=(0,0,0,70)); b.alpha_composite(l)

# --- fix aiming composite: forearm visible left, fist foreground right, ~45% overlap ---
g=scale(load(os.path.join(SRC,"Gauntlet_L.png")),0.85,1.40)
f=load(os.path.join(SRC,"Hand_Fist.png"))
overlap=115; cw=g.width+f.width-overlap; ch=max(g.height,f.height)+10
comp=Image.new("RGBA",(cw,ch),(0,0,0,0))
comp.alpha_composite(g,(0,(ch-g.height)//2)); comp.alpha_composite(f,(g.width-overlap,(ch-f.height)//2))
bb=comp.getchannel("A").getbbox(); comp=comp.crop(bb); comp.save(os.path.join(P,"Forearm_Gauntlet_AimingAtLens.png"))
print("aim fixed",comp.size)

GREY=(128,128,128,255)
# --- Sheet 2, tight joints, vertical shins ---
b=Image.new("RGBA",(1200,1400),GREY); shadow(b,600,1240,300,30)
head=scale(load(os.path.join(SRC,"Head_Front.png")),0.85); torso=scale(load(os.path.join(SRC,"Torso_LeanForward.png")),1.05)
pelvis=scale(load(os.path.join(SRC,"Pelvis_Whole.png")),0.95); ua=load(os.path.join(P,"UpperArm_Z_Short.png"))
hand=scale(load(os.path.join(SRC,"Hand_Fist.png")),0.70)
thigh=trap(load(os.path.join(SRC,"Thigh_L.png")),1.0,0.85,0.70); thigh=scale(thigh,0.9)
shin=scale(load(os.path.join(SRC,"Shin_L.png")),1.0,0.60); sole=scale(load(os.path.join(SRC,"Sole_Boot_Flat_L.png")),0.70)
paste(b,torso,600,470); paste(b,head,600,240); paste(b,pelvis,600,700)
paste(b,ua,330,450); paste(b,ua.transpose(Image.FLIP_LEFT_RIGHT),870,450)
paste(b,hand,245,520); paste(b,hand,955,520)
paste(b,thigh,500,880); paste(b,thigh,700,880)
paste(b,shin,500,1030); paste(b,shin,700,1030)
paste(b,sole,500,1145); paste(b,sole,700,1145)
b.save(os.path.join(A,"Angle_Sheet_2_BirdsEye_DERIVED_ASSEMBLY.png")); print("s2",b.size)
# --- Sheet 3, tight joints ---
b=Image.new("RGBA",(1200,1600),GREY); shadow(b,600,1520,380,34)
boot=scale(load(os.path.join(SRC,"Boot.png")),1.40); thigh3=scale(load(os.path.join(SRC,"Thigh_L.png")),1.05,1.20)
pelvis3=scale(load(os.path.join(SRC,"Pelvis_Whole.png")),1.05); torso3=scale(load(os.path.join(SRC,"Torso_LeanBack.png")),1.0,1.25)
head3=scale(load(os.path.join(SRC,"Head_Front.png")),0.80); aim=scale(load(os.path.join(P,"Forearm_Gauntlet_AimingAtLens.png")),1.10)
paste(b,boot,430,1250); paste(b,boot.transpose(Image.FLIP_LEFT_RIGHT),770,1250)
paste(b,thigh3,470,900); paste(b,thigh3,730,900); paste(b,pelvis3,600,700); paste(b,torso3,600,450); paste(b,head3,600,180)
paste(b,aim,260,560); paste(b,scale(load(os.path.join(SRC,"Hand_Fist.png")),0.70),950,520)
b.save(os.path.join(A,"Angle_Sheet_3_WormsEye_DERIVED_ASSEMBLY.png")); print("s3",b.size)
# --- Sheet 4, diagonal, kick inside canvas ---
b=Image.new("RGBA",(1400,1200),GREY); shadow(b,700,1100,420,30)
torso4=scale(load(os.path.join(SRC,"Torso_LeanForward.png")).rotate(-14,resample=Image.BICUBIC,expand=True),1.05)
head4=scale(load(os.path.join(SRC,"Head_Front.png")).rotate(-10,resample=Image.BICUBIC,expand=True),0.95)
paste(b,scale(load(os.path.join(SRC,"Thigh_L.png")),0.70),480,720)
paste(b,scale(load(os.path.join(SRC,"Boot.png")),0.70),430,950)
paste(b,torso4,700,420); paste(b,head4,780,180); paste(b,scale(load(os.path.join(SRC,"Hand_Fist.png")),0.70),400,380)
paste(b,scale(load(os.path.join(P,"Thigh_KneeForward_Z.png")),1.30),920,680)
paste(b,scale(load(os.path.join(P,"Shin_Boot_Z_Compressed.png")),1.20),1000,850)
paste(b,load(os.path.join(P,"Foot_Kick_Z.png")),1050,970)
paste(b,scale(load(os.path.join(P,"Forearm_Gauntlet_AimingAtLens.png")),1.20),430,600)
b.save(os.path.join(A,"Angle_Sheet_4_DiagonalLunge_DERIVED_ASSEMBLY.png")); print("s4",b.size)
# refresh index sizes/shas for changed files
import hashlib
def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for c in iter(lambda:f.read(65536),b""): h.update(c)
    return h.hexdigest()
idx=json.load(open(os.path.join(OUT,"piece-index-20261101.json")))
for r in idx:
    if r["output"]:
        p=os.path.join(OUT,r["output"]); im=Image.open(p); r["output_size_px"]=list(im.size); r["sha256"]=sha(p)
    if r["item"]=="Forearm_Gauntlet_AimingAtLens":
        r["transform"]="Gauntlet_L x0.85/y1.40 + Hand_Fist 1.0x composited with 115px overlap (forearm visible left, fist foreground right)"
json.dump(idx,open(os.path.join(OUT,"piece-index-20261101.json"),"w"),indent=1)
print("index refreshed")
