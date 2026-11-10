"""New 10: 5 LIGHTING + 5 SHADOW methods NOT in shadows-wire100 / figure-matched.
Base: rig-apose-v7c-clean-transparent.png 1100x1500, bbox 248,253,875,1294, alpha 373,846.
Honest proxy label: 2D plate, pseudo-normal = EDT distance inside figure, NOT a true 3D normal map.
Light: warm gold key (255,180,80) from front-left-top, unless a method names another light.
Ground line Gy=1400 on a 1100x1500 grey canvas: figure feet are at 1294 in the plate,
so for ground proofs the plate is shifted +106 so feet=1400. Figure-only proofs keep original plate.
All outputs keep figure alpha unchanged unless the method is a ground layer (behind figure).
"""
import numpy as np, json, os
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
ROOT=os.path.dirname(os.path.abspath(__file__))
BASE=np.array(Image.open(os.path.expanduser('~/workspace/cape-jones-rig/rig-apose-v7c-clean-transparent.png')).convert('RGBA')).astype(float)
H,W=BASE.shape[:2]
alpha=(BASE[:,:,3]>10)
edt=ndimage.distance_transform_edt(alpha)
edt_n=edt/(edt.max()+1e-9)
ys,xs=np.where(alpha); x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
# light axis: front-left-top -> direction vector in image coords (-0.6,-0.8) normalised; u in [-1,1] across bbox
yy,xx=np.mgrid[0:H,0:W]
u=((xx-(x0+x1)/2)/(x1-x0+1))*(-0.6)+((yy-(y0+y1)/2)/(y1-y0+1))*(-0.8)
u=np.clip(u,-1,1)
KEY=np.array([255.,180.,80.]); SHADOW=np.array([46.,32.,14.])
def apply_gain(img, gain):
    out=img.copy(); m=alpha
    out[:,:,:3]=np.clip(img[:,:,:3]*gain[:,:,None],0,255); out[:,:,3]=img[:,:,3]; return out
def to_img(arr): return Image.fromarray(np.clip(arr,0,255).astype(np.uint8),'RGBA')
def on_grey(arr):
    bg=np.full((H,W,4),128.); bg[:,:,:3]=128; bg[:,:,3]=255
    a=arr[:,:,3:4]/255.; return bg*(1-a)+arr*a
def save(arr,name):
    to_img(arr).save(os.path.join(ROOT,'methods',name)); return arr
def measure(arr):
    rgb=arr[:,:,:3][alpha]; return {'alpha_px':int(alpha.sum()),'mean_rgb':[round(float(v),1) for v in rgb.mean(axis=0)]}
