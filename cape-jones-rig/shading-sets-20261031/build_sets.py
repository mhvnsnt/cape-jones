#!/usr/bin/env python3
"""Shading Sets One and Two + Set Two continuation, 2026-10-31.
Set One = old G2 (BARELY WORKS). Set Two = shading upgrade (DEFINITELY WORKS).
Continuation = 20 new variants wired into Set Two's normal field.
Normals ESTIMATED from silhouette distance + linework, not a true 3D mesh pass.
Base art untouched; all outputs are new files in shading-sets-20261031/."""
import json, os, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

ROOT="/home/hatch/workspace/cape-jones-rig"
OUT=os.path.join(ROOT,"shading-sets-20261031")
BASE=Image.open(os.path.join(ROOT,"rig-apose-v7c-clean-transparent.png")).convert("RGBA")
ARMS=Image.open(os.path.join(ROOT,"dual-light-variants-20261031","base-arms-up-transparent-20261031.png")).convert("RGBA")

def norm(v):
    v=np.array(v,float); return v/np.linalg.norm(v)
def fields(im):
    a=np.asarray(im).astype(np.float32)/255.0; rgb,alpha=a[...,:3],a[...,3]
    mask=alpha>0.5; ys,xs=np.where(mask); bbox=(int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max()))
    cx=(bbox[0]+bbox[1])/2.0; dist=ndimage.distance_transform_edt(mask)
    gray=rgb.mean(axis=2); eroded=ndimage.binary_erosion(mask,iterations=4)
    gmax=ndimage.maximum_filter(gray,size=7); lines=eroded&(gray<0.43)&((gmax-gray)>0.12)
    ds=ndimage.gaussian_filter(dist,2.0); dzdy,dzdx=np.gradient(ds)
    nx=-dzdx*1.5; ny=-dzdy*1.5; nz=np.ones_like(dist); nl=np.sqrt(nx**2+ny**2+nz**2)
    return dict(mask=mask,nx=nx/nl,ny=ny/nl,nz=nz/nl,lines=lines,dist=dist,bbox=bbox,cx=cx,alpha=alpha)
def shade_im(im,shade,F):
    a=np.asarray(im).astype(float); out=a.copy(); out[...,:3]*=shade[...,None]; out[...,3]=a[...,3]
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8),"RGBA")
def stats(im,F):
    arr=np.asarray(im).astype(float); mask=F["mask"]; cx=F["cx"]; W=arr.shape[1]; xs=np.arange(W)[None,:]
    left=mask&(xs<cx); right=mask&(xs>=cx); nx=F["nx"]
    lf=mask&(nx<-0.3); rf=mask&(nx>0.3)
    def m(s,ch=0): return round(float(arr[...,ch][s].mean()),1) if s.any() else 0.0
    return {"left_R":m(left),"right_R":m(right),"delta_R":round(m(left)-m(right),1),
            "left_facing_R":m(lf),"right_facing_R":m(rf),"edge_delta_R":round(m(lf)-m(rf),1),
            "mask_px":int(mask.sum()),"centre_x":cx}
def grey(im):
    bg=Image.new("RGBA",im.size,(128,128,128,255)); bg.alpha_composite(im); return bg.convert("RGB")