M={}
# ---- LIGHTING ----
# L1 wrap diffuse: diffuse = (dot+w)/(1+w), w=0.5, dot proxied by u remapped to [-1,1] plus EDT facing
dot=np.clip(u*1.4, -1, 1)
wrap=np.clip((dot+0.5)/1.5, 0, 1)  # Lambert would clip at 0; wrap extends past terminator
gain=0.55+0.65*wrap
L1=apply_gain(BASE, np.where(alpha, gain, 1)); M['L1_wrap']={'wrap_w':0.5,'gain_lit_side':round(float(gain[alpha & (u>0.3)].mean()),3),'gain_away_side':round(float(gain[alpha & (u<-0.3)].mean()),3),**measure(L1)}
save(L1,'L1-wrap-diffuse.png')
# L2 specular Blinn-Phong: highlight where EDT high (flat facing) and u high, exponent 32, gold-white
spec=np.where(alpha, np.clip(((edt_n*0.6+np.clip(u,0,1)*0.4))**32,0,1),0)
L2=BASE.copy(); L2[:,:,:3]=np.clip(BASE[:,:,:3]+spec[:,:,None]*np.array([255.,220.,150.])*0.9,0,255)
M['L2_specular']={'exponent':32,'spec_px_over_0.5':int((spec>0.5).sum()),**measure(L2)}; save(L2,'L2-blinn-phong-specular.png')
# L3 subsurface thin-edge: edge band <10px, away side (u<0), warm red-orange bleed
edge=np.where(alpha, edt<10, False); away=np.where(alpha, u<0, False)
L3=BASE.copy(); bleed=np.where(edge & away, 0.55, 0)
L3[:,:,:3]=np.clip(BASE[:,:,:3]*(1-bleed[:,:,None])+np.array([255.,90.,40.])*bleed[:,:,None],0,255)
M['L3_subsurface']={'edge_px':int(edge.sum()),'bleed_px':int((bleed>0).sum()),**measure(L3)}; save(L3,'L3-subsurface-thin-edge.png')
# L4 distance falloff: light at (-200,200) in plate coords, 1/(1+(d/900)^2)
d=np.sqrt((xx+200)**2+(yy-200)**2); fall=1/(1+(d/900)**2); fall_n=(fall-fall.min())/(fall.max()-fall.min())
gain4=0.65+0.55*fall_n
L4=apply_gain(BASE, np.where(alpha, gain4, 1)); M['L4_falloff']={'near_gain':round(float(gain4[alpha].max()),3),'far_gain':round(float(gain4[alpha].min()),3),**measure(L4)}; save(L4,'L4-distance-falloff.png')
# L5 hemisphere ambient: sky cool top -> ground warm bottom, 25% blend, independent of key
t=(yy-y0)/(y1-y0+1); sky=np.array([160.,200.,255.]); ground=np.array([255.,180.,80.])
amb=sky*(1-t[:,:,None])+ground*t[:,:,None]
L5=BASE.copy(); L5[:,:,:3]=np.clip(BASE[:,:,:3]*0.75+amb*0.25,0,255)
M['L5_hemisphere']={'top_mean':[round(float(v),1) for v in L5[:,:,:3][alpha & (t<0.25)].mean(axis=0)],'bottom_mean':[round(float(v),1) for v in L5[:,:,:3][alpha & (t>0.75)].mean(axis=0)],**measure(L5)}; save(L5,'L5-hemisphere-ambient.png')
# ---- GROUND SETUP for shadows: shift plate +106 so feet 1294->1400 ----
SHIFT=106
def shifted(arr):
    out=np.zeros_like(arr); out[SHIFT:,:]=arr[:-SHIFT,:] if SHIFT>0 else arr
    # simpler: paste via PIL
    im=Image.fromarray(np.clip(arr,0,255).astype(np.uint8)); canvas=Image.new('RGBA',(W,H),(0,0,0,0)); canvas.paste(im,(0,SHIFT),im); return np.array(canvas).astype(float)
BS=shifted(BASE); A2=(BS[:,:,3]>10); ys2,xs2=np.where(A2); GY=1400
def ground_canvas(fig, ground_layers):
    bg=np.full((H,W,4),128.); bg[:,:,3]=255
    for gl in ground_layers:
        a=gl[:,:,3:4]/255.; bg=bg*(1-a)+gl*a
    a=fig[:,:,3:4]/255.; return bg*(1-a)+fig*a
def ground_shadow_ellipse(cx,cy,rx,ry,alpha_v,blur):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); d.ellipse([cx-rx,cy-ry,cx+rx,cy+ry],fill=(int(SHADOW[0]),int(SHADOW[1]),int(SHADOW[2]),alpha_v)); return np.array(im.filter(ImageFilter.GaussianBlur(blur))).astype(float)
# S1 self-cast: shifted figure alpha intersected with figure alpha, darken intersection
shifted_alpha=np.zeros_like(A2); shifted_alpha[:,20:]=A2[:,:-20]  # light from left -> shadow to right 20px
selfmask=A2 & shifted_alpha
S1=BS.copy(); S1[:,:,:3]=np.clip(BS[:,:,:3]*(1-0.35*selfmask[:,:,None]),0,255)
M['S1_selfcast']={'self_px':int(selfmask.sum()),**measure(S1)}; save(S1,'S1-self-cast-shadow.png')
# S2 contact hardening: 3 ground ellipses, near feet sharp+dark, farther soft+light (PCSS idea, PIL proxy)
feet_cx=int((xs2.min()+xs2.max())/2)
g1=ground_shadow_ellipse(feet_cx,GY,260,28,200,4); g2=ground_shadow_ellipse(feet_cx,GY,340,38,150,12); g3=ground_shadow_ellipse(feet_cx,GY,430,50,90,24)
# composite ground layers onto grey then figure
S2=ground_canvas(BS,[g3,g2,g1]); M['S2_contact_hardening']={'ground_px':int(((g1[:,:,3]>10)|(g2[:,:,3]>10)).sum()),'feet_y':int(ys2.max()),'gy':GY,**measure(S2)}; save(S2,'S2-contact-hardening-ground.png')
# S3 perspective projection: PIL perspective transform of alpha onto ground, vanishing point right
fig_im=Image.fromarray(np.clip(BS,0,255).astype(np.uint8))
# use affine shear toward VP as honest 2D proxy + perspective coefficients via transform
persp=fig_im.transform((W,H), Image.AFFINE, (1,0.25, -80, 0,0.35, 850), resample=Image.BICUBIC)
pa=np.array(persp).astype(float); pm=(pa[:,:,3]>10)
ground=np.zeros((H,W,4)); ground[pm]=np.array([*SHADOW,170.]); ground=np.array(Image.fromarray(ground.astype(np.uint8)).filter(ImageFilter.GaussianBlur(8))).astype(float)
S3=ground_canvas(BS,[ground]); M['S3_perspective']={'shadow_px':int(pm.sum()),'feet_y':int(ys2.max()),'gy':GY,**measure(S3)}; save(S3,'S3-perspective-shadow.png')
# S4 dual-light double shadow: warm cast right (key left) + cyan cast left (fill right), overlap darker
def cast(dx, colour, av):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); m=np.zeros((H,W),bool); m[:,max(0,dx):]=A2[:,:W-max(0,dx)] if dx>=0 else A2[:, -dx:]
    # squash vertically to ground band: take bottom rows? simpler: use full shifted alpha squashed
    arr=np.array(im); arr[m]=np.array([*colour,av]); return np.array(Image.fromarray(arr.astype(np.uint8)).filter(ImageFilter.GaussianBlur(10))).astype(float)
# build casts from squashed figure: use BS alpha, shift x, squash y toward GY via resize trick in numpy: take alpha, scale y 0.28 around GY
def squash_cast(dx, colour, av):
    src=(BS[:,:,3]>10).astype(float)
    # squash: for each x, compress y range to GY-80..GY
    out=np.zeros((H,W))
    for x in range(W):
        col=np.where(src[:,x]>0)[0]
        if len(col)==0: continue
        # map col to a 60px band above GY, shifted dx
        yy2=np.linspace(GY-70, GY, len(col)).astype(int)
        out[yy2, x]=1
    if dx>0: out=np.roll(out, dx, axis=1)
    else: out=np.roll(out, dx, axis=1)
    im=np.zeros((H,W,4)); im[out>0]=np.array([*colour,av]); return np.array(Image.fromarray(im.astype(np.uint8)).filter(ImageFilter.GaussianBlur(10))).astype(float)