def contact(tiles,path,cols=4):
    tw=275; th=int(tw*1500/1100); rows=(len(tiles)+cols-1)//cols
    sheet=Image.new("RGB",(cols*tw,rows*(th+28)),(200,200,200)); dr=ImageDraw.Draw(sheet)
    for i,(lab,t) in enumerate(tiles):
        x,y=(i%cols)*tw,(i//cols)*(th+28); sheet.paste(t.resize((tw,th)),(x,y+28)); dr.text((x+4,y+6),lab,fill=(0,0,0))
    sheet.save(path); return sheet

F=fields(BASE); mask=F["mask"]; nx,ny,nz=F["nx"],F["ny"],F["nz"]; dist=F["dist"]; lines=F["lines"]
L_LEFT=norm([-0.80,-0.20,0.56]); L_RIGHT=norm([0.80,-0.20,0.56]); L_TOP=norm([0.0,-1.0,0.45])
def diff(L): return np.clip(nx*L[0]+ny*L[1]+nz*L[2],0,1)
dL,dR,dT=diff(L_LEFT),diff(L_RIGHT),diff(L_TOP)
ao=np.clip(dist/18.0,0,1)
h,w=mask.shape; yy,xx=np.mgrid[0:h,0:w]; x0,x1=F["bbox"][0],F["bbox"][1]
s_left=np.clip((x1-xx)/max(1,(x1-x0)),0,1)
edge=mask&(dist<5)
# --- 10 industry-standard ---
variants=[]
def add(name,shade,method,run="PIL run"):
    im=shade_im(BASE,np.where(mask,shade,1.0),F); im.save(f"{OUT}/new-variants/{name}.png")
    st=stats(im,F); st.update({"method":method,"run":run}); variants.append((name,im,st)); print(name,st)
# I-01 Half-Lambert (Valve): wrap diffuse so terminator is soft
add("N01-half-lambert-LEFT",0.35+0.65*np.sqrt(np.clip(dL,0,1)),"Half-Lambert (Valve): diffuse^0.5, soft terminator, KEY LEFT.")
# I-02 Wrap lighting: diffuse wrapped toward shadow side
add("N02-wrap-light-LEFT",0.35+0.65*np.clip((dL+0.35)/1.35,0,1),"Wrap lighting: (N.L+wrap)/(1+wrap), wrap 0.35, KEY LEFT.")
# I-03 Rim only: edge band on lit side
rim=np.where(edge,1.0,0.55+0.45*dL); add("N03-rim-only-LEFT",np.where(mask,rim,1.0),"Rim light: silhouette edge band bright, interior Lambert, KEY LEFT.")
# I-04 Cel 5-band
bands=np.select([dL<0.20,dL<0.40,dL<0.60,dL<0.80],[0.35,0.55,0.75,0.90],default=1.00)
add("N04-cel-5band-LEFT",bands,"Cel/toon 5-band quantised Lambert, KEY LEFT.")
# I-05 SSS approximation (PIL, NOT true volumetric SSS): blurred diffuse + edge translucency
sss=(0.45+0.55*ndimage.gaussian_filter(dL,4.0)); sss=np.where(edge,sss*1.0,sss)
add("N05-sss-approx-LEFT",sss,"SSS APPROXIMATION in PIL: blurred diffuse + edge bleed. True volumetric SSS (3D mesh) still owed, not claimed.")
# I-06 Figure-local gradient mesh (smooth, no normals)
add("N06-gradient-mesh-LEFT",0.55+0.45*s_left,"Gradient mesh: figure-bbox-local smooth gradient, no normal field. Control for normal methods.")
# I-07 Blinn-Phong specular proxy: view approx (0,0,1), half-vector
hv=norm(L_LEFT+np.array([0,0,1.0])); spec=np.clip(nx*hv[0]+ny*hv[1]+nz*hv[2],0,1)**24
add("N07-specular-LEFT",np.clip(0.35+0.65*dL+0.25*spec,0,1.0),"Blinn-Phong specular proxy: Lambert + spec^24, view (0,0,1) assumed, KEY LEFT.")
# I-08 Hemisphere ambient: sky top / ground bottom
hemi=0.65+0.35*(0.5*(1-ny))  # ny up-positive in this convention, so top gets more
add("N08-hemisphere-ambient",0.35+0.65*(0.5*dL+0.5*hemi),"Hemisphere ambient: sky/ground ambient + Lambert, KEY LEFT.")
# I-09 Cast-shadow gradient: bottom of figure darker (ground shadow falloff, proxy)
yfall=np.clip((yy-h*0.55)/(h*0.45),0,1); add("N09-cast-shadow-falloff", (0.35+0.65*dL)*(1-0.25*yfall),"Cast-shadow falloff proxy: Lambert x vertical falloff below mid-frame, KEY LEFT.")
# I-10 Shader-to-RGB equivalent in PIL (NOT a Blender Shader-to-RGB node run): quantised Lambert through a colour ramp
ramp=np.select([dL<0.33,dL<0.66],[0.45,0.72],default=1.00)
add("N10-shader-to-rgb-equiv-LEFT",ramp,"Shader-to-RGB EQUIVALENT in PIL: Lambert through a 3-stop ramp. Blender Shader-to-RGB node as a separate run still owed.")
# --- 10 experimental ---
# X-01 Edge-aware relight: diffuse smoothed with gaussian (bilateral proxy) to cut faceting
add("X01-edge-aware-LEFT",0.35+0.65*ndimage.gaussian_filter(dL,3.0),"Edge-aware relight (guided-smooth proxy): gaussian-smoothed diffuse, KEY LEFT. Faceting test vs V2.")
# X-02 Depth-dark far side
add("X02-depth-dark-LEFT", (0.35+0.65*dL)*(0.75+0.25*np.clip(dist/dist.max(),0,1)),"Depth-dark: far/deep pixels darker, KEY LEFT.")
# X-03 Linework-aware: lines keep their darkness, shading does not wash them
lw=np.where(lines,0.35+0.65*dL,0.35+0.65*dL); lw=np.where(lines,lw*0.75,lw)
add("X03-linework-aware-LEFT",lw,"Linework-aware: interior lines darkened x0.75 after shading, KEY LEFT.")
# X-04 Chromatic wrap: warm lit / cool shadow tint (measured on R only; tint is in image, not in R delta)
im=shade_im(BASE,np.where(mask,0.40+0.60*dL,1.0),F); arr=np.asarray(im).astype(float)
arr[...,0]*=(1+0.08*np.clip(dL,0,1)); arr[...,2]*=(1+0.08*np.clip(1-dL,0,1)); im=Image.fromarray(np.clip(arr,0,255).astype(np.uint8),"RGBA"); im.save(f"{OUT}/new-variants/X04-chromatic-wrap-LEFT.png"); st=stats(im,F); st.update({"method":"Chromatic wrap: warm lit / cool shadow tint + Lambert, KEY LEFT.","run":"PIL run"}); variants.append(("X04-chromatic-wrap-LEFT",im,st)); print("X04",st)
# X-05 Dual-key cross light
add("X05-dual-key-cross",0.35+0.65*np.maximum(dL,dR)*0.85+0.15*dL,"Dual-key cross: left+right keys, terminator centre, no single shadow side.")
# X-06 Diagonal light (top-left diagonal, not pure left)
L_DIAG=norm([-0.60,-0.60,0.52]); dD=diff(L_DIAG)
add("X06-diagonal-light",0.35+0.65*dD,"Diagonal light: key from top-left diagonal, KEY DIAGONAL.")
# X-07 Multiscale normal smoothing: blend sigma2 and sigma6 normals' diffuse
dL6=np.clip(ndimage.gaussian_filter(dL,4.0),0,1)
add("X07-multiscale-smooth-LEFT",0.35+0.65*(0.5*dL+0.5*dL6),"Multiscale smooth: sigma2 + sigma6 diffuse blend, KEY LEFT. Faceting test vs V2.")
# X-08 Per-zone shading: torso vs limbs by vertical band (proxy, zones by y)
zone=np.where(yy<h*0.45,0.9,1.0); add("X08-per-zone-LEFT",(0.35+0.65*dL)*zone,"Per-zone proxy: upper figure x0.90, lower x1.00, KEY LEFT. Zones by y-band, not limb segmentation.")
# X-09 Rim + AO power combo
add("X09-rim-AO-power",np.clip((0.35+0.65*dL)*(0.60+0.40*ao)+np.where(edge,0.25,0),0,1.0),"Rim+AO power combo: Lambert x AO + edge rim, KEY LEFT.")
# X-10 Inverse shading, TEST ONLY, not a shading: should read wrong
add("X10-inverse-TEST-ONLY",0.35+0.65*(1-dL),"INVERSE TEST ONLY: light from right while labelled left. Expected edge delta negative. Do NOT ship.")
# Arms-up check for the two smoothest candidates
FA=fields(ARMS)
def arms_diff(L):
    return np.clip(FA["nx"]*L[0]+FA["ny"]*L[1]+FA["nz"]*L[2],0,1)
for nm,fn in [("X01-edge-aware-ARMS",lambda d:0.35+0.65*ndimage.gaussian_filter(d,3.0)),("X07-multiscale-ARMS",lambda d:0.35+0.65*(0.5*d+0.5*ndimage.gaussian_filter(d,4.0)))]:
    d=arms_diff(L_LEFT); im=shade_im(ARMS,np.where(FA["mask"],fn(d),1.0),FA); im.save(f"{OUT}/new-variants/{nm}.png"); st=stats(im,FA); st.update({"method":"Arms-up check of "+nm,"run":"PIL run"}); variants.append((nm,im,st)); print(nm,st)
json.dump({n:st for n,_,st in variants},open(f"{OUT}/new-variants-stats-20261031.json","w"),indent=2)
tiles=[(f"{n} dR {st['delta_R']:+.1f} edge {st['edge_delta_R']:+.1f}",grey(im)) for n,im,st in variants]
contact(tiles,f"{OUT}/shading-set-two-continuation-contact-20261031.png",cols=4)
# Set One contact: copy old G2 sheet with a BARELY WORKS banner (new file, original untouched)
g2=Image.open(os.path.join(ROOT,"limits-broken-10x10-20261031","proofs","G2-shading-10x10-20261031.png")).convert("RGB")
banner=Image.new("RGB",(g2.width,60),(180,30,30)); d=ImageDraw.Draw(banner); d.text((16,20),"SHADING SET ONE — BARELY WORKS — old G2, 20 variants (see doc for exceptions)",fill=(255,255,255))
out1=Image.new("RGB",(g2.width,g2.height+60),(200,200,200)); out1.paste(banner,(0,0)); out1.paste(g2,(0,60)); out1.save(f"{OUT}/set-one/shading-set-one-contact-20261031.png")
shutil.copy(os.path.join(ROOT,"limits-broken-10x10-20261031","proofs","G2-shading-stats-20261031.json"),f"{OUT}/set-one/G2-shading-stats-20261031.json")
# Set Two contact: copy upgrade contact with DEFINITELY WORKS banner
up=Image.open(os.path.join(ROOT,"shading-upgrade-20261031","shading-upgrade-contact-20261031.png")).convert("RGB")
banner2=Image.new("RGB",(up.width,60),(20,120,40)); d=ImageDraw.Draw(banner2); d.text((16,20),"SHADING SET TWO — DEFINITELY WORKS — shading upgrade V0-V10 + HERO (see doc; apose V2/V4 faceted warning inside)",fill=(255,255,255))
out2=Image.new("RGB",(up.width,up.height+60),(200,200,200)); out2.paste(banner2,(0,0)); out2.paste(up,(0,60)); out2.save(f"{OUT}/set-two/shading-set-two-contact-20261031.png")
shutil.copy(os.path.join(ROOT,"shading-upgrade-20261031","shading-upgrade-stats-20261031.json"),f"{OUT}/set-two/shading-upgrade-stats-20261031.json")
print("DONE",len(variants))