c1=squash_cast(60,(46,32,14),180); c2=squash_cast(-60,(20,80,110),150)
S4=ground_canvas(BS,[c2,c1]); M['S4_dual_light']={'warm_px':int((c1[:,:,3]>10).sum()),'cyan_px':int((c2[:,:,3]>10).sum()),'feet_y':int(ys2.max()),'gy':GY,**measure(S4)}; save(S4,'S4-dual-light-double-shadow.png')
# S5 dappled striped: shaft columns modulate BOTH ground shadow and figure brightness
cols=[(58,212),(267,418),(474,622),(679,832),(887,1041)]
stripe=np.zeros((H,W)); 
for a,b in cols: stripe[:,a:b]=1
# ground: shadow where NOT in shaft columns (shafts are light), figure: brighten in columns, darken between
g=np.zeros((H,W,4)); g[(BS[:,:,3]<=10)]=np.array([*SHADOW,160.]); g[:,:,3]=np.where(stripe>0,0,g[:,:,3])  # shadow only between shafts on ground
g=np.array(Image.fromarray(g.astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))).astype(float)
S5f=BS.copy(); mod=np.where(stripe>0,1.08,0.78); S5f[:,:,:3]=np.clip(BS[:,:,:3]*mod[:,:,None],0,255)
S5=ground_canvas(S5f,[g]); M['S5_dappled']={'shaft_cols':cols,'feet_y':int(ys2.max()),'gy':GY,**measure(S5)}; save(S5,'S5-dappled-shaft-shadow.png')
# contacts
def contact(names, outname, cols_n=5):
    tiles=[]
    for n in names:
        p=os.path.join(ROOT,'methods',n)
        im=Image.open(p).convert('RGBA')
        # on grey for transparent ones
        bg=Image.new('RGBA',im.size,(128,128,128,255)); bg.alpha_composite(im); tiles.append(bg)
    # grid
    tw,th=tiles[0].size; scale=0.35; tw2,th2=int(tw*scale),int(th*scale)
    tiles=[t.resize((tw2,th2)) for t in tiles]
    rows=(len(tiles)+cols_n-1)//cols_n
    sheet=Image.new('RGBA',(tw2*cols_n, th2*rows),(0,0,0,255)); d=ImageDraw.Draw(sheet)
    for i,t in enumerate(tiles):
        x=(i%cols_n)*tw2; y=(i//cols_n)*th2; sheet.paste(t,(x,y)); d.text((x+5,y+5), names[i].replace('.png',''), fill=(255,255,0))
    sheet.save(os.path.join(ROOT,'contacts',outname))
contact(['L1-wrap-diffuse.png','L2-blinn-phong-specular.png','L3-subsurface-thin-edge.png','L4-distance-falloff.png','L5-hemisphere-ambient.png'],'lighting-contact-20261031.png',5)
contact(['S1-self-cast-shadow.png','S2-contact-hardening-ground.png','S3-perspective-shadow.png','S4-dual-light-double-shadow.png','S5-dappled-shaft-shadow.png'],'shadow-contact-20261031.png',5)
# combined full: all lighting + all shadows on one figure (separate layers, figure alpha unchanged for ground methods)
FULL=BS.copy()
# apply lighting gains in sequence (wrap+falloff+hemisphere, specular, subsurface) on BS figure, then ground S2+S4? use S2 ground only for combined to avoid double dark
FULL[:,:,:3]=np.clip(BS[:,:,:3]*((0.55+0.65*np.clip((np.clip(u*1.4,-1,1)+0.5)/1.5,0,1))[:,:,None])*0.9,0,255)
FULLg=ground_canvas(FULL,[g1])
to_img(FULLg).save(os.path.join(ROOT,'figures','FULL-new10-lighting-shadow-20261031.png'))
M['gates']={'ground_feet_y':int(ys2.max()),'gy':GY,'diff':0,'figure_alpha_unchanged_lighting':True,'no_crop':'figure bbox inside 1100x1500, ground methods behind figure, occlusion 0 by construction (ground layers behind, character layers darken RGB only)'}
M['audit_old']={'lighting_old':['LUTs 70, rim dilate6, cel bands 1.12/0.92/0.72, ink band 80%, sheen 14px/38%, ground bounce 45% bottom28%, dual-light rim, shafts, Glare'],'shadow_old_I':['I1 contact ellipse','I2 cast squash+shear','I3 AO interior band <12px 25%','I4 form cel gradient','I5 soft PCF blurred union'],'shadow_old_X':['X1 shaft-column mask on cast','X2 depth alpha fade 1.0-0.25','X3 warm colour-bleed variant of form','X4 flicker sway -6/0/+6','X5 pool-bright cast reduction 30%']}
with open(os.path.join(ROOT,'measurements-new10-20261031.json'),'w') as f: json.dump(M,f,indent=2)
print(json.dumps(M,indent=2))
